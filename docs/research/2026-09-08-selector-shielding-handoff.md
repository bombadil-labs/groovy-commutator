# Selector-shielding synthesis handoff

**Unnumbered handoff checkpoint, 2026-09-08.** This file records the latest state of the selector-shielding branch immediately before merge into `main`. It supersedes only the stale proof-status statements in `2026-09-08-selector-shielding.md`; the detailed derivations and protocols remain there.

## What is exact

For an isolated exact lower Rule-90 strip, the protected outer row reads the inner row exactly at those inner-row sites whose reference value is `1`. Therefore, while the lower half-plane agrees between coupled and isolated trajectories,

\[
\text{shielding survives one more tick}
\iff
C_t(2,x)\ge L_t(2,x)\quad\forall x.
\]

A first `1 -> 0` row-2 defect is necessarily visible at the protected outer row one fine tick later. This is the exact selector/dominance reduction.

For the concrete witness

\[
A=\{-5,0\},\qquad B=\{0,1,3,4,6\},
\]

the shielding is genuinely interaction-generated: either upper pulse alone breaks the lower boundary, while the pair cancels the causal leakage in the checked trajectory.

The fresh dyadic prediction at tick 256 passed exactly under the dense and independently written sparse kernels: exact row-0/1/2 coordinate templates, no negative row-2 defect, and no lower-half-plane difference. The saved check covers 514 complete fields and 2,257,852 changed-point comparisons.

## The moving walls are now proved, not merely observed

The earlier notebook described period-32 moving walls as an empirical/post-hoc regularity. That status has been strengthened.

In the left-moving coordinate `u=x+t`, the selector law is one-sided causal: a new `u` can depend only on old `u-2,u-1,u`. Hence every half-plane `u<=U` is a forward-closed subsystem. Dually, in `v=x-t`, a new `v` depends only on old `v,v+1,v+2`, so every `v>=V` half-plane is forward closed.

The committed half-plane verifier independently evolves the witness with both established kernels through ticks 64 and 96 and finds exact equality, in the corresponding co-moving frames, on the complete closed half-planes `u<=48` and `v>=0`. Determinism therefore gives an exact induction:

> The certified left and right moving half-plane states recur with period 32 for all later time.

This proves the two boundary-wall recurrences. It does **not** by itself prove all-time shielding, because the widening region between the two closed half-planes could in principle generate a new negative row-2 defect.

## The Rule-90 edge side of the argument is also exact

The observed wall-hole tables have period 8 in fine time. Conditional on those wall tables, the algebraic Rule-90 edge audit uses Lucas parity/Frobenius structure to prove that every coupled row-2 wall hole lies on a reference Rule-90 hole for every time in the corresponding residue class. The right wall matches the relevant reference edge holes exactly; the left wall is always a subset.

Thus the remaining all-time problem is not the certified walls. It is the widening middle.

## Exact bulk lemma: a stripe diode phase

The selector law has a simple exact two-phase invariant. If every column of one horizontal parity is uniformly `1` (with the opposite-parity columns arbitrary), then after one fine tick every column of the opposite parity is uniformly `1`; after the second tick the original parity is uniformly `1` again.

The reason is local: every destination whose two horizontal neighbors are `1,1` selects a source on the opposite-parity column, and that entire source column is `1` by hypothesis.

So

\[
\text{odd columns all 1}
\longleftrightarrow
\text{even columns all 1}
\]

is an exact period-2 causal-diode phase. The witness visibly nucleates large regions of this phase. What is **not yet proved** is that the expanding middle remains completely covered by this stripe phase (plus the already-certified walls) for all time.

## Bounded family evidence and an important failed prediction

A frozen targeted family census varied upper separation `k=1..8` and all 64 lower supports on logical sites `0..6`. Only **2 of 512** cases remained shielded through tick 64, both at `k=5`:

- `{0,1,3,4,5}`
- `{0,1,3,4,6}`

The census compares dense and independent sparse fields over 66,560 complete fields and 41,356,178 changed-point comparisons.

A separately frozen fresh-tail prediction then tested the idea that logical sites 7 and 8 would be irrelevant to the first shielding decision. That prediction **failed**, which is important. Among 192 fresh tail cases, the prefix decision tree had eight prediction failures, and the two observed shielded cases were not simply the two discovery prefixes crossed with arbitrary tails.

So shielding is not determined by a short static prefix of the lower logical state. Longer-range state can alter the causal outcome quickly. This strengthens the case for a dynamical/closure description rather than a simple local motif classifier.

## Current proof boundary

Established:

1. exact selector/dominance equivalence for the protected strip;
2. interaction-essential shielding witness through the independently checked prefix;
3. fresh exact dyadic continuation through tick 256;
4. exact all-time period-32 recurrence of the certified left and right moving half-planes;
5. exact Rule-90 edge membership of the wall holes, conditional on the wall tables;
6. exact period-2 stripe-diode phase as a law-level invariant;
7. narrow finite-family prevalence and fresh evidence that static short-prefix rules do not control shielding.

Not yet established:

1. `C_t(2)>=L_t(2)` for every fine time for the witness;
2. that no negative row-2 defect can ever be born in the widening middle;
3. that the witness middle is globally tiled by the stripe-diode phase between the two certified walls;
4. a general classification of shielding states.

## Connection to the parallel observation-closure work

The two research trains now meet naturally. Observation-closure/history-lift asks which hidden distinctions must be retained for autonomous effective dynamics. Selector shielding exhibits the spatial/causal dual: large physical differences can exist immediately adjacent to an organization while remaining dynamically invisible because the organization's selector never reads the harmful distinctions.

A useful synthesis question is therefore not merely whether information was discarded or whether a defect exists, but whether that distinction is **causally visible to the future effective state**. The failed short-prefix shielding prediction is especially consistent with the parallel finding that hidden relevance can depend on history rather than on a small instantaneous observer.

This checkpoint is deliberately unnumbered: Research025 is already occupied on `main` by the parallel train. The synthesis session should assign any next number only after deciding whether shielding remains a standalone result or becomes part of a unified causal-visibility / observation-closure program.
