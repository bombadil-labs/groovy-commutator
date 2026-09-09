#!/usr/bin/env python3
"""Exact audit of spatial Rail programs. Five symbols, fixed radius nine."""
from __future__ import annotations

import itertools
import json

B, D0, D1, P0, P1 = range(5)
GUARD = 204
SCALE = 9


def logical_value(word, data):
    """Independent scalar source semantics; data order is L,C,R,+e2,-e2,..."""
    value = (word >> (4 * data[0] + 2 * data[1] + data[2])) & 1
    for index in range(3, len(data), 2):
        value = data[index + value]
    return value


def shifted(position, axis, amount):
    out = list(position)
    out[axis] += amount
    return tuple(out)


def physical_value(dimension, position, get):
    """The same total symbol rule is used on data, program, and blank sites."""
    center = get(position)
    if center not in (D0, D1):
        return center
    program = [get(shifted(position, dimension - 1, q + 1)) for q in range(8)]
    taps = [shifted(position, 0, -SCALE), position, shifted(position, 0, SCALE)]
    for axis in range(1, dimension):
        taps.extend((shifted(position, axis, SCALE), shifted(position, axis, -SCALE)))
    symbols = [get(p) for p in taps]
    if any(p not in (P0, P1) for p in program) or any(s not in (D0, D1) for s in symbols):
        return center
    data = [s - D0 for s in symbols]
    # A physical selector tree, independent of logical_value's integer LUT address.
    leaves = [p - P0 for p in program]
    for control in (data[2], data[1], data[0]):
        leaves = [leaves[2 * j + control] for j in range(len(leaves) // 2)]
    value = leaves[0]
    for axis in range(1, dimension):
        positive, negative = data[2 * axis + 1:2 * axis + 3]
        value = positive if value == 0 else negative
    return D0 + value


def local_physical_patch(dimension, word, data):
    origin = (0,) * dimension
    field = {origin: D0 + data[1]}
    field[shifted(origin, 0, -SCALE)] = D0 + data[0]
    field[shifted(origin, 0, SCALE)] = D0 + data[2]
    for axis in range(1, dimension):
        field[shifted(origin, axis, SCALE)] = D0 + data[2 * axis + 1]
        field[shifted(origin, axis, -SCALE)] = D0 + data[2 * axis + 2]
    for q in range(8):
        field[shifted(origin, dimension - 1, q + 1)] = P0 + ((word >> q) & 1)
    return origin, field


def local_interface(dimension, source_word, guard_word, data, repeated=False):
    """Compare all five transverse layers around one arbitrary source patch."""
    evolved = logical_value(source_word, data)
    comparisons = []
    for layer in range(-2, 3):
        value = data[1] if layer == 0 else int(layer < 0)
        central = data if layer == 0 else [value] * (2 * dimension + 1)
        positive = data[1] if layer == -1 else int(layer + 1 < 0)
        negative = data[1] if layer == 1 else int(layer - 1 < 0)
        word = source_word if layer == 0 or repeated else guard_word
        actual = logical_value(word, central + [positive, negative])
        expected = evolved if layer == 0 else int(layer < 0)
        comparisons.append(actual == expected)
    return comparisons


def coordinates(dimension, periods, radius):
    return itertools.product(*(range(periods[a]) if a < len(periods)
                               else range(-radius, radius + 1) for a in range(dimension)))


class PhysicalField:
    """Sparse exact storage: omitted sites are B, and B remains B under the CA."""
    def __init__(self, dimension, periods, radius, symbols):
        self.dimension = dimension
        self.periods = tuple(periods)
        self.radius = radius
        self.symbols = symbols

    @classmethod
    def encode(cls, dimension, periods, radius, pair_at):
        symbols = {}
        for logical in coordinates(dimension, periods, radius):
            word, value = pair_at(logical)
            origin = tuple(SCALE * x for x in logical)
            symbols[origin] = D0 + value
            for q in range(8):
                symbols[shifted(origin, dimension - 1, q + 1)] = P0 + ((word >> q) & 1)
        return cls(dimension, periods, radius, symbols)

    def get(self, position):
        key = tuple(x % (SCALE * self.periods[a]) if a < len(self.periods) else x
                    for a, x in enumerate(position))
        return self.symbols.get(key, B)

    def edit(self, logical, bit=None):
        physical = tuple(SCALE * x for x in logical)
        if bit is None:
            self.symbols[physical] = D0 + (1 - (self.symbols[physical] - D0))
        else:
            physical = shifted(physical, self.dimension - 1, bit + 1)
            self.symbols[physical] = P0 + (1 - (self.symbols[physical] - P0))
        return physical

    def step(self):
        radius = self.radius - 1 if len(self.periods) < self.dimension else self.radius
        output = {}
        for logical in coordinates(self.dimension, self.periods, radius):
            origin = tuple(SCALE * x for x in logical)
            for q in range(-1, 8):
                position = origin if q == -1 else shifted(origin, self.dimension - 1, q + 1)
                output[position] = physical_value(self.dimension, position, self.get)
        return PhysicalField(self.dimension, self.periods, radius, output)


def lift_pair_at(source, source_dimension, target_dimension):
    def pair_at(position):
        for axis in reversed(range(source_dimension, target_dimension)):
            if position[axis] != 0:
                return GUARD, int(position[axis] < 0)
        return source[position[:source_dimension]]
    return pair_at


def source_step(source, dimension, periods):
    def data_at(position):
        key = tuple(x % periods[a] for a, x in enumerate(position))
        return source[key][1]
    result = {}
    for position, (word, _value) in source.items():
        data = [data_at(shifted(position, 0, -1)), data_at(position),
                data_at(shifted(position, 0, 1))]
        for axis in range(1, dimension):
            data.extend((data_at(shifted(position, axis, 1)),
                         data_at(shifted(position, axis, -1))))
        result[position] = word, logical_value(word, data)
    return result


def run_audit():
    assertion_count = 0
    def check(condition, message):
        nonlocal assertion_count
        assertion_count += 1
        if not condition:
            raise AssertionError(message)

    local_counts = {}
    instruction_witnesses = 0
    malformed_checks = 0
    for dimension in (1, 2, 3):
        count = 0
        for word in range(256):
            for data in itertools.product((0, 1), repeat=2 * dimension + 1):
                origin, field = local_physical_patch(dimension, word, data)
                actual = physical_value(dimension, origin, lambda p: field.get(p, B)) - D0
                check(actual == logical_value(word, data), "physical/logical local evaluation")
                count += 1
            for address in range(8):
                data = [(address >> 2) & 1, (address >> 1) & 1, address & 1] + [0, 1] * (dimension - 1)
                origin, field = local_physical_patch(dimension, word, data)
                get = lambda p: field.get(p, B)
                before = physical_value(dimension, origin, get) - D0
                location = shifted(origin, dimension - 1, address + 1)
                field[location] = P0 + (1 - (field[location] - P0))
                after = physical_value(dimension, origin, get) - D0
                check(before == ((word >> address) & 1) and after == 1 - before,
                      "one physical instruction edit has an inherited witness")
                instruction_witnesses += 1
        local_counts[str(dimension)] = count

        origin, field = local_physical_patch(dimension, 110, [0, 1, 0] + [0, 1] * (dimension - 1))
        valid = dict(field)
        # Every required program slot and neighbor data tap has an explicit type guard.
        for position in field:
            if position == origin:
                continue
            modified = dict(valid)
            modified[position] = B
            check(physical_value(dimension, origin, lambda p: modified.get(p, B)) == valid[origin],
                  "malformed slot retains data center")
            malformed_checks += 1
        for center in (B, P0, P1):
            modified = dict(valid)
            modified[origin] = center
            check(physical_value(dimension, origin, lambda p: modified.get(p, B)) == center,
                  "program and blank symbols are retained")
            malformed_checks += 1
        for center in (D0, D1):
            modified = {origin: center}
            check(physical_value(dimension, origin, lambda p: modified.get(p, B)) == center,
                  "both malformed data symbols are retained")
            malformed_checks += 1

    repeated_pass = []
    for word in range(256):
        passed = all(all(local_interface(1, word, GUARD, list(data), repeated=True))
                     for data in itertools.product((0, 1), repeat=3))
        check(passed == (word & 1 == 0 and word & 128 != 0), "repeated-program endpoint result")
        if passed:
            repeated_pass.append(word)

    good_guards = []
    guard_source_cases = 0
    guard_layer_comparisons = 0
    for guard in range(256):
        passing_sources = 0
        for word in range(256):
            passed = True
            for data in itertools.product((0, 1), repeat=3):
                comparisons = local_interface(1, word, guard, list(data))
                passed = all(comparisons) and passed
                guard_layer_comparisons += len(comparisons)
            if passed:
                passing_sources += 1
            guard_source_cases += 1
        expected = 256 if guard & 1 == 0 and guard & 128 != 0 else 0
        check(passing_sources == expected, "guard/source matrix")
        if passing_sources:
            good_guards.append(guard)
    check(GUARD in good_guards and len(good_guards) == 64, "fixed guard admissibility")

    second_comparisons = 0
    for word in range(256):
        for data in itertools.product((0, 1), repeat=5):
            for comparison in local_interface(2, word, GUARD, list(data)):
                check(comparison, "arbitrary-source second interface")
                second_comparisons += 1

    field_stats = {}
    def field_case(initial, source_dimension, periods, ticks, target_dimensions, actions=False):
        source = dict(initial)
        # Core radius two remains after discarding one open macrocell layer per tick.
        initial_radius = ticks + 2
        source_physical = PhysicalField.encode(source_dimension, periods, 0, lambda p: source[p])
        targets = {d: PhysicalField.encode(d, periods, initial_radius,
                                           lift_pair_at(source, source_dimension, d))
                   for d in target_dimensions}
        counts = {"timepoints": 0, "compared_symbols": 0, "physical_payload_edits": 0}
        for tick in range(ticks):
            if actions:
                position = tuple((tick + axis) % periods[axis] for axis in range(source_dimension))
                address = tick % 8
                word, value = source[position]
                source[position] = (word ^ (1 << address), value ^ 1)
                for field in [source_physical, *targets.values()]:
                    where = position + (0,) * (field.dimension - source_dimension)
                    before = dict(field.symbols)
                    datum_location = field.edit(where)
                    program_location = field.edit(where, address)
                    changed = {p for p in before if before[p] != field.symbols[p]}
                    check(changed == {datum_location, program_location}, "two matched local payload edits")
                    counts["physical_payload_edits"] += 2

            source = source_step(source, source_dimension, periods)
            source_physical = source_physical.step()
            expected_source = PhysicalField.encode(source_dimension, periods, 0, lambda p: source[p])
            check(source_physical.symbols == expected_source.symbols, "whole source physical interpreter")
            counts["compared_symbols"] += len(expected_source.symbols)
            for dimension in target_dimensions:
                targets[dimension] = targets[dimension].step()
                actual = targets[dimension]
                expected = PhysicalField.encode(dimension, periods, actual.radius,
                    lift_pair_at(source, source_dimension, dimension))
                # Exact sparse-map equality compares every occupied value/tag and all omitted B sites.
                check(actual.symbols == expected.symbols, "full spatial program/state lift")
                counts["compared_symbols"] += len(expected.symbols)
                counts["timepoints"] += 1
        return counts

    totals = {"cases": 0, "timepoints": 0, "compared_symbols": 0, "physical_payload_edits": 0}
    for word in range(256):
        for state in itertools.product((0, 1), repeat=3):
            initial = {(x,): (word, value) for x, value in enumerate(state)}
            result = field_case(initial, 1, (3,), 3, (2, 3))
            totals["cases"] += 1
            for key, value in result.items():
                totals[key] += value
    field_stats["all_homogeneous_sources"] = totals

    def random_source(seed, dimension, periods):
        word = seed
        result = {}
        for position in coordinates(dimension, periods, 0):
            word = (1664525 * word + 1013904223) & 0xFFFFFFFF
            program = (word >> 16) & 255
            word = (1664525 * word + 1013904223) & 0xFFFFFFFF
            result[position] = program, (word >> 31) & 1
        return result

    for name, cases, dimension, periods, ticks, targets in (
        ("heterogeneous_sources_with_actions", 16, 1, (5,), 4, (2, 3)),
        ("arbitrary_second_interface_with_actions", 32, 2, (3, 3), 3, (3,)),
    ):
        totals = {"cases": cases, "timepoints": 0, "compared_symbols": 0, "physical_payload_edits": 0}
        for seed in range(1, cases + 1):
            result = field_case(random_source(seed, dimension, periods), dimension, periods,
                                ticks, targets, actions=True)
            for key, value in result.items():
                totals[key] += value
        field_stats[name] = totals

    return {
        "schema_version": 1,
        "protocol": "docs/research/protocols/spatial-rail-programs-20260909.md",
        "protocol_freeze_commit": "7e3d58ca1eb9ab21a0b446fb622eead543f5f811",
        "assertions": assertion_count,
        "physical": {"alphabet": ["B", "D0", "D1", "P0", "P1"], "radius": 9, "scale": 9,
                     "tick_ratio": 1, "cells_per_macrocell_by_dimension": [9, 81, 729],
                     "occupied_symbols_per_macrocell": 9},
        "local_physical_logical_comparisons": local_counts,
        "instruction_edit_witnesses": instruction_witnesses,
        "malformed_layout_checks": malformed_checks,
        "repeated_source_program_variant": {"passing_count": len(repeated_pass), "passing_rules": repeated_pass,
                                           "one_source_program_edit_support": "infinite transverse line"},
        "separate_guard_variant": {"fixed_guard": GUARD, "guard_source_cases": guard_source_cases,
                                   "layer_comparisons": guard_layer_comparisons,
                                   "admissible_first_guards": good_guards,
                                   "passing_source_count_with_fixed_guard": 256,
                                   "second_interface_comparisons": second_comparisons},
        "physical_fields": field_stats,
        "protocol_deviations": [],
        "scope": "Retained but locally editable program words in a declared Rail grammar; no tag self-organization, autonomous program rewriting, or binary radius-one claim.",
    }


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
