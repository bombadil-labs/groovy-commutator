# Does the corrected radius bound hold where the cap census disagreed with its complement?

**Research note, 2026-09-11.** Second unit of the [Invariants Across Representation Contracts](2026-09-10-representation-invariants-program.md) program. Authored by: Claude Code, Fable 5.1. Reviewed by: none at evaluation (Codex inactive; Myk driving). [Protocol](protocols/cap-census-complement-extension-20260911.md) frozen and [verifier](../../scripts/verify_cap_census_complement_extension.py) committed before this single run; canonical output [`results/cap_census_complement_extension_20260911.json`](../../results/cap_census_complement_extension_20260911.json). All four frozen predictions held, including the deliberately weak one.

## Answer

Yes. On the 22 `(rule, h)` K-coordinate cells where the [original census](2026-09-10-local-correction-caps.md) at `R ≤ 2` gave different pass/fail for a rule and its complement-conjugate, extending the radius budget to `R ≤ 6` shows:

- **X1, reproduction:** recomputed pass/fail at `R ≤ 2` matches the saved census in every cell.
- **X2, existence:** a cap exists on both sides in every cell. Every cell that the census reported as `None` passes at radius exactly 3.
- **X3, bound:** `mpr(r̃, h) ≤ max(mpr(r, h), h+1) + h(h+1)/2` and its symmetric form hold in every cell. The bound was derived post hoc in the [first audit note](2026-09-11-representation-invariants-audit.md); this is its first test as a prediction.
- **X4, secondary:** the observed shift `|mpr(r̃, h) − mpr(r, h)|` never exceeds `h + 1`. Observed shifts: 1 in all four `h = 0` cells, 1 in both `h = 1` cells, 1 in twelve and 2 in four of the sixteen `h = 2` cells.

| `h` | cells | shifts observed | derived bound on shift |
| --- | --- | --- | --- |
| 0 | 4 | 1, 1, 1, 1 | 1 |
| 1 | 2 | 1, 1 | up to 2 |
| 2 | 16 | 1 (×12), 2 (×4) | up to 4 |

The four shift-2 cells are 132↔222 and 160↔250 (`mpr` 1 versus 3 at `h = 2`).

## What this settles and what it does not

It settles that the first audit's P5(b) failure was a budget artifact: complement conjugation never removed a cap, it moved its radius by one or two, and the census's `R ≤ 2` window could not see radius 3. The derived bound is confirmed on this domain but is loose; the actual cost of complement conjugation in cap radius is at most 2 here, against a bound of up to 6. Whether the tight value is `h + 1` in general, or something else, is not decided by 22 cells and is not claimed.

Not tested: O coordinates, the 696 cells the census already showed equal, radii above 6, any other transformation. These are exhaustive causal-window computations on the full shift, not samples, but they are confined to the listed cells.

## Reading for the program

A property that looked "changed" under a transformation at one budget was covariant with a small, bounded cost at a slightly larger budget. That is the pattern the program exists to catch: the census's radius parameter is part of the representation contract, and a pass/fail table without its radius budget is not a property of the dynamics.

## Next

The tight shift is an open question; a small census of the shift over all 256 rules at `h ≤ 2`, `R ≤ 4`, would decide whether `h + 1` holds beyond these 22 cells. Separately, the editorial question from the first audit stands: whether the repository's default reading of the commutator under relabeling should transport the derivative as a state.
