# Protocol: local-cap census extension under complement conjugation — 2026-09-11

**Status:** frozen before implementation and evaluation. Nothing run.
**Program:** [Invariants Across Representation Contracts](../2026-09-10-representation-invariants-program.md).
**Authored by:** Claude Code, Fable 5.1. **Reviewed by:** none at freeze (Codex inactive; Myk driving).
**Origin:** the failed prediction P5(b) of the [first audit](representation-invariants-audit-20260910.md), reported in the [audit note](../2026-09-11-representation-invariants-audit.md). This protocol tests the bound that was derived post hoc there; it is the first time that bound is a prediction.

## 1. Question

For the 22 `(rule, h)` cells whose K-coordinate pass/fail differs between a rule and its complement-conjugate within the original census budget `R ≤ 2`, does a cap exist for both sides at a larger radius, and does the radius shift obey the corrected bound?

## 2. The bound being tested

Under complement conjugation, with `K_h = (A_0, …, A_h)`, `A_0 = D`, `A_{j+1} = A_j∘F ⊕ F∘A_j`:

- `A_j^{r̃}(¬S) = A_j^r(S) ⊕ δ_j(K_{j−1}^r(S))` with `δ_j` local of radius at most `j` (`δ_1(x) = F(x) ⊕ ¬F(¬x)`; the recursion uses `A_i(F(S)) = A_{i+1}(S) ⊕ F(A_i(S))`, radius 1 in `K_{i+1}(S)`).
- Recovering `A_j^r` from `K_j^{r̃}` costs radius `ρ_j = j(j+1)/2` (radii compose through the triangular inverse).
- If a cap of radius `R` gives `A_{h+1}^r` from `K_h^r`, then `A_{h+1}^{r̃} = g(K_h^r) ⊕ δ_{h+1}(K_h^r)`, expressed in `K_h^{r̃}` with radius at most `max(R, h+1) + ρ_h`.

**Bound:** `mpr(r̃, h) ≤ max(mpr(r, h), h+1) + h(h+1)/2`, and symmetrically with `r` and `r̃` exchanged, wherever `mpr(r, h)` exists. Numerically: `≤ max(R,1)` at `h=0`; `≤ max(R,2)+1` at `h=1`; `≤ max(R,3)+3` at `h=2`.

## 3. Domain and budget

- Cells: the 22 `(rule, h)` K-coordinate cells listed under `P5_local_cap_census.complement_K_radius_bound_violations` in `results/representation_invariants_20260910.json`, each paired with its conjugate cell. Rules and depths are read from that file, not retyped.
- Radii: `R = 0 … 6` for every cell, so that the `h = 2` bound (at most 6 when `R ≤ 3`) is inside the tested range. Source windows are full causal windows of width `2(h+1+R)+1`, at most 19 bits, as in the original census; no torus.
- O coordinates: not tested. K only, as in the failed prediction.

## 4. Frozen predictions

- **X1 (reproduction control).** For every tested cell, pass/fail at `R ≤ 2` recomputed here equals the saved census value.
- **X2 (existence).** For every one of the 22 cells, a cap exists on both sides within `R ≤ 6`.
- **X3 (bound).** For every cell, `mpr(r̃, h) ≤ max(mpr(r, h), h+1) + h(h+1)/2` and the symmetric inequality hold.
- **X4 (secondary, low confidence, stated so that it can fail).** The observed shift `|mpr(r̃, h) − mpr(r, h)|` never exceeds `h + 1`. This is a guess from the four `h = 0` cells; it is not derived.

## 5. Implementation and artifacts

`scripts/verify_cap_census_complement_extension.py`, committed before evaluation; reuses `tables()` from `scripts/verify_local_correction_caps.py` and checks functionality of the patch-to-target map over every source window with a vectorized grouping. Output `results/cap_census_complement_extension_20260911.json` with source hashes of the script, the census file, and the audit file, every cell's minimum radius on both sides, and every violation of X1–X4. CI replays it.

## 6. Not claimed

Nothing about O coordinates, about the 696 unchanged cells beyond the saved census, about radii above 6, or about transformations other than complement conjugation. A confirmed bound is a bound, not the exact shift.
