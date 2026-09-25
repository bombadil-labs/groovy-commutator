"""Exact, frozen small-ring order check; see research protocol before running."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

import numpy as np

from groovy.ca import apply_rule

RULES = (30, 54, 110)
WIDTHS = (4, 6, 8)
ORDERS = ((30, 54, 110), (30, 110, 54), (54, 110, 30))


def vector_step(word: int, n: int, order: tuple[int, ...]) -> int:
    bits = np.array([(word >> i) & 1 for i in range(n)], dtype=np.uint8)
    for rule in order:
        bits = apply_rule(bits, rule)
    return sum(int(bit) << i for i, bit in enumerate(bits))


def scalar_step(word: int, n: int, order: tuple[int, ...]) -> int:
    for rule in order:
        next_word = 0
        for i in range(n):
            left = (word >> ((i - 1) % n)) & 1
            center = (word >> i) & 1
            right = (word >> ((i + 1) % n)) & 1
            key = 4 * left + 2 * center + right
            next_word |= ((rule >> key) & 1) << i
        word = next_word
    return word


def cycle_counts(mapping: tuple[int, ...]) -> dict[int, int]:
    visited = set()
    counts: Counter[int] = Counter()
    for start in range(len(mapping)):
        if start in visited:
            continue
        index = {}
        path = []
        cur = start
        while cur not in index and cur not in visited:
            index[cur] = len(path)
            path.append(cur)
            cur = mapping[cur]
        if cur in index:
            counts[len(path) - index[cur]] += 1
        visited.update(path)
    return dict(sorted(counts.items()))


def independently_count_cycles(mapping: tuple[int, ...]) -> dict[int, int]:
    """Trace each start separately and canonicalize each recurring orbit."""
    cycles = set()
    for start in range(len(mapping)):
        seen = {}
        orbit = []
        state = start
        while state not in seen:
            seen[state] = len(orbit)
            orbit.append(state)
            state = mapping[state]
        recurring = orbit[seen[state]:]
        cycles.add(tuple(sorted(recurring)))
    return dict(sorted(Counter(len(cycle) for cycle in cycles).items()))


def evaluate() -> dict:
    rows = []
    for n in WIDTHS:
        mappings = {}
        for order in ORDERS:
            fast = tuple(vector_step(s, n, order) for s in range(1 << n))
            independent = tuple(scalar_step(s, n, order) for s in range(1 << n))
            if fast != independent:
                raise AssertionError(f"transition disagreement for width={n}, order={order}")
            if cycle_counts(fast) != independently_count_cycles(independent):
                raise AssertionError("cycle verification failed")
            mappings[order] = fast
        first, second, rotation = ORDERS
        assert cycle_counts(mappings[first]) == cycle_counts(mappings[rotation])
        unequal = next((s for s, (a, b) in enumerate(zip(mappings[first], mappings[second])) if a != b), None)
        rows.append({
            "width": n,
            "orders": [{"first_to_last": list(order), "cycles_by_period": cycle_counts(mappings[order])}
                       for order in ORDERS],
            "first_disagreement": None if unequal is None else {
                "source": unequal,
                "first_result": mappings[first][unequal],
                "second_result": mappings[second][unequal],
            },
            "maps_agree": unequal is None,
        })
    return {
        "protocol": "docs/research/protocols/2026-09-25-three-rule-order.md",
        "evaluation": "exhaustive periodic rings of widths 4,6,8; scalar/vector agreement",
        "source_hashes": {
            path: hashlib.sha256((Path(__file__).resolve().parents[2] / path).read_bytes()).hexdigest()
            for path in (
                "docs/research/protocols/2026-09-25-three-rule-order.md",
                "experiments/three_rule_order_20260925/run.py",
                "src/groovy/ca.py",
            )
        },
        "rows": rows,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(evaluate(), indent=2) + "\n")
