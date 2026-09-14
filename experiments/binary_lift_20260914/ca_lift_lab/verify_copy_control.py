"""Check every stored native constraint against the explicit majority formulas.

This verifier does not compile source histories or call the lift plugin. It
reads physical neighborhoods from the census and evaluates the closed-form
decoder and primitive derivative, including every unlabeled transverse phase.
"""
import argparse
import json
import sqlite3
from pathlib import Path

import numpy as np
from inspect_run import table


def verify(run):
    db = sqlite3.connect(run / 'constraints.sqlite3')
    counts = {'candidates': 0, 'distinct_native_patches': 0,
              'target_checks': 0, 'represented_events': 0}
    stages = {}
    for cid, rule, dimension, record_json in db.execute(
            'SELECT id,rule,dimension,record_json FROM candidates ORDER BY id'):
        record = json.loads(record_json)
        assert record['all_four_pass'] and not record['constant_layers']
        keys, masks, frequencies, names = table(db, cid)
        patches = np.unpackbits(keys, axis=1, bitorder='big')[:, :3**dimension]
        patches = patches.reshape((-1,) + (3,) * dimension)
        # First axis is the newest transverse axis. A radius-one interval
        # contains the whole period-three code in any cyclic phase.
        parent_patch = (patches.sum(axis=1) >= 2).astype(np.uint8)
        parent_center = parent_patch[(slice(None),) + (0,) * (dimension-2) + (1,)]
        source_patch = parent_patch
        for _ in range(dimension-2):
            source_patch = (source_patch.sum(axis=1) >= 2).astype(np.uint8)
        index = 4*source_patch[:, 0] + 2*source_patch[:, 1] + source_patch[:, 2]
        flip = ((rule ^ 204) >> index) & 1
        expected = {'derivative': flip, 'source': source_patch[:, 1],
                    'parent': parent_center, 'parent_derivative': flip}
        for col, name in enumerate(names):
            assert np.array_equal(masks[:, col], 1 << expected[name]), (cid, name)
        counts['candidates'] += 1
        counts['distinct_native_patches'] += len(keys)
        counts['target_checks'] += len(keys)*len(names)
        counts['represented_events'] += int(frequencies.sum())
        stages.setdefault(str(dimension), set()).add(rule)
    assert counts['candidates'] == 768
    assert all(len(stages[str(d)]) == 256 for d in (2, 3, 4))
    counts['passing_rules_by_dimension'] = {d: len(rules) for d, rules in stages.items()}
    counts['status'] = 'passed'
    return counts


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', required=True, type=Path)
    args = parser.parse_args()
    result = verify(args.run)
    (args.run / 'majority_verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))
