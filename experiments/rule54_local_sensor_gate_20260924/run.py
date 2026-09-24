"""Exact local sensor comparison under the frozen Rule-54 address grammar."""

from collections import Counter
import argparse
import hashlib
import json
from pathlib import Path
import resource
import signal

ROOT = Path(__file__).resolve().parents[2]
SRC = "results/rule54_glider_route_gate_20260924.json"
SRC_SHA = "b390b49d3506b5e78e45fbcbd3de710bdcad60b3b0a6d21054e1dc276d166f75"
PROTOCOL = "docs/research/protocols/2026-09-24-rule54-local-sensor-gate.md"
N = 34
MASK = (1 << N) - 1


def step(x):
    left = ((x << 1) | (x >> (N - 1))) & MASK
    right = (x >> 1) | ((x & 1) << (N - 1))
    return ((~left & ~x & right) | (~left & x & ~right)
            | (left & ~x & ~right) | (left & ~x & right)) & MASK


def fields(x):
    e = step(x)
    return e, x ^ e, e ^ step(e) ^ step(x ^ e)


def pattern(x, site):
    return sum(((x >> ((site + offset) % N)) & 1) << (offset + 2)
               for offset in range(-2, 3))


def unique_address(flags):
    return flags.bit_length() - 1 if flags and flags & (flags - 1) == 0 else -1


def policy_action(x, kind, predicate, precomputed=None, lut=None):
    if kind == "none":
        return -1
    e, d, g = precomputed if precomputed is not None else fields(x)
    bits = {"e": e, "d": d, "g": g}
    flags = 0
    for i in range(N):
        p = pattern(x, i)
        trigger = (p == predicate if kind == "raw" else
                   ((lut >> p) & 1) == predicate if kind == "compiled_g" else
                   ((bits[kind] >> i) & 1) == predicate)
        if trigger:
            flags |= 1 << i
    return unique_address(flags)


def score(rows, kind, predicate, lut):
    hits = 0
    unique = 0
    wins = losses = 0
    witness_win = witness_loss = None
    for row in rows:
        action = policy_action(row["at_decision"], kind, predicate,
                               row["_fields"], lut)
        original = -1 in row["winning_actions"]
        success = action in row["winning_actions"]
        hits += success
        unique += action != -1
        if success and not original:
            wins += 1
            witness_win = witness_win or [row["rotation"], row["injury"], action]
        if original and not success:
            losses += 1
            witness_loss = witness_loss or [row["rotation"], row["injury"], action]
    return {"score": hits, "unique": unique, "rescues": wins,
            "harms": losses, "rescue_witness": witness_win,
            "harm_witness": witness_loss}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--implementation-commit", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if len(args.implementation_commit) != 40 or any(c not in "0123456789abcdef" for c in args.implementation_commit):
        parser.error("expected 40-digit lowercase SHA")
    if args.output.exists():
        parser.error("refusing to overwrite result")
    resource.setrlimit(resource.RLIMIT_AS, (256 * 1024**2, 256 * 1024**2))
    signal.alarm(60)
    path = ROOT / SRC
    assert hashlib.sha256(path.read_bytes()).hexdigest() == SRC_SHA
    original = json.loads(path.read_text())
    assert original["schema"] == "rule54-glider-route-gate-v1"
    assert (original["rule"], original["width"]) == (54, N)
    rows = original["trials"]
    assert len(rows) == N*N and {(r["rotation"], r["injury"]) for r in rows} == {
        (r, i) for r in range(N) for i in range(N)}
    for row in rows:
        row["_fields"] = fields(row["at_decision"])

    # Evaluate G at a central site for each radius-two raw input, with zeros
    # elsewhere. Its center has no access beyond these five specified bits.
    lut = 0
    for p in range(32):
        x = sum(((p >> (offset + 2)) & 1) << (offset % N)
                for offset in range(-2, 3))
        lut |= (fields(x)[2] & 1) << p
    for row in rows:
        x, g = row["at_decision"], row["_fields"][2]
        assert all(((g >> i) & 1) == ((lut >> pattern(x, i)) & 1)
                   for i in range(N))

    menus = {
        "g": [("g", 0), ("g", 1)],
        "e": [("e", 0), ("e", 1)],
        "d": [("d", 0), ("d", 1)],
        "raw": [("raw", p) for p in range(32)],
        "compiled_g": [("compiled_g", 0), ("compiled_g", 1)],
    }
    fixed = score(rows, "none", None, lut)
    assert fixed["score"] == original["fixed_scores"]["-1"] == 340
    results = {}
    for family, choices in menus.items():
        entries = {str(p): score(rows, kind, p, lut) for kind, p in choices}
        best = max([(None, fixed), *[(p, entries[str(p)]) for _, p in choices]],
                   key=lambda pair: (pair[1]["score"], pair[0] is None, -(pair[0] or 0)))
        results[family] = {"menu": entries, "best_predicate": best[0],
                           "best": best[1]}
    assert [results["compiled_g"]["menu"][str(i)] for i in (0, 1)] == [
        results["g"]["menu"][str(i)] for i in (0, 1)]
    record = {
        "schema": "rule54-local-sensor-gate-v1", "source": SRC,
        "source_sha256": SRC_SHA, "protocol": PROTOCOL,
        "implementation_commit": args.implementation_commit,
        "source_hashes": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
                          for p in (PROTOCOL, "experiments/rule54_local_sensor_gate_20260924/run.py",
                                    "experiments/rule54_local_sensor_gate_20260924/verify.py")},
        "trials": len(rows), "g_local_truth_table": lut,
        "fixed": fixed, "full_state_ceiling": original["full_state_successes"],
        "families": results,
        "predictions": {
            "P1_g_exceeds_fixed": "supported" if results["g"]["best"]["score"] > 340 else "failed",
            "P2_cheap_simple_matches_g": "supported" if max(results[k]["best"]["score"] for k in ("e", "d", "raw")) >= results["g"]["best"]["score"] else "failed",
            "P3_compiled_g_matches": "supported",
        },
        "cost": {"source_reads_per_site_g_or_compiled": 5,
                 "native_g_rule_passes_total": 3,
                 "native_g_extra_rule_passes_if_base_step_reused": 2,
                 "compiled_g_table_bits_uncompressed": 32,
                 "address_flags_emitted": N},
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        json.dump(record, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({k: {"score": v["best"]["score"],
                           "predicate": v["best_predicate"]} for k, v in results.items()}))


if __name__ == "__main__":
    main()
