#!/usr/bin/env python3
"""All 64 height-one fibers at height two (frozen protocol 2026-09-17-fiber-census-64.md).

Reuses the first census's measurement code unchanged (experiments/fiber_census_20260917/run.py)
under this protocol's seed namespace, 128 uniformly sampled rules per fiber, four
worker processes over fibers. Writes per-fiber shards to results/fiber_census_64_20260917/shards/
then merges them into rows.json.

    python experiments/fiber_census_64_20260917/run.py --workers 4
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, sys, time
from multiprocessing import Pool
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('fc1', ROOT / 'experiments/fiber_census_20260917/run.py')
fc1 = importlib.util.module_from_spec(spec); sys.modules['fc1'] = fc1; spec.loader.exec_module(fc1)

PROTOCOL = 'fiber-census-64-20260917'
SAMPLE = 128
OUT = ROOT / 'results/fiber_census_64_20260917'

def seed(*parts):
    h = hashlib.sha256('|'.join(map(str, (PROTOCOL,) + parts)).encode()).digest()
    return int.from_bytes(h[:8], 'little') & 0x7fff_ffff_ffff_ffff

# Re-point the first census's seed namespace to this protocol for all measurements.
fc1.seed = seed
fc1.PROTOCOL = PROTOCOL

def symmetric_ecas():
    out = []
    for r in range(256):
        f = [(r >> i) & 1 for i in range(8)]
        if all(f[4 * a + 2 * b + c] == f[4 * c + 2 * b + a] for a in (0, 1) for b in (0, 1) for c in (0, 1)):
            out.append(r)
    assert len(out) == 64
    return out

def exposed_bits(base):
    b = lambda n: (base >> n) & 1
    # r = B0 + 18 B3 + 32 B6 + 4 S2 + 72 S5 + 128 S8 ; invert via the fiber's fixed bits
    fib = fc1.fiber(base)
    m = fib[0]
    return {'B0': (m >> 0) & 1, 'B3': (m >> 3) & 1, 'B6': (m >> 6) & 1, 'S2': (m >> 11) & 1, 'S5': (m >> 14) & 1, 'S8': (m >> 17) & 1}

def run_fiber(base):
    fib = fc1.fiber(base); assert len(fib) == 4096
    rng = np.random.default_rng(seed('sample', base))
    chosen = [int(x) for x in rng.choice(fib, size=SAMPLE, replace=False)]
    if not fc1.exactness_control(base, chosen):
        return {'base': base, 'exact': False, 'rows': []}
    rows = []
    t0 = time.time()
    for m in chosen:
        r = fc1.evaluate(m, 2); r['base'] = base; rows.append(r)
    shard = {'base': base, 'exact': True, 'exposed_bits': exposed_bits(base), 'rows': rows, 'wall_seconds': time.time() - t0}
    (OUT / 'shards').mkdir(parents=True, exist_ok=True)
    (OUT / 'shards' / f'fiber_{base:03d}.json').write_text(json.dumps(shard, sort_keys=True, allow_nan=False) + '\n')
    print(f'fiber {base:3d} done {time.time()-t0:.0f}s', flush=True)
    return {'base': base, 'exact': True}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--workers', type=int, default=4)
    ap.add_argument('--bases', type=str, default=None, help='debug only: comma-separated subset')
    args = ap.parse_args()
    bases = symmetric_ecas() if not args.bases else [int(x) for x in args.bases.split(',')]
    OUT.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    with Pool(args.workers) as pool:
        status = pool.map(run_fiber, bases, chunksize=1)
    exact = {str(s['base']): s['exact'] for s in status}
    (OUT / 'exactness_control.json').write_text(json.dumps({'protocol': PROTOCOL, 'height1_identity': exact}, indent=2) + '\n')
    if not all(exact.values()):
        raise SystemExit(f'exactness control failed: {[b for b, ok in exact.items() if not ok]}')
    rows = []; bits = {}
    for b in bases:
        sh = json.loads((OUT / 'shards' / f'fiber_{b:03d}.json').read_text())
        rows += sh['rows']; bits[str(b)] = sh['exposed_bits']
    (OUT / 'rows.json').write_text(json.dumps({'protocol': PROTOCOL, 'height': 2, 'density': fc1.DENSITY, 'sample_per_fiber': SAMPLE,
                                               'bases': bases, 'exposed_bits': bits, 'rows': rows, 'wall_seconds': time.time() - t0},
                                              indent=1, sort_keys=True, allow_nan=False) + '\n')
    print(OUT / 'rows.json', f'{time.time()-t0:.0f}s')

if __name__ == '__main__':
    main()
