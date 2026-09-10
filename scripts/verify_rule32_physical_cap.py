#!/usr/bin/env python3
"""Frozen Rule32 physical-cap audit. No changes to the ambient interpreter."""
import itertools
import json

import verify_editable_routing_tables as base
import verify_finite_routing_boundaries as finite

FREEZE = "f65a63ea5a96824cbed850043b286ad0e5b7c3be"
PROGRAMS = {-1: (204, 240), 0: (32, 60), 1: (128, 240), 2: (204, 240)}


def evolve(state, width):
    # Rule32 is L AND NOT C AND R, independent of physical table execution.
    return sum((((state >> ((x-1) % width)) & 1)
                & (1-((state >> x) & 1))
                & ((state >> ((x+1) % width)) & 1)) << x for x in range(width))


def prepare(state, width):
    next_state = evolve(state, width)
    u = state ^ next_state
    v = next_state ^ evolve(next_state, width) ^ evolve(u, width)
    return {(x, y): (PROGRAMS[y], ((u if y == 0 else v if y == 1 else 0) >> x) & 1)
            for x in range(width) for y in range(-1, 3)}


def native_step(field, width):
    # This reference uses raw integer LUTs, never base.logical_value/step.
    out = {}
    for (x, y), (program, center) in field.items():
        if y in (-1, 2):
            out[x, y] = program, center
            continue
        left, right = field[(x-1) % width, y][1], field[(x+1) % width, y][1]
        b = (program[0] >> (4*left+2*center+right)) & 1
        above, below = field[x, y+1][1], field[x, y-1][1]
        out[x, y] = program, (program[1] >> (4*b+2*above+below)) & 1
    return out


def reference_symbols(field):
    # Independently reconstruct the prepared five-symbol layout.
    out = {}
    for (x, y), (program, value) in field.items():
        out[9*x, 9*y] = 1+value
        for q in range(8):
            out[9*x+q+1, 9*y] = 3+((program[0] >> q) & 1)
            out[9*x, 9*y+q+1] = 3+((program[1] >> q) & 1)
    return out


def active_pair(field, width):
    return tuple(sum(field[x, y][1] << x for x in range(width)) for y in (0, 1))


def local_semantics():
    def f(row):
        return tuple(l & (1-c) & r for l, c, r in zip(row, row[1:], row[2:]))

    def a(j, row):
        if j == 0:
            return row[1] ^ f(row)[0]
        return a(j-1, f(row)) ^ f(tuple(a(j-1, row[i:i+len(row)-2]) for i in range(3)))[0]

    count = 0
    for row in itertools.product((0, 1), repeat=7):
        u = tuple(a(0, row[i:i+3]) for i in range(2, 5))
        v = tuple(a(1, row[i:i+5]) for i in range(3))
        assert f(u)[0] ^ v[1] == a(0, f(row)[1:4])
        assert (v[0] & v[1] & v[2]) == a(1, f(row))
        assert a(2, row) == (v[0] & v[2])
        count += 3
    return count


def audit():
    counts = {"semantic_identity_assertions": local_semantics(),
              "physical_local_cases": 0, "local_program_symbols": 0,
              "local_guard_cases": 0, "field_timepoints": 0,
              "occupied_symbol_comparisons": 0, "blank_symbol_comparisons": 0}
    for program in (PROGRAMS[0], PROGRAMS[1]):
        for data in itertools.product((0, 1), repeat=5):
            origin, symbols = base.local_patch(program, data)
            get = lambda p: symbols.get(p, base.B)
            left, center, right, above, below = data
            expected = (left & (1-center) & right) ^ above if program[0] == 32 else left & center & right
            assert base.physical_value(2, origin, get) == base.D0+expected
            for p, value in symbols.items():
                if value in (base.P0, base.P1):
                    assert base.physical_value(2, p, get) == value
                    counts["local_program_symbols"] += 1
            assert base.physical_value(2, (1, 1), get) == base.B
            counts["physical_local_cases"] += 1
    for data in itertools.product((0, 1), repeat=5):
        for sign in (-1, 1):
            origin, symbols = base.local_patch((204, 240), data)
            del symbols[0, 9*sign]
            assert base.physical_value(2, origin, lambda p: symbols.get(p, base.B)) == base.D0+data[1]
            counts["local_guard_cases"] += 1

    blank_positions = {}
    for width in (3, 5):
        occupied = reference_symbols(prepare(0, width))
        # One horizontal period and a macrocell halo on both vertical sides.
        blank_positions[width] = [p for p in itertools.product(range(9*width), range(-18, 36))
                                  if p not in occupied]

    def compare(physical, native, width):
        expected = reference_symbols(native)
        assert physical.symbols == expected  # Includes all guards and programs.
        assert len(physical.symbols) == 68*width
        assert all(physical.symbols.get(p, base.B) == base.B for p in blank_positions[width])
        # All other infinitely many omitted sites are B and B is absorbing.
        assert base.physical_value(2, (0, 1000), physical.get) == base.B
        counts["field_timepoints"] += 1
        counts["occupied_symbol_comparisons"] += len(expected)
        counts["blank_symbol_comparisons"] += len(blank_positions[width])+1

    baselines, zero_witness, zero_mismatches = [], None, 0
    edit_records = []
    edits = [(y, axis, bit) for y in (0, 1) for axis in (0, 1) for bit in range(8)]
    edits += [(y, None, None) for y in (0, 1)]
    for width in (3, 5):
        image = {active_pair(prepare(s, width), width) for s in range(1 << width)}
        for initial in range(1 << width):
            state, native = initial, prepare(initial, width)
            physical = finite.MaskedField.encode(native, 2, (width,))
            baseline = []
            for tick in range(41):
                compare(physical, native, width)
                assert native == prepare(state, width)
                baseline.append(active_pair(native, width))
                if tick < 40:
                    state = evolve(state, width)
                    native, physical = native_step(native, width), physical.step()
            baselines.append({"width": width, "initial": initial, "active_pairs": baseline})

            zero = prepare(initial, width)
            for x in range(width):
                zero[x, 1] = (32, 240), zero[x, 1][1]
            zero_physical = finite.MaskedField.encode(zero, 2, (width,))
            for tick in range(41):
                compare(zero_physical, zero, width)
                pair = active_pair(zero, width)
                if pair != baseline[tick]:
                    zero_mismatches += 1
                    if zero_witness is None:
                        zero_witness = {"width": width, "initial": initial, "tick": tick,
                                        "actual_pair": pair, "expected_pair": baseline[tick]}
                if tick < 40:
                    zero, zero_physical = native_step(zero, width), zero_physical.step()

            for y, axis, bit in edits:
                pristine = prepare(initial, width)
                native = dict(pristine)
                physical = finite.MaskedField.encode(native, 2, (width,))
                before = dict(physical.symbols)
                edited_position = physical.edit((0, y), axis, bit)
                program, value = native[0, y]
                if axis is None:
                    native[0, y] = program, value ^ 1
                else:
                    new_program = list(program)
                    new_program[axis] ^= 1 << bit
                    native[0, y] = tuple(new_program), value
                assert [p for p in before if before[p] != physical.symbols[p]] == [edited_position]
                same, member, program_same, pairs = [], [], [], []
                for tick in range(9):
                    compare(physical, native, width)
                    pair = active_pair(native, width)
                    same.append(pair == baseline[tick])
                    member.append(pair in image)
                    program_same.append(all(native[p][0] == pristine[p][0] for p in native))
                    pairs.append(pair)
                    assert program_same[-1] == (axis is None)
                    if tick < 8:
                        native, physical = native_step(native, width), physical.step()
                edit_records.append({"width": width, "initial": initial, "row": y,
                                     "stage": axis, "bit": bit,
                                     "kind": "data" if axis is None else "program",
                                     "same_undamaged_data": same, "in_ring_image": member,
                                     "same_program": program_same, "active_pairs": pairs})
    summary = []
    for width in (3, 5):
        for kind in ("program", "data"):
            records = [r for r in edit_records if r["width"] == width and r["kind"] == kind]
            summary.append({"width": width, "kind": kind, "cases": len(records),
                            **{key: [sum(r[key][t] for r in records) for t in range(9)]
                               for key in ("same_undamaged_data", "in_ring_image", "same_program")},
                            "ever_data_departure": sum(not all(r["same_undamaged_data"]) for r in records),
                            "ever_image_departure": sum(not all(r["in_ring_image"]) for r in records)})
    assert len(edit_records) == 1360 and len(baselines) == 40
    return {"schema": 1, "protocol": "rule32-physical-cap-20260910",
            "protocol_freeze_commit": FREEZE,
            "protocol_deviations": [], "implementation_corrections": [],
            "counts": counts, "unmodified_cases": 40, "ticks_unmodified": 40,
            "zero_cap": {"cases": 40, "ticks": 40, "mismatched_timepoints": zero_mismatches,
                         "first_witness": zero_witness},
            "edit_cases": len(edit_records), "ticks_edited": 8, "edit_summary": summary,
            "resources": {"alphabet": 5, "physical_radius": 9, "scale": 9,
                          "ticks_per_source_tick": 1, "logical_rows_with_guards": 4,
                          "occupied_symbols_per_source_site": 68,
                          "program_symbols_per_source_site": 64,
                          "data_symbols_per_source_site": 4,
                          "transverse_span": 36, "preparation_source_radius_bound": 2},
            "packing": "ring bit x has weight 2**x; active pairs are [U,V]",
            "scope": "Local proof gives all-time full-shift closure; edit/repair statistics are finite-ring controls only.",
            "baselines": baselines, "edit_records": edit_records}


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
