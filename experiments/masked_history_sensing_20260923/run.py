#!/usr/bin/env python3
"""Pinned exact known-erasure observation-fiber census on 52 Rule-54 sources."""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import signal
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
N = 12
MASK = (1 << N) - 1
PROTOCOL_COMMIT = '7aaaef3fee531df7e17988bacab00dd58b4bd596'
SOURCES = (
    'experiments/masked_history_sensing_20260923/run.py',
    'experiments/masked_history_sensing_20260923/verify.py',
    'docs/research/protocols/masked-history-sensing-20260923.md',
    'src/groovy/ca.py',
)


def step(s: int) -> int:
    l = ((s << 1) | (s >> (N - 1))) & MASK
    r = ((s >> 1) | (s << (N - 1))) & MASK
    return ((~l & (s ^ r)) | (l & ~s)) & MASK


def rotate(s: int) -> int:
    return ((s << 1) | (s >> (N - 1))) & MASK


def fixed_domain() -> tuple[set[int], list[int]]:
    stripe = sum(int(v) << i for i, v in enumerate('001100110011'))
    target = set()
    for _ in range(N):
        target.add(stripe)
        stripe = rotate(stripe)
    assert len(target) == 4
    domain = sorted(target | {s ^ (1 << i) for s in target for i in range(N)})
    assert len(domain) == 52
    return target, domain


def label(s: int, transition: list[int], target: set[int]) -> int:
    for _ in range(4):
        s = transition[s]
    return int(s in target)


def evaluate() -> dict:
    transition = [step(s) for s in range(1 << N)]
    target, domain = fixed_domain()
    assert all(transition[s] in target for s in target)
    outcomes = {s: label(s, transition, target) for s in domain}
    assert all(outcomes[s] == (s in target) for s in domain)
    histories = {}
    for s in domain:
        states = [s]
        for _ in range(2):
            states.append(transition[states[-1]])
        histories[s] = states
    rows = []
    for h in range(3):
        per_mask = []
        task_witnesses = []
        identity_witnesses = []
        for m in range(N):
            visible = MASK ^ (1 << m)
            fibers = defaultdict(list)
            for s in domain:
                fibers[tuple(histories[s][t] & visible for t in range(h + 1))].append(s)
            conflicting = [f for f in fibers.values() if len({outcomes[s] for s in f}) > 1]
            nonsingleton = [f for f in fibers.values() if len(f) > 1]
            per_mask.append({
                'mask': m, 'distinct_observations': len(fibers),
                'task_conflict_fibers': len(conflicting),
                'task_conflict_cases': sum(len(f) for f in conflicting),
                'source_conflict_fibers': len(nonsingleton),
                'source_conflict_cases': sum(len(f) for f in nonsingleton),
                'max_fiber_size': max(map(len, fibers.values())),
            })
            for f in conflicting:
                task_witnesses += [(m, a, b) for a in f for b in f
                                   if a < b and outcomes[a] != outcomes[b]]
            for f in nonsingleton:
                identity_witnesses += [(m, a, b) for a in f for b in f if a < b]

        def witness(items):
            if not items:
                return None
            m, a, b = min(items)
            split = next((t for t in range(h + 1, 3)
                          if (histories[a][t] ^ histories[b][t]) & (MASK ^ (1 << m))), None)
            return {'mask': m, 'sources': [a, b], 'labels': [outcomes[a], outcomes[b]],
                    'first_later_split': split}

        rows.append({
            'history_h': h, 'per_mask': per_mask,
            'distinct_observations': sum(v['distinct_observations'] for v in per_mask),
            'task_conflict_fibers': sum(v['task_conflict_fibers'] for v in per_mask),
            'task_conflict_cases': sum(v['task_conflict_cases'] for v in per_mask),
            'source_conflict_fibers': sum(v['source_conflict_fibers'] for v in per_mask),
            'source_conflict_cases': sum(v['source_conflict_cases'] for v in per_mask),
            'task_witness': witness(task_witnesses),
            'source_witness': witness(identity_witnesses),
            'observed_bits_per_case': 11 * (h + 1),
            'ca_steps_per_source': h,
        })
    first = {
        kind: [next((h for h in range(3) if rows[h]['per_mask'][m][kind] == 0), None)
               for m in range(N)]
        for kind in ('task_conflict_cases', 'source_conflict_cases')
    }
    return {
        'contract': {'rule': 54, 'ring': N, 'boundary': 'periodic',
                     'target': sorted(target), 'domain': domain, 'mask_known': True,
                     'observed_cell_count_per_snapshot': 11, 'task_endpoint': 4,
                     'history_horizons': [0, 1, 2]},
        'rows': rows, 'first_sufficient_history_by_mask': first,
        'predictions': {
            'P1': 'supported' if rows[0]['task_conflict_cases'] > 0
                  and rows[0]['source_conflict_cases'] > 0 else 'failed',
            'P2': 'supported' if 0 < rows[1]['task_conflict_cases']
                  < rows[0]['task_conflict_cases'] else 'failed',
            'P3': 'supported' if rows[2]['task_conflict_cases'] == 0 else 'failed',
            'P4': 'supported' if any(
                r['task_conflict_cases'] == 0 and r['source_conflict_cases'] > 0
                for row in rows for r in row['per_mask']) else 'failed',
        },
    }


def timeout(*_):
    raise TimeoutError('30-second masked-history evaluation cap')


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--implementation-commit', required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as out:
        result = {
            'created_utc': datetime.now(timezone.utc).isoformat(),
            'protocol_commit': PROTOCOL_COMMIT,
            'implementation_commit': args.implementation_commit,
            'source_hashes': {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
                              for p in SOURCES}, 'python': sys.version,
        }
        start = time.perf_counter()
        signal.signal(signal.SIGALRM, timeout)
        signal.alarm(30)
        try:
            result.update(evaluate(), status='complete')
        except Exception as exc:
            result.update(status='resource_limit' if isinstance(exc, TimeoutError) else 'invalid',
                          error={'type': type(exc).__name__, 'message': str(exc)},
                          predictions={f'P{i}': 'not_evaluated' for i in range(1, 5)})
        finally:
            signal.alarm(0)
        result['elapsed_seconds'] = time.perf_counter() - start
        json.dump(result, out, indent=2)
        out.write('\n')
    print(json.dumps({
        'status': result['status'],
        'counts_by_h': [{k: v for k, v in row.items() if k in (
            'history_h', 'task_conflict_cases', 'source_conflict_cases',
            'task_conflict_fibers', 'source_conflict_fibers')}
                        for row in result.get('rows', [])],
        'first_sufficient_history_by_mask': result.get('first_sufficient_history_by_mask'),
        'predictions': result['predictions'], 'elapsed_seconds': result['elapsed_seconds'],
    }, indent=2))
    return 0 if result['status'] == 'complete' else 1


if __name__ == '__main__':
    raise SystemExit(main())
