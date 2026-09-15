#!/usr/bin/env python3
"""Post-hoc endpoint-period inspection, separate from frozen catalog scoring.

Run catalog_compare.py lift first: that independently validates these decoded
roots and their actual archive source order against the original source archive.
This script exhausts the free-orbit pairs for the four reported width-eight
cases. It verifies an existing witness file rather than silently replacing it.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / 'experiments/observation_catalog_20260915'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def inspect(unit):
    prior_path = unit / 'inputs/previous_result.json'
    assert digest(prior_path) == '5101ad951144527fad7f32bc3819da3b540fe3320fde34478ca99fe136fa71b3'
    prior = {row['id']: row for row in json.loads(prior_path.read_text())['records']}
    results = []
    for rule, dimension in itertools.product((54, 110), (3, 4)):
        ident = f'w8_r{rule:03d}_d{dimension}'
        relations = unit / 'inputs/relations' / (ident + '.npz')
        assert digest(relations) == prior[ident]['arrays_sha256']
        with np.load(relations) as data, np.load(unit / 'lift' / (ident + '.npz')) as graph:
            root = graph['root']
            assert root.shape == (256, 8)
            # Direct cyclic equality on decoded rows: never infer orientation
            # from a numeric source index in the archive.
            periods = [next(p for p in range(1, 9)
                            if all(int(row[i]) == int(row[(i+p) % 8])
                                   for i in range(8))) for row in root]
            assert np.array_equal(periods, graph['spatial_period'])
            reps = data['orbit_representatives']
            labels = data['finite_symbol'].ravel()[reps]
            sources = reps // int(np.prod(data['grid_shape'][1:-1]))
            groups = defaultdict(list)
            for orbit, label in enumerate(labels):
                if label:
                    groups[int(label)].append(orbit)
            counts = Counter()
            witnesses = {}
            # First encountered free block in the frozen orbit ordering.
            for variable in groups:
                for left, right in itertools.combinations(groups[variable], 2):
                    source_pair = [int(sources[left]), int(sources[right])]
                    endpoint_periods = [periods[s] for s in source_pair]
                    key = tuple(sorted(endpoint_periods))
                    counts[key] += 1
                    witnesses.setdefault(key, {
                        'variable': variable,
                        'orbit_indices': [left, right],
                        'source_indices': source_pair,
                        'source_bits_x0_first': [''.join(map(str, root[s])) for s in source_pair],
                        'periods': endpoint_periods,
                    })
            results.append({
                'rule': rule, 'width': 8, 'dimension': dimension,
                'pair_period_counts': [
                    {'periods': list(key), 'pairs': counts[key], 'witness': witnesses[key]}
                    for key in sorted(counts)
                ],
                'total_pairs': sum(counts.values()),
            })
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--unit', type=Path, default=UNIT)
    parser.add_argument('--output', type=Path, default=ROOT / 'review/catalog-replay/period-witnesses.json')
    args = parser.parse_args()
    result = inspect(args.unit)
    if args.output.exists():
        assert json.loads(args.output.read_text()) == result, 'Existing witness output differs'
        operation = 'verified_existing'
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')
        operation = 'created'
    print(json.dumps({'operation': operation, 'cases': len(result),
                      'pairs': sum(row['total_pairs'] for row in result),
                      'source_sha256': digest(__file__),
                      'output_sha256': digest(args.output),
                      'post_hoc': True}))


if __name__ == '__main__':
    main()
