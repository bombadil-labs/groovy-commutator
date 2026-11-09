# The commutator restricted to where a finite ring settles

**Status:** exact algebra plus exhaustive finite-ring computation. Written
2026-07-21 on a local branch that was never pushed; ported to `main` on
2026-11-09 during repository housekeeping. **Reviewed by: none.** The port's
author (Claude, `claude-fable-5-2`) re-derived the headline counts with separate
integer-coded code; that is self-verification, not review.

## Contract

- **Rules:** all 256 elementary cellular automata, one rule at a time.
- **State family and boundary:** every binary state of a periodic ring. Widths
  8 through 14 with a full cycle decomposition; widths 16 and 18 for all rules
  and width 20 for the rules still constant at 18, using a vectorised
  period-at-most-two test. A separate commensurability scan covers widths 6
  through 20.
- **Observation:** the native commutator `G = D∘H ⊕ H∘D`, with `D = 𝟙 ⊕ H`.
- **Domain of the claim:** the *eventual image* of the one-step ring map, that
  is, the states lying on cycles. It is computed by iterating the image of the
  whole state space until it stops shrinking, with no round cap.
- **Cadence and horizon:** one step; no trajectory statistics.

Nothing here is a full-line statement. A finite ring's eventual image is not
the nonwandering set of the infinite line, and
[small-ring agreement does not transfer automatically](representation-case-studies.md).

## Question

Globally, `G` is constant across all states when the rule is
[affine](../knowledge/affine-implication.md), and
[only two nonlinear rules, 4 and 200, share that property](../knowledge/affine-converse.md).
Which other rules have a constant commutator once the state is restricted to
the eventual image?

## Exact algebra

These four statements hold for every rule and every ring width.

1. **Fixed points.** If `H(S) = S` then `D(S) = 0` and `G(S) = H(0)`. A rule
   whose eventual image consists only of fixed points therefore has a constant
   commutator there for free, with the value set by one bit of the rule number.
2. **Period at most two.** If `H²(S) = S` then `D(H(S)) = D(S)`, so
   `G(S) = D(S) ⊕ H(D(S)) = D(D(S))`. On such states the commutator is the
   second difference.
3. **Shift invariance of the constant.** `G` commutes with the ring shift, and
   the eventual image is closed under the shift. If `G` equals a constant `c`
   on it, then `c` equals its own shift, and the only shift-invariant ring
   states are all-zeros and all-ones. The two-valued outcome is forced by
   symmetry; the dynamics do not select it.
4. **Difference recurrence.** Along any orbit, with `X_t = S_t ⊕ S_{t+1}`,
   `G ≡ c` on the orbit if and only if `X_{t+1} = H(X_t) ⊕ c`. This is the
   `k = 0` rung of the [commutator-jet recurrence](../knowledge/commutator-jet.md),
   `D(HX) = H(DX) ⊕ G(X)`, found here before the jet was defined.

The runner asserts items 1, 3 and 4 on every run, over all 256 rules.

## Exhaustive finite-ring results

- **Constant on the eventual image at every tested width.** Beyond the 16
  affine rules, 49 rules have a constant commutator on the eventual image at
  every tested width (8 through 14, then 16, 18 and 20). Two of them are the globally constant rules 4 and
  200; the other 47 are not constant on the full state space. The constant is
  all-zeros or all-ones in every case, as item 3 requires, and its kind is the
  same at every width from 8 to 14 for all 49.
- **Most of that is the fixed-point lemma.** Only ten of the 49 carry
  period-two cycles at every width from 8 to 14:
  `{13, 19, 23, 33, 55, 69, 77, 79, 93, 178}`. Rules 19, 23, 33, 55 and 178
  have eventual images that are almost entirely period-two states. Nine of the
  ten settle on all-ones; Rule 178 settles on all-zeros.
- **Mirror-closed, not complement-closed.** The set of ten is closed under
  reflection (13↔69, 79↔93, the rest self-mirrored). It is not closed under
  complement conjugation: Rule 33 is in it and its conjugate 123 is not, though
  the two have the same eventual-image geometry (326 states, all of period
  two, at width 12), and 123 takes 130 distinct commutator values there. The
  [complement-covariance entry](../knowledge/commutator-complement-covariance.md)
  already explains why: the native commutator is complement-covariant only for
  self-dual rules.

## A conjecture made and falsified in the same unit

**Conjecture.** Outside the globally constant rules, a constant commutator on
the eventual image tolerates cycles of period at most two and nothing longer.

It held at widths 8 through 14 under the filter then in use. It is false.
Rules **44 and 100** are nonlinear, are not 4 or 200, have `G ≡ 0` on the
eventual image, and carry a period-three cycle exactly when the width is a
multiple of three. At width 12 the cycle is the rigidly translating wave
`110110110110 → 101101101101 → 011011011011`. The scan over widths 6 through
20 finds hits at 6, 9, 12, 15 and 18, with no other rule and no other period.

Two lessons are worth keeping.

- The "true at every width" filter that was meant as a caution hid the
  counterexample. It discarded 44 and 100 because their eventual images are
  fixed-point-only at widths not divisible by three.
- The natural repair, "constant if and only if every eventual orbit is a rigid
  translation", is also false in both directions at widths 10 and 12. The ten
  rules above are constant on orbits that do not translate, and about sixty
  rules per width have all-translating eventual images without a constant
  commutator.

**Open.** Which eventual orbits admit a constant commutator? Item 4 restates
the question exactly and does not answer it.

## Limits

- Finite periodic rings only, widths 6 through 20.
- No Class-IV inference. The ten rules are simple, mostly majority-like rules.
- The July write-up called this "emergent affinity" and counted the result as
  established. That wording predates the current evidence contract; the
  statements above are the ones the evidence supports.
- The parquet files were regenerated on 2026-11-09 by rerunning the script on
  `main`. They carry no recorded source hashes, so the result is not registered
  in `scripts/check_result_integrity.py`.

## Reproduce

```
python scripts/experiment_g_on_attractor.py
```

The run takes several minutes at width 20 and belongs outside automatic CI.
It writes `results/g_on_attractor.parquet`, `results/g_on_attractor_bign.parquet`
and `site/src/data/g_on_attractor.json`.

## Provenance

The unit was prompted by an outside essay proposing that an observable be read
at the attractor of a flow instead of averaged along it. An unsent draft reply
to that essay's author is preserved as
[a historical draft](archive/2026-07-21-lattice-riff-draft.md); it is not a
project position and makes claims about that essay that this repository has
not checked.
