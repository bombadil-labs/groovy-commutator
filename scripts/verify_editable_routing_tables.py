#!/usr/bin/env python3
"""Audit a frozen, costed CA family with one editable table per spatial axis.

Logical execution uses integer LUT indexing. Physical execution reads symbols
at relative coordinates and reduces selector trees. No prior saved result is
used as input. Finite field checks support the separate local proofs.
"""
from __future__ import annotations

import itertools
import json

B, D0, D1, P0, P1 = range(5)
SCALE, MUX, IDENTITY, FIRST = 9, 172, 204, 240
FREEZE = "68f8437ef7166e6fa85ddc812d77b4c5381d31ac"


def shifted(position, axis, amount):
    result = list(position)
    result[axis] += amount
    return tuple(result)


def coordinates(dimension, periods, radius):
    return itertools.product(*(range(periods[a]) if a < len(periods)
                               else range(-radius, radius + 1)
                               for a in range(dimension)))


def logical_value(program, data):
    """Data order L,C,R,+e2,-e2,...; all words belong to the updated site."""
    value = (program[0] >> (4 * data[0] + 2 * data[1] + data[2])) & 1
    for axis, word in enumerate(program[1:], 1):
        value = (word >> (4 * value + 2 * data[2 * axis + 1]
                         + data[2 * axis + 2])) & 1
    return value


def guard(dimension):
    return (IDENTITY,) + (MUX,) * (dimension - 1)


def physical_value(dimension, position, get, copy=False):
    """One total, translation-invariant symbol rule per dimension and mode."""
    center = get(position)
    if center == B:
        return B
    if center in (P0, P1):
        if not copy:
            return center
        owners = [get(shifted(position, axis, -distance))
                  for axis in range(dimension) for distance in range(1, 9)]
        owners = [symbol for symbol in owners if symbol in (D0, D1)]
        neighbor = get(shifted(position, 0, -SCALE))
        return neighbor if (owners == [D1] and neighbor in (P0, P1)) else center

    words = [[get(shifted(position, axis, q + 1)) for q in range(8)]
             for axis in range(dimension)]
    taps = [shifted(position, 0, -SCALE), position, shifted(position, 0, SCALE)]
    for axis in range(1, dimension):
        taps.extend((shifted(position, axis, SCALE), shifted(position, axis, -SCALE)))
    symbols = [get(p) for p in taps]
    if (any(bit not in (P0, P1) for word in words for bit in word)
            or any(value not in (D0, D1) for value in symbols)):
        return center
    data = [value - D0 for value in symbols]
    value = 0
    for axis, word in enumerate(words):
        controls = data[:3] if axis == 0 else [value, *data[2 * axis + 1:2 * axis + 3]]
        leaves = [bit - P0 for bit in word]
        for control in reversed(controls):
            leaves = [leaves[2 * j + control] for j in range(len(leaves) // 2)]
        value = leaves[0]
    return D0 + value


def local_patch(program, data):
    dimension = len(program)
    origin = (0,) * dimension
    symbols = {origin: D0 + data[1]}
    symbols[shifted(origin, 0, -SCALE)] = D0 + data[0]
    symbols[shifted(origin, 0, SCALE)] = D0 + data[2]
    for axis in range(1, dimension):
        symbols[shifted(origin, axis, SCALE)] = D0 + data[2 * axis + 1]
        symbols[shifted(origin, axis, -SCALE)] = D0 + data[2 * axis + 2]
    for axis, word in enumerate(program):
        for q in range(8):
            symbols[shifted(origin, axis, q + 1)] = P0 + ((word >> q) & 1)
    return origin, symbols


class PhysicalField:
    """Omitted sites are B. B stays B, so sparse-map equality is exact."""
    def __init__(self, dimension, periods, radius, symbols, copy):
        self.dimension, self.periods, self.radius = dimension, tuple(periods), radius
        self.symbols, self.copy = symbols, copy

    @classmethod
    def encode(cls, dimension, periods, radius, pair_at, copy):
        symbols = {}
        for logical in coordinates(dimension, periods, radius):
            program, value = pair_at(logical)
            if len(program) != dimension:
                raise ValueError("wrong native program depth")
            origin = tuple(SCALE * x for x in logical)
            symbols[origin] = D0 + value
            for axis, word in enumerate(program):
                for q in range(8):
                    symbols[shifted(origin, axis, q + 1)] = P0 + ((word >> q) & 1)
        return cls(dimension, periods, radius, symbols, copy)

    def get(self, position):
        key = tuple(x % (SCALE * self.periods[a]) if a < len(self.periods) else x
                    for a, x in enumerate(position))
        return self.symbols.get(key, B)

    def edit(self, logical, axis=None, bit=None):
        position = tuple(SCALE * x for x in logical)
        offset = D0
        if axis is not None:
            position = shifted(position, axis, bit + 1)
            offset = P0
        self.symbols[position] = offset + (1 - (self.symbols[position] - offset))
        return position

    def step(self):
        radius = self.radius - int(len(self.periods) < self.dimension)
        output = {}
        for logical in coordinates(self.dimension, self.periods, radius):
            origin = tuple(SCALE * x for x in logical)
            positions = [origin] + [shifted(origin, axis, q + 1)
                                   for axis in range(self.dimension) for q in range(8)]
            for position in positions:
                output[position] = physical_value(self.dimension, position, self.get, self.copy)
        return PhysicalField(self.dimension, self.periods, radius, output, self.copy)


def lifted_pair_at(source, source_dimension, dimension):
    def at(position):
        for axis in reversed(range(source_dimension, dimension)):
            if position[axis]:
                return guard(dimension), int(position[axis] < 0)
        program, value = source[position[:source_dimension]]
        return program + (MUX,) * (dimension - source_dimension), value
    return at


def logical_step(source, periods, copy):
    def key(position):
        return tuple(x % periods[a] for a, x in enumerate(position))

    def datum(position):
        return source[key(position)][1]

    output = {}
    for position, (program, value) in source.items():
        data = [datum(shifted(position, 0, -1)), value, datum(shifted(position, 0, 1))]
        for axis in range(1, len(periods)):
            data.extend((datum(shifted(position, axis, 1)), datum(shifted(position, axis, -1))))
        inherited = source[key(shifted(position, 0, -1))][0] if copy and value else program
        output[position] = inherited, logical_value(program, data)
    return output


def random_source(seed, periods):
    state = seed
    result = {}
    for position in coordinates(len(periods), periods, 0):
        program = []
        for _ in periods:
            state = (1664525 * state + 1013904223) & 0xFFFFFFFF
            program.append((state >> 16) & 255)
        state = (1664525 * state + 1013904223) & 0xFFFFFFFF
        result[position] = tuple(program), (state >> 31) & 1
    return result


def run_audit():
    assertions = 0

    def check(condition, message):
        nonlocal assertions
        assertions += 1
        if not condition:
            raise AssertionError(message)

    local_counts, edit_counts = {}, {}
    malformed, copy_cases = 0, 0
    for dimension in range(1, 5):
        local_counts[str(dimension)] = edit_counts[str(dimension)] = 0
        for stage in range(dimension):
            for word in range(256):
                for address in range(8):
                    inputs = [(address >> 2) & 1, (address >> 1) & 1, address & 1]
                    program = [255 * inputs[0]] + [FIRST] * (dimension - 1)
                    program[stage] = word
                    data = [0] * (2 * dimension + 1)
                    if stage == 0:
                        data[:3] = inputs
                    else:
                        data[2 * stage + 1:2 * stage + 3] = inputs[1:]
                    origin, field = local_patch(program, data)
                    get = lambda p: field.get(p, B)
                    actual = physical_value(dimension, origin, get) - D0
                    expected = (word >> address) & 1
                    check(actual == expected == logical_value(program, data), "isolated physical table")
                    local_counts[str(dimension)] += 1
                    before = dict(field)
                    position = shifted(origin, stage, address + 1)
                    field[position] = P0 + (1 - (field[position] - P0))
                    check(physical_value(dimension, origin, get) - D0 == 1 - expected,
                          "each program entry has a physical causal witness")
                    check([p for p in field if before[p] != field[p]] == [position],
                          "instruction witness edits exactly one symbol")
                    edit_counts[str(dimension)] += 1

            for slot, own, left, gate in itertools.product(range(8), (0, 1), (0, 1), (0, 1)):
                origin = (0,) * dimension
                owner = shifted(origin, stage, -(slot + 1))
                neighbor = shifted(origin, 0, -SCALE)
                field = {origin: P0 + own, owner: D0 + gate, neighbor: P0 + left}
                check(physical_value(dimension, origin, lambda p: field.get(p, B), True)
                      == P0 + (left if gate else own), "local autonomous payload copy")
                copy_cases += 1

        origin, valid = local_patch(guard(dimension), [0, 1, 0] + [0, 1] * (dimension - 1))
        for missing in valid:
            if missing == origin:
                continue
            field = dict(valid)
            field[missing] = B
            check(physical_value(dimension, origin, lambda p: field.get(p, B)) == valid[origin],
                  "missing data/program type retains D")
            malformed += 1
        owner = shifted(origin, 0, -1)
        other = shifted(origin, dimension - 1, -2)
        neighbor = shifted(origin, 0, -SCALE)
        for field in (
            {origin: P0, neighbor: P1},
            {origin: P0, owner: D1},
            {origin: P0, owner: D1, neighbor: D0},
            {origin: P0, owner: D1, other: D0, neighbor: P1},
            {origin: B, owner: D1, neighbor: P1},
            {origin: D0}, {origin: D1},
        ):
            check(physical_value(dimension, origin, lambda p: field.get(p, B), True) == field[origin],
                  "malformed owners, neighbor tags, data, or blank")
            malformed += 1

    # Full 2D local semantics, including syntactic aliases. The physical gates
    # above are exhaustive separately; this census uses independent integer LUTs.
    stencils = list(itertools.product((0, 1), repeat=5))
    tables, distinct = {}, set()
    second_interface = 0
    for leaf in range(256):
        for route in range(256):
            table = 0
            for q, data in enumerate(stencils):
                value = logical_value((leaf, route), data)
                table |= value << q
                check(logical_value((leaf, route, MUX), data + (0, 1)) == value,
                      "arbitrary two-word source survives the next lift")
                second_interface += 1
            tables[leaf, route] = table
            distinct.add(table)
    check(len(distinct) == 30496, "exact two-word behavioral census")
    for (leaf, route), table in tables.items():
        swapped = ((route & 15) << 4) | (route >> 4)
        check(tables[leaf ^ 255, swapped] == table, "complement/swap data-function alias")

    neutral, failures = [], []
    for word in range(256):
        witnesses = []
        for value in (0, 1):
            actual = (word >> (4 * value + 1)) & 1
            if actual != value:
                witnesses.append({"word": word, "inner_output": value,
                                  "actual": actual, "expected": value})
        predicted = not (word & 2) and bool(word & 32)
        check((not witnesses) == predicted, "neutral appended-table condition")
        if witnesses:
            failures.append(witnesses[0])
        else:
            neutral.append(word)
    check(len(neutral) == 64 and MUX in neutral, "canonical neutral routing table")

    first_interface, guard_checks = 0, 0
    for word in range(256):
        for data in itertools.product((0, 1), repeat=3):
            expected = logical_value((word,), data)
            for layer in range(-2, 3):
                value = data[1] if layer == 0 else int(layer < 0)
                inner = data if layer == 0 else (value,) * 3
                positive = data[1] if layer == -1 else int(layer + 1 < 0)
                negative = data[1] if layer == 1 else int(layer - 1 < 0)
                program = (word, MUX) if layer == 0 else guard(2)
                check(logical_value(program, inner + (positive, negative))
                      == (expected if layer == 0 else value), "first interface and guards")
                first_interface += 1
    for dimension in range(1, 5):
        for value in (0, 1):
            check(logical_value(guard(dimension), [value] * (2 * dimension + 1)) == value,
                  "uniform guard fixed point")
            guard_checks += 1
        for datum in (0, 1):
            for layer in (-2, -1, 1, 2):
                value = int(layer < 0)
                positive = datum if layer == -1 else int(layer + 1 < 0)
                negative = datum if layer == 1 else int(layer - 1 < 0)
                data = [value] * (2 * dimension + 1) + [positive, negative]
                check(logical_value(guard(dimension + 1), data) == value,
                      "guard boundary for every possible source datum")
                guard_checks += 1

    # Entry zero is invisible on the canonical (0,1) interface rails, but has
    # a witness on an arbitrary 2D field and survives as an inherited 3D edit.
    targeted = {"address": 0, "before": [], "after": [], "edited_positions": []}
    for dimension in (2, 3):
        program = (0, MUX) + (MUX,) * (dimension - 2)
        data = [0] * 5 + [0, 1] * (dimension - 2)
        origin, field = local_patch(program, data)
        get = lambda p: field.get(p, B)
        targeted["before"].append(physical_value(dimension, origin, get) - D0)
        edited = shifted(origin, 1, 1)
        field[edited] = P1
        targeted["after"].append(physical_value(dimension, origin, get) - D0)
        targeted["edited_positions"].append(list(edited))
    check(targeted["before"] == [0, 0] and targeted["after"] == [1, 1],
          "dormant new instruction becomes causal and then lifts")
    check(logical_value((0, MUX), [0, 0, 0, 0, 1])
          == logical_value((0, MUX ^ 1), [0, 0, 0, 0, 1]), "entry zero is dormant on rails")

    field_stats = {}
    for copy in (False, True):
        mode = "copy" if copy else "hold"
        field_stats[mode] = {}
        for name, cases, periods, ticks, dimensions in (
            ("one_dimensional_and_two_lifts", 8, (5,), 3, (2, 3)),
            ("arbitrary_two_dimensional_source", 16, (3, 3), 4, (3,)),
            ("arbitrary_three_dimensional_source", 8, (2, 3, 2), 3, (4,)),
        ):
            source_dimension = len(periods)
            totals = {"cases": cases, "target_timepoints": 0, "compared_symbols": 0,
                      "physical_payload_edits": 0,
                      "autonomous_source_word_changes_by_stage": [0] * source_dimension}
            for seed in range(1, cases + 1):
                source = random_source(seed, periods)
                source_field = PhysicalField.encode(source_dimension, periods, 0, lambda p: source[p], copy)
                targets = {d: PhysicalField.encode(d, periods, ticks + 2,
                           lifted_pair_at(source, source_dimension, d), copy) for d in dimensions}
                for tick in range(ticks):
                    position = tuple((tick + axis) % size for axis, size in enumerate(periods))
                    old_program, old_data = source[position]
                    bits = [(tick + 3 * axis) % 8 for axis in range(source_dimension)]
                    source[position] = (tuple(word ^ (1 << bits[axis])
                                              for axis, word in enumerate(old_program)), old_data ^ 1)
                    for field in [source_field, *targets.values()]:
                        where = position + (0,) * (field.dimension - source_dimension)
                        before = dict(field.symbols)
                        edits = {field.edit(where)}
                        edits.update(field.edit(where, axis, bit) for axis, bit in enumerate(bits))
                        changed = {p for p in before if before[p] != field.symbols[p]}
                        check(changed == edits and len(edits) == source_dimension + 1,
                              "matched physical edits of every inherited instruction stage")
                        totals["physical_payload_edits"] += len(edits)

                    old_source = source
                    source = logical_step(source, periods, copy)
                    for axis in range(source_dimension):
                        totals["autonomous_source_word_changes_by_stage"][axis] += sum(
                            old_source[p][0][axis] != source[p][0][axis] for p in source)
                    source_field = source_field.step()
                    expected = PhysicalField.encode(source_dimension, periods, 0, lambda p: source[p], copy)
                    check(source_field.symbols == expected.symbols, "complete physical source execution")
                    totals["compared_symbols"] += len(expected.symbols)
                    for dimension in dimensions:
                        targets[dimension] = targets[dimension].step()
                        actual = targets[dimension]
                        expected = PhysicalField.encode(dimension, periods, actual.radius,
                            lifted_pair_at(source, source_dimension, dimension), copy)
                        check(actual.symbols == expected.symbols, "complete lift including evolving routing words")
                        totals["target_timepoints"] += 1
                        totals["compared_symbols"] += len(expected.symbols)
            changes = totals["autonomous_source_word_changes_by_stage"]
            check(all(n > 0 for n in changes) if copy else all(n == 0 for n in changes),
                  "every routing stage actually changes autonomously in copy mode only")
            field_stats[mode][name] = totals

    return {
        "schema_version": 1,
        "protocol": "docs/research/protocols/editable-routing-tables-20260909.md",
        "protocol_freeze_commit": FREEZE,
        "assertions": assertions,
        "physical": {"alphabet": ["B", "D0", "D1", "P0", "P1"], "radius": 9,
                     "scale": 9, "tick_ratio": 1, "program_bits_by_dimension": [8, 16, 24, 32],
                     "occupied_sites_by_dimension": [9, 17, 25, 33],
                     "macrocell_sites_by_dimension": [9, 81, 729, 6561]},
        "isolated_physical_table_evaluations": local_counts,
        "physical_instruction_edit_witnesses": edit_counts,
        "two_dimensional_semantics": {"stored_programs": 65536, "data_stencils_each": 32,
                                     "distinct_data_functions": len(distinct), "alias_checks": len(tables)},
        "appended_table_contract": {"canonical": MUX, "neutral_words": neutral,
                                    "failed_words": len(failures), "failure_witnesses": failures},
        "interface_checks": {"first_all_layers": first_interface, "second_central": second_interface,
                             "uniform_and_boundary_guard_checks": guard_checks},
        "local_program_copy_cases": copy_cases,
        "malformed_layout_checks": malformed,
        "dormant_then_inherited_instruction_witness": targeted,
        "physical_fields": field_stats,
        "protocol_deviations": [],
        "implementation_corrections": [],
        "scope": "Editable table contents in a fixed axis-ordered chain, with hold/copy policies; prepared roles and guard backgrounds; no unrestricted editable syntax or novelty claim.",
    }


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
