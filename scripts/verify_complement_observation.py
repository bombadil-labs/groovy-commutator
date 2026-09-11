#!/usr/bin/env python3
"""Complement-of-the-observation audit (protocol frozen 2026-09-11, gate-1 sign-off
by Codex at 3a09b31 before this implementation; see the protocol's Section 5).

Observations psi in {32, 200, 22} and their conjugates {251, 236, 151}, each
applied once at cadence one on rings n in {6..12}; rule 4 joins the Q4 word
check. Per observation: closed set C, exact commuters K, collapse rules Z
(closed, constant factor), residual class X = C \\ (K u Z), the observational
equivalence partition (r ~ s iff psi o F_r == psi o F_s on all states), the
32-word local partition, factor tables for X, and h_*.

Q1  255 - psi in C at every n, factor psi o not on the image.
Q2  255 - psi not in K and not in Z, hence in X, at every n.
Q3  X subset of the equivalence class of 255 - psi; violations listed.
Q4  the global equivalence partition equals the 32-word partition at every n
    (psi in {32, 200, 22, 4}); under rule 4, rules 123 and 251 agree on all words.
Q5  {0, 170, 204, 240, psi} subset of K; 255 in K_200; 255 in Z_32 and Z_22.
Q6  h_* = 0 iff closed; annex: h_* at rings 13-16 for {106,120,169,225} under
    232 (bet: max at 16 exceeds 16) and {62,118} under 4 (reported).
Q7  reflection invariance per psi; complement covariance to the conjugate census.
"""
from __future__ import annotations
import hashlib, json, pathlib
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[1]
MAJORITY = ROOT / 'results/block_majority_20260911.json'
ISOLATED = ROOT / 'results/isolated_cell_20260911.json'
OUT = ROOT / 'results/complement_observation_20260911.json'
OBS = {32: 251, 200: 236, 22: 151}                    # observation -> conjugate observation
RINGS = (6, 7, 8, 9, 10, 11, 12)
ANNEX = {232: [106, 120, 169, 225], 4: [62, 118]}; ANNEX_RINGS = (13, 14, 15, 16)

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

def local_table(r, psi):
    """32-entry table of (psi o F_r) at the centre of a five-cell word (non-cyclic)."""
    out = []
    for w in range(32):
        cells = [(w >> (4 - i)) & 1 for i in range(5)]
        mid = [lut(r)[4 * cells[i - 1] + 2 * cells[i] + cells[i + 1]] for i in (1, 2, 3)]
        out.append(int(lut(psi)[4 * mid[0] + 2 * mid[1] + mid[2]]))
    return tuple(out)

def partition(keys):
    """Sorted list of sorted classes of rules 0..255 sharing a key."""
    groups = {}
    for r, k in enumerate(keys): groups.setdefault(k, []).append(r)
    return sorted(groups.values())

def depth(fiber, nxt, N):
    cls = fiber; d = 0
    while True:
        new = relabel(cls * N + cls[nxt])
        if len(np.unique(new)) == len(np.unique(cls)): break
        cls = new; d += 1
    return d

def analyse(n, psi, rules=range(256), full=True):
    S = all_states(n); N = len(S); Y = step(S, psi); y = ints(Y); fiber = relabel(y)
    image_ints = np.unique(y); image_states = S[image_ints]; sizes = np.bincount(fiber)
    out = {'image_size': int(len(image_ints)), 'image_fraction': float(len(image_ints) / N), 'max_fiber': int(sizes.max())}
    first = {}
    for idx in range(N):
        if y[idx] not in first: first[y[idx]] = idx
    reps = np.array([first[yi] for yi in image_ints])
    code = 4 * np.roll(image_states, 1, axis=1) + 2 * image_states + np.roll(image_states, -1, axis=1)
    closed = []; commute = []; collapse = []; h = {}; factors = {}; keys = []
    for r in rules:
        FS = step(S, r); nxt = ints(FS); succ = fiber[nxt]
        h[str(r)] = depth(fiber, nxt, N)
        if not full: continue
        order = np.argsort(fiber, kind='stable'); f, s = fiber[order], succ[order]
        is_closed = not np.any((f[1:] == f[:-1]) & (s[1:] != s[:-1]))
        if is_closed: closed.append(r)
        if np.array_equal(step(FS, psi), step(Y, r)): commute.append(r)
        keys.append(hashlib.sha256(ints(step(FS, psi)).tobytes()).hexdigest())      # observed-successor map fingerprint
        if is_closed:
            B = step(step(S[reps], r), psi)
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
                               'equals_F_r_on_image': bool(np.array_equal(B, step(image_states, r))), 'constant_on_image': constant}
    if full:
        residual = sorted(set(closed) - set(commute) - set(collapse))
        out.update({'closed': closed, 'commuters': commute, 'collapse': collapse, 'residual': residual, 'h_star': h,
                    'factors_residual': {str(r): factors[str(r)] for r in residual}, 'factor_complement': factors.get(str(255 - psi)),
                    'equivalence_partition': partition(keys)})
    else:
        out.update({'h_star': h})
    return out

def main():
    T = {}
    for psi in list(OBS) + list(OBS.values()):
        T[psi] = {str(n): analyse(n, psi) for n in RINGS}
    word_partition = {psi: partition([local_table(r, psi) for r in range(256)]) for psi in list(OBS) + [4]}
    def field(psi, n, k): return T[psi][str(n)][k]
    def cls_of(psi, n, r): return next(c for c in field(psi, n, 'equivalence_partition') if r in c)
    P = {}
    q1 = {str(psi): {str(n): (255 - psi) in field(psi, n, 'closed') for n in RINGS} for psi in OBS}
    q1f = {str(psi): {str(n): field(psi, n, 'factor_complement') for n in RINGS} for psi in OBS}
    P['Q1_complement_closes'] = {'closed_by_ring': q1, 'factor_by_ring': q1f, 'pass': all(v for d in q1.values() for v in d.values())}
    q2 = {str(psi): {str(n): {'in_K': (255 - psi) in field(psi, n, 'commuters'), 'in_Z': (255 - psi) in field(psi, n, 'collapse'),
                             'in_X': (255 - psi) in field(psi, n, 'residual')} for n in RINGS} for psi in OBS}
    P['Q2_complement_in_residual_class'] = {'by_ring': q2, 'pass': all(v['in_X'] and not v['in_K'] and not v['in_Z'] for d in q2.values() for v in d.values())}
    q3 = {}
    for psi in OBS:
        q3[str(psi)] = {}
        for n in RINGS:
            X = field(psi, n, 'residual'); E = cls_of(psi, n, 255 - psi)
            viol = sorted(set(X) - set(E))
            q3[str(psi)][str(n)] = {'X': X, 'class_of_complement': E, 'X_subset_of_class': not viol, 'violations': viol,
                                    'violation_factors': {str(r): field(psi, n, 'factors_residual')[str(r)] for r in viol},
                                    'violation_classes': {str(r): cls_of(psi, n, r) for r in viol},
                                    'class_subset_of_C': set(E) <= set(field(psi, n, 'closed')),
                                    'class_minus_X': sorted(set(E) - set(X))}
    P['Q3_residual_in_complement_class'] = {'by_ring': q3, 'control_class_subset_of_C': all(v['class_subset_of_C'] for d in q3.values() for v in d.values()),
                                            'pass': all(v['X_subset_of_class'] for d in q3.values() for v in d.values())}
    T4 = {str(n): analyse(n, 4) for n in RINGS}
    q4 = {str(psi): {str(n): (T4[str(n)] if psi == 4 else T[psi][str(n)])['equivalence_partition'] == word_partition[psi] for n in RINGS} for psi in list(OBS) + [4]}
    w123 = local_table(123, 4) == local_table(251, 4)
    P['Q4_equivalence_is_local'] = {'global_equals_word_partition': q4, 'word_partition_class_counts': {str(psi): len(word_partition[psi]) for psi in word_partition},
                                    'rule123_rule251_agree_on_32_words': w123, 'class_of_251_under_4_by_words': next(c for c in word_partition[4] if 251 in c),
                                    'pass': all(v for d in q4.values() for v in d.values()) and w123}
    named = {psi: [0, 170, 204, 240, psi] for psi in OBS}
    q5 = {str(psi): {str(n): {'named_missing_from_K': [r for r in named[psi] if r not in field(psi, n, 'commuters')],
                             '255_in_K': 255 in field(psi, n, 'commuters'), '255_in_Z': 255 in field(psi, n, 'collapse')} for n in RINGS} for psi in OBS}
    ok5 = all(not v['named_missing_from_K'] for d in q5.values() for v in d.values()) and all(q5['200'][str(n)]['255_in_K'] for n in RINGS) \
        and all(q5[str(p)][str(n)]['255_in_Z'] and not q5[str(p)][str(n)]['255_in_K'] for p in (32, 22) for n in RINGS)
    P['Q5_named_commuters_and_collapses'] = {'by_ring': q5, 'pass': ok5}
    iff = all((field(psi, n, 'h_star')[str(r)] == 0) == (r in field(psi, n, 'closed')) for psi in OBS for n in RINGS for r in range(256))
    hist = {str(psi): {str(n): {str(k): int(v) for k, v in zip(*np.unique(list(field(psi, n, 'h_star').values()), return_counts=True))} for n in RINGS} for psi in OBS}
    mx = {str(psi): {str(n): max(field(psi, n, 'h_star').values()) for n in RINGS} for psi in OBS}
    annex = {str(psi): {str(n): analyse(n, psi, rules=ANNEX[psi], full=False)['h_star'] for n in ANNEX_RINGS} for psi in ANNEX}
    annex_bet = max(annex['232']['16'].values()) > 16
    P['Q6_history_census_and_annex'] = {'h_star_zero_iff_closed': iff, 'histogram': hist, 'max': mx,
                                        'rules_at_max': {str(psi): {str(n): [r for r in range(256) if field(psi, n, 'h_star')[str(r)] == mx[str(psi)][str(n)]] for n in RINGS} for psi in OBS},
                                        'annex_depths': annex, 'annex_bet_majority_max_at_16_exceeds_16': annex_bet, 'pass': iff and annex_bet}
    def tab(psi, n, r): return (r in field(psi, n, 'closed'), r in field(psi, n, 'commuters'), r in field(psi, n, 'collapse'), r in field(psi, n, 'residual'), field(psi, n, 'h_star')[str(r)])
    refl = {str(psi): all(tab(psi, n, r) == tab(psi, n, mirror(r)) for n in RINGS for r in range(256)) for psi in OBS}
    refl_part = {str(psi): all(sorted(sorted(mirror(r) for r in c) for c in field(psi, n, 'equivalence_partition')) == field(psi, n, 'equivalence_partition') for n in RINGS) for psi in OBS}
    cov = {str(psi): all(tab(psi, n, r) == tab(OBS[psi], n, conj(r)) for n in RINGS for r in range(256)) for psi in OBS}
    cov_class = {str(psi): all(sorted(conj(r) for r in cls_of(psi, n, 255 - psi)) == cls_of(OBS[psi], n, 255 - OBS[psi]) for n in RINGS) for psi in OBS}
    inv = {str(psi): {str(n): field(psi, n, 'closed') == field(OBS[psi], n, 'closed') for n in RINGS} for psi in OBS}
    P['Q7_symmetries'] = {'reflection_invariant': refl, 'reflection_invariant_partition': refl_part, 'complement_covariant': cov, 'complement_covariant_class': cov_class,
                          'complement_invariant_outright': inv, 'pass': all(refl.values()) and all(refl_part.values()) and all(cov.values()) and all(cov_class.values())}
    census = {str(psi): {str(n): {k: T[psi][str(n)][k] for k in ('image_size', 'image_fraction', 'max_fiber', 'closed', 'commuters', 'collapse', 'residual')} for n in RINGS} for psi in T}
    report = {'protocol': 'complement-observation-20260911', 'schema': 1, 'cadence': 1, 'observations': list(OBS), 'conjugates': OBS, 'rings': list(RINGS),
              'source_hashes': {'script': sha(pathlib.Path(__file__)), 'block_majority_result': sha(MAJORITY), 'isolated_cell_result': sha(ISOLATED)},
              'census': census, 'h_star': {str(psi): {str(n): field(psi, n, 'h_star') for n in RINGS} for psi in OBS},
              'factors_residual_n12': {str(psi): field(psi, 12, 'factors_residual') for psi in OBS},
              'equivalence_partition_n12': {str(psi): field(psi, 12, 'equivalence_partition') for psi in OBS},
              'word_partitions': {str(psi): word_partition[psi] for psi in word_partition},
              'predictions': P, 'summary': {k: v.get('pass', 'reported') for k, v in P.items()}}
    OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False, default=jsonable) + '\n')
    print(json.dumps(report['summary']))
    for psi in OBS: print(psi, 'C', len(field(psi, 12, 'closed')), 'K', field(psi, 12, 'commuters'), 'Z', len(field(psi, 12, 'collapse')), 'X', field(psi, 12, 'residual'), 'class of comp', cls_of(psi, 12, 255 - psi))
    print('max h*', mx); print('annex', annex); print('written', OUT.relative_to(ROOT))

if __name__ == '__main__':
    main()
