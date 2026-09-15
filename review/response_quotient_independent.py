#!/usr/bin/env python3
"""Independent, counter-based audit of the response quotient experiment.

This module does not import the author experiment or its metric functions.
Full experiment verification will read saved endpoint arrays, not evolve them.
"""

from __future__ import annotations

from collections import Counter
import base64
import difflib
import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
POLICIES = ('no_flip', 'flip', 'output_zero', 'output_one', 'hash1701', 'hash1702', 'hash1703', 'hash1704')
BANKS = {'all': tuple(range(8)), 'structured': tuple(range(4)), 'hash': tuple(range(4, 8))}


def entropy_counts(counts) -> float:
    counts = tuple(int(n) for n in counts if n)
    total = sum(counts)
    if total == 0:
        return 0.0
    return math.fsum((n / total) * math.log2(total / n) for n in counts)


def reference_metrics(endpoints: np.ndarray, width: int) -> dict:
    """Input axes: policy, source, known probe; each endpoint is an integer."""
    arr = np.asarray(endpoints)
    assert arr.ndim == 3
    bank, sources, probes = arr.shape
    assert sources == 1 << width
    signatures = [tuple(map(int, arr[p].flat)) for p in range(bank)]
    groups = []
    seen = {}
    for p, signature in enumerate(signatures):
        if signature not in seen:
            seen[signature] = len(groups)
            groups.append([])
        groups[seen[signature]].append(p)
    reps = [g[0] for g in groups]
    quotient = arr[reps]
    class_count = len(reps)
    diversity_terms = []
    mixture_terms = []
    known_terms = []
    raw_entropies = []
    for j in range(probes):
        mixture_terms.append(entropy_counts(Counter(map(int, quotient[:, :, j].flat)).values()))
        for s in range(sources):
            diversity_terms.append(entropy_counts(Counter(map(int, quotient[:, s, j])).values()))
        for a in range(class_count):
            known_terms.append(entropy_counts(Counter(map(int, quotient[a, :, j])).values()))
    for p in range(bank):
        raw_entropies.append(math.fsum(
            entropy_counts(Counter(map(int, arr[p, :, j])).values())
            for j in range(probes)
        ) / probes)
    response_entropy = math.fsum(diversity_terms) / (sources * probes)
    output_entropy = math.fsum(mixture_terms) / probes
    source_information = output_entropy - response_entropy
    known_retention = math.fsum(known_terms) / (class_count * probes * width)
    retention = source_information / width
    score = retention * response_entropy / math.log2(bank) if bank > 1 else 0.0
    assert -1e-12 <= retention <= 1 + 1e-12
    assert -1e-12 <= response_entropy <= math.log2(class_count) + 1e-12
    assert retention <= known_retention + 1e-12
    return {
        "bank_size": bank,
        "classes": groups,
        "class_count": class_count,
        "M": retention,
        "F": response_entropy,
        "T": score,
        "known_retention": known_retention,
        "output_entropy": output_entropy,
        "source_information": source_information,
        "per_policy_source_output_entropy": raw_entropies,
    }


def reference_key(grid: np.ndarray, row: int, col: int) -> int:
    """Explicit lexicographic tuple, first bit most significant."""
    rows, cols = grid.shape
    bits = tuple(
        int(grid[(row + dr) % rows, (col + dc) % cols])
        for dr in range(-3, 4)
        for dc in range(-2, 3)
    )
    return int("".join(map(str, bits)), 2)


def reference_keys(grid: np.ndarray) -> np.ndarray:
    """Independent direct sum of the 35 weighted translated binary fields."""
    values = np.zeros(grid.shape, dtype=np.uint64)
    for bit_index, (dr, dc) in enumerate(itertools.product(range(-3, 4), range(-2, 3))):
        translated = np.take(np.take(grid, (np.arange(grid.shape[-2]) + dr) % grid.shape[-2], axis=-2),
                             (np.arange(grid.shape[-1]) + dc) % grid.shape[-1], axis=-1)
        values += translated.astype(np.uint64) * np.uint64(1 << (34 - bit_index))
    return values


def reference_hash(key: int, seed: int) -> int:
    mask = (1 << 64) - 1
    x = ((key + seed) + 0x9E3779B97F4A7C15) & mask
    x = ((x ^ (x >> 30)) * 0xBF58476D1CE4E5B9) & mask
    x = ((x ^ (x >> 27)) * 0x94D049BB133111EB) & mask
    return (x ^ (x >> 31)) & 1


def reference_offbeam(key: int, policy: int) -> int:
    center = (key >> 17) & 1
    if policy == 0:
        return 0
    if policy == 1:
        return 1
    if policy == 2:
        return center
    if policy == 3:
        return 1 ^ center
    return reference_hash(key, 1701 + policy - 4)


def self_checks() -> dict:
    checks = {}
    identity = np.array([[[0], [1]], [[0], [1]]], dtype=np.uint64)
    m = reference_metrics(identity, 1)
    assert m["M"] == 1 and m["F"] == 0 and m["class_count"] == 1
    checks["duplicate_identity"] = True
    erase = np.array([[[0], [0]], [[0], [0]]], dtype=np.uint64)
    m = reference_metrics(erase, 1)
    assert m["M"] == 0 and m["F"] == 0
    checks["erasure"] = True
    xor = np.array([[[0], [1]], [[1], [0]]], dtype=np.uint64)
    m = reference_metrics(xor, 1)
    assert m["M"] == 0 and m["F"] == 1 and m["known_retention"] == 1
    checks["xor_nuisance"] = True
    # Two disjoint identity channels, plus an exact duplicate of the first.
    disjoint = np.array([[[0], [1]], [[2], [3]], [[0], [1]]], dtype=np.uint64)
    m = reference_metrics(disjoint, 1)
    assert m["M"] == 1 and m["F"] == 1 and m["class_count"] == 2
    assert abs(m["T"] - 1 / math.log2(3)) < 1e-15
    checks["fixed_bank_denominator"] = True
    # Collapse at individual probes is not enough to collapse endpoint maps.
    panel = np.array([
        [[0, 0], [1, 1]],
        [[0, 2], [1, 3]],
    ], dtype=np.uint64)
    m = reference_metrics(panel, 1)
    assert m["M"] == 1 and m["F"] == 0.5 and m["class_count"] == 2
    checks["entire_panel_quotient"] = True
    for dr in range(-3, 4):
        for dc in range(-2, 3):
            a = np.zeros((7, 5), dtype=np.uint8)
            a[(3 + dr) % 7, (2 + dc) % 5] = 1
            expected_bit = 34 - ((dr + 3) * 5 + dc + 2)
            assert reference_key(a, 3, 2) == 1 << expected_bit
    checks["lexicographic_key_bits"] = True
    assert reference_offbeam(1 << 17, 2) == 1
    assert reference_offbeam(1 << 17, 3) == 0
    checks["central_bit"] = True
    return checks


def production_controls() -> dict:
    """Small semantic comparisons only; no archived trajectory replay."""
    source = ROOT / 'scripts/response_quotient_20260915.py'
    spec = importlib.util.spec_from_file_location('response_author_controls', source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rng = np.random.default_rng(982361)
    checks = {}
    trials = []
    for width in (5, 7, 8):
        grid = rng.integers(0, 2, (6, width), dtype=np.uint8)
        expected = np.array([[reference_key(grid, r, c) for c in range(width)] for r in range(6)], dtype=np.uint64)
        assert np.array_equal(module.keys(grid), expected)
        assert np.array_equal(module.unpack_states(module.pack_states(grid), width), grid)
        key_bank = np.concatenate((expected.ravel(), np.array([0, 1 << 17, (1 << 35) - 1], dtype=np.uint64)))
        for p in range(8):
            assert module.off_mask(key_bank, p).tolist() == [reference_offbeam(int(k), p) for k in key_bank]
        trials.append(width)
    checks['tuple_neighborhoods_all_positions'] = trials
    checks['all_policy_masks_scalar'] = True
    checks['packed_endpoint_roundtrips'] = True
    grid = rng.integers(0, 2, (8, 1, 6, 7), dtype=np.uint8)
    forced = {reference_key(grid[0, 0], 0, 0): 1, reference_key(grid[1, 0], 2, 5): 0}
    sorted_keys = sorted(forced)
    table = (np.array(sorted_keys, dtype=np.uint64), np.array([forced[k] for k in sorted_keys], dtype=np.uint8))
    out = module.advance(grid, table)
    for p, r, c in itertools.product(range(8), range(6), range(7)):
        key = reference_key(grid[p, 0], r, c)
        expected = int(grid[p, 0, r, c]) ^ forced.get(key, reference_offbeam(key, p))
        assert int(out[p, 0, r, c]) == expected
    checks['one_step_mixed_forced_unforced'] = True
    for width, rule in itertools.product((3, 5), (0, 9, 30, 54, 73, 90, 110, 126, 170, 204)):
        expected = []
        for s in range(1 << width):
            bits = [int(x) for x in f'{s:0{width}b}']
            y = [((rule >> (4*bits[(i-1) % width] + 2*bits[i] + bits[(i+1) % width])) & 1) for i in range(width)]
            expected.append(int(''.join(map(str, y)), 2))
        assert module.source_successors(rule, width).tolist() == expected
    checks['eca_source_successor_scalar'] = 20
    # Distinct local keys represent repeated shared variables, not fresh coin flips.
    for variables in range(5):
        key_positions = [i for i in range(variables) for _ in range(i + 1)]
        values = set()
        for assignment in itertools.product((0, 1), repeat=variables):
            values.add(tuple(assignment[key] for key in key_positions))
        assert len(values) == 1 << variables
    checks['exact_one_step_injection'] = 5
    return checks


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reference_ranking(scores: dict, labels: dict) -> dict:
    positive = (54, 110)
    disputed = (41, 106)
    negative = [r for r in scores if r not in positive + disputed]
    c3 = [r for r in negative if labels[r] == 3]
    lower = min(scores[p] for p in positive)
    above = sorted((r for r in negative if scores[r] >= lower), key=lambda r: (-scores[r], r))
    def auc(group):
        total = 0
        for p in positive:
            for n in group:
                total += (2 if scores[p] > scores[n] else 1 if scores[p] == scores[n] else 0)
        return total / (2 * len(positive) * len(group))
    included = positive + tuple(negative)
    return dict(
        auc_all=auc(negative), auc_class3=auc(c3),
        clean_separation=not above,
        separation_margin=lower - max(scores[r] for r in negative),
        positive_scores={str(p): scores[p] for p in positive},
        positive_ranks={str(p): 1 + sum(scores[r] > scores[p] for r in included) +
                        (sum(scores[r] == scores[p] for r in included) - 1)/2 for p in positive},
        negatives_at_or_above_lower_positive=[dict(rule=r, class_label=labels[r], score=scores[r]) for r in above],
        disputed={str(r): scores[r] for r in disputed},
    )


def compare(left, right, path='', tolerance=2e-11):
    if isinstance(left, dict):
        assert left.keys() == right.keys(), (path, left.keys(), right.keys())
        for key in left:
            compare(left[key], right[key], f'{path}/{key}', tolerance)
    elif isinstance(left, list):
        assert len(left) == len(right), (path, len(left), len(right))
        for i, (a, b) in enumerate(zip(left, right)):
            compare(a, b, f'{path}/{i}', tolerance)
    elif isinstance(left, (float, np.floating)):
        assert abs(left - right) <= tolerance, (path, left, right)
    else:
        assert left == right, (path, left, right)


def audit_inputs_and_recovery() -> dict:
    start = time.perf_counter()
    data = json.loads((ROOT / 'results/response_quotient_20260915.json').read_text())
    run = ROOT / 'experiments/response_quotient_20260915/run'
    frozen_path = ROOT / data['reporting_recovery']['frozen_scientific_runner']
    current_path = ROOT / 'scripts/response_quotient_20260915.py'
    old, new = frozen_path.read_text(), current_path.read_text()
    old_line = "predictions[f'P3_w{w}_{p}_beats_{c}']=selected[p]['metrics']['4']['all']['score']>selected[c]['metrics']['4']['all']['score']"
    new_line = "predictions[f'P3_w{w}_{p}_beats_{c}']=bool(selected[p]['metrics']['4']['all']['score']>selected[c]['metrics']['4']['all']['score'])"
    old_locator = "input_record=f'w{w}/rule{r}/d2.json'"
    new_locator = "input_record=f'w{w}/rule{r:03d}/d2.json'"
    assert old.count(old_line) == 1 and old.count(old_locator) == 1
    assert old.replace(old_line, new_line).replace(old_locator, new_locator) == new
    assert file_hash(frozen_path) == data['execution']['source_hashes']['scripts/response_quotient_20260915.py']
    for path, digest in data['execution']['source_hashes'].items():
        target = frozen_path if path == 'scripts/response_quotient_20260915.py' else ROOT / path
        assert file_hash(target) == digest
    assert data['reporting_recovery']['regenerated_trajectories'] is False
    changed_lines = [line for line in difflib.unified_diff(old.splitlines(), new.splitlines())
                     if line[:1] in ('+', '-') and line[:3] not in ('+++', '---')]
    assert len(changed_lines) == 4
    total_probes, total_source_states = 0, 0
    max_u = 0
    locator_discrepancies = []
    for row in data['per_rule']:
        width, rule = row['width'], row['rule']
        record_path = f'w{width}/rule{rule:03d}/d2.json'
        assert record_path in data['execution']['input_record_sha256']
        assert record_path == row['input_record']
        historical = json.loads((run / 'rules' / f'w{width}_r{rule:03d}.json').read_text())['input_record']
        if record_path != historical:
            locator_discrepancies.append(dict(rule=rule, width=width, recorded=historical, resolved=record_path))
        record = json.loads((run / 'inputs' / record_path).read_text())
        assert record['rule'] == rule and record['width'] == width
        assert record['dimension'] == 2 and record['mode'] == 'jet6'
        assert record['radii_array_order'] == [3, 2]
        assert record['grid_shape'] == [1 << width, 6, width]
        encoded = np.frombuffer(base64.b64decode(record['grid_bits_big'], validate=True), dtype=np.uint8)
        grid_bits = np.unpackbits(encoded, bitorder='big')
        cells = (1 << width) * 6 * width
        assert not np.any(grid_bits[cells:])
        grid = grid_bits[:cells].reshape(1 << width, 6, width)
        source = np.array([[int(b) for b in f'{s:0{width}b}'] for s in range(1 << width)], dtype=np.uint8)
        assert np.array_equal(source, grid[:, 4] ^ grid[:, 5])
        beam_keys = reference_keys(grid)
        root_positions = np.frombuffer(base64.b64decode(record['representative_flat_indices_u32le'], validate=True), dtype='<u4')
        root_keys = beam_keys.flat[root_positions]
        assert len(root_keys) == len(set(map(int, root_keys))) == record['forced_root_count'] == row['forced_keys']
        assert set(map(int, beam_keys.flat)) == set(map(int, root_keys))
        derivative_raw = np.frombuffer(base64.b64decode(record['forced_derivative_bits_big'], validate=True), dtype=np.uint8)
        derivative_bits = np.unpackbits(derivative_raw, bitorder='big')
        assert not np.any(derivative_bits[len(root_keys):])
        forcing = {int(k): int(b) for k, b in zip(root_keys, derivative_bits)}
        flip = np.fromiter((forcing[int(k)] for k in beam_keys.flat), dtype=np.uint8).reshape(grid.shape)
        next_sources = []
        for bits in source:
            output = [int((rule >> (4*int(bits[(i-1) % width]) + 2*int(bits[i]) + int(bits[(i+1) % width]))) & 1)
                      for i in range(width)]
            next_sources.append(int(''.join(map(str, output)), 2))
        assert np.array_equal(grid ^ flip, grid[next_sources])
        probes = np.tile(grid[None], (6, 1, 1, 1))
        for j in range(6):
            probes[j, :, j, 0] ^= 1
        probe_keys = reference_keys(probes)
        expected_u = np.array([[len(set(map(int, probe_keys[j, s].flat)) - forcing.keys())
                                for s in range(1 << width)] for j in range(6)], dtype=np.uint8)
        with np.load(run / row['endpoints']['path'], allow_pickle=False) as arrays:
            assert np.array_equal(expected_u, arrays['unforced_distinct_keys']), (width, rule)
        assert int(expected_u.max()) <= 30
        max_u = max(max_u, int(expected_u.max()))
        total_probes += expected_u.size
        total_source_states += len(source)
    return dict(status='passed', input_records=176, exact_u_values_recomputed=total_probes,
                unperturbed_source_transitions_checked=total_source_states, maximum_u=max_u,
                source_decoder_recovered_all_states=True, invariant_family_control=True,
                historical_freeze_hash_matched=True, exact_reporting_only_diff=changed_lines,
                archived_locator_discrepancy_count=len(locator_discrepancies),
                locator_resolution='Use zero-padded paths in the SHA256 input manifest, preserving historical checkpoint labels.',
                elapsed_seconds=time.perf_counter()-start)


def audit_saved() -> dict:
    start = time.perf_counter()
    result_path = ROOT / 'results/response_quotient_20260915.json'
    data = json.loads(result_path.read_text())
    run = ROOT / 'experiments/response_quotient_20260915/run'
    assert data['status'] == 'complete' and len(data['per_rule']) == 176
    exact_sources = {}
    for relative, claimed in data['source_hashes'].items():
        actual = file_hash(ROOT / relative)
        assert actual == claimed, relative
        exact_sources[relative] = actual
    for relative, claimed in data['execution']['input_record_sha256'].items():
        assert file_hash(run / 'inputs' / relative) == claimed, relative
    labels = {int(k): v for k, v in data['class_by_representative'].items()}
    assert len(labels) == 88
    scores = {}
    maximum_delta = 0.0
    metric_comparisons = 0
    examples = []
    support_audit = dict(panels=0, probes=0, hash_structured_overlap_probes=0,
                         hash_noninjective_probes=0, quotient_nonfull_panels=0,
                         largest_affine_identity_error=0.0)
    for row_idx, row in enumerate(data['per_rule']):
        width, rule = row['width'], row['rule']
        assert rule in labels
        archive_path = run / row['endpoints']['path']
        assert file_hash(archive_path) == row['endpoints']['sha256']
        checkpoint = json.loads((run / 'rules' / f'w{width}_r{rule:03d}.json').read_text())
        checkpoint['input_record'] = f'w{width}/rule{rule:03d}/d2.json'
        assert checkpoint == row
        with np.load(archive_path, allow_pickle=False) as arrays:
            assert set(arrays.files) == {'unforced_distinct_keys', 'endpoint_t1', 'endpoint_t2', 'endpoint_t4', 'endpoint_t8'}
            u = arrays['unforced_distinct_keys']
            assert u.shape == (6, 1 << width) and np.issubdtype(u.dtype, np.integer)
            assert int(u.min()) >= 0 and int(u.max()) <= 30
            expected_u = dict(mean=float(u.mean()), minimum=int(u.min()), maximum=int(u.max()),
                              median=float(np.median(u)), positive_fraction=float(np.mean(u > 0)))
            compare(expected_u, row['exact_one_step_response_bits'])
            for horizon in (1, 2, 4, 8):
                endpoint = arrays[f'endpoint_t{horizon}']
                assert endpoint.shape == (8, 6, 1 << width) and endpoint.dtype == np.uint64
                assert not np.any(endpoint >> np.uint64(6*width))
                support_audit['panels'] += 1
                for j in range(6):
                    structured_support = set(map(int, endpoint[:4, j].flat))
                    hash_support = set(map(int, endpoint[4:, j].flat))
                    support_audit['probes'] += 1
                    support_audit['hash_structured_overlap_probes'] += int(bool(structured_support & hash_support))
                    support_audit['hash_noninjective_probes'] += int(len(hash_support) != 4 * (1 << width))
                for bank_name, indices in BANKS.items():
                    view = endpoint[list(indices)].transpose(0, 2, 1)
                    expected = reference_metrics(view, width)
                    support_audit['quotient_nonfull_panels'] += int(expected['class_count'] != len(indices))
                    declared = row['metrics'][str(horizon)][bank_name]
                    fields = {'score': expected['T'], 'retention': expected['M'], 'response_bits': expected['F'],
                              'known_completion_retention': expected['known_retention'], 'quotient_count': expected['class_count'],
                              'bank_size': expected['bank_size']}
                    for field, computed in fields.items():
                        delta = abs(computed - declared[field])
                        maximum_delta = max(maximum_delta, delta)
                        assert delta <= 2e-11, (width, rule, horizon, bank_name, field, computed, declared[field])
                        metric_comparisons += 1
                    original_index_classes = [[indices[p] for p in group] for group in expected['classes']]
                    assert original_index_classes == declared['quotient_classes']
                    per_policy = {POLICIES[p]: expected['per_policy_source_output_entropy'][i] / width for i, p in enumerate(indices)}
                    compare(per_policy, declared['retention_by_policy'])
                    for j in range(6):
                        # Crucially use the global quotient, not a separately reweighted
                        # per-probe quotient. Recompute with the original global reps.
                        reps = [g[0] for g in expected['classes']]
                        one_probe = view[reps, :, j]
                        f_probe = math.fsum(entropy_counts(Counter(map(int, one_probe[:, s])).values())
                                            for s in range(1 << width)) / (1 << width)
                        h_probe = entropy_counts(Counter(map(int, one_probe.flat)).values())
                        m_probe = (h_probe - f_probe)/width
                        assert abs(f_probe - declared['response_bits_by_probe'][j]) <= 2e-11
                        assert abs(m_probe - declared['retention_by_probe'][j]) <= 2e-11
                    for metric in ('score', 'retention', 'response_bits'):
                        scores.setdefault((width, horizon, bank_name, metric), {})[rule] = declared[metric]
                    if horizon == 4 and rule in (0, 9, 54, 73, 90, 110, 122, 126, 170, 204):
                        examples.append(dict(width=width, rule=rule, bank=bank_name, **fields))
                all_score = row['metrics'][str(horizon)]['all']['score']
                structured_score = row['metrics'][str(horizon)]['structured']['score']
                support_audit['largest_affine_identity_error'] = max(
                    support_audit['largest_affine_identity_error'], abs(all_score - (1 + structured_score) / 2))
        if (row_idx + 1) % 32 == 0:
            print(json.dumps(dict(audited_rows=row_idx+1, seconds=round(time.perf_counter()-start, 2))), flush=True)
    for key, score in scores.items():
        width, horizon, bank, metric = key
        assert len(score) == 88
        expected = reference_ranking(score, labels)
        compare(expected, data['reports'][str(width)][str(horizon)][bank][metric])
    predictions = {}
    by_rule_width = {(row['width'], row['rule']): row for row in data['per_rule']}
    for width in (7, 8):
        predictions[f'P1_w{width}_unperturbed'] = all(by_rule_width[width, r]['on_beam_control'] for r in labels)
        predictions[f'P2_w{width}_clean'] = reference_ranking(scores[width, 4, 'all', 'score'], labels)['clean_separation']
        for bank in ('structured', 'hash'):
            predictions[f'P4_w{width}_{bank}_clean'] = reference_ranking(scores[width, 4, bank, 'score'], labels)['clean_separation']
        for positive, control in itertools.product((54, 110), (0, 1, 15, 51, 60, 90, 105, 150, 170, 204)):
            candidate_scores = scores[width, 4, 'all', 'score']
            predictions[f'P3_w{width}_{positive}_beats_{control}'] = candidate_scores[positive] > candidate_scores[control]
    compare(predictions, data['predictions'])
    return dict(
        status='passed', result_sha256=file_hash(result_path), source_hashes=exact_sources,
        saved_rows_audited=176, endpoint_panels_audited=704, metric_sets_audited=2112,
        scalar_metric_comparisons=metric_comparisons, largest_absolute_metric_difference=maximum_delta,
        input_records_hashed=len(data['execution']['input_record_sha256']),
        support_audit=support_audit,
        hypotheses=predictions, examples=examples,
        elapsed_seconds=time.perf_counter()-start,
        limitations=['Audit recomputes all metrics from saved endpoints; it is not a full trajectory replay.',
                     'Uniformity over panel-equivalence classes is a declared prior and differs among rules, banks, and horizons.',
                     'One-cell probes are periodic defects on the 6 by W torus.'],
    )


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--audit', action='store_true')
    args = parser.parse_args()
    report = {'self_checks': self_checks(), 'production_semantic_controls': production_controls()}
    if args.audit:
        report['saved_endpoint_audit'] = audit_saved()
        report['input_and_reporting_audit'] = audit_inputs_and_recovery()
        out = ROOT / 'review/response_quotient_independent.json'
        out.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, indent=2))
