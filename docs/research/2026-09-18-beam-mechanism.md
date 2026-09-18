# The invariant beam: why history gain anticorrelates between rules

The previous unit found that history gain **anticorrelates** between distant
base rules rather than merely failing to transfer: a completion that buys rule
110 memory costs rule 30 memory. It was recorded as the Program's best open
question. This unit answers it, and the answer is a theorem plus a mediation
that the theorem predicts.

Evidence: **exact** for the beam theorem, which is proved and independently
verified; **exploratory** for the mediation census (one contract, one density,
sixteen bases, height two with a height-three arm). Protocol frozen before
implementation (`protocols/2026-09-18-beam-mechanism.md`); runner and evaluator
committed before the run; evaluation preceded review under Myk's 2026-09-17
suspension of the cross-model gates. Drafted by Claude/Fable 5.1; reviewed,
amended, implemented and run by Claude Opus 5. Fifth unit of the
[Class-IV Refinement Program](2026-09-17-class-iv-refinement-program.md).

Every prediction was calibrated on the drafting agent's pilot and is declared
so; the canonical completions come from a disjoint namespace and eight of the
sixteen bases are fresh, so this is a **pre-registered out-of-sample
replication**, not a set of blind bets.

## The theorem

On a height-two strip the vertical wrap sends both off-rows onto the other
row. A state whose two rows are equal therefore has Moore count `3L + 2C + 3R`
and west neighbour `L`, so `n₇ = 2L + 2C + 3R` and the condition index is

    16C + 8L + (2L + 2C + 3R)

which is **exactly the height-one exposed index** for the window `(L, C, R)`.

Those are the eight entries the base rule fixes and no completion can reach.
So every cell of an equal-row state reads an entry the refinement does not
own: the strip acts as the base elementary rule, and equal rows stay equal.

> **The equal-row set is exactly invariant under every rule of the handed
> family, and on it the strip is the base rule.**

In the standard language, it is a closed, shift-invariant, `F`-invariant
subsystem of the strip, isomorphic to the one-dimensional configuration space,
on which the global map is conjugate to the base elementary automaton. It is
called the *beam* here. The executing session re-derived it from scratch rather
than accepting the drafting agent's report, and the run asserts it again as a
control: sixteen bases, eight completions each, equal rows preserved and the
top row equal to the base rule's orbit for 256 steps, at heights two and three.

**This stands independently of everything below.** It is proved, not measured.

## Why that makes history gain anticorrelate

The theorem turns history gain into a **mixture**. On the beam it is the base's
own one-dimensional value, because the strip *is* the base rule there. Off the
beam it is something the completion sets. Whether a random start ends up near
the beam is a property of the completion, roughly independent of the base.

So beam proximity is a **shared mediator**, and each base responds to it with
the sign of its own one-dimensional gain minus the off-beam value. Two bases on
opposite sides of that threshold respond with opposite signs to the same
completion. A shared mediator with opposite-signed responses is an
anticorrelation.

## Result

| base | 1D `M` | response `ρ` | on-beam median | off-beam median |
| ---: | ---: | ---: | ---: | ---: |
| 5 | 0.976 | +0.730 | 0.968 | 0.114 |
| 29 | 0.954 | +0.745 | 0.886 | 0.075 |
| 110 | 0.903 | +0.759 | 0.793 | 0.047 |
| 62 | 0.765 | +0.714 | 0.754 | 0.117 |
| 54 | 0.601 | +0.624 | 0.576 | 0.138 |
| 33 | 0.563 | +0.606 | 0.556 | 0.069 |
| 46 | 0.374 | +0.299 | 0.417 | 0.080 |
| 18 | 0.164 | +0.280 | 0.150 | 0.121 |
| 22 | 0.137 | +0.579 | 0.132 | 0.113 |
| 30 | 0.000 | −0.737 | −0.003 | 0.029 |
| 90 | 0.000 | −0.679 | −0.003 | 0.040 |
| 106 | 0.000 | −0.657 | −0.004 | 0.071 |
| 232 | 0.000 | −0.412 | 0.000 | 0.170 |
| 0, 204, 8 | 0.000 | −0.13, −0.13, −0.11 | 0.000 | 0.080, 0.130, 0.126 |

The on-beam column **is** the one-dimensional column, to within a few
hundredths. The off-beam column is a narrow band from 0.029 to 0.170 with no
relation to the base. That is the mixture, measured.

- **P1 held on all four arms.** The anticorrelation replicates at −0.341 on
  fresh completions, bootstrap `[−0.444, −0.227]`. Conditioning on the mediator
  does not merely remove it but reverses it: **+0.204** given the two beam
  proximities, **+0.163** given transverse stability, and −0.055 given the
  leave-two-out score. The last was flagged at freeze as the protocol's
  least-calibrated threshold, and held anyway. Across the 55 pairs where both
  responses are strong, the sign of the transfer equals the product of the two
  response signs in **53**.
- **P2 held without exception.** Beam proximity transfers at 0.349 or better
  on **every one of the 120 pairs**, so the strict all-pairs form held and the
  relaxed companion added at freeze was not needed. Transverse stability
  transfers at 0.501 or better among non-frozen bases. It also gates: the
  probability of sitting on the beam given low transverse stability is at most
  0.034 in every base.
- **P3 held strongly, on bases that could not have been fitted.** The ordering
  of response against one-dimensional history gain is **0.960** over sixteen
  bases, bootstrap `[0.919, 0.972]`, with all six high-gain bases above +0.606
  and all three chaotic bases below −0.657. Eight of the sixteen were never
  used to find the mechanism.
- **P5 and P6 held.** The on-beam identity is the table above. Retention is
  untouched by the mediator, 0.623 raw against 0.634 partial, so the beam is
  specific to history gain and not a general nuisance factor.

## The two that did not go as designed

**P4 held, and it was the one expected to fail.** It asserted that the mid-band
bases 22, 18 and 46 all respond positively, which the naive "sign of 1D gain"
rule predicts and the mixture reading was supposed to contradict for rule 18.
All three responded positively. The reason is a measurement correction: the
previous unit put the off-beam value near 0.2 bits, and measured properly here
it is 0.03 to 0.17. That is low enough that 18 and 22 still have on-beam
medians above their own off-beam medians, so they still respond positively. The
mixture reading is right, its companion P4′ held on all ten testable bases, and
the naive rule agreed with it only because **no base on this panel falls in the
discriminating window**. The unit therefore did not perform the comparison P4
existed to perform. Discriminating would need a base with one-dimensional gain
strictly between zero and its own off-beam median, a window this panel missed.

**P7 failed on its first arm, and the demoted descriptive arm says why.** The
anticorrelation does not survive to height three: the transfer there is +0.074,
not negative. On-beam fractions at height three are far higher than at height
two in every base, 0.771 against 0.458 for rule 110 and 0.854 against 0.542 for
rule 30. Almost everything sits on the beam, so the mixture degenerates, and
with no off-beam population there is nothing for opposite-signed responses to
act on. This is a post hoc reading of a number the protocol demoted from
prediction to description, and it is consistent with the mechanism rather than
independent support for it. The height-three proximity transfer, P7's second
arm, held at 0.599.

## What this does and does not show

It explains the anticorrelation, which is the first question in this Program
whose answer is a mechanism rather than a distribution. The chain is: an exact
invariant set on which the refinement is powerless, a mixture whose weight the
completion controls, and a response whose sign the base's own one-dimensional
memory fixes.

It does not show that the beam is why anything is Class IV. It says nothing
about why some completions attract trajectories onto the beam and others do
not, which is now the open question and is a question about the structure of a
completion rather than about any base. The mediation is measured under one
contract at one density, and the sixteen bases are a panel, not a census.

## Deviations

The first canonical run was discarded. Its matched null-pair control failed at
a maximum difference of 7.9, localized to the three transverse quantities while
the four trajectory quantities matched to exactly zero. The cause was a
copy-paste error in the control's own conjugate beam-state construction: rule
137 being the complement conjugate of 110, the conjugate beam state is
`F₁₃₇²⁵⁶(¬x)`, and the code complemented after the burn rather than before,
producing a different state. A second fault compounded it: the implementation
ran that control *after* the tiers, so a broken control could gate nothing,
contrary to the protocol. Both were fixed, the fix verified in isolation before
re-running, and the unit re-run in full rather than patched, so that the
committed runner is the runner that produced the data. The discarded run's
orphaned summary was deleted rather than committed.

## Files

`experiments/beam_mechanism_20260918/run.py`, `evaluate.py`;
`results/beam_mechanism_20260918/` (`rows.json`, `controls.json`,
`summary.json` with source hashes).
