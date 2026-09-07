#!/usr/bin/env python3
"""Regenerate finite-repertoire tables and figure from the exhaustive CSV."""
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
PREFIX = ROOT / "results/future_repertoire_20260907"
COUNTS = ["initial_states", "noncommuting_states", "different_sets", "unequal_sizes",
          "equal_size_different_sets", "AB_strict_subset_BA", "BA_strict_subset_AB",
          "incomparable_sets", "changed_response_maps", "equal_sets_different_maps",
          "different_prepared_equal_sets"]


def main():
    with PREFIX.with_suffix(".csv").open() as f:
        rows = list(csv.DictReader(f))
    summary = []
    for n in sorted({int(r["n"]) for r in rows}):
        for observation in ("identity", "population_count"):
            for h in range(7):
                selected = [r for r in rows if int(r["n"]) == n
                            and r["observation"] == observation and int(r["h"]) == h]
                assert len(selected) == 66
                record = {"n": n, "observation": observation, "h": h, "rule_pairs": len(selected)}
                record.update({key: sum(int(r[key]) for r in selected) for key in COUNTS})
                assert record["initial_states"] == 66 * 2 ** n
                assert record["different_sets"] == (record["unequal_sizes"]
                                                     + record["equal_size_different_sets"])
                summary.append(record)
    Path(str(PREFIX) + "_summary.json").write_text(json.dumps({
        "weighting": "Every initial state in each of the 66 configured rule pairs; widths separate.",
        "primary_horizon": 6, "records": summary,
    }, indent=2) + "\n")
    table = ["# Future repertoires at six continuation ticks", "",
             "Exact counts over the configured 66 pairs and all initial states at each width.",
             "Shared states, pairs, horizons, and observations are not independent replicates.", "",
             "| Width | Observation | Cases | Different sets | Different sizes | Equal size, different sets | Equal sets, different action maps |",
             "| --- | --- | ---: | ---: | ---: | ---: | ---: |"]
    for row in summary:
        if row["h"] != 6:
            continue
        fields = [str(row["n"]), row["observation"]]
        for key in ["initial_states", "different_sets", "unequal_sizes",
                    "equal_size_different_sets", "equal_sets_different_maps"]:
            fields.append(f"{row[key]:,}")
        table.append("| " + " | ".join(fields) + " |")
    Path(str(PREFIX) + "_table.md").write_text("\n".join(table) + "\n")
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "svg.hashsalt": "future-repertoire-20260907"})
    fig, axes = plt.subplots(1, 3, figsize=(11.7, 4.2), sharey=True)
    series = [("different_sets", "Different outcome sets", "#2e6690"),
              ("unequal_sizes", "Different numbers of outcomes", "#b96222"),
              ("equal_sets_different_maps", "Same set, different action map", "#37755b")]
    for ax, n in zip(axes, (6, 9, 11)):
        selected = [r for r in summary if r["n"] == n and r["observation"] == "identity"]
        for key, label, color in series:
            ax.plot([r["h"] for r in selected],
                    [100 * r[key] / r["initial_states"] for r in selected],
                    marker="o", markersize=3.5, linewidth=1.8, color=color, label=label)
        ax.set_title(f"{n} cells · {66 * 2 ** n:,} pair–state cases", fontsize=11)
        ax.set(xlabel="Continuation ticks (exactly h)", xlim=(-0.1, 6.1), ylim=(0, 55), xticks=range(7))
        ax.grid(axis="y", alpha=0.2)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("Share of enumerated cases (%)")
    fig.suptitle("Operation order: outcomes and action responses separate", y=0.98, fontsize=15)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, frameon=False, fontsize=9)
    fig.subplots_adjust(top=0.80, bottom=0.25, left=0.065, right=0.985, wspace=0.15)
    out = ROOT / "docs/research/assets/future-repertoire-20260907.svg"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, metadata={"Date": None}, facecolor="white")
    print(f"Wrote 42 summary rows, primary-horizon table, and {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
