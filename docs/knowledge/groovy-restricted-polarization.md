# Centered Groovy is polarization on the trajectory graph

For Boolean dynamics `H` write the centered polarization
`B_H(X,U) = H(X⊕U) ⊕ H(X) ⊕ H(U) ⊕ H(0)` and the finite-difference tangent
action `∂H_X(U) = H(X) ⊕ H(X⊕U)`. Then the centered commutator satisfies
`G°_H(X) = ∂H_X(D_HX) ⊕ ∂H_0(D_HX) = B_H(X, D_HX)`: polarization evaluated
only on the trajectory-displacement graph `{(X, D_HX)}`. `B_H ≡ 0` on all
pairs exactly when `H` is affine (16 elementary rules), while `G° ≡ 0`
requires vanishing only on the graph, which the nonlinear rules 4 and 200 also
satisfy. Exact on the seven-cell ring for all 256 rules.

Consequences recorded with it: the uncentered `G = ∂H_X(D_HX) ⊕ H(D_HX)` is
the defect between transporting the displacement as a tangent vector and
evolving it as a point; the affine six-field jet's secant-versus-point
residual is `(0,0,K_1,K_2,0,0)` with `K_1 = G` and `K_2 = [D_H, H²]`; the
horizon commutators obey `K_{t+1} = G(H^t X) ⊕ ∂H_{H^t D_HX}(K_t)`, which
unrolls to a linear Duhamel sum exactly in the affine case.

Source: [the affine-oriented lift theorem](../research/2026-09-17-affine-oriented-lift-theorem.md); the rules 4/200 fact is established result 1.
