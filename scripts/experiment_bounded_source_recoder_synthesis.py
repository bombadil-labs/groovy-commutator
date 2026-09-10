"""Terminal CEGIS synthesis of bounded adaptive source recoders."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import threading
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
import experiment_two_switch_rail_selector_sat as domain_base  # noqa:E402

PROTOCOL = ROOT / "docs/research/protocols/bounded-source-recoder-synthesis-20260910.md"
DOMAIN_RESULT = ROOT / "results/phase_splice_source_recoder_20260909.json"
DOMAIN_SHA256 = "af00ce04f134bd98ecd2d2bd7a0bf2a00b2c2c5d9b7d34c2ebcd9cc22e329138"

TMAX = 6
MAX_STATES = 4
SEED_WALL_SECONDS = 1200
MAX_CEGIS_COUNTEREXAMPLES = 256
MAX_SYNTH_VARS = 100_000
MAX_SYNTH_CLAUSES = 1_000_000
MAX_VERIFY_VARS = 20_000
MAX_VERIFY_CLAUSES = 200_000

MUX_TABLE = tuple((idx & 1) if ((idx >> 2) & 1) else ((idx >> 1) & 1) for idx in range(8))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_domain():
    if sha256(DOMAIN_RESULT) != DOMAIN_SHA256:
        raise AssertionError("phase-splice domain hash mismatch")
    rows = domain_base.load_domain()
    assert len(rows) == 22
    assert sum(len(r["incoming_target_ids"]) for r in rows) == 170
    return rows


def ordered_deltas(k: int):
    return sorted(range(-k, k + 1), key=lambda d: (abs(d), d))


def structural_candidates():
    for m in range(1, MAX_STATES + 1):
        for t in range(2, TMAX + 1):
            for j in range(1, t):
                k = t - j
                for delta in ordered_deltas(k):
                    yield {"m": m, "t": t, "k": k, "j": j, "delta": delta}


def candidate_positions(cand):
    t, j, delta = cand["t"], cand["j"], cand["delta"]
    outside = [p for p in range(-t, t + 1) if not (delta - j <= p <= delta + j)]
    inside = [p for p in range(-t, t + 1) if delta - j <= p <= delta + j]
    return outside + inside


def exactly_one(builder: CNFBuilder, vs):
    vs = list(vs)
    if not vs:
        raise ValueError("empty exactly_one")
    builder.clauses.append(vs)
    for i in range(len(vs)):
        for j in range(i + 1, len(vs)):
            builder.clauses.append([-vs[i], -vs[j]])


def fixed_var(builder: CNFBuilder, value: int):
    v = builder.var()
    builder.unit(v, int(value))
    return v


def equal_literal(builder: CNFBuilder, out: int, var: int, negated: bool = False):
    if not negated:
        builder.equal(out, var)
    else:
        builder.clauses.append([out, var])
        builder.clauses.append([-out, -var])


def table_variables(builder: CNFBuilder, m: int):
    choice = [[builder.var() for _ in range(64)] for _ in range(m)]
    nxt = [[[builder.var() for _ in range(m)] for _ in range(64)] for _ in range(m)]
    for s in range(m):
        for code in range(64):
            exactly_one(builder, nxt[s][code])
    return choice, nxt


def symbolic_machine_step_concrete(builder, state, code, choice_table, next_table):
    m = len(state)
    ch = builder.var()
    ns = [builder.var() for _ in range(m)]
    exactly_one(builder, ns)
    for s in range(m):
        cs = choice_table[s][code]
        builder.clauses.append([-state[s], -cs, ch])
        builder.clauses.append([-state[s], cs, -ch])
        for q in range(m):
            tv = next_table[s][code][q]
            builder.clauses.append([-state[s], -tv, ns[q]])
            builder.clauses.append([-state[s], tv, -ns[q]])
    return ch, ns


def symbolic_machine_step_symbolic(builder, state, left_bits, right_bits, machine):
    m = len(state)
    ch = builder.var()
    ns = [builder.var() for _ in range(m)]
    exactly_one(builder, ns)
    inputs = list(left_bits) + list(right_bits)
    for s in range(m):
        for code in range(64):
            pattern = bit_pattern(code & 7) + bit_pattern((code >> 3) & 7)
            neg_condition = [-state[s]]
            for v, bit in zip(inputs, pattern):
                neg_condition.append(-v if bit else v)
            cval = bool(machine["choice"][s][code])
            builder.clauses.append(neg_condition + ([ch] if cval else [-ch]))
            qnext = int(machine["next"][s][code])
            for q in range(m):
                builder.clauses.append(neg_condition + ([ns[q]] if q == qnext else [-ns[q]]))
    return ch, ns


def selected_concrete_symbol_bits(builder, ch: int, left_symbol: int, right_symbol: int):
    lb, rb = bit_pattern(left_symbol), bit_pattern(right_symbol)
    out = []
    for l, r in zip(lb, rb):
        if l == r:
            out.append(fixed_var(builder, l))
        else:
            v = builder.var()
            if l == 0 and r == 1:
                equal_literal(builder, v, ch, False)
            else:
                equal_literal(builder, v, ch, True)
            out.append(v)
    return out


def selected_symbolic_bits(builder, ch: int, left_bits, right_bits):
    out = []
    for l, r in zip(left_bits, right_bits):
        v = builder.var()
        builder.truth_gate((ch, l, r), v, MUX_TABLE)
        out.append(v)
    return out


def concrete_rows_from_example(rule: int, seed_pair, example, k: int):
    a, b = seed_pair
    coords = example["coords"]
    bg = example["background"]
    left = [a if q == 0 else int(bg[str(q)]) for q in coords]
    right = [b if q == 0 else int(bg[str(q)]) for q in coords]
    zlb = fine_evolve(macro_to_bits(left), rule, 3 * k)
    zrb = fine_evolve(macro_to_bits(right), rule, 3 * k)
    return left, right, bits_to_macro(zlb), bits_to_macro(zrb)


def concrete_actual_output(rule: int, seed_pair, example, t: int, p: int):
    a, b = seed_pair
    coords = example["coords"]
    bg = example["background"]
    left = [a if q == 0 else int(bg[str(q)]) for q in coords]
    right = [b if q == 0 else int(bg[str(q)]) for q in coords]
    lb = bits_to_macro(fine_evolve(macro_to_bits(left), rule, 3 * t))
    rb = bits_to_macro(fine_evolve(macro_to_bits(right), rule, 3 * t))
    lo_out = coords[0] + t
    idx = p - lo_out
    return lb[idx], rb[idx]


def add_example_constraints(builder, rule, seed_pair, cand, example, choice_table, next_table):
    m, t, k, j, delta = (cand[x] for x in ("m", "t", "k", "j", "delta"))
    p = int(example["p"])
    coords = list(map(int, example["coords"]))
    if coords != list(range(coords[0], coords[-1] + 1)):
        raise AssertionError("noncontiguous example")
    _, _, zl_all, zr_all = concrete_rows_from_example(rule, seed_pair, example, k)
    z_lo = coords[0] + k
    actual_l, actual_r = concrete_actual_output(rule, seed_pair, example, t, p)

    state = [builder.var() for _ in range(m)]
    exactly_one(builder, state)
    for s, v in enumerate(state):
        builder.unit(v, s == 0)

    choices = {}
    for q in range(-k, k + 1):
        idx = q - z_lo
        ls, rs = int(zl_all[idx]), int(zr_all[idx])
        code = ls + 8 * rs
        ch, state = symbolic_machine_step_concrete(builder, state, code, choice_table, next_table)
        choices[q] = (ch, ls, rs)

    rec_l, rec_r = [], []
    abit, bbit = bit_pattern(seed_pair[0]), bit_pattern(seed_pair[1])
    for q in range(p - j, p + j + 1):
        if q == delta:
            rec_l.extend(fixed_var(builder, bit) for bit in abit)
            rec_r.extend(fixed_var(builder, bit) for bit in bbit)
        elif -k <= q <= k:
            ch, ls, rs = choices[q]
            bits = selected_concrete_symbol_bits(builder, ch, ls, rs)
            rec_l.extend(bits)
            rec_r.extend(bits)
        else:
            idx = q - z_lo
            sym = int(zl_all[idx])
            bits = [fixed_var(builder, bit) for bit in bit_pattern(sym)]
            rec_l.extend(bits)
            rec_r.extend(bits)

    table = rule_table(rule)
    out_l = evolve_cnf(builder, rec_l, table, 3 * j)
    out_r = evolve_cnf(builder, rec_r, table, 3 * j)
    for v, bit in zip(out_l, bit_pattern(actual_l)):
        builder.unit(v, bit)
    for v, bit in zip(out_r, bit_pattern(actual_r)):
        builder.unit(v, bit)


def solve_builder(builder: CNFBuilder, deadline=None):
    if deadline is not None and time.perf_counter() >= deadline:
        return None, None, 0.0
    remaining = None if deadline is None else max(0.0, deadline - time.perf_counter())
    started = time.perf_counter()
    with Minisat22(bootstrap_with=builder.clauses) as solver:
        timer = None
        if remaining is not None:
            timer = threading.Timer(remaining, solver.interrupt)
            timer.daemon = True
            timer.start()
        try:
            status = solver.solve() if remaining is None else solver.solve_limited(expect_interrupt=True)
        finally:
            if timer is not None:
                timer.cancel()
        seconds = time.perf_counter() - started
        if status is None:
            return None, None, seconds
        model = solver.get_model() if status else None
        return bool(status), model, seconds


def synthesize_machine(rule, seed_pair, cand, examples, deadline=None):
    builder = CNFBuilder()
    choice, nxt = table_variables(builder, cand["m"])
    for ex in examples:
        add_example_constraints(builder, rule, seed_pair, cand, ex, choice, nxt)
        if builder.variables > MAX_SYNTH_VARS or len(builder.clauses) > MAX_SYNTH_CLAUSES:
            return {"status": "censored", "reason": "synthesis-cnf-ceiling",
                    "variables": builder.variables, "clauses": len(builder.clauses)}
    sat, model, seconds = solve_builder(builder, deadline)
    meta = {"variables": builder.variables, "clauses": len(builder.clauses), "solver_seconds": seconds}
    if sat is None:
        return {"status": "censored", "reason": "seed-wall-time-during-synthesis", **meta}
    if not sat:
        return {"status": "unsat", **meta}
    positive = {x for x in model if x > 0}
    machine = {"m": cand["m"], "choice": [], "next": []}
    for s in range(cand["m"]):
        machine["choice"].append([1 if choice[s][code] in positive else 0 for code in range(64)])
        row = []
        for code in range(64):
            q = next((q for q, v in enumerate(nxt[s][code]) if v in positive), None)
            if q is None:
                raise AssertionError("missing synthesized transition")
            row.append(q)
        machine["next"].append(row)
    return {"status": "sat", "machine": machine, **meta}


def verifier_interval(cand, p: int):
    t, k = cand["t"], cand["k"]
    return min(-2 * k, p - t), max(2 * k, p + t)


def build_verify_query(rule, seed_pair, cand, machine, p: int):
    m, t, k, j, delta = (cand[x] for x in ("m", "t", "k", "j", "delta"))
    lo, hi = verifier_interval(cand, p)
    coords = list(range(lo, hi + 1))
    builder = CNFBuilder()
    fine_len = 3 * len(coords)
    left0 = [builder.var() for _ in range(fine_len)]
    right0 = [builder.var() for _ in range(fine_len)]
    abit, bbit = bit_pattern(seed_pair[0]), bit_pattern(seed_pair[1])
    for block, q in enumerate(coords):
        for bit in range(3):
            idx = 3 * block + bit
            if q == 0:
                builder.unit(left0[idx], abit[bit])
                builder.unit(right0[idx], bbit[bit])
            else:
                builder.equal(left0[idx], right0[idx])

    table = rule_table(rule)
    z_left = evolve_cnf(builder, left0, table, 3 * k)
    z_right = evolve_cnf(builder, right0, table, 3 * k)
    z_lo = lo + k
    actual_left_all = evolve_cnf(builder, z_left, table, 3 * j)
    actual_right_all = evolve_cnf(builder, z_right, table, 3 * j)
    actual_lo = lo + t
    aidx = 3 * (p - actual_lo)
    actual_l = actual_left_all[aidx:aidx + 3]
    actual_r = actual_right_all[aidx:aidx + 3]
    assert len(actual_l) == len(actual_r) == 3

    state = [builder.var() for _ in range(m)]
    exactly_one(builder, state)
    for s, v in enumerate(state):
        builder.unit(v, s == 0)

    choices = {}
    for q in range(-k, k + 1):
        idx = 3 * (q - z_lo)
        lb = z_left[idx:idx + 3]
        rb = z_right[idx:idx + 3]
        ch, state = symbolic_machine_step_symbolic(builder, state, lb, rb, machine)
        choices[q] = (ch, lb, rb)

    rec_l, rec_r = [], []
    for q in range(p - j, p + j + 1):
        if q == delta:
            rec_l.extend(fixed_var(builder, bit) for bit in abit)
            rec_r.extend(fixed_var(builder, bit) for bit in bbit)
        elif -k <= q <= k:
            ch, lb, rb = choices[q]
            bits = selected_symbolic_bits(builder, ch, lb, rb)
            rec_l.extend(bits)
            rec_r.extend(bits)
        else:
            idx = 3 * (q - z_lo)
            bits = z_left[idx:idx + 3]
            rec_l.extend(bits)
            rec_r.extend(bits)

    out_l = evolve_cnf(builder, rec_l, table, 3 * j)
    out_r = evolve_cnf(builder, rec_r, table, 3 * j)
    mismatch = []
    for x, y in zip(actual_l + actual_r, out_l + out_r):
        d = builder.var()
        builder.xor_gate(x, y, d)
        mismatch.append(d)
    builder.clauses.append(mismatch)
    return builder, left0, coords


def replay_machine(rule, seed_pair, cand, machine, p: int, coords, bg):
    a, b = seed_pair
    left = [a if q == 0 else bg[q] for q in coords]
    right = [b if q == 0 else bg[q] for q in coords]
    t, k, j, delta = (cand[x] for x in ("t", "k", "j", "delta"))
    zlb = fine_evolve(macro_to_bits(left), rule, 3 * k)
    zrb = fine_evolve(macro_to_bits(right), rule, 3 * k)
    zl, zr = bits_to_macro(zlb), bits_to_macro(zrb)
    z_lo = coords[0] + k

    st = 0
    selected = {}
    for q in range(-k, k + 1):
        idx = q - z_lo
        ls, rs = zl[idx], zr[idx]
        code = ls + 8 * rs
        selected[q] = rs if machine["choice"][st][code] else ls
        st = machine["next"][st][code]

    rec_l, rec_r = [], []
    for q in range(p - j, p + j + 1):
        if q == delta:
            rec_l.append(a)
            rec_r.append(b)
        elif -k <= q <= k:
            rec_l.append(selected[q])
            rec_r.append(selected[q])
        else:
            idx = q - z_lo
            rec_l.append(zl[idx])
            rec_r.append(zl[idx])

    actual_lb = bits_to_macro(fine_evolve(macro_to_bits(left), rule, 3 * t))
    actual_rb = bits_to_macro(fine_evolve(macro_to_bits(right), rule, 3 * t))
    actual_lo = coords[0] + t
    actual_l = actual_lb[p - actual_lo]
    actual_r = actual_rb[p - actual_lo]
    out_l = bits_to_macro(fine_evolve(macro_to_bits(rec_l), rule, 3 * j))[0]
    out_r = bits_to_macro(fine_evolve(macro_to_bits(rec_r), rule, 3 * j))[0]
    if actual_l == out_l and actual_r == out_r:
        raise AssertionError("SAT verifier model did not replay")
    return {
        "p": p,
        "coords": coords,
        "background": {str(q): int(bg[q]) for q in coords if q != 0},
        "actual_outputs": [actual_l, actual_r],
        "recoded_outputs": [out_l, out_r],
        "replay_pass": True,
    }


def verify_machine(rule, seed_pair, cand, machine, deadline=None):
    max_vars = max_clauses = 0
    solver_seconds = 0.0
    for p in candidate_positions(cand):
        builder, left0, coords = build_verify_query(rule, seed_pair, cand, machine, p)
        max_vars = max(max_vars, builder.variables)
        max_clauses = max(max_clauses, len(builder.clauses))
        if builder.variables > MAX_VERIFY_VARS or len(builder.clauses) > MAX_VERIFY_CLAUSES:
            return {"status": "censored", "reason": "verification-cnf-ceiling",
                    "max_variables": max_vars, "max_clauses": max_clauses,
                    "solver_seconds": solver_seconds}
        sat, model, seconds = solve_builder(builder, deadline)
        solver_seconds += seconds
        if sat is None:
            return {"status": "censored", "reason": "seed-wall-time-during-verification",
                    "max_variables": max_vars, "max_clauses": max_clauses,
                    "solver_seconds": solver_seconds}
        if sat:
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
            ex = replay_machine(rule, seed_pair, cand, machine, p, coords, bg)
            return {"status": "counterexample", "counterexample": ex,
                    "max_variables": max_vars, "max_clauses": max_clauses,
                    "solver_seconds": solver_seconds}
    return {"status": "verified", "max_variables": max_vars, "max_clauses": max_clauses,
            "solver_seconds": solver_seconds}


def cegis_structure(rule, seed_pair, cand, deadline=None):
    examples = []
    synth_seconds = verify_seconds = 0.0
    max_sv = max_sc = max_vv = max_vc = 0
    first_cex = last_cex = None
    for iteration in range(MAX_CEGIS_COUNTEREXAMPLES + 1):
        if deadline is not None and time.perf_counter() >= deadline:
            return {"status": "censored", "reason": "seed-wall-time", "iterations": iteration,
                    "counterexamples": len(examples)}
        syn = synthesize_machine(rule, seed_pair, cand, examples, deadline)
        synth_seconds += syn.get("solver_seconds", 0.0)
        max_sv = max(max_sv, syn.get("variables", 0))
        max_sc = max(max_sc, syn.get("clauses", 0))
        if syn["status"] == "censored":
            return {"status": "censored", "reason": syn["reason"], "iterations": iteration,
                    "counterexamples": len(examples), "max_synthesis_variables": max_sv,
                    "max_synthesis_clauses": max_sc, "synthesis_seconds": synth_seconds,
                    "verification_seconds": verify_seconds}
        if syn["status"] == "unsat":
            return {"status": "exact-negative", "iterations": iteration,
                    "counterexamples": len(examples), "max_synthesis_variables": max_sv,
                    "max_synthesis_clauses": max_sc, "synthesis_seconds": synth_seconds,
                    "verification_seconds": verify_seconds,
                    "first_counterexample": first_cex, "last_counterexample": last_cex}
        machine = syn["machine"]
        ver = verify_machine(rule, seed_pair, cand, machine, deadline)
        verify_seconds += ver.get("solver_seconds", 0.0)
        max_vv = max(max_vv, ver.get("max_variables", 0))
        max_vc = max(max_vc, ver.get("max_clauses", 0))
        if ver["status"] == "censored":
            return {"status": "censored", "reason": ver["reason"], "iterations": iteration + 1,
                    "counterexamples": len(examples), "max_synthesis_variables": max_sv,
                    "max_synthesis_clauses": max_sc, "max_verification_variables": max_vv,
                    "max_verification_clauses": max_vc, "synthesis_seconds": synth_seconds,
                    "verification_seconds": verify_seconds}
        if ver["status"] == "verified":
            return {"status": "certificate", "iterations": iteration + 1,
                    "counterexamples": len(examples), "machine": machine,
                    "max_synthesis_variables": max_sv, "max_synthesis_clauses": max_sc,
                    "max_verification_variables": max_vv, "max_verification_clauses": max_vc,
                    "synthesis_seconds": synth_seconds, "verification_seconds": verify_seconds}
        ex = ver["counterexample"]
        if first_cex is None:
            first_cex = ex
        last_cex = ex
        examples.append(ex)
        if len(examples) >= MAX_CEGIS_COUNTEREXAMPLES:
            return {"status": "censored", "reason": "cegis-counterexample-ceiling",
                    "iterations": iteration + 1, "counterexamples": len(examples),
                    "max_synthesis_variables": max_sv, "max_synthesis_clauses": max_sc,
                    "max_verification_variables": max_vv, "max_verification_clauses": max_vc,
                    "synthesis_seconds": synth_seconds, "verification_seconds": verify_seconds,
                    "first_counterexample": first_cex, "last_counterexample": last_cex}
    raise AssertionError("unreachable CEGIS loop")


def compact_structure(cand, rec):
    out = {**cand, "status": rec["status"], "iterations": rec.get("iterations"),
           "counterexamples": rec.get("counterexamples"),
           "synthesis_seconds": rec.get("synthesis_seconds", 0.0),
           "verification_seconds": rec.get("verification_seconds", 0.0)}
    for k in ("reason", "max_synthesis_variables", "max_synthesis_clauses",
              "max_verification_variables", "max_verification_clauses"):
        if k in rec:
            out[k] = rec[k]
    return out


def run_seed(seed_index: int, wall_seconds: int = SEED_WALL_SECONDS):
    row = load_domain()[seed_index]
    a, b = map(int, row["pair"].split("-"))
    started = time.perf_counter()
    deadline = started + wall_seconds
    structures = []
    first_certificate = None
    censored_structures = 0
    exact_negative_structures = 0
    max_state_completed = 0
    for cand in structural_candidates():
        if time.perf_counter() >= deadline:
            return {**row, "seed_index": seed_index, "status": "censored",
                    "censoring_reason": "seed-wall-time", "first_certificate": first_certificate,
                    "structures_attempted": len(structures), "exact_negative_structures": exact_negative_structures,
                    "censored_structures": censored_structures, "max_state_completed": max_state_completed,
                    "elapsed_seconds": time.perf_counter() - started, "structures": structures}
        rec = cegis_structure(row["rule"], (a, b), cand, deadline)
        structures.append(compact_structure(cand, rec))
        if rec["status"] == "certificate":
            first_certificate = {**cand, "machine": rec["machine"], "iterations": rec["iterations"],
                                 "counterexamples": rec["counterexamples"]}
            return {**row, "seed_index": seed_index, "status": "bounded-recoder-certified",
                    "first_certificate": first_certificate, "structures_attempted": len(structures),
                    "exact_negative_structures": exact_negative_structures,
                    "censored_structures": censored_structures,
                    "max_state_completed": max(max_state_completed, cand["m"]),
                    "elapsed_seconds": time.perf_counter() - started, "structures": structures}
        if rec["status"] == "exact-negative":
            exact_negative_structures += 1
        else:
            censored_structures += 1
            if rec.get("reason", "").startswith("seed-wall-time"):
                return {**row, "seed_index": seed_index, "status": "censored",
                        "censoring_reason": rec["reason"], "first_certificate": None,
                        "structures_attempted": len(structures),
                        "exact_negative_structures": exact_negative_structures,
                        "censored_structures": censored_structures,
                        "max_state_completed": max_state_completed,
                        "elapsed_seconds": time.perf_counter() - started, "structures": structures}
        if cand["t"] == TMAX and cand["j"] == TMAX - 1 and cand["delta"] == 1:
            max_state_completed = cand["m"]
    status = "no-bounded-recoder-through-4" if censored_structures == 0 else "censored"
    return {**row, "seed_index": seed_index, "status": status,
            "first_certificate": None, "structures_attempted": len(structures),
            "exact_negative_structures": exact_negative_structures,
            "censored_structures": censored_structures, "max_state_completed": max_state_completed,
            "elapsed_seconds": time.perf_counter() - started, "structures": structures}


def run_controls():
    pos = {"m": 1, "t": 3, "k": 2, "j": 1, "delta": 0}
    pr = cegis_structure(5, (0, 2), pos, deadline=time.perf_counter() + 120)
    if pr["status"] != "certificate":
        raise AssertionError(("Rule5 synthesis positive control failed", pr))
    negatives = []
    for m in (1, 2):
        for j in (1, 2):
            k = 3 - j
            for delta in ordered_deltas(k):
                cand = {"m": m, "t": 3, "k": k, "j": j, "delta": delta}
                rec = cegis_structure(35, (2, 6), cand, deadline=time.perf_counter() + 120)
                if rec["status"] != "exact-negative":
                    raise AssertionError(("Rule35 synthesis negative control failed", cand, rec))
                negatives.append({**cand, "iterations": rec["iterations"], "counterexamples": rec["counterexamples"]})
    assert len(negatives) == 16
    return {"ok": True,
            "rule5": {"status": "pass", "candidate": pos, "iterations": pr["iterations"],
                      "machine": pr["machine"]},
            "rule35": {"status": "pass", "exact_negative_structures": len(negatives),
                       "max_iterations": max(x["iterations"] for x in negatives)}}


def provenance():
    return {
        "scripts/experiment_bounded_source_recoder_synthesis.py": sha256(Path(__file__)),
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
        out = {"ok": True, "experiment": "bounded-source-recoder-synthesis-controls",
               "working_identity": "bounded-source-recoder-synthesis",
               "source_hashes": provenance(), "controls": run_controls()}
    else:
        if not (0 <= args.seed_index < 22):
            raise SystemExit("bad seed index")
        out = {"ok": True, "experiment": "bounded-source-recoder-synthesis-seed",
               "working_identity": "bounded-source-recoder-synthesis",
               "seed_wall_seconds": SEED_WALL_SECONDS,
               "max_states": MAX_STATES, "source_hashes": provenance(),
               "result": run_seed(args.seed_index)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, separators=(",", ":")) + "\n")
    if args.controls_only:
        print(json.dumps(out["controls"], indent=2))
    else:
        r = out["result"]
        print(json.dumps({k: r.get(k) for k in (
            "seed_index", "rule", "pair", "status", "structures_attempted",
            "exact_negative_structures", "censored_structures", "max_state_completed",
            "elapsed_seconds")}, indent=2))


if __name__ == "__main__":
    main()
