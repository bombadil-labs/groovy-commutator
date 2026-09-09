#!/usr/bin/env python3
"""Exact structural checks for the derivative-completed dimensional lift.

This instrument intentionally contains no Wolfram class labels.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

RESULT = Path("results/derivative_completed_lift_20260909.json")


def bits(x: int, n: int) -> tuple[int, ...]:
    return tuple((x >> i) & 1 for i in range(n))


def eca_bit(rule: int, address: int) -> int:
    return (rule >> address) & 1


def eca_center(address: int) -> int:
    return (address >> 1) & 1


def incoming_derivative_values(rule: int) -> set[int]:
    return {eca_center(k) ^ eca_bit(rule, k) for k in range(8)}


def base_lift(rule: int, delta: int) -> int:
    """Counts 0..7 store the ECA table; count 8 stores incoming delta."""
    assert 0 <= rule < 256 and delta in (0, 1)
    return rule | (delta << 8)


def recursive_lift(
    rule_bits: tuple[int, ...],
    state_bits: tuple[int, ...],
    derivative_bits: tuple[int, ...],
    role_order: tuple[str, str, str] = ("rule", "state", "derivative"),
) -> tuple[int, ...]:
    m = len(rule_bits)
    assert len(state_bits) == m == len(derivative_bits)
    blocks = {
        "rule": rule_bits,
        "state": state_bits,
        "derivative": derivative_bits,
    }
    return tuple(bit for role in role_order for bit in blocks[role])


def totalistic_side3_step(
    rule_bits: tuple[int, ...], state_bits: tuple[int, ...]
) -> tuple[int, ...]:
    """Radius-one center-independent Moore update on a side-three d-torus.

    The caller supplies bit strings of equal length M=3^d. On a side-three
    torus, the M-1 outer offsets visit every other cell exactly once.
    """
    assert len(rule_bits) == len(state_bits)
    population = sum(state_bits)
    return tuple(rule_bits[population - center] for center in state_bits)


def main() -> None:
    # Base ECA + delta -> T2 is a bijection when delta is treated formally.
    formal_images = {
        base_lift(rule, delta) for rule in range(256) for delta in (0, 1)
    }
    assert formal_images == set(range(512))

    # If delta must actually occur at some ECA local transition, only identity
    # and NOT-center have a single derivative value; every other ECA realizes
    # both values on some local address.
    derivative_cardinality = Counter()
    singleton_rules: dict[int, list[int]] = {}
    realized_images: set[int] = set()
    for rule in range(256):
        ds = incoming_derivative_values(rule)
        derivative_cardinality[len(ds)] += 1
        if len(ds) == 1:
            singleton_rules[rule] = sorted(ds)
        for delta in ds:
            lifted = base_lift(rule, delta)
            realized_images.add(lifted)
            assert tuple((lifted >> k) & 1 for k in range(8)) == bits(rule, 8)

    assert derivative_cardinality == Counter({2: 254, 1: 2})
    assert singleton_rules == {51: [1], 204: [0]}
    assert len(realized_images) == 510

    # Recursive native-type identity: three M-bit roles make one 3M-bit table.
    recursive_checks = []
    for d in (1, 2, 3, 4):
        m = 3**d
        assert 3 * m == 3 ** (d + 1)
        recursive_checks.append(
            {
                "dimension": d,
                "lower_table_bits": m,
                "next_table_bits": 3 * m,
                "identity": f"3*3^{d}=3^{d+1}",
            }
        )

    # Exact count-address selector identity. A lower central slice with outer
    # neighbor count n plus q all-one transverse M-cell layers has higher outer
    # count q*M+n. Concatenation therefore selects block q at entry n.
    selector_checks = 0
    role_order = ("rule", "state", "derivative")
    for d in (1, 2, 3):
        m = 3**d
        # Deterministic nontrivial bit patterns are enough because the identity
        # is purely index algebra; the note gives the general proof.
        block = {
            "rule": tuple((i * 3 + 1) & 1 for i in range(m)),
            "state": tuple((i * 5 + 2) & 1 for i in range(m)),
            "derivative": tuple((i * 7 + 3) & 1 for i in range(m)),
        }
        lifted = recursive_lift(
            block["rule"], block["state"], block["derivative"], role_order
        )
        for q, role in enumerate(role_order):
            for n in range(m):
                higher_count = q * m + n
                assert lifted[higher_count] == block[role][n]
                selector_checks += 1

    # Self-substrate control: on a side-three 2D torus, using the 9-bit table
    # as its own 9-bit state can only yield 0, 1, itself, or its complement.
    self_categories = Counter()
    for rule in range(512):
        r = bits(rule, 9)
        nxt = totalistic_side3_step(r, r)
        candidates = {
            "zero": (0,) * 9,
            "one": (1,) * 9,
            "same": r,
            "complement": tuple(1 - b for b in r),
        }
        assert nxt in candidates.values()
        if rule in (0, 511):
            self_categories["constant_fixed"] += 1
        else:
            matches = [name for name, value in candidates.items() if value == nxt]
            assert len(matches) == 1
            self_categories[matches[0]] += 1

    assert self_categories == Counter(
        {
            "same": 128,
            "complement": 128,
            "zero": 127,
            "one": 127,
            "constant_fixed": 2,
        }
    )

    result = {
        "protocol": "docs/research/protocols/derivative-completed-lift-20260909.md",
        "class_labels_loaded": False,
        "base": {
            "formal_pairs": 512,
            "formal_distinct_T2_rules": len(formal_images),
            "formal_bijection": True,
            "actual_derivative_cardinality_histogram": dict(
                sorted(derivative_cardinality.items())
            ),
            "single_derivative_rules": {
                str(k): v for k, v in singleton_rules.items()
            },
            "dynamically_realized_T2_rules": len(realized_images),
            "missing_T2_rules_under_actual_local_delta": sorted(
                set(range(512)) - realized_images
            ),
        },
        "recursive_storage_checks": recursive_checks,
        "selector_index_checks": selector_checks,
        "self_substrate_2d": dict(sorted(self_categories.items())),
    }

    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
