#!/usr/bin/env python3
"""Source-only implementation chunk for the frozen dimensional-response protocol.

This module intentionally performs *no physical evolution* and computes no
V/M/S/R response value.  It pins the pre-evaluation combinatorics approved in
Gate 1 for PR #173:

* exhaustive ordered nonliteral pairs on logical rings 6 and 7;
* the six-component matched-control descriptor;
* nonliteral dihedral homology and shift/reflection/both tags;
* exact joint-shift-orbit partitions in every scored class;
* the orbit-preserving deterministic placebo assignments from clarification B1.

The physical-response verifier must import or reproduce these objects only after
this source-only stage is green and integrated.  Running ``--self-test`` is safe
before evaluation because it inspects source bits and labels only.

Gate-1 stack:
  dimensional-resonance-response-20260912.md
  dimensional-resonance-response-gate1-refreeze-20260912.md
  dimensional-resonance-response-gate1-null-clarification-20260912.md
  dimensional-resonance-response-gate1-approval-20260912.md

Authored by: Codex / OpenAI GPT-5.6 Sol, 2026-09-12.
Independent Gate 1: Claude Code / Fable 5.1 on gathering head
15787fa8a2671f899e1d974aff8753386e423cfc.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable

RINGS = (6, 7)

# Exact frozen ring-7 source-only census from the Gate-1 refreeze.
# descriptor -> (H, C, shift_capable, reflection_only, both)
EXPECTED_RING7 = {
    (2, 2, 4, 4, 2, 2): (14, 28, 0, 0, 14),
    (2, 2, 4, 4, 2, 4): (14, 28, 0, 0, 14),
    (2, 2, 4, 4, 4, 4): (14, 42, 0, 0, 14),
    (3, 3, 4, 4, 2, 2): (14, 28, 0, 14, 0),
    (3, 3, 4, 4, 2, 4): (42, 56, 0, 28, 14),
    (3, 3, 4, 4, 4, 2): (14, 28, 0, 14, 0),
    (3, 3, 4, 4, 4, 4): (98, 28, 84, 14, 0),
    (3, 3, 4, 4, 4, 6): (28, 28, 0, 14, 14),
    (3, 3, 4, 4, 6, 2): (28, 28, 0, 14, 14),
    (4, 4, 4, 4, 2, 2): (14, 28, 0, 14, 0),
    (4, 4, 4, 4, 2, 4): (42, 56, 0, 28, 14),
    (4, 4, 4, 4, 4, 2): (14, 28, 0, 14, 0),
    (4, 4, 4, 4, 4, 4): (98, 28, 84, 14, 0),
    (4, 4, 4, 4, 4, 6): (28, 28, 0, 14, 14),
    (4, 4, 4, 4, 6, 2): (28, 28, 0, 14, 14),
    (5, 5, 4, 4, 2, 2): (14, 28, 0, 0, 14),
    (5, 5, 4, 4, 2, 4): (14, 28, 0, 0, 14),
    (5, 5, 4, 4, 4, 4): (14, 42, 0, 0, 14),
}

EXPECTED_RING6 = {
    (2, 2, 4, 4, 4, 4): (12, 12),
    (4, 4, 4, 4, 4, 4): (12, 12),
}


@dataclass(frozen=True, order=True)
class Pair:
    """One ordered source pair, ordered by integer a then b (MSB-first words)."""

    a: int
    b: int


@dataclass(frozen=True)
class PairInfo:
    pair: Pair
    descriptor: tuple[int, int, int, int, int, int]
    homologous: bool
    shift_capable: bool
    reflection_only: bool
    both: bool


def rotate_left(x: int, n: int, steps: int = 1) -> int:
    """Cyclic left rotation of the fixed-width MSB-first n-bit word."""

    steps %= n
    mask = (1 << n) - 1
    if not steps:
        return x & mask
    return ((x << steps) & mask) | (x >> (n - steps))


def reverse_bits(x: int, n: int) -> int:
    y = 0
    for i in range(n):
        y = (y << 1) | ((x >> i) & 1)
    return y


def transitions(x: int, n: int) -> int:
    """Number of cyclic nearest-neighbour bit changes."""

    return sum(((x >> i) & 1) != ((x >> ((i + 1) % n)) & 1) for i in range(n))


def shift_related(a: int, b: int, n: int) -> bool:
    return any(rotate_left(a, n, j) == b for j in range(1, n))


def reflection_related(a: int, b: int, n: int) -> bool:
    r = reverse_bits(a, n)
    return any(rotate_left(r, n, j) == b for j in range(n))


def descriptor(a: int, b: int, n: int) -> tuple[int, int, int, int, int, int]:
    return (
        a.bit_count(),
        b.bit_count(),
        transitions(a, n),
        transitions(b, n),
        (a ^ b).bit_count(),
        transitions(a ^ b, n),
    )


def pair_info(a: int, b: int, n: int) -> PairInfo:
    if a == b:
        raise ValueError("primary source census excludes literal pairs")
    shift = shift_related(a, b, n)
    refl = reflection_related(a, b, n)
    return PairInfo(
        pair=Pair(a, b),
        descriptor=descriptor(a, b, n),
        homologous=shift or refl,
        shift_capable=shift,
        reflection_only=refl and not shift,
        both=shift and refl,
    )


def all_pair_info(n: int) -> list[PairInfo]:
    return [
        pair_info(a, b, n)
        for a in range(1 << n)
        for b in range(1 << n)
        if b != a
    ]


def scored_classes(n: int) -> dict[tuple[int, ...], list[PairInfo]]:
    grouped: dict[tuple[int, ...], list[PairInfo]] = defaultdict(list)
    for info in all_pair_info(n):
        grouped[info.descriptor].append(info)

    scored = {}
    for key, rows in grouped.items():
        h = sum(row.homologous for row in rows)
        c = len(rows) - h
        if h and c:
            scored[key] = sorted(rows, key=lambda row: row.pair)
    return dict(sorted(scored.items()))


def joint_shift(pair: Pair, n: int, steps: int = 1) -> Pair:
    return Pair(rotate_left(pair.a, n, steps), rotate_left(pair.b, n, steps))


def canonical_joint_shift_orbit(pair: Pair, n: int) -> tuple[Pair, ...]:
    members = {joint_shift(pair, n, j) for j in range(n)}
    return tuple(sorted(members))


def class_orbits(rows: Iterable[PairInfo], n: int) -> list[tuple[Pair, ...]]:
    """Exact joint-shift orbits in canonical representative order."""

    row_map = {row.pair: row for row in rows}
    unseen = set(row_map)
    orbits: list[tuple[Pair, ...]] = []
    while unseen:
        seed = min(unseen)
        orbit = canonical_joint_shift_orbit(seed, n)
        if any(member not in row_map for member in orbit):
            raise AssertionError("joint shift left the frozen descriptor class")
        labels = {row_map[member].homologous for member in orbit}
        if len(labels) != 1:
            raise AssertionError("homology label is not joint-shift invariant")
        orbits.append(orbit)
        unseen.difference_update(orbit)
    return sorted(orbits, key=lambda orbit: orbit[0])


def rotate_tuple(values: tuple[int, ...], steps: int) -> tuple[int, ...]:
    if not values:
        return values
    steps %= len(values)
    if not steps:
        return values
    return values[steps:] + values[:steps]


def orbit_label_vector(rows: Iterable[PairInfo], n: int) -> tuple[tuple[Pair, ...], tuple[int, ...]]:
    row_map = {row.pair: row for row in rows}
    orbits = class_orbits(row_map.values(), n)
    labels = tuple(int(row_map[orbit[0]].homologous) for orbit in orbits)
    return tuple(orbits), labels


def global_placebo_assignments(
    classes: dict[tuple[int, ...], list[PairInfo]], n: int
) -> dict[str, object]:
    """Build every distinct nonidentity B1 global orbit-label assignment.

    The common rotation index runs from 1 through L-1, where L is the LCM of
    the class orbit counts.  Within each class it is reduced modulo that orbit
    count.  Global signatures are deduplicated exactly as required by B1.
    """

    prepared = []
    counts = []
    for key, rows in classes.items():
        orbits, labels = orbit_label_vector(rows, n)
        prepared.append((key, orbits, labels))
        counts.append(len(orbits))

    lcm = math.lcm(*counts) if counts else 1
    actual_signature = tuple((key, labels) for key, _, labels in prepared)
    signatures = {}
    for r in range(1, lcm):
        signature = tuple((key, rotate_tuple(labels, r)) for key, _, labels in prepared)
        if signature == actual_signature:
            # A nonzero common index can in principle reproduce the original
            # labels when every vector has a smaller period; B1 asks for
            # nontrivial *assignments*, so do not count it.
            continue
        signatures.setdefault(signature, []).append(r)

    return {
        "common_rotation_lcm": lcm,
        "candidate_nonzero_rotations": max(0, lcm - 1),
        "distinct_nonidentity_assignments": len(signatures),
        "rotation_alias_classes": [tuple(rs) for rs in signatures.values()],
    }


def census_record(n: int) -> dict[str, object]:
    classes = scored_classes(n)
    records = []
    for key, rows in classes.items():
        h_rows = [row for row in rows if row.homologous]
        c_rows = [row for row in rows if not row.homologous]
        orbits = class_orbits(rows, n)
        row_map = {row.pair: row for row in rows}
        h_orbits = sum(row_map[orbit[0]].homologous for orbit in orbits)
        c_orbits = len(orbits) - h_orbits
        records.append(
            {
                "descriptor": list(key),
                "homologous_pairs": len(h_rows),
                "control_pairs": len(c_rows),
                "shift_capable": sum(row.shift_capable for row in h_rows),
                "reflection_only": sum(row.reflection_only for row in h_rows),
                "both": sum(row.both for row in h_rows),
                "homologous_orbits": h_orbits,
                "control_orbits": c_orbits,
                "orbit_sizes": sorted({len(orbit) for orbit in orbits}),
            }
        )
    return {
        "ring": n,
        "scored_class_count": len(classes),
        "homologous_pairs": sum(r["homologous_pairs"] for r in records),
        "control_pairs": sum(r["control_pairs"] for r in records),
        "classes": records,
        "placebo": global_placebo_assignments(classes, n),
    }


def assert_frozen_census() -> dict[str, object]:
    out = {n: census_record(n) for n in RINGS}

    ring6 = {
        tuple(row["descriptor"]): (row["homologous_pairs"], row["control_pairs"])
        for row in out[6]["classes"]
    }
    assert ring6 == EXPECTED_RING6, (ring6, EXPECTED_RING6)
    assert out[6]["scored_class_count"] == 2
    assert out[6]["homologous_pairs"] == 24
    assert out[6]["control_pairs"] == 24
    for row in out[6]["classes"]:
        assert row["shift_capable"] == 12
        assert row["reflection_only"] == 0
        assert row["both"] == 12

    ring7 = {
        tuple(row["descriptor"]): (
            row["homologous_pairs"],
            row["control_pairs"],
            row["shift_capable"],
            row["reflection_only"],
            row["both"],
        )
        for row in out[7]["classes"]
    }
    assert ring7 == EXPECTED_RING7, (ring7, EXPECTED_RING7)
    assert out[7]["scored_class_count"] == 18
    assert out[7]["homologous_pairs"] == 532
    assert out[7]["control_pairs"] == 588
    for row in out[7]["classes"]:
        assert row["orbit_sizes"] == [7]
        assert row["homologous_orbits"] * 7 == row["homologous_pairs"]
        assert row["control_orbits"] * 7 == row["control_pairs"]

    # Reviewer-side Gate-1 analysis bounded the common rotation period by 504.
    assert out[7]["placebo"]["common_rotation_lcm"] == 504
    assert out[7]["placebo"]["candidate_nonzero_rotations"] == 503
    assert 0 < out[7]["placebo"]["distinct_nonidentity_assignments"] <= 503
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run source-only Gate-1 census/placebo checks; no physical evolution",
    )
    parser.add_argument("--output", help="optional source-only JSON diagnostic path")
    args = parser.parse_args()

    if not args.self_test:
        raise SystemExit(
            "physical-response evaluation is intentionally unavailable in this "
            "source-only implementation chunk; use --self-test"
        )

    result = {
        "schema": 1,
        "stage": "implementation_source_only_no_result",
        "reviewed_gate1_head": "15787fa8a2671f899e1d974aff8753386e423cfc",
        "physical_response_evaluated": False,
        "rings": list(RINGS),
        "census": assert_frozen_census(),
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
