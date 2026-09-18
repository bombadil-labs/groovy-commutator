# Protocol — held structures: the structural census, the six-bit gadget and the edge automaton (Class-IV Refinement, ninth unit)

**Frozen** 2026-09-18 by Claude Opus 5 (executing session), on a draft and addendum
by Claude/Fable 5.1 (planning agent). Committed before `run.py` exists.

**Protocol review:** none at freeze. Myk's 2026-09-17 suspension of the cross-model
review gates is in force. The results note must state that evaluation preceded
review. The suspension does not waive the freeze.

**Standing.** §2.2 is exact content, each clause asserted as a gating control and
standing however the census scores. The drafting agent derived every clause by hand
or index algebra and ran nothing; **the executing session verified five of six by
simulation before freeze (§8), and the sixth only in part** — that partial status is
recorded in §2.2 and is what controls 4 and 5 exist to close. Every empirical
prediction is calibrated on a reanalysis of the eighth unit's canonical rows and says
so; 10 of the 33 panel bases carry no calibration at all.

---

## 0. Why the target moved, and two corrections

**The puzzle as the executing session posed it assumed the wrong partition.** "Why do
four bits order the *non-blind* residual" takes the stratum decomposition as the right
cut. It is not. Mapping each of the 28 pairs to the local defect structure that reads
it — every pair has exactly one (§2.2 T1, verified) — shows the lit stratum straddles
two different things: **singletons** (width-one defects, the gadget's `B` pairs) and
**the interiors of alternating runs**, which are completion-held column by column and
exist only while base-held edges shield them.

Decomposing the eighth unit's own rows by structure (identity closes to 1e-13):

| `K∀`, 32 leaky bases | Spearman vs Π | vs \|β\| | range of base means |
| --- | ---: | ---: | --- |
| singletons (`B` pairs) | **+0.07** | −0.12 | 51.3–69.2 |
| alternating interiors (3 diagonals) | +0.80 | −0.82 | 0.0–42.4 |
| in-phase columns (5 dark pairs) | +0.88 | −0.84 | 2.4–19.3 |
| non-blind total (the eighth unit's +0.829) | +0.83 | −0.82 | 58.5–105.9 |

So the +0.829 is carried entirely by structures **attached to base-held edges**; the
one structure whose every column is completion-held is **flat across 36 bases**, with
the most crowded base (204) at the bottom, so this is not two effects cancelling. The
honest question is not a Spearman on a stratum but: **which columns does the base
hold, which does the completion hold, and through which channels does the base reach
the completion-held census?** Three channels are named and tested — *shielding*,
*absorption/crowding*, and *the driven input stream*.

**Correction owed to the record, and now merged (PR #278).** The eighth unit's P3(d)
and P5(c) were frozen and **never scored**: no flank-change field in the rows, no key
in the evaluator. They are **not evaluated**, not unsupported, and that unit supplies
**no evidence either way** on a base-only predictor of the `K∃` position. **P4 below
is the Program's first evaluated test of a base-only predictor**, not a replacement
for a negative result.

**Handedness is closed by theorem, not re-run.** T1 makes the assignment exact at one
step (east alternating edges read β₁/β₃, west β₂/β₄) and T5 shows why no terminal
width can isolate it: erosion is an edge automaton mixing β with the base's phase
values, the completion's dark bits and the input. The eighth unit's chance result is
explained. No handedness test is proposed.

## 1. Purpose

> (a) **Bookkeeping, exact.** Is every defect column's read decided by its junctions,
>     so blind = alternating edges and non-blind = singletons + alternating interiors
>     + in-phase columns, as integers at every step?
> (b) **The six-bit gadget, exact.** Is the gadget a function of six free bits, and are
>     the three lit diagonals equivalent to `B01`?
> (c) **Position lock and dense-field permanence, exact.** Do isolated structures never
>     move or merge, so a SAFE singleton — and, on the eight pair-permanent bases with
>     the matching pattern, an isolated alternating run — is permanent in the dense
>     field, not only in transverse trials?
> (d) **The edge automaton, exact.** Does each edge of an alternating run evolve as an
>     eight-state automaton with a one-bit input, on **both** junction branches?
> (e) **Specificity by structure, pre-registered.** Is the singleton census bounded and
>     unordered by Π off the pair-permanent class, and completion-ordered within every
>     base, while the attached terms are ordered by shielding and phase?
> (f) **The driven stream.** Does the base's *free* beam stream predict transverse fate,
>     or only the *driven* stream?

Not: height three; other densities or observers; any claim about `M*`; handedness.

## 2. Objects

### 2.1 Contract, helpers, seeds

Standing height-two contract unchanged: width 521, density 0.5, burn 512, 256 scored
transitions, six event seeds (4 train / 2 test), 64 sites; spread 4 seeds × 8 origins
at horizons 64/128; transverse 4 reps × 8 origins, 128 steps. `evaluate`,
`sample_events_full`, `transverse_gadget`, `spread_keyed`, `_initial`, `beam_state`,
`gadget`, `clusters2` are **copied** from the eighth unit's runner — not imported —
with this protocol's seed function keyed on `held-structures-20260918`, every helper
taking `seedfn` as an argument. Seeds key on `(stream, u, k, density, rep)`,
`('transverse', u, rep)`, `('pair', u, rep)`; never on the base or the table.

**Additions per scored step:** the **structural census** (singleton; alternating
interior by diagonal; in-phase edge west/east; in-phase interior; alternating edge
west/east; flank A/C; one-gap unequal/equal) with per-structure one-step survival, as
integers; the **run census** (maximal defect runs by width and junction class, how
many isolated); and at steps 1 and 256 the positions and extents of every isolated
singleton with its gadget state and every isolated alternating run. **Deviation,
justified:** the eighth unit's stratum census is kept for regeneration only; the
structural census replaces it as the scored object, because the stratum census is what
mis-formed the specificity question.

**Transverse tier, per trial:** origin window, gadget start, healing step, the **driven
stream** (`x_t[j−2], x_t[j+2]` from the perturbed strip) for 128 steps, and the **free
stream** (the same columns of the unperturbed beam under the base ECA), computed once
per `(base, rep, origin)`.

### 2.2 The exact content

Flank classes under `A ∧ C`: `α₀ = {1,2,8}`, `α₁ = {5,11,12}`, `α₂ = {19,20,26}`,
`α₃ = {23,29,30}`, each a single free bit *(verified: 0 violations of 3,200)*.

- **T1 (structural dictionary).** Each of the 28 pairs is read by exactly one local
  structure, decided by the column's two junctions. Exposed (6): alternating edges
  west `(3,18)`→β₂, `(13,28)`→β₄; east `(10,18)`→β₁, `(13,21)`→β₃; unequal one-gaps
  `(3,10)`→γ₀, `(21,28)`→γ₁. Lit (15): flanks `A`, flanks `C`, singletons `B`, and
  three interior diagonals `(11,20)`, `(5,26)`, `(12,19)`. Dark (7): in-phase edges,
  in-phase interior `(6,25)`, equal one-gaps `(4,9)`, `(22,27)`. Hence as integer
  identities: **blind = alternating-edge column-steps; non-blind = singletons +
  alternating interiors + in-phase columns.** The base holds exactly the alternating
  edges and the unequal one-gaps. *(Verified: 0 of 28 pairs read by more than one
  structure.)*
- **T2 (six-bit gadget).** `B00 ⇔ α₀ = t16`, `B01 ⇔ B10 ⇔ α₁ = α₂`, `B11 ⇔ α₃ = t15`;
  the three diagonals are each `⇔ B01`. The gadget uses only `α₀..α₃, t15, t16`, so
  there are **64 types of 1,024 completions**, and `K∀`/`K∃`/`K⊥` are unions of
  24/28/4 types. *(Verified: all 64 types present, **0 with mixed gadget class**.)*
- **T3 (position lock).** Under `A ∧ C` a structure whose columns ±1 and ±2 agree keeps
  them agreeing forever: it never moves, never merges, and interacts only through its
  input. **Corollary:** an isolated SAFE singleton is a defect at the same column
  forever, in the dense field, on every base. *(Verified on the adversarial cell —
  bases 90, 91, 218, 219, 37, 110 × small-DOOMED `K∃` × dense field: **0 moved, 0 grew,
  0 merged of 54,428 tracked structure-steps**.)*
- **T4 (interior inertness).** An interior column with an alternating junction survives
  one step iff `α₁ ≠ α₂`, then takes `α₁` (old centre 0) or `α₂` (old centre 1). A
  fully in-phase interior survives iff `(6,25)` is violated. *(Consistent with the
  eighth unit's rows: mean 0.035 interior column-steps on 1,044 `B01`-holding rows
  against 10.6 on 684 violating rows.)*
- **T5 (edge automaton).** For an isolated alternating run of width ≥ 3 the interior is
  inert, so the run changes only at its edges, each an automaton on
  `(flank L, edge value a, junction j)` with input `LL` (west; mirror east).
  *`j = alt`*: survives iff `F(L,a,¬a) ≠ F(L,¬a,a)`; then `a′ = F(L,a,¬a)`,
  `L′ = a(LL,L)`, and `j′ = alt` iff `a′ ≠ (α₂ if a = 0 else α₁)`.
  *`j = same`*: reads `(4,17)`/`(14,27)` by `L`; survives iff violated.
  **PARTIALLY VERIFIED.** The **alternating branch** is exact: 0 errors of 96 steps on
  survival, `a′`, `L′` and `j′`, across pair-permanent-opposite and chaotic cells. The
  **same-junction branch is NOT verified** — the executing session's check exits on it.
  Controls 4 and 5 exist to close that, and **control 4 must assert it exercised the
  branch** (§2.6).
- **T6 (permanent runs).** For a base with `e1 = e4 = e5 = ¬e2 = ¬e3 = ¬e6` — exactly
  **{50, 51, 76, 77, 178, 179, 204, 205}** — and a `K` completion with
  `(α₁, α₂) = (¬e2, ¬e5)`, every isolated alternating run of width ≥ 2 is permanent in
  position and extent. *(Verified: **28/28 extent kept on all eight bases**, widths 2–8,
  256 steps, matching pattern; opposite pattern only 4–7 of 28.)*
- **T7 (Π theorem).** A width-two alternating pair survives for every `(L,a,R)` iff the
  base is pair-permanent, so **Π = 1 on every beam state for exactly those eight rules**.
  *(Verified: the pair-permanence condition and T6's entry condition give the **identical
  set**.)*
- **T8 (undriven streams).** Driven equals free iff `F` depends on the centre alone:
  **{0, 51, 204, 255}**, plus rule 8 (dead beam).

### 2.3 Bases: thirty-three, selected before any observable

Selection rule stated first: (i) the **whole β = 0000 block** (16 rules), the block in
which the base holds nothing but alternating-edge survival, containing the eight
pair-permanent rules; (ii) the four frozen anchors with leaky companions; (iii) two
bases from each Π > 0 block outside 0000 (one for 1000), giving ≥ 20 leaky
non-pair-permanent bases.

| β | bases |
| --- | --- |
| 0000 | 36, 37, 50, 51, 76, 77, 90, 91, 164, 165, 178, 179, 204, 205, 218, 219 |
| 1111 | **0**, 22, 232 · 1101 | **8**, 30 · 0111 | 110 |
| 0001 | 27, 26 · 0010 | 45, 59 · 0100 | 177, 89 · 1000 | 163 |
| 0011 | 5, 18 · 1100 | 54, 33 |

Asserted at run time: 33 bases, all β by value, block 0000 complete at 16, the
pair-permanent set by T6's entry condition at 8, centre-only `{0, 51, 204}`, rule 8's
beam all-zero at every planting site.

### 2.4 Completions: six arms, 64 per base

From `default_rng(seed('completions'))`, in order, asserted disjoint from units 4–8
(the `U+` coincidence recorded, expected ≈ 3%): **`K∀⁺` 12** (6 with `(α₁,α₂) = (0,1)`,
6 with `(1,0)`), **`K∀⁻` 8** (`B01` holds), **`K∃` 16** (4 with `|DOOMED| ≤ 2`, 12
uniform), **`U+` 4**, **`G` 8**, **random 16**. 64 × 33 = **2,112 evaluations**,
transverse on all. `K⊥` dropped: theorem-trivial.

### 2.5 Pair-survival tier

As the eighth unit's, 8 `U++` per base. Endpoints asserted: 1 on the eight
pair-permanent bases, 0 on totalistic bases.

### 2.6 Controls — before any observable; each can fail; any failure stops the run

**Look at the adversarial cell first, and assert the cell was reached.**

1. **Algebra, asserted:** T1's dictionary with one structure per pair; the four flank
   classes; 64 types with constant gadget class, 24/28/4; diagonals ⇔ `B01`; T0; block
   0000 = the 16 listed; pair-permanent = the 8 listed; centre-only = `{0,51,204,255}`.
2. **Structural census identity on real dynamics, can fail:** `|D_{t+1}| = Σ v·N` as
   integers; blind = alternating-edge count; per-structure survival = the structure's
   violation bit.
3. **Position lock (T3) on the adversarial cell, can fail:** 90-class and 37, 110, 30 ×
   4 small-DOOMED `K∃` × dense starts × 64 steps: no move, no growth, no merge.
   **Witness that must fail:** a random non-`A ∧ C` completion.
4. **Edge automaton (T5) against dynamics, can fail — AMENDED:** isolated alternating
   runs of widths 3–8 on 12 bases × 12 `K` completions × 8 origins × 64 steps; each
   edge's `(L, a, j)` and each shrink event predicted from the observed input, zero
   mismatches. **The control MUST additionally assert that the `same`-junction branch
   was exercised at least 50 times, and fail if it was not.** An unexercised branch is
   an ungated one, and that branch is the only part of T5 unverified at freeze.
   **Witness:** under a random completion the interior is not inert.
5. **Permanent runs (T6), can fail — AMENDED:** all eight pair-permanent bases ×
   matching-pattern `K` × planted runs of widths 2–8 × 256 steps: extent unchanged.
   **Witness, corrected:** with the opposite pattern the **junction type** must convert
   at step 1. The draft stated this on *extent*; the executing session measured extent
   at step 1 and it never changes — the junction converts without the run shrinking, so
   the witness as drafted could not fire.
6. **Gadget on the driven stream, all 33 bases, can fail.**
7. **Free = driven (T8), can fail:** identical on `{0, 51, 204, 8}`; **witnesses:** 90
   and 110 must diverge within 4 steps.
8. **Regeneration, can fail:** the copied helpers reproduce the eighth unit's first 16
   canonical rows exactly.
9. **Beam invariance:** heights 2 and 3.
10. **Matched null pairs, paired draws, can fail:** every scalar to 1e-9, every census
    vector as integers.
11. **Disjointness**, with the `U+` coincidence recorded.
12. **Panel assertions** (§2.3).
13. **Evaluator exercised against pilot rows before freeze**; pilot output deleted,
    nothing tuned on it.
14. **Scored set equals frozen set, can fail — the rule earned from PR #278.** The
    frozen key list below is parsed by the runner. Before any tier, `evaluate.py
    --pilot` runs against control-phase pilot rows and its prediction-key set is
    compared to the list. **Falsifier:** any frozen key absent from the output, or any
    output key not in the list, stops the run. A prediction the evaluator deliberately
    does not score must appear with an explicit `not_evaluated: <reason>` in
    `summary.json`, so **"unscored" is a recorded verdict and never an absence**. The
    eighth unit's evaluator would have failed this at 11 keys against 13.

```frozen-prediction-keys
P1a P1b P2a P2b P2c P3a P3b P3c P3d P4a P4b P4c P4d
P5a-i P5a-ii P5a-iii P5b P5c P5d P6a P6b
```

## 3. Frozen analysis (`evaluate.py`, committed before the run)

Per (base, completion): `agree`; the structural census per step; run census; `T_ext`
with gadget bounds; **singletons per step `S`**, **alternating interiors `I`**,
**in-phase `Q`**; `|SAFE|`, `|DOOMED|`, `(α₁, α₂)`, gadget type; isolated-structure
permanence counts (step 1 → 256); per-trial healing step and the driven- and
free-stream gadget predictions. Per base: β, phase class, pair-permanent flag,
centre-only flag, `Π_512`. Spearman (own implementation); sign tests as counts;
bootstrap over completions (2,000, seeded); verdicts on point values. **The evaluator
scores every key in the frozen list or writes `not_evaluated` with a reason under that
key; control 14 asserts the two sets are equal before any tier runs.**

## 4. Frozen predictions (odds are the drafting agent's unless marked)

- **P1 (bookkeeping, exact).** (a) blind = alternating edges and non-blind = `S+I+Q` as
  integers at every scored step of every row. (b) Per-structure one-step survival equals
  the violation bit of that structure's pair. Odds **0.95** each.
- **P2 (dense-field permanence, exact).** (a) Every isolated SAFE singleton at step 1 is
  a defect at the same column at step 256, every `K` row: 0 violations. (b) On the eight
  pair-permanent bases × matching-pattern completions, every isolated alternating run
  has identical extent at step 256: 0 violations. (c) `Π_512 = 1.000` on all eight
  pair-permanent bases and < 1 on the other eight block-0000 bases. Odds 0.85 / 0.8 /
  0.85. *Named risk for (a): a merge through a two-gap; control 3 looks there first.*
- **P3 (the singleton census).** (a) `K∀` mean `S` in **[40, 80]** on every base.
  *Calibrated 51.3–69.2.* Odds 0.7; **named risk: 76, 77, 205.** (b) Within every base,
  Spearman(`S`, `|SAFE|`) ≥ 0.7 over the 36 `K∀ ∪ K∃` completions. *Calibrated
  0.79–0.96 on nine bases.* Odds 0.75. (c) Over the 23 leaky non-pair-permanent bases,
  `|Spearman(S, Π_512)| ≤ 0.4`. *Calibrated +0.07 on 32.* Odds 0.65. (d) The lowest `S`
  on the panel is a pair-permanent base. Odds 0.7.
- **P4 (the driven stream — the Program's first evaluated test of a base-only
  predictor).** (a) On `{0, 51, 204, 8}` the free-stream gadget reproduces every
  transverse healing step as an integer. Odds 0.9. (b) On the 90-class and 110, free and
  driven first differ at step ≤ 4 in ≥ 90% of trials. Odds 0.7. (c) Pooled over `K∃`
  trials on the 29 driven bases, the free-stream proxy's healed-by-128 outcome agrees
  with the actual in ≥ 90% of trials. Odds **0.4 — expected to fail**; a failure would
  be the first evidence that no free-stream statistic can predict the `K∃` position, a
  hold the first evidence that one can. (d) Spearman(actual `T_ext`, free-proxy `T_ext`)
  ≥ 0.7 over `K∃` rows on driven bases. Odds 0.5.
- **P5 (the attached terms: shielding and phase, not Π).** (a)(i) `I ≤ 5` per step on
  every `K∀⁻` and `U+` row. Odds 0.8. (ii) On every Π = 0 base the `K∀⁺` mean `I ≤ 5`.
  Odds 0.75. (iii) On every pair-permanent base the matching-pattern sub-arm has `I ≥ 10`
  on ≥ 5 of 6. Odds 0.75. (b) On each pair-permanent base the matching sub-arm's median
  `I` exceeds the opposite pattern's, 8 of 8. Odds 0.8. (c) Within block 0000,
  Spearman(`K∀⁺` mean `I`, `Π_512`) ≤ 0.5 over the 16 bases. Odds 0.6. (d) The eighth
  unit's in-phase ordering replicates: Spearman(`K∀` mean `Q`, `Π_512`) ≥ 0.5 over the
  29 leaky bases. Odds **0.45 — expected to weaken**, half the panel being one block.
- **P6 (movers, absorption).** (a) On the `G` arm, `S` ordered by Π at ≤ −0.6 over leaky
  bases. Odds 0.7. (b) The random arm's `S` ordered by Π at ≥ +0.5. Odds 0.65. These are
  the witnesses that P3(c) is specific to `A ∧ C`.

Descriptive, unscored: run-width spectrum by junction class; predicted erosion rate
against observed run lifetimes; driven/free divergence step; quiescence variants within
each phase class; `S` on the ten uncalibrated bases.

## 5. Outputs

`results/held_structures_20260918/`: `rows.json`, `pairs.json`, `gadget.json`,
`algebra.json`, `controls.json`, `summary.json` (with `source_hashes` **and the frozen
key list verbatim**, so a later edit to either side surfaces in the fast tier).
Registered in `scripts/check_result_integrity.py`. Knowledge nodes: the structural
dictionary and the held/completion-held split; the six-bit gadget and four flank
classes (refining `isolated-defect-gadget`); position lock and dense-field permanence;
the edge automaton; the pair-permanent rules and the Π theorem — each `finding/exact`.
The eighth unit's specificity finding is **annotated, not retracted**: its direction
stands, its non-blind term is now known to straddle two structures.

## 6. Budget and stopping

≈ 4.6 s per row × 2,112 ≈ 9,700 core-s ≈ **41 min on 3.95 cores**, plus ≈ 4 min of
controls and ≈ 5 min for the Π tier: **about 50 minutes, off GitHub Actions** (the last
four took 46, 37, 58, 81 — 81 was drifting high and this panel is smaller). If wall
exceeds 65 min: random to 8 and `G` to 4, recorded before any outcome is read, full
rerun. No base, completion or arm dropped for its outcome. Stage the results directory
by path; never `git add -A`.

## 7. Non-claims

Not a characterisation of the census on unconfined arms beyond P6's two signs. Not a
claim that the singleton census is exactly base-independent — P3(a) is a band and
crowding is a predicted channel. Not height three, other densities or observers. No
claim about `M*`. **Handedness is not tested** (closed by theorem, §0). The 50/51/178
near-identity of base means in the eighth unit is a mean-level coincidence (5 of 32 rows
identical) and is not a claim.

## 8. Disclosed pre-freeze work

**Drafting agent's pilot** (scratchpad only; **no dynamics run**): the 64-window
enumeration; union-find under `A ∧ C`; the 256-rule enumeration by β, phase and
quiescence class; and a reanalysis of the eighth unit's 3,744 canonical rows giving
every Spearman and range quoted in §0 and §4. The pilot chose the arms, the panel and
every threshold; quoted as origin, nowhere as evidence. One bookkeeping slip disclosed:
its first structural decomposition counted equal-flank one-gaps as defect columns and
failed to close by up to 224; the corrected five-pair in-phase set closes to 1e-13,
which is why §3 defines `Q` on defect columns only.

**Executing session's verification before freeze** (scratchpad `verify_u9*.py`):

| claim | cell | result |
| --- | --- | --- |
| T1 | — | **0 of 28** pairs read by more than one structure |
| T2 | — | all **64 types**, **0 mixed class**; flank classes single-bit, 0 of 3,200 |
| T3 | 90/91/218/219/37/110 × small-DOOMED `K∃` × dense | **0 moved, 0 grew, 0 merged of 54,428** |
| T6 | widths 2–8 × 8 pair-permanent bases × 256 steps | **28/28 kept** matching; 4–7/28 opposite |
| T7 | — | pair-permanence set **identical** to T6's entry condition |
| T5 | pair-permanent-opposite and chaotic | **alt branch 0 errors of 96**; **same branch untested** |

**Two amendments the executing session owes, both of one kind — a check that cannot
fire gates nothing.** Control 5's witness moved from extent to junction type; control 4
must assert it exercised the same-junction branch ≥ 50 times. The same failure mode has
now cost this Program three ways: a control that ran after the tiers, a verification
that sampled the easy population, and an evaluator test that caught crashes but not
completeness.

**Process rules carried forward:** seeds keyed on the completion, never the base;
helpers copied, never imported; controls before observables, on the adversarial cell,
and asserted to have reached it; a specificity claim must name what the base holds
before it is tested; the evaluator tested against pilot rows *and* the frozen key list
before it is called frozen; stage results by path.
