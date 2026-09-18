# The equal-row set of a height-two strip is exactly invariant, and the strip is the base rule on it

Take the handed family of two-dimensional rules `f(c, w, n₇)` and run it on a
cylinder two cells tall. The vertical wrap sends both off-rows onto the other
row, so a state whose two rows are equal has Moore count `3L + 2C + 3R` and
west neighbour `L`. Its condition index is therefore

    16C + 8L + (2L + 2C + 3R)

which is exactly the height-one exposed index for the window `(L, C, R)`.

Those eight entries are the ones the base elementary rule fixes under the
restriction map, and no completion can reach them. So every cell of an
equal-row state reads an entry the refinement does not own: the strip acts as
the base rule, and equal rows stay equal.

**The equal-row set — the *beam* — is exactly invariant under every rule of the
family, and the global map restricted to it is conjugate to the base elementary
automaton.** It is a closed, shift-invariant, `F`-invariant subsystem
isomorphic to the one-dimensional configuration space.

Status: exact within stated bounds. Proved by the index algebra above and verified exactly for
sixteen bases across eight completions each over 256 steps, at heights two and
three, as a gating control of the
[beam-mechanism unit](../research/2026-09-18-beam-mechanism.md).

## Why it matters dynamically

The theorem makes history gain a **mixture**: the base's own one-dimensional
value on the beam, a completion-set value off it. Which one dominates is set by
whether a trajectory settles near the beam, and that is a property of the
completion rather than the base.

Beam proximity is therefore a shared mediator. Each base responds to it with
the sign of its own one-dimensional gain minus the off-beam value, so two bases
on opposite sides of that threshold respond oppositely to the same completion.
That is why history gain anticorrelates between distant rules instead of merely
failing to transfer.

Measured on sixteen bases and 256 completions: on-beam median history gain
equals the base's one-dimensional value to within a few hundredths, off-beam
medians lie in a base-indifferent band from 0.029 to 0.170, the response
ordering against one-dimensional gain is 0.960, and conditioning the
110-against-30 transfer on beam proximity moves it from −0.341 to +0.204.

## Bounds

The theorem is exact and dimension-specific: it is a statement about height two
(and, as verified, height three) on this family's cylinder, not about the
plane. It does not explain *which* completions attract trajectories onto the
beam, which is the open question it leaves. At height three nearly every
trajectory sits on the beam, the mixture degenerates, and the anticorrelation
it explains disappears.
