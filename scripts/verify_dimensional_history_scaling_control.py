#!/usr/bin/env python3
"""Theorem-control verifier for dimensional history scaling.

Governing protocol:
  docs/research/protocols/dimensional-history-scaling-gate1-refreeze-20260912.md

Renewed Gate 1: Claude Code / Fable 5.1 approved exact gathering head
74393d18a33c51cfff133c88e09a40a2a3018cf6 before this implementation.

Normal execution evaluates only the frozen six (d,n) controls and writes the
canonical result. ``--self-test`` uses the out-of-domain odd ring n=3 and does
not write a result.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
from itertools import product

ROOT = pathlib.Path(__file__).resolve().parents[1]
PARENT_PROTOCOL = ROOT / "docs/research/protocols/dimensional-history-scaling-20260912.md"
REFREEZE = ROOT / "docs/research/protocols/dimensional-history-scaling-gate1-refreeze-20260912.md"
OUT = ROOT / "results/dimensional_history_scaling_control_20260912.json"
DIMS = (1, 2, 3)
SIZES = (5, 7)
H_MAX = 8


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def coord_to_index(coord: tuple[int, ...], n: int) -> int:
    out = 0
    for x in coord:
        out = out * n + x
    return out


def index_to_coord(index: int, d: int, n: int) -> tuple[int, ...]:
    out = [0] * d
    for axis in range(d - 1, -1, -1):
        out[axis] = index % n
        index //= n
    return tuple(out)


def apply_rule90_axis(column: int, d: int, n: int, axis: int) -> int:
    """Apply one literal Rule-90 axis pass to a packed column state."""
    out = 0
    x = column
    while x:
        lsb = x & -x
        site = lsb.bit_length() - 1
        coord = list(index_to_coord(site, d, n))
        for delta in (-1, 1):
            moved = coord.copy()
            moved[axis] = (moved[axis] + delta) % n
            out ^= 1 << coord_to_index(tuple(moved), n)
        x ^= lsb
    return out


def build_ordered_axis_rows(d: int, n: int) -> tuple[int, ...]:
    """Build F_d by explicit ordered Rule-90 passes, then return its GF(2) rows."""
    total = n**d
    columns: list[int] = []
    for source in range(total):
        state = 1 << source
        for axis in range(d):
            state = apply_rule90_axis(state, d, n, axis)
        columns.append(state)

    rows = [0] * total
    for source, column in enumerate(columns):
        x = column
        while x:
            lsb = x & -x
            target = lsb.bit_length() - 1
            rows[target] |= 1 << source
            x ^= lsb
    return tuple(rows)


def row_times_matrix(row: int, matrix_rows: tuple[int, ...]) -> int:
    out = 0
    x = row
    while x:
        lsb = x & -x
        out ^= matrix_rows[lsb.bit_length() - 1]
        x ^= lsb
    return out


def reduce_against_basis(value: int, basis: dict[int, int]) -> int:
    out = value
    for pivot in sorted(basis, reverse=True):
        if (out >> pivot) & 1:
            out ^= basis[pivot]
    return out


def add_to_basis(value: int, basis: dict[int, int]) -> bool:
    value = reduce_against_basis(value, basis)
    if value == 0:
        return False
    pivot = value.bit_length() - 1
    for other in list(basis):
        if (basis[other] >> pivot) & 1:
            basis[other] ^= value
    basis[pivot] = value
    return True


def slice_rows(d: int, n: int) -> tuple[int, ...]:
    rows = []
    for prefix in product(range(n), repeat=d - 1):
        rows.append(1 << coord_to_index(tuple(prefix) + (0,), n))
    return tuple(rows)


def matrix_history_control(d: int, n: int, h_max: int = H_MAX) -> dict:
    """Primary packed GF(2) row-span path for the protocol's exact criterion."""
    matrix = build_ordered_axis_rows(d, n)
    current = slice_rows(d, n)
    basis: dict[int, int] = {}
    ranks: list[int] = []
    closes: list[bool] = []

    for _h in range(h_max + 1):
        for row in current:
            add_to_basis(row, basis)
        ranks.append(len(basis))
        nxt = tuple(row_times_matrix(row, matrix) for row in current)
        closes.append(all(reduce_against_basis(row, basis) == 0 for row in nxt))
        current = nxt

    h_min = next((h for h, closed in enumerate(closes) if closed), None)
    return {
        "rank_H_0_through_H_max": ranks,
        "closure_by_h": closes,
        "h_min": h_min,
        "state_bits": n**d,
        "slice_bits": n ** (d - 1),
    }


def rotate_polynomial(word: int, n: int, shift: int) -> int:
    mask = (1 << n) - 1
    shift %= n
    if shift == 0:
        return word & mask
    return ((word << shift) | (word >> (n - shift))) & mask


def multiply_by_g(word: int, n: int) -> int:
    """Independent 1D polynomial action by g=x+x^-1 modulo x^n-1."""
    return rotate_polynomial(word, n, 1) ^ rotate_polynomial(word, n, -1)


def transverse_minimal_polynomial_degree(n: int) -> dict:
    """Find D(n) from 1,g,g^2,... by 1D polynomial/basis action only."""
    basis: dict[int, int] = {}
    powers: list[int] = []
    power = 1
    for degree in range(n + 2):
        if reduce_against_basis(power, basis) == 0:
            return {
                "D": degree,
                "independent_power_words": [format(x, f"0{n}b") for x in powers],
            }
        powers.append(power)
        add_to_basis(power, basis)
        power = multiply_by_g(power, n)
    raise AssertionError(("minimal polynomial degree not found", n))


def evaluate(sizes: tuple[int, ...] = SIZES, dims: tuple[int, ...] = DIMS, *, canonical: bool = True) -> dict:
    transverse = {n: transverse_minimal_polynomial_degree(n) for n in sizes}
    cells = []
    for n in sizes:
        predicted_h = transverse[n]["D"] - 1
        for d in dims:
            matrix = matrix_history_control(d, n)
            cells.append({
                "d": d,
                "n": n,
                "matrix": matrix,
                "D_n": transverse[n]["D"],
                "theorem_h_min": predicted_h,
                "matrix_matches_theorem": matrix["h_min"] == predicted_h,
            })

    fixed_n_equal = {
        str(n): len({row["matrix"]["h_min"] for row in cells if row["n"] == n}) == 1
        for n in sizes
    }
    all_match = all(row["matrix_matches_theorem"] for row in cells)
    result = {
        "protocol": "dimensional-history-scaling-product-law-control-20260912",
        "schema": 1,
        "source_hashes": ({
            "script": sha(pathlib.Path(__file__)),
            "parent_protocol": sha(PARENT_PROTOCOL),
            "gate1_refreeze": sha(REFREEZE),
        } if canonical else {}),
        "parameters": {
            "dimensions": list(dims),
            "side_lengths": list(sizes),
            "source_rule": 90,
            "observation": "newest-axis coordinate-zero complete slice",
            "H_max": H_MAX,
            "criterion": "ker(H_h) subseteq ker(O F^(h+1))",
        },
        "transverse_reference": {str(n): transverse[n] for n in sizes},
        "cells": cells,
        "controls": {
            "matrix_matches_polynomial_theorem_all_cells": all_match,
            "h_min_dimension_independent_at_fixed_n": fixed_n_equal,
        },
        "expected_frozen_values": ({
            "D_5": transverse.get(5, {}).get("D"),
            "D_7": transverse.get(7, {}).get("D"),
            "h_min_n5": transverse.get(5, {}).get("D", 0) - 1 if 5 in transverse else None,
            "h_min_n7": transverse.get(7, {}).get("D", 0) - 1 if 7 in transverse else None,
        } if canonical else {}),
        "scope": "negative design theorem/control for product-form linear ordered-axis Rule90 under coordinate-slice observation; not a test or refutation of general history/dimension scaling",
    }
    if canonical:
        if transverse[5]["D"] != 3 or transverse[7]["D"] != 4:
            raise AssertionError("frozen minimal-polynomial control failed")
        if not all_match or not all(fixed_n_equal.values()):
            raise AssertionError("frozen product-law dimension-blind theorem regression failed")
    return result


def self_test() -> None:
    # n=3 is deliberately outside the frozen source domain.
    result = evaluate((3,), (1, 2), canonical=False)
    if result["transverse_reference"]["3"]["D"] != 2:
        raise AssertionError("out-of-domain polynomial self-test failed")
    if not result["controls"]["matrix_matches_polynomial_theorem_all_cells"]:
        raise AssertionError("out-of-domain independent paths disagree")
    if not result["controls"]["h_min_dimension_independent_at_fixed_n"]["3"]:
        raise AssertionError("out-of-domain dimension-blind control failed")
    if OUT.exists():
        raise AssertionError("implementation-only self-test found canonical result")
    print("dimensional-history-scaling implementation self-test passed on out-of-domain n=3; no canonical result written")


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
        "h_min": {f"d{row['d']}/n{row['n']}": row["matrix"]["h_min"] for row in result["cells"]},
        "D": {n: row["D"] for n, row in result["transverse_reference"].items()},
        "controls": result["controls"],
    }, sort_keys=True))
    print("written", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
