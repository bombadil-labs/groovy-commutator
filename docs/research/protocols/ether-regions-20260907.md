# Frozen protocol: Rule 110 regional history prediction

This protocol and its executable [parameter file](ether-regions-20260907.json)
are recorded before examining held-out prediction outcomes. It implements the
[ether-or-defects plan](../2026-09-07-ether-or-defects.md).

The primary comparison is current-only radius-one prediction versus the same
neighborhood at seven observed times (six previous times), with a training-only
majority lookup and minimum-support-five backoff. All depths use identical
targets. Two disjoint eight-seed training ensembles are scored separately on
the same eight new held-out seeds. Rings of 420 and 840 cells accommodate the
ether's spatial period and all five existing observers. Burn-in is 150 fine
steps, followed by 512 observed steps. Current-only radii 3 and 10 provide
spatial controls; radius 10 has the same 21 input bits as the longest history,
but the two contexts need not carry equal information or have equal coverage.

Reference ether is the repeated word `00010011011111`. Verify its seven-step
temporal period directly, and construct all spatial/temporal phases by exact
evolution. At forecast time t, compare patches at t-2, t-1, t to one coherent
phase. Matching separate arbitrary phases in each row is not permitted.

The primary detector uses short and long radii 3 and 7 (widths 7 and 15).
An exact long match marks a fine center background-compatible; no short match
marks a departure; the remainder is ambiguous. A fixed sensitivity detector
uses radii 7 and 14 (widths 15 and 29). These are local compatibility labels,
not identified particle species or collisions. No detector parameters will
be selected using test prediction accuracy.

To label a predicted coarse target, examine the fine causal footprint at t:
the target block expanded by q cells on each side for block observations at
stride q, or q+1 for the derivative observation. Any departure center makes
the target a departure-neighborhood target; all background centers make it
background; all other cases are ambiguous. Labels never use the predicted
future or enter a predictor. Record all three groups and the aggregate.

Before evaluation, validate all ether phases, a known single-bit perturbation,
translation covariance, the inclusion of long matches in short matches, and
label independence from future rows. Pure-ether forecasts and trajectories
with 2% of initial ether bits flipped are additional controls, scored by the
same random-trained models. They are not independent random-soup replicates.

Save integer sample, error, and support counts by training ensemble, held-out
trajectory, observer, width, detector, region, and history depth. Summarize
paired error differences and signed contributions to aggregate improvement:
region frequency times its error reduction. Report held-out seed ranges
conditional on training; do not manufacture independent samples from cells.
Preserve negative effects and ambiguous targets. This experiment cannot by
itself identify glider computation or establish a finite-memory closure law.
