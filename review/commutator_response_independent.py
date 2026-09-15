#!/usr/bin/env python3
"""Independent scalar census and complete four-arm response replay.

Uses only the earlier independent auditor's local algebra helpers, never the
experimental implementation. All four arms evolve in one separate batch.
"""
from pathlib import Path
import hashlib
import json
import time
import numpy as np
from commutator_history_independent import binary_word, eca_bit, nonlinear_open_step, all_eca_g_tables

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / 'experiments/commutator_history_20260915'
OLD = ROOT / 'experiments/beam_discriminator_loop_20260915'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text())


def scalar_evolve(word, radius, rule, correction):
    def cell(w):
        if rule is not None:
            return eca_bit(rule, *w)
        return w[-1] ^ int(correction and all(w[:-1]))
    return [cell(word[i:i + 2 * radius + 1]) for i in range(len(word) - 2 * radius)]


def scalar_census(radius, rule=None, correction=True):
    interacting, witness = 0, None
    for number in range(1 << (6 * radius + 1)):
        word = binary_word(number, 6 * radius + 1)
        primed = word.copy()
        primed[3 * radius] ^= 1
        a = scalar_evolve(word, radius, rule, correction)
        b = scalar_evolve(primed, radius, rule, correction)
        a_pulse, b_pulse = a.copy(), b.copy()
        a_pulse[2 * radius] ^= 1
        b_pulse[2 * radius] ^= 1
        ends = [scalar_evolve(w, radius, rule, correction) for w in (a, b, a_pulse, b_pulse)]
        r0 = [x ^ y for x, y in zip(ends[0], ends[2])]
        r1 = [x ^ y for x, y in zip(ends[1], ends[3])]
        interaction = [x ^ y for x, y in zip(r0, r1)]
        if any(interaction):
            interacting += 1
            if witness is None:
                witness = {'word': word, 'response_unprimed': r0, 'response_primed': r1,
                           'interaction': interaction}
    return {'radius': radius, 'rule': rule, 'correction': correction,
            'contexts': 1 << (6 * radius + 1), 'interacting_contexts': interacting, 'witness': witness}


def advance(worlds, radius, rule, correction):
    if rule is None:
        return nonlinear_open_step(worlds, radius, correction)
    words = np.lib.stride_tricks.sliding_window_view(worlds, 3, axis=-1)
    indices = np.sum(words * np.array([4, 2, 1], np.uint8), axis=-1)
    return ((rule >> indices) & 1).astype(np.uint8)


def local_g(worlds, at, radius, rule, correction, g_tables):
    neighborhoods = np.take(worlds, at[:, None] + np.arange(-2 * radius, 2 * radius + 1), axis=-1)
    if rule is not None:
        keys = np.sum(neighborhoods * (1 << np.arange(4, -1, -1)), axis=-1)
        return g_tables[rule][keys]
    once = nonlinear_open_step(neighborhoods, radius, correction)
    twice = nonlinear_open_step(once, radius, correction)
    delta = neighborhoods[..., radius:-radius] ^ once
    return (once[..., radius:-radius] ^ twice ^ nonlinear_open_step(delta, radius, correction))[..., 0]


def replay(initial, radius, delay, rule, correction, g_tables):
    horizon = 32
    remote = radius * (delay + 64) + 1
    offsets = np.array([-radius * delay, 0, radius * delay, remote])
    padding = 2 * radius * (delay + horizon) + remote
    if rule is not None:
        origins = np.linspace(0, len(initial) - 1, 16).astype(int)
    else:
        origins = np.linspace(padding, len(initial) - padding - 1, 16).astype(int)
    positions = origins[:, None] + np.arange(-padding, padding + 1)
    if rule is not None:
        positions %= len(initial)
    assert positions.min() >= 0 and positions.max() < len(initial)
    unprimed = initial[positions].copy()
    primed = unprimed.copy()
    primed[:, padding] ^= 1
    worlds = np.stack((unprimed, primed))
    history_times = np.arange(max(0, delay - 17), delay - 1)
    histories = []
    for tick in range(delay):
        if tick in history_times:
            # Direct radius-2r algebra on the current state independently
            # reconstructs G without the author's three-frame bookkeeping.
            at = padding - radius * tick + offsets
            histories.append(local_g(worlds, at, radius, rule, correction, g_tables))
        worlds = advance(worlds, radius, rule, correction)
    center = padding - radius * delay
    coordinates = np.arange(worlds.shape[-1]) - center
    assert not np.any((worlds[0] ^ worlds[1])[:, abs(coordinates) > radius * delay])
    gone = np.repeat(np.all(worlds[0] == worlds[1], axis=1), 4)
    repeated = np.repeat(worlds, 4, axis=1)
    probes = np.tile(center + offsets, 16)
    neighborhoods = probes[:, None] + np.arange(-2 * radius, 2 * radius + 1)
    local_same = np.all(repeated[0, np.arange(64)[:, None], neighborhoods] ==
                        repeated[1, np.arange(64)[:, None], neighborhoods], axis=1)
    history = np.stack(histories, axis=-1).reshape(2, 64, len(history_times))
    history_changed = np.any(history[0] != history[1], axis=1)
    pulsed = repeated.copy()
    pulsed[:, np.arange(64), probes] ^= 1
    arms = np.concatenate((repeated, pulsed), axis=0)
    assert not np.any(arms[0] ^ arms[1] ^ arms[2] ^ arms[3])
    measurements = []
    for h in range(1, horizon + 1):
        arms = advance(arms, radius, rule, correction)
        if h not in (1, 8, 32):
            continue
        responses = arms[2:] ^ arms[:2]
        interaction = responses[0] ^ responses[1]
        count = interaction.sum(axis=1)
        union = np.maximum(responses[0], responses[1]).sum(axis=1)
        ratio = np.zeros(64)
        ratio[union > 0] = count[union > 0] / union[union > 0]
        measurements.append(np.column_stack((count, responses[0].sum(axis=1), responses[1].sum(axis=1), union, ratio)))
        # Full retained outputs include the complete response cone. Everything
        # beyond that cone is independently checked to be zero.
        now_center = padding - radius * (delay + h)
        positions = np.arange(arms.shape[-1]) - now_center
        response_cone = abs(positions[None, :] - np.tile(offsets, 16)[:, None]) <= radius * h
        assert not np.any(responses[:, ~response_cone])
        assert np.all(count[3::4] == 0)
        assert np.all(count[gone] == 0)
        if h == 1:
            assert np.all(count[local_same] == 0)
        if rule in (0, 90, 150, 204) or (rule is None and not correction):
            assert not np.any(count)
    return {'origins': origins, 'offsets': offsets, 'history_times': history_times,
            'local_same': local_same, 'priming_gone': gone, 'history_base': history[0],
            'history_primed': history[1], 'history_changed': history_changed,
            'measurements': np.stack(measurements)}, padding


def main():
    started = time.perf_counter()
    result = read_json(UNIT / 'response-result.json')
    freeze = read_json(UNIT / 'response-freeze.json')
    for name in ('source_hashes', 'raw_input_hashes'):
        assert result[name] == freeze[name]
        for path, expected in result[name].items():
            assert sha(ROOT / path) == expected
    assert sha(UNIT / 'response-protocol.md') == '9025b545e8d60e9009d93dfe39063b6a8bcc2d8df6459f44b1459a3459fe146a'
    assert sha(UNIT / 'response-arrays.npz') == result['raw_sha256']
    assert (UNIT / 'response-arrays.npz').stat().st_size == result['raw_bytes']
    census = [scalar_census(1, rule) for rule in range(256)]
    assert census == result['short_census']
    wider_census = scalar_census(2)
    assert wider_census == result['wider_short_census']
    zero_set = [row['rule'] for row in census if not row['interacting_contexts']]
    center_separable = [rule for rule in range(256) if len({eca_bit(rule, left, 0, right) ^ eca_bit(rule, left, 1, right)
                        for left in (0, 1) for right in (0, 1)}) == 1]
    assert zero_set == center_separable and len(zero_set) == 32
    tables, zero_g, _ = all_eca_g_tables()
    assert 4 in zero_g and census[4]['interacting_contexts'] == 56
    checked_arrays, summaries = 0, []
    with (np.load(OLD / 'round06/trajectories.npz') as eca,
          np.load(OLD / 'round10/trajectories.npz') as wider,
          np.load(UNIT / 'response-arrays.npz') as saved):
        for case in result['cases']:
            radius, delay, seed = case['radius'], case['delay'], case['seed']
            rule = case.get('rule')
            correction = case.get('correction', True)
            if rule is not None:
                initial = np.unpackbits(eca[f's{seed}_r{rule:03d}'][0])[:2039]
            else:
                initial = np.unpackbits(wider[f'r{radius}_g{int(correction)}_s{seed}'][0])[:4093 + 16 * radius]
            computed, padding = replay(initial, radius, delay, rule, correction, tables)
            assert padding == case['half_padding']
            for key, value in computed.items():
                assert np.array_equal(value, saved[f'{case["id"]}_{key}']), (case['id'], key)
                checked_arrays += 1
            assert computed['history_times'].tolist() == case['history_times']
            local = np.arange(64) % 4 != 3
            assert int(computed['priming_gone'][local].sum()) == case['priming_gone_trials']
            for index, outcome in enumerate(case['outcomes']):
                assert outcome['horizon'] == (1, 8, 32)[index]
                measurement = computed['measurements'][index]
                changed = measurement[:, 0] > 0
                assert int(changed[local].sum()) == outcome['changed_local_responses']
                assert outcome['local_trials'] == 48 and outcome['remote_trials'] == 16 and outcome['remote_changed'] == 0
                assert float(measurement[local, 0].mean()) == outcome['mean_interaction_cells']
                assert float(measurement[local, 4].mean()) == outcome['mean_interaction_union_ratio']
                for stratum in outcome['strata']:
                    selected = local & (computed['local_same'] == stratum['local_same']) & (computed['history_changed'] == stratum['G_history_changed'])
                    assert int(selected.sum()) == stratum['trials'] and int(changed[selected].sum()) == stratum['changed']
            summaries.append({'id': case['id'], 'h32_changed_local': int(np.sum(computed['measurements'][-1, local, 0] > 0))})
    assert len(summaries) == 84 and checked_arrays == 756
    report = {'reviewer': 'OpenAI GPT-6 Astra, independent collaborating session /root/beam_loop_review, 2026-09-15',
              'result_sha256': sha(UNIT / 'response-result.json'), 'raw_sha256': result['raw_sha256'],
              'auditor_sha256': sha(__file__), 'audit_helper_sha256': sha(ROOT / 'review/commutator_history_independent.py'),
              'seconds': time.perf_counter() - started, 'all_cases_replayed': True, 'cases': summaries,
              'exact_census_contexts': 256 * 128 + 8192, 'arrays_exactly_reproduced': checked_arrays,
              'delayed_four_arm_trials': 84 * 64, 'horizon_measurements': 84 * 64 * 3,
              'all_G_histories_local_match_erasure_affine_remote_checks_pass': True,
              'short_zero_rules': zero_set, 'short_zero_set_equals_center_separable_rules': True,
              'rule4_G_identically_zero_but_short_modulation_contexts': 56,
              'scope': 'Finite response modulation is generic nonlinear state dependence; no Class IV specificity, causal G feedback, learning or irreducible history outside the full state is established.'}
    (ROOT / 'review/commutator_response_independent.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print('independent response audit complete', report['seconds'], 'seconds', flush=True)


if __name__ == '__main__':
    main()
