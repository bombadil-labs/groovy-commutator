"""Frozen periodic-size controls for Research031 horizon-3 witnesses."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from groovy.ca import apply_rule_int  # noqa:E402

A = 8
BLOCK = 3
CASES = [
    (35, "00000001", 2, 6),
    (49, "00000001", 2, 3),
    (59, "01111111", 1, 5),
    (115, "01111111", 4, 5),
]
SIZES = (4, 5, 6, 7)


def canonicalize(p):
    remap = {}
    out = []
    for x in p:
        x = int(x)
        if x not in remap:
            remap[x] = len(remap)
        out.append(remap[x])
    return tuple(out)


def macro_rule(rule):
    g = np.empty(512, np.uint8)
    for left in range(8):
        for center in range(8):
            for right in range(8):
                state = left | (center << 3) | (right << 6)
                for _ in range(3):
                    state = apply_rule_int(state, 9, rule)
                g[64 * left + 8 * center + right] = (state >> 3) & 7
    return g


def step(digits, g):
    return g[
        np.roll(digits, 1, axis=1).astype(np.uint16) * 64
        + digits.astype(np.uint16) * 8
        + np.roll(digits, -1, axis=1).astype(np.uint16)
    ]


def quotient(word, m):
    tensor = word.reshape((8,) * m, order="F")
    sigmap = {}
    out = []
    for a in range(8):
        sig = tuple(np.take(tensor, a, axis=j).tobytes() for j in range(m))
        if sig not in sigmap:
            sigmap[sig] = len(sigmap)
        out.append(sigmap[sig])
    return canonicalize(out)


def fine_macro_control(rule, g, m):
    nstates = 8**m
    selected = sorted(set(list(range(min(32, nstates))) + [0, nstates - 1, nstates // 3, nstates // 2, (2 * nstates) // 3]))
    for state in selected:
        digits = [(state >> (3 * j)) & 7 for j in range(m)]
        macro_out = step(np.asarray([digits], dtype=np.uint8), g)[0]
        macro_encoded = sum(int(macro_out[j]) << (3 * j) for j in range(m))
        fine = state
        for _ in range(3):
            fine = apply_rule_int(fine, 3 * m, rule)
        assert macro_encoded == fine, (rule, m, state, macro_encoded, fine)


def scan(rule, key, a, b, m):
    g = macro_rule(rule)
    fine_macro_control(rule, g, m)
    nstates = 8**m
    states = np.arange(nstates, dtype=np.uint32)
    digits = ((states[:, None] >> (3 * np.arange(m, dtype=np.uint32))) & 7).astype(np.uint8)
    target = np.asarray(tuple(map(int, key)), dtype=np.uint8)
    word = np.zeros(nstates, dtype=np.uint32)
    current = digits.copy()
    chain = []
    separation = None
    for h in range(4):
        y = target[current]
        weights = 1 << np.arange(m, dtype=np.uint32)
        ycode = (y.astype(np.uint32) * weights).sum(1)
        word |= ycode << np.uint32(m * h)
        q = quotient(word, m)
        chain.append("".join(map(str, q)))
        if separation is None and q[a] != q[b]:
            separation = h
        if h < 3:
            current = step(current, g)
    return {
        "macroblocks": m,
        "fine_width": 3 * m,
        "quotient_chain": chain,
        "pair_separation_horizon": separation,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    rows = []
    for rule, key, a, b in CASES:
        sizes = [scan(rule, key, a, b, m) for m in SIZES]
        assert sizes[0]["pair_separation_horizon"] is None, (rule, "m4 unexpectedly separates")
        assert sizes[-1]["pair_separation_horizon"] == 3, (rule, "m7 failed h3 prediction")
        rows.append({"rule": rule, "target": key, "pair": f"{a}-{b}", "sizes": sizes})
    out = {"ok": True, "cases": rows}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
