"""Exact two-switch LRL/RLR source-recoder census using fine-ECA CNF/Minisat22."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from collections import Counter
from pathlib import Path

from pysat.solvers import Minisat22

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from recover_phase_splice_sat import (  # noqa:E402
    CNFBuilder,
    bit_pattern,
    bits_to_macro,
    evolve_cnf,
    fine_evolve,
    macro_to_bits,
    rule_table,
)

PROTOCOL = ROOT / "docs/research/protocols/two-switch-rail-selector-20260910.md"
DOMAIN_RESULT = ROOT / "results/phase_splice_source_recoder_20260909.json"
DOMAIN_SHA256 = "af00ce04f134bd98ecd2d2bd7a0bf2a00b2c2c5d9b7d34c2ebcd9cc22e329138"
TMAX = 6
SEED_WALL_SECONDS = 1200
MAX_CNF_VARIABLES = 1314
MAX_CNF_CLAUSES = 9943
ORIENTATIONS = ("LRL", "RLR")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ordered_deltas(k: int):
    return sorted(range(-k, k + 1), key=lambda d: (abs(d), d))


def ordered_intervals(k: int, delta: int):
    rows = []
    for u in range(-k + 1, k):
        for v in range(u, k):
            if u == v == delta:
                continue
            rows.append((u, v))
    rows.sort(key=lambda uv: (uv[1] - uv[0] + 1, uv[0], uv[1]))
    return rows


def fresh_candidates(tmax: int = TMAX):
    for t in range(2, tmax + 1):
        for j in range(1, t):
            k = t - j
            for delta in ordered_deltas(k):
                for u, v in ordered_intervals(k, delta):
                    for orientation in ORIENTATIONS:
                        yield {
                            "t": t, "k": k, "j": j, "delta": delta,
                            "u": u, "v": v, "orientation": orientation,
                        }


FAMILY_SIZE = sum(1 for _ in fresh_candidates())
assert FAMILY_SIZE == 2788, FAMILY_SIZE
assert sum(1 for _ in fresh_candidates(3)) == 62


def candidate_positions(candidate):
    t, j, delta = candidate["t"], candidate["j"], candidate["delta"]
    outside = [p for p in range(-t, t + 1) if not (delta - j <= p <= delta + j)]
    inside = [p for p in range(-t, t + 1) if delta - j <= p <= delta + j]
    return outside + inside


def select_source(candidate, q: int, z_left, z_right, bit_index: int):
    inside = candidate["u"] <= q <= candidate["v"]
    orientation = candidate["orientation"]
    if orientation == "LRL":
        return z_right[bit_index] if inside else z_left[bit_index]
    if orientation == "RLR":
        return z_left[bit_index] if inside else z_right[bit_index]
    raise ValueError(orientation)


def load_domain():
    if sha256(DOMAIN_RESULT) != DOMAIN_SHA256:
        raise AssertionError("phase-splice domain audit hash mismatch")
    x = json.loads(DOMAIN_RESULT.read_text())
    rows = []
    for lang in x["language_summaries"]:
        rows.append({
            "rule": int(lang["rule"]),
            "wclass": lang["wclass"],
            "pair_index": int(lang["pair_index"]),
            "pair": lang["pair"],
            "seed_symbol": int(lang["seed_symbol"]),
            "incoming_target_ids": list(map(int, lang["incoming_target_ids"])),
        })
    rows.sort(key=lambda r: (r["rule"], r["pair_index"]))
    assert len(rows) == 22
    assert sum(len(r["incoming_target_ids"]) for r in rows) == 170
    classes = Counter()
    for r in rows:
        classes[r["wclass"]] += len(r["incoming_target_ids"])
    assert dict(sorted(classes.items())) == {"II": 158, "III": 12}
    return rows


def build_query(rule: int, seed_pair, candidate, p: int):
    a, b = seed_pair
    t, k, j, delta = (candidate[x] for x in ("t", "k", "j", "delta"))
    assert t == k + j
    coords = list(range(p - t, p + t + 1))
    assert 0 in coords and len(coords) == 2 * t + 1 <= 13
    fine_len = 3 * len(coords)
    builder = CNFBuilder()
    left0 = [builder.var() for _ in range(fine_len)]
    right0 = [builder.var() for _ in range(fine_len)]
    abit, bbit = bit_pattern(a), bit_pattern(b)
    for block, coord in enumerate(coords):
        for bit in range(3):
            idx = 3 * block + bit
            if coord == 0:
                builder.unit(left0[idx], abit[bit])
                builder.unit(right0[idx], bbit[bit])
            else:
                builder.equal(left0[idx], right0[idx])

    table = rule_table(rule)
    z_left = evolve_cnf(builder, left0, table, 3 * k)
    z_right = evolve_cnf(builder, right0, table, 3 * k)
    assert len(z_left) == len(z_right) == 3 * (2 * j + 1)
    actual_left = evolve_cnf(builder, z_left, table, 3 * j)
    actual_right = evolve_cnf(builder, z_right, table, 3 * j)
    assert len(actual_left) == len(actual_right) == 3

    rec_left, rec_right = [], []
    for block, q in enumerate(range(p - j, p + j + 1)):
        for bit in range(3):
            zidx = 3 * block + bit
            if q == delta:
                lv, rv = builder.var(), builder.var()
                builder.unit(lv, abit[bit])
                builder.unit(rv, bbit[bit])
                rec_left.append(lv)
                rec_right.append(rv)
            else:
                common = select_source(candidate, q, z_left, z_right, zidx)
                rec_left.append(common)
                rec_right.append(common)

    out_left = evolve_cnf(builder, rec_left, table, 3 * j)
    out_right = evolve_cnf(builder, rec_right, table, 3 * j)
    mismatch = []
    for x, y in zip(actual_left + actual_right, out_left + out_right):
        d = builder.var()
        builder.xor_gate(x, y, d)
        mismatch.append(d)
    builder.clauses.append(mismatch)
    if builder.variables > MAX_CNF_VARIABLES or len(builder.clauses) > MAX_CNF_CLAUSES:
        raise AssertionError(("CNF structural ceiling regression", builder.variables, len(builder.clauses)))
    return builder, left0, coords


def replay_model(rule: int, seed_pair, candidate, p: int, coords, left0, model):
    positive = {x for x in model if x > 0}
    a, b = seed_pair
    bg = {}
    for block, coord in enumerate(coords):
        if coord == 0:
            continue
        symbol = 0
        for bit in range(3):
            if left0[3 * block + bit] in positive:
                symbol |= 1 << bit
        bg[coord] = symbol
    row_left = [a if q == 0 else bg[q] for q in coords]
    row_right = [b if q == 0 else bg[q] for q in coords]
    t, k, j, delta = (candidate[x] for x in ("t", "k", "j", "delta"))
    zlb = fine_evolve(macro_to_bits(row_left), rule, 3 * k)
    zrb = fine_evolve(macro_to_bits(row_right), rule, 3 * k)
    zl, zr = bits_to_macro(zlb), bits_to_macro(zrb)
    actual_l = bits_to_macro(fine_evolve(zlb, rule, 3 * j))[0]
    actual_r = bits_to_macro(fine_evolve(zrb, rule, 3 * j))[0]
    rec_l, rec_r = [], []
    for idx, q in enumerate(range(p - j, p + j + 1)):
        if q == delta:
            rec_l.append(a)
            rec_r.append(b)
        else:
            inside = candidate["u"] <= q <= candidate["v"]
            if candidate["orientation"] == "LRL":
                common = zr[idx] if inside else zl[idx]
            else:
                common = zl[idx] if inside else zr[idx]
            rec_l.append(common)
            rec_r.append(common)
    out_l = bits_to_macro(fine_evolve(macro_to_bits(rec_l), rule, 3 * j))[0]
    out_r = bits_to_macro(fine_evolve(macro_to_bits(rec_r), rule, 3 * j))[0]
    assert actual_l != out_l or actual_r != out_r
    return {
        "position": p,
        "window_start": coords[0],
        "background_word": [None if q == 0 else bg[q] for q in coords],
        "actual_outputs": [actual_l, actual_r],
        "recoded_outputs": [out_l, out_r],
        "replay_pass": True,
    }


def solve_position(rule: int, seed_pair, candidate, p: int):
    builder, left0, coords = build_query(rule, seed_pair, candidate, p)
    started = time.perf_counter()
    with Minisat22(bootstrap_with=builder.clauses) as solver:
        is_sat = solver.solve()
        seconds = time.perf_counter() - started
        model = solver.get_model() if is_sat else None
    out = {
        "status": "sat" if is_sat else "unsat",
        "cnf_variables": builder.variables,
        "cnf_clauses": len(builder.clauses),
        "solver_seconds": seconds,
    }
    if is_sat:
        out["counterexample"] = replay_model(rule, seed_pair, candidate, p, coords, left0, model)
    return out


def check_candidate(rule: int, seed_pair, candidate, deadline=None):
    checked = 0
    max_vars = max_clauses = 0
    solver_seconds = 0.0
    for p in candidate_positions(candidate):
        if deadline is not None and time.perf_counter() >= deadline:
            return {**candidate, "status": "censored", "reason": "seed-wall-time", "checked_positions": checked,
                    "max_cnf_variables": max_vars, "max_cnf_clauses": max_clauses, "solver_seconds": solver_seconds}
        q = solve_position(rule, seed_pair, candidate, p)
        checked += 1
        max_vars = max(max_vars, q["cnf_variables"])
        max_clauses = max(max_clauses, q["cnf_clauses"])
        solver_seconds += q["solver_seconds"]
        if q["status"] == "sat":
            return {**candidate, "status": "fail", "failing_position": p, "checked_positions": checked,
                    "counterexample": q["counterexample"], "max_cnf_variables": max_vars,
                    "max_cnf_clauses": max_clauses, "solver_seconds": solver_seconds}
    return {**candidate, "status": "pass", "checked_positions": checked,
            "max_cnf_variables": max_vars, "max_cnf_clauses": max_clauses, "solver_seconds": solver_seconds}


def run_controls():
    positive = {"t": 3, "k": 2, "j": 1, "delta": 0, "u": -1, "v": 1, "orientation": "LRL"}
    r204 = check_candidate(204, (0, 1), positive)
    if r204["status"] != "pass":
        raise AssertionError(("Rule204 two-switch positive control failed", r204))
    negatives = []
    for candidate in fresh_candidates(3):
        rec = check_candidate(35, (2, 6), candidate)
        if rec["status"] != "fail" or not rec["counterexample"]["replay_pass"]:
            raise AssertionError(("Rule35 two-switch negative control failed", rec))
        negatives.append(rec)
    assert len(negatives) == 62
    return {
        "ok": True,
        "rule204": {"status": "pass", "candidate": positive, "checked_positions": r204["checked_positions"],
                    "max_cnf_variables": r204["max_cnf_variables"], "max_cnf_clauses": r204["max_cnf_clauses"]},
        "rule35": {"all_fail": True, "fresh_candidates_t_le_3": len(negatives),
                   "max_cnf_variables": max(x["max_cnf_variables"] for x in negatives),
                   "max_cnf_clauses": max(x["max_cnf_clauses"] for x in negatives)},
    }


def run_seed(seed_index: int):
    domain = load_domain()
    row = domain[seed_index]
    a, b = map(int, row["pair"].split("-"))
    started = time.perf_counter()
    deadline = started + SEED_WALL_SECONDS
    tested = []
    first_certificate = None
    max_vars = max_clauses = 0
    solver_seconds = 0.0
    for candidate in fresh_candidates():
        if time.perf_counter() >= deadline:
            status = "censored"
            break
        rec = check_candidate(row["rule"], (a, b), candidate, deadline)
        tested.append(rec)
        max_vars = max(max_vars, rec["max_cnf_variables"])
        max_clauses = max(max_clauses, rec["max_cnf_clauses"])
        solver_seconds += rec["solver_seconds"]
        if rec["status"] == "pass":
            first_certificate = rec
            status = "two-switch-certified"
            break
        if rec["status"] == "censored":
            status = "censored"
            break
    else:
        status = "no-two-switch-through-6"
    return {
        **row,
        "seed_index": seed_index,
        "status": status,
        "tested_candidates": len(tested),
        "frozen_family_candidates": FAMILY_SIZE,
        "first_certificate": first_certificate,
        "max_cnf_variables": max_vars,
        "max_cnf_clauses": max_clauses,
        "solver_seconds": solver_seconds,
        "elapsed_seconds": time.perf_counter() - started,
        "tested": tested,
    }


def provenance():
    return {
        "scripts/experiment_two_switch_rail_selector_sat.py": sha256(Path(__file__)),
        str(PROTOCOL.relative_to(ROOT)): sha256(PROTOCOL),
        str(DOMAIN_RESULT.relative_to(ROOT)): DOMAIN_SHA256,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--controls-only", action="store_true")
    ap.add_argument("--seed-index", type=int)
    args = ap.parse_args()
    if args.controls_only == (args.seed_index is not None):
        raise SystemExit("choose exactly one of --controls-only or --seed-index")
    if args.controls_only:
        out = {"ok": True, "experiment": "two-switch-rail-selector-controls", "solver": "Minisat22 via python-sat",
               "family_size": FAMILY_SIZE, "source_hashes": provenance(), "controls": run_controls()}
    else:
        if not (0 <= args.seed_index < 22):
            raise SystemExit("bad seed index")
        out = {"ok": True, "experiment": "two-switch-rail-selector-seed", "solver": "Minisat22 via python-sat",
               "seed_wall_seconds": SEED_WALL_SECONDS, "family_size": FAMILY_SIZE,
               "source_hashes": provenance(), "result": run_seed(args.seed_index)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, separators=(",", ":")) + "\n")
    if args.controls_only:
        print(json.dumps(out["controls"], indent=2))
    else:
        r = out["result"]
        print(json.dumps({k: r[k] for k in ("seed_index", "rule", "pair", "status", "tested_candidates",
                                             "max_cnf_variables", "max_cnf_clauses", "elapsed_seconds")}, indent=2))


if __name__ == "__main__":
    main()
