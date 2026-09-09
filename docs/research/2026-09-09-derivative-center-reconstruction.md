# Incoming derivative does not replace the missing center

The derivative-centered version of the original layered lift asks whether the present lower center state can be reconstructed from the present outer-neighbor count and the incoming derivative that produced the center.

On the complete 64-rule one-dimensional outer-totalistic family, the answer is almost maximally negative:

\[
\boxed{2/64}
\]

rules reconstruct exactly, and they are only the constant Rules 0 and 255.

The [protocol](protocols/derivative-center-reconstruction-20260909.md) was frozen before evaluation. The [verifier](../../scripts/verify_derivative_center_reconstruction.py) enumerates all 32 previous radius-two five-cell histories for every source rule and tests whether

\[
(n_t,\delta_t)\mapsto c_t
\]

is single-valued on reachable observations, with

\[
\delta_t=c_{t-1}\oplus c_t.
\]

Every nonconstant source has at least one observation pair compatible with both present center values. A post-hoc diagnostic retaining ordered present left/right bits rather than only their count still leaves exactly the same two constant rules.

This falsifies the simplest reading of the proposal: incoming derivative cannot generally be substituted for the current center variable in the old layered interpreter.

It does **not** make derivative irrelevant to dimensional lifting. The more natural interpretation is now that state and derivative are separate represented roles. The derivative-completed table identity

\[
[r\mid s\mid\delta]
\]

therefore remains the next operator candidate, but its three channels must close jointly rather than using derivative as a lossy replacement for state.
