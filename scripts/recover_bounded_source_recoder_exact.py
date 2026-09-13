#!/usr/bin/env python3
"""Exact, resumable recovery for censored bounded source-recoder synthesis cases.

Solver-slice exhaustion refines a finite partition; it is never a scientific result.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing as mp
import sys
import time
from collections import Counter
from pathlib import Path

from pysat.solvers import Solver

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import experiment_bounded_source_recoder_synthesis as base  # noqa:E402

PROTOCOL = ROOT / "docs/research/protocols/bounded-source-recoder-exact-recovery-20260910.md"
PARENT_RESULT = ROOT / "results/bounded_source_recoder_synthesis_20260910.json"
PARENT_SHA256 = "2d28a4d5e4b668f9a201f3658a986060712a2f9069577810aacd08a49e7f12f2"
RECOVERY_SEEDS = (1, 6, 11, 14, 16, 17, 18, 20)
SOLVERS = ("cadical195", "glucose4", "maplechrono", "minisat22")
SOLVER_SLICE_SECONDS = 10.0
DEFAULT_BATCH_SECONDS = 2700.0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_parent():
    if sha256(PARENT_RESULT) != PARENT_SHA256:
        raise AssertionError("parent bounded-source-recoder result hash mismatch")
    out = json.loads(PARENT_RESULT.read_text())
    rows = out.get("seed_results")
    if not isinstance(rows, list) or len(rows) != 22:
        raise AssertionError("unexpected parent seed_results")
    by_index = {int(r["seed_index"]): r for r in rows}
    censored = {i for i, r in by_index.items() if r["status"] == "censored"}
    if set(RECOVERY_SEEDS) != censored:
        raise AssertionError("recovery set differs from parent censoring set")
    return out, by_index


def candidates():
    return list(base.structural_candidates())


def candidate_key(c):
    return tuple(int(c[k]) for k in ("m", "t", "k", "j", "delta"))


def parent_start_ordinal(parent_row):
    frozen = candidates()
    attempted = parent_row.get("structures", [])
    for i, rec in enumerate(attempted):
        if i >= len(frozen) or candidate_key(rec) != candidate_key(frozen[i]):
            raise AssertionError(("parent structural order mismatch", i))
        if rec["status"] != "exact-negative":
            return i
    return len(attempted)


def fresh_stats():
    return {
        "solver_timeouts": Counter(),
        "solver_unavailable": Counter(),
        "solver_errors": Counter(),
        "solver_decisions": Counter(),
        "solver_seconds": Counter(),
        "last_solver_error": {},
        "partition_splits": 0,
        "direct_leaves": 0,
    }


def stats_to_json(stats):
    return {
        k: (dict(sorted(v.items())) if isinstance(v, Counter) else v)
        for k, v in stats.items()
    }


def merge_stats(dst, src):
    for key in ("solver_timeouts", "solver_unavailable", "solver_errors", "solver_decisions"):
        dst[key].update(src.get(key, {}))
    for name, seconds in src.get("solver_seconds", {}).items():
        dst["solver_seconds"][name] += float(seconds)
    dst["last_solver_error"].update(src.get("last_solver_error", {}))
    dst["partition_splits"] += int(src.get("partition_splits", 0))
    dst["direct_leaves"] += int(src.get("direct_leaves", 0))


def _solver_worker(name, clauses, assumptions, queue):
    try:
        with Solver(name=name, bootstrap_with=clauses) as solver:
            sat = solver.solve(assumptions=assumptions)
            model = solver.get_model() if sat else None
        queue.put(("sat" if sat else "unsat", model, None))
    except BaseException as exc:
        queue.put(("error", None, f"{type(exc).__name__}: {exc}"))


def portfolio_solve(clauses, assumptions, slice_seconds, stats):
    """Return ('sat', model), ('unsat', None), or ('split', None)."""
    ctx = mp.get_context("fork" if sys.platform != "win32" else "spawn")
    for name in SOLVERS:
        q = ctx.Queue(maxsize=1)
        p = ctx.Process(target=_solver_worker, args=(name, clauses, assumptions, q))
        started = time.perf_counter()
        p.start()
        p.join(max(0.0, slice_seconds))
        elapsed = time.perf_counter() - started
        stats["solver_seconds"][name] += elapsed
        if p.is_alive():
            p.terminate()
            p.join()
            stats["solver_timeouts"][name] += 1
            q.close()
            continue
        if q.empty():
            stats["solver_errors"][name] += 1
            q.close()
            continue
        kind, model, error = q.get()
        q.close()
        if kind == "error":
            stats["solver_unavailable"][name] += 1
            if error:
                stats["last_solver_error"][name] = error[:500]
            continue
        stats["solver_decisions"][name] += 1
        return kind, model
    if stats["solver_unavailable"].get("minisat22", 0) and not stats["solver_timeouts"].get("minisat22", 0):
        raise RuntimeError("required minisat22 backend unavailable")
    return "split", None


def clause_satisfied(clause, truth):
    return any((lit > 0) == truth[abs(lit)] for lit in clause)


def decode_machine(cand, choice, nxt, model):
    positive = {x for x in model if x > 0}
    machine = {"m": cand["m"], "choice": [], "next": []}
    for s in range(cand["m"]):
        machine["choice"].append([1 if choice[s][code] in positive else 0 for code in range(64)])
        row = []
        for code in range(64):
            qnext = next((q for q, v in enumerate(nxt[s][code]) if v in positive), None)
            if qnext is None:
                raise AssertionError("missing synthesized transition")
            row.append(qnext)
        machine["next"].append(row)
    return machine


def partition_synthesis(rule, seed_pair, cand, examples, queue_state, deadline, stats, slice_seconds):
    builder = base.CNFBuilder()
    choice, nxt = base.table_variables(builder, cand["m"])
    for ex in examples:
        base.add_example_constraints(builder, rule, seed_pair, cand, ex, choice, nxt)
    nvars = builder.variables
    semantic = [v for row in choice for v in row]
    semantic += [v for state_rows in nxt for code_row in state_rows for v in code_row]
    semantic_set = set(semantic)
    split_vars = semantic + [v for v in range(1, nvars + 1) if v not in semantic_set]
    stack = [list(map(int, a)) for a in (queue_state or [[]])]
    while stack:
        if time.perf_counter() >= deadline:
            return {"status": "pending", "queue": stack}
        assumptions = stack.pop()
        kind, model = portfolio_solve(builder.clauses, assumptions, slice_seconds, stats)
        if kind == "sat":
            return {"status": "sat", "machine": decode_machine(cand, choice, nxt, model)}
        if kind == "unsat":
            continue
        assigned = {abs(lit) for lit in assumptions}
        split = next((v for v in split_vars if v not in assigned), None)
        if split is None:
            truth = {abs(lit): lit > 0 for lit in assumptions}
            if len(truth) != nvars:
                raise AssertionError("full synthesis leaf missing variables")
            stats["direct_leaves"] += 1
            if all(clause_satisfied(c, truth) for c in builder.clauses):
                model = [v if truth[v] else -v for v in range(1, nvars + 1)]
                return {"status": "sat", "machine": decode_machine(cand, choice, nxt, model)}
            continue
        stats["partition_splits"] += 1
        stack.append(assumptions + [split])
        stack.append(assumptions + [-split])
    return {"status": "unsat"}


def ordered_background_vars(left0, coords):
    rows = []
    for block, q in enumerate(coords):
        if q == 0:
            continue
        for bit in range(3):
            rows.append((abs(q), q, bit, left0[3 * block + bit]))
    rows.sort(key=lambda x: (x[0], x[1], x[2]))
    return [v for _, _, _, v in rows]


def background_from_model(left0, coords, model):
    positive = {x for x in model if x > 0}
    bg = {}
    for block, q in enumerate(coords):
        if q == 0:
            continue
        sym = 0
        for bit in range(3):
            if left0[3 * block + bit] in positive:
                sym |= 1 << bit
        bg[q] = sym
    return bg


def background_from_literals(left0, coords, literals):
    truth = {abs(lit): lit > 0 for lit in literals}
    bg = {}
    for block, q in enumerate(coords):
        if q == 0:
            continue
        sym = 0
        for bit in range(3):
            v = left0[3 * block + bit]
            if truth[v]:
                sym |= 1 << bit
        bg[q] = sym
    return bg


def verify_position_partition(rule, seed_pair, cand, machine, p, queue_state, deadline, stats, slice_seconds):
    builder, left0, coords = base.build_verify_query(rule, seed_pair, cand, machine, p)
    split_vars = ordered_background_vars(left0, coords)
    stack = [list(map(int, a)) for a in (queue_state or [[]])]
    while stack:
        if time.perf_counter() >= deadline:
            return {"status": "pending", "queue": stack}
        assumptions = stack.pop()
        kind, model = portfolio_solve(builder.clauses, assumptions, slice_seconds, stats)
        if kind == "sat":
            bg = background_from_model(left0, coords, model)
            ex = base.replay_machine(rule, seed_pair, cand, machine, p, coords, bg)
            return {"status": "counterexample", "counterexample": ex}
        if kind == "unsat":
            continue
        assigned = {abs(lit) for lit in assumptions}
        split = next((v for v in split_vars if v not in assigned), None)
        if split is None:
            stats["direct_leaves"] += 1
            bg = background_from_literals(left0, coords, assumptions)
            try:
                ex = base.replay_machine(rule, seed_pair, cand, machine, p, coords, bg)
            except AssertionError as exc:
                if str(exc) != "SAT verifier model did not replay":
                    raise
                continue
            return {"status": "counterexample", "counterexample": ex}
        stats["partition_splits"] += 1
        stack.append(assumptions + [split])
        stack.append(assumptions + [-split])
    return {"status": "unsat"}


def recover_structure(rule, seed_pair, cand, state, deadline, stats, slice_seconds):
    state = dict(state or {})
    examples = list(state.get("examples", []))
    phase = state.get("phase", "synthesis")
    synth_queue = state.get("synthesis_queue")
    machine = state.get("machine")
    pos_index = int(state.get("position_index", 0))
    verify_queue = state.get("verification_queue")
    iterations = int(state.get("iterations", 0))
    while True:
        if time.perf_counter() >= deadline:
            return {"status": "pending", "checkpoint": {
                "phase": phase, "examples": examples, "synthesis_queue": synth_queue,
                "machine": machine, "position_index": pos_index,
                "verification_queue": verify_queue, "iterations": iterations}}
        if phase == "synthesis":
            syn = partition_synthesis(rule, seed_pair, cand, examples, synth_queue,
                                      deadline, stats, slice_seconds)
            if syn["status"] == "pending":
                return {"status": "pending", "checkpoint": {
                    "phase": "synthesis", "examples": examples,
                    "synthesis_queue": syn["queue"], "machine": None,
                    "position_index": 0, "verification_queue": None,
                    "iterations": iterations}}
            if syn["status"] == "unsat":
                return {"status": "exact-negative", "iterations": iterations,
                        "counterexamples": len(examples)}
            machine = syn["machine"]
            iterations += 1
            phase, pos_index, verify_queue, synth_queue = "verification", 0, None, None
            continue
        positions = base.candidate_positions(cand)
        if pos_index >= len(positions):
            return {"status": "certificate", "machine": machine,
                    "iterations": iterations, "counterexamples": len(examples)}
        p = positions[pos_index]
        ver = verify_position_partition(rule, seed_pair, cand, machine, p,
                                        verify_queue, deadline, stats, slice_seconds)
        if ver["status"] == "pending":
            return {"status": "pending", "checkpoint": {
                "phase": "verification", "examples": examples,
                "synthesis_queue": None, "machine": machine,
                "position_index": pos_index, "verification_queue": ver["queue"],
                "iterations": iterations}}
        if ver["status"] == "counterexample":
            examples.append(ver["counterexample"])
            phase, machine, pos_index, verify_queue, synth_queue = "synthesis", None, 0, None, None
            continue
        pos_index += 1
        verify_queue = None


def blank_checkpoint(seed_index, parent_row):
    start = parent_start_ordinal(parent_row)
    return {"schema": 1, "seed_index": seed_index, "rule": int(parent_row["rule"]),
            "pair": parent_row["pair"], "status": "pending",
            "parent_start_ordinal": start, "current_ordinal": start,
            "recovery_exact_negative_structures": [], "structure_checkpoint": None,
            "certificate": None, "batches": 0, "stats": stats_to_json(fresh_stats())}


def load_checkpoint(path, seed_index, parent_row):
    if path and path.exists():
        cp = json.loads(path.read_text())
        if (int(cp["seed_index"]), int(cp["rule"]), cp["pair"]) != (seed_index, int(parent_row["rule"]), parent_row["pair"]):
            raise AssertionError("checkpoint identity mismatch")
        return cp
    return blank_checkpoint(seed_index, parent_row)


def provenance():
    return {"scripts/recover_bounded_source_recoder_exact.py": sha256(Path(__file__)),
            str(PROTOCOL.relative_to(ROOT)): sha256(PROTOCOL),
            str(PARENT_RESULT.relative_to(ROOT)): PARENT_SHA256,
            "parent_instrument": base.sha256(Path(base.__file__))}


def run_seed(seed_index, checkpoint_path, batch_seconds, slice_seconds):
    _, rows = load_parent()
    if seed_index not in RECOVERY_SEEDS:
        raise SystemExit(f"seed {seed_index} is not in frozen recovery set")
    row = rows[seed_index]
    a, b = map(int, row["pair"].split("-"))
    cp = load_checkpoint(checkpoint_path, seed_index, row)
    if cp["status"] != "pending":
        return {"ok": True, "experiment": "bounded-source-recoder-exact-recovery-seed",
                "source_hashes": provenance(), "result": cp}
    stats = fresh_stats()
    merge_stats(stats, cp.get("stats", {}))
    cp["batches"] = int(cp.get("batches", 0)) + 1
    deadline = time.perf_counter() + batch_seconds
    frozen = candidates()
    ordinal = int(cp["current_ordinal"])
    while ordinal < len(frozen):
        cand = frozen[ordinal]
        rec = recover_structure(int(row["rule"]), (a, b), cand,
                                cp.get("structure_checkpoint"), deadline, stats, slice_seconds)
        if rec["status"] == "pending":
            cp.update(status="pending", current_ordinal=ordinal, current_candidate=cand,
                      structure_checkpoint=rec["checkpoint"], stats=stats_to_json(stats))
            break
        if rec["status"] == "certificate":
            cp.update(status="bounded-recoder-certified", current_ordinal=ordinal,
                      current_candidate=cand, structure_checkpoint=None,
                      certificate={**cand, "machine": rec["machine"],
                                   "iterations": rec["iterations"],
                                   "counterexamples": rec["counterexamples"]},
                      stats=stats_to_json(stats))
            break
        cp["recovery_exact_negative_structures"].append({
            "ordinal": ordinal, **cand, "iterations": rec["iterations"],
            "counterexamples": rec["counterexamples"]})
        ordinal += 1
        cp.update(current_ordinal=ordinal,
                  current_candidate=frozen[ordinal] if ordinal < len(frozen) else None,
                  structure_checkpoint=None)
        if time.perf_counter() >= deadline:
            cp.update(status="pending", stats=stats_to_json(stats))
            break
    else:
        cp.update(status="no-bounded-recoder-through-4", certificate=None,
                  structure_checkpoint=None, stats=stats_to_json(stats))
    cp["parent_exact_negative_prefix"] = cp["parent_start_ordinal"]
    cp["total_structures"] = len(frozen)
    cp["remaining_structures"] = max(0, len(frozen) - int(cp["current_ordinal"]))
    return {"ok": True, "experiment": "bounded-source-recoder-exact-recovery-seed",
            "source_hashes": provenance(), "result": cp}


def all_left_machine(m=1):
    return {"m": m, "choice": [[0] * 64 for _ in range(m)], "next": [[0] * 64 for _ in range(m)]}


def run_controls():
    stats = fresh_stats()
    deadline = time.perf_counter() + 900
    cand = {"m": 1, "t": 3, "k": 2, "j": 1, "delta": 0}
    machine = all_left_machine()
    for p in base.candidate_positions(cand):
        rec = verify_position_partition(5, (0, 2), cand, machine, p, None,
                                        deadline, stats, SOLVER_SLICE_SECONDS)
        if rec["status"] != "unsat":
            raise AssertionError(("Rule5 partitioned verification failed", p, rec))
    found = None
    for p in base.candidate_positions(cand):
        rec = verify_position_partition(35, (2, 6), cand, machine, p, None,
                                        deadline, stats, SOLVER_SLICE_SECONDS)
        if rec["status"] == "counterexample":
            found = rec["counterexample"]
            break
    if not found or not found.get("replay_pass"):
        raise AssertionError("Rule35 partitioned mismatch control failed")
    negatives = 0
    for m in (1, 2):
        for j in (1, 2):
            k = 3 - j
            for delta in base.ordered_deltas(k):
                c = {"m": m, "t": 3, "k": k, "j": j, "delta": delta}
                rec = recover_structure(35, (2, 6), c, None, deadline, stats, SOLVER_SLICE_SECONDS)
                if rec["status"] != "exact-negative":
                    raise AssertionError(("Rule35 synthesis control failed", c, rec))
                negatives += 1
    if negatives != 16:
        raise AssertionError(negatives)
    # Force the generic split/direct-leaf path on x AND not-x.
    tiny = fresh_stats()
    clauses, stack, exact_unsat = [[1], [-1]], [[]], True
    while stack:
        assumptions = stack.pop()
        kind, _ = portfolio_solve(clauses, assumptions, 0.0, tiny)
        if kind == "sat":
            exact_unsat = False
            break
        if kind == "unsat":
            continue
        assigned = {abs(x) for x in assumptions}
        if 1 in assigned:
            truth = {abs(x): x > 0 for x in assumptions}
            tiny["direct_leaves"] += 1
            if all(clause_satisfied(c, truth) for c in clauses):
                exact_unsat = False
                break
        else:
            tiny["partition_splits"] += 1
            stack.append([1])
            stack.append([-1])
    if not exact_unsat or tiny["partition_splits"] < 1 or tiny["direct_leaves"] < 2:
        raise AssertionError("forced split/direct leaf control failed")
    return {"ok": True, "rule5_verified_positions": len(base.candidate_positions(cand)),
            "rule35_replayed_counterexample": found,
            "rule35_exact_negative_structures": negatives,
            "forced_split_direct_leaf": stats_to_json(tiny),
            "portfolio_stats": stats_to_json(stats)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--seed-index", type=int)
    ap.add_argument("--checkpoint-in", type=Path)
    ap.add_argument("--batch-seconds", type=float, default=DEFAULT_BATCH_SECONDS)
    ap.add_argument("--solver-slice-seconds", type=float, default=SOLVER_SLICE_SECONDS)
    ap.add_argument("--controls-only", action="store_true")
    args = ap.parse_args()
    if args.controls_only == (args.seed_index is not None):
        raise SystemExit("choose exactly one of --controls-only or --seed-index")
    if args.controls_only:
        out = {"ok": True, "experiment": "bounded-source-recoder-exact-recovery-controls",
               "source_hashes": provenance(), "controls": run_controls()}
    else:
        out = run_seed(args.seed_index, args.checkpoint_in, args.batch_seconds, args.solver_slice_seconds)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out["controls"] if args.controls_only else {
        k: out["result"].get(k) for k in ("seed_index", "rule", "pair", "status",
        "parent_start_ordinal", "current_ordinal", "remaining_structures", "batches")
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
