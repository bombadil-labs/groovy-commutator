#!/usr/bin/env python3
"""Exact fresh-width scaling test for asymptotic closure.

Protocol:
  docs/research/protocols/asymptotic-closure-scaling-20261007.md
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

PANEL = [0, 4, 90, 184, 30, 126, 54, 110]
WIDTHS = [16, 18]
BASELINE_H = {54: 5, 110: 4}
OUT = Path("results/asymptotic_closure_scaling_20261007.json")


def rule_lut(rule: int) -> np.ndarray:
    return np.array([(rule >> i) & 1 for i in range(8)], dtype=np.uint8)


def state_map(rule: int, n: int) -> np.ndarray:
    lut = rule_lut(rule)
    ints = np.arange(2**n, dtype=np.uint32)
    s = ((ints[:, None] >> np.arange(n, dtype=np.uint32)) & 1).astype(np.uint8)
    out = lut[4 * np.roll(s, 1, axis=1) + 2 * s + np.roll(s, -1, axis=1)]
    weights = 1 << np.arange(n, dtype=np.uint64)
    return (out.astype(np.uint64) * weights).sum(axis=1).astype(np.uint32)


def block2_parity_map(n: int) -> np.ndarray:
    states = np.arange(2**n, dtype=np.uint32)
    bits = ((states[:, None] >> np.arange(n, dtype=np.uint32)) & 1).astype(np.uint8)
    macro = np.bitwise_xor.reduce(bits.reshape(len(states), n // 2, 2), axis=2)
    weights = 1 << np.arange(n // 2, dtype=np.uint64)
    return (macro.astype(np.uint64) * weights).sum(axis=1).astype(np.uint32)


def compress(values: np.ndarray) -> np.ndarray:
    _, inverse = np.unique(values, return_inverse=True)
    return inverse.astype(np.uint32)


def partition_entropy(labels: np.ndarray) -> float:
    counts = np.bincount(labels.astype(np.int64))
    counts = counts[counts > 0].astype(np.float64)
    p = counts / counts.sum()
    return float(-(p * np.log2(p)).sum())


def profile(rule: int, n: int) -> dict:
    e = state_map(rule, n)
    step = e[e]
    observation = block2_parity_map(n)
    current = np.arange(2**n, dtype=np.uint32)
    labels = compress(observation[current])
    entropies = [partition_entropy(labels)]
    class_count = int(labels.max()) + 1
    repair_bits = []
    hstar = None

    for t in range(n + 8):
        current = step[current]
        target = observation[current]
        pair = (labels.astype(np.uint64) << (n // 2)) | target.astype(np.uint64)
        refined = compress(pair)
        next_count = int(refined.max()) + 1
        h_new = partition_entropy(refined)
        repair_bits.append(h_new - entropies[-1])
        entropies.append(h_new)
        if next_count == class_count:
            hstar = t
            break
        labels = refined
        class_count = next_count

    if hstar is None:
        raise RuntimeError(f"no stabilization rule={rule} n={n}")

    entropies = entropies[: hstar + 1]
    repair_bits = repair_bits[:hstar]
    h0 = entropies[0]
    hinf = entropies[hstar]
    latent = hinf - h0

    if latent <= 1e-12:
        t90 = 0
        a90 = 0.0
    else:
        resolved = [(h - h0) / latent for h in entropies]
        t90 = next(i for i, value in enumerate(resolved)
                   if value + 1e-12 >= 0.90)
        a90 = (hstar - t90) / hstar if hstar else 0.0

    return {
        "rule": rule,
        "n": n,
        "hstar": hstar,
        "Hinf": hinf,
        "reserve_bits": n - hinf,
        "reserve_density": (n - hinf) / n,
        "latent_bits": latent,
        "repair_bits": repair_bits,
        "A90": a90,
    }


def reserve_corridor(rows: dict[int, dict]) -> dict:
    r30 = rows[30]["reserve_bits"]
    r184 = rows[184]["reserve_bits"]
    candidates = {
        str(rule): bool(r30 < rows[rule]["reserve_bits"] < r184)
        for rule in (54, 110)
    }
    return {
        "anchor_order": bool(r30 < r184),
        "candidate_pass": candidates,
        "pass": bool(r30 < r184 and all(candidates.values())),
        "reserve_bits": {
            str(rule): rows[rule]["reserve_bits"]
            for rule in (30, 54, 110, 184, 126)
        },
    }


def main() -> None:
    result = {
        "schema": "asymptotic-closure-scaling-v1",
        "date": "2026-10-07",
        "protocol": "docs/research/protocols/asymptotic-closure-scaling-20261007.md",
        "panel": PANEL,
        "evaluated_widths": [],
        "profiles": {},
        "gates": {},
    }

    rows16 = {rule: profile(rule, 16) for rule in PANEL}
    result["evaluated_widths"].append(16)
    result["profiles"]["16"] = {str(rule): rows16[rule] for rule in PANEL}
    p1 = reserve_corridor(rows16)
    result["gates"]["P1_width16_reserve_corridor"] = p1

    if not p1["pass"]:
        result["stop_reason"] = "P1 reserve corridor failed at n=16"
    else:
        rows18 = {rule: profile(rule, 18) for rule in PANEL}
        result["evaluated_widths"].append(18)
        result["profiles"]["18"] = {str(rule): rows18[rule] for rule in PANEL}
        p2 = reserve_corridor(rows18)
        result["gates"]["P2_width18_reserve_corridor"] = p2

        if not p2["pass"]:
            result["stop_reason"] = "P2 reserve corridor failed at n=18"
        else:
            p3_detail = {
                str(rule): {
                    "baseline_width14_hstar": BASELINE_H[rule],
                    "width18_hstar": rows18[rule]["hstar"],
                    "pass": rows18[rule]["hstar"] > BASELINE_H[rule],
                }
                for rule in (54, 110)
            }
            p3 = all(item["pass"] for item in p3_detail.values())
            result["gates"]["P3_staircase_advances"] = {
                "detail": p3_detail,
                "pass": p3,
            }
            result["stop_reason"] = (
                "frozen scaling program complete"
                if p3 else "P3 repair staircase did not advance for both candidates"
            )

    p1_ok = result["gates"]["P1_width16_reserve_corridor"]["pass"]
    p2_ok = result["gates"].get("P2_width18_reserve_corridor", {}).get("pass", False)
    p3_ok = result["gates"].get("P3_staircase_advances", {}).get("pass", False)
    result["summary"] = {
        "status": "bounded-positive" if p1_ok and p2_ok and p3_ok else "negative",
        "evaluated_widths": result["evaluated_widths"],
        "stop_reason": result["stop_reason"],
    }

    result["source_hashes"] = {
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result["summary"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
