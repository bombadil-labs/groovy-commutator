# Jev as a semantic feature scout for the 54/110 phenotype: Runs 1 and 2 recorded

Can a System One judgement model, shown anonymous primitive measurements of
the 88 elementary-CA symmetry representatives with no rule identities, point
at a mechanism that separates the core complex families 54 and 110? On two of
six frozen questions, persistence across conditions (J4) and selective memory
(J5), yes: both core families rank in the top seven of 88 with finite-panel
AUC 1.0 against the eleven Class-III representatives, and the only rules at or
above them are Class II (62, 5, 9, 25, 14, 1, 108). A generic opaque-profile
control does not reproduce this. Jev was a scout, not a classifier: its lead
was distilled into the transparent statistic `S = max(0,R_7) · max(0,M_8)`,
which the next unit froze and validated on fresh simulation.

Evidence: exploratory. Protocol frozen 2026-09-16 by GPT-5.6 Sol
(`docs/research/protocols/2026-09-16-jev-class4-probe.md`, SHA-256
`9c2f53db…`); runs executed by Myk locally on 2026-09-17 (UTC) with the
official TypeSafe SDK 0.6.0 against model `jev-1.13.0`; records integrated
and independently re-evaluated by Claude/Fable 5.1 on 2026-09-17 from Myk's
workspace. **Review:** none at freeze; Myk authorized the runs; the
cross-model review gates were suspended on 2026-09-17, so this integration is
self-reviewed. Evaluation preceded review.

## What Jev was shown

Each of the 88 representatives became one anonymous JSON state: a
`measurement_contract` giving operational definitions of five measurement
kinds, a label-free `cohort_reference` (median, quartiles, IQR of every
feature over all 88), and a `candidate` block of 49 features in three
families, each as raw value, percentile rank and robust scale:

- F1, 36 features: selective retention `R` at block widths 5, 7, 9; held-out
  predictive gain `M` and residual uncertainty `U` at history depths 4, 8, 12;
  each under the primary and replication conditions of the 2026-09-15
  independent Class-IV unit, as mean and range over fold directions;
- F2, 4 features: commutator-history predictive gain summaries;
- F3, 9 features: partial-rule cohabitation geometry from the 2026-09-15
  cohabitation audit.

Withheld on purpose: the recurrence residual and spreading exponent of the
beam-discriminator baseline, the quotient-cycle slopes, every composite
selected after seeing labels, and the label-selected observation-catalog
slots. No rule number, truth table, class or symmetry identity appears.

Six Noul questions J1–J6 were asked in one request (SHA-256 of the question
block `77f4b192…`), three identical requests per candidate. Run 2 replaced
every feature name with a frozen code from a seed-20260916 codebook, dropped
the contract, and asked one generic coherence question O1.

## Results, re-evaluated from the raw records

Both runs: 264 of 264 requests succeeded, model `jev-1.13.0`, largest
three-attempt range 0.08 (Run 1) and 0.05 (Run 2). Every response's recorded
state and question hashes reproduce from the request files. The frozen
evaluator (`evaluate_jev_probe.py`) gives:

| question | reading | rank 54 | rank 110 | negatives ≥ lower positive | AUC vs Class III | gate | stable |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| J1 | retained history with openness | 7 | 7 | 7 (14, 9, 73, 25, 142, …) | 0.955 | moderate | yes |
| J2 | constrained but non-rigid cohabitation | 25 | 52.5 | 53 | 0.682 | none | yes |
| J3 | cross-channel coherence | 2 | 8.5 | 7 (62, 14, 18, 9, 142, …) | 0.955 | moderate | fails leave-one-out |
| J4 | persistence across conditions | 6 | 3 | 5 (62, 5, 25, 14, 9) | 1.000 | moderate | yes |
| J5 | selective memory | 2.5 | 6.5 | 5 (62, 9, 5, 1, 108) | 1.000 | moderate | yes |
| J6 | balanced capacity | 4 | 41.5 | 40 | 0.818 | none | yes |

Run 2's generic question ranks 54 at 59.5 and 110 at 67.5 of 88 (AUC 0.182
against Class III) and correlates weakly with the semantic judgements
(Spearman 0.14–0.31). The {54,110} pair reaches a moderate-or-strong gate on
four of six questions; 6 of 3,655 arbitrary undisputed pairs do, concentrated
on 9, 14, 54, 110.

## Limits

Two positive families, dependent panel statistics, no generalization claim.
Run 2 changed feature semantics and the question together, so it is not an
ablation of names alone; Run 3 below is that ablation. Jev does not "understand"
cellular automata; the scientific object became the transparent `S`
statistic. The feature table's derivation from the repository's 2026-09-15
canonical results was not re-derived here; the table is preserved as
supplied.

## Run 3: the matched operational-codebook ablation

Frozen as `docs/research/protocols/2026-09-17-jev-codebook-ablation.md`:
the exact Run-1 numeric states (every recorded state hash verified before
renaming), every feature key replaced by its Run-2 codebook code, a
`measurement_contract` keyed by those codes that says how each number is
computed without any of the old names or interpretive words, and the six
J1–J6 questions unchanged. Acquired 2026-09-17 by a child session of this one
(`session_019qKFKRapZhjA8EtzVbgTVS`, acquisition only, no analysis, no access
to rule identities), 264 of 264 requests ok, model `jev-1.13.0`, SDK 0.6.0,
largest three-attempt range 0.07. Every response's source, transformed,
question and codebook hashes match the committed request files.

| question | rank 54 | rank 110 | negatives ≥ lower positive | AUC vs Class III | gate | Spearman vs Run 1 | Spearman vs Run 2 (O1) |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| J1 | 5 | 5 | 6 (25, 14, 9, 142, 62, …) | 1.000 | moderate | 0.80 | 0.44 |
| J2 | 49 | 49 | 53 | 0.318 | none | 0.69 | 0.23 |
| J3 | 1.5 | 8 | 7 (62, 25, 58, 35, 156, …) | 1.000 | moderate | 0.68 | 0.33 |
| J4 | 11 | 2.5 | 11 (5, 62, 156, 14, 142, …) | 1.000 | none | 0.81 | 0.32 |
| J5 | 5.5 | 5.5 | 6 (25, 5, 14, 142, 62, …) | 1.000 | moderate | 0.68 | 0.46 |
| J6 | 3.5 | 28 | 29 | 0.818 | none | 0.72 | 0.40 |

Under the frozen interpretation this is closer to "operational meaning is
sufficient" than to "the effect needed the evocative names": J1, J3 and J5
keep their moderate gates with AUC 1.0 against Class III, J5 and J1 are
stable, the {54,110} pair's finite pair-null fractions stay below 0.01 on
J1/J3/J5, and every question's ranking correlates 0.68–0.81 with Run 1
against 0.23–0.46 with the opaque generic control. The one degradation is
J4 (persistence across conditions): rule 54 falls from rank 6 to 11 with
eleven Class-II negatives at or above it, so its gate lapses while 110 and
the Class-III AUC hold. Yes-probabilities are uniformly higher in Run 3 than
Run 1 (means 0.56–0.82 against 0.46–0.72), so the codebook prompt shifts
calibration as well as ranking. Reading: the operational definitions carry
most of the J1/J3/J5 signal; the J4 result had some dependence on the
original naming or on how the conditions were labelled, and should be
treated as the weaker of the two Jev leads. Files in
`experiments/jev_class4_20260916/run3/` (`jev_codebook_responses.jsonl`,
`jev_codebook_evaluation.json`, `run1_vs_run3_comparison.json`,
`evaluate_run3.py`, the Run-1-scoring evaluator with the mode filter widened).

## Files

`experiments/jev_class4_20260916/`: the frozen protocol, request states,
codebook, truth file (evaluator-only), raw responses of both runs, evaluator,
classical controls and Run-3 materials, with `manifest.json` hashes.
