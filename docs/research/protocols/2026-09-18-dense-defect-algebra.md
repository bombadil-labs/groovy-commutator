# Protocol — the dense defect algebra on the strip (Class-IV Refinement, seventh unit)

**Frozen** 2026-09-18 by Claude Opus 5 (executing session), on a draft by
Claude/Fable 5.1 (planning agent). Committed before `run.py` exists.

**Protocol review:** none at freeze. Myk's 2026-09-17 suspension of the
cross-model review gates is in force ("because GPT currently has no access to
github, our review protocols are suspended. You are authorized to run with
this on your own, review your own PRs etc."). The results note must state that
evaluation preceded review. The suspension does not waive the freeze.

**Standing.** The exact content of §2 is a theorem, proved by index algebra and
verified independently by the executing session before freeze (§8). It stands
however the census scores. Every empirical prediction is calibrated on a
reanalysis of the defect-algebra unit's canonical rows plus the drafting
agent's pilot, and says so; twelve of the twenty bases carry no calibration for
the grower and random arms, so the ordering predictions are out of sample on
twelve. This unit is a pre-registered replication of an exact structure read
off existing data, plus theorems.

---

## 0. What this unit replaces, and a correction the coordinator owes the record

The defect-algebra unit (result 18) proved the twelve single-defect bits and
then found that residence from a dense random start is not the same quantity:
universal healers never reside under base 204, and growers do not sit below the
random arm in three bases.

Reviewing that result, the executing session proposed a floor/carry
decomposition and offered a mechanism: that the identity contributes no mixing,
so nothing carries a dense state the last few percent onto the beam. **That
reading is wrong, and this protocol records it as wrong.** Rule 51 — which
flips every cell every step, maximal activity — has the identical exact
residual to the identity, and totalistic rule 0 heals every planted pair.
Measured before freeze, 64 completions × 8 origins × 512 steps: permanence
1.000 under 204, 1.000 under 51, 0.205 under 90, 0.031 under 5, and exactly
0.000 under 0, 22, 110, 30. Activity is irrelevant. What decides survival is
whether the base's exposed entries reproduce a disagreement on two
equal-popcount windows — four bits of the base (§2.2).

The drafting agent declined the floor/carry decomposition on those grounds and
proposed a sharper one, by **stratum of the read**. The executing session
verified the algebra independently (§8) and accepted it. The floor claim is the
coordinator's and is post hoc on eight bases; it enters here only as P4(e), a
pre-registered test on twenty bases, and control 10, never as an assumption.

## 1. Purpose

Extend the algebra from one defect to any configuration. At height two it is
finite and small: **28 pair-constraints in all**, stratified by what the two
rows' popcounts do at a column.

Questions:

> (a) Is the identity exception exact through the real measurement path, and
>     does it replicate on a base with maximal activity (51)?
> (b) With every free constraint satisfied (`U++`), is the residual across
>     twenty bases ordered by the base's blind-pair survival `Π`, out of
>     sample on twelve?
> (c) Is the grower floor east-edge erosion — ordered by `β₁+β₃` for `G` and
>     `β₂+β₄` for `G′`, handed, out of sample — and does it collapse under 51
>     as under 204?
> (d) Do the dark bits matter for residence where the background is frozen
>     (`D+` vs random), and not once the lit bits hold (`U+` vs `U++`)?
> (e) **(amendment)** Is the stratum decomposition *specific* — does the
>     confined cell `K`, whose residual the algebra says is lit-governed,
>     remain unordered by `Π` out of sample?

Not: a basin theory for active bases; height three; other densities or
observers; any claim about `M*`.

## 2. Objects

### 2.1 Contract, helpers, seeds

Standing height-two contract unchanged: width 521, density 0.5, burn 512, 256
scored transitions, six event seeds (4 train / 2 test), 64 sites; disturbance
4 seeds × 8 origins at horizons 64/128. `evaluate`, `transverse_traced`,
`_initial`, `sample_events_agree`, `spread_keyed`, `beam_measure` are **copied**
from unit six's runner into this unit's runner — not imported — with this
protocol's seed function keyed on `dense-defect-algebra-20260918`, and every
helper takes `seedfn` as an argument. Seeds key on `(stream, u, k, density,
rep)` and `('pair', u, rep)`; never on the base or the table.

Addition to the events loop, recorded per scored step: defect-column counts by
stratum (`Δ=0`, `|Δ|=1`, `|Δ|≥2`), cluster count, count of width-two
anti-phase clusters, and one-step survival counts per stratum. The accounting
must reproduce `agree` exactly from its own counts (control 2). Under `U++` the
lit and dark survival counts are identically zero (T5; control 5).

### 2.2 The exact algebra

Row `r` at column `j` reads index `16x_r[j] + 8x_r[j−1] + x_r[j+1] + 2s_{r′}(j)`
where `s` is a row's three-cell popcount. With `Δ_j = s₁(j) − s₀(j)`:

| `\|Δ\|` | both rows read | pairs |
| --- | --- | ---: |
| 0 | exposed (base-owned) | 6 |
| 1 | lit | 15 |
| ≥ 2 | dark | 7 |

This **characterizes** unit six's 8/14/10 entry partition rather than
enumerating it. The 64 six-bit windows give 8 trivially agreeing cases and 28
unordered pairs; the one-step law is `D_{t+1}[j] = t[i₀(W)] ⊕ t[i₁(W)]`.

- **Exposed (base bits).** `β₁: F(100)=F(010)`, `β₂: F(001)=F(010)`,
  `β₃: F(011)=F(101)`, `β₄: F(110)=F(101)` (defect centre);
  `γ₀: F(001)=F(100)`, `γ₁: F(011)=F(110)` (agreeing centre, swapped flanks).
  Complement conjugation swaps `β₁↔β₃`, `β₂↔β₄`; reflection swaps `β₁↔β₂`,
  `β₃↔β₄`.
- **Lit (15).** Unit six's twelve, plus diagonals `{5,26}`, `{11,20}`,
  `{12,19}`, which lie in the hexagon 19–20–26–12–11–5 and are **implied** by
  its edges (rank is 11 with or without them; verified).
- **Dark (7).** `{4,9}`, `{4,17}`, `{4,24}`, `{6,25}`, `{7,27}`, `{14,27}`,
  `{22,27}`. Rank 7.
- Free rank 11 + 7 = 18 over 24 free entries, so **exactly 64 completions
  satisfy every free constraint** (`U++`), one per connected component.
- **Blind defects.** A defect column is blind iff it is the edge of a run of
  width ≥ 2 whose edge pair is anti-phase. The **left** edge reads `β₂` (west
  flank 0) or `β₄` (west flank 1); the **right** edge reads `β₁` (east flank 0)
  or `β₃` (east flank 1). Hence east-erosion `e_G = β₁+β₃` for a westward
  grower, `e_{G′} = β₂+β₄` for an eastward one. (Re-derived independently by
  the executing session; matches the draft exactly.)
- **T3, one-step collapse.** `β` all hold ⇔ the base is totalistic (exactly 16
  rules: 0, 1, 22, 23, 104, 105, 126, 127, 128, 129, 150, 151, 232, 233, 254,
  255), and then `γ` hold too. Totalistic base × `U++` ⇒ every column agrees
  after one step from **every** state.
- **T4, the identity exception, exact residual.** Under 204 and 51,
  anti-phase width-two runs with agreeing flanks are fixed for every `A ∧ C`
  completion; under `U++` the disagreement field from `t = 2` is exactly those
  runs of `D₀`, so `agree = 1 − 2N_ap(x₀)/521`, expectation `1 − 1/16 = 0.9375`
  at density ½. Verified **bit-exact** (difference 0.00e+00, not merely within
  tolerance) on eight cells across both bases before freeze.
- **T5, containment.** Under any base × `U++`, `D_{t+1} ⊆ {blind columns at t}`.

### 2.3 Bases: twenty

Unit five's sixteen `{110, 54, 22, 5, 30, 90, 0, 204, 106, 232, 8, 18, 46, 33,
62, 29}` plus four chosen by blind-bit count before any observable: **51**
(`β=0000`, activity 1.0), **37** (`β=0000`, active), **45** (`β=0010`,
chaotic), **27** (`β=0001`, active). All twenty `β` values asserted by value at
run time. Beam activity recorded per base; the frozen set `{0, 204, 232, 8}` is
named for P6.

### 2.4 Completions: seven arms, one namespace, per base

All from `default_rng(seed('completions'))` in this protocol's namespace, in
this order, asserted disjoint from units 4/5/6 (the `U++` exception below).

- **`U++`, all 64** — the complete cell. Members may coincide with unit six's
  `U+` arm by chance (0.8% each); any overlap is **recorded, not a failure**,
  since the cell is complete and nothing selected it.
- **`U+ \ U++`, 16** fresh (twelve lit hold, dark free).
- **`D+ \ U++`, 16** fresh (seven dark hold, lit free).
- **`G`, 24** fresh (`A≡0, B≡1, C≡1`); **`G′`, 16** fresh (`A≡1, B≡1, C≡0`).
- **`K`, 24** fresh (`A≡1, B` free, `C≡1`) — **amendment, see §4 P7.**
- **Random, 48** fresh.

208 completions × 20 bases = **4,160 evaluations**.

### 2.5 The pair-survival tier (`Π`)

For the first 16 `U++` completions of every base: four beam states
(`('pair', u, rep)`), eight origins each, and at each origin **overwrite both
rows** with an anti-phase block — row 0 `(φ, 1−φ)`, row 1 `(1−φ, φ)`. (Flipping
one row of a beam state cannot make an anti-phase pair on a uniform background;
the draft's first attempt hung on rule 0 exactly there.) 512 steps; survival
recorded at 64, 128, 256, 512. Exact endpoints: `Π = 0` for totalistic bases,
`Π = 1` for 204 and 51 — both confirmed before freeze.

### 2.6 Controls — run before any observable; any failure stops the run

1. **Algebra, exact, asserted:** the 64-window enumeration gives the
   stratification, the 8/6/15/7 partition, the pairs of §2.2, ranks 11 and 7,
   `|U++| = 64`, diagonals hold on all 8,192 `U+`, `β`-all-hold = the 16
   totalistic rules with `γ` holding on all.
2. **One-step law on real dynamics, can fail:** 64 random (base, completion,
   state) × 8 steps: `D_{t+1}` equals the window lookup column by column; and
   the strata accounting reproduces `agree` from its own counts.
3. **One-step collapse, can fail:** 0, 22, 232 × all 64 `U++` × 4 states:
   `D₁ ≡ 0`. Witness: 110 × 8 `U++` × 4 states: `D₁ ≢ 0` at least once.
4. **Identity exception through the measurement path, can fail:** for 4 `U++`
   × bases 204 and 51, the scored disagreement count equals `2·N_ap(x₀)`
   **as integers** (amendment: integer counts, not a float tolerance on
   `agree`, which removes the tolerance question entirely — the pre-freeze
   check was bit-exact); and 64 planted pairs under 64 random `A ∧ C`
   completions on 204 and 51 remain exactly width two for 512 steps.
5. **Containment on trajectories, can fail:** 8 bases × 4 `U++` × 32 steps:
   `D_{t+1} ⊆ blind(t)`; lit and dark one-step survival exactly zero.
6. **Regeneration, can fail:** the copied `evaluate` and `transverse_traced`,
   given unit six's seed function, reproduce its first 16 canonical rows
   exactly.
7. **Beam invariance, exact:** 8 completions per base, 256 steps, heights 2, 3.
8. **Matched null pairs, paired draws, can fail:** 110/137 for 8 random, 8
   `U++`, 4 `G`; 51/51 for 4 `U++`. Complemented initial states keyed on the
   original `u`. Complement conjugation permutes lit within blocks and dark
   within stars, so `U++`, `U+`, `D+`, `G`, `G′`, `K` are each closed under it
   (asserted).
9. **Disjointness**, asserted, with the `U++` exception recorded.
10. **Grower edge law on trajectories, can fail:** 4 `G` × 4 bases × 32 steps:
    the leftmost column of every cluster moves west by exactly one per step;
    mirror for `G′`. This is the control the coordinator's floor claim needs.

## 3. Frozen analysis (`evaluate.py`, committed before the run)

Per base: `ρ(r) = mean_{U++}(1 − agree)`; `P(on)` and median `agree` per arm;
`Π_h(r)`; `β` count, `e_G`, `e_{G′}`, activity. Spearman (own implementation;
scipy is not installed) of `ρ` with `Π_512` and `β`; `G` median with `e_G` and
`e_{G′}`; `G′` median with both; random median with `β` and `Π_512`; `K`
`P(on)` with `Π_512`. Strata budget per arm and base. Terminal cluster-width
census. Bootstrap over completions (2,000, seeded) for every threshold;
verdicts on point values.

## 4. Frozen predictions (odds are the drafting agent's unless marked)

- **P1 (identity exception exact; replicates on 51).** (a) All 64 `U++` × 204
  and × 51: integer identity holds and `on_beam = 0`; median `agree` in
  `[0.925, 0.950]` on each. *Calibrated:* bit-exact on 8 cells pre-freeze;
  unit six `U+` median 0.9399. Odds **0.95**. (b) `U+ \ U++` × 204 and 51:
  `|agree − formula| ≤ 0.05` in ≥ 14 of 16, `P(on) = 0`. Odds 0.8.
- **P2 (one-step collapse).** 0, 22, 232 × all 64 `U++`: `agree = 1.000`
  exactly, `on_beam = 1`, every evaluation. Odds **0.95**.
- **P3 (the blind stratum is the `U++` residual; ordered by `Π`).**
  (a) Spearman(`ρ`, `Π_512`) ≥ 0.6 over 20 bases. Odds 0.75. (b) Every base
  with `Π_512 = 0` has `ρ ≤ 0.005` and `P(on|U++) ≥ 0.95`. Odds 0.8.
  (c) The three largest `ρ` are `{204, 51, 37}`. *Margin .022 vs .013.*
  Odds **0.55 — the drafting agent expects this may fail (37 vs 45).**
- **P4 (grower floor is east-edge erosion; handed; out of sample on twelve).**
  (a) Every `e_G = 0` base `{90, 204, 51, 37, 27}` has `G` median below every
  `e_G ≥ 1` base; Spearman ≥ 0.6. Odds 0.65 strict / 0.85 Spearman. (b) Same
  for `G′` with `e_{G′}` (`0`-group `{90, 204, 51, 37, 45}`). Odds 0.7 / 0.85.
  (c) **Chirality, stated only where one score is zero:** `G′(27) − G(27) ≥
  0.05` and `G(45) − G′(45) ≥ 0.05`. *Within-base signs were unreliable on 110
  and 30, so the claim is scoped to the zero-score bases — the scoping unit
  six's P3(a) lacked.* Odds 0.6. (d) Under 51, `G` and `G′` medians ≤ 0.45.
  Odds 0.7. (e) **The coordinator's floor claim, tested:** among the 15 bases
  with `e_G ≥ 1`, `G` medians all lie in `[0.55, 0.90]`. Odds 0.6; the frozen
  bases 8 and 232 are the named risk.
- **P5 (random-arm base dependence).** Spearman(random median, `β`) ≥ 0.5 and
  with `Π_512` ≤ −0.4, over 20 bases. Odds 0.7.
- **P6 (dark bits).** (a) `|median(U+) − median(U++)| ≤ 0.02` every base. Odds
  0.8. (b) `median(D+) − median(random) ≥ 0.05` in ≥ 3 of the 4 frozen bases,
  and larger than the gap over active bases. *Uncalibrated.* Odds 0.5 —
  **expected to be the informative failure if it fails.**
- **P7 (amendment — specificity of the stratum decomposition).** `K`'s
  residual is lit-governed, not blind-governed, so `|Spearman(K P(on),
  Π_512)| ≤ 0.3` over 20 bases, while P3(a) holds for `U++` at ≥ 0.6.
  *Calibrated:* −0.10 for `K` against +0.94/+0.98/+0.98/+0.78 for the
  blind-governed cells, on unit six's eight bases. Odds 0.6 (executing
  session's). **Rationale for the amendment:** the draft dropped `K` as "not
  needed", but the drafting agent's own central argument for the stratum
  decomposition is that `K` is the one cell the blind bits do *not* order.
  That specificity is the evidence, so it is tested out of sample on twenty
  bases rather than asserted from eight. A null or negative Spearman here
  supports the decomposition; a strong positive one refutes it and would mean
  the blind bits order everything, decomposition or not.

Descriptive, unscored: strata budgets by arm; terminal width census; `Π` at
four horizons; `G` − random sign against the random level (the coordinator's
reading); activity against the random arm.

## 5. Outputs

`results/dense_defect_algebra_20260918/`: `rows.json`, `pairs.json`,
`algebra.json`, `controls.json`, `summary.json` (§3, P1–P7, source hashes).
Runner and evaluator committed before the run. Registered in
`scripts/check_result_integrity.py` with keys matching `source_hashes` exactly.
Knowledge nodes: the stratification and one-step law (finding, exact); the
identity-exception theorem with its exact residual (finding, exact); `Π` as a
measured mediator (exploratory).

## 6. Budget and stopping

≈ 2.07 s per evaluation, 0.60 s per transverse loop, 34 s per base for `Π`.
Per base: 208 × 2.07 = 431 s; transverse for random + `D+` only (theorem-fixed
elsewhere, checked on subsets in controls 3/10); `Π` 38 s; strata ≈ 5%.
≈ 505 s × 20 = 10,100 CPU-s ≈ **43 min on 3.95 cores, plus ≈ 4 min of
controls: about 47 minutes, off GitHub Actions.** Order: controls 1–10, then
`U++`, `U+`, `D+`, `G`, `G′`, `K`, random; read nothing before every tier is
written. If wall exceeds 70 min: `D+` and `G′` to 8, random to 32, recorded
before any outcome is read, full rerun. No base, completion or arm dropped for
its outcome.

## 7. Non-claims

Not a characterization of the terminal field for active bases (`Π` is measured,
exact only at its endpoints). Not height three, other densities or observers.
Not a claim about `M*`. The random-arm ordering is descriptive-grade with
frozen outliers expected. `K` enters as a specificity control, not as a
characterization of confined refinements.

## 8. Disclosed pre-freeze work

**Drafting agent's pilot** (scratchpad, namespace `pilot-u7`, not in the
repository): the 64-window enumeration; T3 and T4 permanence; the exact
formula; the reanalysis of unit six's rows giving the Spearmans quoted in P3–P5
and P7; the 256-rule enumeration that chose 51, 37, 45, 27. The pilot chose the
arms, the extra bases and every threshold; it is quoted as origin, nowhere as
evidence. The drafting agent discloses that its first containment claim
("successor defects lie in blind *defect* columns") was false — 27 of 208
violations — and was corrected to blind columns of either kind; that correction
is why `γ` is in the algebra.

**Executing session's independent verification before freeze** (scratchpad
`verify_u7_algebra.py`, `verify_u7_rank.py`, `verify_u7_t4.py`): the
stratification exact with zero mismatches; 28 pairs splitting 6/15/7; ranks 11
and 7; `|U++| = 64` by six components; the twelve a subset of the fifteen with
the diagonals implied; `β`-all-hold = the 16 totalistic rules with `γ`
holding; all twenty panel `β` values correct; planted-pair permanence 1.000 /
1.000 / 0.205 / 0.031 / 0.000×4 on 204 / 51 / 90 / 5 / {0, 22, 110, 30}; the
exact residual formula bit-exact on 8 cells; and the edge-to-`β` correspondence
re-derived from the read-index definition, matching the draft. The algebra was
not taken on report.

**Process note carried from the draft:** the pilot's `pkill -f` on a script
name killed its own shell mid-heredoc. The runner must never spawn or kill by
pattern.
