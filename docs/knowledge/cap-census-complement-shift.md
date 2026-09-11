# Complement conjugation shifts local-cap radii beyond the tested budget

Reflection preserves pass/fail of all 4,608 budgets in the local correction-cap census exactly. Complement conjugation does not preserve pass/fail within the census budget `R ≤ 2`: 22 of 768 `(rule, h)` cells differ for K coordinates, 696 have identical minimum radius.

The frozen prediction bounded the radius shift by `h`. That was wrong: under complement conjugation every correction row, including the target row `A_{h+1}`, transforms by a local triangular recoding of radius up to its depth, and recovering the original tuple composes radii. At `h = 0` the corrected bound is 1, and all four differing `h = 0` cells (4↔223, 200↔236) differ by exactly 1. For `h ≥ 1` the corrected bound exceeds the census budget, so a `None` on one side is "not within `R ≤ 2`", not "no cap". The corrected bound is post hoc and is the prediction of the next frozen protocol, not a result. See the [audit note](../research/2026-09-11-representation-invariants-audit.md) and the [census](../research/2026-09-10-local-correction-caps.md).


Revision 2026-09-11: the [extension](../research/2026-09-11-cap-census-complement-extension.md) at `R ≤ 6` confirms the post-hoc bound on all 22 cells and shows every cell has a cap on both sides, every former `None` passing at radius 3. The observed shift is 1 or 2, never more than `h + 1`. The shift is therefore a bounded cost of the transformation, not a loss of closure; the bound remains loose and the tight value is open.
