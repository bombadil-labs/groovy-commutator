"""Frozen Rule-54 published-seed route gate; see dated protocol."""

from __future__ import annotations

import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import resource
import signal


WIDTH = 34
MASK = (1 << WIDTH) - 1
SEED_WORD = "1000" * 4 + "10" + "1110" * 4
PROTOCOL = "docs/research/protocols/2026-09-24-rule54-glider-route-gate.md"
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def rotate(state: int, shift: int) -> int:
    shift %= WIDTH
    return ((state << shift) | (state >> (WIDTH - shift))) & MASK


@lru_cache(maxsize=100_000)
def step(state: int) -> int:
    answer = 0
    for cell in range(WIDTH):
        left = (state >> ((cell - 1) % WIDTH)) & 1
        center = (state >> cell) & 1
        right = (state >> ((cell + 1) % WIDTH)) & 1
        triple = (left << 2) | (center << 1) | right
        answer |= ((54 >> triple) & 1) << cell
    return answer


def advance(state: int, count: int) -> int:
    for _ in range(count):
        state = step(state)
    return state


def string(state: int) -> str:
    return "".join(str((state >> i) & 1) for i in range(WIDTH))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--implementation-commit", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if len(args.implementation_commit) != 40 or any(
        char not in "0123456789abcdef" for char in args.implementation_commit.lower()
    ):
        parser.error("--implementation-commit requires a 40-digit SHA")
    if args.output.exists():
        parser.error("refusing to overwrite an existing result")
    resource.setrlimit(resource.RLIMIT_AS, (256 * 1024**2, 256 * 1024**2))
    signal.alarm(60)
    assert len(SEED_WORD) == WIDTH
    seed = sum((character == "1") << i for i, character in enumerate(SEED_WORD))
    clean_route = [seed]
    for _ in range(8):
        clean_route.append(step(clean_route[-1]))
    target = sorted({rotate(clean_route[8], i) for i in range(WIDTH)})
    target_set = set(target)
    actions = [-1, *range(WIDTH)]
    rows = []
    first_rescue = None
    for rotation in range(WIDTH):
        clean_initial = rotate(seed, rotation)
        for injury in range(WIDTH):
            initial = clean_initial ^ (1 << injury)
            after_two = advance(initial, 2)
            ordinary = step(after_two)
            winners = []
            for action in actions:
                postaction = ordinary if action == -1 else (
                    ordinary & ~(1 << action)) | (after_two & (1 << action))
                if advance(postaction, 5) in target_set:
                    winners.append(action)
            if -1 not in winners and winners and first_rescue is None:
                chosen = winners[0]
                trajectory = [initial]
                for _ in range(2):
                    trajectory.append(step(trajectory[-1]))
                switched = ordinary if chosen == -1 else (
                    ordinary & ~(1 << chosen)) | (after_two & (1 << chosen))
                trajectory.append(switched)
                for _ in range(5):
                    trajectory.append(step(trajectory[-1]))
                first_rescue = {"rotation": rotation, "injury": injury,
                                "action": chosen, "trajectory": trajectory}
            rows.append({"rotation": rotation, "injury": injury, "initial": initial,
                         "at_decision": after_two, "winning_actions": winners})
    fixed_scores = {str(action): sum(action in row["winning_actions"] for row in rows)
                    for action in actions}
    best_fixed = min(actions, key=lambda action: (-fixed_scores[str(action)], action))
    passive = fixed_scores["-1"]
    full = sum(bool(row["winning_actions"]) for row in rows)
    rescued = sum(-1 not in row["winning_actions"] and bool(row["winning_actions"])
                  for row in rows)
    grouped = {}
    for row in rows:
        key = row["at_decision"]
        previous = grouped.setdefault(key, row["winning_actions"])
        assert previous == row["winning_actions"]
    predictions = {"P0_replay_consistency": "pending_independent_verification",
                   "P1_passive_failures": "supported" if passive < len(rows) else "failed",
                   "P2_dynamic_rescue": "supported" if rescued else "failed",
                   "P3_state_over_fixed": "supported" if full > fixed_scores[str(best_fixed)] else "failed"}
    source_hashes = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
                     for p in [PROTOCOL, "experiments/rule54_glider_route_gate_20260924/run.py",
                               "experiments/rule54_glider_route_gate_20260924/verify.py"]}
    record = {"schema": "rule54-glider-route-gate-v1", "protocol": PROTOCOL,
              "implementation_commit": args.implementation_commit,
              "source_hashes": source_hashes, "width": WIDTH, "rule": 54,
              "seed_word": SEED_WORD, "seed": seed,
              "clean_route": clean_route, "clean_route_words": [string(s) for s in clean_route],
              "target": target, "trials": rows, "distinct_decision_states": len(grouped),
              "best_fixed_action": best_fixed, "fixed_scores": fixed_scores,
              "passive_successes": passive, "full_state_successes": full,
              "rescued_from_passive_failure": rescued, "first_rescue": first_rescue,
              "predictions": predictions}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(record, handle, sort_keys=True, indent=2)
        handle.write("\n")
    print(json.dumps({"predictions": predictions, "passive": passive,
                      "fixed": fixed_scores[str(best_fixed)], "full": full,
                      "rescued": rescued}, sort_keys=True))


if __name__ == "__main__":
    main()
