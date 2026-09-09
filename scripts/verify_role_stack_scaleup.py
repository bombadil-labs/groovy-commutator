#!/usr/bin/env python3
"""Exact 2D->3D scale-up of the frozen zero-guard role-stack geometry."""

from __future__ import annotations

import json
from pathlib import Path

RESULT = Path("results/role_stack_scaleup_20260909.json")
M = 9


def bits(x: int, n: int) -> tuple[int, ...]:
    return tuple((x >> i) & 1 for i in range(n))


def pack(xs: tuple[int, ...]) -> int:
    return sum(bit << i for i, bit in enumerate(xs))


def lower_step(rule: tuple[int, ...], state: tuple[int, ...]) -> tuple[int, ...]:
    """Center-independent totalistic update on the complete 3x3 torus."""
    population = sum(state)
    return tuple(rule[population - center] for center in state)


def structured_3d_step(
    lifted_rule: tuple[int, ...],
    slices: tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]],
) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    """Exact side-three 3D Moore update, exploiting whole-slice populations."""
    pops = tuple(sum(s) for s in slices)
    out = []
    for z in range(3):
        prev_pop = pops[(z - 1) % 3]
        next_pop = pops[(z + 1) % 3]
        current_pop = pops[z]
        out.append(
            tuple(
                lifted_rule[prev_pop + next_pop + current_pop - center]
                for center in slices[z]
            )
        )
    return tuple(out)  # type: ignore[return-value]


def population_criterion(rule: tuple[int, ...], population: int, state: tuple[int, ...]) -> bool:
    if population < M:
        return rule[population] == 0
    assert population == M
    return state[0] == 0


def algebraic_condition(rule: tuple[int, ...]) -> bool:
    if rule[0] or rule[M - 1]:
        return False
    for p in range(1, M):
        if rule[p - 1] and rule[p]:
            return False
        if (not rule[p - 1]) and rule[p] and rule[M - p]:
            return False
    return True


def main() -> None:
    closed_rules = []
    rows = []
    direct_cases = 0
    criterion_cases = 0

    for rule_code in range(1 << M):
        rule = bits(rule_code, M)
        reachable_populations = set()
        first_failure = None
        direct_closed = True
        criterion_closed = True

        for predecessor_code in range(1 << M):
            predecessor = bits(predecessor_code, M)
            state = lower_step(rule, predecessor)
            delta = tuple(a ^ b for a, b in zip(predecessor, state))
            next_state = lower_step(rule, state)
            lifted_rule = rule + state + delta
            encoded = (state, (0,) * M, (0,) * M)
            expected = (next_state, (0,) * M, (0,) * M)
            actual = structured_3d_step(lifted_rule, encoded)
            direct_cases += 1
            if actual != expected:
                direct_closed = False
                if first_failure is None:
                    first_failure = {
                        "predecessor": predecessor_code,
                        "state": pack(state),
                        "state_population": sum(state),
                        "actual_slices": [pack(s) for s in actual],
                        "expected_slices": [pack(s) for s in expected],
                    }

            population = sum(state)
            reachable_populations.add(population)
            criterion_ok = population_criterion(rule, population, state)
            criterion_cases += 1
            if not criterion_ok:
                criterion_closed = False

            assert (actual == expected) == criterion_ok

        algebraic = algebraic_condition(rule)
        assert direct_closed == criterion_closed == algebraic
        if direct_closed:
            closed_rules.append(rule_code)

        rows.append(
            {
                "rule": rule_code,
                "table_bits_count0to8": list(rule),
                "closed": direct_closed,
                "reachable_state_populations": sorted(reachable_populations),
                "algebraic_condition": algebraic,
                "first_failure": first_failure,
            }
        )

    expected_closed = [
        0, 2, 4, 8, 10, 16, 18, 20, 32, 34, 36, 40, 42, 64, 66,
        68, 80, 82, 84, 128, 130, 136, 138, 144, 146, 160, 162, 168, 170,
    ]
    assert closed_rules == expected_closed

    result = {
        "protocol": "docs/research/protocols/role-stack-scaleup-20260909.md",
        "class_labels_loaded": False,
        "rules_checked": 1 << M,
        "predecessor_states_per_rule": 1 << M,
        "direct_3d_cases": direct_cases,
        "population_criterion_cases": criterion_cases,
        "closed_rule_count": len(closed_rules),
        "closed_rules": closed_rules,
        "algebraic_characterization": {
            "r0_zero": True,
            "r8_zero": True,
            "no_adjacent_ones": True,
            "rising_edge_reflection_zero": "if r[p-1]=0 and r[p]=1 then r[9-p]=0",
        },
        "rules": rows,
    }
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "rules"}, indent=2))


if __name__ == "__main__":
    main()
