"""Independent scalar physical replay of the two selected raw triggers."""

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
N = 34


def evolve(x):
    y = 0
    for i in range(N):
        a = (x >> ((i - 1) % N)) & 1
        b = (x >> i) & 1
        c = (x >> ((i + 1) % N)) & 1
        y |= ((54 >> (4*a + 2*b + c)) & 1) << i
    return y


def word(state, center):
    bits = ''.join(str((state >> ((center + j) % N)) & 1) for j in (-2, -1, 0, 1, 2))
    return int(bits[::-1], 2)


def physical_success(state, choice, target):
    ordinary = evolve(state)
    if choice >= 0:
        ordinary = (ordinary & ~(1 << choice)) | (state & (1 << choice))
    for _ in range(5):
        ordinary = evolve(ordinary)
    return ordinary in target


def audit(rows, allowed, target):
    record = {"score": 0, "rescues": 0, "harms": 0,
              "unique_trials": 0, "both_pattern_trials": 0,
              "collisions": [], "harmed": [], "rescued": []}
    for row in rows:
        state = row["at_decision"]
        a = [i for i in range(N) if word(state, i) == 19]
        b = [i for i in range(N) if word(state, i) == 25]
        fired = sorted((a if 19 in allowed else []) + (b if 25 in allowed else []))
        action = fired[0] if len(fired) == 1 else -1
        identity = [row["rotation"], row["injury"]]
        if allowed == {19, 25} and a and b:
            record["both_pattern_trials"] += 1
            record["collisions"].append({"trial": identity, "sites_19": a, "sites_25": b,
                                         "action": action, "winning_actions": row["winning_actions"]})
        good = physical_success(state, action, target)
        passive = physical_success(state, -1, target)
        assert good == (action in row["winning_actions"])
        assert passive == (-1 in row["winning_actions"])
        record["score"] += good
        record["unique_trials"] += action != -1
        if good and not passive:
            record["rescues"] += 1
            record["rescued"].append({"trial": identity, "action": action})
        if passive and not good:
            record["harms"] += 1
            record["harmed"].append({"trial": identity, "action": action,
                                     "sites_19": a, "sites_25": b})
    return record


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("result", type=Path)
    args = p.parse_args()
    result = json.loads(args.result.read_text())
    assert result["schema"] == "rule54-two-pattern-closure-v1"
    for path, digest in result["source_hashes"].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest
    for path, digest in result["sources"].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest
    source = json.loads((ROOT / "results/rule54_glider_route_gate_20260924.json").read_text())
    earlier = json.loads((ROOT / "results/rule54_local_sensor_gate_20260924.json").read_text())
    rows = source["trials"]
    assert len(rows) == result["trial_count"] == N*N
    target = set(source["target"])
    assert len(target) == N
    for pnum in (19, 25):
        got = audit(rows, {pnum}, target)
        assert got == result["single"][str(pnum)]
        assert got["score"] == earlier["families"]["raw"]["menu"][str(pnum)]["score"] == 374
    combined = audit(rows, {19, 25}, target)
    assert combined == result["or"]
    assert result["fixed"] == source["fixed_scores"]["-1"] == 340
    assert result["full_state"] == source["full_state_successes"] == 408
    assert result["predictions"]["P1_full_ceiling_no_harm"] == (
        "supported" if combined["score"] == 408 and combined["harms"] == 0 else "failed")
    salvageable = [row for row in rows if row["winning_actions"] and -1 not in row["winning_actions"]]
    assert result["predictions"]["P2_no_salvageable_double_trigger"] == (
        "supported" if all(not ([i for i in range(N) if word(row["at_decision"], i) == 19]
                                and [i for i in range(N) if word(row["at_decision"], i) == 25])
                            for row in salvageable) else "failed")
    print("Independent scalar site flags and physical outcome replay verified")


if __name__ == "__main__":
    main()
