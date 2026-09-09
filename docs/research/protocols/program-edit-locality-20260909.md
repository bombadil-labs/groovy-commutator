# Frozen audit: spatial edit costs and dimensional information budgets

Date: 2026-09-09. This protocol is frozen before running the new audit. The mathematical deductions below precede enumeration and were prompted by integrating the previously stale dimensional-intertwining PR #35.

## Questions

1. Can a finite spatial program edit switch the rule applied everywhere on an infinite source lattice in bounded time under one fixed local interpreter and a fixed local decoder?
2. How do the recovered stripe encoding and the two-rail interface differ in their physical edit support?
3. Can a deterministic encoding with an O(n)-site source footprint supply O(n^2) independent binary information in an n-by-n target patch?

## Deductions to check, with assumptions

A radius-R target CA maps a finite disagreement set A into its radius-Rt neighborhood after t ticks. A fixed decoder with radius rho and a proper set of output anchors can therefore change only finitely many decoded sites after any finite time. “Proper” means a bounded target region contains only finitely many output anchors.

Distinct ECA rules have a periodic source witness on which their next states differ infinitely often. In particular, flipping table bit q changes the output at every center of the repeated triple encoding q. Consequently finitely different physical program encodings cannot implement a global ECA instruction replacement with fixed finite cadence and a fixed local decoder. This is not a prohibition on finite-region program edits, distributed edits, growing computation regions, or finite worlds with size-dependent latency.

For the stripe encoding E(S)(x,y)=S(x+y), a source bit edit changes an entire diagonal: n target sites on the n-by-n torus. For the two-rail interface, the corresponding state edit changes one interface cell. Neither construction places the source instructions in mutable target cells.

The stripe image has exactly 2^(2n-1) distinct n-by-n patches; an interface-crossing two-rail patch has exactly 2^n. More generally, if an output patch depends on at most Cn source sites, it has at most |alphabet|^(Cn) possible values. This rules out positive information per target area under that footprint assumption. It does not rule out rich dynamics, computation, or other meanings of dimensional organization.

## Fixed computational audit

- All 256 ECAs, each of eight one-bit instruction changes, and source rings of widths 9, 15, 21. Repeat the address triple with its center at sites congruent to zero modulo three. Require disagreement at every such site after one tick.
- On width nine, apply that instruction change only to the program at site zero in a nonuniform program field. Require exactly one changed next-state cell. This audits the distinction between global and per-site program edits, not a new nonuniform-CA construction.
- For every torus width 2 through 16 and each source bit location, compare stripe encodings before/after a one-bit edit and count its support.
- Enumerate all stripe patches of side n=1 through 7 from the 2n-1 relevant source bits; separately enumerate all interface patches of those side lengths from n source bits. Check exact distinct-pattern counts.
- Audit finite propagation on both the active and strong 2D laws from the recovered verifier: rules 0,30,54,90,110,150,204,255; four deterministic fields; side 21; a single central physical edit; four ticks. Compare every site outside the corresponding periodic Chebyshev cone at each tick. Radius bounds are one and two respectively; the largest cone has radius eight, below half the torus width.
- Use a dependency-free Python script, deterministic field generation, and canonical sorted JSON. Save the output and compare it byte-for-byte in CI.

## Reporting discipline

Retain the previous suggestion about finite program edits as a historical proposal, and explicitly correct its globally uniform interpretation in the current Program. State the theorem's decoder, anchoring, support, and timing assumptions. Treat finite experiments as implementation audits of the proofs. Do not claim that the original recursive spatial-program conjecture is impossible, that a preferred dimension exists, or that spatial entropy classifies interesting dynamics.
