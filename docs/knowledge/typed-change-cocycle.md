# Finite-difference transport is a nonlinear cocycle

For Boolean dynamics \(H\), define the based finite difference

\[
\partial H_X(U)=H(X\oplus U)\oplus H(X)
\]

and its \(n\)-step transport

\[
\Phi_n(X,U)=H^n(X\oplus U)\oplus H^n(X).
\]

Then

\[
\Phi_{n+m}(X,U)
=
\Phi_m(H^nX,\Phi_n(X,U)).
\]

Thus \(\Phi\) is an exact discrete-time nonlinear cocycle over \(H\). Under the
coordinate change

\[
\Psi(X,U)=(X,X\oplus U),
\]

the skew product \((X,U)\mapsto(HX,\partial H_X(U))\) is conjugate to the pair
system \(H\times H\). The cocycle is therefore ordinary pair evolution written
as basepoint plus displacement.

The rule's own dynamical displacement \(d_H(X)=X\oplus H(X)\) is an invariant
section:

\[
\partial H_X(d_HX)=d_H(HX).
\]

Raw Groovy compares this correctly typed transport with evolving the same bit
pattern as an ordinary point. Centered Groovy compares typed transport at the
real basepoint with transport at the origin.

For affine rules the fibre action is basepoint-independent and linear. The
2026-10-06 ECA audit finds basepoint-independent local transport for exactly
the 16 affine elementary rules; all 240 nonlinear ECAs have a local witness of
basepoint dependence.

Source: [typed difference geometry](../research/2026-10-06-typed-difference-geometry.md).
