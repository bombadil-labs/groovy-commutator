#!/usr/bin/env python3
"""Parity coarse-graining audit (protocol frozen 2026-09-11, reviewed by Codex at
revision 9997462 before this implementation; see the protocol's Section 5).

T_pi: pi(S)_i = S_i XOR S_{i+1}, elementary rule 102 applied once as an
observation at cadence q = 1. Fibers are the complement pairs {S, not S}.

C1  factor closure under pi, per ring size; predicted set for n >= 6: the 32
    constant-complement-response rules (16 complement-invariant, 16 self-dual).
C2  the factor B of each closed rule is elementary; extracted on the n = 8 image
    and compared with the frozen formula; rule 90 fixed; affine -> linear;
    nonlinear -> nonlinear.
C3  pi o G_r = G_B o pi on rings 8 and 10 (theorem control); result-1 class of B.
C4  h_* and split counts for all 256 rules at n in {6, 8, 10, 12}: each initial
    complement pair counted once (S_0 = 0 fixes the source bit); a pair separates
    first at t >= 1 when F^t S XOR F^t (not S) is neither all-zero nor all-one;
    equality is absorbing and never separates; a pair still unsplit after 2^{n+1}
    steps is periodic (count over unsplit ordered pairs) and never separates.
C5  closed set == first audit's self-dual set  union  complement-invariant set.
"""
from __future__ import annotations
import hashlib, json, pathlib
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'results/representation_invariants_20260910.json'
OUT = ROOT / 'results/parity_coarse_graining_20260911.json'
C1_RINGS_PREDICTED = (6, 8, 10, 12); C1_RINGS_REPORTED = (4, 5); C3_RINGS = (8, 10); C4_RINGS = (6, 8, 10, 12)
ZERO_G = {0, 4, 60, 90, 102, 150, 170, 200, 204, 240}          # established result 1
ONE_G = {15, 51, 85, 105, 153, 165, 195, 255}
AFFINE = {0, 15, 51, 60, 85, 90, 102, 105, 150, 153, 165, 170, 195, 204, 240, 255}

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def all_states(n):
    k = np.arange(2 ** n, dtype=np.int64); return ((k[:, None] >> (n - 1 - np.arange(n))) & 1).astype(np.uint8)
def lut(r): return np.array([(r >> i) & 1 for i in range(8)], dtype=np.uint8)
def step(S, r):
    t = lut(r); return t[4 * np.roll(S, 1, axis=1) + 2 * S + np.roll(S, -1, axis=1)]
def pi(S): return S ^ np.roll(S, -1, axis=1)
def D(S, r): return S ^ step(S, r)
def G(S, r): return D(step(S, r), r) ^ step(D(S, r), r)
def response(r):                      # g_r(l,m,r) = r(l,m,r) XOR r(~l,~m,~r), indexed 4l+2m+r
    t = lut(r); return [int(t[i] ^ t[7 - i]) for i in range(8)]
def anf(table):                       # algebraic normal form of a 3-input table (Moebius transform)
    a = list(table)
    for bit in (1, 2, 4):
        for i in range(8):
            if i & bit: a[i] ^= a[i ^ bit]
    return a                          # a[m] = coefficient of the monomial with mask m (4=l, 2=m, 1=r)
def degree(table): return max([bin(m).count('1') for m in range(8) if anf(table)[m]] or [0])
def is_linear(table): a = anf(table); return bool(degree(table) <= 1 and a[0] == 0)
def jsonable(o):                      # serialization patch 2026-09-11: the first run computed fully, then failed on a numpy bool
    if isinstance(o, (np.bool_,)): return bool(o)
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.floating): return float(o)
    raise TypeError(type(o))

CI = [r for r in range(256) if all(v == 0 for v in response(r))]
SD = [r for r in range(256) if all(v == 1 for v in response(r))]
PREDICTED_CLOSED = sorted(CI + SD)

def closed_rules(n):
    S = all_states(n); out = []
    for r in range(256):
        if np.array_equal(pi(step(S, r)), pi(step(1 - S, r))): out.append(r)
    return out

def extract_factor(r, n=8):
    """B on the image: B(pi S) = pi F S. Then read a radius-1 table off every site of every image state."""
    S = all_states(n); Y = pi(S); Z = pi(step(S, r))
    code = 4 * np.roll(Y, 1, axis=1) + 2 * Y + np.roll(Y, -1, axis=1)
    table = [None] * 8; consistent = True
    for c in range(8):
        vals = np.unique(Z[code == c])
        if len(vals) == 0: return None, 'code unseen'
        if len(vals) > 1: consistent = False
        table[c] = int(vals[0])
    if not consistent: return None, 'not radius-1'
    return sum(table[c] << c for c in range(8)), 'ok'

def formula_factor(r):
    t = lut(r); q = lambda a, b: int(t[4 * a + b])       # m = 0 representative of the pair
    sd = r in SD
    table = [(q(l, m) ^ q(m, rr) ^ (m if sd else 0)) for (l, m, rr) in [((c >> 2) & 1, (c >> 1) & 1, c & 1) for c in range(8)]]
    return sum(table[c] << c for c in range(8))

def result1_class(rule, n=8):
    g = G(all_states(n), rule)
    if not g.any(): return 'zero'
    if g.all(): return 'one'
    return 'varies'

def refinement(r, n):
    """First separation times for all complement pairs, S_0 = 0. Returns h_*, split count, pairs absorbed as equal."""
    S = all_states(n); S = S[S[:, 0] == 0]                    # 2^{n-1} pairs, each once
    X = S.copy(); Y = 1 - S; alive = np.ones(len(S), dtype=bool)
    first_split = np.zeros(len(S), dtype=np.int64); became_equal = np.zeros(len(S), dtype=bool)
    bound = 2 ** (n + 1); t = 0; termination = 'all_resolved'
    while alive.any():
        if t >= bound: termination = 'bound_reached_periodic'; break
        t += 1
        X[alive] = step(X[alive], r); Y[alive] = step(Y[alive], r)
        d = X[alive] ^ Y[alive]; s = d.sum(axis=1)
        eq = s == 0; comp = s == n; split = ~(eq | comp)
        idx = np.flatnonzero(alive)
        first_split[idx[split]] = t; became_equal[idx[eq]] = True
        alive[idx[split | eq]] = False                             # equality is absorbing; split is final
    return {'h_star': int(first_split.max()), 'split_count': int((first_split > 0).sum()), 'pairs': int(len(S)),
            'split_fraction': float((first_split > 0).sum() / len(S)), 'became_equal': int(became_equal.sum()),
            'stayed_complementary': int((alive).sum()), 'steps_run': int(t), 'termination': termination}

def main():
    audit = json.loads(AUDIT.read_text())
    report = {'protocol': 'parity-coarse-graining-20260911', 'schema': 1, 'cadence': 1,
              'source_hashes': {'script': sha(pathlib.Path(__file__)), 'representation_invariants_audit': sha(AUDIT)},
              'transformation': {'map': 'pi(S)_i = S_i xor S_{i+1} (rule 102 as an observation)', 'fibers': '{S, not S}', 'forward_radius': 1,
                                 'inverse': 'none; right-inverse fixes an anchor and is non-local', 'information_lost_bits_per_ring': 1,
                                 'information_note': 'log2 of the fiber size (uniform-prior conditional entropy), not an assertion for every prior'},
              'complement_invariant_rules': CI, 'self_dual_rules': SD, 'predicted_closed_set': PREDICTED_CLOSED}
    P = {}
    # C1
    c1 = {'by_ring': {}, 'predicted_rings': list(C1_RINGS_PREDICTED), 'reported_rings': list(C1_RINGS_REPORTED)}
    for n in C1_RINGS_REPORTED + C1_RINGS_PREDICTED:
        cl = closed_rules(n)
        c1['by_ring'][str(n)] = {'closed': cl, 'count': len(cl), 'equals_predicted': cl == PREDICTED_CLOSED,
                                 'extra_over_predicted': sorted(set(cl) - set(PREDICTED_CLOSED)), 'missing_from_predicted': sorted(set(PREDICTED_CLOSED) - set(cl))}
    c1['pass'] = all(c1['by_ring'][str(n)]['equals_predicted'] for n in C1_RINGS_PREDICTED)
    P['C1_closure_classification'] = c1
    closed8 = c1['by_ring']['8']['closed']
    # C2
    factors = {}; c2_viol = []
    for r in closed8:
        b, status = extract_factor(r); f = formula_factor(r)
        rec = {'extracted': b, 'status': status, 'formula': f, 'agrees': b == f, 'kind': 'complement_invariant' if r in CI else 'self_dual',
               'factor_linear': is_linear(lut(f)) if f is not None else None, 'factor_degree': degree(lut(f)) if f is not None else None,
               'rule_affine': r in AFFINE, 'fixed_point': b == r}
        factors[str(r)] = rec
        if not rec['agrees']: c2_viol.append(r)
    c2 = {'factor_by_rule': factors, 'extraction_or_formula_violations': c2_viol,
          'rule90_maps_to_90': factors.get('90', {}).get('extracted') == 90,
          'affine_rules_in_closed_set': sorted(AFFINE) == sorted(set(AFFINE) & set(closed8)),
          'affine_to_linear': all(factors[str(r)]['factor_linear'] for r in closed8 if r in AFFINE),
          'nonlinear_to_nonlinear': all(factors[str(r)]['factor_degree'] == 2 for r in closed8 if r not in AFFINE),
          'fixed_points': sorted(r for r in closed8 if factors[str(r)]['fixed_point']),
          'factor_image': sorted(set(factors[str(r)]['extracted'] for r in closed8)),
          'factor_map_injective': len(set(factors[str(r)]['extracted'] for r in closed8)) == len(closed8)}
    c2['pass'] = not c2_viol and c2['rule90_maps_to_90'] and c2['affine_rules_in_closed_set'] and c2['affine_to_linear'] and c2['nonlinear_to_nonlinear']
    P['C2_factor_is_elementary'] = c2
    # C3
    c3 = {'by_ring': {}, 'factor_class': {}}
    for n in C3_RINGS:
        S = all_states(n); bad = []
        for r in closed8:
            b = factors[str(r)]['extracted']
            if not np.array_equal(pi(G(S, r)), G(pi(S), b)): bad.append(r)
        c3['by_ring'][str(n)] = {'covariance_violations': bad}
    for r in closed8:
        b = factors[str(r)]['extracted']
        c3['factor_class'][str(r)] = {'factor': b, 'rule_class': 'zero' if r in ZERO_G else 'one' if r in ONE_G else 'varies',
                                      'factor_class_n8': result1_class(b, 8), 'factor_class_n10': result1_class(b, 10),
                                      'factor_in_result1_sets': 'zero' if b in ZERO_G else 'one' if b in ONE_G else 'varies'}
    c3['one_G_rules_all_closed'] = ONE_G <= set(closed8)
    c3['one_G_factors_zero_everywhere'] = all(c3['factor_class'][str(r)]['factor_class_n8'] == 'zero' and c3['factor_class'][str(r)]['factor_class_n10'] == 'zero' for r in ONE_G)
    c3['nonlinear_factors_vary'] = all(c3['factor_class'][str(r)]['factor_class_n8'] == 'varies' for r in closed8 if r not in AFFINE)
    c3['factor_classes_match_result1_sets'] = all(v['factor_class_n8'] == v['factor_in_result1_sets'] for v in c3['factor_class'].values())
    c3['pass'] = all(not v['covariance_violations'] for v in c3['by_ring'].values()) and c3['one_G_rules_all_closed'] and c3['one_G_factors_zero_everywhere'] and c3['nonlinear_factors_vary']
    P['C3_commutator_covariance'] = c3
    # C4
    c4 = {'by_ring': {}, 'pair_counting': 'S_0 = 0, each complement pair once; denominator 2^(n-1)', 'bound': '2^(n+1) steps over unsplit ordered pairs'}
    per_rule = {str(r): {} for r in range(256)}
    for n in C4_RINGS:
        zero_set = []
        for r in range(256):
            rec = refinement(r, n); per_rule[str(r)][str(n)] = rec
            if rec['h_star'] == 0: zero_set.append(r)
        closed_n = c1['by_ring'][str(n)]['closed']
        c4['by_ring'][str(n)] = {'h_star_zero_set': zero_set, 'equals_closed_set': zero_set == closed_n,
                                 'max_h_star': max(per_rule[str(r)][str(n)]['h_star'] for r in range(256)),
                                 'terminations': {k: sum(1 for r in range(256) if per_rule[str(r)][str(n)]['termination'] == k) for k in ('all_resolved', 'bound_reached_periodic')},
                                 'h_star_histogram': {}}
        hist = {}
        for r in range(256): h = per_rule[str(r)][str(n)]['h_star']; hist[h] = hist.get(h, 0) + 1
        c4['by_ring'][str(n)]['h_star_histogram'] = {str(k): v for k, v in sorted(hist.items())}
    for r in range(256):
        hs = [per_rule[str(r)][str(n)]['h_star'] for n in C4_RINGS]
        per_rule[str(r)]['h_star_by_n'] = hs; per_rule[str(r)]['h_star_nondecreasing_in_n'] = all(a <= b for a, b in zip(hs, hs[1:]))
        per_rule[str(r)]['split_fraction_by_n'] = [per_rule[str(r)][str(n)]['split_fraction'] for n in C4_RINGS]
    c4['per_rule'] = per_rule
    c4['nondecreasing_count'] = sum(1 for r in range(256) if per_rule[str(r)]['h_star_nondecreasing_in_n'])
    c4['nondecreasing_count_nonclosed'] = sum(1 for r in range(256) if r not in closed8 and per_rule[str(r)]['h_star_nondecreasing_in_n'])
    c4['pass'] = all(v['equals_closed_set'] for v in c4['by_ring'].values())
    P['C4_refinement_census'] = c4
    # C5
    audit_sd = audit['predictions']['P3_pointwise_covariance']['self_dual_rules']
    c5 = {'audit_self_dual': audit_sd, 'audit_self_dual_equals_local': audit_sd == SD,
          'closed_equals_union': closed8 == sorted(set(audit_sd) | set(CI)), 'union_size': len(set(audit_sd) | set(CI))}
    c5['pass'] = c5['audit_self_dual_equals_local'] and c5['closed_equals_union']
    P['C5_relation_to_first_audit'] = c5
    report['predictions'] = P
    report['summary'] = {k: v['pass'] for k, v in P.items()}
    OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False, default=jsonable) + '\n')
    print(json.dumps(report['summary']))
    print('closed per ring:', {n: c1['by_ring'][str(n)]['count'] for n in C1_RINGS_REPORTED + C1_RINGS_PREDICTED})
    print('fixed points:', c2['fixed_points'], 'factor image size:', len(c2['factor_image']))
    print('C4 max h* per ring:', {n: c4['by_ring'][str(n)]['max_h_star'] for n in C4_RINGS}, 'terminations:', {n: c4['by_ring'][str(n)]['terminations'] for n in C4_RINGS})
    print('written', OUT.relative_to(ROOT))

if __name__ == '__main__':
    main()
