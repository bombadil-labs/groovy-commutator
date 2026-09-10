# Protocol: iterated commutator tower as a correction-role hierarchy

Date: 2026-09-09
Status: preregistered before evaluation

## Motivation

The all-ECA fanout role-algebra census found that ordinary state/derivative transport closes exactly on the zero-Groovy-commutator family, plus the special constant-derivative Rule 51.

For a fixed deterministic evolution `F`, define

\[
D(S)=S\oplus F(S).
\]

The Groovy commutator

\[
G(S)=D(F(S))\oplus F(D(S))
\]

is exactly the correction needed to transport the derivative:

\[
D(F(S))=F(D(S))\oplus G(S).
\]

Apply the same construction recursively. The resulting correction hierarchy is a canonical candidate for the extra roles required when derivative transport does not close at first order.

## Frozen finite substrate

Use the existing eight-cell periodic ECA substrate and standard truth-table mapping used by the all-ECA fanout census.

For each source rule `r`, let

\[
F_r:X\to X,\qquad X=\{0,1\}^8.
\]

All maps below are evaluated exactly on all 256 states. No Wolfram class labels are loaded.

## Tower definition

Define the first correction map

\[
A_1(S)=D_r(S)=S\oplus F_r(S).
\]

For `k >= 1`, define

\[
A_{k+1}(S)=A_k(F_r(S))\oplus F_r(A_k(S)).
\]

Thus:

- `A1` is the derivative;
- `A2` is the ordinary Groovy commutator;
- `A3` is the correction needed to transport `A2` under `F`;
- generally,

\[
A_k(F(S))=F(A_k(S))\oplus A_{k+1}(S).
\]

No alternate normalization or state-dependent stopping rule is permitted.

## Frozen horizon

Evaluate levels

\[
A_1,\ldots,A_{256}.
\]

The horizon is fixed before outcomes. A repeat before or at level 256 is exact on this finite substrate; absence of a repeat by level 256 is reported as right-censored, not extrapolated.

## Primary outputs per source rule

Record:

1. **first zero level** — smallest `k` with `A_k(S)=0` for all `S`, if any;
2. **first constant level** — smallest `k` with `A_k` independent of `S`, including zero;
3. **first repeat** — lexicographically earliest pair `j < k` with `A_j = A_k` as complete functions `X -> X`;
4. **distinct tower maps through level 256**;
5. **image size** `|A_k(X)|` at each level;
6. **nonzero-state count** at each level;
7. whether a repeat is a fixed point (`A_{k+1}=A_k`), a zero tail, or a longer cycle.

## Secondary structural summaries

Before attaching class labels, group rules by complete tower signature:

- zero/constant depth;
- repeat preperiod and period where observed;
- sequence of image sizes for the first 16 levels;
- sequence of nonzero-state counts for the first 16 levels.

Also cross-check that the known zero-commutator family has `A2=0` exactly and that constant-commutator rules have constant `A2`, reproducing the earlier algebra note.

## Interpretation

A tower terminating at level `h` gives an exact finite correction hierarchy: transporting role `A_{h-1}` needs no further residual.

A periodic tower gives a finite recurrent correction vocabulary on this finite substrate, though it does not by itself supply a spatial realization.

A long nonrepeating tower suggests that progressively higher correction roles continue to be generated.

This protocol does **not** assume that short, long, or periodic towers correspond to any Wolfram class. The previously preregistered Class-IV conjecture is downstream: labels are attached only after the complete structural tower table is frozen.

## Decision boundary

If tower signatures collapse to a small number of exact families, characterize those families algebraically before spatializing them.

If a subset has unusually long/nonrepeating towers, test fresh ring widths before interpreting that as intrinsic rather than finite-size behavior.

If the tower is short for nearly every rule, the correction hierarchy is architectural rather than selective and cannot by itself be the dimensional-lift razor.