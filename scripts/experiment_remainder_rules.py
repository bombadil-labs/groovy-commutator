"""Cycle-1 follow-up: WHICH structured remainders are exactly closed, what
rule do they follow, and why.

experiment_remainder_autonomy.py established the spectrum (structured
remainders are observationally closed local dynamics; noisy remainders are
irreducibly open). This script extracts the exact cases:

1. Among live structured pairs, how many disagreement fields are EXACTLY
   predicted (held-out test accuracy 1.0) by a radius-2 rule? By a plain
   elementary (radius-1) rule?
2. For the elementary cases, extract the remainder rule number. Empirical
   result: every elementary remainder found is rule 170 or 240 -- the two
   shifts. The relationship is a soliton: a disagreement pattern that only
   ever translates.
3. Mechanism test, exhaustive at n=12. The algebraic explanation
   ("Galilean pairs": A.B == sigma^k . B.A as maps) is FALSE for every
   pair tested. The dynamical explanation holds for most: the pair's
   round map acts as a PURE SHIFT on its reachable attractor (eventual
   image), i.e. both orderings fall into traveling-wave attractors of a
   shared velocity, and the disagreement inherits the drift. For the
   remaining pairs the shift action holds only on the component reachable
   from equal starting states (diagonal), not the whole eventual image --
   and those are exactly the ones whose remainder-shift is seed-dependent.

Caveat that must travel with this result: "exactly closed" means exact on
the observed trajectory/attractor (zero contradictions, held-out-perfect),
NOT an identity over all of state space. The remainder is a thing *on the
attractor where the relationship lives*.

Output: results/remainder_rules.csv + printed summary.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from groovy.ca import apply_rule, rule_lut  # noqa: E402

N = 200
STEPS = 400
BURN = 50
SAMPLE = 200
N_EXACT = 12  # ring size for the exhaustive mechanism tests


def divergence_field(s0, a, b, steps):
    p1, p2 = s0.copy(), s0.copy()
    field = np.zeros((steps, len(s0)), dtype=np.uint8)
    for t in range(steps):
        field[t] = p1 ^ p2
        p1 = apply_rule(apply_rule(p1, a), b)
        p2 = apply_rule(apply_rule(p2, b), a)
    return field


def fit(field, radius):
    idx = np.zeros((field.shape[0] - 1, field.shape[1]), dtype=np.int64)
    for off in range(-radius, radius + 1):
        idx = (idx << 1) | np.roll(field[:-1], -off, axis=1).astype(np.int64)
    nxt = field[1:].astype(np.int64)
    half = idx.shape[0] // 2
    buckets = 1 << (2 * radius + 1)
    tr = np.bincount(idx[:half].ravel() * 2 + nxt[:half].ravel(),
                     minlength=buckets * 2).reshape(buckets, 2)
    rule = (tr[:, 1] > tr[:, 0]).astype(np.int64)
    seen = tr.sum(axis=1) > 0
    mb = int(nxt[:half].mean() > 0.5)
    pred = np.where(seen[idx[half:]], rule[idx[half:]], mb)
    return float((pred == nxt[half:]).mean()), rule, seen


def rule_map(rn, n):
    lut = rule_lut(rn)
    ints = np.arange(2 ** n, dtype=np.uint32)
    S = ((ints[:, None] >> np.arange(n, dtype=np.uint32)[None, :]) & 1).astype(np.uint8)
    out = lut[4 * np.roll(S, 1, axis=1) + 2 * S + np.roll(S, -1, axis=1)]
    pow2 = (1 << np.arange(n, dtype=np.uint64))
    return (out.astype(np.uint64) * pow2[None, :]).sum(axis=1).astype(np.uint32)


def shift_map(k, n):
    ints = np.arange(2 ** n, dtype=np.uint32)
    S = ((ints[:, None] >> np.arange(n, dtype=np.uint32)[None, :]) & 1).astype(np.uint8)
    S2 = np.roll(S, k, axis=1)
    pow2 = (1 << np.arange(n, dtype=np.uint64))
    return (S2.astype(np.uint64) * pow2[None, :]).sum(axis=1).astype(np.uint32)


def main() -> None:
    sweep = pd.read_parquet(ROOT / "results" / "sweep_full_classified.parquet")
    grp = sweep[sweep.regime == "structured"].sample(SAMPLE, random_state=5)
    rng = np.random.default_rng(4)

    rows = []
    for r in grp.to_dict("records"):
        a, b = int(r["rule_a"]), int(r["rule_b"])
        s0 = rng.integers(0, 2, N).astype(np.uint8)
        F = divergence_field(s0, a, b, STEPS)[BURN:]
        if F.mean() < 0.02 or (F[1:] ^ F[:-1]).mean() < 0.02:
            continue
        acc2, _, _ = fit(F, 2)
        acc1, rule1, seen1 = fit(F, 1)
        remainder = None
        if acc1 == 1.0 and seen1.sum() == 8:
            remainder = int(sum(int(rule1[i]) << i for i in range(8)))
        rows.append(dict(rule_a=a, rule_b=b, acc_r2=round(acc2, 4),
                         acc_r1=round(acc1, 4), remainder_rule=remainder))

    df = pd.DataFrame(rows)
    df.to_csv(ROOT / "results" / "remainder_rules.csv", index=False)
    live = len(df)
    exact2 = int((df.acc_r2 == 1.0).sum())
    elem = df[df.remainder_rule.notna()]
    print(f"live structured pairs: {live}; exactly closed at r2: {exact2} ({exact2/live:.0%}); "
          f"exactly elementary: {len(elem)}")
    print("remainder-rule histogram:", elem.remainder_rule.value_counts().to_dict())

    # mechanism, exhaustive at n=12
    maps = {}

    def M(rn):
        if rn not in maps:
            maps[rn] = rule_map(rn, N_EXACT)
        return maps[rn]

    shifts = {k: shift_map(k, N_EXACT) for k in range(N_EXACT)}
    full = (1 << N_EXACT) - 1

    galilean = 0
    eventual_shift = 0
    checked = 0
    for r in elem.to_dict("records"):
        a, b = int(r["rule_a"]), int(r["rule_b"])
        AB = M(a)[M(b)]
        BA = M(b)[M(a)]
        checked += 1
        if any(np.array_equal(AB, shifts[k][BA]) or np.array_equal(AB, shifts[k][BA] ^ full)
               for k in range(N_EXACT)):
            galilean += 1
        img = np.unique(BA)
        for _ in range(48):
            new = np.unique(BA[img])
            if len(new) == len(img) and np.array_equal(new, img):
                break
            img = new
        if any(np.array_equal(BA[img], shifts[k][img]) for k in range(N_EXACT)):
            eventual_shift += 1
    print(f"mechanism (n={N_EXACT} exhaustive) among {checked} shift-remainder pairs:")
    print(f"  algebraic Galilean identity (A.B == shift . B.A): {galilean}")
    print(f"  round map acts as pure shift on its eventual image: {eventual_shift}")


if __name__ == "__main__":
    main()
