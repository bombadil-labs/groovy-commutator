# Protocol: full-shift depth three for the deep rules, and the full-shift depth ladder — 2026-09-12

**Status:** frozen before implementation and evaluation. Nothing run.
**Program:** [Invariants Across Representation Contracts](../2026-09-10-representation-invariants-program.md), sixteenth unit.
**Authored by:** Claude Code, Fable 5.1. **Protocol review:** pending Codex (OpenAI) gate 1 on the gathering PR.
**Why this unit:** the [fifteenth unit](../2026-09-11-full-shift-depth-two.md) found 24 pairs `(ψ, r)` under 232, 200 and 22 whose rules have refinement depth at most one at every ring yet at least three on the full shift, and a rings-versus-full-shift gap at depth two under seven observations. The sparse method decides the full-shift question at any depth `h` by one reachability problem on `4^{2h+2}` vertices. This unit takes the next step, `h = 3` (65,536 vertices, 11-cell violating blocks), for the four non-linear observations that carry gaps, to answer two questions: how deep are the 24 deep rules on the full shift, exactly three or more; and what is the full-shift depth class of every rule, `0, 1, 2, 3, ≥ 4`, tabulated against its rings-3-to-14 depth class. It also realizes the 24 depth-two separations as explicit eventually periodic pairs, as the fifteenth unit did for depth one.

## 1. Objects and definitions

Observations `ψ ∈ {232, 200, 22, 4}` and their complement conjugates `236, 151, 223` (232 is self-dual); rules `r ∈ 0..255`. Observation 32 is omitted: the tenth unit's identity `32 = 4 ∘ ¬` together with the fifteenth unit's complement covariance gives every set below for 32 as the conjugate of the set for 4, and this is recorded as a deduction, not computed. Observation 102 is omitted because `FS²_102` is all 256; 90 and 150 are omitted because their depth sets vary with the ring and belong to a separate unit.

`h_* ≤ 3` at ring `n` means `P_4 = P_3`; `D³_ψ(n)` is computed exhaustively for `3 ≤ n ≤ 14` (five applications of the rule per state).

**The depth-three pair graph `G³_{ψ,r}`.** Vertices are the 65,536 eight-cell pair blocks. A nine-cell pair block is an edge from its first eight cells to its last eight exactly when its centre agrees on `ψ`, `ψ∘F_r`, `ψ∘F_r²` and `ψ∘F_r³` (radii 1 to 4). A violating walk is a three-edge walk reading an 11-cell pair block whose three nine-cell sub-blocks are edges and whose fifth observed successors disagree at the centre, `ψ(F_r⁴ x)_0 ≠ ψ(F_r⁴ y)_0` (radius 5); there are `4^{11} = 4,194,304` such blocks per pair. `r ∈ FS³_ψ` iff no violating walk is bi-infinitely extendable (start reachable from a cycle, end reaching a cycle), decided by strong components and two breadth-first searches on the sparse edge list; no matrix power is taken and no ring certificate at depth three is claimed.

**Full-shift depth class.** For each `(ψ, r)`: `c_FS(r) = 0` if `r` is closed on the full shift (thirteenth unit), `1` if `r ∈ FS¹_ψ \ C_ψ`, `2` if `r ∈ FS²_ψ \ FS¹_ψ`, `3` if `r ∈ FS³_ψ \ FS²_ψ`, and `≥ 4` otherwise; `FS¹` and `FS²` are read from the fourteenth and fifteenth units' result files with their hashes. **Rings-3-to-14 depth class** `c_R(r)` is defined the same way from `⋂_{3≤n≤14} D^h_ψ(n)` for `h = 0, 1, 2, 3`, with `D⁰` the closed sets and `D¹`, `D²` read from the earlier results. Theorem: `c_FS(r) ≥ c_R(r)` for every rule (full-shift depth implies depth at every ring).

**Explicit witness pairs at depth two.** For each of the 24 fifteenth-unit M3 failures, the recorded extendable violating walk `(v_0, v_3)` in `G²_{ψ,r}` is realized by breadth-first search as an eventually periodic pair (left cycle, left path, violating nine-cell block, right path, right cycle), as the fifteenth unit did in `G¹`. The graph path is the certificate; a finite replay on three periods per side checks `ψ`, `ψ∘F`, `ψ∘F²` agreement on the interior trimmed by 4 cells (the radius of `ψ∘F³`) and `ψ∘F³` disagreement at the centre, as an implementation control.

## 2. Frozen predictions

- **N1 (theorem controls).** `FS²_ψ ⊆ FS³_ψ`; `FS³_ψ ⊆ D³_ψ(n)` for every `3 ≤ n ≤ 14`; `D²_ψ(n) ⊆ D³_ψ(n)`; `D³_ψ(kn) ⊆ D³_ψ(n)`; `c_FS ≥ c_R` for every rule.
- **N2 (the 24 deep rules; falsifiable bet).** Not all 24 pairs lie in `FS³_ψ`: at least one has full-shift depth at least four. Reported: the exact split of the 24 into depth exactly three and depth at least four, per observation, each non-member with an extendable violating walk in `G³_{ψ,r}` and its reachability facts. Failure: all 24 lie in `FS³_ψ`.
- **N3 (the depth-three gap; bet).** `Γ³_{ψ,[3,14]} = (⋂_{3≤n≤14} D³_ψ(n)) \ FS³_ψ` is nonempty for each of 232, 200, 22 and 4. `Γ³_{ψ,14} = D³_ψ(14) \ FS³_ψ` is reported without a bet. Neither is an all-ring statement.
- **N4 (the ladder; reported, one bet).** The full cross-tabulation of `c_FS` against `c_R` for every rule under each of the four observations is reported. Bet: under each observation the class `c_FS = 3` is nonempty, that is, the sparse method at depth three separates a new class from the fifteenth unit's `FS²` complement rather than every non-`FS²` rule having depth at least four. Failure: some observation has `FS³_ψ = FS²_ψ`.
- **N5 (explicit witness pairs; control on the verifier).** All 24 depth-two separations pass the finite replay. The finite data of every witness is recorded.
- **N6 (symmetries; theorem controls).** Complement covariance `FS³_{ψ̃} = {r̃ : r ∈ FS³_ψ}` and `D³_{ψ̃}(n) = {r̃ : r ∈ D³_ψ(n)}` for the four observations, and reflection covariance (all four observations are reflection-symmetric, so this is invariance of each set under `r ↦ mirror(r)`).

## 3. Artifacts and cost

`scripts/verify_full_shift_depth_three.py`, committed after protocol review and before evaluation; reads the thirteenth, fourteenth and fifteenth units' result files with their hashes; output `results/full_shift_depth_three_20260912.json` with source hashes, `D³_ψ(n)`, `FS³_ψ`, the class tables, per-pair violating and extendable walk counts, gap lists with witnesses, the 24 witness pairs, and the N1–N6 verdicts. Registered in `scripts/check_result_integrity.py`; CI carries both tiers. Note under `docs/research/2026-09-12-full-shift-depth-three.md`.

Cost: per pair, the 262,144 nine-cell and 4,194,304 eleven-cell pair blocks evaluated vectorially (about one second) and one sparse graph search on 65,536 vertices; seven observations (four plus three conjugates) × 256 rules, about 30 to 40 minutes in total; exhaustive depth three for seven observations on rings 3 to 14, a few minutes; the 24 reconstructions negligible. No matrix powers. The CI replay timeout is set to 180 minutes.

## 4. Not claimed

- No ring certificate at depth two or three; `D²`, `D³` are known for rings 3 to 14 only, and every gap is a rings-3-to-14 statement.
- Nothing about full-shift depth four or beyond: a rule outside `FS³_ψ` has full-shift depth at least four and nothing more is certified.
- Nothing about observations 32 beyond the recorded deduction, or about 102, 90, 150, or other observations; nothing about rings 1 and 2.
- No Class IV, novelty, renormalization or dimension claim.

## 5. Protocol review record

Pending.
