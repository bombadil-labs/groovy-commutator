"""Research031: exact local causal-witness horizons for block-3 ECA targets.

For ECA radius 1 with block size/cadence 3, three fine ticks induce an exact
radius-1 CA on the eight-symbol 3-cell block alphabet. This instrument checks
local symbol distinguishability in wrap-free causal cones through macro-horizon
3, and compares those local quotients with the corresponding 4-macroblock
periodic-ring quotients used in Research030.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from groovy.ca import rule_lut  # noqa:E402
from experiment_history_lift_closure import FULL_CLASS, state_map  # noqa:E402
from experiment_contextual_quotient import TARGETS, pkey  # noqa:E402

A = 8
BLOCK = 3
CADENCE = 3
HMAX = 3
PAIR_A = np.asarray([a for a in range(A) for b in range(a + 1, A)], dtype=np.intp)
PAIR_B = np.asarray([b for a in range(A) for b in range(a + 1, A)], dtype=np.intp)
PAIR_INDEX = {(int(a), int(b)): i for i, (a, b) in enumerate(zip(PAIR_A, PAIR_B))}
TARGET_ARRAY = np.asarray(TARGETS, dtype=np.uint8)
PROTOCOL = "docs/research/protocols/causal-witness-horizon-20260909.md"


def canonicalize(labels):
    remap = {}
    out = []
    for x in labels:
        x = int(x)
        if x not in remap:
            remap[x] = len(remap)
        out.append(remap[x])
    return tuple(out)


def macro_rule(rule: int) -> np.ndarray:
    """Exact 8^3 -> 8 block rule for three fine ECA ticks."""
    lut = rule_lut(rule)
    vals = np.arange(A, dtype=np.uint16)
    left, center, right = np.meshgrid(vals, vals, vals, indexing="ij")
    fine_state = (left + (center << BLOCK) + (right << (2 * BLOCK))).reshape(-1)
    bits = ((fine_state[:, None] >> np.arange(9, dtype=np.uint16)) & 1).astype(np.uint8)
    for _ in range(CADENCE):
        bits = lut[4 * np.roll(bits, 1, axis=1) + 2 * bits + np.roll(bits, -1, axis=1)]
    weights = 1 << np.arange(BLOCK, dtype=np.uint16)
    return (bits[:, 3:6].astype(np.uint16) * weights).sum(1).astype(np.uint8)


def macro_step(digits: np.ndarray, g: np.ndarray, periodic: bool) -> np.ndarray:
    if periodic:
        left = np.roll(digits, 1, axis=1)
        right = np.roll(digits, -1, axis=1)
        idx = left.astype(np.uint16) * 64 + digits.astype(np.uint16) * 8 + right.astype(np.uint16)
        return g[idx]
    idx = (
        digits[:, :-2].astype(np.uint16) * 64
        + digits[:, 1:-1].astype(np.uint16) * 8
        + digits[:, 2:].astype(np.uint16)
    )
    return g[idx]


def verify_macro_rule(rule: int, g: np.ndarray) -> None:
    """Exact n=12 control: one macro step equals three fine ECA steps."""
    macro_states = np.arange(A**4, dtype=np.uint16)
    digits = ((macro_states[:, None] >> (BLOCK * np.arange(4, dtype=np.uint16))) & 7).astype(np.uint8)
    macro_out = macro_step(digits, g, periodic=True)
    weights = np.asarray([1 << (BLOCK * j) for j in range(4)], dtype=np.uint16)
    macro_encoded = (macro_out.astype(np.uint16) * weights).sum(1).astype(np.uint16)
    fine = state_map(rule, 12)
    fine3 = fine[fine[fine[np.arange(2**12, dtype=np.uint32)]]]
    if not np.array_equal(macro_encoded, fine3[macro_states].astype(np.uint16)):
        raise AssertionError((rule, "macro-rule mismatch"))


def target_difference_masks():
    """For each ordered output-symbol pair, bitset targets that distinguish it."""
    lo = np.zeros(A * A, dtype=np.uint64)
    hi = np.zeros(A * A, dtype=np.uint64)
    for u in range(A):
        for v in range(A):
            code = u * A + v
            ids = np.nonzero(TARGET_ARRAY[:, u] != TARGET_ARRAY[:, v])[0]
            for tid in ids:
                if tid < 64:
                    lo[code] |= np.uint64(1) << np.uint64(tid)
                else:
                    hi[code] |= np.uint64(1) << np.uint64(tid - 64)
    return lo, hi


DIFF_LO, DIFF_HI = target_difference_masks()


def time_output_tensor(g: np.ndarray, t: int) -> np.ndarray:
    """Center macro-symbol after t steps for every (2t+1)-symbol input word."""
    length = 2 * t + 1
    states = np.arange(A**length, dtype=np.uint32)
    digits = ((states[:, None] >> (BLOCK * np.arange(length, dtype=np.uint32))) & 7).astype(np.uint8)
    work = digits
    for _ in range(t):
        work = macro_step(work, g, periodic=False)
    return work[:, 0].reshape((A,) * length, order="F")


def split_masks_at_time(g: np.ndarray, t: int, chunk: int = 32768):
    """Targets that distinguish each input pair exactly at macro-time t."""
    f = time_output_tensor(g, t)
    lo = np.zeros(len(PAIR_A), dtype=np.uint64)
    hi = np.zeros(len(PAIR_A), dtype=np.uint64)
    for axis in range(2 * t + 1):
        outputs = np.moveaxis(f, axis, 0).reshape(A, -1)
        for start in range(0, outputs.shape[1], chunk):
            o = outputs[:, start : start + chunk]
            codes = o[PAIR_A].astype(np.uint16) * A + o[PAIR_B]
            lo |= np.bitwise_or.reduce(DIFF_LO[codes], axis=1)
            hi |= np.bitwise_or.reduce(DIFF_HI[codes], axis=1)
    return lo, hi


def bit_is_set(lo: np.uint64, hi: np.uint64, tid: int) -> bool:
    if tid < 64:
        return bool((int(lo) >> tid) & 1)
    return bool((int(hi) >> (tid - 64)) & 1)


def target_quotient(tid: int, split_lo: np.ndarray, split_hi: np.ndarray):
    eq = np.eye(A, dtype=bool)
    for p, (a, b) in enumerate(zip(PAIR_A, PAIR_B)):
        merged = not bit_is_set(split_lo[p], split_hi[p], tid)
        eq[a, b] = eq[b, a] = merged
    for a in range(A):
        for b in range(A):
            if not eq[a, b]:
                continue
            for c in range(A):
                if eq[b, c] and not eq[a, c]:
                    raise AssertionError((tid, "nontransitive local relation", a, b, c))
    labels = [-1] * A
    nxt = 0
    for a in range(A):
        if labels[a] >= 0:
            continue
        for b in range(A):
            if eq[a, b]:
                labels[b] = nxt
        nxt += 1
    return canonicalize(labels)


def ring_quotients(g: np.ndarray, target: tuple[int, ...], hmax: int = HMAX):
    states = np.arange(A**4, dtype=np.uint16)
    digits = ((states[:, None] >> (BLOCK * np.arange(4, dtype=np.uint16))) & 7).astype(np.uint8)
    target_lut = np.asarray(target, dtype=np.uint8)
    word = np.zeros(len(states), dtype=np.uint32)
    current = digits.copy()
    out = []
    for h in range(hmax + 1):
        y = target_lut[current]
        ycode = (y.astype(np.uint16) * (1 << np.arange(4, dtype=np.uint16))).sum(1).astype(np.uint32)
        word |= ycode << (4 * h)
        tensor = word.reshape((A,) * 4, order="F")
        sigmap = {}
        q = []
        for a in range(A):
            sig = tuple(np.take(tensor, a, axis=j).tobytes() for j in range(4))
            if sig not in sigmap:
                sigmap[sig] = len(sigmap)
            q.append(sigmap[sig])
        out.append(canonicalize(q))
        if h < hmax:
            current = macro_step(current, g, periodic=True)
    return out


def pair_births_for_target(tid: int, cumulative):
    births = {}
    target = TARGETS[tid]
    for a in range(A):
        for b in range(a + 1, A):
            if target[a] != target[b]:
                births[f"{a}-{b}"] = 0
                continue
            p = PAIR_INDEX[(a, b)]
            birth = None
            for h, (lo, hi) in enumerate(cumulative[1:], start=1):
                if bit_is_set(lo[p], hi[p], tid):
                    birth = h
                    break
            births[f"{a}-{b}"] = birth
    return births


def scan_rule(rule: int, hmax: int = HMAX):
    g = macro_rule(rule)
    verify_macro_rule(rule, g)
    cumulative_lo = np.zeros(len(PAIR_A), dtype=np.uint64)
    cumulative_hi = np.zeros(len(PAIR_A), dtype=np.uint64)
    for p, (a, b) in enumerate(zip(PAIR_A, PAIR_B)):
        code = int(a) * A + int(b)
        cumulative_lo[p] = DIFF_LO[code]
        cumulative_hi[p] = DIFF_HI[code]
    cumulative = [(cumulative_lo.copy(), cumulative_hi.copy())]
    for t in range(1, hmax + 1):
        lo, hi = split_masks_at_time(g, t)
        cumulative_lo |= lo
        cumulative_hi |= hi
        cumulative.append((cumulative_lo.copy(), cumulative_hi.copy()))

    rows = []
    h3_new = 0
    local_ring_mismatch = [0] * (hmax + 1)
    for tid, target in enumerate(TARGETS):
        local = [target_quotient(tid, *cumulative[h]) for h in range(hmax + 1)]
        if local[0] != target:
            raise AssertionError((rule, pkey(target), "h0 mismatch", pkey(local[0])))
        ring = ring_quotients(g, target, hmax)
        equal = [local[h] == ring[h] for h in range(hmax + 1)]
        for h, ok in enumerate(equal):
            if not ok:
                local_ring_mismatch[h] += 1
        births = pair_births_for_target(tid, cumulative)
        new3 = sorted(k for k, v in births.items() if v == 3)
        h3_new += len(new3)
        rows.append(
            {
                "target": pkey(target),
                "local_chain": [pkey(q) for q in local],
                "ring_chain": [pkey(q) for q in ring],
                "local_ring_equal": equal,
                "new_h3_pairs": new3,
                "pair_births_through_h3": births,
            }
        )
    return {
        "rule": rule,
        "wclass": FULL_CLASS[rule],
        "macro_rule": g.tolist(),
        "h3_new_pair_target_events": h3_new,
        "local_ring_mismatch_by_horizon": local_ring_mismatch,
        "targets": rows,
    }


def hashes():
    paths = [Path(__file__), ROOT / PROTOCOL]
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rule-start", type=int, default=0)
    ap.add_argument("--rule-end", type=int, default=256)
    ap.add_argument("--hmax", type=int, default=HMAX)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    if args.hmax != HMAX:
        raise SystemExit("frozen primary instrument currently requires hmax=3")
    if not (0 <= args.rule_start < args.rule_end <= 256):
        raise SystemExit("bad rule range")
    rows = [scan_rule(rule, args.hmax) for rule in range(args.rule_start, args.rule_end)]
    summary = {
        "experiment": "causal-witness-horizon",
        "schema": 1,
        "block_size": BLOCK,
        "cadence": CADENCE,
        "local_hmax": HMAX,
        "rule_start": args.rule_start,
        "rule_end": args.rule_end,
        "source_hashes": hashes(),
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2) + "\n")
    print(
        json.dumps(
            {
                "rules": len(rows),
                "h3_new_pair_target_events": sum(r["h3_new_pair_target_events"] for r in rows),
                "rules_with_h3_events": sum(r["h3_new_pair_target_events"] > 0 for r in rows),
                "local_ring_mismatch_h1": sum(r["local_ring_mismatch_by_horizon"][1] for r in rows),
                "local_ring_mismatch_h2": sum(r["local_ring_mismatch_by_horizon"][2] for r in rows),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
