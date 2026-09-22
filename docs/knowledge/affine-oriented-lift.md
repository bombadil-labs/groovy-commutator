# Every binary finite-memory CA has an exact self-synchronizing lift

For a binary CA `H` on Z^d with finite memory `M` and a chosen primitive
direction `e`, the affine-oriented six-field grammar
`(X⊕τ_{v+}X, 1⊕X⊕τ_{v−}X, X⊕HX, X⊕H²X, 0, X)` laid along a new period-six
axis is evolved exactly by a binary CA one dimension higher, on the marked beam
and all its phase translates, with the parent state and the phase locally
recoverable. Entry uses `v± = ±e` and inherited memory `M+{−e,0,e}` with
radius 3 on the new axis; later floors use `v± = a_n ± e` through the newest
axis and append only a radius-3 axis, so the same grammar closes on its own
image through every finite depth. For ECA roots the compact radii are
(3,2), (3,3,2), (3,3,3,2), ….

Status: proved in GPT-5.6 Sol's proof state, imported verbatim; Fable's
independent reimplementation verifies every finite instance the argument
reasons about (all 256 ECAs on all 512 dependency words, eight radius-two
parents on all 2^15 words, Conway's Life exhaustively on the 3×3 torus and on
random tori, the D3 diagonal-rail recursion for all 256 roots, and the
row-algebra witnesses showing that the dynamical checks are necessary). The
merge was not independently gated (review suspended by Myk, 2026-09-17).

Limits: the theorem concerns the marked beam only; off-beam completion is
free and no ambient property follows. The lift is not unique (a period-3
necklace code is a simpler valid lift; coset-induced CA give the trivial
layered version), it is binary only, and native single-track G of a completed
descendant remains completion-dependent. The two-beam product lift transports
the ancestral horizon commutators `K_t = D_H(H^t X) ⊕ H^t(D_H X)` (with
`K_1 = G`) completion-independently at every depth.

Application status, 2026-09-22: the [repository consumer
audit](../research/2026-09-22-phase-free-consumer-audit.md) found no current
downstream operation requiring this phase-free layout. Existing physical-key
scripts construct or study the lift itself. The marked Groovy readout is
matched by a smaller named cache. Leave application work dormant until an
independent caller supplies an exact geometry and cost contract.

Source: [the affine-oriented lift theorem](../research/2026-09-17-affine-oriented-lift-theorem.md).
