#!/usr/bin/env python3
"""Exact frozen census of ordered axial ECA composition, without guard rows.

Standard library only. Run from the repository root; stdout is canonical JSON.
Words put bit x+3*y+9*z at coordinate (x,y,z) in a local causal block.
Axis 0 acts first. ECA truth indices remain 4*left+2*center+right.
"""
import hashlib
import itertools
import json

PROTOCOL_COMMIT = "c5c380ecd80e53ff7ac1e8c64edcd267a8d61cd4"


def bit(rule, left, center, right):
    return (rule >> (4*left+2*center+right)) & 1


def composite(rule, values):
    """Primary integer pipeline: collapse contiguous triples, axis 0 first."""
    while len(values) > 1:
        values = [bit(rule, *values[i:i+3]) for i in range(0, len(values), 3)]
    return values[0]


def unpack(word, size):
    return [(word >> i) & 1 for i in range(size)]


def boolean_truth(rule):
    # String parsing and tuple selection avoid the primary integer indices.
    return {tuple(c == '1' for c in format(index, '03b')): value == '1'
            for index, value in enumerate(format(rule, '08b')[::-1])}


def shrinking(truth, field, dimension, order):
    """Independent array contraction, retaining named coordinates."""
    extents = [range(3) for _ in range(dimension)]
    for axis in order:
        extents[axis] = (1,)
        after = {}
        for point in itertools.product(*extents):
            neighbors = []
            for coordinate in range(3):
                neighbor = list(point)
                neighbor[axis] = coordinate
                neighbors.append(field[tuple(neighbor)])
            after[point] = truth[tuple(neighbors)]
        field = after
    return int(field[(1,)*dimension])


def patch(word, dimension):
    # Binary strings, coordinate dictionary: separate from unpack/composite.
    text = format(word, f'0{3**dimension}b')[::-1]
    return {point: text[sum(x*3**i for i, x in enumerate(point))] == '1'
            for point in itertools.product(range(3), repeat=dimension)}


def lattice_passes(rule, field, shape):
    for axis in range(len(shape)):
        after = {}
        for point in field:
            neighbors = []
            for delta in (-1, 0, 1):
                neighbor = list(point)
                neighbor[axis] = (neighbor[axis]+delta) % shape[axis]
                neighbors.append(field[tuple(neighbor)])
            after[point] = bit(rule, *neighbors)
        field = after
    return field


def local_tree(truth, field, shape, point, stage):
    """Independent direct local composite, with periodic source reads only."""
    if stage == 0:
        return bool(field[tuple(x % size for x, size in zip(point, shape))])
    neighbors = []
    axis = stage-1
    for delta in (-1, 0, 1):
        neighbor = list(point)
        neighbor[axis] += delta
        neighbors.append(local_tree(truth, field, shape, tuple(neighbor), stage-1))
    return truth[tuple(neighbors)]


def witness(word, expected, actual):
    return {"source_word": word, "expected": expected, "actual": actual}


def audit():
    first, second, commuting, both = [], [], [], []
    records = []
    primary_hash, independent_hash = hashlib.sha256(), hashlib.sha256()
    affine = sorted({sum((a*l ^ b*c ^ d*r ^ e) << (4*l+2*c+r)
                         for l, c, r in itertools.product(range(2), repeat=3))
                     for a, b, d, e in itertools.product(range(2), repeat=4)})
    assert len(affine) == 16
    patches2 = [patch(word, 2) for word in range(512)]
    patches3 = [{(x, y, z): field[x, y] for x, y, z in
                 itertools.product(range(3), repeat=3)} for field in patches2]
    triples = [patch(word, 1) for word in range(8)]
    replicated = [{(x, y): field[x,] for x, y in itertools.product(range(3), repeat=2)}
                  for field in triples]
    for rule in range(256):
        truth = boolean_truth(rule)
        first_bad, second_bad, axis_bad = None, None, None
        first_count = second_count = axis_count = 0
        disagreement = 0
        for word in range(8):
            expected = composite(rule, unpack(word, 3))
            actual = bit(rule, expected, expected, expected)
            reference = shrinking(truth, triples[word], 1, (0,))
            lifted = shrinking(truth, replicated[word], 2, (0, 1))
            assert (expected, actual) == (reference, lifted)
            primary_hash.update(bytes((expected, actual)))
            independent_hash.update(bytes((reference, lifted)))
            if actual != expected:
                first_count += 1
                if first_bad is None:
                    first_bad = witness(word, expected, actual)
        for word in range(512):
            values = unpack(word, 9)
            xy = composite(rule, values)
            yx = composite(rule, [values[x+3*y] for x in range(3) for y in range(3)])
            lifted = bit(rule, xy, xy, xy)
            ref_xy = shrinking(truth, patches2[word], 2, (0, 1))
            ref_yx = shrinking(truth, patches2[word], 2, (1, 0))
            ref_lift = shrinking(truth, patches3[word], 3, (0, 1, 2))
            assert (xy, yx, lifted) == (ref_xy, ref_yx, ref_lift)
            primary_hash.update(bytes((xy, yx, lifted)))
            independent_hash.update(bytes((ref_xy, ref_yx, ref_lift)))
            if lifted != xy:
                second_count += 1
                if second_bad is None:
                    second_bad = witness(word, xy, lifted)
            if xy != yx:
                axis_count += 1
                disagreement |= 1 << word
                if axis_bad is None:
                    axis_bad = {"source_word": word, "axis_0_then_1": xy,
                                "axis_1_then_0": yx}
            if rule in (0, 255, 204):
                assert xy == (values[4] if rule == 204 else rule//255)
        if first_bad is None:
            first.append(rule)
        if second_bad is None:
            second.append(rule)
        if axis_bad is None:
            commuting.append(rule)
        if first_bad is None and axis_bad is None:
            both.append(rule)
        records.append({"rule": rule, "first_interface_disagreements": first_count,
                        "second_interface_disagreements": second_count,
                        "axis_order_disagreements": axis_count,
                        "first_interface_witness": first_bad,
                        "second_interface_witness": second_bad,
                        "axis_order_witness": axis_bad,
                        "axis_order_disagreement_hex": format(disagreement, '0128x')})
    criterion = [rule for rule in range(256)
                 if rule in (0, 255) or (bit(rule, 0, 0, 0) == 0 and bit(rule, 1, 1, 1) == 1)]
    assert first == second == criterion
    assert set(affine) <= set(commuting)
    assert {0, 255, 204} <= set(both)
    assert primary_hash.digest() == independent_hash.digest()

    finite = []
    for shape in ((4,), (2, 2), (2, 2, 2)):
        # Finite words use bit i for coordinate points[i] (lexicographic).
        points = list(itertools.product(*(range(size) for size in shape)))
        size = len(points)
        checksums = [hashlib.sha256(), hashlib.sha256()]
        cases = cells = 0
        for rule in range(256):
            truth = boolean_truth(rule)
            for word in range(1 << size):
                field = {point: (word >> i) & 1 for i, point in enumerate(points)}
                actual = lattice_passes(rule, field, shape)
                reference = {point: int(local_tree(truth, field, shape, point, len(shape)))
                             for point in points}
                assert actual == reference
                if rule in (0, 255, 204):
                    assert actual == (field if rule == 204 else
                                      {point: rule//255 for point in points})
                for checksum, output in zip(checksums, (actual, reference)):
                    packed = sum(output[point] << i for i, point in enumerate(points))
                    checksum.update(packed.to_bytes((size+7)//8, 'little'))
                cases += 1
                cells += size
        assert checksums[0].digest() == checksums[1].digest()
        finite.append({"shape": list(shape), "source_states_per_rule": 1 << size,
                       "macro_updates": cases, "compared_cells": cells,
                       "ordered_passes_sha256": checksums[0].hexdigest(),
                       "direct_local_tree_sha256": checksums[1].hexdigest()})

    return {
        "protocol_commit": PROTOCOL_COMMIT,
        "constructor": "G_r,d = F_r,d composed with ... composed with F_r,1",
        "embedding": "R_d copies the field unchanged along the new last axis",
        "local_word_convention": "bit x+3*y+9*z is site (x,y,z), x fastest; axis 0 first",
        "disagreement_convention": "hex integer bit p is axis-order disagreement at patch word p",
        "checksum_convention": "rules ascending; first triples: expected,actual bytes; then 2D patches: xy,yx,lifted bytes",
        "first_interface_rules": first,
        "second_interface_rules": second,
        "all_interfaces_rules": criterion,
        "axis_permutation_equivariant_rules": commuting,
        "compatible_and_axis_permutation_equivariant_rules": both,
        "affine_commutation_controls": affine,
        "counts": {"first_interface_rules": len(first), "second_interface_rules": len(second),
                   "all_interfaces_rules": len(criterion), "axis_permutation_rules": len(commuting),
                   "both_rules": len(both), "first_interface_patches": 256*8,
                   "second_interface_patches": 256*512, "axis_order_patches": 256*512},
        "local_primary_sha256": primary_hash.hexdigest(),
        "local_independent_sha256": independent_hash.hexdigest(),
        "finite_word_convention": "bit i corresponds to lexicographic coordinate points[i]",
        "finite_checksum_convention": "rules then source words ascending; packed output little endian",
        "finite_controls": finite,
        "processing": {"lattice_passes_per_macro_update": "d",
                       "naive_single_output_lookups": "(3**d-1)/2",
                       "source_block_sites": "3**d", "alphabet_size": 2, "Moore_radius_bound": 1},
        "rules": records,
    }


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2, sort_keys=True))
