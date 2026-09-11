# Protocol: the higher-block recoding as a declared local transformation — 2026-09-11

**Status:** frozen before implementation and evaluation. Nothing run.
**Program:** [Invariants Across Representation Contracts](../2026-09-10-representation-invariants-program.md).
**Authored by:** Claude Code, Fable 5.1. **Reviewed by:** none at freeze (Codex inactive; Myk driving).
**Why this transformation:** the first three units used global relabelings. Codex's review of #67 noted that conjugacy permits alphabet growth, with the higher-block presentation as the simplest case, and asked for declared recoding and inverse-locality budgets. This protocol declares that transformation and audits the same properties against it.

## 1. The transformation and its costs

`T_β` (2-block recoding): `S ↦ S'` with `S'_i = (S_i, S_{i+1}) ∈ {0,1}^2`.

| component | transport |
| --- | --- |
| alphabet | `{0,1}` → `{0,1}^2` with componentwise XOR |
| family | full binary shift → the subshift of consistent pairs (`S'_i[1] = S'_{i+1}[0]`) |
| law | `F'(S')_i = (F(S)_i, F(S)_{i+1})`, computed from first components; total on all 4-symbol configurations, radius 1 |
| derivative, correction rows | `A_j' = β(A_j)` componentwise; `K_h' = β(K_h)` |
| forward locality | radius 1 (a symbol reads two cells) |
| inverse locality | radius 0 (projection to the first component) |
| touched sites | all; information 0 |

`T_β` is injective with a radius-0 inverse on the image; it is the standard higher-block conjugacy of symbolic dynamics.

## 2. Frozen predictions

- **B1 (cap radius under recoding).** A K or O cap of radius `R` in block coordinates reads original cells `i−R … i+R+1`, so `mpr(r,h) − 1 ≤ mpr_β(r,h) ≤ mpr(r,h)` for every rule, kind, and `h ≤ 2`, wherever both are decided within `R ≤ 4`. Consistency where one side is undecided: `mpr ≤ 4 ⇒ mpr_β ≤ 4`, and `mpr_β ≤ 3 ⇒ mpr ≤ 4`. The distribution of `mpr − mpr_β ∈ {0, 1}` is reported; no prediction on it.
- **B2 (componentwise covariance).** On rings `n ∈ {8, 10}`, for all 256 rules and all states, `D'(β(S)) = β(D(S))` and `G'(β(S)) = β(G(S))`, where `D' = 𝟙 ⊕ F'` and `G'` are computed natively on the 4-symbol system with componentwise XOR.
- **B3 (derivative closure).** Derivative-observation closure on the image equals closure of the original for all 256 rules (conjugacy control).
- **B4 (observer-family closure, Research026).** The static observer family of the [possibility-frontier census](../2026-09-08-possibility-frontier.md), all nonconstant Boolean functions of 2-cell and 3-cell blocks with output-complement pairs identified, is closed under input complement and input reversal, and the block alignment on the 12-ring is preserved by reflection for both block sizes. Consequence, by conjugacy: every per-rule summary of that census is identical for `r`, `r̃`, and `r^m`. The per-rule tables of that census are not in the repository, so only the finite closure check is computed here; the numerical covariance is a deduction, stated as such.

## 3. Artifacts

`scripts/verify_higher_block_recoding.py`, committed before evaluation; reuses the census `tables()`; output `results/higher_block_recoding_20260911.json` with source hashes, the full `mpr_β` table for both kinds at `R ≤ 4`, the shift distribution, ring checks, the family-closure check, and every violation of B1–B4. CI replays it.

## 4. Not claimed

Nothing about `k`-block recodings with `k > 2`, about non-injective recodings, or about observers other than the census family. B1 is an inequality; the exact shift is reported, not predicted.

## Dated deviation and clarifications after retrospective review (2026-09-11)

Frozen text unchanged. Codex reviewed the merged run (PR #83).

1. **Deviation: the executed total block law has ambient radius 2, not the declared 1.** The implementation reads first components, computes `f = F(s)`, and returns `(f_i, f_{i+1})`; the second entry reads the first component at `i + 2`. Witness (Rule 170, all-zero arrays of shape `(1,7,2)`, one differing in `B[0,2,0]`): radius-1 patches at site 0 agree, outputs differ. The verifier now asserts this witness. A radius-1 completion exists: apply the binary rule to each component field separately; it agrees with the executed law on the consistent-pair family (checked for all 256 rules on the 8-ring) and differs off it. The corrected run reports B2 and B3 under **both** laws; every on-family result is unchanged, as expected, since the laws coincide there. The original run is attributed to the first-component law with ambient radius 2, not silently to the componentwise one.
2. **B4 transports maximizers; it does not make literal per-rule summaries identical.** Closure of the family under input complement and reversal gives explicit permutations of observer tables (for 2-cell blocks, table 1 maps under input complement to table 8, whose canonical output-complement representative is 7); the verifier now records both permutations for both block sizes. The claim is preservation of scalar optima, counts and overlap statistics under the declared prior, cadence and alignment, with optimal observer identities compared after transport. Still a deduction from a finite check; no numerical replay.
3. **Costs.** The recoding doubles stored bits per site (recorded), and nine measured cap radii decrease. "No new decoded dynamics" is the defensible statement; whether the recoded system is a useful new implementation depends on the resource contract.
