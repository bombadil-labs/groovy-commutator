# The dense defect algebra: 28 pair-constraints, stratified by popcount

**Date:** 2026-09-18 · **Evidence:** exact (theorem) + replicated census
**Protocol:** [`2026-09-18-dense-defect-algebra.md`](protocols/2026-09-18-dense-defect-algebra.md), frozen before implementation
**Artifacts:** `experiments/dense_defect_algebra_20260918/`, `results/dense_defect_algebra_20260918/`
**Program:** Class-IV Refinement, seventh unit
**Review:** gates suspended by Myk 2026-09-17. **Evaluation preceded review.** Self-gated.
**Authorship:** protocol drafted by Claude/Fable 5.1; amended, frozen, implemented, run and scored by Claude Opus 5.

## The theorem

Every column of a height-two strip has both rows read one table entry each. Row `r`
at column `j` reads `16x_r[j] + 8x_r[j−1] + x_r[j+1] + 2s_{r′}(j)`, where `s` is a
row's three-cell popcount. With `Δ_j = s₁(j) − s₀(j)`:

| `\|Δ\|` | both rows read | pairs |
| --- | --- | ---: |
| 0 | exposed — owned by the base ECA | 6 |
| 1 | lit | 15 |
| ≥ 2 | dark | 7 |

The 64 six-bit windows give 8 trivially agreeing cases and 28 unordered pairs, with
**no mixed pair**. This **characterizes** the previous unit's 8/14/10 entry partition
rather than enumerating it: the counts were 8, 14 and 10 because of what two rows'
popcounts can do at a column. GF(2) ranks are 11 (lit) and 7 (dark) over 24 free
entries, leaving exactly **64** completions that satisfy every free constraint
(`U++`), one per connected component. The previous unit's twelve constraints are a
subset of the fifteen; the three extra are diagonals of a hexagon and are implied.

Three consequences, all asserted as gating controls:

- **T3.** β-all-hold ⇔ the base is totalistic (exactly 16 rules), and then γ holds
  too. Totalistic base × `U++` ⇒ every column agrees after one step, from every state.
- **T4.** Under 204 and 51, anti-phase width-two runs with agreeing flanks are fixed
  for every `A ∧ C` completion; under `U++` the disagreement field is exactly those
  runs, so `agree = 1 − 2N_ap(x₀)/521`, expectation `0.9375`.
- **T5.** Under any base × `U++`, disagreement survives only through blind columns.

## It corrects the coordinator, not the record

Reviewing the previous unit I proposed that the identity exception is about the base
contributing no mixing — that under rule 204 nothing carries a dense state onto the
beam. **That is wrong.** Rule 51 flips every cell every step, maximal activity, and
has the *identical* exact residual; totalistic rule 0 heals every planted pair.
Measured before freeze, 64 completions × 8 origins × 512 steps:

| base | 204 | 51 | 90 | 5 | 0, 22, 110, 30 |
| --- | ---: | ---: | ---: | ---: | ---: |
| planted-pair permanence | 1.000 | 1.000 | 0.205 | 0.031 | 0.000 |

Activity is irrelevant. What decides survival is whether the base's exposed entries
reproduce a disagreement on two equal-popcount windows — four bits. The drafting
agent declined the floor/carry decomposition I proposed and defended a sharper one,
by stratum of the read; I verified the algebra independently and accepted it, and my
floor claim entered as a prediction with its own control rather than an assumption.

## Census

20 bases × 7 arms × 208 completions = **4,160 evaluations**, 57.8 minutes off
Actions. All ten controls passed first, in 170 s.

**Held: P1a, P1b, P2, P3a, P3b, P3c, P4d, P6a. Failed: P4c, P4e, P5, P6b, P7.**
P4a and P4b split: the Spearman clause held (0.687, 0.770), strict separation did not.

The exact content confirms at full scale. Under 204 and 51 every one of the 64 `U++`
completions satisfies the integer identity with zero mismatches, and the two bases
give a **bit-identical** median of `0.9366602687140115` with strata `[50392, 0, 0]` —
all blind, zero lit, zero dark. That identity is not a coincidence and not a bug: the
same two bases differ sharply on every other arm (`G` median 0.455 vs 0.081, random
0.776 vs 0.547). It is T4 doing what it claims — the residual is fixed by the initial
disagreement field, and seeds key on the completion rather than the base, so two
different `β = 0000` bases inherit the same anti-phase set. Totalistic bases 0, 22
and 232 collapse to `agree = 1.000` exactly on all 64 (T3). `ρ` tracks pair survival
at Spearman **0.934**, and all twelve bases with `Π = 0` have `ρ ≤ 0.005` and
`P(on) ≥ 0.95` with no violations. **P3c held at odds 0.55** — the drafting agent's
named risk did not fire.

### Four failures, three of them mine

**P4e, the floor claim, is refuted.** I read a base-indifferent grower floor of ~0.75
off eight bases. On twenty, bases 54 and 18 sit at **0.316** and **0.279**, far
outside the predicted `[0.55, 0.90]`. It was tested rather than assumed, and it did
not survive.

**P7, my amendment, fails as stated and survives in direction.** `K` *is* ordered by
pair survival (−0.454), against the predicted `|ρ| ≤ 0.3`. But `U++` is ordered at
**−0.992**, more than twice as strongly. So the blind bits order the lit-governed
cell too, just far more weakly: the stratum decomposition keeps its direction and
loses its clean form. This is the reason the arm was restored — the drafting agent's
central argument rested on `K` being unordered, calibrated at −0.10 on eight bases,
and on twenty it is −0.45. Without the arm that argument would have entered the
record untested and overstated.

**P4c fails 2/2 in the reversed direction**, on exactly the two bases built to
discriminate handedness (27: `e_G = 0, e_G′ = 1`; 45: `e_G = 1, e_G′ = 0`). In both,
the grower with erosion score **zero** has the higher proximity. Meanwhile the two
scores are identical on **13 of 20** bases (Pearson 0.669), and each grower is
ordered slightly better by the *other* score. So the between-base ordering cannot be
distinguished from total β count, and the handed edge assignment is **unsupported on
this panel rather than refuted** — the panel lacks the power to separate them.

**P6b fails with its sign reversed**, which is the informative outcome the protocol
flagged at odds 0.5. `D+` beats random on **active** bases (mean +0.095) and **loses**
on frozen ones (mean −0.037; only 232 is positive, at +0.016). The premise was wrong
about where dark reads happen: dark needs `|Δ| ≥ 2`, and the frozen bases carry among
the highest random-arm dark counts in the panel (75,523 / 74,936 / 76,055
column-steps). Beam-frozen does not mean dark-quiet.

**P5 missed narrowly on one clause**: the β correlation held (0.512 ≥ 0.5), the pair-
survival correlation did not (−0.358 against a required ≤ −0.4).

## What this unit settles and what it leaves open

Settled: the algebra of a dense configuration at height two is finite, small, and
decided by popcount; the previous unit's entry partition has a reason; the identity
exception is a theorem with an exact residual, and it is not about activity.

Open, and sharper than before: **what orders residence beyond the blind bits.** The
blind bits order everything measured here, `K` included, so the clean
lit-versus-blind split does not hold. Whether the handed edge assignment is real
needs a panel where `e_G` and `e_G′` differ on many more than seven bases.

## Non-claims

Not a characterization of the terminal field for active bases — `Π` is measured,
exact only at its endpoints. Not height three, other densities or other observers.
No claim about `M*`. The random-arm ordering is descriptive-grade. `K` entered as a
specificity control and its census is not a characterization of confined refinements.
