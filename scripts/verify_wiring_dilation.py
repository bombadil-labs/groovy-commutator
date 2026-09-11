#!/usr/bin/env python3
"""Wiring-dilation audit (protocol frozen 2026-09-11, gate-1 sign-off by Codex at
aa312e6 before this implementation; see the protocol's Section 5).

Dilated automaton F_r^(d)(S)_i = f_r(S_{i-d}, S_i, S_{i+d}) on the n-ring, d in
{2, 3}, rings 6..12, observations psi in {232, 4}. Two transports: whole-contract
(rule and observation dilated) and partial (rule dilated, observation standard).
Per census: C, K, Z, X, h_* (as in the tenth unit) and the result-1 commutator
classification of the realized state map (zero, one, varying).

W1  gcd(d, n) = 1, whole-contract: census identical to the standard census at
    ring n (computed fresh, and cross-checked against the eighth and ninth
    units' result files); G classification identical for all 256 rules.
W2  d = 2, odd n, partial: (a) closed set differs from the standard closed set;
    (b) psi not in K; {0, 170, 204, 240} in K; consistency C/K/Z/X/h of the
    partial census equal the standard census under the observation dilated by
    e = 2^{-1} mod n. (a) and (b) scored separately.
W3  d = 2, even n, whole-contract: census equals the n/2-ring standard census
    (C, K, Z, X, h_*), including depth.
W4  d = 3: coprime rings as W1; rings 6, 9, 12 as W3 with n/3.
W5  G classification under partial dilation equals that under whole-contract
    dilation (same map); preserved for coprime (d, n); reported on split rings.
"""
from __future__ import annotations
import hashlib, json, math, pathlib
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[1]
MAJORITY = ROOT / 'results/block_majority_20260911.json'
ISOLATED = ROOT / 'results/isolated_cell_20260911.json'
OUT = ROOT / 'results/wiring_dilation_20260911.json'
OBS = (232, 4); DIL = (2, 3); RINGS = (6, 7, 8, 9, 10, 11, 12)

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def all_states(n):
    k = np.arange(2 ** n, dtype=np.int64); return ((k[:, None] >> (n - 1 - np.arange(n))) & 1).astype(np.uint8)
def lut(r): return np.array([(r >> i) & 1 for i in range(8)], dtype=np.uint8)
def step(S, r, d=1):
    t = lut(r); return t[4 * np.roll(S, d, axis=1) + 2 * S + np.roll(S, -d, axis=1)]
def ints(S): return (S.astype(np.int64) << (S.shape[1] - 1 - np.arange(S.shape[1]))).sum(axis=1)
def relabel(keys): _, inv = np.unique(keys, return_inverse=True); return inv
def jsonable(o):
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.floating): return float(o)
    raise TypeError(type(o))

def depth(fiber, nxt, N):
    cls = fiber; h = 0
    while True:
        new = relabel(cls * N + cls[nxt])
        if len(np.unique(new)) == len(np.unique(cls)): break
        cls = new; h += 1
    return h

def census(n, psi, d_rule, d_obs):
    S = all_states(n); N = len(S); Y = step(S, psi, d_obs); y = ints(Y); fiber = relabel(y)
    image_ints = np.unique(y); image_states = S[image_ints]
    first = {}
    for idx in range(N):
        if y[idx] not in first: first[y[idx]] = idx
    reps = np.array([first[yi] for yi in image_ints])
    closed = []; commute = []; collapse = []; h = {}; gcls = {}
    for r in range(256):
        FS = step(S, r, d_rule); nxt = ints(FS); succ = fiber[nxt]
        order = np.argsort(fiber, kind='stable'); f, s = fiber[order], succ[order]
        is_closed = not np.any((f[1:] == f[:-1]) & (s[1:] != s[:-1]))
        if is_closed: closed.append(r)
        if np.array_equal(step(FS, psi, d_obs), step(Y, r, d_rule)): commute.append(r)
        h[str(r)] = depth(fiber, nxt, N)
        if is_closed:
            B = step(step(S[reps], r, d_rule), psi, d_obs)
            if len(np.unique(ints(B))) == 1: collapse.append(r)
        D = S ^ FS; G = (FS ^ step(FS, r, d_rule)) ^ step(D, r, d_rule)     # D(F S) = F S ^ F(F S); F(D S)
        u = np.unique(ints(G)); gcls[str(r)] = ('zero' if u[0] == 0 else 'one') if len(u) == 1 and u[0] in (0, 2 ** n - 1) else ('const' if len(u) == 1 else 'varying')
    residual = sorted(set(closed) - set(commute) - set(collapse))
    return {'closed': closed, 'commuters': commute, 'collapse': collapse, 'residual': residual, 'h_star': h, 'g_class': gcls}

KEYS = ('closed', 'commuters', 'collapse', 'residual', 'h_star')
def same(a, b, keys=KEYS): return all(a[k] == b[k] for k in keys)

def main():
    maj = json.loads(MAJORITY.read_text()); iso = json.loads(ISOLATED.read_text())
    ref = {232: {'C': maj['predictions']['M3_closed_vs_commuters']['C_by_ring'], 'K': maj['predictions']['M3_closed_vs_commuters']['K_by_ring'], 'h': maj['h_star']},
           4: {'C': iso['predictions']['N3_commute_or_collapse']['C_by_ring'], 'K': iso['predictions']['N3_commute_or_collapse']['K_by_ring'], 'h': iso['h_star']['4']}}
    std = {psi: {n: census(n, psi, 1, 1) for n in RINGS} for psi in OBS}                      # standard census, fresh
    small = {psi: {m: census(m, psi, 1, 1) for m in (2, 3, 4, 5)} for psi in OBS}             # small rings for W3/W4
    whole = {d: {psi: {n: census(n, psi, d, d) for n in RINGS} for psi in OBS} for d in DIL}
    partial = {d: {psi: {n: census(n, psi, d, 1) for n in RINGS} for psi in OBS} for d in DIL}
    P = {}
    # reference consistency (control): fresh standard census vs the earlier units' files
    refcheck = {str(psi): {str(n): std[psi][n]['closed'] == ref[psi]['C'][str(n)] and std[psi][n]['commuters'] == ref[psi]['K'][str(n)] and std[psi][n]['h_star'] == ref[psi]['h'][str(n)] for n in RINGS} for psi in OBS}
    P['reference_consistency'] = {'by_ring': refcheck, 'pass': all(v for d_ in refcheck.values() for v in d_.values())}
    def coprime(d, n): return math.gcd(d, n) == 1
    w1 = {}
    for d in DIL:
        for psi in OBS:
            for n in RINGS:
                if not coprime(d, n): continue
                w1[f'{d}/{psi}/{n}'] = {'census_equal': same(whole[d][psi][n], std[psi][n]), 'g_class_equal': whole[d][psi][n]['g_class'] == std[psi][n]['g_class']}
    P['W1_whole_contract_conjugacy'] = {'cells': w1, 'pass': all(v['census_equal'] and v['g_class_equal'] for v in w1.values())}
    w2 = {}
    for psi in OBS:
        for n in (7, 9, 11):
            e = pow(2, -1, n); part = partial[2][psi][n]; inv = census(n, psi, 1, e)
            w2[f'{psi}/{n}'] = {'closed_set_differs': part['closed'] != std[psi][n]['closed'], 'psi_not_in_K': psi not in part['commuters'],
                                'named_in_K': all(r in part['commuters'] for r in (0, 170, 204, 240)), 'inverse_offset_e': e,
                                'consistency_with_inverse_offset_observation': same(part, inv),
                                'closed_partial': part['closed'], 'commuters_partial': part['commuters'], 'residual_partial': part['residual'],
                                'max_h_partial': max(part['h_star'].values()), 'max_h_standard': max(std[psi][n]['h_star'].values()),
                                'depth_table_differs': part['h_star'] != std[psi][n]['h_star']}
    P['W2_partial_dilation_changes'] = {'cells': w2, 'pass_a_closed_set_differs': all(v['closed_set_differs'] for v in w2.values()),
                                        'pass_b_psi_leaves_K': all(v['psi_not_in_K'] for v in w2.values()), 'named_stay_in_K': all(v['named_in_K'] for v in w2.values()),
                                        'consistency_control': all(v['consistency_with_inverse_offset_observation'] for v in w2.values())}
    P['W2_partial_dilation_changes']['pass'] = all(P['W2_partial_dilation_changes'][k] for k in ('pass_a_closed_set_differs', 'pass_b_psi_leaves_K', 'named_stay_in_K', 'consistency_control'))
    def split_cell(d, psi, n):
        m = n // d; small_c = small[psi][m] if m in small[psi] else std[psi][m]
        return {'ring_size': m, 'census_equal_to_small_ring': same(whole[d][psi][n], small_c), 'closed_small_ring': small_c['closed'],
                'max_h': max(whole[d][psi][n]['h_star'].values()), 'g_class_equal_to_small_ring': whole[d][psi][n]['g_class'] == small_c['g_class']}
    w3 = {f'{psi}/{n}': split_cell(2, psi, n) for psi in OBS for n in (6, 8, 10, 12)}
    P['W3_even_rings_split'] = {'cells': w3, 'pass': all(v['census_equal_to_small_ring'] for v in w3.values())}
    w4s = {f'{psi}/{n}': split_cell(3, psi, n) for psi in OBS for n in (6, 9, 12)}
    w4c = {k: v for k, v in w1.items() if k.startswith('3/')}
    P['W4_dilation_by_three'] = {'coprime_cells': w4c, 'split_cells': w4s, 'pass': all(v['census_equal'] and v['g_class_equal'] for v in w4c.values()) and all(v['census_equal_to_small_ring'] for v in w4s.values())}
    w5 = {f'{d}/{psi}/{n}': {'partial_equals_whole': partial[d][psi][n]['g_class'] == whole[d][psi][n]['g_class'],
                             'equals_standard': whole[d][psi][n]['g_class'] == std[psi][n]['g_class'], 'coprime': coprime(d, n),
                             'counts': {c: sum(1 for v in whole[d][psi][n]['g_class'].values() if v == c) for c in ('zero', 'one', 'const', 'varying')}}
          for d in DIL for psi in OBS for n in RINGS}
    P['W5_commutator_classification'] = {'cells': w5, 'partial_equals_whole_all': all(v['partial_equals_whole'] for v in w5.values()),
                                         'standard_counts': {str(n): {c: sum(1 for v in std[232][n]['g_class'].values() if v == c) for c in ('zero', 'one', 'const', 'varying')} for n in RINGS}}
    trim = lambda c: {k: c[k] for k in ('closed', 'commuters', 'collapse', 'residual')} | {'max_h': max(c['h_star'].values())}
    report = {'protocol': 'wiring-dilation-20260911', 'schema': 1, 'observations': list(OBS), 'dilations': list(DIL), 'rings': list(RINGS),
              'source_hashes': {'script': sha(pathlib.Path(__file__)), 'block_majority_result': sha(MAJORITY), 'isolated_cell_result': sha(ISOLATED)},
              'standard': {str(psi): {str(n): trim(std[psi][n]) for n in RINGS} for psi in OBS},
              'small_rings': {str(psi): {str(m): trim(small[psi][m]) for m in small[psi]} for psi in OBS},
              'whole_contract': {str(d): {str(psi): {str(n): trim(whole[d][psi][n]) for n in RINGS} for psi in OBS} for d in DIL},
              'partial': {str(d): {str(psi): {str(n): trim(partial[d][psi][n]) for n in RINGS} for psi in OBS} for d in DIL},
              'h_star_partial_d2': {str(psi): {str(n): partial[2][psi][n]['h_star'] for n in RINGS} for psi in OBS},
              'predictions': P, 'summary': {k: v.get('pass', 'reported') for k, v in P.items()}}
    OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False, default=jsonable) + '\n')
    print(json.dumps(report['summary']))
    for k, v in w2.items(): print('W2', k, 'C differs', v['closed_set_differs'], 'psi out of K', v['psi_not_in_K'], 'e', v['inverse_offset_e'], 'consistent', v['consistency_with_inverse_offset_observation'], '|C|', len(v['closed_partial']), 'K', v['commuters_partial'], 'max h', v['max_h_partial'], 'vs', v['max_h_standard'])
    for k, v in w3.items(): print('W3', k, v['census_equal_to_small_ring'], 'ring', v['ring_size'], '|C small|', len(v['closed_small_ring']))
    print('written', OUT.relative_to(ROOT))

if __name__ == '__main__':
    main()
