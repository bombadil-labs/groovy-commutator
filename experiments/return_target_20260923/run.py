#!/usr/bin/env python3
"""Frozen Rule-54 target-eligibility preflight; no observer search."""
from __future__ import annotations

import argparse
from collections import deque
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import signal
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
N = 12
SIZE = 1 << N
MASK = SIZE - 1
PROTOCOL_COMMIT = 'b44a27ccfda26cb75421649512e27ad1e222cef5'
SOURCES = (
    'experiments/return_target_20260923/run.py',
    'experiments/return_target_20260923/verify.py',
    'docs/research/protocols/return-target-eligibility-20260923.md',
    'src/groovy/ca.py',
)


def step(s: int) -> int:
    """Independent bit arithmetic for synchronous Rule 54, periodic n=12."""
    left = ((s << 1) | (s >> (N - 1))) & MASK
    right = ((s >> 1) | (s << (N - 1))) & MASK
    return ((~left & (s ^ right)) | (left & ~s)) & MASK


def rotate(s: int) -> int:
    return ((s << 1) | (s >> (N - 1))) & MASK


def candidates(transition: list[int]) -> dict[tuple[int, ...], int]:
    visited: set[int] = set()
    targets: dict[tuple[int, ...], int] = {}
    for initial in range(SIZE):
        if initial in visited:
            continue
        trail: list[int] = []
        seen: dict[int, int] = {}
        s = initial
        while s not in visited and s not in seen:
            seen[s] = len(trail)
            trail.append(s)
            s = transition[s]
        if s in seen:
            cycle = trail[seen[s]:]
            if len(cycle) >= 2:
                closure: set[int] = set()
                for phase in cycle:
                    rotated = phase
                    for _ in range(N):
                        closure.add(rotated)
                        rotated = rotate(rotated)
                if len(closure) < SIZE and 0 not in closure and MASK not in closure:
                    key = tuple(sorted(closure))
                    targets[key] = min(targets.get(key, SIZE + 1), len(cycle))
        visited.update(trail)
    return targets


def injury_set(target: set[int]) -> set[int]:
    return {s ^ (1 << i) for s in target for i in range(N)} - target


def distances(target: set[int], reverse: list[list[int]]) -> list[int | None]:
    """First target-hit distance by backwards breadth-first search."""
    d: list[int | None] = [None] * SIZE
    q = deque(sorted(target))
    for s in q:
        d[s] = 0
    while q:
        s = q.popleft()
        for predecessor in reverse[s]:
            if d[predecessor] is None:
                d[predecessor] = d[s] + 1
                q.append(predecessor)
    return d


def summary(target: set[int], reverse: list[list[int]]) -> dict:
    d = distances(target, reverse)
    injuries = sorted(injury_set(target))
    early = [s for s in injuries if d[s] is not None and d[s] <= 4]
    late = [s for s in injuries if d[s] is not None and d[s] > 4]
    never = [s for s in injuries if d[s] is None]
    return {
        'injuries': len(injuries), 'early': len(early),
        'late': len(late), 'never': len(never),
        'early_witness': {'state': min(early, key=lambda s: (d[s], s)),
                          'first_return': min(d[s] for s in early)} if early else None,
        'not_by_four_witness': (
            {'state': min(late + never), 'first_return': d[min(late + never)]}
            if late or never else None),
    }


def evaluate() -> dict:
    transition = [step(s) for s in range(SIZE)]
    reverse: list[list[int]] = [[] for _ in range(SIZE)]
    for s, successor in enumerate(transition):
        reverse[successor].append(s)
    families = candidates(transition)
    rows = []
    eligible_targets = []
    for target, period in sorted(families.items(), key=lambda item: (len(item[0]), item[1], item[0])):
        stat = summary(set(target), reverse)
        row = {'size': len(target), 'period': period, 'representative': target[0], **stat}
        rows.append(row)
        if row['early'] and row['late'] + row['never']:
            eligible_targets.append((target, row))
    selected_target, selected_row = eligible_targets[0] if eligible_targets else (None, None)
    stripe = {sum(int(b) << i for i, b in enumerate('001100110011'[k:] + '001100110011'[:k]))
              for k in range(12)}
    stripe_stat = summary(stripe, reverse)
    return {
        'transition_sha256': hashlib.sha256(json.dumps(transition, separators=(',', ':')).encode()).hexdigest(),
        'candidate_sha256': hashlib.sha256(json.dumps(sorted(families), separators=(',', ':')).encode()).hexdigest(),
        'candidate_count': len(rows),
        'some_early_count': sum(bool(r['early']) for r in rows),
        'eligible_count': len(eligible_targets),
        'family_rows': rows,
        'selected': {'states': list(selected_target), **selected_row} if selected_row else None,
        'old_stripe': {'states': sorted(stripe), **stripe_stat},
        'predictions': {
            'P1': 'supported' if stripe_stat['early'] == 0 else 'failed',
            'P2': 'supported' if any(r['early'] for r in rows) else 'failed',
            'P3': 'supported' if eligible_targets else 'failed',
        },
    }


def timeout(*_):
    raise TimeoutError('30-second evaluation wall cap')


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--implementation-commit', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as out:
        result = {
            'created_utc': datetime.now(timezone.utc).isoformat(),
            'implementation_commit': args.implementation_commit,
            'protocol_commit': PROTOCOL_COMMIT,
            'source_hashes': {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in SOURCES},
            'contract': {'rule': 54, 'ring': N, 'boundary': 'periodic', 'injury_bits': 1,
                         'passive_return_horizon': 4},
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
                          predictions={f'P{i}': 'not_evaluated' for i in range(1, 4)})
        finally:
            signal.alarm(0)
        result['elapsed_seconds'] = time.perf_counter() - start
        json.dump(result, out, indent=2)
        out.write('\n')
    print(json.dumps({k: result.get(k) for k in (
        'status', 'candidate_count', 'some_early_count', 'eligible_count', 'selected',
        'old_stripe', 'predictions', 'elapsed_seconds')}, indent=2))
    return 0 if result['status'] == 'complete' else 1


if __name__ == '__main__':
    raise SystemExit(main())
