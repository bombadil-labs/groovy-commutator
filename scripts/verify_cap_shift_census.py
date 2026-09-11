#!/usr/bin/env python3
"""Complement-conjugation shift census over all local caps (protocol frozen 2026-09-11).

Correction 2026-09-11 after retrospective review (PR #82): X5 now implements the
declared predicate (a half-decided cell must have existing radius 4 or h = 2); a
half-decided cell with existing radius a implies shift >= 5-a and refutes shift <= h+1
when 5-a > h+1, and is reported as such. Source windows have width
2*max(h+1+R, h+2)+1. The saved census has no half-decided cells, so these are
prospective scoring fixes.

All 256 rules, kinds K and O, depths h<=2, radii R<=4: minimum passing cap radius for
each rule and its complement-conjugate, the shift on decided cells, reflection control,
reproduction of the saved R<=2 census, and the predictions X1-X5 of the protocol.
Evaluator: census tables() plus the vectorized functional test used by the extension.
"""
from __future__ import annotations
import hashlib, importlib.util, json, pathlib
from collections import Counter
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[1]
CENSUS = ROOT / 'results/local_correction_caps_20260910.json'
OUT = ROOT / 'results/cap_shift_census_20260911.json'
R_MAX = 4
spec = importlib.util.spec_from_file_location('caps', ROOT / 'scripts/verify_local_correction_caps.py')
caps = importlib.util.module_from_spec(spec); spec.loader.exec_module(caps)

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def conj(r):
    f = [(r >> i) & 1 for i in range(8)]; return sum((1 - f[7 - i]) << i for i in range(8))
def mirror(r):
    f = [(r >> i) & 1 for i in range(8)]; out = 0
    for i in range(8):
        l, m, rr = (i >> 2) & 1, (i >> 1) & 1, i & 1
        out |= f[4 * rr + 2 * m + l] << i
    return out

def cap_exists(ts, h, radius):
    m = max(h + 1 + radius, h + 2); width = 2 * m + 1
    words = np.arange(1 << width, dtype=np.int64); patch = np.zeros_like(words)
    for j in range(h + 1):
        table = np.asarray(ts[j], dtype=np.int64); mask = (1 << (2 * j + 3)) - 1
        for x in range(-radius, radius + 1):
            patch = (patch << 1) | table[(words >> (m - x - j - 1)) & mask]
    target = np.asarray(ts[h + 1], dtype=np.int64)[(words >> (m - h - 2)) & ((1 << (2 * h + 5)) - 1)]
    order = np.argsort(patch, kind='stable'); p, t = patch[order], target[order]
    return not np.any((p[1:] == p[:-1]) & (t[1:] != t[:-1]))

def main():
    census = json.loads(CENSUS.read_text())
    saved = {(e['rule'], e['kind'], e['h'], e['R']): e['pass'] for e in census['records']}
    passes = {}; x1 = []
    for r in range(256):
        ts = caps.tables(r)
        for kind in ('K', 'O'):
            for h in range(3):
                row = [cap_exists(ts[kind], h, R) for R in range(R_MAX + 1)]
                passes[(r, kind, h)] = row
                for R in range(3):
                    if row[R] != saved[(r, kind, h, R)]: x1.append({'rule': r, 'kind': kind, 'h': h, 'R': R})
    mpr = {k: next((R for R, ok in enumerate(v) if ok), None) for k, v in passes.items()}
    x2 = [k for k in mpr if mpr[k] != mpr[(mirror(k[0]),) + k[1:]]]
    shifts = {'K': {h: Counter() for h in range(3)}, 'O': {h: Counter() for h in range(3)}}
    x3, x4, x4p, x5, half, undecided = [], [], [], [], [], []
    for (r, kind, h), a in mpr.items():
        b = mpr[(conj(r), kind, h)]
        if a is None and b is None: undecided.append({'rule': r, 'kind': kind, 'h': h}); continue
        if a is None or b is None:
            existing = a if a is not None else b
            cell = {'rule': r, 'conj': conj(r), 'kind': kind, 'h': h, 'existing_radius': existing}
            cell['shift_lower_bound'] = R_MAX + 1 - existing
            cell['refutes_shift_le_h_plus_1'] = (R_MAX + 1 - existing) > h + 1
            half.append(cell)
            if not (existing == R_MAX or h == 2): x5.append(cell)   # declared predicate
            continue
        s = abs(a - b); shifts[kind][h][s] += 1
        cell = {'rule': r, 'conj': conj(r), 'kind': kind, 'h': h, 'mpr_rule': a, 'mpr_conj': b, 'shift': s}
        if kind == 'K' and s > h + 1: x3.append(cell)
        if kind == 'O':
            if s > h + 1: x4.append(cell)
            if s != 0: x4p.append(cell)
    o_table_invariant = all(passes[(r, 'O', h)] == passes[(conj(r), 'O', h)] for r in range(256) for h in range(3))
    report = {'protocol': 'cap-shift-census-20260911', 'schema': 1, 'R_max': R_MAX,
              'source_hashes': {'script': sha(pathlib.Path(__file__)), 'local_correction_caps': sha(CENSUS)},
              'mpr': [{'rule': r, 'K': [mpr[(r, 'K', h)] for h in range(3)], 'O': [mpr[(r, 'O', h)] for h in range(3)]} for r in range(256)],
              'shift_histograms': {kind: {h: dict(sorted(c.items())) for h, c in hs.items()} for kind, hs in shifts.items()},
              'source_window_width': '2*max(h+1+R, h+2)+1',
              'half_decided': half, 'undecided': undecided,
              'half_decided_refuting_shift_bound': [c for c in half if c['refutes_shift_le_h_plus_1']],
              'X1_reproduction_violations': x1, 'X2_reflection_violations': [list(k) for k in x2],
              'X3_K_shift_violations': x3, 'X4_O_shift_violations': x4, 'X4prime_O_nonzero_shift': x4p,
              'X4prime_O_pass_table_complement_invariant': o_table_invariant, 'X5_half_decided_violations': x5,
              'summary': {'X1': not x1, 'X2': not x2, 'X3': not x3, 'X4': not x4, 'X4prime': (not x4p) and o_table_invariant, 'X5': not x5,
                          'half_decided_cells': len(half), 'undecided_cells': len(undecided)}}
    OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False) + '\n')
    print(json.dumps(report['summary'])); print(json.dumps(report['shift_histograms'])); print('written', OUT.relative_to(ROOT))

if __name__ == '__main__':
    main()
