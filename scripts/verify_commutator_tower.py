#!/usr/bin/env python3
"""Exact all-ECA census of the preregistered commutator correction tower.

This instrument intentionally contains no Wolfram class labels.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results"
FULL_RESULT = OUT / "commutator_tower_20260909.json"
SUMMARY_RESULT = OUT / "commutator_tower_20260909_summary.json"
HORIZON = 256
WIDTH = 8
ZERO_COMMUTATOR_CONTROL = [0, 4, 60, 90, 102, 150, 170, 200, 204, 240]


def scalar_step(rule: int, state: int, width: int = WIDTH) -> int:
    """Direct periodic ECA step; bit i is cell i."""
    out = 0
    for i in range(width):
        left = (state >> ((i - 1) % width)) & 1
        center = (state >> i) & 1
        right = (state >> ((i + 1) % width)) & 1
        address = (left << 2) | (center << 1) | right
        out |= ((rule >> address) & 1) << i
    return out


def vector_step_map(rule: int, width: int = WIDTH) -> np.ndarray:
    """All-state map for one ECA rule."""
    states = np.arange(1 << width, dtype=np.uint16)
    bits = ((states[:, None] >> np.arange(width)) & 1).astype(np.uint8)
    address = (
        4 * np.roll(bits, 1, axis=1)
        + 2 * bits
        + np.roll(bits, -1, axis=1)
    )
    out_bits = ((rule >> address) & 1).astype(np.uint16)
    weights = (1 << np.arange(width)).astype(np.uint16)
    return (out_bits * weights).sum(axis=1).astype(np.uint16)


def tower(rule: int) -> dict[str, object]:
    states = np.arange(1 << WIDTH, dtype=np.uint16)
    f = vector_step_map(rule)

    # Independent scalar/vector check over the complete finite state space.
    scalar = np.array([scalar_step(rule, int(s)) for s in states], dtype=np.uint16)
    assert np.array_equal(f, scalar)

    a = states ^ f  # A1 = derivative
    maps: list[np.ndarray] = []
    keys: list[bytes] = []

    for _level in range(1, HORIZON + 1):
        maps.append(a.copy())
        keys.append(a.tobytes())
        a = a[f] ^ f[a]

    first_zero = None
    first_constant = None
    image_sizes: list[int] = []
    nonzero_counts: list[int] = []
    constant_values: list[int | None] = []

    for level, a in enumerate(maps, start=1):
        nonzero = int(np.count_nonzero(a))
        image_size = int(len(np.unique(a)))
        is_constant = bool(np.all(a == a[0]))
        if first_zero is None and nonzero == 0:
            first_zero = level
        if first_constant is None and is_constant:
            first_constant = level
        image_sizes.append(image_size)
        nonzero_counts.append(nonzero)
        constant_values.append(int(a[0]) if is_constant else None)

    # "Lexicographically earliest pair j < k" from the frozen protocol.
    positions: dict[bytes, list[int]] = defaultdict(list)
    for level, key in enumerate(keys, start=1):
        positions[key].append(level)
    repeated_pairs = [
        (levels[0], levels[1])
        for levels in positions.values()
        if len(levels) >= 2
    ]
    first_repeat = min(repeated_pairs) if repeated_pairs else None

    if first_repeat is None:
        repeat_type = None
        preperiod = None
        period = None
    else:
        j, k = first_repeat
        preperiod = j - 1
        period = k - j
        cycle_entry = maps[j - 1]
        if period == 1 and np.count_nonzero(cycle_entry) == 0:
            repeat_type = "zero_tail"
        elif period == 1:
            repeat_type = "fixed_point"
        else:
            repeat_type = "cycle"

        # Determinism audit: the observed recurrence must persist thereafter
        # throughout the frozen horizon.
        for level in range(j, HORIZON - period + 1):
            assert keys[level - 1] == keys[level + period - 1]

    return {
        "rule": rule,
        "first_zero_level": first_zero,
        "first_constant_level": first_constant,
        "first_repeat": list(first_repeat) if first_repeat else None,
        "repeat_preperiod": preperiod,
        "repeat_period": period,
        "repeat_type": repeat_type,
        "distinct_tower_maps_through_256": len(set(keys)),
        "image_sizes": image_sizes,
        "nonzero_state_counts": nonzero_counts,
        "constant_values": constant_values,
    }


def main() -> None:
    rules = [tower(rule) for rule in range(256)]

    # Frozen algebra controls.
    a2_zero = sorted(
        r["rule"]
        for r in rules
        if r["nonzero_state_counts"][1] == 0
    )
    assert a2_zero == ZERO_COMMUTATOR_CONTROL

    a2_constant = sorted(
        r["rule"]
        for r in rules
        if r["constant_values"][1] is not None
    )

    signature_groups: dict[tuple[object, ...], list[int]] = defaultdict(list)
    for r in rules:
        signature = (
            r["first_zero_level"],
            r["first_constant_level"],
            r["repeat_preperiod"],
            r["repeat_period"],
            tuple(r["image_sizes"][:16]),
            tuple(r["nonzero_state_counts"][:16]),
        )
        signature_groups[signature].append(int(r["rule"]))

    group_records = [
        {
            "rules": sorted(group),
            "count": len(group),
            "first_zero_level": signature[0],
            "first_constant_level": signature[1],
            "repeat_preperiod": signature[2],
            "repeat_period": signature[3],
            "image_sizes_first16": list(signature[4]),
            "nonzero_state_counts_first16": list(signature[5]),
        }
        for signature, group in signature_groups.items()
    ]
    group_records.sort(key=lambda x: (-x["count"], x["rules"]))

    right_censored = sorted(
        int(r["rule"]) for r in rules if r["first_repeat"] is None
    )

    first_zero_hist = Counter(
        str(r["first_zero_level"]) if r["first_zero_level"] is not None else "none"
        for r in rules
    )
    first_constant_hist = Counter(
        str(r["first_constant_level"])
        if r["first_constant_level"] is not None
        else "none"
        for r in rules
    )
    repeat_type_hist = Counter(
        r["repeat_type"] if r["repeat_type"] is not None else "right_censored"
        for r in rules
    )

    full = {
        "protocol": "docs/research/protocols/commutator-tower-20260909.md",
        "class_labels_loaded": False,
        "width": WIDTH,
        "horizon": HORIZON,
        "source_rules_checked": 256,
        "states_per_rule": 256,
        "scalar_vector_transition_checks": 256 * 256,
        "rules": rules,
        "signature_groups": group_records,
    }

    summary = {
        "protocol": full["protocol"],
        "class_labels_loaded": False,
        "width": WIDTH,
        "horizon": HORIZON,
        "source_rules_checked": 256,
        "states_per_rule": 256,
        "zero_commutator_control": a2_zero,
        "constant_A2_rules": a2_constant,
        "first_zero_level_histogram": dict(sorted(first_zero_hist.items())),
        "first_constant_level_histogram": dict(sorted(first_constant_hist.items())),
        "repeat_type_histogram": dict(sorted(repeat_type_hist.items())),
        "right_censored_rule_count": len(right_censored),
        "right_censored_rules": right_censored,
        "complete_signature_group_count": len(group_records),
        "largest_signature_group_size": max(g["count"] for g in group_records),
    }

    OUT.mkdir(parents=True, exist_ok=True)
    FULL_RESULT.write_text(json.dumps(full, separators=(",", ":")) + "\n")
    SUMMARY_RESULT.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
