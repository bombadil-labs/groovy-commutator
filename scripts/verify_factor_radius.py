#!/usr/bin/env python3
"""Factor-radius audit (protocol frozen 2026-09-11, gate-1 sign-off by Codex at
46d9a7c before this implementation; see the protocol's Section 5).

For observations psi in {232, 4, 32, 200, 22} on rings 6..12, and for every rule
closed under psi, the factor B_r on the image (B_r(psi(S)) = psi(F_r S)) and its
locality radius rho_r(n): the least rho in {0,1,2,3} such that the (2 rho + 1)-window
table read off image words is conflict-free; '>3' otherwise. Observations 236 and
223 are conjugate-observation symmetry controls only (R6), outside the primary
five-observation census.

R1  200 and 4 are idempotent; for their closed rules B_r(y) == psi(F_r(y)) on the
    image and rho <= 2.
R2  under 200 the sixteen tenth-unit residual rules have rho == 2 at every ring and
    every other closed rule rho <= 1; under 4 every closed rule rho <= 1.
R3  under 232, 32, 22 every closed rule has rho <= 2 (census bet); failures listed
    with their radius-2 conflicting windows.
R4  collapse rules rho == 0; commuters rho <= 1.
R5  ring independence reported; frozen for 200 and 4 at n >= 7.
R6  reflection invariance of rho tables; complement covariance 200<->236, 4<->223.
"""
from __future__ import annotations
import hashlib, json, pathlib
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[1]
MAJORITY = ROOT / 'results/block_majority_20260911.json'
ISOLATED = ROOT / 'results/isolated_cell_20260911.json'
COMPLEMENT = ROOT / 'results/complement_observation_20260911.json'
OUT = ROOT / 'results/factor_radius_20260911.json'
OBS = (232, 4, 32, 200, 22); CONTROLS = {200: 236, 4: 223}; IDEMPOTENT = (200, 4); NONIDEMPOTENT = (232, 32, 22)
RINGS = (6, 7, 8, 9, 10, 11, 12); RADII = (0, 1, 2, 3)
SIXTEEN = [72, 76, 128, 130, 132, 136, 140, 144, 152, 160, 162, 176, 183, 192, 194, 196]

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

def window_keys(Y, rho):
    """Cyclic (2 rho + 1)-cell window code at every site of every row of Y, MSB first."""
    n = Y.shape[1]; key = np.zeros(Y.shape, dtype=np.int64)
    for d in range(-rho, rho + 1): key = key * 2 + np.roll(Y, -d, axis=1)
    return key

def analyse(n, psi):
    S = all_states(n); N = len(S); Y = step(S, psi); y = ints(Y); fiber = relabel(y)
    image_ints = np.unique(y); image_states = S[image_ints]
    idem = bool(np.array_equal(step(Y, psi), Y))
    first = {}
    for idx in range(N):
        if y[idx] not in first: first[y[idx]] = idx
    reps = np.array([first[yi] for yi in image_ints])
    out = {'idempotent': idem, 'image_size': int(len(image_ints)), 'closed': [], 'commuters': [], 'collapse': [], 'rho': {}, 'conflicts_r1': {}, 'conflicts_r2': {}, 'B_equals_psi_F_on_image': {}}
    for r in range(256):
        FS = step(S, r); nxt = ints(FS); succ = fiber[nxt]
        order = np.argsort(fiber, kind='stable'); f, s = fiber[order], succ[order]
        if np.any((f[1:] == f[:-1]) & (s[1:] != s[:-1])): continue
        out['closed'].append(r)
        if np.array_equal(step(FS, psi), step(Y, r)): out['commuters'].append(r)
        B = step(step(S[reps], r), psi)                                   # factor applied to each image state
        if len(np.unique(ints(B))) == 1: out['collapse'].append(r)
        out['B_equals_psi_F_on_image'][str(r)] = bool(np.array_equal(B, step(step(image_states, r), psi)))
        rho_found = '>3'
        for rho in RADII:
            keys = window_keys(image_states, rho).ravel(); vals = B.ravel()
            order2 = np.argsort(keys, kind='stable'); k2, v2 = keys[order2], vals[order2]
            conflict = (k2[1:] == k2[:-1]) & (v2[1:] != v2[:-1])
            if rho in (1, 2):
                bad = sorted(set(int(k) for k in k2[1:][conflict]))
                if bad: out['conflicts_r%d' % rho][str(r)] = [format(k, '0%db' % (2 * rho + 1)) for k in bad]
            if not conflict.any(): rho_found = rho; break
        out['rho'][str(r)] = rho_found
    return out

def main():
    maj = json.loads(MAJORITY.read_text()); iso = json.loads(ISOLATED.read_text()); comp = json.loads(COMPLEMENT.read_text())
    ref = {232: maj['predictions']['M3_closed_vs_commuters']['C_by_ring'], 4: iso['predictions']['N3_commute_or_collapse']['C_by_ring'],
           32: {n: comp['census']['32'][n]['closed'] for n in comp['census']['32']}, 200: {n: comp['census']['200'][n]['closed'] for n in comp['census']['200']},
           22: {n: comp['census']['22'][n]['closed'] for n in comp['census']['22']}}
    T = {psi: {n: analyse(n, psi) for n in RINGS} for psi in OBS}
    U = {psi: {n: analyse(n, CONTROLS[psi]) for n in RINGS} for psi in CONTROLS}
    def rho(psi, n, r): return T[psi][n]['rho'][str(r)]
    def num(x): return 99 if x == '>3' else x
    P = {}
    refcheck = {str(psi): {str(n): T[psi][n]['closed'] == ref[psi][str(n)] for n in RINGS} for psi in OBS}
    P['reference_consistency'] = {'closed_sets_match_earlier_units': refcheck, 'pass': all(v for d in refcheck.values() for v in d.values())}
    idem = {str(psi): {str(n): T[psi][n]['idempotent'] for n in RINGS} for psi in OBS}
    r1 = {'idempotent': idem,
          'B_equals_psi_F_all_closed': {str(psi): {str(n): all(T[psi][n]['B_equals_psi_F_on_image'].values()) for n in RINGS} for psi in IDEMPOTENT},
          'rho_le_2_all_closed': {str(psi): {str(n): all(num(rho(psi, n, r)) <= 2 for r in T[psi][n]['closed']) for n in RINGS} for psi in IDEMPOTENT}}
    r1['pass'] = all(idem[str(p)][str(n)] for p in IDEMPOTENT for n in RINGS) and all(not idem[str(p)][str(n)] for p in NONIDEMPOTENT for n in RINGS) \
        and all(v for d in r1['B_equals_psi_F_all_closed'].values() for v in d.values()) and all(v for d in r1['rho_le_2_all_closed'].values() for v in d.values())
    P['R1_idempotent_factor'] = r1
    r2 = {'sixteen_at_2_under_200': {str(n): [r for r in SIXTEEN if rho(200, n, r) != 2] for n in RINGS},
          'others_le_1_under_200': {str(n): [r for r in T[200][n]['closed'] if r not in SIXTEEN and num(rho(200, n, r)) > 1] for n in RINGS},
          'all_le_1_under_4': {str(n): [r for r in T[4][n]['closed'] if num(rho(4, n, r)) > 1] for n in RINGS}}
    r2['pass'] = all(not v for d in (r2['sixteen_at_2_under_200'], r2['others_le_1_under_200'], r2['all_le_1_under_4']) for v in d.values()); P['R2_sixteen_exactly_two'] = r2
    r3 = {str(psi): {str(n): {str(r): {'rho': rho(psi, n, r), 'radius2_conflicts': T[psi][n]['conflicts_r2'].get(str(r), [])} for r in T[psi][n]['closed'] if num(rho(psi, n, r)) > 2} for n in RINGS} for psi in NONIDEMPOTENT}
    r3['pass'] = all(not v for d in [r3[str(p)] for p in NONIDEMPOTENT] for v in d.values()); P['R3_nonidempotent_radius_le_2'] = r3
    r4 = {'collapse_not_0': {str(psi): {str(n): [r for r in T[psi][n]['collapse'] if rho(psi, n, r) != 0] for n in RINGS} for psi in OBS},
          'commuter_gt_1': {str(psi): {str(n): [r for r in T[psi][n]['commuters'] if num(rho(psi, n, r)) > 1] for n in RINGS} for psi in OBS}}
    r4['pass'] = all(not v for k in r4 for d in r4[k].values() for v in d.values()); P['R4_collapse_and_commuters'] = r4
    def ring_indep(psi, rings): return {str(r): len({rho(psi, n, r) for n in rings}) == 1 for r in T[psi][rings[-1]]['closed'] if all(r in T[psi][n]['closed'] for n in rings)}
    r5 = {'ring_independent_6_to_12': {str(psi): ring_indep(psi, RINGS) for psi in OBS},
          'idempotent_ring_independent_7_to_12': {str(psi): ring_indep(psi, RINGS[1:]) for psi in IDEMPOTENT}}
    r5['pass'] = all(v for p in IDEMPOTENT for v in r5['idempotent_ring_independent_7_to_12'][str(p)].values()); P['R5_ring_independence'] = r5
    refl = {str(psi): all(rho(psi, n, r) == rho(psi, n, mirror(r)) for n in RINGS for r in T[psi][n]['closed']) and all(mirror(r) in T[psi][n]['closed'] for n in RINGS for r in T[psi][n]['closed']) for psi in OBS}
    cov = {f'{psi}<->{CONTROLS[psi]}': all(set(conj(r) for r in T[psi][n]['closed']) == set(U[psi][n]['closed']) and all(rho(psi, n, r) == U[psi][n]['rho'][str(conj(r))] for r in T[psi][n]['closed']) for n in RINGS) for psi in CONTROLS}
    P['R6_symmetries'] = {'reflection_invariant': refl, 'complement_covariant_controls': cov, 'pass': all(refl.values()) and all(cov.values())}
    hist = {str(psi): {str(n): {str(k): sum(1 for r in T[psi][n]['closed'] if str(rho(psi, n, r)) == str(k)) for k in (0, 1, 2, 3, '>3')} for n in RINGS} for psi in OBS}
    report = {'protocol': 'factor-radius-20260911', 'schema': 1, 'observations': list(OBS), 'conjugate_controls': CONTROLS, 'rings': list(RINGS), 'radii': list(RADII),
              'source_hashes': {'script': sha(pathlib.Path(__file__)), 'block_majority_result': sha(MAJORITY), 'isolated_cell_result': sha(ISOLATED), 'complement_observation_result': sha(COMPLEMENT)},
              'idempotent': idem, 'rho': {str(psi): {str(n): T[psi][n]['rho'] for n in RINGS} for psi in OBS}, 'rho_histogram': hist,
              'conflicts_radius1_n12': {str(psi): T[psi][12]['conflicts_r1'] for psi in OBS}, 'conflicts_radius2_n12': {str(psi): T[psi][12]['conflicts_r2'] for psi in OBS},
              'closed_by_ring': {str(psi): {str(n): T[psi][n]['closed'] for n in RINGS} for psi in OBS},
              'predictions': P, 'summary': {k: v.get('pass', 'reported') for k, v in P.items()}}
    OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False, default=jsonable) + '\n')
    print(json.dumps(report['summary'])); print('idempotent', {p: idem[str(p)]['12'] for p in OBS}); print('hist@12', {p: hist[str(p)]['12'] for p in OBS})
    print('R3 failures', {p: {n: list(r3[str(p)][n].keys()) for n in r3[str(p)] if r3[str(p)][n]} for p in NONIDEMPOTENT}); print('written', OUT.relative_to(ROOT))

if __name__ == '__main__':
    main()
