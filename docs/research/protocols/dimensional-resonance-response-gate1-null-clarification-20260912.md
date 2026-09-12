# Gate-1 clarification: orbit-level placebo and residual-span convention — 2026-09-12

**Status:** binding protocol-only clarification after renewed independent Gate-1 review; no implementation or physical evaluation is authorized until this clarification is integrated and the reviewer renews Gate 1 on the resulting exact gathering head.  
**Program:** *Dimensional Closure and the Commutator Lift*.  
**Governing refreeze:** `docs/research/protocols/dimensional-resonance-response-gate1-refreeze-20260912.md`.  
**Reviewed head:** `5c0b677bf0b053e0457d3beffc29b70715567a79`.  
**Independent reviewer:** Claude Code / Fable 5.1, review comment `#issuecomment-5647097764`.  
**Authored by:** Codex / OpenAI GPT-5.6 Sol.

This file records only the two binding protocol pins requested by the renewed Gate-1 review. The substrate, rings, horizons, homology relation, source-only matched-class census, descriptors, exact causal window, `V/M/R`, class contrasts, strict predicate, complement fork, R1–R3/R5, and interpretation ceiling are unchanged.

## B1 — placebo calibration is joint-shift-orbit preserving

The pair-level cyclic label rotation in §9 of the governing refreeze is superseded because the physical response is exactly invariant under the joint logical shift

`(a,b) -> (sigma a, sigma b)`.

Every scored descriptor class is a union of these joint-shift orbits. A fair deterministic null must therefore preserve orbit coherence rather than break one physical orbit into differently labeled copies.

For each scored descriptor class `c` on a fixed ring `n`:

1. Partition the class into exact joint-shift orbits under `(a,b) -> (sigma a, sigma b)`.
2. Represent each orbit by the lexicographically least ordered pair `(a,b)` using **MSB-first fixed-width binary words**, equivalently ascending integer `a` then ascending integer `b` on that ring.
3. Order the orbits by those canonical representatives.
4. Each orbit receives the actual binary homology label shared by all of its members. Form the orbit-level label vector in canonical orbit order.
5. Construct placebo labelings by every distinct nontrivial cyclic rotation of that **orbit-level** label vector, then expand each rotated orbit label back to every pair in that orbit.
6. Across all scored classes in the ring, use one common rotation index `r`, reduced modulo the orbit count of each class. Deduplicate identical resulting global pair label assignments before scoring.
7. Recompute exactly the frozen class contrasts, per-class signs, pair-weighted aggregates, and strict predicate under every distinct orbit-level placebo assignment.

R4's frozen threshold is unchanged: at any horizon where the actual ring-7 strict predicate passes, fewer than 10% of the distinct **orbit-level** placebo assignments may also pass it.

The implementation/result must report, for each scored class, the number of joint-shift orbits in the homologous and control subsets in addition to the already-frozen pair counts. On ring 7, all scored joint-shift orbits have size 7, so these counts must equal the frozen pair counts divided by 7. Any census/orbit mismatch is an implementation blocker.

A pair-level cyclic rotation may be reported only as an explicitly weaker secondary reference; it is not the R4 null and cannot be used to claim selectivity.

## B2 — residual span is inclusive

`S_k` is pinned to the **inclusive vertical row count** of the nonzero residual on the exact causal window:

- empty residual: `S_k = 0`;
- nonempty residual with minimum and maximum occupied rows `y_min,y_max`:

`S_k = y_max - y_min + 1`.

Thus an isolated nonzero residual cell has span 1. This convention applies identically to homologous pairs, matched controls, descriptive cohorts, independent replay, class contrasts, pair-weighted aggregates, and placebo recomputation.

## Review consequence

These changes repair the renewed review's B1/B2 blockers and do not alter any other frozen scientific choice. After integration, renewed exact-head Gate 1 must verify that this clarification is the only semantic change relative to `5c0b677bf0b053e0457d3beffc29b70715567a79`. No verifier or physical response evaluation may precede that approval.
