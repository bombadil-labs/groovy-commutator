#!/usr/bin/env python3
"""Exact affine families of G values over partial native-rule completions."""
from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone
import hashlib
import itertools
import json
from pathlib import Path
import platform
import resource
import tarfile
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / 'experiments/commutator_completion_20260915'
INPUT = ROOT.parent / 'gc-pilot/experiments/uniform_jet6_cache_20260914/run'
ARCHIVE = INPUT / 'uniform_jet6_rules.tar.gz'
MANIFEST = INPUT / 'archive_manifest.json'
ARCHIVE_SHA = '766e4db7083fbdb551bc4aee66abc554079c5d118905f6d65aa5e5372c9418d1'
FULL = ROOT / 'experiments/beam_discriminator_loop_20260915/round01/tables.npz'
SOURCE_PATHS = ('scripts/commutator_completion.py',
                'experiments/commutator_completion_20260915/protocol.md',
                'experiments/commutator_completion_20260915/protocol-freeze.json',
                'experiments/beam_discriminator_loop_20260915/round01/result.json')


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def save_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False) + '\n')
    temp.replace(path)


def save_arrays(path, arrays):
    temp = path.with_suffix('.npz.tmp')
    with temp.open('wb') as f:
        np.savez_compressed(f, **arrays)
    temp.replace(path)


def unpack(text, shape):
    raw = base64.b64decode(text, validate=True)
    bits = np.unpackbits(np.frombuffer(raw, np.uint8), bitorder='big')
    n = int(np.prod(shape))
    assert len(raw) == (n + 7) // 8 and not np.any(bits[n:])
    return bits[:n].reshape(shape)


class PeriodKeys:
    """Exact physical-key DAG on period-six transverse fields.

    Six five-bit strips form a physical 30-bit key. Further transverse
    directions intern ordered six-tuples. Restoring the repeated seventh
    child at each depth recovers the original 7^k by 5 physical neighborhood.
    Pools are retained across all arrays whose key IDs are compared.
    """
    def __init__(self, dimension):
        self.dimension = dimension
        self.pools = [{} for _ in range(dimension - 2)]
        self.nodes = [[] for _ in range(dimension - 2)]

    def keys(self, grid):
        assert grid.ndim == self.dimension + 1
        assert all(n == 6 for n in grid.shape[1:-1])
        line = np.zeros(grid.shape, np.uint32)
        for dx in range(-2, 3):
            line = (line << np.uint32(1)) | np.roll(grid, -dx, axis=-1)
        result = np.zeros(grid.shape, np.uint32)
        for dy in range(-3, 3):
            result = (result << np.uint32(5)) | np.roll(line, -dy, axis=-2)
        for depth, axis in enumerate(range(grid.ndim - 3, 0, -1)):
            chunks = np.stack([np.roll(result, -dy, axis=axis) for dy in range(-3, 3)], axis=-1)
            packed = np.ascontiguousarray(chunks, dtype='<u4').reshape(-1, 6).view('V24').ravel()
            unique, inverse = np.unique(packed, return_inverse=True)
            remap = np.empty(len(unique), np.uint32)
            pool, nodes = self.pools[depth], self.nodes[depth]
            for i, item in enumerate(unique):
                key = bytes(item)
                identifier = pool.get(key)
                if identifier is None:
                    identifier = len(nodes)
                    pool[key] = identifier
                    nodes.append(tuple(map(int, np.frombuffer(key, dtype='<u4'))))
                remap[i] = identifier
            result = remap[inverse].reshape(grid.shape)
        return result

    def expand(self, key, depth=None):
        if depth is None:
            depth = self.dimension - 3
        if depth < 0:
            bits = tuple((int(key) >> b) & 1 for b in range(29, -1, -1))
            return bits + bits[:5]
        children = self.nodes[depth][int(key)]
        return tuple(bit for child in children + children[:1] for bit in self.expand(child, depth - 1))


def literal_key(grid, flat):
    source, *coord = np.unravel_index(flat, grid.shape)
    ranges = [range(-3, 4)] * (grid.ndim - 2) + [range(-2, 3)]
    return tuple(int(grid[(source,) + tuple((c + a) % n for c, a, n in zip(coord, offsets, grid.shape[1:]))])
                 for offsets in itertools.product(*ranges))


def lookup(keys, values, queries):
    at = np.searchsorted(keys, queries)
    clipped = np.minimum(at, len(keys) - 1)
    known = (at < len(keys)) & (keys[clipped] == queries)
    out = np.zeros(queries.shape, np.uint8)
    out[known] = values[clipped[known]]
    return known, out


def symbolic(queries, two_step, keys, values, in_family):
    known, supplied = lookup(keys, values, queries)
    free_keys = np.unique(queries[~known])
    labels = np.zeros(queries.shape, np.uint32)
    labels[~known] = np.searchsorted(free_keys, queries[~known]).astype(np.uint32) + 1
    constant = two_step ^ supplied
    u = len(free_keys)
    flat_label, flat_const = labels.ravel(), constant.ravel()
    counts = np.bincount(flat_label, minlength=u + 1)[1:].astype(np.int64)
    ones = np.bincount(flat_label[flat_const == 1], minlength=u + 1)[1:].astype(np.int64)
    zeros = counts - ones
    per_state = []
    state_uses = np.zeros(u, np.uint32)
    for row in labels:
        seen = np.unique(row)
        seen = seen[seen > 0] - 1
        per_state.append(len(seen))
        state_uses[seen] += 1
    free_per_phase = np.sum(~known, axis=(0,) + tuple(range(2, queries.ndim))).tolist()
    n = queries.size
    assert np.all(np.asarray(per_state)[in_family] == 0)
    summary = {
        'cells': n, 'fixed_zero': int(np.sum(known & (constant == 0))),
        'fixed_one': int(np.sum(known & (constant == 1))), 'free_cells': int(np.sum(~known)),
        'free_fraction': float(np.mean(~known)), 'free_keys': u,
        'log2_distinct_joint_G_fields': u, 'per_state_free_keys': per_state,
        'per_state_free_cells': np.sum(~known, axis=tuple(range(1, queries.ndim))).tolist(),
        'free_cells_by_newest_phase': free_per_phase,
        'fully_fixed_states': int(np.sum(np.asarray(per_state) == 0)),
        'difference_in_family_states': int(np.sum(in_family)),
        'fully_fixed_off_family_states': int(np.sum((np.asarray(per_state) == 0) & ~in_family)),
        'variables_shared_across_states': int(np.sum(state_uses > 1)),
        'variable_state_uses_sum': int(state_uses.sum()),
        'mean_variable_occurrences': float(counts.mean()) if u else 0.0,
        'max_variable_occurrences': int(counts.max()) if u else 0,
        'equal_G_pairs_from_shared_variable': int(np.sum(zeros * (zeros - 1) // 2 + ones * (ones - 1) // 2)),
        'opposite_G_pairs_from_shared_variable': int(np.sum(zeros * ones)),
    }
    assert summary['fixed_zero'] + summary['fixed_one'] + summary['free_cells'] == n
    return summary, {'free_keys': free_keys, 'g_constant_bits': np.packbits(constant.ravel(), bitorder='big'),
                     'g_symbol': labels, 'variable_occurrences': counts,
                     'variable_one_constants': ones, 'variable_state_uses': state_uses}, constant


def toy_controls():
    queries = np.array([[[0, 1, 1, 2, 2, 3]]], np.uint32)
    t = np.array([[[1, 0, 1, 0, 1, 1]]], np.uint8)
    result, arrays, const = symbolic(queries, t, np.array([0, 3], np.uint32), np.array([0, 1], np.uint8), np.array([False]))
    assert result['free_keys'] == 2 and result['fixed_one'] == 1 and result['fixed_zero'] == 1
    assert result['opposite_G_pairs_from_shared_variable'] == 2
    fields = set()
    labels = arrays['g_symbol']
    for bits in itertools.product((0, 1), repeat=2):
        assignment = np.array((0,) + bits, np.uint8)
        g = const ^ assignment[labels]
        fields.add(g.tobytes())
        assert int(g[0, 0, 1] ^ g[0, 0, 2]) == 1
    assert len(fields) == 4
    for a, b, c, flip in itertools.product((0, 1), repeat=4):
        assert ((b ^ c) ^ ((a ^ b) ^ flip)) == ((a ^ c) ^ flip)
    return {'enumerated_completions': 4, 'distinct_G_fields': 4, 'scalar_identity_cases': 16}


def audit_record(record, full):
    d, w, rule = record['dimension'], record['width'], record['rule']
    shape = (1 << w,) + (6,) * (d - 1) + (w,)
    assert record['format'] == 'grid-referenced-physical-partial-rule-v1'
    assert tuple(record['grid_shape']) == shape
    assert record['radii_array_order'] == [3] * (d - 1) + [2]
    grid = unpack(record['grid_bits_big'], shape)
    dag = PeriodKeys(d)
    family_queries = dag.keys(grid)
    reps = np.frombuffer(base64.b64decode(record['representative_flat_indices_u32le'], validate=True), dtype='<u4')
    pinned_keys = family_queries.ravel()[reps]
    values = unpack(record['forced_derivative_bits_big'], (len(reps),))
    order = np.argsort(pinned_keys)
    pinned_keys, values = pinned_keys[order], values[order]
    assert len(reps) == record['forced_root_count']
    assert np.array_equal(pinned_keys, np.unique(family_queries))
    known, delta = lookup(pinned_keys, values, family_queries)
    assert np.all(known)
    successor = grid ^ delta
    family = {row.tobytes(): i for i, row in enumerate(grid)}
    assert len(family) == shape[0]
    next_index = np.array([family[row.tobytes()] for row in successor], np.uint16)
    assert np.array_equal(successor, grid[next_index])
    second = grid[next_index[next_index]]
    two_step = grid ^ second
    root = grid
    for _ in range(d - 1):
        root = root[:, 4] ^ root[:, 5]
    assert root.shape == (1 << w, w)
    root_family = {row.tobytes(): i for i, row in enumerate(root)}
    assert len(root_family) == 1 << w
    lut = np.array([(rule >> k) & 1 for k in range(8)], np.uint8)
    expected = lut[4 * np.roll(root, 1, axis=-1) + 2 * root + np.roll(root, -1, axis=-1)]
    expected_index = np.array([root_family[row.tobytes()] for row in expected], np.uint16)
    assert np.array_equal(next_index, expected_index)
    delta_queries = dag.keys(delta)
    in_family = np.array([row.tobytes() in family for row in delta], bool)
    checks = 0
    for g, qs in ((grid, family_queries), (delta, delta_queries)):
        for at in (0, g.size // 2, g.size - 1):
            assert literal_key(g, at) == dag.expand(qs.ravel()[at])
            checks += 1
    contracts = {'finite': (pinned_keys, values)}
    if d == 2:
        fk = (full[f'r{rule:03d}_keys'] >> np.uint64(5)).astype(np.uint32)
        fv = full[f'r{rule:03d}_native'] - np.uint8(1)
        assert np.all(fv <= 1)
        included, agree = lookup(fk, fv, pinned_keys)
        assert np.all(included) and np.array_equal(agree, values)
        contracts['full_input_d2'] = (fk, fv)
    arrays = {'pinned_keys': pinned_keys, 'pinned_values': values, 'next_index': next_index,
              'difference_in_family': in_family.astype(np.uint8),
              **{f'dag_{i}': np.asarray(nodes, dtype=np.uint32).reshape(-1, 6) for i, nodes in enumerate(dag.nodes)}}
    result = {'rule': rule, 'width': w, 'dimension': d, 'shape': list(shape),
              'forced_keys': len(pinned_keys), 'contracts': {}, 'scalar_physical_checks': checks}
    for name, (keys, vals) in contracts.items():
        summary, saved, const = symbolic(delta_queries, two_step, keys, vals, in_family)
        arrays.update({name + '_' + key: value for key, value in saved.items()})
        # Direct definition, using zero only as an affine coordinate origin.
        known, supplied = lookup(keys, vals, delta_queries)
        h_delta_origin = delta ^ supplied
        direct = (successor ^ second) ^ h_delta_origin
        assert np.array_equal(direct, const)
        witness = None
        if summary['free_keys']:
            key = int(saved['free_keys'][0])
            occurrences = delta_queries == key
            at = int(np.flatnonzero(occurrences)[0])
            assert np.array_equal((successor ^ second) ^ (h_delta_origin ^ occurrences), const ^ occurrences)
            assert not np.any(family_queries == key)
            full_bits = literal_key(delta, at)
            assert full_bits == dag.expand(key)
            witness = {'query_key_id': key, 'symbol': 1, 'event': list(map(int, np.unravel_index(at, shape))),
                       'physical_bits': ''.join(map(str, full_bits)),
                       'origin_G': int(const.ravel()[at]), 'flipped_G': int(const.ravel()[at] ^ 1),
                       'changed_cells': int(occurrences.sum())}
        summary['witness'] = witness
        if rule in (0, 204):
            assert summary['free_cells'] == summary['fixed_one'] == 0
        result['contracts'][name] = summary
    if d == 2:
        a, b = result['contracts']['finite'], result['contracts']['full_input_d2']
        result['finite_free_cells_resolved_by_full_input'] = a['free_cells'] - b['free_cells']
        assert result['finite_free_cells_resolved_by_full_input'] >= 0
    return result, arrays


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--archive', type=Path, default=ARCHIVE)
    parser.add_argument('--manifest', type=Path, default=MANIFEST)
    parser.add_argument('--resume', action='store_true')
    args = parser.parse_args()
    start = time.perf_counter()
    UNIT.mkdir(parents=True, exist_ok=True)
    out = UNIT / 'records'; out.mkdir(exist_ok=True)
    assert not (UNIT / 'result.json').exists(), 'Completed scientific output must not be overwritten'
    hashes = {p: digest(ROOT / p) for p in SOURCE_PATHS}
    assert digest(args.archive) == ARCHIVE_SHA
    manifest = json.loads(args.manifest.read_text())
    assert manifest['archive_sha256'] == ARCHIVE_SHA
    assert manifest['archive_size'] == args.archive.stat().st_size
    members = {m['path']: m for m in manifest['members']}
    assert len(members) == len(manifest['members']) == 1536
    full_sha = digest(FULL)
    assert full_sha == json.loads((FULL.parent / 'result.json').read_text())['table_sha256']
    raw_inputs = {'uniform_jet6_rules.tar.gz': ARCHIVE_SHA,
                  'archive_manifest.json': digest(args.manifest), str(FULL.relative_to(ROOT)): full_sha}
    freeze = {'source_hashes': hashes, 'raw_input_hashes': raw_inputs,
              'started_at': datetime.now(timezone.utc).isoformat(),
              'python': platform.python_version(), 'numpy': np.__version__}
    if args.resume:
        prior = json.loads((UNIT / 'freeze.json').read_text())
        assert prior['source_hashes'] == hashes and prior['raw_input_hashes'] == raw_inputs
    else:
        assert not (UNIT / 'freeze.json').exists()
        save_json(UNIT / 'freeze.json', freeze)
    controls = toy_controls()
    records, resumed, timed_out = [], 0, False
    with np.load(FULL) as full, tarfile.open(args.archive, 'r|gz') as tf:
        for member in tf:
            if not member.isfile() or not member.name.endswith(('/d2.json', '/d3.json', '/d4.json')):
                continue
            raw = tf.extractfile(member).read()
            assert len(raw) == members[member.name]['size']
            assert hashlib.sha256(raw).hexdigest() == members[member.name]['sha256']
            original = json.loads(raw)
            ident = f'w{original["width"]}_r{original["rule"]:03d}_d{original["dimension"]}'
            path = out / (ident + '.npz')
            meta = out / (ident + '.json')
            if args.resume and meta.exists():
                result = json.loads(meta.read_text())
                assert result['archive_member_sha256'] == hashlib.sha256(raw).hexdigest()
                assert digest(path) == result['arrays_sha256']
                resumed += 1
            else:
                assert not path.exists() and not meta.exists(), 'Unregistered checkpoint requires explicit recovery'
                if time.perf_counter() - start > 1200:
                    timed_out = True
                    break
                case_start = time.perf_counter()
                result, arrays = audit_record(original, full)
                save_arrays(path, arrays)
                result.update({'id': ident, 'archive_member': member.name,
                               'archive_member_sha256': hashlib.sha256(raw).hexdigest(),
                               'arrays_file': str(path.relative_to(ROOT)), 'arrays_sha256': digest(path),
                               'arrays_bytes': path.stat().st_size, 'seconds': time.perf_counter() - case_start})
                save_json(meta, result)
            records.append(result)
            if len(records) % 24 == 0:
                print(json.dumps({'records': len(records), 'last': ident,
                                  'seconds': round(time.perf_counter() - start, 3),
                                  'last_free_fraction': result['contracts']['finite']['free_fraction']}), flush=True)
            assert resource.getrusage(resource.RUSAGE_SELF).ru_maxrss < 2 * 1024 * 1024, '2 GiB process-memory budget'
    result = {'source_hashes': hashes, 'raw_input_hashes': raw_inputs, 'controls': controls,
              'records': records, 'completed_records': len(records), 'expected_records': 1536,
              'resumed_records': resumed, 'censored_records': 1536 - len(records), 'budget_expired': timed_out,
              'seconds': time.perf_counter() - start,
              'peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'raw_arrays_bytes': sum(r['arrays_bytes'] for r in records)}
    assert timed_out or len(records) == 1536
    save_json(UNIT / ('partial-result.json' if timed_out else 'result.json'), result)
    print(json.dumps({k: v for k, v in result.items() if k not in ('records', 'source_hashes', 'raw_input_hashes')}), flush=True)


if __name__ == '__main__':
    main()
