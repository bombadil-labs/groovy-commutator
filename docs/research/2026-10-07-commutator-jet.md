# The commutator jet internalizes successive transport errors

**Evidence:** exact Boolean algebra, exhaustive finite-ring computation and
complete local truth tables for Rules 110 and 62.  
**Authored by:** GPT-5.6 Sol (OpenAI), 2026-10-07. **Reviewed by:** none.

The latent-Q discussion suggested a recursive interpretation:

- \(D\) is current change;
- \(G\) is the correction required to transport \(D\);
- \(Q\) should be the correction required to transport \(G\);
- \(R\) should correct \(Q\); and so on.

This unit makes that construction exact.

Protocol: [intrinsic commutator jet](protocols/commutator-jet-20261007.md).  
Runner: [experiment_commutator_jet.py](../../scripts/experiment_commutator_jet.py).  
Result: [commutator_jet_20261007.json](../../results/commutator_jet_20261007.json).

## Definition

For any configuration-valued observable \(A\), define

\[
\mathcal C_H(A)=A\circ H\oplus H\circ A.
\]

Start with

\[
A_0=D_H=I\oplus H
\]

and recursively set

\[
A_{k+1}=\mathcal C_H(A_k).
\]

We name

\[
A_0=D,\qquad A_1=G,\qquad A_2=Q,\qquad A_3=R.
\]

Along a source trajectory \(S_{t+1}=H(S_t)\),

\[
\boxed{
A_{k,t+1}=H(A_{k,t})\oplus A_{k+1,t}.
}
\]

So each new field is literally the residual needed to evolve the previous
field coherently under the source rule.

This is the exact same structural move at every level.

## The cadence-two future coordinate is a nonlinear jet combination

The parity-history work used cadence

\[
F=H^2.
\]

For any \(A\),

\[
\mathcal C_{H^2}(A)
=
A\circ H^2\oplus H^2\circ A.
\]

Expanding the one-step recurrences gives the exact identity

\[
\boxed{
\mathcal C_{H^2}(A)
=
\mathcal C_H^2(A)
\oplus
B_H\!\big(H\circ A,\mathcal C_H(A)\big)
\oplus H(0).
}
\]

For zero-preserving Rules 110 and 62,

\[
\boxed{
\mathcal C_{H^2}(A)
=
\mathcal C_H^2(A)
\oplus
B_H\!\big(H\circ A,\mathcal C_H(A)\big).
}
\]

For \(A=G\),

\[
\boxed{
\mathcal C_{H^2}(G)
=
R\oplus B_H(H(G),Q).
}
\]

This corrects a tempting oversimplification. The cadence-two complement of
\(G\) is not simply the one-step \(Q\) or \(R\). Nonlinearity contributes an
additional polarization term.

The temporal coordinate \(G(H^2S)\) found in the latent-Q unit is still
equivalent, given current \(G\), to the intrinsic cadence-two residual
\(\mathcal C_{H^2}(G)\). The two are related by

\[
G(H^2S)=H^2(G(S))\oplus\mathcal C_{H^2}(G)(S).
\]

Thus the user's "future value versus present derived field" analogy is exact,
but the intrinsic present-time field at cadence two is itself a nonlinear
combination of the one-step jet.

## Rules 110 and 62 are matched already at D

For an ECA,

\[
D_H(S)=S\oplus H(S)
\]

is itself an ECA with truth-table number

\[
D\text{-rule}=H\text{-rule}\oplus204.
\]

Therefore

\[
D_{110}=\text{Rule }162,
\qquad
D_{62}=\text{Rule }242.
\]

And exactly,

\[
242=\mathrm{reflect}(\mathrm{conjugate}(162)).
\]

So the derivative maps of Rules 110 and 62 are symmetry-equivalent.

This explains why their finite-ring \(D\)-fiber statistics are identical in
the matched experiment. The pair begins with the same change geometry up to
the standard ECA symmetry, then diverges when the different source rules act
back on that change field through \(G\).

That makes the pair a particularly useful test of situated transport rather
than merely a convenient empirical match.

## The local jet becomes rapidly more nonlinear

Complete source-window truth tables give:

| Rule | Field | minimum radius | ANF degree | ANF terms | activity |
| ---: | --- | ---: | ---: | ---: | ---: |
| 110 | D | 1 | 3 | 3 | 0.3750 |
| 110 | G | 2 | 4 | 4 | 0.3125 |
| 110 | Q | 3 | 6 | 20 | 0.3281 |
| 110 | R | 4 | 9 | 102 | 0.4004 |
| 110 | A4 | 5 | 9 | 294 | 0.4199 |
| 110 | A5 | 6 | 12 | 812 | 0.4846 |
| 62 | D | 1 | 3 | 5 | 0.6250 |
| 62 | G | 2 | 4 | 6 | 0.1875 |
| 62 | Q | 3 | 6 | 22 | 0.4844 |
| 62 | R | 4 | 8 | 90 | 0.4102 |
| 62 | A4 | 5 | 10 | 346 | 0.4424 |
| 62 | A5 | 6 | 11 | 1,660 | 0.4653 |

Every tested level uses its full expected source radius. The tower does not
collapse to a smaller pointwise rule in these coordinates.

The algebraic degree and support grow quickly. The successive latent fields
are therefore not merely shifted or relabelled copies of one another.

## Frozen primary finite-ring result: D + G already nearly determines S

For the frozen \(D\)-anchored prefix

\[
J_k=(D,G,Q,\ldots,A_k),
\]

both rules reach global finite-ring closure at

\[
\boxed{k=1}
\]

on every tested width 8 through 16.

That is, \(Q\) is globally determined by the complete current pair \((D,G)\)
on each tested ring.

But the reason is not attractive compression.

### Rule 62

For Rule 62,

\[
(D,G)
\]

is completely injective on every tested ring. It reconstructs the source
exactly.

### Rule 110

For Rule 110, \((D,G)\) is injective on widths 10 and 14.

At widths 8, 12 and 16, it has exactly two size-two ambiguous fibers and all
other source states are singletons. Those four exceptional source states are
the four phases of the period-four background \(1110\), with opposite phases
paired.

The source information safely forgotten by \((D,G)\) is therefore:

| n | Rule 110 | Rule 62 |
| ---: | ---: | ---: |
| 8 | 0.015625 bits | 0 |
| 10 | 0 | 0 |
| 12 | 0.0009765625 | 0 |
| 14 | 0 | 0 |
| 16 | 0.0000610352 | 0 |

So the finite global closure is another near-microscopic closure, not a useful
compression theorem.

## But full-line locality separates the matched pair

Finite-ring near-injectivity does not imply a local full-line factor.

Ask whether the next jet field \(Q_i\) is determined by a finite neighborhood
of current \(D\) and \(G\).

For Rule 110, exact complete local-window checks fail at radii

\[
0,1,2,3.
\]

For Rule 62, radii 0, 1 and 2 fail, but radius 3 passes exactly:

\[
\boxed{
Q_i
=
F\big((D,G)_{i-3:i+3}\big)
\quad\text{for Rule 62}.
}
\]

There are 279 admissible radius-three contexts.

Thus Rule 62 has an exact present-only local \((D,G)\) dynamics under this
contract:

\[
D' = H(D)\oplus G,
\]

and

\[
G' = H(G)\oplus Q(D,G).
\]

The corresponding Rule-110 factor is absent through radius three.

This is an exact mechanistic difference between two rules whose derivative
maps are symmetry-equivalent.

It is not yet a proof that no finite Rule-110 radius exists.

## Post-hoc diagnostic: anchor the jet at G

The frozen protocol started at \(D\). After seeing that \((D,G)\) is nearly
lossless, we also inspected the tower beginning at

\[
(G,Q,R,\ldots).
\]

This is explicitly post-hoc and is not a frozen decision gate.

### Rule 110

On every tested width 8 through 16, the prefix

\[
\boxed{(G,Q,R)}
\]

already determines the next jet field \(A_4\).

The remaining source uncertainty after \((G,Q,R)\) falls rapidly:

| n | source bits forgotten by G | by (G,Q) | by (G,Q,R) |
| ---: | ---: | ---: | ---: |
| 8 | 1.6693 | 0.1719 | 0.0469 |
| 10 | 2.0199 | 0.1910 | 0.00781 |
| 12 | 2.4210 | 0.2264 | 0.00293 |
| 14 | 2.8115 | 0.2619 | 0.000488 |
| 16 | 3.2108 | 0.2991 | 0.000183 |

Again, finite closure is purchased by approaching microscopic identity.

And despite global finite-ring closure, no radius-0 through radius-3 local
factor from \((G,Q,R)\) to \(A_4\) exists on the complete local source domain.

### Rule 62

The G-anchored closure depth grows across the small widths before stabilizing in
this bounded experiment:

| n | first closing prefix |
| ---: | --- |
| 8 | G,Q,R |
| 10 | G,Q,R,A4 |
| 12 | G,Q,R,A4,A5 |
| 14 | G,Q,R,A4,A5 |
| 16 | G,Q,R,A4,A5 |

At width 16,

\[
H(S\mid G,Q,R)\approx0.12868\text{ bits},
\]

and the later fields continue splitting those remaining source fibers until the
prefix through \(A_5\) is nearly injective.

The first finite-ring closing prefix also fails all tested local radii 0 through
3.

This is not evidence that Rule 62 is "more complex" than Rule 110. It says only
that the exact commutator jet organizes their hidden source distinctions
differently.

## The cadence-two nonlinear correction is substantial

For the #323-style cadence-two residual of \(G\),

\[
\mathcal C_{H^2}(G)
=
R\oplus B_H(H(G),Q),
\]

the polarization term is not a negligible edge case.

On the complete radius-four source truth table:

| Rule | activity of \(C_{H^2}(G)\) | activity of R | activity of polarization correction | fraction equal to R |
| ---: | ---: | ---: | ---: | ---: |
| 110 | 0.4414 | 0.4004 | 0.1855 | 0.8145 |
| 62 | 0.4258 | 0.4102 | 0.1875 | 0.8125 |

So roughly 19% of local source contexts carry a genuine nonlinear cadence
correction beyond \(R\).

This is exactly where the temporal-vs-intrinsic analogy differs from a linear
finite-difference tower.

## What survives

The strongest result of this unit is structural, not classificatory.

The construction

\[
D,\quad G,\quad Q,\quad R,\ldots
\]

is a genuine same-lattice hierarchy of successive transport residuals:

\[
\boxed{
A_{k+1}
=
\text{the information needed to correct naive }H\text{-transport of }A_k.
}
\]

A future field and an intrinsic residual are two coordinate presentations of
the same missing temporal information once the current field is known.

But for nonlinear rules, changing cadence mixes adjacent jet orders through
polarization. The tower is therefore better understood as a **nonlinear
commutator jet** than as ordinary successive temporal differences.

The finite-ring closures found here are mostly near-injective and should not be
read as compression advantages.

The matched 110/62 comparison is nevertheless informative:

> **Their derivatives are symmetry-equivalent, but their higher transport
> residuals organize differently.**

That is a cleaner statement of where their dynamics diverge than the earlier
history-budget comparison.

## Next question

The useful next question is no longer whether \(Q\) exists. It does, canonically:

\[
Q=\mathcal C_H(G).
\]

The next question is whether the **infinite jet**

\[
G,Q,R,A_4,\ldots
\]

admits a smaller symbolic/state-space presentation than its raw fields.

The local truth tables rapidly become large, while finite-ring prefixes become
nearly source-injective. A promising next route is therefore to minimize the
**language of realized jet configurations**, not add more source-derived
features.

That would ask whether the jet has a compact constrained subshift / finite
presentation even when its naive binary-field coordinates are redundant.
