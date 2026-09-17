#!/usr/bin/env python3
"""Fiber census: the height-one strip fibers of ECAs 54, 22, 90, 204, 0 at height two.

Frozen protocol: docs/research/protocols/2026-09-17-fiber-census.md (committed
before this implementation). Observables are imported unchanged from the
cross-dimensional unit's strip harness (`strip_spectrum.py` / `run.py`), with
the fixed contract: k = 2 (and a k = 4 subsample), width 521, density 0.5,
burn 512, score 256, six seeds (4 train / 2 test), 64 sites per seed,
disturbance 4 base seeds x 8 origins at horizons 64 and 128.

    python experiments/fiber_census_20260917/run.py --phase k2
    python experiments/fiber_census_20260917/run.py --phase k4
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, sys, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CROSS = ROOT / 'experiments/cross_dimensional_class4_20260917'
spec = importlib.util.spec_from_file_location('crossdim_base', CROSS / 'run.py')
base = importlib.util.module_from_spec(spec); sys.modules['crossdim_base'] = base; spec.loader.exec_module(base)
spec2 = importlib.util.spec_from_file_location('strip', CROSS / 'strip_spectrum.py')
strip = importlib.util.module_from_spec(spec2); sys.modules['strip'] = strip; spec2.loader.exec_module(strip)

PROTOCOL = 'fiber-census-20260917'
BASES = [54, 22, 90, 204, 0]
SAMPLE = 512
K4_SUBSAMPLE = 64
DENSITY = 0.5
EXEMPLARS = {'highlife': ((3, 6), (2, 3)), 'life': ((3,), (2, 3)), 'b35s236': ((3, 5), (2, 3, 6))}

def seed(*parts):
    h = hashlib.sha256('|'.join(map(str, (PROTOCOL,) + parts)).encode()).digest()
    return int.from_bytes(h[:8], 'little') & 0x7fff_ffff_ffff_ffff

def mask_to_rule(mask):
    births = tuple(n for n in range(9) if (mask >> n) & 1)
    survives = tuple(n for n in range(9) if (mask >> (9 + n)) & 1)
    return births, survives

def rule_to_mask(births, survives):
    return sum(1 << n for n in births) + sum(1 << (9 + n) for n in survives)

def height1_eca(mask):
    b = lambda n: (mask >> n) & 1
    s = lambda n: (mask >> (9 + n)) & 1
    return b(0) + 18 * b(3) + 32 * b(6) + 4 * s(2) + 72 * s(5) + 128 * s(8)

def fiber(base_rule):
    return [m for m in range(1 << 18) if height1_eca(m) == base_rule]

def rulestring(births, survives):
    return 'B' + ''.join(map(str, births)) + '/S' + ''.join(map(str, survives))

def sample_fiber(base_rule):
    fib = fiber(base_rule)
    assert len(fib) == 4096, (base_rule, len(fib))
    rng = np.random.default_rng(seed('sample', base_rule))
    chosen = [int(x) for x in rng.choice(fib, size=SAMPLE, replace=False)]
    flagged = {}
    for name, (bb, ss) in EXEMPLARS.items():
        m = rule_to_mask(bb, ss)
        if m in fib:
            flagged[m] = name
            if m not in chosen: chosen.append(m)
    return chosen, flagged

def exactness_control(base_rule, masks):
    """Height-one trajectories of eight fiber members must equal the base ECA's."""
    rng = np.random.default_rng(seed('exact', base_rule))
    row = rng.integers(0, 2, size=strip.WIDTH, dtype=np.uint8)
    ok = True
    for m in masks[:8]:
        bb, ss = mask_to_rule(m)
        lr = base.LifeRule(f'm{m}', bb, ss, 'fiber')
        st = row[None, :].copy(); e = row.copy()
        for _ in range(256):
            if not np.array_equal(st[0], e): ok = False; break
            st = base.life_step(st, lr); e = base.eca_step(e, base_rule)
        if not ok: break
    return ok

def evaluate(mask, k):
    bb, ss = mask_to_rule(mask)
    lr = base.LifeRule(f'm{mask}', bb, ss, 'fiber')
    # identical machinery to strip_spectrum.evaluate, with this protocol's seed namespace
    t = time.time()
    events = sample_events(lr, k)
    p, nref, refmode = strip.reference_strip(lr, k)
    r, mu, sd, missing = base.selective_r(events, p)
    if missing and k >= 4:
        n = 200_000
        while missing and n <= 800_000:
            p, nref, refmode = strip.reference_strip(lr, k, n, n)
            r, mu, sd, missing = base.selective_r(events, p); n *= 2
    m, bll, hll, ntr, nte = base.predictive_gain(events[:4], events[4:6])
    sp = spread(lr, k)
    import math
    return {'mask': mask, 'rulestring': rulestring(bb, ss), 'height': k, 'density': DENSITY,
            'R_star': r, 'M_star': m, 'S_star': max(0, r) * max(0, m) if math.isfinite(r) else None,
            'reference_mode': refmode, 'reference_samples': nref, 'unsupported_symbols': missing,
            'baseline_logloss_bits': bll, 'history_logloss_bits': hll, 'train_events': ntr, 'test_events': nte,
            **sp, 'wall_seconds': time.time() - t}

def sample_events(rule, k):
    events = []; total = k * strip.WIDTH
    for rep in range(strip.EVENT_SEEDS):
        rng = np.random.default_rng(seed('events', rule.name, k, DENSITY, rep))
        st = (rng.random((k, strip.WIDTH)) < DENSITY).astype(np.uint8)
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

def spread(rule, k):
    import math
    x1 = []; x2 = []; extinct = 0; total = k * strip.WIDTH
    for rep in range(strip.SPREAD_SEEDS):
        rng = np.random.default_rng(seed('spread', rule.name, k, DENSITY, rep))
        st = (rng.random((k, strip.WIDTH)) < DENSITY).astype(np.uint8)
        for _ in range(strip.BURN): st = base.life_step(st, rule)
        for flat in rng.choice(total, size=strip.ORIGINS, replace=False):
            oy, ox = divmod(int(flat), strip.WIDTH); a = st.copy(); b = st.copy(); b[oy, ox] ^= 1
            aa = bb = None
            for t in range(1, strip.T2 + 1):
                a = base.life_step(a, rule); b = base.life_step(b, rule)
                if t == strip.T1: aa = strip.xdiam(a ^ b, ox)
                if t == strip.T2: bb = strip.xdiam(a ^ b, ox)
            x1.append(aa); x2.append(bb); extinct += int(bb == 0)
    ma = float(np.mean(x1)); mb = float(np.mean(x2))
    alpha = 0.0 if (ma == 0 and mb == 0) else (float(math.log2(mb / ma)) if ma > 0 and mb > 0 else None)
    return {'Dx64': ma, 'Dx128': mb, 'alpha_x': alpha, 'extinction_fraction': extinct / len(x2), 'spread_trials': len(x2)}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--phase', choices=['k2', 'k4'], default='k2')
    ap.add_argument('--output-dir', default='results/fiber_census_20260917')
    ap.add_argument('--limit', type=int, default=None, help='debug only; never for the canonical run')
    args = ap.parse_args()
    out = ROOT / args.output_dir; out.mkdir(parents=True, exist_ok=True)
    k = 2 if args.phase == 'k2' else 4
    samples = {}; exact = {}
    for b in BASES:
        chosen, flagged = sample_fiber(b)
        if args.phase == 'k4': chosen = chosen[:K4_SUBSAMPLE] + [m for m in flagged if m not in chosen[:K4_SUBSAMPLE]]
        if args.limit: chosen = chosen[:args.limit]
        samples[b] = (chosen, flagged)
        exact[b] = exactness_control(b, chosen)
        if not exact[b]: raise SystemExit(f'exactness control failed for base {b}')
    (out / f'exactness_control_{args.phase}.json').write_text(json.dumps({'protocol': PROTOCOL, 'height1_identity': exact}, indent=2) + '\n')
    rows = []; t0 = time.time()
    for b in BASES:
        chosen, flagged = samples[b]
        for i, m in enumerate(chosen):
            r = evaluate(m, k); r['base'] = b; r['exemplar'] = flagged.get(m); rows.append(r)
            if i % 32 == 0:
                print(f'base {b} {i+1}/{len(chosen)} {r["rulestring"]:14s} S*={r["S_star"]:.4g} ax={r["alpha_x"]} {time.time()-t0:.0f}s', flush=True)
    payload = {'protocol': PROTOCOL, 'phase': args.phase, 'height': k, 'density': DENSITY, 'sample_per_fiber': SAMPLE if k == 2 else K4_SUBSAMPLE,
               'bases': BASES, 'exemplars_flagged': {str(b): {str(m): n for m, n in samples[b][1].items()} for b in BASES},
               'rows': rows, 'wall_seconds': time.time() - t0}
    (out / f'fiber_census_{args.phase}.json').write_text(json.dumps(payload, indent=1, sort_keys=True, allow_nan=False) + '\n')
    print(out / f'fiber_census_{args.phase}.json')

if __name__ == '__main__':
    main()
