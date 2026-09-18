#!/usr/bin/env python3
"""Frozen analysis for the beam-mechanism unit (protocol sections 3-4).

Written and committed before the canonical run; thresholds are the protocol's
and are not changed after any output is read. Every prediction is
pilot-calibrated and declared as such; the unit is a pre-registered
out-of-sample replication on fresh completions and eight fresh bases.
"""
from __future__ import annotations
import hashlib, json, math
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / 'results/beam_mechanism_20260918'
COND_P = ROOT / 'experiments/class4_selective_persistence_20260916/evidence/class4_selective_persistence_all_conditions_20260916.RECOVERED.csv'
FROZEN = [0, 204, 8, 232]          # excluded from P2(b) by the protocol

def rank(x):
    return pd.Series(x).rank().to_numpy(float)

def pearson(a, b):
    a = np.asarray(a, float) - np.mean(a); b = np.asarray(b, float) - np.mean(b)
    d = math.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / d) if d else None

def spearman(a, b):
    return pearson(rank(a), rank(b))

def partial_spearman(y1, y2, covars):
    """Rank-partial: residualize ranks on ranked covariates, then Pearson."""
    R1, R2 = rank(y1), rank(y2)
    X = np.column_stack([np.ones(len(R1))] + [rank(c) for c in covars])
    def resid(y):
        w, *_ = np.linalg.lstsq(X, y, rcond=None)
        return y - X @ w
    return pearson(resid(R1), resid(R2))

def main():
    d = json.loads((OUT / 'rows.json').read_text())
    df = pd.DataFrame(d['rows'])
    df['alpha_x0'] = df.alpha_x.fillna(0.0)
    df['logT128'] = np.log1p(df.T128.fillna(0.0)) if 'T128' in df else np.nan
    bases = d['bases']; orig = d['original_bases']; us = d['completions']
    main_t = df[df.tier == 'main']; h3 = df[df.tier == 'h3']

    def grid(frame, col, order, blist):
        p = frame.pivot(index='base', columns='completion', values=col)
        return p.reindex(index=blist, columns=order).to_numpy(float)

    G = {o: grid(main_t, o, us, bases) for o in
         ('M_star', 'R_star', 'alpha_x0', 'agree', 'T_ext', 'logT128')}
    idx = {b: i for i, b in enumerate(bases)}

    transfer = {o: {str(a): {str(b): spearman(G[o][idx[a]], G[o][idx[b]]) for b in bases}
                    for a in bases} for o in G}
    pairs = [(a, b) for i, a in enumerate(bases) for b in bases[i + 1:]]
    partial_agree = {f'{a}|{b}': partial_spearman(G['M_star'][idx[a]], G['M_star'][idx[b]],
                                                  [G['agree'][idx[a]], G['agree'][idx[b]]])
                     for a, b in pairs}
    partial_text = {f'{a}|{b}': partial_spearman(G['M_star'][idx[a]], G['M_star'][idx[b]],
                                                 [G['T_ext'][idx[a]], G['T_ext'][idx[b]]])
                    for a, b in pairs}
    l2o = {}
    for a, b in pairs:
        others = [idx[x] for x in bases if x not in (a, b)]
        score = G['agree'][others].mean(axis=0)
        l2o[f'{a}|{b}'] = partial_spearman(G['M_star'][idx[a]], G['M_star'][idx[b]], [score])
    partial_R = {f'{a}|{b}': partial_spearman(G['R_star'][idx[a]], G['R_star'][idx[b]],
                                              [G['agree'][idx[a]], G['agree'][idx[b]]])
                 for a, b in pairs}

    cp = pd.read_csv(COND_P); cp = cp[(cp.condition == 'P') & (cp.radius == 1)]
    M1D = {int(r): float(m) for r, m in zip(cp.rule, cp.M)}

    resp = {}
    for b in bases:
        i = idx[b]
        on = G['M_star'][i][G['agree'][i] > 0.98]; off = G['M_star'][i][G['agree'][i] < 0.5]
        mid = G['M_star'][i][(G['agree'][i] >= 0.5) & (G['agree'][i] <= 0.98)]
        resp[str(b)] = {
            'rho_agree': spearman(G['M_star'][i], G['agree'][i]),
            'rho_text': spearman(G['M_star'][i], G['T_ext'][i]),
            'M_1D': M1D[b],
            'n_on': int(len(on)), 'n_off': int(len(off)), 'n_mid': int(len(mid)),
            'median_on': float(np.median(on)) if len(on) else None,
            'median_off': float(np.median(off)) if len(off) else None,
            'median_mid': float(np.median(mid)) if len(mid) else None,
            'gate_on_given_Text_high': float((G['agree'][i][G['T_ext'][i] >= 0.9] > 0.98).mean())
                                        if (G['T_ext'][i] >= 0.9).any() else None,
            'gate_on_given_Text_low': float((G['agree'][i][G['T_ext'][i] < 0.5] > 0.98).mean())
                                       if (G['T_ext'][i] < 0.5).any() else None}
    rho = {b: resp[str(b)]['rho_agree'] for b in bases}
    order_stat = spearman([rho[b] for b in bases], [M1D[b] for b in bases])

    strong = [(a, b) for a, b in pairs if abs(rho[a]) >= 0.3 and abs(rho[b]) >= 0.3]
    sign_hits = sum(1 for a, b in strong
                    if np.sign(transfer['M_star'][str(a)][str(b)]) == np.sign(rho[a] * rho[b]))
    sign_acct = {'pairs': len(strong), 'agree': sign_hits,
                 'fraction': sign_hits / len(strong) if strong else None}

    # height three
    h3u = us[:d['n_h3']]
    G3 = {o: grid(h3, o, h3u, orig) for o in ('M_star', 'agree')}
    i3 = {b: i for i, b in enumerate(orig)}
    h3res = {'r_M3_110_30': spearman(G3['M_star'][i3[110]], G3['M_star'][i3[30]]),
             'agree3_transfer_110_30': spearman(G3['agree'][i3[110]], G3['agree'][i3[30]]),
             'on_beam_fraction_h3': {str(b): float((G3['agree'][i3[b]] > 0.98).mean()) for b in orig},
             'on_beam_fraction_h2_same48': {
                 str(b): float((G['agree'][idx[b]][:d['n_h3']] > 0.98).mean()) for b in orig}}

    def boot(fn, n=2000):
        rng = np.random.default_rng(7); vals = []
        for _ in range(n):
            s = rng.integers(0, len(us), len(us))
            v = fn(s)
            if v is not None and np.isfinite(v): vals.append(v)
        return [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))] if vals else None

    rM = transfer['M_star']['110']['30']
    pa = partial_agree['110|30'] if '110|30' in partial_agree else partial_agree['30|110']
    pt = partial_text['110|30'] if '110|30' in partial_text else partial_text['30|110']
    pl = l2o['110|30'] if '110|30' in l2o else l2o['30|110']
    agree_off = [transfer['agree'][str(a)][str(b)] for a, b in pairs]
    nonfrozen = [(a, b) for a, b in pairs if a not in FROZEN and b not in FROZEN]
    text_off = [transfer['T_ext'][str(a)][str(b)] for a, b in nonfrozen]
    hi = [b for b in bases if M1D[b] >= 0.5]; chaotic = [30, 90, 106]
    mid_band = [b for b in bases if 0.10 <= M1D[b] <= 0.40]
    rR = transfer['R_star']['110']['30']
    pR = partial_R['110|30'] if '110|30' in partial_R else partial_R['30|110']

    p4prime = []
    for b in bases:
        e = resp[str(b)]
        if e['n_on'] >= 10 and e['n_off'] >= 10 and e['median_on'] is not None \
           and abs(e['median_on'] - e['median_off']) >= 0.10:
            p4prime.append((b, np.sign(rho[b]) == np.sign(e['median_on'] - e['median_off'])))

    preds = {
      'P1_anticorrelation_and_mediation': {
        'a_raw': rM, 'b_partial_agree': pa, 'c_partial_Text': pt, 'd_partial_leave_two_out': pl,
        'a_held': rM <= -0.25, 'b_held': pa >= -0.05, 'c_held': pt >= -0.05, 'd_held': pl >= -0.15,
        'd_note': 'least-calibrated arm per the freeze amendment; a failure confined to (d) reads as a mis-set threshold',
        'held': rM <= -0.25 and pa >= -0.05 and pt >= -0.05 and pl >= -0.15,
        'bootstrap_raw': boot(lambda s: spearman(G['M_star'][idx[110]][s], G['M_star'][idx[30]][s]))},
      'P2_beam_proximity_is_a_completion_property': {
        'a_min_agree_transfer': float(np.min(agree_off)), 'a_held': float(np.min(agree_off)) >= 0.25,
        'a_prime_frac_ge_025': float(np.mean([v >= 0.25 for v in agree_off])),
        'a_prime_min': float(np.min(agree_off)),
        'a_prime_held': float(np.mean([v >= 0.25 for v in agree_off])) >= 0.95 and float(np.min(agree_off)) >= 0.10,
        'b_min_Text_transfer_nonfrozen': float(np.min(text_off)),
        'b_held': float(np.min(text_off)) >= 0.40,
        'held': float(np.min(agree_off)) >= 0.25 and float(np.min(text_off)) >= 0.40},
      'P3_response_follows_1D_history_gain': {
        'a_order_spearman': order_stat, 'a_held': order_stat >= 0.70,
        'b_high_bases': {str(b): rho[b] for b in hi}, 'b_held': all(rho[b] >= 0.40 for b in hi),
        'c_chaotic': {str(b): rho[b] for b in chaotic}, 'c_held': all(rho[b] <= -0.40 for b in chaotic),
        'held': order_stat >= 0.70 and all(rho[b] >= 0.40 for b in hi) and all(rho[b] <= -0.40 for b in chaotic),
        'bootstrap_order': boot(lambda s: spearman(
            [spearman(G['M_star'][idx[b]][s], G['agree'][idx[b]][s]) for b in bases],
            [M1D[b] for b in bases]))},
      'P4_naive_sign_rule_expected_to_fail': {
        'mid_band_bases': {str(b): rho[b] for b in mid_band},
        'held': all(rho[b] >= 0.20 for b in mid_band),
        'P4prime_mixture_reading': {'checked': [(b, bool(ok)) for b, ok in p4prime],
                                    'held': all(ok for _, ok in p4prime) and len(p4prime) > 0}},
      'P5_on_beam_identity': {
        'on_gaps': {str(b): (abs(resp[str(b)]['median_on'] - M1D[b])
                             if resp[str(b)]['n_on'] >= 10 and resp[str(b)]['median_on'] is not None else None)
                    for b in bases},
        'off_medians': {str(b): resp[str(b)]['median_off'] for b in bases if resp[str(b)]['n_off'] >= 10},
        'held': all(abs(resp[str(b)]['median_on'] - M1D[b]) <= 0.15
                    for b in bases if resp[str(b)]['n_on'] >= 10 and resp[str(b)]['median_on'] is not None)
                and all(0.02 <= resp[str(b)]['median_off'] <= 0.45
                        for b in bases if resp[str(b)]['n_off'] >= 10 and resp[str(b)]['median_off'] is not None)},
      'P6_retention_not_mediated': {
        'raw': rR, 'partial_agree': pR,
        'held': rR >= 0.50 and abs(rR - pR) <= 0.15},
      'P7_height_three': {
        'a_r_M3': h3res['r_M3_110_30'], 'a_held': h3res['r_M3_110_30'] <= -0.20,
        'b_agree3_transfer': h3res['agree3_transfer_110_30'], 'b_held': h3res['agree3_transfer_110_30'] >= 0.50,
        'held': h3res['r_M3_110_30'] <= -0.20 and h3res['agree3_transfer_110_30'] >= 0.50,
        'descriptive_on_beam_h3_vs_h2': {'h3': h3res['on_beam_fraction_h3'],
                                         'h2_same_48': h3res['on_beam_fraction_h2_same48']}},
    }

    ctrl = json.loads((OUT / 'controls.json').read_text())
    def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
    out = {'protocol': d['protocol'],
           'standing': ('Every prediction is pilot-calibrated and declared so; this unit is a '
                        'pre-registered out-of-sample replication on fresh completions and eight fresh '
                        'bases, not a set of blind bets. The beam theorem is exact and independent of '
                        'how P1-P7 score.'),
           'transfer': transfer, 'partial_agree': partial_agree, 'partial_Text': partial_text,
           'partial_leave_two_out': l2o, 'partial_R_given_agree': partial_R,
           'response': resp, 'order_statistic': order_stat, 'sign_accounting': sign_acct,
           'height_three': h3res, 'matched_null_pairs_identical': ctrl['all_matched_identical'],
           'predictions': preds,
           'source_hashes': {
               'protocol': sha(ROOT / 'docs/research/protocols/2026-09-18-beam-mechanism.md'),
               'run': sha(HERE / 'run.py'), 'evaluate': sha(HERE / 'evaluate.py'),
               'rows': sha(OUT / 'rows.json'), 'controls': sha(OUT / 'controls.json'),
               'condition_p_table': sha(COND_P)}}
    (OUT / 'summary.json').write_text(json.dumps(out, indent=1, sort_keys=True, allow_nan=False) + '\n')
    print(json.dumps({k: v.get('held') for k, v in preds.items()}, indent=1))
    print('P4prime:', preds['P4_naive_sign_rule_expected_to_fail']['P4prime_mixture_reading']['held'],
          '| P2a-prime:', preds['P2_beam_proximity_is_a_completion_property']['a_prime_held'])
    print('raw %.3f -> partial(agree) %.3f, partial(T_ext) %.3f, l2o %.3f' % (rM, pa, pt, pl))

if __name__ == '__main__':
    main()
