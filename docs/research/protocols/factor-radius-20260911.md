# Protocol: the locality radius of the factor on the image — 2026-09-11

**Status:** frozen before implementation and evaluation. Nothing run.
**Program:** [Invariants Across Representation Contracts](../2026-09-10-representation-invariants-program.md), twelfth unit.
**Authored by:** Claude Code, Fable 5.1. **Protocol review:** pending (Codex, gate 1, requested on the gathering PR before implementation).
**Why this unit:** the [tenth unit](../2026-09-11-complement-observation.md) found that under observation 200 sixteen of the seventeen residual rules have a factor that is not radius-1 consistent on image words, the first closed rules in the program whose factor on the image is not elementary, and reported the fact without explanation. This unit asks what radius the factor needs, and why. The answer is organized by one property of the observation: whether it is idempotent (`ψ ∘ ψ = ψ`). For an idempotent observation the image is exactly its fixed-point set, every image word is its own preimage, and the factor of any closed rule is `ψ ∘ F_r` restricted to the image, a radius-2 local map by construction. Rule 200 and rule 4 are idempotent; 232, 32 and 22 are not. So the unit has a theorem half and a census half.

## 1. Objects and definitions

Observations `ψ ∈ {232, 4, 32, 200, 22}`, each applied once at cadence one on rings `n ∈ {6, …, 12}`, with closed sets `C_ψ(n)` as computed in units eight to ten. Observation-only facts from the rule tables, disclosed and not counted as results: `ψ ∘ ψ = ψ` holds for 200 (a one survives iff it has a one-neighbor, and applying that twice changes nothing) and for 4 (an isolated one stays isolated); it fails for 232, 32 and 22 (checked on a single five-cell word each before freezing: for 232 the word `01101` changes twice, for 32 the word `10101` has ones after one step that are removed by the second, for 22 the word `00100` grows and then changes again).

For a closed rule `r`, the **factor** `B_r` is the map on the image `ψ(Ω_n)` with `B_r(ψ(S)) = ψ(F_r S)`. Its **locality radius on the image** `ρ_r(n)` is the least `ρ ∈ {0, 1, 2, 3}` such that `B_r(y)_i` is a function of `y_{i−ρ}, …, y_{i+ρ}` uniformly over all image words `y` at ring `n` and all sites `i`; that is, the `(2ρ+1)`-window table read off image words has no conflicting entries. Windows never seen on the image are don't-cares, as in the eighth unit. If no radius up to 3 is consistent the cell is recorded as `> 3`.

## 2. Frozen predictions

- **R1 (idempotent observations: the factor is `ψ ∘ F_r` on the image; theorem control).** For `ψ ∈ {200, 4}` and every closed rule at every ring, `B_r(y) = ψ(F_r(y))` for every image word `y` (since `ψ(y) = y`), and therefore `ρ_r(n) ≤ 2`. Every closed rule under 200 and 4 has a consistent radius-2 table at every ring 6 to 12.
- **R2 (the sixteen need exactly radius 2).** Under 200, the sixteen residual rules found radius-1 inconsistent in the tenth unit, `{72, 76, 128, 130, 132, 136, 140, 144, 152, 160, 162, 176, 183, 192, 194, 196}`, have `ρ_r(n) = 2` at every ring 6 to 12, and every other closed rule under 200 has `ρ_r(n) ≤ 1`. Under 4, every closed rule has `ρ_r(n) ≤ 1`, consistent with the ninth unit's tables.
- **R3 (non-idempotent observations: the factor is still local with radius at most 2; falsifiable).** For `ψ ∈ {232, 32, 22}` and every closed rule at every ring 6 to 12, `ρ_r(n) ≤ 2`. No theorem is claimed here: the preimage of an image word is not determined by the word, so locality of `B_r` is not automatic. A closed rule with `ρ_r(n) = 3` or `> 3` is a failure of R3 and is listed with its observation, ring and the conflicting windows. The eighth and tenth units' censuses found every such factor radius-1 consistent, which makes R3 a bet on the census continuing, not a deduction.
- **R4 (collapse and commuters; control).** Every collapse rule has `ρ_r(n) = 0` and every exact commuter has `ρ_r(n) ≤ 1` (its factor is `F_r` on the image), for every observation and ring.
- **R5 (ring independence; reported with one frozen part).** Whether `ρ_r(n)` is the same at every ring 6 to 12 for every closed rule is reported. Frozen: for the idempotent observations it is ring-independent for `n ≥ 7`, since a radius-2 table on image words is decided by five-cell image windows and every admissible five-cell window of the image subshift occurs on every ring of size at least 7 (the image of 200 is the words with no isolated one, the image of 4 the words with no two adjacent ones, both subshifts of finite type with a forbidden word of length 3, so any five-cell admissible window extends to a ring word of length 7 or more).
- **R6 (symmetries).** Reflection: `ρ` tables are invariant under `r ↦ mirror(r)` for every observation (all five are reflection-symmetric). Complement: covariant to the conjugate observation under `r ↦ r̃` (checked for 200 ↔ 236 and 4 ↔ 223 only, to bound cost).

## 3. Artifacts

`scripts/verify_factor_radius.py`, committed after protocol review and before evaluation; reads `results/block_majority_20260911.json`, `results/isolated_cell_20260911.json` and `results/complement_observation_20260911.json` for the closed sets and provenance hashes, recomputing closure as a consistency control; output `results/factor_radius_20260911.json` with source hashes, the idempotence facts, `ρ_r(n)` for every closed rule, observation and ring, the conflicting windows for every cell above radius 1, the R1–R6 verdicts with every violation. Registered in `scripts/check_result_integrity.py`; CI carries both tiers. Note under `docs/research/2026-09-11-factor-radius.md`; the Program's non-injective table gains a row.

## 4. Not claimed

Nothing about observations other than the five named, cadences above one, or rings outside 6 to 12 except where R1 and R5 are theorems. R3, if it holds, is a census fact for three observations. Nothing about the factor off the image. No claim that idempotence characterizes bounded factor radius in general. No Class IV, novelty, or renormalization claim.

## 5. Protocol review record

Pending. To be filled with the reviewer's identity, date, reviewed revision, requested checks and binding clarifications before any implementation commit.
