#!/usr/bin/env python3
"""Import existing finite catalog measurements; never run CA evolution."""
from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import tempfile

import numpy as np

from rule_ring_selectors import Case, canonical, sha256


CATALOG_IMPLEMENTATION_SHA = 'a9946232dd347121adfd51b7ff8c240d5fc258e6fe20428692e7cec92364fc88'


def catalog_cases(root, *, rules, candidates, metrics, widths):
    """Yield cases from the frozen 2026-09-15 archive with explicit subsets.

    Each input hash is carried in the source reference. This checks schema and
    coordinates, but does not independently reverify the archived measurements.
    """
    root = Path(root)
    definition = root / 'scripts/observation_catalog.py'
    if sha256(definition) != CATALOG_IMPLEMENTATION_SHA:
        raise ValueError('catalog definition does not match the supported frozen revision')
    # Import definitions only after checking their exact frozen source bytes.
    import importlib.util
    spec = importlib.util.spec_from_file_location('frozen_observation_catalog', definition)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    selections = [(rules, 256, 'rules'), (candidates, 300, 'candidates'), (metrics, 7, 'metrics')]
    for selected, stop, name in selections:
        if not selected or len(set(selected)) != len(selected) or any(type(i) is not int or not 0 <= i < stop for i in selected):
            raise ValueError(f'invalid or duplicate {name}')
    if not widths or len(set(widths)) != len(widths) or set(widths) - {7, 8, 9}:
        raise ValueError('finite catalog widths must be a subset of 7, 8, 9')
    unit = root / 'experiments/observation_catalog_20260915'
    context = {'ensemble': 'all_binary_source_states', 'burn_in': 0,
               'sampling': 'all_states_at_pointed_site_zero', 'floor': 1,
               'completion': 'full_ECA_rule', 'cadence': 1,
               'observation_definition_sha256': CATALOG_IMPLEMENTATION_SHA,
               'catalog': 'observation_catalog_20260915'}
    for filename, supported in [('discovery-metrics.npz', (7, 8)), ('confirmation-metrics.npz', (9,))]:
        chosen = sorted(set(widths) & set(supported))
        if not chosen:
            continue
        path = unit / filename
        digest = sha256(path)
        with np.load(path, allow_pickle=False) as archive:
            values = archive['metrics']
            expected = (2, 256, 300, 7) if len(supported) == 2 else (256, 300, 7)
            if values.shape != expected or values.dtype.kind != 'f':
                raise ValueError(f'unexpected catalog schema: {filename}')
            if len(supported) == 2 and archive['widths'].tolist() != [7, 8]:
                raise ValueError('unexpected discovery width coordinates')
            for width in chosen:
                for rule in sorted(rules):
                    for candidate in sorted(candidates):
                        names = '+'.join(module.NAMES[i] for i in module.CANDIDATES[candidate])
                        for metric in sorted(metrics):
                            index = ((supported.index(width),) if len(supported) == 2 else ()) + (rule, candidate, metric)
                            value = float(values[index])
                            if not np.isfinite(value) and not (np.isnan(value) and candidate < 24 and metric == 6):
                                raise ValueError('unexpected non-finite catalog value')
                            yield Case(str(rule), width, f'{names}/{module.METRICS[metric]}',
                                       None if np.isnan(value) else value, context,
                                       f'{filename}#sha256={digest};metrics{index}')
        if sha256(path) != digest:
            raise RuntimeError('catalog changed during import')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', required=True, type=Path, help='root of the extracted observation catalog archive')
    parser.add_argument('--output', required=True, type=Path, help='JSONL cases')
    parser.add_argument('--rules', required=True, nargs='+', type=int)
    parser.add_argument('--candidates', required=True, nargs='+', type=int)
    parser.add_argument('--metrics', required=True, nargs='+', type=int)
    parser.add_argument('--widths', nargs='+', type=int, default=[7, 8, 9])
    args = parser.parse_args()
    protected = [args.catalog / 'scripts/observation_catalog.py',
                 args.catalog / 'experiments/observation_catalog_20260915/discovery-metrics.npz',
                 args.catalog / 'experiments/observation_catalog_20260915/confirmation-metrics.npz']
    if args.output.resolve() in {p.resolve() for p in protected}:
        parser.error('output must not overwrite catalog inputs')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    count = 0
    try:
        with tempfile.NamedTemporaryFile(mode='w', dir=args.output.parent, delete=False) as stream:
            temporary = Path(stream.name)
            for case in catalog_cases(args.catalog, rules=args.rules, candidates=args.candidates,
                                      metrics=args.metrics, widths=args.widths):
                stream.write(canonical(asdict(case)) + '\n')
                count += 1
        temporary.replace(args.output)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    print(json.dumps({'status': 'complete', 'cases': count, 'sha256': sha256(args.output)}))


if __name__ == '__main__':
    main()
