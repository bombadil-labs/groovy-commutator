#!/usr/bin/env python3
"""Higher-block recoding audit (protocol frozen 2026-09-11).

T_beta: S'_i = (S_i, S_{i+1}). Audits cap radii (K and O, h<=2, R<=4) in block
coordinates against the original, componentwise covariance of D and G on rings,
derivative-closure preservation, and closure of the Research026 static observer
family under input complement and reversal with 12-ring block alignment.
Evaluator: census tables() with asymmetric source windows for block patches.
"""
from __future__ import annotations
import hashlib, importlib.util, itertools, json, pathlib
from collections import Counter
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[1]
CENSUS = ROOT / 'results/local_correction_caps_20260910.json'
SHIFT = ROOT / 'results/cap_shift_census_20260911.json'
OUT = ROOT / 'results/higher_block_recoding_20260911.json'
R_MAX = 4
spec = importlib.util.spec_from_file_location('caps', ROOT / 'scripts/verify_local_correction_caps.py')
caps = importlib.util.module_from_spec(spec); spec.loader.exec_module(caps)

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def cap_exists_cells(ts, h, left, right):
    """cap exists when the target A_{h+1} at the cells `target_cells` (relative to
    center) is a function of A_j (j<=h) on cells center-left .. center+right."""
    Lext = max(h + 1 + left, h + 2); Rext = max(h + 2 + right, h + 3)  # target at cells 0 and +1
    width = Lext + Rext + 1
    words = np.arange(1 << width, dtype=np.int64); patch = np.zeros_like(words)
    for j in range(h + 1):
        table = np.asarray(ts[j], dtype=np.int64); mask = (1 << (2 * j + 3)) - 1
        for x in range(-left, right + 1):
            shift = width - (Lext + x + j + 1) - 1
            patch = (patch << 1) | table[(words >> shift) & mask]
    tt = np.asarray(ts[h + 1], dtype=np.int64); tmask = (1 << (2 * h + 5)) - 1
    t0 = tt[(words >> (width - (Lext + h + 2) - 1)) & tmask]
    t1 = tt[(words >> (width - (Lext + 1 + h + 2) - 1)) & tmask]
    target = 2 * t0 + t1
    order = np.argsort(patch, kind='stable'); p, t = patch[order], target[order]
    return not np.any((p[1:] == p[:-1]) & (t[1:] != t[:-1]))

def block_mpr(ts, h):
    for R in range(R_MAX + 1):
        if cap_exists_cells(ts, h, R, R + 1): return R
    return None

def all_states(n):
    k = np.arange(2 ** n, dtype=np.int64); return ((k[:, None] >> (n - 1 - np.arange(n))) & 1).astype(np.uint8)
def lut(r): return np.array([(r >> i) & 1 for i in range(8)], dtype=np.uint8)
def step(S, r):
    t = lut(r); return t[4 * np.roll(S, 1, axis=1) + 2 * S + np.roll(S, -1, axis=1)]
def beta(S): return np.stack([S, np.roll(S, -1, axis=1)], axis=2)          # (k, n, 2)
def step_block(B, r):
    """native law on 4-symbol configurations: read first components, output pair."""
    s = B[..., 0]; f = step(s, r); return np.stack([f, np.roll(f, -1, axis=1)], axis=2)
def D_block(B, r): return B ^ step_block(B, r)
def G_block(B, r): return D_block(step_block(B, r), r) ^ step_block(D_block(B, r), r)
def D(S, r): return S ^ step(S, r)
def G(S, r): return D(step(S, r), r) ^ step(D(S, r), r)

def family_closure():
    out = {}
    for b in (2, 3):
        m = 1 << b; funcs = set(range(1, (1 << m) - 1))          # nonconstant
        def compl(h):  # h o (input complement)
            return sum(((h >> ((m - 1) - code)) & 1) << code for code in range(m))
        def rev(h):    # h o (input reversal within block)
            def r(code): return int(''.join(reversed(format(code, f'0{b}b'))), 2)
            return sum(((h >> r(code)) & 1) << code for code in range(m))
        out[b] = {'closed_under_input_complement': all(compl(h) in funcs for h in funcs),
                  'closed_under_input_reversal': all(rev(h) in funcs for h in funcs),
                  'output_complement_pairs_preserved': all((m and ((1 << m) - 1 - compl(h)) == compl((1 << m) - 1 - h)) for h in funcs),
                  'ring12_block_alignment_preserved_by_reflection': (12 % b == 0)}
    return out

def main():
    shift = json.loads(SHIFT.read_text()); mpr0 = {m['rule']: m for m in shift['mpr']}
    rows = []; b1 = []; dist = {'K': {h: Counter() for h in range(3)}, 'O': {h: Counter() for h in range(3)}}
    for r in range(256):
        ts = caps.tables(r); rec = {'rule': r, 'K': [], 'O': []}
        for kind in ('K', 'O'):
            for h in range(3):
                mb = block_mpr(ts[kind], h); m0 = mpr0[r][kind][h]; rec[kind].append(mb)
                if m0 is not None and mb is not None:
                    if not (m0 - 1 <= mb <= m0): b1.append({'rule': r, 'kind': kind, 'h': h, 'mpr': m0, 'mpr_block': mb})
                    dist[kind][h][m0 - mb] += 1
                elif m0 is not None and mb is None: b1.append({'rule': r, 'kind': kind, 'h': h, 'mpr': m0, 'mpr_block': None, 'why': 'mpr<=4 but no block cap within budget'})
                elif m0 is None and mb is not None and mb <= 3: b1.append({'rule': r, 'kind': kind, 'h': h, 'mpr': None, 'mpr_block': mb, 'why': 'block cap <=3 but no original cap within budget'})
        rows.append(rec)
    b2 = {}
    for n in (8, 10):
        S = all_states(n); B = beta(S); bad = []
        for r in range(256):
            if not (np.array_equal(D_block(B, r), beta(D(S, r))) and np.array_equal(G_block(B, r), beta(G(S, r)))): bad.append(r)
        b2[n] = bad
    b3 = {}
    for n in (8, 10):
        S = all_states(n); B = beta(S); bad = []
        for r in range(256):
            def closed(d, dn):
                keys = {}
                for a, b in zip(map(bytes, d.reshape(len(d), -1)), map(bytes, dn.reshape(len(dn), -1))):
                    if keys.setdefault(a, b) != b: return False
                return True
            c0 = closed(D(S, r), D(step(S, r), r)); cb = closed(D_block(B, r), D_block(step_block(B, r), r))
            if c0 != cb: bad.append(r)
        b3[n] = bad
    b4 = family_closure()
    report = {'protocol': 'higher-block-recoding-20260911', 'schema': 1, 'R_max': R_MAX,
              'source_hashes': {'script': sha(pathlib.Path(__file__)), 'local_correction_caps': sha(CENSUS), 'cap_shift_census': sha(SHIFT)},
              'costs': {'forward_radius': 1, 'inverse_radius': 0, 'alphabet': '2 -> 4', 'family': 'full shift -> consistent-pair subshift', 'information': 0},
              'mpr_block': rows, 'shift_distribution_mpr_minus_block': {k: {h: dict(sorted(c.items())) for h, c in v.items()} for k, v in dist.items()},
              'B1_violations': b1, 'B2_covariance_violations_by_ring': b2, 'B3_closure_violations_by_ring': b3, 'B4_family_closure': b4,
              'summary': {'B1': not b1, 'B2': all(not v for v in b2.values()), 'B3': all(not v for v in b3.values()),
                          'B4': all(all(v.values()) for v in b4.values())}}
    OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False) + '\n')
    print(json.dumps(report['summary'])); print(json.dumps(report['shift_distribution_mpr_minus_block'])); print(json.dumps(b4)); print('written', OUT.relative_to(ROOT))

if __name__ == '__main__':
    main()
