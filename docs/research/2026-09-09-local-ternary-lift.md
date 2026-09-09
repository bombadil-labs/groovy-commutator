# Intrinsic local role growth removes the finite-ring ambiguity

The finite commutator and ternary-role censuses depend partly on the size of the periodic world. The same descendant transformations can instead be represented directly as local rules on the infinite one-dimensional lattice.

The [protocol](protocols/local-ternary-lift-20260909.md) freezes the same `L/R/C` operator, expands every descendant through depth four, and minimizes each local truth table to its exact centered radius. No periodic boundary conditions or Wolfram class labels enter the evaluation.

## Exact local result

Only **21 of 256** ECAs generate a cumulative local descendant vocabulary that is closed under all three `L/R/C` operations by depth four.

The closed rules are:

`0, 1, 4, 8, 12, 19, 36, 51, 55, 64, 68, 72, 76, 200, 204, 219, 223, 236, 239, 253, 255`.

Closure depths are 0 for one rule, 1 for nine, 2 for five, and 3 for six. No new rule first closes at depth four.

At the opposite extreme, **156 of 256** rules attain the universal role-count ceiling

\[
1,3,7,15,31
\]

at every exact depth through four.

Radius growth is widespread. By depth four, 230 rules have at least one descendant with the full possible minimal radius five, and 145 rules have **every** distinct depth-four descendant at radius five.

Rules 30, 54, 106, 110, and 184 all have the maximally expanding signature

\[
(1,3,7,15,31)
\]

and all 31 depth-four descendants have minimal radius five.

Thus strong local role growth is intrinsic rather than a torus artifact, but it is not Class-IV-exclusive.

## Rule 90 exposes why full ternary closure is too strong

On the width-eight finite map census, Rule 90 appeared to close after a few depths. Locally it does not.

Its exact-depth role counts are

\[
1,2,2,2,2.
\]

One branch is the zero residual created by its vanishing commutator. The other is a nonzero `L/R` descendant whose minimal radius grows

\[
1,2,3,4,5.
\]

So finite-ring wraparound eventually identifies maps that are genuinely distinct local rules on the infinite lattice.

More importantly, derivative transport does **not** require the entire `L/R/C` vocabulary to close. The update identity only needs each represented role and its `C`-correction. Rule 90 is therefore a warning against using full ternary closure as the dimensional-lift criterion: it correctly transports its derivative even while repeated time-composition paths keep generating larger-radius maps.

## What the local result changes

The ternary cube still supplies the canonical semantics of a commuting square, but the dynamical realization should be organized around the **correction map**

\[
C_F(A)=A\circ F\oplus F\circ A,
\]

not around retaining every `L` and `R` path as an autonomous role.

For any role `A`,

\[
A(F(S))=F(A(S))\oplus C_F(A)(S).
\]

Therefore a spatial layer carrying `A(S)` can be updated exactly if it can locally access a layer carrying its correction `C_F(A)(S)`.

This suggests a correction-stack lift: the extra dimension represents successive correction roles, while the base-dimensional neighborhood applies `F` within each layer. The next task is to formulate that lift as an explicit higher-dimensional local rule and determine when its correction graph admits a bounded, overlap-consistent Euclidean embedding.
