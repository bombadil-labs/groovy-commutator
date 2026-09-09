#!/usr/bin/env python3
"""Exact class-blind audit of derivative-center reconstruction in OT1 rules."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import product
from pathlib import Path

RESULT = Path("results/derivative_center_reconstruction_20260909.json")


def ot_bit(table: tuple[int, ...], center: int, count: int) -> int:
    return table[3 * center + count]


def table_to_eca(table: tuple[int, ...]) -> int:
    rule = 0
    for left, center, right in product((0, 1), repeat=3):
        idx = 4 * left + 2 * center + right
        rule |= ot_bit(table, center, left + right) << idx
    return rule


def main() -> None:
    rows = []
    ambiguity_hist = Counter()
    reconstructible = []
    ordered_reconstructible = []

    for code in range(64):
        table = tuple((code >> i) & 1 for i in range(6))
        relation: dict[tuple[int, int], set[int]] = defaultdict(set)
        ordered_relation: dict[tuple[int, int, int], set[int]] = defaultdict(set)
        witnesses: dict[tuple[int, int, int], list[tuple[int, ...]]] = defaultdict(list)

        for a, b, c, d, e in product((0, 1), repeat=5):
            left_t = ot_bit(table, b, a + c)
            center_t = ot_bit(table, c, b + d)
            right_t = ot_bit(table, d, c + e)
            incoming_delta = c ^ center_t
            count_t = left_t + right_t

            relation[(count_t, incoming_delta)].add(center_t)
            ordered_relation[(left_t, right_t, incoming_delta)].add(center_t)
            witnesses[(count_t, incoming_delta, center_t)].append((a, b, c, d, e))

        ambiguous = {
            f"{n},{delta}": sorted(values)
            for (n, delta), values in sorted(relation.items())
            if len(values) > 1
        }
        ordered_ambiguous = {
            f"{left},{right},{delta}": sorted(values)
            for (left, right, delta), values in sorted(ordered_relation.items())
            if len(values) > 1
        }
        ambiguity_hist[len(ambiguous)] += 1

        eca_rule = table_to_eca(table)
        exact = not ambiguous
        ordered_exact = not ordered_ambiguous
        if exact:
            reconstructible.append(eca_rule)
        if ordered_exact:
            ordered_reconstructible.append(eca_rule)

        decoder = None
        evolution_failures = []
        if exact:
            decoder = {
                f"{n},{delta}": next(iter(values))
                for (n, delta), values in sorted(relation.items())
            }
            for a, b, c, d, e in product((0, 1), repeat=5):
                left_t = ot_bit(table, b, a + c)
                center_t = ot_bit(table, c, b + d)
                right_t = ot_bit(table, d, c + e)
                incoming_delta = c ^ center_t
                count_t = left_t + right_t
                reconstructed = decoder[f"{count_t},{incoming_delta}"]
                got = ot_bit(table, reconstructed, count_t)
                expected = ot_bit(table, center_t, count_t)
                if got != expected:
                    evolution_failures.append((a, b, c, d, e))

        ambiguous_witnesses = {}
        for key in ambiguous:
            n, delta = map(int, key.split(","))
            ambiguous_witnesses[key] = {
                str(center): list(witnesses[(n, delta, center)][0])
                for center in (0, 1)
                if witnesses[(n, delta, center)]
            }

        rows.append(
            {
                "ot_code": code,
                "eca_rule": eca_rule,
                "table_bits_c0_n0to2_then_c1_n0to2": list(table),
                "reachable_count_delta_pairs": len(relation),
                "ambiguous_count_delta_pairs": ambiguous,
                "ambiguous_witnesses": ambiguous_witnesses,
                "exact_reconstruction": exact,
                "decoder": decoder,
                "evolution_failures": [list(w) for w in evolution_failures],
                "ordered_left_right_delta_exact_posthoc": ordered_exact,
                "ordered_ambiguity_count_posthoc": len(ordered_ambiguous),
            }
        )

    assert reconstructible == [0, 255]
    assert ordered_reconstructible == [0, 255]
    assert all(not row["evolution_failures"] for row in rows)

    result = {
        "protocol": "docs/research/protocols/derivative-center-reconstruction-20260909.md",
        "class_labels_loaded": False,
        "rules_checked": 64,
        "five_cell_histories_per_rule": 32,
        "exact_reconstruction_count": len(reconstructible),
        "exact_reconstruction_eca_rules": reconstructible,
        "ambiguity_count_histogram": dict(sorted(ambiguity_hist.items())),
        "posthoc_ordered_left_right_delta_exact_count": len(ordered_reconstructible),
        "posthoc_ordered_left_right_delta_exact_rules": ordered_reconstructible,
        "rules": rows,
    }
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "rules"}, indent=2))


if __name__ == "__main__":
    main()
