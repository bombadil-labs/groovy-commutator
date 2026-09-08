"""Exact finite contact-template checks supporting the all-integer scattering proof.

This is a post-census deductive audit, not a preregistered prediction.  It
exhausts arbitrary deeper interior bits across the complete causal depth needed
by the longest (8 fine tick) contact template.
"""
from __future__ import annotations

from itertools import product
from pathlib import Path
import hashlib
import json

from experiment_pulse_scattering import background, dense_step

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/pulse_scattering_20260908_templates.json"


def encode_v0(a: set[int], b: set[int]) -> set[tuple[int, int]]:
    delta = set()
    for i in a:
        delta.add((0, 2*i + 1)); delta.add((1, 2*i))
    for i in b:
        delta.add((2, 2*i + 1)); delta.add((3, 2*i))
    return delta


def rule90(s: set[int]) -> set[int]:
    if not s:
        return set()
    return {i for i in range(min(s)-1, max(s)+2)
            if ((i-1 in s) ^ (i+1 in s))}


def first_exterior(delta: set[tuple[int, int]], limit: int = 10):
    for t in range(limit + 1):
        if any(y < 0 or y > 3 for y, _ in delta):
            ymin = min(y for y, _ in delta); ymax = max(y for y, _ in delta)
            top = sorted(x for y, x in delta if y == ymin)
            bottom = sorted(x for y, x in delta if y == ymax)
            return t, top, bottom, delta
        if t < limit:
            delta = dense_step(delta, t)
    return None


def persistent_parity(t: int, top: list[int], bottom: list[int]) -> bool:
    return (bool(top) and bool(bottom)
            and all(background(t, x+1) == 1 for x in top)
            and all(background(t, x-1) == 0 for x in bottom))


def interiors(direction: int, edge: int, p: int, bits: tuple[int, int, int]):
    """Edge, fixed first inward coefficient p, then three arbitrary deeper bits."""
    s = {edge}
    if p:
        s.add(edge + 2*direction)
    for k, bit in enumerate(bits, start=2):
        if bit:
            s.add(edge + 2*k*direction)
    return s


def template_rows(name: str, p: int, ua, ub):
    if name == "positive-even":
        # lower approaches from left: B edge -1; upper from right: A edge +1
        return interiors(+1, 1, p, ua), interiors(-1, -1, p, ub)
    if name == "positive-odd":
        # adjacent edges: lower B at 0, upper A at 1
        return interiors(+1, 1, p, ua), interiors(-1, 0, p, ub)
    if name == "negative-odd":
        # adjacent edges with upper on left
        return interiors(-1, 0, p, ua), interiors(+1, 1, p, ub)
    if name == "negative-even":
        # coincident edges after the special preceding cancellation
        return interiors(-1, 0, p, ua), interiors(+1, 0, p, ub)
    raise ValueError(name)


EXPECTED = {
    ("positive-even", 0): (6, [4], [-3]),
    ("positive-even", 1): (8, [4], [-3]),
    ("positive-odd", 0): (4, [4], [-1]),
    ("positive-odd", 1): (4, [4], [-1]),
    ("negative-odd", 0): (8, [2], [1]),
    ("negative-odd", 1): (8, [4, 6], [-3, -1]),
    ("negative-even", 0): (6, [4], [-3]),
    ("negative-even", 1): (6, [4], [-3]),
}


def main():
    records = []
    checks = 0
    for (name, p), expected in EXPECTED.items():
        outcomes = set()
        for bits_a in product((0, 1), repeat=3):
            for bits_b in product((0, 1), repeat=3):
                a, b = template_rows(name, p, bits_a, bits_b)
                got = first_exterior(encode_v0(a, b), limit=8)
                if got is None:
                    raise AssertionError((name, p, bits_a, bits_b, "no exterior"))
                t, top, bottom, _ = got
                observed = (t, tuple(top), tuple(bottom))
                outcomes.add(observed)
                checks += 1
                if (t, top, bottom) != expected:
                    raise AssertionError((name, p, bits_a, bits_b, observed, expected))
                if not persistent_parity(t, top, bottom):
                    raise AssertionError((name, p, bits_a, bits_b, "front parity"))
        records.append({"template": name, "edge_parity": p,
                        "assignments": 64, "outcomes": [list(x) for x in sorted(outcomes)]})

    # Negative-even approach has one interaction one coarse tick before the
    # coincident-edge template. Exhaustively verify that it cancels back into
    # the exact V0 Rule-90 image, for arbitrary deeper interior bits.
    cancellation_checks = 0
    for p in (0, 1):
        for bits_a in product((0, 1), repeat=3):
            for bits_b in product((0, 1), repeat=3):
                a = interiors(-1, -1, p, bits_a)
                b = interiors(+1, 1, p, bits_b)
                delta = encode_v0(a, b)
                delta = dense_step(delta, 0)
                delta = dense_step(delta, 1)
                expected = encode_v0(rule90(a), rule90(b))
                cancellation_checks += 1
                if delta != expected:
                    raise AssertionError(("negative-even cancellation", p, bits_a, bits_b))

    result = {
        "ok": True,
        "contact_template_assignments": checks,
        "negative_even_cancellation_assignments": cancellation_checks,
        "records": records,
        "deductive_inputs": {
            "rule90_edge": "C(n,0)=1 at either edge",
            "rule90_first_inward": "C(n,1)=n mod 2",
            "deeper_bits": "three inward coefficients per row exhausted arbitrarily",
            "max_contact_horizon": 8,
        },
        "source_sha256": {
            "script": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "primary_instrument": hashlib.sha256((ROOT / "scripts/experiment_pulse_scattering.py").read_bytes()).hexdigest(),
        },
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in (
        "ok", "contact_template_assignments", "negative_even_cancellation_assignments")}, indent=2))
    for r in records:
        print(r["template"], r["edge_parity"], r["outcomes"])


if __name__ == "__main__":
    main()
