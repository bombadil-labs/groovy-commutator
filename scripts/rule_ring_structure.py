#!/usr/bin/env python3
"""Prospectively specified finite whole-state partition study; run off CI."""
from __future__ import annotations

import argparse
from collections import defaultdict, deque
from dataclasses import asdict
from functools import lru_cache
import importlib.util
import json
import math
from pathlib import Path
import resource
import signal
import time

import numpy as np

from rule_ring_selectors import (Case, atomic_json, canonical, compare, default_registry,
                                 pearson, sha256)

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / 'experiments/rule_ring_structure_20260915'
RULES = [0, 18, 30, 54, 90, 110, 126, 204]
HORIZONS = [1, 2, 4, 8, 16, 32]
OBSERVATIONS = [f'future_{t}' for t in HORIZONS] + ['basin', 'cycle_length', 'transient_depth']
CONTEXT = {'ensemble': 'all_binary_source_states', 'burn_in': 0, 'floor': 1,
           'cadence': 1, 'completion': 'full_ECA_rule', 'alignment': 'same_source_state',
           'study': 'rule-ring-structure-20260915/v1'}
SOURCES = ['scripts/rule_ring_structure.py', 'scripts/rule_ring_selectors.py',
           'src/groovy/ca.py', 'docs/research/protocols/rule-ring-structure-20260915.md']
spec = importlib.util.spec_from_file_location('study_ca', ROOT / 'src/groovy/ca.py')
ca = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ca)


def check_budget(start):
    if time.monotonic() - start > 600:
        raise TimeoutError('600-second stage budget exhausted')
    if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss > 2 * 1024 * 1024:
        raise MemoryError('2-GiB resident memory budget exhausted')


def successors(n, rule):
    ids = np.arange(1 << n, dtype=np.uint32)
    x = ((ids[:, None] >> np.arange(n)) & 1).astype(np.uint8)
    index = 4 * np.roll(x, 1, axis=1) + 2*x + np.roll(x, -1, axis=1)
    evolved = ca.rule_lut(rule)[index]
    for row in sorted({0, 1, (1 << n)//3, (1 << n)-1}):
        assert np.array_equal(evolved[row], ca.apply_rule(x[row], rule))
    return np.sum(evolved.astype(np.uint32) << np.arange(n), axis=1, dtype=np.uint32)


def graph_partitions(nxt):
    """Peel trees, label residual cycles, propagate labels in reverse order."""
    count = len(nxt)
    indegree = np.bincount(nxt, minlength=count).astype(np.int32)
    queue = deque(map(int, np.flatnonzero(indegree == 0)))
    removed = []
    while queue:
        node = queue.popleft()
        removed.append(node)
        target = int(nxt[node])
        indegree[target] -= 1
        if indegree[target] == 0:
            queue.append(target)
    basin = np.full(count, -1, np.int32)
    period = np.zeros(count, np.uint32)
    depth = np.zeros(count, np.uint32)
    for node in np.flatnonzero(indegree):
        node = int(node)
        if basin[node] >= 0:
            continue
        cycle = [node]
        current = int(nxt[node])
        while current != node:
            cycle.append(current)
            current = int(nxt[current])
        basin[cycle] = min(cycle)
        period[cycle] = len(cycle)
    for node in reversed(removed):
        target = int(nxt[node])
        basin[node], period[node], depth[node] = basin[target], period[target], depth[target] + 1
    assert np.all(basin >= 0) and np.all(period > 0)
    return {'basin': basin.astype(np.uint32), 'cycle_length': period, 'transient_depth': depth}


def entropy_counts(counts):
    counts = np.asarray(counts)
    p = counts[counts > 0] / counts.sum()
    return float(-np.sum(p * np.log2(p)))


def label_entropy(labels):
    return entropy_counts(np.bincount(labels.astype(np.int64)))


def generate_case(n, rule):
    nxt = successors(n, rule)
    labels = graph_partitions(nxt)
    current = np.arange(1 << n, dtype=np.uint32)
    for t in range(1, max(HORIZONS) + 1):
        current = nxt[current]
        if t in HORIZONS:
            labels[f'future_{t}'] = current.copy()
    for t in HORIZONS:
        if rule == 0:
            assert np.all(labels[f'future_{t}'] == 0)
        if rule == 204:
            assert np.array_equal(labels[f'future_{t}'], np.arange(1 << n))
    if rule == 90:
        assert bool(np.all(labels['future_16'] == 0)) == (n in (4, 8, 16))
    path = UNIT / 'partitions' / f'n{n:02d}_r{rule:03d}.npz'
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(f'refusing to overwrite an evaluated case: {path}')
    temporary = path.with_suffix('.tmp.npz')
    np.savez_compressed(temporary, successor=nxt, **labels)
    temporary.replace(path)
    digest = sha256(path)
    relative = str(path.relative_to(ROOT))
    cases = [Case(str(rule), n, observation,
                  {'path': relative, 'sha256': digest, 'key': observation, 'ring': n},
                  CONTEXT, f'{relative}#sha256={digest};{observation}') for observation in OBSERVATIONS]
    info = {'rule': rule, 'ring': n, 'states': 1 << n, 'path': relative, 'sha256': digest,
            'entropies': {name: label_entropy(labels[name]) for name in OBSERVATIONS},
            'blocks': {name: len(np.unique(labels[name])) for name in OBSERVATIONS},
            'max_transient': int(labels['transient_depth'].max()),
            'max_cycle_length': int(labels['cycle_length'].max())}
    return cases, info


@lru_cache(maxsize=128)
def load_partition(payload_json):
    payload = json.loads(payload_json)
    path = ROOT / payload['path']
    if sha256(path) != payload['sha256']:
        raise ValueError('partition input hash changed')
    with np.load(path, allow_pickle=False) as archive:
        labels = archive[payload['key']].copy()
    if labels.shape != (1 << payload['ring'],):
        raise ValueError('partition shape does not match ring')
    return labels, label_entropy(labels)


@lru_cache(maxsize=None)
def partition_relation_cached(a_json, b_json):
    a_meta, b_meta = json.loads(a_json), json.loads(b_json)
    if a_meta['ring'] != b_meta['ring']:
        raise ValueError('partition relations require a common source-state population')
    a, ha = load_partition(a_json)
    b, hb = load_partition(b_json)
    joint = a.astype(np.uint64) * (int(b.max()) + 1) + b
    _, counts = np.unique(joint, return_counts=True)
    hab = entropy_counts(counts)
    vi = 2*hab - ha - hb
    if not -1e-12 <= vi <= a_meta['ring'] + 1e-12:
        raise ArithmeticError('variation of information outside source entropy bound')
    vi = max(0., min(float(a_meta['ring']), vi))
    return {'h_a': ha, 'h_b': hb, 'h_joint': hab, 'vi': vi, 'vi_per_bit': vi/a_meta['ring']}


def partition_relation(a, b):
    return partition_relation_cached(canonical(a), canonical(b))


def relation_change(a, b):
    delta = b['vi_per_bit'] - a['vi_per_bit']
    return {'at_n': a['vi_per_bit'], 'at_m': b['vi_per_bit'],
            'change': delta, 'absolute_change': abs(delta)}


def query():
    return {'rules': [str(r) for r in RULES], 'max_comparisons': 20000,
            'ring': [{'name': 'arithmetic'}]
                    + [{'name': 'divisibility', 'id': f'div{d}', 'params': {'divisor': d}} for d in (2,3,4,5)]
                    + [{'name': 'valuation', 'id': f'v{p}', 'params': {'prime': p}} for p in (2,3,5)],
            'rule': [{'name': 'eca'}], 'relation': [{'name': 'partition_vi'}],
            'comparison': [{'name': 'vi_change'}]}


def ring_responses(report):
    grouped = defaultdict(list)
    for row in report['rows']:
        grouped[row['observation'], *row['rings']].append(row)
    out = []
    for (observation, n, m), rows in sorted(grouped.items()):
        assert len(rows) == 28
        out.append({'observation': observation, 'rings': [n, m], 'rule_pairs': 28,
                    'mean_absolute_change': math.fsum(r['scores']['absolute_change'] for r in rows)/28,
                    'ring_features': rows[0]['ring_features']})
    return out


def associations(responses, widths):
    out = []
    for observation in OBSERVATIONS:
        rows = [r for r in responses if r['observation'] == observation and set(r['rings']) <= set(widths)]
        for feature in sorted(rows[0]['ring_features']):
            value, reason = pearson([(r['ring_features'][feature], r['mean_absolute_change']) for r in rows])
            out.append({'observation': observation, 'feature': feature, 'pearson': value,
                        'undefined_reason': reason, 'ring_pairs': len(rows)})
    return out


def selection(associations_rows):
    out = []
    for observation in OBSERVATIONS:
        defined = [r for r in associations_rows if r['observation'] == observation and r['pearson'] is not None]
        defined.sort(key=lambda r: (-round(abs(r['pearson']), 12), r['feature']))
        out.extend(defined[:3])
    return out


def sign(value):
    return None if value is None or abs(value) <= 1e-12 else (1 if value > 0 else -1)


def execute(stage, start):
    frozen = json.loads((UNIT / 'implementation-freeze.json').read_text())
    actual = {name: sha256(ROOT / name) for name in SOURCES}
    if frozen['source_hashes'] != actual:
        raise ValueError('implementation changed after freeze')
    if (UNIT / f'{stage}-result.json').exists():
        raise FileExistsError('this stage already has a completed result')
    if stage == 'confirmation':
        seal = json.loads((UNIT / 'confirmation-seal.json').read_text())
        if seal['selection_sha256'] != sha256(UNIT / 'discovery-selection.json'):
            raise ValueError('discovery selection changed after sealing')
        if seal['discovery_result_sha256'] != sha256(UNIT / 'discovery-result.json'):
            raise ValueError('discovery result changed after sealing')
    cases, case_info = [], []
    widths = list(range(4, 13)) if stage == 'discovery' else list(range(13, 17))
    for n in widths:
        for rule in RULES:
            check_budget(start)
            rows, info = generate_case(n, rule)
            cases.extend(rows)
            case_info.append(info)
            atomic_json(UNIT / f'{stage}-progress.json', {'status': 'running', 'completed_cases': case_info})
        print(f'{stage}: ring {n} complete; {len(case_info)} rule/ring cases; {time.monotonic()-start:.2f}s', flush=True)
    atomic_json(UNIT / f'{stage}-cases.json', [asdict(c) for c in cases])
    if stage == 'confirmation':
        cases = [Case(**c) for c in json.loads((UNIT / 'discovery-cases.json').read_text())] + cases
    registry = default_registry()
    registry.add('relation', 'partition_vi', partition_relation)
    registry.add('comparison', 'vi_change', relation_change)
    check_budget(start)
    report = compare(cases, query(), registry)
    check_budget(start)
    atomic_json(UNIT / f'{stage}-evidence.json', report)
    responses = ring_responses(report)
    assoc = associations(responses, widths)
    result = {'status': 'complete', 'stage': stage, 'rules': RULES, 'widths': widths,
              'observations': OBSERVATIONS, 'case_info': case_info,
              'response_count': len(responses), 'comparison_count': report['comparison_count'],
              'associations': assoc, 'source_hashes': actual,
              'case_data_sha256': sha256(UNIT / f'{stage}-cases.json'),
              'evidence_sha256': sha256(UNIT / f'{stage}-evidence.json')}
    atomic_json(UNIT / f'{stage}-responses.json', responses)
    if stage == 'discovery':
        chosen = selection(assoc)
        atomic_json(UNIT / 'discovery-selection.json', chosen)
        result['selection_sha256'] = sha256(UNIT / 'discovery-selection.json')
    else:
        chosen = json.loads((UNIT / 'discovery-selection.json').read_text())
        by = {(r['observation'], r['feature']): r for r in assoc}
        result['selected_confirmation'] = []
        for row in chosen:
            other = by[row['observation'], row['feature']]
            a, b = sign(row['pearson']), sign(other['pearson'])
            result['selected_confirmation'].append({'observation': row['observation'], 'feature': row['feature'],
                'discovery_pearson': row['pearson'], 'confirmation_pearson': other['pearson'],
                'undefined_reason': other['undefined_reason'],
                'sign_agreement': None if a is None or b is None else a == b})
        result['seal'] = seal
    check_budget(start)
    atomic_json(UNIT / f'{stage}-result.json', result)
    atomic_json(UNIT / f'{stage}-progress.json', {'status': 'complete', 'completed_cases': case_info})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=['discovery', 'confirmation'])
    args = parser.parse_args()
    UNIT.mkdir(parents=True, exist_ok=True)
    def timeout(_signum, _frame):
        raise TimeoutError('600-second stage alarm')
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(600)
    # Address-space limit is an additional hard ceiling; RSS is recorded below.
    resource.setrlimit(resource.RLIMIT_AS, (2 * 1024**3, 2 * 1024**3))
    start = time.monotonic()
    execution = {'stage': args.stage, 'status': 'incomplete', 'numpy': np.__version__}
    try:
        execute(args.stage, start)
        execution['status'] = 'complete'
        execution['result_sha256'] = sha256(UNIT / f'{args.stage}-result.json')
    except Exception as error:
        execution['error'] = f'{type(error).__name__}: {error}'
        raise
    finally:
        signal.alarm(0)
        execution['wall_seconds'] = time.monotonic() - start
        execution['max_rss_kib'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        atomic_json(UNIT / f'{args.stage}-execution.json', execution)
        print(canonical(execution), flush=True)


if __name__ == '__main__':
    main()
