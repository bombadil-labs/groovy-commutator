# Protocol: block majority as the first non-linear observation — 2026-09-11

**Status:** frozen before implementation and evaluation. Nothing run.
**Program:** [Invariants Across Representation Contracts](../2026-09-10-representation-invariants-program.md), eighth unit.
**Authored by:** Claude Code, Fable 5.1. **Protocol review:** pending; requested from Codex (OpenAI) on the gathering PR before any implementation or evaluation.
**Why this unit:** units [five](../2026-09-11-parity-coarse-graining.md) to [seven](../2026-09-11-linear-observations.md) covered every linear observation; closure there is decided by a kernel and the richer kernels keep only the affine rules. Block majority, rule 232 applied once, is the simplest observation whose fibers are not cosets of anything: it is non-linear, non-injective and non-surjective. This unit asks which rules close under it, whether closure coincides with exact commutation with rule 232, and what the history cost is.

## 1. The transformation and its costs

`π(S) = F_232(S)`, the three-cell majority at cadence one on the `n`-ring. Definitional facts, verified from the rule table and by enumeration before freezing and not counted as results: rule 232 is self-dual (`π(¬S) = ¬π(S)`) and reflection-symmetric; it is non-surjective, with image fractions 0.531, 0.453, 0.375, 0.355, 0.326, 0.291, 0.255 at rings 6 to 12, and its fibers (the sets of states with the same majority field) range from singletons to 10, 15, 21, 31, 46, 67, 98 states at those rings, the largest fiber at each ring being the preimage of the all-zeros field and, by self-duality, of the all-ones field. Costs: forward radius 1; no inverse; information lost varies by fiber, from zero bits on singleton fibers to `log₂ 98` bits at ring 12; the image is a proper subset, so a factor `B` is defined on the image only.

Closure of `F_r` under `π` (Research022, shared closure account): `π(F_r S)` is constant on every fiber of `π`, equivalently a map `B` on the image with `π ∘ F_r = B ∘ π`. Exact commutation: `F_r ∘ F_232 = F_232 ∘ F_r` on every state of the `n`-ring. If `F_r` commutes exactly with `F_232` then `F_r` is closed with `B = F_r` restricted to the image, since `π F_r S = F_r π S`. `h_*` is the Research023 refinement depth computed by exact partition refinement from the fibers to the first stationary step, as in the seventh unit.

## 2. Frozen predictions

- **M1 (commuters close; theorem control).** For every `n ∈ {6, …, 12}`, every rule that commutes exactly with rule 232 on the `n`-ring is closed. The set of exact commuters `K(n)` is computed in the unit and contains at least `{0, 255, 204, 51, 170, 240, 15, 85, 232, 23}` at every `n`: constants, the identity and the shifts commute with every elementary rule; their complements commute with 232 because 232 is self-dual; 232 commutes with itself; 23 is `¬232`.
- **M2 (the remaining affine rules do not close).** The eight affine rules `{60, 90, 102, 105, 150, 153, 165, 195}` are not closed at any `n ∈ {6, …, 12}`. Reason: their responses are XOR combinations of neighbors, and a single isolated cell, which lies in the all-zeros fiber, is sent to a pattern whose majority field is not all-zeros (checked by hand for rule 90 at `n = 6` before freezing: `100000 ↦ 010001 ↦` majority field `100000`); the same mechanism is expected for the other seven. So, unlike every linear observation, majority does not preserve the affine rules.
- **M3 (closed set versus commuters).** `K(n) ⊆ C(n)` by M1. Whether `C(n) = K(n)`, and which rules if any are closed without commuting, is reported, not predicted. Whether `C(n)` is the same set at every ring is reported.
- **M4 (the factor is elementary).** For every closed rule the factor `B` on the image is radius-1 consistent on image words, so it is realized by an elementary rule on the image; for commuters `B = F_r` (control). Any closed rule whose factor is not radius-1 consistent is a failure of M4 and is listed.
- **M5 (history census).** `h_*` for all 256 rules at every `n ∈ {6, …, 12}`; `h_* = 0` exactly on `C(n)`. No prediction on the magnitude or ring dependence; the histogram per ring, the maximum, and the rules attaining it are reported, as is the count of rules whose depth changes with `n`.
- **M6 (symmetries).** Every closed set, commuter set and depth table is invariant under complement conjugation (self-duality maps fibers to fibers) and under reflection (232 is symmetric).
- **M7 (relation to the parity criterion).** `C(n) ⊄ CLOSED_32` is not predicted; what is frozen: `CLOSED_32 ⊄ C(n)` at every `n`, because rule 90 lies in `CLOSED_32` and is not closed under majority by M2. Whether `C(n) ⊆ CLOSED_32` is reported; the ten rules named in M1 all lie in `CLOSED_32`.

## 3. Artifacts

`scripts/verify_block_majority.py`, committed after protocol review and before evaluation; reads `results/parity_coarse_graining_20260911.json` for `CLOSED_32`; output `results/block_majority_20260911.json` with source hashes, image sizes and fiber-size histograms per ring, `K(n)`, `C(n)`, factor tables for closed rules, `h_*` per `(n, rule)`, and the M1–M7 verdicts with every violation. Registered in `scripts/check_result_integrity.py`; CI carries both tiers. Note under `docs/research/2026-09-11-block-majority.md`; the Program's non-injective table gains a row for majority.

## 4. Not claimed

Nothing about other non-linear observations, larger blocks, or cadences above one. Nothing about rings outside 6 to 12 except where a statement is a theorem (M1's inclusion). The factor's locality (M4) is asserted on image words only; behavior off the image is undefined and not claimed. No Class IV, novelty, or renormalization claim; majority coarse-graining is a standard object and is used here only as the first non-linear test of the program's closure vocabulary.
