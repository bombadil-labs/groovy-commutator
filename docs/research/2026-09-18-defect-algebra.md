# The defect algebra: twelve exclusive-ors decide what a refinement does to the beam

The beam unit proved that the equal-row set of a height-two strip is exactly
invariant and that the strip is the base rule on it, then left one question:
**what makes a refinement attract trajectories onto that set?** This unit
answers it, and the answer is first a theorem and only second a measurement.

Evidence: **exact** for the defect algebra and the edge lemma, which are
proved and independently re-derived; **exploratory** for the census
(one contract, one density, eight bases, 408 completions). Protocol frozen
before implementation (`protocols/2026-09-18-defect-algebra.md`); runner and
evaluator committed before the run; evaluation preceded review under Myk's
2026-09-17 suspension of the cross-model gates. Drafted by Claude/Fable 5.1;
reviewed, amended, implemented and run by Claude Opus 5. Sixth unit of the
[Class-IV Refinement Program](2026-09-17-class-iv-refinement-program.md).

Every prediction is calibrated on earlier canonical rows or the drafting
agent's pilot and declared so; the completions are fresh and disjoint and
eight of them are *built* rather than sampled, so this is a **pre-registered
out-of-sample replication**, not a set of blind bets.

## The algebra

Flip one cell of a beam state. Exactly six reads change: rows zero and one at
the flipped column and its two neighbours. **None of the post-flip reads
lands on an exposed entry** — the arithmetic cannot turn the beam's `3R` term
into an exposed index — so the damage is carried entirely by table positions
the base rule does not own.

Whether that defect heals in one step is a conjunction of three pairwise
bit-equalities between free entries, and the pair involved in each depends on
the surrounding five-cell window only through a two-cell window of its own:

| block | window it reads | what it governs | index gap of its pairs |
| --- | --- | --- | ---: |
| `A` | the two cells left | leftward growth | 1 |
| `B` | the cells either side | isolated survival | 14 |
| `C` | the two cells right | rightward growth | 6 |

Twelve equalities in all, of GF(2) rank **eleven**. Refinements therefore fall
into 2,048 signature classes of 8,192 each, and a thirteen-dimensional
subspace satisfies all twelve and heals every possible single defect at once.
Expected one-step healing under a uniform refinement is exactly `1/8`.

**Edge lemma.** For any defect cluster, the column west of its leftmost defect
reads exactly the `A` pair, the column east of its rightmost reads the `C`
pair, and an isolated defect reads `B` at its own column — regardless of the
cluster's interior. So the three blocks govern growth and survival at *every*
step, not only the first. Corollaries: if `A` or `C` never holds the defect
never dies; if both always hold it is confined to its column forever; if all
twelve hold it dies immediately.

Re-derived from the read-index definition by the executing session rather
than taken on report, and confirmed as a gating control: six perturbed reads
with zero on exposed entries, the fourteen lit and ten dark entries, the
factorization for all three blocks, rank eleven, cell sizes exactly 8,192,
and a simulated step matching the violated-constraint count on 256 random
pairs with zero mismatches.

**This stands however the predictions below scored.**

## It resolves an older puzzle

Two units ago, history gain resisted every linear model on the refinement's
twenty-four bits, with negative cross-validated fit in every base. Here, with
the same data shape:

| regressed on | cross-validated `R²` of transverse stability |
| --- | --- |
| the 24 raw bits | **negative in every base**, −0.145 to −0.271 |
| the 12 healing exclusive-ors | **+0.369 to +0.433** in every base |

The refinement's effect was never absent. It was written in a basis no linear
model on the raw bits can read. **P1 held** in every base on both targets.

**P2 held**: the beam-measure-weighted healing rate predicts transverse
stability at Spearman 0.685 to 0.865.

## The open question, answered with one exception

| base | universal healers: median proximity | on the beam | growers: on the beam |
| ---: | ---: | ---: | ---: |
| 110 | 1.000 | 0.958 | 0.000 |
| 22 | 1.000 | 0.958 | 0.000 |
| 30 | 1.000 | 0.958 | 0.000 |
| 0 | 1.000 | 0.958 | 0.000 |
| 54 | 1.000 | 0.917 | 0.000 |
| 5 | 1.000 | 0.917 | 0.000 |
| 90 | 1.000 | 0.833 | 0.000 |
| **204** | **0.940** | **0.000** | 0.000 |

**P3(a) failed, on exactly one base of eight.** In seven, refinements built to
satisfy all twelve equalities sit on the beam in 83 to 96 percent of trials
against a threshold of 50, with median proximity exactly 1.000. Under the
identity rule they never do. So healing isolated defects is very nearly
sufficient for beam residence, and there is one base where it buys nothing.
The prediction is scored as failed because it was stated for every base, and
the drafting agent flagged it at odds 0.45 as the one genuinely at risk.

**P3(b) failed on a clause that is not about the theorem.** The growers never
sit on the beam — zero in every base, exactly as the edge lemma requires and
as bet. But in three bases their *median proximity* exceeds the random arm's
instead of falling below it. A refinement that provably cannot heal an
isolated defect can still sit closer to the beam on average than a typical
one. Residence from a dense random start is therefore not the same quantity
as isolated-defect healing, which is the distinction the next two results
sharpen.

**P3(c) held**: confined refinements have higher mean transverse stability
than the random arm in every base.

## Two more, one of them against expectation

**P4 held on both arms, and (b) was expected to fail.** Flipping three dark
entries — the ten an isolated defect cannot reach on its first step — leaves
transverse stability nearly unchanged in every base, as bet. It also leaves
*beam proximity* nearly unchanged in every base, which the drafting agent
predicted would fail at odds 0.25 on the strength of a pilot where one base
broke. At full sample it does not break. So the dark entries appear to go
unread even by dense random configurations, not merely by isolated defects.

**P6 held.** Among trials that heal at all, only 21 to 30 percent heal at step
one in the non-frozen bases. The fourteen first-step entries decide nearly all
of transverse stability while directly deciding a minority of healing events,
which is what makes P4's dark-flip invariance a statement about which entries
matter rather than about how fast healing happens.

## The amendment, and what it bought

The draft proposed deducing the eastward-growth class from the westward one.
Nothing licenses that: reflection maps this family to the east-marked family
rather than to itself, which is why the chirality question three units ago had
to be settled empirically; complement conjugation permutes the twelve bits
within each block and cannot exchange the two; and the blocks are not
structurally alike, as the index gaps in the table above show.

Measured rather than assumed: **both growers have transverse extinction
exactly zero in every base**, so the edge lemma is confirmed in both
directions rather than one. Their proximity statistics differ by up to 0.12
with no consistent direction, which at twenty-four per cell may well be
sampling noise. The amendment cost two minutes and converted an assumption
into a weak measurement; it did not overturn anything.

## What this does and does not show

The Program's chain is now: an exactly invariant set on which the refinement
is powerless; a mixture whose weight the refinement controls; and, here, the
exact algebra by which it controls it. Twelve exclusive-ors, rank eleven,
governing growth and survival at every step through the edges of a defect.

It does not show that beam residence *is* one-step healing: one base breaks
that, and three bases show growers sitting closer to the beam than typical
refinements. What sets residence beyond the healing signature is open. Nothing
here concerns Class-IV-ness; the object explained is inheritance of history
gain. Eight bases is a panel, one contract, one density.

## Deviations

The first launch stopped at the matched null-pair control with nothing
computed, which is the control ordering introduced after the previous unit
working as intended. Two faults, both mine, both in the trajectory path: the
complement flag was dropped when the evaluation helper was rewritten for this
unit, so the conjugate ran from the same initial states rather than
complemented ones; and the trajectory helpers were imported from the previous
unit, so event and spread seeds were drawn from its protocol namespace instead
of this one's. The completions are disjoint so nothing was contaminated, but
the runner would have recorded provenance it did not have. Fixed, verified in
isolation at 6.1e-16, relaunched. Cost two minutes rather than a discarded
run.

## Files

`experiments/defect_algebra_20260918/run.py`, `evaluate.py`;
`results/defect_algebra_20260918/` (`rows.json`, `controls.json`,
`summary.json` with source hashes).
