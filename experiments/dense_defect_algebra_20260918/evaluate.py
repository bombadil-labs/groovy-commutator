#!/usr/bin/env python3
"""Frozen analysis for the dense defect algebra. Committed before the run.

Scoring note declared before any data exists: P1 references the exact residual
`1 - 2*N_ap(x0)/W`. For U++ the disagreement field IS the anti-phase set, so
the row's own `mean_antiphase_pairs` reproduces `agree` exactly and the test is
the integer identity. For U+ the field is not that set and each completion has
its own x0, so there is no matched reference; P1(b) is therefore scored against
the formula's density-1/2 expectation 0.9375, and the per-base U++ median is
reported alongside it. This is a faithful reading of the frozen clause, fixed
here before the run, not a post hoc choice.
"""
from __future__ import annotations
import json, math, statistics as st
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / 'results/dense_defect_algebra_20260918'
BASES = [110, 54, 22, 5, 30, 90, 0, 204, 106, 232, 8, 18, 46, 33, 62, 29, 51, 37, 45, 27]
FROZEN_BASES = [0, 204, 232, 8]
ARMS = ['Upp', 'Uplus', 'Dplus', 'G', 'Gprime', 'K', 'random']
W = 521
EXPECTED = 1 - 1/16

def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    a, b = a[ok], b[ok]
    if len(a) < 3: return None
    def rank(v):
        o = np.argsort(v, kind='mergesort'); r = np.empty(len(v), float); r[o] = np.arange(len(v))
        # average ties
        for val in np.unique(v):
            m = v == val
            if m.sum() > 1: r[m] = r[m].mean()
        return r
    ra, rb = rank(a), rank(b)
    ra, rb = ra - ra.mean(), rb - rb.mean()
    d = math.sqrt((ra*ra).sum() * (rb*rb).sum())
    return float((ra*rb).sum()/d) if d else None

def main():
    rows = json.loads((RES/'rows.json').read_text())['rows']
    pis = json.loads((RES/'pairs.json').read_text())['pi']
    alg = json.loads((RES/'algebra.json').read_text())
    bb = alg['base_bits']

    by = {}
    for r in rows:
        by.setdefault((int(r['base']), r['arm']), []).append(r)

    per = {}
    for b in BASES:
        e = {}
        for arm in ARMS:
            rs = by.get((b, arm), [])
            if not rs: continue
            ag = [float(x['agree']) for x in rs]
            e[arm] = {'n': len(rs), 'median_agree': float(st.median(ag)),
                      'mean_agree': float(np.mean(ag)),
                      'P_on': float(np.mean([x['on_beam'] for x in rs])),
                      'P_off': float(np.mean([x['off_beam'] for x in rs])),
                      'median_nap': float(st.median([float(x['mean_antiphase_pairs']) for x in rs])),
                      'strata_column_steps': [int(np.mean([x['strata_column_steps'][i] for x in rs])) for i in range(3)],
                      'strata_survival': [int(np.mean([x['strata_one_step_survival'][i] for x in rs])) for i in range(3)]}
            tx = [x['T_ext'] for x in rs if 'T_ext' in x]
            if tx: e[arm]['mean_T_ext'] = float(np.mean(tx))
        upp = by.get((b, 'Upp'), [])
        e['rho'] = float(np.mean([1 - float(x['agree']) for x in upp])) if upp else None
        e['beta'] = bb[str(b)]['beta']; e['beta_count'] = sum(bb[str(b)]['beta'])
        e['e_G'] = bb[str(b)]['e_G']; e['e_Gprime'] = bb[str(b)]['e_Gprime']
        e['totalistic'] = bb[str(b)]['totalistic']
        e.update(pis[str(b)])
        per[b] = e

    rho = [per[b]['rho'] for b in BASES]
    pi512 = [per[b]['Pi_512'] for b in BASES]
    betac = [per[b]['beta_count'] for b in BASES]
    eG = [per[b]['e_G'] for b in BASES]
    eGp = [per[b]['e_Gprime'] for b in BASES]
    Gmed = [per[b].get('G', {}).get('median_agree') for b in BASES]
    Gpmed = [per[b].get('Gprime', {}).get('median_agree') for b in BASES]
    rmed = [per[b].get('random', {}).get('median_agree') for b in BASES]
    Kon = [per[b].get('K', {}).get('P_on') for b in BASES]

    cor = {'rho_vs_Pi512': spearman(rho, pi512), 'rho_vs_beta': spearman(rho, betac),
           'G_vs_eG': spearman(Gmed, eG), 'G_vs_eGprime': spearman(Gmed, eGp),
           'Gprime_vs_eGprime': spearman(Gpmed, eGp), 'Gprime_vs_eG': spearman(Gpmed, eG),
           'random_vs_beta': spearman(rmed, betac), 'random_vs_Pi512': spearman(rmed, pi512),
           'K_on_vs_Pi512': spearman(Kon, pi512), 'Upp_on_vs_Pi512':
               spearman([per[b]['Upp']['P_on'] for b in BASES], pi512)}

    P = {}
    # P1 identity exception
    p1a = {}
    for b in (204, 51):
        rs = by[(b, 'Upp')]
        idmis = sum(1 for x in rs if abs(float(x['agree']) - (1 - 2*float(x['mean_antiphase_pairs'])/W)) > 1e-9)
        med = float(st.median([float(x['agree']) for x in rs]))
        p1a[b] = {'n': len(rs), 'integer_identity_mismatches': idmis,
                  'P_on': float(np.mean([x['on_beam'] for x in rs])), 'median_agree': med,
                  'median_in_window': 0.925 <= med <= 0.950}
    P['P1a'] = {'per_base': p1a,
                'held': all(v['integer_identity_mismatches'] == 0 and v['P_on'] == 0.0
                            and v['median_in_window'] for v in p1a.values())}
    p1b = {}
    for b in (204, 51):
        rs = by[(b, 'Uplus')]
        near = sum(1 for x in rs if abs(float(x['agree']) - EXPECTED) <= 0.05)
        p1b[b] = {'n': len(rs), 'within_0.05_of_0.9375': near,
                  'P_on': float(np.mean([x['on_beam'] for x in rs])),
                  'Upp_median_same_base': p1a[b]['median_agree']}
    P['P1b'] = {'per_base': p1b, 'held': all(v['within_0.05_of_0.9375'] >= 14 and v['P_on'] == 0.0
                                             for v in p1b.values())}
    # P2 one-step collapse
    p2 = {}
    for b in (0, 22, 232):
        rs = by[(b, 'Upp')]
        p2[b] = {'n': len(rs), 'all_agree_one': all(float(x['agree']) == 1.0 for x in rs),
                 'all_on_beam': all(x['on_beam'] == 1 for x in rs),
                 'min_agree': min(float(x['agree']) for x in rs)}
    P['P2'] = {'per_base': p2, 'held': all(v['all_agree_one'] and v['all_on_beam'] for v in p2.values())}
    # P3 blind stratum
    zero_pi = [b for b in BASES if per[b]['Pi_512'] == 0.0]
    top3 = sorted(BASES, key=lambda b: -per[b]['rho'])[:3]
    P['P3a'] = {'spearman_rho_Pi512': cor['rho_vs_Pi512'],
                'held': (cor['rho_vs_Pi512'] or -1) >= 0.6}
    P['P3b'] = {'zero_Pi_bases': zero_pi,
                'violations': [b for b in zero_pi if not (per[b]['rho'] <= 0.005 and per[b]['Upp']['P_on'] >= 0.95)],
                'held': all(per[b]['rho'] <= 0.005 and per[b]['Upp']['P_on'] >= 0.95 for b in zero_pi)}
    P['P3c'] = {'top3_rho': top3, 'predicted': [204, 51, 37], 'held': set(top3) == {204, 51, 37}}
    # P4 grower floor
    z = [b for b in BASES if per[b]['e_G'] == 0]; nz = [b for b in BASES if per[b]['e_G'] >= 1]
    strict = (max(per[b]['G']['median_agree'] for b in z) < min(per[b]['G']['median_agree'] for b in nz)) if z and nz else None
    zp = [b for b in BASES if per[b]['e_Gprime'] == 0]; nzp = [b for b in BASES if per[b]['e_Gprime'] >= 1]
    strictp = (max(per[b]['Gprime']['median_agree'] for b in zp) < min(per[b]['Gprime']['median_agree'] for b in nzp)) if zp and nzp else None
    P['P4a'] = {'zero_group': z, 'strict_separation': strict, 'spearman': cor['G_vs_eG'],
                'held_strict': bool(strict), 'held_spearman': (cor['G_vs_eG'] or -1) >= 0.6}
    P['P4b'] = {'zero_group': zp, 'strict_separation': strictp, 'spearman': cor['Gprime_vs_eGprime'],
                'held_strict': bool(strictp), 'held_spearman': (cor['Gprime_vs_eGprime'] or -1) >= 0.6}
    ch = {}
    for b, sign in ((27, +1), (45, -1)):
        g, gp = per[b]['G']['median_agree'], per[b]['Gprime']['median_agree']
        ch[b] = {'G': g, 'Gprime': gp, 'diff_signed': (gp - g) if sign > 0 else (g - gp),
                 'held': ((gp - g) if sign > 0 else (g - gp)) >= 0.05}
    P['P4c'] = {'per_base': ch, 'held': all(v['held'] for v in ch.values())}
    P['P4d'] = {'G_51': per[51]['G']['median_agree'], 'Gprime_51': per[51]['Gprime']['median_agree'],
                'held': per[51]['G']['median_agree'] <= 0.45 and per[51]['Gprime']['median_agree'] <= 0.45}
    band = {b: per[b]['G']['median_agree'] for b in nz}
    P['P4e'] = {'n_bases': len(nz), 'out_of_band': {b: v for b, v in band.items() if not (0.55 <= v <= 0.90)},
                'held': all(0.55 <= v <= 0.90 for v in band.values())}
    # P5 random arm
    P['P5'] = {'spearman_beta': cor['random_vs_beta'], 'spearman_Pi512': cor['random_vs_Pi512'],
               'held': (cor['random_vs_beta'] or -1) >= 0.5 and (cor['random_vs_Pi512'] or 1) <= -0.4}
    # P6 dark bits
    d6a = {b: abs(per[b]['Uplus']['median_agree'] - per[b]['Upp']['median_agree']) for b in BASES}
    P['P6a'] = {'max_gap': max(d6a.values()), 'over_0.02': {b: v for b, v in d6a.items() if v > 0.02},
                'held': all(v <= 0.02 for v in d6a.values())}
    gapf = {b: per[b]['Dplus']['median_agree'] - per[b]['random']['median_agree'] for b in FROZEN_BASES}
    gapa = {b: per[b]['Dplus']['median_agree'] - per[b]['random']['median_agree']
            for b in BASES if b not in FROZEN_BASES}
    nf = sum(1 for v in gapf.values() if v >= 0.05)
    P['P6b'] = {'frozen_gaps': gapf, 'n_frozen_over_0.05': nf,
                'mean_frozen_gap': float(np.mean(list(gapf.values()))),
                'mean_active_gap': float(np.mean(list(gapa.values()))),
                'held': nf >= 3 and float(np.mean(list(gapf.values()))) > float(np.mean(list(gapa.values())))}
    # P7 specificity
    P['P7'] = {'spearman_K_on_Pi512': cor['K_on_vs_Pi512'], 'spearman_Upp_on_Pi512': cor['Upp_on_vs_Pi512'],
               'held': (abs(cor['K_on_vs_Pi512']) <= 0.3 if cor['K_on_vs_Pi512'] is not None else False)
                       and (cor['rho_vs_Pi512'] or -1) >= 0.6}

    # descriptive: the coordinator's floor reading
    floor = {b: {'G_minus_random': per[b]['G']['median_agree'] - per[b]['random']['median_agree'],
                 'random_median': per[b]['random']['median_agree']} for b in BASES}
    out = {'per_base': per, 'correlations': cor, 'predictions': P,
           'descriptive': {'floor_reading': floor,
                           'G_median_spread': {'sd': float(np.std([per[b]['G']['median_agree'] for b in BASES])),
                                               'range': [min(Gmed), max(Gmed)]},
                           'random_median_spread': {'sd': float(np.std(rmed)), 'range': [min(rmed), max(rmed)]}},
           'algebra': {k: alg[k] for k in ('agreeing_windows','n_pairs','rank_lit','rank_dark','n_components','n_Upp','totalistic')},
           'n_rows': len(rows)}
    (RES/'summary.json').write_text(json.dumps(out, indent=1, default=str))

    print(f'rows {len(rows)}')
    for k in sorted(P):
        v = P[k]
        print(f'  {k}: held={v.get("held")}')
    print('\ncorrelations:')
    for k, v in cor.items(): print(f'  {k}: {v}')

if __name__ == '__main__':
    main()
