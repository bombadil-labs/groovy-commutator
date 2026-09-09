"""Exact symbolic rail-normalization certificates for one-defect ECA macro dynamics."""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from collections import Counter
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from experiment_causal_witness_automaton import MDD, NodeBudgetExceeded  # noqa:E402
from experiment_causal_witness_horizon import macro_rule  # noqa:E402
from experiment_window3_reachable_language import scan_rule as scan_research034  # noqa:E402

A = 8
TMAX = 6
NODE_BUDGET = 5_000_000
WALL_SECONDS = 20 * 60
PROTOCOL = "docs/research/protocols/symbolic-defect-normalization-20260909.md"


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ordered_deltas(k: int):
    return sorted(range(-k, k + 1), key=lambda d: (abs(d), d))


def candidates(tmax: int = TMAX):
    for t in range(2, tmax + 1):
        for j in range(1, t):
            k = t - j
            for delta in ordered_deltas(k):
                for rail in ("left", "right"):
                    yield {"t": t, "k": k, "j": j, "delta": delta, "rail": rail}


def candidate_positions(candidate):
    t = int(candidate["t"])
    j = int(candidate["j"])
    delta = int(candidate["delta"])
    outside = [p for p in range(-t, t + 1) if not (delta - j <= p <= delta + j)]
    inside = [p for p in range(-t, t + 1) if delta - j <= p <= delta + j]
    return outside + inside


def step_symbolic(mdd: MDD, g, row):
    return [mdd.apply3(g, row[i], row[i + 1], row[i + 2]) for i in range(len(row) - 2)]


def evolve_symbolic_pair(mdd: MDD, g, row_a, row_b, steps: int):
    a = list(row_a)
    b = list(row_b)
    for _ in range(steps):
        mdd.apply_cache.clear()
        a = step_symbolic(mdd, g, a)
        b = step_symbolic(mdd, g, b)
    return a, b


def evolve_symbolic_single(mdd: MDD, g, row, steps: int):
    out = list(row)
    for _ in range(steps):
        mdd.apply_cache.clear()
        out = step_symbolic(mdd, g, out)
    return out


def find_unequal_assignment(mdd: MDD, left: int, right: int):
    if left == right:
        return None
    memo = {}

    def rec(a: int, b: int):
        key = (a, b)
        if key in memo:
            return memo[key]
        if a < A and b < A:
            ans = ({}, a, b) if a != b else None
            memo[key] = ans
            return ans
        var = min(mdd.var_index(a), mdd.var_index(b))
        ca = mdd.children(a) if mdd.var_index(a) == var else (a,) * A
        cb = mdd.children(b) if mdd.var_index(b) == var else (b,) * A
        for value in range(A):
            ans = rec(ca[value], cb[value])
            if ans is not None:
                assignment, u, v = ans
                assignment = dict(assignment)
                assignment[var] = value
                out = (assignment, u, v)
                memo[key] = out
                return out
        memo[key] = None
        return None

    return rec(left, right)


def scalar_step(g, row):
    return [int(g[64 * row[i] + 8 * row[i + 1] + row[i + 2]]) for i in range(len(row) - 2)]


def scalar_evolve(g, row, steps: int):
    out = list(row)
    for _ in range(steps):
        out = scalar_step(g, out)
    return out


def replay_counterexample(g, seed_pair, candidate, p: int, coords, assignment, mismatch: str):
    a, b = seed_pair
    background = [0] * len(coords)
    for var, value in assignment.items():
        background[int(var)] = int(value)
    row_a = [a if coord == 0 else background[i] for i, coord in enumerate(coords)]
    row_b = [b if coord == 0 else background[i] for i, coord in enumerate(coords)]
    t, k, j, delta = (int(candidate[x]) for x in ("t", "k", "j", "delta"))
    actual_a = scalar_evolve(g, row_a, t)[0]
    actual_b = scalar_evolve(g, row_b, t)[0]
    base = scalar_evolve(g, row_a if candidate["rail"] == "left" else row_b, k)
    assert len(base) == 2 * j + 1
    qa = list(base)
    qb = list(base)
    left_coord = p - j
    if left_coord <= delta <= p + j:
        idx = delta - left_coord
        qa[idx] = a
        qb[idx] = b
    cand_a = scalar_evolve(g, qa, j)[0]
    cand_b = scalar_evolve(g, qb, j)[0]
    if mismatch == "left":
        assert actual_a != cand_a
    else:
        assert actual_b != cand_b
    return {
        "position": p,
        "mismatch_rail": mismatch,
        "window_start": coords[0],
        "background_word": background,
        "actual_outputs": [actual_a, actual_b],
        "normalized_outputs": [cand_a, cand_b],
    }


def check_position(rule: int, seed_pair, candidate, p: int, node_budget: int):
    a, b = seed_pair
    t, k, j, delta = (int(candidate[x]) for x in ("t", "k", "j", "delta"))
    coords = list(range(p - t, p + t + 1))
    assert len(coords) == 2 * t + 1 <= 13
    g = macro_rule(rule)
    mdd = MDD(len(coords), node_budget)
    variables = [mdd.variable(i) for i in range(len(coords))]
    row_a = [a if coord == 0 else variables[i] for i, coord in enumerate(coords)]
    row_b = [b if coord == 0 else variables[i] for i, coord in enumerate(coords)]

    row_a_k, row_b_k = evolve_symbolic_pair(mdd, g, row_a, row_b, k)
    assert len(row_a_k) == len(row_b_k) == 2 * j + 1

    actual_a_row, actual_b_row = evolve_symbolic_pair(mdd, g, row_a_k, row_b_k, j)
    assert len(actual_a_row) == len(actual_b_row) == 1
    actual_a, actual_b = actual_a_row[0], actual_b_row[0]

    base = list(row_a_k if candidate["rail"] == "left" else row_b_k)
    qa = list(base)
    qb = list(base)
    left_coord = p - j
    if left_coord <= delta <= p + j:
        idx = delta - left_coord
        qa[idx] = a
        qb[idx] = b

    candidate_a = evolve_symbolic_single(mdd, g, qa, j)[0]
    candidate_b = evolve_symbolic_single(mdd, g, qb, j)[0]
    nodes = mdd.node_count

    if actual_a == candidate_a and actual_b == candidate_b:
        return {"status": "pass", "position": p, "mdd_nodes": nodes, "variables": len(coords)}

    mismatch = "left" if actual_a != candidate_a else "right"
    unequal = find_unequal_assignment(mdd, actual_a if mismatch == "left" else actual_b,
                                     candidate_a if mismatch == "left" else candidate_b)
    assert unequal is not None
    assignment, _, _ = unequal
    counterexample = replay_counterexample(g, seed_pair, candidate, p, coords, assignment, mismatch)
    return {
        "status": "fail",
        "position": p,
        "mdd_nodes": nodes,
        "variables": len(coords),
        "counterexample": counterexample,
    }


def check_candidate(rule: int, seed_pair, candidate, node_budget: int, deadline: float | None = None):
    points = []
    max_nodes = 0
    started = time.perf_counter()
    for p in candidate_positions(candidate):
        if deadline is not None and time.perf_counter() >= deadline:
            return {
                **candidate,
                "status": "censored",
                "reason": "seed-wall-time",
                "checked_positions": points,
                "max_mdd_nodes": max_nodes,
                "elapsed_seconds": time.perf_counter() - started,
            }
        try:
            rec = check_position(rule, seed_pair, candidate, p, node_budget)
        except NodeBudgetExceeded as exc:
            return {
                **candidate,
                "status": "censored",
                "reason": str(exc),
                "position": p,
                "node_budget": node_budget,
                "checked_positions": points,
                "max_mdd_nodes": max_nodes,
                "elapsed_seconds": time.perf_counter() - started,
            }
        points.append({k: v for k, v in rec.items() if k != "counterexample"})
        max_nodes = max(max_nodes, int(rec["mdd_nodes"]))
        if rec["status"] == "fail":
            return {
                **candidate,
                "status": "fail",
                "failing_position": p,
                "counterexample": rec["counterexample"],
                "checked_positions": points,
                "max_mdd_nodes": max_nodes,
                "elapsed_seconds": time.perf_counter() - started,
            }
    return {
        **candidate,
        "status": "pass",
        "checked_positions": points,
        "max_mdd_nodes": max_nodes,
        "elapsed_seconds": time.perf_counter() - started,
    }


def run_language(rule: int, seed_pair, incoming_target_ids, node_budget: int, wall_seconds: float):
    started = time.perf_counter()
    deadline = started + wall_seconds
    tested = []
    status_counts = Counter()
    first_pass = None
    first_censored = None
    max_nodes = 0
    for candidate in candidates():
        if time.perf_counter() >= deadline:
            first_censored = first_censored or {**candidate, "reason": "seed-wall-time"}
            break
        rec = check_candidate(rule, seed_pair, candidate, node_budget, deadline)
        tested.append(rec)
        status_counts[rec["status"]] += 1
        max_nodes = max(max_nodes, int(rec.get("max_mdd_nodes", 0)))
        if rec["status"] == "pass":
            first_pass = rec
            break
        if rec["status"] == "censored" and first_censored is None:
            first_censored = {k: v for k, v in rec.items() if k not in ("checked_positions", "counterexample")}
        if rec["status"] == "censored" and rec.get("reason") == "seed-wall-time":
            break

    if first_pass is not None:
        status = "certified"
    elif first_censored is not None:
        status = "censored"
    else:
        status = "no-certificate-in-frozen-family"

    return {
        "pair": f"{seed_pair[0]}-{seed_pair[1]}",
        "seed_symbol": 8 * seed_pair[0] + seed_pair[1],
        "incoming_target_ids": list(map(int, incoming_target_ids)),
        "status": status,
        "candidate_status_counts": dict(sorted(status_counts.items())),
        "tested_candidates": len(tested),
        "frozen_family_candidates": sum(1 for _ in candidates()),
        "first_certificate": first_pass,
        "first_censoring": first_censored,
        "max_mdd_nodes": max_nodes,
        "elapsed_seconds": time.perf_counter() - started,
        "tested": tested,
    }


def run_controls(node_budget: int):
    rule5_candidate = {"t": 3, "k": 2, "j": 1, "delta": 0, "rail": "left"}
    rule5 = check_candidate(5, (0, 2), rule5_candidate, node_budget)
    assert rule5["status"] == "pass", rule5

    rule35_rows = []
    for candidate in candidates(3):
        rec = check_candidate(35, (2, 6), candidate, node_budget)
        if rec["status"] != "fail":
            raise AssertionError(("Rule35 pre-witness normalization control", rec))
        rule35_rows.append({k: v for k, v in rec.items() if k not in ("checked_positions", "counterexample")})
    return {
        "ok": True,
        "rule5": {k: v for k, v in rule5.items() if k != "checked_positions"},
        "rule35_t_le_3_candidates": len(rule35_rows),
        "rule35_all_fail": True,
        "rule35_max_mdd_nodes": max((r["max_mdd_nodes"] for r in rule35_rows), default=0),
    }


def scan_rule(rule: int, node_budget: int, wall_seconds: float):
    base = scan_research034(rule)
    languages = []
    for lang in base["languages"]:
        incoming = list(lang["width3_unresolved_target_ids"])
        if not incoming:
            continue
        a, b = map(int, lang["pair"].split("-"))
        rec = run_language(rule, (a, b), incoming, node_budget, wall_seconds)
        rec.update({
            "pair_index": int(lang["pair_index"]),
            "width3_word_count": int(lang["width3_word_count"]),
            "width3_rounds": int(lang["width3_rounds"]),
            "is_r122_161_sentinel": bool(lang["is_r122_161_sentinel"]),
        })
        languages.append(rec)
    return {
        "rule": rule,
        "wclass": base["wclass"],
        "survivor_seed_languages": len(languages),
        "survivor_target_questions": sum(len(x["incoming_target_ids"]) for x in languages),
        "languages": languages,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rule-start", type=int, default=0)
    ap.add_argument("--rule-end", type=int, default=256)
    ap.add_argument("--node-budget", type=int, default=NODE_BUDGET)
    ap.add_argument("--seed-wall-seconds", type=float, default=WALL_SECONDS)
    ap.add_argument("--controls-only", action="store_true")
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    if args.node_budget != NODE_BUDGET:
        raise SystemExit(f"frozen primary node budget is {NODE_BUDGET}")
    if args.seed_wall_seconds != WALL_SECONDS:
        raise SystemExit(f"frozen primary seed wall time is {WALL_SECONDS} seconds")

    if args.controls_only:
        out = {
            "experiment": "symbolic-defect-normalization-controls",
            "schema": 1,
            "working_identity": "symbolic-defect-normalization",
            "node_budget": NODE_BUDGET,
            "controls": run_controls(NODE_BUDGET),
            "source_hashes": {
                "scripts/experiment_symbolic_defect_normalization.py": file_hash(Path(__file__)),
                PROTOCOL: file_hash(ROOT / PROTOCOL),
            },
        }
    else:
        if not (0 <= args.rule_start < args.rule_end <= 256):
            raise SystemExit("bad rule range")
        rows = [scan_rule(rule, NODE_BUDGET, WALL_SECONDS) for rule in range(args.rule_start, args.rule_end)]
        out = {
            "experiment": "symbolic-defect-normalization",
            "schema": 1,
            "working_identity": "symbolic-defect-normalization",
            "rule_start": args.rule_start,
            "rule_end": args.rule_end,
            "tmax": TMAX,
            "node_budget": NODE_BUDGET,
            "seed_wall_seconds": WALL_SECONDS,
            "source_hashes": {
                "scripts/experiment_symbolic_defect_normalization.py": file_hash(Path(__file__)),
                PROTOCOL: file_hash(ROOT / PROTOCOL),
            },
            "rows": rows,
        }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2) + "\n")
    if args.controls_only:
        print(json.dumps(out["controls"], indent=2))
    else:
        print(json.dumps({
            "rules": len(out["rows"]),
            "seed_languages": sum(r["survivor_seed_languages"] for r in out["rows"]),
            "target_questions": sum(r["survivor_target_questions"] for r in out["rows"]),
            "statuses": dict(Counter(l["status"] for r in out["rows"] for l in r["languages"])),
        }, indent=2))


if __name__ == "__main__":
    main()
