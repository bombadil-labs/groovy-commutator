#!/usr/bin/env python3
"""Bounded exact commutator-jet comparator: Rules 54, 30, and 90.

Reuse the already pinned symbolic-language and full-line pair-graph machinery
from the stacked research units, with no feature or rule selection.

Frozen protocols:
  docs/research/protocols/jet-control-panel-20261007.md
  docs/research/protocols/jet54-deeper-fibers-20261007.md

Requires NumPy, matching the existing research package dependency.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "scripts"
OUT = ROOT / "results"
PANEL = (54, 30, 90)
LEVEL_NAMES = ("D", "G", "Q", "R", "A4", "A5")
EDGE_CAP = 5_000_000


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def anf_stats(truth: np.ndarray) -> tuple[int, int]:
    coeff = truth.copy().astype(np.uint8)
    nbits = len(coeff).bit_length() - 1
    for bit in range(nbits):
        stride = 1 << bit
        coeff = coeff.reshape(-1, 2 * stride)
        coeff[:, stride:] ^= coeff[:, :stride]
        coeff = coeff.reshape(-1)
    support = np.flatnonzero(coeff)
    degree = max((int(i).bit_count() for i in support), default=0)
    return int(degree), int(len(support))


def minimum_radius(truth: np.ndarray, source_radius: int) -> int:
    nbits = 2 * source_radius + 1
    for radius in range(source_radius + 1):
        seen: dict[int, int] = {}
        shift = source_radius - radius
        mask = (1 << (2 * radius + 1)) - 1
        for word, value in enumerate(truth):
            key = (word >> shift) & mask
            previous = seen.setdefault(key, int(value))
            if previous != int(value):
                break
        else:
            return radius
    raise AssertionError("Full source radius must suffice")


def pair_edge_budget(fibers, rule: int, end_level: int) -> int:
    src, dst, labels, nstates, radius, truths = fibers.source_edges(
        rule, end_level
    )
    counts = np.bincount(labels.astype(np.int64))
    return sum(int(c) ** 2 for c in counts)


def summarize_pair_graph(result: dict, estimated_edges: int) -> dict:
    recurrent = result["recurrent_components"]
    nond = [x for x in recurrent if x["non_diagonal_vertices"]]
    branching = [x for x in nond if not x["simple_cycle"]]
    return {
        "prefix_names": result["prefix_names"],
        "source_radius": result["source_radius"],
        "predicted_equal_label_pair_edges": estimated_edges,
        "biinfinite_vertices": result["biinfinite_vertices"],
        "biinfinite_edges": result["biinfinite_edges"],
        "biinfinite_non_diagonal_vertices":
            result["biinfinite_non_diagonal_vertices"],
        "recurrent_components": recurrent,
        "recurrent_non_diagonal_count": len(nond),
        "branching_recurrent_non_diagonal_count": len(branching),
        "all_recurrent_non_diagonal_are_cycles": not branching,
        "largest_offdiagonal_spectral_radius": max(
            (x["spectral_radius"] for x in nond), default=0
        ),
        "periodic_phase_periods": sorted(set(
            x["period"] for x in nond
            if x["simple_cycle"] and "period" in x
        )),
        "pair_graph_entropy_bits_per_site":
            result["pair_graph_entropy_bits_per_site"],
        "interface_count": len(result["interfaces"]),
        "interfaces": result["interfaces"],
    }


def scored_pair(fibers, rule: int, end_level: int):
    count = pair_edge_budget(fibers, rule, end_level)
    if count > EDGE_CAP:
        return {"status": "resource-censored", "predicted_edges": count,
                "cap": EDGE_CAP}
    result = fibers.analyze_factor(
        f"rule{rule}_G_prefix_{end_level}", rule, end_level, False
    )
    return {"status": "evaluated", **summarize_pair_graph(result, count)}


def main():
    language_path = BASE / "experiment_commutator_jet_language.py"
    fibers_path = BASE / "experiment_commutator_jet_fibers.py"
    language = load_module("commutator_jet_language", language_path)
    fibers = load_module("commutator_jet_fibers", fibers_path)

    source_hashes = {
        "script_sha256": sha(Path(__file__)),
        "language_runner_sha256": sha(language_path),
        "fiber_runner_sha256": sha(fibers_path),
    }

    data = {
        "schema": "jet-control-panel-v1",
        "date": "2026-10-07",
        "protocol": "docs/research/protocols/jet-control-panel-20261007.md",
        "panel": list(PANEL),
        "jet_definitions": {
            "A0": "D=I xor H",
            "Ak_plus_1": "Ak o H xor H o Ak",
            "g_anchored_prefixes": "G through G,Q,R,A4,A5",
        },
        "local_truth_tables": {},
        "spatial_languages": {},
        "primary_fiber_graphs": {},
        "algebraic_rule90_control": {
            "identity": "H linear => D=I+H commutes with H => G=0",
            "pair_language": "full four-symbol source-pair shift",
            "pair_entropy_bits_per_site": 2,
        },
        "source_hashes": source_hashes,
    }

    for rule in PANEL:
        local = []
        for level in range(6):
            truth = language.local_level_truth(rule, level)
            degree, count = anf_stats(truth)
            local.append({
                "field": LEVEL_NAMES[level],
                "level": level,
                "minimum_source_radius": minimum_radius(truth, level + 1),
                "ANF_degree": degree,
                "ANF_terms": count,
                "activity_fraction": float(truth.mean()),
                "identically_zero": bool(np.all(truth == 0)),
            })
        data["local_truth_tables"][str(rule)] = local

        language_rows = [
            language.prefix_result(rule, end)
            for end in range(1, 6)
        ]
        data["spatial_languages"][str(rule)] = language_rows

    assert all(x["identically_zero"]
               for x in data["local_truth_tables"]["90"][1:]), (
        "Rule 90 additive control must vanish above D"
    )

    data["summary"] = {
        "first_full_entropy_prefix": {
            str(rule): next(
                (row["prefix_names"]
                 for row in data["spatial_languages"][str(rule)]
                 if abs(row["topological_entropy_bits_per_site"] - 1.0)
                    < 1e-9),
                None,
            )
            for rule in PANEL
        },
        "rule90_higher_jet_identically_zero": True,
    }

    for rule in (54, 30):
        for end in (2, 3):
            result = scored_pair(fibers, rule, end)
            data["primary_fiber_graphs"][f"{rule}_end_{end}"] = result
    data["primary_fiber_graphs"]["90_all_prefixes"] = {
        "status": "algebraic-control",
        "pair_language": "full four-symbol shift",
        "pair_entropy_bits_per_site": 2,
        "source": "every G-anchored jet field is identically zero",
    }

    data["summary"]["first_full_entropy_fiber_decision"] = {
        str(rule): (
            data["primary_fiber_graphs"][f"{rule}_end_3"].get(
                "all_recurrent_non_diagonal_are_cycles"
            )
        )
        for rule in (54, 30)
    }

    OUT.mkdir(parents=True, exist_ok=True)
    primary_path = OUT / "jet_control_panel_20261007.json"
    primary_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    print(json.dumps(data["summary"], indent=2, sort_keys=True))

    # Separately frozen after the primary result, before the deeper evaluation.
    secondary = {
        "schema": "jet54-deeper-fibers-v1",
        "date": "2026-10-07",
        "protocol": "docs/research/protocols/jet54-deeper-fibers-20261007.md",
        "reason": "Rule 54 retains branching off-diagonal SCCs at GQR",
        "rule": 54,
        "levels": {},
        "source_hashes": source_hashes,
    }
    for end in (4, 5):
        secondary["levels"][str(end)] = scored_pair(fibers, 54, end)
    secondary["summary"] = {
        "positive_branching_through_A5": all(
            secondary["levels"][str(end)].get(
                "branching_recurrent_non_diagonal_count", 0
            ) > 0 for end in (4, 5)
        )
    }
    secondary_path = OUT / "jet54_deeper_fibers_20261007.json"
    secondary_path.write_text(
        json.dumps(secondary, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(secondary["summary"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
