#!/usr/bin/env python3
"""Exact class-blind selector-only role algebra search."""

from __future__ import annotations

import itertools
import json
from collections import defaultdict
from pathlib import Path

RESULT = Path("results/role_algebra_closure_20260909.json")


def step(rule: tuple[int, ...], state: tuple[int, ...]) -> tuple[int, ...]:
    population = sum(state)
    return tuple(rule[population - center] for center in state)


def main() -> None:
    permutations = list(itertools.permutations(range(3)))
    candidates = []
    by_rule: dict[int, list[dict[str, object]]] = defaultdict(list)

    for selectors in itertools.product(range(3), repeat=3):
        for permutation in permutations:
            passing = []
            for rule_code in range(8):
                rule = tuple((rule_code >> i) & 1 for i in range(3))
                ok = True
                for predecessor in itertools.product((0, 1), repeat=3):
                    state = step(rule, predecessor)
                    delta = tuple(a ^ b for a, b in zip(predecessor, state))
                    next_state = step(rule, state)
                    next_delta = tuple(a ^ b for a, b in zip(state, next_state))
                    blocks = (rule, state, delta)
                    outputs = tuple(
                        step(blocks[selectors[row]], blocks[row]) for row in range(3)
                    )
                    targets = (rule, next_state, next_delta)
                    expected = tuple(targets[permutation[row]] for row in range(3))
                    if outputs != expected:
                        ok = False
                        break
                if ok:
                    passing.append(rule_code)
                    by_rule[rule_code].append(
                        {"selectors": list(selectors), "permutation": list(permutation)}
                    )
            if passing:
                candidates.append(
                    {
                        "selectors": list(selectors),
                        "permutation": list(permutation),
                        "passing_rules": passing,
                    }
                )

    counts = {rule: len(by_rule[rule]) for rule in range(8)}
    assert counts == {0: 48, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}

    result = {
        "protocol": "docs/research/protocols/role-algebra-closure-20260909.md",
        "class_labels_loaded": False,
        "candidate_count": 162,
        "successful_candidate_count": len(candidates),
        "nonconstant_success_count": 0,
        "success_counts_by_source_rule": counts,
        "successful_candidates": candidates,
    }
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "successful_candidates"}, indent=2))


if __name__ == "__main__":
    main()
