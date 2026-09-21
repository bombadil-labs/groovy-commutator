# Held structures: completion record and stream-timing correction

**2026-09-21.** Authored by Codex (OpenAI), from the frozen work by Claude/Fable
in [PR #279](https://github.com/bombadil-labs/groovy-commutator/pull/279), head
`e8cc3d11f94fe085271329a10c7faaaf90849743`.
Reviewed by: none; Myk suspended the review protocol for this repository reset.
This is a retrospective account and bounded diagnostic, not an independent
full replay or a new pre-registered experiment.

## What is being integrated

The [frozen protocol](protocols/2026-09-18-held-structures.md), runner,
evaluator and [canonical evidence](../../results/held_structures_20260918/)
are preserved unchanged. The record contains 2,112 rows: 33 bases and 64
completions per base across six arms, under the declared height-two contract.
It includes the algebra, gadget, pair-survival tier, controls and all 21
frozen prediction keys. The saved controls have no reported failures.

The original summary records eleven HELD and ten FAILED verdicts, with no
missing keys. **Three of these scores are invalid as scientific tests**:
P4a, P4c and P4d. They consume mistimed gadget predictions. Preserving their
historical JSON does not endorse those verdicts.

## The correction

`transverse_streams()` advances the strip and then appends its two input
columns. It similarly constructs the free stream starting at the first
successor. `gadget_heal()` starts at the initial local state and expects the
input at that same initial time for its first transition. The measurement
therefore feeds `input(t+1)` where the gadget requires `input(t)`.

Control 6 uses pre-step inputs and correctly checks the local transition.
It does not exercise the measurement path that builds the shifted stream.
Consequently passing controls and coherent source hashes did not detect the
measurement defect. The stored rows themselves contain **3,916 disagreements
between driven-gadget healing and actual healing in 38,016 K-arm trials**.

The [bounded diagnostic](../../scripts/audit_held_structure_stream_timing.py)
selects the first stored failing trial for bases 51, 90 and 110, reconstructs
its exact initial state and replays 128 steps. It reproduces the stored
actual healing and erroneous prediction, then supplies the pre-step stream:

| Base | Completion | Rep / origin | Actual healing | Historical prediction | Corrected driven prediction |
| ---: | ---: | --- | ---: | ---: | ---: |
| 51 | 14076995 | 0 / 293 | 2 | 3 | 2 |
| 90 | 16766764 | 1 / 431 | 3 | 2 | 3 |
| 110 | 1433512 | 0 / 288 | 7 | 6 | 7 |

On the Rule-51 witness the free and driven streams agree, and correcting their
alignment makes both predictions agree with the dynamics. P4a's recorded
failure therefore cannot refute the undriven-stream claim. On the Rule-110
witness the corrected free predictor still differs (6 versus 7); three
witnesses do not settle any aggregate prediction. Exact diagnostic output
and source hashes are in
[`held_structures_20260921_timing_audit.json`](../../results/held_structures_20260921_timing_audit.json).

This is a post hoc bug diagnosis. The original predictions are **invalidated,
not converted from FAILED to HELD**. A corrected source-domain run and fresh
scoring are needed before interpreting P4a/P4c/P4d. We are not funding that
run as an automatic consequence of discovering the bug.

## Complete prediction accounting

| Keys | Stored verdict | Current interpretation |
| --- | --- | --- |
| P1a, P1b | HELD | Exact census/read identities hold on all 2,112 stored rows. |
| P2a, P2b, P2c | HELD | SAFE singletons, matching alternating runs and the eight pair-permanent bases pass the stated finite checks. All-time claims rely on the protocol's algebra, not the observation horizon alone. |
| P3a | HELD | The specified base-mean singleton band holds on this panel. |
| P3b, P3c, P3d | FAILED | The stronger within-base ordering, weak base dependence and lowest-base predictions do not hold as scored. |
| P4a | FAILED | **Invalidated by timing defect.** |
| P4b | FAILED | Direct stream-divergence threshold fails; it compares the two streams at the same recorded time and does not consume gadget healing predictions. |
| P4c, P4d | HELD | **Invalidated by timing defect.** Do not cite the recorded agreement or correlation as predictor performance. |
| P5a-i, P5a-ii | FAILED | Proposed small alternating-interior bounds fail. |
| P5a-iii, P5b | HELD | Matching-pattern comparisons hold on the specified eight bases. |
| P5c, P5d | FAILED | Specificity and replication expectations fail under the frozen scoring. |
| P6a | HELD | The G-arm singleton/pair-survival anticorrelation meets its declared threshold. |
| P6b | FAILED | The random-arm comparison does not meet its declared threshold. |

This leaves nine HELD, nine FAILED and three invalidated scores. A tally is
not a measure of theory quality. Unaffected scores are accepted as the
recorded finite computation, not newly independently replicated conclusions.

## What survives and where we stop

The local structural dictionary, the six-bit gadget reduction and the
edge-automaton argument remain distinct from the broken healing-predictor
measurement. The canonical controls record both branches of the edge check,
including 2,252 same-junction steps with no errors. Finite controls alone do
not upgrade every “theorem-level” protocol clause to a reviewed theorem;
the arguments and their exact assumptions remain in the protocol.

The census still does not supply a general Class-IV explanation. Several
specificity and transfer bets fail even outside the timing defect. The
research program is **paused after this accounting**, with no tenth unit
queued. A future restart must justify the mechanism's independent payoff
and correct the measurement path before using the invalidated scores.

Earlier provenance incidents remain visible in PR #279: amended controls,
the initial unreachable-control return, and the evaluator's P1b correction.
PR #278's earlier “not evaluated” correction is also preserved. Missing,
invalid and negative results are different states.

## Verification

The reset re-scored the saved rows with the frozen evaluator and compared the
summary byte for byte, checked the registered source hashes, and ran the
small timing diagnostic above. These checks do not re-run the 2,112-row
experiment or independently review all its mathematics. The frozen runner is
retained for historical reproduction, with notices in its experiment and
result directories; it should not seed another run without a correction.
