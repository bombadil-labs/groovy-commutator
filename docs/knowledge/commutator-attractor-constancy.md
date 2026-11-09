# A commutator that varies globally can be constant where a finite ring settles

**Status: exact on finite periodic rings at the tested widths, 8 through 14
and 16, 18, 20.** No full-line claim.

Restrict the native commutator `G` to the eventual image of a ring map, the
states that lie on cycles. Beyond the 16 affine rules and the globally constant
nonlinear rules 4 and 200, 47 further elementary rules have a constant `G`
there at every tested width.

Three exact facts organise the result.

- On a fixed point `G(S) = H(0)`, so a fixed-point-only eventual image is
  constant for free. This accounts for most of the 47.
- On a state of period at most two, `G(S) = D(D(S))`.
- `G` commutes with the ring shift and the eventual image is shift-closed, so
  any constant value is shift-invariant: all-zeros or all-ones. The two-valued
  outcome is forced by symmetry.

Ten rules keep the property with period-two cycles present at every width from
8 to 14: 13, 19, 23, 33, 55, 69, 77, 79, 93 and 178. The set is closed under
reflection and not under complement conjugation, consistent with the
[complement-covariance criterion](commutator-complement-covariance.md).

A conjectured ceiling at period two is refuted. Rules 44 and 100 have `G ≡ 0`
on the eventual image and carry a period-three translating wave exactly when
the width is a multiple of three. Which eventual orbits admit a constant
commutator is open; along an orbit the condition is equivalent to the
difference recurrence `X_{t+1} = H(X_t) ⊕ c`, the first rung of the
[commutator jet](commutator-jet.md).

Scope: one-step cadence, native `G`, finite rings. What would change the
account: a full-line formulation on a stated subshift, or a classification of
the admissible orbits.

Source: [the finite-ring account](../research/2026-11-09-g-on-attractor.md).
