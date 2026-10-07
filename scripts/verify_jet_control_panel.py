#!/usr/bin/env python3
"""Recompute the Rule54/30/90 jet panel and verify its saved exact summaries.

Run from any working directory:
  python scripts/verify_jet_control_panel.py

This is a same-code scientific replay and comparison against a result independently
computed with local vectorized/tuple implementations; not independent peer review.
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def close(value: float, expected: float, tolerance: float = 1e-7) -> bool:
    return math.isclose(value, expected, abs_tol=tolerance, rel_tol=0)


def main():
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "experiment_jet_control_panel.py")],
        cwd=ROOT, check=True,
    )
    primary = json.loads(
        (ROOT / "results" / "jet_control_panel_20261007.json").read_text()
    )
    secondary = json.loads(
        (ROOT / "results" / "jet54_deeper_fibers_20261007.json").read_text()
    )
    expected = json.loads(
        (ROOT / "results" / "jet_control_panel_20261007_summary.json").read_text()
    )
    deeper_expected = json.loads(
        (ROOT / "results" / "jet54_deeper_fibers_20261007_summary.json").read_text()
    )

    for rule in (54, 30, 90):
        key = str(rule)
        observed_local = primary["local_truth_tables"][key]
        for idx, actual in enumerate(observed_local):
            reference = expected["local"][key]
            for item, field in (
                ("minimum_source_radius", "radius"),
                ("ANF_degree", "ANF_degree"),
                ("ANF_terms", "ANF_terms"),
            ):
                assert actual[item] == reference[field][idx], (
                    rule, idx, item, actual[item], reference[field][idx]
                )
            assert close(actual["activity_fraction"], reference["activity"][idx])

        language = primary["spatial_languages"][key]
        exp_lang = expected["spatial_languages"][key]
        for idx, actual in enumerate(language):
            assert close(
                actual["topological_entropy_bits_per_site"],
                exp_lang["entropy"][idx],
            ), (rule, idx, "entropy")
            assert actual["minimal_dfa_accepting_states"] == (
                exp_lang["DFA_accepting_states"][idx]
            ), (rule, idx, "DFA states")
            assert actual["realized_alphabet_size"] == (
                exp_lang["realized_alphabet_size"][idx]
            ), (rule, idx, "alphabet size")

    assert primary["summary"]["first_full_entropy_prefix"] == {
        "54": ["G", "Q", "R"],
        "30": ["G", "Q", "R"],
        "90": None,
    }
    assert primary["summary"]["rule90_higher_jet_identically_zero"]

    for rule in (54, 30):
        for depth in (2, 3):
            record = primary["primary_fiber_graphs"][f"{rule}_end_{depth}"]
            assert record["status"] == "evaluated"
            reference = expected["primary_pair_graphs"][f"{rule}_"
                + ("GQ" if depth == 2 else "GQR")]
            assert record["predicted_equal_label_pair_edges"] == (
                reference["predicted_edges"]
            )
            assert record["all_recurrent_non_diagonal_are_cycles"] == (
                reference.get("all_off_diagonal_recurrent_cycle_only", False)
                if depth == 3 else False
            )
            for component in reference.get("pure_branching_components", []):
                assert any(
                    entry["size"] == component["vertices"]
                    and entry["edges"] == component["edges"]
                    and close(entry["spectral_radius"], component["rho"])
                    for entry in record["recurrent_components"]
                ), (rule, depth, component)

    assert not primary["primary_fiber_graphs"]["54_end_3"][
        "all_recurrent_non_diagonal_are_cycles"
    ]
    assert primary["primary_fiber_graphs"]["30_end_3"][
        "all_recurrent_non_diagonal_are_cycles"
    ]

    for depth in (4, 5):
        row = secondary["levels"][str(depth)]
        exp = deeper_expected["levels"][str(depth)]
        assert row["status"] == "evaluated"
        assert row["predicted_equal_label_pair_edges"] == exp["pair_edges"]
        assert row["branching_recurrent_non_diagonal_count"] == len(
            exp["recurrent_branching_offdiagonal_SCCs"]
        )
        assert close(
            row["largest_offdiagonal_spectral_radius"],
            exp["max_offdiagonal_entropy_bits_per_site"] and
            2 ** exp["max_offdiagonal_entropy_bits_per_site"],
        )

    print("PASS: Rule 90 algebraic control")
    print("PASS: Rules 54/30 exact jet local truth and spatial-language summaries")
    print("PASS: Rule 54/30 first-full-entropy pair-fiber SCC classifications")
    print("PASS: targeted Rule-54 A4/A5 branching-fiber follow-up")


if __name__ == "__main__":
    main()
