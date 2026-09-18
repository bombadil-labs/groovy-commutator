#!/usr/bin/env python3
"""Frozen analysis for the defect-algebra unit (protocol sections 3-4).

Written and committed before the canonical run; thresholds are the protocol's
and are not changed after any output is read. Every prediction is calibrated
on earlier canonical rows or the drafting agent's pilot and is declared so;
the unit is a pre-registered out-of-sample replication on fresh and built
completions, not a set of blind bets.

P3(a') is scored over the five class cells, not four: the freeze amendment
added the eastward grower G', which the draft had proposed to deduce.
"""
from __future__ import annotations
import hashlib, json, math
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / 'results/defect_algebra_20260918'
NONFROZEN = [110, 54, 22, 5, 30, 90]
LIT = sorted({1,2,5,8,11,12,15,16,19,20,23,26,29,30})

def rank(x): return pd.Series(x).rank().to_numpy(float)
def pearson(a,b):
    a = np.asarray(a,float)-np.mean(a); b = np.asarray(b,float)-np.mean(b)
    d = math.sqrt((a*a).sum()*(b*b).sum())
    return float((a*b).sum()/d) if d else None
def spearman(a,b): return pearson(rank(a), rank(b))

def ridge_cv_r2(X, y, lam=1.0, folds=8, seed=0):
    X = np.asarray(X, float); y = np.asarray(y, float)
    if np.allclose(y, y[0]): return None
    n = len(y); idx = np.random.default_rng(seed).permutation(n); pred = np.zeros(n)
    Xd = np.column_stack([np.ones(n), X])
    for f in range(folds):
        te = idx[f::folds]; tr = np.setdiff1d(idx, te)
        A = Xd[tr].T @ Xd[tr] + lam*np.eye(Xd.shape[1]); A[0,0] -= lam
        w = np.linalg.solve(A, Xd[tr].T @ y[tr]); pred[te] = Xd[te] @ w
    ss_res = ((y-pred)**2).sum(); ss_tot = ((y-y.mean())**2).sum()
    return float(1 - ss_res/ss_tot) if ss_tot > 0 else None

def main():
    d = json.loads((OUT / 'rows.json').read_text())
    df = pd.DataFrame(d['rows'])
    bases = d['bases']; CONS = [tuple(c) for c in d['constraints']]
    FREE = sorted({e for c in CONS for e in c} | set(range(32)) - set())  # placeholder, real FREE below
    import importlib.util, sys
    spec = importlib.util.spec_from_file_location('hf', ROOT/'experiments/handed_fiber_census_20260917/run.py')
    hf = importlib.util.module_from_spec(spec); sys.modules['hf']=hf; spec.loader.exec_module(hf)
    FREE = hf.FREE; POS = {e:i for i,e in enumerate(FREE)}

    def bits24(u): return [(u >> i) & 1 for i in range(24)]
    def bits12(sig): return [(sig >> k) & 1 for k in range(12)]

    rnd = df[df.arm == 'random']; flip = df[df.arm == 'flip']; cls = df[df.arm == 'class']

    # ---- P1, P5: regressions per base on the random arm
    reg = {}
    for b in bases:
        s = rnd[rnd.base == b]
        X24 = np.array([bits24(int(u)) for u in s.completion])
        X12 = np.array([bits12(int(g)) for g in s.signature])
        X3  = np.array([list(t) for t in s.nABC])
        XH  = np.array(s.H1).reshape(-1,1)
        reg[str(b)] = {}
        for tgt in ('T_ext','agree','M_star'):
            y = s[tgt].fillna(0).to_numpy(float)
            reg[str(b)][tgt] = {'raw24': ridge_cv_r2(X24,y,seed=17), 'heal12': ridge_cv_r2(X12,y,seed=17),
                                'nABC': ridge_cv_r2(X3,y,seed=17), 'H1': ridge_cv_r2(XH,y,seed=17)}
    # ---- P2 and gating
    h1 = {}
    for b in bases:
        s = rnd[rnd.base == b]
        z = s.H1.to_numpy(float)
        h1[str(b)] = {'spearman_T_ext': spearman(z, s.T_ext.to_numpy(float)),
                      'spearman_agree': spearman(z, s.agree.to_numpy(float)),
                      'P_on_given_H1_zero': float(s.on_beam[z == 0].mean()) if (z == 0).any() else None,
                      'P_Text_hi_given_H1_zero': float((s.T_ext[z == 0] >= 0.9).mean()) if (z == 0).any() else None}
    # ---- P4: flip arm
    tagmap = {}
    for _, r in flip.iterrows():
        kind, parent = str(r.tag).split(':'); tagmap.setdefault((r.base, kind), {})[int(parent)] = r
    flips = {}
    for b in bases:
        e = {}
        par = rnd[rnd.base == b].set_index('completion')
        for kind in ('dark','lit'):
            m = tagmap.get((b, kind), {})
            pu = [u for u in m if u in par.index]
            for tgt in ('T_ext','agree'):
                a = [float(par.loc[u, tgt]) for u in pu]; c = [float(m[u][tgt]) for u in pu]
                e[f'{kind}_{tgt}_spearman'] = spearman(a, c)
                e[f'{kind}_{tgt}_median_abs_delta'] = float(np.median(np.abs(np.array(a)-np.array(c))))
            e[f'{kind}_n'] = len(pu)
        flips[str(b)] = e
    # ---- P3: class arm
    cell = {}
    for b in bases:
        cell[str(b)] = {}
        for name in ('Uplus','Uminus','G','Gprime','K'):
            s = cls[(cls.base == b) & (cls.tag == name)]
            cell[str(b)][name] = {'n': int(len(s)), 'median_agree': float(s.agree.median()),
                                  'P_on': float(s.on_beam.mean()), 'P_off': float(s.off_beam.mean()),
                                  'mean_T_ext': float(s.T_ext.mean()), 'median_M': float(s.M_star.median())}
        r = rnd[rnd.base == b]
        cell[str(b)]['random'] = {'median_agree': float(r.agree.median()), 'P_on': float(r.on_beam.mean()),
                                  'mean_T_ext': float(r.T_ext.mean())}
    # ---- P6: healing times on the random arm
    heal = {}
    for b in bases:
        s = rnd[rnd.base == b]
        ts = [t for row in s.heal_times for t in row]
        healed = [t for t in ts if t is not None]
        heal[str(b)] = {'n_trials': len(ts), 'n_healed': len(healed),
                        'cum': {str(k): (float(np.mean([t <= k for t in healed])) if healed else None)
                                for k in (1,2,4,8,16,32,64)}}
    ctrl = json.loads((OUT / 'controls.json').read_text())

    P1 = {str(b): {'T_ext_heal12': reg[str(b)]['T_ext']['heal12'], 'T_ext_raw24': reg[str(b)]['T_ext']['raw24'],
                   'agree_heal12': reg[str(b)]['agree']['heal12'], 'agree_raw24': reg[str(b)]['agree']['raw24']}
          for b in bases}
    p1_held = all(P1[str(b)]['T_ext_heal12'] is not None and P1[str(b)]['T_ext_heal12'] >= 0.15
                  and P1[str(b)]['T_ext_raw24'] <= 0.10
                  and P1[str(b)]['agree_heal12'] >= 0.10 and P1[str(b)]['agree_raw24'] <= 0.10 for b in bases)
    p2_held = all(h1[str(b)]['spearman_T_ext'] is not None and h1[str(b)]['spearman_T_ext'] >= 0.50 for b in bases)
    p3a = all(cell[str(b)]['Uplus']['median_agree'] >= 0.95 and cell[str(b)]['Uplus']['P_on'] >= 0.50 for b in bases)
    p3a2 = all(cell[str(b)]['Uplus']['median_agree'] >=
               max(cell[str(b)][n]['median_agree'] for n in ('Uminus','G','Gprime','K')) for b in bases)
    p3b = all(cell[str(b)][n]['P_on'] <= 0.02 and cell[str(b)][n]['median_agree'] < cell[str(b)]['random']['median_agree']
              for b in bases for n in ('Uminus','G'))
    p3c = all(cell[str(b)]['K']['mean_T_ext'] >= cell[str(b)]['random']['mean_T_ext'] for b in bases)
    def p4(tgt):
        return all(flips[str(b)][f'dark_{tgt}_spearman'] is not None
                   and flips[str(b)][f'dark_{tgt}_spearman'] >= 0.50
                   and flips[str(b)][f'dark_{tgt}_spearman'] > flips[str(b)][f'lit_{tgt}_spearman']
                   and flips[str(b)][f'dark_{tgt}_median_abs_delta'] <= 0.10 for b in bases)
    p5_held = (all(reg[str(b)]['M_star']['heal12'] is not None and reg[str(b)]['M_star']['heal12'] >= 0.15
                   for b in (110,54,5))
               and all(reg[str(b)]['M_star']['heal12'] <= 0.10 for b in (30,90,0,204)))
    p6_held = all(heal[str(b)]['cum']['1'] is not None and heal[str(b)]['cum']['1'] <= 0.45 for b in NONFROZEN)

    preds = {
      'P1_healing_bits_are_the_structure': {'per_base': P1, 'held': p1_held},
      'P2_H1_predicts_transverse_stability': {'spearman': {str(b): h1[str(b)]['spearman_T_ext'] for b in bases},
                                              'held': p2_held},
      'P3_built_classes': {'a_held': p3a, 'a_prime_held_over_five_cells': p3a2, 'b_held': p3b, 'c_held': p3c,
                           'held': p3a, 'cells': cell},
      'P4_dark_flips': {'a_T_ext_held': p4('T_ext'), 'b_agree_held_expected_to_fail': p4('agree'),
                        'per_base': flips, 'held': p4('T_ext')},
      'P5_structure_reaches_M': {'heal12_R2': {str(b): reg[str(b)]['M_star']['heal12'] for b in bases},
                                 'held': p5_held},
      'P6_most_healing_is_not_first_step': {'frac_step_one': {str(b): heal[str(b)]['cum']['1'] for b in bases},
                                            'held': p6_held},
    }
    def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
    out = {'protocol': d['protocol'],
           'standing': ('Every prediction is calibrated on earlier canonical rows or the drafting agent\'s pilot '
                        'and declared so; this is a pre-registered out-of-sample replication on fresh and built '
                        'completions. The defect algebra itself is exact and independent of how P1-P6 score. '
                        "P3(a') is scored over five class cells, not four: the freeze amendment added the "
                        'eastward grower, which the draft had proposed to deduce.'),
           'regressions': reg, 'H1': h1, 'flips': flips, 'cells': cell, 'healing_times': heal,
           'matched_null_pairs_identical': ctrl['all_matched_identical'], 'predictions': preds,
           'source_hashes': {'protocol': sha(ROOT/'docs/research/protocols/2026-09-18-defect-algebra.md'),
                             'run': sha(HERE/'run.py'), 'evaluate': sha(HERE/'evaluate.py'),
                             'rows': sha(OUT/'rows.json'), 'controls': sha(OUT/'controls.json')}}
    (OUT / 'summary.json').write_text(json.dumps(out, indent=1, sort_keys=True, allow_nan=False) + '\n')
    print(json.dumps({k: v.get('held') for k, v in preds.items()}, indent=1))
    print("P3a'", p3a2, '| P3b', p3b, '| P3c', p3c, '| P4b (expected fail)', p4('agree'))

if __name__ == '__main__':
    main()
