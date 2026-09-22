#!/usr/bin/env python3
"""Extract and check three existing certificates; no historical census.

Run with --write to save the deterministic report, or --check [FILE] to
recompute and compare it. The original result files are never modified.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from groovy.ca import apply_rule
from verify_depth_one_certificate import depth_one_graph

OUT = ROOT / "results/representation_case_studies_20260921.json"
INPUTS = [
    "scripts/verify_representation_case_studies.py",
    "scripts/verify_depth_one_certificate.py",
    "src/groovy/ca.py",
    "results/ring_closure_certificate_20260911.json",
    "results/depth_one_certificate_20260911.json",
    "results/full_shift_depth_two_20260911.json",
]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def bits(word):
    require(bool(word) and set(word) <= {"0", "1"}, "invalid binary word")
    return np.array(list(map(int, word)), dtype=np.uint8)


def word(state):
    return "".join(map(str, state.tolist()))


def local(rule, state):
    """Interior only: no periodic boundary is silently introduced."""
    return np.array([(rule >> (4 * int(a) + 2 * int(b) + int(c))) & 1
                     for a, b, c in zip(state, state[1:], state[2:])], dtype=np.uint8)


def case_a():
    for row in itertools.product((0, 1), repeat=7):
        x = np.array(row, dtype=np.uint8)
        fx = apply_rule(x, 255)
        dx = x ^ fx
        dfx = fx ^ apply_rule(fx, 255)
        edx = apply_rule(dx, 255)
        require(np.array_equal(dx, 1 ^ x), "A: derivative is not complementation")
        require(not dfx.any() and edx.all(), "A: incorrect commutator")
    return {"rule": 255, "observation": "D = I XOR E", "ring_check": 7,
            "states_checked": 128, "effective_law": "constant zero",
            "general_certificate": "E(x)=1; D(x)=1 XOR x; DE(x)=0; ED(x)=1"}


def case_b():
    source = json.loads((ROOT / INPUTS[3]).read_text())
    for n in range(3, 8):
        require((223 in source["exhaustive_closed"]["22"][str(n)]) == (n < 7),
                "B: historical closure table changed")
    seen = {}
    witness = None
    for row in itertools.product((0, 1), repeat=7):
        x = np.array(row, dtype=np.uint8)
        present = word(apply_rule(x, 22))
        following = word(apply_rule(apply_rule(x, 223), 22))
        if present in seen and seen[present][1] != following and witness is None:
            y, previous_output = seen[present]
            witness = {"x": y, "y": word(x), "equal_present": present,
                       "next_x": previous_output, "next_y": following}
        seen.setdefault(present, (word(x), following))
    require(witness is not None, "B: no ring-7 obstruction")
    return {"rule": 223, "observation": 22, "ring": 7,
            "states_checked": 128, "witness": witness}


def pair_code(x, y):
    code = 0
    for a, b in zip(x, y):
        code = 4 * code + 2 * int(a) + int(b)
    return code


def multiply(rows, adjacency):
    result = []
    for row in rows:
        out = 0
        while row:
            low = row & -row
            out |= adjacency[low.bit_length() - 1]
            row -= low
        result.append(out)
    return result


def case_c():
    d1 = json.loads((ROOT / INPUTS[4]).read_text())
    d2 = json.loads((ROOT / INPUTS[5]).read_text())
    k, p = d1["predictions"]["L3_certificates"]["232"]["k_p_by_rule"]["58"]
    require((k, p) == (11, 12), "C: unexpected power certificate")
    A, violations = depth_one_graph(232, 58)
    adjacency = [sum(1 << int(j) for j in np.flatnonzero(row)) for row in A]
    powers = [[1 << i for i in range(256)]]
    for _ in range(k + p):
        powers.append(multiply(powers[-1], adjacency))
    require(powers[k] == powers[k + p], "C: Boolean power equality fails")
    require(all(not ((M[v3] >> v0) & 1)
                for M in powers[1:k + p] for v0, v3 in violations),
            "C: a violating walk closes on a ring")
    # The graph criterion is stated for n >= 4. Check all smaller rings directly.
    for n in (1, 2, 3):
        observed = {}
        for row in itertools.product((0, 1), repeat=n):
            x = np.array(row, dtype=np.uint8)
            fx = apply_rule(x, 58)
            key = (word(apply_rule(x, 232)), word(apply_rule(fx, 232)))
            out = word(apply_rule(apply_rule(fx, 58), 232))
            require(key not in observed or observed[key] == out,
                    "C: depth-one closure fails on a small ring")
            observed[key] = out
    saved = next(w for w in d2["predictions"]["M6_witness_pairs"]["pairs"]
                 if (w["psi"], w["rule"]) == (232, 58))
    require(saved["left_path_word"] == {"x": "", "y": ""}, "unexpected left bridge")
    extended = {}
    for side in ("x", "y"):
        left, right = saved["left_cycle_word"][side], saved["right_cycle_word"][side]
        require(len(left) == saved["left_period"] == 4, "bad left period")
        require(len(right) == saved["right_period"] == 3, "bad right period")
        reconstructed = left * 3 + saved["violating_block"][side] + saved["right_path_word"][side] + right * 3
        require(reconstructed == saved["window"][side], "C: malformed bridge/window")
        require(len(reconstructed) == saved["window_length"] == 30, "bad window length")
        # Two extra periods cover every phase of each tail and every five-cell seam.
        extended[side] = bits(left * 2 + reconstructed + right * 2)
    x, y = extended["x"], extended["y"]
    for start in range(len(x) - 4):
        u = pair_code(x[start:start + 4], y[start:start + 4])
        v = pair_code(x[start + 1:start + 5], y[start + 1:start + 5])
        require(A[u, v] == 1, "C: tail/bridge edge violates observed agreement")
    bx, by = (bits(saved["violating_block"][side]) for side in ("x", "y"))
    require(pair_code(bx[:4], by[:4]) == saved["v0"] == 15, "wrong initial vertex")
    require(pair_code(bx[3:], by[3:]) == saved["v3"] == 246, "wrong final vertex")
    out_x = int(local(232, local(58, local(58, bx)))[0])
    out_y = int(local(232, local(58, local(58, by)))[0])
    require(out_x != out_y, "C: alleged infinite-line obstruction does not violate")
    require(saved["centre"] == 15 and saved["trimmed_margin"] == 3, "wrong witness coordinates")
    for side in ("x", "y"):
        require(saved["window"][side][12:19] == saved["violating_block"][side], "wrong centre")
    return {"rule": 58, "observation": 232,
            "all_ring_certificate": {"vertices": 256, "violating_walks": len(violations),
                                     "power_equality": [k, k + p], "period": p,
                                     "small_rings_checked": [1, 2, 3]},
            "full_line_witness": saved,
            "central_second_observations": [out_x, out_y],
            "tail_certificate": "every five-cell edge in both periodic tails and their bridge is in A"}


def report():
    return {"schema": 1, "kind": "existing-certificate extraction",
            "source_hashes": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in INPUTS},
            "cases": {"A": case_a(), "B": case_b(), "C": case_c()}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", nargs="?", const=str(OUT), metavar="FILE")
    args = parser.parse_args()
    result = report()
    if args.check:
        require(json.loads(Path(args.check).read_text()) == result, "certificate differs from exact replay")
    elif args.write:
        OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"verified": list(result["cases"]), "B": result["cases"]["B"]["witness"],
                      "C_outputs": result["cases"]["C"]["central_second_observations"]}))


if __name__ == "__main__":
    main()
