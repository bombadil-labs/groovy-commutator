"""Exact whole-row collision witnesses on an eight-cell periodic source.

A collision at the same projection phase rules out autonomous horizontal-row
evolution at every radius on the prepared family. Absence of a witness is only
a finite-width result. This implements the encodings directly, without using
the lift plugin or the local-table compiler.
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np


def jets(rule, width, steps):
    source = ((np.arange(1 << width, dtype=np.uint64)[:, None]
               >> np.arange(width-1, -1, -1, dtype=np.uint64)) & 1).astype(np.uint8)
    result = [source]
    for _ in range(steps):
        x = result[-1]
        idx = 4*np.roll(x, 1, axis=-1)+2*x+np.roll(x, -1, axis=-1)
        result.append(x ^ (((rule ^ 204) >> idx) & 1).astype(np.uint8))
    return result


def lift_pair_sequence(states, family, choice):
    result = []
    for a, b in zip(states, states[1:]):
        if family == 'copy_complement':
            result.append(np.stack([a, a, 1-a], axis=1))
            continue
        derivative = a ^ b
        other = np.roll(a, -choice['shift'], axis=-1)
        for axis, shift in enumerate(choice['offsets'], 1):
            other = np.roll(other, -shift, axis=axis)
        mask = choice['mask']
        if mask == 'birth': m = (1-a) & derivative
        elif mask == 'death': m = a & derivative
        elif mask == 'stay_one': m = a & (1-derivative)
        elif mask == 'stay_zero': m = (1-a) & (1-derivative)
        else: raise ValueError(mask)
        result.append(np.stack([a ^ other, derivative, m], axis=1))
    return result


def witness(states, width):
    shape = states[0].shape[1:-1]
    weights = (1 << np.arange(width-1, -1, -1, dtype=np.uint64))
    now = states[0].reshape(1 << width, -1, width) @ weights
    nxt = states[1].reshape(1 << width, -1, width) @ weights
    failures = []
    for phase in range(now.shape[1]):
        seen = {}
        found = None
        for source in range(1 << width):
            key, target = int(now[source, phase]), int(nxt[source, phase])
            if key in seen:
                previous, previous_target = seen[key]
                if previous_target != target:
                    found = {'phase': phase,
                             'phase_coordinates': [int(n) for n in np.unravel_index(phase, shape)],
                             'source_a': format(previous, f'0{width}b'),
                             'source_b': format(source, f'0{width}b'),
                             'identical_current_row': format(key, f'0{width}b'),
                             'next_row_a': format(previous_target, f'0{width}b'),
                             'next_row_b': format(target, f'0{width}b')}
                    break
            else:
                seen[key] = (source, target)
        if found is not None:
            failures.append(found)
    return {'witness_found': bool(failures), 'failing_phases': len(failures),
            'projection_phases': now.shape[1], 'first_witness': failures[0] if failures else None}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--support-run', type=Path, required=True)
    ap.add_argument('--width', type=int, default=8)
    args = ap.parse_args()
    start = time.perf_counter()
    records = [json.loads(line) for line in (args.support_run/'candidates.jsonl').read_text().splitlines()]
    # Each 4D path includes its successful 2D and 3D parents. Match by full recipe.
    rows = []
    with (args.support_run/'whole_rows.jsonl').open('w') as log:
        for record in records:
            if record['dimension'] != 4:
                continue
            sequence = jets(record['rule'], args.width, 4)
            for depth, choice in enumerate(record['recipe'], 1):
                sequence = lift_pair_sequence(sequence, record['family'], choice)
                result = {'family': record['family'], 'rule': record['rule'],
                          'dimension': depth+1, 'recipe': record['recipe'][:depth],
                          'width': args.width, **witness(sequence, args.width)}
                rows.append(result)
                log.write(json.dumps(result, separators=(',', ':'))+'\n')
    summary = {}
    for family in ('pdm', 'copy_complement'):
        summary[family] = {}
        for d in (2, 3, 4):
            rr = [r for r in rows if r['family'] == family and r['dimension'] == d]
            codes = sorted({r['rule'] for r in rr})
            all_fail = [rule for rule in codes if all(r['witness_found'] for r in rr if r['rule'] == rule)]
            some_fail = [rule for rule in codes if any(r['witness_found'] for r in rr if r['rule'] == rule)]
            summary[family][str(d)] = {'candidate_count': len(rr),
                                      'candidates_with_witness': sum(r['witness_found'] for r in rr),
                                      'rules_with_witness_in_every_candidate': all_fail,
                                      'rules_with_witness_in_some_candidate': some_fail,
                                      'rules_without_any_witness': [r for r in codes if r not in some_fail]}
    output = {'width': args.width, 'elapsed_seconds': time.perf_counter()-start,
              'no_witness_does_not_prove_autonomy': True, 'summary': summary}
    (args.support_run/'whole_rows_summary.json').write_text(json.dumps(output, indent=2)+'\n')
    compact = {f: {d: {k: len(v) if isinstance(v, list) else v for k, v in s.items()}
                   for d, s in ds.items()} for f, ds in summary.items()}
    print(json.dumps({'elapsed_seconds': output['elapsed_seconds'], 'summary': compact}))


if __name__ == '__main__':
    main()
