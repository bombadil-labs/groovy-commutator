"""Post-discovery algebraic audit for selector-shielding wall holes.

The coupled wall tables U_p,V_p were inferred from the directly checked
trajectory.  This script proves the *reference-membership* half of the
shielding argument: for every fine-time residue p=t mod 8, every proposed
coupled row-2 hole lies on a Rule-90 hole of the isolated lower strip for all
times in that residue class.

The proof is finite because the candidate offsets are at most 13.  In edge
coordinates, the isolated strip is

    (1+z)^eps (1+z^2)^n S(z)

on the left and the same expression with the reversed seed on the right,
where t=2n+eps.  Coefficients through logical depth 6 involve C(n,j) only for
j<4; by Lucas, their parity depends only on n mod 4, equivalently t mod 8.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/selector_shielding_reference_edges_20260908.json"
SEED = {0, 1, 3, 4, 6}
DEG = max(SEED)
REVERSED = {DEG - i for i in SEED}

# Coupled physical hole offsets observed from tick 32 onward, expressed in the
# two characteristic frames x=-t+u and x=t+v.  All offsets are odd because
# they lie on the background-one parity in those frames.
LEFT_WALL = {
    0: {1, 3, 7, 9},
    1: {5, 11},
    2: {1, 3},
    3: set(),
    4: {1, 3},
    5: {5, 7},
    6: {1, 3, 5},
    7: {7},
}
RIGHT_WALL = {
    0: {1, 3, 7, 9, 13},
    1: {3, 5, 9, 11, 13},
    2: {1, 5, 7, 13},
    3: {1, 3, 7, 11, 13},
    4: {3, 5, 7, 9, 13},
    5: {1, 9, 11, 13},
    6: {1, 7, 13},
    7: {1, 5, 7, 11, 13},
}


def choose_parity_lucas(n: int, j: int) -> int:
    """C(n,j) mod 2 from Lucas: all 1-bits of j must occur in n."""
    if j < 0 or j > n:
        return 0
    return int((j & ~n) == 0)


def coefficient(seed: set[int], n_mod4: int, eps: int, k: int) -> int:
    """Coefficient z^k of (1+z)^eps (1+z^2)^n S, for any n>=3
    having the declared n mod 4.

    At k<=6, only binomial indices j<=3 can contribute, so using a
    representative n=4+n_mod4 is exact for every larger n in the same class.
    """
    n = 4 + n_mod4
    total = 0
    eps_shifts = (0, 1) if eps else (0,)
    for s in seed:
        for e in eps_shifts:
            rem = k - s - e
            if rem >= 0 and rem % 2 == 0:
                total ^= choose_parity_lucas(n, rem // 2)
    return total


def left_reference_offsets(p: int) -> set[int]:
    eps = p & 1
    n_mod4 = (p // 2) % 4
    # Candidate wall offsets never exceed 13 => logical depth <=6.
    return {
        2*k + 1
        for k in range(7)
        if coefficient(SEED, n_mod4, eps, k)
    }


def right_reference_offsets(p: int) -> set[int]:
    eps = p & 1
    n_mod4 = (p // 2) % 4
    # k is logical distance from the right edge, physical v=13-2k.
    return {
        13 - 2*k
        for k in range(7)
        if coefficient(REVERSED, n_mod4, eps, k)
    }


def main() -> None:
    records = []
    failures = []
    for p in range(8):
        lref = left_reference_offsets(p)
        rref = right_reference_offsets(p)
        lok = LEFT_WALL[p] <= lref
        rok = RIGHT_WALL[p] <= rref
        row = {
            "phase": p,
            "left_wall": sorted(LEFT_WALL[p]),
            "left_reference": sorted(lref),
            "left_subset": lok,
            "right_wall": sorted(RIGHT_WALL[p]),
            "right_reference": sorted(rref),
            "right_subset": rok,
        }
        records.append(row)
        if not (lok and rok):
            failures.append(row)

    result = {
        "ok": not failures,
        "claim": (
            "Conditional on the observed period-8 coupled wall table, every "
            "coupled row-2 hole is an isolated Rule-90 row-2 hole for every "
            "fine time t>=32."
        ),
        "reason_period_8_is_exact": (
            "Candidate physical offsets <=13 correspond to logical edge depth "
            "<=6. Their coefficients use C(n,j) only for j<=3, whose parity "
            "depends only on n mod 4 by Lucas; t=2n+eps therefore reduces to "
            "t mod 8."
        ),
        "records": records,
        "failures": failures,
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
