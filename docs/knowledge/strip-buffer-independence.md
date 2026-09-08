# One background row keeps aligned strips independent

Under the fixed ternary 2D law, any collection of the two-row Rule-90 strips
with at least one alternating background row between neighbors evolves as
independent Rule-90 rows at cadence two. The separator alternates between
01 and 10, reading fixed cells at each phase, so it does not transmit the
strips' data into one another.

The all-gap and arbitrary-strip-count statement follows from a local
two-phase buffer argument. Exact enumeration checks all six-bit input
combinations for gaps one through four. Independent finite-field checks and
all declared matched action words corroborate the dynamical and action
identities. A logical flip costs two physical cells within its own strip.

One row is the minimum gap guaranteeing this for arbitrary data under the
fixed alignment: adjacent strips fail the code test on 47 of 64 local inputs.
This is a scoped composition result, not a claim that one row isolates every
possible encoding or physical perturbation. See the
[proof and experiment](../research/2026-09-08-coupled-strips.md).
