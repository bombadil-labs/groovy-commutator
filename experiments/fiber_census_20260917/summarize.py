#!/usr/bin/env python3
"""Evaluate the fiber census against its frozen predictions and draw the figure.

Reads results/fiber_census_20260917/fiber_census_k2.json (and _k4 if present),
writes summary.json (with a source_hashes block for the fast integrity tier;
added after the canonical run, scoring unchanged) and fiber_census_k2.svg. Pure NumPy plus an optional
matplotlib for the figure. Frozen predictions (protocol section 6):

  P1  both-positive fractions differ across fibers (max - min > 0.10) and a
      Kruskal-Wallis test on S* across the five fibers has p < 0.01;
  P2  fiber(54) both-positive fraction > each of fiber(0), fiber(204), fiber(90);
  P3  HighLife's S* is within the 10th-90th percentile of fiber(54); Life's
      within that of fiber(22);
  P4  fiber(22) has >= 25% of rules with alpha_x > 0.9 and >= 25% below 0.5.

Both-positive means S* > 0 and alpha_x > 0.5. Rules with alpha_x undefined
(one horizon zero, the other not) are counted as not spreading.
"""
from __future__ import annotations
import json, math, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / 'results/fiber_census_20260917'

def kruskal_wallis(groups):
    allv = np.concatenate(groups); n = len(allv)
    order = np.argsort(allv, kind='mergesort'); ranks = np.empty(n); ranks[order] = np.arange(1, n + 1)
    # average ties
    vals = allv[order]; i = 0
    while i < n:
        j = i
        while j + 1 < n and vals[j + 1] == vals[i]: j += 1
        if j > i: ranks[order[i:j + 1]] = (i + 1 + j + 1) / 2
        i = j + 1
    h = 0.0; start = 0
    for g in groups:
        r = ranks[start:start + len(g)]; start += len(g)
        h += r.sum() ** 2 / len(g)
    h = 12 / (n * (n + 1)) * h - 3 * (n + 1)
    # tie correction
    _, counts = np.unique(allv, return_counts=True)
    c = 1 - np.sum(counts ** 3 - counts) / (n ** 3 - n)
    h = h / c if c > 0 else h
    df = len(groups) - 1
    # chi-square survival function for even df: exp(-x/2) * sum_{j<df/2} (x/2)^j / j!
    m = df // 2; x = h / 2
    p = math.exp(-x) * sum(x ** j / math.factorial(j) for j in range(m)) if df % 2 == 0 else float('nan')
    return float(h), float(p)

def summarize(rows):
    fibers = {}
    for r in rows: fibers.setdefault(r['base'], []).append(r)
    summ = {}
    for b, rs in sorted(fibers.items()):
        S = np.array([r['S_star'] if r['S_star'] is not None else 0.0 for r in rs])
        A = np.array([r['alpha_x'] if r['alpha_x'] is not None else -np.inf for r in rs])
        both = (S > 0) & (A > 0.5)
        summ[str(b)] = {'n': len(rs), 'both_positive_fraction': float(both.mean()),
                        'S_positive_fraction': float((S > 0).mean()), 'spread_fraction': float((A > 0.5).mean()),
                        'S_quartiles': [float(np.percentile(S, q)) for q in (10, 25, 50, 75, 90)],
                        'alpha_quartiles': [float(np.percentile(A[np.isfinite(A)], q)) for q in (10, 25, 50, 75, 90)],
                        'alpha_above_0.9_fraction': float((A > 0.9).mean()), 'alpha_below_0.5_fraction': float((A < 0.5).mean()),
                        'exemplars': {r['exemplar']: {'S_star': r['S_star'], 'alpha_x': r['alpha_x'], 'rulestring': r['rulestring']} for r in rs if r.get('exemplar')}}
    return fibers, summ

def main():
    d = json.loads((OUT / 'fiber_census_k2.json').read_text())
    fibers, summ = summarize(d['rows'])
    groups = [np.array([r['S_star'] or 0.0 for r in fibers[b]]) for b in (54, 22, 90, 204, 0)]
    H, p = kruskal_wallis(groups)
    bp = {b: summ[str(b)]['both_positive_fraction'] for b in (54, 22, 90, 204, 0)}
    def pct(b, key):
        S = np.array([r['S_star'] or 0.0 for r in fibers[b]]); return float(np.percentile(S, 10)), float(np.percentile(S, 90))
    ex54 = summ['54']['exemplars'].get('highlife'); ex22 = summ['22']['exemplars'].get('life')
    lo54, hi54 = pct(54, 'S'); lo22, hi22 = pct(22, 'S')
    preds = {
        'P1_fibers_differ': {'max_minus_min': max(bp.values()) - min(bp.values()), 'kruskal_H': H, 'kruskal_p': p,
                             'held': (max(bp.values()) - min(bp.values()) > 0.10) and p < 0.01},
        'P2_fiber54_enriched': {'fractions': {str(k): v for k, v in bp.items()},
                                'held': bp[54] > bp[0] and bp[54] > bp[204] and bp[54] > bp[90]},
        'P3_exemplars_typical': {'highlife_S': ex54['S_star'] if ex54 else None, 'fiber54_p10_p90': [lo54, hi54],
                                 'life_S': ex22['S_star'] if ex22 else None, 'fiber22_p10_p90': [lo22, hi22],
                                 'held': bool(ex54 and ex22 and lo54 <= (ex54['S_star'] or 0) <= hi54 and lo22 <= (ex22['S_star'] or 0) <= hi22)},
        'P4_fiber22_bimodal': {'above_0.9': summ['22']['alpha_above_0.9_fraction'], 'below_0.5': summ['22']['alpha_below_0.5_fraction'],
                               'held': summ['22']['alpha_above_0.9_fraction'] >= 0.25 and summ['22']['alpha_below_0.5_fraction'] >= 0.25},
    }
    import hashlib
    def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
    out = {'protocol': d['protocol'], 'height': d['height'], 'per_fiber': summ, 'predictions': preds,
           'source_hashes': {'protocol': sha(ROOT / 'docs/research/protocols/2026-09-17-fiber-census.md'),
                             'run': sha(HERE / 'run.py'), 'summarize': sha(HERE / 'summarize.py'),
                             'census_k2': sha(OUT / 'fiber_census_k2.json'), 'census_k4': sha(OUT / 'fiber_census_k4.json'),
                             'exactness_k2': sha(OUT / 'exactness_control_k2.json'), 'exactness_k4': sha(OUT / 'exactness_control_k4.json')}}
    k4 = OUT / 'fiber_census_k4.json'
    if k4.exists():
        d4 = json.loads(k4.read_text()); _, s4 = summarize(d4['rows']); out['k4_per_fiber'] = s4
    (OUT / 'summary.json').write_text(json.dumps(out, indent=1, sort_keys=True) + '\n')
    print(json.dumps({'per_fiber_both_positive': bp, 'predictions': {k: v['held'] for k, v in preds.items()}, 'kruskal': [H, p]}, indent=1))
    try:
        import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
        fig, axes = plt.subplots(1, 5, figsize=(15, 3.2), sharex=True, sharey=True)
        for ax, b in zip(axes, (54, 22, 90, 204, 0)):
            rs = fibers[b]
            S = [r['S_star'] or 0.0 for r in rs]; A = [r['alpha_x'] if r['alpha_x'] is not None else -0.1 for r in rs]
            ax.scatter(A, S, s=6, alpha=0.5, color='#4c72b0')
            for r in rs:
                if r.get('exemplar'): ax.scatter([r['alpha_x']], [r['S_star'] or 0], s=40, color='#c44e52', marker='D'); ax.annotate(r['exemplar'], (r['alpha_x'], r['S_star'] or 0), fontsize=7)
            ax.axvline(0.5, color='grey', lw=0.6, ls='--'); ax.set_title(f'fiber of ECA {b}  (both+ {bp[b]:.2f})', fontsize=9); ax.set_xlabel('alpha_x (64→128)')
        axes[0].set_ylabel('S* at height 2'); fig.tight_layout(); fig.savefig(OUT / 'fiber_census_k2.svg'); print('figure written')
    except Exception as e:
        print('figure skipped:', e)

if __name__ == '__main__':
    main()
