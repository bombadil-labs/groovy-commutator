#!/usr/bin/env python3
"""Exact checks for 1D->2D cellular-automaton intertwining constructions."""

from __future__ import annotations

import itertools
import json
from pathlib import Path


RESULT_PATH = Path("results/dimensional_intertwining_20260909.json")
SELECTED_GLOBAL_RULES = [0, 30, 54, 90, 110, 255]
WIDTHS = [3, 4, 5, 6]

ACTIVE_OFFSETS = {
    "left": (-1, 0),
    "center": (0, 0),
    "right": (0, 1),
}

GATED_OFFSETS = {
    "left": (-1, 0),
    "center": (0, 0),
    "right": (1, 0),
    "gate_a": (2, 0),
    "gate_b": (1, 1),
}

STRONG_OFFSETS = {
    "left": (-1, 0),
    "center": (0, 0),
    "right": (1, 0),
    "gate_p_a": (2, 0),
    "gate_p_b": (1, 1),
    "gate_m_a": (-2, 0),
    "gate_m_b": (-1, -1),
}


def eca(rule: int, left: int, center: int, right: int) -> int:
    idx = (left << 2) | (center << 1) | right
    return (rule >> idx) & 1


def source_essential(rule: int) -> dict[str, bool]:
    names = ["left", "center", "right"]
    out: dict[str, bool] = {}
    for index, name in enumerate(names):
        essential = False
        for values in itertools.product((0, 1), repeat=3):
            flipped = list(values)
            flipped[index] ^= 1
            if eca(rule, *values) != eca(rule, *flipped):
                essential = True
                break
        out[name] = essential
    return out


def directional_rank(offsets: list[tuple[int, int]]) -> int:
    vectors = [v for v in offsets if v != (0, 0)]
    if not vectors:
        return 0
    first = vectors[0]
    if any(first[0] * v[1] - first[1] * v[0] != 0 for v in vectors[1:]):
        return 2
    return 1


def affine_dimension(points: list[tuple[int, int]]) -> int:
    if len(points) <= 1:
        return 0
    x0, y0 = points[0]
    vectors = [(x - x0, y - y0) for x, y in points[1:]]
    first = next((v for v in vectors if v != (0, 0)), None)
    if first is None:
        return 0
    if any(first[0] * v[1] - first[1] * v[0] != 0 for v in vectors):
        return 2
    return 1


def active_output(rule: int, values: dict[str, int]) -> int:
    return eca(rule, values["left"], values["center"], values["right"])


def gated_output(rule: int, values: dict[str, int]) -> int:
    base = eca(rule, values["left"], values["center"], values["right"])
    return base ^ values["gate_a"] ^ values["gate_b"]


def strong_output(rule: int, values: dict[str, int]) -> int:
    base = eca(rule, values["left"], values["center"], values["right"])
    return (
        base
        ^ values["gate_p_a"]
        ^ values["gate_p_b"]
        ^ values["gate_m_a"]
        ^ values["gate_m_b"]
    )


def strong_essential(rule: int) -> dict[str, bool]:
    names = list(STRONG_OFFSETS)
    out: dict[str, bool] = {}
    for name in names:
        essential = False
        for bits in itertools.product((0, 1), repeat=len(names)):
            values = dict(zip(names, bits))
            flipped = dict(values)
            flipped[name] ^= 1
            if strong_output(rule, values) != strong_output(rule, flipped):
                essential = True
                break
        out[name] = essential
    return out


def gated_essential(rule: int) -> dict[str, bool]:
    names = list(GATED_OFFSETS)
    out: dict[str, bool] = {}
    for index, name in enumerate(names):
        essential = False
        for bits in itertools.product((0, 1), repeat=len(names)):
            values = dict(zip(names, bits))
            flipped = dict(values)
            flipped[name] ^= 1
            if gated_output(rule, values) != gated_output(rule, flipped):
                essential = True
                break
        out[name] = essential
    return out


def step_1d(rule: int, state: tuple[int, ...]) -> tuple[int, ...]:
    n = len(state)
    return tuple(
        eca(rule, state[(i - 1) % n], state[i], state[(i + 1) % n])
        for i in range(n)
    )


def encode_torus(state: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    n = len(state)
    return tuple(tuple(state[(x + y) % n] for x in range(n)) for y in range(n))


def step_active(rule: int, field: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    n = len(field)
    return tuple(
        tuple(
            eca(
                rule,
                field[y][(x - 1) % n],
                field[y][x],
                field[(y + 1) % n][x],
            )
            for x in range(n)
        )
        for y in range(n)
    )


def step_strong(rule: int, field: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    n = len(field)
    return tuple(
        tuple(
            eca(
                rule,
                field[y][(x - 1) % n],
                field[y][x],
                field[y][(x + 1) % n],
            )
            ^ field[y][(x + 2) % n]
            ^ field[(y + 1) % n][(x + 1) % n]
            ^ field[y][(x - 2) % n]
            ^ field[(y - 1) % n][(x - 1) % n]
            for x in range(n)
        )
        for y in range(n)
    )


def step_gated(rule: int, field: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    n = len(field)
    return tuple(
        tuple(
            eca(
                rule,
                field[y][(x - 1) % n],
                field[y][x],
                field[y][(x + 1) % n],
            )
            ^ field[y][(x + 2) % n]
            ^ field[(y + 1) % n][(x + 1) % n]
            for x in range(n)
        )
        for y in range(n)
    )


def main() -> None:
    local_active_failures: list[dict[str, object]] = []
    local_gated_failures: list[dict[str, object]] = []
    active_rank2_rules: list[int] = []
    gated_rank2_rules: list[int] = []
    active_affine2_rules: list[int] = []
    strong_affine2_rules: list[int] = []
    local_strong_failures: list[dict[str, object]] = []
    all_rule_details: dict[str, object] = {}

    for rule in range(256):
        source_ess = source_essential(rule)

        # The active construction reads logical -1,0,+1 from west, center, north.
        for triple in itertools.product((0, 1), repeat=3):
            values = dict(zip(("left", "center", "right"), triple))
            if active_output(rule, values) != eca(rule, *triple):
                local_active_failures.append({"rule": rule, "triple": triple})

            # On an encoded state, gate_a and gate_b represent the same logical +2 bit.
            for plus_two in (0, 1):
                gated_values = {
                    "left": triple[0],
                    "center": triple[1],
                    "right": triple[2],
                    "gate_a": plus_two,
                    "gate_b": plus_two,
                }
                if gated_output(rule, gated_values) != eca(rule, *triple):
                    local_gated_failures.append(
                        {"rule": rule, "triple": triple, "plus_two": plus_two}
                    )

        active_essential_offsets = [
            ACTIVE_OFFSETS[name] for name, essential in source_ess.items() if essential
        ]
        active_rank = directional_rank(active_essential_offsets)
        active_affine = affine_dimension(active_essential_offsets)
        if active_rank == 2:
            active_rank2_rules.append(rule)
        if active_affine == 2:
            active_affine2_rules.append(rule)

        gated_ess = gated_essential(rule)
        gated_essential_offsets = [
            GATED_OFFSETS[name] for name, essential in gated_ess.items() if essential
        ]
        gated_rank = directional_rank(gated_essential_offsets)
        if gated_rank == 2:
            gated_rank2_rules.append(rule)

        strong_ess = strong_essential(rule)
        strong_essential_offsets = [
            STRONG_OFFSETS[name] for name, essential in strong_ess.items() if essential
        ]
        strong_affine = affine_dimension(strong_essential_offsets)
        if strong_affine == 2:
            strong_affine2_rules.append(rule)

        for triple in itertools.product((0, 1), repeat=3):
            for plus_two, minus_two in itertools.product((0, 1), repeat=2):
                strong_values = {
                    "left": triple[0],
                    "center": triple[1],
                    "right": triple[2],
                    "gate_p_a": plus_two,
                    "gate_p_b": plus_two,
                    "gate_m_a": minus_two,
                    "gate_m_b": minus_two,
                }
                if strong_output(rule, strong_values) != eca(rule, *triple):
                    local_strong_failures.append(
                        {
                            "rule": rule,
                            "triple": triple,
                            "plus_two": plus_two,
                            "minus_two": minus_two,
                        }
                    )

        all_rule_details[str(rule)] = {
            "source_essential": source_ess,
            "active_directional_rank": active_rank,
            "active_affine_dimension": active_affine,
            "gated_essential": gated_ess,
            "gated_directional_rank": gated_rank,
            "strong_essential": strong_ess,
            "strong_affine_dimension": strong_affine,
        }

    global_failures: list[dict[str, object]] = []
    global_checks = 0
    for rule in SELECTED_GLOBAL_RULES:
        for width in WIDTHS:
            for bits in itertools.product((0, 1), repeat=width):
                source_next = step_1d(rule, bits)
                encoded = encode_torus(bits)
                expected = encode_torus(source_next)
                for construction, actual in (
                    ("active", step_active(rule, encoded)),
                    ("gated", step_gated(rule, encoded)),
                    ("strong", step_strong(rule, encoded)),
                ):
                    global_checks += 1
                    if actual != expected:
                        global_failures.append(
                            {
                                "rule": rule,
                                "width": width,
                                "state": bits,
                                "construction": construction,
                            }
                        )

    result = {
        "protocol": "docs/research/protocols/dimensional-intertwining-20260909.md",
        "embedding": "E(s)(x,y)=s((x+y) mod n) on finite tori; same formula over Z in the proof",
        "active_offsets": ACTIVE_OFFSETS,
        "gated_offsets": GATED_OFFSETS,
        "strong_offsets": STRONG_OFFSETS,
        "local": {
            "eca_rules_checked": 256,
            "source_triples_per_rule": 8,
            "active_failures": local_active_failures,
            "gated_equal-pair_failures": local_gated_failures,
            "active_rank2_count": len(active_rank2_rules),
            "active_rank2_rules": active_rank2_rules,
            "active_rank_lt2_rules": [r for r in range(256) if r not in active_rank2_rules],
            "gated_rank2_count": len(gated_rank2_rules),
            "gated_rank2_rules": gated_rank2_rules,
            "active_affine2_count": len(active_affine2_rules),
            "active_affine2_rules": active_affine2_rules,
            "active_affine_lt2_rules": [r for r in range(256) if r not in active_affine2_rules],
            "strong_failures": local_strong_failures,
            "strong_affine2_count": len(strong_affine2_rules),
            "strong_affine2_rules": strong_affine2_rules,
        },
        "global_periodic_audit": {
            "rules": SELECTED_GLOBAL_RULES,
            "widths": WIDTHS,
            "construction_state_checks": global_checks,
            "failures": global_failures,
        },
        "rules": all_rule_details,
    }

    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    assert not local_active_failures
    assert not local_gated_failures
    assert len(active_rank2_rules) == 228
    assert len(gated_rank2_rules) == 256
    assert len(active_affine2_rules) == 218
    assert not local_strong_failures
    assert len(strong_affine2_rules) == 256
    assert not global_failures

    # Keep the published compact summary tied to this executable census.
    summary = json.loads(Path("results/dimensional_intertwining_20260909_summary.json").read_text())
    assert summary["checks"] == {
        "local_active_intertwining_failures": len(local_active_failures),
        "local_two_site_gate_intertwining_failures": len(local_gated_failures),
        "local_four_site_gate_intertwining_failures": len(local_strong_failures),
        "active_linear_rank_2_rules": len(active_rank2_rules),
        "active_affine_dimension_2_rules": len(active_affine2_rules),
        "two_site_gate_linear_rank_2_rules": len(gated_rank2_rules),
        "four_site_gate_affine_dimension_2_rules": len(strong_affine2_rules),
        "selected_global_periodic_construction_state_checks": global_checks,
        "selected_global_periodic_failures": len(global_failures),
    }
    assert summary["selected_global_rules"] == SELECTED_GLOBAL_RULES
    assert summary["selected_global_widths"] == WIDTHS

    print(json.dumps({
        "active_rank2_count": len(active_rank2_rules),
        "gated_rank2_count": len(gated_rank2_rules),
        "active_affine2_count": len(active_affine2_rules),
        "strong_affine2_count": len(strong_affine2_rules),
        "global_checks": global_checks,
        "result": str(RESULT_PATH),
    }, indent=2))


if __name__ == "__main__":
    main()
