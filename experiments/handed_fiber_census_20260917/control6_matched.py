#!/usr/bin/env python3
"""Control 6, implemented in full: matched complement pairs.

The protocol deduces that fiber(110) and fiber(137) carry identical phenotype
distributions, because complement conjugation maps one onto the other and every
observable is complement-covariant. The census's calibration test rejected that
null on the both-positive fraction (p = 0.027), which the protocol says flags
the implementation or the seeds rather than science, and makes P3 unscorable
until resolved. The run's control 6 only checked that conjugates land in
fiber(137); it never compared observables, so it could not have caught a real
covariance break. This script supplies the missing comparison.

Two parts:

A. Dynamical covariance, exact. For sampled fiber(110) tables R with conjugate
   C, check handed_step(NOT S, C) == NOT handed_step(S, R) on random states at
   several strip heights. If this holds, conjugation is implemented as the
   mathematical conjugate and the observer's z -> 17 - z relabeling carries the
   rest.

B. Matched-seed observables. Evaluate R normally, then evaluate C driven by the
   same seed stream with every initial state complemented, and compare R*, M*
   and alpha_x. Independent seeding is what the census used; this pairing is
   what the deduction actually predicts.

    python experiments/handed_fiber_census_20260917/control6_matched.py
"""
from __future__ import annotations
import importlib.util, json, math, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('hf', HERE / 'run.py')
hf = importlib.util.module_from_spec(spec); sys.modules['hf'] = hf; spec.loader.exec_module(hf)
base, strip, fc1 = hf.base, hf.strip, hf.fc1

def conj(t):
    out = 0
    for c in (0, 1):
        for w in (0, 1):
            for n7 in range(8):
                if not ((t >> (16 * c + 8 * w + n7)) & 1):
                    out |= 1 << (16 * (1 - c) + 8 * (1 - w) + (7 - n7))
    return out

def part_a(tables):
    rng = np.random.default_rng(12345)
    rows = []
    for t in tables:
        c = conj(t); ok = True
        for h in (1, 2, 3, 5):
            S = rng.integers(0, 2, (h, 61), dtype=np.uint8)
            lhs = hf.handed_step(1 - S, hf.HandedRule('c', c))
            rhs = 1 - hf.handed_step(S, hf.HandedRule('r', t))
            if not np.array_equal(lhs, rhs): ok = False; break
        rows.append({'table': t, 'conjugate': c, 'step_covariance_exact': ok})
    return rows

def sample_events_matched(rule, k, seed_name, flip):
    """fc1.sample_events with the seed stream pinned to seed_name and an optional
    complement of the initial state; everything else identical."""
    events = []; total = k * strip.WIDTH
    for rep in range(strip.EVENT_SEEDS):
        rng = np.random.default_rng(hf.seed('events', seed_name, k, hf.DENSITY, rep))
        st = (rng.random((k, strip.WIDTH)) < hf.DENSITY).astype(np.uint8)
        if flip: st = (1 - st).astype(np.uint8)
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

def spread_matched(rule, k, seed_name, flip):
    x1 = []; x2 = []; total = k * strip.WIDTH
    for rep in range(strip.SPREAD_SEEDS):
        rng = np.random.default_rng(hf.seed('spread', seed_name, k, hf.DENSITY, rep))
        st = (rng.random((k, strip.WIDTH)) < hf.DENSITY).astype(np.uint8)
        if flip: st = (1 - st).astype(np.uint8)
        for _ in range(strip.BURN): st = base.life_step(st, rule)
        for flat in rng.choice(total, size=strip.ORIGINS, replace=False):
            oy, ox = divmod(int(flat), strip.WIDTH)
            a = st.copy(); b = st.copy(); b[oy, ox] ^= 1
            aa = bb = None
            for tt in range(1, strip.T2 + 1):
                a = base.life_step(a, rule); b = base.life_step(b, rule)
                if tt == strip.T1: aa = strip.xdiam(a ^ b, ox)
                if tt == strip.T2: bb = strip.xdiam(a ^ b, ox)
            x1.append(aa); x2.append(bb)
    ma = float(np.mean(x1)); mb = float(np.mean(x2))
    alpha = 0.0 if (ma == 0 and mb == 0) else (float(math.log2(mb / ma)) if ma > 0 and mb > 0 else None)
    return {'Dx64': ma, 'Dx128': mb, 'alpha_x': alpha}

def observables(table, seed_name, flip, k=2):
    r = hf.HandedRule(f'h{table}', table)
    ev = sample_events_matched(r, k, seed_name, flip)
    p, _, _ = strip.reference_strip(r, k)
    R, _, _, _ = base.selective_r(ev, p)
    M, _, _, _, _ = base.predictive_gain(ev[:4], ev[4:6])
    sp = spread_matched(r, k, seed_name, flip)
    return {'R_star': R, 'M_star': M, 'alpha_x': sp['alpha_x'],
            'S_star': max(0, R) * max(0, M) if math.isfinite(R) else None}

def main():
    tables = hf.sample_fiber(110, 8)
    a = part_a(tables)
    print('A. step covariance exact for all 8:', all(r['step_covariance_exact'] for r in a))
    rows = []
    for t in tables:
        c = conj(t)
        o1 = observables(t, f'h{t}', False)
        o2 = observables(c, f'h{t}', True)          # same seeds, complemented start
        d = {k: (None if o1[k] is None or o2[k] is None else abs(o1[k] - o2[k]))
             for k in ('R_star', 'M_star', 'alpha_x', 'S_star')}
        rows.append({'table': t, 'conjugate': c, 'base': hf.res1(t), 'conjugate_base': hf.res1(c),
                     'original': o1, 'matched_conjugate': o2, 'abs_diff': d,
                     'identical_to_1e-9': all(v is not None and v < 1e-9 for v in d.values())})
        print(f'  {t} S*={o1["S_star"]:.6f} vs {o2["S_star"]:.6f}  '
              f'alpha={o1["alpha_x"]:.6f} vs {o2["alpha_x"]:.6f}  max|d|={max(v for v in d.values() if v is not None):.2e}')
    out = {'part_a_step_covariance': a, 'part_b_matched_observables': rows,
           'all_matched_identical': all(r['identical_to_1e-9'] for r in rows)}
    (ROOT / 'results/handed_fiber_census_20260917/control6_matched.json').write_text(
        json.dumps(out, indent=1, sort_keys=True, allow_nan=False) + '\n')
    print('B. all matched pairs identical to 1e-9:', out['all_matched_identical'])

if __name__ == '__main__':
    main()
