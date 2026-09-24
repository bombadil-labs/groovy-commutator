"""Separate scalar reimplementation of the exact Rule-54 route gate."""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import signal
import sys


N = 34
SEED = "1000" * 4 + "10" + "1110" * 4
ALLOWED = {"001", "100", "010", "101"}


def encode(word: str) -> int:
    return sum(int(bit) * 2**i for i, bit in enumerate(word))


def decode(state: int) -> str:
    return "".join(str((state // 2**i) % 2) for i in range(N))


@lru_cache(maxsize=100_000)
def evolve(state: int) -> int:
    bits = decode(state)
    return encode("".join(
        "1" if bits[(i-1) % N] + bits[i] + bits[(i+1) % N] in ALLOWED else "0"
        for i in range(N)
    ))


def steps(state: int, number: int) -> int:
    for _ in range(number):
        state = evolve(state)
    return state


def shifted(state: int, rotation: int) -> int:
    bits = decode(state)
    return encode(bits[-rotation:] + bits[:-rotation] if rotation else bits)


def check(path: Path) -> dict:
    signal.alarm(60)
    record = json.loads(path.read_text(encoding="utf-8"))
    assert record["schema"] == "rule54-glider-route-gate-v1"
    assert record["width"] == N and record["rule"] == 54
    assert record["seed_word"] == SEED and record["seed"] == encode(SEED)
    assert len(record["implementation_commit"]) == 40
    root = Path(__file__).resolve().parents[2]
    for path_name, digest in record["source_hashes"].items():
        assert hashlib.sha256((root / path_name).read_bytes()).hexdigest() == digest
    clean = [encode(SEED)]
    for _ in range(8):
        clean.append(evolve(clean[-1]))
    assert clean == record["clean_route"]
    assert [decode(state) for state in clean] == record["clean_route_words"]
    target = {shifted(clean[8], shift) for shift in range(N)}
    assert sorted(target) == record["target"]
    rows = record["trials"]
    assert len(rows) == N * N
    scores = Counter()
    groups = {}
    rescued = 0
    first = None
    for index, row in enumerate(rows):
        rotation, injury = divmod(index, N)
        assert (row["rotation"], row["injury"]) == (rotation, injury)
        initial = shifted(encode(SEED), rotation) ^ (1 << injury)
        state = steps(initial, 2)
        assert (row["initial"], row["at_decision"]) == (initial, state)
        ordinary = evolve(state)
        winners = []
        for action in [-1, *range(N)]:
            new_bits = list(decode(ordinary))
            if action >= 0:
                new_bits[action] = decode(state)[action]
            endpoint = steps(encode("".join(new_bits)), 5)
            if endpoint in target:
                winners.append(action)
                scores[action] += 1
        assert row["winning_actions"] == winners
        if state in groups:
            assert groups[state] == winners
        else:
            groups[state] = winners
        if -1 not in winners and winners:
            rescued += 1
            if first is None:
                action = winners[0]
                trace = [initial]
                for _ in range(2):
                    trace.append(evolve(trace[-1]))
                bits = list(decode(evolve(trace[-1])))
                bits[action] = decode(trace[-1])[action]
                trace.append(encode("".join(bits)))
                for _ in range(5):
                    trace.append(evolve(trace[-1]))
                assert trace[-1] in target
                first = {"rotation": rotation, "injury": injury,
                         "action": action, "trajectory": trace}
    scores = {str(action): scores[action] for action in [-1, *range(N)]}
    best = min([-1, *range(N)], key=lambda action: (-scores[str(action)], action))
    full = sum(bool(row["winning_actions"]) for row in rows)
    assert record["fixed_scores"] == scores
    assert record["best_fixed_action"] == best
    assert record["passive_successes"] == scores["-1"]
    assert record["full_state_successes"] == full
    assert record["rescued_from_passive_failure"] == rescued
    assert record["first_rescue"] == first
    assert record["distinct_decision_states"] == len(groups)
    assert record["predictions"] == {
        "P0_replay_consistency": "pending_independent_verification",
        "P1_passive_failures": "supported" if scores["-1"] < len(rows) else "failed",
        "P2_dynamic_rescue": "supported" if rescued else "failed",
        "P3_state_over_fixed": "supported" if full > scores[str(best)] else "failed",
    }
    return {"P0_replay_consistency": "supported", "trial_count": len(rows),
            "target_size": len(target), "passive": scores["-1"],
            "best_fixed": scores[str(best)], "full": full, "rescued": rescued}


if __name__ == "__main__":
    print(json.dumps(check(Path(sys.argv[1])), sort_keys=True))
