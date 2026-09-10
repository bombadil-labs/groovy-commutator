"""Independent fine-ECA CNF recovery for the 12 censored phase-splice sentinels."""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

from pysat.solvers import Minisat22

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "docs/research/protocols/phase-splice-sat-recovery-20260910.md"
TMAX = 6
SEED_WALL_SECONDS = 1200
FRESH_POLICIES = ("LR", "RL")
CASES = (
    (122, (1, 4)), (122, (1, 5)), (122, (3, 6)), (122, (3, 7)), (122, (4, 5)), (122, (6, 7)),
    (161, (0, 1)), (161, (0, 4)), (161, (1, 4)), (161, (2, 3)), (161, (2, 6)), (161, (3, 6)),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bit_pattern(symbol: int):
    return tuple((symbol >> i) & 1 for i in range(3))


def rule_table(rule: int):
    return tuple((rule >> i) & 1 for i in range(8))


def ordered_deltas(k: int):
    return sorted(range(-k, k + 1), key=lambda d: (abs(d), d))


def fresh_candidates(tmax: int = TMAX):
    for t in range(2, tmax + 1):
        for j in range(1, t):
            k = t - j
            for delta in ordered_deltas(k):
                for policy in FRESH_POLICIES:
                    yield {"t": t, "k": k, "j": j, "delta": delta, "policy": policy}


def candidate_positions(candidate):
    t, j, delta = candidate["t"], candidate["j"], candidate["delta"]
    outside = [p for p in range(-t, t + 1) if not (delta - j <= p <= delta + j)]
    inside = [p for p in range(-t, t + 1) if delta - j <= p <= delta + j]
    return outside + inside


class CNFBuilder:
    def __init__(self):
        self.next_var = 1
        self.clauses: list[list[int]] = []

    def var(self):
        v = self.next_var
        self.next_var += 1
        return v

    @property
    def variables(self):
        return self.next_var - 1

    def unit(self, v, value):
        self.clauses.append([v if value else -v])

    def equal(self, a, b):
        self.clauses.append([-a, b])
        self.clauses.append([a, -b])

    def truth_gate(self, inputs, output, table):
        for idx in range(8):
            bits = ((idx >> 2) & 1, (idx >> 1) & 1, idx & 1)
            clause = [(-v if bit else v) for v, bit in zip(inputs, bits)]
            clause.append(output if table[idx] else -output)
            self.clauses.append(clause)

    def xor_gate(self, a, b, out):
        self.clauses.extend([
            [-a, -b, -out],
            [a, b, -out],
            [a, -b, out],
            [-a, b, out],
        ])


def evolve_cnf(builder: CNFBuilder, row, table, steps: int):
    out = list(row)
    for _ in range(steps):
        nxt = []
        for i in range(len(out) - 2):
            z = builder.var()
            builder.truth_gate((out[i], out[i + 1], out[i + 2]), z, table)
            nxt.append(z)
        out = nxt
    return out


def select_source(policy: str, q: int, delta: int, z_left, z_right, bit_index: int):
    if policy == "LL":
        return z_left[bit_index]
    if policy == "RR":
        return z_right[bit_index]
    if policy == "LR":
        return z_left[bit_index] if q < delta else z_right[bit_index]
    if policy == "RL":
        return z_right[bit_index] if q < delta else z_left[bit_index]
    raise ValueError(policy)


def build_query(rule: int, seed_pair, candidate, p: int):
    a, b = seed_pair
    t, k, j, delta, policy = (candidate[x] for x in ("t", "k", "j", "delta", "policy"))
    assert t == k + j
    coords = list(range(p - t, p + t + 1))
    assert 0 in coords and len(coords) == 2 * t + 1
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

    rec_left = []
    rec_right = []
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
                common = select_source(policy, q, delta, z_left, z_right, zidx)
                rec_left.append(common)
                rec_right.append(common)

    out_left = evolve_cnf(builder, rec_left, table, 3 * j)
    out_right = evolve_cnf(builder, rec_right, table, 3 * j)
    assert len(out_left) == len(out_right) == 3

    mismatch = []
    for x, y in zip(actual_left + actual_right, out_left + out_right):
        d = builder.var()
        builder.xor_gate(x, y, d)
        mismatch.append(d)
    builder.clauses.append(mismatch)
    return builder, left0, right0, coords


def fine_evolve(row, rule: int, steps: int):
    table = rule_table(rule)
    out = list(row)
    for _ in range(steps):
        out = [table[4 * out[i] + 2 * out[i + 1] + out[i + 2]] for i in range(len(out) - 2)]
    return out


def macro_to_bits(word):
    out = []
    for symbol in word:
        out.extend(bit_pattern(symbol))
    return out


def bits_to_macro(bits):
    assert len(bits) % 3 == 0
    out = []
    for i in range(0, len(bits), 3):
        out.append(bits[i] | (bits[i + 1] << 1) | (bits[i + 2] << 2))
    return out


def replay_model(rule: int, seed_pair, candidate, p: int, coords, left0, right0, model):
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
    t, k, j, delta, policy = (candidate[x] for x in ("t", "k", "j", "delta", "policy"))
    zlb = fine_evolve(macro_to_bits(row_left), rule, 3 * k)
    zrb = fine_evolve(macro_to_bits(row_right), rule, 3 * k)
    zl, zr = bits_to_macro(zlb), bits_to_macro(zrb)
    actual_l_bits = fine_evolve(zlb, rule, 3 * j)
    actual_r_bits = fine_evolve(zrb, rule, 3 * j)
    actual_l = bits_to_macro(actual_l_bits)[0]
    actual_r = bits_to_macro(actual_r_bits)[0]
    rec_l, rec_r = [], []
    for idx, q in enumerate(range(p - j, p + j + 1)):
        if q == delta:
            rec_l.append(a)
            rec_r.append(b)
        else:
            if policy == "LL":
                common = zl[idx]
            elif policy == "RR":
                common = zr[idx]
            elif policy == "LR":
                common = zl[idx] if q < delta else zr[idx]
            elif policy == "RL":
                common = zr[idx] if q < delta else zl[idx]
            else:
                raise ValueError(policy)
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
    builder, left0, right0, coords = build_query(rule, seed_pair, candidate, p)
    started = time.perf_counter()
    with Minisat22(bootstrap_with=builder.clauses) as solver:
        is_sat = solver.solve()
        seconds = time.perf_counter() - started
        model = solver.get_model() if is_sat else None
    rec = {
        "position": p,
        "status": "sat" if is_sat else "unsat",
        "cnf_variables": builder.variables,
        "cnf_clauses": len(builder.clauses),
        "solver_seconds": seconds,
    }
    if is_sat:
        rec["counterexample"] = replay_model(rule, seed_pair, candidate, p, coords, left0, right0, model)
    return rec


def check_candidate(rule: int, seed_pair, candidate, deadline=None):
    positions = []
    max_vars = max_clauses = 0
    solver_seconds = 0.0
    for p in candidate_positions(candidate):
        if deadline is not None and time.perf_counter() >= deadline:
            return {**candidate, "status": "censored", "reason": "seed-wall-time", "positions": positions,
                    "max_cnf_variables": max_vars, "max_cnf_clauses": max_clauses, "solver_seconds": solver_seconds}
        q = solve_position(rule, seed_pair, candidate, p)
        positions.append(q)
        max_vars = max(max_vars, q["cnf_variables"])
        max_clauses = max(max_clauses, q["cnf_clauses"])
        solver_seconds += q["solver_seconds"]
        if q["status"] == "sat":
            return {**candidate, "status": "fail", "failing_position": p, "positions": positions,
                    "max_cnf_variables": max_vars, "max_cnf_clauses": max_clauses, "solver_seconds": solver_seconds}
    return {**candidate, "status": "pass", "positions": positions,
            "max_cnf_variables": max_vars, "max_cnf_clauses": max_clauses, "solver_seconds": solver_seconds}


def run_controls():
    r5c = {"t": 3, "k": 2, "j": 1, "delta": 0, "policy": "LL"}
    r5 = check_candidate(5, (0, 2), r5c)
    if r5["status"] != "pass" or any(p["status"] != "unsat" for p in r5["positions"]):
        raise AssertionError(("Rule5 SAT positive control failed", r5))
    r35 = []
    for cand in fresh_candidates(3):
        rec = check_candidate(35, (2, 6), cand)
        if rec["status"] != "fail":
            raise AssertionError(("Rule35 SAT negative control failed", rec))
        if not rec["positions"][-1]["counterexample"]["replay_pass"]:
            raise AssertionError(("Rule35 replay failed", rec))
        r35.append(rec)
    return {
        "ok": True,
        "rule5": {"status": "pass", "candidate": r5c, "positions": len(r5["positions"]),
                  "max_cnf_variables": r5["max_cnf_variables"], "max_cnf_clauses": r5["max_cnf_clauses"]},
        "rule35": {"all_fail": True, "fresh_candidates_t_le_3": len(r35),
                   "max_cnf_variables": max(x["max_cnf_variables"] for x in r35),
                   "max_cnf_clauses": max(x["max_cnf_clauses"] for x in r35)},
    }


def run_case(case_index: int, wall_seconds: int = SEED_WALL_SECONDS):
    rule, seed_pair = CASES[case_index]
    started = time.perf_counter()
    deadline = started + wall_seconds
    tested = []
    first_certificate = None
    max_vars = max_clauses = 0
    solver_seconds = 0.0
    for cand in fresh_candidates():
        if time.perf_counter() >= deadline:
            status = "censored"
            break
        rec = check_candidate(rule, seed_pair, cand, deadline)
        tested.append(rec)
        max_vars = max(max_vars, rec["max_cnf_variables"])
        max_clauses = max(max_clauses, rec["max_cnf_clauses"])
        solver_seconds += rec["solver_seconds"]
        if rec["status"] == "pass":
            first_certificate = rec
            status = "phase-splice-certified"
            break
        if rec["status"] == "censored":
            status = "censored"
            break
    else:
        status = "no-phase-splice-through-6"
    return {
        "case_index": case_index,
        "rule": rule,
        "pair": f"{seed_pair[0]}-{seed_pair[1]}",
        "status": status,
        "tested_candidates": len(tested),
        "frozen_family_candidates": sum(1 for _ in fresh_candidates()),
        "first_certificate": first_certificate,
        "max_cnf_variables": max_vars,
        "max_cnf_clauses": max_clauses,
        "solver_seconds": solver_seconds,
        "elapsed_seconds": time.perf_counter() - started,
        "tested": tested,
    }


def provenance():
    return {
        "scripts/recover_phase_splice_sat.py": sha256(Path(__file__)),
        str(PROTOCOL.relative_to(ROOT)): sha256(PROTOCOL),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--controls-only", action="store_true")
    ap.add_argument("--case-index", type=int)
    args = ap.parse_args()
    if args.controls_only == (args.case_index is not None):
        raise SystemExit("choose exactly one of --controls-only or --case-index")
    if args.controls_only:
        out = {"ok": True, "experiment": "phase-splice-sat-recovery-controls", "solver": "Minisat22 via python-sat",
               "encoding": "manual CNF over original fine-ECA shrinking cones", "source_hashes": provenance(), "controls": run_controls()}
    else:
        if not (0 <= args.case_index < len(CASES)):
            raise SystemExit("bad case index")
        out = {"ok": True, "experiment": "phase-splice-sat-recovery-seed", "solver": "Minisat22 via python-sat",
               "encoding": "manual CNF over original fine-ECA shrinking cones", "seed_wall_seconds": SEED_WALL_SECONDS,
               "source_hashes": provenance(), "result": run_case(args.case_index)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2) + "\n")
    if args.controls_only:
        print(json.dumps(out["controls"], indent=2))
    else:
        r = out["result"]
        print(json.dumps({k: r[k] for k in ("case_index", "rule", "pair", "status", "tested_candidates", "max_cnf_variables", "max_cnf_clauses", "elapsed_seconds")}, indent=2))


if __name__ == "__main__":
    main()
