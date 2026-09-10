# Targeted selector-shielding family census — 2026-09-08

## Status

Frozen before evaluating the 512 cases below. This is a follow-up to the one-sided shielding witness found after Research021.

## Fixed physical system

Use the same selector law, alternating background, phase, and adjacent two-strip encoding as Research018–021 and the selector-shielding note.

For a finite logical support `S`, encode

\[
U_j(S)=\{(j,2i+1),(j+1,2i):i\in S\}.
\]

Rows 0/1 hold the upper state and rows 2/3 the lower state.

## Frozen input family

The known shielding witness has upper logical support `{-5,0}` and lower support `{0,1,3,4,6}`. To test whether this belongs to a small structural family rather than being an isolated accident, vary exactly two features while keeping the right upper pulse and lower origin fixed.

Upper states:

\[
A_k=\{-k,0\},\qquad k=1,2,\ldots,8.
\]

Lower states are every nonempty translation-normalized support contained in seven logical sites:

\[
\mathcal H_7=\{B\subseteq\{0,1,\ldots,6\}:0\in B\}.
\]

There are 64 lower states and therefore

\[
8\times64=512
\]

frozen encounters.

No additional displacement is varied in this census.

## Reference trajectory and shielding criterion

For each lower state `B`, evolve both:

1. the coupled field `C_t` from `U_0(A_k) union U_2(B)`;
2. the isolated lower reference `L_t` from `U_2(B)`.

Attempt direct evolution through fine tick 64 inclusive.

Record the first tick, if any, at which a negative inner-row defect appears:

\[
L_t(2,x)=1,\qquad C_t(2,x)=0.
\]

By the exact selector/dominance lemma already established, while rows `y>=3` agree this is precisely the defect polarity capable of breaking the protected lower outer row on the next tick.

Also record the first tick at which any row `y>=3` differs between coupled and isolated fields.

A case is `shielded-through-64` iff both events are absent through tick 64. This is a bounded discovery label, not an all-time theorem.

## Complete-field implementation check

Use both Research020 update kernels:

- cropped dense physical-field evolution;
- independently written sparse infinite-lattice scalar evolution.

They must agree on the complete changed-coordinate set for both coupled and isolated trajectories at every directly checked tick. Any disagreement invalidates the census.

Because a monolithic 512-case scalar run may exceed the execution ceiling, execution may be sharded by `k` without changing the frozen family, horizon, update routines, or criteria.

## Post-census analyses

Only after all 512 classifications are fixed may exploratory analysis ask whether shielding correlates with:

- upper separation `k`;
- lower mass or span;
- lower support polynomial over `GF(2)`;
- Rule-90 images/preimages of the lower support;
- exact local contact residues;
- common Boolean or polynomial factors among the shielding lower states.

Any algebraic law inferred from the census requires a fresh validation family or proof.

## Nonclaims

This census does not classify upper states with more than two bits, separations above eight, translated lower states, other relative alignments, or other physical laws. `shielded-through-64` is finite-horizon evidence only unless separately certified by an exact wall/bulk argument.
