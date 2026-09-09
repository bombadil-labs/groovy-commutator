"""Aggregate sharded Research031 causal-witness horizon results."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    shards = [json.loads(p.read_text()) for p in sorted(args.input_dir.rglob("*.json"))]
    shards = [x for x in shards if x.get("experiment") == "causal-witness-horizon"]
    if not shards:
        raise SystemExit("no causal-witness-horizon shards")
    assert {x["schema"] for x in shards} == {1}
    assert {x["block_size"] for x in shards} == {3}
    assert {x["cadence"] for x in shards} == {3}
    assert {x["local_hmax"] for x in shards} == {3}
    assert len({json.dumps(x["source_hashes"], sort_keys=True) for x in shards}) == 1

    coverage = []
    rules = []
    for shard in shards:
        coverage.extend(range(shard["rule_start"], shard["rule_end"]))
        rules.extend(shard["rows"])
    assert sorted(coverage) == list(range(256)) and len(set(coverage)) == 256
    assert sorted(r["rule"] for r in rules) == list(range(256))

    targets = [t for r in rules for t in r["targets"]]
    assert len(targets) == 256 * 127
    mismatch = [sum(r["local_ring_mismatch_by_horizon"][h] for r in rules) for h in range(4)]
    h3_events = []
    h3_target_cases = 0
    class_target_cases = Counter()
    class_events = Counter()
    q2_to_q3_changes = 0
    q1_to_q2_changes = 0
    ring_q2_vs_local_q3 = 0
    for r in rules:
        wc = r["wclass"]
        for t in r["targets"]:
            q = t["local_chain"]
            if q[1] != q[2]:
                q1_to_q2_changes += 1
            if q[2] != q[3]:
                q2_to_q3_changes += 1
            if t["ring_chain"][2] != q[3]:
                ring_q2_vs_local_q3 += 1
            if t["new_h3_pairs"]:
                h3_target_cases += 1
                class_target_cases[wc] += 1
                class_events[wc] += len(t["new_h3_pairs"])
                for pair in t["new_h3_pairs"]:
                    h3_events.append({"rule": r["rule"], "wclass": wc, "target": t["target"], "pair": pair,
                                      "local_chain": q, "ring_chain": t["ring_chain"]})

    summary = {
        "ok": True,
        "experiment": "causal-witness-horizon",
        "rules": len(rules),
        "targets": len(targets),
        "local_ring_mismatch_by_horizon": {str(h): mismatch[h] for h in range(4)},
        "q1_to_q2_target_changes": q1_to_q2_changes,
        "q2_to_q3_target_changes": q2_to_q3_changes,
        "h3_new_pair_target_events": len(h3_events),
        "h3_target_cases": h3_target_cases,
        "h3_rules": len({x["rule"] for x in h3_events}),
        "h3_events_by_class": dict(sorted(class_events.items())),
        "h3_target_cases_by_class": dict(sorted(class_target_cases.items())),
        "ring_q2_vs_local_q3_target_mismatches": ring_q2_vs_local_q3,
        "first_h3_events": h3_events[:50],
        "source_hashes": shards[0]["source_hashes"],
    }
    # h=0 and h=1 must agree exactly: those dependency contexts fit on the
    # 4-macroblock ring without any periodic identification.
    if mismatch[0] != 0 or mismatch[1] != 0:
        raise AssertionError({"unexpected early ring mismatch": mismatch[:2]})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
