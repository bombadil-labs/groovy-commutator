# Protocol: a handed refinement family gives every ECA a fiber; the fiber of 110

**Status:** FROZEN before implementation and evaluation.
**Date:** 2026-09-17.
**Author:** drafted by Claude/Fable 5.1; reviewed, amended and frozen by
Claude Opus 5, who implements, runs and records the unit. Myk's session.
The amendments at freeze were: P2's ranking excludes the deduced duplicate
137; P1 and P2 carry an inline pointer to the disclosed pilot; the panel
size of fiber(137) is retained as load-bearing for P3's calibration rather
than trimmed.
**Program:** Class-IV refinement, third unit.
**Protocol review:** none at freeze. Myk's 2026-09-17 suspension of the
cross-model review gates remains in force; the executing session runs,
self-reviews and merges. The results note must say evaluation preceded
review.

## 1. Purpose

The two fiber censuses ([first](2026-09-17-fiber-census.md),
[64-fiber](2026-09-17-fiber-census-64.md)) used the Life-like family, whose
height-one restriction reaches only the 64 reflection-symmetric ECAs. Rule
110, the program's headline Class-IV rule and the discriminator's second
core rule, has no fiber there. This unit defines the smallest anisotropic
extension of the Life-like family for which the height-one restriction is a
coordinate projection onto **all 256** ECAs, verifies its exactness, and
repeats the census with three questions:

> (a) Does the fiber of 110 sit with the fiber of 54 at the enriched end of
> the persistence × spreading phenotype, or does the enrichment track the
> exposed bits' activity regardless of the base's own dynamics?
> (b) Does chirality matter: the family marks one horizontal direction, so
> the fiber of 110 and the fiber of its mirror 124 are different sets. Do
> they have different phenotype distributions?
> (c) Does a base's own one-dimensional phenotype (the recovered
> discriminator's `S` and `alpha`) predict its fiber's phenotype fractions?

The observation contract is held fixed (the 18-symbol outer-totalistic
observer of the earlier censuses). The candidate observer change (an
unstandardized surprisal gap) is deliberately not made here, so that fiber
fractions remain comparable across the two families; it is the next unit's
question, not this one's.

## 2. Objects

### 2.1 The handed family `H`

A rule in `H` is a function `f(c, w, n₇)` of the centre state `c`, the
**west** neighbour `w` (offset `(dx, dy) = (−1, 0)`), and the count `n₇` of
the other seven Moore neighbours (with multiplicity on periodic strips, as
`life_step` counts them). Table index `i(c, w, n₇) = 16c + 8w + n₇`, 32
entries, rule number `R = Σ f · 2^i` in `[0, 2³²)`. The Life-like family
embeds by `ι(B, S)(c, w, n₇) = [w + n₇ ∈ (S if c else B)]`; `ι` is
injective and `H` has `2³²` rules, of which `2¹⁸` are Life-like.

### 2.2 Height-one restriction

On a periodic strip of height one, the vertical neighbours of `(0, x)` are
`(0, x)` itself, the two north-west/south-west cells are `(0, x−1)` and the
three eastern cells are `(0, x+1)`, so `c = S[x]`, `w = S[x−1]`,
`n₇ = 2S[x−1] + 2S[x] + 3S[x+1]`. Hence

    Res₁(R): bit (4L + 2C + R) of the ECA = bit i(C, L, 2L + 2C + 3R) of R.

The eight exposed indices, in `(L, C, R)` order `000 … 111`, are
`{0, 3, 18, 21, 10, 13, 28, 31}`; they are distinct, so `Res₁` is a
coordinate projection: **onto all 256 ECAs, every fiber exactly `2²⁴`
rules**. `Res₁ ∘ ι` equals the Life-like formula
`B0 + 18 B3 + 32 B6 + 4 S2 + 72 S5 + 128 S8`.

### 2.3 Height two is faithful

Enumerating the 64 column triples of a height-two strip and both rows
reaches all 32 conditions `(c, w, n₇)`, so height two determines the rule:
the fiber is a genuine refinement family with no bolt-on freedom, as in the
Life-like case.

### 2.4 Symmetries

Complement conjugation `f ↦ ¬f(¬c, ¬w, 7 − n₇)` maps `H` to itself and
commutes with `Res₁` (fiber(`r̄`) is the conjugate of fiber(`r`)); every
observable below is exactly complement-covariant (symbol `z ↦ 17 − z`,
Jeffreys tables `p ↦ 1 − p`, XOR support unchanged), so **fiber(110) and
fiber(137) have identical phenotype distributions by deduction**: a null
pair. Reflection maps `H` to the east-marked family, not to itself, so
fiber(110) and fiber(124) are different subsets of `H` and their comparison
is empirical. Every `H` rule's mirror lies outside `H`; nothing about
east-marked rules is computed, because every statement about them follows
from `H` by reflection.

### 2.5 Exactness controls (run before any observable; any failure stops)

1. The eight exposed indices are distinct (asserted).
2. Height-two reachability of all 32 conditions (asserted by enumeration).
3. `Res₁ ∘ ι` equals the Life-like height-one formula for all `2¹⁸` rules.
4. `ι(HighLife)` under the handed step equals HighLife under `life_step`
   for 256 steps at heights 1, 2, 3 from a common random state; the handed
   successor-symbol routine agrees with the Life-like one on 5,000 random
   height-two patches.
5. For eight sampled rules of **every** fiber, the ECA derived from the
   eight `1×3` windows equals the base, and the height-one trajectory from a
   random 521-cell row is byte-identical to the base ECA's for 256 steps.
6. Complement covariance: eight rules of fiber(110), evaluated under the
   full contract, and their conjugates in fiber(137) evaluated from
   complemented initial states with the same seeds, give identical `R*`,
   `M*`, `alpha_x` to `1e-9`.

### 2.6 Sampling

Uniform members of a fiber are drawn by fixing the eight exposed bits and
drawing the 24 free bits uniformly, rejecting duplicates; seed from SHA-256
of `("handed-fiber-census-20260917", "sample", base)`. Two tiers:

- **Whole census:** every one of the 256 ECAs, 12 rules per fiber
  (3,072 rules).
- **Panel:** bases `{110, 124, 137, 54, 22, 30, 90, 0, 204}` raised to 256
  rules per fiber (244 additional each, 2,196 rules); fiber(137) is held at
  the full 256 rather than trimmed, because P3 is not scorable without its
  empirical null-pair calibration; the whole-census rows
  are the first twelve of each panel fiber's sample order. Roles: 110
  headline; 124 its mirror (chirality); 137 its complement conjugate (null
  pair); 54 and 22 the Life-like censuses' top two; 30 a non-symmetric
  Class-III control matched to 110 in being non-symmetric; 90, 0, 204 the
  earlier censuses' affine, null and identity anchors.
- **Exemplars:** `ι(HighLife)` and `ι(Life)` are added to fibers 54 and 22
  and flagged; no exemplar exists for 110 (no named handed rule).

### 2.7 Contract

Identical to the earlier censuses, with the handed step substituted for the
Life-like step and nothing else changed: strip height 2, width 521, density
0.5, burn 512, 256 scored transitions, six trajectory seeds (four train, two
test), 64 sites per seed, disturbance four base seeds × eight origins at
horizons 64 and 128; `R*` against the exact height-two uniform-predecessor
reference (`2¹⁰` patches pushed through the handed rule, read by the
18-symbol outer-totalistic observer), `M*` the eight-step centre-bit history
gain, `S* = max(0, R*)·max(0, M*)`, `alpha_x = log2(Dx(128)/Dx(64))`.
Outcomes per rule: persist (`S* > 0`), spread (`alpha_x > 0.5`, undefined
counted as not spreading), both. Seeds derive from SHA-256 of
`("handed-fiber-census-20260917", base, rule, purpose, replicate)`.

## 3. Frozen analysis

- Per-fiber fractions of persist, spread and both, with binomial standard
  errors; panel fibers at `n = 256` (257 with an exemplar).
- Named panel comparisons by two-sided two-proportion z-tests (pooled
  variance) on the both-positive and spread fractions.
- Whole census: for each outcome, logistic regressions across the 256
  fibers with the base's eight truth-table bits as covariates, M1 (intercept
  plus eight bits, 9 parameters) and M2 (M1 plus 28 pairwise products, 37
  parameters), IRLS with ridge `1e-6`; deviances, LRT on 28 degrees of
  freedom, leave-one-fiber-out mean log-loss (256 refits each).
- Base-phenotype join: each ECA maps to the smallest rule number in its
  reflection-and-complement orbit; those 88 representatives are exactly the
  radius-one rows of the recovered discriminator's condition-P table
  (`experiments/class4_selective_persistence_20260916/evidence/…all_conditions…csv`,
  width 2053, density 0.5), asserted at run time. Fiber-level fractions
  (12-rule tier) are compared between bases whose representative has
  `alpha > 0.5` (15 orbits) and the rest, and between bases with `S > 0`
  (17 orbits) and the rest, by one-sided Mann–Whitney U. Fibers are not
  independent (complement pairs share a distribution); p-values are
  descriptive, as in the earlier censuses.
- Descriptive, unscored: pooled fractions over the 64 symmetric bases'
  `H`-fibers against the Life-like 64-census pooled values (persist 0.468,
  spread 0.421, both 0.230); Spearman of fiber fractions against the
  forced-table invariants `|T_r|`, `h₂`, `h₃`
  (`results/forced_tables_20260917/invariants.json`); the exemplars' values
  against their Life-like census values.

## 4. Frozen predictions

- **P1 (110 is enriched, the bet):** fiber(110)'s both-positive fraction
  strictly exceeds each of fiber(0), fiber(90), fiber(204) and fiber(30).
  The comparison with 30 carries the risk: 110 fixes three survival
  conditions on and 30 only two, and the 64-census found survivals lower
  the fraction. Failure against 30 alone means the enrichment tracks
  exposed-bit activity, not the base's own class. **Contamination notice:**
  the §7 pilot observed one member of fiber(110) under the full contract and
  it was both-positive (`S* = 0.28`, `alpha_x = 0.75`). That is one draw of
  the 256 this unit will take, weak but not nil, and it bears on P1 and P2
  specifically. Any report that P1 or P2 held states this alongside the
  result.
- **P2 (110 joins 54 at the top; unsure):** fiber(110) ranks first or
  second by both-positive fraction among the **eight** panel bases other
  than 137. Fiber(137) is excluded from the ranking because §2.4 deduces
  that it has fiber(110)'s distribution, so its presence would let P2 be
  satisfied by 110's own conjugate; the eight-base ranking is the
  scientific statement. Fiber(22) was second in both Life-like censuses and
  fiber(30) is untested; even odds.
- **P3 (chirality matters, direction predicted; the prediction most likely
  to fail):** fiber(110) has a strictly higher spread fraction than
  fiber(124), with two-proportion `p < 0.05`. Rationale: the two fibers
  differ only in swapping the fixed values at `(c=0, w=0, n₇=3)` and
  `(c=0, w=1, n₇=2)`, conditions of multiplicity 35 and 21 among the 256
  Moore neighbourhoods, so fiber(110) fixes birth on 35 and off 21 and
  fiber(124) the reverse. The effect may be real but below detection at
  `n = 256`; a null outcome is scored as a failure. **Calibration (must
  hold):** the null pair fiber(110), fiber(137) does not reject at
  `p < 0.05` on either the spread or the both-positive fraction; a
  rejection there flags the implementation or seeds, not science, and
  P3 is then not scorable until it is resolved.
- **P4 (the symmetric ordering survives the change of family):** among the
  panel, `54 > 22`, `22 > max(0, 90)` and `min(0, 90) > 204` in
  both-positive fraction (three inequalities; 0 versus 90 is not bet, the
  64-census could not resolve it).
- **P5 (the base's 1D phenotype predicts its fiber):** (a) fibers whose
  base representative has 1D `alpha > 0.5` have higher spread fractions than
  the rest, Mann–Whitney one-sided `p < 0.01`; (b) fibers whose base has 1D
  `S > 0` have higher persist fractions than the rest, `p < 0.01`. The
  author expects (a) to hold and (b) to fail: persistence in the Life-like
  census was bought by birth-on-zero, a 2D activity effect with no evident
  1D counterpart.
- **P6 (non-additivity replicates in eight bits):** for the spread outcome,
  the LRT has `p < 0.01` **and** M2's leave-one-fiber-out log-loss is below
  M1's. Failure would mean the 64-census's interaction finding was specific
  to the outer-totalistic family.

## 5. Outputs

`results/handed_fiber_census_20260917/`: `rows.json` (one row per rule:
base, 32-bit rule, tier, exemplar flag, `R*`, `M*`, `S*`, `Dx64`, `Dx128`,
`alpha_x`, extinction fraction, counts, wall), `exactness_control.json`
(controls 1–6 with the complement-covariance values), `summary.json`
(per-fiber fractions with SE, panel tests, both model fits, the
base-phenotype join, descriptive joins, P1–P6, with a `source_hashes`
block registered with the fast integrity tier), and two figures: `S*`
against `alpha_x` for the nine panel fibers, and the 256 fiber both-positive
fractions against the base's 1D `alpha` with the panel bases labelled.
Runner `experiments/handed_fiber_census_20260917/run.py` (family, controls,
sampling, measurement; imports the cross-dimensional harness for the
observer, `selective_r`, `predictive_gain`, `xdiam`) and `evaluate.py`
(frozen analysis), both committed before the run; the evaluator's
thresholds are those above and are not to be changed after any output is
read.

## 6. Budget and stopping

5,268 rules at 1.83 s each single-core (measured on the harness with the
handed step; the same as the Life-like step), four worker processes over
fibers with the nine panel fibers scheduled first, expected about 40
minutes wall off GitHub Actions (the 64-census ran 8,192 rules in 65
minutes on the same machine class). Exactness controls add under a minute.
If wall time exceeds 90 minutes, reduce the whole-census tier uniformly to
8 rules per fiber and the panel to 192, record the deviation before reading
any outcome, and rerun everything. No fiber may be dropped for its outcome.
Not run in CI; the fast integrity tier checks the committed bytes.

## 7. Disclosed pre-freeze pilot

Before this draft was written, a throwaway script
(`scratchpad/handed/verify_handed.py`, not part of the repository)
established the exact facts of §2 and timed the harness on `ι(HighLife)`
(`S* = 0.135`, `alpha_x = 1.04`, against the Life-like census's 0.125 and
0.98 on other seeds) and on one member of fiber(110) (`S* = 0.28`,
`alpha_x = 0.75`), then evaluated 16 uniformly random rules of `H` under the
full contract, from no chosen fiber: persist 0.50, spread 0.56, both 0.19.
That pilot shows the family is not degenerate under the contract. It
informed nothing in P1–P6 except the decision that a census was worth
running; it did inform the decision to keep the family-level comparison
descriptive rather than bet.

## 8. Non-claims

Not a Class-IV definition; not the full plane; not a statement about
east-marked rules beyond what reflection deduces; not a mechanism for any
enrichment; not a claim that `H` is the natural or unique anisotropic
family (it is the smallest extension of the Life-like family whose
height-one restriction is onto, and one of several such); not a comparison
across observers, since the observer is held fixed and is itself
reflection-symmetric while the family is not. A positive P1 shows that in
this family, under this contract, the height-one quotient at 110 predicts
enrichment of its preimages; nothing more.
