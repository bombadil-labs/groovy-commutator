"""Independent direct checks for the support audit's two main claims."""
import argparse
import itertools
import json
import sqlite3
from pathlib import Path

import numpy as np
from inspect_run import table


def brute_minimum(bits, masks, columns):
    # Enumerate subsets and use a plain dictionary, independent of pairwise
    # difference/hitting-set computation in audit_local_support.py.
    words = [sum(int(bit) << i for i, bit in enumerate(row)) for row in bits]
    outputs = [tuple(int(row[c]) for c in columns) for row in masks]
    for size in range(1, 10):
        for others in itertools.combinations([0, 2, 3, 4, 5, 6, 7, 8], size-1):
            support = 2 + sum(1 << i for i in others)
            seen = {}
            valid = True
            for word, output in zip(words, outputs):
                key = word & support
                if key in seen and seen[key] != output:
                    valid = False
                    break
                seen[key] = output
            if valid:
                return size
    raise AssertionError('No support')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', type=Path, required=True)
    args = ap.parse_args()
    root = args.run.parent.parent
    dbs = {f: sqlite3.connect(root/'runs'/r/'constraints.sqlite3') for f, r in {
        'pdm': 'fixed_transverse_to_4', 'copy_complement': 'copy_complement_control_to_4'}.items()}
    rows = [json.loads(x) for x in (args.run/'candidates.jsonl').read_text().splitlines()]
    chosen = {}
    for r in rows:
        if r['dimension'] != 2:
            continue
        for task in ('derivative', 'source', 'strict'):
            chosen.setdefault((r['family'], task, r['exact_2d'][task]['cells']), r)
        if r['rule'] in (90, 110):
            chosen[r['family'], r['rule'], r['candidate']] = r
    selected = {(r['family'], r['candidate']): r for r in chosen.values()}
    minimum_checks = 0
    for r in selected.values():
        keys, masks, _, names = table(dbs[r['family']], r['candidate'])
        bits = np.unpackbits(keys, axis=1, bitorder='big')[:, :9]
        for task, cols in [('derivative', [names.index('derivative')]),
                           ('source', [names.index('source')]),
                           ('strict', [names.index(n) for n in ('derivative', 'source', 'parent')])]:
            assert brute_minimum(bits, masks, cols) == r['exact_2d'][task]['cells']
            minimum_checks += 1
    # Verify the explicit O(d) cross decoder/flip on all control constraints.
    cross_patches = 0
    for r in rows:
        if r['family'] != 'copy_complement':
            continue
        d = r['dimension']
        keys, masks, _, names = table(dbs['copy_complement'], r['candidate'])
        bits = np.unpackbits(keys, axis=1, bitorder='big')[:, :3**d]
        patch = bits.reshape((-1,) + (3,)*d)
        center = patch[(slice(None),) + (0,)*(d-1) + (1,)]
        polarity = np.zeros_like(center)
        parent = None
        for axis in range(d-1):
            index = [slice(None)] + [0]*(d-1) + [1]
            index[axis+1] = slice(None)
            majority = (patch[tuple(index)].sum(axis=1) >= 2).astype(np.uint8)
            polarity ^= center ^ majority
            if axis == 0:
                parent = majority
        horizontal = patch[(slice(None),) + (0,)*(d-1) + (slice(None),)]
        source = horizontal ^ polarity[:, None]
        idx = 4*source[:, 0]+2*source[:, 1]+source[:, 2]
        flip = ((r['rule'] ^ 204) >> idx) & 1
        expected = {'derivative': flip, 'parent_derivative': flip,
                    'source': source[:, 1], 'parent': parent}
        for j, name in enumerate(names):
            assert np.array_equal(masks[:, j], 1 << expected[name])
        cross_patches += len(keys)
    result = {'status': 'passed', 'minimum_cases': len(selected),
              'direct_minimum_checks': minimum_checks,
              'explicit_cross_formula_patches': cross_patches,
              'explicit_cross_formula_target_checks': 4*cross_patches}
    (args.run/'verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
