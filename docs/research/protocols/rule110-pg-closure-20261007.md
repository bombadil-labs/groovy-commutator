# Protocol: does parity + centered Groovy form a closed local Rule-110 state?

**Status:** frozen before evaluation, 2026-10-07.  
**Authored by:** GPT-5.6 Sol (OpenAI). **Reviewed by:** none.

## Correction motivating this unit

The matched-history work proves that current centered Groovy plus the current
predictive-history label determines the next block-parity observation for Rule
110. A post-hoc local audit further proves

\[
(P_t,G_t^\circ)\longrightarrow P_{t+1}
\]

by a radius-one local factor on the full admissible source image.

That does **not** yet prove that \((P,G^\circ)\) is itself a closed Markov
state. Autonomous closure requires the next augmented state as well:

\[
(P_t,G_t^\circ)\longrightarrow(P_{t+1},G_{t+1}^\circ).
\]

This unit tests that missing condition exactly.

## Fixed definitions

Source rule: ECA Rule 110 on the full binary line.

Macro blocking: nonoverlapping pairs \((2j,2j+1)\).

Coarse cadence: two source updates.

Current macro symbol:

\[
Z_j=(P_j,G^\circ_{2j},G^\circ_{2j+1}),
\]

where

\[
P_j=X_{2j}\oplus X_{2j+1}.
\]

Next macro symbol:

\[
Z'_j=
\left(
P(H^2X)_j,
G^\circ(H^2X)_{2j},
G^\circ(H^2X)_{2j+1}
\right).
\]

## Gate A — radius-one full-state closure

Ask whether there exists an exact map

\[
F:(Z_{j-1},Z_j,Z_{j+1})\mapsto Z'_j
\]

on every admissible source context.

Enumerate the complete source window required by the three current macro
symbols and all three next output bits.

If Gate A passes, save the exact number of admissible input contexts and
continue to minimality.

If Gate A fails, save the lexicographically first exact pair of source windows
with equal current three-symbol context and unequal next augmented symbol.

## Gate B — bounded-radius closure search

Only if Gate A fails, test macro radii \(r=2,3\) exactly, each on its complete
source causal window.

Stop at the first radius that closes. If radius three still fails, end the unit
as a negative bounded result. Do not search larger radii in this protocol.

## Gate C — literal-coordinate minimality

If some radius \(r\le3\) closes, take its obvious raw feature grammar:
all current \(P\) bits and current centered-\(G\) bits in that macro radius.

Exhaust all coordinate subsets and find the minimum number of literal feature
bits whose values determine the entire next augmented symbol on the admissible
image.

This is minimum only within the frozen literal-coordinate grammar.

## Gate D — algebraic simplicity of the parity readout

Independently of full augmented closure, revisit the already-proved seven-bit
minimum literal subset for the next parity bit:

\[
(P_{j-1},G_{2j-1},P_j,G_{2j},G_{2j+1},P_{j+1},G_{2j+2}).
\]

On its 61 admissible input contexts, ask for the lowest algebraic degree over
\(\mathbb F_2\) of any Boolean polynomial extension that matches the target.

For the minimum degree, solve for:

- existence of an extension;
- minimum number of ANF monomials among all extensions at that degree, by exact
  exhaustive/branch-and-bound search over the finite affine solution space when
  feasible;
- one canonical minimum-support ANF.

If minimum-support search is too large for an exact bounded run, record degree
and affine solution-space dimension and stop that subgate rather than use a
heuristic.

## Decision meaning

A positive full-state closure would justify the phrase:

> current block parity plus current centered Groovy is an autonomous local
> coarse state for Rule 110 at cadence two.

A failure would require correcting the current research note to say only that
Groovy is a sufficient **readout correction** for next parity, not a closed
state.

The algebraic ANF result concerns why the parity readout is simple; it does not
by itself establish state closure.

## Scope

- exact full-line local identities only, via exhaustive finite causal windows;
- no Class-IV comparison;
- no all-rule census;
- no claim of globally minimal encoding beyond the declared literal-coordinate
  grammar;
- no off-image extension is interpreted as physically canonical.

## Planned artifacts

- scripts/verify_rule110_pg_closure.py
- results/rule110_pg_closure_20261007.json
- docs/research/2026-10-07-rule110-pg-closure.md
