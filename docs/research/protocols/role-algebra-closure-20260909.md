# Protocol: can rule, state, and derivative form a closed role algebra?

Date: 2026-09-09
Status: preregistered before evaluation

## Motivation

The derivative-completed lift produces a next-dimensional totalistic rule table with three equal-size blocks:

\[
L(r,s,\delta)=[r\mid s\mid\delta].
\]

The zero-guard spatial realization closes across one dimensional interface but fails to recurse on changing trajectories because it only ever addresses the first `rule` block.

Before adding more spatial geometry, test the smaller necessary question: **can the three represented roles update one another under the three available rule blocks in a fixed, rule-blind way?**

If no such role algebra exists, no arrangement of simple guard rows that merely chooses among those three blocks can repair recursive closure.

## Lower control family

Use all eight one-dimensional center-independent totalistic rules `r`, with complete width-three predecessor state space.

For each predecessor `p`, define

\[
s=F_r(p),\qquad
\delta=p\oplus s,
\]

and the next lower transition

\[
s^+=F_r(s),\qquad
\delta^+=s\oplus s^+.
\]

The three current role tables/rows are therefore

\[
B_0=r,\qquad B_1=s,\qquad B_2=\delta.
\]

Each is a three-bit center-independent totalistic table and can also be used as a three-cell side-three state.

## Frozen role-selector family

A variable row in the higher geometry can be surrounded so that its total neighbor count enters block 0, 1, or 2. Abstract this before spatialization by choosing, for each current semantic row `R`, `S`, and `D`, one rule-block selector

\[
(q_R,q_S,q_D)\in\{0,1,2\}^3.
\]

The row outputs are

\[
O_R=F_{B_{q_R}}(r),\qquad
O_S=F_{B_{q_S}}(s),\qquad
O_D=F_{B_{q_D}}(\delta).
\]

Enumerate all `3^3 = 27` selector triples.

## Fixed semantic phase / role permutation

Allow a fixed permutation `pi` of the three next semantic roles

\[
(r, s^+, \delta^+).
\]

This represents a rule-independent role phase: after one fine update, the three physical rows may cyclically or reflectively exchange semantic interpretation, provided the same permutation is used for every rule and every transition.

Enumerate all `3! = 6` permutations.

The complete role-algebra family therefore contains exactly

\[
27\times 6=162
\]

candidates.

## Success criterion

For a source rule `r`, a candidate `(q_R,q_S,q_D,pi)` succeeds iff for all eight predecessor states `p`, the ordered output triple

\[
(O_R,O_S,O_D)
\]

is exactly the permuted next-role triple

\[
\pi(r,s^+,\delta^+).
\]

Record per candidate and per source rule:

- success/failure;
- first failing predecessor and mismatching row;
- whether any successful candidate uses the derivative block `q=2`;
- whether the successful target permutation is identity or a nontrivial role cycle.

A **universal role algebra** succeeds for all eight source rules. A **nontrivial source role algebra** succeeds for at least one nonconstant source rule on all eight predecessor states.

## Anti-overfitting

- All 162 candidates are frozen before evaluation.
- No spatial guard pattern is chosen in this checkpoint.
- No Wolfram class labels are loaded.
- Candidate selectors/permutations are applied to every source rule; none is chosen using a favored rule number.

## Decision boundary

If at least one nontrivial source rule has a successful role algebra, freeze the successful algebra(s) and next ask whether their selector triples can be realized by an overlap-consistent transverse guard geometry.

If only constants succeed, derive the algebraic obstruction before adding more roles or operations.

If no source succeeds, the three-way selector architecture is insufficient even before spatialization; the next model must add an operation beyond choosing one of `r`, `s`, or `delta` as the rule for one of the three roles.