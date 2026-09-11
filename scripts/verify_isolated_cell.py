#!/usr/bin/env python3
"""Isolated-cell audit (protocol frozen 2026-09-11, re-frozen at 9ae9d17 after
Codex's first gate-1 round; gate-1 sign-off at that head, see Section 5).

pi(S) = F_4(S), isolated-cell detection (window 010) at cadence one, on rings
n in {6..12}. The same census is run for the conjugate observation F_223 so that
complement covariance can be scored. Fibers: states with equal observation.
Closure of F_r: pi(F_r S) constant on each fiber. Exact commutation K(n):
F_r F_psi = F_psi F_r on every state. Collapse Z(n): closed with a constant
factor (pi(F_r S) the same field for every S). h_*: exact partition refinement
from the fibers to the first stationary step.

N1  K(n) subset of C(n); K(n) contains {0,4,170,204,240,232}; 255 not in K(n).
N2  255 in Z(n) \\ K(n).
N3  C(n) == K(n) union Z(n); every violation listed with its factor table.
N4  the affine rules {60,90,102,105,150,153,165,195} are not closed at any n;
    per-rule frozen witness W_r in the all-zeros fiber: 11 for 60,102,150,153,195;
    111 for 105; 110111 for 90,165 (the pair (0^n, W_r) has different observed
    successors). Scored separately from non-closure.
N5  h_* census; h_* = 0 iff closed.
N6  reflection invariance of the observation-4 tables; complement covariance:
    tab_4(r) == tab_223(conj(r)) for C, K, Z and h_*.
N7  CLOSED_32 not a subset of C_4(n) (rule 90); relations to C_232, K_232 and
    CLOSED_32 reported.
"""
from __future__ import annotations
import hashlib, json, pathlib
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[1]
PARITY = ROOT / 'results/parity_coarse_graining_20260911.json'
MAJORITY = ROOT / 'results/block_majority_20260911.json'
OUT = ROOT / 'results/isolated_cell_20260911.json'
PSI = 4; PSI_CONJ = 223; RINGS = (6, 7, 8, 9, 10, 11, 12)
NAMED = [0, 4, 170, 204, 240, 232]
AFFINE_TEST = [60, 90, 102, 105, 150, 153, 165, 195]
WITNESS = {60: '11', 102: '11', 150: '11', 153: '11', 195: '11', 105: '111', 90: '110111', 165: '110111'}

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def all_states(n):
    k = np.arange(2 ** n, dtype=np.int64); return ((k[:, None] >> (n - 1 - np.arange(n))) & 1).astype(np.uint8)
def lut(r): return np.array([(r >> i) & 1 for i in range(8)], dtype=np.uint8)
def step(S, r):
    t = lut(r); return t[4 * np.roll(S, 1, axis=1) + 2 * S + np.roll(S, -1, axis=1)]
def ints(S): return (S.astype(np.int64) << (S.shape[1] - 1 - np.arange(S.shape[1]))).sum(axis=1)
def conj(r): return sum((((r >> (7 - i)) & 1) ^ 1) << i for i in range(8))
def mirror(r): return sum(((r >> (((i & 4) >> 2) | (i & 2) | ((i & 1) << 2))) & 1) << i for i in range(8))
def relabel(keys): _, inv = np.unique(keys, return_inverse=True); return inv
def embed(pattern, n): return sum(int(b) << (n - 1 - i) for i, b in enumerate(pattern))   # pattern at the first sites, zeros after
def jsonable(o):
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.floating): return float(o)
    raise TypeError(type(o))

def analyse(n, psi):
    S = all_states(n); N = len(S); Y = step(S, psi); y = ints(Y); fiber = relabel(y)
    image_ints = np.unique(y); image_states = S[image_ints]
    sizes = np.bincount(fiber)
    out = {'image_size': int(len(image_ints)), 'image_fraction': float(len(image_ints) / N), 'max_fiber': int(sizes.max()),
           'fiber_size_histogram': {str(k): int(v) for k, v in zip(*np.unique(sizes, return_counts=True))}}
    first = {}
    for idx in range(N):
        if y[idx] not in first: first[y[idx]] = idx
    reps = np.array([first[yi] for yi in image_ints])
    code = 4 * np.roll(image_states, 1, axis=1) + 2 * image_states + np.roll(image_states, -1, axis=1)
    closed = []; commute = []; collapse = []; h = {}; factors = {}; witness = {}
    zero = 0
    for r in range(256):
        FS = step(S, r); nxt = ints(FS); succ = fiber[nxt]
        order = np.argsort(fiber, kind='stable'); f, s = fiber[order], succ[order]
        is_closed = not np.any((f[1:] == f[:-1]) & (s[1:] != s[:-1]))
        if is_closed: closed.append(r)
        if np.array_equal(step(FS, psi), step(Y, r)): commute.append(r)
        if r in WITNESS:
            w = embed(WITNESS[r], n)
            witness[str(r)] = {'pattern': WITNESS[r], 'same_fiber': bool(fiber[zero] == fiber[w]), 'successors_differ': bool(succ[zero] != succ[w])}
        cls = fiber; depth = 0
        while True:
            new = relabel(cls * N + cls[nxt])
            if len(np.unique(new)) == len(np.unique(cls)): break
            cls = new; depth += 1
        h[str(r)] = depth
        if is_closed:
            B = step(step(S[reps], r), psi)                                  # factor applied to each image state
            table = {}; consistent = True
            for c in range(8):
                vals = np.unique(B[code == c])
                if len(vals) == 0: table[c] = None
                elif len(vals) > 1: consistent = False; table[c] = 'conflict'
                else: table[c] = int(vals[0])
            constant = bool(len(np.unique(ints(B))) == 1)
            if constant: collapse.append(r)
            factors[str(r)] = {'radius1_consistent_on_image': consistent, 'table_image_determined': {str(c): table[c] for c in range(8)},
                               'unseen_codes': [c for c in range(8) if table[c] is None],
                               'equals_F_r_on_image': bool(np.array_equal(B, step(image_states, r))),
                               'constant_on_image': constant, 'constant_value': (int(ints(B)[0]) if constant else None)}
    out.update({'closed': closed, 'commuters': commute, 'collapse': collapse, 'h_star': h, 'factors': factors, 'witness': witness})
    return out

def main():
    parity = json.loads(PARITY.read_text()); CLOSED_32 = parity['predictions']['C1_closure_classification']['by_ring']['8']['closed']
    majority = json.loads(MAJORITY.read_text())['predictions']['M3_closed_vs_commuters']
    C232 = {n: majority['C_by_ring'][n] for n in majority['C_by_ring']}; K232 = {n: majority['K_by_ring'][n] for n in majority['K_by_ring']}
    T = {str(n): analyse(n, PSI) for n in RINGS}; U = {str(n): analyse(n, PSI_CONJ) for n in RINGS}
    def C(n): return T[str(n)]['closed']
    def K(n): return T[str(n)]['commuters']
    def Z(n): return T[str(n)]['collapse']
    def H(n): return T[str(n)]['h_star']
    P = {}
    n1 = {'K_subset_C': {str(n): set(K(n)) <= set(C(n)) for n in RINGS}, 'named_missing_from_K': {str(n): [r for r in NAMED if r not in K(n)] for n in RINGS},
          'rule255_in_K': {str(n): 255 in K(n) for n in RINGS}}
    n1['pass'] = all(n1['K_subset_C'].values()) and all(not v for v in n1['named_missing_from_K'].values()) and not any(n1['rule255_in_K'].values())
    P['N1_commuters_close'] = n1
    n2 = {'rule255_in_Z': {str(n): 255 in Z(n) for n in RINGS}, 'C_equals_K': {str(n): C(n) == K(n) for n in RINGS}}
    n2['pass'] = all(n2['rule255_in_Z'].values()) and not any(n1['rule255_in_K'].values())
    P['N2_collapse_without_commuting'] = n2
    viol = {str(n): sorted(set(C(n)) - set(K(n)) - set(Z(n))) for n in RINGS}
    n3 = {'C_by_ring': {str(n): C(n) for n in RINGS}, 'K_by_ring': {str(n): K(n) for n in RINGS}, 'Z_by_ring': {str(n): Z(n) for n in RINGS},
          'closed_neither_commuting_nor_collapse': viol,
          'violation_factors': {str(n): {str(r): T[str(n)]['factors'][str(r)] for r in viol[str(n)]} for n in RINGS},
          'K_and_Z_overlap': {str(n): sorted(set(K(n)) & set(Z(n))) for n in RINGS},
          'C_same_across_rings': len({tuple(C(n)) for n in RINGS}) == 1, 'K_same_across_rings': len({tuple(K(n)) for n in RINGS}) == 1,
          'Z_same_across_rings': len({tuple(Z(n)) for n in RINGS}) == 1, 'C_size': {str(n): len(C(n)) for n in RINGS}}
    n3['pass'] = all(not v for v in viol.values()); P['N3_commute_or_collapse'] = n3
    n4 = {'closed_violations': {str(n): [r for r in AFFINE_TEST if r in C(n)] for n in RINGS},
          'witness': {str(n): T[str(n)]['witness'] for n in RINGS}}
    n4['witness_holds_all'] = all(v['same_fiber'] and v['successors_differ'] for n in RINGS for v in n4['witness'][str(n)].values())
    n4['pass'] = all(not v for v in n4['closed_violations'].values()) and n4['witness_holds_all']; P['N4_affine_rules_not_closed'] = n4
    iff = all((H(n)[str(r)] == 0) == (r in C(n)) for n in RINGS for r in range(256))
    hist = {str(n): {str(k): int(v) for k, v in zip(*np.unique(list(H(n).values()), return_counts=True))} for n in RINGS}
    mx = {str(n): max(H(n).values()) for n in RINGS}
    n5 = {'h_star_zero_iff_closed': iff, 'histogram': hist, 'max': mx, 'rules_at_max': {str(n): [r for r in range(256) if H(n)[str(r)] == mx[str(n)]] for n in RINGS},
          'rules_whose_depth_varies_with_n': sum(1 for r in range(256) if len({H(n)[str(r)] for n in RINGS}) > 1),
          'majority_max_for_comparison': {n: max(v.values()) for n, v in json.loads(MAJORITY.read_text())['h_star'].items()}}
    n5['pass'] = iff; P['N5_history_census'] = n5
    def tab(X, n): return {str(r): (r in X[str(n)]['closed'], r in X[str(n)]['commuters'], r in X[str(n)]['collapse'], X[str(n)]['h_star'][str(r)]) for r in range(256)}
    n6 = {'reflection_invariant': all(tab(T, n)[str(r)] == tab(T, n)[str(mirror(r))] for n in RINGS for r in range(256)),
          'complement_covariant': all(tab(T, n)[str(r)] == tab(U, n)[str(conj(r))] for n in RINGS for r in range(256)),
          'complement_invariant_outright': {str(n): tab(T, n) == tab(U, n) for n in RINGS},
          'C_223_by_ring': {str(n): U[str(n)]['closed'] for n in RINGS}, 'K_223_by_ring': {str(n): U[str(n)]['commuters'] for n in RINGS}}
    n6['pass'] = n6['reflection_invariant'] and n6['complement_covariant']; P['N6_symmetries'] = n6
    n7 = {'CLOSED_32_not_subset_of_C4': {str(n): not set(CLOSED_32) <= set(C(n)) for n in RINGS}, 'rule90_in_C4': {str(n): 90 in C(n) for n in RINGS},
          'C4_subset_of_CLOSED_32': {str(n): set(C(n)) <= set(CLOSED_32) for n in RINGS}, 'C4_minus_CLOSED_32': {str(n): sorted(set(C(n)) - set(CLOSED_32)) for n in RINGS},
          'C4_subset_of_C232': {str(n): set(C(n)) <= set(C232[str(n)]) for n in RINGS}, 'C232_subset_of_C4': {str(n): set(C232[str(n)]) <= set(C(n)) for n in RINGS},
          'C4_and_C232': {str(n): sorted(set(C(n)) & set(C232[str(n)])) for n in RINGS}, 'K4_and_K232': {str(n): sorted(set(K(n)) & set(K232[str(n)])) for n in RINGS}}
    n7['pass'] = all(n7['CLOSED_32_not_subset_of_C4'].values()); P['N7_relation_to_earlier_criteria'] = n7
    facts = lambda X: {str(n): {k: X[str(n)][k] for k in ('image_size', 'image_fraction', 'max_fiber', 'fiber_size_histogram')} for n in RINGS}
    report = {'protocol': 'isolated-cell-20260911', 'schema': 1, 'cadence': 1, 'observation': PSI, 'conjugate_observation': PSI_CONJ, 'rings': list(RINGS),
              'source_hashes': {'script': sha(pathlib.Path(__file__)), 'parity_coarse_graining_result': sha(PARITY), 'block_majority_result': sha(MAJORITY)},
              'observation_facts': {'4': facts(T), '223': facts(U)},
              'h_star': {'4': {str(n): H(n) for n in RINGS}, '223': {str(n): U[str(n)]['h_star'] for n in RINGS}},
              'factors_n12': {'4': T['12']['factors'], '223': U['12']['factors']},
              'predictions': P, 'summary': {k: v.get('pass', 'reported') for k, v in P.items()}}
    OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False, default=jsonable) + '\n')
    print(json.dumps(report['summary'])); print('C(12):', C(12)); print('K(12):', K(12)); print('Z(12):', Z(12)); print('N3 violations:', viol)
    print('max h*:', mx, 'varies:', n5['rules_whose_depth_varies_with_n']); print('C4 subset 32:', n7['C4_subset_of_CLOSED_32']); print('written', OUT.relative_to(ROOT))

if __name__ == '__main__':
    main()
