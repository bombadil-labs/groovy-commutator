# Protocol: refinement depth at most one, certified at every ring — 2026-09-11

**Status:** frozen before implementation and evaluation. Nothing run.
**Program:** [Invariants Across Representation Contracts](../2026-09-10-representation-invariants-program.md), fourteenth unit.
**Authored by:** Claude Code, Fable 5.1. **Protocol review:** pending Codex (OpenAI) gate 1 on the gathering PR.
**Why this unit:** the [thirteenth unit](../2026-09-11-ring-closure-certificate.md) certified closure, refinement depth `h_* = 0`, at every ring from a sixteen-vertex pair graph. Depth itself is still a ring-by-ring census: units [eight](../2026-09-11-block-majority.md) to [ten](../2026-09-11-complement-observation.md) reported `h_*` on rings 6 to 12 and found it ring-dependent, and the [sixth unit](../2026-09-11-parity-history-bound.md) certified depth for all rings under parity only, by a lemma specific to complement pairs. This unit extends the certificate one step: for every observation and rule, whether one step of observed history suffices (`h_* ≤ 1`) is decided at every ring by closed walks in a 256-vertex pair graph that now depends on the rule as well as the observation. The recorded tables show the depth-at-most-one sets stabilizing by ring 9 or 10 for four observations, oscillating with the ring's residue modulo 3 under 22, and alternating under 90 and 150; the certificate decides which of these continue.

## 1. Objects and definitions

Observations `ψ ∈ {232, 4, 32, 200, 22, 102, 90, 150}` as in the thirteenth unit. For rule `r` at ring `n`, the observed trajectory partition `P_t` classes states by `(ψ(x), ψ(F_r x), …, ψ(F_r^t x))`; the refinement depth `h_*` is the least `t` with `P_{t+1} = P_t` (the eighth unit's definition, computed by iterated refinement). So `h_* ≤ 1` at ring `n` iff for all `x, y`: `ψ(x) = ψ(y)` and `ψ(F_r x) = ψ(F_r y)` imply `ψ(F_r² x) = ψ(F_r² y)`. Write `D_ψ(n) = {r : h_*(r, ψ, n) ≤ 1}`; it contains `C_ψ(n)`. `D_ψ^∞ = ⋂_{n ≥ 4} D_ψ(n)`.

**The depth-one pair graph `G_{ψ,r}`.** Vertices are the 256 four-cell pair blocks. There is an edge from block `(x_0..3, y_0..3)` to `(x_1..4, y_1..4)` exactly when the five-cell pair block `(x_0..4, y_0..4)` satisfies both agreements at its centre: `ψ(x_1 x_2 x_3) = ψ(y_1 y_2 y_3)` and `ψ(F_r x)_2 = ψ(F_r y)_2` (the latter reads all five cells). Ring-`n` pair configurations with `ψ(x) = ψ(y)` and `ψ(F_r x) = ψ(F_r y)` are exactly the closed walks of length `n` in `G_{ψ,r}` (each cyclic five-cell block is an edge). `A_{ψ,r}` is the boolean adjacency matrix.

**Violating walks.** A three-edge walk `v_0 → v_1 → v_2 → v_3` reads a seven-cell pair block `(x_{−3..3}, y_{−3..3})` whose three five-cell sub-blocks are edges; it is **violating** when `ψ(F_r² x)_0 ≠ ψ(F_r² y)_0`, a radius-3 quantity that the seven cells decide. `V_{ψ,r}` is the set of `(v_0, v_3)` over violating walks, computed from the `4^7 = 16384` seven-cell pair blocks.

**Ring criterion (theorem; same proof as the thirteenth unit's Section 2 with the graph replaced).** For `n ≥ 4`, `r ∉ D_ψ(n)` iff some `(v_0, v_3) ∈ V_{ψ,r}` has `(A_{ψ,r}^{n−3})[v_3, v_0] = 1`.

**Certificate.** Boolean powers of `A_{ψ,r}` repeat: least `k, p` with `A^{k+p} = A^k`; then membership of `r` in `D_ψ(n)` is periodic in `n` from `k + 3` with period `p`, decided by the finite list `n = 4, …, k + p + 2`. Per observation, the set sequence `D_ψ(n)` is eventually periodic with period dividing the least common multiple of the rules' periods; the verifier reports the least eventual period `P_ψ` and the least ring `N_ψ` from which `D_ψ(n + P_ψ) = D_ψ(n)`.

**Divisibility (theorem).** If `r ∉ D_ψ(n)` then `r ∉ D_ψ(kn)`: the violating pair repeats, and `ψ`, `F_r`, `F_r²` commute with repetition. So `D_ψ(kn) ⊆ D_ψ(n)`.

**Full-shift depth one.** `r` has depth at most one on the full shift iff no violating walk is bi-infinitely extendable in `G_{ψ,r}` (`v_0` reachable from a cycle, `v_3` reaching a cycle). Full-shift depth one implies depth one at every ring; the converse is not automatic.

## 2. Facts fixed before the run

- **Kernel facts (theorem, from the seventh unit).** Depth under a linear observation depends only on its kernel. Rule 150 is bijective on rings with `3 ∤ n`, so `D_150(n)` is all 256 rules there. On odd rings `ker 90 = {0^n, 1^n} = ker 102`, so `D_90(n) = D_102(n)` for odd `n`.
- **Parity (theorem, from the sixth unit's certificate).** Under 102, `h_* ≤ 1` for exactly the 32 closed rules and the 216 rules of depth 1, `248` in all, at every ring `n ≥ 6`; the eight rules `{22, 73, 104, 109, 146, 151, 182, 233}` have depth 2 on every ring `n ≥ 5` where realized. So `D_102(n)` is the same 248 rules for every `n ≥ 6`, and by the kernel fact so is `D_90(n)` for every odd `n ≥ 7`.

## 3. Frozen predictions

- **L1 (divisibility; theorem control).** For all eight observations and all `3 ≤ n < kn ≤ 14`, the exhaustive sets satisfy `D_ψ(kn) ⊆ D_ψ(n)`.
- **L2 (the criterion is exact; theorem control).** For all eight observations and every `4 ≤ n ≤ 14`, the depth-one set computed from `G_{ψ,r}` equals the exhaustive `D_ψ(n)`; and the exhaustive `D_ψ(n)` at rings 6 to 12 equals `{r : h_* ≤ 1}` read from the recorded depth tables of the eighth (232), ninth (4), tenth (32, 200, 22) and seventh (102, 90, 150) units.
- **L3 (certificates; reported).** For every `(ψ, r)` the pair `(k, p)`; per observation the largest `k`, the least common multiple of the `p`, the least eventual period `P_ψ` of the set sequence and its onset ring `N_ψ`; the certified list `D_ψ(4), …, D_ψ(N_ψ + P_ψ − 1)` and `D_ψ^∞`.
- **L4 (stabilization; bets).** (a) For `ψ ∈ {232, 4, 32, 200}`, `D_ψ(n)` is the same set for every `n ≥ 10` (the recorded tables stabilize at rings 9, 9, 9 and 10 within `n ≤ 12`; the bet is that nothing changes again). (b) Under 22, the least eventual period `P_22` is exactly 3 (the recorded sizes at rings 7 to 12 depend on `n mod 3`). (c) Under 102, `D_102(n)` is the parity 248 for every `n ≥ 6` (theorem, Section 2; scored as a control). A failure of (a) lists the smallest ring `n ≥ 10` and the rules entering or leaving; a failure of (b) reports the actual period.
- **L5 (linear observations; theorem controls and reported parts).** Theorem: `D_150(n)` is all 256 rules for `3 ∤ n`; `D_90(n)` is the parity 248 for every odd `n ≥ 7`. Reported, no bet: `D_90(n)` on even rings and `D_150(n)` on multiples of 3 (the recorded sizes 140, 130, 138, 130 and 130, 100, 98 are not yet stable at ring 12), with their certified eventual behaviour.
- **L6 (symmetries; theorem controls).** Complement covariance `D_{ψ̃}(n) = {r̃ : r ∈ D_ψ(n)}` and reflection covariance for all eight observations at every ring 4 to 14, the conjugate and mirrored observations' sets computed by the criterion.
- **L7 (all-ring depth one equals full-shift depth one; bet).** For all eight observations, `D_ψ^∞` equals the full-shift depth-one set. A failure lists the rule, a violating walk and the components of its ends.

## 4. Artifacts and cost

`scripts/verify_depth_one_certificate.py`, committed after protocol review and before evaluation; reads `results/block_majority_20260911.json`, `results/isolated_cell_20260911.json`, `results/complement_observation_20260911.json` and `results/linear_observations_20260911.json` for the recorded depth tables and provenance hashes; output `results/depth_one_certificate_20260911.json` with source hashes, exhaustive `D_ψ(n)` for `3 ≤ n ≤ 14`, per-rule `(k, p)`, per-observation `P_ψ`, `N_ψ`, certified lists, `D_ψ^∞`, full-shift sets, the L1–L7 verdicts with every violation. Registered in `scripts/check_result_integrity.py`; CI carries both tiers. Note under `docs/research/2026-09-11-depth-one-certificate.md`; the Program's non-injective table gains a row.

Cost: exhaustive depth-one checks for 8 observations × 12 rings × 256 rules at up to `2^14` states with three applications of the rule, a few minutes; per `(ψ, r)` a 256-vertex graph from 16384 seven-cell blocks and its boolean powers to the first repeat, 2048 graphs, a few minutes. Depth two would need 4096-vertex graphs per rule and is out of scope.

## 5. Not claimed

- Nothing about depth beyond one: rules outside `D_ψ(n)` have `h_* ≥ 2` there and nothing more is certified about them; the sixth unit's parity depth-two certificate is the only all-ring depth-two statement.
- Nothing about observations outside the eight, and the stabilization bets are for the named observations only.
- Nothing about rings 1 and 2, or about rings 3 beyond the exhaustive lists.
- No Class IV, novelty, renormalization or dimension claim.

## 6. Protocol review record

Pending.
