"""Exact phase-splice source-recoder certificates for one-defect ECA macro dynamics."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from experiment_causal_witness_automaton import MDD, NodeBudgetExceeded  # noqa:E402
from experiment_causal_witness_horizon import FULL_CLASS, macro_rule  # noqa:E402
from experiment_window3_reachable_language import scan_rule as scan_research034  # noqa:E402

A = 8
TMAX = 6
NODE_BUDGET = 5_000_000
SEED_WALL_SECONDS = 20 * 60
PROTOCOL = "docs/research/protocols/phase-splice-source-recoder-20260909.md"
RESOURCE_ADDENDUM = "docs/research/protocols/phase-splice-source-recoder-resource-addendum-20260909.md"
FRESH_POLICIES = ("LR", "RL")
DISCLOSED_POLICIES = ("LL", "RR")
EXPECTED_FRONTIER_RULES = (122, 154, 161, 164, 166, 180, 210, 218)


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ordered_deltas(k: int):
    return sorted(range(-k, k + 1), key=lambda d: (abs(d), d))


def fresh_candidates(tmax: int = TMAX):
    """Frozen primary order: t, j, (abs(delta),delta), LR then RL."""
    for t in range(2, tmax + 1):
        for j in range(1, t):
            k = t - j
            for delta in ordered_deltas(k):
                for policy in FRESH_POLICIES:
                    yield {"t": t, "k": k, "j": j, "delta": delta, "policy": policy}


def candidate_positions(candidate):
    """Frozen resource-addendum order: outside seed future cone, then inside."""
    t = int(candidate["t"])
    j = int(candidate["j"])
    delta = int(candidate["delta"])
    outside = [p for p in range(-t, t + 1) if not (delta - j <= p <= delta + j)]
    inside = [p for p in range(-t, t + 1) if delta - j <= p <= delta + j]
    return outside + inside


def step_symbolic(mdd: MDD, g, row):
    return [mdd.apply3(g, row[i], row[i + 1], row[i + 2]) for i in range(len(row) - 2)]


def evolve_symbolic(mdd: MDD, g, row, steps: int):
    out = list(row)
    for _ in range(steps):
        mdd.apply_cache.clear()
        out = step_symbolic(mdd, g, out)
    return out


def find_unequal_assignment(mdd: MDD, left: int, right: int):
    """Return one partial variable assignment reaching unequal terminal values."""
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


def select_background(policy: str, q: int, delta: int, z_left, z_right, index: int):
    if policy == "LL":
        return z_left[index]
    if policy == "RR":
        return z_right[index]
    if policy == "LR":
        return z_left[index] if q < delta else z_right[index]
    if policy == "RL":
        return z_right[index] if q < delta else z_left[index]
    raise ValueError(policy)


def replay_counterexample(g, seed_pair, candidate, p: int, coords, assignment, mismatch: str):
    """Scalar replay of the exact MDD inequality before accepting a failure."""
    a, b = seed_pair
    background = [0] * len(coords)
    for var, value in assignment.items():
        background[int(var)] = int(value)

    row_left = [a if coord == 0 else background[i] for i, coord in enumerate(coords)]
    row_right = [b if coord == 0 else background[i] for i, coord in enumerate(coords)]

    t = int(candidate["t"])
    k = int(candidate["k"])
    j = int(candidate["j"])
    delta = int(candidate["delta"])
    policy = candidate["policy"]

    z_left = scalar_evolve(g, row_left, k)
    z_right = scalar_evolve(g, row_right, k)
    assert len(z_left) == len(z_right) == 2 * j + 1

    actual_left = scalar_evolve(g, z_left, j)[0]
    actual_right = scalar_evolve(g, z_right, j)[0]

    q0 = p - j
    candidate_left = []
    candidate_right = []
    for idx, q in enumerate(range(q0, p + j + 1)):
        if q == delta:
            candidate_left.append(a)
            candidate_right.append(b)
        else:
            common = select_background(policy, q, delta, z_left, z_right, idx)
            candidate_left.append(common)
            candidate_right.append(common)

    recoded_left = scalar_evolve(g, candidate_left, j)[0]
    recoded_right = scalar_evolve(g, candidate_right, j)[0]

    if mismatch == "left":
        assert actual_left != recoded_left
    else:
        assert actual_right != recoded_right

    return {
        "position": p,
        "mismatch_rail": mismatch,
        "window_start": coords[0],
        "background_word": background,
        "actual_outputs": [actual_left, actual_right],
        "recoded_outputs": [recoded_left, recoded_right],
    }


def check_position(rule: int, seed_pair, candidate, p: int, node_budget: int = NODE_BUDGET):
    """Exact pointwise identity check in one fresh canonical MDD manager."""
    a, b = seed_pair
    t = int(candidate["t"])
    k = int(candidate["k"])
    j = int(candidate["j"])
    delta = int(candidate["delta"])
    policy = candidate["policy"]

    assert t == k + j and 2 <= t <= TMAX
    assert policy in FRESH_POLICIES + DISCLOSED_POLICIES

    coords = list(range(p - t, p + t + 1))
    assert len(coords) == 2 * t + 1 <= 13

    g = macro_rule(rule)
    mdd = MDD(len(coords), node_budget)
    variables = [mdd.variable(i) for i in range(len(coords))]
    row_left = [a if coord == 0 else variables[i] for i, coord in enumerate(coords)]
    row_right = [b if coord == 0 else variables[i] for i, coord in enumerate(coords)]

    z_left = evolve_symbolic(mdd, g, row_left, k)
    z_right = evolve_symbolic(mdd, g, row_right, k)
    assert len(z_left) == len(z_right) == 2 * j + 1

    actual_left = evolve_symbolic(mdd, g, z_left, j)[0]
    actual_right = evolve_symbolic(mdd, g, z_right, j)[0]

    candidate_left = []
    candidate_right = []
    for idx, q in enumerate(range(p - j, p + j + 1)):
        if q == delta:
            candidate_left.append(a)
            candidate_right.append(b)
        else:
            common = select_background(policy, q, delta, z_left, z_right, idx)
            candidate_left.append(common)
            candidate_right.append(common)

    recoded_left = evolve_symbolic(mdd, g, candidate_left, j)[0]
    recoded_right = evolve_symbolic(mdd, g, candidate_right, j)[0]
    nodes = mdd.node_count

    if actual_left == recoded_left and actual_right == recoded_right:
        return {"status": "pass", "position": p, "mdd_nodes": nodes, "variables": len(coords)}

    mismatch = "left" if actual_left != recoded_left else "right"
    unequal = find_unequal_assignment(
        mdd,
        actual_left if mismatch == "left" else actual_right,
        recoded_left if mismatch == "left" else recoded_right,
    )
    assert unequal is not None
    assignment, _, _ = unequal
    replay = replay_counterexample(g, seed_pair, candidate, p, coords, assignment, mismatch)
    return {
        "status": "fail",
        "position": p,
        "mdd_nodes": nodes,
        "variables": len(coords),
        "counterexample": replay,
    }


def check_candidate(rule: int, seed_pair, candidate, node_budget: int = NODE_BUDGET, deadline: float | None = None):
    checked_positions = []
    max_nodes = 0
    started = time.perf_counter()

    for p in candidate_positions(candidate):
        if deadline is not None and time.perf_counter() >= deadline:
            return {
                **candidate,
                "status": "censored",
                "reason": "seed-wall-time",
                "checked_positions": checked_positions,
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
                "checked_positions": checked_positions,
                "max_mdd_nodes": max_nodes,
                "elapsed_seconds": time.perf_counter() - started,
            }
        checked_positions.append({k: v for k, v in rec.items() if k != "counterexample"})
        max_nodes = max(max_nodes, int(rec["mdd_nodes"]))
        if rec["status"] == "fail":
            return {
                **candidate,
                "status": "fail",
                "failing_position": p,
                "counterexample": rec["counterexample"],
                "checked_positions": checked_positions,
                "max_mdd_nodes": max_nodes,
                "elapsed_seconds": time.perf_counter() - started,
            }

    return {
        **candidate,
        "status": "pass",
        "checked_positions": checked_positions,
        "max_mdd_nodes": max_nodes,
        "elapsed_seconds": time.perf_counter() - started,
    }


def run_seed_language(rule: int, seed_pair, incoming_target_ids, node_budget: int = NODE_BUDGET,
                      wall_seconds: float = SEED_WALL_SECONDS):
    started = time.perf_counter()
    deadline = started + wall_seconds
    tested = []
    counts = Counter()
    first_pass = None
    first_censoring = None
    max_nodes = 0
    family_size = sum(1 for _ in fresh_candidates())

    for candidate in fresh_candidates():
        if time.perf_counter() >= deadline:
            first_censoring = first_censoring or {**candidate, "reason": "seed-wall-time"}
            break
        rec = check_candidate(rule, seed_pair, candidate, node_budget, deadline)
        tested.append(rec)
        counts[rec["status"]] += 1
        max_nodes = max(max_nodes, int(rec.get("max_mdd_nodes", 0)))
        if rec["status"] == "pass":
            first_pass = rec
            break
        if rec["status"] == "censored" and first_censoring is None:
            first_censoring = {k: v for k, v in rec.items() if k not in ("checked_positions", "counterexample")}
        if rec["status"] == "censored" and rec.get("reason") == "seed-wall-time":
            break

    if first_pass is not None:
        status = "phase-splice-certified"
    elif first_censoring is not None:
        status = "censored"
    else:
        status = "no-phase-splice-through-6"

    return {
        "pair": f"{seed_pair[0]}-{seed_pair[1]}",
        "seed_symbol": 8 * seed_pair[0] + seed_pair[1],
        "incoming_target_ids": list(map(int, incoming_target_ids)),
        "status": status,
        "tested_candidates": len(tested),
        "frozen_family_candidates": family_size,
        "candidate_status_counts": dict(sorted(counts.items())),
        "first_certificate": first_pass,
        "first_censoring": first_censoring,
        "max_mdd_nodes": max_nodes,
        "elapsed_seconds": time.perf_counter() - started,
        "tested": tested,
    }


def run_controls(node_budget: int = NODE_BUDGET):
    # Disclosed, non-fresh positive control from the abandoned single-rail design.
    rule5_candidate = {"t": 3, "k": 2, "j": 1, "delta": 0, "policy": "LL"}
    rule5 = check_candidate(5, (0, 2), rule5_candidate, node_budget)
    if rule5["status"] != "pass":
        raise AssertionError(("Rule5 disclosed LL normalization failed", rule5))

    # Fresh-family semantic exclusion control: all LR/RL candidates through h=3 must fail.
    rule35_rows = []
    for candidate in fresh_candidates(3):
        rec = check_candidate(35, (2, 6), candidate, node_budget)
        if rec["status"] != "fail":
            raise AssertionError(("Rule35 cross-phase pre-witness control", rec))
        rule35_rows.append(rec)

    return {
        "ok": True,
        "rule5": {
            "status": "pass",
            "candidate": rule5_candidate,
            "max_mdd_nodes": rule5["max_mdd_nodes"],
            "checked_positions": len(rule5["checked_positions"]),
        },
        "rule35": {
            "all_fail": True,
            "fresh_candidates_t_le_3": len(rule35_rows),
            "max_mdd_nodes": max((r["max_mdd_nodes"] for r in rule35_rows), default=0),
        },
    }


def scan_rule(rule: int, node_budget: int = NODE_BUDGET, wall_seconds: float = SEED_WALL_SECONDS):
    base = scan_research034(rule)
    languages = []
    for lang in base["languages"]:
        incoming = list(lang["width3_unresolved_target_ids"])
        if not incoming:
            continue
        a, b = map(int, lang["pair"].split("-"))
        rec = run_seed_language(rule, (a, b), incoming, node_budget, wall_seconds)
        rec.update({
            "pair_index": int(lang["pair_index"]),
            "width3_word_count": int(lang["width3_word_count"]),
            "width3_rounds": int(lang["width3_rounds"]),
            "is_r122_161_sentinel": bool(lang["is_r122_161_sentinel"]),
        })
        languages.append(rec)
    return {
        "rule": rule,
        "wclass": FULL_CLASS[rule],
        "survivor_seed_languages": len(languages),
        "survivor_target_questions": sum(len(x["incoming_target_ids"]) for x in languages),
        "languages": languages,
    }


def source_hashes():
    return {
        "scripts/experiment_phase_splice_source_recoder.py": file_hash(Path(__file__)),
        PROTOCOL: file_hash(ROOT / PROTOCOL),
        RESOURCE_ADDENDUM: file_hash(ROOT / RESOURCE_ADDENDUM),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rule-start", type=int, default=0)
    ap.add_argument("--rule-end", type=int, default=256)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--controls-only", action="store_true")
    args = ap.parse_args()

    if args.controls_only:
        out = {
            "experiment": "phase-splice-source-recoder-controls",
            "schema": 1,
            "working_identity": "phase-splice-source-recoder",
            "resource_limits": {"mdd_nodes_per_position": NODE_BUDGET, "seed_wall_seconds": SEED_WALL_SECONDS, "tmax": TMAX},
            "source_hashes": source_hashes(),
            "controls": run_controls(),
        }
    else:
        if not (0 <= args.rule_start < args.rule_end <= 256):
            raise SystemExit("bad rule range")
        rows = [scan_rule(rule) for rule in range(args.rule_start, args.rule_end)]
        out = {
            "experiment": "phase-splice-source-recoder",
            "schema": 1,
            "working_identity": "phase-splice-source-recoder",
            "rule_start": args.rule_start,
            "rule_end": args.rule_end,
            "fresh_policies": list(FRESH_POLICIES),
            "tmax": TMAX,
            "resource_limits": {"mdd_nodes_per_position": NODE_BUDGET, "seed_wall_seconds": SEED_WALL_SECONDS},
            "source_hashes": source_hashes(),
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
