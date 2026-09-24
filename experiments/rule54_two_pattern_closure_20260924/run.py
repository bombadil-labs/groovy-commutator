"""Frozen 19-or-25 Rule-54 one-site hold under the previous arbiter."""

import argparse
import hashlib
import json
from pathlib import Path
import resource
import signal

ROOT = Path(__file__).resolve().parents[2]
SOURCE = "results/rule54_glider_route_gate_20260924.json"
SOURCE_SHA = "b390b49d3506b5e78e45fbcbd3de710bdcad60b3b0a6d21054e1dc276d166f75"
SELECTED = "results/rule54_local_sensor_gate_20260924.json"
SELECTED_SHA = "04374a9ec5b0a5c67ecdea92d2cffde6784cdba0f6d8460c43cb1267afce7970"
PROTOCOL = "docs/research/protocols/2026-09-24-rule54-two-pattern-closure.md"
N = 34


def pattern(state, i):
    return sum(((state >> ((i + j - 2) % N)) & 1) << j for j in range(5))


def select(state, allowed):
    flagged = [i for i in range(N) if pattern(state, i) in allowed]
    return flagged[0] if len(flagged) == 1 else -1, flagged


def metrics(rows, allowed):
    score = rescues = harms = unique = 0
    collisions = []
    harmed = []
    rescued = []
    both_pattern_trials = 0
    for row in rows:
        s = row["at_decision"]
        action, flags = select(s, allowed)
        flags19 = [i for i in range(N) if pattern(s, i) == 19]
        flags25 = [i for i in range(N) if pattern(s, i) == 25]
        if allowed == {19, 25}:
            assert sorted(flags) == sorted(flags19 + flags25)
        identity = [row["rotation"], row["injury"]]
        if allowed == {19, 25} and flags19 and flags25:
            both_pattern_trials += 1
            collisions.append({"trial": identity, "sites_19": flags19, "sites_25": flags25,
                               "action": action, "winning_actions": row["winning_actions"]})
        good = action in row["winning_actions"]
        passive = -1 in row["winning_actions"]
        score += good
        unique += action != -1
        if good and not passive:
            rescues += 1
            rescued.append({"trial": identity, "action": action})
        if passive and not good:
            harms += 1
            harmed.append({"trial": identity, "action": action,
                           "sites_19": flags19, "sites_25": flags25})
    return {"score": score, "rescues": rescues, "harms": harms,
            "unique_trials": unique, "both_pattern_trials": both_pattern_trials,
            "collisions": collisions, "harmed": harmed, "rescued": rescued}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--implementation-commit", required=True)
    p.add_argument("--output", required=True, type=Path)
    args = p.parse_args()
    if len(args.implementation_commit) != 40 or any(c not in "0123456789abcdef" for c in args.implementation_commit):
        p.error("implementation commit must be a lowercase 40-digit SHA")
    if args.output.exists():
        p.error("refusing to overwrite result")
    resource.setrlimit(resource.RLIMIT_AS, (256 * 1024**2, 256 * 1024**2))
    signal.alarm(30)
    assert hashlib.sha256((ROOT / SOURCE).read_bytes()).hexdigest() == SOURCE_SHA
    assert hashlib.sha256((ROOT / SELECTED).read_bytes()).hexdigest() == SELECTED_SHA
    source = json.loads((ROOT / SOURCE).read_text())
    previous = json.loads((ROOT / SELECTED).read_text())
    assert source["schema"] == "rule54-glider-route-gate-v1" and source["width"] == N and source["rule"] == 54
    assert previous["schema"] == "rule54-local-sensor-gate-v1"
    rows = source["trials"]
    assert len(rows) == N*N and {(r["rotation"], r["injury"]) for r in rows} == {
        (r, i) for r in range(N) for i in range(N)}
    singles = {str(a): metrics(rows, {a}) for a in (19, 25)}
    for a in (19, 25):
        assert singles[str(a)]["score"] == previous["families"]["raw"]["menu"][str(a)]["score"] == 374
        assert singles[str(a)]["rescues"] == 34 and singles[str(a)]["harms"] == 0
    union = metrics(rows, {19, 25})
    assert source["fixed_scores"]["-1"] == 340 and source["full_state_successes"] == 408
    assert union["score"] <= 408
    record = {"schema": "rule54-two-pattern-closure-v1", "protocol": PROTOCOL,
              "implementation_commit": args.implementation_commit,
              "sources": {SOURCE: SOURCE_SHA, SELECTED: SELECTED_SHA},
              "source_hashes": {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
                                for path in (PROTOCOL,
                                             "experiments/rule54_two_pattern_closure_20260924/run.py",
                                             "experiments/rule54_two_pattern_closure_20260924/verify.py",
                                             SOURCE, SELECTED)},
              "trial_count": len(rows), "single": singles, "or": union,
              "fixed": 340, "full_state": 408,
              "predictions": {
                  "P1_full_ceiling_no_harm": "supported" if union["score"] == 408 and union["harms"] == 0 else "failed",
                  "P2_no_salvageable_double_trigger": "supported" if all(-1 in row["winning_actions"] or not row["winning_actions"] or
                      not ([i for i in range(N) if pattern(row["at_decision"], i) == 19] and
                           [i for i in range(N) if pattern(row["at_decision"], i) == 25]) for row in rows) else "failed",
              },
              "cost": {"source_radius": 2, "source_reads_per_site": 5,
                       "literal_pattern_bits": 10, "flags_per_site": 1,
                       "extra_g_evaluations": 0},
              }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as f:
        json.dump(record, f, indent=2, sort_keys=True)
        f.write("\n")
    print(json.dumps({"score": union["score"], "rescues": union["rescues"],
                      "harms": union["harms"], "collisions": len(union["collisions"]),
                      "predictions": record["predictions"]}))


if __name__ == "__main__":
    main()
