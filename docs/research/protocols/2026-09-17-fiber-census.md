# Protocol: strip-height-one fibers as a refinement family for the 54/110 phenotype

**Status:** FROZEN before implementation and evaluation.
**Date:** 2026-09-17.
**Author:** Claude/Fable 5.1, Myk's session.
**Program:** Class-IV refinement (opened 2026-09-17).
**Protocol review:** none at freeze. Myk suspended the cross-model review gates
on 2026-09-17 (GPT has no GitHub access; no other collaborating agent is
available) and authorized this session to run, self-review and merge. Record
on the results note that evaluation preceded independent review.

## 1. Question

The 2026-09-17 strip restriction (GPT-5.6 Sol, cross-dimensional unit) makes
an exact refinement family available: on a periodic strip of height one, a
binary outer-totalistic Life-like rule `(B, S)` restricts to the elementary
rule

    r_1 = B0 + 18 B3 + 32 B6 + 4 S2 + 72 S5 + 128 S8,

so the fiber `Res_1^{-1}(r)` over a reflection-symmetric ECA `r` is exactly
the 4096 Life-like rules with those six bits fixed and the other twelve free.
At height two every one of the 18 bits is dynamical.

The refinement-depth conjecture in Myk's handoff asks whether a source rule's
ability to enter the selective-persistence × sustained-spreading regime is a
property of the source or a susceptibility of its refinement fiber. The
general form is not well posed (no definition of "source-faithful", and the
phenotype is observer-relative). This protocol asks the smallest well-posed
version:

> For a fixed observation contract (height-two periodic strips, the starred
> observables of the cross-dimensional unit), does the distribution of the
> phenotype over a rule's height-one fiber depend on the rule?

The fiber is a legitimate refinement family with no bolt-on freedom: every
member is outer-totalistic on the Moore neighbourhood, has the same alphabet,
and restricts exactly to the source at height one. Nothing can be "bolted on"
because there is nowhere to put it.

## 2. The trivial bolt-on lemma, recorded so it cannot contaminate the reading

For any CA `F` on `Z^d` and any CA `U` on `Z^k`, the product `F × U` on
`Z^{d+k}` (with `F` acting along the first `d` coordinates and `U` along the
rest, or more simply the coset-induced `F` with an independent `U` on a
disjoint set of layers) restricts exactly to `F` and has whatever ambient
behaviour `U` has. Hence "every source rule admits some higher-dimensional
extension with any desired ambient property" is true and empty. The only
questions worth asking are about restricted families, and this protocol's
family is restricted by the outer-totalistic constraint, not by a
description-length budget.

## 3. Bases and their fibers

Only reflection-symmetric ECAs have nonempty fibers; **rule 110 is not
reflection-symmetric and has an empty fiber**, which is itself a recorded
fact: refining 110 in this family is impossible, and any 110 refinement needs
an anisotropic family. The bases are:

| base ECA | fixed bits (B0,B3,B6,S2,S5,S8) | contains | role |
| --- | --- | --- | --- |
| 54 | (0,1,1,1,0,0) | HighLife B36/S23 | core positive base |
| 22 | (0,1,0,1,0,0) | Life B3/S23, B35/S236 | complex-and-explosive base |
| 90 | (0,1,0,0,1,0) | | additive base (G ≡ 0) |
| 204 | (0,0,0,1,1,1) | | identity base |
| 0 | (0,0,0,0,0,0) | | null base |

Each fiber has exactly 4096 rules. The census samples **512 rules per fiber**,
drawn uniformly without replacement from the fiber with seed derived from
SHA-256 of `("fiber-census-20260917", base)`. The named exemplars (HighLife,
Life, B35/S236) are added to their fibers' samples if not drawn, and flagged.

## 4. Fixed observation contract

Reused verbatim from `experiments/cross_dimensional_class4_20260917/strip_spectrum.py`
(the frozen starred observables), at strip height `k = 2`, width 521,
density 0.5, burn 512, score 256, six trajectory seeds (four train, two test
for `M*`), 64 sample sites per seed, disturbance four base seeds × eight
origins at horizons 64 and 128:

- `R*` selective visitation against the height-matched uniform predecessor
  reference (exact enumeration at `k = 2`);
- `M*` held-out eight-step centre-bit history gain;
- `S* = max(0, R*) · max(0, M*)`;
- `alpha_x = log2(Dx(128) / Dx(64))`, longitudinal support span.

Seeds derive from SHA-256 of `("fiber-census-20260917", base, rule, purpose,
replicate)`. No threshold is fitted. The region used for counting is fixed
now: **both-positive** means `S* > 0` (the clipped product's natural zero)
and `alpha_x > 0.5` (the inherited spreading gate from the ECA unit; not
tuned to 2D).

A `k = 4` secondary pass runs on a 64-rule subsample per fiber (first 64 of
the sampled order) with the same contract, reported descriptively.

## 5. Exactness control

For eight rules of each fiber sample, the height-one trajectory from a common
random row must be byte-identical to the base ECA's trajectory for 256 steps.
Any mismatch stops the run.

## 6. Frozen predictions

- **P1 (fibers differ).** The both-positive fraction is not the same across
  the five fibers: the largest and smallest fiber fractions differ by more
  than 0.10 and a Kruskal–Wallis test on `S*` across fibers has `p < 0.01`
  (descriptive; the 512-rule samples are not independent positives).
- **P2 (the bet).** Fiber(54) has a strictly higher both-positive fraction
  than fiber(0), fiber(204) and fiber(90). If it does not, "the source rule
  confers a susceptibility" is refuted for this family and contract.
- **P3 (exemplars are typical).** HighLife's `S*` lies between the 10th and
  90th percentile of fiber(54)'s `S*`, and Life's between those of
  fiber(22). Failure means the named exemplars are special within their
  fibers, which would be more interesting than success.
- **P4 (22 is bimodal).** Fiber(22) contains both Life (some spread, `S* = 0`
  at density 0.5 in the parent unit) and B35/S236 (ballistic, `S* ≈ 0`);
  the bet is that fiber(22)'s `alpha_x` distribution has at least 25% of
  rules above 0.9 and at least 25% below 0.5.

## 7. Outputs

`results/fiber_census_20260917/fiber_census_k2.json` (one row per sampled
rule: base, rule mask, rulestring, flagged exemplar, `R*`, `M*`, `S*`,
`Dx64`, `Dx128`, `alpha_x`, extinction fraction, counts), `fiber_census_k4.json`,
`exactness_control.json`, a per-fiber summary with the both-positive fraction
and quartiles, and one figure (`S*` versus `alpha_x`, one panel per fiber).
Save every file before reading any outcome.

## 8. Budget and stopping

Expected runtime about one to two hours off GitHub Actions; not run in CI. If
the `k = 2` pass exceeds four hours, reduce every fiber's sample uniformly to
256 rules, record the deviation before reading outcomes, and rerun all fibers
at the reduced budget. No rule may be dropped for its outcome. Unsupported
reference symbols follow the parent protocol's doubling schedule (only
possible at `k ≥ 4`; `k = 2` is exact).

## 9. Non-claims

Not a definition of Class IV; not a claim about the full plane; not a
statement about 110 (empty fiber); not a description-length result; not
novelty over the storage × spreading literature. A positive P2 shows that the
height-one quotient of a rule predicts something about the phenotype
distribution of its preimages under one contract. That is all.
