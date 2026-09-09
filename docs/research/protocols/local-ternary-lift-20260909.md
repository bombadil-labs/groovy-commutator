# Protocol: intrinsic local growth of the ternary commutator lift

Date: 2026-09-09
Status: preregistered before evaluation

## Motivation

The finite width-eight ternary-lift census found strong rule-dependent role growth, but the commutator-tower fresh-width experiment showed that complete finite-map recurrence is substantially size-sensitive.

The ternary descendants themselves are local translation-invariant maps on the infinite one-dimensional lattice. Their **minimal local rule representations** can therefore be computed without choosing a finite ring.

This checkpoint measures that intrinsic local growth.

## Source family

Use all 256 elementary cellular automata, with no Wolfram class labels loaded.

Let the source update `F` be the radius-one ECA local map on the infinite lattice.

Start from

\[
D=I\oplus F.
\]

For any local map `A`, define

\[
L(A)=A\circ F,\qquad R(A)=F\circ A,
\]

\[
C(A)=L(A)\oplus R(A).
\]

These are the same frozen ternary-lift operators as the finite-map protocol.

## Exact local representation

Represent a local binary map by its complete truth table on a centered radius-`r` window.

Composition is evaluated exactly by expanding the input window as necessary:

- if `A` has radius `r`, then `L(A)` and `R(A)` have declared radius at most `r+1`;
- `C(A)` uses the same declared radius;
- after computing the full truth table, minimize radius by repeatedly dropping the leftmost and rightmost inputs only when the output is independent of both outer positions.

Canonical equality of two local maps means equality of their minimized radius and complete minimized truth table.

No periodic boundary conditions enter this computation.

## Frozen depth

Enumerate every ternary descendant through exact depth four.

The universal semantic ceiling at depths `0..4` is

\[
1,3,7,15,31.
\]

The maximum declared radius is five and the largest local truth table has `2^11 = 2048` rows.

Depth four is fixed before outcomes. No source is extended further based on its result in this checkpoint.

## Primary outputs per source rule

Record:

1. number of distinct canonical local maps at each exact depth;
2. cumulative distinct canonical maps through each depth;
3. number of newly appearing local maps at each depth;
4. minimal-radius histogram at each depth;
5. maximum minimal radius attained at each depth;
6. number of descendants that remain radius one or smaller;
7. first exact local closure depth within the explored vocabulary, if the cumulative role set is closed under `L/R/C`;
8. whether the rule attains the universal semantic ceiling at every depth through four.

## Cross-checks

- The all-`C` branch must agree with direct local construction of the commutator tower.
- Known zero-commutator rules must have local `C(D)=0` exactly.
- The universal identities `L(R(A))=R(L(A))` and `L(C(A))=C(L(A))` must hold on the canonical local tables generated in the census.

## Interpretation

A descendant whose minimal radius grows is demanding more **within-dimension causal context**. A higher-dimensional spatial realization may trade that growing context for additional represented channels.

A finite locally closed descendant vocabulary is much stronger than a repeated map on one periodic ring: it is an exact identity of local rules on the infinite lattice.

Maximal local role growth is also stronger than finite-map nonrecurrence, but it is not assumed to correspond to any Wolfram class.

## Anti-overfitting

- No class labels are loaded during evaluation.
- No rule-specific block size, radius cap, quotient, or tolerance is used.
- Local maps are minimized only by exact independence of outer input variables.
- The depth-four budget is frozen for every rule.

## Decision boundary

If a small subset closes locally by depth four, characterize its exact quotient graphs.

If a large subset shows maximal radius and role growth, derive the local algebra responsible before attaching class labels.

If the familiar complex rules differ from finite-width behavior, prefer this intrinsic local result when reasoning about dimensional liftability.