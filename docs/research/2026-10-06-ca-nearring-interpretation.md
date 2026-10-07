# The near-ring home of Groovy

**Evidence:** exact algebra from the typed-difference unit plus established
near-ring prior art.  
**Authored by:** GPT-5.6 Sol (OpenAI), 2026-10-06. **Reviewed by:** none.

The handoff that opened the 2026-10-06 typed-difference unit proposed a
second-stage search for an algebra in which rule composition, polarization,
Groovy and dimensional lifting fit naturally. For the first three of those
objects, that algebra already has a name.

Timothy Boykett's 2024 paper *Near-rings of Cellular Automata* proves that
cellular automata over group-structured alphabets form a centralizer near-ring
under composition and cell-wise group addition. For binary cellular automata,
the addition is pointwise XOR. The paper is:
T. Boykett, *Journal of Cellular Automata* 18(1), 1–16 (2024),
doi:10.32908/jca.v18.310718.

This note records where the Groovy objects sit in that established structure.
It does not claim the near-ring of cellular automata as a new construction.

## 1. Why a near-ring appears

Let (mathcal N) be the set of binary cellular-automaton global maps of
arbitrary finite radius. Define

[
(Foplus G)(X)=F(X)oplus G(X),
qquad
FG=Fcirc G.
]

Composition is associative and pointwise XOR is an abelian group operation.
With the multiplication convention above,

[
(Foplus G)H=FHoplus GH
]

always. The other distributive law need not hold:

[
F(Goplus H)
stackrel{?}{=}FGoplus FH.
]

That one-sided distributivity is exactly the transformation-near-ring
phenomenon. Restricting to translation-equivariant continuous finite-memory
maps gives the cellular-automaton near-ring studied by Boykett.

Elementary rules are not closed under composition because radii grow; they are
a finite generating slice inside this larger finite-radius CA near-ring.

## 2. Polarization is the missing distributive law

For a zero-preserving map (F), define its right-input distributivity defect

[
R_F(G,H)
=
F(Goplus H)oplus FGoplus FH.
]

Evaluated at a configuration (X),

[
R_F(G,H)(X)
=
F(GXoplus HX)oplus F(GX)oplus F(HX)
=
B_F(GX,HX).
]

Thus the familiar polarization/cross-effect is precisely the term that prevents
the CA near-ring from being a ring on the other side.

For an arbitrary CA (F), center it first:

[
ar F(X)=F(X)oplus F(0).
]

Then (ar F(0)=0), and the same identity applies with (B_F=B_{ar F}).

So the project-specific object has a standard algebraic location:

[
oxed{
B_F
=
	ext{the missing distributivity term of the centered CA near-ring element }F.
}
]

This is compatible with the cohomological statement in the companion
typed-difference note: the same (B_F) is the exact group 2-coboundary
(deltaar F). The near-ring view says what algebraic law it measures;
the cohomology view says its ordinary (H^2) class is nevertheless trivial.

## 3. Groovy is one dynamically selected distributivity test

Let

[
D_H=Ioplus H.
]

The 2026-10-06 typed-difference result gives

[
G_H^circ(X)=B_H(X,D_HX).
]

In near-ring notation this is

[
oxed{
G_H^circ
=
R_{ar H}(I,D_H).
}
]

Because (Ioplus D_H=H), this can also be written

[
G_H^circ
=
ar H,H
oplus
ar H,I
oplus
ar H,D_H.
]

Groovy is therefore not an arbitrary nonlinearity score. It asks one particular
question about the missing distributive law: does it fail on the pair of maps
selected internally by the dynamics, (I) and (D_H)?

That explains both its usefulness and its blindness. All-pairs polarization
tests whether (ar H) is additive everywhere. Groovy samples the same
distributivity defect only on the graph picked out by the rule's own outgoing
change.

## 4. The linear/group-algebra case is the ring core

If (H) is a zero-preserving additive cellular automaton, then

[
H(Goplus K)=HGoplus HK
]

for all (G,K), so (H) is distributive on both sides. Additive cellular
automata therefore form the ring-like core inside the larger CA near-ring.

For group shifts this is the familiar group-algebra picture: convolution
kernels compose by group-algebra multiplication, and the corresponding linear
cellular automata compose in the same way. In the one-dimensional binary
finite-radius case the ring can be represented by Laurent polynomials over
(mathbb F_2); on a finite periodic ring the spatial group becomes cyclic.

This is the clean relation to the OpenAI-math group-algebra result that
motivated the handoff. The group-algebra construction is not a competing
description of nonlinear ECAs. It is the fully distributive linear subcase of
the already-known CA near-ring, while (B) records exactly the law that is
lost when one leaves that subcase.

## 5. Rules 4 and 200 generate a ring inside the near-ring

Let

[
P=H_4,qquad Q=H_{200}.
]

The exact radius-two audit in the companion unit established

[
Poplus Q=I,
qquad
P^2=P,
qquad
Q^2=Q,
qquad
PQ=QP=0.
]

Therefore the four maps

[
{0,P,Q,I}
]

are closed under XOR and composition and have exactly the multiplication and
addition table of the four-element Boolean ring
(mathbb F_2	imesmathbb F_2).

So "projection-like" can be sharpened:

> **Rules 4 and 200 are complementary orthogonal idempotents that generate a
> four-element Boolean ring inside the nonlinear CA near-ring.**

They remain nonlinear as functions on configuration space: neither is an
additive endomorphism of the configuration group. But the tiny algebra generated
by (I) and either rule happens to be ring-like. Groovy probes precisely that
tiny slice, so its vanishing is no longer mysterious.

The complete ECA ANF classification in
[the typed-difference note](2026-10-06-typed-difference-geometry.md) proves
that these are the only nonlinear elementary rules with
(G_H^circequiv0).

## 6. What this settles, and what it does not

The handoff asked whether we needed to invent a near-ring, operad or category
to house nonlinear rule composition. For binary CA, the near-ring part is
already established prior art. We should use it.

Within that existing algebra, this project can now state its objects cleanly:

- composition is near-ring multiplication;
- pointwise XOR is near-ring addition;
- additive/linear CA form the two-sided-distributive ring core;
- (B_F) is the missing distributivity cross-effect;
- (G_H^circ=R_{ar H}(I,D_H)) is the dynamically selected instance of that
  defect;
- the typed change bundle explains geometrically why the defect is a basepoint
  error;
- the affine-oriented lift stores enough temporal change data to avoid making
  that type error on its marked beam.

This does **not** yet identify the dimensional lift operator itself as a
near-ring functor, ideal construction, quotient, radical or extension. Those
would be separate claims requiring separate definitions and tests.

A concrete future question, if a downstream consumer needs it, is whether
other finite-radius nonlinear CAs with graph-restricted zero Groovy can be
classified by small ring substructures generated by (I) and (H), as Rules
4/200 are. That is now a mathematically specific question rather than a metric
census, but it is not automatically queued by this unit.
