# Selective predictive persistence × spreading: the recovered 2026-09-16 discriminator record

Does a statistic frozen before fresh simulation separate the core complex
families 54 and 110 from every undisputed Class I–III representative under
five fresh width/density conditions? On the surviving evidence, yes: the
candidate `S = max(0,R_7)·max(0,M_8)` with `select ⇔ S > 0.20 ∧ α_512 > 0.50`
passes 10 of 10 core decisions, 0 of 420 undisputed negatives, 0 of 10 for
the disputed 41/106, and rejects a radius-two rare-correction adversary
(0/5) and a pure shift (0/5). This note records that result at the evidence
level it can now support: **the report and the complete result tables
survive; the three hash-pinned protocol files, the runner and the canonical
JSON were lost with the GPT session and have not been recovered byte for
byte.**

Evidence: prospective finite result on the surviving tables; provenance
partially reconstructed. Executed by GPT-5.6 Sol, 2026-09-16, under Myk's
no-review-at-freeze authorization. Reconstruction packaged by GPT on
2026-09-17 with explicit non-claims; integrated by Claude/Fable 5.1 on
2026-09-17 with the cross-model review gates suspended by Myk. Evaluation
preceded review.

## What survives and what does not

Survives (Project Library copies, integrated under
`experiments/class4_selective_persistence_20260916/evidence/`): the final
report; the 450-row all-conditions table (90 candidates × 5 conditions); the
90-candidate cross-condition summary. The rows satisfy `S = max(0,R)·max(0,M)`
and `α = log2(d̄_512 / d̄_256)` to floating precision, and the counts and
margins above recompute from them (`verify_reconstruction.py`).

Not recovered: the protocol bytes whose SHA-256 the report cites
(`3e5c7efe…`, `71fc7979…`, `bd3b231e…`), the runner, the six fresh seeds per
condition, the exact local definition of the radius-two rare-correction
challenge, and the canonical JSON. The reconstructed protocols and runner
under `reconstructed/` restate the scientific contract from the report and
from the exact `R` and `M` definitions in the 2026-09-15 independent Class-IV
unit; they carry new hashes and must never be presented as the originals.
A run of the reconstructed runner is a new replication.

## The candidate

`R` is the same-window selective-retention statistic at block width 7
(visited mean of boundary-conditioned reference ambiguity minus predecessor
ambiguity, standardized by the uniform standard deviation). `M` is the
held-out log-loss gain of an eight-step local history over the current bit,
averaged over both fold directions. `α_512` is the doubling exponent of the
mean single-bit disturbance-support diameter from t = 256 to t = 512 over 96
trials (16 origins × 6 burned seeds). Conditions: P (2053, 0.5), V1 (2063,
0.3), V2 (2081, 0.7), S1 (2069, 0.1), S2 (2099, 0.9); burn 2048; 512 scored
transitions.

## Margins

| quantity | value |
| --- | ---: |
| minimum positive `S` | 0.204989562 |
| minimum positive `α_512` | 0.683126863 |
| maximum `S` among undisputed negatives with `α > 0.5` | 0.000000000 |
| maximum `α_512` among undisputed negatives with `S > 0.2` | 0.498938757 (rule 62) |

Rule 5 persists without spreading; rule 62 persists and spreads just under
the gate in all five conditions; rules 122 and 126 spread at `α ≈ 1` with
`S = 0`; the radius-two correction family spreads in four of five conditions
with `S = 0` throughout, which is what defeats the earlier recurrence-plus-
spreading proxy.

## What this is and is not

A finite discriminator for the 54/110 core phenotype under the project's
convention. It rejects the conventionally Class-IV rules 41 and 106, so it is
not a Wolfram-class classifier. The two-axis idea (organization plus damage
spreading) is prior art (Langton 1990; Bagnoli, Rechtman and Ruffo 1992;
Wuensche 1999; Feldman, McTague and Crutchfield 2008; Borriello and Walker
2017; Mediano et al. 2022; Mirza 2026, whose block-entropy × damage-spreading
plane is the closest). The candidate-specific delta is that `S` is a
selective-visitation statistic times held-out history value rather than an
entropy, and that it rejects the rare-correction mechanism. Novelty is
unverified.

## Files

`experiments/class4_selective_persistence_20260916/` with `HASH_MANIFEST.json`
and `PROVENANCE.json` as received.
