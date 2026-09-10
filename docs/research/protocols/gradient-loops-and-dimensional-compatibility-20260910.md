# Frozen next experiment: gradient loops and dimensional compatibility

Date: 2026-09-10. Status: planned, not executed. This follows full-gradient closure for 0,142,150,170,178,204,212,232,240,255. Keep those ten source words, the original ordered axial laws, and all nearest-neighbor gradient components. No class or visual-behavior filtering is allowed.

## Domain and proposed invariants

For each dimension d, the native state has d binary edge components per site. Require XOR around every elementary square to vanish. On the infinite lattice this is the gradient condition. On a periodic lattice, also record h_i: XOR along one full wrapping loop in direction i. Local flatness makes this loop parity independent of the transverse base point. Zero loop vector is required for a periodic binary source potential; nonzero loop vectors allow a potential that changes by h_i when it crosses one period in direction i.

Represent a flat periodic edge field by a binary potential on one fundamental tile, anchored to zero at the origin, plus the d-bit loop vector. Across a seam the edge difference includes the corresponding loop bit. Check that this parameterization is one-to-one and complete for the tested shapes; validate local flatness, loop base-point independence, and source ambiguity by global complement. Boundary topology is an explicit choice, not an intrinsic dimension or prime-factor classification.

The frozen prediction is that the eight nonconstant self-dual sources preserve the loop vector, while the two constant sources erase it. Derive the general statement from translation covariance and complement symmetry. Test it without using that prediction to assign the native edge updates.

## Native gradient evolution and independent audit

Implement Q_(r,d) directly from current gradient components: read all outgoing edges at the Moore radius-one sites, integrate their connected local edge graph with a declared temporary anchor, evaluate the d+1 source windows needed for the next gradient, and discard the anchor. The two possible anchors must give identical outputs. Keep local consistency checks explicit; do not invent update values on curl-violating neighborhoods.

Independently evolve a twisted source potential with the unchanged axial passes and then take its gradient. Handle wrapping signs directly. For constant sources derive the resulting zero loop vector separately; do not retain an invalid old twist after a constant pass. Compare all native output components with this source-based reference and check every plaquette and wrapping loop after each update.

## Frozen finite budgets

Use shapes (4) in 1D,(2,2) in 2D, and(2,2,2) in 3D. Enumerate every anchored potential and every loop vector, giving16,32,1,024 distinct flat edge fields respectively if the parameterization proof is correct. For each of the ten source words run four macro updates from every initial field. Count repeated timepoints as checks without calling them independent initial states. The base budget is10,720 initial rule/field cases and 42,880 macro updates.

Also check the literal gradient embedding P: replicate all old components along a new axis of period2 and append an identically zero new component. Test1D shape (4) to2D shape (4,2), and 2D shape (2,2) to3D shape (2,2,2), for all source ensemble states, all ten rules, and the same four ticks. Compare independently computed target updates with embedded source updates, and verify that P appends a zero loop bit while preserving the inherited ones. These tests support the all-dimension intertwining proof; they do not replace it.

## Decision and publication

Commit implementation before evaluation. Preserve exact source lists, every loop-sector transition, discrepancies, deterministic certificates, and independent checksums in canonical JSON with CI reproduction. Account for d edge bits per site, the local integration support, ordered passes, and the global boundary data. Distinguish arbitrary periodic gradient components, locally flat fields, and gradients of periodic potentials.

This asks whether a specific kind of loop information survives time evolution and dimensional lifting in the declared family. It does not test self-assembly, mutable programs, arbitrary ambient completions, or a preferred truth-table layout. Preserve any failure and freeze changes of topology, observation, cadence, or law separately before evaluating them.
