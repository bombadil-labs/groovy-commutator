# How far does complement conjugation move a local cap, over all 256 rules?

**Research note, 2026-09-11.** Third unit of the [Invariants Across Representation Contracts](2026-09-10-representation-invariants-program.md) program. Authored by: Claude Code, Fable 5.1. Reviewed by: none at evaluation (Codex inactive; Myk driving). Retrospective review: Codex (OpenAI), 2026-09-11, after merge; corrections applied in the follow-up PR and dated below. [Protocol](protocols/cap-shift-census-20260911.md) frozen and [verifier](../../scripts/verify_cap_shift_census.py) committed before this single deterministic run; canonical output [`results/cap_shift_census_20260911.json`](../../results/cap_shift_census_20260911.json). All six frozen predictions held.

## Answer

Over all 256 rules, both coordinate kinds, depths `h ≤ 2`, radii `R ≤ 4`:

- **O coordinates are complement-invariant, exactly.** The pass/fail table for O caps is identical for every rule and its conjugate at every radius, so every O shift is zero. This was predicted (X4′) from the identity `B_j^{r̃}(¬S) = B_j^r(S)`: the derivative is a difference and `F^j` intertwines, so the O tuple does not see the relabeling at all.
- **K shifts are 0, 1 or 2, never more than `h + 1`.** Histogram of `|mpr(r̃) − mpr(r)|` on decided K cells:

| `h` | decided cells | shift 0 | shift 1 | shift 2 |
| --- | --- | --- | --- | --- |
| 0 | 30 | 26 | 4 | — |
| 1 | 128 | 110 | 18 | — |
| 2 | 180 | 124 | 52 | 4 |

The four shift-2 cells are the pairs 132↔222 and 160↔250 at `h = 2`, the same ones the [extension](2026-09-11-cap-census-complement-extension.md) found.

- **No half-decided cells.** At `R ≤ 4`, every cell either has a cap on both sides or on neither. A half-decided cell with existing radius `a` would imply a shift of at least `5 − a` and would refute `shift ≤ h + 1` whenever `5 − a > h + 1`; the protocol's claim that such cells could not be counterexamples was wrong and the verifier now reports the lower bound (corrected 2026-09-11; none occurred). 862 cells are undecided on both sides (K: 226 / 128 / 76 at `h = 0, 1, 2`; O: 226 / 128 / 78). So within this budget, complement conjugation never creates or destroys a cap; it only moves K radii.
- **Controls.** Recomputed pass/fail at `R ≤ 2` matches the saved census in all 4,608 budgets. Reflection leaves `mpr` identical in every cell for both kinds, now up to `R ≤ 4`.

## A post-hoc observation, not a prediction

The 30 rules with a K cap at `h = 0` are exactly the 30 rules with an O cap at `h = 0`, and exactly the 30 rules whose derivative observation closes on rings `n = 6, 8, 10` in the [first audit](2026-09-11-representation-invariants-audit.md). At depth 0 both cap kinds ask whether `D∘F` is a local function of `D` (for K, `A_1 = D∘F ⊕ F∘D` and the second term is already local in `D`), which is derivative-observation closure with a local factor. That the global ring test and the full-shift local test at radius `≤ 4` agree on all 256 rules is exact within these budgets and was noticed after the run; it is recorded here and not counted as a prediction.

## Reading for the program

For the O coordinates, complement conjugation is a transformation the representation does not see; for the K coordinates it is covariant with a cost of at most two units of radius on this domain, and the cost is never a loss of existence. "Shift `≤ h + 1`" is now an observed bound over the whole census, not a theorem: at `h = 2` the observed maximum is 2, below `h + 1 = 3`, so the true bound may be tighter still. Nothing above radius 4 is claimed.

## Next

The transformation family has been exhausted for the global relabelings. The next unit should declare a transformation of a different type, either a local recoding with a locality budget or a change of completion on a shared family, and audit an observer-side result from the Erased Distinctions Program against it.

## Correction 2026-09-11, after retrospective review by Codex

Three prospective scoring corrections, recorded in the [protocol addendum](protocols/cap-shift-census-20260911.md): half-decided cells can refute the shift bound and are now reported with a lower bound; X5 now implements its declared predicate (existing radius 4 or `h = 2`); the source-window width is `2·max(h+1+R, h+2)+1`. The saved census has no half-decided cells, so no reported number changes. Existence invariance beyond `R ≤ 4` rests on the transfer argument, not on this census.