# Centered Groovy is polarization on the trajectory graph

For Boolean dynamics \(H\), write

\[
d_H(X)=X\oplus H(X)
\]

and the based finite-difference transport

\[
\partial H_X(U)=H(X\oplus U)\oplus H(X).
\]

The centered polarization is

\[
B_H(X,U)
=
H(X\oplus U)\oplus H(X)\oplus H(U)\oplus H(0)
=
\partial H_X(U)\oplus\partial H_0(U).
\]

The centered commutator therefore satisfies

\[
\boxed{
G_H^\circ(X)
=
\partial H_X(d_HX)\oplus\partial H_0(d_HX)
=
B_H(X,d_HX).
}
\]

So centered Groovy is polarization restricted to the
trajectory-displacement graph \(\{(X,d_HX)\}\).

The 2026-10-06 typed-difference unit supplies the geometric reason. Correct
transport sends the rule's own displacement according to

\[
\partial H_X(d_HX)=d_H(HX),
\]

whereas Groovy flattens that based change and evolves its bits as an ordinary
point. Thus \(G^\circ\) is precisely the basepoint dependence of change
transport sampled on the rule's own displacement.

All-pairs \(B_H\) vanishes exactly when \(H\) is affine. The graph restriction
is weaker. For ECAs an exact radius-two ANF classification now proves

\[
G_H^\circ\equiv0
\quad\Longleftrightarrow\quad
H\text{ is affine or }H\in\{4,200\}.
\]

The same unit also identifies the affine-oriented lift's temporal residual as
the temporal part of the second cross-effect of the centered lift encoding:
\((0,0,K_1\oplus H(0),K_2\oplus H^2(0),0,0)\).

Sources:
[affine-oriented lift theorem](../research/2026-09-17-affine-oriented-lift-theorem.md);
[typed difference geometry](../research/2026-10-06-typed-difference-geometry.md).
