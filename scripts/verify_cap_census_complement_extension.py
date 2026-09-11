#!/usr/bin/env python3
"""Local-cap census extension under complement conjugation (protocol frozen 2026-09-11).

Correction 2026-09-11 after retrospective review (PR #81): the selected domain is the
22 entries flagged by the first audit's checker (4 genuine h=0 bound violations plus
18 right-censored comparisons), not "22 cells whose minima differ". Source windows
have width 2*max(h+1+R, h+2)+1, as the census evaluator defines them.

Tests the corrected radius bound mpr(conj r, h) <= max(mpr(r, h), h+1) + h(h+1)/2 on
the 22 (rule, h) K-coordinate cells where the R<=2 census pass/fail differs between a
rule and its complement-conjugate, at radii R = 0..6. Reuses tables() from the census
evaluator; a cap of radius R exists iff patch -> target is functional over every source
window of width 2(h+1+R)+1 (no torus), exactly as in the census.
"""
from __future__ import annotations
import hashlib, importlib.util, json, pathlib
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[1]
CENSUS = ROOT / 'results/local_correction_caps_20260910.json'
AUDIT = ROOT / 'results/representation_invariants_20260910.json'
OUT = ROOT / 'results/cap_census_complement_extension_20260911.json'
R_MAX = 6
spec = importlib.util.spec_from_file_location('caps', ROOT / 'scripts/verify_local_correction_caps.py')
caps = importlib.util.module_from_spec(spec); spec.loader.exec_module(caps)

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def conj(r):
    f = [(r >> i) & 1 for i in range(8)]; return sum((1 - f[7 - i]) << i for i in range(8))

def cap_exists(ts, h, radius):
    """K-coordinate cap of given radius at depth h, over all source windows (vectorized)."""
    m = max(h + 1 + radius, h + 2); width = 2 * m + 1
    words = np.arange(1 << width, dtype=np.int64)
    patch = np.zeros_like(words)
    for j in range(h + 1):
        table = np.asarray(ts[j], dtype=np.int64); mask = (1 << (2 * j + 3)) - 1
        for x in range(-radius, radius + 1):
            local = (words >> (m - x - j - 1)) & mask
            patch = (patch << 1) | table[local]
    target_table = np.asarray(ts[h + 1], dtype=np.int64)
    target = target_table[(words >> (m - h - 2)) & ((1 << (2 * h + 5)) - 1)]
    order = np.argsort(patch, kind='stable'); p, t = patch[order], target[order]
    same = p[1:] == p[:-1]
    return not np.any(same & (t[1:] != t[:-1]))

def min_radius(ts, h):
    for radius in range(R_MAX + 1):
        if cap_exists(ts, h, radius): return radius
    return None

def main():
    census = json.loads(CENSUS.read_text()); audit = json.loads(AUDIT.read_text())
    viol = audit['predictions']['P5_local_cap_census']['complement_K_radius_bound_violations']
    cells = sorted({(v['rule'], v['h']) for v in viol})
    saved = {(e['rule'], e['h'], e['R']): e['pass'] for e in census['records'] if e['kind'] == 'K'}
    rows, x1, x2, x3, x4 = [], [], [], [], []
    cache = {}
    for rule, h in cells:
        for r in (rule, conj(rule)):
            if (r, h) in cache: continue
            ts = caps.tables(r)['K']
            passes = {R: cap_exists(ts, h, R) for R in range(R_MAX + 1)}
            for R in range(3):
                if passes[R] != saved[(r, h, R)]: x1.append({'rule': r, 'h': h, 'R': R, 'recomputed': passes[R], 'saved': saved[(r, h, R)]})
            cache[(r, h)] = next((R for R in range(R_MAX + 1) if passes[R]), None)
        a, b = cache[(rule, h)], cache[(conj(rule), h)]
        bound = lambda x: None if x is None else max(x, h + 1) + h * (h + 1) // 2
        row = {'rule': rule, 'conj': conj(rule), 'h': h, 'mpr_rule': a, 'mpr_conj': b,
               'bound_from_rule': bound(a), 'bound_from_conj': bound(b),
               'shift': None if a is None or b is None else abs(a - b)}
        # 2026-09-11: classify the flagged entry and test the ORIGINAL <=h bound after resolution
        orig = next(v for v in viol if v['rule'] == rule and v['h'] == h)
        row['flag_kind'] = 'censored' if (orig['mpr_r'] is None or orig['mpr_conj'] is None) else 'genuine_h0_violation'
        row['original_le_h_bound_holds_after_resolution'] = None if a is None or b is None else abs(a - b) <= h
        rows.append(row)
        if a is None or b is None: x2.append(row)
        else:
            if b > bound(a) or a > bound(b): x3.append(row)
            if abs(a - b) > h + 1: x4.append(row)
    composition = {'genuine_h0_violation': sum(r['flag_kind'] == 'genuine_h0_violation' for r in rows), 'censored': sum(r['flag_kind'] == 'censored' for r in rows)}
    orig_bound = {'holds': sum(bool(r['original_le_h_bound_holds_after_resolution']) for r in rows), 'fails': sum(r['original_le_h_bound_holds_after_resolution'] is False for r in rows)}
    report = {'protocol': 'cap-census-complement-extension-20260911', 'schema': 1, 'R_max': R_MAX,
              'source_window_width': '2*max(h+1+R, h+2)+1 (census convention; the frozen text wrote 2(h+1+R)+1, which differs only at R=0)',
              'selected_domain_composition': composition, 'original_le_h_bound_after_resolution': orig_bound,
              'source_hashes': {'script': sha(pathlib.Path(__file__)), 'local_correction_caps': sha(CENSUS), 'representation_invariants_audit': sha(AUDIT)},
              'cells': rows, 'cell_count': len(cells),
              'X1_reproduction_violations': x1, 'X2_existence_violations': x2, 'X3_bound_violations': x3, 'X4_shift_le_h_plus_1_violations': x4,
              'summary': {'X1': not x1, 'X2': not x2, 'X3': not x3, 'X4': not x4}}
    OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False) + '\n')
    print(json.dumps(report['summary'])); print(json.dumps(rows, indent=0)); print('written', OUT.relative_to(ROOT))

if __name__ == '__main__':
    main()
