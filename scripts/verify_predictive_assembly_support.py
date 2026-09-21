#!/usr/bin/env python3
"""Exact predictive-assembly-support verifier for the accepted #157 finite cells.

Protocol:
  docs/research/protocols/predictive-assembly-support-20260912.md
Binding Gate-1 clarification:
  docs/research/protocols/predictive-assembly-support-gate1-clarification-20260912.md

Implementation-only discipline: ``--self-test`` uses synthetic decision tables and
predecessor hash/schema checks only. Running without ``--self-test`` performs the
frozen n=6,7 scientific census and writes the canonical result.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import pathlib
from dataclasses import dataclass
from functools import lru_cache
from typing import Iterable, Sequence

from verify_interface_factor import COORDINATES, build_ring_orbit, field_mask
import verify_interface_history_global as predecessor

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "docs/research/protocols/predictive-assembly-support-20260912.md"
CLARIFICATION = ROOT / "docs/research/protocols/predictive-assembly-support-gate1-clarification-20260912.md"
PREV_SCRIPT = ROOT / "scripts/verify_interface_history_global.py"
PREV_RESULT = ROOT / "results/interface_history_global_20260912.json"
OUT = ROOT / "results/predictive_assembly_support_20260912.json"
PRIMARY = {6: (11, 13, 15), 7: (3, 5, 7, 11, 13, 15)}


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def selected_channels(mask: int) -> tuple[int, ...]:
    selected = field_mask(mask)
    return tuple(i for i in range(len(COORDINATES)) if (selected >> i) & 1)


def atom_labels(n: int, mask: int) -> tuple[tuple[int, int, str], ...]:
    channels = selected_channels(mask)
    return tuple(
        (lag, site, COORDINATES[ch])
        for lag in (2, 1, 0)
        for site in range(n)
        for ch in channels
    )


def orbit_labels(mask: int) -> tuple[tuple[int, str], ...]:
    channels = selected_channels(mask)
    return tuple((lag, COORDINATES[ch]) for lag in (2, 1, 0) for ch in channels)


def flatten_key_int(orbit, source: int, t: int, mask: int) -> int:
    channels = selected_channels(mask)
    value = 0
    bit = 0
    for tt in range(t - 2, t + 1):
        symbols = orbit.symbols[tt][source]
        for site in range(orbit.n):
            symbol = int(symbols[site])
            for ch in channels:
                value |= ((symbol >> ch) & 1) << bit
                bit += 1
    return value


def flatten_target_int(orbit, source: int, t: int, mask: int) -> int:
    channels = selected_channels(mask)
    value = 0
    bit = 0
    symbols = orbit.symbols[t + 1][source]
    for site in range(orbit.n):
        symbol = int(symbols[site])
        for ch in channels:
            value |= ((symbol >> ch) & 1) << bit
            bit += 1
    return value


def flatten_key_tuple(orbit, source: int, t: int, mask: int) -> tuple[int, ...]:
    channels = selected_channels(mask)
    return tuple(
        (int(orbit.symbols[tt][source, site]) >> ch) & 1
        for tt in range(t - 2, t + 1)
        for site in range(orbit.n)
        for ch in channels
    )


def flatten_target_tuple(orbit, source: int, t: int, mask: int) -> tuple[int, ...]:
    channels = selected_channels(mask)
    return tuple(
        (int(orbit.symbols[t + 1][source, site]) >> ch) & 1
        for site in range(orbit.n)
        for ch in channels
    )


@dataclass(frozen=True)
class PackedClass:
    key: int
    target: int
    first_record: int


@dataclass(frozen=True)
class TupleClass:
    key: tuple[int, ...]
    target: tuple[int, ...]
    first_record: int


def packed_classes(orbit, mask: int) -> tuple[PackedClass, ...]:
    records = predecessor.build_global_records(orbit, "D2", 2)
    seen: dict[int, tuple[int, int]] = {}
    for i in range(len(records.t)):
        source = int(records.source[i])
        t = int(records.t[i])
        key = flatten_key_int(orbit, source, t, mask)
        target = flatten_target_int(orbit, source, t, mask)
        old = seen.get(key)
        if old is None:
            seen[key] = (target, i)
        elif old[0] != target:
            raise AssertionError(("accepted pass became conflicting", orbit.n, mask, old[1], i))
    return tuple(PackedClass(k, target, first) for k, (target, first) in sorted(seen.items()))


def tuple_classes(orbit, mask: int) -> tuple[TupleClass, ...]:
    records = predecessor.build_global_records(orbit, "D2", 2)
    seen: dict[tuple[int, ...], tuple[tuple[int, ...], int]] = {}
    for i in range(len(records.t)):
        source = int(records.source[i])
        t = int(records.t[i])
        key = flatten_key_tuple(orbit, source, t, mask)
        target = flatten_target_tuple(orbit, source, t, mask)
        old = seen.get(key)
        if old is None:
            seen[key] = (target, i)
        elif old[0] != target:
            raise AssertionError(("accepted pass became conflicting(reference)", orbit.n, mask, old[1], i))
    return tuple(TupleClass(k, target, first) for k, (target, first) in sorted(seen.items()))


def first_packed_conflict(classes: Sequence[PackedClass], support: int) -> tuple[int, int, int] | None:
    seen: dict[int, tuple[int, int, int]] = {}
    for idx, row in enumerate(classes):
        proj = row.key & support
        old = seen.get(proj)
        if old is None:
            seen[proj] = (row.target, idx, row.key)
            continue
        old_target, old_idx, old_key = old
        if old_target != row.target:
            diff = old_key ^ row.key
            if diff == 0:
                raise AssertionError("different targets with identical full keys")
            return old_idx, idx, diff
    return None


def tuple_support_ok(classes: Sequence[TupleClass], selected: tuple[int, ...]) -> bool:
    seen: dict[tuple[int, ...], tuple[int, ...]] = {}
    for row in classes:
        proj = tuple(row.key[i] for i in selected)
        old = seen.get(proj)
        if old is None:
            seen[proj] = row.target
        elif old != row.target:
            return False
    return True


def first_tuple_conflict(classes: Sequence[TupleClass], selected: tuple[int, ...]) -> tuple[int, int, tuple[int, ...]] | None:
    seen: dict[tuple[int, ...], tuple[tuple[int, ...], int]] = {}
    chosen = set(selected)
    for idx, row in enumerate(classes):
        proj = tuple(row.key[i] for i in selected)
        old = seen.get(proj)
        if old is None:
            seen[proj] = (row.target, idx)
            continue
        old_target, old_idx = old
        if old_target != row.target:
            diff = tuple(i for i, (a, b) in enumerate(zip(classes[old_idx].key, row.key)) if a != b and i not in chosen)
            if not diff:
                return old_idx, idx, ()
            return old_idx, idx, diff
    return None


def minimize_constraints(constraints: Iterable[int]) -> tuple[int, ...]:
    unique = sorted(set(c for c in constraints if c), key=lambda x: (x.bit_count(), x))
    kept: list[int] = []
    for c in unique:
        if any((k & c) == k for k in kept):
            continue
        kept.append(c)
    return tuple(kept)


def support_tuple(mask: int) -> tuple[int, ...]:
    return tuple(i for i in range(mask.bit_length()) if (mask >> i) & 1)


def better_support(a: int | None, b: int) -> int:
    if a is None:
        return b
    ka, kb = a.bit_count(), b.bit_count()
    if kb < ka:
        return b
    if kb > ka:
        return a
    return b if support_tuple(b) < support_tuple(a) else a


def greedy_hitting_set(constraints: tuple[int, ...]) -> int:
    remaining = list(constraints)
    chosen = 0
    while remaining:
        counts: dict[int, int] = {}
        for c in remaining:
            x = c
            while x:
                lsb = x & -x
                i = lsb.bit_length() - 1
                counts[i] = counts.get(i, 0) + 1
                x ^= lsb
        bit = min((-count, i) for i, count in counts.items())[1]
        chosen |= 1 << bit
        remaining = [c for c in remaining if not ((c >> bit) & 1)]
    return chosen


def disjoint_lower_bound(constraints: tuple[int, ...]) -> int:
    used = 0
    count = 0
    for c in sorted(constraints, key=lambda x: (x.bit_count(), x)):
        if c & used:
            continue
        used |= c
        count += 1
    return count


def exact_hitting_set(constraints: Iterable[int]) -> int:
    """Exact branch-and-bound minimum hitting set with canonical tie-breaking."""
    initial = minimize_constraints(constraints)
    if not initial:
        return 0
    best_size = greedy_hitting_set(initial).bit_count()

    @lru_cache(maxsize=None)
    def solve(state: tuple[int, ...], chosen_count: int = 0) -> int | None:
        nonlocal best_size
        state = minimize_constraints(state)
        if not state:
            return 0
        if chosen_count + disjoint_lower_bound(state) > best_size:
            return None
        forced = 0
        rest = state
        while True:
            singleton = next((c for c in rest if c.bit_count() == 1), None)
            if singleton is None:
                break
            forced |= singleton
            rest = tuple(c for c in rest if not (c & singleton))
            rest = minimize_constraints(rest)
        if forced:
            tail = solve(rest, chosen_count + forced.bit_count())
            if tail is None:
                return None
            return forced | tail
        pivot = min(rest, key=lambda c: (c.bit_count(), c))
        candidates = []
        bits = support_tuple(pivot)
        coverage = {i: sum(bool(c & (1 << i)) for c in rest) for i in bits}
        for i in sorted(bits, key=lambda i: (-coverage[i], i)):
            bit = 1 << i
            next_state = tuple(c for c in rest if not (c & bit))
            tail = solve(next_state, chosen_count + 1)
            if tail is None:
                continue
            candidates.append(bit | tail)
        answer: int | None = None
        for c in candidates:
            answer = better_support(answer, c)
        if answer is not None:
            best_size = min(best_size, chosen_count + answer.bit_count())
        return answer

    answer = solve(initial, 0)
    if answer is None:
        raise AssertionError("exact hitting-set search failed")
    return answer


def cutting_plane_optimum(classes: Sequence[PackedClass]) -> tuple[int, tuple[int, ...]]:
    constraints: list[int] = []
    support = 0
    seen_constraints: set[int] = set()
    while True:
        conflict = first_packed_conflict(classes, support)
        if conflict is None:
            return support, minimize_constraints(constraints)
        diff = conflict[2]
        if diff in seen_constraints:
            raise AssertionError("cutting-plane stalled on repeated violated constraint")
        seen_constraints.add(diff)
        constraints.append(diff)
        support = exact_hitting_set(constraints)


def reference_exists_at_most(classes: Sequence[TupleClass], k: int, n_atoms: int) -> int | None:
    """Independent direct decision-table search; no prebuilt difference family."""
    memo: set[tuple[tuple[int, ...], int]] = set()

    def rec(selected: tuple[int, ...], remaining: int) -> tuple[int, ...] | None:
        key = (selected, remaining)
        if key in memo:
            return None
        memo.add(key)
        conflict = first_tuple_conflict(classes, selected)
        if conflict is None:
            return selected
        if remaining == 0:
            return None
        diff = conflict[2]
        for atom in diff:
            if atom in selected:
                continue
            nxt = tuple(sorted((*selected, atom)))
            found = rec(nxt, remaining - 1)
            if found is not None:
                return found
        return None

    found = rec((), k)
    if found is None:
        return None
    mask = sum(1 << i for i in found)
    if not tuple_support_ok(classes, found):
        raise AssertionError("reference solver returned insufficient support")
    return mask


def target_count_lower_bound(classes: Sequence[TupleClass]) -> tuple[int, int]:
    """Independent information lower bound from the tuple decision table.

    A support of s binary atoms has at most 2**s projected keys. Prediction
    sufficiency forbids two distinct target classes from sharing a projected key,
    so s >= ceil(log2(number of target classes)). This uses only the explicit
    tuple table, not the packed cutting-plane constraint family.
    """
    target_count = len({row.target for row in classes})
    lower = 0 if target_count <= 1 else (target_count - 1).bit_length()
    return lower, target_count


def tuple_difference_mask(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    out = 0
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            out |= 1 << i
    return out


def disjoint_witness_packing(classes: Sequence[TupleClass], optimum: int) -> tuple[int, ...] | None:
    """Try to certify |optimum| by pairwise-disjoint cross-target differences.

    Minimality of a sufficient support S implies that, for each atom i in S,
    removing i exposes at least one cross-target collision. We enumerate the
    exact tuple-table collisions under S\{i}; every resulting difference meets
    S exactly in i. A backtracking matching then asks for one witness per support
    atom whose full difference sets are pairwise disjoint. If found, these k
    actual decision-table differences are a machine-checkable lower bound k for
    every hitting set. Failure to find such a packing is not treated as evidence;
    the canonical evaluation stops without a result instead of falling back to
    the previously unbounded iterative-deepening search.
    """
    support_atoms = support_tuple(optimum)
    if not support_atoms:
        return ()
    support_mask = optimum
    candidates: dict[int, tuple[int, ...]] = {}
    for atom in support_atoms:
        selected = tuple(i for i in support_atoms if i != atom)
        groups: dict[tuple[int, ...], list[TupleClass]] = {}
        for row in classes:
            proj = tuple(row.key[i] for i in selected)
            groups.setdefault(proj, []).append(row)
        diffs: set[int] = set()
        bit = 1 << atom
        for rows in groups.values():
            if len(rows) < 2:
                continue
            for i, left in enumerate(rows):
                for right in rows[i + 1:]:
                    if left.target == right.target:
                        continue
                    diff = tuple_difference_mask(left.key, right.key)
                    if not (diff & bit):
                        raise AssertionError("full optimum would conflict after removing one atom")
                    if diff & (support_mask ^ bit):
                        raise AssertionError("projection group disagrees on another optimum atom")
                    diffs.add(diff)
        minimal = minimize_constraints(diffs)
        if not minimal:
            raise AssertionError(("minimum support atom has no tuple-table necessity witness", atom))
        candidates[atom] = minimal

    order = sorted(support_atoms, key=lambda atom: (len(candidates[atom]), atom))

    def rec(pos: int, used: int, chosen: tuple[int, ...]) -> tuple[int, ...] | None:
        if pos == len(order):
            return chosen
        atom = order[pos]
        for diff in candidates[atom]:
            if diff & used:
                continue
            found = rec(pos + 1, used | diff, (*chosen, diff))
            if found is not None:
                return found
        return None

    packed = rec(0, 0, ())
    if packed is None:
        return None
    if len(packed) != len(support_atoms):
        raise AssertionError("disjoint witness packing cardinality mismatch")
    used = 0
    for diff in packed:
        if not diff or (diff & used):
            raise AssertionError("invalid disjoint witness packing")
        used |= diff
    return packed


def independent_raw_certificate(classes: Sequence[TupleClass], optimum: int, n_atoms: int) -> dict:
    """Machine-check an exact lower bound without exponential tuple DFS."""
    del n_atoms
    k = optimum.bit_count()
    lower, target_count = target_count_lower_bound(classes)
    if lower == k:
        return {
            "method": "target_class_count_binary_projection_bound",
            "target_class_count": target_count,
            "lower_bound": lower,
            "reference_optimum": k,
        }
    if lower > k:
        raise AssertionError(("independent counting lower bound exceeds primary optimum", lower, k))

    packing = disjoint_witness_packing(classes, optimum)
    if packing is not None and len(packing) == k:
        return {
            "method": "pairwise_disjoint_difference_witness_packing",
            "target_class_count": target_count,
            "counting_lower_bound": lower,
            "lower_bound": len(packing),
            "difference_witness_masks": list(packing),
            "reference_optimum": k,
        }
    raise RuntimeError(
        f"independent exact lower-bound certificate did not reach primary optimum k={k}; "
        f"target-count bound={lower}, disjoint packing="
        f"{None if packing is None else len(packing)}. No canonical result written."
    )


def orbit_support_mask(raw_orbit_subset: int, n: int, mask: int) -> int:
    labels = atom_labels(n, mask)
    orbits = orbit_labels(mask)
    lookup = {label: i for i, label in enumerate(orbits)}
    support = 0
    for atom_i, (lag, _site, channel) in enumerate(labels):
        if (raw_orbit_subset >> lookup[(lag, channel)]) & 1:
            support |= 1 << atom_i
    return support


def exact_orbit_solutions(classes: Sequence[PackedClass], n: int, mask: int) -> tuple[int, list[int]]:
    count = len(orbit_labels(mask))
    for size in range(count + 1):
        solutions: list[int] = []
        for combo in itertools.combinations(range(count), size):
            subset = sum(1 << i for i in combo)
            support = orbit_support_mask(subset, n, mask)
            if first_packed_conflict(classes, support) is None:
                solutions.append(subset)
        if solutions:
            return size, solutions
    raise AssertionError("full orbit support should be sufficient for accepted pass")


def single_lag_orbit_possible(classes: Sequence[PackedClass], n: int, mask: int, lag: int) -> bool:
    labels = orbit_labels(mask)
    eligible = [i for i, (ell, _ch) in enumerate(labels) if ell == lag]
    for r in range(len(eligible) + 1):
        for combo in itertools.combinations(eligible, r):
            subset = sum(1 << i for i in combo)
            if first_packed_conflict(classes, orbit_support_mask(subset, n, mask)) is None:
                return True
    return False


def support_json(mask: int, labels: Sequence[tuple[int, int, str]]) -> list[dict]:
    return [
        {"lag": labels[i][0], "site": labels[i][1], "channel": labels[i][2]}
        for i in support_tuple(mask)
    ]


def orbit_support_json(subset: int, labels: Sequence[tuple[int, str]]) -> list[dict]:
    return [
        {"lag": labels[i][0], "channel": labels[i][1]}
        for i in support_tuple(subset)
    ]


def evaluate_cell(orbit, mask: int) -> dict:
    labels = atom_labels(orbit.n, mask)
    packed = packed_classes(orbit, mask)
    tuples = tuple_classes(orbit, mask)
    if len(packed) != len(tuples):
        raise AssertionError(("packed/reference class count mismatch", orbit.n, mask))

    optimum, generated_constraints = cutting_plane_optimum(packed)
    if first_packed_conflict(packed, optimum) is not None:
        raise AssertionError("reported raw support is insufficient")
    reference_certificate = independent_raw_certificate(tuples, optimum, len(labels))

    orbit_k, orbit_solutions = exact_orbit_solutions(packed, orbit.n, mask)
    canonical_orbit = min(orbit_solutions, key=lambda x: support_tuple(x))
    lag_restricted = {str(lag): single_lag_orbit_possible(packed, orbit.n, mask, lag) for lag in (2, 1, 0)}
    if lag_restricted["0"]:
        raise AssertionError("P5 lag-0 predecessor deduction violated")
    if not any(labels[i][0] == 2 for i in support_tuple(optimum)):
        raise AssertionError("P3 deduced lag-2 necessity violated")

    n_full = len(labels)
    return {
        "ring": orbit.n,
        "mask": mask,
        "retained_channels": [COORDINATES[i] for i in selected_channels(mask)],
        "record_class_count": len(packed),
        "target_class_count": len({row.target for row in packed}),
        "N_full": n_full,
        "PAS_raw": optimum.bit_count(),
        "PAS_raw_density": optimum.bit_count() / n_full,
        "canonical_raw_support": support_json(optimum, labels),
        "cutting_plane_minimal_difference_constraints": len(generated_constraints),
        "independent_raw_optimality_certificate": reference_certificate,
        "P2_strict_redundancy_bet": 0 < optimum.bit_count() < n_full,
        "P3_deduced_lag2_present": True,
        "PAS_orbit": orbit_k,
        "canonical_orbit_support": orbit_support_json(canonical_orbit, orbit_labels(mask)),
        "orbit_minimum_solution_count": len(orbit_solutions),
        "single_lag_orbit_sufficiency": lag_restricted,
    }


def check_predecessor_exact() -> dict:
    accepted = json.loads(PREV_RESULT.read_text())
    if accepted["source_hashes"].get("script") != sha(PREV_SCRIPT):
        raise AssertionError("#157 verifier hash mismatch")
    if accepted["source_hashes"].get("protocol") != sha(ROOT / "docs/research/protocols/interface-history-global-20260912.md"):
        raise AssertionError("#157 protocol hash mismatch")
    regenerated = predecessor.evaluate()
    if regenerated != accepted:
        raise AssertionError("P1: current predecessor machinery does not reproduce accepted #157 result exactly")
    return accepted


def evaluate() -> dict:
    accepted = check_predecessor_exact()
    cells = []
    for n in (6, 7):
        orbit = build_ring_orbit(n)
        for mask in PRIMARY[n]:
            if not accepted["census"][str(n)]["D2"]["2"][str(mask)]["pass"]:
                raise AssertionError(("primary cell no longer accepted pass", n, mask))
            cells.append(evaluate_cell(orbit, mask))

    by = {(row["ring"], row["mask"]): row for row in cells}
    p15_density_diff = abs(by[(6, 15)]["PAS_raw_density"] - by[(7, 15)]["PAS_raw_density"])
    p5_open = {
        str(n): {
            "lag1_only_sufficient": by[(n, 15)]["single_lag_orbit_sufficiency"]["1"],
            "lag2_only_sufficient": by[(n, 15)]["single_lag_orbit_sufficiency"]["2"],
        }
        for n in (6, 7)
    }
    return {
        "protocol": "predictive-assembly-support-20260912",
        "schema": 1,
        "source_hashes": {
            "script": sha(pathlib.Path(__file__)),
            "protocol": sha(PROTOCOL),
            "gate1_clarification": sha(CLARIFICATION),
            "predecessor_script": sha(PREV_SCRIPT),
            "predecessor_result": sha(PREV_RESULT),
        },
        "parameters": {
            "primary_cells": {"6": [11, 13, 15], "7": [3, 5, 7, 11, 13, 15]},
            "atom_order": "lag oldest-to-newest (2,1,0), site, accepted channel order",
            "target": "complete next retained field",
            "raw_solver": "exact cutting-plane minimum hitting set",
            "independent_certificate": "machine-checked tuple-table lower bound: target-class count, with disjoint-difference packing fallback",
            "orbit_solver": "full subset enumeration over lag/channel translation orbits",
        },
        "controls": {
            "P1_predecessor_byte_exact_regeneration": True,
            "P3_lag2_necessity_deduced_and_checked_all_nine": all(row["P3_deduced_lag2_present"] for row in cells),
            "P5_lag0_only_impossible_deduced_and_checked": all(not row["single_lag_orbit_sufficiency"]["0"] for row in cells),
        },
        "cells": cells,
        "predictions": {
            "P2_all_cells_strict_redundancy": all(row["P2_strict_redundancy_bet"] for row in cells),
            "P4_P15_density_difference": p15_density_diff,
            "P4_density_difference_at_most_0_15": p15_density_diff <= 0.15,
            "P5_full_P15_single_lag_open_cases": p5_open,
            "P5_orbit_minima_use_multiple_times_both_rings": all(
                not any(by[(n, 15)]["single_lag_orbit_sufficiency"][lag] for lag in ("2", "1", "0"))
                for n in (6, 7)
            ),
        },
        "deduced_conflicting_cells": {
            "count": 183,
            "PAS": "infinity/no finite support by accepted #157 global conflict; no new computation",
        },
        "scope": "minimum predictive coordinate support on accepted finite #157 D2,h=2 records only; not Assembly Theory assembly index, entropy, state complexity, intrinsic dimension, self-assembly, endogenous control, or physics/metaphysics",
    }


def self_test() -> None:
    packed = tuple(
        PackedClass(key, ((key >> 0) & 1) | (((key >> 2) & 1) << 1), key)
        for key in range(16)
    )
    optimum, constraints = cutting_plane_optimum(packed)
    assert optimum.bit_count() == 2 and support_tuple(optimum) == (0, 2)
    tuples = tuple(
        TupleClass(
            tuple((key >> i) & 1 for i in range(4)),
            ((row.target & 1), (row.target >> 1) & 1),
            key,
        )
        for key, row in enumerate(packed)
    )
    cert = independent_raw_certificate(tuples, optimum, 4)
    assert cert["reference_optimum"] == 2
    assert cert["method"] == "target_class_count_binary_projection_bound"
    assert constraints

    parity_packed = tuple(PackedClass(key, (key & 1) ^ ((key >> 1) & 1), key) for key in range(4))
    parity_optimum, _ = cutting_plane_optimum(parity_packed)
    assert parity_optimum.bit_count() == 2
    parity_tuples = tuple(
        TupleClass(tuple((key >> i) & 1 for i in range(2)), (row.target,), key)
        for key, row in enumerate(parity_packed)
    )
    parity_cert = independent_raw_certificate(parity_tuples, parity_optimum, 2)
    assert parity_cert["reference_optimum"] == 2
    assert parity_cert["method"] == "pairwise_disjoint_difference_witness_packing"
    assert len(parity_cert["difference_witness_masks"]) == 2

    accepted = json.loads(PREV_RESULT.read_text())
    assert accepted["source_hashes"]["script"] == sha(PREV_SCRIPT)
    assert sum(
        int(accepted["census"][str(n)]["D2"]["2"][str(mask)]["pass"])
        for n in (6, 7) for mask in range(16)
    ) == 9
    assert PROTOCOL.exists() and CLARIFICATION.exists()
    print("predictive-assembly-support implementation self-test passed; no PAS source-domain evaluation performed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    result = evaluate()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "PAS_raw": {f"{r['ring']}/{r['mask']}": r["PAS_raw"] for r in result["cells"]},
        "PAS_orbit": {f"{r['ring']}/{r['mask']}": r["PAS_orbit"] for r in result["cells"]},
        "predictions": result["predictions"],
    }, sort_keys=True))
    print("written", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
