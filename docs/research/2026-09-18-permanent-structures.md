# Permanent structures: the isolated-defect gadget, and specificity fails twice

**Date:** 2026-09-18 · **Evidence:** exact (theorem) + replicated census
**Protocol:** [`2026-09-18-permanent-structures.md`](protocols/2026-09-18-permanent-structures.md), frozen before implementation, with a dated addendum written before any tier ran
**Artifacts:** `experiments/permanent_structures_20260918/`, `results/permanent_structures_20260918/`
**Program:** Class-IV Refinement, eighth unit
**Review:** gates suspended by Myk 2026-09-17. **Evaluation preceded review.** Self-gated.
**Authorship:** protocol drafted by Claude/Fable 5.1; amended, frozen, implemented, run and scored by Claude Opus 5.

## The reframing, and why it made the unit exact

The seventh unit's open question — *what orders beam residence beyond the blind
bits* — is a census question. The drafting agent declined it on two facts the
executing session verified.

**Residence is not a transient.** On every base and arm of the seventh unit, the
defect count at scored step 1 equals the count at step 256 to within 0.5%. The
field is already *permanent* when scoring begins, and on the confined arm it is
almost entirely isolated defects.

**So the question is exact.** Under `A ∧ C` an isolated defect's west flank reads
`A(LL,L)`, the defect column reads `B(L,R)`, the east flank reads `C(R,RR)`, and
columns `j±2` read exposed entries with agreeing windows. The state `(L, d₀, d₁, R)`
is therefore a deterministic **16-state automaton with a 2-bit input** `(LL, RR)`.
SAFE and DOOMED partition the 57,344 `K` completions into **`K∀` 24,576 /
`K∃` 28,672 / `K⊥` 4,096** — verified exactly, and the gadget matches the real
step with **0 mismatches of 22,270**.

## What is exact, at full scale

- **P1.** On each of the four frozen-context anchors (204, 51, 0, 8), **zero
  mismatches of 1,536 trials** — 6,144 in total. Every transverse trial's healing
  step is predicted exactly by iterating the gadget under the base's own input law.
- **P2.** **Zero bound violations of 1,728.** Every `K⊥` completion has
  `T_ext = 1` exactly; no SAFE-started trial ever healed. The partition predicts
  individual trial fates, not just aggregates.
- **T0.** `γ` is a function of `β`, so the 256 rules form **16 blocks of 16** and a
  base's exposed contribution is four bits and nothing more.
- **T1.** `|D_{t+1}| = Σ_p v_p N_p(t)` over the 28 pairs, exact at **0 of 512**.
  Residence is affine in the 22 free violation bits **at fixed census** — which is
  precisely why additivity fails in practice (P7).

## The independence horizon — a correction to this protocol's own amendment

The draft claimed 1-clusters independent at separation 2. At freeze I corrected
that to 2-clusters at separation ≥ 3. **Control 6 refuted my correction too**, 15
violations of 72 across 13 bases. Under `A ∧ C` the defect set never grows, but a
cluster perturbs the *agreeing background* — the flanks take `a(LL,L)` and
`c(R,RR)`, not what the base rule would produce — and that perturbation travels at
speed one.

| separation | 4 | 6 | 8 | 12 | 16 | 24 | 32 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| first mismatch step, minimum | 4 | 6 | 8 | — | — | — | — |
| trials with any mismatch in 128 steps | 8/36 | 3/36 | 5/36 | 0 | 0 | 0 | 0 |

**Two clusters separated by `s` agreeing columns are independent for `t < s`.** No
fixed separation gives all-time independence. The corrected control passes at
**0 of 216** on the adversarial cell.

**Why the pre-freeze check missed it.** It drew completions uniformly from `K`,
which is dominated by fast-healing classes (`K∀` alone is 24,576 of 57,344), so
defects healed before any perturbation could travel. The control used a `K∃`
completion with `|DOOMED| = 2`, where defects persist. **Verify on the adversarial
cell, not a random draw.**

## The census

3,744 evaluations, 36 bases × 7 arms, 81.2 minutes off Actions, twelve controls
first. **Held:** P1, P2, P3a, P4 (both clauses), P5a, P7b. **Failed:** P3b, P3c,
P4b, P5b, P6, P7c.

### The positive: residence is permanence

**P4 held on both clauses and strongly.** Within every one of 36 bases, the
non-blind defect count per step is ordered against `T_ext` at Spearman ≤ −0.6, and
pooled at **−0.836** against a predicted −0.7. Isolated-defect permanence is what
sets dense-start residence on the confined arm. This was the cell the argument
rested on, and it was measured on both arms.

### The negative that matters: specificity fails, correctly formed

The seventh unit's P7 claimed the stratum decomposition is *specific* — that the
blind bits order the blind-governed cells and not the lit-governed one. That test
was **mis-formed**: `K ⊂ A ∧ C` inherits a blind term identical in kind to
`U++`'s, so some ordering was guaranteed.

This unit re-formed it so the shared term is subtracted by construction. **It
fails again.** `K∀`'s *non-blind* term is ordered by pair survival at **+0.829**,
where the prediction was `|ρ| ≤ 0.4`. The blind bits order the non-blind residual
too.

So: twice, the second time under a test built specifically to be fair. The
stratum decomposition keeps its direction and does not have the specificity the
seventh unit's reading and this unit's re-formulation both looked for. That is the
finding, not a technicality.

### My design failure: P6

I chose a 36-base panel with **23 discriminating** on `e_G ≠ e_G′` — against the
seventh unit's 7 — specifically so handedness would be decided either way. Result:
**10 of 23 agreeing, against a chance expectation of 11.5.** No signal at all, yet
inside the band I had pre-registered as "still unsupported" rather than the ≤ 9 I
had called a refutation.

The frozen verdict word is *unsupported*, and that is what the record says. The
point estimate is dead on chance. Building a panel to force an answer and still
not getting one is a design failure worth naming: my banding, not the panel size,
is what left the dead zone.

### The rest

- **P3c** failed, but **not on its named risk**: 51 versus 90 behaved as predicted
  (0.859 vs 1.0). Bases 50 and 178 broke it at 0.8125, *below* the frozen anchors.
- **P3b inverted**: the base-dependent cell `K∃` is *less* spread across bases
  (0.188) than `K∀` (0.297), ratio 0.63 against a predicted ≥ 2.
- **P4b** failed at 12 of 36: the relationship is nearly as strong on the random
  arm, so the gadget's formal applicability does not by itself distinguish the
  confined arm.
- **P7b held** (max CV `R²` 0.199) and **P7c failed** (zero of 36 bases reach 0.4
  on the `K` arm). Gadget class is a function of the bits, and residence still is
  not additive in them — consistent with T1 being affine only at fixed census.

## Process

The evaluator was exercised end-to-end against a real pilot `rows.json` before
being committed as frozen — the seventh unit's was committed untested and crashed
on load. The pilot's verdicts were not read as results and nothing was tuned on
them; the pilot output was deleted.

The first canonical launch **failed controls with nothing computed**. Two failures,
different in kind: control 5 was an implementation bug of mine (the heal-class
clause keyed on a reassigned loop variable, testing the final state's membership
against the start state's guarantee — 5 → 0 under nothing but re-keying), and
control 6 was the real refutation above. **Both read "0" in the final log, but one
zero came from fixing code and the other from weakening a claim to the true one.**

One further mistake: an addendum commit used `git add -A` over live run output and
swept in the abandoned launch's artifacts. Untracked in `2784e22`. **Stage results
directories by path while a run is in flight.**

## Non-claims

Not a characterisation of the terminal field on unconfined arms beyond the
translation floor. Not a base-only predictor of residence: P3(d) and P5(c) were
the attempt and are not supported. Not height three, other densities or observers.
No claim about `M*`. The handed test is scoped to terminal 2-cluster width; its
null result says the erosion bits do not order that observable, not that chirality
has no other expression.
