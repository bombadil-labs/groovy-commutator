# Protocol — permanent structures: the isolated-defect gadget and what the base does beyond its four bits (Class-IV Refinement, eighth unit)

**Frozen** 2026-09-18 by Claude Opus 5 (executing session), on a draft by
Claude/Fable 5.1 (planning agent). Committed before `run.py` exists.

**Protocol review:** none at freeze. Myk's 2026-09-17 suspension of the
cross-model review gates is in force. The results note must state that
evaluation preceded review. The suspension does not waive the freeze.

**Standing.** §2.2 is exact content, each clause asserted as a gating control
and standing however the census scores. Every empirical prediction is
calibrated on a reanalysis of the seventh unit's canonical rows (20 bases) plus
the drafting agent's pilot, and says so; 16 of the 36 panel bases carry no
calibration at all.

---

## 0. Why the target moved, and one correction the draft owes the record

The seventh unit's open question — "what orders beam residence beyond the blind
bits" — is a census question, and answered by regression it would make a weak
unit. The drafting agent declined it and reframed, for two reasons the
executing session verified:

**Residence is not a transient.** On every base and arm of the seventh unit,
the defect count at scored step 1 equals the count at step 256 to within 0.5%.
By the time scoring begins the field is a *permanent structure*, and on the
confined arm it is almost entirely **isolated defects** (K's cluster count
equals its defect count to within 10% on 16 of 20 bases). So the question is
which (base, completion) pairs support permanent isolated defects — and that is
exact, because an isolated defect under `A ∧ C` is a **16-state automaton with
a 2-bit input**.

**P7 was mis-formed, not merely under-armed.** `K ⊂ A ∧ C`, so K inherits a
blind term identical in kind to `U++`'s; its `P(on)` was *guaranteed* to be
ordered by `Π` to some degree, and the seventh unit's −0.454 is that term
showing through. The specificity claim was never the right test. **A
specificity claim must subtract the shared term exactly before it is tested, or
it tests nothing.** This unit separates the terms by construction and tests the
residue.

## 1. Purpose

> (a) **Exactness.** On the four frozen-context bases, is every transverse
>     trial's fate — and the dense K residual — predicted exactly by the
>     isolated-defect automaton, as integers, through the real measurement path?
> (b) **Bounds.** On every base, does `T_ext` lie inside
>     `[P_μ(DOOMED), 1 − P_μ(SAFE)]`, with DOOMED healing within 8 steps and
>     SAFE never?
> (c) **The base's contribution.** In the base-dependent cell `K∃`, how does
>     `T_ext` order, and does it separate frozen from chaotic bases *within* the
>     `β = 0000` block, where the blind bits are identical by construction?
> (d) **Residence is permanence.** Does isolated-defect permanence order
>     dense-start non-blind residence on the confined arm, and less well on the
>     unconfined arms?
> (e) **Handedness, with power.** On 23 bases with `e_G ≠ e_G′`, does the arm
>     with the larger erosion score have the narrower terminal clusters?
> (f) **Census identity.** Is `|D_{t+1}| = Σ_p v_p N_p(t)` exactly, so
>     residence is affine in the 22 free violation bits at fixed census?

Not: height three; other densities or observers; any claim about `M*`; a
base-only predictor of residence in general.

## 2. Objects

### 2.1 Contract, helpers, seeds

Standing height-two contract unchanged: width 521, density 0.5, burn 512, 256
scored transitions, six event seeds (4 train / 2 test), 64 sites; spread 4 seeds
× 8 origins at horizons 64/128; transverse 4 reps × 8 origins, 128 steps.
`evaluate`, `sample_events_strata`, `transverse_plain`, `spread_keyed`,
`_initial`, `beam_state` are **copied** from the seventh unit's runner — not
imported — with this protocol's seed function keyed on
`permanent-structures-20260918`, every helper taking `seedfn` as an argument.
Seeds key on `(stream, u, k, density, rep)`, `('transverse', u, rep)`,
`('pair', u, rep)`; never on the base or the table.

Additions to the events loop, per scored step: the **28-pair census** `N_p(t)`
via a 64-entry window LUT; per-pair one-step survival; the **2-cluster census**
(see §2.2 T6) with widths; for each isolated defect its gadget state and class;
and an **edge census** for `G`/`G′`. Transverse trials additionally record the
five-cell origin window, the gadget start state, its class, and the healing step.

### 2.2 The exact content

- **T0.** `γ₀ = 1 ⊕ β₁ ⊕ β₂` and `γ₁ = 1 ⊕ β₃ ⊕ β₄`. The six exposed pairs
  carry four bits; the 256 rules fall into **16 β-blocks of exactly 16**.
  *(Verified before freeze for all 256 rules.)*
- **T1 (census identity).** `|D_{t+1}| = Σ_{p=1}^{28} v_p(u, r) · N_p(t)`, with
  six violation bits decided by `β` via T0 and 22 by `u`. So `1 − agree` is
  exactly affine in the 22 violation bits **at fixed census**; what defeats
  additivity is that the census depends on the completion.
- **T2 (the isolated-defect gadget).** Under a completion satisfying `A ∧ C`,
  an isolated defect at `j` has its west flank read `A(LL, L)`, the defect
  column read `B(L, R)`, and its east flank read `C(R, RR)`; columns `j±2` read
  exposed entries with agreeing windows. So `(L, d₀, d₁, R)` evolves as a
  deterministic automaton on **8 defect states plus an absorbing healed class,
  with input `(LL, RR)`**. **SAFE** = greatest set closed under every input;
  **DOOMED** = least set containing healed and closed under "every input leads
  in". Over the 65,536 `A ∧ C` completions: `U+` (8,192) is entirely
  `|DOOMED| = 8`; the 57,344 K completions split **K∀ 24,576 / K∃ 28,672 /
  K⊥ 4,096**. *(Verified before freeze: gadget matches the real step with 0
  mismatches; all nine class sizes exact.)*
- **T3 (frozen-context exactness).** On **204** (constant input), **51**
  (alternating), **0** and **8** (constant `(0,0)`), the input sequence is
  determined by the base alone, so every transverse trial's fate is a function
  of its five-cell origin window and the completion. *(Verified before freeze:
  far-field deviation exactly 0 over 64 steps on all four; chaotic witnesses 110
  and 90 deviate by 29 and 115.)*
- **T4 (bounds on every base).** `P_μ(DOOMED) ≤ T_ext ≤ 1 − P_μ(SAFE)` with `μ`
  the beam's three-window measure; the two extreme classes are predicted exactly
  per trial. The width of the interval is the room the base has.
- **T5 (translation under growers).** Under `G` an isolated defect moves west
  exactly one column per step and stays isolated, on every base, forever. So the
  `G` residual has a floor of permanent width-one translators and `e_G` can act
  only on clusters of width ≥ 2. Mirror for `G′`.
- **T6 (no growth, and the independence radius) — AMENDED AT FREEZE.** Under
  `A ∧ C` a cluster never grows. **The draft claimed independence for
  1-clusters (runs allowing single gaps) separated by two columns; that is
  false.** Two defects three columns apart *do* interact, on 3–5 of 40 trials
  even on the frozen anchors, always first at step 3 — a flank perturbation
  crossing a two-gap at speed one. The verified object is the **2-cluster**
  (runs allowing gaps of up to 2), independent at separation **≥ 3 agreeing
  columns**: mismatches are exactly **0 of 40** at distances 4, 6, 8, 12 and 20.
  **The independence does not require frozen context** — it is a locality
  property of `A ∧ C` and holds on chaotic bases too (110 verified at 0 of 40).
  So the dense decomposition clause applies to **all 36 bases**, not the four
  anchors, and is a stronger control than drafted. At scored time the field
  really does decompose: 27–51 separate 2-clusters of mean width 0.5–5.6.

### 2.3 Bases: thirty-six, selected before any observable

Four frozen anchors (204, 51, 0, 8); every β-block with `e_G ≠ e_G′` carries at
least two members; the `β = 0000` block carries two frozen and four leaky bases
with identical exposed bits. **23 bases have `e_G ≠ e_G′`**, against 7 in the
seventh unit — the panel change that gives P6 power.

| β | e_G, e_G′ | bases |
| --- | --- | --- |
| 0000 | 0, 0 | **204, 51** (frozen), 90, 37, 50, 178 |
| 1111 | 2, 2 | **0** (frozen), 22, 232 |
| 1101 | 1, 2 | **8** (frozen), 30, 31 |
| 0001 | 0, 1 | 27, 114, 26 |
| 0010 | 1, 0 | 45, 59, 58 |
| 0100 | 0, 1 | 177, 89 |
| 1000 | 1, 0 | 163, 75 |
| 0101 | 0, 2 | 25, 102 |
| 1010 | 2, 0 | 67, 60 |
| 0111 | 1, 2 | 110, 7 |
| 1011 | 2, 1 | 106, 21 |
| 1110 | 2, 1 | 62, 87 |
| 0011 | 1, 1 | 5, 18 |
| 1100 | 1, 1 | 54, 33 |

*(Verified before freeze: 36 bases, zero mislabelled β, no duplicates, 23
discriminating, every discriminating block with ≥ 2 members.)* All 36 β values
asserted by value at run time; the frozen property of the anchors by simulation.

### 2.4 Completions: seven arms, one namespace, per base

From `default_rng(seed('completions'))` in this namespace, in order, asserted
disjoint from units 4–7 except `U++`: **`U++` 8**; **`K∀` 16, `K∃` 16, `K⊥` 16**
drawn uniformly within each gadget class (enumerated exactly at run time, sizes
asserted); **`G` 12, `G′` 12**; **random 24**. 104 × 36 = **3,744 evaluations**,
transverse on all.

### 2.5 The pair-survival tier

As the seventh unit's, on the 8 `U++` completions per base. Endpoints asserted:
0 on totalistic bases, 1 on 204 and 51.

### 2.6 Controls — before any observable; each can fail; any failure stops the run

1. **Algebra** (seventh unit's control 1 verbatim) plus T0 on all 256 rules.
2. **Census identity on real dynamics:** 64 random (base, completion, state) × 8
   steps, `|D_{t+1}| = Σ_p v_p N_p(t)` exactly; strata equal the pair sums.
3. **Gadget derivation:** all 64 (state, input) pairs read the named A/B/C
   pairs; class sizes exact; `U+` entirely `(0,8)`; DOOMED depth ≤ 8.
4. **Frozen context:** 204, 51, 0, 8 × 8 completions × 128 steps, far field
   carries the base's own beam trajectory. **Witness:** 110 and 90 must fail.
5. **Gadget against dynamics:** 16 K × 8 bases × 8 planted defects × 64 steps,
   simulated state equals the gadget's given the observed input, zero
   mismatches; DOOMED heals by 8, SAFE never.
6. **Frozen-context exactness through the measurement path (T3):** healing steps
   equal the gadget's as integers; and the dense field equals the union of
   per-**2-cluster** isolated simulations, as integer counts. **Amended: run on
   all 36 bases, not only the anchors** (T6).
7. **No growth of 2-clusters under `A ∧ C`:** 8 K × 8 bases × 32 steps, every
   hull at `t+1` inside a hull at `t`. **Witness:** under `G` the west edge
   advances by one per step.
8. **Translation under `G`/`G′` (T5):** 4 × 8 bases × 8 defects × 64 steps.
9. **Regeneration:** the copied helpers, given the seventh unit's seed function,
   reproduce its first 16 canonical rows exactly.
10. **Beam invariance:** heights 2 and 3.
11. **Matched null pairs, paired draws:** 110/137 across arms, 51/51 for `U++`;
    every scalar to `1e-9` and every census vector as integers.
12. **Disjointness**, with the `U++` exception recorded.

## 3. Frozen analysis (`evaluate.py`, committed before the run)

Per (base, completion): `agree`; blind/lit/dark column-steps per step; 28-pair
census means; `T_ext` with the gadget bounds and the trial's position inside
them; isolated-defect count and SAFE fraction; mean terminal 2-cluster width
**defined as total defect column-steps ÷ total cluster count over steps with at
least one cluster** — never a per-row ratio, which the draft's pilot showed
produces division artefacts. Per base: `Π_512`, `β`, `e_G`, `e_G′`, frozen flag,
beam activity, flank-change rate. Spearman (own implementation); sign tests as
counts; bootstrap over completions (2,000, seeded); verdicts on point values.

**Process debt cleared this unit:** the evaluator is exercised against a pilot
`rows.json` before it is committed as frozen. The seventh unit's was committed
untested and needed two post-freeze edits.

## 4. Frozen predictions (odds are the drafting agent's unless marked)

- **P1 (exactness on the frozen anchors).** Every transverse trial on 204, 51,
  0, 8 matches the gadget's healing step as an integer; the dense union identity
  holds at every checked step. Odds **0.9**.
- **P2 (bounds; extreme cells exact).** On all 36 bases and all 48 K
  completions, `T_ext ∈ [P_μ(DOOMED), 1 − P_μ(SAFE)]`; every `K⊥` has
  `T_ext = 1`; every SAFE-started `K∀` trial has healing step 129. Odds **0.9**.
- **P3 (the base's contribution lives in `K∃`).** (a) Median `T_ext` orders
  `K⊥ = 1 > K∃ > K∀` on every base. Odds 0.8. (b) The `K∃` spread exceeds the
  `K∀` spread by ≥ 2×. Odds 0.7. (c) **Within `β = 0000`**, 204 and 51 have
  `K∃` median `T_ext` below all four of 90, 37, 50, 178, and `K∃` non-blind
  residual above all four. Odds **0.55 — named risk: 51 versus 90**. (d) Across
  the ≥ 30 leaky bases, `K∃` median `T_ext` is ordered by the base's 1D
  flank-change rate at Spearman ≥ 0.5. Odds **0.45 — expected to fail**, stated
  because the absence of a base-only predictor deserves to be on the record with
  power.
- **P4 (residence is permanence).** Within every base, Spearman of non-blind
  defects per step against `T_ext` over the 48 K completions ≤ −0.6; pooled
  ≤ −0.7. Odds 0.7 pooled, 0.5 for "every base". (b) The same on the random arm
  is weaker by ≥ 0.2 in ≥ 24 of 36 bases. Odds 0.6. **This is the cell the
  argument rests on and it is measured on both arms.**
- **P5 (specificity, correctly formed).** (a) K's blind term is ordered by
  `Π_512` at ≥ 0.75. Odds 0.75. (b) `K∀`'s non-blind term is ordered by `Π_512`
  at `|ρ| ≤ 0.4` over the 32 leaky bases. Odds 0.5. (c) `K∃`'s non-blind term is
  ordered by flank-change rate at ≤ −0.4. Odds 0.45 — expected to fail with P3(d).
- **P6 (handedness, with power).** On the 23 discriminating bases,
  `sign(w̄_G − w̄_G′) = sign(e_G′ − e_G)` in ≥ 14 of 23 supports; ≤ 9 refutes;
  10–13 is recorded as still unsupported. *Calibrated 4 of 7 on the old panel —
  chance.* Odds **0.4 — expected to fail, and a failure here is decisive rather
  than underpowered.** (b) Edge census as an integer identity per row. Odds 0.95.
- **P7 (census identity and the death of additivity).** (a) T1 exact on every
  row. Odds 0.95. (b) Within-base CV `R²` of `1 − agree` on the 22 violation
  bits ≤ 0.3 on every base for the random arm. Odds 0.8. (c) On the K arm the
  same `R²` is ≥ 0.4 in ≥ 24 bases. Odds 0.55.

Descriptive, unscored: the 28-pair budget by arm and base; SAFE fraction against
beam activity; `T_ext` position inside the gadget interval; terminal width
distributions; the random arm's width spectrum.

## 5. Outputs

`results/permanent_structures_20260918/`: `rows.json`, `pairs.json`,
`gadget.json`, `algebra.json`, `controls.json`, `summary.json` (with
`source_hashes`). Registered in `scripts/check_result_integrity.py` with keys
matching exactly. Knowledge nodes: the isolated-defect gadget with its three
classes (finding, exact); the census identity and affine law (finding, exact);
the 2-cluster independence radius (finding, exact).

## 6. Budget and stopping

≈ 105 s of controls plus ≈ 305 s per base × 36 ≈ **51 minutes on 3.95 cores**,
off GitHub Actions (the last three took 46, 37, 58). Order: controls 1–12, then
`U++`, `K∀`, `K∃`, `K⊥`, `G`, `G′`, random. If wall exceeds 75 min: random to
16, `G`/`G′` to 8, recorded before any outcome is read, full rerun. No base,
completion or arm dropped for its outcome.

## 7. Non-claims

Not a characterisation of the terminal field on unconfined arms beyond the
translation floor. Not a base-only predictor of residence — P3(d) and P5(c) are
the attempt and are expected to fail. Not height three, other densities or
observers. No claim about `M*`. The handed test is scoped to terminal width; a
refutation says the erosion bits do not order width, not that chirality has no
other expression.

## 8. Disclosed pre-freeze work

**Drafting agent's pilot** (scratchpad only): enumeration of all 256 rules by
`β`, `γ`, `e_G`, `e_G′`; reanalysis of the seventh unit's 4,160 rows (snapshot
flatness; K cluster ≈ defect counts; blind term vs `Π` 0.79, non-blind 0.62;
**no base-only predictor found**, `|ρ| ≤ 0.36` for five candidates); the gadget
and its class sizes; the width-based handed sign test at 4 of 7 on the old
panel. The pilot chose the arms, the panel and every threshold; it is quoted as
origin, nowhere as evidence. The draft discloses a per-row division artefact in
its first width computation, which is why §3 fixes the ratio-of-sums definition.

**Executing session's independent verification before freeze** (scratchpad
`verify_u8*.py`): T0 exact on all 256; 16 blocks of 16; 160 rules with
`e_G ≠ e_G′`; the gadget matching the real step with **0 mismatches**;
`|A∧C| = 65536`, `|U+| = 8192`, `|K| = 57344`; **all nine gadget class sizes
exact**, `K∀` 24576 / `K∃` 28672 / `K⊥` 4096; no-growth 0 violations of 7,200
steps; frozen context exactly 0 on 204, 51, 0, 8 with witnesses 110 and 90
failing; the panel validated at 36 bases, zero mislabelled, 23 discriminating;
**and the draft's gap-2 independence claim refuted**, with the corrected
2-cluster radius established at 0 of 40 for distances 4, 6, 8, 12, 20 on frozen
and chaotic bases alike (T6).

**Process rules carried forward:** seeds keyed on the completion, never the
base; helpers copied, never imported; the runner never spawns or kills by
pattern; a specificity claim must subtract the shared term before it is tested;
and the evaluator is tested against pilot rows before it is called frozen.
