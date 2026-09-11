#!/usr/bin/env python3
"""Block-majority audit (protocol frozen 2026-09-11, reviewed by Codex at revision
6f4eb6c before this implementation; see the protocol's Section 5).

pi(S) = F_232(S), three-cell majority at cadence one, on rings n in {6..12}.
Fibers: states with equal majority field. Closure of F_r: pi(F_r S) constant on
each fiber (successor-fiber constancy). Exact commutation K(n): F_r F_232 =
F_232 F_r on every state. h_*: exact partition refinement from the fibers to the
first stationary step.

M1  K(n) subset of C(n); K(n) contains {0,255,204,51,170,240,15,85,232,23}.
M2  the affine rules {60,90,102,105,150,153,165,195} are not closed at any n;
    the pairwise witness (0^n vs one isolated cell, same fiber, different
    observed successors) is recorded per the review's scoring clarification.
M3  C(n) vs K(n) reported: extras, equality, ring dependence.
M4  factor B on the image is radius-1 consistent on image words; unseen
    neighborhoods are don't-cares; for commuters B == F_r on image words.
M5  h_* census; h_* = 0 iff closed.
M6  complement-conjugation and reflection invariance of C, K and h_* tables.
M7  CLOSED_32 not a subset of C(n) (rule 90); C(n) subset of CLOSED_32 reported.
"""
from __future__ import annotations
import hashlib, json, pathlib
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[1]
PARITY = ROOT / 'results/parity_coarse_graining_20260911.json'
OUT = ROOT / 'results/block_majority_20260911.json'
PSI = 232; RINGS = (6, 7, 8, 9, 10, 11, 12)
NAMED = [0, 255, 204, 51, 170, 240, 15, 85, 232, 23]
AFFINE_TEST = [60, 90, 102, 105, 150, 153, 165, 195]

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
def jsonable(o):
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.floating): return float(o)
    raise TypeError(type(o))

def analyse(n):
    S = all_states(n); N = len(S); Y = step(S, PSI); y = ints(Y); fiber = relabel(y)
    image_ints = np.unique(y); image_states = all_states(n)[image_ints]        # image configurations as states
    sizes = np.bincount(fiber)
    out = {'image_size': int(len(image_ints)), 'image_fraction': float(len(image_ints) / N), 'max_fiber': int(sizes.max()),
           'fiber_size_histogram': {str(k): int(v) for k, v in zip(*np.unique(sizes, return_counts=True))}}
    closed = []; commute = []; h = {}; factors = {}; witness = {}
    zero = 0; iso = 1 << (n - 1)                                              # 0^n and one isolated cell (first site)
    for r in range(256):
        FS = step(S, r); nxt = ints(FS); succ = fiber[nxt]
        order = np.argsort(fiber, kind='stable'); f, s = fiber[order], succ[order]
        is_closed = not np.any((f[1:] == f[:-1]) & (s[1:] != s[:-1]))
        if is_closed: closed.append(r)
        if np.array_equal(step(FS, PSI), step(Y, r)): commute.append(r)
        witness[str(r)] = {'same_fiber': bool(fiber[zero] == fiber[iso]), 'successors_differ': bool(succ[zero] != succ[iso])}
        cls = fiber; depth = 0
        while True:
            new = relabel(cls * N + cls[nxt])
            if len(np.unique(new)) == len(np.unique(cls)): break
            cls = new; depth += 1
        h[str(r)] = depth
        if is_closed:
            # factor on the image: B(y) = pi(F_r S) for any S in the fiber of y; radius-1 table read on image words only
            first = {}                                                       # for each image state y, any S with pi(S) = y
            for idx in range(N):
                yi = y[idx]
                if yi not in first: first[yi] = idx
            reps = np.array([first[yi] for yi in image_ints])
            B = step(step(S[reps], r), PSI)                                  # (|image|, n) = B applied to each image state
            code = 4 * np.roll(image_states, 1, axis=1) + 2 * image_states + np.roll(image_states, -1, axis=1)
            table = {}; consistent = True
            for c in range(8):
                vals = np.unique(B[code == c])
                if len(vals) == 0: table[c] = None
                elif len(vals) > 1: consistent = False; table[c] = 'conflict'
                else: table[c] = int(vals[0])
            equals_Fr = bool(np.array_equal(B, step(image_states, r)))
            factors[str(r)] = {'radius1_consistent_on_image': consistent, 'table_image_determined': {str(c): table[c] for c in range(8)},
                               'unseen_codes': [c for c in range(8) if table[c] is None], 'equals_F_r_on_image': equals_Fr}
    out.update({'closed': closed, 'commuters': commute, 'h_star': h, 'factors': factors, 'witness_zero_vs_isolated': witness})
    return out

def main():
    parity = json.loads(PARITY.read_text()); CLOSED_32 = parity['predictions']['C1_closure_classification']['by_ring']['8']['closed']
    T = {str(n): analyse(n) for n in RINGS}
    def C(n): return T[str(n)]['closed']
    def K(n): return T[str(n)]['commuters']
    def H(n): return T[str(n)]['h_star']
    P = {}
    m1 = {'K_subset_C': {str(n): set(K(n)) <= set(C(n)) for n in RINGS}, 'named_in_K': {str(n): [r for r in NAMED if r not in K(n)] for n in RINGS}}
    m1['pass'] = all(m1['K_subset_C'].values()) and all(not v for v in m1['named_in_K'].values()); P['M1_commuters_close'] = m1
    m2 = {'closed_violations': {str(n): [r for r in AFFINE_TEST if r in C(n)] for n in RINGS},
          'witness': {str(n): {str(r): T[str(n)]['witness_zero_vs_isolated'][str(r)] for r in AFFINE_TEST} for n in RINGS}}
    m2['witness_holds_all'] = all(v['same_fiber'] and v['successors_differ'] for n in RINGS for v in m2['witness'][str(n)].values())
    m2['pass'] = all(not v for v in m2['closed_violations'].values()); P['M2_affine_rules_not_closed'] = m2
    m3 = {'C_by_ring': {str(n): C(n) for n in RINGS}, 'K_by_ring': {str(n): K(n) for n in RINGS},
          'extras_closed_not_commuting': {str(n): sorted(set(C(n)) - set(K(n))) for n in RINGS},
          'C_equals_K': {str(n): C(n) == K(n) for n in RINGS}, 'C_same_across_rings': len({tuple(C(n)) for n in RINGS}) == 1,
          'K_same_across_rings': len({tuple(K(n)) for n in RINGS}) == 1, 'C_size': {str(n): len(C(n)) for n in RINGS}}
    P['M3_closed_vs_commuters'] = m3
    m4 = {'inconsistent': {str(n): [int(r) for r, f in T[str(n)]['factors'].items() if not f['radius1_consistent_on_image']] for n in RINGS},
          'commuter_factor_equals_Fr': {str(n): all(T[str(n)]['factors'][str(r)]['equals_F_r_on_image'] for r in K(n)) for n in RINGS},
          'factors_n12': T['12']['factors']}
    m4['pass'] = all(not v for v in m4['inconsistent'].values()) and all(m4['commuter_factor_equals_Fr'].values()); P['M4_factor_elementary_on_image'] = m4
    iff = all((H(n)[str(r)] == 0) == (r in C(n)) for n in RINGS for r in range(256))
    hist = {str(n): {str(k): int(v) for k, v in zip(*np.unique(list(H(n).values()), return_counts=True))} for n in RINGS}
    mx = {str(n): max(H(n).values()) for n in RINGS}
    m5 = {'h_star_zero_iff_closed': iff, 'histogram': hist, 'max': mx, 'rules_at_max': {str(n): [r for r in range(256) if H(n)[str(r)] == mx[str(n)]] for n in RINGS},
          'rules_whose_depth_varies_with_n': sum(1 for r in range(256) if len({H(n)[str(r)] for n in RINGS}) > 1)}
    m5['pass'] = iff; P['M5_history_census'] = m5
    def tab(n): return {str(r): (r in C(n), r in K(n), H(n)[str(r)]) for r in range(256)}
    m6 = {'complement_invariant': all(tab(n)[str(r)] == tab(n)[str(conj(r))] for n in RINGS for r in range(256)),
          'reflection_invariant': all(tab(n)[str(r)] == tab(n)[str(mirror(r))] for n in RINGS for r in range(256))}
    m6['pass'] = m6['complement_invariant'] and m6['reflection_invariant']; P['M6_symmetries'] = m6
    m7 = {'CLOSED_32_not_subset_of_C': {str(n): not set(CLOSED_32) <= set(C(n)) for n in RINGS}, 'rule90_in_C': {str(n): 90 in C(n) for n in RINGS},
          'C_subset_of_CLOSED_32': {str(n): set(C(n)) <= set(CLOSED_32) for n in RINGS}, 'C_minus_CLOSED_32': {str(n): sorted(set(C(n)) - set(CLOSED_32)) for n in RINGS}}
    m7['pass'] = all(m7['CLOSED_32_not_subset_of_C'].values()); P['M7_relation_to_parity_criterion'] = m7
    report = {'protocol': 'block-majority-20260911', 'schema': 1, 'cadence': 1, 'observation': PSI, 'rings': list(RINGS),
              'source_hashes': {'script': sha(pathlib.Path(__file__)), 'parity_coarse_graining_result': sha(PARITY)},
              'observation_facts': {str(n): {k: T[str(n)][k] for k in ('image_size', 'image_fraction', 'max_fiber', 'fiber_size_histogram')} for n in RINGS},
              'h_star': {str(n): H(n) for n in RINGS}, 'predictions': P, 'summary': {k: v.get('pass', 'reported') for k, v in P.items()}}
    OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False, default=jsonable) + '\n')
    print(json.dumps(report['summary'])); print('C(12):', C(12)); print('K(12):', K(12)); print('extras:', m3['extras_closed_not_commuting'])
    print('max h*:', mx, 'varies:', m5['rules_whose_depth_varies_with_n']); print('C subset 32:', m7['C_subset_of_CLOSED_32']); print('written', OUT.relative_to(ROOT))

if __name__ == '__main__':
    main()
