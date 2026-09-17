#!/usr/bin/env python3
"""Frozen analysis for the matched-completion unit (protocol sections 3-4).

Written and committed before the canonical run; thresholds are the protocol's
and are not changed after any output is read.

P4 is scored on degrees-of-freedom-adjusted variance components, per the freeze
amendment: the grid has one observation per cell, so a completion mean rests on
8 observations against a base mean's 512 and raw eta-squared for the completion
factor is mechanically inflated. Raw fractions are reported alongside.
"""
from __future__ import annotations
import hashlib, json, math
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / 'results/matched_completion_20260918'
OBS = ['M_star', 'R_star', 'alpha_x0']

def norm_sf(z): return 0.5 * math.erfc(z / math.sqrt(2))

def spearman(a, b):
    a = pd.Series(a).rank().to_numpy(float); b = pd.Series(b).rank().to_numpy(float)
    a = a - a.mean(); b = b - b.mean()
    d = math.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / d) if d else None

def pearson(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    a = a - a.mean(); b = b - b.mean()
    d = math.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / d) if d else None

def wilcoxon(d):
    """Two-sided signed-rank, normal approximation with tie correction."""
    d = np.asarray([x for x in d if x == x and x != 0], float)
    n = len(d)
    if n == 0: return {'n': 0, 'z': None, 'p': None}
    r = pd.Series(np.abs(d)).rank().to_numpy()
    W = r[d > 0].sum()
    mu = n * (n + 1) / 4
    _, cnt = np.unique(np.abs(d), return_counts=True)
    tie = ((cnt ** 3 - cnt).sum()) / 48
    sd = math.sqrt(n * (n + 1) * (2 * n + 1) / 24 - tie)
    z = 0.0 if sd == 0 else (W - mu) / sd
    return {'n': n, 'z': float(z), 'p': 2 * norm_sf(abs(z))}

def mcnemar(x, y):
    b = int(((x == 1) & (y == 0)).sum()); c = int(((x == 0) & (y == 1)).sum())
    if b + c == 0: return {'b': b, 'c': c, 'p': 1.0}
    z = (abs(b - c) - 1) / math.sqrt(b + c)
    return {'b': b, 'c': c, 'p': 2 * norm_sf(max(z, 0.0))}

def variance_components(Y, a, n):
    """Two-way, one observation per cell. Y is [a, n]. Returns raw eta^2 and df-adjusted sigma^2."""
    grand = Y.mean()
    SST = ((Y - grand) ** 2).sum()
    SS_base = n * ((Y.mean(axis=1) - grand) ** 2).sum()
    SS_comp = a * ((Y.mean(axis=0) - grand) ** 2).sum()
    SS_res = SST - SS_base - SS_comp
    MS_base = SS_base / (a - 1); MS_comp = SS_comp / (n - 1)
    MS_res = SS_res / ((a - 1) * (n - 1))
    return {'eta2_base': float(SS_base / SST), 'eta2_comp': float(SS_comp / SST),
            'eta2_res': float(SS_res / SST),
            'sigma2_base': float(max(0.0, (MS_base - MS_res) / n)),
            'sigma2_comp': float(max(0.0, (MS_comp - MS_res) / a)),
            'sigma2_resid': float(max(0.0, MS_res)), 'SST': float(SST)}

def ridge_cv_r2(X, y, lam=1e-3, folds=8, seed=0):
    n = len(y)
    idx = np.random.default_rng(seed).permutation(n)
    pred = np.zeros(n)
    Xd = np.column_stack([np.ones(n), X])
    for f in range(folds):
        te = idx[f::folds]; tr = np.setdiff1d(idx, te)
        A = Xd[tr].T @ Xd[tr] + lam * np.eye(Xd.shape[1]); A[0, 0] -= lam
        w = np.linalg.solve(A, Xd[tr].T @ y[tr])
        pred[te] = Xd[te] @ w
    ss_res = ((y - pred) ** 2).sum(); ss_tot = ((y - y.mean()) ** 2).sum()
    return float(1 - ss_res / ss_tot) if ss_tot > 0 else None

def main():
    d = json.loads((OUT / 'rows.json').read_text())
    df = pd.DataFrame(d['rows'])
    df['alpha_x0'] = df.alpha_x.fillna(0.0)
    df['persist'] = ((df.S_star.fillna(0) > 0)).astype(int)
    df['spread'] = (df.alpha_x.fillna(-np.inf) > 0.5).astype(int)
    df['both'] = df.persist & df.spread
    df['Mpos'] = (df.M_star.fillna(0) > 0).astype(int)
    df['Rpos'] = (df.R_star.fillna(-1) > 0).astype(int)
    bases = d['bases']; us = d['completions']
    A2 = df[(df.stream == 'A') & (df.height == 2)]
    B2 = df[(df.stream == 'B') & (df.height == 2)]
    A4 = df[(df.stream == 'A') & (df.height == 4)]
    assert len(A2) == len(bases) * d['n_completions'], (len(A2),)

    def grid(frame, col, order):
        p = frame.pivot(index='base', columns='completion', values=col)
        return p.reindex(index=bases, columns=order).to_numpy(float)

    order2 = us
    decomp = {}
    for o in OBS:
        Y = grid(A2, o, order2)
        vc = variance_components(Y, len(bases), d['n_completions'])
        decomp[o] = vc
    # replicate-tier noise floor
    rep_order = us[:d['n_replicate']]
    noise = {}
    for o in OBS:
        YA = grid(A2[A2.completion.isin(rep_order)], o, rep_order)
        YB = grid(B2, o, rep_order)
        noise[o] = {'sigma2_noise': float(np.mean((YA - YB) ** 2) / 2),
                    'test_retest_r': {str(b): pearson(YA[i], YB[i]) for i, b in enumerate(bases)}}
    transfer = {}
    for o in OBS:
        Y = grid(A2, o, order2)
        transfer[o] = {str(bases[i]): {str(bases[j]): spearman(Y[i], Y[j]) for j in range(len(bases))}
                       for i in range(len(bases))}
    # paired comparisons of 110 against each base
    paired = {}
    i110 = bases.index(110)
    for o in OBS + ['S_star']:
        col = o if o != 'S_star' else 'S_star'
        Y = grid(A2, col, order2) if o != 'S_star' else grid(A2.assign(S_star=A2.S_star.fillna(0)), 'S_star', order2)
        paired[o] = {}
        for j, b in enumerate(bases):
            if b == 110: continue
            diff = Y[i110] - Y[j]
            paired[o][str(b)] = {'sign_fraction': float((diff > 0).mean()),
                                 'mean_diff': float(np.nanmean(diff)), **wilcoxon(diff)}
    binary = {}
    for col in ('persist', 'spread', 'both', 'Mpos', 'Rpos'):
        Y = grid(A2, col, order2)
        binary[col] = {'fractions': {str(b): float(Y[i].mean()) for i, b in enumerate(bases)},
                       'mcnemar_vs_110': {str(b): mcnemar(Y[i110], Y[j])
                                          for j, b in enumerate(bases) if b != 110}}
    # bit additivity within base
    bits = np.array([[(u >> j) & 1 for j in range(24)] for u in order2], float)
    additivity = {}
    for o in OBS:
        Y = grid(A2, o, order2)
        additivity[o] = {str(b): ridge_cv_r2(bits, Y[i], seed=17) for i, b in enumerate(bases)}
    # height-four arm
    k4_order = us[:d['n_k4']]
    k4 = {}
    for o in OBS:
        Y = grid(A4, o, k4_order)
        k4[o] = {'components': variance_components(Y, len(bases), d['n_k4']),
                 'grid_mean': {str(b): float(Y[i].mean()) for i, b in enumerate(bases)}}
    Y4 = grid(A4, 'M_star', k4_order)
    diff4 = Y4[i110] - Y4[bases.index(30)]
    k4['paired_110_vs_30_M'] = {'sign_fraction': float((diff4 > 0).mean()),
                                'mean_diff': float(np.nanmean(diff4)), **wilcoxon(diff4)}
    k4['censoring'] = {'unsupported': int(A4.unsupported_symbols.sum()),
                       'monte_carlo': int((A4.reference_mode == 'monte-carlo').sum())}

    # ------------------------------------------------------------ predictions
    M = grid(A2, 'M_star', order2); R = grid(A2, 'R_star', order2)
    i30 = bases.index(30)
    dM = M[i110] - M[i30]; dR = R[i110] - R[i30]
    p1a = float((dM > 0).mean()); p1b_sign = float((dR > 0).mean()); p1b_mean = float(np.nanmean(dR))
    tM = transfer['M_star']['110']; tR = transfer['R_star']['110']
    preds = {
        'P1_base_sets_M_completion_sets_R': {
            'a_M_sign_fraction': p1a, 'a_held': p1a >= 0.85,
            'b_R_sign_fraction': p1b_sign, 'b_R_mean_diff': p1b_mean,
            'b_held': 0.40 <= p1b_sign <= 0.60 and abs(p1b_mean) < 0.10,
            'held': p1a >= 0.85 and 0.40 <= p1b_sign <= 0.60 and abs(p1b_mean) < 0.10},
        'P2_transfer_dissociation': {
            'R_transfer_110_30': tR['30'], 'M_transfer_110_30': tM['30'],
            'gap': (tR['30'] - tM['30']) if tR['30'] is not None and tM['30'] is not None else None,
            'held': tR['30'] is not None and tM['30'] is not None and (tR['30'] - tM['30']) >= 0.40},
        'P3_M_transfer_follows_1D_history_gain': {
            'r_110_54': tM['54'], 'r_110_5': tM['5'], 'r_110_30': tM['30'], 'r_110_0': tM['0'],
            'held': (tM['54'] >= 0.60 and tM['5'] >= 0.50 and tM['30'] < 0.40 and tM['0'] < 0.40)},
        'P4_variance_fractions': {
            'a_R_sigma2_comp_gt_base': decomp['R_star']['sigma2_comp'] > decomp['R_star']['sigma2_base'],
            'b_M_sigma2_base_gt_comp': decomp['M_star']['sigma2_base'] > decomp['M_star']['sigma2_comp'],
            'R_components': {k: decomp['R_star'][k] for k in ('sigma2_base', 'sigma2_comp', 'eta2_base', 'eta2_comp')},
            'M_components': {k: decomp['M_star'][k] for k in ('sigma2_base', 'sigma2_comp', 'eta2_base', 'eta2_comp')}},
        'P5_completion_effect_real_not_bit_additive': {
            'min_test_retest': min(v for o in OBS for v in noise[o]['test_retest_r'].values() if v is not None),
            'max_ridge_cv_r2': max(v for o in OBS for v in additivity[o].values() if v is not None),
            'held': (min(v for o in OBS for v in noise[o]['test_retest_r'].values() if v is not None) >= 0.90
                     and max(v for o in OBS for v in additivity[o].values() if v is not None) < 0.25)},
        'P6_dissociation_at_height_four': {
            'sign_fraction': k4['paired_110_vs_30_M']['sign_fraction'],
            'grid_means': k4['M_star']['grid_mean'],
            'held': (k4['paired_110_vs_30_M']['sign_fraction'] >= 0.75
                     and max(k4['M_star']['grid_mean'], key=lambda b: k4['M_star']['grid_mean'][b]) == '110')},
    }
    preds['P4_variance_fractions']['held'] = (preds['P4_variance_fractions']['a_R_sigma2_comp_gt_base']
                                              and preds['P4_variance_fractions']['b_M_sigma2_base_gt_comp'])
    ctrl = json.loads((OUT / 'controls.json').read_text())
    def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
    out = {'protocol': d['protocol'],
           'standing': ('Every prediction was informed by the protocol section-7 pilot on disjoint '
                        'completions; this unit is a pre-registered out-of-sample replication, not a set '
                        'of blind bets. P4 is scored on df-adjusted variance components.'),
           'decomposition': decomp, 'noise': noise, 'transfer': transfer, 'paired': paired,
           'binary': binary, 'bit_additivity': additivity, 'height_four': k4,
           'matched_null_pairs_identical': ctrl['all_matched_identical'],
           'predictions': preds,
           'source_hashes': {
               'protocol': sha(ROOT / 'docs/research/protocols/2026-09-18-matched-completion-persistence.md'),
               'run': sha(HERE / 'run.py'), 'evaluate': sha(HERE / 'evaluate.py'),
               'rows': sha(OUT / 'rows.json'), 'controls': sha(OUT / 'controls.json')}}
    (OUT / 'summary.json').write_text(json.dumps(out, indent=1, sort_keys=True, allow_nan=False) + '\n')
    print(json.dumps({k: v.get('held') for k, v in preds.items()}, indent=1))
    print('sigma2 M base/comp %.4g %.4g   R base/comp %.4g %.4g' % (
        decomp['M_star']['sigma2_base'], decomp['M_star']['sigma2_comp'],
        decomp['R_star']['sigma2_base'], decomp['R_star']['sigma2_comp']))

if __name__ == '__main__':
    main()
