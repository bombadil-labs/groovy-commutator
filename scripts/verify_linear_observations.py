#!/usr/bin/env python3
"""Linear observations audit (protocol frozen 2026-09-11, reviewed by Codex at
revision eb7d2f1 before this implementation; see the protocol's Section 5).

For each linear rule psi in {0, 60, 90, 102, 150, 170, 204, 240} the observation
pi_psi(S) = F_psi(S) at cadence one, on rings n in {6, ..., 12}. Fibers are the
cosets of ker pi_psi; closure of F_r means F_r maps fibers into fibers
(pi_psi(F_r S) constant on every fiber). h_* is computed by exact partition
refinement: R_0 = fiber equality, R_{t+1} = R_t and R_t of the successor; h_* is
the least h with R_h = R_{h+1}.

E1  affine rules closed under every psi at every n (theorem control).
E2  trivial observations: 204/170/240/0 all closed; 150 at n in {7,8,10,11}.
E3  psi in {60, 102} at all n and psi = 90 at odd n: closed set == the 32.
E4  psi = 90 at even n: AFFINE <= X <= CLOSED_32, same X at all even n.
E5  psi = 150 at n in {6, 9, 12}: AFFINE <= X, same X at all three; reported
    whether X leaves CLOSED_32.
E6  h_* = 0 iff closed; for 60/102 (all n) and 90 (odd n) h_* equals the sixth
    unit's certified depth.
E7  complement-conjugation invariance of every table; reflection invariance for
    psi in {0, 90, 150, 204}; 60<->102 and 170<->240 exchanged by reflection.
"""
from __future__ import annotations
import hashlib, json, pathlib
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[1]
PARITY = ROOT / 'results/parity_coarse_graining_20260911.json'
HISTORY = ROOT / 'results/parity_history_bound_20260911.json'
OUT = ROOT / 'results/linear_observations_20260911.json'
PSIS = (0, 60, 90, 102, 150, 170, 204, 240); RINGS = (6, 7, 8, 9, 10, 11, 12)
AFFINE = sorted({0, 15, 51, 60, 85, 90, 102, 105, 150, 153, 165, 170, 195, 204, 240, 255})

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def all_states(n):
    k = np.arange(2 ** n, dtype=np.int64); return ((k[:, None] >> (n - 1 - np.arange(n))) & 1).astype(np.uint8)
def lut(r): return np.array([(r >> i) & 1 for i in range(8)], dtype=np.uint8)
def step(S, r):
    t = lut(r); return t[4 * np.roll(S, 1, axis=1) + 2 * S + np.roll(S, -1, axis=1)]
def ints(S): return (S.astype(np.int64) << (S.shape[1] - 1 - np.arange(S.shape[1]))).sum(axis=1)
def conj(r): return sum((((r >> (7 - i)) & 1) ^ 1) << i for i in range(8))
def mirror(r): return sum(((r >> (((i & 4) >> 2) | (i & 2) | ((i & 1) << 2))) & 1) << i for i in range(8))
def jsonable(o):
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.floating): return float(o)
    raise TypeError(type(o))

def relabel(keys):
    """dense class ids for a 1-D array of hashable keys (row-wise np.unique)."""
    _, inv = np.unique(keys, return_inverse=True); return inv

def analyse(psi, n):
    """closed set and h_* for every rule under pi_psi on the n-ring."""
    S = all_states(n); N = len(S)
    fiber = relabel(ints(step(S, psi)))                     # R_0 class of each state
    kernel = int((ints(step(S, psi)) == 0).sum())
    closed = []; h = {}
    for r in range(256):
        nxt = ints(step(S, r)); succ = fiber[nxt]           # fiber of the successor, indexed by state int
        # closure: fiber of successor constant within each fiber
        order = np.argsort(fiber, kind='stable'); f, s = fiber[order], succ[order]
        is_closed = not np.any((f[1:] == f[:-1]) & (s[1:] != s[:-1]))
        if is_closed: closed.append(r)
        # partition refinement
        cls = fiber; depth = 0
        while True:
            new = relabel(cls * N + cls[nxt])
            if len(np.unique(new)) == len(np.unique(cls)): break
            cls = new; depth += 1
        h[str(r)] = depth
    return {'kernel_size': kernel, 'closed': closed, 'closed_count': len(closed), 'h_star': h}

def main():
    parity = json.loads(PARITY.read_text()); history = json.loads(HISTORY.read_text())
    CLOSED_32 = parity['predictions']['C1_closure_classification']['by_ring']['8']['closed']
    certified = history['predictions']['D2_exact_depth']['certified_depth']
    T = {str(psi): {str(n): analyse(psi, n) for n in RINGS} for psi in PSIS}
    def closed(psi, n): return T[str(psi)][str(n)]['closed']
    def hs(psi, n): return T[str(psi)][str(n)]['h_star']
    P = {}
    # E1
    e1 = {'violations': [(psi, n, r) for psi in PSIS for n in RINGS for r in AFFINE if r not in closed(psi, n)]}
    e1['pass'] = not e1['violations']; P['E1_affine_closed_everywhere'] = e1
    # E2
    all256 = list(range(256))
    e2 = {'trivial': {str(psi): all(closed(psi, n) == all256 for n in RINGS) for psi in (0, 170, 204, 240)},
          'rule150_injective_rings': {str(n): closed(150, n) == all256 for n in (7, 8, 10, 11)}}
    e2['pass'] = all(e2['trivial'].values()) and all(e2['rule150_injective_rings'].values()); P['E2_trivial_observations'] = e2
    # E3
    e3 = {'rule60': {str(n): closed(60, n) == CLOSED_32 for n in RINGS}, 'rule102': {str(n): closed(102, n) == CLOSED_32 for n in RINGS},
          'rule90_odd': {str(n): closed(90, n) == CLOSED_32 for n in (7, 9, 11)}}
    e3['pass'] = all(all(v.values()) for v in e3.values() if isinstance(v, dict)); P['E3_complement_kernel_observations'] = e3
    # E4
    X90 = {str(n): closed(90, n) for n in (6, 8, 10, 12)}
    e4 = {'X90_by_ring': X90, 'affine_subset': all(set(AFFINE) <= set(v) for v in X90.values()),
          'subset_of_32': all(set(v) <= set(CLOSED_32) for v in X90.values()), 'same_across_even_rings': len({tuple(v) for v in X90.values()}) == 1,
          'X90': X90['6'], 'nonlinear_survivors': sorted(set(X90['6']) - set(AFFINE)), 'nonlinear_dropped': sorted(set(CLOSED_32) - set(X90['6']))}
    e4['pass'] = e4['affine_subset'] and e4['subset_of_32'] and e4['same_across_even_rings']; P['E4_rule90_even_rings'] = e4
    # E5
    X150 = {str(n): closed(150, n) for n in (6, 9, 12)}
    e5 = {'X150_by_ring': X150, 'affine_subset': all(set(AFFINE) <= set(v) for v in X150.values()), 'same_across_rings': len({tuple(v) for v in X150.values()}) == 1,
          'X150': X150['6'], 'count': len(X150['6']), 'outside_32': sorted(set(X150['6']) - set(CLOSED_32)), 'inside_32_nonaffine': sorted((set(X150['6']) & set(CLOSED_32)) - set(AFFINE)),
          'leaves_CLOSED_32': bool(set(X150['6']) - set(CLOSED_32))}
    e5['pass'] = e5['affine_subset'] and e5['same_across_rings']; P['E5_rule150_rings_divisible_by_3'] = e5
    # E6
    iff = all((hs(psi, n)[str(r)] == 0) == (r in closed(psi, n)) for psi in PSIS for n in RINGS for r in range(256))
    match = {'rule60': all(hs(60, n)[str(r)] == certified[str(r)] for n in RINGS for r in range(256)),
             'rule102': all(hs(102, n)[str(r)] == certified[str(r)] for n in RINGS for r in range(256)),
             'rule90_odd': all(hs(90, n)[str(r)] == certified[str(r)] for n in (7, 9, 11) for r in range(256))}
    hist = {f'{psi}@{n}': {str(k): int(v) for k, v in zip(*np.unique(list(hs(psi, n).values()), return_counts=True))} for psi in (90, 150) for n in RINGS}
    e6 = {'h_star_zero_iff_closed': iff, 'matches_certified_depth': match, 'histograms_90_150': hist,
          'max_h_star': {f'{psi}@{n}': max(hs(psi, n).values()) for psi in PSIS for n in RINGS}}
    e6['pass'] = iff and all(match.values()); P['E6_history_census'] = e6
    # E7
    def table(psi, n): return {str(r): (r in closed(psi, n), hs(psi, n)[str(r)]) for r in range(256)}
    conj_ok = all(table(psi, n)[str(r)] == table(psi, n)[str(conj(r))] for psi in PSIS for n in RINGS for r in range(256))
    mirror_ok = all(table(psi, n)[str(r)] == table(psi, n)[str(mirror(r))] for psi in (0, 90, 150, 204) for n in RINGS for r in range(256))
    swap_ok = all(table(a, n)[str(r)] == table(b, n)[str(mirror(r))] for a, b in ((60, 102), (170, 240)) for n in RINGS for r in range(256))
    e7 = {'complement_invariant': conj_ok, 'reflection_invariant_symmetric_psi': mirror_ok, 'reflection_exchanges_60_102_and_170_240': swap_ok}
    e7['pass'] = conj_ok and mirror_ok and swap_ok; P['E7_symmetries'] = e7
    report = {'protocol': 'linear-observations-20260911', 'schema': 1, 'cadence': 1, 'psis': list(PSIS), 'rings': list(RINGS),
              'source_hashes': {'script': sha(pathlib.Path(__file__)), 'parity_coarse_graining_result': sha(PARITY), 'parity_history_bound_result': sha(HISTORY)},
              'kernel_sizes': {str(psi): {str(n): T[str(psi)][str(n)]['kernel_size'] for n in RINGS} for psi in PSIS},
              'closed_sets': {str(psi): {str(n): closed(psi, n) for n in RINGS} for psi in PSIS},
              'h_star': {str(psi): {str(n): hs(psi, n) for n in RINGS} for psi in PSIS},
              'predictions': P, 'summary': {k: v['pass'] for k, v in P.items()}}
    report['summary']['E5_leaves_CLOSED_32'] = e5['leaves_CLOSED_32']
    OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False, default=jsonable) + '\n')
    print(json.dumps(report['summary'])); print('X90:', e4['X90'], 'dropped:', e4['nonlinear_dropped'])
    print('X150:', e5['X150'], 'outside 32:', e5['outside_32']); print('max h*:', e6['max_h_star']); print('written', OUT.relative_to(ROOT))

if __name__ == '__main__':
    main()
