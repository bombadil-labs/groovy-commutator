#!/usr/bin/env python3
"""Exact Rule-110 parity+Groovy closure and parity-readout algebra audit.

Protocol:
  docs/research/protocols/rule110-pg-closure-20261007.md
"""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

OUT = Path("results/rule110_pg_closure_20261007.json")
RULE = 110
FEATURE_NAMES = ["P-1", "G-1", "P0", "G0", "G1", "P1", "G2"]


def f(rule: int, l: int, c: int, r: int) -> int:
    return (rule >> ((l << 2) | (c << 1) | r)) & 1


def bit(bits: list[int], lo: int, p: int) -> int:
    return bits[p - lo]


def h_at(rule: int, bits: list[int], lo: int, p: int) -> int:
    return f(rule, bit(bits, lo, p - 1), bit(bits, lo, p), bit(bits, lo, p + 1))


def g_at(rule: int, bits: list[int], lo: int, p: int) -> int:
    hp = {q: h_at(rule, bits, lo, q) for q in (p - 1, p, p + 1)}
    h2 = f(rule, hp[p - 1], hp[p], hp[p + 1])
    d = {q: bit(bits, lo, q) ^ hp[q] for q in (p - 1, p, p + 1)}
    hd = f(rule, d[p - 1], d[p], d[p + 1])
    return hp[p] ^ h2 ^ hd ^ (rule & 1)


def macro_symbol(rule: int, bits: list[int], lo: int, j: int) -> tuple[int, int, int]:
    a = 2 * j
    return (
        bit(bits, lo, a) ^ bit(bits, lo, a + 1),
        g_at(rule, bits, lo, a),
        g_at(rule, bits, lo, a + 1),
    )


def current_context(rule: int, bits: list[int], lo: int, radius: int) -> tuple[int, ...]:
    return tuple(
        value
        for j in range(-radius, radius + 1)
        for value in macro_symbol(rule, bits, lo, j)
    )


def second_state(rule: int, bits: list[int], lo: int) -> dict[int, int]:
    # Enough H^2 cells to evaluate next P and next G at source sites 0 and 1.
    h1 = {p: h_at(rule, bits, lo, p) for p in range(-3, 5)}
    return {
        p: f(rule, h1[p - 1], h1[p], h1[p + 1])
        for p in range(-2, 4)
    }


def g_from_dict(rule: int, state: dict[int, int], p: int) -> int:
    hp = {
        q: f(rule, state[q - 1], state[q], state[q + 1])
        for q in (p - 1, p, p + 1)
    }
    h2 = f(rule, hp[p - 1], hp[p], hp[p + 1])
    d = {q: state[q] ^ hp[q] for q in (p - 1, p, p + 1)}
    hd = f(rule, d[p - 1], d[p], d[p + 1])
    return hp[p] ^ h2 ^ hd ^ (rule & 1)


def next_augmented(rule: int, bits: list[int], lo: int) -> tuple[int, int, int]:
    h2 = second_state(rule, bits, lo)
    return (
        h2[0] ^ h2[1],
        g_from_dict(rule, h2, 0),
        g_from_dict(rule, h2, 1),
    )


def radius_factor(radius: int) -> dict:
    lo = -2 * radius - 2
    width = 4 * radius + 6
    table: dict[tuple[int, ...], tuple[tuple[int, int, int], int]] = {}
    for word in range(1 << width):
        bits = [(word >> i) & 1 for i in range(width)]
        key = current_context(RULE, bits, lo, radius)
        target = next_augmented(RULE, bits, lo)
        previous = table.get(key)
        if previous is not None and previous[0] != target:
            return {
                "radius": radius,
                "pass": False,
                "source_width": width,
                "contexts_before_conflict": len(table),
                "conflict": {
                    "word_x": previous[1],
                    "word_y": word,
                    "current_context": list(key),
                    "next_augmented_x": list(previous[0]),
                    "next_augmented_y": list(target),
                },
            }
        table[key] = (target, word)
    return {
        "radius": radius,
        "pass": True,
        "source_width": width,
        "distinct_contexts": len(table),
        "conflict": None,
    }


# Infinite-line certificate -------------------------------------------------

def x_inf(i: int) -> int:
    return int(i <= -2 or i == 0)


def y_inf(i: int) -> int:
    return int(i in (-1, 1))


def h_conf(conf, p: int) -> int:
    return f(RULE, conf(p - 1), conf(p), conf(p + 1))


def g_conf(conf, p: int) -> int:
    hp = {q: h_conf(conf, q) for q in (p - 1, p, p + 1)}
    h2 = f(RULE, hp[p - 1], hp[p], hp[p + 1])
    d = {q: conf(q) ^ hp[q] for q in (p - 1, p, p + 1)}
    hd = f(RULE, d[p - 1], d[p], d[p + 1])
    return hp[p] ^ h2 ^ hd ^ (RULE & 1)


def z_conf(conf, j: int) -> tuple[int, int, int]:
    a = 2 * j
    return (
        conf(a) ^ conf(a + 1),
        g_conf(conf, a),
        g_conf(conf, a + 1),
    )


def evolve_conf(conf):
    return lambda p: h_conf(conf, p)


def infinite_line_certificate() -> dict:
    # Outside these blocks both configurations are uniform-tail situations whose
    # macro symbol is exactly (0,0,0). Locality reduces equality of the entire
    # current Z field to this finite seam check.
    seam_js = list(range(-4, 5))
    current = [
        {
            "j": j,
            "x": list(z_conf(x_inf, j)),
            "y": list(z_conf(y_inf, j)),
        }
        for j in seam_js
    ]
    c2x = evolve_conf(evolve_conf(x_inf))
    c2y = evolve_conf(evolve_conf(y_inf))
    next_rows = [
        {
            "j": j,
            "x": list(z_conf(c2x, j)),
            "y": list(z_conf(c2y, j)),
        }
        for j in range(-4, 5)
    ]
    return {
        "x_definition": "x_i=1 iff i<=-2 or i=0",
        "y_definition": "y_i=1 iff i in {-1,1}",
        "uniform_tail_macro_symbol_zero": {
            "all_zero": list(z_conf(lambda _: 0, 0)),
            "all_one": list(z_conf(lambda _: 1, 0)),
        },
        "current_seam_check": current,
        "current_entire_Z_equal": all(row["x"] == row["y"] for row in current)
        and z_conf(lambda _: 0, 0) == z_conf(lambda _: 1, 0) == (0, 0, 0),
        "next_seam_check": next_rows,
        "next_center_x": list(z_conf(c2x, 0)),
        "next_center_y": list(z_conf(c2y, 0)),
        "next_center_differs": z_conf(c2x, 0) != z_conf(c2y, 0),
    }


# Seven-feature parity readout algebra -------------------------------------

def parity_dataset() -> dict[tuple[int, ...], int]:
    # The established unique seven-literal subset:
    # (P-1,G-1,P0,G0,G1,P1,G2).
    lo = -4
    out: dict[tuple[int, ...], int] = {}
    for word in range(1 << 10):
        bits = [(word >> i) & 1 for i in range(10)]
        full = current_context(RULE, bits, lo, 1)
        # Full order is P-1,G-2,G-1,P0,G0,G1,P1,G2,G3.
        key = tuple(full[i] for i in (0, 2, 3, 4, 5, 6, 7))
        target = next_augmented(RULE, bits, lo)[0]
        if key in out and out[key] != target:
            raise AssertionError("seven-feature parity factor unexpectedly conflicts")
        out[key] = target
    return out


def monomial_masks(max_degree: int) -> list[int]:
    masks = []
    for degree in range(max_degree + 1):
        for combo in itertools.combinations(range(7), degree):
            mask = 0
            for i in combo:
                mask |= 1 << i
            masks.append(mask)
    return masks


def monomial_value(point: tuple[int, ...], mask: int) -> int:
    return int(all(point[i] for i in range(7) if (mask >> i) & 1))


def gf2_solve(matrix: list[list[int]], rhs: list[int]):
    aug = [row[:] + [b] for row, b in zip(matrix, rhs)]
    m = len(aug)
    n = len(matrix[0]) if matrix else 0
    pivots: list[int] = []
    row = 0
    for col in range(n):
        pivot = next((r for r in range(row, m) if aug[r][col]), None)
        if pivot is None:
            continue
        aug[row], aug[pivot] = aug[pivot], aug[row]
        for r in range(m):
            if r != row and aug[r][col]:
                aug[r] = [a ^ b for a, b in zip(aug[r], aug[row])]
        pivots.append(col)
        row += 1
        if row == m:
            break

    for r in range(row, m):
        if not any(aug[r][:n]) and aug[r][n]:
            return None

    free = [c for c in range(n) if c not in pivots]
    particular = [0] * n
    for i, col in enumerate(pivots):
        particular[col] = aug[i][n]

    basis = []
    for fc in free:
        v = [0] * n
        v[fc] = 1
        for i, col in enumerate(pivots):
            if aug[i][fc]:
                v[col] = 1
        basis.append(v)

    return {
        "particular": particular,
        "basis": basis,
        "rank": len(pivots),
        "nullity": len(free),
    }


def term_name(mask: int) -> str:
    if mask == 0:
        return "1"
    return "*".join(
        FEATURE_NAMES[i] for i in range(7) if (mask >> i) & 1
    )


def parity_anf_audit() -> dict:
    data = parity_dataset()
    points = sorted(data.items())

    degree_rows = []
    first_solution = None
    first_masks = None
    first_degree = None
    for degree in range(8):
        masks = monomial_masks(degree)
        matrix = [
            [monomial_value(point, mask) for mask in masks]
            for point, _ in points
        ]
        rhs = [target for _, target in points]
        solution = gf2_solve(matrix, rhs)
        degree_rows.append({
            "degree": degree,
            "monomial_count": len(masks),
            "solvable": solution is not None,
            "rank": None if solution is None else solution["rank"],
            "nullity": None if solution is None else solution["nullity"],
        })
        if solution is not None and first_solution is None:
            first_solution = solution
            first_masks = masks
            first_degree = degree
            break

    assert first_solution is not None and first_masks is not None

    basis = first_solution["basis"]
    particular = first_solution["particular"]
    support_best = None
    best_vectors = []
    for choice in range(1 << len(basis)):
        vector = particular[:]
        for i, bvec in enumerate(basis):
            if (choice >> i) & 1:
                vector = [a ^ b for a, b in zip(vector, bvec)]
        support = sum(vector)
        if support_best is None or support < support_best:
            support_best = support
            best_vectors = [vector]
        elif support == support_best:
            best_vectors.append(vector)

    formulas = []
    for vector in best_vectors:
        terms = [
            term_name(first_masks[i])
            for i, coefficient in enumerate(vector)
            if coefficient
        ]
        formulas.append(terms)

    return {
        "admissible_context_count": len(data),
        "feature_names": FEATURE_NAMES,
        "degree_search": degree_rows,
        "minimum_degree": first_degree,
        "minimum_degree_rank": first_solution["rank"],
        "minimum_degree_solution_dimension": first_solution["nullity"],
        "minimum_support_at_minimum_degree": support_best,
        "minimum_support_solution_count": len(formulas),
        "minimum_support_anfs": formulas,
    }


def main() -> None:
    radius = [radius_factor(r) for r in (1, 2, 3)]
    infinite = infinite_line_certificate()
    anf = parity_anf_audit()

    result = {
        "schema": "rule110-pg-closure-v1",
        "date": "2026-10-07",
        "protocol": "docs/research/protocols/rule110-pg-closure-20261007.md",
        "gate_A_radius1": radius[0],
        "gate_B_bounded_radius": radius[1:],
        "posthoc_infinite_line_counterexample": infinite,
        "gate_C_literal_minimality": {
            "evaluated": False,
            "reason": "no full augmented closure at radii 1,2,3",
        },
        "gate_D_parity_readout_anf": anf,
        "summary": {
            "augmented_PG_autonomous": False,
            "radius1_pass": radius[0]["pass"],
            "radius2_pass": radius[1]["pass"],
            "radius3_pass": radius[2]["pass"],
            "infinite_line_same_current_Z_next_Z_differs":
                infinite["current_entire_Z_equal"] and infinite["next_center_differs"],
            "parity_readout_minimum_anf_degree": anf["minimum_degree"],
            "parity_readout_minimum_support": anf["minimum_support_at_minimum_degree"],
        },
    }
    result["source_hashes"] = {
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result["summary"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
