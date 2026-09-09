#!/usr/bin/env python3
"""Exact infinite-lattice local-rule census for the ternary commutator lift."""

from __future__ import annotations

import json
from collections import Counter
from functools import lru_cache
from pathlib import Path

import numpy as np

RESULT = Path("results/local_ternary_lift_20260909.json")
SUMMARY = Path("results/local_ternary_lift_20260909_summary.json")
MAX_DEPTH = 4


@lru_cache(None)
def pattern_bits(nbits: int) -> np.ndarray:
    values = np.arange(1 << nbits, dtype=np.uint32)
    return ((values[:, None] >> np.arange(nbits)) & 1).astype(np.uint8)


@lru_cache(None)
def weights(nbits: int) -> np.ndarray:
    return (1 << np.arange(nbits)).astype(np.uint32)


def eca_lut(rule: int) -> np.ndarray:
    return np.array([(rule >> i) & 1 for i in range(8)], dtype=np.uint8)


def minimize(radius: int, table: np.ndarray) -> tuple[int, np.ndarray]:
    table = np.asarray(table, dtype=np.uint8)
    r = radius
    while r > 0:
        nbits = 2 * r + 1
        inner = np.arange(1 << (nbits - 2), dtype=np.uint32)
        base = inner << 1
        idx00 = base
        idx10 = base | 1
        idx01 = base | (1 << (nbits - 1))
        idx11 = idx10 | (1 << (nbits - 1))
        vals = table[idx00]
        if (
            np.array_equal(vals, table[idx10])
            and np.array_equal(vals, table[idx01])
            and np.array_equal(vals, table[idx11])
        ):
            table = vals.copy()
            r -= 1
        else:
            break
    return r, table


def key(local_map: tuple[int, np.ndarray]) -> tuple[int, bytes]:
    radius, table = local_map
    return radius, table.tobytes()


def root_derivative(rule_lut: np.ndarray) -> tuple[int, np.ndarray]:
    bits = pattern_bits(3)
    address = 4 * bits[:, 0] + 2 * bits[:, 1] + bits[:, 2]
    table = bits[:, 1] ^ rule_lut[address]
    return minimize(1, table)


def children(
    rule_lut: np.ndarray, local_map: tuple[int, np.ndarray]
) -> tuple[tuple[int, np.ndarray], tuple[int, np.ndarray], tuple[int, np.ndarray]]:
    radius, table = local_map
    child_radius = radius + 1
    bits = pattern_bits(2 * child_radius + 1)

    addresses = 4 * bits[:, :-2] + 2 * bits[:, 1:-1] + bits[:, 2:]
    intermediate = rule_lut[addresses]
    intermediate_index = (intermediate * weights(intermediate.shape[1])).sum(axis=1)
    left = table[intermediate_index]

    local_width = 2 * radius + 1
    w = weights(local_width)
    values = []
    for offset in range(3):
        subwindow = bits[:, offset : offset + local_width]
        index = (subwindow * w).sum(axis=1)
        values.append(table[index])
    address = 4 * values[0] + 2 * values[1] + values[2]
    right = rule_lut[address]

    comm = left ^ right
    return tuple(minimize(child_radius, x) for x in (left, right, comm))


def main() -> None:
    rows = []
    closure_hist = Counter()
    faithful_rules = []

    for rule in range(256):
        lut = eca_lut(rule)
        root = root_derivative(lut)
        current = {key(root): (root, 1)}
        cumulative: dict[tuple[int, bytes], tuple[int, np.ndarray]] = {}
        cache = {}

        distinct_at_depth = []
        cumulative_counts = []
        new_counts = []
        radius_histograms = []
        max_radii = []
        radius_le_one = []
        multiplicity_histograms = []
        first_closed = None

        def child_maps(local_map):
            k = key(local_map)
            if k not in cache:
                cache[k] = children(lut, local_map)
            return cache[k]

        for depth in range(MAX_DEPTH + 1):
            distinct_at_depth.append(len(current))
            multiplicity_histograms.append(
                {str(k): v for k, v in sorted(Counter(m for _, m in current.values()).items())}
            )
            radius_hist = Counter(local_map[0] for local_map, _ in current.values())
            radius_histograms.append({str(k): v for k, v in sorted(radius_hist.items())})
            max_radii.append(max(radius_hist))
            radius_le_one.append(sum(1 for local_map, _ in current.values() if local_map[0] <= 1))

            new = 0
            for map_key, (local_map, _) in current.items():
                if map_key not in cumulative:
                    cumulative[map_key] = local_map
                    new += 1
            new_counts.append(new)
            cumulative_counts.append(len(cumulative))

            if first_closed is None:
                keys = set(cumulative)
                if all(
                    key(child) in keys
                    for local_map, _ in current.values()
                    for child in child_maps(local_map)
                ):
                    first_closed = depth

            if depth < MAX_DEPTH:
                nxt = {}
                for local_map, multiplicity in current.values():
                    for child in child_maps(local_map):
                        child_key = key(child)
                        if child_key in nxt:
                            old_map, old_mult = nxt[child_key]
                            nxt[child_key] = (old_map, old_mult + multiplicity)
                        else:
                            nxt[child_key] = (child, multiplicity)
                current = nxt

        ceiling = [2 ** (d + 1) - 1 for d in range(MAX_DEPTH + 1)]
        faithful = distinct_at_depth == ceiling
        if faithful:
            faithful_rules.append(rule)
        closure_hist["none" if first_closed is None else str(first_closed)] += 1

        rows.append({
            "rule": rule,
            "distinct_at_depth": distinct_at_depth,
            "cumulative_distinct": cumulative_counts,
            "new_maps_at_depth": new_counts,
            "radius_histograms": radius_histograms,
            "max_minimal_radius_at_depth": max_radii,
            "distinct_descendants_radius_le_1": radius_le_one,
            "multiplicity_histograms": multiplicity_histograms,
            "first_closed_depth": first_closed,
            "faithful_to_universal_ceiling_through_depth_4": faithful,
        })

    closed_rules = [row["rule"] for row in rows if row["first_closed_depth"] is not None]
    assert len(closed_rules) == 21
    assert len(faithful_rules) == 156

    result = {
        "protocol": "docs/research/protocols/local-ternary-lift-20260909.md",
        "class_labels_loaded": False,
        "max_depth": MAX_DEPTH,
        "rules_checked": 256,
        "universal_ceiling_by_depth": [2 ** (d + 1) - 1 for d in range(MAX_DEPTH + 1)],
        "finite_local_closure_within_depth_4_count": len(closed_rules),
        "finite_local_closure_rules": closed_rules,
        "closure_depth_histogram": dict(sorted(closure_hist.items())),
        "faithful_to_ceiling_through_depth_4_count": len(faithful_rules),
        "faithful_to_ceiling_through_depth_4_rules": faithful_rules,
        "rules": rows,
    }
    summary = {k: v for k, v in result.items() if k != "rules"}

    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
