# The near-ring home of Groovy

**Evidence:** exact algebra from the typed-difference unit plus established
near-ring prior art.  
**Authored by:** GPT-5.6 Sol (OpenAI), 2026-10-06. **Reviewed by:** none.

The handoff that opened the 2026-10-06 typed-difference unit proposed a
second-stage search for an algebra in which rule composition, polarization,
Groovy and dimensional lifting fit naturally. For the first three of those
objects, that algebra already has a name.

Timothy Boykett's 2024 paper
[*Near-rings of Cellular Automata*](https://doi.org/10.32908/jca.v18.310718)
shows that cellular automata over group-structured alphabets form a centralizer
near-ring under composition and cell-wise group addition. For binary cellular
automata, the addition is pointwise XOR.

This note records where the Groovy objects sit in that established structure.
It does not claim the near-ring of cellular automata as a new construction.

## 1. Why a near-ring appears

Let \(\mathcal N\) be the set of binary cellular-automaton global maps of
arbitrary finite radius. Define

\[
(F\oplus G)(X)=F(X)\oplus G(X),
\qquad
FG=F\circ G.
\]

Composition is associative and pointwise XOR is an abelian group operation.
With this multiplication convention,

\[
(F\oplus G)H=FH\oplus GH
\]

always. The other distributive law need not hold:

\[
F(G\oplus H)
\stackrel{?}{=}
FG\oplus FH.
\]

That one-sided distributivity is the transformation-near-ring phenomenon.
Restricting to translation-equivariant continuous finite-memory maps gives the
cellular-automaton near-ring studied by Boykett.

Elementary rules are not closed under composition because radii can grow; they
are a finite slice inside this larger finite-radius CA near-ring.

## 2. Polarization is the missing distributive law

For a zero-preserving map \(F\), define its input-side distributivity defect

\[
R_F(G,H)
=
F(G\oplus H)\oplus FG\oplus FH.
\]

Evaluated at a configuration \(X\),

\[
R_F(G,H)(X)
=
F(GX\oplus HX)\oplus F(GX)\oplus F(HX)
=
B_F(GX,HX).
\]

Thus the familiar polarization/cross-effect is precisely the term that
prevents the CA near-ring from being a ring on the other side.

For an arbitrary CA \(F\), center it first:

\[
\bar F(X)=F(X)\oplus F(0).
\]

Then \(\bar F(0)=0\), and \(B_F=B_{\bar F}\). Therefore

\[
\boxed{
B_F
=
\text{the missing distributivity term of the centered near-ring element }F.
}
\]

This complements the cohomological statement in the companion
[typed-difference note](2026-10-06-typed-difference-geometry.md): the same
\(B_F\) is the exact group 2-coboundary \(\delta\bar F\). The near-ring view
states which algebraic law it measures; ordinary group cohomology states that
its cohomology class is nevertheless trivial.

## 3. Groovy is one dynamically selected distributivity test

Let

\[
D_H=I\oplus H.
\]

The typed-difference result gives

\[
G_H^\circ(X)=B_H(X,D_HX).
\]

In near-ring notation this is

\[
\boxed{
G_H^\circ
=
R_{\bar H}(I,D_H).
}
\]

Since \(I\oplus D_H=H\), it may also be written

\[
G_H^\circ
=
\bar H H
\oplus
\bar H I
\oplus
\bar H D_H.
\]

Groovy is therefore not an arbitrary nonlinearity score. It asks one particular
question about the missing distributive law: does it fail on the pair of maps
selected internally by the dynamics, \(I\) and \(D_H\)?

That explains both its usefulness and its blindness. All-pairs polarization
tests whether \(\bar H\) is additive everywhere. Groovy samples the same
distributivity defect only on the graph picked out by the rule's own outgoing
change.

## 4. The linear/group-algebra case is the ring core

If \(H\) is a zero-preserving additive cellular automaton, then

\[
H(G\oplus K)=HG\oplus HK
\]

for all \(G,K\). Additive cellular automata therefore form the
two-sided-distributive ring core inside the larger CA near-ring.

For group shifts this is the familiar group-algebra picture: convolution
kernels compose by group-algebra multiplication, and the corresponding linear
cellular automata compose in the same way. In the one-dimensional binary
finite-radius case this ring can be represented by Laurent polynomials over
\(\mathbb F_2\); on a finite periodic ring the spatial group becomes cyclic.

This is the clean relation to the OpenAI-math group-algebra result that
motivated the handoff. The group-algebra construction is not a competing
description of nonlinear ECAs. It is the fully distributive linear subcase of
the already-known CA near-ring, while \(B\) records exactly the law that is
lost when one leaves that subcase.

## 5. Rules 4 and 200 generate a ring inside the near-ring

Let

\[
P=H_4,\qquad Q=H_{200}.
\]

The exact radius-two audit in the companion unit establishes

\[
P\oplus Q=I,
\qquad
P^2=P,
\qquad
Q^2=Q,
\qquad
PQ=QP=0.
\]

Therefore the four maps

\[
\{0,P,Q,I\}
\]

are closed under XOR and composition and have exactly the addition and
multiplication tables of the four-element Boolean ring

\[
\mathbb F_2\times\mathbb F_2.
\]

So the earlier phrase “projection-like complements” can be sharpened:

> **Rules 4 and 200 are complementary orthogonal idempotents that generate a
> four-element Boolean ring inside the nonlinear CA near-ring.**

They remain nonlinear as functions on configuration space: neither is an
additive endomorphism of the configuration group. But the tiny algebra
generated by \(I\) and either rule happens to be ring-like.

This gives an algebraic explanation of their zero Groovy field. Since
\(D_P=Q\) and \(D_Q=P\),

\[
G_P
=
D_P P\oplus P D_P
=
QP\oplus PQ
=
0,
\]

and symmetrically \(G_Q=0\).

The complete ECA ANF classification in
[the typed-difference note](2026-10-06-typed-difference-geometry.md) proves
that Rules 4 and 200 are the only nonlinear elementary rules with
\(G_H^\circ\equiv0\).

This small ring is structurally suggestive, but no novelty is claimed for the
idempotence itself. Idempotent cellular automata are an explicit subject of
Castillo-Ramirez, Magaña-Chavez and Veliz-Quintero,
[*Idempotent cellular automata and their natural order*](https://doi.org/10.1016/j.tcs.2024.114698),
and elementary-rule composition has been studied separately. The specific
complementary-XOR/mutual-annihilation identification is the project-level
observation relevant to Groovy.

## 6. The typed geometry and near-ring algebra say the same thing from two sides

The companion note defines the nonlinear cocycle

\[
\Phi_n(X,U)
=
H^n(X\oplus U)\oplus H^n(X),
\]

which transports a based change \(U\) along the base orbit \(X\mapsto H^nX\).
At one step the fibre map is \(\partial H_X(U)\).

The near-ring defect \(B_H(X,U)\) compares this transport at two basepoints:

\[
B_H(X,U)
=
\partial H_X(U)\oplus\partial H_0(U).
\]

So the two views are equivalent descriptions of the same nonlinearity:

- **typed geometry:** a change cannot generally be transported without its
  basepoint;
- **near-ring algebra:** left composition by a nonlinear \(H\) is not
  distributive over XOR in its input.

Centered Groovy chooses the particular change \(U=D_HX\) selected by the
dynamics itself.

## 7. What this settles, and what it does not

The handoff asked whether we needed to invent a near-ring, operad or category
to house nonlinear rule composition. For binary CA, the near-ring part is
already established prior art. We should use it.

Within that existing algebra, this project can now state its objects cleanly:

- composition is near-ring multiplication;
- pointwise XOR is near-ring addition;
- additive/linear CA form the two-sided-distributive ring core;
- \(B_F\) is the missing distributivity cross-effect;
- \(G_H^\circ=R_{\bar H}(I,D_H)\) is the dynamically selected instance of that
  defect;
- the nonlinear finite-difference cocycle explains geometrically why that
  defect is a basepoint error;
- the affine-oriented lift stores enough temporal change data to avoid making
  that type error on its marked beam.

This does **not** identify the dimensional lift operator itself as a near-ring
functor, ideal construction, quotient, radical or extension. Those would be
separate claims requiring separate definitions and tests.

A concrete future question, if a downstream consumer needs it, is whether
other finite-radius nonlinear CAs with graph-restricted zero Groovy can be
classified by small ring substructures generated by \(I\) and \(H\), as Rules
4/200 are. That is now a mathematically specific question rather than a metric
census, but it is not automatically queued by this unit.
