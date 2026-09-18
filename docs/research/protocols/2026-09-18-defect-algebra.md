# Protocol: the single-defect algebra on the beam — twelve count-insensitivity bits decide transverse stability

**Status:** FROZEN before implementation and evaluation.
**Date:** drafted 2026-09-18.
**Author:** drafted by Claude/Fable 5.1; reviewed, amended and frozen by
Claude Opus 5, who implements, runs and records the unit. Myk's session.

**Independent re-derivation at freeze (Opus 5).** The exact content of §2 was
re-derived from the read-index definition rather than taken on report, and
every claim reproduces: flipping one cell of a beam state perturbs exactly six
reads and **none** of the post-flip reads lands on an exposed entry (0 of 192);
the lit set is exactly the 14 entries `{1,2,5,8,11,12,15,16,19,20,23,26,29,30}`
and the dark set the complementary 10; one-step healing is a conjunction of
three pairwise bit-equalities whose pairs depend on the window **only** through
`(LL,L)`, `(L,R)` and `(R,RR)` respectively; the twelve constraints have GF(2)
rank **11**, giving 2,048 signatures of 8,192 completions each and a 13-dimensional
universal-healer subspace; `E[H1] = 0.1251` against the predicted `1/8`; and a
completion satisfying all twelve heals every window.

Structure the draft did not name, recorded because it bears on the amendment
below: the three blocks are pairwise-disjoint in form. Every `A` constraint
equates two entries **1** apart in table index, every `C` constraint two entries
**6** apart, every `B` constraint two entries **14** apart.

**Amendments at freeze (Opus 5).** (i) The mirror cell `A ≡ 1, C ≡ 0` is
**added as a fifth class cell and run**, not deduced — see §2.3. (ii) The edge
lemma and its corollaries are promoted as an exact knowledge node on their own
proof, independent of P1–P6, as the beam theorem was.
**Program:** Class-IV refinement, sixth unit.
**Protocol review:** none at freeze. Myk's 2026-09-17 suspension of the
cross-model review gates remains in force; the executing session runs,
self-reviews and merges. The results note must say evaluation preceded
review. Suspension is not authorization to skip the freeze: this draft is
amended and committed before `run.py` is written.

**Standing.** The exact part (§2.2) is proved by index algebra and verified
by exhaustive enumeration in the drafting session; the executing session
re-derives it rather than taking it on report, and the run asserts it as a
gating control. Every empirical prediction (§4) is calibrated on a
reanalysis of the [beam-mechanism unit's](2026-09-18-beam-mechanism.md)
canonical rows (its 4,096 transverse trials regenerated exactly, zero
mismatches) plus a small fresh pilot (§7), and each says so. The canonical
completions of this unit come from a fresh seed namespace and, for the
built classes, from a construction the canonical rows could not have
sampled. This unit is therefore a **pre-registered out-of-sample
replication of an exact structure read off existing data**, and is reported
as one. P3(a) and P4(b) are the predictions the drafting agent expects to
be at real risk; P4(b) is the one it expects to fail.

## 1. Purpose

The beam-mechanism unit proved that on a height-two strip the equal-row set
is invariant under every rule of the handed family and the strip is the base
rule on it, and measured that beam proximity is the completion-set mediator
of history-gain transfer. Its open question, recorded in the checkpoint: **what
makes a completion attract trajectories onto the beam?** It found one handle,
transverse stability gates residence downward (`P(on | T_ext < 0.5) ≤ 0.034`),
and proposed "an exact single-defect first-step analysis on the beam".

This unit performs that analysis and finds it is not only first-step. Its
exact content, proved in §2.2:

- A single defect on the beam reads, on its first step, **14 of the 24 free
  entries**; ten are dark to it. One-step healing at a five-cell beam window
  `(LL, L, C, R, RR)` is the conjunction of three bit-equalities between free
  entries, `A(LL,L) ∧ B(L,R) ∧ C(R,RR)`, twelve equalities in all. Each is a
  **count-insensitivity** of the completion: row 1 sees the defect once, row
  0 sees it twice through the wrap, and healing at a column means the
  completion does not tell those two readings apart.
- **Edge lemma.** For *any* defect configuration on the strip, the column
  west of the leftmost defect reads exactly the pair `A(x[j−2], x[j−1])` and
  the column east of the rightmost defect reads exactly `C(x[j+1], x[j+2])`,
  independent of the cluster's interior; an isolated single defect at column
  `o` reads `B(x[o−1], x[o+1])` at its own column. So the twelve bits split
  into **A = leftward growth, B = survival of an isolated defect, C =
  rightward growth**, at every step, not only the first.
- Corollaries: a completion with all four `A` bits violated (or all four `C`
  bits) never heals any defect on any base — the front advances one column
  per step forever, `T_ext = 0` exactly; a completion with all `A` and all `C`
  bits satisfied confines a single defect to its column forever; a completion
  satisfying all twelve heals every single defect in one step on every base
  (`T_ext = 1` exactly). The twelve bits have rank 11 over GF(2), so 2,048
  healing signatures are realizable, each by exactly `2¹³` completions.

The empirical content, read off the canonical rows and to be replicated
here: the exact one-step healing rate `H1(r, u) = Σ_w μ_r(w)·heal_u(w)`, a
pen-and-computer quantity from the twelve bits and the base's beam-window
measure, orders the measured 128-step `T_ext` at Spearman +0.65 to +0.88 in
every one of sixteen bases; the twelve healing bits, as features, explain
`T_ext`, beam proximity and (on high-gain bases) `M*` with cross-validated
`R²` of +0.25 to +0.52, +0.18 to +0.46 and +0.23 to +0.39, where the 24 raw
completion bits explain nothing (`R² ≤ 0.01`, replicating the matched
unit's negative). **The completion's effect is additive in pairwise XORs of
free entries, which a linear model in bits cannot see.** And flipping three
dark entries leaves `T_ext` nearly unchanged (paired Spearman +0.66 to +1.00)
while flipping three lit entries destroys it (≈ 0), even though most healing
events happen after step one and step two lights every entry: over 128
steps, transverse stability is close to a function of the fourteen lit
entries alone. Beam residence from a random start is **not** — dense defects
read the dark entries — and that is the discrepancy this unit measures.

Questions:

> (a) Do the twelve healing bits, and the scalar `H1`, predict transverse
> stability on fresh completions, where the raw bits do not?
> (b) Do completions **built** to be universal one-step healers reside on
> the beam from random starts, and do built never-healers never reside?
> (c) Is transverse stability a function of the lit entries (dark flips
> invariant) while beam residence is not?
> (d) Does the healing-bit structure reach `M*` on high-gain bases through
> the mediator, and not on zero-gain bases?

What this unit is **not**: not a basin theory for the beam (the built
classes bound residence from two sides, they do not characterize it); not a
multi-step exact enumeration (the window a `k`-step fate depends on has
`4k+1` cells and the beam measure is empirical anyway; the trials' healing
times are the instrument); not the discriminating-window base panel the
previous checkpoint asked for (that is a question about the base response,
separate from the completion structure asked here, and it is parked, not
dropped); not height three (the vertical wrap there gives a different
constraint algebra, and the mixture degenerates there anyway); not a
statement about the plane, other observers, or other densities.

## 2. Objects

### 2.1 Family, restriction, completions, contract

`H`, `E`, `F`, `embed`, `res1`, the handed step, the height-two contract,
`evaluate` (with beam proximity `agree`), `transverse` (`T64`, `T128`,
`T_ext`), `_initial`, `bits_of`, `conj_table` are the beam-mechanism unit's
unchanged; `run.py` imports them from
`experiments/beam_mechanism_20260918/run.py`. Width 521, density 0.5, burn
512, 256 scored transitions, six event seeds, 64 sites, the exact height-two
reference. Seeds keyed on `(stream, u, k, density, rep)` and on
`("transverse", u, rep)` as before, never on the base or table; the seed
function is this protocol's, keyed on `defect-algebra-20260918`.

### 2.2 The exact algebra (proved; asserted at run time)

Index of cell `(r, j)` on a two-row strip:
`16·x_r[j] + 8·x_r[j−1] + x_r[j+1] + 2·(x_{r'}[j−1] + x_{r'}[j] + x_{r'}[j+1])`.
On the beam (`x_0 = x_1 = x`) this is `16C + 8L + 2L + 2C + 3R`, the exposed
index. Flip `(1, o)` on a beam state:

- row 0 at `o−1, o, o+1`: `n₇` shifts by `2 − 4C` (the defect is seen twice
  through the wrap); row 1 at `o−1`: `n₇` shifts by `1 − 2C`; row 1 at `o+1`:
  `w` flips; row 1 at `o`: `c` flips. A shift of `±1` or `±2` in `3R` never
  lands on `{0, 3}` and a `c` or `w` flip moves the exposed `n₇` by `±2`, not
  a multiple of 3, so **all six reads are free entries**.
- The six reads form three pairs, one per column, and by the index formula
  the pair at `o−1` depends only on `(LL, L)`, at `o` only on `(L, R)`, at
  `o+1` only on `(R, RR)`. Explicitly, as `(c, w, n₇)` triples:
  `A(LL,L)`: (0,0): {(0,0,1),(0,0,2)}; (0,1): {(1,0,3),(1,0,4)}; (1,0):
  {(0,1,3),(0,1,4)}; (1,1): {(1,1,5),(1,1,6)}.
  `B(L,R)`: (0,0): {(0,0,2),(1,0,0)}; (0,1): {(0,0,5),(1,0,3)}; (1,0):
  {(0,1,4),(1,1,2)}; (1,1): {(0,1,7),(1,1,5)}.
  `C(R,RR)`: (0,0): {(0,0,2),(0,1,0)}; (0,1): {(0,0,5),(0,1,3)}; (1,0):
  {(1,0,4),(1,1,2)}; (1,1): {(1,0,7),(1,1,5)}.
  Table indices: A {1,2},{19,20},{11,12},{29,30}; B {2,16},{5,19},{12,26},
  {15,29}; C {2,8},{5,11},{20,26},{23,29}. Lit set (14):
  {1,2,5,8,11,12,15,16,19,20,23,26,29,30}; dark set (10):
  {4,6,7,9,14,17,22,24,25,27}. Both sets are closed under complement
  conjugation, which permutes the twelve bits by `(a,b) ↦ (1−a, 1−b)` within
  each block.
- The number of new defects after one step is exactly the number of violated
  constraints among the three (0 to 3).
- The constraint graph on the 24 free entries has components {1,2,8,16},
  {15,23,29,30}, {5,11,12,19,20,26} (one cycle: 19–20–26–12–11–5) and ten
  isolated vertices, so the twelve XORs have rank 11, each of the 2,048
  realizable signatures has exactly `2¹³ = 8,192` completions, every window
  heals with probability exactly 1/8 under a uniform completion, and
  `E[H1] = 1/8` for every base.
- **Edge lemma.** With the leftmost defect at column `j` (rows agree at
  `j−1, j−2`, disagree at `j` with values `a, 1−a`), the two reads at `j−1`
  are `16·x[j−1] + 8·x[j−2] + {2LL + 2L + 1, 2LL + 2L + 2}` with
  `(LL, L) = (x[j−2], x[j−1])`: the pair `A(LL, L)`, whatever lies east. The
  mirror computation at the rightmost defect gives `C(R, RR)`. An isolated
  defect with both flanks agreeing reads `B(L, R)` at its own column.
  Hence: `A ≡ 0` or `C ≡ 0` ⇒ never heals (`T_ext = 0` on every base and
  beam state); `A ≡ 1 ∧ C ≡ 1` ⇒ a single defect never leaves its column;
  all twelve ⇒ heals in one step on every base (`T_ext = 1`, `T64 = T128 = 0`).
- At step two, over all completions and all nine-cell windows, every one of
  the 32 entries is read (verified for bases 110, 30, 0, 204, 90): the dark
  set is a first-step fact, not a permanent one.

### 2.3 Completions: three arms, one namespace

All drawn from `default_rng(seed("completions"))` in this protocol's
namespace, in the order below, and asserted disjoint from the matched unit's
512, the beam unit's 256 and the §7 pilot's draws.

- **Random arm, 192 completions** drawn uniformly without replacement.
- **Flip arm, 96 completions:** for each of the first 48 random-arm
  completions `u`, a **dark partner** `u ⊕ (three dark entries)` and a **lit
  partner** `u ⊕ (three lit entries)`, the three entries chosen without
  replacement by the same generator, in that order. The dark partner has the
  same twelve healing bits as `u` by construction (asserted).
- **Class arm, 96 completions, 24 per cell**, built by enumerating the
  twelve bits over all `2²⁴` completions at run time (two seconds) and
  sampling from the index set of each cell with the generator:
  **U+** (all twelve satisfied; `T_ext = 1` by theorem),
  **U−** (all twelve violated; `T_ext = 0` by theorem),
  **G** (`A ≡ 0`, `B ≡ 1`, `C ≡ 1`: westward grower; `T_ext = 0` by theorem),
  **G′** (`A ≡ 1`, `B ≡ 1`, `C ≡ 0`: eastward grower; `T_ext = 0` by theorem),
  **K** (`A ≡ 1`, `C ≡ 1`, `B` random but not all satisfied: confined).
  The remaining bits are whatever the sampled completion carries.

**Amendment at freeze: `G′` is run, not deduced.** The draft proposed deducing
the mirror cell from `G`. There is no symmetry of this family that licenses
that. Reflection does not preserve the handed family at all — it maps it to the
east-marked family, which is precisely why the chirality question in the third
unit had to be settled empirically rather than by deduction. Complement
conjugation permutes the twelve bits within each block and so cannot exchange
`A` with `C`. And the blocks are not even structurally alike: `A` constraints
equate table entries one apart, `C` constraints entries six apart. Whether a
westward and an eastward grower behave alike is therefore an empirical question
in a family built around a distinguished direction, and it costs about two
minutes to answer rather than assume.

408 completions in all (24 more than the draft, for `G′`).

### 2.4 Bases

The matched unit's eight, `{110, 54, 22, 5, 30, 90, 0, 204}`, for continuity
with both previous units' calibrations; condition-P rows asserted by value
as before. Frozen bases 0 and 204 are kept because their beam measures are
degenerate (rule 0's beam is the zero row, so `H1 ∈ {0, 1}` exactly and the
edge lemma applies with `(LL, L) = (0, 0)` only) and they are where the
scalar `H1` explains the most (`R²` 0.77).

### 2.5 Quantities per (base, completion)

`R*`, `M*`, `S*`, `alpha_x`, `agree`, `on_beam`, `off_beam` from `evaluate`;
`T64`, `T128`, `T_ext` from `transverse`, plus per-trial **healing time**
(first step with zero disagreement, or none within 128) and the defect count
at steps 1, 2, 4, 8, 16, 32, 64, 128, recorded by a `transverse_traced`
variant that must reproduce `transverse` exactly (control 4). Exact
per-(base, completion): the twelve healing bits, `(nA, nB, nC)`, the
five-cell beam-window measure `μ_r` over all 521 columns of the four
transverse beam states, and `H1 = Σ_w μ_r(w)·heal_u(w)`.

### 2.6 Controls (before any observable; any failure stops the run)

1. **Algebra, exact:** enumerate the six reads for all 32 windows: all free,
   14 lit, 10 dark, the three pairs per window equal to the `A`, `B`, `C`
   tables of §2.2; rank of the twelve XORs is 11; the U+ and U− index sets
   have exactly 8,192 members each; the complement conjugation of 64 random
   completions permutes the signature exactly as stated. Asserted.
2. **Defect-count identity, can fail:** for 256 random `(completion,
   window)` pairs, the simulated step-one disagreement count on a width-13
   ring equals the number of violated constraints. Asserted.
3. **Edge-lemma corollaries on built classes, can fail:** for every base and
   every U+ completion, all 32 trials heal at step one (`T_ext = 1`,
   `T64 = T128 = 0`); for every U− and G completion, no trial heals
   (`T_ext = 0`) and the leftmost defect column moves west by exactly one at
   every step for the first 16 steps; for every K completion, the defect
   count never exceeds one. These run the transverse tier of the class arm
   early, as a control; the rows are kept, not recomputed.
4. **Regeneration, can fail:** the traced transverse code reproduces the
   beam unit's canonical `T64`, `T128`, `T_ext` exactly on its first 16 main
   rows (base 110 and 54, the canonical seeds and completions); and its
   untraced twin `transverse` gives identical numbers on the same rows.
5. **Beam invariance, exact:** as the beam unit's control 2, for eight
   random-arm completions of every base, 256 steps at heights two and three.
6. **Matched null pair, the finding-4 form:** for the first eight random-arm
   completions, `embed(137, ū)` from complemented initial states keyed on the
   original `u`, and its transverse tier from the complemented beam state
   keyed on the original `u`; `R*`, `M*`, `alpha_x`, `agree`, `T64`, `T128`,
   `T_ext` each to `1e-9`, and the twelve healing bits of `ū` equal to the
   permuted bits of `u`. The seed key is an argument, never derived from the
   table.
7. Disjointness of the three arms from the earlier units' completions and
   the pilot's, and the eight condition-P rows by value. Asserted.

Controls 3 and 6 cannot be written so that they cannot fail: a sampler bug,
a wrong table, a wrong complement or a changed transverse loop each produces
a non-zero difference. The runner runs 1–7 in this order before the tiers,
writes `controls_failed.json` and stops on any failure.

## 3. Frozen analysis

All by `evaluate.py`, committed before the run.

- **Regressions per base**, 8-fold cross-validated ridge (`λ = 1`, fixed
  permutation seed), targets `T_ext`, `agree`, `M*`, features: the 24 raw
  bits; the 12 healing bits; `(nA, nB, nC)`; `H1` alone. On the random arm.
- **`H1` against `T_ext`** and against `agree`: Spearman per base on the
  random arm; gating `P(on | H1 = 0)` and `P(T_ext ≥ 0.9 | H1 = 0)`.
- **Flip arm:** per base, paired Spearman of `T_ext(u)` with `T_ext(dark
  partner)` and with `T_ext(lit partner)`; medians of `|Δ|`; the same for
  `agree` and for the on-beam indicator's concordance.
- **Class arm:** per base and cell, median `agree`, `P(on_beam)`,
  `P(off_beam)`, mean `T_ext` (theorem-fixed for U+, U−, G), median `M*`.
- **Healing times** on the random arm: per base, among healed trials the
  cumulative fraction healed by steps 1, 2, 4, 8, 16, 32, 64.
- **Bootstrap** over completions (2,000 resamples, seeded) for every
  threshold statistic; intervals reported, verdicts on point values.

## 4. Frozen predictions

Odds are the drafting agent's. Each states its calibration (§7).

- **P1 (the healing bits are the additive structure; replication).** On the
  192 random-arm completions, in **every** one of the eight bases: (a)
  cross-validated `R²` of `T_ext` on the 12 healing bits `≥ 0.15`; (b) on
  the 24 raw bits `≤ 0.10`; (c) `R²` of `agree` on the 12 bits `≥ 0.10` and
  on the raw bits `≤ 0.10`. *Calibrated on the canonical rows (n = 256 per
  base):* (a) 0.25–0.52 across sixteen bases, minimum 0.252 at base 5; (b)
  maximum +0.014; (c) 0.18–0.46, minimum 0.179 at base 54, raw maximum
  +0.009. The thresholds allow for n = 192. Odds 0.75; base 5 on (a) and
  base 54 on (c) are the risks.
- **P2 (`H1` predicts transverse stability).** Spearman of `H1` with `T_ext`
  `≥ 0.50` in every base on the random arm. *Calibrated:* +0.65 (base 33) to
  +0.88 (base 0) over sixteen bases; on this panel +0.66 to +0.88. Odds 0.85.
- **P3 (built classes and beam residence; the bet on the open question).**
  (a) **U+**: median `agree ≥ 0.95` and `P(on_beam) ≥ 0.50` in every base.
  *Weakly calibrated:* the one universal healer the canonical draw happened
  to contain (`u = 15150256`) has `agree ≥ 0.916` on all sixteen bases and
  is on-beam on twelve; the canonical `nsat ≥ 10` class (seven completions)
  has `P(on)` 0.29 (bases 0, 5, 8, 46, 204) to 0.71 per base. **This is the
  prediction at real risk**: one-step healing of isolated defects does not
  imply the beam attracts dense random states, and the frozen bases are the
  likely failures. Odds 0.45. Companion **P3(a′)**: U+ has the highest median
  `agree` of the four cells in every base. Odds 0.7.
  (b) **U− and G**: `P(on_beam) ≤ 0.02` in every base and the median `agree`
  of each is below the random arm's. *Calibrated:* the 27 canonical
  completions with `A ≡ 0` or `C ≡ 0` are on-beam in 0 of 432 rows (max
  `agree` 0.80). Not a theorem (simultaneous healing of every column is not
  excluded), so it is bet, at odds 0.90.
  (c) **K** (confined): mean `T_ext` at least the random arm's in every
  base. *Calibrated on four canonical completions:* 0.50–0.93 against
  0.14–0.62. Odds 0.6.
- **P4 (dark flips: transverse stability is lit-only, residence is not).**
  (a) On the 48 flip pairs, in every base, paired Spearman of `T_ext` with
  the dark partner `≥ 0.50`, strictly greater than with the lit partner, and
  median `|ΔT_ext|` under dark flips `≤ 0.10`. *Pilot-calibrated (32 pairs,
  six bases):* dark +0.66 to +1.00, lit −0.15 to +0.31, dark medians
  0.00–0.078. Odds 0.8.
  (b) The same three conditions for `agree` in every base. *Pilot-calibrated
  (24 pairs, six bases):* dark +0.24 (90) to +0.82 (0); lit −0.15 to +0.56;
  base 90 fails on both the level and the ordering, base 204 nearly ties.
  **Expected to fail**; a failure confined to one or two bases is the
  informative outcome, read as: dense defects from a random start do read
  the dark entries. Odds 0.25.
- **P5 (the structure reaches `M*` through the mediator).** Cross-validated
  `R²` of `M*` on the 12 healing bits `≥ 0.15` for 110, 54 and 5, and
  `≤ 0.10` for 30, 90, 0 and 204; 22 is unscored (mid band). *Calibrated:*
  0.387, 0.386, 0.231; −0.052, +0.018, −0.076, −0.019. Odds 0.6; base 5 at
  n = 192 is the risk.
- **P6 (most healing is not first-step, yet lit-only).** On the random arm,
  among trials that heal within 128 steps, the fraction healing at step one
  is `≤ 0.45` in every non-frozen base (110, 54, 22, 5, 30, 90). *Calibrated:*
  0.19 (22) to 0.34 (18) on non-frozen bases; frozen bases 0.78–0.80. Odds
  0.85. Scored because it pins the reading of P4(a): the first step decides
  a minority of healing events while the fourteen first-step entries decide
  nearly all of `T_ext`.

Descriptive, unscored: the `(nA, nB, nC)` compression (canonical: explains
`T_ext` as well as the twelve bits in every non-frozen base, 0.27–0.48); the
healing-time curves; per-bit marginal effects; the A-versus-C asymmetry of
the handed family on the flip and class arms, now measured on both grower
cells rather than deduced; any asymmetry between `nA` and `nC` effects is
recorded, not bet (canonical pooled means by `nA` and by `nC` agree to 0.02); the fraction of `T_ext = 0`
rows the edge corollaries explain (canonical: 432 of 1,268); `P(on | H1 = 0)`
per base (canonical 0.00–0.24).

## 5. Outputs

`results/defect_algebra_20260918/`: `rows.json` (one row per evaluation:
base, completion, arm, cell or partner role, table, all §2.5 quantities
including the 32 healing times and defect-count traces, the twelve bits,
`(nA, nB, nC)`, `H1`, wall), `algebra.json` (the enumerated reads, tables,
lit/dark sets, components, rank, class sizes, step-two reach), `controls.json`
(§2.6 with the eight null-pair maximum differences over all seven quantities
and the signature permutation check), `summary.json` (§3 statistics, P1–P6,
`source_hashes` registered with the fast integrity tier), and two figures:
`T_ext` against `H1` per base with the four cells marked, and the paired
dark/lit flip scatter for `T_ext` and `agree`. Runner
`experiments/defect_algebra_20260918/run.py` and `evaluate.py`, committed
before the run. The exact algebra is recorded as a knowledge node
(finding, exact) on its own proof, independent of P1–P6.

## 6. Budget and stopping

Measured on the canonical machine class: 2.07 s per height-two evaluation
with beam proximity, 0.60 s per transverse measurement (no early exit; the
traced variant is the same loop). 384 completions × 8 bases = 3,072
evaluations × 2.67 s = 8,200 CPU-seconds; controls under 120 s. About
**35 minutes** on four workers at 3.95 effective cores, off GitHub Actions.
Order: controls 1–7, then the class arm's transverse tier is already written
by control 3, then the random arm, the flip arm, the class arm's
evaluations; read no outcome before every tier is written. If wall time
exceeds 60 minutes, reduce the random arm to 128 and the flip arm to 32
pairs, record the deviation before reading any outcome, and rerun
everything. No base, completion or cell may be dropped for its outcome. The
exact part costs seconds and would stand at any budget. Not run in CI.

## 7. Disclosed pre-freeze pilot

Throwaway scripts in the planning session's scratchpad (`defect/d1.py` …
`d12.py`, `sp.py`; not part of the repository):

- `d1`–`d3`, `d5`: the enumeration and rank facts of §2.2, the step-two
  reach, and the signature distribution over all `2²⁴` completions (number
  of satisfied constraints is Binomial-shaped with mean 6.0; 8,192 at each
  extreme).
- `d2`, `d4`: the beam unit's 4,096 transverse rows regenerated with healing
  times, `T64`/`T128`/`T_ext` reproduced with zero mismatches; simulated
  step-one defect counts equal violated-constraint counts on all 131,072
  trials. Among healed trials 28% heal at step one, 56% by step four, 81% by
  step sixteen, pooled; per base 0.19–0.34 non-frozen, 0.78–0.80 frozen.
  Pooled Spearman with `T_ext` of the healed-by-`k` fraction rises 0.72
  (`k = 1`), 0.82, 0.90, 0.94, 0.97 (`k = 16`).
- `d6`, `d6b`, `d12`: `H1` (all 521 columns, four beam states) against
  `T_ext` +0.65 to +0.88 per base; cross-validated ridge `R²` as quoted in
  P1 and P5; `(nA, nB, nC)` explains `T_ext` 0.27–0.48 non-frozen; the edge
  corollaries exact on 432 never-healer rows and 2,048 confined trials.
- `d8`, `d9`: `P(on)` by signature class: `nsat ≤ 2` 0/80; 3–5 0.13; 6 0.27;
  7–9 0.46; 10–12 0.55; the single canonical universal healer as quoted.
- `d7`, `d11`: flip pilot from `default_rng(20260918)`, 32 (transverse) and
  24 (evaluation) triples, bases 110, 30, 0, 204, 5, 90; numbers as quoted
  in P4. Those completions are excluded from this unit's arms.
- `d10`: sampled U+ completions give `T_ext = 1` exactly and U− give 0 on
  bases 110, 30, 0, 204; the signature complement permutation as stated.

The pilot chose the arms, the cells and every threshold; its numbers are
quoted as the origin of each bet and nowhere as evidence.

## 8. Non-claims

Not a characterization of which completions attract the beam from random
starts: the built classes bound residence from both sides and the healing
bits explain a third to a half of its variance; the remainder, and the dark
entries' share of it, is what P4(b) measures, not explains. Not a claim that
`T_ext` is exactly a function of the lit entries (P4(a) is a near-invariance,
and step two reads every entry). Not a multi-step exact theory: the edge
lemma governs the cluster's extent, not its interior, and healing needs
both. Not a statement at height three, on the plane, at other densities or
observers, or about the base response (the discriminating-window panel is
parked). A positive P1–P2 with P3(a) says the exact twelve-bit structure is
the first-order account of transverse stability and, through the gating the
beam unit measured, of beam residence; a P3(a) failure with P3(b) holding
says isolated-defect healing is necessary for residence and not sufficient,
which is the more interesting outcome and is reported as such.
