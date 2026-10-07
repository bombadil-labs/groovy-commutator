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

## Post-hoc phase-gradient repair: closure by almost reconstructing the source

The infinite-line obstruction identifies a specific hidden object: the block
phase

\[
Q_j=X_{2j}.
\]

Block parity satisfies

\[
P_j=Q_j\oplus X_{2j+1},
\]

so parity forgets one phase bit per block.

The witness pair differs by a half-line flip of \(Q\). That suggests storing
the phase gradient

\[
\Phi_j=Q_j\oplus Q_{j+1}
=X_{2j}\oplus X_{2j+2}.
\]

Define the augmented symbol

\[
W_j=
(P_j,G^\circ_{2j},G^\circ_{2j+1},\Phi_j).
\]

A separate exact post-hoc verifier tests whether \(W\) updates autonomously at
cadence two.

Radius zero fails. Radius one fails.

At macro radius two, however, the full augmented state closes exactly:

\[
\boxed{
(W_{j-2},W_{j-1},W_j,W_{j+1},W_{j+2})
\longmapsto
W'_j
}
\]

on all \(2^{14}=16{,}384\) source words in the complete causal window,
covering 3,876 distinct admissible current contexts.

So the hidden phase gradient is enough to repair the failure of
\((P,G^\circ)\) autonomy.

But it is a poor compression.

Given \(P\) and \(\Phi\), choose one global phase bit \(Q_0\). The entire even
sublattice then follows from

\[
Q_{j+1}=Q_j\oplus\Phi_j,
\]

and every odd source bit follows from

\[
X_{2j+1}=Q_j\oplus P_j.
\]

Therefore \((P,\Phi)\) already reconstructs the source up to at most one global
complement bit. On every connected periodic ring its fibers have size exactly
two before adding Groovy; exhaustive rings 8, 10 and 12 reproduce that
two-to-one count.

Thus

\[
(P,G^\circ,\Phi)
\]

restores autonomous local coherence by retaining essentially the microscopic
state.

This is a blocked version of a pattern already present in the repository.
The 2026-09-22 Groovy-field census found that source spatial-gradient rails are
a universal one-bit repair for Groovy with history and noted that such
gradients determine the source up to global complement. The six-field lift
also carries explicit gradient rails. The new result is the Rule-110/block-
parity specialization: the hidden **block phase gradient** is precisely enough
to repair the present-time parity-plus-Groovy state, at radius two.

Verifier:
[verify_rule110_phase_gradient_repair.py](../../scripts/verify_rule110_phase_gradient_repair.py).  
Result:
[rule110_phase_gradient_repair_20261007.json](../../results/rule110_phase_gradient_repair_20261007.json).

The resulting hierarchy is now exact:

1. **Parity alone:** compressed but non-Markovian.
2. **Parity + centered Groovy:** enough for the next parity readout, but not
   enough to update Groovy itself.
3. **Parity + Groovy + block-phase gradient:** autonomous and local, but
   almost microscopically complete.

This sharply locates the remaining problem: find a state between levels 2 and
3, if one exists.

## Bounded middle-track search: simple present-time repairs are nearly injective

The phase-gradient repair closes the system by almost reconstructing the source.
To ask whether that was merely a poor feature choice, we searched a complete
simple track family.

For every radius-one Boolean function \(t\), define one extra bit per macroblock

\[
T_j=t(X_{2j-1},X_{2j},X_{2j+1}),
\]

and the current state

\[
V_j=(P_j,G^\circ_{2j},G^\circ_{2j+1},T_j).
\]

All 256 truth tables were tested exactly.

At macro radius one, **no track closes** the full augmented state.

At macro radius two, exactly

\[
\boxed{48/256}
\]

tracks close.

This is a stricter contract than the older Groovy-field track census: the
track must participate in a present-time autonomous state containing parity,
both Groovy bits and its **own next value**, not merely help predict next
Groovy under the older history contract.

The closing tracks were then evaluated as source encoders on rings 12, 14 and
16. They split into three exact 16-track groups:

| Closing-track family | width 12 | width 14 | width 16 |
| --- | --- | --- | --- |
| 16 tracks | 2 two-state fibers | 2 two-state fibers | 2 two-state fibers |
| 16 tracks | 1 two-state fiber | 1 two-state fiber | 1 two-state fiber |
| 16 tracks | injective | injective | injective |

Every other source fiber is a singleton.

Under the uniform source ensemble, the **largest** information loss among any
successful track is therefore only

\[
0.0009765625\text{ bits at }n=12,
\]

\[
0.000244140625\text{ bits at }n=14,
\]

and

\[
0.00006103515625\text{ bits at }n=16.
\]

So all successful encodings in this grammar are essentially microscopic.
Even the most compressive ones retain all but \(O(1)\) isolated source-pair
ambiguities over these rings.

The complete closing set is

\[
\begin{aligned}
\{&
48,49,50,51,52,54,56,57,58,59,60,62,80,82,84,85,\\
&86,87,88,90,92,93,94,95,160,161,162,163,165,167,\\
&168,169,170,171,173,175,193,195,196,197,198,199,\\
&201,203,204,205,206,207
\}.
\end{aligned}
\]

This family includes familiar gradient-like tracks such as 60 and 90, but the
negative is broader: **no** radius-one one-bit block track in the complete
256-table family supplies both radius-\(\le2\) present-time autonomy and a
meaningful finite-ring quotient.

Protocol:
[rule110-middle-tracks-20261007.md](protocols/rule110-middle-tracks-20261007.md).  
Runner:
[experiment_rule110_middle_tracks.py](../../scripts/experiment_rule110_middle_tracks.py).  
Result:
[rule110_middle_tracks_20261007.json](../../results/rule110_middle_tracks_20261007.json).

This does not rule out a middle state. It rules out a particularly natural,
complete simple grammar for one.

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
