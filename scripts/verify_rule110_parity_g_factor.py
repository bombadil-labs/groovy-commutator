#!/usr/bin/env python3
"""Post-hoc exact mechanism audit for the matched Rule-62/Rule-110 result.

For Rule 110, verify on the complete 10-bit local source domain that the next
block-parity bit after H^2 is a radius-one factor of the macro symbols
(P_j, G_{2j}, G_{2j+1}). Also find the minimum feature-cardinality subset on
that admissible domain.

For Rule 62, preserve both a local radius-one conflict and the whole-ring
(P,G)-equal / next-P-different witness from the primary matched experiment.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

OUT = Path("results/rule110_parity_g_factor_20261007.json")
FEATURES = ["P-1", "G-2", "G-1", "P0", "G0", "G1", "P1", "G2", "G3"]


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
    parity = bit(bits, lo, a) ^ bit(bits, lo, a + 1)
    return parity, g_at(rule, bits, lo, a), g_at(rule, bits, lo, a + 1)


def target(rule: int, bits: list[int], lo: int) -> int:
    hp = {q: h_at(rule, bits, lo, q) for q in (-1, 0, 1, 2)}
    h20 = f(rule, hp[-1], hp[0], hp[1])
    h21 = f(rule, hp[0], hp[1], hp[2])
    return h20 ^ h21


def local_dataset(rule: int) -> list[tuple[int, tuple[int, ...], int]]:
    # Radius-one macro factor uses blocks -1,0,1. G has radius two, so
    # source positions -4..5 (10 bits) are the complete local domain.
    lo = -4
    rows = []
    for word in range(1 << 10):
        bits = [(word >> i) & 1 for i in range(10)]
        features = tuple(
            value
            for j in (-1, 0, 1)
            for value in macro_symbol(rule, bits, lo, j)
        )
        rows.append((word, features, target(rule, bits, lo)))
    return rows


def factor(rows: list[tuple[int, tuple[int, ...], int]], subset: tuple[int, ...]) -> dict:
    table: dict[tuple[int, ...], tuple[int, int]] = {}
    for word, features, y in rows:
        key = tuple(features[i] for i in subset)
        if key in table and table[key][0] != y:
            prev_y, prev_word = table[key]
            return {
                "pass": False,
                "distinct_contexts_before_conflict": len(table),
                "conflict": {
                    "previous_word": prev_word,
                    "word": word,
                    "context": list(key),
                    "previous_target": prev_y,
                    "target": y,
                },
            }
        table[key] = (y, word)
    return {
        "pass": True,
        "distinct_contexts": len(table),
        "conflict": None,
    }


def step_state(rule: int, state: int, n: int) -> int:
    out = 0
    for i in range(n):
        l = (state >> ((i - 1) % n)) & 1
        c = (state >> i) & 1
        r = (state >> ((i + 1) % n)) & 1
        out |= f(rule, l, c, r) << i
    return out


def parity_state(state: int, n: int) -> int:
    out = 0
    for j in range(n // 2):
        out |= (((state >> (2 * j)) & 1) ^ ((state >> (2 * j + 1)) & 1)) << j
    return out


def centered_g_state(rule: int, state: int, n: int) -> int:
    h = step_state(rule, state, n)
    h2 = step_state(rule, h, n)
    d = state ^ h
    raw = h ^ h2 ^ step_state(rule, d, n)
    h0 = step_state(rule, 0, n)
    return raw ^ h0


def global_witness(rule: int, n: int, x: int, y: int) -> dict:
    hx = step_state(rule, x, n)
    hy = step_state(rule, y, n)
    return {
        "n": n,
        "source_x": x,
        "source_y": y,
        "same_current_parity": parity_state(x, n) == parity_state(y, n),
        "current_parity": parity_state(x, n),
        "same_centered_G": centered_g_state(rule, x, n) == centered_g_state(rule, y, n),
        "centered_G": centered_g_state(rule, x, n),
        "next_parity_x": parity_state(step_state(rule, hx, n), n),
        "next_parity_y": parity_state(step_state(rule, hy, n), n),
    }


def main() -> None:
    rows110 = local_dataset(110)
    rows62 = local_dataset(62)

    full_subset = tuple(range(9))
    r110 = factor(rows110, full_subset)
    r62 = factor(rows62, full_subset)

    minima = []
    for size in range(1, 10):
        for subset in itertools.combinations(range(9), size):
            if factor(rows110, subset)["pass"]:
                minima.append(subset)
        if minima:
            break

    result = {
        "schema": "rule110-parity-g-factor-v1",
        "date": "2026-10-07",
        "provenance": "post-hoc mechanism audit after matched-history result",
        "rule110": {
            "radius1_macro_factor": r110,
            "source_words_checked": 1024,
            "macro_feature_names": FEATURES,
            "minimum_feature_count": len(minima[0]),
            "minimum_subsets": [
                [FEATURES[i] for i in subset] for subset in minima
            ],
            "minimum_subset_factor": factor(rows110, minima[0]),
        },
        "rule62": {
            "radius1_macro_factor": r62,
            "global_witnesses": [
                global_witness(62, 16, 60, 204),
                global_witness(62, 18, 60, 204),
            ],
        },
    }

    result["summary"] = {
        "rule110_radius1_factor_pass": r110["pass"],
        "rule110_unique_minimum_feature_count": len(minima[0]),
        "rule110_number_of_minimum_subsets": len(minima),
        "rule62_radius1_factor_pass": r62["pass"],
        "rule62_global_witness_pass": all(
            w["same_current_parity"]
            and w["same_centered_G"]
            and w["next_parity_x"] != w["next_parity_y"]
            for w in result["rule62"]["global_witnesses"]
        ),
    }
    result["source_hashes"] = {
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result["summary"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
