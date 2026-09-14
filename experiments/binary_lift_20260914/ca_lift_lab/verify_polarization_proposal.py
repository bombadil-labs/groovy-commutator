"""Independent ring-five verification and row-label diagnostic.

Uses direct periodic formulas, constructs first-order tables itself, and merges
all constraints simultaneously with bit masks. It does not use the Compiler
or the lift plugin. Ring five enumerates every relevant five-cell word.
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np


def d(x, rule):
    idx = 4*np.roll(x, 1, axis=-1)+2*x+np.roll(x, -1, axis=-1)
    return (((rule ^ 204) >> idx) & 1).astype(np.uint8)


def encode(x, rule, choice):
    delta = d(x, rule)
    p = x ^ np.roll(x, -choice['shift'], axis=-1)
    mask = choice['mask']
    if mask == 'birth': m = (1-x) & delta
    elif mask == 'death': m = x & delta
    elif mask == 'stay_one': m = x & (1-delta)
    elif mask == 'stay_zero': m = (1-x) & (1-delta)
    else: raise ValueError(mask)
    return np.stack([p, delta, m], axis=-2)


def cubes(x):
    result = np.zeros_like(x, dtype=np.uint16)
    for dy in (0, 1, -1):
        for dx in (-1, 0, 1):
            result = 2*result+np.roll(x, (-dy, -dx), axis=(-2, -1))
    return result


def impose(base, keys, targets, zero_bit=None):
    required = base.copy()
    if zero_bit is not None:
        required[0] |= 1 << zero_bit
        targets = targets ^ zero_bit
    np.bitwise_or.at(required, keys.ravel(), (1 << targets.ravel()).astype(np.uint8))
    return not np.any(required == 3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', type=Path, required=True)
    args = ap.parse_args()
    start = time.perf_counter()
    source = ((np.arange(32)[:, None] >> np.arange(4, -1, -1)) & 1).astype(np.uint8)
    source7 = ((np.arange(128)[:, None] >> np.arange(6, -1, -1)) & 1).astype(np.uint8)
    records = [json.loads(x) for x in (args.run/'candidates.jsonl').read_text().splitlines()]
    tagged_records = []
    orbit_records = []
    direct_g_comparisons = 0
    for rec in records:
        rule = rec['rule']; choice = rec['recipe'][0]
        delta = d(source, rule)
        encoded = encode(source, rule, choice)
        flip = encoded ^ encode(source ^ delta, rule, choice)
        keys = cubes(encoded)
        base = np.zeros(512, dtype=np.uint8)
        np.bitwise_or.at(base, keys.ravel(), (1 << flip.ravel()).astype(np.uint8))
        assert not np.any(base == 3)
        assert np.count_nonzero(base) == rec['observed_first_order_cubes']
        pair_keys = keys[:, None, :2] ^ keys[None, :, :2]
        summed_source = source[:, None] ^ source[None, :]
        b = delta[:, None] ^ delta[None, :] ^ d(summed_source, rule)
        carrier = np.stack([b ^ np.roll(b, -choice['shift'], axis=-1), b], axis=-2)
        target = flip[:, None, :2] ^ flip[None, :, :2] ^ carrier
        raw_pass = impose(base, pair_keys, target)
        centered_target = target.copy()
        centered_target[..., 1, :] ^= rule & 1
        centered_pass = any(impose(base, pair_keys, centered_target, z) for z in (0, 1))
        assert raw_pass == rec['uncentered']['passes'], rec['candidate']
        assert centered_pass == rec['centered_pass'], rec['candidate']
        # Relax only row identity: distinct tables and zero bits per P/D phase.
        raw_tagged = True; centered_tagged = True
        for phase in (0, 1):
            phase_base = np.zeros(512, dtype=np.uint8)
            np.bitwise_or.at(phase_base, keys[:, phase].ravel(), (1 << flip[:, phase].ravel()).astype(np.uint8))
            raw_tagged &= impose(phase_base, pair_keys[:, :, phase], target[:, :, phase])
            centered_tagged &= any(impose(phase_base, pair_keys[:, :, phase], centered_target[:, :, phase], z) for z in (0, 1))
        tagged_records.append({'candidate': rec['candidate'], 'rule': rule,
                               'uncentered_tagged': bool(raw_tagged), 'centered_tagged': bool(centered_tagged)})
        dx = d(source7, rule); ex = source7 ^ dx
        lx = encode(source7, rule, choice); le = encode(ex, rule, choice)
        lee = encode(ex ^ d(ex, rule), rule, choice)
        lifted_delta = lx ^ le
        d_after_step = le ^ lee
        gs = d(ex, rule) ^ dx ^ d(dx, rule)
        transport_g = np.stack([gs ^ np.roll(gs, -choice['shift'], axis=-1), gs], axis=-2)
        orbit_target = transport_g ^ d_after_step[:, :2] ^ lifted_delta[:, :2]
        orbit_keys = cubes(lifted_delta)[:, :2]
        orbit_pass = impose(base, orbit_keys, orbit_target)
        orbit_target0 = orbit_target.copy(); orbit_target0[:, 1] ^= rule & 1
        orbit_centered_pass = any(impose(base, orbit_keys, orbit_target0, z) for z in (0, 1))
        assert orbit_pass == rec['groovy_orbit_uncentered']['passes']
        assert orbit_centered_pass == rec['groovy_orbit_centered_pass']
        unseen = base[cubes(lifted_delta)] == 0
        assert int(unseen.sum()) == rec['groovy_probe']['unseen_events']*7
        for mode, solutions in [('raw', [rec['groovy_orbit_uncentered']]),
                                ('centered', rec['groovy_orbit_centered_zero_branches'])]:
            for solution in solutions:
                if not solution['passes']: continue
                full = np.maximum(np.array(solution['flip_table'], dtype=np.int8), 0)
                dh = full[cubes(lx)]
                step = lx ^ dh
                assert np.array_equal(step, le)
                # Direct evaluation of G = Derive(Step(X)) XOR Step(Derive(X)).
                gh = full[cubes(step)] ^ dh ^ full[cubes(dh)]
                desired = transport_g.copy()
                if mode == 'centered':
                    gh ^= full[0]
                    desired[:, 1] ^= rule & 1
                assert np.array_equal(gh[:, :2], desired)
                direct_g_comparisons += int(desired.size)
        orbit_records.append({'candidate': rec['candidate'], 'rule': rule,
                              'source_G_nonzero': bool(gs.any()),
                              'source_G_nonconstant': bool(gs.any() and not gs.all()),
                              'source_G_zero_corrected_nonzero': bool((gs ^ (rule & 1)).any()),
                              'raw_pass': bool(orbit_pass), 'centered_pass': bool(orbit_centered_pass)})
    result = {'status': 'passed', 'candidates_independently_verified': len(records),
              'pair_events_per_candidate': 32*32*5*2,
              'pair_events_total': len(records)*32*32*5*2,
              'uncentered_tagged_codes': sorted({r['rule'] for r in tagged_records if r['uncentered_tagged']}),
              'centered_tagged_codes': sorted({r['rule'] for r in tagged_records if r['centered_tagged']}),
              'groovy_orbit_raw_nonzero_codes': sorted({r['rule'] for r in orbit_records if r['raw_pass'] and r['source_G_nonzero']}),
              'groovy_orbit_centered_nonzero_codes': sorted({r['rule'] for r in orbit_records if r['centered_pass'] and r['source_G_zero_corrected_nonzero']}),
              'direct_native_G_cell_comparisons': direct_g_comparisons,
              'elapsed_seconds': time.perf_counter()-start}
    (args.run/'verification.json').write_text(json.dumps(result, indent=2)+'\n')
    (args.run/'tagged_diagnostic.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in tagged_records))
    (args.run/'orbit_verification.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in orbit_records))
    print(json.dumps(result))


if __name__ == '__main__':
    main()
