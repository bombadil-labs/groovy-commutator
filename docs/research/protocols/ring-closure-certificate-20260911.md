# Protocol: closure at every ring, certified from a finite pair graph — 2026-09-11

**Status:** frozen before implementation and evaluation. Nothing run.
**Program:** [Invariants Across Representation Contracts](../2026-09-10-representation-invariants-program.md), thirteenth unit.
**Authored by:** Claude Code, Fable 5.1. **Protocol review:** pending Codex (OpenAI) gate 1 on the gathering PR.
**Why this unit:** every closure census so far is ring by ring on `6 ≤ n ≤ 12`, and two of them are ring-dependent: rule 223 closes under observation 22 at ring 6 only ([tenth unit](../2026-09-11-complement-observation.md)), and the linear observations 90 and 150 close different sets on even and odd rings, or on rings divisible by 3 ([seventh unit](../2026-09-11-linear-observations.md)). The [twelfth unit](../2026-09-11-factor-radius.md) found that the one ring-6 closure has a factor needing the whole configuration, and could say nothing about rings above 12. This unit replaces the ring-by-ring census by a finite certificate: closure at ring `n` is decided by closed walks of length `n` in a 16-vertex graph that depends only on the observation, and boolean powers of that graph's adjacency matrix are eventually periodic, so the closed set at every ring `n ≥ 4` is decided by finitely many matrix powers. The unit has a theorem half (the criterion and two divisibility facts) and a census half (what the certified all-ring sequences look like for eight observations).

## 1. Objects and definitions

Observations `ψ ∈ {232, 4, 32, 200, 22, 102, 90, 150}`: the five non-linear observations of units eight to twelve, the parity observation 102 of units five and six, and the two linear observations whose closed sets were found ring-dependent in the seventh unit. Each is applied once at cadence one. Rule `r` is **closed under `ψ` at ring `n`** when `ψ(x) = ψ(y)` implies `ψ(F_r x) = ψ(F_r y)` for all `x, y ∈ {0,1}^n`; `C_ψ(n)` is the closed set. `C_ψ^∞ = ⋂_{n ≥ 4} C_ψ(n)` is the **all-ring closed set**.

**The pair graph `G_ψ`.** Vertices are the 16 two-cell pair blocks `((x_0, y_0), (x_1, y_1))`. There is an edge from `((a, a'), (b, b'))` to `((b, b'), (c, c'))` exactly when the three-cell pair block `(abc, a'b'c')` satisfies `ψ(abc) = ψ(a'b'c')` at its centre. Then ring-`n` pair configurations `(x, y)` with `ψ(x) = ψ(y)` are exactly the closed walks of length `n` in `G_ψ` (each cyclic three-cell block is an edge), for every `n ≥ 1`. Let `A_ψ` be the boolean adjacency matrix.

**Violating walks.** A four-edge walk `v_0 → v_1 → v_2 → v_3 → v_4` in `G_ψ` reads a five-cell pair block `(x_{-2..2}, y_{-2..2})` with all three-cell sub-blocks `ψ`-agreeing. It is **violating for `r`** when `ψ(F_r x)_0 ≠ ψ(F_r y)_0` at the centre (a radius-2 quantity, so the five-cell block decides it). Let `V_ψ(r)` be the set of violating walks; it is computed from the 4^5 = 1024 five-cell pair blocks.

**Ring criterion (theorem, proved in Section 2).** For `n ≥ 4`, `r ∉ C_ψ(n)` iff some violating walk `(v_0, …, v_4) ∈ V_ψ(r)` has `(A_ψ^{n−4})[v_4, v_0] = 1`, that is, some walk of length `n − 4` returns from `v_4` to `v_0`.

**Certificate.** The sequence `A_ψ^0, A_ψ^1, A_ψ^2, …` of boolean matrices takes values in a finite set, so it is eventually periodic: there are least `k_ψ ≥ 0` and `p_ψ ≥ 1` with `A_ψ^{k_ψ + p_ψ} = A_ψ^{k_ψ}`. Then `C_ψ(n + p_ψ) = C_ψ(n)` for every `n ≥ k_ψ + 4`, and the finite list `C_ψ(4), …, C_ψ(k_ψ + p_ψ + 3)` determines `C_ψ(n)` for every `n ≥ 4`.

**Full-shift closure.** `r` is closed under `ψ` on the full shift when `ψ(x) = ψ(y)` implies `ψ(F_r x) = ψ(F_r y)` for all bi-infinite `x, y`. By the same block argument this fails iff some violating walk is bi-infinitely extendable in `G_ψ`: `v_0` is reachable from a vertex on a cycle and `v_4` reaches a vertex on a cycle. Full-shift closure implies closure at every ring (periodic configurations are configurations). The converse is not automatic: a violating walk could be bi-infinitely extendable while lying on no closed walk (its ends in different strongly connected components).

## 2. Two facts fixed before the run

**Divisibility (theorem control).** If `r ∉ C_ψ(n)` then `r ∉ C_ψ(kn)` for every `k ≥ 1`: a violating pair `(x, y)` at ring `n` repeats to `(x^k, y^k)` at ring `kn`, and `ψ`, `F_r` commute with repetition because they are shift-commuting local maps, so `ψ(x^k) = ψ(x)^k = ψ(y)^k` while `ψ(F_r x^k) = (ψ F_r x)^k ≠ (ψ F_r y)^k`. Hence `C_ψ(kn) ⊆ C_ψ(n)`.

**Ring criterion (proof).** A ring-`n` pair configuration is a closed walk `w` of length `n`; its five-cell blocks are the four-edge sub-walks of the periodic unrolling of `w`, and `r` fails closure at ring `n` iff one of them is violating. Given a violating walk `v_0 … v_4` and a walk of length `n − 4` from `v_4` back to `v_0`, their concatenation is a closed walk of length `n` whose first four edges are the violating walk; conversely a closed walk of length `n ≥ 4` through a violating four-edge sub-walk supplies the return walk. For `n < 4` the sub-walk wraps around the ring more than once, and only the exhaustive computation is used.

## 3. Frozen predictions

- **K1 (divisibility; theorem control).** For all eight observations and all `3 ≤ n < kn ≤ 14`, the exhaustive closed sets satisfy `C_ψ(kn) ⊆ C_ψ(n)`.
- **K2 (the ring criterion is exact; theorem control).** For all eight observations and every `4 ≤ n ≤ 14`, the closed set computed from `G_ψ` and `V_ψ(r)` via the ring criterion equals the exhaustive closed set. Reference consistency: the exhaustive sets at rings 6 to 12 equal the recorded sets of the twelfth unit (232, 4, 32, 200, 22) and the seventh unit (102, 90, 150).
- **K3 (certificate; reported).** `k_ψ` and `p_ψ` are found for each observation and recorded with the complete list `C_ψ(4), …, C_ψ(k_ψ + p_ψ + 3)`; this is the all-ring census. No prediction is made about `k_ψ` or `p_ψ` beyond K4 and K5.
- **K4 (the six observations audited on rings 6–12 are constant from ring 7; falsifiable bet).** For `ψ ∈ {232, 4, 32, 200, 22, 102}`, `C_ψ(n) = C_ψ^∞` for every `n ≥ 7`; equivalently the certified sequence has eventual period 1 with all ring-dependence confined to `n ≤ 6`. In particular rule 223 under 22 is closed at ring 6 and at no ring `n ≥ 7`. The ring-6 closure of 223 was found in one census; nothing proves that no other small-ring closure recurs at a larger ring, so this is a bet. A failure is any `(ψ, n ≥ 7, r)` with `r ∈ C_ψ(n) \ C_ψ^∞`, listed with the smallest such `n`.
- **K5 (linear observations have the periods the kernels predict; theorem control).** Under 90, `C_90(n)` equals the seventh unit's odd-ring set (the 32) for every odd `n ≥ 5` and its even-ring set (the 16 affine rules) for every even `n ≥ 6`, so the certified sequence has eventual period 2. Under 150, `C_150(n)` is all 256 rules for every `n ≥ 4` with `3 ∤ n` (150 is injective there) and the 16 affine rules for every `n ≥ 6` with `3 | n`, eventual period 3. Rings 4 and 5 under 90 and ring 3 under 150 are reported.
- **K6 (symmetries; theorem controls).** Complement: `C_{ψ̃}(n) = {r̃ : r ∈ C_ψ(n)}` for every `n` and all eight observations, with the conjugate observation's sets computed by the ring criterion. Reflection: `C_{mirror ψ}(n) = {mirror(r) : r ∈ C_ψ(n)}`; the seven reflection-symmetric observations are invariant, and 102 maps to 60.
- **K7 (all-ring closure equals full-shift closure; falsifiable bet).** For all eight observations the full-shift closed set (no bi-infinitely extendable violating walk) equals `C_ψ^∞` (no violating walk on any closed walk of length `≥ 4`). The inclusion full-shift ⊆ all-ring is a theorem; the bet is the converse. A failure is a rule closed at every ring but not on the full shift, listed with a violating walk and the components of its ends.

## 4. Artifacts and cost

`scripts/verify_ring_closure_certificate.py`, committed after protocol review and before evaluation; reads `results/factor_radius_20260911.json` and `results/linear_observations_20260911.json` for the reference closed sets and provenance hashes; output `results/ring_closure_certificate_20260911.json` with source hashes, exhaustive `C_ψ(n)` for `3 ≤ n ≤ 14`, the pair-graph edge lists, `k_ψ`, `p_ψ`, the certified list `C_ψ(4), …, C_ψ(k_ψ + p_ψ + 3)`, the full-shift closed sets, the K1–K7 verdicts with every violation. Registered in `scripts/check_result_integrity.py`; CI carries both tiers. Note under `docs/research/2026-09-11-ring-closure-certificate.md`; the Program's non-injective table gains a row.

Cost: exhaustive closure for 8 observations × 12 rings × 256 rules, at most `2^14` states per cell, vectorized, about a minute; the graph part is 16 × 16 boolean matrices and 1024 five-cell blocks per rule, negligible.

## 5. Not claimed

- Nothing about observations beyond the eight named; the constancy bet K4 is for six observations only, and 90 and 150 show it is not a general fact.
- Nothing about refinement depth `h_*`, factor radius, or the derivative and commutator constructions at rings above 12; only closure is certified.
- No claim that the certificate's `k_ψ` and `p_ψ` are small in general, only their computed values here.
- No claim about rings 1 to 3 beyond the exhaustive lists at ring 3.
- No Class IV, novelty, renormalization or dimension claim.

## 6. Protocol review record

Pending.
