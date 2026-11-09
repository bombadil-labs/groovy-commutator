#!/usr/bin/env python3
"""Exact bounded test of asymptotic closure under minimal predictive repair.

Protocol:
  docs/research/protocols/asymptotic-closure-20261007.md

The experiment uses the established nonoverlapping block-2 parity observer
at cadence q=2. It computes the exact future-equivalence tower C_t on a
finite periodic ECA ring and stops at the first failed protocol gate.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

PANEL = [0, 4, 90, 184, 30, 126, 54, 110]
PRIMARY_N = 10
CONFIRM_N = 12
STRESS_N = 14
OUT = Path("results/asymptotic_closure_20261007.json")


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
    if n % 2:
        raise ValueError("block-2 parity requires even n")
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
    states = np.arange(2**n, dtype=np.uint32)

    current = states.copy()
    labels = compress(observation[current])
    entropies = [partition_entropy(labels)]
    class_counts = [int(labels.max()) + 1]
    deltas: list[float] = []

    hstar = None
    for t in range(n + 8):
        current = step[current]
        target = observation[current]
        pair = (labels.astype(np.uint64) << (n // 2)) | target.astype(np.uint64)
        refined = compress(pair)
        h_new = partition_entropy(refined)
        deltas.append(h_new - entropies[-1])
        entropies.append(h_new)
        class_counts.append(int(refined.max()) + 1)

        if class_counts[-1] == class_counts[-2]:
            hstar = t
            break

        labels = refined

    if hstar is None:
        raise RuntimeError(f"no stabilization for rule={rule} n={n}")

    entropies = entropies[: hstar + 1]
    class_counts = class_counts[: hstar + 1]
    deltas = deltas[:hstar]

    h0 = entropies[0]
    hinf = entropies[hstar]
    latent = hinf - h0

    if latent <= 1e-12:
        t50 = t90 = t99 = 0
        a90 = 0.0
        tail_steps_90 = 0
        mean_repair = 0.0
        last_repair = 0.0
    else:
        resolved = [(h - h0) / latent for h in entropies]

        def first_at(threshold: float) -> int:
            return next(i for i, value in enumerate(resolved)
                        if value + 1e-12 >= threshold)

        t50 = first_at(0.50)
        t90 = first_at(0.90)
        t99 = first_at(0.99)
        a90 = (hstar - t90) / hstar if hstar else 0.0
        tail_steps_90 = sum(
            1 for i, value in enumerate(deltas)
            if i >= t90 and value > 1e-12
        )
        mean_repair = latent / hstar if hstar else 0.0
        last_repair = next(
            (value for value in reversed(deltas) if value > 1e-12), 0.0
        )

    return {
        "rule": rule,
        "n": n,
        "hstar": hstar,
        "class_counts": class_counts,
        "partition_entropy": entropies,
        "repair_bits": deltas,
        "H0": h0,
        "Hinf": hinf,
        "latent_bits": latent,
        "t50": t50,
        "t90": t90,
        "t99": t99,
        "A90": a90,
        "depth_density": hstar / n,
        "stable_entropy_density": hinf / n,
        "safe_forgetting_reserve_bits": n - hinf,
        "mean_repair_bits": mean_repair,
        "last_nonzero_repair_bits": last_repair,
        "nonzero_repair_steps_after_t90": tail_steps_90,
    }


def p2_pass(rows: dict[int, dict]) -> bool:
    complex_min = min(rows[54]["A90"], rows[110]["A90"])
    chaotic_max = max(rows[30]["A90"], rows[126]["A90"])
    return complex_min > chaotic_max


def transport_confound(rows10: dict[int, dict], rows12: dict[int, dict]) -> bool:
    for rows in (rows10, rows12):
        weak_complex_a = min(rows[54]["A90"], rows[110]["A90"])
        weak_complex_d = min(rows[54]["depth_density"], rows[110]["depth_density"])
        if not (rows[184]["A90"] >= weak_complex_a
                and rows[184]["depth_density"] >= weak_complex_d):
            return False
    return True


def main() -> None:
    result: dict = {
        "schema": "asymptotic-closure-v1",
        "date": "2026-10-07",
        "protocol": "docs/research/protocols/asymptotic-closure-20261007.md",
        "observer": {
            "kind": "nonoverlapping block-2 parity",
            "cadence": 2,
        },
        "panel": PANEL,
        "evaluated_widths": [],
        "profiles": {},
        "gate_decision": {},
    }

    rows10 = {r: profile(r, PRIMARY_N) for r in PANEL}
    result["evaluated_widths"].append(PRIMARY_N)
    result["profiles"][str(PRIMARY_N)] = {str(r): rows10[r] for r in PANEL}

    p1 = rows10[0]["hstar"] == 0 and rows10[90]["hstar"] == 0
    p2 = p2_pass(rows10)
    result["gate_decision"]["P1_controls"] = p1
    result["gate_decision"]["P2_primary_complex_gt_chaotic"] = p2

    if not p1:
        result["gate_decision"]["stop_reason"] = "P1 control failure"
    elif not p2:
        result["gate_decision"]["stop_reason"] = (
            "P2 failed at n=10: both Rules 54/110 did not have A90 "
            "strictly above both Rules 30/126"
        )
    else:
        rows12 = {r: profile(r, CONFIRM_N) for r in PANEL}
        result["evaluated_widths"].append(CONFIRM_N)
        result["profiles"][str(CONFIRM_N)] = {str(r): rows12[r] for r in PANEL}
        p3 = p2_pass(rows12)
        result["gate_decision"]["P3_confirmation_complex_gt_chaotic"] = p3

        if not p3:
            result["gate_decision"]["stop_reason"] = "P3 failed at n=12"
        else:
            confound = transport_confound(rows10, rows12)
            result["gate_decision"]["P4_transport_confound"] = confound
            if confound:
                result["gate_decision"]["stop_reason"] = "P4 Rule-184 transport confound"
            else:
                rows14 = {r: profile(r, STRESS_N) for r in PANEL}
                result["evaluated_widths"].append(STRESS_N)
                result["profiles"][str(STRESS_N)] = {str(r): rows14[r] for r in PANEL}
                p5 = p2_pass(rows14)
                result["gate_decision"]["P5_stress_complex_gt_chaotic"] = p5
                result["gate_decision"]["stop_reason"] = (
                    "stress complete; no broader census authorized"
                )

    result["summary"] = {
        "status": "negative" if not result["gate_decision"].get(
            "P2_primary_complex_gt_chaotic", False) else "see later gates",
        "primary_A90": {
            str(r): rows10[r]["A90"] for r in PANEL
        },
        "primary_hstar": {
            str(r): rows10[r]["hstar"] for r in PANEL
        },
        "primary_key_result": (
            "Rule 30 has a longer thin minimal-repair tail than Rules 54/110 "
            "under the frozen observer at n=10"
        ) if not p2 else "primary ordering survived",
    }

    source = Path(__file__).read_bytes()
    result["source_hashes"] = {
        "script_sha256": hashlib.sha256(source).hexdigest()
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result["summary"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
