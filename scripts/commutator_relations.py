#!/usr/bin/env python3
"""Frozen completion-independent relation quotient and address-transport audit.

No probabilities on completions: G=c XOR u[key], and a parity is fixed
exactly when its variable supports cancel. Science runs outside Actions.
"""
from __future__ import annotations

import argparse
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

import commutator_completion as previous

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / 'experiments/commutator_relations_20260915'
PANEL = (0, 4, 18, 30, 54, 90, 110, 124, 126, 137, 147, 193, 204)
PRIOR = ROOT / 'results/commutator_completion_20260915.json'
FULL = ROOT / 'experiments/beam_discriminator_loop_20260915/round01/tables.npz'
SOURCES = ('scripts/commutator_relations.py', 'scripts/commutator_completion.py',
           'experiments/commutator_relations_20260915/protocol.md',
           'experiments/commutator_relations_20260915/protocol-freeze.json',
           'experiments/commutator_relations_20260915/recovery.md')


def quotient_counts(row):
    w, m, u = row['width'], row['free_cells'], row['free_keys']
    e, o = (row['equal_G_pairs_from_shared_variable'],
            row['opposite_G_pairs_from_shared_variable'])
    numerator = 2 * e - m * (w - 1)
    assert m % w == 0 and numerator >= 0 and numerator % (2 * w * w) == 0
    assert o % (w * w) == 0
    assert m // w >= u
    return {'ambiguous_events': m // w, 'variables': u, 'rank': m // w - u,
            'equal_pairs': numerator // (2 * w * w), 'opposite_pairs': o // (w * w)}


def relation_counts(labels, constants):
    labels, constants = labels.ravel(), constants.ravel()
    take = labels > 0
    unique, inverse = np.unique(labels[take], return_inverse=True)
    n = np.bincount(inverse, minlength=len(unique)).astype(np.int64)
    one = np.bincount(inverse[constants[take] == 1], minlength=len(unique)).astype(np.int64)
    zero = n - one
    return {'events': len(labels), 'ambiguous_events': int(take.sum()),
            'variables': len(unique), 'rank': int(take.sum()) - len(unique),
            'equal_pairs': int(np.sum(zero * (zero - 1) // 2 + one * (one - 1) // 2)),
            'opposite_pairs': int(np.sum(zero * one)),
            'fixed_zero': int(np.sum(~take & (constants == 0))),
            'fixed_one': int(np.sum(~take & (constants == 1)))}


def full_state_quotient(grid):
    """Center entire Y at every transverse point, after longitudinal x=0.

    Byte keys are complete configurations, with fixed zero padding. np.unique
    compares exact bytes; no digest is used to decide equality.
    """
    phases = grid.shape[1:-1]
    row_bytes = (int(np.prod(grid.shape[1:])) + 7) // 8
    packed = np.empty((len(grid), *phases, row_bytes), np.uint8)
    for point in np.ndindex(phases):
        centered = np.roll(grid, tuple(-c for c in point), axis=tuple(range(1, grid.ndim - 1)))
        packed[(slice(None), *point, slice(None))] = np.packbits(centered.reshape(len(grid), -1), axis=1)
    keys = packed.reshape(-1, row_bytes).view(f'V{row_bytes}').ravel()
    _, reps, inverse = np.unique(keys, return_index=True, return_inverse=True)
    assert np.array_equal(keys, keys[reps][inverse])
    return inverse.reshape((len(grid), *phases)).astype(np.uint32), reps.astype(np.uint32)


def expression(labels, constants, phases):
    """Return canonical two-slot support for one bit or XOR of two bits."""
    parts = [labels[:, phase].reshape(-1) for phase in phases]
    const = constants[:, phases[0]].reshape(-1).copy()
    if len(phases) == 1:
        support = np.column_stack((np.zeros_like(parts[0]), parts[0]))
    else:
        assert len(phases) == 2
        const ^= constants[:, phases[1]].reshape(-1)
        support = np.sort(np.column_stack(parts), axis=1)
        support[support[:, 0] == support[:, 1]] = 0
    return support, const


def transfer_counts(parent_label, parent_const, support, child_const):
    """Count all same-parent-variable pairs without enumerating quadratically."""
    keep = parent_label > 0
    pl, pc, su, cc = parent_label[keep], parent_const[keep], support[keep], child_const[keep]
    counts = relation_counts(pl, pc)
    denominator = counts['equal_pairs'] + counts['opposite_pairs']
    matrix = np.column_stack((pl, su)).astype('<u4')
    _, inv = np.unique(matrix.view('V12').ravel(), return_inverse=True)
    n = np.bincount(inv).astype(np.int64)
    reverse_bit = pc ^ cc
    one = np.bincount(inv[reverse_bit == 1], minlength=len(n)).astype(np.int64)
    zero = n - one
    _, representatives = np.unique(inv, return_index=True)
    fixed = np.all(su[representatives] == 0, axis=1)
    result = {'eligible_pairs': denominator, 'status': 'ok' if denominator else 'not_applicable'}
    for name, mask in [('fixed', fixed), ('shared_nonempty', ~fixed)]:
        result[name + '_agree'] = int(np.sum((zero * (zero - 1) // 2 + one * (one - 1) // 2)[mask]))
        result[name + '_reverse'] = int(np.sum((zero * one)[mask]))
    result['surviving_pairs'] = sum(result[k] for k in ('fixed_agree', 'fixed_reverse', 'shared_nonempty_agree', 'shared_nonempty_reverse'))
    result['lost_pairs'] = denominator - result['surviving_pairs']
    assert result['lost_pairs'] >= 0
    result['survival_fraction'] = result['surviving_pairs'] / denominator if denominator else None
    # Retain exact representative-index witnesses of each nonempty outcome.
    examples = {}
    seen = {}
    original_indices = np.flatnonzero(keep)
    for i, group in enumerate(inv):
        by_bit = seen.setdefault(int(group), {})
        for bit, j in by_bit.items():
            category = ('fixed' if not np.any(su[i]) else 'shared_nonempty') + ('_agree' if bit == reverse_bit[i] else '_reverse')
            if category not in examples:
                examples[category] = {'parent_orbit_indices': [int(original_indices[j]), int(original_indices[i])],
                                     'parent_parity': int(pc[j] ^ pc[i]), 'child_parity': int(cc[j] ^ cc[i]),
                                     'child_support': su[i].tolist()}
        by_bit.setdefault(int(reverse_bit[i]), i)
    result['examples'] = examples
    return result


def synthetic_tests():
    l = np.array([1, 1, 1, 2, 2, 0], np.uint32)
    c = np.array([0, 0, 1, 0, 1, 1], np.uint8)
    base = relation_counts(l, c)
    for w in (2, 7, 8):
        rep = relation_counts(np.repeat(l, w), np.repeat(c, w))
        row = {'width': w, 'free_cells': rep['ambiguous_events'], 'free_keys': rep['variables'],
               'equal_G_pairs_from_shared_variable': rep['equal_pairs'],
               'opposite_G_pairs_from_shared_variable': rep['opposite_pairs']}
        assert quotient_counts(row) == {k: base[k] for k in quotient_counts(row)}
    supports = np.array([[0, 3], [0, 3], [0, 3], [0, 0], [0, 0], [0, 9]], np.uint32)
    cc = np.array([0, 1, 1, 0, 1, 0], np.uint8)
    result = transfer_counts(l, c, supports, cc)
    assert result['eligible_pairs'] == result['surviving_pairs'] == 4
    assert result['shared_nonempty_agree'] == 1 and result['shared_nonempty_reverse'] == 2
    assert result['fixed_agree'] == 1
    for assignments in itertools.product((0, 1), repeat=3):
        a = np.array((0, 0, 0) + assignments, np.uint8)
        g = cc[:5] ^ a[supports[:5, 0]] ^ a[supports[:5, 1]]
        assert int(g[0] ^ g[1]) == 1 and int(g[3] ^ g[4]) == 1
    sl = np.array([[[1, 2], [1, 0]]], np.uint32)
    sc = np.zeros_like(sl, np.uint8)
    s, _ = expression(sl, sc, (0, 1))
    assert s.tolist() == [[0, 0], [0, 2]]
    grid = np.array([[[1, 0, 0], [0, 1, 0]], [[0, 1, 0], [1, 0, 0]]], np.uint8)
    ids, reps = full_state_quotient(grid)
    assert len(reps) == 2 and ids[0, 0] == ids[1, 1] and ids[0, 1] == ids[1, 0]
    empty = transfer_counts(np.zeros(2, np.uint32), np.zeros(2, np.uint8), np.zeros((2, 2), np.uint32), np.zeros(2, np.uint8))
    assert empty['status'] == 'not_applicable' and empty['survival_fraction'] is None
    return {'translation_widths': [2, 7, 8], 'transfer_pairs': 4, 'whole_state_orbits': 2,
            'support_cancellation': True, 'zero_denominator_is_NA': True}


def selected_record(raw, full, expected):
    record = json.loads(raw)
    summary, arrays = previous.audit_record(record, full)
    shape = tuple(summary['shape'])
    grid = previous.unpack(record['grid_bits_big'], shape)
    orbit_ids, reps = full_state_quotient(grid)
    kept = {'grid_shape': np.asarray(shape, np.uint32), 'orbit_ids': orbit_ids,
            'orbit_representatives': reps}
    out = {'rule': summary['rule'], 'width': summary['width'], 'dimension': summary['dimension'],
           'events_x0': int(orbit_ids.size), 'full_spatial_orbits': len(reps), 'contracts': {}}
    for contract, stats in summary['contracts'].items():
        prior = expected[(summary['width'], summary['rule'], summary['dimension'], contract)]
        for k in ('cells', 'fixed_zero', 'fixed_one', 'free_cells', 'free_keys',
                  'equal_G_pairs_from_shared_variable', 'opposite_G_pairs_from_shared_variable'):
            assert stats[k] == prior[k], (contract, k, stats[k], prior[k])
        labels = arrays[contract + '_g_symbol'][..., 0]
        constants = np.unpackbits(arrays[contract + '_g_constant_bits'])[:int(np.prod(shape))].reshape(shape)[..., 0]
        longitudinal = relation_counts(labels, constants)
        assert all(longitudinal[k] == v for k, v in quotient_counts(prior).items())
        ll, cc = labels.ravel(), constants.ravel()
        assert np.array_equal(ll, ll[reps][orbit_ids.ravel()])
        assert np.array_equal(cc, cc[reps][orbit_ids.ravel()])
        spatial = relation_counts(ll[reps], cc[reps])
        blocks = labels.reshape(len(labels), 6, -1)
        free_count = np.sum(blocks > 0, axis=1)
        block_summary = {'all_free': int(np.sum(free_count == 6)),
                         'all_fixed': int(np.sum(free_count == 0)),
                         'mixed': int(np.sum((free_count > 0) & (free_count < 6)))}
        block_summary['distinct_ambiguous_variables_after_x0'] = longitudinal['rank'] == 0
        block_summary['sibling_nonconstant_readout_no_go_conditions'] = bool(
            longitudinal['rank'] == 0 and block_summary['mixed'] == 0 and block_summary['all_free'] > 0)
        out['contracts'][contract] = {'longitudinal': longitudinal, 'spatial': spatial, 'child_sibling_blocks': block_summary}
        kept[contract + '_symbol'] = labels.copy()
        kept[contract + '_constant'] = constants.copy()
    return out, kept


def transfer_record(parent, child, parent_meta):
    pids, reps = parent['orbit_ids'].ravel(), parent['orbit_representatives']
    n = int(parent['grid_shape'][0])
    child_ids = child['orbit_ids'].reshape(n, 6, -1)
    maps = []
    for phase in range(6):
        address = child_ids[:, phase].ravel()
        respects = np.array_equal(address, address[reps][pids])
        injective = len(np.unique(address[reps])) == len(reps)
        maps.append({'phase': phase, 'respects_quotient': bool(respects), 'injective': injective})
    out = {'rule': parent_meta['rule'], 'width': parent_meta['width'],
           'parent_dimension': parent_meta['dimension'], 'maps': maps, 'contracts': {}}
    cl = child['finite_symbol'].reshape(n, 6, -1)
    cc = child['finite_constant'].reshape(n, 6, -1)
    for contract in parent_meta['contracts']:
        pl = parent[contract + '_symbol'].ravel()[reps]
        pc = parent[contract + '_constant'].ravel()[reps]
        readouts = []
        for phases in [(p,) for p in range(6)] + [(4, 5)]:
            name = 'xor_4_5' if len(phases) == 2 else 'phase_' + str(phases[0])
            valid = all(maps[p]['respects_quotient'] and maps[p]['injective'] for p in phases)
            if valid:
                support, const = expression(cl, cc, phases)
                result = transfer_counts(pl, pc, support[reps], const[reps])
            else:
                result = {'status': 'invalid_address_map', 'survival_fraction': None}
            readouts.append({'readout': name, **result})
        out['contracts'][contract] = readouts
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--archive', type=Path)
    parser.add_argument('--manifest', type=Path)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    controls = synthetic_tests()
    if args.self_test:
        print(json.dumps(controls)); return
    assert args.archive and args.manifest
    assert not (UNIT / 'result.json').exists(), 'Do not overwrite completed output'
    prior = json.loads(PRIOR.read_text())
    assert previous.digest(ROOT / 'scripts/commutator_completion.py') == prior['source_hashes']['scripts/commutator_completion.py']
    inputs = {'results/commutator_completion_20260915.json': previous.digest(PRIOR),
              'uniform_jet6_rules.tar.gz': previous.digest(args.archive),
              'archive_manifest.json': previous.digest(args.manifest),
              str(FULL.relative_to(ROOT)): previous.digest(FULL)}
    for k, v in prior['raw_input_hashes'].items():
        assert inputs[k] == v, k
    manifest = json.loads(args.manifest.read_text())
    members = {m['path']: m for m in manifest['members']}
    source_hashes = {p: previous.digest(ROOT / p) for p in SOURCES}
    assert previous.digest(UNIT / 'protocol.md') == json.loads((UNIT / 'protocol-freeze.json').read_text())['protocol_sha256']
    freeze = {'source_hashes': source_hashes, 'input_hashes': inputs,
              'started_at': datetime.now(timezone.utc).isoformat(),
              'python': platform.python_version(), 'numpy': np.__version__}
    previous.save_json(UNIT / 'execution-freeze.json', freeze)
    start = time.perf_counter()
    census = [{k: r[k] for k in ('id', 'rule', 'width', 'dimension', 'contract')} | quotient_counts(r) for r in prior['records']]
    assert len(census) == 2048
    previous.save_json(UNIT / 'census.json', census)
    expected = {(r['width'], r['rule'], r['dimension'], r['contract']): r for r in prior['records']}
    records, censored = [], False
    directory = UNIT / 'records'; directory.mkdir(exist_ok=True)
    with np.load(FULL) as full, tarfile.open(args.archive, 'r|gz') as archive:
        for member in archive:
            if not member.isfile() or member.name not in members:
                continue
            raw = archive.extractfile(member).read()
            obj = json.loads(raw)
            if obj['rule'] not in PANEL:
                continue
            if time.perf_counter() - start > 600:
                censored = True; break
            assert len(raw) == members[member.name]['size']
            assert hashlib.sha256(raw).hexdigest() == members[member.name]['sha256']
            meta, arrays = selected_record(raw, full, expected)
            ident = f'w{meta["width"]}_r{meta["rule"]:03d}_d{meta["dimension"]}'
            path = directory / (ident + '.npz')
            previous.save_arrays(path, arrays)
            meta.update({'id': ident, 'archive_member': member.name,
                         'archive_member_sha256': hashlib.sha256(raw).hexdigest(),
                         'arrays_sha256': previous.digest(path), 'arrays_bytes': path.stat().st_size})
            previous.save_json(directory / (ident + '.json'), meta)
            records.append(meta)
            print(json.dumps({'records': len(records), 'last': ident, 'seconds': round(time.perf_counter() - start, 2),
                              'spatial_ranks': {k: v['spatial']['rank'] for k, v in meta['contracts'].items()}}), flush=True)
            assert resource.getrusage(resource.RUSAGE_SELF).ru_maxrss < 2 * 1024 * 1024
    indexed = {(r['width'], r['rule'], r['dimension']): r for r in records}
    transfers = []
    for width, rule, dimension in itertools.product((7, 8), PANEL, (2, 3)):
        if time.perf_counter() - start > 600:
            censored = True; break
        if (width, rule, dimension + 1) not in indexed or (width, rule, dimension) not in indexed:
            continue
        meta = indexed[width, rule, dimension]
        child_meta = indexed[width, rule, dimension + 1]
        with np.load(directory / (meta['id'] + '.npz')) as parent, np.load(directory / (child_meta['id'] + '.npz')) as child:
            transfers.append(transfer_record(parent, child, meta))
    result = {'source_hashes': source_hashes, 'input_hashes': inputs, 'controls': controls,
              'census': census, 'records': records, 'transfers': transfers,
              'completed_records': len(records), 'expected_records': 78,
              'completed_transfers': len(transfers), 'expected_transfers': 52,
              'budget_expired': censored, 'seconds': time.perf_counter() - start,
              'peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    assert censored or (len(records) == 78 and len(transfers) == 52)
    previous.save_json(UNIT / ('partial-result.json' if censored else 'result.json'), result)
    print(json.dumps({k: v for k, v in result.items() if k not in ('source_hashes', 'input_hashes', 'controls', 'census', 'records', 'transfers')}), flush=True)


if __name__ == '__main__':
    main()
