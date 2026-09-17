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
ablation of names alone; the matched operational-codebook ablation (Run 3,
frozen as `docs/research/protocols/2026-09-17-jev-codebook-ablation.md`, with
its transformed states built and hash-verified in
`experiments/jev_class4_20260916/run3/`) is unrun. Jev does not "understand"
cellular automata; the scientific object became the transparent `S`
statistic. The feature table's derivation from the repository's 2026-09-15
canonical results was not re-derived here; the table is preserved as
supplied.

## Files

`experiments/jev_class4_20260916/`: the frozen protocol, request states,
codebook, truth file (evaluator-only), raw responses of both runs, evaluator,
classical controls and Run-3 materials, with `manifest.json` hashes.
