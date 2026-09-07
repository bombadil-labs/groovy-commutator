# Are we predicting the background, or the moving structures?

## The question

In the [history-repair experiment](2026-09-07-history-repairability.md), a
short sequence of coarse observations makes Rule 110 much easier to predict.
But Rule 110's trajectories include a repeating background—the **ether**—and
disturbances that move through it. A predictor could score well by recognizing
the background's phase while missing much of what happens at disturbances.

This note preserves the original proposed experiment. **Update, 2026-09-07:**
the [frozen protocol has now been run](2026-09-07-ether-regions.md). History
improves prediction in all three operational regions, including departure
neighborhoods. Read the new note for results, detector limits, and controls.

## Two explanations to separate

**Phase recovery:** history mostly identifies where the repeating background
is in its cycle. Errors remain concentrated around departures from that
background.

**Recovery of local dynamical context:** history also improves prediction
around moving disturbances and their interactions, beyond its benefit on
background cells.

Both effects could occur. The experiment should measure their relative
contributions rather than force a yes-or-no answer.

## Proposed protocol

1. Start with the existing train/test seed separation and record each
   prediction's position and time, not only its contribution to a mean error.
2. Define a background detector independently of the predictor. Check it
   against a pure ether reference and known departures before using it to
   interpret random trajectories. It must handle the background's spatial
   and temporal phases; matching a single row is not enough.
3. Assign observed targets to background, disturbance neighborhood, or
   ambiguous regions. For a coarse block, state exactly how fine-scale
   labels are combined. Retain ambiguous regions in the aggregate result
   and report their fraction separately.
4. Compare current-only and history predictors within those regions, at
   matched positions and times. Report each region's frequency as well as
   its error so a rare but difficult region cannot disappear in the average.
5. Repeat across independent initial states, ring widths, and observation
   families. Include pure ether as a phase-learning control and preserve
   the existing support/coverage diagnostics.

The exact detector, neighborhood width, and matching tolerances should be
chosen on reference or training data and recorded before examining held-out
prediction outcomes. Detector uncertainty must remain visible in the result.

## What would change our interpretation?

If nearly all improvement comes from background cells, the existing result
would still demonstrate history-dependent prediction, but its connection to
moving computational structures would weaken.

If history also reduces error around disturbances across seeds and
projections, that would justify a more focused study of which local
histories carry the missing predictive context. It would still not establish
a general Class IV criterion.

## What is ready to explain now?

The current evidence supports a modest accessible idea: **a snapshot and a
path can support different predictions**. Claims about what the predictor
understands about gliders or interactions should wait for this distinction
to be tested.
