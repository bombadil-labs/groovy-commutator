#!/usr/bin/env python3
"""Frozen finite-boundary audit using the UNCHANGED editable-routing CA."""
from __future__ import annotations

import itertools
import json

import verify_editable_routing_tables as base

FREEZE = "c7072fb1143d1b545f21a89fd47cb3ddc858846d"


def wrapped(position, periods):
    return tuple(x % periods[a] if a < len(periods) else x
                 for a, x in enumerate(position))


def logical_step(source, dimension, periods, copy=False):
    """Absent sites are not zero data. A dictionary carries the fixed mask."""
    output = {}
    for position, (program, value) in source.items():
        neighbors = [wrapped(base.shifted(position, axis, sign), periods)
                     for axis in range(dimension) for sign in (-1, 1)]
        if all(p in source for p in neighbors):
            data = [source[neighbors[0]][1], value, source[neighbors[1]][1]]
            for axis in range(1, dimension):
                data.extend((source[neighbors[2 * axis + 1]][1],
                             source[neighbors[2 * axis]][1]))
            new_value = base.logical_value(program, data)
        else:
            new_value = value
        left = neighbors[0]
        inherited = source[left][0] if copy and value and left in source else program
        output[position] = inherited, new_value
    return output


def lift(source, dimension, layers=(-1, 0, 1)):
    output = {}
    for position, (program, value) in source.items():
        for layer in layers:
            output[position + (layer,)] = ((program + (base.MUX,), value) if layer == 0
                                         else (base.guard(dimension + 1), int(layer < 0)))
    return output


def repeated_lift(source, dimension, target):
    output = source
    for d in range(dimension, target):
        output = lift(output, d)
    return output


class MaskedField:
    """All stored sites are nonblank. The fixed CA cannot create a site from B."""
    def __init__(self, dimension, periods, symbols, copy):
        self.dimension, self.periods, self.symbols, self.copy = dimension, periods, symbols, copy

    @classmethod
    def encode(cls, source, dimension, periods=(), copy=False):
        symbols = {}
        for position, (program, value) in source.items():
            if len(program) != dimension:
                raise ValueError("wrong program depth")
            origin = tuple(base.SCALE * x for x in position)
            symbols[origin] = base.D0 + value
            for axis, word in enumerate(program):
                for bit in range(8):
                    symbols[base.shifted(origin, axis, bit + 1)] = base.P0 + ((word >> bit) & 1)
        return cls(dimension, tuple(periods), symbols, copy)

    def get(self, position):
        return self.symbols.get(wrapped(position, tuple(base.SCALE * p for p in self.periods)), base.B)

    def step(self):
        # No clamp, shrinking halo, cropped guards or idealized boundary rule.
        symbols = {p: base.physical_value(self.dimension, p, self.get, self.copy)
                   for p in self.symbols}
        return MaskedField(self.dimension, self.periods, symbols, self.copy)

    def decode(self):
        output = {}
        for origin, symbol in self.symbols.items():
            if symbol not in (base.D0, base.D1):
                continue
            if any(x % base.SCALE for x in origin):
                raise ValueError("noncanonical datum position")
            position = tuple(x // base.SCALE for x in origin)
            program = []
            for axis in range(self.dimension):
                word = 0
                for bit in range(8):
                    payload = self.get(base.shifted(origin, axis, bit + 1))
                    if payload not in (base.P0, base.P1):
                        raise ValueError("incomplete native program")
                    word |= (payload - base.P0) << bit
                program.append(word)
            output[position] = tuple(program), symbol - base.D0
        return output

    def edit(self, position, axis=None, bit=None):
        physical = tuple(base.SCALE * x for x in position)
        offset = base.D0
        if axis is not None:
            physical = base.shifted(physical, axis, bit + 1)
            offset = base.P0
        self.symbols[physical] = offset + (1 - (self.symbols[physical] - offset))
        return physical


def random_source(seed, positions, dimension):
    state, source = seed, {}
    for position in sorted(positions):
        program = []
        for _ in range(dimension):
            state = (1664525 * state + 1013904223) & 0xFFFFFFFF
            program.append((state >> 16) & 255)
        state = (1664525 * state + 1013904223) & 0xFFFFFFFF
        source[position] = tuple(program), (state >> 31) & 1
    return source


def run_audit():
    assertions = 0

    def check(condition, message):
        nonlocal assertions
        assertions += 1
        if not condition:
            raise AssertionError(message)

    local_cases = 0
    for word, value, left, right in itertools.product(range(256), (0, 1), (None, 0, 1), (None, 0, 1)):
        source = {(0,): ((word,), value)}
        for position, datum in ((-1, left), (1, right)):
            if datum is not None:
                source[position,] = ((base.IDENTITY,), datum)
        physical = MaskedField.encode(source, 1)
        expected = logical_step(source, 1, ())[(0,)][1]
        check(base.physical_value(1, (0,), physical.get) == base.D0 + expected,
              "masked source datum update")
        target = MaskedField.encode(lift(source, 1), 2)
        for layer in (-1, 0, 1):
            actual = base.physical_value(2, (0, base.SCALE * layer), target.get)
            check(actual == base.D0 + (expected if layer == 0 else int(layer < 0)),
                  "finite central interface and frozen guards")
        local_cases += 1

    completion_failures, passing_words = [], []
    for word in range(256):
        passes = True
        for value in (0, 1):
            source = MaskedField.encode({(0,): ((word,), value)}, 1)
            source_after = base.physical_value(1, (0,), source.get) - base.D0
            origin, patch = base.local_patch((word, base.MUX), [0, value, 0, 0, 1])
            actual = base.physical_value(2, origin, lambda p: patch.get(p, base.B)) - base.D0
            check(source_after == value and actual == ((word >> (2 * value)) & 1),
                  "missing-as-zero control has its declared local semantics")
            if actual != source_after:
                completion_failures.append({"word": word, "datum": value,
                                            "expected": source_after, "actual": actual})
                passes = False
        check(passes == (not (word & 1) and bool(word & 4)), "zero-completion passing-word condition")
        if passes:
            passing_words.append(word)
    check(len(completion_failures) == 256 and len(passing_words) == 64, "retained zero-completion failures")
    origin, patch = base.local_patch((255, base.MUX), [0, 0, 0, 0, 1])
    check(base.physical_value(2, origin, lambda p: patch.get(p, base.B), True) == base.D1,
          "word255 zero-datum witness also fails in copy mode")

    thin_results = []
    source = {(x,): ((255,), 0) for x in range(3)}
    check(logical_step(source, 1, (3,))[(0,)][1] == 1, "changing source for thickness control")
    for layers in ((0,), (-1, 0), (0, 1), (-1, 0, 1)):
        field = MaskedField.encode(lift(source, 1, layers), 2, (3,))
        value = base.physical_value(2, (0, 0), field.get) - base.D0
        expected = int(len(layers) == 3)
        check(value == expected, "both transverse data neighbors are required")
        thin_results.append({"layers": list(layers), "source_next": 1,
                             "target_next": value, "intertwines_this_witness": value == 1})

    copy_cases = 0
    for dimension in range(1, 5):
        origin = (0,) * dimension
        for stage, bit, present, gate, own, left in itertools.product(
                range(dimension), range(8), (False, True), (0, 1), (0, 1), (0, 1)):
            owner = base.shifted(origin, stage, -(bit + 1))
            neighbor = base.shifted(origin, 0, -base.SCALE)
            patch = {origin: base.P0 + own, owner: base.D0 + gate}
            if present:
                patch[neighbor] = base.P0 + left
            actual = base.physical_value(dimension, origin, lambda p: patch.get(p, base.B), True)
            check(actual == base.P0 + (left if present and gate else own), "presence-sensitive program copy")
            copy_cases += 1
        patch = {base.shifted(origin, axis, 1): base.D1 if axis % 2 else base.P1
                 for axis in range(dimension)}
        for copy in (False, True):
            check(base.physical_value(dimension, origin, lambda p: patch.get(p, base.B), copy) == base.B,
                  "blank exterior is absorbing")

    full2 = list(itertools.product(range(3), repeat=2))
    full3 = list(itertools.product(range(2), range(3), range(2)))
    families = (
        ("full_1d", 1, (5,), [(x,) for x in range(5)], (2, 3, 4)),
        ("holed_1d", 1, (5,), [(x,) for x in (0, 1, 3)], (2, 3)),
        ("full_2d", 2, (3, 3), full2, (3, 4)),
        ("holed_2d", 2, (3, 3), [p for p in full2 if p not in ((0, 0), (1, 2))], (3, 4)),
        ("holed_3d", 3, (2, 3, 2), [p for p in full3 if p not in ((0, 0, 0), (1, 2, 1))], (4,)),
        ("finite_nonperiodic_1d", 1, (), [(x,) for x in (0, 1, 2, 4)], (2, 3)),
    )
    statistics = {}

    def compare(field, expected, initial_support):
        encoded = MaskedField.encode(expected, field.dimension, field.periods, field.copy)
        check(field.symbols == encoded.symbols, "entire physical field including guards and implied B")
        check(set(field.symbols) == initial_support, "no occupied support changes")
        check(field.decode() == expected, "occupancy-aware block-local decoding")
        check(len(field.symbols) == len(expected) * (8 * field.dimension + 1), "exact occupied-site budget")
        return len(encoded.symbols)

    for copy in (False, True):
        mode = "copy" if copy else "hold"
        statistics[mode] = {}
        for name, dimension, periods, positions, targets in families:
            totals = {"cases": 8, "ticks_each": 4, "target_timepoints": 0, "compared_symbols": 0,
                      "physical_payload_edits": 0, "autonomous_data_changes": 0,
                      "autonomous_program_word_changes": [0] * dimension}
            for seed in range(1, 9):
                source = random_source(seed, positions, dimension)
                fields = {d: MaskedField.encode(repeated_lift(source, dimension, d), d, periods, copy)
                          for d in (dimension, *targets)}
                supports = {d: set(field.symbols) for d, field in fields.items()}
                for d, field in fields.items():
                    check(len(field.decode()) == len(source) * 3 ** (d - dimension), "threefold mask growth")
                for tick in range(4):
                    position = sorted(source)[tick % len(source)]
                    program, value = source[position]
                    bits = [(tick + 3 * axis) % 8 for axis in range(dimension)]
                    source[position] = (tuple(word ^ (1 << bits[axis])
                                              for axis, word in enumerate(program)), value ^ 1)
                    for d, field in fields.items():
                        where = position + (0,) * (d - dimension)
                        before = dict(field.symbols)
                        edits = {field.edit(where)}
                        edits.update(field.edit(where, axis, bit) for axis, bit in enumerate(bits))
                        check({p for p in before if before[p] != field.symbols[p]} == edits
                              and len(edits) == dimension + 1, "single-symbol inherited edits")
                        totals["physical_payload_edits"] += len(edits)
                    old = source
                    source = logical_step(source, dimension, periods, copy)
                    totals["autonomous_data_changes"] += sum(source[p][1] != old[p][1] for p in source)
                    for axis in range(dimension):
                        totals["autonomous_program_word_changes"][axis] += sum(
                            source[p][0][axis] != old[p][0][axis] for p in source)
                    for d in fields:
                        fields[d] = fields[d].step()
                        expected = repeated_lift(source, dimension, d)
                        totals["compared_symbols"] += compare(fields[d], expected, supports[d])
                        totals["target_timepoints"] += int(d != dimension)
            changes = totals["autonomous_program_word_changes"]
            check(all(n > 0 for n in changes) if copy else all(n == 0 for n in changes),
                  "program transport actually occurs at every source stage only in copy mode")
            statistics[mode][name] = totals

    edited_guard = {}
    for copy in (False, True):
        source = lift(random_source(1, [(x,) for x in range(5)], 1), 1)
        program, value = source[0, 1]
        source[0, 1] = ((program[0], program[1] ^ 1), value ^ 1)
        fields = {d: MaskedField.encode(repeated_lift(source, 2, d), d, (5,), copy) for d in (2, 3)}
        supports = {d: set(f.symbols) for d, f in fields.items()}
        count = 0
        for _ in range(4):
            source = logical_step(source, 2, (5,), copy)
            for d in fields:
                fields[d] = fields[d].step()
                count += compare(fields[d], repeated_lift(source, 2, d), supports[d])
        edited_guard["copy" if copy else "hold"] = {"ticks": 4, "compared_symbols": count,
                                                      "edited_source_position": [0, 1]}

    return {
        "schema_version": 1, "protocol": "docs/research/protocols/finite-routing-boundaries-20260910.md",
        "protocol_freeze_commit": FREEZE, "assertions": assertions,
        "unchanged_interpreter": "scripts/verify_editable_routing_tables.py",
        "local_mask_and_guard_cases": local_cases, "local_presence_sensitive_copy_cases": copy_cases,
        "missing_as_zero_control": {"cases": 512, "failed_data_cases": len(completion_failures),
                                    "words_passing_both_data_values": passing_words,
                                    "failure_witnesses": completion_failures},
        "insufficient_thickness_control": thin_results,
        "physical_fields": statistics, "edited_guard_then_lifted": edited_guard,
        "physical_budget": {"alphabet_size": 5, "radius": 9, "tick_ratio": 1,
                            "logical_layers_per_added_axis": 3, "physical_band_width": 27,
                            "occupied_sites_per_original_1d_site_after_0_to_3_lifts": [9, 51, 225, 891],
                            "exterior": "absorbing B; finite transverse support, not necessarily finite total support"},
        "protocol_deviations": [], "implementation_corrections": [],
        "scope": "Fixed occupancy masks and complete macrocells; missing-input guard freezing; inherited payload edits only. No occupancy edits, self-assembly, or commutator-closure result.",
    }


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
