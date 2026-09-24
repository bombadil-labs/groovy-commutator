"""Frozen global Rule-54 G sensor information gate; see dated protocol."""

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import resource
import signal

ROOT = Path(__file__).resolve().parents[2]
SOURCE = "results/rule54_glider_route_gate_20260924.json"
SOURCE_SHA = "b390b49d3506b5e78e45fbcbd3de710bdcad60b3b0a6d21054e1dc276d166f75"
PROTOCOL = "docs/research/protocols/2026-09-24-rule54-g-sensor-gate.md"
WIDTH = 34
ACTIONS = (-1, *range(WIDTH))


def step(state):
    result = 0
    for i in range(WIDTH):
        triple = (4 * ((state >> ((i - 1) % WIDTH)) & 1)
                  + 2 * ((state >> i) & 1)
                  + ((state >> ((i + 1) % WIDTH)) & 1))
        result |= ((54 >> triple) & 1) << i
    return result


def groovy(state):
    next_state = step(state)
    return next_state ^ step(next_state) ^ step(state ^ next_state)


def optimize(rows, key):
    fibers = defaultdict(list)
    for row in rows:
        fibers[key(row)].append(row)
    score = 0
    policy = {}
    for observation, members in fibers.items():
        counts = {action: sum(action in member["winning_actions"] for member in members)
                  for action in ACTIONS}
        chosen = max(ACTIONS, key=lambda action: (counts[action], -ACTIONS.index(action)))
        policy[observation] = chosen
        score += counts[chosen]
    return score, fibers, policy


def witness(fibers):
    for observation, members in sorted(fibers.items()):
        feasible = [row for row in members if row["winning_actions"]]
        if not feasible:
            continue
        if set.intersection(*(set(row["winning_actions"]) for row in feasible)):
            continue
        selected = feasible[:]
        for row in feasible[:]:
            if len(selected) > 1 and not set.intersection(*(
                    set(other["winning_actions"]) for other in selected if other is not row)):
                selected.remove(row)
        return {"g_word": observation, "rows": [
            {field: row[field] for field in ("rotation", "injury", "at_decision", "winning_actions")}
            for row in selected]}
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--implementation-commit", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if len(args.implementation_commit) != 40 or any(c not in "0123456789abcdef" for c in args.implementation_commit):
        parser.error("implementation commit must be a lowercase 40-digit SHA")
    if args.output.exists():
        parser.error("refusing to overwrite result")
    resource.setrlimit(resource.RLIMIT_AS, (256 * 1024**2, 256 * 1024**2))
    signal.alarm(60)
    source_path = ROOT / SOURCE
    assert hashlib.sha256(source_path.read_bytes()).hexdigest() == SOURCE_SHA
    source = json.loads(source_path.read_text())
    assert source["schema"] == "rule54-glider-route-gate-v1"
    assert source["width"] == WIDTH and source["rule"] == 54
    rows = source["trials"]
    assert len(rows) == WIDTH * WIDTH
    assert {(row["rotation"], row["injury"]) for row in rows} == {
        (r, i) for r in range(WIDTH) for i in range(WIDTH)}
    raw_actions = {}
    for row in rows:
        assert 0 <= row["at_decision"] < (1 << WIDTH)
        assert all(action in ACTIONS for action in row["winning_actions"])
        previous = raw_actions.setdefault(row["at_decision"], row["winning_actions"])
        assert previous == row["winning_actions"]
    baseline, _, _ = optimize(rows, lambda _: 0)
    raw, raw_fibers, _ = optimize(rows, lambda row: row["at_decision"])
    g, g_fibers, _ = optimize(rows, lambda row: groovy(row["at_decision"]))
    assert baseline == source["fixed_scores"][str(source["best_fixed_action"])]
    assert raw == source["full_state_successes"] and len(raw_fibers) == source["distinct_decision_states"]
    assert g <= raw
    record = {
        "schema": "rule54-g-sensor-gate-v1",
        "source": SOURCE, "source_sha256": SOURCE_SHA,
        "protocol": PROTOCOL, "implementation_commit": args.implementation_commit,
        "source_hashes": {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
                          for path in (PROTOCOL, "experiments/rule54_g_sensor_gate_20260924/run.py",
                                       "experiments/rule54_g_sensor_gate_20260924/verify.py")},
        "trials": len(rows), "full_source_fibers": len(raw_fibers),
        "full_g_fibers": len(g_fibers), "best_fixed_score": baseline,
        "full_source_score": raw, "full_g_score": g, "loss_from_source": raw - g,
        "g_witness": witness(g_fibers),
        "predictions": {"P1_g_loses_at_least_one": "supported" if g < raw else "failed",
                        "P2_g_never_beats_source": "supported"},
        "cost": {"source_bits_read": 34, "source_rule_evaluations": 0,
                 "g_source_bits_read": 34, "g_rule_evaluations": 3,
                 "central_address_bits": 6,
                 "source_table_uncompressed_bits": len(raw_fibers) * 40,
                 "g_table_uncompressed_bits": len(g_fibers) * 40},
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        json.dump(record, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({key: record[key] for key in ("full_source_score", "full_g_score", "loss_from_source", "full_g_fibers", "predictions")}))


if __name__ == "__main__":
    main()
