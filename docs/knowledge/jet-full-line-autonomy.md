# Rule 54's complete G-anchored jet is an autonomous full-line CA factor

For any ECA H, define A0=I xor H and successive commutator residuals
Ak+1 = Ak∘H xor H∘Ak. Write Jm=(G,Q,R,...,Am)=(A1,...,Am).

The identity

\[
A_k(HX)=H(A_k(X))\oplus A_{k+1}(X)
\]

implies that Jm can update itself on the full binary line precisely when
equality of entire current Jm fields implies equality of A(m+1).

An exact bi-infinite equal-output de Bruijn source-pair graph checks every
compatible three-edge path on Rules 30, 54, 62, and 110, for m=1..5.

- Rule 30 first closes at J3=(G,Q,R); minimum symmetric induced jet radius 5.
- Rule 54 first closes at J5=(G,Q,R,A4,A5); minimum radius 6.
- Rule 62 also first closes at J5; minimum radius 6.
- Rule 110 does not close on the full binary line through J5. A phase-wall
  counterexample survives despite small finite rings that appear closed.

Rule 54 J5 has 4,316 bi-infinite equal-output source-pair contexts and 8,460
compatible pair edges. All 33,162 complete three-edge pair paths agree on A6,
while J4 has 12 counterexample paths. J5 therefore induces a unique continuous
shift-commuting map on its admissible image; exact context enumeration gives
its sharp radius-six local rule there.

This is **autonomy**, not injectivity or compression. Complete periodic
Rule-54 source rings at widths 8..18 show that J5 retains almost every source
state under the uniform source prior; at n18 it has 261,985 image states from
262,144 sources, and loses only 0.00122 bits.

The exceptional ambiguous source pairs include the Rule-54 period-four
half-period gauge, transient preimages, and separate periodic phase sectors.
These explain how the factor can forget source distinctions without ever
needing them for its own evolution.

This result is exact under the declared source/jet construction and needs
independent review. It does not identify a Wolfram class discriminator or
a compressed source model.

Source: [Full-line jet autonomy and radius audit](../research/2026-10-07-jet-full-line-autonomy.md).
