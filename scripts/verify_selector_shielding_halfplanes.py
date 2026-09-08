"""Post-discovery exact verifier for selector-shielding moving walls.

The scientific deduction is analytic: in the left-moving frame u=x+t the
selector law is one-sided in u, so every half-plane u<=U is forward closed.
In the right-moving frame v=x-t every half-plane v>=V is forward closed.
Therefore exact equality of two frame states 32 ticks apart on such a
half-plane proves period-32 recurrence there for all later times.

This script independently evolves the shielding witness with the established
dense and sparse kernels through ticks 64 and 96, confirms complete-field
agreement, and checks the finite-support equality that certifies the two
half-plane recurrences.
"""
from __future__ import annotations

import json
from pathlib import Path

from experiment_pulse_scattering import dense_step
from audit_pulse_scattering import sparse_step

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/selector_shielding_halfplanes_20260908.json"
A = {-5, 0}
B = {0, 1, 3, 4, 6}
T0 = 64
T1 = 96
PERIOD = T1 - T0
LEFT_U_MAX = 48
RIGHT_V_MIN = 0


def encode(row: int, support: set[int]) -> set[tuple[int, int]]:
    out: set[tuple[int, int]] = set()
    for i in support:
        out.add((row, 2 * i + 1))
        out.add((row + 1, 2 * i))
    return out


def seed() -> set[tuple[int, int]]:
    return encode(0, A) | encode(2, B)


def left_frame(delta: set[tuple[int, int]], t: int, u_max: int):
    return {(y, x + t) for y, x in delta if x + t <= u_max}


def right_frame(delta: set[tuple[int, int]], t: int, v_min: int):
    return {(y, x - t) for y, x in delta if x - t >= v_min}


def main() -> None:
    dense = seed()
    sparse = set(dense)
    snapshots: dict[int, set[tuple[int, int]]] = {}
    checked_ticks = 0
    checked_points = 0

    for t in range(T1 + 1):
        if dense != sparse:
            raise AssertionError(f"dense/sparse mismatch at tick {t}")
        checked_ticks += 1
        checked_points += len(dense)
        if t in (T0, T1):
            snapshots[t] = set(dense)
        if t < T1:
            dense = dense_step(dense, t)
            sparse = sparse_step(sparse, t)

    d0, d1 = snapshots[T0], snapshots[T1]
    left0 = left_frame(d0, T0, LEFT_U_MAX)
    left1 = left_frame(d1, T1, LEFT_U_MAX)
    right0 = right_frame(d0, T0, RIGHT_V_MIN)
    right1 = right_frame(d1, T1, RIGHT_V_MIN)

    left_diff = sorted(left0 ^ left1)
    right_diff = sorted(right0 ^ right1)
    if left_diff or right_diff:
        raise AssertionError({"left": left_diff[:20], "right": right_diff[:20]})

    result = {
        "ok": True,
        "witness": {"upper": sorted(A), "lower": sorted(B)},
        "ticks": [T0, T1],
        "period": PERIOD,
        "dense_sparse_complete_field_ticks": checked_ticks,
        "dense_sparse_changed_points": checked_points,
        "left_halfplane": {
            "frame": "u=x+t",
            "domain": f"u<={LEFT_U_MAX}",
            "tick64_points": len(left0),
            "tick96_points": len(left1),
            "symmetric_difference": 0,
            "causal_fact": "new u reads only old u-2,u-1,u; the half-plane is forward closed",
            "conclusion": "period 32 for this complete left-frame half-plane for all t>=64",
        },
        "right_halfplane": {
            "frame": "v=x-t",
            "domain": f"v>={RIGHT_V_MIN}",
            "tick64_points": len(right0),
            "tick96_points": len(right1),
            "symmetric_difference": 0,
            "causal_fact": "new v reads only old v,v+1,v+2; the half-plane is forward closed",
            "conclusion": "period 32 for this complete right-frame half-plane for all t>=64",
        },
        "proof_boundary": (
            "This proves the two moving-wall recurrences, not absence of a new "
            "negative row-2 defect born in the widening middle."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
