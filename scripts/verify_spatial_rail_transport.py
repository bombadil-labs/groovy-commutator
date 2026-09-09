#!/usr/bin/env python3
"""Autonomous program transport in the frozen spatial Rail representation."""
from __future__ import annotations

import json
import verify_spatial_rail_programs as base


def physical_transport(dimension, position, get):
    center = get(position)
    if center not in (base.P0, base.P1):
        return base.physical_value(dimension, position, get)
    owners = [get(base.shifted(position, dimension - 1, -distance))
              for distance in range(1, 9)]
    data_owners = [symbol for symbol in owners if symbol in (base.D0, base.D1)]
    neighbor = get(base.shifted(position, 0, -base.SCALE))
    if len(data_owners) == 1 and data_owners[0] == base.D1 and neighbor in (base.P0, base.P1):
        return neighbor
    return center


class TransportField(base.PhysicalField):
    def step(self):
        radius = self.radius - 1 if len(self.periods) < self.dimension else self.radius
        output = {}
        for logical in base.coordinates(self.dimension, self.periods, radius):
            origin = tuple(base.SCALE * x for x in logical)
            for q in range(-1, 8):
                position = origin if q == -1 else base.shifted(origin, self.dimension - 1, q + 1)
                output[position] = physical_transport(self.dimension, position, self.get)
        return TransportField(self.dimension, self.periods, radius, output)


def logical_transport(source, dimension, periods):
    state_step = base.source_step(source, dimension, periods)
    result = {}
    for position, (own, data) in source.items():
        left = base.shifted(position, 0, -1)
        left = tuple(x % periods[a] for a, x in enumerate(left))
        program = source[left][0] if data else own
        result[position] = program, state_step[position][1]
    return result


def run_audit():
    assertions = 0
    def check(condition, message):
        nonlocal assertions
        assertions += 1
        if not condition:
            raise AssertionError(message)

    local_cases = 0
    malformed_cases = 0
    for dimension in (1, 2, 3):
        for slot in range(8):
            for own in (0, 1):
                for left in (0, 1):
                    for gate in (0, 1):
                        position = (0,) * dimension
                        owner = base.shifted(position, dimension - 1, -(slot + 1))
                        neighbor = base.shifted(position, 0, -base.SCALE)
                        field = {position: base.P0 + own, owner: base.D0 + gate,
                                 neighbor: base.P0 + left}
                        actual = physical_transport(dimension, position, lambda p: field.get(p, base.B))
                        check(actual == base.P0 + (left if gate else own), "local program transport")
                        local_cases += 1

        origin = (0,) * dimension
        owner = base.shifted(origin, dimension - 1, -1)
        other_owner = base.shifted(origin, dimension - 1, -2)
        neighbor = base.shifted(origin, 0, -base.SCALE)
        for field in (
            {origin: base.P0, neighbor: base.P1},
            {origin: base.P0, owner: base.D1},
            {origin: base.P0, owner: base.D1, other_owner: base.D0, neighbor: base.P1},
            {origin: base.B, owner: base.D1, neighbor: base.P1},
        ):
            check(physical_transport(dimension, origin, lambda p: field.get(p, base.B)) == field[origin],
                  "declared malformed/blank behavior")
            malformed_cases += 1

    def random_source(seed, dimension, periods):
        word = seed
        result = {}
        for position in base.coordinates(dimension, periods, 0):
            word = (1664525 * word + 1013904223) & 0xFFFFFFFF
            program = (word >> 16) & 255
            word = (1664525 * word + 1013904223) & 0xFFFFFFFF
            result[position] = program, (word >> 31) & 1
        return result

    stats = {}
    for name, cases, source_dimension, periods, ticks, target_dimensions in (
        ("heterogeneous_source_and_two_lifts", 16, 1, (5,), 4, (2, 3)),
        ("arbitrary_second_interface", 32, 2, (3, 3), 3, (3,)),
    ):
        totals = {"cases": cases, "timepoints": 0, "compared_symbols": 0,
                  "external_payload_edits": 0, "autonomous_source_program_changes": 0}
        for seed in range(1, cases + 1):
            source = random_source(seed, source_dimension, periods)
            source_field = TransportField.encode(source_dimension, periods, 0, lambda p: source[p])
            targets = {d: TransportField.encode(d, periods, ticks + 2,
                                                 base.lift_pair_at(source, source_dimension, d))
                       for d in target_dimensions}
            for tick in range(ticks):
                position = tuple((tick + axis) % periods[axis] for axis in range(source_dimension))
                address = tick % 8
                program, data = source[position]
                source[position] = program ^ (1 << address), data ^ 1
                for field in [source_field, *targets.values()]:
                    where = position + (0,) * (field.dimension - source_dimension)
                    before = dict(field.symbols)
                    edits = {field.edit(where), field.edit(where, address)}
                    changed = {p for p in before if before[p] != field.symbols[p]}
                    check(changed == edits and len(changed) == 2, "matched finite physical edits")
                    totals["external_payload_edits"] += 2

                old_source = source
                source = logical_transport(old_source, source_dimension, periods)
                totals["autonomous_source_program_changes"] += sum(
                    old_source[p][0] != source[p][0] for p in source
                )
                source_field = source_field.step()
                expected_source = TransportField.encode(source_dimension, periods, 0, lambda p: source[p])
                check(source_field.symbols == expected_source.symbols, "physical source word coherence")
                totals["compared_symbols"] += len(expected_source.symbols)
                for dimension in target_dimensions:
                    targets[dimension] = targets[dimension].step()
                    actual = targets[dimension]
                    expected = TransportField.encode(dimension, periods, actual.radius,
                        base.lift_pair_at(source, source_dimension, dimension))
                    check(actual.symbols == expected.symbols, "complete lift with autonomous program changes")
                    totals["compared_symbols"] += len(expected.symbols)
                    totals["timepoints"] += 1
        check(totals["autonomous_source_program_changes"] > 0, "program transport actually occurs")
        stats[name] = totals

    return {
        "schema_version": 1,
        "protocol": "docs/research/protocols/spatial-rail-transport-20260909.md",
        "protocol_freeze_commit": "7d2db9eef4e682e4926553138193852a8548c252",
        "assertions": assertions,
        "local_program_cases": local_cases,
        "malformed_layout_checks": malformed_cases,
        "guard": base.GUARD,
        "physical_radius": base.SCALE,
        "physical_fields": stats,
        "retained_data_audit": "results/spatial_rail_programs_20260909.json",
        "protocol_deviations": [],
        "scope": "Autonomous state-gated copying of complete spatial program words; no program synthesis or mutable wrapper syntax.",
    }


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
