#!/usr/bin/env python3
"""Frozen analysis for the handed fiber census (protocol sections 3-4).

Written and committed before the canonical run; thresholds are the protocol's
and are not changed after any output is read.

Whole-census analyses (logistic models, base-phenotype join) use the uniform
twelve-rule tier of every fiber, which the protocol fixes as the first twelve
of each panel fiber's sample order, so panel fibers do not dominate. Panel
comparisons use the full 256.
"""
from __future__ import annotations
import hashlib, json, math
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / 'results/handed_fiber_census_20260917'
PANEL = [110, 124, 137, 54, 22, 30, 90, 0, 204]
WHOLE = 12
COND_P = ROOT / 'experiments/class4_selective_persistence_20260916/evidence/class4_selective_persistence_all_conditions_20260916.RECOVERED.csv'

# ------------------------------------------------------------------ stats

def norm_sf(z):
    return 0.5 * math.erfc(z / math.sqrt(2))

def two_prop(k1, n1, k2, n2):
    """Two-sided pooled-variance two-proportion z-test."""
    if n1 == 0 or n2 == 0: return {'p1': None, 'p2': None, 'z': None, 'p': None}
    p1, p2 = k1 / n1, k2 / n2
    pp = (k1 + k2) / (n1 + n2)
    se = math.sqrt(pp * (1 - pp) * (1 / n1 + 1 / n2))
    z = 0.0 if se == 0 else (p1 - p2) / se
    return {'p1': p1, 'p2': p2, 'z': z, 'p': 2 * norm_sf(abs(z))}

def mannwhitney_one_sided(x, y):
    """H1: x stochastically greater than y. Normal approximation with tie correction."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    n1, n2 = len(x), len(y)
    allv = np.concatenate([x, y])
    order = np.argsort(allv, kind='mergesort')
    ranks = np.empty(len(allv), float)
    sv = allv[order]; i = 0
    while i < len(sv):
        j = i
        while j + 1 < len(sv) and sv[j + 1] == sv[i]: j += 1
        ranks[order[i:j + 1]] = (i + j) / 2 + 1
        i = j + 1
    R1 = ranks[:n1].sum()
    U1 = R1 - n1 * (n1 + 1) / 2
    mu = n1 * n2 / 2
    _, cnt = np.unique(allv, return_counts=True)
    tie = (cnt ** 3 - cnt).sum()
    N = n1 + n2
    sd = math.sqrt(n1 * n2 / 12 * ((N + 1) - tie / (N * (N - 1))))
    z = 0.0 if sd == 0 else (U1 - mu) / sd
    return {'U': float(U1), 'z': float(z), 'p_one_sided': norm_sf(z),
            'median_x': float(np.median(x)), 'median_y': float(np.median(y)), 'n_x': n1, 'n_y': n2}

def spearman(a, b):
    a = pd.Series(a).rank().to_numpy(); b = pd.Series(b).rank().to_numpy()
    a = a - a.mean(); b = b - b.mean()
    d = math.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / d) if d else None

def chi2_sf(x, df):
    a, z = df / 2.0, x / 2.0
    if z <= 0: return 1.0
    if z < a + 1:
        s = t = 1.0 / a; n = 1
        while abs(t) > 1e-16 * abs(s) and n < 10000:
            t *= z / (a + n); s += t; n += 1
        return 1.0 - s * math.exp(-z + a * math.log(z) - math.lgamma(a))
    b = z + 1 - a; c = 1e300; d = 1 / b; h = d
    for i in range(1, 10000):
        an = -i * (i - a); b += 2
        d = an * d + b; d = 1e-300 if d == 0 else d
        c = b + an / c; c = 1e-300 if c == 0 else c
        d = 1 / d; delta = d * c; h *= delta
        if abs(delta - 1) < 1e-16: break
    return math.exp(-z + a * math.log(z) - math.lgamma(a)) * h

def fit_logistic(X, y, ridge=1e-6, iters=100):
    w = np.zeros(X.shape[1])
    for _ in range(iters):
        p = np.clip(1 / (1 + np.exp(-X @ w)), 1e-12, 1 - 1e-12)
        W = p * (1 - p)
        H = X.T @ (X * W[:, None]) + ridge * np.eye(X.shape[1])
        step = np.linalg.solve(H, X.T @ (y - p) - ridge * w)
        w = w + step
        if np.max(np.abs(step)) < 1e-10: break
    return w

def logloss(X, y, w):
    p = np.clip(1 / (1 + np.exp(-X @ w)), 1e-12, 1 - 1e-12)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))

# ------------------------------------------------------------------ orbits

def mirror(r):
    return sum(((r >> (4 * a + 2 * b + c)) & 1) << (4 * c + 2 * b + a)
               for a in (0, 1) for b in (0, 1) for c in (0, 1))

def complement(r):
    return sum((1 - ((r >> (7 - i)) & 1)) << i for i in range(8))

def orbit_rep(r):
    orb = {r}
    for _ in range(4):
        orb |= {mirror(x) for x in orb} | {complement(x) for x in orb}
    return min(orb)

# -------------------------------------------------------------------- main

def main():
    d = json.loads((OUT / 'rows.json').read_text())
    df = pd.DataFrame(d['rows'])
    df['persist'] = (df.S_star.fillna(0) > 0).astype(int)
    df['spread'] = (df.alpha_x.fillna(-np.inf) > 0.5).astype(int)
    df['both'] = df.persist & df.spread
    bases = sorted(df.base.unique())

    # uniform twelve-rule tier: first WHOLE rows of each fiber in sample order
    tier = df.groupby('base', sort=False).head(WHOLE).reset_index(drop=True)
    assert tier.groupby('base').size().eq(WHOLE).all(), 'twelve-rule tier incomplete'

    def fracs(frame):
        g = frame.groupby('base')
        out = {}
        for b, sub in g:
            n = len(sub); row = {'n': n}
            for k in ('persist', 'spread', 'both'):
                p = float(sub[k].mean()); row[k] = p
                row[k + '_se'] = math.sqrt(p * (1 - p) / n) if n else None
            out[int(b)] = row
        return out

    per_fiber_full = fracs(df)
    per_fiber_tier = fracs(tier)

    # ---- panel comparisons (full n)
    def cnt(b, k): return int(df[df.base == b][k].sum()), int((df.base == b).sum())
    panel_tests = {}
    for name, (a, bb, k) in {
        '110_vs_30_both': (110, 30, 'both'), '110_vs_0_both': (110, 0, 'both'),
        '110_vs_90_both': (110, 90, 'both'), '110_vs_204_both': (110, 204, 'both'),
        '110_vs_124_spread': (110, 124, 'spread'), '110_vs_124_both': (110, 124, 'both'),
        '110_vs_137_spread': (110, 137, 'spread'), '110_vs_137_both': (110, 137, 'both'),
        '54_vs_22_both': (54, 22, 'both'), '110_vs_54_both': (110, 54, 'both'),
    }.items():
        k1, n1 = cnt(a, k); k2, n2 = cnt(bb, k)
        panel_tests[name] = two_prop(k1, n1, k2, n2)

    # ---- logistic models on the uniform tier, eight truth-table bits
    bits = np.array([[(b >> i) & 1 for i in range(8)] for b in tier.base], float)
    inter = np.array([[bits[:, i] * bits[:, j] for i in range(8) for j in range(i + 1, 8)]]).squeeze(0).T
    X1 = np.column_stack([np.ones(len(bits)), bits])
    X2 = np.column_stack([X1, inter])
    tb = tier.base.to_numpy()
    models = {}
    for name in ('persist', 'spread', 'both'):
        y = tier[name].to_numpy(float)
        w1, w2 = fit_logistic(X1, y), fit_logistic(X2, y)
        dev1, dev2 = 2 * len(y) * logloss(X1, y, w1), 2 * len(y) * logloss(X2, y, w2)
        lrt = dev1 - dev2
        l1 = []; l2 = []
        for b in bases:
            tr = tb != b; te = ~tr
            l1.append(logloss(X1[te], y[te], fit_logistic(X1[tr], y[tr])))
            l2.append(logloss(X2[te], y[te], fit_logistic(X2[tr], y[tr])))
        models[name] = {'deviance_M1': dev1, 'deviance_M2': dev2, 'LRT': lrt,
                        'LRT_p_df28': chi2_sf(lrt, 28),
                        'loo_logloss_M1': float(np.mean(l1)), 'loo_logloss_M2': float(np.mean(l2)),
                        'M1_coefficients': {k: float(v) for k, v in
                                            zip(['intercept'] + [f'bit{i}' for i in range(8)], w1)}}

    # ---- base-phenotype join
    cp = pd.read_csv(COND_P)
    cp = cp[(cp.condition == 'P') & (cp.radius == 1)]
    reps = {int(r): {'S': float(s), 'alpha': float(a)} for r, s, a in zip(cp.rule, cp.S, cp.alpha)}
    assert set(reps) == {orbit_rep(r) for r in range(256)}, 'condition-P rows are not the 88 orbit reps'
    rep_of = {b: orbit_rep(b) for b in bases}
    hi_alpha = [b for b in bases if reps[rep_of[b]]['alpha'] > 0.5]
    hi_S = [b for b in bases if reps[rep_of[b]]['S'] > 0]
    join = {
        'n_bases_alpha_gt_half': len(hi_alpha), 'n_bases_S_gt_zero': len(hi_S),
        'a_spread': mannwhitney_one_sided([per_fiber_tier[b]['spread'] for b in hi_alpha],
                                          [per_fiber_tier[b]['spread'] for b in bases if b not in hi_alpha]),
        'b_persist': mannwhitney_one_sided([per_fiber_tier[b]['persist'] for b in hi_S],
                                           [per_fiber_tier[b]['persist'] for b in bases if b not in hi_S]),
    }

    # ---- descriptive, unscored
    sym = [b for b in bases if mirror(b) == b]
    desc = {'pooled_symmetric_bases_tier': {k: float(tier[tier.base.isin(sym)][k].mean())
                                            for k in ('persist', 'spread', 'both')},
            'lifelike_64_census_pooled': {'persist': 0.468, 'spread': 0.421, 'both': 0.230},
            'n_symmetric_bases': len(sym)}
    inv_path = ROOT / 'results/forced_tables_20260917/invariants.json'
    if inv_path.exists():
        # invariants.json is a list of per-rule records keyed by 'rule', not a dict.
        inv = {int(e['rule']): e for e in json.loads(inv_path.read_text())}
        sp = {}
        for key in ('size', 'h2', 'h3'):
            vals = [inv[b].get(key) for b in bases]
            if all(isinstance(v, (int, float)) for v in vals):
                sp[key] = {k: spearman(vals, [per_fiber_tier[b][k] for b in bases])
                           for k in ('persist', 'spread', 'both')}
        desc['spearman_vs_forced_table'] = sp

    # ---- predictions
    F = per_fiber_full
    rank_bases = [b for b in PANEL if b != 137]
    ranking = sorted(rank_bases, key=lambda b: -F[b]['both'])
    p1_targets = {str(t): F[110]['both'] > F[t]['both'] for t in (0, 90, 204, 30)}
    calib_ok = (panel_tests['110_vs_137_spread']['p'] >= 0.05 and
                panel_tests['110_vs_137_both']['p'] >= 0.05)
    p3_dir = F[110]['spread'] > F[124]['spread']
    p3_sig = panel_tests['110_vs_124_spread']['p'] < 0.05
    preds = {
        'P1_110_enriched': {'fiber110_both': F[110]['both'],
                            'comparators': {str(t): F[t]['both'] for t in (0, 90, 204, 30)},
                            'per_target': p1_targets, 'held': all(p1_targets.values()),
                            'contamination_notice': 'the disclosed pre-freeze pilot observed one '
                                                    'fiber(110) member as both-positive (S*=0.28, alpha=0.75); '
                                                    'one draw of 256, weak but not nil'},
        'P2_110_top_two': {'ranking_excluding_137': ranking,
                           'both_fractions': {str(b): F[b]['both'] for b in rank_bases},
                           'held': 110 in ranking[:2]},
        'P3_chirality': {'fiber110_spread': F[110]['spread'], 'fiber124_spread': F[124]['spread'],
                         'test': panel_tests['110_vs_124_spread'],
                         'calibration_110_vs_137': {'spread': panel_tests['110_vs_137_spread'],
                                                    'both': panel_tests['110_vs_137_both'],
                                                    'passes': calib_ok},
                         'held': bool(p3_dir and p3_sig and calib_ok),
                         'scorable': calib_ok},
        'P4_symmetric_ordering': {
            '54_gt_22': F[54]['both'] > F[22]['both'],
            '22_gt_max_0_90': F[22]['both'] > max(F[0]['both'], F[90]['both']),
            'min_0_90_gt_204': min(F[0]['both'], F[90]['both']) > F[204]['both'],
            'fractions': {str(b): F[b]['both'] for b in (54, 22, 0, 90, 204)}},
        'P5_base_phenotype_predicts_fiber': {
            'a_alpha_predicts_spread': {'p': join['a_spread']['p_one_sided'],
                                        'held': join['a_spread']['p_one_sided'] < 0.01},
            'b_S_predicts_persist': {'p': join['b_persist']['p_one_sided'],
                                     'held': join['b_persist']['p_one_sided'] < 0.01}},
        'P6_non_additivity_replicates': {
            'LRT_p_df28': models['spread']['LRT_p_df28'],
            'loo_M1': models['spread']['loo_logloss_M1'], 'loo_M2': models['spread']['loo_logloss_M2'],
            'held': models['spread']['LRT_p_df28'] < 0.01 and
                    models['spread']['loo_logloss_M2'] < models['spread']['loo_logloss_M1']},
    }
    preds['P4_symmetric_ordering']['held'] = all(
        preds['P4_symmetric_ordering'][k] for k in ('54_gt_22', '22_gt_max_0_90', 'min_0_90_gt_204'))

    def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
    out = {'protocol': d['protocol'], 'analysis_tier': {'whole_census_rows_per_fiber': WHOLE,
                                                        'panel_rows_per_fiber': d['panel_sample']},
           'per_fiber_full': per_fiber_full, 'per_fiber_twelve_tier': per_fiber_tier,
           'panel_tests': panel_tests, 'models': models, 'base_phenotype_join': join,
           'descriptive': desc, 'predictions': preds,
           'source_hashes': {
               'protocol': sha(ROOT / 'docs/research/protocols/2026-09-17-handed-fiber-census.md'),
               'run': sha(HERE / 'run.py'), 'evaluate': sha(HERE / 'evaluate.py'),
               'rows': sha(OUT / 'rows.json'), 'exactness': sha(OUT / 'exactness_control.json'),
               'condition_p_table': sha(COND_P)}}
    (OUT / 'summary.json').write_text(json.dumps(out, indent=1, sort_keys=True, allow_nan=False) + '\n')
    print(json.dumps({k: v.get('held') for k, v in preds.items()}, indent=1))

    try:
        import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(7.5, 4.5))
        for b in PANEL:
            s = df[df.base == b]
            ax.scatter(s.alpha_x.fillna(-0.5), s.S_star.fillna(0), s=9, alpha=0.5, label=f'fiber {b}')
        ax.axvline(0.5, lw=0.8, ls='--', c='k'); ax.axhline(0, lw=0.8, ls='--', c='k')
        ax.set_xlabel('alpha_x'); ax.set_ylabel('S*'); ax.legend(fontsize=7, ncol=3)
        fig.tight_layout(); fig.savefig(OUT / 'handed_panel.svg')

        fig, ax = plt.subplots(figsize=(7.5, 4.5))
        xa = [reps[rep_of[b]]['alpha'] for b in bases]
        ya = [per_fiber_tier[b]['both'] for b in bases]
        ax.scatter(xa, ya, s=16, c='#4c72b0', alpha=0.7)
        for b in PANEL:
            ax.annotate(str(b), (reps[rep_of[b]]['alpha'], per_fiber_tier[b]['both']), fontsize=8)
        ax.set_xlabel("base's 1D alpha (orbit representative, condition P)")
        ax.set_ylabel('fiber both-positive fraction (12-rule tier)')
        fig.tight_layout(); fig.savefig(OUT / 'handed_fiber_vs_1d.svg')
        print('figures written')
    except Exception as e:
        print('figures skipped:', e)

if __name__ == '__main__':
    main()
