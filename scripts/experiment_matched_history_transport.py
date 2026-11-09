#!/usr/bin/env python3
"""Matched Rule-62/Rule-110 predictive-history versus Groovy transport test.

Protocol:
  docs/research/protocols/matched-history-transport-20261007.md
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

RULES = (62, 110)
WIDTHS = (16, 18)
OUT = Path("results/matched_history_transport_20261007.json")


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


def entropy(labels: np.ndarray) -> float:
    counts = np.bincount(labels.astype(np.int64))
    counts = counts[counts > 0].astype(np.float64)
    p = counts / counts.sum()
    return float(-(p * np.log2(p)).sum())


def centered_g_map(rule: int, n: int, h: np.ndarray) -> np.ndarray:
    states = np.arange(2**n, dtype=np.uint32)
    h2 = h[h]
    d = states ^ h
    raw_g = h ^ h2 ^ h[d]
    return raw_g ^ h[0]


def first_factor_witness(
    states: np.ndarray,
    current: np.ndarray,
    labels: np.ndarray,
    g_current: np.ndarray,
    next_obs: np.ndarray,
    h: np.ndarray,
    n: int,
) -> dict | None:
    key = (labels.astype(np.uint64) << np.uint64(n)) | g_current.astype(np.uint64)
    order = np.argsort(key, kind="mergesort")
    sorted_key = key[order]
    sorted_obs = next_obs[order]

    start = 0
    while start < len(order):
        end = start + 1
        while end < len(order) and sorted_key[end] == sorted_key[start]:
            end += 1
        if end - start > 1:
            first_index = order[start]
            first_obs = sorted_obs[start]
            for pos in range(start + 1, end):
                if sorted_obs[pos] != first_obs:
                    second_index = order[pos]
                    cx = int(current[first_index])
                    cy = int(current[second_index])
                    return {
                        "source_x": int(states[first_index]),
                        "source_y": int(states[second_index]),
                        "current_x": cx,
                        "current_y": cy,
                        "predictive_label": int(labels[first_index]),
                        "centered_G": int(g_current[first_index]),
                        "current_D_x": int(cx ^ h[cx]),
                        "current_D_y": int(cy ^ h[cy]),
                        "next_observation_x": int(next_obs[first_index]),
                        "next_observation_y": int(next_obs[second_index]),
                    }
        start = end
    return None


def profile(rule: int, n: int) -> dict:
    h = state_map(rule, n)
    coarse_step = h[h]
    observation = block2_parity_map(n)
    g_map = centered_g_map(rule, n, h)

    states = np.arange(2**n, dtype=np.uint32)
    current = states.copy()
    labels = compress(observation[current])
    steps = []

    t = 0
    while True:
        g_current = g_map[current]
        next_current = coarse_step[current]
        next_obs = observation[next_current]

        witness = first_factor_witness(
            states, current, labels, g_current, next_obs, h, n
        )
        factor_pass = witness is None

        pair = (labels.astype(np.uint64) << (n // 2)) | next_obs.astype(np.uint64)
        refined = compress(pair)

        repair_bits = entropy(refined) - entropy(labels)

        key = (labels.astype(np.uint64) << np.uint64(n)) | g_current.astype(np.uint64)
        key_labels = compress(key)
        joint = (
            key_labels.astype(np.uint64) << (n // 2)
        ) | next_obs.astype(np.uint64)
        conditional_next_given_cg = entropy(compress(joint)) - entropy(key_labels)
        g_coupled_bits = repair_bits - conditional_next_given_cg
        gamma = (
            g_coupled_bits / repair_bits
            if repair_bits > 1e-12
            else None
        )

        steps.append({
            "t": t,
            "repair_bits": repair_bits,
            "factor_pass": factor_pass,
            "conditional_next_given_C_G_bits": conditional_next_given_cg,
            "G_coupled_bits": g_coupled_bits,
            "gamma": gamma,
            "witness": witness,
        })

        old_count = int(labels.max()) + 1
        new_count = int(refined.max()) + 1
        if new_count == old_count:
            break

        labels = refined
        current = next_current
        t += 1
        if t > n + 20:
            raise RuntimeError(f"no closure rule={rule} n={n}")

    nonzero = [x for x in steps if x["repair_bits"] > 1e-12]
    total_repair = sum(x["repair_bits"] for x in nonzero)
    total_coupled = sum(x["G_coupled_bits"] for x in nonzero)

    return {
        "rule": rule,
        "n": n,
        "hstar": len(nonzero),
        "all_nonzero_steps_factor": all(x["factor_pass"] for x in nonzero),
        "any_nonzero_step_failure": any(not x["factor_pass"] for x in nonzero),
        "cumulative_G_coupled_fraction": (
            total_coupled / total_repair if total_repair > 1e-12 else None
        ),
        "uncoupled_repair_bits": total_repair - total_coupled,
        "steps": steps,
    }


def main() -> None:
    result = {
        "schema": "matched-history-transport-v1",
        "date": "2026-10-07",
        "protocol": "docs/research/protocols/matched-history-transport-20261007.md",
        "rules": list(RULES),
        "widths": list(WIDTHS),
        "profiles": {},
        "gates": {},
    }

    for n in WIDTHS:
        rows = {rule: profile(rule, n) for rule in RULES}
        result["profiles"][str(n)] = {str(rule): rows[rule] for rule in RULES}

        p110 = rows[110]["all_nonzero_steps_factor"]
        p62 = rows[62]["any_nonzero_step_failure"]
        result["gates"][str(n)] = {
            "rule110_all_repairs_G_sufficient": p110,
            "rule62_has_G_insufficient_repair": p62,
            "pass": p110 and p62,
        }

        if not (p110 and p62):
            result["stop_reason"] = f"matched separation failed at n={n}"
            break

    all_pass = all(
        result["gates"].get(str(n), {}).get("pass", False)
        for n in WIDTHS
    )
    result["summary"] = {
        "status": "bounded-positive" if all_pass else "negative",
        "stop_reason": result.get(
            "stop_reason",
            "fresh matched program complete"
        ),
        "fresh_widths_evaluated": [
            n for n in WIDTHS if str(n) in result["profiles"]
        ],
    }

    result["source_hashes"] = {
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result["summary"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
