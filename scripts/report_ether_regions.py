"""Rebuild tables and publication figures from the frozen experiment's integer counts."""
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PREFIX = ROOT / "results/ether_regions_20260907"
OBSERVERS = [("parity", 2), ("parity", 4), ("majority", 3), ("majority", 5), ("derivative", 1)]
COLORS = {"background": "#298374", "ambiguous": "#b37a2b", "departure": "#7356a1"}


def load():
    with PREFIX.with_suffix(".csv").open() as f:
        rows = list(csv.DictReader(f))
    strings = {"projection", "test_kind", "model", "detector", "region"}
    return [{k: v if k in strings else int(v) for k, v in r.items()} for r in rows]


def select(rows, **filters):
    return [r for r in rows if all(r[k] == v for k, v in filters.items())]


def pooled(rows, field="errors"):
    n = sum(r["samples"] for r in rows)
    return sum(r[field] for r in rows) / n if n else float("nan")


def validate_counts(rows):
    from collections import defaultdict
    import json
    protocol = json.loads((ROOT / "docs/research/protocols/ether-regions-20260907.json").read_text())
    expected = (len(protocol["sizes"]) * len(protocol["observers"]) * len(protocol["train_ensembles"])
                * (len(protocol["test_seeds"]) + 1 + len(protocol["perturbed_seeds"]))
                * len(protocol["detectors"]) * 4
                * (protocol["hmax"] + 1 + len(protocol["snapshot_control_radii"])))
    assert len(rows) == expected
    keys = ("n", "projection", "block", "stride", "ensemble", "test_kind", "test_seed",
            "detector", "model", "depth", "radius")
    groups, across_models, detectors = defaultdict(dict), defaultdict(set), defaultdict(set)
    for r in rows:
        key = tuple(r[k] for k in keys)
        assert r["region"] not in groups[key]
        groups[key][r["region"]] = r
        assert 0 <= r["supported_errors"] <= r["supported"] <= r["seen"] <= r["samples"]
        assert 0 <= r["errors"] <= r["samples"] and 0 <= r["baseline_errors"] <= r["samples"]
        assert r["baseline_errors"] - r["errors"] == r["fixed"] - r["broken"]
        invariant_key = tuple(r[k] for k in keys if k not in ("model", "depth", "radius")) + (r["region"],)
        across_models[invariant_key].add((r["samples"], r["baseline_errors"]))
        if r["region"] == "all":
            detectors[tuple(r[k] for k in keys if k != "detector")].add(
                tuple(r[k] for k in ("samples", "errors", "supported", "baseline_errors")))
    fields = ("samples", "errors", "seen", "supported", "supported_errors", "baseline_errors", "fixed", "broken")
    for group in groups.values():
        assert set(group) == {"all", "background", "ambiguous", "departure"}
        for field in fields:
            assert group["all"][field] == sum(group[k][field] for k in ("background", "ambiguous", "departure"))
    assert all(len(v) == 1 for v in across_models.values())
    assert all(len(v) == 1 for v in detectors.values())
    ether = select(rows, test_kind="ether", region="all", model="history", depth=6)
    assert all(r["errors"] == 0 for r in ether)
    assert all(r["samples"] == 0 for r in rows if r["test_kind"] == "ether" and r["region"] in ("departure", "ambiguous"))
    departures = select(rows, test_kind="random", region="departure", model="history", depth=6)
    histories = select(rows, test_kind="random", region="all", detector="r3-7", model="history", depth=6)
    match_keys = ("n", "projection", "block", "ensemble", "test_seed")
    snapshots = {tuple(r[k] for k in match_keys): r for r in select(rows,
        test_kind="random", region="all", detector="r3-7", model="snapshot", radius=10)}
    checks = {"row_count": len(rows), "expected_row_count": expected,
        "count_bounds": True, "region_accounting": True, "paired_error_accounting": True,
        "same_samples_and_baseline_across_models": True, "same_predictions_across_detectors": True,
        "pure_ether_all_background_and_zero_history_errors": True,
        "departure_comparisons": len(departures),
        "departure_positive_gains": sum(r["baseline_errors"] > r["errors"] for r in departures),
        "history_spatial_comparisons": len(histories),
        "history_lower_error_than_wide": sum(r["errors"] < snapshots[tuple(r[k] for k in match_keys)]["errors"] for r in histories)}
    PREFIX.with_name(PREFIX.name + "_checks.json").write_text(json.dumps(checks, indent=2) + "\n")


def table(rows):
    lines = ["| Observation | Departure frequency | Departure error: snapshot → history | Gain from departures | All-target error: history / wide snapshot | History / wide supported |",
             "| --- | ---: | ---: | ---: | ---: | ---: |"]
    for kind, block in OBSERVERS:
        base = select(rows, n=840, projection=kind, block=block, test_kind="random", detector="r3-7")
        dep = select(base, region="departure", model="history", depth=6)
        all_rows = select(base, region="all", model="history", depth=6)
        wide = select(base, region="all", model="snapshot", radius=10)
        frequency = sum(r["samples"] for r in dep) / sum(r["samples"] for r in all_rows)
        share = sum(r["baseline_errors"] - r["errors"] for r in dep) / sum(r["baseline_errors"] - r["errors"] for r in all_rows)
        label = f"{kind.capitalize()} {block}" if kind != "derivative" else "Derivative"
        lines.append(f"| {label} | {100*frequency:.1f}% | {100*pooled(dep,'baseline_errors'):.2f}% → {100*pooled(dep):.2f}% | {100*share:.1f}% | {100*pooled(all_rows):.2f}% / {100*pooled(wide):.2f}% | {100*pooled(all_rows,'supported'):.1f}% / {100*pooled(wide,'supported'):.1f}% |")
    return "\n".join(lines) + "\n"


def figures(rows):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"svg.fonttype": "none", "svg.hashsalt": "ether-regions-20260907",
                         "font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(2, 3, figsize=(13, 7), sharey=True)
    for ax, (kind, block) in zip(axes.flat, OBSERVERS):
        base = select(rows, n=840, projection=kind, block=block, test_kind="random", detector="r3-7")
        for region, color in COLORS.items():
            curve = [select(base, region=region, model="history", depth=h) for h in range(7)]
            ax.plot(range(7), [100*pooled(c) for c in curve], color=color, label=region.capitalize(), marker="o", ms=3)
            ax.fill_between(range(7), [100*min(pooled([r]) for r in c if r["samples"]) for c in curve],
                            [100*max(pooled([r]) for r in c if r["samples"]) for c in curve], color=color, alpha=.12)
            wide = select(base, region=region, model="snapshot", radius=10)
            ax.scatter([8], [100*pooled(wide)], color=color, marker="D", s=35)
        ax.set_title(f"{kind.capitalize()}, block {block}" if kind != "derivative" else "Derivative field")
        ax.set_xticks([0, 2, 4, 6, 8], ["0", "2", "4", "6", "Wide\nsnapshot"])
        ax.set_ylim(-1, 47)
        ax.grid(axis="y", alpha=.18)
    axes[0, 0].set_ylabel("Held-out next-bit error (%)")
    axes[1, 0].set_ylabel("Held-out next-bit error (%)")
    axes[1, 1].set_xlabel("Previous observed times")
    axes[1, 2].axis("off")
    axes[1, 2].legend(*axes[0, 0].get_legend_handles_labels(), loc="upper left", frameon=False)
    axes[1, 2].text(.02, .60, "Lines: radius-one history\nDiamonds: radius-ten snapshot\nBoth longest contexts: 21 input bits\n\nShading: range over eight test seeds\nand two training ensembles; not a CI.\n\nLabels score targets only.\nThey never enter a predictor.", transform=axes[1, 2].transAxes, va="top", linespacing=1.55)
    fig.suptitle("History improves prediction beyond the ether-compatible background", fontsize=16)
    fig.text(.5, .01, "Rule 110 · n = 840 · fixed short/long detector radii 3/7 · support-aware lookup · 506 matched forecast times", ha="center", fontsize=10)
    fig.tight_layout(rect=(0, .04, 1, .96))
    fig.savefig(PREFIX.with_name(PREFIX.name + "_curves.svg"), metadata={"Date": None})
    plt.close(fig)

    # Plot a fixed, declared illustration; it is not selected for prediction accuracy.
    from experiment_ether_regions import PROTOCOL, make_raw, fine_labels, target_labels
    import json
    config = json.loads(PROTOCOL.read_text())
    raw = make_raw(config, 840, "random", 301)
    anchors = np.arange(156, 316)
    fine = fine_labels(raw, anchors, 3, 7, config["ether_word"])
    from matplotlib.colors import ListedColormap
    fig, axes = plt.subplots(1, 3, figsize=(12, 5), sharey=True)
    axes[0].imshow(raw[anchors, :210], cmap="binary", interpolation="nearest", aspect="auto")
    axes[0].set_title("Fine state")
    axes[1].imshow(fine[:, :210], cmap=ListedColormap(list(COLORS.values())), vmin=0, vmax=2,
                   interpolation="nearest", aspect="auto")
    axes[1].set_title("Fine-center compatibility")
    target = target_labels(fine, "derivative", 1, 1).reshape(fine.shape)
    axes[2].imshow(target[:, :210], cmap=ListedColormap(list(COLORS.values())), vmin=0, vmax=2,
                   interpolation="nearest", aspect="auto")
    axes[2].set_title("Derivative-target causal footprint")
    for ax in axes:
        ax.set_xlabel("Fine position (crop 0–209)")
    axes[0].set_ylabel("Fine time after t = 156")
    fig.suptitle("A departure label marks local incompatibility, not an identified glider", fontsize=14)
    fig.text(.5, .01, "Fixed illustration: n = 840, seed 301 · green = compatible background · amber = ambiguous · purple = departure", ha="center", fontsize=9)
    fig.tight_layout(rect=(0, .035, 1, .95))
    fig.savefig(PREFIX.with_name(PREFIX.name + "_detector.svg"), metadata={"Date": None})
    plt.close(fig)


if __name__ == "__main__":
    rows = load()
    validate_counts(rows)
    PREFIX.with_name(PREFIX.name + "_table.md").write_text(table(rows))
    figures(rows)
    print(table(rows))
