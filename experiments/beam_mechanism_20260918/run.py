#!/usr/bin/env python3
"""The invariant beam mediates history-gain transfer between bases.

Frozen protocol: docs/research/protocols/2026-09-18-beam-mechanism.md
(committed before this implementation).

The beam theorem. On a height-two strip the vertical wrap sends both off-rows
onto the other row, so a state with equal rows has Moore count 3L + 2C + 3R and
west neighbour L; hence n7 = 2L + 2C + 3R and the condition index is
16C + 8L + (2L + 2C + 3R), exactly the height-one exposed index for (L, C, R).
Every cell of such a state reads an exposed entry, which no completion can
touch, so the strip acts as the base ECA and equal rows stay equal. The
equal-row set is therefore exactly invariant under every rule of the handed
family, and on it the strip IS the base rule.

That makes history gain a mixture: the base's own 1D value on the beam, a
completion-set value off it. Beam proximity is the shared mediator, and bases
respond to it with opposite signs, which is the anticorrelation.

Every seed is keyed on (stream, completion, ...) and never on the rule table or
the base, so the matched null-pair control is a paired comparison.

    python experiments/beam_mechanism_20260918/run.py --workers 4
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, math, sys, time
from multiprocessing import Pool
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('mc', ROOT / 'experiments/matched_completion_20260918/run.py')
mc = importlib.util.module_from_spec(spec); sys.modules['mc'] = mc; spec.loader.exec_module(mc)
hf, base, strip, fc1 = mc.hf, mc.base, mc.strip, mc.fc1
HandedRule, handed_step, embed, res1 = hf.HandedRule, hf.handed_step, hf.embed, hf.res1

PROTOCOL = 'beam-mechanism-20260918'
OUT = ROOT / 'results/beam_mechanism_20260918'
ORIGINAL = [110, 54, 22, 5, 30, 90, 0, 204]
NEW = [106, 232, 8, 18, 46, 33, 62, 29]
BASES = ORIGINAL + NEW
N_COMPLETIONS = 256
N_H3 = 48
DENSITY = 0.5
COND_P = mc.COND_P
EXPECTED_1D = dict(mc.EXPECTED_1D)
EXPECTED_1D.update({106: (-0.000, -0.000, 0.000, 0.989), 232: (-0.314, 0.000, 0.000, 0.000),
                    8: (-0.585, 0.000, 0.000, 0.000), 18: (-0.027, 0.164, 0.000, 1.002),
                    46: (-0.240, 0.374, 0.000, 0.000), 33: (0.083, 0.563, 0.047, 0.000),
                    62: (0.775, 0.765, 0.593, 0.396), 29: (0.100, 0.954, 0.095, 0.000)})

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

def eca_step(row, rule):
    idx = (np.roll(row, 1) << 2) | (row << 1) | np.roll(row, -1)
    return np.array([(rule >> i) & 1 for i in range(8)], dtype=np.uint8)[idx]

def rows_agree(st):
    """Fraction of columns whose rows are all equal."""
    return float(np.all(st == st[0], axis=0).mean())

# --------------------------------------------------- events with proximity

def sample_events_agree(rule, k, key, flip=False):
    """mc.sample_events_keyed, additionally accumulating beam proximity on the
    same trajectory that yields M*."""
    events = []; total = k * strip.WIDTH; ag = []
    for rep in range(strip.EVENT_SEEDS):
        rng, st = mc._initial(k, key, rep, 'events', flip)
        for _ in range(strip.BURN): st = base.life_step(st, rule)
        flat = np.sort(rng.choice(total, size=min(strip.SITES, total), replace=False))
        ys, xs = flat // strip.WIDTH, flat % strip.WIDTH
        hist = np.zeros(len(flat), dtype=np.uint8)
        for _ in range(7):
            ag.append(rows_agree(st))
            hist = ((hist << 1) | st[ys, xs]) & 0xff
            st = base.life_step(st, rule)
        cc = []; hh = []; yy = []; zz = []
        for _ in range(strip.SCORE):
            ag.append(rows_agree(st))
            cur = st[ys, xs].copy(); hist = ((hist << 1) | cur) & 0xff
            sym = base.life_symbols(st, ys, xs); nxt = base.life_step(st, rule)
            cc.append(cur); hh.append(hist.copy()); yy.append(nxt[ys, xs].copy()); zz.append(sym)
            st = nxt
        events.append({'current': np.concatenate(cc), 'history': np.concatenate(hh),
                       'target': np.concatenate(yy), 'symbol': np.concatenate(zz)})
    return events, float(np.mean(ag))

def evaluate(table, k, key, u, flip=False):
    rule = HandedRule(f'h{table}', table)
    t0 = time.time()
    events, agree = sample_events_agree(rule, k, key, flip)
    p, nref, refmode = strip.reference_strip(rule, k)      # exact for k <= 3
    R, mu, sd, missing = base.selective_r(events, p)
    M, bll, hll, ntr, nte = base.predictive_gain(events[:4], events[4:6])
    sp = mc.spread_keyed(rule, k, key, flip)
    return {'table': table, 'height': k, 'R_star': R, 'M_star': M,
            'S_star': max(0, R) * max(0, M) if math.isfinite(R) else None,
            'agree': agree, 'on_beam': int(agree > 0.98), 'off_beam': int(agree < 0.5),
            'reference_mode': refmode, 'unsupported_symbols': len(missing) if isinstance(missing, list) else int(bool(missing)),
            **sp, 'wall_seconds': time.time() - t0}

# ------------------------------------------------- transverse beam stability

def transverse(table, base_rule, u, complement=False):
    """Defect on the beam: flip one cell of row 1 and follow the strip."""
    r = HandedRule(f'h{table}', table)
    d64 = []; d128 = []
    for rep in range(4):
        rng = np.random.default_rng(seed('transverse', u, rep))
        x = (rng.random(strip.WIDTH) < 0.5).astype(np.uint8)
        # The conjugate beam state must be F_137^256(NOT x) = NOT F_110^256(x), so the
        # complement is applied to the seed row BEFORE the burn, not after it. Applying
        # it after gives NOT F_137^256(x), which is a different state, and the control
        # then compares unmatched beam states.
        if complement: x = (1 - x).astype(np.uint8)
        for _ in range(256): x = eca_step(x, base_rule)
        for o in rng.choice(strip.WIDTH, size=8, replace=False):
            st = np.vstack([x, x.copy()]); st[1, int(o)] ^= 1
            for t in range(1, 129):
                st = handed_step(st, r)
                if t == 64: d64.append(int((st[0] != st[1]).sum()))
            d128.append(int((st[0] != st[1]).sum()))
    return {'T64': float(np.mean(d64)), 'T128': float(np.mean(d128)),
            'T_ext': float(np.mean([d == 0 for d in d128]))}

# ------------------------------------------------------------------ controls

def controls(us):
    c = {'exposed_indices_distinct': len(set(hf.EXPOSED)) == 8}
    for k in (2, 3):
        reach = set()
        for v in range(1 << (3 * k)):
            g = np.array([[(v >> (3 * r + j)) & 1 for j in range(3)] for r in range(k)], dtype=np.uint8)
            tot = np.zeros_like(g, dtype=np.uint8)
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx == 0 and dy == 0: continue
                    tot += np.roll(np.roll(g, dy, axis=0), dx, axis=1)
            w = np.roll(g, 1, axis=1)
            for r in range(k): reach.add((int(g[r, 1]), int(w[r, 1]), int(tot[r, 1] - w[r, 1])))
        c[f'height{k}_conditions'] = {'reached': len(reach), 'ok': len(reach) == 32}
    # beam invariance, exact, at heights 2 and 3
    rng = np.random.default_rng(seed('beam'))
    bad = []
    for b in BASES:
        for u in us[:8]:
            t = embed(b, mc.bits_of(u)); r = HandedRule(f'h{t}', t)
            for h in (2, 3):
                x = rng.integers(0, 2, 121, dtype=np.uint8)
                st = np.vstack([x] * h); e = x.copy()
                for _ in range(256):
                    st = handed_step(st, r); e = eca_step(e, b)
                    if not np.all(st == st[0]) or not np.array_equal(st[0], e):
                        bad.append((b, u, h)); break
    c['beam_invariance'] = {'ok': not bad, 'failures': bad[:5]}
    old = set(json.loads((ROOT / 'results/matched_completion_20260918/rows.json').read_text())['completions'])
    c['completions_disjoint'] = {'ok': not (old & set(us)), 'overlap': len(old & set(us))}
    covar = True
    for u in us[:8]:
        t = embed(110, mc.bits_of(u)); ct = mc.conj_table(t)
        for h in (1, 2, 3, 5):
            S = rng.integers(0, 2, (h, 61), dtype=np.uint8)
            if not np.array_equal(handed_step(1 - S, HandedRule('c', ct)),
                                  1 - handed_step(S, HandedRule('r', t))): covar = False
    c['step_covariance_exact'] = covar
    return c

def matched_null_pairs(us):
    rows = []
    for u in us[:8]:
        t = embed(110, mc.bits_of(u)); ct = mc.conj_table(t)
        assert res1(ct) == 137
        o1 = evaluate(t, 2, ('A', u), u, flip=False); o1.update(transverse(t, 110, u))
        o2 = evaluate(ct, 2, ('A', u), u, flip=True); o2.update(transverse(ct, 137, u, complement=True))
        keys = ('R_star', 'M_star', 'alpha_x', 'agree', 'T64', 'T128', 'T_ext')
        d = {k: (None if o1[k] is None or o2[k] is None else abs(o1[k] - o2[k])) for k in keys}
        rows.append({'completion': u, 'abs_diff': d,
                     'max_abs_diff': max((v for v in d.values() if v is not None), default=None),
                     'identical_to_1e-9': all(v is not None and v < 1e-9 for v in d.values())})
    return rows

# ----------------------------------------------------------------------- run

def job(spec):
    kind, idxs, us = spec
    rows = []
    for i in idxs:
        u = us[i]; ub = mc.bits_of(u)
        if kind == 'main':
            for b in BASES:
                t = embed(b, ub)
                r = evaluate(t, 2, ('A', u), u)
                r.update(transverse(t, b, u))
                r.update({'base': b, 'completion': u, 'completion_index': i, 'tier': 'main'})
                rows.append(r)
        else:
            for b in ORIGINAL:
                t = embed(b, ub)
                r = evaluate(t, 3, ('A', u), u)
                r.update({'base': b, 'completion': u, 'completion_index': i, 'tier': 'h3'})
                rows.append(r)
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--workers', type=int, default=4)
    ap.add_argument('--timing', action='store_true')
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    us = completions()

    import pandas as pd
    cp = pd.read_csv(COND_P); cp = cp[(cp.condition == 'P') & (cp.radius == 1)]
    vals = {int(r): (float(R), float(M), float(S), float(a))
            for r, R, M, S, a in zip(cp.rule, cp.R, cp.M, cp.S, cp.alpha)}
    for b, exp in EXPECTED_1D.items():
        assert all(abs(g - e) < 5e-4 for g, e in zip(vals[b], exp)), (b, vals[b], exp)
    print(f'condition-P 1D values asserted for all {len(EXPECTED_1D)} bases')

    if args.timing:
        u = us[0]; t = embed(110, mc.bits_of(u))
        t0 = time.time(); r = evaluate(t, 2, ('A', u), u); e2 = time.time() - t0
        t0 = time.time(); tr = transverse(t, 110, u); et = time.time() - t0
        t0 = time.time(); r3 = evaluate(embed(110, mc.bits_of(u)), 3, ('A', u), u); e3 = time.time() - t0
        print(f'h2 {e2:.2f}s (agree {r["agree"]:.3f}) | transverse {et:.2f}s ({tr}) | h3 {e3:.2f}s mode={r3["reference_mode"]}')
        return

    ctrl = controls(us)
    print(json.dumps(ctrl, indent=1))
    if not (ctrl['exposed_indices_distinct'] and ctrl['height2_conditions']['ok']
            and ctrl['height3_conditions']['ok'] and ctrl['beam_invariance']['ok']
            and ctrl['completions_disjoint']['ok'] and ctrl['step_covariance_exact']):
        raise SystemExit('controls failed')

    print('matched null pairs (control, before any tier)...', flush=True)
    nulls = matched_null_pairs(us)
    if not all(r['identical_to_1e-9'] for r in nulls):
        (OUT / 'controls_failed.json').write_text(json.dumps(
            {'controls': ctrl, 'matched_null_pairs': nulls}, indent=1, allow_nan=False) + '\n')
        raise SystemExit('matched null-pair control failed; see controls_failed.json')
    print('matched null pairs pass', flush=True)

    t0 = time.time()
    chunks = lambda n, size: [list(range(i, min(i + size, n))) for i in range(0, n, size)]
    specs = ([('main', c, us) for c in chunks(N_COMPLETIONS, 8)]
             + [('h3', c, us) for c in chunks(N_H3, 8)])
    out = []
    with Pool(args.workers) as pool:
        for i, rows in enumerate(pool.imap_unordered(job, specs, chunksize=1)):
            out += rows
            print(f'chunk {i+1}/{len(specs)} rows={len(out)} {time.time()-t0:.0f}s', flush=True)
    (OUT / 'controls.json').write_text(json.dumps(
        {'protocol': PROTOCOL, 'controls': ctrl, 'matched_null_pairs': nulls,
         'all_matched_identical': all(r['identical_to_1e-9'] for r in nulls),
         'condition_p_1d': {str(b): vals[b] for b in BASES}}, indent=1, allow_nan=False) + '\n')
    (OUT / 'rows.json').write_text(json.dumps(
        {'protocol': PROTOCOL, 'bases': BASES, 'original_bases': ORIGINAL, 'new_bases': NEW,
         'n_completions': N_COMPLETIONS, 'n_h3': N_H3, 'density': DENSITY,
         'completions': us, 'rows': out, 'wall_seconds': time.time() - t0},
        indent=1, sort_keys=True, allow_nan=False) + '\n')
    print(OUT / 'rows.json', f'{time.time()-t0:.0f}s rows={len(out)}')

if __name__ == '__main__':
    main()
