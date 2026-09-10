#!/usr/bin/env python3
"""Frozen transverse-difference closure census; stdout is canonical JSON.

All 66 replication-compatible axial sources. Local words use bit x+3*y
for x=0..2,y=0..3 (physical coordinates x-1,y-1). Finite words use the
same addressing on a periodic 3-by-3 field. No source or correction state
is added to the proposed transverse observation.
"""
import hashlib
import itertools
import json

import verify_guard_free_axial_lift as axial

PROTOCOL_COMMIT = "869bc08f998b0b3afe47c878acdf6f2fc3869103"
RULES = [0, *range(128, 255, 2), 255]


def pack(values):
    return sum(int(value) << i for i, value in enumerate(values))


def reference_pack(values):
    return int(''.join('1' if value else '0' for value in values)[::-1], 2)


def local_reference(truth, field):
    lower = {(x, y): field[x, y] for y in range(3) for x in range(3)}
    upper = {(x, y): field[x, y+1] for y in range(3) for x in range(3)}
    a = axial.shrinking(truth, lower, 2, (0, 1))
    b = axial.shrinking(truth, upper, 2, (0, 1))
    observed = reference_pack(field[x, y] != field[x, y+1]
                              for y in range(3) for x in range(3))
    return observed, int(a != b), a, b


def finite_difference(field):
    return pack(field[x, y] ^ field[x, (y+1) % 3]
                for y in range(3) for x in range(3))


def reference_difference(field):
    return reference_pack(field[x, y] != field[x, (y+1) % 3]
                          for y in range(3) for x in range(3))


def audit():
    assert len(RULES) == 66
    affine = {sum((a*l ^ b*c ^ d*r ^ e) << (4*l+2*c+r)
                  for l, c, r in itertools.product(range(2), repeat=3))
              for a, b, d, e in itertools.product(range(2), repeat=4)}
    controls = sorted(affine.intersection(RULES))
    fields = []
    for word in range(4096):
        bits = format(word, '012b')[::-1]
        fields.append({(x, y): bits[x+3*y] == '1'
                       for y in range(4) for x in range(3)})
    local_hashes = [hashlib.sha256(), hashlib.sha256()]
    finite_hashes = [hashlib.sha256(), hashlib.sha256()]
    passing = {0: [], 1: []}
    finite_functional, full_obstructions = [], []
    records = []
    cap_cell_checks = 0
    for rule in RULES:
        truth = axial.boolean_truth(rule)
        g = [axial.composite(rule, axial.unpack(word, 9)) for word in range(512)]
        seen = [{}, {}]
        collisions = [None, None]
        mismatch_counts = [0, 0]
        for word in range(4096):
            observed = (word ^ (word >> 3)) & 511
            lower, upper = g[word & 511], g[word >> 3]
            target = lower ^ upper
            reference = local_reference(truth, fields[word])
            assert (observed, target, lower, upper) == reference
            for checksum, values in zip(local_hashes, ((observed, target, lower, upper), reference)):
                checksum.update(values[0].to_bytes(2, 'little')+bytes(values[1:]))
            if rule in affine:
                linear_rule = rule ^ (255 * axial.bit(rule, 0, 0, 0))
                assert target == axial.composite(linear_rule, axial.unpack(observed, 9))
            for radius, key in enumerate(((observed >> 4) & 1, observed)):
                if key not in seen[radius]:
                    seen[radius][key] = (target, word)
                elif seen[radius][key][0] != target:
                    mismatch_counts[radius] += 1
                    if collisions[radius] is None:
                        old_target, old_word = seen[radius][key]
                        collisions[radius] = {"observed_word": key,
                                              "source_words": [old_word, word],
                                              "next_transverse_bits": [old_target, target]}
        budgets = []
        for radius in (0, 1):
            patterns = 2 if radius == 0 else 512
            reachable = sorted(seen[radius])
            # Each column's four source bits realize every three-bit difference.
            assert reachable == list(range(patterns))
            table = None
            if collisions[radius] is None:
                passing[radius].append(rule)
                table = [seen[radius].get(key, (None, None))[0] for key in range(patterns)]
            budgets.append({"radius": radius, "passes": table is not None,
                            "reachable_neighborhoods": len(reachable),
                            "unreachable_neighborhoods": [key for key in range(patterns) if key not in seen[radius]],
                            "conflicts_against_first_representative": mismatch_counts[radius],
                            "first_conflict": collisions[radius], "cap_table": table})

        fibers = {}
        first_finite = None
        finite_conflicts = 0
        for word in range(512):
            field = {(x, y): (word >> (x+3*y)) & 1 for y in range(3) for x in range(3)}
            text = format(word, '09b')[::-1]
            ref_field = {(x, y): text[x+3*y] == '1' for y in range(3) for x in range(3)}
            after = axial.lattice_passes(rule, field, (3, 3))
            ref_after = {point: axial.local_tree(truth, ref_field, (3, 3), point, 2)
                         for point in ref_field}
            assert after == ref_after
            observed, target = finite_difference(field), finite_difference(after)
            ref_observed, ref_target = reference_difference(ref_field), reference_difference(ref_after)
            assert (observed, target) == (ref_observed, ref_target)
            actual_word = pack(after[x, y] for y in range(3) for x in range(3))
            reference_word = reference_pack(ref_after[x, y] for y in range(3) for x in range(3))
            for checksum, values in zip(finite_hashes, ((observed, target, actual_word),
                                                       (ref_observed, ref_target, reference_word))):
                checksum.update(b''.join(value.to_bytes(2, 'little') for value in values))
            if observed not in fibers:
                fibers[observed] = {"first_word": word, "first_target": target,
                                    "targets": set(), "size": 0}
            fiber = fibers[observed]
            fiber["targets"].add(target)
            fiber["size"] += 1
            if fiber["first_target"] != target:
                finite_conflicts += 1
                if first_finite is None:
                    difference = fiber["first_target"] ^ target
                    index = next(i for i in range(9) if (difference >> i) & 1)
                    first_finite = {"observed_full_word": observed,
                                    "source_words": [fiber["first_word"], word],
                                    "next_transverse_words": [fiber["first_target"], target],
                                    "first_differing_site": [index % 3, index // 3]}
            if observed == 0:
                assert target == 0
            if rule in affine:
                linear_rule = rule ^ (255 * axial.bit(rule, 0, 0, 0))
                delta_field = {(x, y): (observed >> (x+3*y)) & 1
                               for y in range(3) for x in range(3)}
                predicted = axial.lattice_passes(linear_rule, delta_field, (3, 3))
                assert target == pack(predicted[x, y] for y in range(3) for x in range(3))
            for budget in budgets:
                if not budget["passes"]:
                    continue
                table = budget["cap_table"]
                for y in range(3):
                    for x in range(3):
                        if budget["radius"] == 0:
                            key = (observed >> (x+3*y)) & 1
                        else:
                            key = pack((observed >> ((x+dx) % 3+3*((y+dy) % 3))) & 1
                                       for dy in (-1, 0, 1) for dx in (-1, 0, 1))
                        assert table[key] == ((target >> (x+3*y)) & 1)
                        cap_cell_checks += 1
        assert len(fibers) == 64
        assert {fiber["size"] for fiber in fibers.values()} == {8}
        if first_finite is None:
            finite_functional.append(rule)
        else:
            full_obstructions.append(rule)
        records.append({"rule": rule, "local_budgets": budgets,
                        "periodic": {"observed_fields": len(fibers), "fiber_size": 8,
                                     "conflicting_fibers": sum(len(fiber["targets"]) > 1 for fiber in fibers.values()),
                                     "conflicts_against_first_representative": finite_conflicts,
                                     "first_conflict": first_finite,
                                     "distinct_next_fields_per_fiber": [[key, len(fibers[key]["targets"])] for key in sorted(fibers)]}})
    assert set(controls) <= set(passing[1])
    assert {0, 204, 255} <= set(passing[0])
    assert set(passing[0]) <= set(passing[1]) <= set(finite_functional)
    assert all(a.digest() == b.digest() for a, b in (local_hashes, finite_hashes))
    return {"protocol_commit": PROTOCOL_COMMIT,
            "source_rules": RULES,
            "observation": "T(X)(x,y) = X(x,y) XOR X(x,y+1)",
            "local_word_convention": "bit x+3*y; x=0..2,y=0..3 represent physical x-1,y-1; observed word uses y=0..2",
            "finite_word_convention": "bit x+3*y on periodic x,y=0..2",
            "cap_table_convention": "entry p is output for observed neighborhood word p; radius zero uses center bit",
            "witness_convention": "ascending source words; first later source differing from first representative of its observation",
            "radius_zero_rules": passing[0], "radius_one_rules": passing[1],
            "finite_functional_rules": finite_functional,
            "full_field_obstruction_rules": full_obstructions,
            "selected_affine_controls": controls,
            "counts": {"source_rules": len(RULES), "local_source_windows": len(RULES)*4096,
                       "local_rule_budget_windows": len(RULES)*4096*2,
                       "periodic_macro_updates": len(RULES)*512,
                       "periodic_compared_output_cells": len(RULES)*512*9,
                       "passing_cap_cell_checks": cap_cell_checks,
                       "radius_zero_rules": len(passing[0]), "radius_one_rules": len(passing[1]),
                       "finite_functional_rules": len(finite_functional),
                       "full_field_obstruction_rules": len(full_obstructions)},
            "local_checksum_convention": "rules,source words ascending; observation uint16LE followed by next difference,lower G,upper G bytes",
            "local_primary_sha256": local_hashes[0].hexdigest(),
            "local_independent_sha256": local_hashes[1].hexdigest(),
            "finite_checksum_convention": "rules,source words ascending; observed T,next T,next X as uint16LE",
            "finite_primary_sha256": finite_hashes[0].hexdigest(),
            "finite_independent_sha256": finite_hashes[1].hexdigest(),
            "rules": records}


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2, sort_keys=True))
