#!/usr/bin/env python3
"""Verifier for the frozen relational-rank protocol.

Protocol: docs/research/protocols/relational-rank-20260912.md
Gate 1: Claude Code / Fable 5.1 approved exact gathering head
803a775715a2a8bfe4a3214a43186f81c6aab431 on 2026-09-12.

This file is the implementation-only stage. Committing it does not execute the
frozen 256-rule x 512-patch audit and does not create a canonical result.
Running without --self-test performs the complete frozen audit and writes
results/relational_rank_20260912.json. --self-test uses only synthetic
out-of-domain Boolean functions and writes nothing.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "docs/research/protocols/relational-rank-20260912.md"
OUT = ROOT / "results/relational_rank_20260912.json"
AXIAL = ROOT / "results/guard_free_axial_lift_20260910.json"
TRANSVERSE = ROOT / "results/transverse_freedom_20260911.json"
INTERVENTION = ROOT / "results/intervention_axis_20260911.json"

# Exact accepted Git blobs, frozen before implementation.
ACCEPTED_GIT_BLOBS = {
    "protocol": "06e7a12222c8ba62430eb0c2c055971ff3d5c028",
    "guard_free_axial": "872ada3cdbfb581a3edae536bfe3be4363084ec2",
    "transverse_freedom": "ff6e7a56c4e5616e19a20edc8f4249d12eb23dce",
    "intervention_axis": "7a229b925d7f4165e63573d41515402fe1666938",
}

# ECA coordinates and 3x3 target patch order. Axis 0 / x acts first;
# axis 1 / y acts second, matching the accepted axial constructor.
SOURCE_OFFSETS = (-1, 0, 1)
PATCH_OFFSETS = tuple((x, y) for y in (-1, 0, 1) for x in (-1, 0, 1))
PATCH_INDEX = {offset: i for i, offset in enumerate(PATCH_OFFSETS)}

EXPECTED_SOURCE_RANK0 = {0, 51, 204, 255}
EXPECTED_TARGET_RANK1 = {15, 85, 170, 240}
EXPECTED_TARGET_RANK0 = EXPECTED_SOURCE_RANK0
EXPECTED_TARGET_RANK2 = set(range(256)) - EXPECTED_TARGET_RANK0 - EXPECTED_TARGET_RANK1


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob_sha(path: pathlib.Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def assert_accepted_inputs() -> dict[str, dict[str, str]]:
    paths = {
        "protocol": PROTOCOL,
        "guard_free_axial": AXIAL,
        "transverse_freedom": TRANSVERSE,
        "intervention_axis": INTERVENTION,
    }
    out = {}
    for key, path in paths.items():
        actual = git_blob_sha(path)
        expected = ACCEPTED_GIT_BLOBS[key]
        if actual != expected:
            raise AssertionError(f"accepted input drift for {key}: {actual} != {expected}")
        out[key] = {
            "path": str(path.relative_to(ROOT)),
            "git_blob_sha": actual,
            "sha256": sha256(path),
        }
    return out


def eca_bit(rule: int, left: int, center: int, right: int) -> int:
    return (rule >> (4 * left + 2 * center + right)) & 1


def eca_truth_dict(rule: int) -> dict[tuple[bool, bool, bool], bool]:
    # Independent representation: textual truth word plus Boolean tuple keys.
    word = format(rule, "08b")[::-1]
    return {
        tuple(c == "1" for c in format(i, "03b")): word[i] == "1"
        for i in range(8)
    }


def source_essential_primary(rule: int) -> tuple[int, ...]:
    essential = []
    for axis in range(3):
        found = False
        for bits in itertools.product((0, 1), repeat=3):
            flipped = list(bits)
            flipped[axis] ^= 1
            if eca_bit(rule, *bits) != eca_bit(rule, *flipped):
                found = True
                break
        if found:
            essential.append(SOURCE_OFFSETS[axis])
    return tuple(essential)


def source_essential_reference(rule: int) -> tuple[int, ...]:
    truth = eca_truth_dict(rule)
    essential = []
    for axis in range(3):
        found = False
        for bits in itertools.product((False, True), repeat=3):
            flipped = list(bits)
            flipped[axis] = not flipped[axis]
            if truth[tuple(bits)] != truth[tuple(flipped)]:
                found = True
                break
        if found:
            essential.append(SOURCE_OFFSETS[axis])
    return tuple(essential)


def bits9(word: int) -> tuple[int, ...]:
    return tuple((word >> i) & 1 for i in range(9))


def target_primary(rule: int, patch_bits: tuple[int, ...]) -> int:
    # Collapse each y-row horizontally, then collapse those three values vertically.
    rows = []
    for y in (-1, 0, 1):
        rows.append(
            eca_bit(
                rule,
                patch_bits[PATCH_INDEX[(-1, y)]],
                patch_bits[PATCH_INDEX[(0, y)]],
                patch_bits[PATCH_INDEX[(1, y)]],
            )
        )
    return eca_bit(rule, rows[0], rows[1], rows[2])


def target_reference(rule: int, patch_bits: tuple[int, ...]) -> int:
    # Independent Boolean tuple dictionary and coordinate-map evaluator.
    truth = eca_truth_dict(rule)
    field = {offset: bool(patch_bits[i]) for i, offset in enumerate(PATCH_OFFSETS)}
    intermediate = {}
    for y in (-1, 0, 1):
        intermediate[y] = truth[(field[(-1, y)], field[(0, y)], field[(1, y)])]
    return int(truth[(intermediate[-1], intermediate[0], intermediate[1])])


def essential_offsets_from_table(table: list[int]) -> tuple[tuple[int, int], ...]:
    essential = []
    for i, offset in enumerate(PATCH_OFFSETS):
        bit = 1 << i
        if any(table[w] != table[w | bit] for w in range(512) if not (w & bit)):
            essential.append(offset)
    return tuple(essential)


def product_expected(source_essential: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    # Preserve the same y-major canonical order used by PATCH_OFFSETS.
    source = set(source_essential)
    return tuple(offset for offset in PATCH_OFFSETS if offset[0] in source and offset[1] in source)


def rank1d(essential: tuple[int, ...]) -> int:
    return int(any(v != 0 for v in essential))


def rank2d(essential: tuple[tuple[int, int], ...]) -> int:
    vectors = [v for v in essential if v != (0, 0)]
    if not vectors:
        return 0
    for i, (x1, y1) in enumerate(vectors):
        for x2, y2 in vectors[i + 1 :]:
            if x1 * y2 - y1 * x2 != 0:
                return 2
    return 1


def target_formula_control(rule: int) -> dict:
    table = [target_primary(rule, bits9(w)) for w in range(512)]
    if rule in (0, 255):
        expected = [rule // 255] * 512
        label = "constant"
    elif rule == 204:
        expected = [bits9(w)[PATCH_INDEX[(0, 0)]] for w in range(512)]
        label = "center"
    elif rule == 51:
        expected = [1 ^ bits9(w)[PATCH_INDEX[(0, 0)]] for w in range(512)]
        label = "not-center"
    elif rule in (170, 85):
        # R then R => southeast diagonal; 85 complements at both passes,
        # so the complements cancel.
        expected = [bits9(w)[PATCH_INDEX[(1, 1)]] for w in range(512)]
        label = "southeast-diagonal"
    elif rule in (240, 15):
        # L then L => northwest diagonal; 15 complements at both passes.
        expected = [bits9(w)[PATCH_INDEX[(-1, -1)]] for w in range(512)]
        label = "northwest-diagonal"
    elif rule == 90:
        corners = ((-1, -1), (1, -1), (-1, 1), (1, 1))
        expected = [sum(bits9(w)[PATCH_INDEX[p]] for p in corners) & 1 for w in range(512)]
        label = "four-corner-parity"
    elif rule == 150:
        expected = [sum(bits9(w)) & 1 for w in range(512)]
        label = "nine-site-parity"
    else:
        raise ValueError(rule)
    return {"label": label, "pass": table == expected}


def load_axial_sets() -> dict[str, set[int]]:
    data = json.loads(AXIAL.read_text())
    keys = {
        "replication_compatible_66": "all_interfaces_rules",
        "axis_commuting_24": "axis_permutation_equivariant_rules",
        "both_14": "compatible_and_axis_permutation_equivariant_rules",
        "affine_16": "affine_commutation_controls",
    }
    expected_sizes = {
        "replication_compatible_66": 66,
        "axis_commuting_24": 24,
        "both_14": 14,
        "affine_16": 16,
    }
    out = {}
    for label, key in keys.items():
        values = set(map(int, data[key]))
        if len(values) != expected_sizes[label]:
            raise AssertionError(f"accepted axial set {label} has unexpected size {len(values)}")
        out[label] = values
    return out


def cross_tabs(records: list[dict], axial_sets: dict[str, set[int]]) -> dict:
    result = {}
    for label, rules in axial_sets.items():
        ranks = Counter(records[r]["target_rho_C"] for r in sorted(rules))
        result[label] = {
            "rule_count": len(rules),
            "target_rho_C_counts": {str(k): ranks.get(k, 0) for k in (0, 1, 2)},
            "rules_by_target_rho_C": {
                str(k): [r for r in sorted(rules) if records[r]["target_rho_C"] == k]
                for k in (0, 1, 2)
            },
        }
    return result


def translation_controls() -> dict:
    # Theorem-backed bookkeeping over declared infinite families; finite tori do
    # not define rho_T.
    return {
        "T0_binary_0D": {
            "ambient_lattice": "one-point",
            "rho_T": 0,
            "reason": "translation group trivial",
        },
        "T1_full_shifts": {
            "Z": {"H_generators": [[1]], "K_generators": [], "rho_T": 1},
            "Z2": {"H_generators": [[1, 0], [0, 1]], "K_generators": [], "rho_T": 2},
        },
        "T2_literal_replication_1D_to_2D": {
            "source_rho_T": 1,
            "copied_image_rho_T": 1,
            "full_target_rho_T": 2,
            "new_axis_generator_in_pointwise_kernel": [0, 1],
        },
        "T3_finite_product_alphabet_on_Z": {
            "rho_T": 1,
            "statement": "finite per-site coordinate/alphabet multiplication introduces no new lattice translation generator",
        },
        "T4_channel_pair": {
            "anchored_S_m": {
                "H_generators": [[1, 0]],
                "K_generators": [],
                "rho_T": 1,
            },
            "translation_closure_Sprime_m": {
                "H_generators": [[1, 0], [0, 1]],
                "K_generators": [],
                "rho_T": 2,
            },
            "interpretation": "rho_T changes with the declared family/anchoring convention; it is presentation-relative",
        },
    }


def evaluate() -> dict:
    provenance = assert_accepted_inputs()
    axial_sets = load_axial_sets()
    records = []
    primary_hash = hashlib.sha256()
    reference_hash = hashlib.sha256()
    discrepancies = []

    for rule in range(256):
        source_a = source_essential_primary(rule)
        source_b = source_essential_reference(rule)
        if source_a != source_b:
            raise AssertionError(f"source essential disagreement rule {rule}: {source_a} != {source_b}")

        primary = [target_primary(rule, bits9(w)) for w in range(512)]
        reference = [target_reference(rule, bits9(w)) for w in range(512)]
        if primary != reference:
            first = next(i for i, (a, b) in enumerate(zip(primary, reference)) if a != b)
            raise AssertionError(f"target evaluator disagreement rule {rule} patch {first}")
        primary_hash.update(bytes(primary))
        reference_hash.update(bytes(reference))

        actual_offsets = essential_offsets_from_table(primary)
        expected_offsets = product_expected(source_a)
        theorem_ok = actual_offsets == expected_offsets
        if not theorem_ok:
            discrepancies.append({
                "rule": rule,
                "source_essential_offsets": list(source_a),
                "expected_target_essential_offsets": [list(v) for v in expected_offsets],
                "actual_target_essential_offsets": [list(v) for v in actual_offsets],
            })

        source_rank = rank1d(source_a)
        target_rank = rank2d(actual_offsets)
        records.append({
            "rule": rule,
            "source_essential_offsets": list(source_a),
            "source_rho_C": source_rank,
            "target_essential_offsets": [list(v) for v in actual_offsets],
            "target_rho_C": target_rank,
            "product_theorem_regression": theorem_ok,
        })

    if primary_hash.digest() != reference_hash.digest():
        raise AssertionError("independent target checksums disagree")

    source_rank0 = {r["rule"] for r in records if r["source_rho_C"] == 0}
    target_rank0 = {r["rule"] for r in records if r["target_rho_C"] == 0}
    target_rank1 = {r["rule"] for r in records if r["target_rho_C"] == 1}
    target_rank2 = {r["rule"] for r in records if r["target_rho_C"] == 2}

    source_class_ok = source_rank0 == EXPECTED_SOURCE_RANK0
    target_class_ok = (
        target_rank0 == EXPECTED_TARGET_RANK0
        and target_rank1 == EXPECTED_TARGET_RANK1
        and target_rank2 == EXPECTED_TARGET_RANK2
    )

    controls = {
        str(rule): target_formula_control(rule)
        for rule in (0, 51, 204, 255, 15, 85, 170, 240, 90, 150)
    }
    formula_controls_ok = all(item["pass"] for item in controls.values())

    transitions = Counter(f'{r["source_rho_C"]}->{r["target_rho_C"]}' for r in records)
    if transitions.get("1->0", 0):
        raise AssertionError("forbidden 1->0 transition appeared")

    summary = {
        "P1_translation_rank_floor_and_full_shifts": True,
        "P2_literal_replication_preserves_inherited_translation_rank": True,
        "P3_product_alphabet_and_channel_presentation_controls": True,
        "P4_source_ECA_causal_rank_control": source_class_ok,
        "P5_ordered_axis_product_theorem_regression": not discrepancies and target_class_ok,
        "P6_analytic_target_formula_controls": formula_controls_ok,
        "P7_exact_cross_tabs_reported": True,
        "P8_relational_lift_profile_bookkeeping_only": True,
    }

    return {
        "protocol": "relational-rank-20260912",
        "schema": 1,
        "gate1_approved_gathering_head": "803a775715a2a8bfe4a3214a43186f81c6aab431",
        "source_hashes": {
            "script": sha256(pathlib.Path(__file__)),
            "protocol": sha256(PROTOCOL),
            "guard_free_axial": sha256(AXIAL),
            "transverse_freedom": sha256(TRANSVERSE),
            "intervention_axis": sha256(INTERVENTION),
        },
        "accepted_input_provenance": provenance,
        "canonical_ordering": {
            "rules": "ascending 0..255",
            "source_offsets_LCR": list(SOURCE_OFFSETS),
            "target_patch_offsets": [list(v) for v in PATCH_OFFSETS],
            "patch_words": "ascending 0..511; bit i is target_patch_offsets[i]",
            "axis_order": "x/axis0 first, y/axis1 second",
            "discrepancies": "ascending rule and target_patch_offsets order",
        },
        "translation_rank_controls": translation_controls(),
        "causal_rank": {
            "source_rank0_rules": sorted(source_rank0),
            "target_rank0_rules": sorted(target_rank0),
            "target_rank1_rules": sorted(target_rank1),
            "target_rank2_rules": sorted(target_rank2),
            "transition_counts": dict(sorted(transitions.items())),
            "records": records,
            "product_theorem_discrepancies": discrepancies,
            "primary_sha256": primary_hash.hexdigest(),
            "independent_sha256": reference_hash.hexdigest(),
        },
        "analytic_formula_controls": controls,
        "accepted_axial_cross_tabs": cross_tabs(records, axial_sets),
        "negative_information_result": (
            "for the accepted ordered-axis constructor, target rho_C is fully determined by the source essential-offset set; "
            "the relational-lift profile is bookkeeping and supplies no additional rule classification"
        ),
        "relational_lift_profiles": {
            "0D_to_1D_center_only": [0, 0, 1, 0],
            "1D_to_2D": {
                "prefix": [1, 1, 2],
                "target_rho_C_by_rule": [r["target_rho_C"] for r in records],
            },
        },
        "summary": summary,
        "interpretation_scope": {
            "establishes": [
                "declared-family translation-rank controls",
                "ordered-axis essential-offset product theorem regression",
                "presentation sensitivity of rho_T",
                "descriptive exact cross-tabs against accepted axial source families",
            ],
            "nonclaims": [
                "no intrinsic or representation-independent dimension",
                "no unique theory of space or dimensionality",
                "no self-assembly, endogenous control, spacetime emergence, physics, or metaphysics",
                "no mathematical equivalence to Buddhist dependent origination",
                "no prime or 8n+1 connection",
            ],
        },
    }


def self_test() -> None:
    # Synthetic, out-of-domain tests of rank/essential machinery only.
    assert rank2d(()) == 0
    assert rank2d(((1, 1),)) == 1
    assert rank2d(((1, 0), (0, 1))) == 2
    assert rank2d(((-1, -1), (1, 1))) == 1

    # A four-variable toy function a XOR (b AND c) with a dummy d.
    table = []
    for word in range(16):
        a, b, c, _d = ((word >> i) & 1 for i in range(4))
        table.append(a ^ (b & c))
    essential = []
    for i in range(4):
        bit = 1 << i
        if any(table[w] != table[w | bit] for w in range(16) if not (w & bit)):
            essential.append(i)
    assert essential == [0, 1, 2]
    print("implementation self-test passed (synthetic out-of-domain functions; no canonical result written)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true", help="run only synthetic implementation checks; write no result")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    result = evaluate()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result["summary"], sort_keys=True))
    print("written", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
