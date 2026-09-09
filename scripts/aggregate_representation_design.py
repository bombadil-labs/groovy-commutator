"""Aggregate and validate sharded Research027 representation-design results."""
from __future__ import annotations
import argparse
import json
from collections import Counter
from pathlib import Path

TOL = 1e-9


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    files = sorted(args.input_dir.rglob("*.json"))
    shards = [json.loads(p.read_text()) for p in files]
    shards = [x for x in shards if x.get("experiment") == "representation-design"]
    if not shards:
        raise SystemExit("no representation-design shard JSON found")
    widths = {x["ring_width"] for x in shards}
    schemas = {x["schema"] for x in shards}
    hashes = {json.dumps(x["source_hashes"], sort_keys=True) for x in shards}
    if widths != {12} or schemas != {1} or len(hashes) != 1:
        raise AssertionError({"widths": widths, "schemas": schemas, "source_hash_sets": len(hashes)})
    coverage = []
    rows = []
    for s in shards:
        coverage.extend(range(s["rule_start"], s["rule_end"]))
        rows.extend(s["rows"])
    if sorted(coverage) != list(range(256)) or len(set(coverage)) != 256:
        raise AssertionError("shards do not cover each ECA rule exactly once")
    if sorted(r["rule"] for r in rows) != list(range(256)):
        raise AssertionError("row coverage mismatch")

    targets = [t for r in rows for t in r["targets"]]
    nonclosed = [t for t in targets if not t["closed"]]
    if len(targets) != 256 * 7 or len(nonclosed) != 1590:
        raise AssertionError({"targets": len(targets), "nonclosed": len(nonclosed)})
    greedy_opt = sum(t["greedy_globally_optimal"] for t in nonclosed)
    disagreements = [t for t in nonclosed if not t["bulk_tail_agree"]]
    by_class = Counter(t["wclass"] for t in disagreements)
    class_iv_total = sum(t["wclass"] == "IV" for t in nonclosed)
    frontier_fracs = [t["possibility_path_frontier_fraction"] for t in nonclosed]
    drift_edges = sum(r["diagonal_target_drift_increasing_edges"] for r in rows)

    if greedy_opt != 1590:
        raise AssertionError(f"greedy global-optimum count changed: {greedy_opt}/1590")
    if len(disagreements) != 326:
        raise AssertionError(f"bulk/tail disagreement count changed: {len(disagreements)}")
    if class_iv_total != 98 or by_class["IV"] != 60:
        raise AssertionError({"class_iv_targets": class_iv_total, "class_iv_disagreements": by_class["IV"]})

    r106 = next(r for r in rows if r["rule"] == 106)
    parity = next(t for t in r106["targets"] if t["target"] == "0110")
    nodes = {x["partition"]: x for x in parity["first_split_nodes"]}
    even = nodes["0112"]
    odd = nodes["0120"]
    if parity["target_hstar"] != 13 or even["tail"] != 13 or odd["tail"] != 7:
        raise AssertionError({"rule106_parity": parity, "even": even, "odd": odd})
    if even["W"] > odd["W"] + TOL:
        raise AssertionError("Rule106 even split should be no worse in bulk residual entropy")
    if "0112" not in parity["bulk_first_split_set"] or parity["tail_first_split"] != "0120":
        raise AssertionError("Rule106 split identities changed")

    summary = {
        "ok": True,
        "experiment": "representation-design",
        "ring_width": 12,
        "shards": len(shards),
        "rules": len(rows),
        "binary_targets": len(targets),
        "nonclosed_targets": len(nonclosed),
        "greedy_closure_globally_optimal": greedy_opt,
        "greedy_closure_globally_optimal_fraction": greedy_opt / len(nonclosed),
        "bulk_tail_disagreements": len(disagreements),
        "bulk_tail_disagreement_fraction": len(disagreements) / len(nonclosed),
        "bulk_tail_disagreements_by_class": dict(sorted(by_class.items())),
        "class_iv_nonclosed_targets": class_iv_total,
        "class_iv_bulk_tail_disagreements": by_class["IV"],
        "class_iv_bulk_tail_disagreement_fraction": by_class["IV"] / class_iv_total,
        "mean_greedy_possibility_frontier_fraction": sum(frontier_fracs) / len(frontier_fracs),
        "diagonal_refinement_edges_increasing_future_repertoire": drift_edges,
        "rule106_parity": {
            "base_tail": parity["target_hstar"],
            "bulk_split": "0112",
            "bulk_split_W": even["W"],
            "bulk_split_tail": even["tail"],
            "tail_split": "0120",
            "tail_split_W": odd["W"],
            "tail_split_tail": odd["tail"],
        },
        "source_hashes": shards[0]["source_hashes"],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
