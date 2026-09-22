#!/usr/bin/env python3
"""Exact bounded G-only factor test; protocol frozen before implementation.

Local checks use shrinking causal words. Periodic search uses packed integers.
--check replays the deterministic scientific record; --integrity registers
this unit with the shared integrity engine without triggering legacy runs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import resource
import subprocess
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
RESULT = "results/rule110_g_autonomy_20260922.json"
EXECUTION = "experiments/rule110_g_autonomy_20260922/execution.json"
SOURCES = (
    "docs/research/protocols/rule110-g-autonomy-20260922.md",
    "scripts/verify_rule110_g_autonomy.py",
)


def digest(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def bits(value, width):
    return tuple((value >> i) & 1 for i in range(width - 1, -1, -1))


def word(row):
    return "".join(map(str, row))


def shrink(row, rule):
    return tuple((rule >> (4*l + 2*c + r)) & 1
                 for l, c, r in zip(row, row[1:], row[2:]))


def groovy_word(row, rule):
    e = shrink(row, rule)
    ee = shrink(e, rule)
    d = tuple(a ^ b for a, b in zip(row[1:-1], e))
    ed = shrink(d, rule)
    return tuple(a ^ b ^ c for a, b, c in zip(e[1:-1], ee, ed))


def step_ring(state, n, rule):
    """MSB is the leftmost displayed site; supports aliased n=1,2 rings."""
    mask = (1 << n) - 1
    left = (state >> 1) | ((state & 1) << (n - 1))
    right = ((state << 1) & mask) | (state >> (n - 1))
    out = 0
    for index in range(8):
        if (rule >> index) & 1:
            a = left if index & 4 else left ^ mask
            b = state if index & 2 else state ^ mask
            c = right if index & 1 else right ^ mask
            out |= a & b & c
    return out


def g_ring(state, n, rule):
    e = step_ring(state, n, rule)
    return e ^ step_ring(e, n, rule) ^ step_ring(state ^ e, n, rule)


def trace(state, n, rule):
    e = step_ring(state, n, rule)
    fmt = lambda value: format(value, f"0{n}b")
    return {"S": fmt(state), "E": fmt(e), "D": fmt(state ^ e),
            "G": fmt(g_ring(state, n, rule)),
            "next_G": fmt(g_ring(e, n, rule))}


def local_factor(radius):
    m = max(radius + 2, 3)
    seen, required = {}, {}
    conflict = None
    for value in range(1 << (2*m + 1)):
        row = bits(value, 2*m + 1)
        g = groovy_word(row, 110)
        patch = g[m - 2 - radius:m - 1 + radius]
        target = groovy_word(shrink(row, 110), 110)[m - 3]
        required.setdefault(patch, set()).add(target)
        if patch not in seen:
            seen[patch] = (row, target)
        elif seen[patch][1] != target and conflict is None:
            conflict = {"source_words": [word(seen[patch][0]), word(row)],
                        "G_patch": word(patch),
                        "next_G_center": [seen[patch][1], target]}
    passed = conflict is None
    table = [next(iter(required.get(bits(p, 2*radius+1), {0})))
             for p in range(1 << (2*radius+1))] if passed else None
    return {"R": radius, "status": "factor" if passed else "conflict",
            "source_radius": m, "source_windows": 1 << (2*m + 1),
            "realized_patches": len(required),
            "required_targets": {word(p): sorted(ts) for p, ts in sorted(required.items())},
            "table_zero_off_image": table, "conflict": conflict}


def evaluate():
    deadline = time.monotonic() + 120
    out = {
        "schema": "groovy-g-autonomy-v1", "rule": 110,
        "domain": "full binary integer line; cadence one; original-source G",
        "base_main": "5aee7bb9ac6c70eaa114a8ed5baf38ba6b10e8c1",
        "protocol_reviewed_commit": "ad38b4937321501889b6b8a1caab4e4bfb54052e",
        "source_hashes": {p: digest(p) for p in SOURCES},
        "controls": {"C1_rule32_factor": {"status": "not_evaluated"},
                     "C2_rule90_constant": {"status": "not_evaluated"}},
        "predictions": {"P1_no_full_shift_factor": "unresolved_within_budget"},
        "prediction_context": "001/011 collision candidate hand-derived after protocol freeze, before execution",
        "local": [{"R": r, "status": "not_evaluated"} for r in (0, 1, 2)],
        "rings": [{"n": n, "status": "not_evaluated", "states_visited": 0}
                  for n in range(1, 17)],
        "witness": None, "status": "incomplete", "protocol_deviations": [],
    }
    try:
        ok32 = all(groovy_word(shrink(bits(s, 7), 32), 32)[0]
                   == shrink(groovy_word(bits(s, 7), 32), 128)[0]
                   for s in range(128))
        out["controls"]["C1_rule32_factor"] = {
            "status": "pass" if ok32 else "fail", "source_windows": 128,
            "identity": "G_32 E_32 = E_128 G_32"}
        ok90 = all(groovy_word(bits(s, 5), 90) == (0,) for s in range(32))
        out["controls"]["C2_rule90_constant"] = {
            "status": "pass" if ok90 else "fail", "source_windows": 32,
            "identity": "G_90 = 0"}
        if not (ok32 and ok90):
            out["status"] = "invalid_controls"
            out["predictions"]["P1_no_full_shift_factor"] = "not_evaluated_invalid_controls"
            return out
        for r in (0, 1, 2):
            out["local"][r] = local_factor(r)
        if any(x["status"] == "factor" for x in out["local"]):
            out["status"] = "exact_local_factor"
            out["predictions"]["P1_no_full_shift_factor"] = "refuted_by_local_factor"
            for row in out["rings"]:
                row["status"] = "not_needed_local_factor"
            return out
        for rec in out["rings"]:
            n = rec["n"]
            seen = {}
            rec["status"] = "in_progress"
            for s in range(1 << n):
                if time.monotonic() >= deadline:
                    raise TimeoutError
                g = g_ring(s, n, 110)
                ng = g_ring(step_ring(s, n, 110), n, 110)
                rec["states_visited"] += 1
                if g in seen and seen[g][1] != ng:
                    rec["status"] = "collision"
                    out["witness"] = {"n": n, "sources": [trace(seen[g][0], n, 110), trace(s, n, 110)]}
                    for later in out["rings"][n:]:
                        later["status"] = "not_run_after_witness"
                    out["status"] = "no_full_shift_factor"
                    out["predictions"]["P1_no_full_shift_factor"] = "supported_by_counterexample"
                    return out
                seen.setdefault(g, (s, ng))
            rec["status"] = "no_collision_on_this_ring"
            rec["distinct_G_words"] = len(seen)
        out["status"] = "bounded_inconclusive"
    except (TimeoutError, MemoryError) as exc:
        out["status"] = "resource_censored"
        out["resource_limit"] = type(exc).__name__
        for row in out["rings"]:
            if row["status"] == "in_progress":
                row["status"] = "incomplete_resource_limit"
    return out


def integrity():
    import check_result_integrity as shared
    shared.REGISTRY[RESULT] = {p: p for p in SOURCES}
    problems = shared.check(RESULT)
    if problems:
        raise SystemExit("\n".join(problems))
    print("Source integrity passed:", RESULT)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--integrity", action="store_true")
    args = parser.parse_args()
    if args.integrity:
        integrity()
        return
    _, hard = resource.getrlimit(resource.RLIMIT_AS)
    cap = 1024**3 if hard == resource.RLIM_INFINITY else min(1024**3, hard)
    resource.setrlimit(resource.RLIMIT_AS, (cap, hard))
    if args.check:
        integrity()
    started = datetime.now(timezone.utc).isoformat()
    t0 = time.monotonic()
    result = evaluate()
    if args.write:
        if (ROOT / RESULT).exists() or (ROOT / EXECUTION).exists():
            raise SystemExit("Refusing to overwrite preserved evaluation artifacts")
        (ROOT / RESULT).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        record = {"implementation_commit": subprocess.check_output(
                      ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                  "started_utc": started, "finished_utc": datetime.now(timezone.utc).isoformat(),
                  "elapsed_seconds": time.monotonic()-t0,
                  "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  "wall_budget_seconds": 120, "memory_budget_bytes": cap,
                  "result_sha256": digest(RESULT)}
        (ROOT / EXECUTION).parent.mkdir(parents=True, exist_ok=True)
        (ROOT / EXECUTION).write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    else:
        saved = json.loads((ROOT / RESULT).read_text())
        if result != saved:
            raise SystemExit("Scientific replay differs from preserved result")
    print(json.dumps({"status": result["status"], "controls": result["controls"],
                      "local": [{k: r[k] for k in ("R", "status")} for r in result["local"]],
                      "witness": result["witness"]}, indent=2))


if __name__ == "__main__":
    main()
