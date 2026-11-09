#!/usr/bin/env python3
"""Exact ECA classification for identically flat centered Groovy.

This is a post-hoc algebraic corollary of the 2026-10-06 typed-difference
geometry unit, not a preregistered prediction.

For an ECA local rule f(l,c,r), write its ANF as

  a0 + aL*l + aC*c + aR*r
     + aLC*l*c + aLR*l*r + aCR*c*r + aLCR*l*c*r.

The center cell of G depends on a radius-2 source word, so all 32 five-bit
words form the complete full-line local domain. This script exhaustively
checks all 256 ECA truth tables and verifies that centered G is identically
zero iff the ANF coefficients satisfy

  aLR = 0
  aCR = aLCR
  aLC = aLCR
  a0*aLCR = aR*aLCR = aL*aLCR = 0.

Those equations split into the 16 affine rules (aLCR=0) plus exactly two
nonlinear rules (aLCR=1): Rules 4 and 200.
"""
from __future__ import annotations

import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "results/centered_g_zero_classification_20261006.json"


def f(rule: int, l: int, c: int, r: int) -> int:
    return (rule >> ((l << 2) | (c << 1) | r)) & 1


def centered_g_center(rule: int, word: int) -> int:
    """Centered G at the center of a five-bit source word."""
    x = [(word >> i) & 1 for i in range(5)]  # positions -2..2
    hx = [f(rule, x[i], x[i + 1], x[i + 2]) for i in range(3)]
    h2 = f(rule, hx[0], hx[1], hx[2])
    dx = [x[i + 1] ^ hx[i] for i in range(3)]
    hdx = f(rule, dx[0], dx[1], dx[2])
    raw_g = hx[1] ^ h2 ^ hdx
    h0 = rule & 1
    return raw_g ^ h0


def anf(rule: int) -> dict[str, int]:
    # Truth-table index bits are r=1, c=2, l=4. The Boolean Möbius transform
    # is its own inverse over F2.
    coeff = [(rule >> i) & 1 for i in range(8)]
    for axis in range(3):
        for mask in range(8):
            if mask & (1 << axis):
                coeff[mask] ^= coeff[mask ^ (1 << axis)]
    names = ["a0", "aR", "aC", "aCR", "aL", "aLR", "aLC", "aLCR"]
    return dict(zip(names, coeff))


def coefficient_condition(a: dict[str, int]) -> bool:
    q = a["aLCR"]
    return (
        a["aLR"] == 0
        and a["aCR"] == q
        and a["aLC"] == q
        and (a["a0"] & q) == 0
        and (a["aR"] & q) == 0
        and (a["aL"] & q) == 0
    )


def main() -> None:
    flat = []
    classified = []
    mismatches = []
    nonlinear = []

    for rule in range(256):
        is_flat = all(centered_g_center(rule, word) == 0 for word in range(32))
        a = anf(rule)
        predicted = coefficient_condition(a)
        if is_flat:
            flat.append(rule)
        if predicted:
            classified.append(rule)
        if is_flat != predicted:
            mismatches.append({"rule": rule, "flat": is_flat, "condition": predicted})
        if is_flat and any(a[k] for k in ("aCR", "aLR", "aLC", "aLCR")):
            nonlinear.append({"rule": rule, "anf": a})

    affine = [r for r in flat if anf(r)["aLCR"] == 0]
    nonlinear_rules = [x["rule"] for x in nonlinear]

    result = {
        "schema": "centered-g-zero-eca-classification-v1",
        "date": "2026-10-06",
        "source_hashes": {
            "script_sha256": hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
        },
        "domain": {
            "rules": 256,
            "source_words_per_rule": 32,
            "reason": "the center of G has radius 2, so five source bits are the complete full-line local domain",
        },
        "classification": {
            "equations": [
                "aLR = 0",
                "aCR = aLCR",
                "aLC = aLCR",
                "a0*aLCR = 0",
                "aR*aLCR = 0",
                "aL*aLCR = 0",
            ],
            "flat_rules": flat,
            "condition_rules": classified,
            "affine_branch_count": len(affine),
            "nonlinear_branch_rules": nonlinear_rules,
            "nonlinear_branch_anf": nonlinear,
            "mismatches": mismatches,
        },
        "summary": {
            "pass": not mismatches,
            "flat_rule_count": len(flat),
            "affine_branch_count": len(affine),
            "nonlinear_branch_rules": nonlinear_rules,
        },
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result["summary"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
