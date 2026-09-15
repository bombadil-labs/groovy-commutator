#!/usr/bin/env python3
"""Independent audit of the adaptive beam-discriminator loop.

No author experiment or cache implementation is imported. Round 1 uses shrinking
open windows instead of the author's periodic evolution. Round 2 reconstructs
physical patches directly from immutable input grids and independently counts
intersections of partial maps, never default-completed rules.
"""
import argparse
import base64
import hashlib
import itertools
import json
from functools import lru_cache
from pathlib import Path
import tarfile
import time
import zipfile

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / 'experiments/beam_discriminator_loop_20260915'
ARCHIVE = ROOT.parent / 'gc-pilot/experiments/uniform_jet6_cache_20260914/run/uniform_jet6_rules.tar.gz'
ARCHIVE_SHA = '766e4db7083fbdb551bc4aee66abc554079c5d118905f6d65aa5e5372c9418d1'


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text())


def bits(s, shape):
    return np.unpackbits(np.frombuffer(base64.b64decode(s), np.uint8), bitorder='big')[:np.prod(shape)].reshape(shape)


def provenance(round_no):
    directory = UNIT / f'round{round_no:02d}'
    result = read_json(directory / 'result.json')
    freeze = read_json(directory / 'freeze.json')
    assert result['source_hashes'] == freeze
    for path, digest in freeze.items():
        assert sha(ROOT / path) == digest, path
    if 'table_sha256' in result:
        assert sha(directory / 'tables.npz') == result['table_sha256']
    return result


def crop_step(x, rule):
    # Exterior cells are discarded; no periodic boundary is introduced.
    neighborhood = (x[:, :-2] << 2) | (x[:, 1:-1] << 1) | x[:, 2:]
    return ((rule >> neighborhood.astype(np.uint16)) & 1).astype(np.uint8)


def independent_first_floor(rule):
    x = ((np.arange(512, dtype=np.uint16)[:, None] >> np.arange(9)) & 1).astype(np.uint8)
    y = crop_step(x, rule)       # Source positions 1..7.
    z = crop_step(y, rule)       # Source positions 2..6.
    t = crop_step(z, rule)       # Source positions 3..5.
    source = x[:, 2:7]
    change = source ^ y[:, 1:6]
    g = np.stack((source ^ x[:, 3:8], source ^ x[:, 1:6], change,
                  source ^ z, source & change, source & (1 - change)), axis=1)
    current = y[:, 3]
    delta = current ^ z[:, 2]
    target = np.stack((current ^ y[:, 4], current ^ y[:, 2], delta,
                       current ^ t[:, 1], current & delta,
                       current & (1 - delta)), axis=1)
    assert np.all((g[:, 4] ^ g[:, 5]) == source)
    assert not np.any(g[:, 4] & g[:, 5])
    native = {}
    decoder = {}
    for phase in range(6):
        patch = g[:, [(phase + dy) % 6 for dy in range(-3, 4)], :]
        keys = (patch.reshape(512, 35).astype(np.uint64) << np.arange(34, -1, -1, dtype=np.uint64)).sum(axis=1)
        flips = g[:, phase, 2] ^ target[:, phase]
        for key, flip, decoded in zip(keys.tolist(), flips.tolist(), x[:, 4].tolist()):
            native[key] = native.get(key, 0) | (1 << flip)
            decoder[key] = decoder.get(key, 0) | (1 << decoded)
    return native, decoder


def round01():
    result = provenance(1)
    stored = np.load(UNIT / 'round01/tables.npz')
    full = []
    for rule in range(256):
        native, decoder = independent_first_floor(rule)
        expected_native = dict(zip(stored[f'r{rule:03d}_keys'].tolist(), stored[f'r{rule:03d}_native'].tolist()))
        expected_decoder = dict(zip(stored[f'r{rule:03d}_keys'].tolist(), stored[f'r{rule:03d}_decoder'].tolist()))
        assert native == expected_native
        assert decoder == expected_decoder
        assert all(value in (1, 2) for value in native.values())
        assert all(value in (1, 2) for value in decoder.values())
        recorded = result['roots'][rule]
        assert recorded['rule'] == rule and recorded['forced'] == len(native)
        assert recorded['native'] == {'conflicts': 0, 'first_witness': None}
        assert recorded['decoder'] == {'conflicts': 0, 'first_witness': None}
        # For period-six patches, final five-bit row duplicates the first.
        assert all((q & 31) == (q >> 30) for q in native)
        full.append({((q >> 5) << 2).to_bytes(4, 'big'): v - 1 for q, v in native.items()})
    assert result['native_failed'] == result['decoder_failed'] == []
    return {
        'roots': 256, 'source_words_per_root': 512, 'phases': 6,
        'all_native_and_decoder_tables_equal': True,
        'independent_method': 'shrinking open-window evolution; all local keys and both targets regenerated',
        'full_line_argument': 'key radius at most 4, next-center target radius at most 3; all nine-cell words and all six transverse phases exhaust the union of dependencies',
        'scope': 'first lift of all binary radius-one ECAs under the declared six-field encoding; no arbitrary-parent or all-dimensional theorem',
        'result_sha256': sha(UNIT / 'round01/result.json'),
    }, full


def physical_keys(record):
    g = bits(record['grid_bits_big'], record['grid_shape'])
    indices = np.frombuffer(base64.b64decode(record['representative_flat_indices_u32le']), '<u4')
    c = np.array(np.unravel_index(indices, g.shape)).T
    dimension = record['dimension']
    assert record['radii_array_order'] == [3] * (dimension - 1) + [2]
    assert g.shape[1:-1] == (6,) * (dimension - 1)
    offsets = list(itertools.product(*([range(-3, 3)] * (dimension - 1) + [range(-2, 3)])))
    patch = np.stack([g[tuple([c[:, 0]] + [(c[:, axis + 1] + offset[axis]) % g.shape[axis + 1]
                                         for axis in range(dimension)])] for offset in offsets], axis=1)
    packed = np.packbits(patch, bitorder='big', axis=1)
    values = bits(record['forced_derivative_bits_big'], (len(indices),))
    assert len(set(map(bytes, packed))) == len(indices) == record['forced_root_count']
    # Exact scalar full-neighborhood checks: reconstruct the omitted +3
    # aliases from the retained -3 slices along every lifted axis.
    full_offsets = list(itertools.product(*([range(-3, 4)] * (dimension - 1) + [range(-2, 3)])))
    offset_index = {offset: i for i, offset in enumerate(offsets)}
    scalar_checked = 0
    for at in sorted({0, len(indices) // 2, len(indices) - 1}):
        coordinate = c[at]
        for offset in full_offsets:
            folded = tuple((-3 if x == 3 and i < dimension - 1 else x) for i, x in enumerate(offset))
            actual = int(g[tuple([coordinate[0]] + [(coordinate[i + 1] + offset[i]) % g.shape[i + 1]
                                                  for i in range(dimension)])])
            assert actual == int(patch[at, offset_index[folded]])
            scalar_checked += 1
    return packed, values, scalar_checked


def transformed_orbit(rule):
    outputs = [(rule >> i) & 1 for i in range(8)]
    mirror = sum(outputs[int(f'{i:03b}'[::-1], 2)] << i for i in range(8))
    conjugate = sum((1 - outputs[7 - i]) << i for i in range(8))
    mirror_conjugate = sum((1 - outputs[7 - int(f'{i:03b}'[::-1], 2)]) << i for i in range(8))
    return sorted({rule, mirror, conjugate, mirror_conjugate})


def count_pairs(tables):
    supports = [set(table) for table in tables]
    result = []
    for a in range(256):
        for b in range(a + 1, 256):
            common = supports[a].intersection(supports[b])
            same_zero = same_one = disagreement = 0
            for key in common:
                first, second = tables[a][key], tables[b][key]
                if first != second:
                    disagreement += 1
                elif first:
                    same_one += 1
                else:
                    same_zero += 1
            result.append((a, b, same_zero, same_one, disagreement))
    return np.array(result, dtype=np.uint32)


def check_summaries(matrix, tables, expected, labels):
    degree = np.zeros(256, int)
    occupied = np.zeros(256, int)
    samples = [[] for _ in range(256)]
    edge = np.eye(256, dtype=bool)
    compatible = vacant = nonempty = 0
    for a, b, zero, one, conflicts in matrix.tolist():
        shared = zero + one + conflicts
        if shared:
            samples[a].append(conflicts / shared)
            samples[b].append(conflicts / shared)
        if conflicts == 0:
            compatible += 1
            edge[a, b] = edge[b, a] = True
            degree[a] += 1
            degree[b] += 1
            if shared:
                occupied[a] += 1
                occupied[b] += 1
                nonempty += 1
            else:
                vacant += 1
    assert expected['compatible'] == compatible
    assert expected['occupied'] == nonempty
    assert expected['vacuous'] == vacant
    features = []
    for rule in range(256):
        features.append({'degree': int(degree[rule]), 'occupied_degree': int(occupied[rule]),
                         'mean_conflict_fraction': float(np.mean(samples[rule])) if samples[rule] else None})
        stored = expected['per_rule'][rule]
        assert stored['rule'] == rule and stored['forced'] == len(tables[rule])
        assert stored['occupied_comparisons'] == len(samples[rule])
        for key, value in features[-1].items():
            assert np.isclose(stored[key], value, atol=2e-15, rtol=0), (rule, key)
    for key, rows in expected['symmetry_spreads'].items():
        for row in rows:
            orbit = transformed_orbit(row['root'])
            assert orbit == row['members'] and min(orbit) == row['root']
            values = [features[member][key] for member in orbit]
            assert np.isclose(row['range'], max(values) - min(values), atol=2e-15, rtol=0)
    for label, means in expected['classes_core'].items():
        population = [r for r in labels['representatives'][label] if r not in (41, 106)]
        for key, average in means.items():
            assert np.isclose(average, np.mean([features[r][key] for r in population]), atol=2e-15, rtol=0)
    return edge


def round02(full):
    result = provenance(2)
    assert sha(ARCHIVE) == ARCHIVE_SHA
    labels = read_json(ROOT / 'experiments/on_beam_256_4d_20260914/labels.json')
    recorded = np.load(UNIT / 'round02/tables.npz')
    tables = {name: [None] * 256 for name in ('d2w7', 'd2w8', 'd3w7', 'd3w8')}
    checked_members = scalar_checked = entries = 0
    with tarfile.open(ARCHIVE, 'r|gz') as tf:
        for member in tf:
            if member.name not in result['archive_member_hashes']:
                continue
            raw = tf.extractfile(member).read()
            assert hashlib.sha256(raw).hexdigest() == result['archive_member_hashes'][member.name]
            record = json.loads(raw)
            name = f'd{record["dimension"]}w{record["width"]}'
            rule = record['rule']
            keys, values, checks = physical_keys(record)
            assert np.array_equal(recorded[f'{name}_r{rule:03d}_keys'], keys)
            assert np.array_equal(recorded[f'{name}_r{rule:03d}_values'], values)
            tables[name][rule] = dict(zip(map(bytes, keys), values.tolist()))
            if record['dimension'] == 2:
                assert all(full[rule].get(k) == v for k, v in tables[name][rule].items())
            scalar_checked += checks
            entries += len(values)
            checked_members += 1
    assert checked_members == len(result['archive_member_hashes']) == 1024
    tables['d2full'] = full
    edges = {}
    domains = {}
    for name, partial_maps in tables.items():
        independent = count_pairs(partial_maps)
        assert np.array_equal(independent, np.load(UNIT / f'round02/{name}_pairs.npz')['rows'])
        edges[name] = check_summaries(independent, partial_maps, result['domains'][name], labels)
        domains[name] = {key: result['domains'][name][key] for key in ('compatible', 'occupied', 'vacuous')}
        print('audited', name, domains[name], flush=True)
    upper = np.triu(np.ones((256, 256), bool), 1)
    for width in (7, 8):
        lower, higher = edges[f'd2w{width}'], edges[f'd3w{width}']
        changes = {'lost': int(np.sum(upper & lower & ~higher)),
                   'gained': int(np.sum(upper & ~lower & higher)),
                   'shared': int(np.sum(upper & lower & higher))}
        assert changes == result['cross_floor_changes'][str(width)]
        assert not np.any(edges['d2full'] & ~lower)
    return {
        'archive_members': checked_members, 'reconstructed_forced_entries': entries,
        'scalar_full_patch_bits_checked': scalar_checked, 'pair_rows_recomputed': 5 * 32640,
        'all_physical_keys_targets_and_summaries_equal': True,
        'domains': domains, 'cross_floor_changes': result['cross_floor_changes'],
        'interpretation': 'saturation and symmetry sensitivity defeat these literal-table graph proxies; they neither disprove a beam invariant nor establish all-input D3 validity',
        'result_sha256': sha(UNIT / 'round02/result.json'),
    }


def round03():
    result = provenance(3)
    assert sha(ARCHIVE) == ARCHIVE_SHA
    directory = UNIT / 'round03'
    recovery = result.get('recovery')
    if recovery:
        assert recovery == read_json(directory / 'recovery-freeze.json')
        assert sha(ROOT / 'scripts/beam_loop_round03_recover.py') == recovery['repair_script_sha256']
        assert len(recovery['bad_files']) == 31
        assert all(row['prior_bytes'] == 0 for row in recovery['bad_files'].values())
    expected_pairs = {}
    needed = {}
    for width in (7, 8):
        previous = np.load(UNIT / f'round02/d3w{width}_pairs.npz')['rows']
        expected_pairs[width] = {(int(a), int(b)): int(c) for a, b, z, o, c in previous if c}
        needed[width] = {r for pair in expected_pairs[width] for r in pair}
    expected_names = {f'w{w}_r{r:03d}.npz' for w in needed for r in needed[w]}
    assert set(result['tables']) == expected_names
    for name, row in result['tables'].items():
        assert sha(directory / name) == row['sha256']
        stored = np.load(directory / name)
        assert len(stored['values']) == row['keys']
        assert len(set(map(bytes, stored['keys']))) == row['keys']
    # R2 exhaustively validated the dimension-parametric physical extractor.
    # Reconstruct complete D4 tables for core/control roots and deterministic
    # boundary records; additionally check every archived member's raw hash.
    sampled_names = {f'w{w}_r{r:03d}.npz' for w in needed
                     for r in (needed[w] & {0, 1, 30, 54, 90, 110, 122, 126, 204}) | {min(needed[w]), max(needed[w])}}
    if recovery:
        sampled_names.update(recovery['bad_files'])
    by_record = {row['record']: name for name, row in result['tables'].items()}
    reconstructed = scalar_checks = members = 0
    with tarfile.open(ARCHIVE, 'r|gz') as tf:
        for member in tf:
            if member.name not in by_record:
                continue
            raw = tf.extractfile(member).read()
            name = by_record[member.name]
            assert hashlib.sha256(raw).hexdigest() == result['tables'][name]['record_sha256']
            members += 1
            if name in sampled_names:
                record = json.loads(raw)
                k, v, checked = physical_keys(record)
                stored = np.load(directory / name)
                assert np.array_equal(stored['keys'], k)
                assert np.array_equal(stored['values'], v)
                reconstructed += len(v)
                scalar_checks += checked
    assert members == len(result['tables'])

    @lru_cache(maxsize=4)
    def table(width, rule):
        saved = np.load(directory / f'w{width}_r{rule:03d}.npz')
        return dict(zip(map(bytes, saved['keys']), saved['values'].tolist()))

    domains = {}
    for width in (7, 8):
        expected = result['domains'][str(width)]
        assert expected['tested_pairs'] == len(expected_pairs[width])
        assert {(row['a'], row['b']) for row in expected['pairs']} == set(expected_pairs[width])
        remaining = 0
        for row in expected['pairs']:
            a, b = row['a'], row['b']
            assert row['previous_conflicts'] == expected_pairs[width][a, b]
            first, second = table(width, a), table(width, b)
            common = first.keys() & second.keys()
            disagree = sorted(q for q in common if first[q] != second[q])
            same0 = sum(first[q] == second[q] == 0 for q in common)
            same1 = sum(first[q] == second[q] == 1 for q in common)
            assert row['shared_zero'] == same0 and row['shared_one'] == same1
            assert row['conflicts'] == len(disagree)
            if disagree:
                remaining += 1
                q = base64.b64decode(row['witness']['physical_1080_bits_base64'])
                assert q == disagree[0]
                assert row['witness']['a'] == first[q] and row['witness']['b'] == second[q]
            else:
                assert row['witness'] is None
        assert expected['persistent_pairs'] == remaining
        domains[str(width)] = {'tested_pairs': len(expected_pairs[width]), 'persistent_pairs': remaining}
    return {'all_selected_pair_counts_and_witnesses_equal': True, 'domains': domains,
            'archive_members_hashed': members, 'complete_d4_tables_reconstructed': sorted(sampled_names),
            'reconstructed_forced_entries': reconstructed, 'scalar_full_patch_bits_checked': scalar_checks,
            'recovery': {'frozen_original_source_hashes_unchanged': True,
                         'repaired_tables_independently_reconstructed': len(recovery['bad_files'])} if recovery else None,
            'scope': 'D3-conflicting pairs only; no complete D4 graph, no all-input D4 claim',
            'result_sha256': sha(directory / 'result.json')}


def periodic_step(row, rule):
    left = np.concatenate((row[..., -1:], row[..., :-1]), axis=-1)
    right = np.concatenate((row[..., 1:], row[..., :1]), axis=-1)
    key = (left << 2) | (row << 1) | right
    truth = np.array([(rule >> k) & 1 for k in range(8)], np.uint8)
    return truth[key]


def independently_replay_trajectory(rule, seed, width, burn, frames, density=.5):
    state = (np.random.Generator(np.random.PCG64(seed)).random(width) < density).astype(np.uint8)
    for _ in range(burn):
        state = periodic_step(state, rule)
    observed = np.empty((frames, width), np.uint8)
    for i in range(frames):
        observed[i] = state
        state = periodic_step(state, rule)
    return observed


def independent_residual(a, period, velocity, frames):
    positions = (np.arange(a.shape[1]) + velocity) % a.shape[1]
    return a[:frames] != a[period:period + frames, positions]


def independent_residual_statistics(residual):
    frames, width = residual.shape
    density = np.count_nonzero(residual) / residual.size
    variance = density * (1 - density)
    covariance, correlation = {}, {}
    for lag in (1, 4, 16):
        adjacent = residual[:, (np.arange(width) + lag) % width]
        moment = np.count_nonzero(residual & adjacent) / residual.size
        covariance[str(lag)] = moment - density * density
        correlation[str(lag)] = covariance[str(lag)] / variance if variance else 0.
    count = total = maximum = 0
    # Counts of runs are obtained from starts; max run is checked directly
    # in a streaming scan, with no wraparound across row boundaries.
    for row in residual:
        current = 0
        for bit in row:
            if not bit:
                current += 1
            elif current:
                total += current
                count += 1
                maximum = max(maximum, current)
                current = 0
        if current:
            total += current
            count += 1
            maximum = max(maximum, current)
    return {'density': density, 'covariance': covariance, 'correlation': correlation,
            'zero_run_mean': total / count if count else 0., 'zero_run_max': maximum}


def round04():
    result = provenance(4)
    directory = UNIT / 'round04'
    assert sha(directory / 'trajectories.npz') == result['trajectory_sha256']
    stored = np.load(directory / 'trajectories.npz')
    labels = read_json(ROOT / 'experiments/on_beam_256_4d_20260914/labels.json')
    rules = sorted(r for population in labels['representatives'].values() for r in population)
    assert [row['rule'] for row in result['rules']] == rules and len(rules) == 88
    candidates = sorted([(period, velocity) for period in range(1, 9)
                         for velocity in range(-period, period + 1)], key=lambda pair: (pair[0], abs(pair[1]), pair[1]))
    assert list(map(list, candidates)) == result['candidates']
    checked_values = 0
    for row in result['rules']:
        rule = row['rule']
        expected = np.unpackbits(stored[f'r{rule:03d}'], bitorder='big', axis=1)[:, :result['width']]
        independently_generated = independently_replay_trajectory(rule, result['seed'], result['width'], result['burn'], result['frames'])
        assert np.array_equal(independently_generated, expected)
        checked_values += expected.size
        rates = [float(independent_residual(expected, p, v, 512).mean()) for p, v in candidates]
        assert rates == row['candidate_rates']
        best = min(range(len(rates)), key=lambda i: rates[i])
        assert candidates[best] == (row['p'], row['v'])
        stats = independent_residual_statistics(independent_residual(expected, row['p'], row['v'], 512))
        for name, value in stats.items():
            if isinstance(value, dict):
                for key, number in value.items():
                    assert np.isclose(number, row[name][key], atol=1e-15, rtol=0)
            else:
                assert np.isclose(value, row[name], atol=1e-15, rtol=0)
        activity = np.count_nonzero(expected[1:] != expected[:-1]) / expected[1:].size
        assert activity == row['raw_activity']
    return {'complete_native_trajectories_reproduced': 88, 'saved_cells_checked': checked_values,
            'all_candidate_rates_selection_and_statistics_equal': True,
            'finite_ring_caveat': 'At width512, Rule90 is nilpotent by time256; burn512 guarantees all-zero output. This does not describe its generic infinite-line chaotic behavior.',
            'scope': 'one seed and one power-of-two ring; exploratory recurrence residual, not an established invariant or classifier',
            'result_sha256': sha(directory / 'result.json')}


def independent_damage(rule, state, trials=16, horizon=256):
    width = len(state)
    center = width // 2
    assert center - horizon >= 0 and center + horizon < width
    positions = np.linspace(0, width - 1, trials, dtype=int)
    translated = state[(np.arange(width)[None, :] - center + positions[:, None]) % width]
    ensemble = np.concatenate((translated, translated), axis=0)
    ensemble[trials:, center] ^= 1
    aggregate = []
    for time_index in range(horizon + 1):
        differences = ensemble[:trials] != ensemble[trials:]
        mass = np.count_nonzero(differences, axis=1)
        alive = mass > 0
        diameters = [int(indices[-1] - indices[0] + 1) if len(indices) else 0
                     for indices in map(np.flatnonzero, differences)]
        aggregate.append((np.count_nonzero(alive) / trials, mass.sum() / trials, sum(diameters) / trials))
        if time_index < horizon:
            ensemble = periodic_step(ensemble, rule)
    return np.array(aggregate)


def round05():
    result = provenance(5)
    directory = UNIT / 'round05'
    assert sha(directory / 'trajectories.npz') == result['raw_sha256']
    old = read_json(UNIT / 'round04/result.json')
    old_rows = {row['rule']: row for row in old['rules']}
    candidates = [tuple(pair) for pair in old['candidates']]
    stored = np.load(directory / 'trajectories.npz')
    expected_design = {(r, w, s) for r in old_rows for w in (509, 1021) for s in (6041502, 6041503, 6041504)}
    assert {(row['rule'], row['width'], row['seed']) for row in result['rules']} == expected_design
    assert len(result['rules']) == len(expected_design) == 528
    cells = damages = 0
    for row in result['rules']:
        rule, width, seed = row['rule'], row['width'], row['seed']
        name = f'w{width}_s{seed}_r{rule:03d}'
        trajectory = np.unpackbits(stored[name], bitorder='big', axis=1)[:, :width]
        regenerated = independently_replay_trajectory(rule, seed, width, 1024, 520)
        assert np.array_equal(trajectory, regenerated)
        cells += trajectory.size
        rates = [float(independent_residual(trajectory, p, v, 512).mean()) for p, v in candidates]
        best = min(range(len(rates)), key=lambda i: rates[i])
        assert candidates[best] == (row['p'], row['v'])
        stats = independent_residual_statistics(independent_residual(trajectory, row['p'], row['v'], 512))
        for name_, value in stats.items():
            if isinstance(value, dict):
                for key, number in value.items():
                    assert np.isclose(number, row[name_][key], atol=1e-15, rtol=0)
            else:
                assert np.isclose(value, row[name_], atol=1e-15, rtol=0)
        fraction = np.count_nonzero(trajectory) / trajectory.size
        assert fraction == row['one_density']
        normalization = stats['density'] / (2 * fraction * (1 - fraction)) if 0 < fraction < 1 else 0.
        assert normalization == row['normalized_density']
        previous = old_rows[rule]
        assert float(independent_residual(trajectory, previous['p'], previous['v'], 512).mean()) == row['old_pair_density']
        if width == 1021:
            damage = independent_damage(rule, trajectory[0])
            assert np.array_equal(damage, stored[name + '_damage'])
            growth = float(np.log2(damage[256, 2] / damage[128, 2])) if damage[256, 2] > 0 and damage[128, 2] > 0 else 0.
            assert growth == row['damage']['growth_128_256']
            for tick in (16, 32, 64, 128, 256):
                expected = row['damage']['checkpoints'][str(tick)]
                assert (expected['survival'], expected['hamming'], expected['diameter']) == tuple(damage[tick])
            damages += 1
    return {'complete_native_trajectories_reproduced': 528, 'saved_cells_checked': cells,
            'complete_damage_ensembles_reproduced': damages, 'damage_trials_per_ensemble': 16,
            'all_selection_residual_statistics_normalizations_and_damage_summaries_equal': True,
            'lightcone_check': 'center510 +/-256 stays inside width1021, so no perturbation wrap alias in recorded support diameter',
            'scope': 'fresh prime-width finite-horizon diagnostics; does not establish asymptotic disturbance growth or an intrinsic Class-IV definition',
            'result_sha256': sha(directory / 'result.json')}


def round06():
    result = provenance(6)
    directory = UNIT / 'round06'
    assert sha(directory / 'trajectories.npz') == result['raw_sha256']
    original = read_json(UNIT / 'round04/result.json')
    root_rules = {row['rule'] for row in original['rules']}
    candidates = [tuple(pair) for pair in original['candidates']]
    design = {(rule, seed) for rule in root_rules for seed in range(6041511, 6041515)}
    assert len(result['rules']) == len(design) == 352
    assert {(row['rule'], row['seed']) for row in result['rules']} == design
    stored = np.load(directory / 'trajectories.npz')
    hits = {str(rule): 0 for rule in sorted(root_rules)}
    cells = 0
    for row_number, row in enumerate(result['rules']):
        rule, seed = row['rule'], row['seed']
        assert (row['width'], row['burn'], row['frames'], row['initial_density']) == (2039, 2048, 1024, .5)
        name = f's{seed}_r{rule:03d}'
        a = np.unpackbits(stored[name], bitorder='big', axis=1)[:, :2039]
        regenerated = independently_replay_trajectory(rule, seed, 2039, 2048, 1032)
        assert np.array_equal(a, regenerated)
        cells += a.size
        rates = [float(independent_residual(a, period, velocity, 1024).mean()) for period, velocity in candidates]
        best = min(range(len(rates)), key=lambda index: rates[index])
        assert candidates[best] == (row['p'], row['v'])
        assert rates[best] == row['mismatch']
        fraction = np.count_nonzero(a) / a.size
        assert fraction == row['one_density']
        q = rates[best] / (2 * fraction * (1 - fraction)) if 0 < fraction < 1 else 0.
        assert q == row['q']
        curve = independent_damage(rule, a[0], trials=32, horizon=512)
        assert np.array_equal(curve, stored[name + '_damage'])
        assert row['final_damage'] == curve[-1].tolist()
        alpha = float(np.log2(curve[512, 2] / curve[256, 2])) if curve[512, 2] > 0 and curve[256, 2] > 0 else 0.
        assert alpha == row['alpha']
        decision = bool(0 < q < .5 and alpha > .5)
        assert decision == row['selected']
        hits[str(rule)] += decision
        if (row_number + 1) % 88 == 0:
            print('round06 independent runs', row_number + 1, flush=True)
    assert hits == result['hit_counts']
    selected = [int(rule) for rule, count in hits.items() if count >= 3]
    assert selected == result['majority_selected']
    return {'complete_native_trajectories_reproduced': 352, 'saved_cells_checked': cells,
            'complete_damage_ensembles_reproduced': 352, 'damage_trials_per_ensemble': 32,
            'all_candidate_selections_normalizations_growth_decisions_and_majorities_equal': True,
            'majority_selected': selected,
            'scope': 'held-out larger finite rings for a predictor selected post hoc in R5; only two independent positive symmetry families',
            'result_sha256': sha(directory / 'result.json')}


def independent_lift_series(series):
    current, following, two_later = series[:-2], series[1:-1], series[2:]
    width = current.shape[-1]
    ahead = np.take(current, (np.arange(width) + 1) % width, axis=-1)
    behind = np.take(current, (np.arange(width) - 1) % width, axis=-1)
    if current.ndim > 2:
        phase = (np.arange(current.shape[1]) + 1) % current.shape[1]
        ahead = np.take(ahead, phase, axis=1)
        behind = np.take(behind, phase, axis=1)
    difference = current != following
    return np.stack((current != ahead, current != behind, difference,
                     current != two_later, current & difference,
                     current & ~difference), axis=1).astype(np.uint8)


def macro_support(first, second):
    return np.any((first != second).reshape(-1, first.shape[-1]), axis=0)


def round07():
    result = provenance(7)
    previous = {row['rule']: row for row in read_json(UNIT / 'round04/result.json')['rules']}
    expected = {(row['rule'], row['t'], row['kind'], row['dimension']): row for row in result['rows']}
    assert len(expected) == len(result['rows']) == 504
    assert result['all_support_checks']
    actual_rows = 0
    source_cells = 0
    for rule in (0, 18, 54, 73, 110, 126, 204):
        baseline = independently_replay_trajectory(rule, 6041521, 521, 512, 148)
        perturbed = np.empty_like(baseline)
        perturbed[0] = baseline[0]
        perturbed[0, 260] ^= 1
        for tick in range(1, len(baseline)):
            perturbed[tick] = periodic_step(perturbed[tick - 1], rule)
        source_cells += baseline.size + perturbed.size
        period, velocity = previous[rule]['p'], previous[rule]['v']
        for tick in (0, 1, 8, 32, 64, 128):
            for kind in ('perturbation', 'recurrence'):
                first = baseline[tick:tick + 11]
                if kind == 'perturbation':
                    second = perturbed[tick:tick + 11]
                else:
                    positions = (np.arange(521) + velocity) % 521
                    second = baseline[tick + period:tick + period + 11, positions]
                source = macro_support(first[0], second[0])
                for dimension in range(1, 7):
                    if dimension > 1:
                        old_first, old_second = first[0], second[0]
                        first, second = independent_lift_series(first), independent_lift_series(second)
                        assert np.array_equal(first[0, 4] ^ first[0, 5], old_first)
                        assert np.array_equal(second[0, 4] ^ second[0, 5], old_second)
                    decoded_first, decoded_second = first[0], second[0]
                    for _ in range(dimension - 1):
                        decoded_first = decoded_first[4] ^ decoded_first[5]
                        decoded_second = decoded_second[4] ^ decoded_second[5]
                    assert np.array_equal(decoded_first ^ decoded_second, source.astype(np.uint8))
                    support = macro_support(first[0], second[0])
                    radius = 2 * (dimension - 1)
                    dilation = np.any(source[(np.arange(521)[None, :] + np.arange(-radius, radius + 1)[:, None]) % 521], axis=0)
                    assert not np.any(source & ~support)
                    assert not np.any(support & ~dilation)
                    row = expected[rule, tick, kind, dimension]
                    assert row['radius_bound'] == radius
                    assert row['source_count'] == np.count_nonzero(source)
                    assert row['macrocolumn_count'] == np.count_nonzero(support)
                    assert row['physical_mismatch'] == np.count_nonzero(first[0] != second[0]) / first[0].size
                    assert row['support_checks']
                    if kind == 'perturbation':
                        locations, initial = np.flatnonzero(support), np.flatnonzero(source)
                        diameter = int(locations[-1] - locations[0] + 1) if len(locations) else 0
                        left = int(initial[0] - locations[0]) if len(initial) else 0
                        right = int(locations[-1] - initial[-1]) if len(initial) else 0
                        assert (row['diameter'], row['left_extra'], row['right_extra']) == (diameter, left, right)
                        assert 0 <= left <= radius and 0 <= right <= radius
                    else:
                        assert (row['p'], row['v']) == (period, velocity)
                    actual_rows += 1
    return {'support_and_decoder_cases_reproduced': actual_rows, 'root_trajectory_cells_reproduced': source_cells,
            'all_macrocolumn_counts_physical_densities_and_extrema_equal': True,
            'support_proof': 'locality radius grows by at most2 per floor; same-column decoder gives A subset B, locality gives B subset A thickened by2(d-1)',
            'tail_proof': 'stationarity and support inclusion sandwich empty-interval probabilities between source lengths L and L+2R; exponential rate is unchanged if the limit exists',
            'scope': 'ancestral encoding and same-column decoding throughD6; native phase-free D6 rule validity not established; fixed dimension required for asymptotic transport',
            'result_sha256': sha(UNIT / 'round07/result.json')}


def round08():
    result = provenance(8)
    directory = UNIT / 'round08'
    assert sha(directory / 'trajectories.npz') == result['raw_sha256']
    original = read_json(UNIT / 'round04/result.json')
    roots = {row['rule'] for row in original['rules']}
    candidates = [tuple(pair) for pair in original['candidates']]
    expected_design = {(r, d, s) for r in roots for d in (.1, .3, .7, .9) for s in (6041531, 6041532)}
    assert {(r['rule'], r['initial_density'], r['seed']) for r in result['rules']} == expected_design
    assert len(result['rules']) == len(expected_design) == 704
    stored = np.load(directory / 'trajectories.npz')
    hits = {str(rule): 0 for rule in sorted(roots)}
    replayed = []
    cells = 0
    controls = {9, 18, 54, 73, 110, 126, 204}
    for number, row in enumerate(result['rules']):
        r, density, seed = row['rule'], row['initial_density'], row['seed']
        assert (row['width'], row['burn'], row['frames']) == (2039, 2048, 1024)
        name = f'd{int(density * 10)}_s{seed}_r{r:03d}'
        a = np.unpackbits(stored[name], bitorder='big', axis=1)[:, :2039]
        regenerated = independently_replay_trajectory(r, seed, 2039, 2048, 1032, density)
        assert np.array_equal(a, regenerated)
        cells += a.size
        rates = [float(independent_residual(a, p, v, 1024).mean()) for p, v in candidates]
        best = min(range(len(rates)), key=lambda i: rates[i])
        assert candidates[best] == (row['p'], row['v'])
        assert rates[best] == row['mismatch']
        fraction = float(a.mean())
        assert fraction == row['one_density']
        q = rates[best] / (2 * fraction * (1 - fraction)) if 0 < fraction < 1 else 0.
        assert q == row['q']
        curve = stored[name + '_damage']
        assert curve.shape == (513, 3) and np.all(np.isfinite(curve))
        assert np.array_equal(curve[0], [1, 1, 1])
        assert np.all((curve[:, 0] >= 0) & (curve[:, 0] <= 1))
        assert np.all(np.diff(curve[:, 0]) <= 0)
        assert np.all(curve[:, 1] >= curve[:, 0])
        assert np.all(curve[:, 2] >= curve[:, 1])
        assert np.all(curve[:, 2] <= curve[:, 0] * (2 * np.arange(513) + 1))
        assert np.array_equal(curve * 32, np.rint(curve * 32))
        assert row['final_damage'] == curve[-1].tolist()
        alpha = float(np.log2(curve[512, 2] / curve[256, 2])) if curve[512, 2] > 0 and curve[256, 2] > 0 else 0.
        assert alpha == row['alpha']
        selected = bool(0 < q < .5 and alpha > .5)
        assert selected == row['selected']
        hits[str(r)] += selected
        if selected or r in controls:
            reproduced_curve = independent_damage(r, a[0], 32, 512)
            assert np.array_equal(reproduced_curve, curve)
            replayed.append(name)
        if (number + 1) % 176 == 0:
            print('round08 independent runs', number + 1, flush=True)
    assert hits == result['hit_counts']
    selected = [int(rule) for rule, count in hits.items() if count >= 5]
    assert selected == result['majority_selected']
    exceptions = [{'rule': row['rule'], 'density': row['initial_density'], 'seed': row['seed'], 'selected': row['selected']}
                  for row in result['rules'] if (row['rule'] in (54, 110)) != row['selected']]
    return {'complete_native_trajectories_reproduced': 704, 'saved_cells_checked': cells,
            'all_candidate_choices_decisions_and_majorities_equal': True,
            'all_damage_summaries_and_structural_bounds_checked': 704,
            'complete_damage_curves_independently_replayed': replayed,
            'damage_replay_scope': 'every selected run and every run of roots9,18,54,73,110,126,204; unchanged damage implementation already fully verified in R6',
            'majority_selected': selected, 'per_run_exceptions_to_core_labels': exceptions,
            'scope': 'four Bernoulli input-density ensembles at one width/horizon; finite diagnostics do not imply all-state classification',
            'result_sha256': sha(directory / 'result.json')}


def independent_interval_counts(residual, lengths):
    width = residual.shape[1]
    assert min(lengths) >= 1 and max(lengths) <= width
    histogram = np.zeros(width, dtype=np.int64)
    empty_rows = 0
    for row in residual:
        occupied = np.flatnonzero(row)
        if len(occupied) == 0:
            empty_rows += 1
            continue
        gaps = np.diff(np.r_[occupied, occupied[0] + width]) - 1
        counts = np.bincount(gaps)
        histogram[:len(counts)] += counts
    result = {}
    for length in sorted(set(lengths)):
        run_lengths = np.arange(length, width)
        count = empty_rows * width + np.dot(histogram[length:], run_lengths - length + 1)
        result[str(length)] = {'count': int(count), 'total': int(residual.size)}
    return result


def verify_tail_summary(residual, row):
    lengths = [1, 2, 4, 8, 16, 32, 64, 128, 256]
    counts = independent_interval_counts(residual, lengths)
    assert row['intervals'] == counts
    density = np.count_nonzero(residual) / residual.size
    assert density == row['density']
    for length in lengths[:-1]:
        first, second = counts[str(length)], counts[str(2 * length)]
        if first['count'] and second['count']:
            slope = (np.log(first['count'] / first['total']) - np.log(second['count'] / second['total'])) / length
            assert np.isclose(slope, row['slopes'][str(length)], atol=1e-15, rtol=0)
        else:
            assert row['slopes'][str(length)] is None
    return counts


def round09():
    result = provenance(9)
    earlier = read_json(UNIT / 'round06/result.json')
    old = {(row['rule'], row['seed']): row for row in earlier['rules']}
    recorded = {(row['rule'], row['seed']): row for row in result['rules']}
    assert set(recorded) == set(old) and len(result['rules']) == 352
    saved = np.load(UNIT / 'round06/trajectories.npz')
    native_counts = 0
    rule122_absorption = []
    transport = {(row['rule'], row['dimension']): row for row in result['transport']}
    assert len(transport) == len(result['transport']) == 21
    transport_checks = 0
    for tag, row in recorded.items():
        rule, seed = tag
        original = old[tag]
        for key in ('p', 'v', 'q', 'alpha'):
            assert row[key] == original[key]
        a = np.unpackbits(saved[f's{seed}_r{rule:03d}'], bitorder='big', axis=1)[:, :2039]
        residual = independent_residual(a, row['p'], row['v'], 1024)
        verify_tail_summary(residual, row)
        native_counts += 9
        if rule == 122:
            zero_states = np.flatnonzero(~np.any(a, axis=1))
            rule122_absorption.append({'seed': seed,
                                       'first_zero_state': int(zero_states[0]) if len(zero_states) else None,
                                       'empty_residual_rows': int(np.count_nonzero(~np.any(residual, axis=1)))})
        if (rule, 1) not in transport or seed != 6041511:
            continue
        first = a[:260]
        positions = (np.arange(2039) + row['v']) % 2039
        second = a[row['p']:row['p'] + 260, positions]
        source = first[:256] != second[:256]
        lengths = [1, 2, 4, 8, 16, 32, 64, 128, 256]
        source_counts = independent_interval_counts(source, [length + extra for length in lengths for extra in (0, 4, 8)])
        for dimension in (1, 2, 3):
            if dimension > 1:
                first, second = independent_lift_series(first), independent_lift_series(second)
            actual = np.any((first[:256] != second[:256]).reshape(256, -1, 2039), axis=1)
            expected = transport[rule, dimension]
            counts = verify_tail_summary(actual, expected)
            radius = 2 * (dimension - 1)
            assert expected['radius'] == radius and expected['bounds_passed']
            for length in lengths:
                assert source_counts[str(length + 2 * radius)]['count'] <= counts[str(length)]['count'] <= source_counts[str(length)]['count']
                transport_checks += 1
    censored = sum(value is None for row in result['rules'] for value in row['slopes'].values())
    return {'native_interval_counts_independently_recomputed': native_counts,
            'native_runs': 352, 'lifted_or_source_transport_tables': 21, 'transport_inequalities_verified': transport_checks,
            'all_finite_slopes_and_censoring_equal': True, 'native_censored_slope_estimates': censored,
            'rule122_absorption_diagnostic_from_existing_trajectories': rule122_absorption,
            'independent_count_method': 'cyclic zero-run lengths, not prefix-sum windows',
            'scope': 'finite interval counts and exact cyclic-origin bounds; no existence or estimated value of an infinite-line tail limit established',
            'result_sha256': sha(UNIT / 'round09/result.json')}


def independent_open_step(state, radius, correction):
    neighborhoods = np.lib.stride_tricks.sliding_window_view(state, 2 * radius + 1, axis=-1)
    result = neighborhoods[..., -1].copy()
    if correction:
        result ^= np.all(neighborhoods[..., :-1] != 0, axis=-1).astype(np.uint8)
    return result


def independent_open_damage(initial, radius, correction, width, horizon, trials=32):
    center = len(initial) // 2
    sites = np.linspace(center - width // 2, center + width // 2, trials, dtype=int)
    padding = 2 * radius * horizon
    positions = sites[:, None] + np.arange(-padding, padding + 1)[None, :]
    assert positions.min() >= 0 and positions.max() < len(initial)
    original = initial[positions]
    ensemble = np.concatenate((original, original), axis=0)
    ensemble[trials:, padding] ^= 1
    rows = []
    for tick in range(horizon + 1):
        differing = ensemble[:trials] != ensemble[trials:]
        mass = np.count_nonzero(differing, axis=1)
        alive = mass > 0
        first = np.argmax(differing, axis=1)
        last = differing.shape[1] - 1 - np.argmax(differing[:, ::-1], axis=1)
        diameter = np.where(alive, last - first + 1, 0)
        assert np.all(first[alive] >= padding - 2 * radius * tick)
        assert np.all(last[alive] <= padding)
        rows.append((np.count_nonzero(alive) / trials, mass.sum() / trials, diameter.sum() / trials))
        if tick < horizon:
            ensemble = independent_open_step(ensemble, radius, correction)
    return np.array(rows)


def round10():
    result = provenance(10)
    directory = UNIT / 'round10'
    assert sha(directory / 'trajectories.npz') == result['raw_sha256']
    design = {(radius, correction, seed) for radius in (1, 2, 3)
              for correction in (False, True) for seed in (6041541, 6041542)}
    assert len(result['rules']) == 12
    assert {(r['radius'], r['correction'], r['seed']) for r in result['rules']} == design
    stored = np.load(directory / 'trajectories.npz')
    identities = 0
    for rule in range(256):
        truth = [(rule >> i) & 1 for i in range(8)]
        reflected = [truth[int(f'{i:03b}'[::-1], 2)] for i in range(8)]
        complemented = [1 - truth[7 - i] for i in range(8)]
        for left, middle, right in itertools.product((0, 1), repeat=3):
            index = 4 * left + 2 * middle + right
            assert reflected[4 * right + 2 * middle + left] == truth[index]
            assert complemented[4 * (1 - left) + 2 * (1 - middle) + 1 - right] == 1 - truth[index]
            if rule == 106:
                assert truth[index] == (right ^ (left & middle))
            identities += 2
    assert identities == result['symmetry_identity_checks'] == 4096
    decisions = []
    for row in result['rules']:
        radius, correction, seed = row['radius'], row['correction'], row['seed']
        width, burn, frames, horizon = 4093, 2048, 1024, 512
        assert row['width'] == width
        margin = 8 * radius
        keep = width + 2 * margin
        total = width + 2 * radius * (burn + frames + 8 + 2 * horizon)
        initial = (np.random.Generator(np.random.PCG64(seed)).random(total) < .5).astype(np.uint8)
        for _ in range(burn):
            initial = independent_open_step(initial, radius, correction)
        burned = initial.copy()
        name = f'r{radius}_g{int(correction)}_s{seed}'
        expected = np.unpackbits(stored[name], bitorder='big', axis=1)[:, :keep]
        trajectory = np.empty((1032, keep), np.uint8)
        for tick in range(1032):
            center = len(initial) // 2
            trajectory[tick] = initial[center - keep // 2:center + keep // 2 + 1]
            if tick < 1031:
                initial = independent_open_step(initial, radius, correction)
        assert np.array_equal(expected, trajectory)
        core = trajectory[:1024, margin:margin + width]
        candidates = sorted([(p, v) for p in range(1, 9) for v in range(-radius * p, radius * p + 1)],
                            key=lambda pair: (pair[0], abs(pair[1]), pair[1]))
        rates = [np.count_nonzero(core != trajectory[p:p + frames, margin + v:margin + v + width]) / core.size
                 for p, v in candidates]
        winner = min(range(len(rates)), key=lambda i: rates[i])
        assert candidates[winner] == (row['p'], row['v'])
        fraction = float(trajectory[:, margin:margin + width].mean())
        assert fraction == row['one_density']
        q = rates[winner] / (2 * fraction * (1 - fraction))
        assert q == row['q']
        assert rates[candidates.index((1, -radius))] == row['matched_shift_error']
        assert row['theoretical_matched_error'] == (2. ** (-2 * radius) if correction else 0.)
        codes = np.zeros((frames, width - 7), np.uint16)
        for bit in range(8):
            codes += core[:, bit:bit + width - 7].astype(np.uint16) * (1 << (7 - bit))
        counts = np.bincount(codes.ravel(), minlength=256)
        frequencies = counts[counts > 0] / counts.sum()
        entropy = float(-np.dot(frequencies, np.log2(frequencies)) / 8)
        assert np.isclose(entropy, row['block8_entropy_per_bit'], atol=2e-15, rtol=0)
        curve = independent_open_damage(burned, radius, correction, width, horizon)
        assert np.array_equal(curve, stored[name + '_damage'])
        assert curve[-1].tolist() == row['final_damage']
        alpha = float(np.log2(curve[-1, 2] / curve[horizon // 2, 2])) if curve[-1, 2] > 0 and curve[horizon // 2, 2] > 0 else 0.
        assert alpha == row['alpha']
        decision = bool(0 < q < .5 and alpha > .5)
        assert decision == row['selected']
        if not correction:
            assert rates[winner] == q == alpha == 0
            assert np.all(curve == 1)
        decisions.append({'radius': radius, 'correction': correction, 'seed': seed, 'selected': decision})
    return {'complete_open_window_trajectories_and_damage_ensembles_reproduced': 12,
            'symmetry_local_identities_independently_checked': identities,
            'all_selectors_errors_entropies_growth_and_decisions_equal': True,
            'decisions': decisions,
            'geometry': 'initial damage half-width2*r*horizon retains the entire influence cone throughout shrinking evolution',
            'theory': 'right-permutivity gives2^(2r) preimage blocks for each output block; uniform Bernoulli spatial slices persist; matched residual is AND of2r iid bits',
            'scope': 'mechanism adversary with unassigned Wolfram classes; selection challenges ordered-spatial-background interpretation, not established class labels',
            'result_sha256': sha(directory / 'result.json')}


def round11():
    result = provenance(11)
    directory = UNIT / 'round11'
    assert sha(directory / 'curves.npz') == result['raw_sha256']
    earlier = read_json(UNIT / 'round10/result.json')
    initial_rows = {(r['radius'], r['seed']): r for r in earlier['rules'] if r['correction']}
    assert len(result['rules']) == 6 and {(r['radius'], r['seed']) for r in result['rules']} == set(initial_rows)
    original_data = np.load(UNIT / 'round10/trajectories.npz')
    stored = np.load(directory / 'curves.npz')
    decisions = []
    for row in result['rules']:
        radius, seed = row['radius'], row['seed']
        assert row['q'] == initial_rows[radius, seed]['q']
        width, burn, horizon = 4093, 2048, 4096
        original_length = width + 2 * radius * (burn + 1024 + 8 + 2 * 512)
        core = (np.random.Generator(np.random.PCG64(seed)).random(original_length) < .5).astype(np.uint8)
        length = width + 4 * radius * horizon + 2 * radius * burn
        extra = (length - original_length) // 2
        assert length == 2 * extra + original_length
        random = np.random.Generator(np.random.PCG64(seed + 100000000))
        left = (random.random(extra) < .5).astype(np.uint8)
        right = (random.random(extra) < .5).astype(np.uint8)
        state = np.concatenate((left, core, right))
        for _ in range(burn):
            state = independent_open_step(state, radius, True)
        curve = independent_open_damage(state, radius, True, width, horizon)
        name = f'r{radius}_g1_s{seed}_damage'
        assert np.array_equal(curve, stored[name])
        assert np.array_equal(curve[:513], original_data[name])
        assert row['prefix_exact']
        for endpoint in (512, 1024, 2048, 4096):
            saved = row['checkpoints'][str(endpoint)]
            alpha = float(np.log2(curve[endpoint, 2] / curve[endpoint // 2, 2])) if curve[endpoint, 2] > 0 and curve[endpoint // 2, 2] > 0 else 0.
            assert saved['alpha'] == alpha
            assert (saved['survival'], saved['hamming'], saved['diameter']) == tuple(curve[endpoint])
            selected = bool(0 < row['q'] < .5 and alpha > .5)
            assert saved['selected'] == selected
            decisions.append({'radius': radius, 'seed': seed, 'horizon': endpoint, 'selected': selected})
        print('round11 independent radius/seed', radius, seed, flush=True)
    return {'complete4096_step_open_window_damage_ensembles_reproduced': 6,
            'trials_per_ensemble': 32, 'entire0_to512_prefix_matches': True,
            'all_checkpoint_exponents_and_fixed_q_decisions_equal': True,
            'decisions': decisions,
            'scope': 'extension of exact existing trials with independent iid padding; q reused from R10 and no asymptotic exponent established',
            'result_sha256': sha(directory / 'result.json')}


def audit_archives():
    manifest = read_json(UNIT / 'raw-archive.json')
    outputs = []
    seen = set()
    for volume in manifest['volumes']:
        path = ROOT.parent / volume['filename']
        assert path.stat().st_size == volume['bytes']
        assert sha(path) == volume['sha256']
        members = {row['path']: row for row in volume['members']}
        assert not seen.intersection(members)
        seen.update(members)
        with zipfile.ZipFile(path) as archive:
            assert set(archive.namelist()) == set(members)
            for member in archive.infolist():
                relative = Path(member.filename)
                assert not relative.is_absolute() and '..' not in relative.parts
                expected = members[member.filename]
                assert member.file_size == expected['bytes']
                h = hashlib.sha256()
                with archive.open(member) as content:
                    for block in iter(lambda: content.read(1 << 20), b''):
                        h.update(block)
                assert h.hexdigest() == expected['sha256']
                assert sha(ROOT.parent / relative) == expected['sha256']
        outputs.append({'filename': volume['filename'], 'members': len(members),
                        'bytes': volume['bytes'], 'sha256': volume['sha256']})
    return {'volumes': outputs, 'all_members_match_local_audited_artifacts': True,
            'members': len(seen), 'manifest_sha256': sha(UNIT / 'raw-archive.json')}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rounds', default='1,2')
    parser.add_argument('--archives', action='store_true')
    args = parser.parse_args()
    selected = {int(x) for x in args.rounds.split(',') if x}
    started = time.perf_counter()
    target = ROOT / 'review/beam_loop_independent.json'
    report = read_json(target) if target.exists() else {'rounds': {}}
    full = None
    if 1 in selected or 2 in selected:
        finding, full = round01()
        report['rounds']['1'] = finding
        print('audited round01', flush=True)
    if 2 in selected:
        report['rounds']['2'] = round02(full)
    if 3 in selected:
        report['rounds']['3'] = round03()
    if 4 in selected:
        report['rounds']['4'] = round04()
    if 5 in selected:
        report['rounds']['5'] = round05()
    if 6 in selected:
        report['rounds']['6'] = round06()
    if 7 in selected:
        report['rounds']['7'] = round07()
    if 8 in selected:
        report['rounds']['8'] = round08()
    if 9 in selected:
        report['rounds']['9'] = round09()
    if 10 in selected:
        report['rounds']['10'] = round10()
    if 11 in selected:
        report['rounds']['11'] = round11()
    if args.archives:
        report['raw_archives'] = audit_archives()
    report['reviewer'] = 'independent collaborating agent /root/beam_loop_review, OpenAI GPT-6 Astra, 2026-09-15'
    report['auditor_sha256'] = sha(__file__)
    report['last_audit_seconds'] = time.perf_counter() - started
    target.write_text(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + '\n')
    print('audit complete', report['last_audit_seconds'], flush=True)


if __name__ == '__main__':
    main()
