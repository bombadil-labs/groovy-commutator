#!/usr/bin/env python3
"""Independent dictionary/set reconstruction of saved partial-rule comparisons.

No author comparison functions are imported. No new lift or trajectory is run.
"""
from __future__ import annotations

import base64
import hashlib
import itertools
import json
from pathlib import Path
import statistics
import tarfile
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / 'experiments/partial_cohabitation_20260915/run'
RESULT = ROOT / 'results/partial_cohabitation_20260915.json'
POLICIES = ('no_flip', 'flip', 'output_zero', 'output_one')
ANCHORS = (0, 1, 18, 30, 41, 54, 90, 106, 110, 122, 126, 204)
ARCHIVE = ROOT.parent / 'gc-pilot/experiments/uniform_jet6_cache_20260914/run/uniform_jet6_rules.tar.gz'


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b''):
            digest.update(chunk)
    return digest.hexdigest()


def default(key, policy):
    if policy == 0:
        return 0
    if policy == 1:
        return 1
    center = (key >> 17) & 1
    return center if policy == 2 else 1 - center


def witness(key, a, b):
    return {'key': key, 'bits_35': f'{key:035b}', 'a_forced': a.get(key), 'b_forced': b.get(key)}


def ref_conjugate(rule):
    out = 0
    for left, center, right in itertools.product((0, 1), repeat=3):
        at = 4*left + 2*center + right
        other = 4*(1-left) + 2*(1-center) + (1-right)
        out |= (1 - ((rule >> other) & 1)) << at
    return out


def controls():
    tested = 0
    for pvalues, qvalues in itertools.product(itertools.product((None, 0, 1), repeat=3), repeat=2):
        p = {i: value for i, value in enumerate(pvalues) if value is not None}
        q = {i: value for i, value in enumerate(qvalues) if value is not None}
        bad = {key for key in p.keys() & q.keys() if p[key] != q[key]}
        all_assignments = tuple(itertools.product((0, 1), repeat=3))
        pe = [f for f in all_assignments if all(f[k] == v for k, v in p.items())]
        qe = [g for g in all_assignments if all(g[k] == v for k, v in q.items())]
        shared = set(pe) & set(qe)
        assert bool(shared) == (not bad)
        assert min(sum(x != y for x, y in zip(f, g)) for f in pe for g in qe) == len(bad)
        if not bad:
            cost = len(q.keys() - p.keys())
            assert len(pe) == len(shared) * (1 << cost)
        for mode in range(4):
            values = ((0, 0, 0), (1, 1, 1), (0, 1, 0), (1, 0, 1))[mode]
            fp = tuple(p.get(k, values[k]) for k in range(3))
            fq = tuple(q.get(k, values[k]) for k in range(3))
            if fp == fq:
                assert not bad
        tested += 1
    return {'ternary_three_key_pairs': tested,
            'conditional_completion_counts_exhaustive': True,
            'minimum_completion_hamming_distance_exhaustive': True,
            'completed_equality_subset_exhaustive': True}


def compare(a, b, where=''):
    if isinstance(a, dict):
        assert a.keys() == b.keys(), (where, a.keys(), b.keys())
        for key in a:
            compare(a[key], b[key], f'{where}/{key}')
    elif isinstance(a, list):
        assert len(a) == len(b), (where, len(a), len(b))
        for i, (x, y) in enumerate(zip(a, b)):
            compare(x, y, f'{where}/{i}')
    elif isinstance(a, float):
        assert abs(a - b) < 1e-12, (where, a, b)
    else:
        assert a == b, (where, a, b)


def audit_domain(name, tables, stated, labels):
    start = time.perf_counter()
    with np.load(RUN / stated['pair_file'], allow_pickle=False) as arrays:
        assert arrays.files == ['rows']
        saved = arrays['rows']
    assert saved.shape == (32640, 9)
    assert sha(RUN / stated['pair_file']) == stated['pair_file_sha256']
    stats = []
    for rule, table in enumerate(tables):
        assert all(value in (0, 1) for value in table.values())
        stats.append({'rule': rule, 'forced': len(table),
                      'forced_zero': sum(value == 0 for value in table.values()),
                      'forced_one': sum(value == 1 for value in table.values()),
                      'compatible_partners': 0, 'occupied_partners': 0,
                      'shared_keys_sum_all_partners': 0, 'conflicting_keys_sum_all_partners': 0,
                      'shared_keys_sum_compatible_partners': 0, 'additional_pins_sum_compatible_partners': 0})
    edges = set()
    equals = [0]*4
    vacuous = 0
    first_false = [None]*4
    first_conflict = None
    compared = 0
    selected_pair = None
    for (a, b), saved_row in zip(itertools.combinations(range(256), 2), saved):
        p, q = tables[a], tables[b]
        shared = p.keys() & q.keys()
        bad = {key for key in shared if p[key] != q[key]}
        zero = sum(p[key] == q[key] == 0 for key in shared)
        one = sum(p[key] == q[key] == 1 for key in shared)
        assert zero + one + len(bad) == len(shared)
        union = p.keys() | q.keys()
        eq = [int(all(p.get(key, default(key, policy)) == q.get(key, default(key, policy))
                      for key in union)) for policy in range(4)]
        actual = [a, b, zero, one, len(bad), *eq]
        assert actual == saved_row.tolist(), (name, a, b, actual, saved_row.tolist())
        if (a, b) == (54, 110):
            selected_pair = {'shared_zero': zero, 'shared_one': one, 'conflicts': len(bad),
                             'witness': witness(min(bad), p, q) if bad else None}
        for r in (a, b):
            stats[r]['shared_keys_sum_all_partners'] += len(shared)
            stats[r]['conflicting_keys_sum_all_partners'] += len(bad)
        for policy in range(4):
            equals[policy] += eq[policy]
            assert not eq[policy] or not bad
        if bad:
            if first_conflict is None:
                first_conflict = {'a': a, 'b': b, **witness(min(bad), p, q)}
        else:
            edges.add((a, b))
            vacuous += int(not shared)
            for r, other in ((a, b), (b, a)):
                stats[r]['compatible_partners'] += 1
                stats[r]['occupied_partners'] += int(bool(shared))
                stats[r]['shared_keys_sum_compatible_partners'] += len(shared)
                stats[r]['additional_pins_sum_compatible_partners'] += len(tables[other].keys() - tables[r].keys())
            for policy in range(4):
                if not eq[policy] and first_false[policy] is None:
                    key = min(key for key in union if p.get(key, default(key, policy)) != q.get(key, default(key, policy)))
                    first_false[policy] = {'a': a, 'b': b, **witness(key, p, q)}
        compared += 1
    classes = {}
    for label, reps in labels['representatives'].items():
        chosen = [r for r in reps if r not in (41, 106)]
        degrees = [stats[r]['compatible_partners'] for r in chosen]
        classes[label] = {'representatives': chosen, 'n': len(chosen), 'mean_degree': statistics.mean(degrees),
                          'median_degree': statistics.median(degrees), 'min_degree': min(degrees), 'max_degree': max(degrees)}
    transforms = {}
    for tag, fn in (('output_complement', lambda r: r ^ 255), ('boolean_conjugacy', ref_conjugate)):
        pairs = [(r, fn(r)) for r in range(256) if r < fn(r)]
        transforms[tag] = {'distinct_pairs': len(pairs), 'compatible_pairs': sum(pair in edges for pair in pairs),
                           'incompatible_pairs': [list(pair) for pair in pairs if pair not in edges]}
    expected = {'pairs': compared, 'compatible_pairs': len(edges), 'compatible_fraction': len(edges) / compared,
                'vacuous_compatible_pairs': vacuous, 'occupied_compatible_pairs': len(edges) - vacuous,
                'completed_equal_pairs': dict(zip(POLICIES, equals)),
                'false_conflicts': {policy: len(edges)-equals[i] for i, policy in enumerate(POLICIES)},
                'first_false_conflicts': dict(zip(POLICIES, first_false)), 'first_conflict': first_conflict,
                'per_rule': stats, 'anchors': {str(r): stats[r] for r in ANCHORS}, 'classes_core_convention': classes,
                'transforms': transforms, 'pair_file': stated['pair_file'], 'pair_file_sha256': stated['pair_file_sha256']}
    compare(expected, stated, name)
    assert sum(r['compatible_partners'] for r in stats) == 2*len(edges)
    print(json.dumps({'domain_audited': name, 'seconds': time.perf_counter()-start, 'pairs': compared}), flush=True)
    return edges, {'pairs': compared, 'compatible_pairs': len(edges), 'vacuous': vacuous,
                   'occupied': len(edges)-vacuous, 'completed_equal_pairs': equals, 'pair_54_110': selected_pair,
                   'seconds': time.perf_counter()-start}


def direct_keys(grid):
    result = np.zeros(grid.shape, dtype=np.uint64)
    for i, (dy, dx) in enumerate(itertools.product(range(-3, 4), range(-2, 3))):
        selected = np.take(np.take(grid, (np.arange(6)+dy) % 6, axis=-2),
                           (np.arange(grid.shape[-1])+dx) % grid.shape[-1], axis=-1)
        result += selected.astype(np.uint64) * np.uint64(1 << (34-i))
    return result


def audit_archive(records, data):
    assert sha(ARCHIVE) == data['archive_sha256']
    anchors = set(ANCHORS) | {9, 51, 104, 132, 146, 170, 196, 233, 254, 255}
    sampled, member_hashes = 0, {}
    with tarfile.open(ARCHIVE, 'r|gz') as tf:
        for member in tf:
            if not member.isfile() or member.name not in data['member_sha256']:
                continue
            raw = tf.extractfile(member).read()
            digest = hashlib.sha256(raw).hexdigest()
            assert digest == data['member_sha256'][member.name]
            member_hashes[member.name] = digest
            d = json.loads(raw)
            if d['rule'] not in anchors:
                continue
            width, rule = d['width'], d['rule']
            n = 1 << width
            values = np.unpackbits(np.frombuffer(base64.b64decode(d['grid_bits_big']), dtype=np.uint8), bitorder='big')
            grid = values[:n*6*width].reshape(n, 6, width)
            keys = direct_keys(grid)
            indices = np.frombuffer(base64.b64decode(d['representative_flat_indices_u32le']), dtype='<u4')
            bits = np.unpackbits(np.frombuffer(base64.b64decode(d['forced_derivative_bits_big']), dtype=np.uint8), bitorder='big')
            table = dict(zip(map(int, keys.flat[indices]), map(int, bits[:len(indices)])))
            assert table == records[width][rule]
            assert len(table) == len(indices) == d['forced_root_count']
            assert set(map(int, keys.flat)) == table.keys()
            source = np.array([[int(b) for b in f'{s:0{width}b}'] for s in range(n)], dtype=np.uint8)
            assert np.array_equal(grid[:, 4] ^ grid[:, 5], source)
            targets = []
            for bits in source:
                output = [int((rule >> (4*int(bits[(i-1) % width]) + 2*int(bits[i]) + int(bits[(i+1) % width]))) & 1)
                          for i in range(width)]
                targets.append(int(''.join(map(str, output)), 2))
            flip = np.fromiter((table[int(key)] for key in keys.flat), dtype=np.uint8).reshape(grid.shape)
            assert np.array_equal(grid ^ flip, grid[targets])
            sampled += 1
    assert member_hashes == data['member_sha256']
    assert sampled == 2*len(anchors)
    return {'archive_hash_matched': True, 'member_hashes_checked': len(member_hashes),
            'physical_tables_independently_reconstructed': sampled, 'sampled_roots': sorted(anchors),
            'sampled_decoder_and_successor_checks_passed': True}


def main():
    started = time.perf_counter()
    data = json.loads(RESULT.read_text())
    for path, digest in data['source_hashes'].items():
        assert sha(ROOT / path) == digest
    for name, digest in data['raw_files'].items():
        assert sha(RUN / name) == digest
    freeze = json.loads((RUN / 'freeze.json').read_text())
    assert freeze['source_hashes'] == data['source_hashes']
    assert freeze['archive_sha256'] == data['archive_sha256']
    assert tuple(data['pair_columns']) == ('a', 'b', 'shared_zero', 'shared_one', 'conflicts', *POLICIES)
    records = {7: {}, 8: {}}
    global_keys = set()
    with np.load(RUN / 'physical_tables.npz', allow_pickle=False) as arrays:
        assert len(arrays.files) == 1024
        for width, rule in itertools.product((7, 8), range(256)):
            keys = arrays[f'w{width}_r{rule:03d}_keys']
            values = arrays[f'w{width}_r{rule:03d}_values']
            assert keys.shape == values.shape and keys.ndim == 1
            assert np.all(keys[1:] > keys[:-1]) and np.all(keys < 1 << 35)
            assert np.all(values <= 1)
            table = dict(zip(map(int, keys), map(int, values)))
            assert len(table) == len(keys)
            records[width][rule] = table
            global_keys.update(table)
    assert len(global_keys) == data['global_physical_keys']
    assert data['ambient_table_entries'] == 1 << 35
    labels = json.loads((ROOT / 'experiments/on_beam_256_4d_20260914/labels.json').read_text())
    domains = {f'w{w}': [records[w][r] for r in range(256)] for w in (7, 8)}
    cross, pooled = [], []
    for rule in range(256):
        p, q = records[7][rule], records[8][rule]
        bad = {key for key in p.keys() & q.keys() if p[key] != q[key]}
        cross.append({'rule': rule, 'conflicts': len(bad), 'witness': witness(min(bad), p, q) if bad else None})
        pooled.append(p | q)
    compare(cross, data['cross_width'])
    if all(x['conflicts'] == 0 for x in cross):
        domains['pooled'] = pooled
    assert domains.keys() == data['domains'].keys()
    adjacency, reports = {}, {}
    for name, tables in domains.items():
        adjacency[name], reports[name] = audit_domain(name, tables, data['domains'][name], labels)
    expected_width = {'w7_only': len(adjacency['w7'] - adjacency['w8']),
                      'w8_only': len(adjacency['w8'] - adjacency['w7']),
                      'both': len(adjacency['w7'] & adjacency['w8'])}
    if 'pooled' in adjacency:
        assert adjacency['pooled'] <= adjacency['w7'] & adjacency['w8']
        expected_width['both_but_not_pooled'] = len((adjacency['w7'] & adjacency['w8']) - adjacency['pooled'])
    compare(expected_width, data['width_change'])
    expected_predictions = {'P1_archive_validation': True, 'P2_completed_equal_subset': True,
                            'P3_no_flip_false_conflicts': all(reports[k]['compatible_pairs'] > reports[k]['completed_equal_pairs'][0] for k in reports),
                            'P4_cross_width_consistent': all(x['conflicts'] == 0 for x in cross)}
    compare(expected_predictions, data['predictions'])
    archive_report = audit_archive(records, data)
    report = {'status': 'passed', 'result_sha256': sha(RESULT), 'source_hashes': data['source_hashes'],
              'controls': controls(), 'domains': reports, 'width_change': expected_width,
              'archive_audit': archive_report, 'pair_records_recomputed': sum(r['pairs'] for r in reports.values()),
              'completed_equality_predicates_recomputed': 4*sum(r['pairs'] for r in reports.values()),
              'physical_tables': 512, 'cross_width_roots_checked': 256,
              'witnesses_classes_anchors_and_per_root_statistics_checked': True,
              'comparison_method': 'Actual integer-key dictionaries; shared-key intersection and pointwise default completion on domain unions.',
              'no_author_comparison_functions_imported': True, 'new_lifts_or_trajectories': 0,
              'elapsed_seconds': time.perf_counter()-started,
              'limitations': ['The old separate-workspace cohabitation implementation was not audited or reproduced.',
                              'Table compatibility is for the finite archived beam families, without decoder compatibility or a full-shift claim.',
                              'Completed-rule equality is an intentionally different predicate; disagreement under fixed defaults alone is not a partial-rule conflict.']}
    path = ROOT / 'review/partial_cohabitation_independent.json'
    path.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
