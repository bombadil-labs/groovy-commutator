# Protocol: stronger dimensionality test for intertwining lifts

## Why this follow-up exists

The first dimensional-intertwining protocol measured the linear rank of essential input offsets relative to the output cell. After the first evaluation, a moving-frame objection became clear: if only two physical input sites are essential, translating the neighborhood between ticks can place them on a single line even when their position vectors from the output cell are linearly independent.

This follow-up is fixed before evaluating the stronger construction. It does not erase the first protocol or its result.

## Stronger criterion

Call a 2D local rule **affinely two-dimensional** when the set of its essential physical input sites has affine dimension two. Equivalently, at least three essential sites are not collinear.

This excludes a rule that can be reduced to a one-dimensional dependency stencil by a fixed spatial change of basis together with a uniform moving frame.

For the active lift

$$
F_2^{\mathrm{active}}(X)(x,y)
=f\bigl(X(x-1,y),X(x,y),X(x,y+1)\bigr),
$$

all three displayed sites must therefore be essential. For ECAs this is exactly the set of rules in which left, center, and right are all essential.

## Strong universal gate

Keep the diagonal embedding

$$
E(s)(x,y)=s(x+y).
$$

Encoded states identify every pair of physical sites with the same coordinate sum. Starting from the horizontal base rule

$$
B_f(X)(x,y)=f\bigl(X(x-1,y),X(x,y),X(x+1,y)\bigr),
$$

define

$$
\begin{aligned}
F_2^{\mathrm{strong}}(X)(x,y)=B_f(X)(x,y)
&\oplus X(x+2,y)\oplus X(x+1,y+1)\\
&\oplus X(x-2,y)\oplus X(x-1,y-1).
\end{aligned}
$$

On every encoded state, the first added pair is equal because both sites have coordinate sum `x+y+2`, and the second added pair is equal because both have sum `x+y-2`. The four-bit parity therefore vanishes exactly, so the source dynamics should remain unchanged.

The four gate sites are individually essential for every source rule because each enters by XOR and none overlaps the base stencil. They occupy two distinct parallel anti-diagonals, so their union has affine dimension two. Therefore the full rule should be affinely two-dimensional for every one of the 256 ECAs, including constant rules.

This construction makes two-dimensional dependence essential on the full 2D configuration space but dormant on the encoded subshift. It still does not give the encoded family independent two-dimensional degrees of freedom.

## Checks

Extend the existing verifier to:

- compute affine dimension of essential sites;
- confirm that the active lift is affinely 2D exactly when all three source inputs are essential;
- exhaustively evaluate the seven distinct physical inputs of the strong gated rule for every ECA and verify that each of the four gate sites is essential;
- verify that the strong gated essential-site set has affine dimension two for all 256 rules;
- verify local intertwining for all source triples and both equal-pair gate values;
- verify global commutation for the same selected rules and torus widths used in the first audit.

No ECA class labels will be loaded.

## Interpretation boundary

If the checks pass, the exact claim is: every ECA has an invariant diagonal-stripe realization inside a 2D CA whose full local rule cannot be reduced to a one-dimensional dependency stencil, even after allowing a uniform moving frame.

The stronger unresolved question remains whether one can require the *encoded trajectories themselves* to exercise irreducibly two-dimensional degrees of freedom while still being conjugate or factor-related to the 1D source dynamics.
