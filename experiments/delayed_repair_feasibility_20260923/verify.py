#!/usr/bin/env python3
"""Separate scalar replay of all interventions under the frozen contract."""
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
TARGET = {273, 546, 1092, 1911, 2184, 3003, 3549, 3822}
SOURCES = (
    'experiments/delayed_repair_feasibility_20260923/run.py',
    'experiments/delayed_repair_feasibility_20260923/verify.py',
    'docs/research/protocols/delayed-repair-feasibility-20260923.md',
    'src/groovy/ca.py',
)


def timeout(*_):
    raise TimeoutError('30-second scalar audit wall cap')


def replay(result: dict) -> None:
    assert result['status'] == 'complete'
    assert result['protocol_commit'] == '58ae1451e80b9f5565626f74f31b77cc85adba68'
    assert set(result['predictions']) == {'P1', 'P2', 'P3', 'P4'}
    for p in SOURCES:
        assert result['source_hashes'][p] == hashlib.sha256((ROOT / p).read_bytes()).hexdigest(), p
    transition = [apply_rule_int(s, N, 54) for s in range(1 << N)]
    assert len(TARGET) == 8 and all(transition[t] in TARGET for t in TARGET)
    initial = sorted({t ^ (1 << j) for t in TARGET for j in range(N)} - TARGET)
    assert len(initial) == 96
    assert result['contract'] == {
        'rule': 54, 'ring': 12, 'target': sorted(TARGET), 'initial_count': 96,
        'observe_after_steps': 2, 'endpoint_steps': 4,
        'actions': 'noop 0; flip physical cell i for action i+1',
    }
    by_state = {}
    rows = []
    for s in initial:
        y = transition[transition[s]]
        wins = []
        outside = []
        static = []
        for action in range(13):
            changed = y if action == 0 else y ^ (1 << (action - 1))
            endpoint = transition[transition[changed]]
            if endpoint not in TARGET:
                continue
            wins.append(action)
            if changed in TARGET:
                static.append(action)
            elif action != 0:
                outside.append(action)
        row = {'initial': s, 'decision_state': y, 'passive': 0 in wins,
               'winning_actions': wins, 'dynamic_flips': outside,
               'static_actions': static}
        if y in by_state:
            assert by_state[y] == (wins, outside, static), 'same observation has different actions'
        by_state[y] = (wins, outside, static)
        rows.append(row)
    assert result['rows'] == rows
    passive = sum(r['passive'] for r in rows)
    assert passive == 36 and result['passive_successes'] == passive
    fixed = [sum(action in row['winning_actions'] for row in rows) for action in range(13)]
    assert result['fixed_scores'] == fixed
    assert (result['best_fixed_action'], result['best_fixed_successes']) == (
        fixed.index(max(fixed)), max(fixed))
    full = sum(bool(row['winning_actions']) for row in rows)
    assert result['full_state_successes'] == full
    assert result['distinct_decision_states'] == len(by_state)
    rescued = [r for r in rows if not r['passive'] and r['winning_actions']]
    dynamic = [r for r in rescued if r['dynamic_flips']]
    static = [r for r in rescued if r['static_actions']]
    dynamic_only = [r for r in dynamic if not r['static_actions']]
    assert (result['rescued_count'], result['static_rescue_count'],
            result['dynamic_rescue_count'], result['dynamic_only_count']) == (
                len(rescued), len(static), len(dynamic), len(dynamic_only))
    assert result['predictions'] == {
        'P1': 'supported' if passive == 36 else 'failed',
        'P2': 'supported' if rescued else 'failed',
        'P3': 'supported' if dynamic else 'failed',
        'P4': 'supported' if full > max(fixed) else 'failed',
    }
    for label, pool, actions_key in (
        ('rescue', rescued, 'winning_actions'),
        ('dynamic_rescue', dynamic, 'dynamic_flips'),
        ('dynamic_only', dynamic_only, 'dynamic_flips'),
    ):
        witness = result['witnesses'][label]
        if not pool:
            assert witness is None
            continue
        row = pool[0]
        action = row[actions_key][0]
        changed = row['decision_state'] if action == 0 else row['decision_state'] ^ (1 << (action - 1))
        assert witness == {'initial': row['initial'], 'decision_state': row['decision_state'],
                           'action': action, 'postaction': changed,
                           'endpoint': transition[transition[changed]]}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('result', type=Path)
    args = ap.parse_args()
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(30)
    try:
        replay(json.loads(args.result.read_text()))
    finally:
        signal.alarm(0)
    print('96 sources x 13 actions, scalar transition and policy audit: PASS')


if __name__ == '__main__':
    main()
