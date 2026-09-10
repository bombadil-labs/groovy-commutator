#!/usr/bin/env python3
"""Replay all frozen radius-one witnesses as full 3-by-4 periodic fields."""
import hashlib
import json
from pathlib import Path

import verify_guard_free_axial_lift as axial

ROOT = Path(__file__).resolve().parents[1]
CENSUS = ROOT / 'results/transverse_difference_closure_20260910.json'


def difference(field):
    return sum((int(field[x, y]) ^ int(field[x, (y+1) % 4])) << (x+3*y)
               for y in range(4) for x in range(3))


def independent_difference(field):
    bits = ['1' if field[x, y] != field[x, (y+1) % 4] else '0'
            for y in range(4) for x in range(3)]
    return int(''.join(bits)[::-1], 2)


def audit():
    raw = CENSUS.read_bytes()
    data = json.loads(raw)
    records = []
    cells = 0
    hashes = [hashlib.sha256(), hashlib.sha256()]
    for row in data['rules']:
        budget = next(b for b in row['local_budgets'] if b['radius'] == 1)
        if budget['passes']:
            continue
        rule = row['rule']
        witness = budget['first_conflict']
        a, b = witness['source_words']
        mask = (a ^ b) & 7
        assert (a ^ b) == sum(mask << (3*y) for y in range(4))
        truth = axial.boolean_truth(rule)
        observed, following = [], []
        for word in (a, b):
            field = {(x, y): (word >> (x+3*y)) & 1 for y in range(4) for x in range(3)}
            text = format(word, '012b')[::-1]
            reference = {(x, y): text[x+3*y] == '1' for y in range(4) for x in range(3)}
            after = axial.lattice_passes(rule, field, (3, 4))
            ref_after = {point: axial.local_tree(truth, reference, (3, 4), point, 2)
                         for point in reference}
            assert after == ref_after
            current, future = difference(field), difference(after)
            ref_current, ref_future = independent_difference(reference), independent_difference(ref_after)
            assert (current, future) == (ref_current, ref_future)
            for checksum, values in zip(hashes, ((current, future), (ref_current, ref_future))):
                checksum.update(b''.join(value.to_bytes(2, 'little') for value in values))
            assert (current & 511) == witness['observed_word']
            observed.append(current)
            following.append(future)
            cells += len(field)
        assert observed[0] == observed[1]
        assert following[0] != following[1]
        center = [(word >> 4) & 1 for word in following]
        assert center == witness['next_transverse_bits']
        assert center[0] != center[1]
        records.append({'rule': rule, 'source_words': [a, b], 'column_baseline_mask': mask,
                        'observed_periodic_word': observed[0], 'next_transverse_words': following,
                        'center_next_transverse_bits': center})
    assert len(records) == len(data['source_rules'])-len(data['radius_one_rules'])
    assert hashes[0].digest() == hashes[1].digest()
    return {'census_sha256': hashlib.sha256(raw).hexdigest(),
            'census_protocol_commit': data['protocol_commit'],
            'supplement_protocol': 'docs/research/protocols/transverse-witness-extension-20260910.md',
            'word_convention': 'bit x+3*y on periodic x=0..2,y=0..3; central observed site is (1,1)',
            'full_field_obstruction_rules': [r['rule'] for r in records],
            'counts': {'witness_pairs': len(records), 'periodic_macro_updates': 2*len(records),
                       'compared_output_cells': cells},
            'checksum_convention': 'failed source rules ascending, first then second source; current T,next T uint16LE',
            'primary_sha256': hashes[0].hexdigest(), 'independent_sha256': hashes[1].hexdigest(),
            'certificates': records}


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2, sort_keys=True))
