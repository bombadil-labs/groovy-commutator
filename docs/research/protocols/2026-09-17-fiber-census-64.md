# Protocol: all 64 height-one fibers, and whether the phenotype fraction is additive in the exposed bits

**Status:** FROZEN before implementation and evaluation.
**Date:** 2026-09-17.
**Author:** Claude/Fable 5.1, Myk's session.
**Program:** Class-IV refinement, second unit.
**Protocol review:** none at freeze. Myk's 2026-09-17 suspension of the
cross-model review gates remains in force; this session runs, self-reviews
and merges. The results note must say evaluation preceded review.

## 1. Question

The [first census](2026-09-17-fiber-census.md) found that the height-one
base ECA predicts the persistence × spreading phenotype fraction of its
4096-rule fiber, with fiber(54) most enriched and fiber(204) least. Its
stated confound: the base rule is exactly its six exposed bits
(B0, B3, B6, S2, S5, S8), and those bits impose activity directly. "Does the
base carry more than its fixed bits" is therefore only well posed as:

> Is a fiber's phenotype fraction an **additive** function of the six
> exposed bits, or are interactions between the bits required?

If the bits act independently, "source-rule susceptibility" is a bit-count
story. If interactions carry the ordering, the base rule as a whole matters
on the quotient, which is a structural fact about the restriction map.

## 2. Family and sampling

All 64 reflection-symmetric ECAs, each with its 4096-rule fiber. For each
fiber, 128 rules sampled without replacement with a seed derived from
`("fiber-census-64-20260917", base)`. No exemplars are added: samples are
uniform. The five bases of the first census receive fresh samples under this
protocol's seed namespace, so their ordering is re-tested on independent
draws.

## 3. Contract

Identical to the first census, reusing its implementation: strip height 2,
width 521, density 0.5, burn 512, 256 scored transitions, six trajectory
seeds (four train, two test), 64 sites per seed, disturbance four base seeds
× eight origins at horizons 64 and 128, exact height-two predecessor
reference, `S* = max(0,R*)·max(0,M*)`, `alpha_x = log2(Dx(128)/Dx(64))`.
Seeds derive from `("fiber-census-64-20260917", base, rule, purpose,
replicate)`. Outcomes per rule: persist (`S* > 0`), spread (`alpha_x > 0.5`,
undefined counted as not spreading), both-positive (both). Exactness
control: eight rules per fiber must reproduce the base ECA byte-for-byte at
height one for 256 steps; any failure stops the run.

## 4. Frozen analysis

For each outcome, fit two logistic regressions across the 64 fibers, each
fiber contributing its 128 Bernoulli outcomes:

- **M1 (main effects):** intercept plus the six bits (7 parameters);
- **M2 (pairwise interactions):** M1 plus all 15 pairwise products
  (22 parameters).

Report the deviance of each, the likelihood-ratio statistic `2(ℓ₂ − ℓ₁)`
with a chi-square tail on 15 degrees of freedom, and the leave-one-fiber-out
mean predictive log-loss of both models (refit 64 times each). Fit by
iteratively reweighted least squares with a small ridge (1e-6) for
separability; report any fiber whose outcome is constant.

## 5. Frozen predictions

- **P1 (interactions needed, the bet):** for both-positive, the
  likelihood-ratio test has `p < 0.01` **and** M2's leave-one-fiber-out
  log-loss is lower than M1's. Failure means the phenotype fraction is
  additive in the exposed bits to within predictive accuracy, and the
  "base rule as a whole" reading is refuted for this family and contract.
- **P2 (the first census's ordering replicates):** on the fresh samples,
  both-positive fractions satisfy 54 > 22, 22 > 0, 0 > 90, 90 > 204 (all
  four).
- **P3 (the commutator of the base does not predict the fiber):** the
  median both-positive fraction over the eight affine bases
  {0, 51, 90, 105, 150, 165, 204, 255} lies inside the interquartile range
  of the other 56 fibers. Failure in either direction is informative: it
  would tie the fiber phenotype to the base's `G ≡ c` property.
- **P4 (descriptive, not scored):** the single bit with the largest
  main-effect coefficient for spreading is B3, and for persistence is S2.

## 6. Outputs

`results/fiber_census_64_20260917/`: `rows.json` (one row per rule),
`exactness_control.json`, `summary.json` (per-fiber fractions, both model
fits, LRT, leave-one-out losses, P1–P4, with a `source_hashes` block),
`fiber_census_64.svg` (both-positive fraction per fiber against the number
of fixed-on birth bits and survival bits). The summary is registered with
the fast integrity tier.

## 7. Budget and stopping

8,192 rules at about two seconds each, run as four worker processes over
fibers (deterministic per fiber, order-independent), expected about 1.2
hours wall, off GitHub Actions. If wall time exceeds four hours, reduce every
fiber uniformly to 64 rules, record the deviation before reading outcomes,
and rerun all fibers. No fiber may be dropped for its outcome.

## 8. Non-claims

Not a Class-IV definition; not the full plane; not a statement about
non-symmetric ECAs (empty fibers); not a mechanism. A positive P1 says the
six-bit quotient interacts, not why.
