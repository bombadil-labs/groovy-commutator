#!/usr/bin/env python3
"""Audit program-edit support and dimensional patch counts; no external packages."""
from __future__ import annotations

import itertools
import json

from verify_dimensional_intertwining import encode_torus, step_1d, step_active, step_strong


def run_audit() -> dict:
    assertions = 0

    def check(condition: bool, message: str) -> None:
        nonlocal assertions
        assertions += 1
        if not condition:
            raise AssertionError(message)

    global_cases = 0
    local_cases = 0
    global_disagreement_counts: dict[str, list[int]] = {}
    for width in (9, 15, 21):
        observed = set()
        for rule in range(256):
            for address in range(8):
                left, center, right = (address >> 2) & 1, (address >> 1) & 1, address & 1
                state = tuple((center, right, left)[i % 3] for i in range(width))
                changed_rule = rule ^ (1 << address)
                before = step_1d(rule, state)
                after = step_1d(changed_rule, state)
                disagreement = {i for i in range(width) if before[i] != after[i]}
                check(set(range(0, width, 3)) <= disagreement, "periodic global edit witness")
                expected_size = width if address in (0, 7) else width // 3
                check(len(disagreement) == expected_size, "exact periodic witness support")
                observed.add(len(disagreement))
                global_cases += 1
                if width == 9:
                    # One fixed interpreter; the program field differs at only one site.
                    program = [rule] * width
                    program[0] = changed_rule
                    local_after = tuple(
                        (program[i] >> (4 * state[(i-1) % width] +
                                        2 * state[i] + state[(i+1) % width])) & 1
                        for i in range(width)
                    )
                    check({i for i in range(width) if before[i] != local_after[i]} == {0},
                          "per-site program edit")
                    local_cases += 1
        global_disagreement_counts[str(width)] = sorted(observed)

    stripe_edit_cases = 0
    stripe_supports = []
    for width in range(2, 17):
        original = encode_torus((0,) * width)
        counts = set()
        for edited_site in range(width):
            source = [0] * width
            source[edited_site] = 1
            edited = encode_torus(tuple(source))
            actual = {(x, y) for y in range(width) for x in range(width)
                      if original[y][x] != edited[y][x]}
            expected = {(x, y) for y in range(width) for x in range(width)
                        if (x + y) % width == edited_site}
            check(actual == expected, "stripe edit geometry")
            check(len(actual) == width, "stripe edit support")
            counts.add(len(actual))
            stripe_edit_cases += 1
        stripe_supports.append({"width": width, "support_sizes": sorted(counts)})

    patch_counts = []
    for side in range(1, 8):
        stripes = {
            tuple(source[x + y] for y in range(side) for x in range(side))
            for source in itertools.product((0, 1), repeat=2 * side - 1)
        }
        center_row = side // 2
        interfaces = {
            tuple(source[x] if y == center_row else int(y < center_row)
                  for y in range(side) for x in range(side))
            for source in itertools.product((0, 1), repeat=side)
        }
        check(len(stripes) == 2 ** (2 * side - 1), "stripe patch count")
        check(len(interfaces) == 2 ** side, "interface patch count")
        patch_counts.append({"side": side, "stripe_patterns": len(stripes),
                             "interface_patterns": len(interfaces),
                             "unrestricted_binary_patterns": 2 ** (side * side)})

    # Actual 2D evolution under two independent laws from the recovered checkpoint.
    # The field generator is an explicitly fixed 32-bit LCG, avoiding RNG-version drift.
    width = 21
    origin = width // 2
    ticks = 4
    selected_rules = (0, 30, 54, 90, 110, 150, 204, 255)
    field_cases = 0
    timepoint_checks = 0
    outside_cone_comparisons = 0
    observed_max_distance = {"active": 0, "strong": 0}
    for seed in (1, 2, 3, 4):
        word = seed
        rows = []
        for _y in range(width):
            row = []
            for _x in range(width):
                word = (1664525 * word + 1013904223) & 0xFFFFFFFF
                row.append((word >> 31) & 1)
            rows.append(tuple(row))
        initial = tuple(rows)
        edited_rows = [list(row) for row in initial]
        edited_rows[origin][origin] ^= 1
        edited_initial = tuple(tuple(row) for row in edited_rows)
        for rule in selected_rules:
            for name, step, radius in (("active", step_active, 1), ("strong", step_strong, 2)):
                field, edited = initial, edited_initial
                field_cases += 1
                for tick in range(1, ticks + 1):
                    field, edited = step(rule, field), step(rule, edited)
                    for y in range(width):
                        for x in range(width):
                            dx, dy = abs(x-origin), abs(y-origin)
                            distance = max(min(dx, width-dx), min(dy, width-dy))
                            if field[y][x] != edited[y][x]:
                                observed_max_distance[name] = max(observed_max_distance[name], distance)
                            if distance > radius * tick:
                                check(field[y][x] == edited[y][x], "finite propagation cone")
                                outside_cone_comparisons += 1
                    timepoint_checks += 1

    return {
        "schema_version": 1,
        "protocol": "docs/research/protocols/program-edit-locality-20260909.md",
        "protocol_freeze_commit": "d665bc9ecd3cf15ee2842f8531996a4a4516b872",
        "assertions": assertions,
        "global_instruction_edits": {
            "rules": 256, "instruction_bits": 8, "widths": [9, 15, 21],
            "cases": global_cases, "disagreement_counts_by_width": global_disagreement_counts,
        },
        "per_site_program_edits": {"width": 9, "cases": local_cases, "changed_output_support": [0]},
        "stripe_state_edits": {"cases": stripe_edit_cases, "by_width": stripe_supports},
        "patch_counts": patch_counts,
        "finite_propagation": {
            "rules": list(selected_rules), "seeds": [1, 2, 3, 4],
            "field_generator": "LCG: x = (1664525*x + 1013904223) mod 2^32; output high bit",
            "width": width, "ticks": ticks, "field_cases": field_cases,
            "timepoint_checks": timepoint_checks,
            "outside_cone_comparisons": outside_cone_comparisons,
            "maximum_observed_distance": observed_max_distance,
            "radius_bounds": {"active": 1, "strong": 2},
        },
        "protocol_deviations": [],
        "scope": "Finite audits support explicit locality/counting proofs; no impossibility of recursive spatial programs is claimed.",
    }


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
