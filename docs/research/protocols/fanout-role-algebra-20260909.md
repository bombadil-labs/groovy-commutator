# Protocol: fan out state and derivative instead of storing rule as a state row

Date: 2026-09-09
Status: preregistered before evaluation

## Motivation

Two frozen role-algebra searches have failed for nonconstant sources:

1. selector-only application of one of `[r,s,delta]` to one of the three one-to-one role rows;
2. the same family augmented with either evolve or derivative mode on each row.

Both searches forced `r` to occupy and reproduce a physical **state row**. That is stronger than the derivative-completed lift requires: `r` is already present as the first block of the lifted **rule table**.

The higher state only needs enough channels to carry the evolving lower state and its derivative forward.

## Lower control family

Use all eight one-dimensional center-independent totalistic rules on the complete width-three state space.

For each predecessor `p`:

\[
s=F_r(p),\qquad d=p\oplus s,
\]

\[
s^+=F_r(s),\qquad d^+=s\oplus s^+.
\]

The lifted rule blocks remain

\[
B_0=r,\quad B_1=s,\quad B_2=d.
\]

## Frozen physical-row encodings

Use exactly three variable physical rows. Each row carries either the current state `S` or the current derivative `D`.

Require both semantic roles to appear at least once. With three rows, this gives exactly six ordered encodings:

`SSD, SDS, DSS, SDD, DSD, DDS`.

The same encoding is used at the next tick, replacing `S` by `s+` and `D` by `d+`. No role permutation or trajectory-specific reinterpretation is allowed.

This deliberately allows **fanout**: one semantic role can be represented in two physical rows.

## Allowed row operations

For each physical row, independently choose:

- one rule-block selector `q in {0,1,2}`;
- mode `Evolve`, giving `F_{B_q}(X)`; or
- mode `Derivative`, giving `X xor F_{B_q}(X)`.

There are six selector/mode choices per row and therefore

\[
6^3=216
\]

operation triples for each of the six row encodings, for

\[
1296
\]

frozen candidates total.

## Success criterion

A candidate succeeds for source rule `r` iff, on all eight predecessor states, applying the three declared row operations to the encoded current rows produces exactly the same row encoding of `(s+,d+)`.

Record:

- successful candidates per source rule;
- whether any candidate is universal;
- minimal number of derivative-mode rows among successes;
- whether successful candidates ever select the derivative rule block `q=2`;
- which duplicated semantic role (`S` or `D`) is used.

## Anti-overfitting

- All six encodings and all 216 operation triples per encoding are evaluated completely.
- No spatial guard geometry is chosen yet.
- No constant injection, arbitrary XOR between separate rows, fitted decoder, or class labels are allowed.
- The only fanout is literal duplication of `S` or `D` in the physical state encoding.

## Decision boundary

If a nonconstant source succeeds, freeze the successful fanout algebra and ask whether the required block selectors can be realized by an overlap-consistent higher-dimensional guard geometry.

If only constants succeed, the architecture needs either cross-row combination, more state channels, or a different notion of derivative transport.