#!/usr/bin/env python3
"""Exact fresh-width test of the asymptotic-closure wedge.

Protocol:
  docs/research/protocols/asymptotic-closure-wedge-20261007.md
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

PANEL = [0, 4, 90, 184, 30, 126, 54, 110]
WIDTHS = [12, 14, 16]
OUT = Path("results/asymptotic_closure_wedge_20261007.json")


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
        "latent_bits": latent,
        "repair_bits": repair_bits,
        "A90": a90,
        "depth_density": hstar / n,
        "safe_forgetting_density": (n - hinf) / n,
    }


def wedge(rows: dict[int, dict]) -> dict:
    d184 = rows[184]["depth_density"]
    d30 = rows[30]["depth_density"]
    s184 = rows[184]["safe_forgetting_density"]
    s30 = rows[30]["safe_forgetting_density"]
    anchors = d184 < d30 and s30 < s184
    candidates = {}
    for rule in (54, 110):
        d = rows[rule]["depth_density"]
        s = rows[rule]["safe_forgetting_density"]
        candidates[str(rule)] = bool(
            anchors and d184 < d < d30 and s30 < s < s184
        )
    return {
        "anchors_ordered": anchors,
        "candidate_pass": candidates,
        "pass": anchors and all(candidates.values()),
        "coordinates": {
            str(rule): {
                "depth_density": rows[rule]["depth_density"],
                "safe_forgetting_density": rows[rule]["safe_forgetting_density"],
            }
            for rule in (184, 30, 54, 110, 126)
        },
    }


def main() -> None:
    result = {
        "schema": "asymptotic-closure-wedge-v1",
        "date": "2026-10-07",
        "protocol": "docs/research/protocols/asymptotic-closure-wedge-20261007.md",
        "panel": PANEL,
        "evaluated_widths": [],
        "profiles": {},
        "gates": {},
    }

    for idx, n in enumerate(WIDTHS):
        rows = {rule: profile(rule, n) for rule in PANEL}
        result["evaluated_widths"].append(n)
        result["profiles"][str(n)] = {str(rule): rows[rule] for rule in PANEL}
        gate = wedge(rows)
        result["gates"][str(n)] = gate
        if not gate["pass"]:
            result["stop_reason"] = f"strict wedge failed at n={n}"
            break

    result["summary"] = {
        "status": "positive-through-stress"
        if result["evaluated_widths"] == WIDTHS and result["gates"]["16"]["pass"]
        else "negative",
        "evaluated_widths": result["evaluated_widths"],
        "stop_reason": result.get("stop_reason", "stress complete"),
    }

    result["source_hashes"] = {
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result["summary"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
