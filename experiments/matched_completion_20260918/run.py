#!/usr/bin/env python3
"""Matched completions: decompose persistence into what the base sets and what the completion sets.

Frozen protocol: docs/research/protocols/2026-09-18-matched-completion-persistence.md
(committed before this implementation).

Because the height-one restriction of the handed family is a coordinate
projection, a 24-bit completion u is one object shared by every fiber:
embed(r, u) exists for every base r. Holding u fixed and varying r, with every
rule driven from the same seed stream, turns "what does the base confer" into a
variance decomposition and a transfer correlation.

Seeds are keyed on (stream, completion, k, density, rep) and NEVER on the rule
table or the base, so all eight bases see the same initial states, sites and
disturbance origins for a completion. The previous unit's lesson: a null-pair
control that keys the conjugate on its own identity is an independently seeded
comparison and rejects at the nominal rate by construction; the seed key is
therefore an explicit argument here, and the matched control passes the
ORIGINAL completion's key to the conjugate.

    python experiments/matched_completion_20260918/run.py --workers 4
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, math, sys, time
from multiprocessing import Pool
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('hf', ROOT / 'experiments/handed_fiber_census_20260917/run.py')
hf = importlib.util.module_from_spec(spec); sys.modules['hf'] = hf; spec.loader.exec_module(hf)
base, strip, fc1 = hf.base, hf.strip, hf.fc1
HandedRule, handed_step, embed, res1 = hf.HandedRule, hf.handed_step, hf.embed, hf.res1

PROTOCOL = 'matched-completion-20260918'
OUT = ROOT / 'results/matched_completion_20260918'
BASES = [110, 54, 22, 5, 30, 90, 0, 204]
N_COMPLETIONS = 512
N_REPLICATE = 64
N_K4 = 128
DENSITY = 0.5
COND_P = ROOT / 'experiments/class4_selective_persistence_20260916/evidence/class4_selective_persistence_all_conditions_20260916.RECOVERED.csv'
EXPECTED_1D = {110: (0.252, 0.903, 0.227, 0.766), 54: (0.343, 0.601, 0.206, 1.038),
               22: (-0.143, 0.137, 0.000, 1.000), 5: (0.485, 0.976, 0.474, 0.000),
               30: (-0.001, -0.000, 0.000, 1.000), 90: (0.000, -0.000, 0.000, 0.999),
               0: (0.000, 0.000, 0.000, 0.000), 204: (0.000, 0.000, 0.000, 0.000)}

def seed(*parts):
    h = hashlib.sha256('|'.join(map(str, (PROTOCOL,) + parts)).encode()).digest()
    return int.from_bytes(h[:8], 'little') & 0x7fff_ffff_ffff_ffff

def completions():
    rng = np.random.default_rng(seed('completions'))
    seen = set(); out = []
    while len(out) < N_COMPLETIONS:
        u = int(rng.integers(0, 1 << 24))
        if u not in seen: seen.add(u); out.append(u)
    return out

def bits_of(u):
    return [(u >> j) & 1 for j in range(24)]

# ---------------------------------------------------------- measurement

def _initial(k, key, rep, kind, flip):
    rng = np.random.default_rng(seed(kind, *key, k, DENSITY, rep))
    st = (rng.random((k, strip.WIDTH)) < DENSITY).astype(np.uint8)
    if flip: st = (1 - st).astype(np.uint8)
    return rng, st

def sample_events_keyed(rule, k, key, flip=False):
    """fc1.sample_events with the seed stream keyed on `key`, not the rule."""
    events = []; total = k * strip.WIDTH
    for rep in range(strip.EVENT_SEEDS):
        rng, st = _initial(k, key, rep, 'events', flip)
        for _ in range(strip.BURN): st = base.life_step(st, rule)
        flat = np.sort(rng.choice(total, size=min(strip.SITES, total), replace=False))
        ys, xs = flat // strip.WIDTH, flat % strip.WIDTH
        hist = np.zeros(len(flat), dtype=np.uint8)
        for _ in range(7):
            hist = ((hist << 1) | st[ys, xs]) & 0xff
            st = base.life_step(st, rule)
        cc = []; hh = []; yy = []; zz = []
        for _ in range(strip.SCORE):
            cur = st[ys, xs].copy(); hist = ((hist << 1) | cur) & 0xff
            sym = base.life_symbols(st, ys, xs); nxt = base.life_step(st, rule)
            cc.append(cur); hh.append(hist.copy()); yy.append(nxt[ys, xs].copy()); zz.append(sym)
            st = nxt
        events.append({'current': np.concatenate(cc), 'history': np.concatenate(hh),
                       'target': np.concatenate(yy), 'symbol': np.concatenate(zz)})
    return events

def spread_keyed(rule, k, key, flip=False):
    x1 = []; x2 = []; extinct = 0; total = k * strip.WIDTH
    for rep in range(strip.SPREAD_SEEDS):
        rng, st = _initial(k, key, rep, 'spread', flip)
        for _ in range(strip.BURN): st = base.life_step(st, rule)
        for flat in rng.choice(total, size=strip.ORIGINS, replace=False):
            oy, ox = divmod(int(flat), strip.WIDTH)
            a = st.copy(); b = st.copy(); b[oy, ox] ^= 1
            aa = bb = None
            for t in range(1, strip.T2 + 1):
                a = base.life_step(a, rule); b = base.life_step(b, rule)
                if t == strip.T1: aa = strip.xdiam(a ^ b, ox)
                if t == strip.T2: bb = strip.xdiam(a ^ b, ox)
            x1.append(aa); x2.append(bb); extinct += int(bb == 0)
    ma = float(np.mean(x1)); mb = float(np.mean(x2))
    alpha = 0.0 if (ma == 0 and mb == 0) else (float(math.log2(mb / ma)) if ma > 0 and mb > 0 else None)
    return {'Dx64': ma, 'Dx128': mb, 'alpha_x': alpha,
            'extinction_fraction': extinct / len(x2), 'spread_trials': len(x2)}

def reference_for(rule, k, u):
    """Exact at k<=3; Monte Carlo keyed on the completion at k>=4, escalated by caller."""
    if k <= 3:
        return strip.reference_strip(rule, k)
    return None

def evaluate(table, k, key, u, flip=False):
    rule = HandedRule(f'h{table}', table)
    t0 = time.time()
    events = sample_events_keyed(rule, k, key, flip)
    if k <= 3:
        p, nref, refmode = strip.reference_strip(rule, k)
        R, mu, sd, missing = base.selective_r(events, p)
    else:
        n = 100_000; missing = True; p = nref = refmode = None
        while True:
            rng_key = seed('reference', u, k, n)
            saved = strip.seed
            strip.seed = lambda *a, _k=rng_key: _k          # key the MC reference on the completion
            try:
                p, nref, refmode = strip.reference_strip(rule, k, n, n)
            finally:
                strip.seed = saved
            R, mu, sd, missing = base.selective_r(events, p)
            if not missing or n >= 800_000: break
            n *= 2
    M, bll, hll, ntr, nte = base.predictive_gain(events[:4], events[4:6])
    sp = spread_keyed(rule, k, key, flip)
    return {'table': table, 'height': k, 'R_star': R, 'M_star': M,
            'S_star': max(0, R) * max(0, M) if math.isfinite(R) else None,
            'reference_mode': refmode, 'reference_samples': nref,
            'unsupported_symbols': missing, 'baseline_logloss_bits': bll,
            'history_logloss_bits': hll, **sp, 'wall_seconds': time.time() - t0}

# ------------------------------------------------------------- controls

def conj_table(t):
    out = 0
    for c in (0, 1):
        for w in (0, 1):
            for n7 in range(8):
                if not ((t >> (16 * c + 8 * w + n7)) & 1):
                    out |= 1 << (16 * (1 - c) + 8 * (1 - w) + (7 - n7))
    return out

def controls(us):
    c = {}
    c['exposed_indices'] = {'indices': hf.EXPOSED, 'distinct': len(set(hf.EXPOSED)) == 8}
    reach = set()
    for v in range(1 << 6):
        g = np.array([[(v >> (3 * r + j)) & 1 for j in range(3)] for r in range(2)], dtype=np.uint8)
        tot = np.zeros_like(g, dtype=np.uint8)
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0: continue
                tot += np.roll(np.roll(g, dy, axis=0), dx, axis=1)
        w = np.roll(g, 1, axis=1)
        for r in range(2): reach.add((int(g[r, 1]), int(w[r, 1]), int(tot[r, 1] - w[r, 1])))
    c['height2_conditions'] = {'reached': len(reach), 'ok': len(reach) == 32}
    # step covariance at heights 1,2,3,5
    rng = np.random.default_rng(seed('covariance')); ok = True
    for u in us[:8]:
        t = embed(110, bits_of(u)); ct = conj_table(t)
        for h in (1, 2, 3, 5):
            S = rng.integers(0, 2, (h, 61), dtype=np.uint8)
            if not np.array_equal(handed_step(1 - S, HandedRule('c', ct)),
                                  1 - handed_step(S, HandedRule('r', t))): ok = False
    c['step_covariance_exact'] = ok
    # height-one trajectory identity, 8 completions per base
    rowrng = np.random.default_rng(seed('exact'))
    row = rowrng.integers(0, 2, strip.WIDTH, dtype=np.uint8)
    bad = []
    for b in BASES:
        for u in us[:8]:
            t = embed(b, bits_of(u))
            if res1(t) != b: bad.append((b, u, 'res1')); continue
            st = row[None, :].copy(); e = row.copy()
            for _ in range(256):
                st = handed_step(st, HandedRule(f'h{t}', t)); e = hf.eca_step(e, b)
                if not np.array_equal(st[0], e): bad.append((b, u, 'traj')); break
    c['height1_identity'] = {'ok': not bad, 'failures': bad[:5]}
    return c

def matched_null_pairs(us):
    """The matched control: the conjugate is driven by the ORIGINAL completion's key."""
    rows = []
    for u in us[:16]:
        t = embed(110, bits_of(u)); ct = conj_table(t)
        assert res1(ct) == 137, (u, res1(ct))
        o1 = evaluate(t, 2, ('A', u), u, flip=False)
        o2 = evaluate(ct, 2, ('A', u), u, flip=True)
        d = {k: (None if o1[k] is None or o2[k] is None else abs(o1[k] - o2[k]))
             for k in ('R_star', 'M_star', 'alpha_x', 'S_star')}
        rows.append({'completion': u, 'table': t, 'conjugate': ct,
                     'max_abs_diff': max((v for v in d.values() if v is not None), default=None),
                     'abs_diff': d, 'identical_to_1e-9': all(v is not None and v < 1e-9 for v in d.values())})
    return rows

# ----------------------------------------------------------------- run

def job(spec):
    stream, k, idxs, us = spec
    rows = []
    for i in idxs:
        u = us[i]; ub = bits_of(u)
        for b in BASES:
            r = evaluate(embed(b, ub), k, (stream, u), u)
            r.update({'base': b, 'completion': u, 'completion_index': i, 'stream': stream})
            rows.append(r)
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--workers', type=int, default=4)
    ap.add_argument('--timing', action='store_true')
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    us = completions()
    assert len(set(us)) == N_COMPLETIONS

    import pandas as pd
    cp = pd.read_csv(COND_P); cp = cp[(cp.condition == 'P') & (cp.radius == 1)]
    vals = {int(r): (float(R), float(M), float(S), float(a))
            for r, R, M, S, a in zip(cp.rule, cp.R, cp.M, cp.S, cp.alpha)}
    for b, exp in EXPECTED_1D.items():
        got = vals[b]
        assert all(abs(g - e) < 5e-4 for g, e in zip(got, exp)), (b, got, exp)
    print('condition-P 1D values asserted for all eight bases')

    if args.timing:
        t0 = time.time(); r = evaluate(embed(110, bits_of(us[0])), 2, ('A', us[0]), us[0])
        print(f'one rule k=2 {time.time()-t0:.2f}s S*={r["S_star"]} M*={r["M_star"]:.3f}')
        t0 = time.time(); r4 = evaluate(embed(110, bits_of(us[0])), 4, ('A', us[0]), us[0])
        print(f'one rule k=4 {time.time()-t0:.2f}s S*={r4["S_star"]} mode={r4["reference_mode"]}')
        return

    ctrl = controls(us)
    print(json.dumps({k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items() if kk != 'indices'})
                      for k, v in ctrl.items()}, indent=1))
    if not (ctrl['exposed_indices']['distinct'] and ctrl['height2_conditions']['ok']
            and ctrl['step_covariance_exact'] and ctrl['height1_identity']['ok']):
        raise SystemExit('controls failed')

    t0 = time.time()
    chunks = lambda n, size: [list(range(i, min(i + size, n))) for i in range(0, n, size)]
    specs = ([('A', 2, c, us) for c in chunks(N_COMPLETIONS, 16)]
             + [('B', 2, c, us) for c in chunks(N_REPLICATE, 16)]
             + [('A', 4, c, us) for c in chunks(N_K4, 8)])
    with Pool(args.workers) as pool:
        out = []
        for i, rows in enumerate(pool.imap_unordered(job, specs, chunksize=1)):
            out += rows
            print(f'chunk {i+1}/{len(specs)} rows={len(out)} {time.time()-t0:.0f}s', flush=True)
    print('matched null pairs...', flush=True)
    nulls = matched_null_pairs(us)
    (OUT / 'controls.json').write_text(json.dumps(
        {'protocol': PROTOCOL, 'controls': ctrl, 'matched_null_pairs': nulls,
         'all_matched_identical': all(r['identical_to_1e-9'] for r in nulls),
         'condition_p_1d': {str(b): vals[b] for b in BASES}}, indent=1, allow_nan=False) + '\n')
    (OUT / 'rows.json').write_text(json.dumps(
        {'protocol': PROTOCOL, 'bases': BASES, 'n_completions': N_COMPLETIONS,
         'n_replicate': N_REPLICATE, 'n_k4': N_K4, 'density': DENSITY,
         'completions': us, 'rows': out, 'wall_seconds': time.time() - t0},
        indent=1, sort_keys=True, allow_nan=False) + '\n')
    print(OUT / 'rows.json', f'{time.time()-t0:.0f}s  rows={len(out)}')

if __name__ == '__main__':
    main()
