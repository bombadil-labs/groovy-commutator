#!/usr/bin/env python3
"""Exact bounded audit of typed finite-difference geometry in the affine jet lift.

Research protocol:
  docs/research/protocols/typed-lift-defect-20261006.md
Gate-E supplement:
  docs/research/protocols/typed-lift-defect-gate-e-probes-20261006.md

The algebraic claims are more general than ECAs.  The finite ECA sweeps below
serve as independent verification and tiny-counterexample search.

Conventions:
  - finite rings are encoded as integers, bit i = cell i;
  - H is an ECA global map;
  - d_H(x) = x XOR H(x);
  - partial_H(x,u) = H(x XOR u) XOR H(x);
  - centered G = G XOR H(0);
  - B_H(x,u) = partial_H(x,u) XOR partial_H(0,u).

Ring 5 contains a complete radius-2 source neighbourhood, so the all-pairs
Gate-C check is a complete local-domain verification of the six-field
cross-effect identity for ECAs.  Ring 7 contains a complete radius-3 source
neighbourhood, so the frozen Gate-E dynamic probes are full-line local
certificates, not merely finite-size samples.

The original canonical section/evolution defect is not swept here: the already
accepted lift theorem states H_up(L_H X) = L_H(H X), so that defect is
identically zero on the marked beam by theorem.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "results/typed_lift_defect_20261006.json"


def maskn(n: int) -> int:
    return (1 << n) - 1


def bit(state: int, i: int, n: int) -> int:
    return (state >> (i % n)) & 1


def eca_step(state: int, n: int, rule: int) -> int:
    out = 0
    for i in range(n):
        l = bit(state, i - 1, n)
        c = bit(state, i, n)
        r = bit(state, i + 1, n)
        idx = (l << 2) | (c << 1) | r
        out |= ((rule >> idx) & 1) << i
    return out


def iterate(x: int, n: int, rule: int, t: int) -> int:
    for _ in range(t):
        x = eca_step(x, n, rule)
    return x


def d_h(x: int, n: int, rule: int) -> int:
    return x ^ eca_step(x, n, rule)


def g_h(x: int, n: int, rule: int) -> int:
    hx = eca_step(x, n, rule)
    return (hx ^ eca_step(hx, n, rule)) ^ eca_step(x ^ hx, n, rule)


def partial_h(x: int, u: int, n: int, rule: int) -> int:
    return eca_step(x ^ u, n, rule) ^ eca_step(x, n, rule)


def b_h(x: int, u: int, n: int, rule: int) -> int:
    return partial_h(x, u, n, rule) ^ partial_h(0, u, n, rule)


def k_h(x: int, n: int, rule: int, t: int) -> int:
    ht = iterate(x, n, rule, t)
    return (ht ^ eca_step(ht, n, rule)) ^ iterate(d_h(x, n, rule), n, rule, t)


def shift(x: int, n: int, delta: int) -> int:
    """tau_delta X(p) = X(p+delta)."""
    out = 0
    for p in range(n):
        out |= bit(x, p + delta, n) << p
    return out


def lift1_fields(x: int, n: int, rule: int) -> tuple[int, ...]:
    hx = eca_step(x, n, rule)
    h2x = eca_step(hx, n, rule)
    return (
        x ^ shift(x, n, 1),
        maskn(n) ^ x ^ shift(x, n, -1),
        x ^ hx,
        x ^ h2x,
        0,
        x,
    )


def centered_lift_fields(x: int, n: int, rule: int) -> tuple[int, ...]:
    lx = lift1_fields(x, n, rule)
    l0 = lift1_fields(0, n, rule)
    return tuple(a ^ b for a, b in zip(lx, l0))


def b_iter(x: int, y: int, n: int, rule: int, t: int) -> int:
    return (
        iterate(x ^ y, n, rule, t)
        ^ iterate(x, n, rule, t)
        ^ iterate(y, n, rule, t)
        ^ iterate(0, n, rule, t)
    )


def cr3_global(a: int, b: int, c: int, n: int, rule: int) -> int:
    out = 0
    for subset in range(8):
        q = 0
        if subset & 1:
            q ^= a
        if subset & 2:
            q ^= b
        if subset & 4:
            q ^= c
        out ^= eca_step(q, n, rule)
    return out


def local_delta(rule: int, a: int, u: int) -> int:
    f = lambda q: (rule >> q) & 1
    return f(a ^ u) ^ f(a)


def local_cr3(rule: int, a: int, b: int, c: int) -> int:
    f = lambda q: (rule >> q) & 1
    out = 0
    for subset in range(8):
        q = 0
        if subset & 1:
            q ^= a
        if subset & 2:
            q ^= b
        if subset & 4:
            q ^= c
        out ^= f(q)
    return out


def local_anf_degree(rule: int) -> tuple[int, list[int]]:
    # Möbius transform on the 3-cube.  Bit positions of the index are the
    # three Boolean input variables; degree is invariant to their naming.
    coeff = [(rule >> i) & 1 for i in range(8)]
    for axis in range(3):
        for m in range(8):
            if m & (1 << axis):
                coeff[m] ^= coeff[m ^ (1 << axis)]
    degree = 0
    for monomial, value in enumerate(coeff):
        if value:
            degree = max(degree, monomial.bit_count())
    return degree, coeff


def compose_center_on_word5(rule: int, word5: int) -> tuple[int, int, int]:
    """Return H(x)_0, H^2(x)_0 and H(d_H x)_0 from a full radius-2 word."""
    bits = [(word5 >> j) & 1 for j in range(5)]

    def f3(a: int, b: int, c: int) -> int:
        return (rule >> ((a << 2) | (b << 1) | c)) & 1

    hx = [f3(bits[j - 1], bits[j], bits[j + 1]) for j in (1, 2, 3)]
    h2_center = f3(*hx)
    d_window = [bits[j] ^ hx[k] for k, j in enumerate((1, 2, 3))]
    h_d_center = f3(*d_window)
    return hx[1], h2_center, h_d_center


def gate_b() -> dict:
    result = {}
    for n in (5, 6, 7):
        typed_failures = 0
        g_failures = 0
        first_typed = None
        first_g = None
        for rule in range(256):
            h0 = eca_step(0, n, rule)
            for x in range(1 << n):
                u = d_h(x, n, rule)
                lhs = partial_h(x, u, n, rule)
                rhs = d_h(eca_step(x, n, rule), n, rule)
                if lhs != rhs:
                    typed_failures += 1
                    if first_typed is None:
                        first_typed = [rule, x, lhs, rhs]
                centered_g = g_h(x, n, rule) ^ h0
                polarization = b_h(x, u, n, rule)
                if centered_g != polarization:
                    g_failures += 1
                    if first_g is None:
                        first_g = [rule, x, centered_g, polarization]
        result[str(n)] = {
            "states_per_rule": 1 << n,
            "typed_transport_failures": typed_failures,
            "centered_G_failures": g_failures,
            "first_typed_failure": first_typed,
            "first_G_failure": first_g,
        }
    return result


def gate_c() -> dict:
    # C1: complete local-domain pair check at radius 2.
    n = 5
    failures = 0
    first = None
    for rule in range(256):
        js = [centered_lift_fields(x, n, rule) for x in range(1 << n)]
        for x in range(1 << n):
            for y in range(1 << n):
                cr = tuple(js[x ^ y][i] ^ js[x][i] ^ js[y][i] for i in range(6))
                expected = (0, 0, b_h(x, y, n, rule), b_iter(x, y, n, rule, 2), 0, 0)
                if cr != expected:
                    failures += 1
                    if first is None:
                        first = [rule, x, y, list(cr), list(expected)]

    # C2: specialize to the trajectory graph and compare to centered K1/K2.
    trajectory = {}
    for n in (5, 6, 7):
        fails = 0
        first_t = None
        for rule in range(256):
            h0 = eca_step(0, n, rule)
            h20 = iterate(0, n, rule, 2)
            js = [centered_lift_fields(x, n, rule) for x in range(1 << n)]
            for x in range(1 << n):
                y = eca_step(x, n, rule)
                cr = tuple(js[x ^ y][i] ^ js[x][i] ^ js[y][i] for i in range(6))
                expected = (0, 0, k_h(x, n, rule, 1) ^ h0, k_h(x, n, rule, 2) ^ h20, 0, 0)
                if cr != expected:
                    fails += 1
                    if first_t is None:
                        first_t = [rule, x, list(cr), list(expected)]
        trajectory[str(n)] = {"failures": fails, "first_failure": first_t}

    return {
        "all_pairs_ring5": {
            "pairs_per_rule": (1 << 5) ** 2,
            "failures": failures,
            "first_failure": first,
            "domain_note": "complete radius-2 local source-pair domain for ECA temporal rows",
        },
        "trajectory_checks": trajectory,
    }


def gate_d() -> dict:
    result = {}
    for n in (5, 6, 7):
        failures = 0
        first = None
        for rule in range(256):
            for x in range(1 << n):
                raw_u = d_h(x, n, rule)
                ht = x
                bt = raw_u
                kt = 0
                for t in range(7):
                    k_next = k_h(x, n, rule, t + 1)
                    rhs = g_h(ht, n, rule) ^ partial_h(bt, kt, n, rule)
                    if k_next != rhs:
                        failures += 1
                        if first is None:
                            first = [rule, x, t, k_next, rhs]
                    kt = k_next
                    ht = eca_step(ht, n, rule)
                    bt = eca_step(bt, n, rule)
        result[str(n)] = {
            "states_per_rule": 1 << n,
            "horizons": "0..6",
            "failures": failures,
            "first_failure": first,
        }

    # Exact local truth-table classification: partial_H(x,u) is independent of
    # basepoint x iff the Boolean local rule is affine.
    independent = []
    witnesses = {}
    for rule in range(256):
        ok = True
        witness = None
        for u in range(8):
            values = [local_delta(rule, a, u) for a in range(8)]
            if len(set(values)) > 1:
                ok = False
                for a in range(8):
                    for b in range(a + 1, 8):
                        da = local_delta(rule, a, u)
                        db = local_delta(rule, b, u)
                        if da != db:
                            witness = [a, b, u, da, db]
                            break
                    if witness is not None:
                        break
                break
        if ok:
            independent.append(rule)
        else:
            witnesses[str(rule)] = witness

    result["local_fibre_action"] = {
        "basepoint_independent_rules": independent,
        "basepoint_dependent_count": 256 - len(independent),
        "example_rule110": witnesses.get("110"),
    }
    return result


def gate_e() -> dict:
    degree_counts = Counter()
    cubic_rules = []
    cr3_nonzero = []
    for rule in range(256):
        degree, _ = local_anf_degree(rule)
        degree_counts[degree] += 1
        if degree == 3:
            cubic_rules.append(rule)
        if any(local_cr3(rule, a, b, c) for a in range(8) for b in range(8) for c in range(8)):
            cr3_nonzero.append(rule)

    probes = {}
    n = 7
    for name in ("orbit", "raw", "typed"):
        zero_rules = []
        nonzero_rules = []
        witnesses = {}
        for rule in range(256):
            nonzero = False
            for x in range(1 << n):
                hx = eca_step(x, n, rule)
                u = x ^ hx
                if name == "orbit":
                    args = (x, hx, eca_step(hx, n, rule))
                elif name == "raw":
                    args = (x, u, eca_step(u, n, rule))
                else:
                    args = (x, u, partial_h(x, u, n, rule))
                value = cr3_global(*args, n, rule)
                if value:
                    nonzero = True
                    witnesses[str(rule)] = [x, value]
                    break
            (nonzero_rules if nonzero else zero_rules).append(rule)

        cubic_zero = sorted(set(cubic_rules).intersection(zero_rules))
        probes[name] = {
            "zero_rule_count": len(zero_rules),
            "nonzero_rule_count": len(nonzero_rules),
            "zero_rules": zero_rules,
            "cubic_but_probe_zero_rules": cubic_zero,
            "rules4_200_nonzero": [r for r in (4, 200) if r in nonzero_rules],
            "domain_note": "ring 7 exhausts the radius-3 source neighbourhood, so zero is a full-line local identity",
            "example_witnesses": {k: witnesses[k] for k in list(witnesses)[:5]},
        }

    # Post-hoc mechanism audit prompted by the frozen probes' failure on 4/200.
    # H^2=H and H(d_H x)=H(0) are radius-2 identities, so all 32 words suffice.
    retract_rules = []
    details = {}
    for rule in range(256):
        idempotent = True
        residual_to_bias = True
        for word in range(32):
            hx, h2x, hdx = compose_center_on_word5(rule, word)
            h0 = rule & 1
            if h2x != hx:
                idempotent = False
            if hdx != h0:
                residual_to_bias = False
        if idempotent and residual_to_bias:
            retract_rules.append(rule)
        if rule in (4, 200):
            details[str(rule)] = {
                "H2_eq_H": idempotent,
                "H_of_D_eq_H0": residual_to_bias,
                "H0": rule & 1,
            }

    # Stronger exact relation for the nonlinear zero-bias pair 4/200.
    pair = {"xor_truth_table_is_identity_rule_204": (4 ^ 200) == 204}
    for a, b, label in ((4, 200, "4_then_200"), (200, 4, "200_then_4")):
        # Composition has radius 2; 32 words are complete.
        annihilates = True
        for word in range(32):
            bits = [(word >> j) & 1 for j in range(5)]

            def f3(rule: int, aa: int, bb: int, cc: int) -> int:
                return (rule >> ((aa << 2) | (bb << 1) | cc)) & 1

            first = [f3(a, bits[j - 1], bits[j], bits[j + 1]) for j in (1, 2, 3)]
            if f3(b, *first) != 0:
                annihilates = False
                break
        pair[label + "_is_zero"] = annihilates

    return {
        "local_anf_degree_counts": {str(k): degree_counts[k] for k in sorted(degree_counts)},
        "local_cubic_rule_count": len(cubic_rules),
        "local_cr3_nonzero_rule_count": len(cr3_nonzero),
        "cr3_matches_degree3": cr3_nonzero == cubic_rules,
        "dynamic_probes_ring7": probes,
        "posthoc_projection_mechanism": {
            "rules_satisfying_H2_eq_H_and_HofD_eq_H0": retract_rules,
            "rules4_200": details,
            "rule4_rule200_pair": pair,
        },
    }


def main() -> None:
    script_hash = hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()

    result = {
        "schema": "typed-lift-defect-v1",
        "date": "2026-10-06",
        "source_hashes": {"script_sha256": script_hash},
        "gate_A": {
            "status": "settled_by_existing_theorem",
            "identity": "H_up(L_H(X)) = L_H(H(X))",
            "canonical_section_evolution_defect": "identically zero on the marked beam",
            "new_sweep_required": False,
        },
    }

    result["gate_B"] = gate_b()
    result["gate_C"] = gate_c()
    result["gate_D"] = gate_d()
    result["gate_E"] = gate_e()

    result["summary"] = {
        "gate_B_all_pass": all(
            item["typed_transport_failures"] == 0 and item["centered_G_failures"] == 0
            for item in result["gate_B"].values()
        ),
        "gate_C_all_pass": (
            result["gate_C"]["all_pairs_ring5"]["failures"] == 0
            and all(v["failures"] == 0 for v in result["gate_C"]["trajectory_checks"].values())
        ),
        "gate_D_recurrence_all_pass": all(result["gate_D"][str(n)]["failures"] == 0 for n in (5, 6, 7)),
        "basepoint_independent_rule_count": len(
            result["gate_D"]["local_fibre_action"]["basepoint_independent_rules"]
        ),
        "gate_E_dynamic_catches_rule4_or200": any(
            result["gate_E"]["dynamic_probes_ring7"][name]["rules4_200_nonzero"]
            for name in ("orbit", "raw", "typed")
        ),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(OUT)


if __name__ == "__main__":
    main()
