#!/usr/bin/env python3
"""Pinned physical-response verifier for dimensional-resonance PR #173.

Governing Gate-1 stack:
  docs/research/protocols/dimensional-resonance-response-20260912.md
  docs/research/protocols/dimensional-resonance-response-gate1-refreeze-20260912.md
  docs/research/protocols/dimensional-resonance-response-gate1-null-clarification-20260912.md
  docs/research/protocols/dimensional-resonance-response-gate1-approval-20260912.md

Implementation-only discipline: ``--self-test`` uses only out-of-domain n=3
pairs and synthetic label tables.  It exercises the packed and scalar physical
paths, exact causal-window V/M/S/R observables, the k=1 predecessor 64-word table, exact rational contrasts, and orbit-preserving placebo machinery.  It
never evaluates the frozen n=6,7 source domain and never writes the canonical
result.

Running without ``--self-test`` performs the frozen scientific evaluation.  By
Myk's 2026-09-12 CI-cost rule that run, and any full byte-for-byte replay, must
be executed outside GitHub Actions if expected or observed to exceed ~10 min.
Automatic CI for this verifier is self-test + fast source-integrity only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import pathlib
from collections import defaultdict
from fractions import Fraction
from typing import Iterable, Mapping, Sequence

import numpy as np

from verify_dimensional_resonance_source_census import (
    Pair,
    PairInfo,
    assert_frozen_census,
    class_orbits,
    global_placebo_assignments,
    rotate_tuple,
    scored_classes,
)
from verify_interface_factor import (
    encode_adjacent,
    fine_step_ring,
    row_bits,
    scalar_encode_adjacent,
    scalar_fine_step_ring,
)

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "results/dimensional_resonance_response_20260912.json"
PROTOCOL = ROOT / "docs/research/protocols/dimensional-resonance-response-20260912.md"
REFREEZE = ROOT / "docs/research/protocols/dimensional-resonance-response-gate1-refreeze-20260912.md"
CLARIFICATION = ROOT / "docs/research/protocols/dimensional-resonance-response-gate1-null-clarification-20260912.md"
APPROVAL = ROOT / "docs/research/protocols/dimensional-resonance-response-gate1-approval-20260912.md"
SOURCE_SCRIPT = ROOT / "scripts/verify_dimensional_resonance_source_census.py"
PHYSICAL_SCRIPT = ROOT / "scripts/verify_interface_factor.py"

RINGS = (6, 7)
HORIZONS = (1, 2, 3, 4)
MAX_HORIZON = max(HORIZONS)
METRICS = ("V", "M", "S", "R")


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def row_words(values: Sequence[int], n: int) -> np.ndarray:
    shifts = np.arange(n - 1, -1, -1, dtype=np.uint64)
    arr = np.asarray(values, dtype=np.uint64)
    return ((arr[:, None] >> shifts) & np.uint64(1)).astype(np.uint8)


def rule90_rows(rows: np.ndarray) -> np.ndarray:
    rows = np.asarray(rows, dtype=np.uint8)
    return np.roll(rows, 1, axis=-1) ^ np.roll(rows, -1, axis=-1)


def rule90_int(value: int, n: int) -> int:
    mask = (1 << n) - 1
    left = ((value << 1) & mask) | (value >> (n - 1))
    right = (value >> 1) | ((value & 1) << (n - 1))
    return left ^ right


def causal_window(k: int) -> tuple[int, int]:
    return -2 * k, 3 + 2 * k


def slice_rows(field: np.ndarray, ys: np.ndarray, lo: int, hi: int) -> np.ndarray:
    indices = np.flatnonzero((ys >= lo) & (ys <= hi))
    expected = hi - lo + 1
    if len(indices) != expected or tuple(int(ys[i]) for i in indices) != tuple(range(lo, hi + 1)):
        raise AssertionError(("causal window missing rows", lo, hi, ys.tolist()))
    return field[..., indices, :]


def metric_arrays(physical: np.ndarray, baseline: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    residual = physical ^ baseline
    axes = tuple(range(1, residual.ndim))
    valid = ~np.any(residual, axis=axes)
    mass = residual.sum(axis=axes, dtype=np.int64)
    row_nonzero = np.any(residual, axis=-1)
    span = np.zeros(residual.shape[0], dtype=np.int64)
    for i in range(residual.shape[0]):
        rows = np.flatnonzero(row_nonzero[i])
        if len(rows):
            span[i] = int(rows[-1] - rows[0] + 1)
    return valid.astype(np.uint8), mass, span


def packed_responses(n: int, pairs: Sequence[Pair], max_horizon: int = MAX_HORIZON) -> dict[Pair, dict[int, dict[str, int]]]:
    """Vectorized physical path over an explicit ordered pair list."""
    if not pairs:
        return {}
    a_values = [p.a for p in pairs]
    b_values = [p.b for p in pairs]
    a = row_words(a_values, n)
    b = row_words(b_values, n)
    xs = np.arange(2 * n, dtype=int)

    # fine_step_ring shrinks one vertical row per fine tick.  Starting with
    # +/-4K margin leaves exactly the K-horizon causal window at K and a strict
    # superset at earlier horizons.
    margin = 4 * max_horizon
    ys = np.arange(-margin, 4 + margin, dtype=int)
    field = encode_adjacent(a, b, ys, xs)
    current_ys = ys.copy()
    logical_a = a.copy()
    logical_b = b.copy()
    valid_history: list[np.ndarray] = []
    returned_so_far = np.zeros(len(pairs), dtype=np.uint8)
    result: dict[Pair, dict[int, dict[str, int]]] = {p: {} for p in pairs}

    for k in range(1, max_horizon + 1):
        field = fine_step_ring(field)
        field = fine_step_ring(field)
        current_ys = current_ys[2:-2]
        logical_a = rule90_rows(logical_a)
        logical_b = rule90_rows(logical_b)
        lo, hi = causal_window(k)
        physical = slice_rows(field, current_ys, lo, hi)
        desired_ys = np.arange(lo, hi + 1, dtype=int)
        baseline = encode_adjacent(logical_a, logical_b, desired_ys, xs)
        valid, mass, span = metric_arrays(physical, baseline)
        valid_history.append(valid)
        if k > 1:
            earlier_invalid = ~np.logical_and.reduce([v.astype(bool) for v in valid_history[:-1]])
            returned_so_far |= (earlier_invalid & valid.astype(bool)).astype(np.uint8)
        returned = returned_so_far.copy()
        for i, pair in enumerate(pairs):
            result[pair][k] = {
                "V": int(valid[i]),
                "M": int(mass[i]),
                "S": int(span[i]),
                "R": int(returned[i]),
            }
    return result


def scalar_response(n: int, pair: Pair, max_horizon: int = MAX_HORIZON) -> dict[int, dict[str, int]]:
    """Independent scalar path used for exact replay of reported summaries."""
    margin = 4 * max_horizon
    ys = np.arange(-margin, 4 + margin, dtype=int)
    field = scalar_encode_adjacent(pair.a, pair.b, n, ys)
    logical_a, logical_b = pair.a, pair.b
    validity: list[int] = []
    returned_so_far = 0
    out: dict[int, dict[str, int]] = {}
    for k in range(1, max_horizon + 1):
        field = scalar_fine_step_ring(field)
        field = scalar_fine_step_ring(field)
        ys = ys[2:-2]
        logical_a = rule90_int(logical_a, n)
        logical_b = rule90_int(logical_b, n)
        lo, hi = causal_window(k)
        physical = slice_rows(field[None, ...], ys, lo, hi)[0]
        desired_ys = np.arange(lo, hi + 1, dtype=int)
        baseline = scalar_encode_adjacent(logical_a, logical_b, n, desired_ys)
        residual = physical ^ baseline
        v = int(not np.any(residual))
        m = int(residual.sum(dtype=np.int64))
        occupied = np.flatnonzero(np.any(residual, axis=-1))
        s = int(occupied[-1] - occupied[0] + 1) if len(occupied) else 0
        validity.append(v)
        if k > 1 and v == 1 and any(x == 0 for x in validity[:-1]):
            returned_so_far = 1
        out[k] = {"V": v, "M": m, "S": s, "R": returned_so_far}
    return out


def scalar_open_step(field: list[list[int]]) -> list[list[int]]:
    """Independent literal open-boundary step2 used only for the inherited k=1 table."""
    h = len(field)
    w = len(field[0])
    out = [[0 for _ in range(w - 2)] for _ in range(h - 2)]
    for oy, y in enumerate(range(1, h - 1)):
        for ox, x in enumerate(range(1, w - 1)):
            center = int(field[y][x])
            left = int(field[y][x - 1])
            right = int(field[y][x + 1])
            source_y = y + 2 * center - 1
            source_x = x + left + right - 1
            out[oy][ox] = int(field[source_y][source_x])
    return out


def local_word_predecessor_metrics(word: int) -> tuple[int, int]:
    """Exact predecessor-table entry for one local six-word.

    ``word`` is MSB-first ``(a_l,a_c,a_r,b_l,b_c,b_r)``. This path is
    deliberately scalar and open-boundary. It does not call the vectorized
    physical step used by the scored response census.
    """
    a_l, a_c, a_r, b_l, b_c, b_r = ((word >> shift) & 1 for shift in range(5, -1, -1))
    a = (a_c, a_r, a_l)
    b = (b_c, b_r, b_l)
    ys = tuple(range(-4, 8))
    xs = tuple(range(-2, 4))
    y_index = {y: j for j, y in enumerate(ys)}

    field = [[x & 1 for x in xs] for _ in ys]
    for k, x in enumerate(xs):
        block = (x // 2) % 3
        if x & 1:
            field[y_index[0]][k] = 1 ^ a[block]
            field[y_index[2]][k] = 1 ^ b[block]
        else:
            field[y_index[1]][k] = a[block]
            field[y_index[3]][k] = b[block]

    output = scalar_open_step(scalar_open_step(field))
    rows = tuple(range(-2, 6))
    out_xs = (0, 1)
    row_index = {y: j for j, y in enumerate(rows)}
    decoded_a = int(output[row_index[1]][0])
    decoded_b = int(output[row_index[3]][0])

    reconstructed = [[x & 1 for x in out_xs] for _ in rows]
    for k, x in enumerate(out_xs):
        if x & 1:
            reconstructed[row_index[0]][k] = 1 ^ decoded_a
            reconstructed[row_index[2]][k] = 1 ^ decoded_b
        else:
            reconstructed[row_index[1]][k] = decoded_a
            reconstructed[row_index[3]][k] = decoded_b

    residual_mass = sum(
        int(output[y][x] != reconstructed[y][x])
        for y in range(len(rows))
        for x in range(len(out_xs))
    )
    return int(residual_mass == 0), residual_mass


def predecessor_table() -> tuple[tuple[int, int], ...]:
    table = tuple(local_word_predecessor_metrics(word) for word in range(64))
    valid_count = sum(v for v, _ in table)
    if valid_count != 17:
        raise AssertionError(("R1 17/64 predecessor table mismatch", valid_count))
    return table


def pair_k1_from_predecessor_table(a: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Lift the exact 64-word predecessor table around a periodic logical ring."""
    table = predecessor_table()
    sources, n = a.shape
    valid = np.ones(sources, dtype=np.uint8)
    mass = np.zeros(sources, dtype=np.int64)
    for i in range(n):
        indices = (
            (a[:, (i - 1) % n].astype(np.int64) << 5)
            | (a[:, i].astype(np.int64) << 4)
            | (a[:, (i + 1) % n].astype(np.int64) << 3)
            | (b[:, (i - 1) % n].astype(np.int64) << 2)
            | (b[:, i].astype(np.int64) << 1)
            | b[:, (i + 1) % n].astype(np.int64)
        )
        local_v = np.fromiter((table[int(index)][0] for index in indices), dtype=np.uint8, count=sources)
        local_m = np.fromiter((table[int(index)][1] for index in indices), dtype=np.int64, count=sources)
        valid &= local_v
        mass += local_m
    return valid, mass


def assert_k1_predecessor_control() -> None:
    table = predecessor_table()
    masses = [m for _, m in table]
    if min(masses) != 0 or max(masses) <= 0:
        raise AssertionError("R1 predecessor table has malformed residual masses")


def fraction_json(value: Fraction) -> dict[str, int]:
    return {"numerator": value.numerator, "denominator": value.denominator}


def mean_metric(rows: Sequence[Pair], responses: Mapping[Pair, Mapping[int, Mapping[str, int]]], k: int, metric: str) -> Fraction:
    if not rows:
        raise AssertionError("empty group in matched contrast")
    return Fraction(sum(responses[p][k][metric] for p in rows), len(rows))


def delta_for(rows_h: Sequence[Pair], rows_c: Sequence[Pair], responses: Mapping[Pair, Mapping[int, Mapping[str, int]]], k: int, metric: str) -> Fraction:
    h = mean_metric(rows_h, responses, k, metric)
    c = mean_metric(rows_c, responses, k, metric)
    return (h - c) if metric in ("V", "R") else (c - h)


def sign_name(value: Fraction) -> str:
    return "positive" if value > 0 else "negative" if value < 0 else "zero"


def label_partition(rows: Sequence[PairInfo], labels: Sequence[int]) -> tuple[list[Pair], list[Pair]]:
    if len(rows) != len(labels):
        raise AssertionError("label vector length mismatch")
    h = [row.pair for row, label in zip(rows, labels) if label]
    c = [row.pair for row, label in zip(rows, labels) if not label]
    if not h or not c:
        raise AssertionError("placebo destroyed one side of a matched class")
    return h, c


def actual_class_labels(rows: Sequence[PairInfo]) -> tuple[int, ...]:
    return tuple(int(row.homologous) for row in rows)


def orbit_rotated_pair_labels(rows: Sequence[PairInfo], n: int, r: int) -> tuple[int, ...]:
    """B1 orbit-coherent label rotation expanded back to canonical pair order."""
    row_list = list(rows)
    row_by_pair = {row.pair: row for row in row_list}
    orbits = class_orbits(row_list, n)
    labels = tuple(int(row_by_pair[orbit[0]].homologous) for orbit in orbits)
    rotated = rotate_tuple(labels, r)
    label_by_pair: dict[Pair, int] = {}
    for orbit, label in zip(orbits, rotated):
        for pair in orbit:
            label_by_pair[pair] = label
    return tuple(label_by_pair[row.pair] for row in row_list)


def global_placebo_labelings(classes: Mapping[tuple[int, ...], Sequence[PairInfo]], n: int) -> list[dict[tuple[int, ...], tuple[int, ...]]]:
    counts = [len(class_orbits(rows, n)) for rows in classes.values()]
    lcm = math.lcm(*counts) if counts else 1
    actual = tuple((key, actual_class_labels(rows)) for key, rows in classes.items())
    seen: set[tuple] = set()
    out: list[dict[tuple[int, ...], tuple[int, ...]]] = []
    for r in range(1, lcm):
        assignment = tuple((key, orbit_rotated_pair_labels(rows, n, r)) for key, rows in classes.items())
        if assignment == actual or assignment in seen:
            continue
        seen.add(assignment)
        out.append(dict(assignment))
    return out


def class_contrasts(classes: Mapping[tuple[int, ...], Sequence[PairInfo]], responses: Mapping[Pair, Mapping[int, Mapping[str, int]]], k: int, n: int, labels: Mapping[tuple[int, ...], Sequence[int]] | None = None) -> tuple[list[dict], bool]:
    entries = []
    all_nonnegative = True
    any_strict = False
    for key, rows in classes.items():
        use_labels = tuple(labels[key]) if labels is not None else actual_class_labels(rows)
        h, c = label_partition(rows, use_labels)
        deltas = {metric: delta_for(h, c, responses, k, metric) for metric in METRICS}
        all_nonnegative &= all(v >= 0 for v in deltas.values())
        any_strict |= any(v > 0 for v in deltas.values())
        orbits = class_orbits(rows, n)
        label_by_pair = {row.pair: int(label) for row, label in zip(rows, use_labels)}
        # B1 guarantees one label per joint-shift orbit; count orbit labels from
        # canonical representatives for both actual and placebo assignments.
        h_orbits = sum(label_by_pair[orbit[0]] for orbit in orbits)
        c_orbits = len(orbits) - h_orbits
        tag_rows = {}
        if labels is None:
            for tag, pred in {
                "shift_capable": lambda row: row.shift_capable,
                "reflection_only": lambda row: row.reflection_only,
                "both": lambda row: row.both,
            }.items():
                tagged = [row.pair for row in rows if row.homologous and pred(row)]
                if tagged:
                    td = {metric: delta_for(tagged, c, responses, k, metric) for metric in METRICS}
                    tag_rows[tag] = {
                        "homologous_count": len(tagged),
                        "control_count": len(c),
                        "deltas": {metric: fraction_json(td[metric]) for metric in METRICS},
                        "signs": {metric: sign_name(td[metric]) for metric in METRICS},
                    }
        entries.append({
            "descriptor": list(key),
            "homologous_count": len(h),
            "control_count": len(c),
            "homologous_orbits": int(h_orbits),
            "control_orbits": int(c_orbits),
            "deltas": {metric: fraction_json(deltas[metric]) for metric in METRICS},
            "signs": {metric: sign_name(deltas[metric]) for metric in METRICS},
            **({"tag_split": tag_rows} if labels is None else {}),
        })
    return entries, bool(all_nonnegative and any_strict)


def pair_weighted_contrasts(classes: Mapping[tuple[int, ...], Sequence[PairInfo]], responses: Mapping[Pair, Mapping[int, Mapping[str, int]]], k: int, labels: Mapping[tuple[int, ...], Sequence[int]] | None = None) -> dict[str, Fraction]:
    h_all: list[Pair] = []
    c_all: list[Pair] = []
    for key, rows in classes.items():
        use_labels = tuple(labels[key]) if labels is not None else actual_class_labels(rows)
        h, c = label_partition(rows, use_labels)
        h_all.extend(h)
        c_all.extend(c)
    return {metric: delta_for(h_all, c_all, responses, k, metric) for metric in METRICS}


def tag_summary(classes: Mapping[tuple[int, ...], Sequence[PairInfo]], responses: Mapping[Pair, Mapping[int, Mapping[str, int]]], k: int) -> dict[str, dict]:
    """Pair-weighted tag splits against controls from the same eligible classes."""
    result = {}
    predicates = {
        "shift_capable": lambda row: row.shift_capable,
        "reflection_only": lambda row: row.reflection_only,
        "both": lambda row: row.both,
    }
    for name, pred in predicates.items():
        h_all: list[Pair] = []
        c_all: list[Pair] = []
        class_count = 0
        for rows in classes.values():
            tagged = [row.pair for row in rows if row.homologous and pred(row)]
            if not tagged:
                continue
            controls = [row.pair for row in rows if not row.homologous]
            h_all.extend(tagged)
            c_all.extend(controls)
            class_count += 1
        if not h_all:
            result[name] = {"scored_class_count": 0, "homologous_count": 0, "control_count": 0, "deltas": None}
            continue
        deltas = {metric: delta_for(h_all, c_all, responses, k, metric) for metric in METRICS}
        result[name] = {
            "scored_class_count": class_count,
            "homologous_count": len(h_all),
            "control_count": len(c_all),
            "deltas": {m: fraction_json(v) for m, v in deltas.items()},
            "signs": {m: sign_name(v) for m, v in deltas.items()},
        }
    return result


def descriptive_average(pairs: Sequence[Pair], responses: Mapping[Pair, Mapping[int, Mapping[str, int]]]) -> dict[str, dict[str, dict[str, int]]]:
    out = {}
    for k in HORIZONS:
        out[str(k)] = {
            metric: fraction_json(Fraction(sum(responses[p][k][metric] for p in pairs), len(pairs)))
            for metric in METRICS
        }
    return out


def independent_replay_all(n: int, pairs: Sequence[Pair], packed: Mapping[Pair, Mapping[int, Mapping[str, int]]]) -> dict[str, object]:
    return_witnesses = []
    for pair in pairs:
        scalar = scalar_response(n, pair)
        if scalar != packed[pair]:
            raise AssertionError(("packed/scalar response mismatch", n, pair, packed[pair], scalar))
        for k in HORIZONS:
            if scalar[k]["R"]:
                return_witnesses.append({
                    "pair": [format(pair.a, f"0{n}b"), format(pair.b, f"0{n}b")],
                    "return_horizon": k,
                    "validity_history": [scalar[j]["V"] for j in range(1, k + 1)],
                })
                break
    return {
        "pairs_replayed": len(pairs),
        "all_packed_scalar_metrics_equal": True,
        "return_witnesses": return_witnesses,
    }


def evaluate_ring(n: int) -> dict[str, object]:
    classes = scored_classes(n)
    primary_rows = [row for rows in classes.values() for row in rows]
    primary_pairs = [row.pair for row in primary_rows]
    literal_pairs = [Pair(a, a) for a in range(1 << n)]
    complement_pairs = [Pair(a, ((1 << n) - 1) ^ a) for a in range(1 << n)]
    all_pairs = sorted(set(primary_pairs + literal_pairs + complement_pairs))
    responses = packed_responses(n, all_pairs)

    # R1 exact predecessor control over every exhaustive source pair at k=1.
    exhaustive_pairs = [Pair(a, b) for a in range(1 << n) for b in range(1 << n)]
    exhaustive = packed_responses(n, exhaustive_pairs, max_horizon=1)
    a = row_words([p.a for p in exhaustive_pairs], n)
    b = row_words([p.b for p in exhaustive_pairs], n)
    table_v, table_m = pair_k1_from_predecessor_table(a, b)
    for i, pair in enumerate(exhaustive_pairs):
        if exhaustive[pair][1]["V"] != int(table_v[i]) or exhaustive[pair][1]["M"] != int(table_m[i]):
            raise AssertionError(("R1 k=1 predecessor-table mismatch", n, pair))

    exact_replay = independent_replay_all(n, all_pairs, responses)
    horizons = {}
    placebos = global_placebo_labelings(classes, n)
    source_placebo = global_placebo_assignments(classes, n)
    if len(placebos) != int(source_placebo["distinct_nonidentity_assignments"]):
        raise AssertionError(("B1 placebo assignment count mismatch", n, len(placebos), source_placebo))
    for k in HORIZONS:
        entries, strict = class_contrasts(classes, responses, k, n)
        weighted = pair_weighted_contrasts(classes, responses, k)
        placebo_strict = 0
        placebo_weighted: dict[str, list[Fraction]] = {m: [] for m in METRICS}
        for assignment in placebos:
            _, p_strict = class_contrasts(classes, responses, k, n, assignment)
            placebo_strict += int(p_strict)
            p_weighted = pair_weighted_contrasts(classes, responses, k, assignment)
            for metric in METRICS:
                placebo_weighted[metric].append(p_weighted[metric])
        ranks = {}
        for metric in METRICS:
            vals = placebo_weighted[metric]
            ranks[metric] = {
                "placebos_at_or_below_actual": sum(v <= weighted[metric] for v in vals),
                "placebo_count": len(vals),
            }
        sign_counts = {
            metric: {
                sign: sum(row["signs"][metric] == sign for row in entries)
                for sign in ("positive", "zero", "negative")
            }
            for metric in METRICS
        }
        horizons[str(k)] = {
            "classes": entries,
            "sign_counts": sign_counts,
            "strict_primary_predicate": strict,
            "pair_weighted_deltas": {m: fraction_json(v) for m, v in weighted.items()},
            "tag_split": tag_summary(classes, responses, k),
            "placebo": {
                "distinct_assignments": len(placebos),
                "strict_pass_count": placebo_strict,
                "strict_pass_fraction": fraction_json(Fraction(placebo_strict, len(placebos))) if placebos else fraction_json(Fraction(0, 1)),
                "pair_weighted_actual_rank": ranks,
            },
        }

    ring7_dynamic_passes = [k for k in (2, 3, 4) if horizons[str(k)]["strict_primary_predicate"]]
    r4 = None
    if n == 7 and ring7_dynamic_passes:
        r4 = all(
            Fraction(
                horizons[str(k)]["placebo"]["strict_pass_fraction"]["numerator"],
                horizons[str(k)]["placebo"]["strict_pass_fraction"]["denominator"],
            ) < Fraction(1, 10)
            for k in ring7_dynamic_passes
        )
    return {
        "ring": n,
        "source_census": {
            "scored_class_count": len(classes),
            "homologous_pairs": sum(row.homologous for row in primary_rows),
            "control_pairs": sum(not row.homologous for row in primary_rows),
        },
        "horizons": horizons,
        "descriptive_literal_self": descriptive_average(literal_pairs, responses),
        "descriptive_complement": descriptive_average(complement_pairs, responses),
        "independent_scalar_replay": exact_replay,
        "predictions": {
            "R2_dynamic_strict_pass_horizons": ring7_dynamic_passes if n == 7 else None,
            "R2_at_least_one_k2_to_k4": bool(ring7_dynamic_passes) if n == 7 else None,
            "R4_placebo_selectivity_when_applicable": r4,
            "R5_return_witnesses_replay_prior_invalid_then_valid": all(
                0 in w["validity_history"][:-1] and w["validity_history"][-1] == 1
                for w in exact_replay["return_witnesses"]
            ),
        },
    }


def evaluate() -> dict[str, object]:
    source_census = assert_frozen_census()
    assert_k1_predecessor_control()
    rings = {str(n): evaluate_ring(n) for n in RINGS}
    return {
        "protocol": "dimensional-resonance-response-20260912",
        "schema": 1,
        "reviewed_gate1_head": "15787fa8a2671f899e1d974aff8753386e423cfc",
        "source_hashes": {
            "script": sha(pathlib.Path(__file__)),
            "protocol": sha(PROTOCOL),
            "gate1_refreeze": sha(REFREEZE),
            "gate1_null_clarification": sha(CLARIFICATION),
            "gate1_approval": sha(APPROVAL),
            "source_census_script": sha(SOURCE_SCRIPT),
            "physical_predecessor_script": sha(PHYSICAL_SCRIPT),
        },
        "parameters": {
            "rings": list(RINGS),
            "horizons": list(HORIZONS),
            "causal_window": "all 2n columns and rows [-2k, 3+2k]",
            "residual_span": "inclusive y_max-y_min+1; empty=0",
            "primary_relation": "nonliteral dihedral transformed homologues",
            "placebo": "joint-shift-orbit-coherent common cyclic rotation with global deduplication",
            "response_sign": "mutual transparency",
        },
        "controls": {
            "source_census_matches_gate1_freeze": {str(n): {"scored_classes": source_census[n]["scored_class_count"], "homologous_pairs": source_census[n]["homologous_pairs"], "control_pairs": source_census[n]["control_pairs"]} for n in RINGS},
            "R1_local_valid_words_17_of_64": True,
            "k1_physical_validity_and_mass_match_predecessor_table_exhaustively": True,
            "packed_scalar_response_paths_agree_for_all_scored_and_descriptive_pairs": True,
        },
        "rings": rings,
        "predictions": {
            "R2_ring7_transformed_homologue_response": rings["7"]["predictions"]["R2_at_least_one_k2_to_k4"],
            "R4_ring7_placebo_selectivity": rings["7"]["predictions"]["R4_placebo_selectivity_when_applicable"],
            "R5_return_replay": all(rings[str(n)]["predictions"]["R5_return_witnesses_replay_prior_invalid_then_valid"] for n in RINGS),
        },
        "scope": "finite n=6,7 touching-strip response to an analyst-supplied transformed-homology relation; not consciousness, semantic self-recognition, endogenous control, self-assembly, intrinsic dimension, spacetime/physics, metaphysics, Class IV/universality, or primes/8n+1",
    }


def self_test() -> None:
    """Out-of-domain physical/observable check; no frozen n=6,7 response is scored."""
    before = sha(OUT) if OUT.exists() else None
    assert_frozen_census()  # approved source-only combinatorics; no physical response
    assert_k1_predecessor_control()
    n = 3
    pairs = [Pair(0b001, 0b010), Pair(0b011, 0b101), Pair(0b110, 0b001)]
    packed = packed_responses(n, pairs, max_horizon=2)
    a = row_words([p.a for p in pairs], n)
    b = row_words([p.b for p in pairs], n)
    table_v, table_m = pair_k1_from_predecessor_table(a, b)
    for i, pair in enumerate(pairs):
        scalar = scalar_response(n, pair, max_horizon=2)
        assert scalar == packed[pair]
        assert packed[pair][1]["V"] == int(table_v[i])
        assert packed[pair][1]["M"] == int(table_m[i])
        assert packed[pair][1]["R"] == 0
        assert packed[pair][1]["S"] >= 0

    # Synthetic exact-rational class/placebo exercise, independent of the frozen
    # n=6,7 source census.
    descriptor = (0, 0, 0, 0, 0, 0)
    h_pairs = (Pair(1, 2), Pair(2, 4), Pair(4, 1))
    c_pairs = (Pair(0, 1), Pair(0, 2), Pair(0, 4))
    rows = [
        *(PairInfo(pair, descriptor, True, True, False, False) for pair in h_pairs),
        *(PairInfo(pair, descriptor, False, False, False, False) for pair in c_pairs),
    ]
    responses = {
        **{pair: {1: {"V": 1, "M": 0, "S": 0, "R": 0}} for pair in h_pairs},
        **{pair: {1: {"V": 0, "M": 2, "S": 1, "R": 0}} for pair in c_pairs},
    }
    entries, strict = class_contrasts({descriptor: rows}, responses, 1, 3)
    assert strict
    assert entries[0]["signs"]["V"] == "positive"
    assert entries[0]["signs"]["M"] == "positive"
    assert entries[0]["signs"]["S"] == "positive"
    assert entries[0]["signs"]["R"] == "zero"
    after = sha(OUT) if OUT.exists() else None
    assert after == before, "self-test must not create or modify canonical result"
    print("dimensional-resonance physical verifier self-test passed (out-of-domain n=3; no canonical result written)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true", help="out-of-domain implementation test only")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    result = evaluate()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result["predictions"], sort_keys=True))
    print("written", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
