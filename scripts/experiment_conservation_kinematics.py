"""Sizes as physics: the conservation atlas, and glider kinematics.

Part A -- THE CONSERVATION ATLAS (Noetherpoetics, operationalized).
For every elementary rule and every wet-math observable
    live      |S|            (number-conserving CA, the known baseline)
    absential |A(S)|         (off-but-adjacent count)
    void      |V(S)|         (off-and-isolated count)
    closed    |S|+|A(S)|     (closed-neighborhood / dilation measure)
    ddensity  |S xor phi(S)| (how much is changing)
check EXACT conservation -- f(phi(S)) == f(S) for every S -- exhaustively
at n=12 AND n=13 (both, so even/odd ring artifacts can't sneak through).
The live-count column reproduces the known number-conserving ECA as a
sanity anchor; every other column is, to our knowledge, a new little
atlas: which rules conserve their halo, their void, their footprint,
their rate of change.

Part B -- GLIDER KINEMATICS (the E=mc^2 rant, held lightly).
For the standard Life bestiary measure, per object, over one full period:
    m      mean live cells          ("bare mass")
    m_halo mean live + absential    ("dressed mass" -- mass with its field)
    E      mean cells changed/step  ("activity")
    v      net displacement/period  (cells/step; Moore-metric speed)
Then look at the ratios instead of assuming the famous formula. Note that
c here is literal: radius-1 CA propagate influence at most 1 cell/step,
and Life's proven speed limits are c/2 orthogonal, c/4 diagonal.

Output: results/conservation_atlas.csv, printed kinematics table.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from groovy.ca import rule_lut  # noqa: E402
from groovy import ca2d  # noqa: E402


def all_states(n):
    ints = np.arange(2 ** n, dtype=np.uint32)
    return ((ints[:, None] >> np.arange(n, dtype=np.uint32)[None, :]) & 1).astype(np.uint8)


def step_all(S, rn):
    lut = rule_lut(rn)
    return lut[4 * np.roll(S, 1, axis=1) + 2 * S + np.roll(S, -1, axis=1)]


def observables(S):
    l = np.roll(S, 1, axis=1)
    r = np.roll(S, -1, axis=1)
    nb = (S | l | r)
    A = (nb & (1 - S))
    live = S.sum(axis=1)
    absent = A.sum(axis=1)
    void = S.shape[1] - live - absent
    return dict(live=live, absential=absent, void=void, closed=live + absent)


def conserved_atlas():
    results = {}
    for n in (12, 13):
        S = all_states(n)
        obs0 = observables(S)
        for rn in range(256):
            S1 = step_all(S, rn)
            obs1 = observables(S1)
            dd0 = (S ^ S1).sum(axis=1)
            S2 = step_all(S1, rn)
            dd1 = (S1 ^ S2).sum(axis=1)
            flags = {name: bool(np.array_equal(obs0[name], obs1[name])) for name in obs0}
            flags["ddensity"] = bool(np.array_equal(dd0, dd1))
            results.setdefault(rn, []).append(flags)
    rows = []
    for rn, (f12, f13) in results.items():
        rows.append(dict(rule=rn, **{k: (f12[k] and f13[k]) for k in f12}))
    return pd.DataFrame(rows)


# ---- Life bestiary ---------------------------------------------------------
BESTIARY = {
    # name: (cells, period, displacement per period (dr, dc))
    "block":    ([(0, 0), (0, 1), (1, 0), (1, 1)], 1, (0, 0)),
    "beehive":  ([(0, 1), (0, 2), (1, 0), (1, 3), (2, 1), (2, 2)], 1, (0, 0)),
    "blinker":  ([(0, 0), (0, 1), (0, 2)], 2, (0, 0)),
    "toad":     ([(0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2)], 2, (0, 0)),
    "beacon":   ([(0, 0), (0, 1), (1, 0), (2, 3), (3, 2), (3, 3)], 2, (0, 0)),
    "glider":   ([(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)], 4, (1, 1)),
    "lwss":     ([(0, 1), (0, 4), (1, 0), (2, 0), (2, 4), (3, 0), (3, 1), (3, 2), (3, 3)], 4, (0, -2)),
    "mwss":     ([(0, 2), (1, 0), (1, 4), (2, 5), (3, 0), (3, 5), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5)], 4, (0, -2)),
}
GRID = 40


def kinematics():
    rows = []
    for name, (cells, period, (dr, dc)) in BESTIARY.items():
        g = np.zeros((GRID, GRID), dtype=np.uint8)
        for r, c in cells:
            g[(12 + r) % GRID, (12 + c) % GRID] = 1
        m, halo, E = [], [], []
        cur = g
        for t in range(period):
            m.append(cur.sum())
            halo.append(cur.sum() + ca2d.absential_field_2d(cur).sum())
            nxt = ca2d.apply_2d_rule(cur, {3}, {2, 3})
            E.append(int((cur ^ nxt).sum()))
            cur = nxt
        # auto-detect the displacement instead of trusting the table: find
        # the (dr, dc) that maps the start onto the state after one period
        ok = False
        for ddr in range(-3, 4):
            for ddc in range(-3, 4):
                if np.array_equal(cur, np.roll(np.roll(g, ddr, axis=0), ddc, axis=1)):
                    dr, dc, ok = ddr, ddc, True
                    break
            if ok:
                break
        v = float(np.hypot(dr, dc) / period)          # euclidean cells/step
        v_moore = float(max(abs(dr), abs(dc)) / period)  # chebyshev (light-cone metric)
        rows.append(dict(obj=name, period=period, verified=ok,
                         m=float(np.mean(m)), m_halo=float(np.mean(halo)),
                         E=float(np.mean(E)), v=round(v, 3), v_moore=round(v_moore, 3)))
    return pd.DataFrame(rows)


def main() -> None:
    atlas = conserved_atlas()
    atlas.to_csv(ROOT / "results" / "conservation_atlas.csv", index=False)
    for col in ("live", "absential", "void", "closed", "ddensity"):
        rules = sorted(atlas[atlas[col]].rule.tolist())
        print(f"conserve {col:10s} ({len(rules):3d}): {rules}")

    print("\nLife kinematics (B3/S23):")
    kin = kinematics()
    kin["E_per_m"] = (kin.E / kin.m).round(3)
    kin["E_per_mv"] = np.where(kin.v > 0, (kin.E / (kin.m * kin.v_moore)).round(3), np.nan)
    print(kin.to_string(index=False))


if __name__ == "__main__":
    main()
