"""The U-engine slice: single-rule engine commutators, read out of the pair sweep.

The U construction (from the gallery-vs-engine discussion): for a single rule
phi, run the two composites E.D and D.E as ENGINES -- each iterated on its own
output -- from the same initial state, and XOR the trajectories:

    P_0 = Q_0 = S_0
    P_{t+1} = E(D(P_t))        Q_{t+1} = D(E(Q_t))
    U_t = P_t XOR Q_t          (U_1 = G(S_0), the one-step commutator)

Key identity that makes this free: D(S) = S XOR phi(S) is itself the
elementary rule phi ^ 204 (the prehoc collapse identity, established result 7).
So P and Q are exactly the two paths of divergence_trajectory(phi ^ 204, phi),
and the full 32,640-pair sweep (established result 4) already classified every
such pair. This script just looks up the 128 pairs {phi, phi ^ 204} and emits
one row per rule.

Findings (verified from results/sweep_full_classified.parquet):
  - Per-rule U regimes: structured 106, drain 58, crystalline 56, noisy 26,
    commute 10. U is non-degenerate and spans the full regime vocabulary.
  - Commute set = the 8 linear rules {0, 60, 90, 102, 150, 170, 204, 240}
    plus nonlinear surprises {4, 200}. One-line proof for the linear part:
    D = I xor E, so for linear E,  E.D = E xor E^2 = D.E identically --
    a linear map commutes with any polynomial in itself.
  - The 8 biased-affine rules {15, 51, 85, 105, 153, 165, 195, 255} are all
    crystalline at mean disagreement 0.99: the constant nonzero commutator
    (affine theorem, established result 1) compounds under the engine stance
    into a frozen near-complement offset.

NOT tested here: whether U_t itself follows a local rule R(E.D, D.E) --
that is the follow-up experiment, deliberately not claimed.

Output: results/u_engine_slice.csv (one row per rule phi 0..255).
"""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SWEEP = ROOT / "results" / "sweep_full_classified.parquet"
OUT = ROOT / "results" / "u_engine_slice.csv"

LINEAR_RULES = {0, 60, 90, 102, 150, 170, 204, 240}
BIASED_AFFINE_RULES = {15, 51, 85, 105, 153, 165, 195, 255}


def main() -> None:
    df = pd.read_parquet(SWEEP)
    # Index by unordered pair for O(1) lookup.
    keyed = {}
    for row in df.itertuples(index=False):
        keyed[(min(row.rule_a, row.rule_b), max(row.rule_a, row.rule_b))] = row

    rows = []
    for phi in range(256):
        d_rule = phi ^ 204
        pair = keyed[(min(phi, d_rule), max(phi, d_rule))]
        rows.append(
            {
                "phi": phi,
                "d_rule": d_rule,
                "regime": pair.regime,
                "mean_disagree": pair.mean,
                "final": pair.final,
                "peak": pair.peak,
                "compressibility": pair.compressibility,
                "linear": phi in LINEAR_RULES,
                "biased_affine": phi in BIASED_AFFINE_RULES,
            }
        )
    out = pd.DataFrame(rows)
    out.to_csv(OUT, index=False)

    counts = out.regime.value_counts()
    print("per-rule U regimes:", counts.to_dict())
    commuters = set(out[out.regime == "commute"].phi)
    assert LINEAR_RULES <= commuters, "every linear rule must commute with its D"
    print("commute set:", sorted(commuters))
    affine_regimes = set(out[out.biased_affine].regime)
    assert affine_regimes == {"crystalline"}, affine_regimes
    print("biased-affine rules all crystalline, mean disagreement:",
          sorted(out[out.biased_affine].mean_disagree.round(3).unique()))
    print(f"wrote {OUT.relative_to(ROOT)} ({len(out)} rows)")


if __name__ == "__main__":
    main()
