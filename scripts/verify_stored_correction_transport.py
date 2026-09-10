#!/usr/bin/env python3
"""Physical correction transport, its protected triangle, and a failed zero cap."""
from __future__ import annotations

import functools
import itertools
import json

import verify_editable_routing_tables as base
import verify_finite_routing_boundaries as finite

FREEZE = "c48a52e5d7bab7b5fa0d7b4e8125b3968506f9eb"
TRANSPORT, WIDTH, HEIGHT = 60, 3, 2


def evolve(word, state, width):
    result = 0
    for x in range(width):
        left = (state >> ((x - 1) % width)) & 1
        center = (state >> x) & 1
        right = (state >> ((x + 1) % width)) & 1
        result |= ((word >> (4 * left + 2 * center + right)) & 1) << x
    return result


def run_audit():
    assertions = 0

    def check(condition, message):
        nonlocal assertions
        assertions += 1
        if not condition:
            raise AssertionError(message)

    local_cases = 0
    for word in range(256):
        for data in itertools.product((0, 1), repeat=5):
            origin, symbols = base.local_patch((word, TRANSPORT), data)
            actual = base.physical_value(2, origin, lambda p: symbols.get(p, base.B)) - base.D0
            leaf = (word >> (4 * data[0] + 2 * data[1] + data[2])) & 1
            check(actual == leaf ^ data[3], "stored transport table implements F(row) xor row above")
            local_cases += 1

    cases, compared_symbols, protected_bits, outside_bits, outside_mismatches = 0, 0, 0, 0, 0
    bottom_failures, witness = 0, None
    for word in range(256):
        @functools.lru_cache(maxsize=None)
        def correction(depth, state):
            if depth == 0:
                return state ^ evolve(word, state, WIDTH)
            return (correction(depth - 1, evolve(word, state, WIDTH))
                    ^ evolve(word, correction(depth - 1, state), WIDTH))

        for initial in range(1 << WIDTH):
            state = initial
            rows = {k: correction(k, state) for k in range(HEIGHT + 1)}
            logical = {(x, k): ((word, TRANSPORT), (rows.get(k, 0) >> x) & 1)
                       for x in range(WIDTH) for k in range(-1, HEIGHT + 2)}
            physical = finite.MaskedField.encode(logical, 2, (WIDTH,))
            support = set(physical.symbols)
            failed_bottom = False
            record = []
            for tick in range(1, 5):
                state = evolve(word, state, WIDTH)
                logical = finite.logical_step(logical, 2, (WIDTH,))
                physical = physical.step()
                expected = finite.MaskedField.encode(logical, 2, (WIDTH,))
                check(physical.symbols == expected.symbols, "complete finite correction field")
                check(set(physical.symbols) == support, "finite support is unchanged")
                decoded = physical.decode()
                check(all(program == (word, TRANSPORT) for program, _ in decoded.values()),
                      "all physically stored instructions remain unchanged")
                compared_symbols += len(physical.symbols)
                actual_rows = [sum(decoded[x, k][1] << x for x in range(WIDTH))
                               for k in range(HEIGHT + 1)]
                true_rows = [correction(k, state) for k in range(HEIGHT + 1)]
                for k in range(HEIGHT + 1):
                    for x in range(WIDTH):
                        agrees = ((actual_rows[k] ^ true_rows[k]) >> x) & 1 == 0
                        if k + tick <= HEIGHT:
                            check(agrees, "prepared correction triangle")
                            protected_bits += 1
                        else:
                            outside_bits += 1
                            outside_mismatches += int(not agrees)
                failed_bottom |= actual_rows[0] != true_rows[0]
                if word == 255 and initial == 0:
                    record.append({"tick": tick, "actual_rows": actual_rows,
                                   "true_correction_rows": true_rows})
            cases += 1
            bottom_failures += int(failed_bottom)
            if record:
                witness = {"word": word, "initial_state": initial, "row_bit_width": WIDTH,
                           "trajectory": record}
    first_errors = [next(row["tick"] for row in witness["trajectory"]
                         if row["actual_rows"][k] != row["true_correction_rows"][k])
                    for k in range(HEIGHT + 1)]
    check(first_errors == [3, 2, 1], "zero-cap error reaches lower rows one step at a time")
    check(witness["trajectory"][2]["actual_rows"][0] == 7
          and witness["trajectory"][2]["true_correction_rows"][0] == 0,
          "retained explicit bottom failure")
    witness["first_error_tick_by_row"] = first_errors
    return {
        "schema_version": 1,
        "protocol": "docs/research/protocols/stored-correction-transport-20260910.md",
        "protocol_freeze_commit": FREEZE,
        "assertions": assertions,
        "transport_program_word": TRANSPORT,
        "physical_local_cases": local_cases,
        "finite_stack": {"cases": cases, "source_width": WIDTH, "prepared_max_correction_index": HEIGHT,
                         "ticks_each": 4, "compared_physical_symbols": compared_symbols,
                         "protected_triangle_bit_comparisons": protected_bits,
                         "outside_triangle_bit_comparisons": outside_bits,
                         "outside_triangle_mismatches": outside_mismatches,
                         "cases_with_bottom_discrepancy_by_tick4": bottom_failures},
        "zero_cap_failure_witness": witness,
        "protocol_deviations": [], "implementation_corrections": [],
        "scope": "Stored homogeneous source rule and transport table in hold mode. Finite prepared triangle, not indefinite correction closure or a source-state embedding.",
    }


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
