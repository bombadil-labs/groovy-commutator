# Protocol: Jev matched operational-codebook semantic ablation

**Status:** FROZEN / UNRUN  
**Date:** 2026-09-17  
**Author:** GPT-5.6 Sol, Groovy Commutator session  
**Protocol review:** none at freeze; Myk explicitly authorized further Jev work and the repository no-review-at-freeze path in the project conversation on 2026-09-17. Independent review remains required before this result could be merged/promoted.

## Question

The completed Jev semantic run changed semantic feature names/definitions into a generic opaque profile in its control run. Because the control also replaced J1–J6 with one generic question, it does not isolate **where** the semantic signal entered.

This matched ablation asks:

> If the exact same Run-1 numeric states and exact same J1–J6 questions are retained, but short feature names are replaced by opaque codes while operational measurement definitions remain available, do the J4/J5 rankings survive?

## Frozen source

- Same 88 anonymous representative profiles as completed Run 1.
- Same serialized numeric values, normalization, cohort references, missing values and aliases.
- Three requests per profile.
- Prefer actual model `jev-1.13.0`, which served both prior completed runs.
- No rule ID, truth table, Wolfram class or symmetry-family identity may enter a request.

Before transformation, a rebuilt source state must match the `state_sha256` stored for that alias in `jev_raw_responses.jsonl`. If exact source hashes cannot be reproduced, stop calling the run a matched ablation.

## Only permitted transformation

Create one frozen bijection from semantic feature keys to opaque codes `f001`, `f002`, ... . Reuse the prior seed/codebook `20260916` if available; otherwise save and hash a newly generated one before the first request.

For every numeric feature:

- rename its key to the corresponding opaque code;
- do not alter its value;
- preserve raw, percentile and robust-scale representations;
- preserve cohort statistics;
- key the measurement contract by opaque code;
- give the operational definition of the measurement without revealing its former evocative short name or introducing class/complexity language.

No feature selection, recombination, thresholding or renormalization is allowed.

## Questions

Use the exact original J1–J6 text and criteria from `jev_class4_protocol_20260916.md`, unchanged and in one request. Their original question specification has SHA-256:

`77f4b1924f9f39845bd200deb30931ec30586934373ef4d363309b66691cb8e6`

Do not edit a question after the first response.

## Acquisition

For each alias:

- make three identical scientific requests;
- save failures rather than silently substituting a fourth scientific attempt;
- record actual returned model, timestamp and usage;
- record original source-state SHA-256, transformed-state SHA-256, question SHA-256 and codebook SHA-256.

Recommended raw output: `jev_codebook_responses.jsonl`.

No ranks, rule identities or positive labels may be inspected until all 264 intended requests are saved.

## Frozen primary evaluation

For each J1–J6 separately:

- median yes-probability across successful attempts;
- rank of 54 and 110;
- number of undisputed negatives at or above the weaker positive;
- finite-panel AUC versus all undisputed Class-I–III representatives;
- finite-panel AUC versus inherited Class-III representatives;
- leave-one-attempt stability as in the original analysis;
- hard controls and disputed 41/106 descriptively, using the same original conventions.

Do not fit a weighted combination of questions.

Primary comparison is Run 3 versus the completed semantic Run 1, with the completed generic opaque Run 2 as a second reference.

## Interpretation fixed before acquisition

- Run 3 near Run 1: operational definitions are sufficient; evocative short names were unnecessary.
- Run 3 near generic opaque behavior: original enrichment depended substantially on semantic surface cues not preserved by operational definitions.
- Intermediate: both operational definitions and original lexical framing contributed.

If the returned Jev model differs from `jev-1.13.0`, do not attribute score changes to the ablation without replaying the original semantic condition on the new model.

## Non-claims

This experiment does not establish that Jev understands cellular automata, does not validate a universal Class-IV definition, and does not supply new unseen-positive generalization. It is a matched semantic-source ablation of an already completed exploratory scout.

Operational run instructions with the verbatim J1–J6 text are in `JEV_RUN3_CODEBOOK_ABLATION.md`.
