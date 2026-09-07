"""Exhaustive local checks behind the recovered Rule 90 / 110 comparison.

Truth-table enumeration uses finite causal windows, not a finite torus.
ANF bit j denotes input position j, from left to right. The only periodic
checks explicitly exercise the power-of-two-ring pathology.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from groovy.ca import apply_rule, rule_lut  # noqa: E402


def windows(width):
    return ((np.arange(1 << width, dtype=np.uint32)[:, None]
             >> np.arange(width)) & 1).astype(np.uint8)


def interior_step(x, rule):
    return rule_lut(rule)[4 * x[:, :-2] + 2 * x[:, 1:-1] + x[:, 2:]]


def anf(table):
    out = table.copy()
    width = (len(out) - 1).bit_length()
    for bit in range(width):
        view = out.reshape(-1, 2, 1 << bit)
        view[:, 1] ^= view[:, 0]
    masks = np.flatnonzero(out).tolist()
    return {"degree": max((m.bit_count() for m in masks), default=0),
            "monomials": len(masks), "masks": masks}


def commutator_table(rule):
    x = windows(5)
    e = interior_step(x, rule)
    de = e[:, 1] ^ interior_step(e, rule)[:, 0]
    d = x[:, 1:-1] ^ e
    return de ^ interior_step(d, rule)[:, 0]


def closure_error(rule, block, stride, projection):
    """All 3b microcells; stride <= b keeps the output inside this window."""
    x = windows(3 * block)
    weights = 1 << np.arange(block)
    before = projection[(x.reshape(-1, 3, block) * weights).sum(axis=2)]
    key = 4 * before[:, 0] + 2 * before[:, 1] + before[:, 2]
    evolved = x
    for _ in range(stride):
        evolved = interior_step(evolved, rule)
    start = block - stride
    target = projection[(evolved[:, start:start + block] * weights).sum(axis=1)]
    c0 = np.bincount(key[target == 0], minlength=8)
    c1 = np.bincount(key[target == 1], minlength=8)
    errors = int(np.minimum(c0, c1).sum())
    return errors, len(target), int(((c1 > c0) * (1 << np.arange(8))).sum())


def main():
    result = {"method": "exhaustive causal windows; uniform window weighting",
              "derivative_rules": {}, "commutators": {}, "dyadic": [],
              "parity_closure": [], "bounded_projection_search": []}
    for rule in range(256):
        assert np.array_equal(rule_lut(rule ^ 204),
                              rule_lut(rule) ^ rule_lut(204))
    result["derivative_rules"] = {"90": 150, "110": 162}
    constants = {"zero": [], "one": []}
    for rule in range(256):
        table = commutator_table(rule)
        if np.all(table == table[0]):
            constants["one" if table[0] else "zero"].append(rule)
        if rule in (90, 110, 30, 54):
            result["commutators"][str(rule)] = {
                "ones": int(table.sum()), "windows": 32, **anf(table)}
    assert result["commutators"]["110"]["masks"] == [8, 10, 23, 30]
    assert result["commutators"]["110"]["ones"] == 10
    assert constants["zero"] == [0, 4, 60, 90, 102, 150, 170, 200, 204, 240]
    assert constants["one"] == [15, 51, 85, 105, 153, 165, 195, 255]
    result["constant_commutator_rules"] = constants
    expected = {90: [(1, 3)] * 4,
                110: [(3, 3), (5, 7), (8, 71), (15, 5135)],
                30: [(2, 3), (3, 11), (7, 121), (15, 23093)]}
    for rule in (90, 110, 30):
        for b, pair in zip((1, 2, 4, 8), expected[rule]):
            x = windows(2 * b + 1)
            y = x
            for _ in range(b):
                y = interior_step(y, rule)
            props = anf(x[:, b] ^ y[:, 0])
            assert (props["degree"], props["monomials"]) == pair
            result["dyadic"].append({"rule": rule, "horizon": b,
                                      "degree": props["degree"],
                                      "monomials": props["monomials"]})
        for b in (2, 4):
            projection = np.array([i.bit_count() % 2 for i in range(1 << b)],
                                  dtype=np.uint8)
            e, n, macro = closure_error(rule, b, b, projection)
            if rule == 90:
                assert e == 0 and macro == 90
            result["parity_closure"].append({"rule": rule, "block": b,
                "stride": b, "error_count": e, "windows": n,
                "error": e / n, "best_macro_rule": macro})
    for b in (2, 3):
        for stride in range(1, b + 1):
            hits = []
            for p in range(1, (1 << (1 << b)) - 1):
                projection = np.array([(p >> i) & 1 for i in range(1 << b)],
                                      dtype=np.uint8)
                e, _, macro = closure_error(110, b, stride, projection)
                if e == 0:
                    hits.append({"projection": p, "macro_rule": macro})
            assert not hits
            result["bounded_projection_search"].append({"rule": 110, "block": b,
                "stride": stride, "nonconstant_projections": (1 << (1 << b)) - 2,
                "exact_closures": hits})
    # T^(n/2) = shift^(n/2) XOR shift^(-n/2) = 0 for n a power of two.
    for n in (8, 16, 32, 256):
        s = np.zeros(n, dtype=np.uint8)
        s[0] = 1
        for _ in range(n // 2):
            s = apply_rule(s, 90)
        assert not s.any()
    # Non-power-of-two control at the former burn-in of 150.
    s = np.zeros(300, dtype=np.uint8)
    s[0] = 1
    for _ in range(150):
        s = apply_rule(s, 90)
    assert s.any()
    result["torus_checks"] = {"power_of_two_n": [8, 16, 32, 256],
        "zero_by": "n/2", "n300_single_seed_nonzero_at_t150": True}
    out = ROOT / "results/history_algebra_checks.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print("All exhaustive checks passed; wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
