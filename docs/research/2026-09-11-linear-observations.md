# Under every linear observation, closure is decided by the kernel, and the richer kernels keep only the affine rules

**Research note, 2026-09-11.** Seventh unit of the [Invariants Across Representation Contracts](2026-09-10-representation-invariants-program.md) program. Authored by: Claude Code, Fable 5.1. Protocol review: Codex (OpenAI), 2026-09-11, gate-1 sign-off at frozen revision `eb7d2f1` before implementation ([protocol](protocols/linear-observations-20260911.md), Section 5). Verifier committed before the single deterministic run; canonical output [`results/linear_observations_20260911.json`](../../results/linear_observations_20260911.json), rerun byte-identical and replayed in CI. All seven frozen predictions held. Final review of the completed unit: pending on the gathering PR.

## The question

Units [five](2026-09-11-parity-coarse-graining.md) and [six](2026-09-11-parity-history-bound.md) showed that neighbor parity closes exactly on the 32 constant-complement-response rules, with at most two steps of history for the rest. Both facts rest on parity's kernel being `{0ⁿ, 1ⁿ}`. Is the criterion specific to that kernel? This unit declares all eight linear elementary rules as observations at cadence one. Their kernels on the `n`-ring differ: trivial for 204, 170 and 240; everything for 0; the complement pair for 60 and 102, and for 90 on odd rings; the complement pair plus the two alternating patterns for 90 on even rings; and for 150, trivial unless `3 | n`, when it is the zero vector plus the three period-3 patterns and never contains `1ⁿ`. Closure of a rule under a linear observation means it maps kernel cosets into kernel cosets; `h_*` is the depth of the Research023 refinement chain, computed by exact partition refinement over cosets on rings 6 to 12.

## Answer

- **E1, affine rules close everywhere (theorem control).** All 16 affine rules are closed under all eight observations at every ring 6 to 12, as the commuting of circulant operators requires.
- **E2, trivial observations.** Rules 204, 170, 240 and 0 close every rule at every ring; rule 150 closes every rule at rings 7, 8, 10 and 11, where it is injective.
- **E3, complement-pair kernels.** Rules 60 and 102 at every ring, and rule 90 at rings 7, 9 and 11, close exactly the fifth unit's 32 rules. Same kernel, same fibers, same classification.
- **E4, rule 90 on even rings.** The closed set is the same at rings 6, 8, 10 and 12 and lies between the affine rules and the 32, as predicted. Post hoc, the exact value: it is the 16 affine rules and nothing more. Every one of the 16 nonlinear constant-response rules `{23, 24, 36, 43, 66, 77, 113, 126, 129, 142, 178, 189, 212, 219, 231, 232}` fails the alternating-pattern cosets.
- **E5, rule 150 on rings divisible by 3.** The closed set is the same at rings 6, 9 and 12 and contains the affine rules, as predicted. Post hoc, the exact value: again the 16 affine rules and nothing more. No rule outside the 32 closes, and no nonlinear rule inside the 32 closes either. Per the review caution, this says that for this observation, on these rings, closure held only for affine rules; it is not a characterization of all observations whose kernels omit `1ⁿ`.
- **E6, history census.** `h_* = 0` exactly on the closed set for every observation and ring. For rules 60 and 102 at every ring and rule 90 at odd rings the depths equal the sixth unit's certified depths for all 256 rules, confirming that observations with the same fibers share the whole refinement chain. Reported, not predicted: under rule 90 on even rings the maximum depth is 3 at rings 6 and 8 and 4 at rings 10 and 12 (rules 22 and 151 reach 4), and 16 rules change depth across the even rings; under rule 150 at rings 6, 9 and 12 the maximum depth is 4 at each ring and 48 rules change depth across them. So the parity bound of two steps is specific to the complement-pair kernel: the period-2 and period-3 kernels need up to four steps within the tested rings, and the depth is not ring-independent.

| observation, rings | depth 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| rule 90, ring 12 | 16 | 114 | 112 | 12 | 2 |
| rule 150, ring 12 | 16 | 82 | 136 | 12 | 10 |

- **E7, symmetries.** Every closed set and depth table is invariant under complement conjugation; those of rules 0, 90, 150 and 204 are invariant under reflection; reflection exchanges the tables of 60 and 102 and of 170 and 240.

## Reading for the program

The constant-complement-response criterion is a statement about one kernel, `{0ⁿ, 1ⁿ}`: any linear observation with that kernel reproduces the fifth unit's 32 rules and the sixth unit's depths, and any linear observation with a larger kernel, in this family, keeps only the affine rules. For the primitives program this sharpens the equivalence notion: under a linear coarse-graining, the only rules whose decoded dynamics survive every kernel are the affine ones, and the memory cost of the contract for the rest depends on the kernel and, beyond the complement pair, on the ring size. Block majority, the first non-linear observation, is the intended next unit.

## Limits

Eight linear observations at cadence one on rings 6 to 12; the exact closed sets under rule 90 on even rings and rule 150 on rings divisible by 3 are exhaustive there and were predicted only as bounds. The depth maxima and ring dependence are census facts with no proof and no claim beyond ring 12. No Class IV, novelty, or renormalization claim.
