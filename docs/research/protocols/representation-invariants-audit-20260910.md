# Protocol: representation invariants audit of existing ECA claims — 2026-09-10

**Status:** frozen before implementation and evaluation. Nothing run.
**Program:** [Invariants Across Representation Contracts](../2026-09-10-representation-invariants-program.md).
**Authored by:** Claude Code, Fable 5.1. **Reviewed by:** none at freeze (Codex inactive; Myk driving). First review is requested on this document before results are written up.
**Scope:** elementary CA on rings and causal windows; two global transformations and their composite; six properties already in the record. No dimensional-lift execution, no adaptive observer, no new dynamics.

## 1. Question

For each transformation `T` declared below and each property `Π` audited below, is `Π` preserved, covariant with a stated transport, or changed? Where it is changed, is there a transport of a companion object (the derivative, the initial state, the observation) that restores it, and at what cost?

## 2. Transformations, transports, costs

All transformations act on a ring of `n` cells with periodic boundary, or on causal windows where the property is window-local.

| Symbol | Action on state `S` | Action on rule `r` | Invertible | Touched sites | Information | Locality |
| --- | --- | --- | --- | --- | --- | --- |
| `T_c` (complement conjugation) | `S ↦ ¬S` | `r ↦ r̃`, `r̃(l,m,r) = ¬r(¬l,¬m,¬r)` | yes, involution | `n` | none | radius 0 |
| `T_m` (reflection) | `S ↦ reverse(S)` | `r ↦ r^m`, `r^m(l,m,r) = r(r,m,l)` | yes, involution | 0 (addresses reindexed) | none | radius 0 |
| `T_cm` | both | both | yes, involution | `n` | none | radius 0 |

Both satisfy `F_{T r}(T S) = T F_r(S)` for every `S`, which is the defining intertwining. Costs are declared, not measured: a complement is an edit of every site under a fixed decoder, or a zero-cost change of decoder; a reflection is a renaming of addresses. The local Z2 relabeling of rule fields (archived in the [rule-field relabeling note](../2026-09-10-rule-field-relabeling.md)) restricts to `T_c` on uniform rules and is not re-run here.

**Transports of companion objects.** The native derivative `D_r = 𝟙 ⊕ F_r` transports as a difference: `D_{T r}(T S) = D_r(S)` for `T_c` (both terms complemented, XOR cancels) and `D_{T r}(T S) = reverse(D_r(S))` for `T_m`. The native commutator `G_r = D_r∘F_r ⊕ F_r∘D_r` is computed from the transported law with no further choice. The correction tuples `K_h = (A_0, …, A_h)` with `A_0 = D`, `A_{j+1} = A_j∘F ⊕ F∘A_j` are native as well. A second, non-native transport of the derivative, "as a state", `D ↦ T D`, is used only in property P3 to show which transport makes the commutator covariant.

## 3. Properties audited and frozen predictions

**P1. Commutator classification under `T_m`** (established result 1: zero-G rules `Z = {0,4,60,90,102,150,170,200,204,240}`, one-G rules `U = {15,51,85,105,153,165,195,255}`, all others varying). Computed on the same exhaustive five-cell causal windows. *Prediction:* the class of `r^m` equals the class of `r` for all 256 rules. Reflection commutes with XOR and with composition, so this is expected exact.

**P2. Commutator classification under `T_c`.** *Prediction:* not preserved. Affine rules map to affine rules with bias `c ↦ c ⊕ M𝟙 ⊕ 1`, where `M𝟙` is the parity of the number of linear taps. Predicted images: `0↔255, 60↔195, 90↔165, 102↔153`; `150, 170, 204, 240, 15, 51, 85, 105` fixed. The nonlinear members of `Z` map to `T_c(4) = 223` and `T_c(200) = 236`; *prediction:* both have state-dependent `G` and so leave `Z ∪ U`. Consequently `T_c(Z) = {255,195,165,153,150,170,204,240,223,236}` intersects `Z` in `{150,170,204,240}` only.

**P3. Pointwise commutator covariance.** For all `S` on rings `n ∈ {6, 8, 10}`:
- under `T_m`, `G_{r^m}(reverse S) = reverse(G_r(S))` — *prediction:* all 256 rules.
- under `T_c` with the native (difference) derivative, `G_{r̃}(¬S) = G_r(S)` — *prediction:* exactly the self-dual rules, `r̃ = r` (16 rules), because `G_{r̃}(¬S) ⊕ G_r(S) = F_r(x) ⊕ ¬F_r(¬x)` at `x = D_r(S)`, and the defect vanishes for all `x` iff `r` is self-dual. Any non-self-dual rule that passes at a tested `n` because `D_r`'s image misses a discriminating window is recorded as such, not counted as a counterexample to the derivation.
- under `T_c` with the state transport of the derivative, `D ↦ ¬D`, the corresponding commutator `G^{st}_{r̃}(¬S) := D_{r̃}(F_{r̃}(¬S)) ⊕ ¬F_{r̃}(¬D_{r̃}(¬S))` — *prediction:* equals `G_r(S)` for all 256 rules. This is the transport that makes the commutator covariant; it costs one complement of the derivative field per evaluation.

**P4. Derivative-observation closure** (Research022 object: `ker(D_r) ⊆ ker(D_r∘F_r)` on the ring). *Prediction:* preserved under `T_c`, `T_m`, `T_cm` for all 256 rules at `n ∈ {6, 8, 10}`, by conjugacy. The rule set that closes at each `n` is reported as a by-product.

**P5. Local correction-cap census** (`results/local_correction_caps_20260910.json`, 4,608 budgets `(rule, kind ∈ {K,O}, h ≤ 2, R ≤ 2)`, read from the saved file, no recomputation). *Predictions:* (a) under `T_m`, `pass(r,kind,h,R) = pass(r^m,kind,h,R)` for all budgets; (b) under `T_c`, for every level `j`, `A_j^{r̃}(¬S) = A_j^{r}(S) ⊕ δ_j(A_0^r(S), …, A_{j-1}^r(S))` with `δ_j` local of radius at most `j`, so `pass(r,K,h,R) ⇒ pass(r̃,K,h,R+h)` and symmetrically; the minimum passing radius of `r̃` differs from that of `r` by at most `h`. Both directions are checked over the census; every violation is listed. The O coordinates are checked for (a) only; a prediction for O under `T_c` is deliberately not frozen.

**P6. Five-regime pair labels** (`results/sweep_full_classified.parquet`, 32,640 unordered pairs, five fixed seeds at `n = 100`). The sweep's initial states are not transformed, so exact invariance is not expected. Report, for `T_m` and `T_c` separately: the fraction of pairs whose label equals the label of the image pair, the confusion matrix between label and image label, and the same for the exact quantities `final` and `peak` disagreement. *Predictions:* agreement above 0.90 for both; disagreements concentrated on the drain/crystalline and structured/noisy boundaries already known to be soft (established results 5 and 6); `commute` labels agree exactly under both transformations, because commuting is a property of the pair of maps and its image pair.

**P7. Cost table.** Declared in section 2, reported verbatim, not measured.

## 4. Implementation and artifacts

- `scripts/verify_representation_invariants.py`, committed before any evaluation. It computes P1–P6 with `groovy.ca.apply_rule` and pure-Python window enumeration, reads the two saved result files, and writes `results/representation_invariants_20260910.json` with source hashes of the script and of both input result files, every prediction's pass/fail, and every violation listed.
- A CI workflow reruns the script and compares the JSON.
- The results note is written only after the run; it reports what the predictions got wrong first.

## 5. Not claimed

No transformation beyond the three declared; no claim that they exhaust admissible re-interpretations. No intrinsic-invariant, intrinsic-dimension, beam, or Class IV claim. Sweep-label agreement is a statistic about a sampled result, not an exact invariance. Costs are declared conventions.

## Dated clarifications after retrospective review (2026-09-11)

The frozen text above is unchanged. Codex reviewed the merged run (PR #80) and three corrections are recorded here and applied in the results note.

1. **P6's boundary-concentration clause was frozen without a threshold and was not scored.** The fraction is computed retrospectively: the two boundaries the frozen clause named (drain/crystalline and structured/noisy) carry 452 of 1,588 reflection disagreements (28.46%) and 518 of 1,978 complement disagreements (26.19%); the largest populated boundary, drain/structured, is one the clause did not name. The clause is **unsupported**; there is no prespecified binary score. Separately, the original note's own list of boundaries (drain/structured, drain/noisy, crystalline/drain) was wrong: it omitted crystalline/structured and noisy/structured, both populated. That is an error of the note, not of the protocol, and noisy/structured is the structured/noisy boundary the protocol named. The agreement-rate and commute-exactness clauses stand.
2. **P5(b)'s flagged list mixed two things.** Of the 768 K cells, 696 have identical minimum radius, 54 differ with both finite (50 within the frozen `≤ h` bound, 4 exceeding it, all at `h = 0`), and 18 have one side outside the `R ≤ 2` budget (right-censored, not decidable). The checker flagged the 4 genuine violations plus the 18 censored cells, 22 in all. A censored cell is not a violation. The frozen bound fails at `h = 0` on four cells; that failure is real and the derivation's omission of the target row explains it.
3. **P3's iff needs its finite-local proof route.** The defect identity shows vanishing on `x = D(S)`, not on every `x`. The defect has radius 2, so all 32 five-cell source words decide it for every rule: exactly the 16 self-dual rules pass and each other rule has a witness. The verifier now computes this. "The same criterion as full-gradient factoring" is qualified: that criterion is a *constant* complement response, which admits the constants 0 and 255 as well as self-duality.
