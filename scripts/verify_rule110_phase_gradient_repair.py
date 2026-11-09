#!/usr/bin/env python3
"""Post-hoc Rule-110 block-phase-gradient repair audit.

Candidate selected from the infinite parity+Groovy obstruction. This is a
mechanism audit, not a preregistered discriminator test.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

OUT = Path("results/rule110_phase_gradient_repair_20261007.json")
RULE = 110


def f(rule: int, l: int, c: int, r: int) -> int:
    return (rule >> ((l << 2) | (c << 1) | r)) & 1


def bit(bits: list[int], lo: int, p: int) -> int:
    return bits[p - lo]


def h_at(bits: list[int], lo: int, p: int) -> int:
    return f(RULE, bit(bits, lo, p - 1), bit(bits, lo, p), bit(bits, lo, p + 1))


def g_at(bits: list[int], lo: int, p: int) -> int:
    hp = {q: h_at(bits, lo, q) for q in (p - 1, p, p + 1)}
    h2 = f(RULE, hp[p - 1], hp[p], hp[p + 1])
    d = {q: bit(bits, lo, q) ^ hp[q] for q in (p - 1, p, p + 1)}
    hd = f(RULE, d[p - 1], d[p], d[p + 1])
    return hp[p] ^ h2 ^ hd ^ (RULE & 1)


def symbol(bits: list[int], lo: int, j: int) -> tuple[int, int, int, int]:
    a = 2 * j
    p = bit(bits, lo, a) ^ bit(bits, lo, a + 1)
    phi = bit(bits, lo, a) ^ bit(bits, lo, a + 2)
    return p, g_at(bits, lo, a), g_at(bits, lo, a + 1), phi


def context(bits: list[int], lo: int, radius: int) -> tuple[int, ...]:
    return tuple(
        value
        for j in range(-radius, radius + 1)
        for value in symbol(bits, lo, j)
    )


def next_symbol(bits: list[int], lo: int) -> tuple[int, int, int, int]:
    h1 = {p: h_at(bits, lo, p) for p in range(-3, 5)}
    h2 = {
        p: f(RULE, h1[p - 1], h1[p], h1[p + 1])
        for p in range(-2, 4)
    }

    def next_g(p: int) -> int:
        hp = {
            q: f(RULE, h2[q - 1], h2[q], h2[q + 1])
            for q in (p - 1, p, p + 1)
        }
        hh2 = f(RULE, hp[p - 1], hp[p], hp[p + 1])
        d = {q: h2[q] ^ hp[q] for q in (p - 1, p, p + 1)}
        hd = f(RULE, d[p - 1], d[p], d[p + 1])
        return hp[p] ^ hh2 ^ hd ^ (RULE & 1)

    return (
        h2[0] ^ h2[1],
        next_g(0),
        next_g(1),
        h2[0] ^ h2[2],
    )


def factor(radius: int) -> dict:
    # Current radius-r symbols need [-2r-2,2r+3]. The next central symbol
    # needs [-4,5]. Use the exact union.
    lo = min(-2 * radius - 2, -4)
    hi = max(2 * radius + 3, 5)
    width = hi - lo + 1
    table: dict[tuple[int, ...], tuple[tuple[int, ...], int]] = {}

    for word in range(1 << width):
        bits = [(word >> i) & 1 for i in range(width)]
        key = context(bits, lo, radius)
        target = next_symbol(bits, lo)
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
                    "next_symbol_x": list(previous[0]),
                    "next_symbol_y": list(target),
                },
            }
        table[key] = (target, word)

    return {
        "radius": radius,
        "pass": True,
        "source_width": width,
        "distinct_admissible_contexts": len(table),
        "conflict": None,
    }


def reconstruction_theorem_check(n: int) -> dict:
    # P_j and Phi_j determine block phase Q_j=X_{2j} up to one global bit:
    # Phi_j=Q_j xor Q_{j+1}; then odd source bits are Q_j xor P_j.
    # Exhaustive finite rings check the exact two-to-one claim for (P,Phi).
    def encode(state: int) -> tuple[int, int]:
        m = n // 2
        p = 0
        phi = 0
        for j in range(m):
            q = (state >> (2 * j)) & 1
            odd = (state >> (2 * j + 1)) & 1
            qn = (state >> (2 * ((j + 1) % m))) & 1
            p |= (q ^ odd) << j
            phi |= (q ^ qn) << j
        return p, phi

    fibers: dict[tuple[int, int], int] = {}
    for state in range(1 << n):
        key = encode(state)
        fibers[key] = fibers.get(key, 0) + 1

    sizes = sorted(set(fibers.values()))
    return {
        "n": n,
        "distinct_encodings": len(fibers),
        "fiber_sizes": sizes,
        "all_fibers_size_two": sizes == [2],
    }


def main() -> None:
    factors = [factor(r) for r in (0, 1, 2)]
    rings = [reconstruction_theorem_check(n) for n in (8, 10, 12)]

    result = {
        "schema": "rule110-phase-gradient-repair-v1",
        "date": "2026-10-07",
        "provenance": "post-hoc mechanism audit selected from the parity+Groovy phase-wall witness",
        "definition": {
            "P_j": "X_{2j} xor X_{2j+1}",
            "Phi_j": "X_{2j} xor X_{2j+2}",
            "W_j": "(P_j,G_{2j},G_{2j+1},Phi_j)",
            "cadence": 2,
        },
        "local_closure": factors,
        "compression": {
            "exact_argument": (
                "P and Phi determine Q_j=X_{2j} up to the choice of one global "
                "Q_0 bit; odd cells then equal Q_j xor P_j. Therefore (P,Phi), "
                "and hence W, has fibers of size at most two on a connected "
                "line/ring. The repair restores all but at most one global source bit."
            ),
            "finite_ring_checks": rings,
        },
        "relation_to_prior_work": (
            "Phi is the spatial gradient of the even-sublattice block phase. "
            "This is a blocked analogue of the source-gradient repairs already "
            "recorded in the Groovy-field census and of the lift's gradient rails."
        ),
        "summary": {
            "radius0_pass": factors[0]["pass"],
            "radius1_pass": factors[1]["pass"],
            "radius2_pass": factors[2]["pass"],
            "radius2_contexts": factors[2].get("distinct_admissible_contexts"),
            "phase_gradient_repair_nearly_microscopic": True,
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
