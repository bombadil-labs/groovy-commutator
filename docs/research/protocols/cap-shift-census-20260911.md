# Protocol: complement-conjugation shift census over all local caps — 2026-09-11

**Status:** frozen before implementation and evaluation. Nothing run.
**Program:** [Invariants Across Representation Contracts](../2026-09-10-representation-invariants-program.md).
**Authored by:** Claude Code, Fable 5.1. **Reviewed by:** none at freeze (Codex inactive; Myk driving).
**Origin:** the [extension note](../2026-09-11-cap-census-complement-extension.md) observed shifts of 1 or 2 on 22 cells and stated that the tight value was open. This protocol asks the question on the whole domain.

## 1. Question

Over all 256 rules, both coordinate kinds K and O, and depths `h ≤ 2`, how far does complement conjugation move the minimum passing cap radius, and does the secondary prediction of the extension, shift `≤ h + 1`, hold everywhere it can be decided?

## 2. Domain and budget

- Rules: all 256. Kinds: K and O. Depths: `h ∈ {0, 1, 2}`. Radii: `R ∈ {0, …, 4}`. Full causal windows of width `2(h+1+R)+1`, at most 15 bits, no torus. Evaluator: the census `tables()` and the same vectorized functional test as the extension.
- A cell is **decided** when both `mpr(r, kind, h)` and `mpr(r̃, kind, h)` exist within `R ≤ 4`, **half-decided** when exactly one exists, and **undecided** when neither does. Shifts are computed only on decided cells. Half-decided cells are reported with the existing radius; by the derived bound they cannot be counterexamples to X3 unless the existing radius is 0 at `h ≥ 3`, which is outside the domain, so they are reported, not counted.

## 3. Frozen predictions

- **X1 (reproduction).** Recomputed pass/fail at `R ≤ 2` equals the saved census in all 4,608 budgets.
- **X2 (reflection control).** Under reflection `r ↦ r^m`, `mpr` is identical in every cell for both kinds (already known at `R ≤ 2`; predicted to extend to `R ≤ 4`).
- **X3 (K shift).** On every decided K cell, `|mpr(r̃) − mpr(r)| ≤ h + 1`.
- **X4 (O shift, no derivation).** On every decided O cell, `|mpr(r̃) − mpr(r)| ≤ h + 1`. The O rows are `B_j = D∘F^j`, which transform as `B_j^{r̃}(¬S) = B_j^r(S)` exactly (the derivative is a difference and `F^j` intertwines), so a sharper prediction is available and is frozen as **X4′: the O shift is 0 in every decided cell**, and the O pass/fail table is complement-invariant at every radius. X4 is retained as the fallback statement.
- **X5 (half-decided cells).** Every half-decided cell has its existing radius equal to 4 (the cap on the other side would need radius 5 or more, outside budget) or lies at `h = 2`. Any half-decided cell with existing radius `≤ 2` at `h ≤ 1` is a counterexample to the derived bound and is reported as such.

## 4. Artifacts

`scripts/verify_cap_shift_census.py`, committed before evaluation; output `results/cap_shift_census_20260911.json` with source hashes, the full `mpr` table for both kinds at `R ≤ 4`, all shift histograms by `(kind, h)`, every violation of X1–X5, and the list of half-decided and undecided cells. CI replays it.

## 5. Not claimed

Nothing above radius 4; nothing about transformations other than complement conjugation and reflection; a confirmed `h + 1` is an observed bound on this domain, not a theorem.

## Dated clarifications after retrospective review (2026-09-11)

Frozen text unchanged. Codex reviewed the merged run (PR #82). The saved census has no half-decided cells, so these are prospective scoring corrections; the shift histograms are unaffected.

1. **Half-decided cells can refute the shift bound.** Section 2 said they cannot be counterexamples to X3. That is wrong: if one minimum is `a` and the other exceeds the radius-4 budget, the shift is at least `5 − a`, which refutes `shift ≤ h + 1` whenever `5 − a > h + 1`. The verifier now reports `shift_lower_bound` and a refutation flag for every half-decided cell, kept separate from X3's both-decided scope.
2. **X5's implemented predicate was weaker than declared.** The declared sentence requires existing radius 4 or `h = 2`; the checker flagged only existing radius `≤ 2` at `h ≤ 1`, missing radius 3 at `h ≤ 1`. The verifier now implements the declared predicate.
3. **Source-window width** is `2·max(h+1+R, h+2)+1`, as in the census; maximum width 15 unchanged.

Matching availability within `R ≤ 4` bounds existence within the budget; existence invariance beyond it rests on the transfer argument, not on this census.
