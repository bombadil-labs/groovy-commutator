#!/usr/bin/env python3
"""Handed fiber census: every ECA gets a fiber, including 110.

Frozen protocol: docs/research/protocols/2026-09-17-handed-fiber-census.md
(committed before this implementation).

The handed family H is f(c, w, n7): centre, west neighbour (offset dx = -1),
and the count of the other seven Moore neighbours, index i = 16c + 8w + n7,
32 table entries. Its height-one restriction is a coordinate projection onto
all 256 ECAs with fibers of exactly 2**24 rules.

The observation contract is the earlier censuses' unchanged: the 18-symbol
outer-totalistic observer (centre * 9 + Moore count) is a function of the
state alone, and the handed rule keeps the Life-like causal window, so the
step function is dispatched into the existing harness rather than forked.

    python experiments/handed_fiber_census_20260917/run.py --workers 4
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, math, sys, time
from dataclasses import dataclass
from multiprocessing import Pool
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CROSS = ROOT / 'experiments/cross_dimensional_class4_20260917'

def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); sys.modules[name] = mod; spec.loader.exec_module(mod)
    return mod

# Load the first census first and take ITS harness module objects: fc1 loads
# its own copies under the same names, so importing them separately here would
# leave two shadowed module objects and patch the wrong one.
fc1 = _load('fc1', ROOT / 'experiments/fiber_census_20260917/run.py')
base, strip = fc1.base, fc1.strip

PROTOCOL = 'handed-fiber-census-20260917'
OUT = ROOT / 'results/handed_fiber_census_20260917'
WHOLE_SAMPLE = 12
PANEL_SAMPLE = 256
PANEL = [110, 124, 137, 54, 22, 30, 90, 0, 204]
DENSITY = 0.5

def seed(*parts):
    h = hashlib.sha256('|'.join(map(str, (PROTOCOL,) + parts)).encode()).digest()
    return int.from_bytes(h[:8], 'little') & 0x7fff_ffff_ffff_ffff

fc1.seed = seed
fc1.PROTOCOL = PROTOCOL
fc1.DENSITY = DENSITY

# ---------------------------------------------------------------- the family

@dataclass(frozen=True)
class HandedRule:
    name: str
    table: int
    role: str = 'fiber'

def _exposed():
    """Index i(c, w, n7) forced by each ECA window, in (L,C,R) order 000..111."""
    out = []
    for L in (0, 1):
        for C in (0, 1):
            for R in (0, 1):
                out.append(16 * C + 8 * L + (2 * L + 2 * C + 3 * R))
    return out

EXPOSED = _exposed()
FREE = [i for i in range(32) if i not in EXPOSED]
assert len(set(EXPOSED)) == 8 and len(FREE) == 24

def res1(table):
    """Height-one restriction: a coordinate projection onto the 256 ECAs."""
    return sum(((table >> i) & 1) << bit for bit, i in enumerate(EXPOSED))

def embed(base_rule, free_bits):
    t = sum(((base_rule >> bit) & 1) << i for bit, i in enumerate(EXPOSED))
    return t | sum(b << i for b, i in zip(free_bits, FREE))

def iota(births, survives):
    """The Life-like family embeds into H."""
    t = 0
    for c in (0, 1):
        for w in (0, 1):
            for n7 in range(8):
                if (w + n7) in (survives if c else births):
                    t |= 1 << (16 * c + 8 * w + n7)
    return t

def handed_step(state, rule):
    total = np.zeros_like(state, dtype=np.uint8)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0: continue
            total += np.roll(np.roll(state, dy, axis=0), dx, axis=1)
    west = np.roll(state, 1, axis=1)          # np.roll shift +1 is the dx = -1 neighbour
    tab = np.array([(rule.table >> i) & 1 for i in range(32)], dtype=np.uint8)
    return tab[(16 * state + 8 * west + (total - west)).astype(np.int64)]

def handed_batch_symbol(patches, rule):
    """Successor symbol of the centre of a [batch, k, 5] patch under a handed rule."""
    n, k, _ = patches.shape
    tab = np.array([(rule.table >> i) & 1 for i in range(32)], dtype=np.uint8)
    vals = []; center_idx = None
    for sy in (-1, 0, 1):
        for sx in (1, 2, 3):
            cnt = np.zeros(n, dtype=np.uint8)
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx == 0 and dy == 0: continue
                    cnt += patches[:, (sy + dy) % k, sx + dx]
            c = patches[:, sy % k, sx]
            w = patches[:, sy % k, sx - 1]
            if sy == 0 and sx == 2: center_idx = len(vals)
            vals.append(tab[(16 * c + 8 * w + (cnt - w)).astype(np.int64)])
    arr = np.stack(vals, axis=1)
    c = arr[:, center_idx]
    return (c * 9 + (arr.sum(axis=1) - c)).astype(np.uint8)

# Dispatch the handed step into the harness; the Life-like path is untouched.
_life_step, _batch_symbol = base.life_step, strip.batch_successor_symbol_strip
base.life_step = lambda st, r: handed_step(st, r) if isinstance(r, HandedRule) else _life_step(st, r)
strip.batch_successor_symbol_strip = lambda p, r: handed_batch_symbol(p, r) if isinstance(r, HandedRule) else _batch_symbol(p, r)

# ------------------------------------------------------------- measurement

def evaluate(table, base_rule, k=2):
    hr = HandedRule(name=f'h{table}', table=table)
    t = time.time()
    events = fc1.sample_events(hr, k)
    p, nref, refmode = strip.reference_strip(hr, k)
    r, mu, sd, missing = base.selective_r(events, p)
    m, bll, hll, ntr, nte = base.predictive_gain(events[:4], events[4:6])
    sp = fc1.spread(hr, k)
    return {'table': table, 'base': base_rule, 'height': k, 'density': DENSITY,
            'R_star': r, 'M_star': m, 'S_star': max(0, r) * max(0, m) if math.isfinite(r) else None,
            'reference_mode': refmode, 'reference_samples': nref, 'unsupported_symbols': missing,
            'baseline_logloss_bits': bll, 'history_logloss_bits': hll,
            'train_events': ntr, 'test_events': nte, **sp, 'wall_seconds': time.time() - t}

def sample_fiber(base_rule, n):
    rng = np.random.default_rng(seed('sample', base_rule))
    seen = set(); chosen = []
    while len(chosen) < n:
        t = embed(base_rule, rng.integers(0, 2, 24).tolist())
        if t not in seen: seen.add(t); chosen.append(int(t))
    return chosen

def eca_step(row, rule):
    idx = (np.roll(row, 1) << 2) | (row << 1) | np.roll(row, -1)
    return np.array([(rule >> i) & 1 for i in range(8)], dtype=np.uint8)[idx]

def exactness_trajectory(base_rule, tables, steps=256):
    """Control 5: height-one trajectories of fiber members equal the base ECA's."""
    rng = np.random.default_rng(seed('exact', base_rule))
    row = rng.integers(0, 2, strip.WIDTH, dtype=np.uint8)
    for t in tables[:8]:
        if res1(t) != base_rule: return False
        st = row[None, :].copy(); e = row.copy()
        for _ in range(steps):
            if not np.array_equal(st[0], e): return False
            st = handed_step(st, HandedRule(f'h{t}', t)); e = eca_step(e, base_rule)
    return True

def run_fiber(job):
    base_rule, n = job
    tables = sample_fiber(base_rule, n)
    if not exactness_trajectory(base_rule, tables):
        return {'base': base_rule, 'exact': False}
    t0 = time.time(); rows = []
    for t in tables:
        rows.append(evaluate(t, base_rule))
    (OUT / 'shards').mkdir(parents=True, exist_ok=True)
    (OUT / 'shards' / f'fiber_{base_rule:03d}.json').write_text(
        json.dumps({'base': base_rule, 'exact': True, 'n': n, 'rows': rows,
                    'wall_seconds': time.time() - t0}, sort_keys=True, allow_nan=False) + '\n')
    print(f'fiber {base_rule:3d} n={n:3d} {time.time()-t0:6.0f}s', flush=True)
    return {'base': base_rule, 'exact': True}

# --------------------------------------------------------- global controls

def global_controls():
    c = {}
    c['1_exposed_indices_distinct'] = {'indices': EXPOSED, 'distinct': len(set(EXPOSED)) == 8}
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
    c['2_height2_conditions_reached'] = {'reached': len(reach), 'of': 32, 'ok': len(reach) == 32}
    ok = True
    for mask in range(1 << 18):
        bb, ss = fc1.mask_to_rule(mask)
        if res1(iota(bb, ss)) != fc1.height1_eca(mask): ok = False; break
    c['3_res1_of_lifelike_embedding'] = {'all_262144_agree': ok}
    hl = base.LifeRule('HighLife', (3, 6), (2, 3), 'control')
    thl = iota(hl.births, hl.survives); agree = True
    rng = np.random.default_rng(seed('control4'))
    for h in (1, 2, 3):
        st = rng.integers(0, 2, (h, 97), dtype=np.uint8); a = st.copy(); b = st.copy()
        for _ in range(256):
            a = handed_step(a, HandedRule('hl', thl)); b = _life_step(b, hl)
            if not np.array_equal(a, b): agree = False; break
    pa = rng.integers(0, 2, (5000, 2, 5), dtype=np.uint8)
    sym = bool(np.array_equal(handed_batch_symbol(pa, HandedRule('hl', thl)), _batch_symbol(pa, hl)))
    c['4_highlife_embedding'] = {'trajectories_agree_h123': agree, 'symbols_agree_5000_patches': sym}
    c['6_res1_onto'] = {'images': len({res1(int(t)) for t in
                        np.random.default_rng(seed('onto')).integers(0, 1 << 32, 200000, dtype=np.uint64)}), 'of': 256}
    return c

def complement_control():
    """Control 6b: fiber(110) rules and their conjugates in fiber(137) agree exactly."""
    def conj(t):
        out = 0
        for c in (0, 1):
            for w in (0, 1):
                for n7 in range(8):
                    if not ((t >> (16 * c + 8 * w + n7)) & 1):
                        out |= 1 << (16 * (1 - c) + 8 * (1 - w) + (7 - n7))
        return out
    rows = []
    for t in sample_fiber(110, 8):
        ct = conj(t)
        rows.append({'table': t, 'conjugate': ct, 'res1': res1(t), 'conjugate_res1': res1(ct),
                     'conjugate_in_137': res1(ct) == 137})
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--workers', type=int, default=4)
    ap.add_argument('--bases', type=str, default=None, help='debug only')
    ap.add_argument('--timing', action='store_true', help='time a single rule and exit')
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if args.timing:
        t = sample_fiber(110, 1)[0]; t0 = time.time(); r = evaluate(t, 110)
        print(f'one rule {time.time()-t0:.2f}s S*={r["S_star"]} alpha={r["alpha_x"]}'); return
    ctrl = global_controls()
    print(json.dumps(ctrl, indent=1))
    bad = [k for k, v in ctrl.items() if not all(x is True for x in v.values() if isinstance(x, bool))]
    if bad or ctrl['6_res1_onto']['images'] != 256: raise SystemExit(f'global controls failed: {bad}')
    bases = [int(x) for x in args.bases.split(',')] if args.bases else list(range(256))
    jobs = [(b, PANEL_SAMPLE if b in PANEL else WHOLE_SAMPLE) for b in bases]
    jobs.sort(key=lambda j: (j[0] not in PANEL, j[0]))     # panel fibers first
    t0 = time.time()
    with Pool(args.workers) as pool:
        status = pool.map(run_fiber, jobs, chunksize=1)
    exact = {str(s['base']): s['exact'] for s in status}
    (OUT / 'exactness_control.json').write_text(json.dumps(
        {'protocol': PROTOCOL, 'global': ctrl, 'height1_identity': exact,
         'complement_pairs_110_137': complement_control()}, indent=1) + '\n')
    if not all(exact.values()): raise SystemExit(f'exactness failed: {[b for b, v in exact.items() if not v]}')
    rows = []
    for b, _ in jobs:
        rows += json.loads((OUT / 'shards' / f'fiber_{b:03d}.json').read_text())['rows']
    (OUT / 'rows.json').write_text(json.dumps(
        {'protocol': PROTOCOL, 'height': 2, 'density': DENSITY, 'whole_sample': WHOLE_SAMPLE,
         'panel_sample': PANEL_SAMPLE, 'panel': PANEL, 'bases': bases, 'rows': rows,
         'wall_seconds': time.time() - t0}, indent=1, sort_keys=True, allow_nan=False) + '\n')
    print(OUT / 'rows.json', f'{time.time()-t0:.0f}s')

if __name__ == '__main__':
    main()
