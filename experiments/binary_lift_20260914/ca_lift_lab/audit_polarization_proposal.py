"""First-lift preflight for Fable's P/F/free polarization carrier.

Checks both uncentered B_F(a,b)=F(a)+F(b)+F(a+b), and a separately
named centered B_F^0=B_F+F(0). This does not redefine the Groovy commutator.
All operations are XOR unless explicitly noted. Native unknowns are flip bits.
Five source cells cover both the sum-state cube and all prescribed P/D targets.
"""
import argparse
import hashlib
import json
import sqlite3
import time
from pathlib import Path

import numpy as np
from harness import Compiler, derive, load_operator, physical_observations
from inspect_run import table

WEIGHTS = 1 << np.arange(8, -1, -1, dtype=np.uint16)


def pack(patches):
    return patches @ WEIGHTS


def fit(base, keys, targets, mode, zero_bit=None):
    chosen = base.copy()
    origins = {i: {'kind': 'first_order', 'required': int(v)} for i, v in enumerate(base) if v >= 0}
    if zero_bit is not None:
        if chosen[0] >= 0 and chosen[0] != zero_bit:
            return {'passes': False, 'reason': 'zero_bit_conflicts_with_first_order'}
        chosen[0] = zero_bit
        origins[0] = {'kind': 'chosen_zero_bit', 'required': zero_bit}
    for a in range(32):
        for b in range(32):
            for phase in range(2):
                key = int(keys[a, b, phase])
                desired = int(targets[a, b, phase])
                if zero_bit is not None:
                    desired ^= zero_bit
                event = {'kind': mode, 'source_a': format(a, '05b'),
                         'source_b': format(b, '05b'), 'phase': 'P' if phase == 0 else 'D',
                         'required': desired}
                if chosen[key] >= 0 and chosen[key] != desired:
                    return {'passes': False, 'reason': 'local_output_conflict',
                            'cube': format(key, '09b'), 'existing': origins[key], 'new': event}
                if chosen[key] < 0:
                    chosen[key] = desired
                    origins[key] = event
    return {'passes': True, 'forced_bits': int(np.count_nonzero(chosen >= 0)),
            'free_bits': int(np.count_nonzero(chosen < 0)),
            'flip_table': chosen.tolist(), 'zero_bit': zero_bit}


def fit_orbits(base, keys, targets, zero_bit=None):
    chosen = base.copy()
    origins = {i: {'kind': 'first_order', 'required': int(v)} for i, v in enumerate(base) if v >= 0}
    if zero_bit is not None:
        if chosen[0] >= 0 and chosen[0] != zero_bit:
            return {'passes': False, 'reason': 'zero_bit_conflicts_with_first_order'}
        chosen[0] = zero_bit
        origins[0] = {'kind': 'chosen_zero_bit', 'required': zero_bit}
    for word in range(128):
        for phase in (0, 1):
            key = int(keys[word, phase]); wanted = int(targets[word, phase])
            if zero_bit is not None: wanted ^= zero_bit
            event = {'kind': 'orbit_pair', 'source': format(word, '07b'),
                     'phase': 'P' if phase == 0 else 'D', 'required': wanted}
            if chosen[key] >= 0 and chosen[key] != wanted:
                return {'passes': False, 'reason': 'local_output_conflict',
                        'cube': format(key, '09b'), 'existing': origins[key], 'new': event}
            if chosen[key] < 0:
                chosen[key] = wanted; origins[key] = event
    return {'passes': True, 'forced_bits': int(np.count_nonzero(chosen >= 0)),
            'free_bits': int(np.count_nonzero(chosen < 0)),
            'flip_table': chosen.tolist(), 'zero_bit': zero_bit}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    root = Path(__file__).resolve().parent
    db = sqlite3.connect(root/'runs/fixed_transverse_to_4/constraints.sqlite3')
    op = load_operator(root/'lifts/fixed_transverse.py')
    started = time.perf_counter()
    records = []
    with (args.output/'candidates.jsonl').open('w') as log:
        for cid, rule, raw in db.execute('SELECT id,rule,record_json FROM candidates WHERE dimension=2 AND strict_pass=1 ORDER BY rule,id'):
            rec = json.loads(raw); path = rec['recipe']
            compiler = Compiler(rule, 1, op)
            encoded = compiler.encode(path)
            neighborhoods = physical_observations(encoded)
            pair_keys = pack(neighborhoods[:, None, :2, :] ^ neighborhoods[None, :, :2, :])
            native_flip = compiler.mask(path)[..., 0]
            known_pair_flip = native_flip[:, None, :2] ^ native_flip[None, :, :2]
            source_sum = compiler.source[:, None, :] ^ compiler.source[None, :, :]
            sum_step = source_sum[..., 1:-1] ^ derive(source_sum, rule)
            source_b = compiler.jets[1][:, None, :] ^ compiler.jets[1][None, :, :] ^ sum_step
            side = 0 if path[0]['shift'] == -1 else 2
            transported = np.stack([source_b[..., 1] ^ source_b[..., side], source_b[..., 1]], axis=-1)
            raw_targets = known_pair_flip ^ transported
            centered_targets = raw_targets.copy()
            centered_targets[..., 1] ^= rule & 1  # P annihilates a constant field.
            keys, masks, _, names = table(db, cid)
            bits = np.unpackbits(keys, axis=1, bitorder='big')[:, :9]
            base = np.full(512, -1, dtype=np.int8)
            base[pack(bits)] = masks[:, names.index('derivative')]-1
            raw_fit = fit(base, pair_keys, raw_targets, 'uncentered')
            centered = [fit(base, pair_keys, centered_targets, 'centered', z) for z in (0, 1)]
            # Does the actual Groovy input A XOR H(A) reach unspecified cubes?
            wider = Compiler(rule, 2, op)
            groovy_inputs = physical_observations(wider.mask(path))
            groovy_keys = pack(groovy_inputs)
            unseen = base[groovy_keys] < 0
            source_delta = wider.source_masks[0]
            source_g = wider.source_masks[1] ^ (source_delta[..., 1:-1] ^ derive(source_delta, rule))
            g_carrier = np.stack([source_g[..., 1] ^ source_g[..., side], source_g[..., 1]], axis=-1)
            first_center = wider.encode(path)[..., 2]
            twice_center = wider.encode(path, 2)[..., 0]
            orbit_target = first_center[:, :2] ^ twice_center[:, :2] ^ g_carrier
            orbit_raw = fit_orbits(base, groovy_keys[:, :2], orbit_target)
            orbit_centered_target = orbit_target.copy()
            orbit_centered_target[:, 1] ^= rule & 1
            orbit_centered = [fit_orbits(base, groovy_keys[:, :2], orbit_centered_target, z) for z in (0, 1)]
            result = {'candidate': cid, 'rule': rule, 'recipe': path,
                      'source_width_for_pair_constraints': 5,
                      'observed_first_order_cubes': int(np.count_nonzero(base >= 0)),
                      'zero_pair_obstruction': bool(rule & 1),
                      'uncentered': raw_fit, 'centered_zero_branches': centered,
                      'centered_pass': any(x['passes'] for x in centered),
                      'groovy_orbit_uncentered': orbit_raw,
                      'groovy_orbit_centered_zero_branches': orbit_centered,
                      'groovy_orbit_centered_pass': any(x['passes'] for x in orbit_centered),
                      'groovy_probe': {'source_width': 7, 'events': int(unseen.size),
                                       'unseen_events': int(unseen.sum()),
                                       'distinct_unseen_cubes': int(len(np.unique(groovy_keys[unseen]))),
                                       'some_extension_dependence': bool(unseen.any())},
                      'first_order_table_sha256': rec['unmarked']['table_sha256']}
            records.append(result)
            log.write(json.dumps(result, separators=(',', ':'))+'\n')
    codes = sorted({r['rule'] for r in records})
    summary = {'source_codes_with_first_lift': len(codes), 'variants': len(records),
               'odd_codes_obstructed_by_equal_pair': [r for r in codes if r & 1],
               'uncentered_pass_codes': sorted({r['rule'] for r in records if r['uncentered']['passes']}),
               'uncentered_pass_variants': sum(r['uncentered']['passes'] for r in records),
               'centered_pass_codes': sorted({r['rule'] for r in records if r['centered_pass']}),
               'centered_pass_variants': sum(r['centered_pass'] for r in records),
               'groovy_orbit_uncentered_pass_codes': sorted({r['rule'] for r in records if r['groovy_orbit_uncentered']['passes']}),
               'groovy_orbit_uncentered_pass_variants': sum(r['groovy_orbit_uncentered']['passes'] for r in records),
               'groovy_orbit_centered_pass_codes': sorted({r['rule'] for r in records if r['groovy_orbit_centered_pass']}),
               'groovy_orbit_centered_pass_variants': sum(r['groovy_orbit_centered_pass'] for r in records),
               'groovy_extension_dependent_codes_any_variant': [rule for rule in codes if any(r['groovy_probe']['some_extension_dependence'] for r in records if r['rule'] == rule)],
               'groovy_extension_dependent_codes_every_variant': [rule for rule in codes if all(r['groovy_probe']['some_extension_dependence'] for r in records if r['rule'] == rule)],
               'elapsed_seconds': time.perf_counter()-started,
               'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (args.output/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    (args.output/'source_audit.py').write_text(Path(__file__).read_text())
    print(json.dumps({k:(len(v) if isinstance(v, list) and 'codes' not in k else v) for k,v in summary.items() if 'groovy_extension' not in k}))
    print(json.dumps({k:len(v) for k,v in summary.items() if 'groovy_extension' in k}))


if __name__ == '__main__':
    main()
