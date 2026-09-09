#!/usr/bin/env python3
"""Exact class-blind census for the preregistered ternary commutator lift."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

import numpy as np

RESULT = Path("results/ternary_commutator_lift_20260909.json")
SUMMARY = Path("results/ternary_commutator_lift_20260909_summary.json")
MAX_DEPTH = 6


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


def descendants(a: np.ndarray, f: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    left = a[f]       # A o F
    right = f[a]      # F o A
    residual = left ^ right
    return left, right, residual


def check_closure(vocabulary: dict[bytes, np.ndarray], f: np.ndarray) -> bool:
    keys = set(vocabulary)
    for a in vocabulary.values():
        if any(child.tobytes() not in keys for child in descendants(a, f)):
            return False
    return True


def one_rule(rule: int, f: np.ndarray) -> dict[str, object]:
    states = np.arange(256, dtype=np.uint16)
    derivative = states ^ f

    level: list[np.ndarray] = [derivative]
    vocabulary: dict[bytes, np.ndarray] = {}
    distinct_at_depth: list[int] = []
    cumulative_distinct: list[int] = []
    new_at_depth: list[int] = []
    multiplicity_histograms: list[dict[str, int]] = []
    first_no_new = None
    closure_depth = None
    closure_vocab_size = None

    all_c = derivative.copy()
    tower = derivative.copy()

    for depth in range(MAX_DEPTH + 1):
        keys = [a.tobytes() for a in level]
        multiplicities = Counter(keys)
        distinct_at_depth.append(len(multiplicities))
        multiplicity_histograms.append(
            {
                str(multiplicity): count
                for multiplicity, count in sorted(
                    Counter(multiplicities.values()).items()
                )
            }
        )

        added = 0
        for a, key in zip(level, keys):
            if key not in vocabulary:
                vocabulary[key] = a.copy()
                added += 1
        new_at_depth.append(added)
        cumulative_distinct.append(len(vocabulary))

        if depth > 0 and added == 0 and first_no_new is None:
            first_no_new = depth

        if closure_depth is None and check_closure(vocabulary, f):
            closure_depth = depth
            closure_vocab_size = len(vocabulary)

        # The all-C branch at tree depth d is tower level A_{d+1}.
        if depth > 0:
            all_c = descendants(all_c, f)[2]
            tower = tower[f] ^ f[tower]
            assert np.array_equal(all_c, tower)

        if depth < MAX_DEPTH:
            next_level: list[np.ndarray] = []
            for a in level:
                next_level.extend(descendants(a, f))
            level = next_level

    # Post-evaluation algebraic audit: L commutes with R and C, hence at depth d
    # there can be at most sum_{j=0}^d 2^j = 2^(d+1)-1 semantic maps.
    forced_bounds = [2 ** (depth + 1) - 1 for depth in range(MAX_DEPTH + 1)]
    assert all(
        observed <= bound
        for observed, bound in zip(distinct_at_depth, forced_bounds)
    )

    return {
        "rule": rule,
        "distinct_descendants_at_depth": distinct_at_depth,
        "cumulative_distinct_descendants": cumulative_distinct,
        "new_maps_at_depth": new_at_depth,
        "first_no_new_depth": first_no_new,
        "finite_ternary_role_closure_depth": closure_depth,
        "closure_vocabulary_size": closure_vocab_size,
        "multiplicity_histograms": multiplicity_histograms,
        "forced_distinct_bound_at_depth": forced_bounds,
        "all_C_branch_matches_commutator_tower": True,
    }


def main() -> None:
    transitions = transition_table()
    rows = [one_rule(rule, transitions[rule]) for rule in range(256)]

    closure_histogram = Counter(
        "none"
        if row["finite_ternary_role_closure_depth"] is None
        else str(row["finite_ternary_role_closure_depth"])
        for row in rows
    )
    first_no_new_histogram = Counter(
        "none"
        if row["first_no_new_depth"] is None
        else str(row["first_no_new_depth"])
        for row in rows
    )

    depth_histograms = {}
    for depth in range(MAX_DEPTH + 1):
        hist = Counter(row["distinct_descendants_at_depth"][depth] for row in rows)
        depth_histograms[str(depth)] = {
            str(key): value for key, value in sorted(hist.items())
        }

    closure_rules = {
        str(depth): [
            row["rule"]
            for row in rows
            if row["finite_ternary_role_closure_depth"] == depth
        ]
        for depth in range(MAX_DEPTH + 1)
    }
    nonclosed = [
        row["rule"]
        for row in rows
        if row["finite_ternary_role_closure_depth"] is None
    ]

    generic_bound_signature = [2 ** (d + 1) - 1 for d in range(MAX_DEPTH + 1)]
    bound_saturating = [
        row["rule"]
        for row in rows
        if row["distinct_descendants_at_depth"] == generic_bound_signature
    ]

    result = {
        "protocol": "docs/research/protocols/ternary-commutator-lift-20260909.md",
        "class_labels_loaded": False,
        "max_depth": MAX_DEPTH,
        "rules_checked": 256,
        "states_per_map": 256,
        "forced_distinct_bound_at_depth": generic_bound_signature,
        "rows": rows,
    }

    summary = {
        "protocol": result["protocol"],
        "class_labels_loaded_during_evaluation": False,
        "max_depth": MAX_DEPTH,
        "rules_checked": 256,
        "closure_depth_histogram": dict(sorted(closure_histogram.items())),
        "first_no_new_depth_histogram": dict(sorted(first_no_new_histogram.items())),
        "finite_closure_rule_count": 256 - len(nonclosed),
        "nonclosed_through_depth6_count": len(nonclosed),
        "closure_rules_by_depth": closure_rules,
        "distinct_descendant_histograms_by_depth": depth_histograms,
        "forced_distinct_bound_at_depth": generic_bound_signature,
        "bound_saturating_rule_count": len(bound_saturating),
        "bound_saturating_rules": bound_saturating,
        "all_C_branch_checks": 256 * MAX_DEPTH,
    }

    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(result, separators=(",", ":")) + "\n")
    summary["full_result_sha256"] = hashlib.sha256(RESULT.read_bytes()).hexdigest()
    SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
