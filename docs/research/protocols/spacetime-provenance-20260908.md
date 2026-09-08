# Spacetime provenance and future ambiguity: frozen protocol

2026-09-08. Freeze before enumeration. This tests the many-to-one map from a fixed elementary rule and initial ring to a visible spacetime panel. It is a prerequisite for the dimensional-compatibility program, not a Class-IV classifier or a higher-dimensional dynamics experiment.

## Domain and observations

All 256 fixed binary elementary CA rules, all initial configurations on periodic rings of widths 6, 8, 10. A rule is held fixed for its complete trajectory. A panel contains the full rows S0 through St for t=0..6. No cropped spatial boundaries, hidden initial row, noise, or unknown time cadence. Compare distinct observed panels as the primary units; separately report weighting by generating (rule, initial-state) pairs. Neither count is an independent statistical sample.

## Exact inference

Every observed transition fixes outputs of the rule table at the three-cell input patterns it visits. If mask M records those inputs and V their observed outputs, all and only the rules r with (r & M)=V reproduce the panel from S0. Thus compatible rule count is 2^(8-popcount(M)). Verify against direct replay on every distinct panel at width 6 and all declared t, plus deterministic selected wider panels. Group by complete panel identity; implementation may use an equivalent key (S0,M,V) with fixed t and width. Verify this equivalence and group multiplicities.

## Evolution-sensitive targets

For each observed panel, keep each compatible rule fixed and enumerate its next h rows, h=1..4. Repeat after flipping cell 0 of the final observed row once, before those h evolution steps. The intervention is the same for every compatible rule; it adds no provenance information. Count distinct future continuations, not just endpoints. Record rule-unique panels, ambiguous-rule panels with one continuation, and panels with multiple continuations. Report rule ambiguity bits 8-popcount(M) and the minimum fixed-length side-information budget ceil(log2(number of distinct continuations)) conditional on that panel, intervention and horizon. This last code may be purpose-specific and does not imply a reusable rule identifier. Compare how the flip changes continuation counts in paired panels. Primary comparison: t=2, h=4; retain the entire declared grid.

## Controls and witnesses

Check the CA engine independently, true-rule inclusion, candidate multiplicities, consistency of all observed constraints, nested candidate sets along each trajectory, single-rule future determinism and direct future enumeration. Include the all-zero panel under rules 0 and 204: both have the same unperturbed future forever, but respond differently after a bit flip. Include the smallest width-8 initial ring visiting all eight neighborhoods, using rule 0, to demonstrate identification in one transition without complex dynamics. Save the first lexicographic width-6 t=2 panel with h=4 autonomous ambiguity and the first with h=1 agreement but h=4 disagreement if present; absence is a valid outcome.

Witness provenance records have content-addressed panel nodes and separate generating edges with rule, initial-state identity, width, periodic boundary, timestep count, decoder and bit-order convention. Multiple derivations point to one panel. Label this as a witness subset, not the full provenance graph. Distinguish stored performed derivations from logically compatible alternatives; here exhaustive replay can verify the witness alternatives.

## Reporting

Save reproducible code, complete aggregate rows, uncertainty-count histograms, exact checks, witnesses and a scientific figure. Update Research and the knowledge base. No class labels are loaded, no metric is tuned to known exemplars, and no dimension-independent or unbounded ambiguity claim is inferred from bounded trajectories. The zero-panel forever statement and visited-input count have elementary proofs.
