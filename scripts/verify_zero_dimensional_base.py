#!/usr/bin/env python3
"""Verifier for the frozen zero-dimensional-base selector protocol.

Protocol: docs/research/protocols/zero-dimensional-base-20260912.md
Gate 1: Claude Code / Fable 5.1 approved exact gathering head
c46a6f7d4c13a56512b20832be4f1b2489a50f78 on 2026-09-12.

This file is the implementation-only stage. Committing it does not execute the
frozen Z0/Z1 evaluation and does not create a canonical result. Running without
--self-test performs the complete frozen evaluation and writes
results/zero_dimensional_base_20260912.json. --self-test uses only an
out-of-domain two-address-bit toy multiplexer and writes nothing.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "docs/research/protocols/zero-dimensional-base-20260912.md"
OUT = ROOT / "results/zero_dimensional_base_20260912.json"

HISTORY = ROOT / "results/history_algebra_checks.json"
SHARED_AUDIT = ROOT / "results/shared_state_rule_20260907_audit.json"
SHARED_LOCAL = ROOT / "results/shared_state_rule_20260907_local.json"
AXIAL = ROOT / "results/guard_free_axial_lift_20260910.json"
ROUTING = ROOT / "results/editable_routing_tables_20260909.json"

# Git blob SHAs on the accepted main base, recorded before implementation.
ACCEPTED_GIT_BLOBS = {
    "history_algebra_result": "a63d4ac3ad5176c4e95bc1076107a83086e061e4",
    "shared_state_audit": "4c514a21d843c0a09330f71f02bd9886bdda0327",
    "shared_state_local": "fd639a3a3137016911dfbaf12e16b85207601995",
    "guard_free_axial_result": "872ada3cdbfb581a3edae536bfe3be4363084ec2",
    "editable_routing_result": "8fd5ce533a142c4b7847e535e3c57cefaa985ba8",
}

PATCH_NAMES = ("NW", "N", "NE", "W", "C", "E", "SW", "S", "SE")
PATCH_INDEX = {name: i for i, name in enumerate(PATCH_NAMES)}
SHELL_NAMES = ("N", "NE", "E", "SE", "S", "SW", "W", "NW")
SHELL_PATCH_INDEX = tuple(PATCH_INDEX[name] for name in SHELL_NAMES)
REFERENCE_GRAY = (0, 1, 3, 2, 6, 7, 5, 4)
ADDRESS_VARIABLES = (PATCH_INDEX["W"], PATCH_INDEX["C"], PATCH_INDEX["E"])

Z0_ORIENTATIONS = {
    "Z0-A": (0, 2),
    "Z0-B": (2, 0),
}

EXPECTED_GROOVY = {0: 0, 204: 0, 51: 1, 255: 1}
CENTER_ONLY = (0, 204, 51, 255)


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob_sha(path: pathlib.Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def assert_accepted_inputs() -> dict[str, dict[str, str]]:
    paths = {
        "history_algebra_result": HISTORY,
        "shared_state_audit": SHARED_AUDIT,
        "shared_state_local": SHARED_LOCAL,
        "guard_free_axial_result": AXIAL,
        "editable_routing_result": ROUTING,
    }
    out = {}
    for key, path in paths.items():
        actual = git_blob_sha(path)
        expected = ACCEPTED_GIT_BLOBS[key]
        if actual != expected:
            raise AssertionError(f"accepted input drift for {key}: {actual} != {expected}")
        out[key] = {"path": str(path.relative_to(ROOT)), "git_blob_sha": actual, "sha256": sha256(path)}
    return out


def bits_of(value: int, n: int) -> tuple[int, ...]:
    return tuple((value >> i) & 1 for i in range(n))


def truth_table(nvars: int, func) -> list[int]:
    return [int(func(bits_of(a, nvars))) & 1 for a in range(1 << nvars)]


def anf_from_truth(table: list[int], nvars: int) -> frozenset[int]:
    coeff = list(table)
    for i in range(nvars):
        bit = 1 << i
        for mask in range(1 << nvars):
            if mask & bit:
                coeff[mask] ^= coeff[mask ^ bit]
    return frozenset(mask for mask, c in enumerate(coeff) if c & 1)


def truth_from_anf(poly: frozenset[int], nvars: int) -> list[int]:
    out = []
    for assignment in range(1 << nvars):
        value = 0
        for monomial in poly:
            if monomial & ~assignment == 0:
                value ^= 1
        out.append(value)
    return out


def essential_from_truth(table: list[int], nvars: int) -> tuple[int, ...]:
    essential = []
    for i in range(nvars):
        bit = 1 << i
        if any(table[a] != table[a | bit] for a in range(1 << nvars) if not (a & bit)):
            essential.append(i)
    return tuple(essential)


def poly_xor(a: set[int], b: set[int]) -> set[int]:
    return a.symmetric_difference(b)


def poly_mul(a: set[int], b: set[int]) -> set[int]:
    out: set[int] = set()
    for ma in a:
        for mb in b:
            term = ma | mb
            if term in out:
                out.remove(term)
            else:
                out.add(term)
    return out


def indicator_poly(var_indices: tuple[int, ...], address: int) -> set[int]:
    poly = {0}
    k = len(var_indices)
    for j, var in enumerate(var_indices):
        desired = (address >> (k - 1 - j)) & 1
        factor = {1 << var} if desired else {0, 1 << var}
        poly = poly_mul(poly, factor)
    return poly


def selector_symbolic_anf(nvars: int, address_vars: tuple[int, ...], program_var_by_address: tuple[int, ...]) -> frozenset[int]:
    poly: set[int] = set()
    for address, program_var in enumerate(program_var_by_address):
        term = poly_mul(indicator_poly(address_vars, address), {1 << program_var})
        poly = poly_xor(poly, term)
    return frozenset(poly)


def anf_summary(poly: frozenset[int], names: tuple[str, ...]) -> dict:
    by_degree: dict[int, int] = defaultdict(int)
    for m in poly:
        by_degree[m.bit_count()] += 1
    degree = max(by_degree, default=0)
    essential = sorted(i for i in range(len(names)) if any(m & (1 << i) for m in poly))
    return {
        "degree": degree,
        "monomial_count_by_degree": {str(k): by_degree[k] for k in sorted(by_degree)},
        "essential_inputs": [names[i] for i in essential],
        "highest_degree_monomials": [
            [names[i] for i in range(len(names)) if m & (1 << i)]
            for m in sorted(poly)
            if m.bit_count() == degree
        ],
    }


def z0_scalar(bits: tuple[int, ...], program_vars: tuple[int, int]) -> int:
    l, c, r = bits
    values = (l, r)
    return values[c] if program_vars == (0, 2) else values[1 - c]


def z0_packed(assignment: int, program_vars: tuple[int, int]) -> int:
    address = (assignment >> 1) & 1
    var = program_vars[address]
    return (assignment >> var) & 1


def layout_address_to_shell(layout: tuple[int, ...]) -> tuple[int, ...]:
    if sorted(layout) != list(range(8)):
        raise AssertionError("layout is not a bijection")
    inverse = [0] * 8
    for shell_pos, address in enumerate(layout):
        inverse[address] = shell_pos
    return tuple(inverse)


def layout_program_vars(layout: tuple[int, ...]) -> tuple[int, ...]:
    address_to_shell = layout_address_to_shell(layout)
    return tuple(SHELL_PATCH_INDEX[address_to_shell[a]] for a in range(8))


def z1_scalar(bits: tuple[int, ...], layout: tuple[int, ...]) -> int:
    patch = dict(zip(PATCH_NAMES, bits))
    address = 4 * patch["W"] + 2 * patch["C"] + patch["E"]
    shell_pos = layout_address_to_shell(layout)[address]
    return patch[SHELL_NAMES[shell_pos]]


def z1_packed(assignment: int, layout: tuple[int, ...]) -> int:
    w = (assignment >> PATCH_INDEX["W"]) & 1
    c = (assignment >> PATCH_INDEX["C"]) & 1
    e = (assignment >> PATCH_INDEX["E"]) & 1
    address = (w << 2) | (c << 1) | e
    var = layout_program_vars(layout)[address]
    return (assignment >> var) & 1


def compose_perm(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(p[q[i]] for i in range(len(p)))


def shell_perm_rotation(steps_45: int) -> tuple[int, ...]:
    return tuple((i + steps_45) % 8 for i in range(8))


R0 = tuple(range(8))
R90 = shell_perm_rotation(2)
R180 = shell_perm_rotation(4)
R270 = shell_perm_rotation(6)
SV = tuple((-i) % 8 for i in range(8))
D4 = {
    "id": R0,
    "r90": R90,
    "r180": R180,
    "r270": R270,
    "reflect_NS": SV,
    "reflect_NE_SW": compose_perm(R90, SV),
    "reflect_EW": compose_perm(R180, SV),
    "reflect_NW_SE": compose_perm(R270, SV),
}


def apply_shell_action(layout: tuple[int, ...], perm: tuple[int, ...]) -> tuple[int, ...]:
    out = [None] * 8
    for old_pos, address in enumerate(layout):
        out[perm[old_pos]] = address
    return tuple(int(x) for x in out)


def gray_family() -> list[dict]:
    provenance: dict[tuple[int, ...], list[str]] = defaultdict(list)
    for name, perm in D4.items():
        base = apply_shell_action(REFERENCE_GRAY, perm)
        provenance[base].append(name)
        complemented = tuple(a ^ 7 for a in base)
        provenance[complemented].append(name + "+address_complement")
    return [
        {"layout": layout, "provenance": sorted(provenance[layout])}
        for layout in sorted(provenance)
    ]


def eca_mirror(a: int) -> int:
    w, c, e = (a >> 2) & 1, (a >> 1) & 1, a & 1
    return (e << 2) | (c << 1) | w


def address_perm(func) -> tuple[int, ...]:
    return tuple(func(a) for a in range(8))


ECA_TRANSFORMS = {
    "id": tuple(range(8)),
    "M": address_perm(eca_mirror),
    "C": address_perm(lambda a: a ^ 7),
    "MC": address_perm(lambda a: eca_mirror(a ^ 7)),
}


def induced_address_perm(layout: tuple[int, ...], shell_perm: tuple[int, ...]) -> tuple[int, ...]:
    a2s = layout_address_to_shell(layout)
    return tuple(layout[shell_perm[a2s[a]]] for a in range(8))


def cycles(perm: tuple[int, ...]) -> list[list[int]]:
    seen = set()
    out = []
    for start in range(len(perm)):
        if start in seen:
            continue
        cyc = []
        x = start
        while x not in seen:
            seen.add(x)
            cyc.append(x)
            x = perm[x]
        out.append(cyc)
    return out


def cycle_type(perm: tuple[int, ...]) -> list[int]:
    return sorted((len(c) for c in cycles(perm)))


def eca_bit(rule: int, left: int, center: int, right: int) -> int:
    return (rule >> (4 * left + 2 * center + right)) & 1


def eca_shrink(bits: tuple[int, ...], rule: int) -> tuple[int, ...]:
    return tuple(eca_bit(rule, bits[i], bits[i + 1], bits[i + 2]) for i in range(len(bits) - 2))


def groovy_center_from_five(bits: tuple[int, ...], rule: int) -> int:
    e1 = eca_shrink(bits, rule)
    ee = eca_shrink(e1, rule)[0]
    d_e = e1[1] ^ ee
    d1 = tuple(bits[i + 1] ^ e1[i] for i in range(3))
    e_d = eca_shrink(d1, rule)[0]
    return d_e ^ e_d


def unary_map(rule: int, b: int) -> int:
    return eca_bit(rule, 0, b, 0)


def unary_power(rule: int, b: int, d: int) -> int:
    x = b
    for _ in range(d):
        x = unary_map(rule, x)
    return x


def evaluate_z0() -> dict:
    rows = {}
    all_agree = True
    failures = []
    for name, program_vars in Z0_ORIENTATIONS.items():
        scalar = truth_table(3, lambda b, pv=program_vars: z0_scalar(b, pv))
        packed = [z0_packed(a, program_vars) for a in range(8)]
        agree = scalar == packed
        poly_truth = anf_from_truth(scalar, 3)
        poly_symbolic = selector_symbolic_anf(3, (1,), program_vars)
        anf_agree = poly_truth == poly_symbolic and truth_from_anf(poly_symbolic, 3) == scalar
        essential_direct = essential_from_truth(scalar, 3)
        summary = anf_summary(poly_truth, ("L", "C", "R"))
        passed = agree and anf_agree and summary["degree"] == 2 and len(essential_direct) == 3
        first_mismatch = next((a for a, (x, y) in enumerate(zip(scalar, packed)) if x != y), None)
        rows[name] = {
            "truth_table": scalar,
            "scalar_packed_agree": agree,
            "anf_paths_agree": anf_agree,
            "anf": summary,
            "direct_essential_inputs": [("L", "C", "R")[i] for i in essential_direct],
            "pass": passed,
        }
        if not passed:
            failures.append({
                "orientation": name,
                "first_physical_patch_assignment": first_mismatch,
                "first_physical_patch_bits_LCR": (list(bits_of(first_mismatch, 3)) if first_mismatch is not None else None),
                "scalar_value": (scalar[first_mismatch] if first_mismatch is not None else None),
                "packed_value": (packed[first_mismatch] if first_mismatch is not None else None),
                "anf_paths_agree": anf_agree,
                "anf": summary,
            })
        all_agree &= passed
    return {"orientations": rows, "failures": failures, "canonical_failure": (failures[0] if failures else None), "pass": all_agree}


def evaluate_z1(layouts: list[dict]) -> dict:
    rows = []
    failures = []
    all_agree = True
    signatures = set()
    for item in layouts:
        layout = tuple(item["layout"])
        scalar = truth_table(9, lambda b, L=layout: z1_scalar(b, L))
        packed = [z1_packed(a, layout) for a in range(512)]
        agree = scalar == packed
        poly_truth = anf_from_truth(scalar, 9)
        poly_symbolic = selector_symbolic_anf(9, ADDRESS_VARIABLES, layout_program_vars(layout))
        anf_agree = poly_truth == poly_symbolic and truth_from_anf(poly_symbolic, 9) == scalar
        essential_direct = essential_from_truth(scalar, 9)
        summary = anf_summary(poly_truth, PATCH_NAMES)
        quartic = summary["monomial_count_by_degree"].get("4", 0)
        signatures.add((summary["degree"], tuple(summary["essential_inputs"]), quartic))
        passed = agree and anf_agree and summary["degree"] == 4 and len(essential_direct) == 9 and quartic == 6
        first_mismatch = next((a for a, (x, y) in enumerate(zip(scalar, packed)) if x != y), None)
        all_agree &= passed
        if not passed:
            failures.append({
                "layout": list(layout),
                "first_physical_patch_assignment": first_mismatch,
                "first_physical_patch_bits": (list(bits_of(first_mismatch, 9)) if first_mismatch is not None else None),
                "scalar_value": (scalar[first_mismatch] if first_mismatch is not None else None),
                "packed_value": (packed[first_mismatch] if first_mismatch is not None else None),
                "anf_paths_agree": anf_agree,
                "anf": summary,
                "direct_essential_inputs": [PATCH_NAMES[i] for i in essential_direct],
            })
        rows.append({
            "layout": list(layout),
            "provenance": item["provenance"],
            "program_var_by_address": [PATCH_NAMES[i] for i in layout_program_vars(layout)],
            "scalar_packed_agree": agree,
            "anf_paths_agree": anf_agree,
            "anf": summary,
            "direct_essential_inputs": [PATCH_NAMES[i] for i in essential_direct],
            "pass": passed,
        })
    return {
        "layouts": rows,
        "layout_count": len(rows),
        "failures": failures,
        "canonical_failure": (failures[0] if failures else None),
        "structure_signatures": [
            {"degree": d, "essential_inputs": list(e), "quartic_terms": q}
            for d, e, q in sorted(signatures)
        ],
        "pass": all_agree,
        "interpretation": (
            "degree k+1 and full essentiality are generic multiplexer properties; "
            "the six quartic terms fingerprint the two address/program overlaps and are layout-independent"
        ),
    }


def evaluate_geometry(layouts: list[dict]) -> dict:
    rows = []
    failures = []
    for item in layouts:
        layout = tuple(item["layout"])
        intersections = []
        action_rows = []
        for shell_name, shell_perm in D4.items():
            induced = induced_address_perm(layout, shell_perm)
            matches = [name for name, target in ECA_TRANSFORMS.items() if induced == target]
            intersections.extend(matches)
            action_rows.append({
                "shell_action": shell_name,
                "shell_cycle_type": cycle_type(shell_perm),
                "induced_address_permutation": list(induced),
                "induced_cycles": cycles(induced),
                "matches_eca_transforms": matches,
            })
            for target in matches:
                if target != "id":
                    failures.append({
                        "layout": list(layout),
                        "shell_action": shell_name,
                        "shell_cycle_type": cycle_type(shell_perm),
                        "induced_address_permutation": list(induced),
                        "induced_cycles": cycles(induced),
                        "candidate_eca_transform": target,
                        "candidate_eca_permutation": list(ECA_TRANSFORMS[target]),
                        "candidate_eca_cycles": cycles(ECA_TRANSFORMS[target]),
                    })
        rows.append({"layout": list(layout), "actions": action_rows, "eca_intersection": sorted(set(intersections))})
    failures.sort(key=lambda w: (tuple(w["layout"]), w["shell_action"], w["candidate_eca_transform"]))
    theorem_controls = {
        name: {"permutation": list(p), "cycle_type": cycle_type(p), "fixed_points": sum(p[i] == i for i in range(8))}
        for name, p in ECA_TRANSFORMS.items()
    }
    shell_controls = {
        name: {"permutation": list(p), "cycle_type": cycle_type(p), "fixed_points": sum(p[i] == i for i in range(8))}
        for name, p in D4.items()
    }
    return {
        "eca_transform_controls": theorem_controls,
        "shell_action_controls": shell_controls,
        "layouts": rows,
        "failures": failures,
        "canonical_failure": (failures[0] if failures else None),
        "pass_identity_only": not failures,
    }


def evaluate_commutator_floor() -> dict:
    rows = {}
    passed = True
    for rule, expected in EXPECTED_GROOVY.items():
        outputs = [groovy_center_from_five(bits_of(a, 5), rule) for a in range(32)]
        unique = sorted(set(outputs))
        ok = unique == [expected]
        rows[str(rule)] = {"expected": expected, "unique_outputs_over_32_five_cell_windows": unique, "pass": ok}
        passed &= ok
    return {"rules": rows, "pass": passed}


def evaluate_axial_controls() -> dict:
    rows = {}
    passed = True
    for rule in CENTER_ONLY:
        powers = {str(d): [unary_power(rule, b, d) for b in (0, 1)] for d in range(1, 5)}
        image = {unary_map(rule, b) for b in (0, 1)}
        u = {b: eca_bit(rule, b, b, b) for b in (0, 1)}
        interface_pass = all(u[y] == y for y in image)
        expected_interface = rule != 51
        if rule == 204:
            expected_powers = all(powers[str(d)] == [0, 1] for d in range(1, 5))
        elif rule == 51:
            expected_powers = all(powers[str(d)] == ([1, 0] if d % 2 else [0, 1]) for d in range(1, 5))
        elif rule == 0:
            expected_powers = all(powers[str(d)] == [0, 0] for d in range(1, 5))
        else:
            expected_powers = all(powers[str(d)] == [1, 1] for d in range(1, 5))
        ok = expected_powers and interface_pass == expected_interface
        passed &= ok
        rows[str(rule)] = {
            "f_power_by_dimension_1_to_4_on_inputs_0_1": powers,
            "u_on_0_1": [u[0], u[1]],
            "attainable_after_one_pass": sorted(image),
            "interface_fixed_output_criterion": interface_pass,
            "pass": ok,
        }
    return {"rules": rows, "pass": passed, "rule51_note": "dimension parity is a dynamical corollary; exclusion is the u=NOT fixed-point failure"}


def main_evaluation() -> dict:
    imported = assert_accepted_inputs()
    layouts = gray_family()
    z0 = evaluate_z0()
    z1 = evaluate_z1(layouts)
    geometry = evaluate_geometry(layouts)
    commutator = evaluate_commutator_floor()
    axial = evaluate_axial_controls()

    overlap = {
        "formula": "max(0, k + 2^k - |P|)",
        "Z0": {"k": 1, "patch_sites": 3, "minimum_overlap": 0, "attained_overlap": 0},
        "Z1": {"k": 3, "patch_sites": 9, "minimum_overlap": 2, "attained_overlap": 2, "dual_role_sites": ["W", "E"]},
    }
    p3 = overlap["Z0"]["minimum_overlap"] == overlap["Z0"]["attained_overlap"] and overlap["Z1"]["minimum_overlap"] == overlap["Z1"]["attained_overlap"]
    routing = {"d": 2, "program_bits_8d": 16, "outer_shell_cells_3d_radius1": 26, "below_shell_count": 16 < 26,
               "scope": "accepted factorized routing family only; not compression of an arbitrary 512-bit 2D truth table"}

    complete_0d_floor = sorted(2 * f0 + f1 for f0 in (0, 1) for f1 in (0, 1)) == [0, 1, 2, 3]
    summary = {
        "P1_complete_0D_floor": complete_0d_floor,
        "P2_commutator_floor": commutator["pass"],
        "P3_minimum_role_overlap": p3,
        "P4_common_selector_local_structure": z0["pass"] and z1["pass"],
        "P5_no_nontrivial_Gray_ECA_symmetry_identification": geometry["pass_identity_only"],
        "P6_corrected_axial_deduction": axial["pass"],
        "P7_scoped_routing_storage_comparison": routing["below_shell_count"],
        "P8_stateful_execution_deferred": True,
    }
    return {
        "protocol": "zero-dimensional-base-20260912",
        "schema": 1,
        "source_hashes": {
            "script": sha256(pathlib.Path(__file__)),
            "protocol": sha256(PROTOCOL),
            "history_algebra_result": sha256(HISTORY),
            "shared_state_audit": sha256(SHARED_AUDIT),
            "shared_state_local": sha256(SHARED_LOCAL),
            "guard_free_axial_result": sha256(AXIAL),
            "editable_routing_result": sha256(ROUTING),
        },
        "accepted_input_provenance": imported,
        "canonical_ordering": {
            "z0_patch_variables": ["L", "C", "R"],
            "z1_patch_variables": list(PATCH_NAMES),
            "shell_clockwise_from_north": list(SHELL_NAMES),
            "reference_gray_addresses": [format(a, "03b") for a in REFERENCE_GRAY],
            "layouts": "lexicographic by eight-address tuple after D4/complement deduplication",
            "shell_actions": list(D4),
            "eca_transforms": list(ECA_TRANSFORMS),
        },
        "P1_0D_floor": {
            "unary_truth_words_00_01_10_11": [0, 1, 2, 3],
            "center_only_ECA_rules": [0, 204, 51, 255],
            "complete_binary_unary_rulespace": complete_0d_floor,
            "all_affine": True,
        },
        "P2_commutator_floor": commutator,
        "P3_role_overlap": overlap,
        "P4_selector_structure": {"Z0": z0, "Z1": z1},
        "P5_geometry": geometry,
        "P6_axial": axial,
        "P7_routing_storage": routing,
        "P8_stateful_execution": {"status": "deferred", "claim": "no repeated-execution claim in this unit"},
        "summary": summary,
        "interpretation_scope": {
            "positive_ceiling": "local overlap-permitted selector audit across the first two law/state cardinality matches",
            "nonclaims": [
                "no stateful or repeated dynamical dimensional lift",
                "no unique or naturally selected layout",
                "no arbitrary 2D-to-3D shell encoding",
                "no compression of arbitrary 512-bit 2D rules",
                "no intrinsic dimension, self-assembly, endogenous control, spacetime emergence, physics, metaphysics, or prime connection",
            ],
        },
    }


def self_test() -> None:
    address_vars = (0, 1)
    program_vars = (2, 3, 4, 5)

    def toy(bits: tuple[int, ...]) -> int:
        address = 2 * bits[0] + bits[1]
        return bits[program_vars[address]]

    table = truth_table(6, toy)
    anf_a = anf_from_truth(table, 6)
    anf_b = selector_symbolic_anf(6, address_vars, program_vars)
    assert anf_a == anf_b
    assert truth_from_anf(anf_b, 6) == table
    assert essential_from_truth(table, 6) == tuple(range(6))
    assert max(m.bit_count() for m in anf_a) == 3

    p = (1, 2, 3, 0)
    assert cycle_type(p) == [4]
    assert compose_perm(p, p) == (2, 3, 0, 1)
    print("implementation self-test passed (out-of-domain k=2 toy selector; no canonical result written)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true", help="run only out-of-domain implementation checks; write no result")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    result = main_evaluation()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result["summary"], sort_keys=True))
    print("written", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
