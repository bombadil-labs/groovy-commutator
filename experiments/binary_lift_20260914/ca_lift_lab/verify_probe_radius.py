"""Independent cropped-word census checks and scalar global-witness checks."""
import argparse
import itertools
import json
import math
from pathlib import Path

import numpy as np
from harness import Compiler, derive, load_operator


def read(grid, rx):
    width = 2*rx+1; start = (grid.shape[-1]-width)//2
    b = grid[..., start:start+width]
    b = np.concatenate([b, np.roll(b, -1, axis=1), np.roll(b, 1, axis=1)], axis=-1)
    return b @ (1 << np.arange(3*width-1, -1, -1, dtype=np.uint32))


def consistent(base_keys, base_bits, keys, bits, z=None):
    seen = {} if z is None else {0: z}
    for k, v in zip(base_keys.ravel().tolist(), base_bits.ravel().tolist()):
        if k in seen and seen[k] != v: return False
        seen[k] = v
    for k, v in zip(keys.ravel().tolist(), bits.ravel().tolist()):
        if z is not None: v ^= z
        if k in seen and seen[k] != v: return False
        seen[k] = v
    return True


def scalar_d(s, rule):
    return [((rule ^ 204) >> (4*s[(i-1) % len(s)]+2*s[i]+s[(i+1) % len(s)])) & 1 for i in range(len(s))]


def xor(a, b): return [x ^ y for x, y in zip(a, b)]


def scalar_encode(s, rule, choice):
    ds = scalar_d(s, rule); mask = choice['mask']; shift = choice['shift']
    p = [s[i] ^ s[(i+shift) % len(s)] for i in range(len(s))]
    if mask == 'birth': m = [(1-x) & y for x, y in zip(s, ds)]
    elif mask == 'death': m = [x & y for x, y in zip(s, ds)]
    elif mask == 'stay_one': m = [x & (1-y) for x, y in zip(s, ds)]
    else: m = [(1-x) & (1-y) for x, y in zip(s, ds)]
    return [p, ds, m]


def reconstruct(event, rule, choice, z):
    if event['kind'] == 'chosen_zero_bit': return [[0], [0], [0]], event['required']
    s = [int(x) for x in event['source']]; n = len(s); phase = event['phase']
    ds = scalar_d(s, rule); es = xor(s, ds)
    a = scalar_encode(s, rule, choice); b = scalar_encode(es, rule, choice)
    flip = [xor(x, y) for x, y in zip(a, b)]
    if event['kind'] == 'beam': grid = a; bit = flip[phase][0]
    elif event['kind'] == 'temporal':
        c = scalar_encode(xor(es, scalar_d(es, rule)), rule, choice)
        g = xor(scalar_d(es, rule), xor(ds, scalar_d(ds, rule)))
        grid = flip; bit = a[phase][0] ^ c[phase][0]
        bit ^= g[0] ^ g[choice['shift'] % n] if phase == 0 else g[0]
    else:
        shifted = s[1:] + s[:1]
        g = xor(xor(ds, scalar_d(shifted, rule)), scalar_d(xor(s, shifted), rule))
        grid = [xor(row, row[1:]+row[:1]) for row in a]
        bit = flip[phase][0] ^ flip[phase][1]
        bit ^= g[0] ^ g[choice['shift'] % n] if phase == 0 else g[0]
    if z is not None and event['kind'] != 'beam': bit ^= z ^ ((rule & 1) if phase == 1 else 0)
    return [grid[(phase+y) % 3] for y in range(3)], bit


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--run', type=Path, required=True)
    args = ap.parse_args(); root = Path(__file__).resolve().parent
    op = load_operator(root/'lifts/fixed_transverse.py')
    records = [json.loads(x) for x in (args.run/'candidates.jsonl').read_text().splitlines()]
    prior = {r['candidate']: r for r in map(json.loads, (root/'runs/polarization_preflight_v2/candidates.jsonl').read_text().splitlines())}
    decisions = 0
    for rec in records:
        r = rec['rule']; rx = rec['horizontal_radius']; path = rec['recipe']; sign = path[0]['shift']
        compiler = Compiler(r, rx+1, op)
        a = compiler.encode(path); c = compiler.encode(path, 2); delta = compiler.mask(path)
        bk = read(a, rx); bv = delta[..., rx]
        ds = compiler.source_masks[0]
        gt = compiler.source_masks[1] ^ (ds[..., 1:-1] ^ derive(ds, r))
        def carrier(g): return np.stack([g[:, rx] ^ g[:, rx+sign], g[:, rx]], axis=1)
        probes = {'temporal': (read(delta, rx)[:, :2], a[:, :2, rx+1] ^ c[:, :2, rx-1] ^ carrier(gt))}
        s = compiler.source
        for shift in (-1, 1):
            sa = s[:, 1:-1]; sb = s[:, :-2] if shift == -1 else s[:, 2:]
            gx = derive(sa, r) ^ derive(sb, r) ^ derive(sa ^ sb, r)
            u = a[..., 1:-1] ^ (a[..., :-2] if shift == -1 else a[..., 2:])
            desired = delta[:, :2, rx] ^ delta[:, :2, rx+shift] ^ carrier(gx)
            probes[f'spatial_{shift:+d}'] = (read(u, rx)[:, :2], desired)
        probes['joint'] = (np.concatenate([p[0] for p in probes.values()]), np.concatenate([p[1] for p in probes.values()]))
        for name, (keys, bits) in probes.items():
            assert consistent(bk, bv, keys, bits) == rec['probes'][name]['raw']['passes']
            corrected = bits.copy(); corrected[:, 1] ^= r & 1
            matches = [consistent(bk, bv, keys, corrected, z) for z in (0, 1)]
            assert matches == [b['passes'] for b in rec['probes'][name]['centered_branches']]
            decisions += 3
        if rx == 1:
            old = prior[rec['candidate']]
            assert rec['probes']['temporal']['raw']['passes'] == old['groovy_orbit_uncentered']['passes']
            assert rec['probes']['temporal']['centered_pass'] == old['groovy_orbit_centered_pass']
    witnesses = 0
    for rec in map(json.loads, (args.run/'global_obstructions.jsonl').read_text().splitlines()):
        for probe in rec['probes'].values():
            for z, case in [(None, probe['raw']), *enumerate(probe['centered_branches'])]:
                if not case['obstructed']: continue
                a, x = reconstruct(case['existing'], rec['rule'], rec['recipe'][0], z)
                b, y = reconstruct(case['new'], rec['rule'], rec['recipe'][0], z)
                length = math.lcm(len(a[0]), len(b[0]))
                assert all(a[j][i % len(a[0])] == b[j][i % len(b[0])] for j in range(3) for i in range(length))
                assert x != y and x == case['existing']['required'] and y == case['new']['required']
                witnesses += 1
    result = {'status': 'passed', 'candidate_radius_records': len(records),
              'independent_unmarked_branch_decisions': decisions,
              'global_contradictions_reconstructed': witnesses,
              'radius_one_reproduces_previous_G_census': True}
    (args.run/'verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__': main()
