"""Exact stencil restrictions and exact center-containing 2D support minima.

Consumes saved exhaustive constraints, so no trajectories or new lift choices
are generated. Higher-dimensional support results apply to the named stencils;
they are not claims of global minimality. Tagged row autonomy is diagnostic only.
"""
import argparse
import hashlib
import itertools
import json
import sqlite3
import time
from pathlib import Path

import numpy as np
from inspect_run import table

OFFSETS = (0, 1, -1)


def stencils(d):
    coords = list(itertools.product(OFFSETS, repeat=d-1))
    coords = [(*v, x) for v in coords for x in (-1, 0, 1)]
    tests = {
        'full': list(range(len(coords))),
        'horizontal_row': [i for i, v in enumerate(coords) if not any(v[:-1])],
        'transverse_column': [i for i, v in enumerate(coords) if v[-1] == 0],
        'axis_cross': [i for i, v in enumerate(coords) if sum(x != 0 for x in v) <= 1],
        'newest_axis_sheet': [i for i, v in enumerate(coords) if not any(v[1:-1])],
    }
    for axis in range(d-1):
        tests[f'omit_transverse_axis_{axis}'] = [i for i, v in enumerate(coords) if v[axis] == 0]
    return coords, tests


def restrict(bits, masks, selected, names, prefix=None):
    packed = np.packbits(bits[:, selected], axis=1, bitorder='big')
    if prefix is not None:
        packed = np.concatenate((prefix, packed), axis=1)
    opaque = np.ascontiguousarray(packed).view(np.dtype((np.void, packed.shape[1]))).ravel()
    _, inverse = np.unique(opaque, return_inverse=True)
    merged = np.zeros((int(inverse.max())+1, masks.shape[1]), dtype=np.uint8)
    np.bitwise_or.at(merged, inverse.ravel(), masks)
    conflicts = {name: int(np.count_nonzero(merged[:, j] == 3)) for j, name in enumerate(names)}
    out = {'cells': len(selected), 'observed': len(merged), 'conflicts': conflicts,
           'all_four': not any(conflicts.values()),
           'strict': all(conflicts[n] == 0 for n in ('derivative', 'source', 'parent'))}
    return out


def exact_2d(bits, masks, names):
    """A support must hit every pairwise difference with different targets.

    Native flip supports include the physical center, since the step integrates
    the flip with that bit. Enumerate every one of the 256 such supports.
    """
    weights = (1 << np.arange(9, dtype=np.uint16))
    words = bits @ weights
    differences = words[:, None] ^ words[None, :]
    supports = np.array(sorted((s for s in range(512) if s & 2),
                               key=lambda s: (s.bit_count(), s)), dtype=np.uint16)
    targets = (masks == 2).astype(np.uint16)
    result = {}
    sets = {'derivative': [names.index('derivative')],
            'source': [names.index('source')],
            'strict': [names.index(n) for n in ('derivative', 'source', 'parent')],
            'all_four': list(range(len(names)))}
    for name, columns in sets.items():
        if np.any(masks[:, columns] == 3):
            result[name] = {'cells': None, 'number_of_minima': 0, 'example_indices': None,
                            'reason': 'The full neighborhood already has a conflict for this target.'}
            continue
        target = targets[:, columns] @ (1 << np.arange(len(columns), dtype=np.uint16))
        requirements = np.unique(differences[target[:, None] != target[None, :]])
        assert 0 not in requirements
        ok = np.all((requirements[:, None] & supports[None, :]) != 0, axis=0)
        valid = supports[ok]
        best = int(valid[0]); size = best.bit_count()
        minima = [int(s) for s in valid if int(s).bit_count() == size]
        result[name] = {'cells': size, 'number_of_minima': len(minima),
                        'example_indices': [i for i in range(9) if best & (1 << i)]}
    return result


def aggregate(records):
    output = {}
    for family in sorted({r['family'] for r in records}):
        output[family] = {}
        for d in (2, 3, 4):
            rows = [r for r in records if r['family'] == family and r['dimension'] == d]
            stage = {'passing_full_candidates': len(rows),
                     'passing_full_rules': len({r['rule'] for r in rows}), 'stencils': {}}
            for name in rows[0]['stencils']:
                info = {'cells': rows[0]['stencils'][name]['cells']}
                for task in ('derivative', 'source', 'parent', 'parent_derivative', 'all_four', 'strict'):
                    def passes(r):
                        test = r['stencils'][name]
                        return test[task] if task in ('all_four', 'strict') else test['conflicts'][task] == 0
                    successes = [r for r in rows if passes(r)]
                    success_rules = sorted({r['rule'] for r in successes})
                    info[task] = {'candidates': len(successes), 'rule_count': len(success_rules), 'rules': success_rules}
                stage['stencils'][name] = info
            if d == 2:
                def minimum(rule, task):
                    sizes = [r['exact_2d'][task]['cells'] for r in rows if r['rule'] == rule]
                    return min((s for s in sizes if s is not None), default=None)
                stage['exact_minimum_by_rule'] = {
                    task: {str(rule): minimum(rule, task)
                           for rule in sorted({r['rule'] for r in rows})}
                    for task in ('derivative', 'source', 'strict', 'all_four')}
            output[family][str(d)] = stage
    return output


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    start = time.perf_counter()
    records = []
    inputs = {'pdm': 'fixed_transverse_to_4', 'copy_complement': 'copy_complement_control_to_4'}
    with (args.output/'candidates.jsonl').open('w') as log:
        for family, run in inputs.items():
            db = sqlite3.connect(args.root/'runs'/run/'constraints.sqlite3')
            for cid, rule, dimension, raw in db.execute(
                    'SELECT id,rule,dimension,record_json FROM candidates WHERE strict_pass=1 ORDER BY dimension,rule,id'):
                r = json.loads(raw)
                keys, masks, _, names = table(db, cid)
                assert np.all((masks >= 1) & (masks <= 3))
                bits = np.unpackbits(keys, axis=1, bitorder='big')[:, :3**dimension]
                coords, subsets = stencils(dimension)
                tests = {name: restrict(bits, masks, subset, names) for name, subset in subsets.items()}
                assert tests['full']['strict']
                tkeys, tmasks, _, tnames = table(db, cid, 'tagged')
                tbits = np.unpackbits(tkeys[:, 4:], axis=1, bitorder='big')[:, :3**dimension]
                tests['tagged_horizontal_row'] = restrict(tbits, tmasks, subsets['horizontal_row'], tnames, tkeys[:, :4])
                record = {'family': family, 'candidate': cid, 'rule': rule, 'dimension': dimension,
                          'recipe': r['recipe'], 'constant_layers': r['constant_layers'],
                          'native_table_sha256': r['unmarked']['table_sha256'], 'stencils': tests}
                if dimension == 2:
                    record['exact_2d'] = exact_2d(bits, masks, names)
                records.append(record)
                log.write(json.dumps(record, separators=(',', ':'))+'\n')
                if len(records) % 250 == 0:
                    log.flush()
                    print(json.dumps({'candidates': len(records), 'family': family,
                                      'dimension': dimension, 'seconds': round(time.perf_counter()-start, 2)}), flush=True)
    summary = aggregate(records)
    (args.output/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    meta = {'elapsed_seconds': time.perf_counter()-start, 'candidates': len(records),
            'scope': 'All full-guarantee candidates across all 256 source ECA IDs; PDM has 64 first-floor failures.',
            'center_always_included': True, 'exact_support_minimum_dimensions': [2],
            'tagged_horizontal_row': 'Phase label is extra input; diagnostic only.',
            'inputs': inputs, 'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (args.output/'manifest.json').write_text(json.dumps(meta, indent=2)+'\n')
    (args.output/'source_audit.py').write_text(Path(__file__).read_text())
    compact = {f: {d: {n: {t: s[t]['rule_count'] for t in ('derivative', 'source', 'strict')}
                              for n, s in a['stencils'].items()}
                  for d, a in stages.items()} for f, stages in summary.items()}
    print(json.dumps({'elapsed_seconds': meta['elapsed_seconds'], 'summary': compact}), flush=True)


if __name__ == '__main__':
    main()
