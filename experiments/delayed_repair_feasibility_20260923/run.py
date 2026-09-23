#!/usr/bin/env python3
"""Pinned exhaustive full-state control feasibility, no observer search."""
from __future__ import annotations

import argparse
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
TARGET = frozenset((273, 546, 1092, 1911, 2184, 3003, 3549, 3822))
PROTOCOL_COMMIT = '58ae1451e80b9f5565626f74f31b77cc85adba68'
SOURCES = (
    'experiments/delayed_repair_feasibility_20260923/run.py',
    'experiments/delayed_repair_feasibility_20260923/verify.py',
    'docs/research/protocols/delayed-repair-feasibility-20260923.md',
    'src/groovy/ca.py',
)


def step(s: int) -> int:
    left = ((s << 1) | (s >> (N - 1))) & MASK
    right = ((s >> 1) | (s << (N - 1))) & MASK
    # Rule 54: left=0 -> center XOR right; left=1 -> NOT center.
    return ((~left & (s ^ right)) | (left & ~s)) & MASK


def twice(s: int) -> int:
    return step(step(s))


def act(s: int, action: int) -> int:
    return s if action == 0 else s ^ (1 << (action - 1))


def evaluate() -> dict:
    assert len(TARGET) == 8
    assert all(step(s) in TARGET for s in TARGET)
    initial = sorted({s ^ (1 << j) for s in TARGET for j in range(N)} - TARGET)
    assert len(initial) == 96
    rows = []
    for s in initial:
        y = twice(s)
        wins = [action for action in range(N + 1) if twice(act(y, action)) in TARGET]
        outside = [action for action in wins if action and act(y, action) not in TARGET]
        static = [action for action in wins if act(y, action) in TARGET]
        rows.append({'initial': s, 'decision_state': y,
                     'passive': 0 in wins, 'winning_actions': wins,
                     'dynamic_flips': outside, 'static_actions': static})
    passive = sum(row['passive'] for row in rows)
    assert passive == 36, f'prior passive count disagrees: {passive}'
    fixed_scores = [sum(action in row['winning_actions'] for row in rows)
                    for action in range(N + 1)]
    fixed = max(fixed_scores)
    best_fixed = fixed_scores.index(fixed)
    full = sum(bool(row['winning_actions']) for row in rows)
    rescued = [row for row in rows if not row['passive'] and row['winning_actions']]
    dynamic_rescued = [row for row in rescued if row['dynamic_flips']]
    static_rescued = [row for row in rescued if row['static_actions']]
    dynamic_only = [row for row in dynamic_rescued if not row['static_actions']]
    witnesses = {}
    for label, pool, key in (('rescue', rescued, 'winning_actions'),
                             ('dynamic_rescue', dynamic_rescued, 'dynamic_flips'),
                             ('dynamic_only', dynamic_only, 'dynamic_flips')):
        if pool:
            row = pool[0]
            action = row[key][0]
            witnesses[label] = {'initial': row['initial'], 'decision_state': row['decision_state'],
                                'action': action, 'postaction': act(row['decision_state'], action),
                                'endpoint': twice(act(row['decision_state'], action))}
        else:
            witnesses[label] = None
    return {
        'contract': {'rule': 54, 'ring': N, 'target': sorted(TARGET), 'initial_count': len(initial),
                     'observe_after_steps': 2, 'endpoint_steps': 4,
                     'actions': 'noop 0; flip physical cell i for action i+1'},
        'rows': rows, 'distinct_decision_states': len({row['decision_state'] for row in rows}),
        'passive_successes': passive, 'fixed_scores': fixed_scores,
        'best_fixed_action': best_fixed, 'best_fixed_successes': fixed,
        'full_state_successes': full, 'rescued_count': len(rescued),
        'static_rescue_count': len(static_rescued),
        'dynamic_rescue_count': len(dynamic_rescued),
        'dynamic_only_count': len(dynamic_only), 'witnesses': witnesses,
        'predictions': {
            'P1': 'supported' if passive == 36 else 'failed',
            'P2': 'supported' if rescued else 'failed',
            'P3': 'supported' if dynamic_rescued else 'failed',
            'P4': 'supported' if full > fixed else 'failed',
        },
    }


def timeout(*_):
    raise TimeoutError('30-second evaluation wall cap')


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
            'prerequisite_result_sha256':
            '02213ca3dd688ca4c3451751b867f3310a63d65c6866a8f485cf370c00e3b2f1',
            'source_hashes': {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in SOURCES},
            'python': sys.version,
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
    print(json.dumps({k: result.get(k) for k in (
        'status', 'distinct_decision_states', 'passive_successes', 'best_fixed_action',
        'best_fixed_successes', 'full_state_successes', 'rescued_count',
        'static_rescue_count', 'dynamic_rescue_count', 'dynamic_only_count',
        'witnesses', 'predictions', 'elapsed_seconds')}, indent=2))
    return 0 if result['status'] == 'complete' else 1


if __name__ == '__main__':
    raise SystemExit(main())
