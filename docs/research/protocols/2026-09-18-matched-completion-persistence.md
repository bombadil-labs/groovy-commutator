# Protocol: matched completions decompose the persistence phenotype into what the base sets and what the completion sets

**Status:** FROZEN before implementation and evaluation.
**Date:** drafted 2026-09-17 for freeze on 2026-09-18.
**Author:** drafted by Claude/Fable 5.1 (planning session); to be reviewed,
amended and frozen by Claude Opus 5, who implements, runs and records the
unit. Myk's session. Amendments at freeze, both in §4: every prediction is
classified against the pilot, and P4 is scored on degrees-of-freedom-adjusted
variance components rather than raw eta-squared.
**Program:** Class-IV refinement, fourth unit.
**Protocol review:** none at freeze. Myk's 2026-09-17 suspension of the
cross-model review gates remains in force; the executing session runs,
self-reviews and merges. The results note must say evaluation preceded
review. Suspension is not authorization to skip the freeze: this draft is
amended and committed before `run.py` is written.

## 1. Purpose

The [handed fiber census](2026-09-17-handed-fiber-census.md) found that
the enrichment of fiber(110) lives on the **persistence** axis: fibers 22
and 30 spread more than 110's and persist far less. Persistence is the
conjunction `S* > 0`, that is `R* > 0` (selective retention of rare
rule-input symbols) **and** `M* > 0` (eight-step centre-bit history gain).
The two factors are different kinds of thing: `M*` transports exactly under
state conjugacy while `R*` is observer-relative
([strip spectrum](2026-09-17-strip-spectrum.md)). The census machinery,
which samples every fiber independently, cannot say which factor the base
sets and which the completion sets, because no two fibers share a member.

In the handed family `H` they can share a **completion**. The height-one
restriction is a coordinate projection onto the eight exposed table indices,
so a completion `u ∈ {0,1}²⁴` on the free indices is one object, and
`embed(r, u)` is a well-defined rule of `H` for **every** base `r`. Holding
`u` fixed and varying `r` isolates the base; holding `r` fixed and varying
`u` isolates the completion; driving every rule from the same seed stream
removes the ensemble as a source of difference. This unit runs that two-way
design at strip height two under the censuses' unchanged contract, with a
smaller arm at height four, and asks:

> (a) Which of `M*`, `R*` and `alpha_x` does the base set and which does the
> completion set, measured as variance fractions of a base × completion
> grid against a replicated noise floor?
> (b) For the same completion, does an observable's value **transfer**
> between bases, and does the transfer structure follow the base's own
> one-dimensional history gain?
> (c) Is the completion's effect additive in its 24 bits, or real but not
> bit-additive?
> (d) Does the base-level dissociation survive at strip height four?

The observer, contract and family are held fixed so every height-two number
is comparable with the three censuses. Only the **coupling** between rules
changes (shared completions, shared seeds); each rule's marginal
distribution is what it was.

What this unit is **not**: not a repeat census at height four (the height-
four arm tests one base-level statement, the paired 110-versus-30 `M*`
advantage, and the base ordering; it does not re-estimate fiber fractions);
not a search for the bit identity of enriched members (the pilot in §7
shows bit-additive models explain none of the within-fiber variance, and
P5 freezes that negative); not an observer change; not chirality (settled
negative); not a whole-census matched grid over all 256 bases (8,192
evaluations would buy only 32 completions per base, too few for transfer
correlations; it is the natural follow-up if P3's cluster structure holds).

## 2. Objects

### 2.1 Family, restriction, completions

`H`, its table index `i(c, w, n₇) = 16c + 8w + n₇`, the exposed indices
`E = {0, 3, 18, 21, 10, 13, 28, 31}` (window order `000 … 111`) and the
restriction `Res₁` are exactly as in the handed protocol §2.1–2.3, and
`run.py` imports the handed unit's `embed`, `res1`, `handed_step`,
`handed_batch_symbol` and `HandedRule` unchanged. The free indices `F` are
the 24 others in increasing order; a completion `u` is a 24-bit integer
whose bit `j` is placed at `F[j]`; `embed(r, u)` puts `r`'s eight bits at
`E` and `u`'s at `F`. Occupancy under uniform states at height two (pilot,
§7): ten free conditions are common (about 0.047 each: `c0w0n{2,4,5}`,
`c0w1n{3,4}`, `c1w0n{3,4}`, `c1w1n{2,3,5}`) and fourteen rare (about
0.015); this is descriptive context, not a covariate split.

### 2.2 Bases

`B = {110, 54, 22, 5, 30, 90, 0, 204}`, eight bases, roles: 110 the
headline; 54 the Life-like censuses' top fiber and the discriminator's
other core rule; 22 Life's base (spreading, small 1D `M`); **5** the
recovered discriminator's persistence-only control (1D `M = 0.98`,
`alpha = 0`), included so that `M*` inheritance can be told apart from
Class-IV-ness; 30 the non-symmetric Class-III comparator (1D `M ≈ 0`,
`alpha ≈ 1`); 90, 0, 204 the affine, null and identity anchors. Their
condition-P one-dimensional values (`R`, `M`, `S`, `alpha`), read from the
recovered table by orbit representative (each of the eight is its own
representative), are recorded in the output and asserted at run time to
match to three decimals: 110 (0.252, 0.903, 0.227, 0.766), 54 (0.343,
0.601, 0.206, 1.038), 22 (−0.143, 0.137, 0.000, 1.000), 5 (0.485, 0.976,
0.474, 0.000), 30 (−0.001, −0.000, 0.000, 1.000), 90 (0.000, −0.000,
0.000, 0.999), 0 and 204 (0.000, 0.000, 0.000, 0.000).

Not included, and why: 124 and every east-marked rule (its fiber lies in
the reflected family, where "the same completion" is a different object;
nothing is deducible from `H` beyond reflection, and chirality is settled);
137 (deduced identical to 110; used only inside the null-pair control).

### 2.3 Completions and seed streams

`N = 512` completions drawn uniformly from `{0,1}²⁴` without replacement,
in order, from `numpy.default_rng(seed)` with
`seed = SHA-256("matched-completion-20260918", "completions")` (the handed
unit's `seed()` with this protocol name). The grid is
`{embed(r, u) : r ∈ B, u ∈ U}`, 4,096 rules at height two.

Every seed used to drive a rule is keyed on the **completion and the
stream**, never on the table or the base:
`seed("events", stream, u, k, density, rep)` for trajectories and
`seed("spread", stream, u, k, density, rep)` for disturbances, with
`stream ∈ {"A", "B"}`. Hence for fixed `(u, k)` all eight bases start from
the same initial states, score the same sites, and disturb the same
origins. The Monte-Carlo reference at height four is likewise keyed
`seed("reference", u, k, n)`. This is a variance-reduction coupling; it
changes no rule's marginal distribution under the contract.

Tiers:

- **Main grid, stream A, height two:** all 8 × 512.
- **Replicate tier, stream B, height two:** the first 64 completions in
  sample order under all eight bases (512 rules). Same rules, independent
  seed stream: the test-retest noise floor.
- **Height-four arm, stream A:** the first 128 completions under all eight
  bases (1,024 rules).

### 2.4 Contract

Identical to the three censuses at height two, with the handed step and
nothing else changed: width 521, density 0.5, burn 512, 256 scored
transitions, six trajectory seeds (four train, two test), 64 sites per
seed, disturbance four base seeds × eight origins at horizons 64 and 128;
`R*` against the exact height-two uniform-predecessor reference (`2¹⁰`
patches through the handed rule, 18-symbol outer-totalistic observer),
`M*` the eight-step centre-bit history gain, `S* = max(0,R*)·max(0,M*)`,
`alpha_x = log2(Dx(128)/Dx(64))`. Outcomes: persist (`S* > 0`), spread
(`alpha_x > 0.5`, undefined counted as not spreading), both.

At height four the reference is Monte-Carlo, 100,000 patches, escalated to
200,000 / 400,000 / 800,000 while any trajectory symbol is unsupported,
exactly as the first census's `evaluate` does; a rule still unsupported at
800,000 has `R*` recorded as censored (`null`), counts as not persisting,
and is excluded pairwise from continuous analyses, with the count reported.
No threshold is fitted anywhere.

### 2.5 Exactness and covariance controls (run before any observable; any failure stops)

1. Exposed indices distinct; height two reaches all 32 conditions
   (asserted, as in the handed unit).
2. For eight completions of every base, `res1(embed(r, u)) = r` and the
   height-one trajectory from a random 521-cell row is byte-identical to
   the base ECA's for 256 steps.
3. **Matched null pair, the finding-4 form.** Conjugation sends index
   `i ↦ 31 − i` and flips the bit; on completions, `ū` has bit `j` equal to
   `1 − u`'s bit at the index `31 − F[j]`, and
   `conj(embed(110, u)) = embed(137, ū)` (asserted for every `u` used).
   For the first 16 completions, `embed(137, ū)` is evaluated under the
   full height-two contract from **complemented initial states on stream A
   keyed on the original `u`** (the same `seed("events", "A", u, …)` and
   `seed("spread", "A", u, …)` calls, the initial state complemented after
   drawing, sites and origins unchanged). Its `R*`, `M*`, `alpha_x` must
   equal `embed(110, u)`'s to `1e-9`, each observable compared and the
   maximum absolute difference recorded per pair. Keying the conjugate's
   stream on `ū` instead of `u` makes this an independently seeded
   comparison that rejects at the nominal rate; the pilot (§7) made exactly
   that mistake and the control must be written so it cannot be made: the
   seed key is passed in, never derived from the table.
4. Step covariance `handed_step(¬S, conj R) = ¬handed_step(S, R)` for those
   16 pairs on random states at heights 1, 2, 3, 5.
5. The eight condition-P rows named in §2.2 are the orbit representatives'
   rows of the recovered table (asserted by hash and by value).

## 3. Frozen analysis

All statistics below are computed by `evaluate.py`, committed before the
run, with the thresholds of §4; nothing is changed after any output is read.

- **Two-way decomposition** per observable `Y ∈ {M*, R*, alpha_x⁰}` on the
  8 × 512 stream-A grid, where `alpha_x⁰` is `alpha_x` with undefined
  values set to 0 (collapse between the horizons; count reported):
  `η²_base = Σ_{b,u} (Ȳ_b· − Ȳ)² / SST`, `η²_comp = Σ_{b,u} (Ȳ_·u − Ȳ)² / SST`,
  `η²_res = 1 − η²_base − η²_comp`. Noise floor from the replicate tier:
  `σ²_noise = mean over the 8 × 64 replicated cells of (Y_A − Y_B)² / 2`,
  reported as the fraction `σ²_noise / (SST / (8·512 − 1))`; the
  interaction fraction is `η²_res` minus that. Bootstrap over completions
  (2,000 resamples, seeded) gives 95% intervals for each fraction.
- **Test-retest reliability:** Pearson `r` between stream A and stream B
  per base per observable over the 64 replicated completions.
- **Transfer matrix:** for each observable, the 8 × 8 Spearman correlation
  of the same completion's value across bases over the 512 completions
  (complete-case pairwise for `R*` where censored; none expected at height
  two).
- **Paired comparisons** of 110 against each other base on `M*`, `R*`,
  `alpha_x`: sign fraction `P(Y_110,u > Y_b,u)`, mean paired difference,
  Wilcoxon signed-rank two-sided `p`; McNemar for paired persist, spread,
  both.
- **Persistence factorization** per base: fractions with `M* > 0`,
  `R* > 0`, both (`= persist`), spread, both-positive, with binomial SE;
  comparable with the handed census's 256-rule panel values for 110, 54,
  22, 30, 90, 0, 204.
- **Bit-additivity within base:** ridge regression (`λ = 1e-3`, intercept)
  of each observable on the 24 completion bits, 8-fold cross-validated
  `R²` with a fixed fold seed, per base; also the logistic analogue for
  persist and spread (IRLS, ridge `1e-6`, 8-fold log-loss against the
  intercept-only model).
- **Height-four arm:** the two-way decomposition on 8 × 128 (no replicate
  tier, so no noise split; `η²_base`, `η²_comp`, `η²_res` only); the paired
  110-versus-30 comparison; per-base mean `M*` ordering; Pearson `r`
  between a rule's height-two and height-four `M*`, `R*`, `alpha_x` per base
  (the same 128 rules appear in both arms); censoring counts.
- **Base-level join, descriptive:** the eight bases' 1D `M` and `R` against
  their grid-mean `M*` and `R*` (Spearman on 8 points; reported, not bet).

## 4. Frozen predictions

Odds are the drafting agent's, recorded so the scoring is honest.

**Standing of these predictions (added at freeze).** Every prediction below
was informed by the §7 pilot, which measured the same observables, in the
same bases, by the same code. The canonical completions are drawn from a
disjoint seed namespace and none of the pilot's sixteen are reused, so this
unit is a **pre-registered out-of-sample replication** of pilot observations,
not a set of blind bets. That is a legitimate and useful design — it is what
"survive being checked" asks for — but the results note must describe it as
replication and must not claim these as blind predictions. P3 is the most
strongly calibrated: its four thresholds were chosen to sit inside the
pilot's own uncertainty, so it tests reproducibility of a pilot pattern at
32× the sample size, nothing more. P1's 85% arm, P2's 0.40 gap and P5's 0.25
ceiling were likewise set from pilot values. The one quantity no pilot
estimated cleanly is P4's noise-corrected interaction fraction.

**Scoring of variance fractions (added at freeze).** The main grid has one
observation per cell, so a completion mean rests on 8 observations while a
base mean rests on 512. Raw `η²_comp` is therefore inflated relative to
`η²_base` by cell noise, mechanically and in a known direction: it favours
P4a and penalises P4b, which is exactly the prediction the drafting agent
expects to fail. Scoring P4 on raw `η²` would let P4b fail for an artifact.
**P4 is therefore scored on degrees-of-freedom-adjusted variance components**
from the two-way random-effects expected mean squares,
`σ²_base = (MS_base − MS_res)/512`, `σ²_comp = (MS_comp − MS_res)/8`, with
`MS_res` the residual mean square on `(8−1)(512−1)` degrees of freedom; a
component estimated below zero is reported as zero. The raw `η²` fractions
and the replicate-tier noise floor are reported alongside, and the note
states both.

- **P1 (the base sets `M*`, the completion sets `R*`, on the pair 110/30;
  the bet).** (a) `M*(110, u) > M*(30, u)` for at least 85% of the 512
  completions. (b) The paired `R*` difference is null: sign fraction in
  `[0.40, 0.60]` **and** `|mean paired difference| < 0.10`. Both arms must
  hold. Pilot (§7): 0.94 and 0.50 / −0.02 on 16 completions. Odds 0.75
  (the `R*` arm can fail on a small systematic shift that 512 pairs
  resolve).
- **P2 (dissociation in transfer).** Spearman transfer `r(110, 30)` for
  `R*` exceeds that for `M*` by at least 0.40. Pilot 0.83 against 0.10.
  Odds 0.80.
- **P3 (`M*` transfer follows the base's 1D history gain).** Four
  inequalities on the `M*` transfer row of 110: `r(110, 54) ≥ 0.60`,
  `r(110, 5) ≥ 0.50`, `r(110, 30) < 0.40`, `r(110, 0) < 0.40`. Pilot 0.81,
  0.74, 0.10, 0.22 on 16 completions, whose standard errors are about
  0.25, so the thresholds are inside the pilot's uncertainty. Odds 0.60 for
  all four together.
- **P4 (variance fractions; scored on `σ²` components per the note above).**
  (a) For `R*`, `σ²_comp > σ²_base`. Pilot
  0.37 against 0.12 over six bases (raw, uncorrected). Odds 0.80. (b) **For
  `M*`, `σ²_base > σ²_comp`. The drafting agent expects this to fail:** the pilot
  gave 0.28 against 0.38, because the completion's `M*` effect is shared
  within a cluster of high-`M` bases and within a cluster of low-`M` bases
  rather than across, so the completion main effect is large even though
  it does not transfer between clusters. Odds 0.35. A failure with P3
  holding is the informative outcome: `M*` would be a base-cluster ×
  completion interaction, not a base main effect.
- **P5 (the completion effect is real and not bit-additive).** In every
  base, test-retest `r ≥ 0.90` for `M*`, `R*` and `alpha_x` (pilot 0.95–1.00
  for 110 and 30), **and** the 24-bit ridge cross-validated `R² < 0.25` for
  every observable in every base (pilot maximum 0.18, `R*` in fiber 110 at
  `n = 256`; at `n = 512` an additive fit may sharpen). Odds 0.70; the
  `R*`-in-110 cell is the one at risk.
- **P6 (the base-level dissociation at height four).** On the 128-
  completion arm, `M*(110, u) > M*(30, u)` for at least 75% of completions
  with defined values, **and** 110 has the largest grid-mean `M*` of the
  eight bases at height four. Pilot on 8 completions: 0.62 sign fraction
  (mean difference +0.38), means 110 / 30 / 54 / 0 = 0.43 / 0.06 / 0.07 /
  0.01, with fiber(54)'s `M*` collapsing at height four although HighLife
  itself peaks there. Odds 0.50.

Descriptive, unscored: the full transfer matrices; `alpha_x` decomposition;
the persistence factorization against the handed census's values; the
height-two-to-four correlations; the base-level join.

## 5. Outputs

`results/matched_completion_20260918/`: `rows.json` (one row per
evaluation: base, completion, table, stream, height, tier, `R*`, `M*`,
`S*`, `Dx64`, `Dx128`, `alpha_x`, extinction fraction, reference mode and
samples, censoring flag, wall), `controls.json` (§2.5 controls 1–5 with
the sixteen null-pair maximum differences and the step-covariance results),
`summary.json` (decompositions with bootstrap intervals, reliability,
transfer matrices, paired tests, factorization, bit-additivity, height-four
arm, base join, P1–P6, `source_hashes` registered with the fast integrity
tier) and two figures: the three 8 × 8 transfer matrices at height two, and
paired `M*` and `R*` of 110 against 30 (512 points each). Runner
`experiments/matched_completion_20260918/run.py` (imports the handed unit's
family and step; a `sample_events`/`spread` pair that take the seed key as
an argument; the first census's height-four reference escalation) and
`evaluate.py`, both committed before the run.

## 6. Budget and stopping

Measured on this machine class with the handed step: 2.07 s per rule at
height two, 2.15 s at height four including Monte-Carlo references (the
first census's height-four pass averaged 2.13 s with escalations). Main
grid 4,096 × 2.07 = 8,480 s; replicate tier 512 × 2.07 = 1,060 s; height-
four arm 1,024 × 2.15 = 2,200 s plus escalations (allow 500 s); null pairs
32 × 2.07 = 66 s; controls under a minute. About 12,400 CPU-seconds, which
is **52 minutes** on four workers at the handed census's measured
parallel efficiency (3.95 effective cores), off GitHub Actions. Schedule
the main grid first, the height-four arm second, the replicate tier last;
no outcome is read before every tier is written. If wall time exceeds 80
minutes, reduce uniformly to 384 completions, 48 replicated, 96 at height
four, record the deviation before reading any outcome, and rerun
everything. No base or completion may be dropped for its outcome. Not run
in CI; the fast integrity tier checks the committed bytes.

## 7. Disclosed pre-freeze pilot

Throwaway scripts in the planning session's scratchpad (`persist/pilot1.py`
… `pilot4.py`, `eta.py`, `timing.py`, `occupancy.py`, `nullpair_debug.py`;
not part of the repository) established, on the handed census's existing
rows and on 132 fresh evaluations:

- On the handed census's twelve-rule tier over all 256 bases, the fiber
  median `M*` correlates with the base's 1D `M` at Spearman 0.61 and with
  its 1D `R` at 0.03; the fiber median `R*` correlates with the base's 1D
  `R` at 0.26. Within the 256-rule panel fibers, in fiber(110) every member
  has `M* > 0` (median 0.71) so persistence there equals `R* > 0` (0.629);
  fiber(30) has `R* > 0` at 0.586 and `M* > 0` at 0.477 (median 0.00).
  Ridge regression of any observable on the 24 free bits gives cross-
  validated `R² ≤ 0.18` in every panel fiber (most cells at or below 0).
- Sixteen completions from `default_rng(20260918)` (a different seed
  namespace from this protocol's) embedded under 110, 30, 54, 0, 5, 204,
  stream A keyed on the completion, height two, plus a second stream for
  110 and 30: test-retest `r` 0.995 / 0.945 (`M*`), 0.998 / 1.000 (`R*`),
  0.981 / 0.982 (`alpha_x`); transfer `r(110, 30)` 0.10 for `M*`, 0.83 for
  `R*`, 0.68 for `alpha_x`; the `M*` transfer matrix clusters {110, 54, 5}
  (0.72–0.81) apart from {30, 0, 204} (0.53–0.80); crude sum-of-squares
  fractions base / completion / rest 0.28 / 0.38 / 0.34 for `M*` and 0.12
  / 0.37 / 0.51 for `R*`. Eight completions under 110, 30, 54, 0 at height
  four gave the values quoted in P6; one height-four `R*` was censored
  because the pilot harness lacks the reference escalation.
- The matched null pair: four completions evaluated with the conjugate's
  stream keyed on the original `u` agree to `7.8e-16` or exactly; the same
  pairs keyed on `ū` (the first, wrong, attempt) differed by up to 0.14.

The pilot chose the bases, the design and the thresholds; its completions
are not reused; its numbers are quoted above as the origin of each bet and
nowhere as evidence.

## 8. Non-claims

Not a Class-IV definition; not the full plane; not a mechanism: a variance
fraction says where a quantity's variation lives on this grid, not why. Not
a statement about east-marked rules, other observers, other densities, or
strip heights other than two and four. Not a claim that `M*` is "the" Class-
IV coordinate: base 5 is in the design precisely because high `M*` is also
what periodic Class-II behaviour produces, and the conjunction with
spreading remains the phenotype. A positive P1–P3 shows that, in this
family under this contract, the eight exposed bits govern the history-gain
factor of persistence while the completion governs the retention factor,
for the bases named; a failure of P4b with P3 holding means the base acts
through an interaction with the completion rather than as a shift, which
is a sharper, not a weaker, statement of the same dependence.
