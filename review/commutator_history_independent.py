#!/usr/bin/env python3
"""Independent review of the fixed direct commutator-history experiment.

This file does not import the experimental implementation. G is reconstructed
from local root-rule truth tables, and losses from independently counted joint
context/target histograms. Publication scope is recorded by the audit report.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / 'experiments/commutator_history_20260915'
PREVIOUS = ROOT / 'experiments/beam_discriminator_loop_20260915'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text())


def binary_word(number, length):
    return [(number >> (length - i - 1)) & 1 for i in range(length)]


def eca_bit(rule, left, center, right):
    return (rule >> (4 * left + 2 * center + right)) & 1


def scalar_g(rule, word):
    after = [eca_bit(rule, *word[i:i + 3]) for i in range(3)]
    twice = eca_bit(rule, *after)
    change = [word[i + 1] ^ after[i] for i in range(3)]
    return after[1] ^ twice ^ eca_bit(rule, *change)


def all_eca_g_tables():
    tables = np.array([[scalar_g(rule, binary_word(word, 5))
                        for word in range(32)] for rule in range(256)], np.uint8)
    zero = np.flatnonzero(np.all(tables == 0, axis=1)).tolist()
    one = np.flatnonzero(np.all(tables == 1, axis=1)).tolist()
    assert zero == [0, 4, 60, 90, 102, 150, 170, 200, 204, 240]
    assert one == [15, 51, 85, 105, 153, 165, 195, 255]
    return tables, zero, one


def eca_g_from_native(native, rule, tables):
    state = native[:-2]
    offsets = np.arange(state.shape[1])
    key = np.zeros(state.shape, np.uint8)
    for delta in range(-2, 3):
        key = 2 * key + np.take(state, (offsets + delta) % state.shape[1], axis=1)
    return tables[rule][key]


def nonlinear_open_step(array, radius, correction):
    windows = np.lib.stride_tricks.sliding_window_view(array, 2 * radius + 1, axis=-1)
    output = windows[..., -1].copy()
    if correction:
        output ^= np.bitwise_and.reduce(windows[..., :-1], axis=-1)
    return output


def wider_g_from_native(native, radius, correction):
    # Direct composition on the initial configuration uses a shrinking causal
    # window, independently of the recorded native intermediate frames.
    state = native[:-2]
    once = nonlinear_open_step(state, radius, correction)
    twice = nonlinear_open_step(once, radius, correction)
    change = state[:, radius:-radius] ^ once
    evolve_change = nonlinear_open_step(change, radius, correction)
    return once[:, radius:-radius] ^ twice ^ evolve_change


def joint_counts(features, target, bits):
    keys = (features.astype(np.uint32).ravel() << 1) | target.ravel()
    return np.bincount(keys, minlength=2 ** (bits + 1)).reshape(-1, 2)


def kt_loss(train_joint, test_joint):
    totals = train_joint.sum(axis=1)
    probability = (train_joint[:, 1] + .5) / (totals + 1.)
    losses = -np.log2(np.column_stack((1 - probability, probability)))
    return float(np.sum(test_joint * losses) / test_joint.sum())


def independent_counts(field, start, stop, radius, velocity2, periodic):
    # Open fields were obtained by a 2r causal crop, while the author uses an
    # r crop plus recorded later native states. Margin 16r therefore addresses
    # exactly the same physical cells as their margin 17r.
    margin = 0 if periodic else 16 * radius
    positions = np.arange(margin, field.shape[1] - margin)
    times = np.arange(start, stop)
    def bits(lag, displacement):
        indices = positions + displacement
        if periodic:
            indices %= field.shape[1]
        assert indices.min() >= 0 and indices.max() < field.shape[1]
        return np.take(field[times + lag], indices, axis=1)
    present_bits = 2 * radius + 1
    context = np.zeros((len(times), len(positions)), np.uint16)
    for delta in range(-radius, radius + 1):
        context += bits(0, delta).astype(np.uint16) * (1 << (radius - delta))
    for index, lag in enumerate((4, 8, 16)):
        displacement = -velocity2 * lag // 2
        context += bits(-lag, displacement).astype(np.uint16) * (1 << (present_bits + index))
    target = bits(4, 2 * velocity2)
    counts = joint_counts(context, target, present_bits + 3)
    assert counts.sum() == (stop - start) * len(positions)
    return counts


def independent_losses(fit, test, present_bits):
    losses, unseen = [], []
    full_keys = np.arange(len(fit))
    for history_bits in range(4):
        width = 1 << (present_bits + history_bits)
        key = full_keys % width
        train = np.zeros((width, 2), np.int64)
        heldout = np.zeros((width, 2), np.int64)
        # Marginalization by explicit context-key projection, rather than the
        # author's tensor reshape, independently fixes the nested bit order.
        np.add.at(train, key, fit)
        np.add.at(heldout, key, test)
        losses.append(kt_loss(train, heldout))
        unseen.append(float(heldout[train.sum(axis=1) == 0].sum() / heldout.sum()))
    return losses, unseen


def assert_close(actual, expected):
    assert np.allclose(actual, expected, rtol=0, atol=2e-12), (actual, expected)


def symmetry_variant(rule, flip, reflect):
    bits = []
    for index in range(8):
        word = binary_word(index, 3)
        if reflect:
            word = word[::-1]
        if flip:
            word = [1 - b for b in word]
        bits.append(eca_bit(rule, *word) ^ int(flip))
    return sum(bit << index for index, bit in enumerate(bits))


def exhaustive_wider_algebra():
    checked = 0
    for radius in (1, 2, 3):
        words = [binary_word(number, 4 * radius + 1)
                 for number in range(1 << (4 * radius + 1))]
        for correction in (False, True):
            def cell(word):
                return word[-1] ^ int(correction and all(word[:-1]))
            values = []
            for word in words:
                after = [cell(word[i:i + 2 * radius + 1]) for i in range(2 * radius + 1)]
                changes = [word[i + radius] ^ after[i] for i in range(2 * radius + 1)]
                values.append(after[radius] ^ cell(after) ^ cell(changes))
            array = np.asarray(words, np.uint8)
            once = nonlinear_open_step(array, radius, correction)
            twice = nonlinear_open_step(once, radius, correction)
            change = array[:, radius:-radius] ^ once
            got = once[:, radius:-radius] ^ twice ^ nonlinear_open_step(change, radius, correction)
            assert np.array_equal(got[:, 0], values)
            checked += len(words)
    return checked


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--families', help='Comma-separated family identifiers; omit for all families.')
    args = parser.parse_args()
    start_time = time.perf_counter()
    result = read_json(UNIT / 'result.json')
    frozen = read_json(UNIT / 'freeze.json')
    for field in ('source_hashes', 'raw_input_hashes'):
        assert result[field] == frozen[field]
        for path, expected in result[field].items():
            assert sha(ROOT / path) == expected, path
    assert sha(UNIT / 'protocol.md') == 'ec9c742858fdef3db07879a84f16bcfacb9821e84a2655f3729f2d00fb8b0755'
    assert read_json(UNIT / 'protocol-freeze.json')['protocol_sha256'] == sha(UNIT / 'protocol.md')
    assert sha(UNIT / 'histories-and-counts.npz') == result['raw_output_sha256']
    assert (UNIT / 'histories-and-counts.npz').stat().st_size == result['raw_output_bytes']
    tables, zero, one = all_eca_g_tables()
    expected_constants = {str(rule): 0 for rule in zero} | {str(rule): 1 for rule in one}
    assert result['algebra_checks']['constant_G_rules'] == expected_constants
    assert result['algebra_checks']['eca_scalar_contexts'] == tables.size == 8192
    wider_cases = exhaustive_wider_algebra()
    assert wider_cases == result['algebra_checks']['wider_scalar_contexts'] == 17472
    base6 = read_json(PREVIOUS / 'round06/result.json')['rules']
    base10 = read_json(PREVIOUS / 'round10/result.json')['rules']
    selected_ids = set(args.families.split(',')) if args.families else None
    outputs, checked_histories = [], set()
    count_tables = 0
    with (np.load(PREVIOUS / 'round06/trajectories.npz') as eca_cache,
          np.load(PREVIOUS / 'round10/trajectories.npz') as wider_cache,
          np.load(UNIT / 'histories-and-counts.npz') as saved):
        for family in result['families']:
            name = family['id']
            if selected_ids is not None and name not in selected_ids:
                continue
            base_name = name.removesuffix('_shuffle')
            radius = family['radius']
            periodic = family['periodic']
            fields, densities = {}, {}
            if periodic:
                baseline = {row['seed']: row for row in base6 if row['rule'] == family['representative']}
                assert family['rule'] == symmetry_variant(family['representative'], family['flip'], family['reflect'])
                for seed in baseline:
                    state = np.unpackbits(eca_cache[f's{seed}_r{family["representative"]:03d}'], axis=1)[:, :2039]
                    if family['flip']:
                        state = 1 - state
                    if family['reflect']:
                        state = np.flip(state, axis=1)
                    g = eca_g_from_native(state, family['rule'], tables)
                    stored_name = f'{base_name}_G_s{seed}'
                    assert np.array_equal(np.packbits(g, axis=1), saved[stored_name]), stored_name
                    checked_histories.add(stored_name)
                    fields[seed] = g
                    densities[seed] = float(g.mean())
            else:
                baseline = {row['seed']: row for row in base10
                            if row['radius'] == radius and row['correction'] == family['correction']}
                for seed in baseline:
                    state = np.unpackbits(wider_cache[f'r{radius}_g{int(family["correction"])}_s{seed}'], axis=1)[:, :4093 + 16 * radius]
                    direct = wider_g_from_native(state, radius, family['correction'])
                    change = state[1:] ^ state[:-1]
                    full = change[1:, radius:-radius] ^ nonlinear_open_step(change[:-1], radius, family['correction'])
                    assert np.array_equal(direct, full[:, radius:-radius])
                    stored_name = f'{base_name}_G_s{seed}'
                    assert np.array_equal(np.packbits(full, axis=1), saved[stored_name]), stored_name
                    checked_histories.add(stored_name)
                    fields[seed] = direct
                    densities[seed] = float(full.mean())
            if family['shuffled']:
                fields = {seed: g[np.random.default_rng(seed + 9000000).permutation(g.shape[0])]
                          for seed, g in fields.items()}
            train_seed = 6041511 if periodic else 6041541
            assert family['fit_seed'] == train_seed
            assert train_seed not in {row['seed'] for row in family['tests']}
            velocities = [0, -radius, radius, -2 * radius, 2 * radius]
            assert [row['velocity2'] for row in family['choices']] == velocities
            fits, computed_gains = {}, []
            for velocity2, chosen_row in zip(velocities, family['choices']):
                fit = independent_counts(fields[train_seed], 16, 480, radius, velocity2, periodic)
                selection = independent_counts(fields[train_seed], 528, 1026, radius, velocity2, periodic)
                assert np.array_equal(fit, saved[f'{name}_fit_v{velocity2}'])
                assert np.array_equal(selection, saved[f'{name}_selection_v{velocity2}'])
                count_tables += 2
                losses, unseen = independent_losses(fit, selection, 2 * radius + 1)
                assert_close(losses, chosen_row['losses'])
                assert_close(unseen, chosen_row['unseen_fraction'])
                gain = losses[0] - losses[-1]
                assert_close(gain, chosen_row['gain'])
                computed_gains.append(gain)
                fits[velocity2] = fit
            chosen_index = int(np.argmax(computed_gains))
            velocity2 = velocities[chosen_index]
            # Different but equivalent floating summation orders can differ at
            # roundoff. A nontrivial choice discrepancy is never accepted.
            if velocity2 / 2 != family['chosen_velocity']:
                stored_index = velocities.index(int(2 * family['chosen_velocity']))
                assert abs(computed_gains[chosen_index] - computed_gains[stored_index]) < 2e-12
                velocity2 = velocities[stored_index]
            tests = []
            for row in family['tests']:
                seed = row['seed']
                table = independent_counts(fields[seed], 16, 1026, radius, velocity2, periodic)
                assert np.array_equal(table, saved[f'{name}_test_s{seed}'])
                count_tables += 1
                loss, unseen = independent_losses(fits[velocity2], table, 2 * radius + 1)
                assert_close(loss, row['losses'])
                assert_close(unseen, row['unseen_fraction'])
                gain = loss[0] - loss[-1]
                assert_close(gain, row['gain_bits'])
                assert_close([loss[i] - loss[i + 1] for i in range(3)], row['incremental_gains'])
                density = densities[seed]
                entropy = -density * np.log2(density) - (1 - density) * np.log2(1 - density) if 0 < density < 1 else 0.
                assert_close(density, row['G_density'])
                assert_close(entropy, row['G_marginal_entropy'])
                assert row['targets'] == int(table.sum())
                assert row['q'] == baseline[seed]['q'] and row['alpha'] == baseline[seed]['alpha']
                assert row['baseline_selected'] == baseline[seed]['selected']
                memory = gain > .01
                augmented = bool(baseline[seed]['selected'] and memory)
                assert memory == row['memory_selected'] and augmented == row['augmented_selected']
                tests.append({'seed': seed, 'gain_bits': gain, 'baseline_selected': row['baseline_selected'],
                              'augmented_selected': augmented})
            outputs.append({'id': name, 'chosen_velocity': velocity2 / 2, 'tests': tests})
            if len(outputs) % 10 == 0:
                print('independently audited families', len(outputs), flush=True)
    complete = selected_ids is None
    if complete:
        assert len(outputs) == 110 and len(checked_histories) == 380
        assert count_tables == 1406
        assert len(checked_histories) + count_tables == 1786
    report = {
        'reviewer': 'OpenAI GPT-6 Astra, independent collaborating session /root/beam_loop_review, 2026-09-15',
        'result_sha256': sha(UNIT / 'result.json'),
        'raw_output_sha256': result['raw_output_sha256'],
        'auditor_sha256': sha(__file__),
        'seconds': time.perf_counter() - start_time,
        'all_families_replayed': complete,
        'families': outputs,
        'G_histories_exactly_reproduced': len(checked_histories),
        'joint_count_tables_exactly_reproduced': count_tables,
        'all_requested_losses_coverage_gains_and_decisions_match': True,
        'scalar_eca_contexts': 8192,
        'scalar_wider_contexts': wider_cases,
        'scope': 'Finite observational prediction with the frozen current/history features; no causal-memory, convention-invariant or universal classifier conclusion.',
        'temporal_split': {'fit_maximum_native_frame': 485, 'selection_minimum_native_frame': 512,
                           'last_target_native_frame': 1031, 'training_seed_never_scored_as_test': True,
                           'note': 'Native-frame gap refers to the ordered observation; permutation is a separate temporal-organization control.'},
        'rule106_scope': 'The sole R6 baseline-positive seed 6041511 trains this unit; its three held-out seeds were already baseline-negative.'
    }
    target = ROOT / 'review/commutator_history_independent.json'
    target.write_text(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + '\n')
    print('independent audit complete', report['seconds'], flush=True)


if __name__ == '__main__':
    main()
