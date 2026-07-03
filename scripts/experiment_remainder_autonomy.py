"""Is the remainder a THING? Autonomy of the disagreement field.

The disagreement field C(path1, path2) of a rule pair is, mechanically, a
shadow: diff(t+1) is determined by the two hidden substrate trajectories
(6 bits per cell of hidden neighborhood), not by diff(t) itself. The
question "when does a relationship become a thing" has a sharp local
version: HOW CLOSE does the disagreement field come to having its own
closed local dynamics -- a rule of its own that predicts diff(t+1) from
diff(t)'s neighborhood alone, no access to the substrates?

Measured: for each pair, run the divergence construction, then fit the
best deterministic radius-r local rule to the observed diff transitions
(majority outcome per neighborhood) and score its accuracy. Autonomy = 1
means the remainder IS a cellular automaton in its own right; ~0.5 on a
density-0.5 field means the remainder is pure shadow.

Guardrails, because two regimes are trivially autonomous:
  - commute (all-zero field) and crystalline (near-constant field) score
    ~1.0 for free; we report field density/activity alongside so the
    interesting claim -- NONTRIVIAL autonomy -- is separable.
  - baseline: per-neighborhood-blind accuracy (predict the field's
    majority bit everywhere).

Output:
    results/remainder_autonomy.csv
    printed per-regime summaries (promoted to NOTES/site only if they
    survive scrutiny)
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from groovy.ca import apply_rule  # noqa: E402

N = 200
STEPS = 400
BURN = 50
PAIRS_PER_REGIME = 120
RADII = (1, 2, 3)


def divergence_field(state0, rule_a, rule_b, steps):
    p1, p2 = state0.copy(), state0.copy()
    field = np.zeros((steps, len(state0)), dtype=np.uint8)
    for t in range(steps):
        field[t] = np.bitwise_xor(p1, p2)
        p1 = apply_rule(apply_rule(p1, rule_a), rule_b)
        p2 = apply_rule(apply_rule(p2, rule_b), rule_a)
    return field


def autonomy_score(field, radius):
    """Fit the best deterministic radius-r rule to field's transitions,
    return (accuracy, n_transitions). Neighborhood = 2r+1 cells."""
    steps, n = field.shape
    width = 2 * radius + 1
    # pack neighborhoods of row t into integers
    idx = np.zeros((steps - 1, n), dtype=np.int64)
    for k, off in enumerate(range(-radius, radius + 1)):
        idx = (idx << 1) | np.roll(field[:-1], -off, axis=1).astype(np.int64)
    nxt = field[1:].astype(np.int64)
    buckets = 1 << width
    flat = idx.ravel() * 2 + nxt.ravel()
    counts = np.bincount(flat, minlength=buckets * 2).reshape(buckets, 2)
    correct = counts.max(axis=1).sum()
    total = counts.sum()
    return correct / total, total


def field_stats(field):
    dens = float(field.mean())
    # activity: fraction of cells that change between consecutive rows
    act = float(np.bitwise_xor(field[1:], field[:-1]).mean())
    return dens, act


def main() -> None:
    sweep = pd.read_parquet(ROOT / "results" / "sweep_full_classified.parquet")
    rng = np.random.default_rng(0)
    sample = sweep.groupby("regime").sample(n=PAIRS_PER_REGIME, random_state=1)
    print(f"sampled {len(sample)} pairs")

    rows = []
    for i, r in enumerate(sample.to_dict("records")):
        s0 = rng.integers(0, 2, N).astype(np.uint8)
        field = divergence_field(s0, int(r["rule_a"]), int(r["rule_b"]), STEPS)[BURN:]
        dens, act = field_stats(field)
        row = dict(rule_a=int(r["rule_a"]), rule_b=int(r["rule_b"]), regime=r["regime"],
                   density=round(dens, 4), activity=round(act, 4),
                   baseline=round(max(dens, 1 - dens), 4))
        for rad in RADII:
            acc, _ = autonomy_score(field, rad)
            row[f"autonomy_r{rad}"] = round(float(acc), 4)
        rows.append(row)
        if i % 100 == 0:
            print(f"{i}/{len(sample)}", flush=True)

    df = pd.DataFrame(rows)
    df.to_csv(ROOT / "results" / "remainder_autonomy.csv", index=False)

    # nontrivial subset: field actually alive (density and activity not ~0)
    live = df[(df.activity > 0.02) & (df.density > 0.02)]
    print("\nALL pairs, median by regime:")
    print(df.groupby("regime")[["density", "activity", "baseline",
                                "autonomy_r1", "autonomy_r2", "autonomy_r3"]].median().round(3))
    print("\nLIVE fields only (density & activity > 0.02), median by regime:")
    print(live.groupby("regime")[["density", "baseline",
                                  "autonomy_r1", "autonomy_r2", "autonomy_r3"]].median().round(3))
    print("\nlift over blind baseline (autonomy_r2 - baseline), live fields, median:")
    live2 = live.copy()
    live2["lift_r2"] = live2.autonomy_r2 - live2.baseline
    print(live2.groupby("regime")["lift_r2"].median().round(3))
    print("\nflagship examples:")
    for a, b in [(110, 54), (110, 30), (90, 165), (184, 250)]:
        s0 = np.random.default_rng(7).integers(0, 2, N).astype(np.uint8)
        f = divergence_field(s0, a, b, STEPS)[BURN:]
        d, ac = field_stats(f)
        accs = [round(autonomy_score(f, rad)[0], 3) for rad in RADII]
        print(f"  {a}/{b}: density={d:.3f} activity={ac:.3f} autonomy r1/r2/r3 = {accs}")


if __name__ == "__main__":
    main()
