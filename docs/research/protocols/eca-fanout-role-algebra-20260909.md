# Protocol: fanout role algebra across all 256 elementary cellular automata

Date: 2026-09-09
Status: preregistered before evaluation

## Motivation

The frozen three-cell totalistic control found a nonconstant fanout role algebra for the Rule-90 / Rule-165 affine pair. For Rule 90, two state channels and one derivative channel can all evolve under the source rule because linear evolution transports XOR differences exactly.

The next outcome-independent step is to apply **the identical role-algebra family** to the full elementary cellular-automaton rule space using the project's existing eight-bit shared state/rule substrate.

No new operation, role encoding, or favorable rule-specific mapping is added in this checkpoint.

## Shared eight-bit substrate

Use periodic eight-cell binary rings. Every eight-bit pattern can be read either as a ring state or as an ECA truth table.

Freeze the default identity rule-table mapping from the earlier shared-state-rule experiment:

- truth-table output bit `k` is pattern bit `k`;
- ECA input address is `4L+2C+R`;
- all updates are synchronous.

Alternative ring permutations are **not** searched in this checkpoint. They remain a later spatialization-family question if the fixed algebra produces a selective source set.

Let

\[
E_a(x)
\]

denote applying the ECA rule decoded from eight-bit pattern `a` to eight-cell ring state `x`.

## Source transitions

For every source ECA rule

\[
r\in\{0,\ldots,255\}
\]

and every predecessor ring state

\[
p\in\{0,\ldots,255\},
\]

define

\[
s=E_r(p),\qquad d=p\oplus s,
\]

\[
s^+=E_r(s),\qquad d^+=s\oplus s^+.
\]

The three available role blocks are the eight-bit patterns

\[
B_0=r,\qquad B_1=s,\qquad B_2=d,
\]

and each can itself be decoded as an ECA rule through the same frozen identity mapping.

## Frozen state-row encodings

Use exactly the six three-row fanout encodings from the successful control protocol:

`SSD, SDS, DSS, SDD, DSD, DDS`.

The same encoding is required at the next tick, replacing `S` by `s+` and `D` by `d+`.

## Frozen row operations

For each physical row choose independently:

- rule-block selector `q in {0,1,2}`;
- **Evolve**: `E_{B_q}(X)`; or
- **Derivative**: `X xor E_{B_q}(X)`.

There are six selector/mode choices per row, 216 operation triples per row encoding, and therefore

\[
6\times216=1296
\]

candidate fanout algebras.

These are exactly the candidates declared in `fanout-role-algebra-20260909.md`, with only the pattern width/rule engine enlarged from 3 to 8.

## Success criterion

A candidate succeeds for source rule `r` iff for **all 256 predecessor states** its three row outputs equal the same fixed fanout encoding of `(s+,d+)`.

Record before attaching any external class labels:

- number of successful candidates per source ECA;
- source rules with at least one successful fanout algebra;
- whether any candidate is universal across all 256 sources;
- successful row encodings and selector/mode triples;
- whether success uses derivative mode;
- whether success selects the derivative block `q=2`;
- symmetry/conjugacy relationships visible directly in the structural result.

## Controls

The evaluator must reproduce the three-cell control qualitatively when restricted to equivalent Rule-90/165 behavior, but no source is privileged in search order or scoring.

No Wolfram class labels, glider facts, universality labels, or prior class assignments are loaded before the complete structural success table is saved.

## Relation to the Class-IV conjecture

This is the first derivative-active role-algebra census on the **full 256-rule ECA space**. It is still not the final dimensional-lift criterion because spatial guard realizability and recursive dimensional closure remain downstream constraints.

The previously preregistered Class-IV hypothesis is evaluated only after the structural table is frozen. Exact exclusivity, enrichment, affine concentration, or broad failure are all valid outcomes; the algebra family is not retuned afterward.

## Decision boundary

If a small nontrivial source subset succeeds, characterize it algebraically and only then attach frozen class labels.

If a large/universal family succeeds, fanout role closure is architectural and spatial/recursive constraints must provide selectivity.

If only affine/additive rules succeed, record that the fanout algebra is another form of derivative/evolution commutation and do not reinterpret it as Class-IV evidence.