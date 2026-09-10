"""Wall-enforced runner for the frozen two-switch rail-selector SAT census."""
from __future__ import annotations

import argparse
import hashlib
import json
import threading
import time
from pathlib import Path

from pysat.solvers import Minisat22

import experiment_two_switch_rail_selector_sat as base

ROOT = Path(__file__).resolve().parents[1]
ADDENDUM = ROOT / "docs/research/protocols/two-switch-rail-selector-wall-enforcement-20260910.md"
_ORIGINAL_PROVENANCE = base.provenance


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def provenance():
    out = dict(_ORIGINAL_PROVENANCE())
    out["scripts/experiment_two_switch_rail_selector_sat_wall.py"] = sha256(Path(__file__))
    out[str(ADDENDUM.relative_to(ROOT))] = sha256(ADDENDUM)
    return out


def solve_position(rule: int, seed_pair, candidate, p: int, deadline=None):
    builder, left0, coords = base.build_query(rule, seed_pair, candidate, p)
    remaining = None if deadline is None else deadline - time.perf_counter()
    if remaining is not None and remaining <= 0:
        return {
            "status": "censored", "reason": "seed-wall-time-before-solve",
            "cnf_variables": builder.variables, "cnf_clauses": len(builder.clauses),
            "solver_seconds": 0.0,
        }

    started = time.perf_counter()
    with Minisat22(bootstrap_with=builder.clauses) as solver:
        timer = None
        if remaining is not None:
            timer = threading.Timer(remaining, solver.interrupt)
            timer.daemon = True
            timer.start()
        try:
            is_sat = solver.solve() if remaining is None else solver.solve_limited(expect_interrupt=True)
        finally:
            if timer is not None:
                timer.cancel()
        seconds = time.perf_counter() - started
        if is_sat is None:
            return {
                "status": "censored", "reason": "seed-wall-time-during-solve",
                "cnf_variables": builder.variables, "cnf_clauses": len(builder.clauses),
                "solver_seconds": seconds,
            }
        model = solver.get_model() if is_sat else None

    out = {
        "status": "sat" if is_sat else "unsat",
        "cnf_variables": builder.variables,
        "cnf_clauses": len(builder.clauses),
        "solver_seconds": seconds,
    }
    if is_sat:
        out["counterexample"] = base.replay_model(rule, seed_pair, candidate, p, coords, left0, model)
    return out


def check_candidate(rule: int, seed_pair, candidate, deadline=None):
    checked = 0
    max_vars = max_clauses = 0
    solver_seconds = 0.0
    for p in base.candidate_positions(candidate):
        if deadline is not None and time.perf_counter() >= deadline:
            return {
                **candidate, "status": "censored", "reason": "seed-wall-time",
                "checked_positions": checked, "max_cnf_variables": max_vars,
                "max_cnf_clauses": max_clauses, "solver_seconds": solver_seconds,
            }
        q = solve_position(rule, seed_pair, candidate, p, deadline)
        checked += 1
        max_vars = max(max_vars, q["cnf_variables"])
        max_clauses = max(max_clauses, q["cnf_clauses"])
        solver_seconds += q["solver_seconds"]
        if q["status"] == "censored":
            return {
                **candidate, "status": "censored", "reason": q["reason"],
                "checked_positions": checked, "max_cnf_variables": max_vars,
                "max_cnf_clauses": max_clauses, "solver_seconds": solver_seconds,
            }
        if q["status"] == "sat":
            return {
                **candidate, "status": "fail", "failing_position": p,
                "checked_positions": checked, "counterexample": q["counterexample"],
                "max_cnf_variables": max_vars, "max_cnf_clauses": max_clauses,
                "solver_seconds": solver_seconds,
            }
    return {
        **candidate, "status": "pass", "checked_positions": checked,
        "max_cnf_variables": max_vars, "max_cnf_clauses": max_clauses,
        "solver_seconds": solver_seconds,
    }


# base.run_controls and base.run_seed resolve this global dynamically.
base.check_candidate = check_candidate
base.provenance = provenance


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--controls-only", action="store_true")
    ap.add_argument("--seed-index", type=int)
    args = ap.parse_args()
    if args.controls_only == (args.seed_index is not None):
        raise SystemExit("choose exactly one of --controls-only or --seed-index")
    if args.controls_only:
        out = {
            "ok": True, "experiment": "two-switch-rail-selector-controls",
            "solver": "Minisat22 via python-sat", "family_size": base.FAMILY_SIZE,
            "source_hashes": provenance(), "controls": base.run_controls(),
        }
    else:
        if not (0 <= args.seed_index < 22):
            raise SystemExit("bad seed index")
        out = {
            "ok": True, "experiment": "two-switch-rail-selector-seed",
            "solver": "Minisat22 via python-sat", "seed_wall_seconds": base.SEED_WALL_SECONDS,
            "family_size": base.FAMILY_SIZE, "source_hashes": provenance(),
            "result": base.run_seed(args.seed_index),
        }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, separators=(",", ":")) + "\n")
    if args.controls_only:
        print(json.dumps(out["controls"], indent=2))
    else:
        r = out["result"]
        print(json.dumps({k: r[k] for k in (
            "seed_index", "rule", "pair", "status", "tested_candidates",
            "max_cnf_variables", "max_cnf_clauses", "elapsed_seconds")}, indent=2))


if __name__ == "__main__":
    main()
