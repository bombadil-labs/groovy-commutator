#!/usr/bin/env python3
"""Frozen analysis for the held-structures unit (Class-IV Refinement, ninth unit).

Committed before the canonical run. Scores EVERY key in the protocol's frozen
list or writes `not_evaluated` with a reason under that key -- the rule earned
from PR #278, where two frozen predictions of the eighth unit were silently
never scored and reported as unsupported. Control 14 in the runner compares this
evaluator's key set to the protocol's machine-readable list before any tier runs,
so "unscored" is a recorded verdict and never an absence.

    python experiments/held_structures_20260918/evaluate.py            # canonical
    python experiments/held_structures_20260918/evaluate.py --pilot F  # control 14
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('u9', HERE / 'run.py')
u9 = importlib.util.module_from_spec(spec); sys.modules['u9'] = u9; spec.loader.exec_module(u9)

STRUCTS, PAIR_KEYS = u9.STRUCTS, u9.PAIR_KEYS
SI = {n: STRUCTS.index(n) for n in STRUCTS}
BLIND = ['alt_edge_w', 'alt_edge_e']
NONBLIND = ['singleton', 'alt_interior', 'inphase_interior', 'inphase_edge_w', 'inphase_edge_e']
KALL = ['Kall_plus', 'Kall_minus']
KARMS = KALL + ['Kex']
UNDRIVEN = [0, 51, 204, 8]
NINETY_CLASS = [90, 91, 218, 219]
OUT = ROOT / 'results/held_structures_20260918'

class Insufficient(Exception): pass

# ------------------------------------------------------------- statistics

def rank(v):
    v = np.asarray(v, dtype=float); o = np.argsort(v, kind='mergesort')
    r = np.empty(len(v), dtype=float); r[o] = np.arange(len(v), dtype=float)
    i = 0
    while i < len(v):
        j = i
        while j+1 < len(v) and v[o[j+1]] == v[o[i]]: j += 1
        if j > i: r[o[i:j+1]] = (i+j)/2.0
        i = j+1
    return r

def spearman(a, b):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    if len(a) < 3: raise Insufficient(f'n={len(a)} < 3')
    ra, rb = rank(a), rank(b)
    sa, sb = ra.std(), rb.std()
    if sa == 0 or sb == 0: raise Insufficient('constant on one side')
    return float(((ra-ra.mean())*(rb-rb.mean())).mean()/(sa*sb))

def boot_spearman(a, b, n=2000, tag='boot'):
    a, b = np.asarray(a, float), np.asarray(b, float)
    rng = np.random.default_rng(int(hashlib.sha256(tag.encode()).hexdigest()[:8], 16))
    out = []
    for _ in range(n):
        i = rng.integers(0, len(a), len(a))
        try: out.append(spearman(a[i], b[i]))
        except Insufficient: pass
    if len(out) < n//4: raise Insufficient('bootstrap degenerate')
    q = np.quantile(out, [0.025, 0.975])
    return [float(q[0]), float(q[1])]

def median(v):
    if not len(v): raise Insufficient('empty')
    return float(np.median(np.asarray(v, dtype=float)))

# ------------------------------------------------------------ row derivation

def per_step(row, names):
    n = row.get('scored_steps') or 0
    if not n: raise Insufficient('no scored steps')
    sc = row['structural_census']
    return sum(sc[SI[m]] for m in names) / n

def derive(rows):
    for r in rows:
        r['S'] = per_step(r, ['singleton'])
        r['I'] = per_step(r, ['alt_interior'])
        r['Q'] = per_step(r, ['inphase_interior', 'inphase_edge_w', 'inphase_edge_e'])
        r['blind'] = per_step(r, BLIND)
    return rows

def sel(rows, arms=None, bases=None):
    out = [r for r in rows
           if (arms is None or r['arm'] in arms) and (bases is None or r['base'] in bases)]
    if not out: raise Insufficient('no rows match')
    return out

def need_bases(rows, want, label):
    """A claim quantified over a set of bases is not scorable on a subset.

    Without this a five-row pilot reports FAILED for 'on every base', which is
    exactly the kind of verdict-from-absence PR #278 was about."""
    have = {r['base'] for r in rows}
    miss = [b for b in want if b not in have]
    if miss: raise Insufficient(f'{label}: {len(miss)} of {len(want)} bases absent')
    return sorted(want)

def by_base(rows, arms, f):
    d = {}
    for r in sel(rows, arms): d.setdefault(r['base'], []).append(r)
    return {b: f(v) for b, v in d.items()}

# ------------------------------------------------------------ the predictions

def P1a(R, ctx):
    bad = []
    for r in R:
        sc = r['structural_census']
        want = sum(sc[SI[m]] for m in BLIND + NONBLIND)
        if want != r['total_defect_column_steps']:
            bad.append([r['base'], r['u'], want, r['total_defect_column_steps']])
    return {'violations': len(bad), 'rows': len(R), 'examples': bad[:3],
            'verdict': 'HELD' if not bad else 'FAILED'}

def P1b(R, ctx):
    # The violation bit must come from the FULL table: the exposed entries are
    # held by the BASE, not the completion, so tab_of_u -- which leaves them 0 --
    # marks every alternating-edge pair held and fails on the base-held reads.
    viol = {}
    for r in R:
        key = int(r['table'])
        if key not in viol:
            t = [(key >> i) & 1 for i in range(32)]
            viol[key] = np.array([int(t[a] != t[b]) for a, b in PAIR_KEYS], dtype=np.int64)
        want = viol[key] * np.array(r['pair_census'], dtype=np.int64)
        got = np.array(r['pair_survival'], dtype=np.int64)
        if not np.array_equal(want, got):
            ctx.setdefault('_p1b', []).append([r['base'], r['u'],
                                               int(np.abs(want-got).sum())])
    bad = ctx.get('_p1b', [])
    return {'violations': len(bad), 'rows': len(R), 'examples': bad[:3],
            'verdict': 'HELD' if not bad else 'FAILED'}

def _snaps(r):
    s = r.get('isolated_snapshots') or {}
    if '0' not in s or '255' not in s: raise Insufficient('no isolated snapshots')
    return s['0'], s['255']

def P2a(R, ctx):
    rows = sel(R, KARMS); bad = []; n = 0
    for r in rows:
        try: s0, s1 = _snaps(r)
        except Insufficient: continue
        safe = {tuple(x) for x in u9.gadget(r['u'])[0]}
        keep = {(x[1]) for x in s1 if x[0] == 'singleton'}
        for kind, lo, hi, gs in s0:
            if kind != 'singleton' or gs is None or tuple(gs) not in safe: continue
            n += 1
            if lo not in keep: bad.append([r['base'], r['u'], lo])
    if not n: raise Insufficient('no isolated SAFE singletons at step 1')
    return {'violations': len(bad), 'safe_singletons': n, 'examples': bad[:3],
            'verdict': 'HELD' if not bad else 'FAILED'}

def P2b(R, ctx):
    bad = []; n = 0
    for r in sel(R, KARMS, u9.PAIR_PERMANENT):
        if tuple(r['alphas']) != u9.matching_pattern(r['base']): continue
        try: s0, s1 = _snaps(r)
        except Insufficient: continue
        keep = {(x[1], x[2]) for x in s1 if x[0] == 'alt_run'}
        for kind, lo, hi, _ in s0:
            if kind != 'alt_run': continue
            n += 1
            if (lo, hi) not in keep: bad.append([r['base'], r['u'], lo, hi])
    if not n: raise Insufficient('no isolated alternating runs on matching-pattern rows')
    return {'violations': len(bad), 'alt_runs': n, 'examples': bad[:3],
            'verdict': 'HELD' if not bad else 'FAILED'}

def P2c(R, ctx):
    pi = ctx.get('pi')
    if not pi: raise Insufficient('no pair-survival tier (pilot rows carry none)')
    pp = {b: pi[str(b)]['Pi_512'] for b in u9.PAIR_PERMANENT if str(b) in pi}
    other = {b: pi[str(b)]['Pi_512'] for b in u9.BLOCK0
             if b not in u9.PAIR_PERMANENT and str(b) in pi}
    if len(pp) != 8 or len(other) != 8: raise Insufficient('block 0000 incomplete in the Pi tier')
    ok = all(v == 1.0 for v in pp.values()) and all(v < 1.0 for v in other.values())
    return {'pair_permanent_Pi512': pp, 'other_block0_Pi512': other,
            'verdict': 'HELD' if ok else 'FAILED'}

def P3a(R, ctx):
    need_bases(sel(R, KALL), u9.BASES, 'P3a quantifies over every base')
    m = by_base(R, KALL, lambda v: float(np.mean([x['S'] for x in v])))
    out = {str(b): round(v, 3) for b, v in sorted(m.items())}
    bad = {k: v for k, v in out.items() if not (40.0 <= v <= 80.0)}
    return {'base_mean_S': out, 'outside_band': bad, 'band': [40, 80],
            'verdict': 'HELD' if not bad else 'FAILED'}

def P3b(R, ctx):
    need_bases(sel(R, KARMS), u9.BASES, 'P3b quantifies over every base')
    res = {}
    for b, v in sorted(by_base(R, KARMS, lambda v: v).items()):
        try: res[str(b)] = round(spearman([x['S'] for x in v], [x['n_safe'] for x in v]), 3)
        except Insufficient as e: res[str(b)] = f'insufficient: {e}'
    num = {k: v for k, v in res.items() if isinstance(v, float)}
    if not num: raise Insufficient('no base admitted a Spearman')
    bad = {k: v for k, v in num.items() if v < 0.7}
    return {'per_base_spearman': res, 'n_completions': len(sel(R, KARMS))//max(len(num),1),
            'below_threshold': bad, 'min': min(num.values()),
            'verdict': 'HELD' if not bad else 'FAILED'}

def _leaky(ctx, exclude_pp=False):
    pi = ctx.get('pi')
    if not pi: raise Insufficient('no pair-survival tier (pilot rows carry none)')
    bs = [int(b) for b, v in pi.items() if v['Pi_512'] > 0]
    if exclude_pp: bs = [b for b in bs if b not in u9.PAIR_PERMANENT]
    if len(bs) < 3: raise Insufficient(f'only {len(bs)} leaky bases')
    return sorted(bs)

def _base_arm_stat(R, arms, bases, field):
    m = by_base(sel(R, arms, bases), arms, lambda v: float(np.mean([x[field] for x in v])))
    bs = sorted(m)
    if len(bs) < 3: raise Insufficient(f'{len(bs)} bases with rows')
    return bs, [m[b] for b in bs]

def P3c(R, ctx):
    bases = _leaky(ctx, exclude_pp=True)
    need_bases(sel(R, KARMS), bases, 'P3c quantifies over the leaky non-pair-permanent bases')
    bs, S = _base_arm_stat(R, KARMS, set(bases), 'S')
    pi = [ctx['pi'][str(b)]['Pi_512'] for b in bs]
    rho = spearman(S, pi)
    return {'n_bases': len(bs), 'bases': bs, 'spearman_S_Pi': round(rho, 3),
            'bootstrap95': [round(x, 3) for x in boot_spearman(S, pi, tag='P3c')],
            'threshold': 0.4, 'verdict': 'HELD' if abs(rho) <= 0.4 else 'FAILED'}

def P3d(R, ctx):
    need_bases(sel(R, KARMS), u9.BASES, 'P3d is the minimum over the whole panel')
    m = by_base(R, KARMS, lambda v: float(np.mean([x['S'] for x in v])))
    lo = min(m, key=lambda b: m[b])
    return {'lowest_base': lo, 'lowest_mean_S': round(m[lo], 3),
            'pair_permanent': lo in u9.PAIR_PERMANENT,
            'verdict': 'HELD' if lo in u9.PAIR_PERMANENT else 'FAILED'}

def P4a(R, ctx):
    bad = []; n = 0
    for r in sel(R, KARMS, set(UNDRIVEN)):
        for t in r['trials']:
            n += 1
            if t['heal_free_pred'] != t['heal']:
                bad.append([r['base'], r['u'], t['origin'], t['heal_free_pred'], t['heal']])
    return {'violations': len(bad), 'trials': n, 'examples': bad[:3],
            'verdict': 'HELD' if not bad else 'FAILED'}

def P4b(R, ctx):
    per = {}
    for r in sel(R, KARMS, set(NINETY_CLASS + [110])):
        d = per.setdefault(r['base'], [])
        d.extend(int(t['stream_divergence'] <= 4) for t in r['trials'])
    if not per: raise Insufficient('no rows on the 90-class or 110')
    frac = {str(b): round(float(np.mean(v)), 3) for b, v in sorted(per.items())}
    bad = {k: v for k, v in frac.items() if v < 0.90}
    return {'fraction_diverging_by_step_4': frac, 'below_threshold': bad,
            'verdict': 'HELD' if not bad else 'FAILED'}

def P4c(R, ctx):
    agree = []
    for r in sel(R, ['Kex'], None):
        if r['base'] in UNDRIVEN: continue
        agree.extend(int((t['heal_free_pred'] <= 128) == (t['heal'] <= 128)) for t in r['trials'])
    if not agree: raise Insufficient('no Kex trials on driven bases')
    f = float(np.mean(agree))
    return {'agreement': round(f, 4), 'trials': len(agree), 'threshold': 0.90,
            'note': 'odds 0.4 at freeze -- expected to fail',
            'verdict': 'HELD' if f >= 0.90 else 'FAILED'}

def P4d(R, ctx):
    rows = [r for r in sel(R, ['Kex'], None) if r['base'] not in UNDRIVEN]
    if len(rows) < 3: raise Insufficient('fewer than 3 Kex rows on driven bases')
    a = [r['T_ext'] for r in rows]; b = [r['T_ext_free_pred'] for r in rows]
    rho = spearman(a, b)
    return {'n_rows': len(rows), 'spearman': round(rho, 3),
            'bootstrap95': [round(x, 3) for x in boot_spearman(a, b, tag='P4d')],
            'threshold': 0.7, 'verdict': 'HELD' if rho >= 0.7 else 'FAILED'}

def P5a_i(R, ctx):
    rows = sel(R, ['Kall_minus', 'Uplus'])
    bad = [[r['base'], r['u'], round(r['I'], 3)] for r in rows if r['I'] > 5.0]
    return {'rows': len(rows), 'violations': len(bad), 'max_I': round(max(r['I'] for r in rows), 3),
            'examples': bad[:3], 'verdict': 'HELD' if not bad else 'FAILED'}

def P5a_ii(R, ctx):
    pi = ctx.get('pi')
    if not pi: raise Insufficient('no pair-survival tier (pilot rows carry none)')
    quiet = {int(b) for b, v in pi.items() if v['Pi_512'] == 0}
    if not quiet: raise Insufficient('no Pi = 0 base on the panel')
    m = by_base(sel(R, ['Kall_plus'], quiet), ['Kall_plus'],
                lambda v: float(np.mean([x['I'] for x in v])))
    bad = {str(b): round(v, 3) for b, v in m.items() if v > 5.0}
    return {'quiet_bases': sorted(quiet), 'mean_I': {str(b): round(v, 3) for b, v in sorted(m.items())},
            'violations': bad, 'verdict': 'HELD' if not bad else 'FAILED'}

def _sub(R, base, matching):
    want = u9.matching_pattern(base)
    return [r for r in R if r['base'] == base and r['arm'] == 'Kall_plus'
            and (tuple(r['alphas']) == want) == matching]

def P5a_iii(R, ctx):
    need_bases(sel(R, ['Kall_plus']), u9.PAIR_PERMANENT, 'P5a-iii quantifies over all eight')
    res = {}; bad = []
    for b in u9.PAIR_PERMANENT:
        s = _sub(R, b, True)
        if not s: continue
        k = sum(1 for r in s if r['I'] >= 10.0)
        res[str(b)] = [k, len(s)]
        if not (k >= 5 and len(s) >= 6): bad.append(b)
    if not res: raise Insufficient('no matching-pattern rows on pair-permanent bases')
    return {'matching_rows_with_I_at_least_10': res, 'failing_bases': bad,
            'verdict': 'HELD' if not bad and len(res) == 8 else 'FAILED'}

def P5b(R, ctx):
    need_bases(sel(R, ['Kall_plus']), u9.PAIR_PERMANENT, 'P5b quantifies over all eight')
    res = {}; ok = 0
    for b in u9.PAIR_PERMANENT:
        m, o = _sub(R, b, True), _sub(R, b, False)
        if not m or not o: continue
        mm, mo = median([r['I'] for r in m]), median([r['I'] for r in o])
        res[str(b)] = [round(mm, 3), round(mo, 3)]
        ok += int(mm > mo)
    if not res: raise Insufficient('no pair-permanent base carries both sub-arms')
    return {'median_I_matching_vs_opposite': res, 'bases_holding': ok, 'of': len(res),
            'verdict': 'HELD' if ok == 8 and len(res) == 8 else 'FAILED'}

def P5c(R, ctx):
    pi = ctx.get('pi')
    if not pi: raise Insufficient('no pair-survival tier (pilot rows carry none)')
    need_bases(sel(R, ['Kall_plus']), u9.BLOCK0, 'P5c quantifies over block 0000')
    bs, I = _base_arm_stat(R, ['Kall_plus'], set(u9.BLOCK0), 'I')
    p = [pi[str(b)]['Pi_512'] for b in bs]
    rho = spearman(I, p)
    return {'n_bases': len(bs), 'spearman_I_Pi': round(rho, 3),
            'bootstrap95': [round(x, 3) for x in boot_spearman(I, p, tag='P5c')],
            'threshold': 0.5, 'verdict': 'HELD' if rho <= 0.5 else 'FAILED'}

def P5d(R, ctx):
    bases = _leaky(ctx)
    need_bases(sel(R, KALL), bases, 'P5d quantifies over the leaky bases')
    bs, Q = _base_arm_stat(R, KALL, set(bases), 'Q')
    p = [ctx['pi'][str(b)]['Pi_512'] for b in bs]
    rho = spearman(Q, p)
    return {'n_bases': len(bs), 'spearman_Q_Pi': round(rho, 3),
            'bootstrap95': [round(x, 3) for x in boot_spearman(Q, p, tag='P5d')],
            'threshold': 0.5, 'note': 'odds 0.45 at freeze -- expected to weaken',
            'verdict': 'HELD' if rho >= 0.5 else 'FAILED'}

def _arm_vs_pi(R, ctx, arm, tag):
    bases = _leaky(ctx)
    need_bases(sel(R, [arm]), bases, f'{tag} quantifies over the leaky bases')
    bs, S = _base_arm_stat(R, [arm], set(bases), 'S')
    p = [ctx['pi'][str(b)]['Pi_512'] for b in bs]
    return bs, S, p, spearman(S, p), boot_spearman(S, p, tag=tag)

def P6a(R, ctx):
    bs, S, p, rho, ci = _arm_vs_pi(R, ctx, 'G', 'P6a')
    return {'n_bases': len(bs), 'spearman_S_Pi_G_arm': round(rho, 3),
            'bootstrap95': [round(x, 3) for x in ci], 'threshold': -0.6,
            'verdict': 'HELD' if rho <= -0.6 else 'FAILED'}

def P6b(R, ctx):
    bs, S, p, rho, ci = _arm_vs_pi(R, ctx, 'random', 'P6b')
    return {'n_bases': len(bs), 'spearman_S_Pi_random_arm': round(rho, 3),
            'bootstrap95': [round(x, 3) for x in ci], 'threshold': 0.5,
            'verdict': 'HELD' if rho >= 0.5 else 'FAILED'}

SCORERS = {'P1a': P1a, 'P1b': P1b, 'P2a': P2a, 'P2b': P2b, 'P2c': P2c,
           'P3a': P3a, 'P3b': P3b, 'P3c': P3c, 'P3d': P3d,
           'P4a': P4a, 'P4b': P4b, 'P4c': P4c, 'P4d': P4d,
           'P5a-i': P5a_i, 'P5a-ii': P5a_ii, 'P5a-iii': P5a_iii,
           'P5b': P5b, 'P5c': P5c, 'P5d': P5d, 'P6a': P6a, 'P6b': P6b}

# ---------------------------------------------------------------- descriptive

def descriptive(R, ctx):
    d = {}
    try:
        d['run_width_by_junction'] = {
            a: {k: round(float(np.mean([r['run_census'][k] for r in sel(R, [a])])), 3)
                for k in ('n_runs', 'n_isolated', 'alt', 'inphase', 'mixed')}
            for a in u9.ARMS}
        d['mean_width'] = {a: round(float(np.mean([r['mean_width'] for r in sel(R, [a])])), 3)
                           for a in u9.ARMS}
    except Insufficient: pass
    try:
        d['divergence_step'] = round(float(np.mean(
            [t['stream_divergence'] for r in sel(R, KARMS) for t in r['trials']])), 3)
    except Insufficient: pass
    try:
        d['S_by_arm'] = {a: round(float(np.mean([r['S'] for r in sel(R, [a])])), 3) for a in u9.ARMS}
        d['I_by_arm'] = {a: round(float(np.mean([r['I'] for r in sel(R, [a])])), 3) for a in u9.ARMS}
        d['Q_by_arm'] = {a: round(float(np.mean([r['Q'] for r in sel(R, [a])])), 3) for a in u9.ARMS}
    except Insufficient: pass
    return d

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest() if Path(p).exists() else None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pilot', default=None)
    a = ap.parse_args()
    src = Path(a.pilot) if a.pilot else OUT/'rows.json'
    rows = derive(json.loads(Path(src).read_text())['rows'])
    ctx = {}
    pth = OUT/'pairs.json'
    if not a.pilot and pth.exists(): ctx['pi'] = json.loads(pth.read_text())['pi']
    preds = {}
    for k in u9.frozen_keys():
        fn = SCORERS.get(k)
        if fn is None:
            preds[k] = {'not_evaluated': 'no scorer is registered for this key'}
            continue
        try:
            preds[k] = fn(rows, ctx)
        except Insufficient as e:
            preds[k] = {'not_evaluated': str(e)}
    out = {'protocol': u9.PROTOCOL, 'n_rows': len(rows), 'pilot': bool(a.pilot),
           'frozen_keys': u9.frozen_keys(), 'predictions': preds,
           'descriptive': descriptive(rows, ctx),
           'verdicts': {k: (v.get('verdict') or f"NOT EVALUATED: {v['not_evaluated']}")
                        for k, v in preds.items()}}
    if not a.pilot:
        out['source_hashes'] = {
            'run.py': sha(HERE/'run.py'), 'evaluate.py': sha(HERE/'evaluate.py'),
            'protocol': sha(u9.PROTOCOL_FILE),
            'rows.json': sha(OUT/'rows.json'), 'pairs.json': sha(OUT/'pairs.json'),
            'controls.json': sha(OUT/'controls.json'), 'algebra.json': sha(OUT/'algebra.json'),
            'gadget.json': sha(OUT/'gadget.json')}
        (OUT/'summary.json').write_text(json.dumps(out, indent=1, default=str))
        for k in u9.frozen_keys(): print(f'  {k}: {out["verdicts"][k]}')
    print(json.dumps(out, default=str))

if __name__ == '__main__':
    main()
