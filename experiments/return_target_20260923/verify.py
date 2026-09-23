#!/usr/bin/env python3
"""Independent scalar audit of the complete 12-cell Rule-54 preflight."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import signal
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from groovy.ca import apply_rule_int  # noqa: E402

N = 12
SIZE = 1 << N
SOURCES = (
    'experiments/return_target_20260923/run.py',
    'experiments/return_target_20260923/verify.py',
    'docs/research/protocols/return-target-eligibility-20260923.md',
    'src/groovy/ca.py',
)


def timeout(*_):
    raise TimeoutError('30-second scalar audit wall cap')


def cycles(transition: list[int]) -> dict[tuple[int, ...], int]:
    result = {}
    for initial in range(SIZE):
        visit_order = {}
        path = []
        s = initial
        while s not in visit_order:
            visit_order[s] = len(path)
            path.append(s)
            s = transition[s]
        cycle = path[visit_order[s]:]
        if len(cycle) < 2:
            continue
        target = set()
        for phase in cycle:
            for shift in range(N):
                target.add(sum(((phase >> i) & 1) << ((i + shift) % N) for i in range(N)))
        if len(target) == SIZE or 0 in target or SIZE - 1 in target:
            continue
        key = tuple(sorted(target))
        result[key] = min(result.get(key, SIZE + 1), len(cycle))
    return result


def return_time(s: int, target: set[int], transition: list[int]) -> int | None:
    visited = set()
    t = 0
    while s not in visited and s not in target:
        visited.add(s)
        s = transition[s]
        t += 1
    return t if s in target else None


def summarize(target: set[int], transition: list[int]) -> dict:
    injury = sorted({s ^ (1 << i) for i in range(N) for s in target} - target)
    times = {s: return_time(s, target, transition) for s in injury}
    early = [s for s in injury if times[s] is not None and times[s] <= 4]
    late = [s for s in injury if times[s] is not None and times[s] > 4]
    never = [s for s in injury if times[s] is None]
    return {
        'injuries': len(injury), 'early': len(early), 'late': len(late), 'never': len(never),
        'early_witness': {'state': min(early, key=lambda s: (times[s], s)),
                          'first_return': min(times[s] for s in early)} if early else None,
        'not_by_four_witness': {'state': min(late + never),
                                'first_return': times[min(late + never)]}
        if late or never else None,
    }


def audit(result: dict) -> None:
    assert result['status'] == 'complete'
    assert result['protocol_commit'] == 'b44a27ccfda26cb75421649512e27ad1e222cef5'
    assert set(result['predictions']) == {'P1', 'P2', 'P3'}
    for p in SOURCES:
        assert result['source_hashes'][p] == hashlib.sha256((ROOT / p).read_bytes()).hexdigest(), p
    trans = [apply_rule_int(s, N, 54) for s in range(SIZE)]
    assert result['transition_sha256'] == hashlib.sha256(
        json.dumps(trans, separators=(',', ':')).encode()).hexdigest()
    families = cycles(trans)
    assert result['candidate_sha256'] == hashlib.sha256(
        json.dumps(sorted(families), separators=(',', ':')).encode()).hexdigest()
    entries = []
    selected = None
    for states, period in sorted(families.items(), key=lambda item: (len(item[0]), item[1], item[0])):
        target = set(states)
        assert all(trans[s] in target for s in target)
        row = {'size': len(states), 'period': period, 'representative': states[0],
               **summarize(target, trans)}
        entries.append(row)
        if selected is None and row['early'] and row['late'] + row['never']:
            selected = {'states': list(states), **row}
    assert result['family_rows'] == entries
    assert result['selected'] == selected
    assert result['candidate_count'] == len(entries)
    assert result['some_early_count'] == sum(bool(row['early']) for row in entries)
    assert result['eligible_count'] == sum(
        bool(row['early'] and row['late'] + row['never']) for row in entries)
    bits = [int(b) for b in '001100110011']
    stripe = {sum(bits[(i + shift) % N] << i for i in range(N)) for shift in range(N)}
    assert result['old_stripe'] == {'states': sorted(stripe), **summarize(stripe, trans)}
    assert result['predictions'] == {
        'P1': 'supported' if result['old_stripe']['early'] == 0 else 'failed',
        'P2': 'supported' if result['some_early_count'] else 'failed',
        'P3': 'supported' if result['eligible_count'] else 'failed',
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('result', type=Path)
    args = ap.parse_args()
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(30)
    try:
        audit(json.loads(args.result.read_text()))
    finally:
        signal.alarm(0)
    print('Complete scalar transition, cycle-family and return-class audit: PASS')


if __name__ == '__main__':
    main()
