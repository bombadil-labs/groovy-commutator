# Which existing ECA claims survive complement conjugation and reflection?

**Research note, 2026-09-11.** First unit of the [Invariants Across Representation Contracts](2026-09-10-representation-invariants-program.md) program. Authored by: Claude Code, Fable 5.1. Reviewed by: none at evaluation (Codex inactive; Myk driving). The [protocol](protocols/representation-invariants-audit-20260910.md) was frozen and the [verifier](../../scripts/verify_representation_invariants.py) committed before this run; the canonical output is [`results/representation_invariants_20260910.json`](../../results/representation_invariants_20260910.json). Five of six frozen predictions held. One did not, and that one is reported first.

## The prediction that failed

**P5(b), the local correction-cap census under complement conjugation.** The protocol predicted that the minimum passing cap radius of a rule and of its complement-conjugate differ by at most `h` at correction depth `h`, and that pass/fail within the census budget `R ≤ 2` is therefore preserved. Observed: reflection preserves all 4,608 budgets exactly, but complement conjugation changes pass/fail within budget in 22 of the 768 `(rule, h)` cells for K coordinates; 696 cells have exactly equal minimum radius.

The frozen bound was wrong, not the census. Under complement conjugation the correction rows transform as `A_j' = A_j ⊕ δ_j(A_0, …, A_{j−1})` with `δ_j` of radius at most `j`, and this includes the **target** row `A_{h+1}`, which the frozen argument forgot. Recovering `K_h` from `K_h'` also composes radii. So the radius shift is bounded by a compositional quantity larger than `h`, and for `h ≥ 1` that exceeds the census budget, where "no cap at `R ≤ 2`" then reads as `None` on one side and a small radius on the other. At `h = 0` the corrected bound is `≤ 1`; all four `h = 0` cells that differ (rules 4↔223 and 200↔236) differ by exactly 1. This corrected bound is **post hoc**, derived after seeing the failure, and is the first item of the next protocol, not a result of this one. Every violation is listed in the result file.

## What held

| Property | `T_m` (reflection) | `T_c` (complement conjugation) |
| --- | --- | --- |
| Commutator class zero / one / varying (established result 1) | preserved, all 256 rules | changed: images `0↔255, 60↔195, 90↔165, 102↔153`; `150,170,204,240,15,51,85,105` fixed; `4 ↦ 223` and `200 ↦ 236` leave the zero-G set and have state-dependent `G`. `T_c(Z) ∩ Z = {150,170,204,240}` exactly as predicted |
| Pointwise commutator, native derivative | covariant, all 256 rules, rings 6/8/10 | covariant for exactly the 16 self-dual rules `{15,23,43,51,77,85,105,113,142,150,170,178,204,212,232,240}`, no spurious passes at any ring |
| Pointwise commutator, derivative transported as a state | — | covariant, all 256 rules, rings 6/8/10 |
| Derivative-observation closure (`ker D ⊆ ker D∘F`) | preserved | preserved (and under the composite) |
| Local-cap census pass/fail, 4,608 budgets | preserved exactly | see above |
| Sweep regime labels, 32,640 pairs | 95.13% agree; commute pairs 100% | 93.94% agree; commute pairs 100% |

**The commutator's convention dependence is exactly self-duality.** The defect `G_{r̃}(¬S) ⊕ G_r(S)` equals `F_r(x) ⊕ ¬F_r(¬x)` at `x = D_r(S)`, the complement-response of `F`, so it vanishes for all states iff `r̃ = r`. This is the same criterion that the [full-gradient closure note](2026-09-10-full-gradient-closure.md) found for factoring through the full gradient. Transporting the derivative as a state, at the cost of one complement of the derivative field, restores covariance for every rule. Established result 1 stands as written: the commutator of an affine rule is its bias, and the bias transforms as `c ↦ c ⊕ M𝟙 ⊕ 1`, so it belongs to the interpreter as much as to the rule.

**Derivative-observation closure is representation-independent and stable in `n`.** The set of rules whose derivative observation closes is the same 30 rules at `n = 6, 8, 10`: `{0,4,12,15,23,51,60,68,76,77,85,90,102,105,150,153,165,170,178,195,200,204,205,207,221,223,232,236,240,255}`. It is closed under both transformations, as conjugacy requires. That it contains 223 and 236 while the zero-G set does not is the closure-versus-commutation distinction of Research022 seen through the transformation family.

**Regime labels are far more stable than the statistics behind them.** The sweep's initial states were not transformed, so the raw `final` and `peak` disagreement values of a pair and its image are exactly equal only 28% and 27% of the time under reflection (22% and 17% under complement). The labels nevertheless agree 95% and 94% of the time, and every disagreement lies on the drain/structured, drain/noisy, or crystalline/drain boundaries, which established results 5 and 6 already identified as soft. Commute labels agree exactly under both transformations, because commuting is a property of the pair of maps.

## Controls

The batched stepper agrees with `groovy.ca.apply_rule` on every ring; the intertwining identity `F_{Tr}(TS) = TF_r(S)` holds for all 256 rules at `n = 8` for both transformations; the five-cell window classification reproduces the zero-G and one-G sets of established result 1 exactly. The audit reads the census and sweep files by hash and recomputes nothing they contain.

## Limits

Three transformations only; no claim that they exhaust admissible re-interpretations. Ring results are exhaustive at `n ≤ 10`, not proofs for all `n`, except where the text gives the algebraic reason. The sweep statistic is about a sampled result with fixed seeds and is not an invariance. Costs are declared conventions. No novelty, Class IV, intrinsic-invariant, or beam claim.

## Next

Freeze a small extension of the local-cap census at `R ≤ 4` for the 22 differing `(rule, h)` cells and their conjugates, with the corrected compositional radius bound stated as the prediction. Separately, decide whether "derivative transported as a state" should be the repository's default reading of the commutator under relabeling; that is an editorial decision about the representation contract, not a computation.
