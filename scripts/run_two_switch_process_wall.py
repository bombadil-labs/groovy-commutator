"""Process supervisor for the frozen two-switch rail-selector SAT census."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import experiment_two_switch_rail_selector_sat as base  # noqa:E402
import experiment_two_switch_rail_selector_sat_wall as wall  # noqa:E402

ADDENDUM = ROOT / "docs/research/protocols/two-switch-rail-selector-process-wall-20260910.md"
SCIENTIFIC_WALL = base.SEED_WALL_SECONDS
SHUTDOWN_ALLOWANCE = 5


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def provenance():
    out = dict(wall.provenance())
    out["scripts/run_two_switch_process_wall.py"] = sha256(Path(__file__))
    out[str(ADDENDUM.relative_to(ROOT))] = sha256(ADDENDUM)
    return out


def rewrite_provenance(path: Path):
    out = json.loads(path.read_text())
    out["source_hashes"] = provenance()
    path.write_text(json.dumps(out, separators=(",", ":")) + "\n")
    return out


def fallback(seed_index: int, elapsed: float, reason: str):
    row = base.load_domain()[seed_index]
    return {
        "ok": True,
        "experiment": "two-switch-rail-selector-seed",
        "solver": "Minisat22 via python-sat",
        "seed_wall_seconds": SCIENTIFIC_WALL,
        "family_size": base.FAMILY_SIZE,
        "source_hashes": provenance(),
        "result": {
            **row,
            "seed_index": seed_index,
            "status": "censored",
            "tested_candidates": None,
            "frozen_family_candidates": base.FAMILY_SIZE,
            "first_certificate": None,
            "max_cnf_variables": 0,
            "max_cnf_clauses": 0,
            "solver_seconds": None,
            "elapsed_seconds": min(elapsed, float(SCIENTIFIC_WALL)),
            "tested": [],
            "censoring_reason": reason,
            "process_supervisor": True,
        },
    }


def child_command(tmp: Path, controls: bool, seed_index: int | None):
    cmd = [sys.executable, str(ROOT / "scripts/experiment_two_switch_rail_selector_sat_wall.py")]
    if controls:
        cmd += ["--controls-only"]
    else:
        cmd += ["--seed-index", str(seed_index)]
    cmd += ["--output", str(tmp)]
    return cmd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--controls-only", action="store_true")
    ap.add_argument("--seed-index", type=int)
    args = ap.parse_args()
    if args.controls_only == (args.seed_index is not None):
        raise SystemExit("choose exactly one of --controls-only or --seed-index")
    if args.seed_index is not None and not (0 <= args.seed_index < 22):
        raise SystemExit("bad seed index")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / "child.json"
        if args.controls_only:
            subprocess.run(child_command(tmp, True, None), check=True)
            out = rewrite_provenance(tmp)
            args.output.write_text(json.dumps(out, separators=(",", ":")) + "\n")
            print(json.dumps(out["controls"], indent=2))
            return

        started = time.perf_counter()
        try:
            completed = subprocess.run(
                child_command(tmp, False, args.seed_index),
                check=True,
                timeout=SCIENTIFIC_WALL + SHUTDOWN_ALLOWANCE,
            )
            del completed
        except subprocess.TimeoutExpired:
            elapsed = time.perf_counter() - started
            out = fallback(args.seed_index, elapsed, "seed-wall-process-supervisor")
            args.output.write_text(json.dumps(out, separators=(",", ":")) + "\n")
            print(json.dumps({"seed_index": args.seed_index, "status": "censored", "reason": "seed-wall-process-supervisor"}, indent=2))
            return

        elapsed = time.perf_counter() - started
        if not tmp.exists():
            raise RuntimeError("worker returned successfully without output")
        out = rewrite_provenance(tmp)
        result = out["result"]
        # Exact outcomes must arrive by the scientific wall. The extra five seconds
        # are serialization allowance only; a late exact result is censored.
        if elapsed > SCIENTIFIC_WALL and result["status"] != "censored":
            out = fallback(args.seed_index, elapsed, "seed-wall-process-supervisor-late-exact")
        args.output.write_text(json.dumps(out, separators=(",", ":")) + "\n")
        r = out["result"]
        print(json.dumps({
            "seed_index": r["seed_index"], "rule": r["rule"], "pair": r["pair"],
            "status": r["status"], "tested_candidates": r.get("tested_candidates"),
            "elapsed_seconds": r.get("elapsed_seconds"), "censoring_reason": r.get("censoring_reason"),
        }, indent=2))


if __name__ == "__main__":
    main()
