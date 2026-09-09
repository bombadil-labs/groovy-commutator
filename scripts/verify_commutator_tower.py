#!/usr/bin/env python3
"""Exact class-blind iterated commutator tower census on the 8-cell ECA substrate."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import numpy as np

RESULT = Path("results/commutator_tower_20260909.json")
HORIZON = 256


def transition_table() -> np.ndarray:
    states = np.arange(256, dtype=np.uint16)
    bits = ((states[:, None] >> np.arange(8)) & 1).astype(np.uint8)
    addresses = 4 * np.roll(bits, 1, axis=1) + 2 * bits + np.roll(bits, -1, axis=1)
    weights = (1 << np.arange(8)).astype(np.uint16)
    table = np.empty((256, 256), dtype=np.uint16)
    for rule in range(256):
        output = ((rule >> addresses) & 1).astype(np.uint16)
        table[rule] = (output * weights).sum(axis=1)
    return table


def main() -> None:
    E = transition_table()
    states = np.arange(256, dtype=np.uint16)
    rows = []
    censored_rules = []
    signature_counts = Counter()

    for rule in range(256):
        f = E[rule]
        current = states ^ f  # A1 = derivative
        seen: dict[bytes, int] = {}
        first_zero = None
        first_constant = None
        repeat = None
        image_sizes = []
        nonzero_counts = []

        for level in range(1, HORIZON + 1):
            key = current.tobytes()
            if key in seen:
                repeat = (seen[key], level)
                break
            seen[key] = level

            if first_zero is None and np.all(current == 0):
                first_zero = level
            if first_constant is None and np.all(current == current[0]):
                first_constant = level

            image_sizes.append(int(len(np.unique(current))))
            nonzero_counts.append(int(np.count_nonzero(current)))
            current = current[f] ^ f[current]

        if repeat is None:
            censored_rules.append(rule)
            preperiod = None
            period = None
        else:
            preperiod = repeat[0] - 1
            period = repeat[1] - repeat[0]

        signature = (
            first_zero,
            first_constant,
            preperiod,
            period,
            tuple(image_sizes[:16]),
            tuple(nonzero_counts[:16]),
        )
        signature_counts[signature] += 1

        rows.append(
            {
                "rule": rule,
                "first_zero_level": first_zero,
                "first_constant_level": first_constant,
                "first_repeat": list(repeat) if repeat else None,
                "repeat_preperiod": preperiod,
                "repeat_period": period,
                "distinct_maps_before_repeat_or_horizon": len(seen),
                "right_censored_at_horizon": repeat is None,
                "image_sizes": image_sizes,
                "nonzero_state_counts": nonzero_counts,
            }
        )

    zero_a2 = [row["rule"] for row in rows if row["first_zero_level"] == 2]
    expected_zero_a2 = [0, 4, 60, 90, 102, 150, 170, 200, 240]
    # Rule 204 has A1=0 already and therefore first_zero_level=1.
    assert zero_a2 == expected_zero_a2
    assert rows[204]["first_zero_level"] == 1

    result = {
        "protocol": "docs/research/protocols/commutator-tower-20260909.md",
        "class_labels_loaded": False,
        "horizon": HORIZON,
        "rules_checked": 256,
        "right_censored_rule_count": len(censored_rules),
        "right_censored_rules": censored_rules,
        "distinct_complete_signatures": len(signature_counts),
        "rules": rows,
    }
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "rules"}, indent=2))


if __name__ == "__main__":
    main()
