#!/usr/bin/env python3
"""Exact intrinsic commutator-jet experiment for ECA Rules 110 and 62.

A0 = D = I xor H
A{k+1} = A{k} o H xor H o A{k}

Protocol:
  docs/research/protocols/commutator-jet-20261007.md
"""
from __future__ import annotations

import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

RULES = (110, 62)
WIDTHS = (8, 10, 12, 14, 16)
MAX_LEVEL = 5
OUT = Path("results/commutator_jet_20261007.json")


def eca_map(rule: int, n: int) -> np.ndarray:
    states = np.arange(1 << n, dtype=np.uint32)
    shifts = np.arange(n, dtype=np.uint32)
    bits = ((states[:, None] >> shifts) & 1).astype(np.uint8)
    idx = (np.roll(bits, 1, axis=1) << 2) | (bits << 1) | np.roll(bits, -1, axis=1)
    lut = np.array([(rule >> i) & 1 for i in range(8)], dtype=np.uint8)
    out = lut[idx]
    weights = 1 << np.arange(n, dtype=np.uint64)
    return (out.astype(np.uint64) * weights).sum(axis=1).astype(np.uint32)


def tower_maps(rule: int, n: int, max_level: int = MAX_LEVEL + 1):
    h = eca_map(rule, n)
    states = np.arange(1 << n, dtype=np.uint32)
    levels = [states ^ h]
    for _ in range(max_level):
        a = levels[-1]
        levels.append(a[h] ^ h[a])
    return h, levels


def labels(cols: list[np.ndarray]) -> np.ndarray:
    matrix = np.stack(cols, axis=1)
    _, inverse = np.unique(matrix, axis=0, return_inverse=True)
    return inverse.astype(np.int32)


def entropy_from_labels(x: np.ndarray) -> float:
    counts = np.bincount(x)
    counts = counts[counts > 0].astype(np.float64)
    p = counts / counts.sum()
    return float(-(p * np.log2(p)).sum())


def fiber_histogram(cols: list[np.ndarray]) -> dict[str, int]:
    matrix = np.stack(cols, axis=1)
    _, counts = np.unique(matrix, axis=0, return_counts=True)
    return {str(k): int(v) for k, v in sorted(Counter(counts.tolist()).items())}


def first_factor_witness(prefix: list[np.ndarray], target: np.ndarray):
    matrix = np.stack(prefix, axis=1)
    order = np.lexsort(matrix.T[::-1])
    prev = None
    prev_state = None
    prev_target = None
    for state in order:
        key = tuple(int(x) for x in matrix[state])
        y = int(target[state])
        if key == prev and y != prev_target:
            return {
                "state_x": int(prev_state),
                "state_y": int(state),
                "shared_prefix": list(key),
                "target_x": int(prev_target),
                "target_y": y,
            }
        prev = key
        prev_state = int(state)
        prev_target = y
    return None


def step_line(a: np.ndarray, rule: int) -> np.ndarray:
    left = np.concatenate(([0], a[:-1]))
    right = np.concatenate((a[1:], [0]))
    idx = (left << 2) | (a << 1) | right
    lut = np.array([(rule >> i) & 1 for i in range(8)], dtype=np.uint8)
    return lut[idx]


def local_level_truth(rule: int, level: int) -> np.ndarray:
    radius = level + 1
    width = 2 * radius + 1
    out = np.zeros(1 << width, dtype=np.uint8)
    pad = level + 4

    for word in range(1 << width):
        core = np.array([(word >> i) & 1 for i in range(width)], dtype=np.uint8)
        source = np.pad(core, (pad, pad))
        source_rows = [source]
        for _ in range(level + 2):
            source_rows.append(step_line(source_rows[-1], rule))

        temporal = [
            source_rows[t] ^ source_rows[t + 1]
            for t in range(len(source_rows) - 1)
        ]
        levels = [temporal]
        for _ in range(level):
            prev = levels[-1]
            levels.append([
                prev[t + 1] ^ step_line(prev[t], rule)
                for t in range(len(prev) - 1)
            ])

        out[word] = levels[level][0][pad + radius]
    return out


def minimum_radius(truth: np.ndarray, declared_radius: int) -> int:
    width = 2 * declared_radius + 1
    for radius in range(declared_radius + 1):
        left = declared_radius - radius
        right = declared_radius + radius
        seen = {}
        ok = True
        for word, value in enumerate(truth):
            key = 0
            pos = 0
            for i in range(left, right + 1):
                key |= ((word >> i) & 1) << pos
                pos += 1
            old = seen.get(key)
            if old is not None and old != int(value):
                ok = False
                break
            seen[key] = int(value)
        if ok:
            return radius
    return declared_radius


def anf_summary(truth: np.ndarray) -> dict:
    coeff = truth.copy().astype(np.uint8)
    variables = int(round(math.log2(len(coeff))))
    for i in range(variables):
        for mask in range(1 << variables):
            if mask & (1 << i):
                coeff[mask] ^= coeff[mask ^ (1 << i)]

    degree_counts = Counter()
    for mask, value in enumerate(coeff):
        if value:
            degree_counts[mask.bit_count()] += 1
    return {
        "degree": max(degree_counts, default=0),
        "term_count": int(sum(degree_counts.values())),
        "terms_by_degree": {
            str(k): int(v) for k, v in sorted(degree_counts.items())
        },
    }


def local_prefix_factor(rule: int, end_level: int, radius: int):
    """A0..A_end neighborhood -> A_{end+1} at center, exact full-line window."""
    source_radius = max(end_level + 2, radius + end_level + 1)
    width = 2 * source_radius + 1
    rows = 1 << width

    # For the frozen radius<=3 / end<=4 budget, direct enumeration is small.
    table = {}
    pad = source_radius + end_level + 5
    for word in range(rows):
        core = np.array([(word >> i) & 1 for i in range(width)], dtype=np.uint8)
        source = np.pad(core, (pad, pad))
        source_rows = [source]
        for _ in range(end_level + 3):
            source_rows.append(step_line(source_rows[-1], rule))

        temporal = [
            source_rows[t] ^ source_rows[t + 1]
            for t in range(len(source_rows) - 1)
        ]
        levels = [temporal]
        for _ in range(end_level + 1):
            prev = levels[-1]
            levels.append([
                prev[t + 1] ^ step_line(prev[t], rule)
                for t in range(len(prev) - 1)
            ])

        center = pad + source_radius
        key = tuple(
            int(levels[level][0][center + offset])
            for offset in range(-radius, radius + 1)
            for level in range(end_level + 1)
        )
        target = int(levels[end_level + 1][0][center])
        old = table.get(key)
        if old is not None and old[0] != target:
            return {
                "pass": False,
                "source_width": width,
                "contexts_before_conflict": len(table),
                "witness": {
                    "word_x": old[1],
                    "word_y": word,
                    "shared_context": list(key),
                    "target_x": old[0],
                    "target_y": target,
                },
            }
        table[key] = (target, word)

    return {
        "pass": True,
        "source_width": width,
        "distinct_contexts": len(table),
        "witness": None,
    }


def derivative_rule(rule: int) -> int:
    return rule ^ 204


def reflect_rule(rule: int) -> int:
    out = 0
    for idx in range(8):
        l, c, r = (idx >> 2) & 1, (idx >> 1) & 1, idx & 1
        ridx = (r << 2) | (c << 1) | l
        out |= ((rule >> idx) & 1) << ridx
    return out


def conjugate_rule(rule: int) -> int:
    out = 0
    for idx in range(8):
        l, c, r = (idx >> 2) & 1, (idx >> 1) & 1, idx & 1
        cidx = ((1 - l) << 2) | ((1 - c) << 1) | (1 - r)
        out |= (1 ^ ((rule >> cidx) & 1)) << idx
    return out


def main() -> None:
    result = {
        "schema": "commutator-jet-v1",
        "date": "2026-10-07",
        "protocol": "docs/research/protocols/commutator-jet-20261007.md",
        "definitions": {
            "A0": "D=I xor H",
            "recurrence": "A{k+1}=A{k} o H xor H o A{k}",
            "names": ["D", "G", "Q", "R", "A4", "A5"],
        },
        "rules": {},
        "cross_rule": {},
        "cadence_bridge": {
            "identity": (
                "C_{H^2}(A)=C_H(C_H(A)) xor "
                "B_H(H o A,C_H(A)) xor H(0)"
            ),
            "zero_preserving_specialization": (
                "C_{H^2}(A)=C_H^2(A) xor B_H(H o A,C_H(A))"
            ),
        },
        "exploratory_G_anchored": {
            "status": "post-hoc diagnostic; not a frozen protocol gate",
            "rules": {},
        },
    }

    local_truth = {}
    for rule in RULES:
        local_rows = []
        for level in range(MAX_LEVEL + 1):
            truth = local_level_truth(rule, level)
            local_truth[(rule, level)] = truth
            anf = anf_summary(truth)
            local_rows.append({
                "level": level,
                "name": result["definitions"]["names"][level],
                "declared_radius": level + 1,
                "minimum_radius": minimum_radius(truth, level + 1),
                "activity_fraction": float(truth.mean()),
                **anf,
            })

        finite = {}
        for n in WIDTHS:
            h, levels = tower_maps(rule, n, MAX_LEVEL + 1)
            width_rows = []
            for k in range(0, 5):
                current_labels = labels(levels[: k + 1])
                h_current = entropy_from_labels(current_labels)
                joint_labels = labels(levels[: k + 2])
                conditional_next = entropy_from_labels(joint_labels) - h_current
                witness = (
                    None
                    if abs(conditional_next) < 1e-12
                    else first_factor_witness(levels[: k + 1], levels[k + 1])
                )
                width_rows.append({
                    "end_level": k,
                    "prefix_names": result["definitions"]["names"][: k + 1],
                    "class_count": int(len(np.unique(current_labels))),
                    "source_bits_forgotten": n - h_current,
                    "next_level_conditional_bits": conditional_next,
                    "global_factor": abs(conditional_next) < 1e-12,
                    "fiber_histogram": fiber_histogram(levels[: k + 1]),
                    "witness": witness,
                })

            finite[str(n)] = width_rows

        # Locality only for first globally closed D-anchored prefix, evaluated
        # against the full-line local source language.
        first_closed = next(
            (
                row["end_level"]
                for row in finite[str(WIDTHS[-1])]
                if row["global_factor"]
            ),
            None,
        )
        locality = []
        if first_closed is not None:
            for radius in range(4):
                rec = local_prefix_factor(rule, first_closed, radius)
                rec["radius"] = radius
                locality.append(rec)
                if rec["pass"]:
                    break

        result["rules"][str(rule)] = {
            "local_levels": local_rows,
            "finite_prefix": finite,
            "first_closed_D_prefix_at_n16": first_closed,
            "full_line_locality_for_that_prefix": locality,
        }

        # Explicitly post-hoc: start the jet at G rather than D, because this
        # is the user's latent-complement question.
        g_finite = {}
        for n in WIDTHS:
            h, levels = tower_maps(rule, n, MAX_LEVEL + 2)
            rows = []
            for end in range(1, MAX_LEVEL + 1):
                current = labels(levels[1 : end + 1])
                h_current = entropy_from_labels(current)
                extended = labels(levels[1 : end + 2])
                conditional = entropy_from_labels(extended) - h_current
                rows.append({
                    "end_level": end,
                    "prefix_names": result["definitions"]["names"][1 : end + 1],
                    "class_count": int(len(np.unique(current))),
                    "source_bits_forgotten": n - h_current,
                    "next_level_conditional_bits": conditional,
                    "global_factor": abs(conditional) < 1e-12,
                    "fiber_histogram": fiber_histogram(levels[1 : end + 1]),
                })
            g_finite[str(n)] = rows

        result["exploratory_G_anchored"]["rules"][str(rule)] = g_finite

    d110 = derivative_rule(110)
    d62 = derivative_rule(62)
    result["cross_rule"] = {
        "derivative_rules": {"110": d110, "62": d62},
        "D_rules_reflect_conjugate": reflect_rule(conjugate_rule(d110)) == d62,
        "note": (
            "D_110 is ECA 162 and D_62 is ECA 242; they are related by "
            "reflection plus state-complement conjugacy, explaining the matched "
            "D-level finite-ring fiber statistics."
        ),
    }

    # Cadence-two residual versus the one-step R field: exact local truth-table
    # comparison on the complete radius-four source domain.
    bridge_activity = {}
    for rule in RULES:
        width = 9
        q2 = np.zeros(1 << width, dtype=np.uint8)
        rfield = local_truth[(rule, 3)]
        pad = 8
        for word in range(1 << width):
            core = np.array([(word >> i) & 1 for i in range(width)], dtype=np.uint8)
            source = np.pad(core, (pad, pad))
            rows = [source]
            for _ in range(6):
                rows.append(step_line(rows[-1], rule))
            d = [rows[t] ^ rows[t + 1] for t in range(5)]
            g = [
                d[t + 1] ^ step_line(d[t], rule)
                for t in range(4)
            ]
            center = pad + 4
            q2[word] = (
                g[2][center]
                ^ step_line(step_line(g[0], rule), rule)[center]
            )
        interaction = q2 ^ rfield
        bridge_activity[str(rule)] = {
            "C_H2_G_activity": float(q2.mean()),
            "R_activity": float(rfield.mean()),
            "polarization_correction_activity": float(interaction.mean()),
            "fraction_C_H2_G_equals_R": float((q2 == rfield).mean()),
            "C_H2_G_anf": anf_summary(q2),
            "polarization_correction_anf": anf_summary(interaction),
        }
    result["cadence_bridge"]["exact_rule_activity"] = bridge_activity

    result["source_hashes"] = {
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        rule: {
            "D_prefix_close": result["rules"][str(rule)]["first_closed_D_prefix_at_n16"],
            "locality": result["rules"][str(rule)]["full_line_locality_for_that_prefix"],
        }
        for rule in RULES
    }, indent=2))


if __name__ == "__main__":
    main()
