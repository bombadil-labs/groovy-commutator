# Protocol: the invariant beam mediates history-gain transfer between bases

**Status:** FROZEN before implementation and evaluation.
**Date:** drafted 2026-09-18.
**Author:** drafted by Claude/Fable 5.1 (planning session); reviewed, amended
and frozen by Claude Opus 5, who implements, runs and records the unit.

**Independent verification at freeze (Opus 5).** The beam theorem was
re-derived from scratch rather than taken on report, and confirmed
numerically. On a height-two strip the vertical wrap sends both off-rows to
the other row, so a state with equal rows has Moore count `3L + 2C + 3R` and
west neighbour `L`; hence `n₇ = 2L + 2C + 3R` and the condition index is
`16C + 8L + (2L + 2C + 3R)`, which is **exactly** the height-one exposed
index for the window `(L, C, R)`. Every cell on the beam therefore reads an
exposed entry, the strip acts as the base ECA, and equal rows stay equal.
Checked for 16 bases × 6 completions × 200 steps: invariance exact, and the
top row equal to the base ECA's orbit at every step. The mediation sign
structure was also reproduced on an independent 96-completion subsample:
`agree` transfers between 110 and 30 at +0.79 while the within-base response
is +0.76 (110), −0.83 (30), +0.63 (5), −0.74 (90), with raw `M*` transfer
−0.48. A shared mediator with opposite-signed responses is the anticorrelation.
**The theorem stands independently of how P1–P7 score** and is promoted as an
established result on that basis, not on the strength of the replication.

**Amendments at freeze (Opus 5), all in §4:** P7's third arm is demoted to
descriptive; P2(a) keeps its strict all-pairs form as the bet and gains a
companion relaxed form so that a single-pair failure still carries
information; P1(d) is marked as the least-calibrated arm.

Original drafting line: drafted by Claude/Fable 5.1; to be reviewed,
amended and frozen by Claude Opus 5, who implements, runs and records the
unit. Myk's session.
**Program:** Class-IV refinement, fifth unit.
**Protocol review:** none at freeze. Myk's 2026-09-17 suspension of the
cross-model review gates remains in force; the executing session runs,
self-reviews and merges. The results note must say evaluation preceded
review. Suspension is not authorization to skip the freeze: this draft is
amended and committed before `run.py` is written.

**Standing.** Every prediction below is calibrated on a reanalysis of the
[matched-completion unit's](2026-09-18-matched-completion-persistence.md)
canonical rows and on a 400-evaluation pilot (§7), and each says so. The
canonical completions are drawn from a disjoint seed namespace. This unit is
therefore a **pre-registered out-of-sample replication of a mechanism read
off existing data**, and is reported as one; P4 is the one prediction the
drafting agent expects to fail, and its failure is the informative outcome.

## 1. Purpose

The matched-completion unit found that history gain `M*` **anticorrelates**
between distant bases: the same completion that raises rule 110's history
gain lowers rule 30's (Spearman −0.414), while it transfers positively within
{110, 54, 5, 22} and within {30, 90}. That note called it the first question
in the Program whose answer would be a mechanism rather than a distribution.

The mechanism proposed here is exact in its first step and empirical in its
second.

**Exact.** At strip height two the set of states whose two rows are equal is
invariant under every rule of the handed family: with rows equal, every cell's
condition `(c, w, n₇)` is an exposed index, so both rows step by the base ECA
and remain equal. Call this set the **beam**. On the beam the strip *is* the
base rule, and the height-two history gain equals the one-dimensional history
gain of the base up to sampling.

**Empirical (the claim under test).** Whether a trajectory driven from random
initial rows ends up on the beam is decided by the completion, roughly the
same way for every base: the beam is either transversally attracting under
`embed(r, u)` for most bases `r` or repelling for most. Beam proximity is thus
a **completion-set mediator**. A base's history gain is then a mixture: its
own one-dimensional `M` on the beam, and a completion-set, roughly
base-indifferent value (about 0.2 bits at height two) off it. Bases whose 1D
`M` exceeds the off-beam value gain from the beam (110, 54, 5, 29, 62, 33);
bases whose 1D `M` is zero lose (30, 90, 106, 45; also 232); bases whose 1D
`M` is close to the off-beam value do not respond (22 weakly positive, 18
null). **The sign of transfer between two bases is the product of the signs
of their responses to the mediator**, and the anticorrelation is what a shared
mediator with opposite-signed responses looks like. Conditioning on the
mediator should remove it.

The mediator has a structural, separately measurable form: the **transverse
stability of the beam**, the fate of a single row-disagreement seeded on a
beam state, measured on beam states with their own seed stream and never on
the trajectory that yields `M*`. That is what makes this a mechanism rather
than a correlation between two statistics of one trajectory.

Questions:

> (a) On fresh completions, does conditioning on beam proximity, and on
> transverse beam stability, remove the 110/30 anticorrelation?
> (b) Is beam proximity a completion property, transferring positively
> between every pair of a 16-base panel?
> (c) Does each base's response to beam proximity follow its one-dimensional
> history gain, on eight bases not used to find the mechanism?
> (d) Is the on-beam history gain the base's one-dimensional value, and the
> off-beam value base-indifferent?
> (e) Is the mechanism specific to history gain (retention unmediated), and
> does it persist at height three?

What this unit is **not**: not a transfer-sign map over more pairs for its
own sake (the pilot already shows the sign is not a function of the two
bases' 1D `M` alone: 0 and 204 have `M = 0` like 30 and 90 but transfer at
+0.06 with 110, not −0.4; the map is explained, not extended); not a search
for which completion bits set beam stability (pilot: beam proximity and
transverse stability are as non-bit-additive as `M*`, ridge cross-validated
`R² ≤ 0.06` in every base, so the non-additivity lives in the mediator and a
bit model is the wrong instrument); not a height-four unit (the canonical
height-four arm already shows beam proximity does not transfer there, +0.03
for 110/30, and off-beam `M*` is ≈ 0 for every base, which removes both
ingredients; recorded descriptively in §7, not bet); not a claim about the
full plane, other observers or other densities.

## 2. Objects

### 2.1 Family, restriction, completions, contract

`H`, `E`, `F`, `embed`, `res1`, the handed step and the height-two contract
are exactly the matched-completion unit's (its §2.1, §2.4); `run.py` imports
that unit's `embed`, `bits_of`, `_initial`, `sample_events_keyed`,
`spread_keyed`, `evaluate`, `conj_table` unchanged, except that
`sample_events_keyed` also returns beam proximity (§2.4). Width 521, density
0.5, burn 512, 256 scored transitions, six event seeds, 64 sites, the exact
height-two reference, `R*`, `M*`, `S*`, `alpha_x` as before.

`N = 256` fresh completions from `numpy.default_rng(seed("completions"))`
with `seed` keyed on this protocol's name `beam-mechanism-20260918`, drawn
without replacement in order; asserted disjoint from the matched unit's 512
and from the §7 pilot's sixteen height-three completions. Seeds for
trajectories and disturbances are keyed on `(stream, u, k, density, rep)` as
before, never on the base or table.

### 2.2 Bases

Sixteen. The matched unit's eight, `{110, 54, 22, 5, 30, 90, 0, 204}`, on
which the mechanism was read off, and **eight new bases** chosen in the §7
pilot to spread one-dimensional history gain across the mechanism's regimes,
by orbit representative in the recovered condition-P table (`M`, `alpha`):

| new base | 1D `M` | 1D `alpha` | regime |
| --- | ---: | ---: | --- |
| 106 | 0.000 | 0.99 | chaotic, zero history gain |
| 232 | 0.000 | 0.00 | frozen (majority) |
| 8 | 0.000 | 0.00 | frozen |
| 18 | 0.164 | 1.00 | chaotic with history gain near the off-beam value |
| 46 | 0.374 | 0.00 | intermediate |
| 33 | 0.563 | 0.00 | periodic, mid history gain |
| 62 | 0.765 | 0.40 | high history gain, spreading |
| 29 | 0.954 | 0.00 | high history gain, no spreading |

Their condition-P rows are asserted at run time as in the matched unit
(`R, M, S, alpha` to three decimals): 106 (−0.000, −0.000, 0.000, 0.989),
232 (−0.314, 0.000, 0.000, 0.000), 8 (−0.585, 0.000, 0.000, 0.000),
18 (−0.027, 0.164, 0.000, 1.002), 46 (−0.240, 0.374, 0.000, 0.000),
33 (0.083, 0.563, 0.047, 0.000), 62 (0.775, 0.765, 0.593, 0.396),
29 (0.100, 0.954, 0.095, 0.000). Rule 45 was piloted and dropped only for
budget (it duplicates 30/90/106's regime; pilot `rho = −0.52`).

### 2.3 Tiers

- **Main tier, stream A, height two:** 16 bases × 256 completions (4,096
  rules), each evaluation recording beam proximity.
- **Transverse tier:** for every rule of the main tier, transverse beam
  stability (§2.5), 4,096 measurements.
- **Height-three arm, stream A:** the first 48 completions under the eight
  original bases (384 rules), exact reference (`2¹⁵` patches), beam proximity
  as the fraction of columns where all three rows agree.

### 2.4 Beam proximity (recorded inside the evaluation)

For each event seed, at each of the 7 + 256 steps after burn-in, the fraction
of columns whose rows are all equal; `agree` is its mean over steps and the
six seeds. It is computed in the same loop that samples events, so it is a
statistic of exactly the trajectory that yields `M*`. Derived: `on_beam`
(`agree > 0.98`), `off_beam` (`agree < 0.5`), `mid` otherwise.

### 2.5 Transverse beam stability (measured on the beam, separate seeds)

For each rule `embed(r, u)` and `rep ∈ {0..3}`: draw a random row from
`default_rng(seed("transverse", u, rep))` at density 0.5, evolve it 256 steps
under the **base ECA** `r` (a beam state), form the two-row strip with equal
rows, and for each of eight origins from the same generator flip one cell of
row 1. Follow the strip 128 steps under `embed(r, u)`; record the number of
columns where the rows differ at steps 64 and 128. Report `T64`, `T128`
(means over 32 trials) and `T_ext` (fraction of trials with zero
disagreement at step 128). The seed is keyed on the completion, never on the
table, so the conjugate control below is matched.

### 2.6 Controls (before any observable; any failure stops)

1. Exposed indices distinct; height two reaches all 32 conditions; height
   three reaches all 32 (asserted).
2. **Beam invariance, exact:** for eight completions of every base, a random
   row `x`, the strip `(x, x)` stepped 256 times under `embed(r, u)` keeps its
   rows equal and equals the base ECA's trajectory of `x` at every step; the
   same at height three with `(x, x, x)`.
3. Fresh completions disjoint from the matched unit's 512 (asserted on the
   sets).
4. **Matched null pair, the finding-4 form:** for the first eight fresh
   completions, `embed(137, ū)` evaluated from complemented initial states on
   stream A keyed on the original `u`, and its transverse tier from the
   complemented beam state keyed on the original `u` (the base ECA 137 applied
   to `¬x` is `¬` of 110 applied to `x`, so the beam states are conjugate);
   `R*`, `M*`, `alpha_x`, `agree`, `T64`, `T128`, `T_ext` must each agree to
   `1e-9`. The seed key is passed as an argument, never derived from the table.
5. Step covariance at heights 1, 2, 3, 5 for those eight pairs, as before.
6. The sixteen condition-P rows asserted by value.

## 3. Frozen analysis

All statistics computed by `evaluate.py`, committed before the run.

- **Transfer matrices** (16 × 16 Spearman over the 256 completions) for
  `M*`, `R*`, `alpha_x⁰`, `agree`, `T_ext`, `log(1 + T128)`.
- **Partial transfer:** for every pair `(a, b)` and observable `Y`, the
  rank-partial Spearman of `Y_a` and `Y_b` given `(agree_a, agree_b)`
  (residualize ranks on ranks, then Pearson), and given
  `(T_ext_a, T_ext_b)`. Also given the **leave-two-out completion beam
  score**, the mean of `agree` over the other fourteen bases.
- **Response per base:** `rho_b = Spearman(M*_b, agree_b)` and
  `Spearman(M*_b, T_ext_b)`; band medians of `M*` on-beam, mid and off-beam
  with counts; the base-level join of `rho_b` against the 1D `M` (Spearman on
  16 points) and against the on-minus-off band difference.
- **Sign accounting:** over the 120 pairs, agreement between `sign r_M(a, b)`
  and `sign(rho_a · rho_b)` among pairs with both `|rho| ≥ 0.3`.
- **Mediator gating:** per base, `P(on_beam | T_ext ≥ 0.9)` and
  `P(on_beam | T_ext < 0.5)`.
- **Height three:** the same matrices and partials on 8 × 48; per-base
  on-beam fraction at heights two and three on the same 48 completions.
- **Bootstrap** over completions (2,000 resamples, seeded) for every
  threshold statistic in §4; intervals reported, verdicts on point values.

## 4. Frozen predictions

Odds are the drafting agent's. Each prediction states its calibration.

- **P1 (the anticorrelation replicates and the mediator removes it; the
  bet).** On the 256 fresh completions: (a) `r_M(110, 30) ≤ −0.25`;
  (b) the partial given `(agree_110, agree_30)` is `≥ −0.05`; (c) the partial
  given `(T_ext_110, T_ext_30)` is `≥ −0.05`; (d) the partial given the
  leave-two-out beam score is `≥ −0.15`. All four. *Pilot-calibrated:*
  −0.414 (512) and −0.29 (64 replicate); +0.159; +0.116; −0.097 (six-base
  score). Odds 0.85. **(d) is the least-calibrated arm in this protocol:**
  its threshold rests on a six-base score never piloted at sixteen, so a
  failure confined to (d) is read as a mis-set threshold rather than as
  evidence against the mechanism, and is reported that way.
- **P2 (beam proximity is a completion property).** (a) `agree` transfers at
  Spearman `≥ 0.25` for **every** one of the 120 pairs; (b) `T_ext` transfers
  at `≥ 0.40` for every pair among the twelve non-frozen bases (all but 0,
  204, 8, 232). *Pilot-calibrated:* (a) minimum 0.42 over the 28 original
  pairs, minimum 0.46 for new bases against 110 on 32 completions; (b)
  minimum 0.72 among the original non-frozen bases; 110/0 is 0.25, hence the
  exclusion. Odds 0.60; the frozen bases are the risk in (a).
  **Companion P2(a′), scored alongside:** `agree` transfers at `≥ 0.25` on at
  least 95% of the 120 pairs **and** at `≥ 0.10` on every pair. An all-pairs
  minimum can fail on one frozen-frozen pair for an uninteresting reason;
  scoring both forms distinguishes "the mediator is universal" from "the
  mediator is near-universal with frozen-base exceptions", which the strict
  form alone would collapse into a bare failure.
- **P3 (the response follows one-dimensional history gain, on bases not used
  to find the mechanism).** (a) Spearman between `rho_b` and 1D `M_b` over
  the 16 bases `≥ 0.70`; (b) every base with 1D `M ≥ 0.5` (110, 54, 5, 33,
  62, 29) has `rho_b ≥ +0.40`; (c) every chaotic zero-gain base (30, 90, 106)
  has `rho_b ≤ −0.40`. *Pilot-calibrated:* 0.91 on 8 bases, 0.90 on 17; (b)
  minimum 0.57 at n = 512 (54 gave 0.28 on 32 completions, the risk); (c)
  −0.52 to −0.77. Odds 0.65.
- **P4 (naive sign rule on the discriminating bases; the drafting agent
  expects this to fail).** Every base with 1D `M` in `[0.10, 0.40]` (22, 18,
  46) has `rho_b ≥ +0.20`. The naive reading "response sign is the sign of
  1D `M`" predicts this; the mixture reading predicts the sign of
  `M_1D − M_off`, with `M_off ≈ 0.1–0.3`, so 18 (`M_1D = 0.164`, chaotic)
  should not respond. *Pilot:* 22 +0.38 (512) / +0.22 (32); 18 −0.02 (32);
  46 +0.22 (32). Odds 0.30. Its companion **P4′ (mixture reading)**: for
  every base whose on-beam and off-beam band medians differ by at least 0.10
  (both bands with `n ≥ 10`), `sign(rho_b) = sign(median_on − median_off)`.
  *Pilot-calibrated* on 17 bases with zero exceptions. Odds 0.70.
- **P5 (on-beam identity).** For every base with at least ten on-beam
  completions, `|median on-beam M* − M_1D| ≤ 0.15`; for every base with at
  least ten off-beam completions, the off-beam median lies in
  `[0.02, 0.45]`. *Pilot-calibrated:* largest on-beam gap 0.128 (110);
  off-beam medians 0.024 (33) to 0.411 (0, n = 2). Odds 0.60; the off-beam
  arm is the risk (33 sits at the floor).
- **P6 (specificity: retention is not mediated).** `r_R(110, 30) ≥ 0.50` and
  its partial given `(agree_110, agree_30)` differs from the raw value by at
  most 0.15. *Pilot-calibrated:* 0.680 → 0.697. Odds 0.80.
- **P7 (height three).** On 48 completions: `r_M3(110, 30) ≤ −0.20` and
  `agree3` transfers between 110 and 30 at `≥ 0.50`. Two arms.
  *Pilot-calibrated on sixteen completions:* −0.41 and +0.86. Odds 0.60.
  **Demoted at freeze to descriptive:** whether the on-beam fraction at
  height three is at least the height-two fraction on the same completions.
  It was calibrated on sixteen completions of a single base, which is too
  thin to freeze as a prediction; it is reported as a number, not scored.

Descriptive, unscored: the full matrices; the sign accounting (pilot 100%
on the pairs meeting the `|rho| ≥ 0.3` cut, reported, not bet); mediator
gating (pilot `P(on | T_ext ≥ 0.9)` 0.82–0.98, `P(on | T_ext < 0.5)` 0.00);
`alpha_x` against beam proximity; the base-indifference of the off-beam
band across all sixteen bases.

## 5. Outputs

`results/beam_mechanism_20260918/`: `rows.json` (one row per evaluation:
base, completion, table, stream, height, `R*`, `M*`, `S*`, `alpha_x`,
`agree`, band, `T64`, `T128`, `T_ext`, reference mode, wall), `controls.json`
(§2.6, with the eight matched null-pair maximum differences over all seven
compared quantities), `summary.json` (matrices, partials, responses, band
medians, sign accounting, gating, height three, P1–P7, `source_hashes`
registered with the fast integrity tier), and two figures: `M*` against
`agree` per base (sixteen panels, on/mid/off shading) and the raw `M*`
transfer matrix beside its partial given beam proximity. Runner
`experiments/beam_mechanism_20260918/run.py` and `evaluate.py`, both
committed before the run.

## 6. Budget and stopping

Measured on this machine class: 2.10 s per height-two evaluation with beam
proximity recorded, 0.60 s per transverse measurement, 2.25 s per height-
three evaluation before the exact `2¹⁵` reference (allow 3.3 s). Main tier
4,096 × 2.10 = 8,600 s; transverse 4,096 × 0.60 = 2,460 s; height three
384 × 3.3 = 1,270 s; controls and null pairs under 150 s. About 12,500
CPU-seconds, **53 minutes** on four workers at 3.95 effective cores, off
GitHub Actions. Schedule the main tier first, the transverse tier second,
height three last; read no outcome before every tier is written. If wall
time exceeds 80 minutes, reduce to 192 completions and 36 at height three,
record the deviation before reading any outcome, and rerun everything. No
base or completion may be dropped for its outcome. Not run in CI.

## 7. Disclosed pre-freeze pilot

Throwaway scripts in the planning session's scratchpad (`anti/a1.py` …
`a9.py`, `traj.py`, `trans.py`, `pilot.py`; not part of the repository), on
the matched unit's canonical rows plus 400 fresh evaluations:

- On the 8 × 512 grid, decomposing `M*` into its log-losses: baseline
  log-loss transfers 110→30 at +0.34, history log-loss at −0.19; the
  anticorrelation is not a standardization artifact (it is present in the
  relative gain, −0.23) and it survives conditioning on 110's baseline
  entropy (−0.416) but not 30's (−0.136).
- Beam proximity on the events trajectory (rep 0): means 0.63–0.85 by base,
  47% of completions put 110 on the beam; it transfers 0.42–0.84 across all
  28 pairs; `rho_b` = +0.72, +0.57, +0.38, +0.70 for 110, 54, 22, 5 and
  −0.76, −0.71, −0.21, −0.22 for 30, 90, 0, 204; the 110/30 partial given
  both proximities is +0.159 and every one of the 28 partials is positive
  (minimum +0.03). On-beam band medians 0.796, 0.582, 0.132, 0.950, −0.003,
  −0.003, 0.000, 0.000 against 1D `M` 0.903, 0.601, 0.137, 0.976, 0, 0, 0, 0;
  off-beam band means 0.17–0.32 and medians 0.05–0.25 for all eight. The
  band `0.5 ≤ agree < 0.9` is the lowest of the three for four of the eight
  bases (54, 22, 30, 90: intermittent beam visits defeat the eight-step
  history), so the response is not monotone; `rho_b` is nonetheless ordered
  by 1D `M` at Spearman 0.91.
- Transverse stability on beam states with its own seeds: `T128` against
  `agree` at −0.80 to −0.93 in every base; `T_ext` transfers 0.72–0.83
  between 110 and every non-frozen base, 0.25 to base 0; the 110/30 partial
  given both `T_ext` is +0.116. `P(agree > 0.98 | T_ext ≥ 0.9)` = 0.96,
  0.98, 0.82, 0.88 for 110, 30, 5, 90 and 0.00 given `T_ext < 0.5`.
- Bit-additivity: ridge cross-validated `R²` on the 24 bits for `agree`,
  `T_ext`, `log T128` and the on-beam indicator is between −0.06 and +0.06
  in every base.
- Retention: `R*` against `agree` is inconsistent in sign across bases and
  on-beam `R*` is not the 1D `R` (110: −0.047 against 0.252, the observer is
  height-relative); the 110/30 `R*` transfer is 0.680 raw and 0.697 partial.
- Height four (canonical 8 × 128 rows): on-beam fractions 0.01–0.19, `agree4`
  transfer 110/30 +0.03, off-beam median `M*` ≈ 0.00–0.03 for every base,
  `rho_b` +0.80 for 110 and −0.07 for 30, raw transfer 0.00: both
  ingredients of the mechanism are absent and so is the effect. The
  height-four trajectories often sit on the vertical-period-two manifold
  (rows `a, b, a, b`; fractions 0.18–0.49), which is the embedded height-two
  strip; recorded, not pursued.
- Height three, 16 fresh completions from `default_rng(20260919)` × {110,
  30, 5, 90}: on-beam fractions 0.69, 0.69, 0.38, 0.56; `rho_b` +0.42,
  −0.85, +0.59, −0.78; `r_M3(110, 30)` −0.41; `agree3` transfer +0.86.
- Nine new bases × the first 32 canonical completions: `rho_b` 106 −0.73,
  45 −0.52, 8 −0.02, 232 −0.65, 18 −0.02, 46 +0.22, 33 +0.70, 62 +0.82,
  29 +0.70; on-beam medians within 0.09 of 1D `M` where `n ≥ 4`; Spearman
  of `rho_b` against 1D `M` over 17 bases +0.90; `agree` transfer with 110
  0.46–0.87.

The pilot chose the new bases, the tiers and every threshold; its
sixteen height-three completions are not reused; its numbers are quoted as
the origin of each bet and nowhere as evidence.

## 8. Non-claims

Not a Class-IV definition; not the full plane; not a statement about other
observers or densities. Not a claim that beam proximity is the *only*
mediator: the partials stay positive (about +0.15 to +0.35), a shared
off-beam term this unit does not decompose. Not a claim about which
completion bits make a beam attracting (pilot: not additive). Not a theorem
about transverse stability implying global attraction; the gating numbers
are empirical. Not a claim at height four, where the pilot finds the
mechanism's ingredients absent, nor a monotone claim in height. A positive
P1–P3 shows that in this family, under this contract at height two, the
history-gain transfer structure between bases, including its negative
entries, is the signature of one completion-set variable, how much of the
trajectory lives on the invariant one-dimensional beam, acting through each
base's own one-dimensional history gain. A P4 failure with P4′ holding says
the response is set by 1D history gain *relative to the off-beam value*, not
by 1D history gain alone.
