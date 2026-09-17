#!/usr/bin/env python3
"""Frozen analysis for the 64-fiber census (protocol section 4-5), written before any output was read.

Per outcome (persist: S* > 0; spread: alpha_x > 0.5; both), fit logistic
regressions across all rules with fiber-level covariates: M1 = intercept + six
exposed bits; M2 = M1 + 15 pairwise products. Report deviances, the LRT on 15
df, leave-one-fiber-out mean log-loss for both, and P1-P4. Pure NumPy; IRLS
with ridge 1e-6. Writes summary.json (with source_hashes) and the figure.
"""
from __future__ import annotations
import hashlib, json, math
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / 'results/fiber_census_64_20260917'
BITS = ['B0', 'B3', 'B6', 'S2', 'S5', 'S8']
AFFINE = {0, 51, 90, 105, 150, 165, 204, 255}

def design(bits_row, interactions):
    x = [1.0] + [float(bits_row[b]) for b in BITS]
    if interactions:
        for i in range(6):
            for j in range(i + 1, 6):
                x.append(float(bits_row[BITS[i]] * bits_row[BITS[j]]))
    return x

def fit_logistic(X, y, ridge=1e-6, iters=100):
    w = np.zeros(X.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-X @ w)); p = np.clip(p, 1e-12, 1 - 1e-12)
        W = p * (1 - p)
        H = X.T @ (X * W[:, None]) + ridge * np.eye(X.shape[1])
        g = X.T @ (y - p) - ridge * w
        step = np.linalg.solve(H, g)
        w = w + step
        if np.max(np.abs(step)) < 1e-10: break
    return w

def logloss(X, y, w):
    p = np.clip(1 / (1 + np.exp(-X @ w)), 1e-12, 1 - 1e-12)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))

def chi2_sf(x, df):
    """Regularized upper incomplete gamma Q(df/2, x/2) by series/continued fraction."""
    a = df / 2.0; z = x / 2.0
    if z <= 0: return 1.0
    if z < a + 1:
        s = t = 1.0 / a; n = 1
        while abs(t) > 1e-16 * abs(s) and n < 10000:
            t *= z / (a + n); s += t; n += 1
        return 1.0 - s * math.exp(-z + a * math.log(z) - math.lgamma(a))
    # Lentz continued fraction for the upper gamma
    b = z + 1 - a; c = 1e300; d = 1 / b; h = d
    for i in range(1, 10000):
        an = -i * (i - a); b += 2
        d = an * d + b; d = 1e-300 if d == 0 else d
        c = b + an / c; c = 1e-300 if c == 0 else c
        d = 1 / d; delta = d * c; h *= delta
        if abs(delta - 1) < 1e-16: break
    return math.exp(-z + a * math.log(z) - math.lgamma(a)) * h

def main():
    d = json.loads((OUT / 'rows.json').read_text())
    bits = {int(k): v for k, v in d['exposed_bits'].items()}
    rows = d['rows']
    base = np.array([r['base'] for r in rows])
    S = np.array([r['S_star'] if r['S_star'] is not None else 0.0 for r in rows])
    A = np.array([r['alpha_x'] if r['alpha_x'] is not None else -np.inf for r in rows])
    outcomes = {'persist': (S > 0).astype(float), 'spread': (A > 0.5).astype(float), 'both': ((S > 0) & (A > 0.5)).astype(float)}
    X1 = np.array([design(bits[b], False) for b in base]); X2 = np.array([design(bits[b], True) for b in base])
    fibers = sorted(set(base.tolist()))
    per_fiber = {str(b): {'n': int((base == b).sum()), 'bits': bits[b],
                          **{k: float(v[base == b].mean()) for k, v in outcomes.items()}} for b in fibers}
    models = {}
    for name, y in outcomes.items():
        w1 = fit_logistic(X1, y); w2 = fit_logistic(X2, y)
        dev1 = 2 * len(y) * logloss(X1, y, w1); dev2 = 2 * len(y) * logloss(X2, y, w2)
        lrt = dev1 - dev2; p = chi2_sf(lrt, 15)
        loo1 = []; loo2 = []
        for b in fibers:
            tr = base != b; te = ~tr
            loo1.append(logloss(X1[te], y[te], fit_logistic(X1[tr], y[tr])))
            loo2.append(logloss(X2[te], y[te], fit_logistic(X2[tr], y[tr])))
        models[name] = {'M1_coefficients': dict(zip(['intercept'] + BITS, map(float, w1))),
                        'M2_coefficients_first7': dict(zip(['intercept'] + BITS, map(float, w2[:7]))),
                        'M2_interaction_coefficients': {f'{BITS[i]}*{BITS[j]}': float(w2[7 + k]) for k, (i, j) in enumerate((i, j) for i in range(6) for j in range(i + 1, 6))},
                        'deviance_M1': dev1, 'deviance_M2': dev2, 'LRT': lrt, 'LRT_p_df15': p,
                        'loo_logloss_M1': float(np.mean(loo1)), 'loo_logloss_M2': float(np.mean(loo2)),
                        'constant_fibers': [b for b in fibers if y[base == b].min() == y[base == b].max()]}
    bp = {b: per_fiber[str(b)]['both'] for b in fibers}
    both = models['both']
    aff = [bp[b] for b in fibers if b in AFFINE]; rest = sorted(bp[b] for b in fibers if b not in AFFINE)
    q1, q3 = float(np.percentile(rest, 25)), float(np.percentile(rest, 75)); med_aff = float(np.median(aff))
    largest = lambda m: max(BITS, key=lambda k: abs(models[m]['M1_coefficients'][k]))
    preds = {
        'P1_interactions_needed': {'LRT_p': both['LRT_p_df15'], 'loo_M1': both['loo_logloss_M1'], 'loo_M2': both['loo_logloss_M2'],
                                   'held': both['LRT_p_df15'] < 0.01 and both['loo_logloss_M2'] < both['loo_logloss_M1']},
        'P2_ordering_replicates': {'fractions': {str(b): bp[b] for b in (54, 22, 0, 90, 204)},
                                   'held': bp[54] > bp[22] > bp[0] > bp[90] > bp[204]},
        'P3_affine_bases_not_special': {'affine_median': med_aff, 'others_q1_q3': [q1, q3], 'affine_fractions': {str(b): bp[b] for b in fibers if b in AFFINE},
                                        'held': q1 <= med_aff <= q3},
        'P4_descriptive_largest_main_effects': {'spread': largest('spread'), 'persist': largest('persist'),
                                                'as_bet': largest('spread') == 'B3' and largest('persist') == 'S2'},
    }
    def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
    out = {'protocol': d['protocol'], 'per_fiber': per_fiber, 'models': models, 'predictions': preds,
           'source_hashes': {'protocol': sha(ROOT / 'docs/research/protocols/2026-09-17-fiber-census-64.md'),
                             'run': sha(HERE / 'run.py'), 'evaluate': sha(HERE / 'evaluate.py'),
                             'rows': sha(OUT / 'rows.json'), 'exactness': sha(OUT / 'exactness_control.json')}}
    (OUT / 'summary.json').write_text(json.dumps(out, indent=1, sort_keys=True) + '\n')
    print(json.dumps({k: v['held'] if 'held' in v else v for k, v in preds.items()}, indent=1))
    print({m: (round(models[m]['LRT'], 1), models[m]['LRT_p_df15'], round(models[m]['loo_logloss_M1'], 4), round(models[m]['loo_logloss_M2'], 4)) for m in models})
    try:
        import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(7, 4))
        nb = [bits[b]['B0'] + bits[b]['B3'] + bits[b]['B6'] for b in fibers]; ns = [bits[b]['S2'] + bits[b]['S5'] + bits[b]['S8'] for b in fibers]
        sc = ax.scatter(np.array(nb) + 0.12 * (np.array(ns) - 1.5), [bp[b] for b in fibers], c=ns, cmap='viridis', s=28)
        for b in (54, 22, 0, 90, 204): ax.annotate(str(b), (nb[fibers.index(b)] + 0.12 * (ns[fibers.index(b)] - 1.5), bp[b]), fontsize=7)
        ax.set_xlabel('fixed-on birth bits (B0,B3,B6), jittered by survival count'); ax.set_ylabel('both-positive fraction at height 2')
        fig.colorbar(sc, label='fixed-on survival bits (S2,S5,S8)'); fig.tight_layout(); fig.savefig(OUT / 'fiber_census_64.svg'); print('figure written')
    except Exception as e:
        print('figure skipped:', e)

if __name__ == '__main__':
    main()
