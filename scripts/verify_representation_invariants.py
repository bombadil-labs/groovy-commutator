#!/usr/bin/env python3
"""Representation invariants audit (protocol frozen 2026-09-10, unrun at commit).

Correction 2026-09-11 after retrospective review (PR #80): adds the exhaustive
five-cell local check that supplies the proof route for the self-duality iff (P3),
separates P5 K-cell counts into identical / differing-both-finite / censored /
exceeding-h (the original 22-entry flagged list is retained verbatim), and scores
P6's boundary-concentration clause numerically instead of leaving it unscored.

Audits six existing ECA claims against complement conjugation T_c, reflection
T_m, and their composite, as declared in
docs/research/protocols/representation-invariants-audit-20260910.md.
Every prediction in that protocol is evaluated and reported as pass/fail;
every violation is listed. Reads two saved result files; recomputes nothing
that they contain.

Conventions: cell i has neighbors (i-1, i, i+1) mod n; rule bit index is
4*l + 2*c + r (groovy.ca.rule_lut); ring states are enumerated with cell 0 as
the most significant bit. Batched stepping rolls along axis 1 and is checked
against groovy.ca.apply_rule on every ring size used.
"""
from __future__ import annotations
import hashlib, itertools, json, pathlib, sys
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from groovy.ca import apply_rule, rule_lut  # noqa: E402

CENSUS = ROOT / 'results/local_correction_caps_20260910.json'
SWEEP = ROOT / 'results/sweep_full_classified.parquet'
OUT = ROOT / 'results/representation_invariants_20260910.json'
ZERO_G = {0, 4, 60, 90, 102, 150, 170, 200, 204, 240}
ONE_G = {15, 51, 85, 105, 153, 165, 195, 255}
RINGS = (6, 8, 10)

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def lut(r): return rule_lut(r)
def conj(r):
    """complement conjugation: r~(l,m,r) = NOT r(NOT l, NOT m, NOT r)."""
    t = lut(r); return sum((1 - int(t[7 - i])) << i for i in range(8))
def mirror(r):
    t = lut(r); out = 0
    for i in range(8):
        l, m, rr = (i >> 2) & 1, (i >> 1) & 1, i & 1
        out |= int(t[4 * rr + 2 * m + l]) << i
    return out
def step(S, r):
    """batched synchronous step on rows of S (shape (k, n))."""
    t = lut(r); return t[4 * np.roll(S, 1, axis=1) + 2 * S + np.roll(S, -1, axis=1)]
def D(S, r): return S ^ step(S, r)
def G(S, r): return D(step(S, r), r) ^ step(D(S, r), r)
def all_states(n):
    k = np.arange(2 ** n, dtype=np.int64)
    return ((k[:, None] >> (n - 1 - np.arange(n))) & 1).astype(np.uint8)

def g_class(r):
    """commutator class from exhaustive five-cell causal windows (established result 1)."""
    t = lut(r); vals = set()
    for w in itertools.product((0, 1), repeat=5):
        f = lambda row: tuple(int(t[4 * a + 2 * b + c]) for a, b, c in zip(row, row[1:], row[2:]))
        d = lambda row: tuple(x ^ y for x, y in zip(row[1:-1], f(row)))
        vals.add(d(f(w))[0] ^ f(d(w))[0])
    return 'zero' if vals == {0} else 'one' if vals == {1} else 'varying'

def main():
    report = {'protocol': 'representation-invariants-audit-20260910', 'schema': 1,
              'source_hashes': {'script': sha(pathlib.Path(__file__)), 'local_correction_caps': sha(CENSUS), 'sweep_full_classified': sha(SWEEP)},
              'transformations': {'T_c': 'S -> NOT S, r -> conj(r)', 'T_m': 'S -> reverse(S), r -> mirror(r)', 'T_cm': 'both'},
              'costs': {'T_c': {'touched_sites': 'n', 'information': 0, 'locality': 0}, 'T_m': {'touched_sites': 0, 'information': 0, 'locality': 0}},
              'predictions': {}, 'engine_control': {}}
    P = report['predictions']
    # engine control: batched step == groovy.ca.apply_rule row by row
    for n in RINGS:
        S = all_states(n); r = 110
        ok = all(np.array_equal(step(S[i:i+1], r)[0], apply_rule(S[i], r)) for i in range(0, 2 ** n, max(1, 2 ** n // 64)))
        report['engine_control'][n] = bool(ok); assert ok
    # intertwining control: F_{T r}(T S) == T F_r(S) for all rules at n=8
    S = all_states(8)
    inter = all(np.array_equal(step(1 - S, conj(r)), 1 - step(S, r)) and np.array_equal(step(S[:, ::-1], mirror(r)), step(S, r)[:, ::-1]) for r in range(256))
    report['engine_control']['intertwining_n8_all_rules'] = bool(inter); assert inter

    # --- P1/P2: commutator classification
    cls = {r: g_class(r) for r in range(256)}
    Z = {r for r, c in cls.items() if c == 'zero'}; U = {r for r, c in cls.items() if c == 'one'}
    report['result1_control'] = {'zero_matches': Z == ZERO_G, 'one_matches': U == ONE_G}
    p1_viol = [r for r in range(256) if cls[mirror(r)] != cls[r]]
    P['P1_class_reflection_preserved'] = {'predicted': 'all 256 preserved', 'violations': p1_viol, 'pass': not p1_viol}
    pred_img = {0: 255, 255: 0, 60: 195, 195: 60, 90: 165, 165: 90, 102: 153, 153: 102, 4: 223, 200: 236}
    fixed = {150, 170, 204, 240, 15, 51, 85, 105}
    img_ok = all(conj(a) == b for a, b in pred_img.items()) and all(conj(r) == r for r in fixed)
    conj_Z = {conj(r) for r in ZERO_G}; conj_U = {conj(r) for r in ONE_G}
    leave = sorted(r for r in conj_Z | conj_U if cls[r] == 'varying')
    P['P2_class_complement_not_preserved'] = {
        'predicted_images_hold': img_ok, 'T_c(Z)': sorted(conj_Z), 'T_c(U)': sorted(conj_U),
        'T_c(Z) ∩ Z': sorted(conj_Z & ZERO_G), 'predicted_intersection': [150, 170, 204, 240],
        'rules_leaving_Z∪U': leave, 'predicted_leaving': [223, 236],
        'class_of_223_236': {223: cls[223], 236: cls[236]},
        'pass': img_ok and sorted(conj_Z & ZERO_G) == [150, 170, 204, 240] and leave == [223, 236]}

    # --- P3: pointwise covariance
    self_dual = sorted(r for r in range(256) if conj(r) == r)
    p3 = {'self_dual_rules': self_dual, 'self_dual_count': len(self_dual), 'by_ring': {}}
    for n in RINGS:
        S = all_states(n); nS = 1 - S; rS = S[:, ::-1]
        m_ok = [r for r in range(256) if not np.array_equal(G(rS, mirror(r)), G(S, r)[:, ::-1])]
        c_pass = [r for r in range(256) if np.array_equal(G(nS, conj(r)), G(S, r))]
        st_fail = []
        for r in range(256):
            rc = conj(r); d = D(nS, rc)
            g_st = D(step(nS, rc), rc) ^ (1 - step(1 - d, rc))
            if not np.array_equal(g_st, G(S, r)): st_fail.append(r)
        p3['by_ring'][n] = {'mirror_violations': m_ok, 'complement_native_pass': c_pass,
                            'complement_native_pass_equals_self_dual': c_pass == self_dual,
                            'spurious_passes_non_self_dual': sorted(set(c_pass) - set(self_dual)),
                            'complement_state_transport_violations': st_fail}
    # exhaustive local route: the defect F(x) XOR NOT F(NOT x) at x = D(S) has radius 2, so
    # five-cell source words decide the iff for every rule (added 2026-09-11 after review).
    local_pass = []
    for r in range(256):
        t = lut(r); ok = True
        for w in itertools.product((0, 1), repeat=5):
            fw = [int(t[4 * a + 2 * b + c]) for a, b, c in zip(w, w[1:], w[2:])]
            x = [a ^ b for a, b in zip(w[1:-1], fw)]
            fx = int(t[4 * x[0] + 2 * x[1] + x[2]]); fnx = int(t[4 * (1 - x[0]) + 2 * (1 - x[1]) + (1 - x[2])])
            if fx ^ (1 - fnx): ok = False; break
        if ok: local_pass.append(r)
    p3['local_five_cell_check'] = {'passing_rules': local_pass, 'equals_self_dual': local_pass == self_dual,
                                   'note': 'proof route for the iff: defect radius 2, all 32 five-cell words, all 256 rules'}
    p3['pass'] = all(not v['mirror_violations'] and v['complement_native_pass_equals_self_dual'] and not v['complement_state_transport_violations'] for v in p3['by_ring'].values()) and p3['local_five_cell_check']['equals_self_dual']
    p3['predicted'] = 'mirror: all; complement native: exactly self-dual (16); complement state-transport: all'
    P['P3_pointwise_covariance'] = p3

    # --- P4: derivative-observation closure
    def closed(r, S):
        d = D(S, r); dn = D(step(S, r), r)
        keys = {}
        for a, b in zip(map(bytes, d), map(bytes, dn)):
            if keys.setdefault(a, b) != b: return False
        return True
    p4 = {'by_ring': {}}
    for n in RINGS:
        S = all_states(n); cl = {r: closed(r, S) for r in range(256)}
        viol = {T: [r for r in range(256) if cl[f(r)] != cl[r]] for T, f in (('T_c', conj), ('T_m', mirror), ('T_cm', lambda r: conj(mirror(r))))}
        p4['by_ring'][n] = {'closed_rules': sorted(r for r in range(256) if cl[r]), 'violations': viol}
    p4['pass'] = all(not v for ring in p4['by_ring'].values() for v in ring['violations'].values())
    p4['predicted'] = 'preserved under all three at every ring'
    P['P4_derivative_closure_preserved'] = p4

    # --- P5: local-cap census under T_m and T_c (saved file only)
    census = json.loads(CENSUS.read_text())
    passes = {(e['rule'], e['kind'], e['h'], e['R']): e['pass'] for e in census['records']}
    mpr = {e['rule']: e for e in census['minimum_passing_radius']}
    m_viol = [k for k, v in passes.items() if passes[(mirror(k[0]),) + k[1:]] != v]
    c_viol = []
    for r in range(256):
        for h in range(3):
            a, b = mpr[r]['K'][h], mpr[conj(r)]['K'][h]
            if (a is None) != (b is None) or (a is not None and abs(a - b) > h): c_viol.append({'rule': r, 'conj': conj(r), 'h': h, 'mpr_r': a, 'mpr_conj': b})
    c_exact = sum(1 for r in range(256) for h in range(3) if mpr[r]['K'][h] == mpr[conj(r)]['K'][h])
    # 2026-09-11 correction: classify every K cell; the flagged list above mixes genuine
    # violations with right-censored minima (one side outside the R<=2 budget).
    cells = {'identical': 0, 'differ_both_finite': 0, 'censored_one_side': 0, 'differ_both_finite_exceeding_h': 0}
    genuine, censored = [], []
    for r in range(256):
        for h in range(3):
            a, b = mpr[r]['K'][h], mpr[conj(r)]['K'][h]
            if a == b: cells['identical'] += 1
            elif a is None or b is None: cells['censored_one_side'] += 1; censored.append({'rule': r, 'conj': conj(r), 'h': h, 'mpr_r': a, 'mpr_conj': b})
            else:
                cells['differ_both_finite'] += 1
                if abs(a - b) > h: cells['differ_both_finite_exceeding_h'] += 1; genuine.append({'rule': r, 'conj': conj(r), 'h': h, 'mpr_r': a, 'mpr_conj': b})
    P['P5_local_cap_census'] = {'budgets': len(passes), 'mirror_violations': m_viol, 'mirror_pass': not m_viol,
                                'complement_K_radius_bound_violations': c_viol, 'complement_K_pass': not c_viol,
                                'complement_K_min_radius_exactly_equal': c_exact, 'of': 768,
                                'complement_K_cell_classification': cells, 'complement_K_genuine_violations': genuine,
                                'complement_K_censored_cells': censored,
                                'flagged_list_note': 'complement_K_radius_bound_violations is the original 22-entry flagged list (4 genuine + 18 censored), retained as the selected domain of the extension',
                                'predicted': 'mirror: all 4,608 equal; complement K: |mpr(r)-mpr(conj r)| <= h and same pass/fail existence',
                                'pass': not m_viol and not c_viol}

    # --- P6: sweep regime labels (sampled seeds; approximate invariance expected)
    import pandas as pd
    df = pd.read_parquet(SWEEP)
    rows = {(int(a), int(b)): (reg, float(fi), float(pk)) for a, b, reg, fi, pk in zip(df.rule_a, df.rule_b, df.regime, df.final, df.peak)}
    labels = sorted(set(df.regime))
    p6 = {'pairs': len(rows), 'by_transformation': {}}
    for T, f in (('T_m', mirror), ('T_c', conj)):
        agree = 0; final_eq = 0; peak_eq = 0; commute_agree = 0; commute_n = 0
        conf = {a: {b: 0 for b in labels} for a in labels}
        for (a, b), (reg, fi, pk) in rows.items():
            ia, ib = sorted((f(a), f(b)))
            if (ia, ib) not in rows: continue
            reg2, fi2, pk2 = rows[(ia, ib)]
            agree += reg == reg2; final_eq += fi == fi2; peak_eq += pk == pk2; conf[reg][reg2] += 1
            if reg == 'commute' or reg2 == 'commute': commute_n += 1; commute_agree += reg == reg2
        labs = labels
        disagreements = sum(conf[x][y] for x in labs for y in labs if x != y)
        named = sum(conf[x][y] + conf[y][x] for x, y in (('drain', 'crystalline'), ('structured', 'noisy')))
        by_pair = {f'{x}/{y}': conf[x][y] + conf[y][x] for x in labs for y in labs if x < y and conf[x][y] + conf[y][x]}
        p6['by_transformation'][T] = {'label_agreement': agree / len(rows),
                                     'boundary_clause': {'disagreements': disagreements, 'on_drain_crystalline_or_structured_noisy': named,
                                                         'fraction': named / disagreements if disagreements else None, 'by_unordered_pair': by_pair}, 'final_exact_equal': final_eq / len(rows), 'peak_exact_equal': peak_eq / len(rows),
                                     'confusion': conf, 'commute_agreement': commute_agree / max(1, commute_n), 'commute_pairs_involved': commute_n}
    p6['pass_agreement_above_0.90'] = all(v['label_agreement'] > 0.90 for v in p6['by_transformation'].values())
    p6['pass_commute_exact'] = all(v['commute_agreement'] == 1.0 for v in p6['by_transformation'].values())
    p6['boundary_concentration_clause'] = {'scored': True, 'supported': False,
        'note': 'the frozen clause had no threshold; the two named boundaries carry under 30% of disagreements and two unnamed boundaries (crystalline/structured, noisy/structured) are populated; scored 2026-09-11 after review'}
    p6['predicted'] = 'agreement > 0.90; commute labels agree exactly; disagreements on soft boundaries'
    P['P6_sweep_regime_labels'] = p6

    report['summary'] = {k: v.get('pass', None) for k, v in P.items()}
    report['summary']['P6_sweep_regime_labels'] = {'agreement': p6['pass_agreement_above_0.90'], 'commute_exact': p6['pass_commute_exact'], 'boundary_concentration': False}
    OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False, default=int) + '\n')
    print(json.dumps(report['summary'], indent=1)); print('written', OUT.relative_to(ROOT))

if __name__ == '__main__':
    main()
