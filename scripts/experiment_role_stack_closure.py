#!/usr/bin/env python3
"""Exact class-blind role-stack closure census for the derivative-completed lift."""

from __future__ import annotations

import json
from collections import defaultdict
from itertools import product
from pathlib import Path

RESULT = Path("results/role_stack_closure_20260909.json")


def t1_step(rule: tuple[int, ...], state: tuple[int, ...]) -> tuple[int, ...]:
    assert len(rule) == len(state) == 3
    population = sum(state)
    return tuple(rule[population - center] for center in state)


def t2_step(rule: tuple[int, ...], field: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    m = len(field)
    out = []
    for y in range(m):
        row = []
        for x in range(3):
            count = 0
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dy == 0 and dx == 0:
                        continue
                    count += field[(y + dy) % m][(x + dx) % 3]
            row.append(rule[count])
        out.append(tuple(row))
    return tuple(out)


def encode(state: tuple[int, ...], guards: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    return (tuple(state),) + tuple((g, g, g) for g in guards)


def shift_rows(field: tuple[tuple[int, ...], ...], drift: int) -> tuple[tuple[int, ...], ...]:
    m = len(field)
    return tuple(field[(y - drift) % m] for y in range(m))


def eca_number(rule: tuple[int, ...]) -> int:
    out = 0
    for left, center, right in product((0, 1), repeat=3):
        idx = 4 * left + 2 * center + right
        out |= rule[left + right] << idx
    return out


def used_bands(rule_code: int, m: int, guards: tuple[int, ...]) -> list[int]:
    rule = tuple((rule_code >> i) & 1 for i in range(3))
    bands = set()
    for predecessor in product((0, 1), repeat=3):
        state = t1_step(rule, predecessor)
        delta = tuple(a ^ b for a, b in zip(predecessor, state))
        lifted = rule + state + delta
        field = encode(state, guards)
        for y in range(m):
            for x in range(3):
                count = 0
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        if dy == 0 and dx == 0:
                            continue
                        count += field[(y + dy) % m][(x + dx) % 3]
                assert 0 <= count <= 8
                bands.add(count // 3)
                assert lifted[count] in (0, 1)
    return sorted(bands)


def main() -> None:
    templates_tested = 0
    successful_templates = []
    by_rule: dict[int, list[dict[str, object]]] = defaultdict(list)
    first_failures: dict[str, dict[str, object]] = {}

    for m in range(3, 9):
        for guards in product((0, 1), repeat=m - 1):
            for drift in range(m):
                templates_tested += 1
                passing_rules = []
                for rule_code in range(8):
                    rule = tuple((rule_code >> i) & 1 for i in range(3))
                    ok = True
                    for predecessor in product((0, 1), repeat=3):
                        state = t1_step(rule, predecessor)
                        delta = tuple(a ^ b for a, b in zip(predecessor, state))
                        next_state = t1_step(rule, state)
                        lifted_rule = rule + state + delta
                        actual = t2_step(lifted_rule, encode(state, guards))
                        expected = shift_rows(encode(next_state, guards), drift)
                        if actual != expected:
                            ok = False
                            key = f"m={m};g={''.join(map(str, guards))};j={drift};r={rule_code}"
                            first_failures.setdefault(
                                key,
                                {
                                    "predecessor": list(predecessor),
                                    "state": list(state),
                                    "delta": list(delta),
                                    "next_state": list(next_state),
                                },
                            )
                            break
                    if ok:
                        passing_rules.append(rule_code)
                        entry = {
                            "period": m,
                            "guards": list(guards),
                            "drift": drift,
                            "used_role_bands": used_bands(rule_code, m, guards),
                        }
                        by_rule[rule_code].append(entry)

                if passing_rules:
                    successful_templates.append(
                        {
                            "period": m,
                            "guards": list(guards),
                            "drift": drift,
                            "passing_rule_codes": passing_rules,
                        }
                    )

    expected_counts = {0: 33, 1: 0, 2: 6, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
    actual_counts = {rule: len(by_rule[rule]) for rule in range(8)}
    assert actual_counts == expected_counts
    assert not [t for t in successful_templates if len(t["passing_rule_codes"]) == 8]

    rule_rows = []
    for rule_code in range(8):
        rule_bits = tuple((rule_code >> i) & 1 for i in range(3))
        successes = by_rule[rule_code]
        rule_rows.append(
            {
                "rule_code": rule_code,
                "rule_bits_count0to2": list(rule_bits),
                "eca_equivalent": eca_number(rule_bits),
                "successful_template_count": len(successes),
                "successful_template_fraction": len(successes) / templates_tested,
                "minimal_successful_period": min((s["period"] for s in successes), default=None),
                "successful_templates": successes,
            }
        )

    result = {
        "protocol": "docs/research/protocols/role-stack-closure-20260909.md",
        "class_labels_loaded": False,
        "periods": list(range(3, 9)),
        "templates_tested": templates_tested,
        "universal_template_count": 0,
        "successful_template_count": len(successful_templates),
        "successful_templates": successful_templates,
        "rules": rule_rows,
        "first_failure_count": len(first_failures),
    }
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in ("rules", "successful_templates")}, indent=2))
    print(json.dumps({"rule_success_counts": actual_counts}, indent=2))


if __name__ == "__main__":
    main()
