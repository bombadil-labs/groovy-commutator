# Rule 110: Groovy closes the parity readout, not its own augmented state

**Evidence:** exact exhaustive local computation plus an explicit infinite-line
counterexample.  
**Authored by:** GPT-5.6 Sol (OpenAI), 2026-10-07. **Reviewed by:** none.

The preceding matched-history unit established an exact and useful statement:

\[
(P_t,G_t^\circ)\longmapsto P_{t+1}
\]

for Rule 110 under nonoverlapping block-2 parity at cadence two. A post-hoc
local verifier showed that the next parity bit is a radius-one function of
current parity plus current centered Groovy.

That result was briefly described too strongly as closure of the augmented
state \((P,G^\circ)\). This unit tests the missing condition and corrects the
interpretation.

The correction is substantive:

\[
\boxed{
(P_t,G_t^\circ)\not\longmapsto(P_{t+1},G_{t+1}^\circ)
}
\]

even if the entire current fields are available on the infinite line.

So centered Groovy is an exact **readout correction coordinate** for next
parity in this construction, but it is not by itself an autonomous replacement
for the hidden history.

Protocol: [Rule-110 parity-G closure](protocols/rule110-pg-closure-20261007.md).  
Runner: [verify_rule110_pg_closure.py](../../scripts/verify_rule110_pg_closure.py).  
Result: [rule110_pg_closure_20261007.json](../../results/rule110_pg_closure_20261007.json).

## Radius-one augmented closure fails

Use macro symbols

\[
Z_j=(P_j,G^\circ_{2j},G^\circ_{2j+1}).
\]

The proposed autonomous law would require

\[
(Z_{j-1},Z_j,Z_{j+1})\mapsto Z'_j
\]

where

\[
Z'_j=
(P(H^2X)_j,G^\circ(H^2X)_{2j},G^\circ(H^2X)_{2j+1}).
\]

The complete ten-bit causal domain already contains a conflict.

Two source words 23 and 40 have identical current radius-one macro context

\[
(1,1,0,\;1,0,0,\;0,0,0)
\]

but their next augmented centre symbols are

\[
(1,0,0)
\qquad\text{and}\qquad
(1,1,0).
\]

The parity component agrees. The next Groovy component does not.

## Larger bounded radii fail too

The frozen radius-two and radius-three gates also fail exactly.

At radius two, source words 95 and 160 have the same five-symbol current
context but next augmented symbols \((1,0,0)\) and \((1,1,0)\).

At radius three, words 383 and 640 do the same across seven current macro
symbols.

Those failures are not independent accidents. They are finite prefixes of one
stronger full-line obstruction.

## An exact infinite-line counterexample

Define two bi-infinite source configurations:

\[
x_i=
\begin{cases}
1,&i\le-2\text{ or }i=0,\\
0,&\text{otherwise},
\end{cases}
\]

and

\[
y_i=
\begin{cases}
1,&i\in\{-1,1\},\\
0,&\text{otherwise}.
\end{cases}
\]

Their difference is the half-line mask

\[
x_i\oplus y_i=
\begin{cases}
1,&i\le1,\\
0,&i\ge2.
\end{cases}
\]

Thus the hidden distinction is a **blockwise complement phase domain wall**.

Nevertheless the entire present macro fields agree:

\[
Z(x)=Z(y).
\]

Away from the seam, \(x\) has an all-one left tail while \(y\) has an all-zero
left tail; both tails have macro symbol \((0,0,0)\). The right tails are both
zero. Locality reduces whole-line equality to a finite seam check, which gives

\[
\ldots,(0,0,0),(1,1,0),(1,0,0),(0,0,0),\ldots
\]

for both configurations.

After two Rule-110 updates, however, the centre macro symbols are

\[
Z'_0(x)=(1,0,0),
\qquad
Z'_0(y)=(1,1,0).
\]

Therefore even the **complete current \(P\) and \(G^\circ\) fields** do not
determine their own next augmented state.

No finite-radius law can repair that obstruction, because no present-only
whole-field factor exists.

This pinpoints the earlier matched-history result:

> **Groovy contains everything parity needs next, but not everything Groovy
> itself needs next.**

The hidden phase distinction is irrelevant to the immediate parity readout and
reappears first in the future correction field.

## The parity readout nevertheless has a compact exact algebra

The already-established literal-coordinate audit found that the next parity bit
requires all seven coordinates

\[
(P_{-1},G_{-1},P_0,G_0,G_1,P_1,G_2)
\]

within the frozen nine-coordinate radius-one grammar.

There are 61 admissible seven-bit contexts.

We asked for the lowest-degree Boolean polynomial over \(\mathbb F_2\) that
matches the next parity bit on those admissible contexts.

No extension exists at degree 0, 1 or 2.

Degree 3 is the exact minimum.

The degree-at-most-three system has 64 monomials, rank 58 and nullity 6, so
there are exactly

\[
2^6=64
\]

cubic off-image extensions.

Among them, the minimum ANF support is **nine monomials**, achieved by exactly
two extensions.

One canonical minimum-support formula is

\[
\begin{aligned}
P'_0={}&P_0\oplus G_0\oplus P_1\oplus G_2\\
&\oplus G_1P_1\oplus G_1G_2\oplus P_1G_2\\
&\oplus P_{-1}G_{-1}G_0
\oplus P_0G_1P_1.
\end{aligned}
\]

Writing

\[
M(a,b,c)=ab\oplus ac\oplus bc
\]

for the three-bit majority polynomial, this becomes

\[
\boxed{
P'_0=
P_0\oplus G_0\oplus P_1\oplus G_2
\oplus M(G_1,P_1,G_2)
\oplus P_{-1}G_{-1}G_0
\oplus P_0G_1P_1.
}
\]

So the correction is not linear: cubic context gates are irreducible in this
coordinate grammar.

## Admissibility itself has cubic structure

The two sparsest cubic formulas disagree off the physically reachable image but
are identical on every admissible Rule-110 context.

Their difference factors as

\[
\boxed{
G_2(1\oplus P_0)(1\oplus P_1\oplus G_1)=0
}
\]

on all 61 admissible contexts.

There are no nonzero linear or quadratic polynomial relations among the seven
coordinates; the first algebraic constraints on the admissible image appear at
degree three.

This is useful conceptually. The induced parity law is not a unique Boolean
function on the full seven-bit cube. The source dynamics only occupies a
constrained subset, and different off-image completions are genuinely
equivalent on the physical image.

## What changed

The earlier phrase

> "centered Groovy is a sufficient compressed-history state"

was too strong.

The exact replacement is:

> **For Rule 110 under block-2 parity at cadence two, centered Groovy is a
> sufficient present-time correction coordinate for the next parity readout,
> but parity plus Groovy is not an autonomous state.**

The distinction matters because the future Groovy field can reveal a hidden
phase distinction that neither current parity nor current Groovy sees.

This returns the project to its central question in a more precise form:
what additional coordinate is needed to make the correction field itself
coherent?

## Next structural target

The infinite witness suggests a concrete missing object rather than another
metric: a **block phase / phase-boundary coordinate**.

Block parity forgets the phase bit inside each pair. Current Groovy recovers
enough of that hidden phase to update parity, but the half-line complement
witness proves that some phase-boundary information remains invisible until
the next Groovy field.

A next unit, if pursued, should ask whether a compact phase coordinate added to
\((P,G^\circ)\) closes the augmented dynamics, and whether that coordinate is
strictly smaller than restoring the full microscopic pair state.
