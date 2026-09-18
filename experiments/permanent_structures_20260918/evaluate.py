#!/usr/bin/env python3
"""Frozen analysis for permanent structures. Committed before the canonical run,
and EXERCISED AGAINST A PILOT rows.json first -- the seventh unit's evaluator
was committed untested and needed two post-freeze edits.

P1 is scored by iterating the gadget from each recorded trial's origin window
under the base's own input law, which T3 says is determined by the base alone
on the four frozen anchors: 204 constant (LL,RR), 51 alternating, 0 and 8
constant (0,0).
"""
from __future__ import annotations
import hashlib, json, math, statistics as st, sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RES = ROOT / 'results/permanent_structures_20260918'
FROZEN = [204, 51, 0, 8]
ARMS = ['Upp', 'Kall', 'Kex', 'Kbot', 'G', 'Gprime', 'random']
KARMS = ['Kall', 'Kex', 'Kbot']
BLOCK0 = {'frozen': [204, 51], 'leaky': [90, 37, 50, 178]}
A_TAB = {(0,0):(1,2), (0,1):(19,20), (1,0):(11,12), (1,1):(29,30)}
B_TAB = {(0,0):(2,16), (0,1):(5,19), (1,0):(12,26), (1,1):(15,29)}
C_TAB = {(0,0):(2,8),  (0,1):(5,11), (1,0):(20,26), (1,1):(23,29)}

def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b); a, b = a[ok], b[ok]
    if len(a) < 3: return None
    def rank(v):
        o = np.argsort(v, kind='mergesort'); r = np.empty(len(v), float); r[o] = np.arange(len(v))
        for val in np.unique(v):
            mm = v == val
            if mm.sum() > 1: r[mm] = r[mm].mean()
        return r
    ra, rb = rank(a), rank(b); ra, rb = ra-ra.mean(), rb-rb.mean()
    d = math.sqrt((ra*ra).sum()*(rb*rb).sum())
    return float((ra*rb).sum()/d) if d else None

def cv_r2(X, y, folds=4, lam=1.0):
    X = np.asarray(X, float); y = np.asarray(y, float)
    if len(y) < folds + 2 or np.std(y) == 0: return None
    idx = np.arange(len(y)); preds = np.zeros(len(y))
    for f in range(folds):
        te = idx % folds == f; tr = ~te
        if tr.sum() < 2 or te.sum() == 0: return None
        Xt = np.hstack([X[tr], np.ones((tr.sum(),1))]); yt = y[tr]
        A = Xt.T@Xt + lam*np.eye(Xt.shape[1]); w = np.linalg.solve(A, Xt.T@yt)
        preds[te] = np.hstack([X[te], np.ones((te.sum(),1))])@w
    ss = ((y-preds)**2).sum(); tot = ((y-y.mean())**2).sum()
    return float(1 - ss/tot) if tot > 0 else None

def gadget_from_sets(safe, doomed):
    return {tuple(s) for s in safe}, {tuple(s) for s in doomed}

def predict_heal(u_tab, start, window, base, steps=128):
    """Iterate the gadget under the base's own input law (frozen anchors only)."""
    t = u_tab
    a = lambda LL, L: t[A_TAB[(LL, L)][0]]
    c = lambda R, RR: t[C_TAB[(R, RR)][0]]
    Bh = {(L,R): t[B_TAB[(L,R)][0]] == t[B_TAB[(L,R)][1]] for L in (0,1) for R in (0,1)}
    LL0, RR0 = window[0], window[4]
    s = tuple(start)
    for step in range(1, steps+1):
        if base == 204:   LL, RR = LL0, RR0
        elif base == 51:  LL, RR = (LL0, RR0) if step % 2 == 1 else (1-LL0, 1-RR0)
        else:             LL, RR = 0, 0
        L, b, R = s
        if Bh[(L, R)]: return step
        lo, hi = B_TAB[(L, R)]
        s = (a(LL, L), t[lo] if b == 0 else t[hi], c(R, RR))
    return 129

def main(pilot=False):
    rows = json.loads((RES/'rows.json').read_text())['rows']
    gad = json.loads((RES/'gadget.json').read_text())
    alg = json.loads((RES/'algebra.json').read_text())
    pis = json.loads((RES/'pairs.json').read_text())['pi'] if (RES/'pairs.json').exists() else {}
    bb = alg['base_bits']
    sd = {int(k): gadget_from_sets(*v) for k, v in gad.get('safe_doomed', {}).items()}
    BASES = sorted({int(r['base']) for r in rows})

    by = {}
    for r in rows: by.setdefault((int(r['base']), r['arm']), []).append(r)

    per = {}
    for b in BASES:
        e = {}
        for arm in ARMS:
            rs = by.get((b, arm), [])
            if not rs: continue
            steps = max(1, rs[0].get('scored_steps', 1))
            e[arm] = {'n': len(rs),
                      'median_agree': float(st.median([float(x['agree']) for x in rs])),
                      'P_on': float(np.mean([x['on_beam'] for x in rs])),
                      'median_T_ext': float(st.median([float(x['T_ext']) for x in rs])),
                      'blind_per_step': float(np.mean([x['strata_column_steps'][0] for x in rs]))/steps,
                      'nonblind_per_step': float(np.mean([x['strata_column_steps'][1]+x['strata_column_steps'][2] for x in rs]))/steps,
                      'mean_isolated': float(np.mean([x['mean_isolated'] for x in rs])),
                      'width': float(np.sum([x['total_defect_column_steps'] for x in rs]) /
                                     max(1, np.sum([x['total_cluster_count'] for x in rs])))}
        e['beta'] = bb[str(b)]['beta']; e['e_G'] = bb[str(b)]['e_G']; e['e_Gprime'] = bb[str(b)]['e_Gprime']
        e['frozen'] = bb[str(b)]['frozen']; e['totalistic'] = bb[str(b)]['totalistic']
        if str(b) in pis: e.update(pis[str(b)])
        per[b] = e

    P = {}
    # P1 exactness on the frozen anchors
    p1 = {}
    for b in [x for x in FROZEN if x in BASES]:
        mism = 0; tot = 0
        for arm in KARMS:
            for r in by.get((b, arm), []):
                tab = [(int(r['table']) >> i) & 1 for i in range(32)]
                for start, win, heal in zip(r['trial_starts'], r['trial_windows'], r['heal_steps']):
                    tot += 1
                    if predict_heal(tab, start, win, b) != heal: mism += 1
        p1[b] = {'mismatches': mism, 'of': tot}
    P['P1'] = {'per_base': p1, 'held': all(v['mismatches'] == 0 for v in p1.values()) and bool(p1)}
    # P2 bounds
    viol = 0; tot2 = 0; kbot_bad = 0; safe_bad = 0
    for b in BASES:
        for arm in KARMS:
            for r in by.get((b, arm), []):
                s_, d_ = sd.get(int(r['u']), (set(), set()))
                nd = sum(1 for x in r['trial_starts'] if tuple(x) in d_)
                ns = sum(1 for x in r['trial_starts'] if tuple(x) in s_)
                n = len(r['trial_starts']); tot2 += 1
                lo, hi = nd/n, 1 - ns/n
                if not (lo - 1e-9 <= float(r['T_ext']) <= hi + 1e-9): viol += 1
                if arm == 'Kbot' and float(r['T_ext']) != 1.0: kbot_bad += 1
                for x, h in zip(r['trial_starts'], r['heal_steps']):
                    if tuple(x) in s_ and h != 129: safe_bad += 1
    P['P2'] = {'bound_violations': viol, 'of': tot2, 'Kbot_not_one': kbot_bad,
               'safe_healed': safe_bad, 'held': viol == 0 and kbot_bad == 0 and safe_bad == 0}
    # P3 base contribution
    order = all(per[b]['Kbot']['median_T_ext'] >= per[b]['Kex']['median_T_ext'] >= per[b]['Kall']['median_T_ext']
                for b in BASES if all(a in per[b] for a in KARMS))
    spread_ex = max(per[b]['Kex']['median_T_ext'] for b in BASES) - min(per[b]['Kex']['median_T_ext'] for b in BASES)
    spread_all = max(per[b]['Kall']['median_T_ext'] for b in BASES) - min(per[b]['Kall']['median_T_ext'] for b in BASES)
    fr = [b for b in BLOCK0['frozen'] if b in BASES]; lk = [b for b in BLOCK0['leaky'] if b in BASES]
    c_ok = (max(per[b]['Kex']['median_T_ext'] for b in fr) < min(per[b]['Kex']['median_T_ext'] for b in lk)
            and min(per[b]['Kex']['nonblind_per_step'] for b in fr) > max(per[b]['Kex']['nonblind_per_step'] for b in lk)) if fr and lk else None
    P['P3a'] = {'ordering_holds_every_base': order, 'held': order}
    P['P3b'] = {'spread_Kex': spread_ex, 'spread_Kall': spread_all,
                'ratio': spread_ex/spread_all if spread_all > 0 else None,
                'held': spread_all > 0 and spread_ex >= 2*spread_all}
    P['P3c'] = {'frozen': {b: per[b]['Kex']['median_T_ext'] for b in fr},
                'leaky': {b: per[b]['Kex']['median_T_ext'] for b in lk}, 'held': bool(c_ok)}
    # P4 residence is permanence
    per_base = {}
    for b in BASES:
        rs = [r for arm in KARMS for r in by.get((b, arm), [])]
        if len(rs) < 6: continue
        steps = max(1, rs[0].get('scored_steps', 1))
        nb = [(r['strata_column_steps'][1]+r['strata_column_steps'][2])/steps for r in rs]
        te = [float(r['T_ext']) for r in rs]
        per_base[b] = spearman(nb, te)
    pooled_nb = []; pooled_te = []
    for b in BASES:
        for arm in KARMS:
            for r in by.get((b, arm), []):
                steps = max(1, r.get('scored_steps', 1))
                pooled_nb.append((r['strata_column_steps'][1]+r['strata_column_steps'][2])/steps)
                pooled_te.append(float(r['T_ext']))
    pooled = spearman(pooled_nb, pooled_te)
    rnd = {}
    for b in BASES:
        rs = by.get((b, 'random'), [])
        if len(rs) < 6: continue
        steps = max(1, rs[0].get('scored_steps', 1))
        rnd[b] = spearman([(r['strata_column_steps'][1]+r['strata_column_steps'][2])/steps for r in rs],
                          [float(r['T_ext']) for r in rs])
    weaker = sum(1 for b in per_base if b in rnd and rnd[b] is not None and per_base[b] is not None
                 and rnd[b] >= per_base[b] + 0.2)
    P['P4'] = {'pooled': pooled, 'per_base_all_below': all(v is not None and v <= -0.6 for v in per_base.values()),
               'n_bases': len(per_base), 'random_weaker_in': weaker,
               'held_pooled': pooled is not None and pooled <= -0.7,
               'held_every_base': all(v is not None and v <= -0.6 for v in per_base.values()),
               'held_b': weaker >= 24}
    # P5 specificity, correctly formed
    pi = [per[b].get('Pi_512') for b in BASES]
    kblind = [np.mean([per[b][a]['blind_per_step'] for a in KARMS if a in per[b]]) for b in BASES]
    leaky = [b for b in BASES if per[b].get('Pi_512') is not None and b not in FROZEN]
    P['P5a'] = {'spearman': spearman(kblind, pi), 'held': (spearman(kblind, pi) or -1) >= 0.75}
    s5b = spearman([per[b]['Kall']['nonblind_per_step'] for b in leaky], [per[b]['Pi_512'] for b in leaky])
    P['P5b'] = {'spearman': s5b, 'n': len(leaky), 'held': s5b is not None and abs(s5b) <= 0.4}
    # P6 handedness with power
    disc = [b for b in BASES if per[b]['e_G'] != per[b]['e_Gprime']]
    agree6 = sum(1 for b in disc
                 if np.sign(per[b]['G']['width'] - per[b]['Gprime']['width'])
                 == np.sign(per[b]['e_Gprime'] - per[b]['e_G']))
    P['P6'] = {'n_discriminating': len(disc), 'agreeing': agree6,
               'verdict': 'supports' if agree6 >= 14 else ('refutes' if agree6 <= 9 else 'unsupported'),
               'held': agree6 >= 14}
    # P7 census identity and additivity
    add_rand = {}; add_k = {}
    npairs = len(alg['pair_keys'])
    for b in BASES:
        for label, arms_, store in (('random', ['random'], add_rand), ('K', KARMS, add_k)):
            rs = [r for a in arms_ for r in by.get((b, a), [])]
            if len(rs) < 8: continue
            X = np.array([[(int(r['u']) >> i) & 1 for i in range(24)] for r in rs], float)
            y = np.array([1 - float(r['agree']) for r in rs])
            store[b] = cv_r2(X, y)
    P['P7b'] = {'max_random_R2': max([v for v in add_rand.values() if v is not None], default=None),
                'n': len(add_rand),
                'held': all(v is None or v <= 0.3 for v in add_rand.values())}
    P['P7c'] = {'n_over_0.4': sum(1 for v in add_k.values() if v is not None and v >= 0.4),
                'n': len(add_k), 'held': sum(1 for v in add_k.values() if v is not None and v >= 0.4) >= 24}

    out = {'per_base': per, 'predictions': P, 'n_rows': len(rows),
           'descriptive': {'cv_r2_random': add_rand, 'cv_r2_K': add_k,
                           'P4_per_base': per_base, 'P4_random': rnd}}
    if not pilot:
        def sha(rel): return hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()
        out['source_hashes'] = {
            'protocol': sha('docs/research/protocols/2026-09-18-permanent-structures.md'),
            'run': sha('experiments/permanent_structures_20260918/run.py'),
            'evaluate': sha('experiments/permanent_structures_20260918/evaluate.py'),
            'rows': sha('results/permanent_structures_20260918/rows.json'),
            'controls': sha('results/permanent_structures_20260918/controls.json'),
            'gadget': sha('results/permanent_structures_20260918/gadget.json'),
            'algebra': sha('results/permanent_structures_20260918/algebra.json'),
            'pairs': sha('results/permanent_structures_20260918/pairs.json')}
        (RES/'summary.json').write_text(json.dumps(out, indent=1, default=str))
    print(f'rows {len(rows)}')
    for k in sorted(P): print(f'  {k}: {json.dumps({kk:vv for kk,vv in P[k].items() if kk.startswith("held") or kk=="verdict"}, default=str)}')
    return out

if __name__ == '__main__':
    main(pilot='--pilot' in sys.argv)
