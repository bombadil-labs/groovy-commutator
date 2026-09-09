#!/usr/bin/env python3
"""Exact class-blind fanout role-algebra census across all 256 ECAs."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np

RESULT = Path("results/eca_fanout_role_algebra_20260909.json")


def transition_table() -> np.ndarray:
    states = np.arange(256, dtype=np.uint16)
    bits = ((states[:, None] >> np.arange(8)) & 1).astype(np.uint8)
    addresses = 4 * np.roll(bits, 1, axis=1) + 2 * bits + np.roll(bits, -1, axis=1)
    weights = (1 << np.arange(8)).astype(np.uint16)
    table = np.empty((256, 256), dtype=np.uint16)
    for rule in range(256):
        out = ((rule >> addresses) & 1).astype(np.uint16)
        table[rule] = (out * weights).sum(axis=1)
    return table


def zero_commutator_rules(E: np.ndarray) -> list[int]:
    states = np.arange(256, dtype=np.uint16)
    out = []
    for rule in range(256):
        f = E[rule]
        derivative = states ^ f
        commutator = derivative[f] ^ E[rule, derivative]
        if np.all(commutator == 0):
            out.append(rule)
    return out


def main() -> None:
    E = transition_table()
    states = np.arange(256, dtype=np.uint16)
    encodings = [e for e in itertools.product((1, 2), repeat=3) if 1 in e and 2 in e]
    operations = [(q, mode) for q in range(3) for mode in (0, 1)]

    rows = []
    successful_rules = []

    for source in range(256):
        predecessor = states
        state = E[source, predecessor]
        derivative = predecessor ^ state
        next_state = E[source, state]
        next_derivative = state ^ next_state
        blocks = (np.full(256, source, dtype=np.uint16), state, derivative)
        current = {1: state, 2: derivative}
        target = {1: next_state, 2: next_derivative}

        allowed: dict[int, list[tuple[int, int]]] = {}
        for role in (1, 2):
            X = current[role]
            wanted = target[role]
            role_ops = []
            for q, mode in operations:
                evolved = E[blocks[q], X]
                output = evolved if mode == 0 else X ^ evolved
                if np.array_equal(output, wanted):
                    role_ops.append((q, mode))
            allowed[role] = role_ops

        success_count = 0
        successful_encodings = []
        for encoding in encodings:
            if not all(allowed[role] for role in encoding):
                continue
            count = 1
            for role in encoding:
                count *= len(allowed[role])
            success_count += count
            successful_encodings.append(
                {
                    "encoding": ["S" if role == 1 else "D" for role in encoding],
                    "candidate_count": count,
                }
            )

        if success_count:
            successful_rules.append(source)

        rows.append(
            {
                "source_rule": source,
                "successful_candidate_count": success_count,
                "state_role_operations": [
                    {"selector": q, "mode": "D" if mode else "E"} for q, mode in allowed[1]
                ],
                "derivative_role_operations": [
                    {"selector": q, "mode": "D" if mode else "E"} for q, mode in allowed[2]
                ],
                "successful_encodings": successful_encodings,
            }
        )

    expected = [0, 4, 51, 60, 90, 102, 150, 170, 200, 204, 240]
    assert successful_rules == expected

    zero_groovy = zero_commutator_rules(E)
    expected_zero = [0, 4, 60, 90, 102, 150, 170, 200, 204, 240]
    assert zero_groovy == expected_zero
    assert set(successful_rules) == set(zero_groovy) | {51}

    result = {
        "protocol": "docs/research/protocols/eca-fanout-role-algebra-20260909.md",
        "class_labels_loaded": False,
        "source_rules_checked": 256,
        "predecessor_states_per_source": 256,
        "candidate_algebras_per_source": 1296,
        "successful_source_count": len(successful_rules),
        "successful_sources": successful_rules,
        "zero_groovy_commutator_sources": zero_groovy,
        "fanout_equals_zero_commutator_union_rule51": True,
        "rules": rows,
    }
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "rules"}, indent=2))


if __name__ == "__main__":
    main()
