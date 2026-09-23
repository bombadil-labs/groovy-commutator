#!/usr/bin/env python3
"""Separate scalar and string-encoded audit of all masked history fibers."""
from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import signal
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from groovy.ca import apply_rule_int  # noqa: E402

N = 12
TARGET = {819, 1638, 2457, 3276}
SOURCES = (
    'experiments/masked_history_sensing_20260923/run.py',
    'experiments/masked_history_sensing_20260923/verify.py',
    'docs/research/protocols/masked-history-sensing-20260923.md',
    'src/groovy/ca.py',
)


def timeout(*_):
    raise TimeoutError('30-second scalar audit cap')


def visible_string(state: int, omitted: int) -> str:
    return ''.join(str((state >> i) & 1) for i in range(N) if i != omitted)


def audit(data: dict) -> None:
    assert data['status'] == 'complete'
    assert data['protocol_commit'] == '7aaaef3fee531df7e17988bacab00dd58b4bd596'
    for path in SOURCES:
        assert data['source_hashes'][path] == hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), path
    trans = [apply_rule_int(i, N, 54) for i in range(1 << N)]
    assert {trans[t] for t in TARGET} == TARGET
    domain = sorted(TARGET | {t ^ (1 << i) for t in TARGET for i in range(N)})
    assert len(domain) == 52
    labels = {s: int(trans[trans[trans[trans[s]]]] in TARGET) for s in domain}
    assert all(labels[s] == int(s in TARGET) for s in domain)
    assert data['contract'] == {
        'rule': 54, 'ring': N, 'boundary': 'periodic', 'target': sorted(TARGET),
        'domain': domain, 'mask_known': True,
        'observed_cell_count_per_snapshot': 11,
        'task_endpoint': 4, 'history_horizons': [0, 1, 2],
    }
    trace = {}
    for s in domain:
        trace[s] = (s, trans[s], trans[trans[s]])
    expected = []
    for h in range(3):
        per_mask = []
        task_pairs = []
        source_pairs = []
        for m in range(N):
            groups = defaultdict(list)
            for s in domain:
                groups[tuple(visible_string(trace[s][t], m) for t in range(h + 1))].append(s)
            disagreement = [g for g in groups.values() if len({labels[s] for s in g}) > 1]
            duplicates = [g for g in groups.values() if len(g) > 1]
            per_mask.append({
                'mask': m, 'distinct_observations': len(groups),
                'task_conflict_fibers': len(disagreement),
                'task_conflict_cases': sum(len(g) for g in disagreement),
                'source_conflict_fibers': len(duplicates),
                'source_conflict_cases': sum(len(g) for g in duplicates),
                'max_fiber_size': max(map(len, groups.values())),
            })
            for group in duplicates:
                for i, a in enumerate(group):
                    for b in group[i + 1:]:
                        source_pairs.append((m, a, b))
                        if labels[a] != labels[b]:
                            task_pairs.append((m, a, b))

        def witness(pairs):
            if not pairs:
                return None
            m, a, b = min(pairs)
            first = next((t for t in range(h + 1, 3)
                          if visible_string(trace[a][t], m) != visible_string(trace[b][t], m)), None)
            return {'mask': m, 'sources': [a, b], 'labels': [labels[a], labels[b]],
                    'first_later_split': first}

        expected.append({
            'history_h': h, 'per_mask': per_mask,
            'distinct_observations': sum(r['distinct_observations'] for r in per_mask),
            'task_conflict_fibers': sum(r['task_conflict_fibers'] for r in per_mask),
            'task_conflict_cases': sum(r['task_conflict_cases'] for r in per_mask),
            'source_conflict_fibers': sum(r['source_conflict_fibers'] for r in per_mask),
            'source_conflict_cases': sum(r['source_conflict_cases'] for r in per_mask),
            'task_witness': witness(task_pairs), 'source_witness': witness(source_pairs),
            'observed_bits_per_case': 11 * (h + 1), 'ca_steps_per_source': h,
        })
    assert data['rows'] == expected
    first = {kind: [next((h for h in range(3) if expected[h]['per_mask'][m][kind] == 0), None)
                    for m in range(N)] for kind in ('task_conflict_cases', 'source_conflict_cases')}
    assert data['first_sufficient_history_by_mask'] == first
    assert data['predictions'] == {
        'P1': 'supported' if expected[0]['task_conflict_cases'] > 0
              and expected[0]['source_conflict_cases'] > 0 else 'failed',
        'P2': 'supported' if 0 < expected[1]['task_conflict_cases']
              < expected[0]['task_conflict_cases'] else 'failed',
        'P3': 'supported' if expected[2]['task_conflict_cases'] == 0 else 'failed',
        'P4': 'supported' if any(r['task_conflict_cases'] == 0 and r['source_conflict_cases'] > 0
                                  for row in expected for r in row['per_mask']) else 'failed',
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('result', type=Path)
    args = parser.parse_args()
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(30)
    try:
        audit(json.loads(args.result.read_text()))
    finally:
        signal.alarm(0)
    print('All 4,096 scalar transitions and 624 source-mask fibers: PASS')


if __name__ == '__main__':
    main()
