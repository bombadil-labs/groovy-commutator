# Protocol: close the role algebra by allowing evolution or derivative

Date: 2026-09-09
Status: preregistered before evaluation

## Motivation

The selector-only role-algebra census found no nonconstant source rule for which the three represented roles

\[
(r,s,\delta)
\]

can close by merely choosing one of the three blocks as the rule acting on each role row.

The missing target is structurally obvious:

\[
\delta^+=s\oplus F_r(s).
\]

That is exactly a discrete derivative. The next minimal extension therefore allows each row to apply either **evolution** or **derivative-of-evolution** under one selected role block.

No other Boolean operation is admitted.

## Lower control family

Use all eight one-dimensional center-independent totalistic rules on the complete width-three state space.

For every predecessor `p`:

\[
s=F_r(p),\qquad \delta=p\oplus s,
\]

\[
s^+=F_r(s),\qquad \delta^+=s\oplus s^+.
\]

Current role blocks are

\[
B_0=r,\quad B_1=s,\quad B_2=\delta.
\]

## Allowed row operations

For a row containing state `X` and a selected role block `B_q`, allow exactly two modes:

**Evolve**

\[
E_q(X)=F_{B_q}(X),
\]

or **Derivative**

\[
D_q(X)=X\oplus F_{B_q}(X).
\]

For each of the three current semantic rows `R`, `S`, `D`, choose one selector `q in {0,1,2}` and one mode `E` or `D`.

There are

\[
(3\times2)^3=216
\]

row-operation triples.

As in the selector-only protocol, allow one fixed permutation of the next semantic roles `(r,s+,delta+)`. There are six permutations, giving exactly

\[
216\times6=1296
\]

candidate Groovy role algebras.

## Success criterion

A candidate succeeds for a source rule iff for all eight predecessor states the three row outputs equal the fixed permuted target triple

\[
\pi(r,s^+,\delta^+).
\]

Record:

- all successful source/candidate pairs;
- whether a universal candidate exists;
- which rows use derivative mode;
- whether successful candidates genuinely depend on the derivative role block `q=2`;
- whether the target permutation is identity or a nontrivial role phase.

## Anti-overfitting

- All 1296 candidates are frozen before evaluation.
- The only new operation relative to the failed selector-only family is XOR with a row's own evolved image.
- No constants, arbitrary Boolean combinations, fitted decoders, spatial guard choices, or class labels are introduced.
- Every candidate is applied to every source rule.

## Decision boundary

If a nonconstant source admits at least one Groovy role algebra, freeze the successful algebra family and next test whether its selectors/modes have a literal higher-dimensional spatial realization.

If only constants succeed, the next model must add information or another operation beyond evolution and first difference.

If a universal candidate exists, the role algebra is architectural rather than selective; recursive spatial closure becomes the next possible discriminator.