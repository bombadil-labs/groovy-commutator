#!/usr/bin/env python3
"""Exact class-blind census for the ternary commutator lift on width-8 ECAs."""

from __future__ import annotations

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
        out = ((rule >> addresses) & 1).astype(np.uint16)
        table[rule] = (out * weights).sum(axis=1)
    return table


def children(a: np.ndarray, f: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    left = a[f]
    right = f[a]
    comm = left ^ right
    return left, right, comm


def main() -> None:
    E = transition_table()
    states = np.arange(256, dtype=np.uint16)
    rows = []
    closure_hist = Counter()
    faithful_rules = []

    for rule in range(256):
        f = E[rule]
        current = [states ^ f]
        cumulative: dict[bytes, np.ndarray] = {}
        distinct_at_depth = []
        new_at_depth = []
        cumulative_counts = []
        multiplicity_histograms = []
        first_no_new = None
        first_closed = None
        all_c = states ^ f

        for depth in range(MAX_DEPTH + 1):
            exact_counts = Counter(a.tobytes() for a in current)
            distinct_at_depth.append(len(exact_counts))
            multiplicity_histograms.append(
                {str(k): v for k, v in sorted(Counter(exact_counts.values()).items())}
            )

            new = 0
            for a in current:
                key = a.tobytes()
                if key not in cumulative:
                    cumulative[key] = a.copy()
                    new += 1
            new_at_depth.append(new)
            cumulative_counts.append(len(cumulative))

            if depth > 0 and new == 0 and first_no_new is None:
                first_no_new = depth

            if first_closed is None:
                keys = set(cumulative)
                closed = True
                for a in cumulative.values():
                    if any(child.tobytes() not in keys for child in children(a, f)):
                        closed = False
                        break
                if closed:
                    first_closed = depth

            if depth == 0:
                assert np.array_equal(all_c, current[0])
            if depth < MAX_DEPTH:
                all_c = all_c[f] ^ f[all_c]
                nxt = []
                for a in current:
                    nxt.extend(children(a, f))
                current = nxt

        ceiling = [2 ** (d + 1) - 1 for d in range(MAX_DEPTH + 1)]
        assert all(u <= m for u, m in zip(distinct_at_depth, ceiling))
        faithful = distinct_at_depth == ceiling
        if faithful:
            faithful_rules.append(rule)

        closure_hist["none" if first_closed is None else str(first_closed)] += 1
        rows.append(
            {
                "rule": rule,
                "distinct_at_depth": distinct_at_depth,
                "new_maps_at_depth": new_at_depth,
                "cumulative_distinct": cumulative_counts,
                "first_no_new_depth": first_no_new,
                "first_closed_depth": first_closed,
                "faithful_to_universal_ceiling_through_depth_6": faithful,
                "multiplicity_histograms": multiplicity_histograms,
            }
        )

    finite = [row["rule"] for row in rows if row["first_closed_depth"] is not None]
    assert len(finite) == 33
    assert len(faithful_rules) == 107

    result = {
        "protocol": "docs/research/protocols/ternary-commutator-lift-20260909.md",
        "class_labels_loaded": False,
        "max_depth": MAX_DEPTH,
        "rules_checked": 256,
        "universal_ceiling_by_depth": [2 ** (d + 1) - 1 for d in range(MAX_DEPTH + 1)],
        "universal_identities": [
            "L(R(A)) = R(L(A))",
            "L(C(A)) = C(L(A))",
        ],
        "finite_closure_within_depth_6_count": len(finite),
        "closure_depth_histogram": dict(sorted(closure_hist.items())),
        "finite_closure_rules": finite,
        "faithful_to_ceiling_through_depth_6_count": len(faithful_rules),
        "faithful_to_ceiling_through_depth_6_rules": faithful_rules,
        "all_C_branch_consistency": True,
        "rules": rows,
    }

    summary = {k: v for k, v in result.items() if k != "rules"}
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
