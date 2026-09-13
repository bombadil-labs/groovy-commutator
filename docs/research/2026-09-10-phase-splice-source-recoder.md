# Research Note 038: Changed provenance is not enough — one phase cut fails exactly

**Date:** 2026-09-10  
**Program:** Dynamics of Erased Distinctions  
**Publication identity:** Note 038 / `phase-splice-source-recoder`

## Result

Note 037 showed that exact symbolic local dynamics is compact while same-source temporal recurrence nevertheless resolves none of the 170 Research034 frontier questions. The missing freedom was source provenance: an earlier representative of a later slice need not come from the same initial background.

This note tests the first relational recoder that uses that freedom. For a one-defect source pair, evolve both scalar rails for `k` macrosteps, choose the evolved left rail on one side of a reinserted seed and the evolved right rail on the other side (`LR`), or vice versa (`RL`), then evolve the recoded source for `j` further steps. A passing identity at `t=k+j` would prove

\[
X_t(s)\subseteq X_j(s)
\]

and therefore exact all-time permanence for every still-safe target attached to that seed language.

The frozen primary domain contained the **22 distinct seed languages underlying all 170 Research034 frontier questions**. The fresh family used only `LR/RL`, with `2<=t<=6`, `k,j>=1`, and `|delta|<=k`.

The first exact MDD census settled every Class-II seed language but hit the frozen 20-minute per-seed wall on the twelve Rule-122/161 Class-III sentinels:

- **10/22 seed languages:** exact `no-phase-splice-through-6`;
- **12/22:** censored by wall time;
- **0 certificates**;
- **158 target questions:** exact negative;
- **12 target questions:** initially censored;
- maximum observed MDD size: **1,747,841** nodes, below the 5,000,000-node ceiling.

The censoring was then recovered under the *same* 1,200-second per-seed wall using an independently encoded manual CNF over the original fine ECA and Minisat22. Every one of the twelve sentinels completed exactly:

- **12/12 recovered sentinel seed languages:** `no-phase-splice-through-6`;
- **0 recovery certificates**;
- **0 recovery censoring**;
- largest SAT instance: **1,314 variables / 9,943 clauses**.

Combining primary and recovery gives the final exact result:

\[
\boxed{22/22\text{ frontier seed languages admit no frozen }LR/RL\text{ phase-splice certificate through }t=6.}
\]

Thus **0/170 frontier target questions receive a permanence certificate from this family**.

## What was learned

The negative is sharper than Note 037's recurrence null.

Note 037 ruled out a same-provenance identity family. Note 038 permits a *different admissible source row* and explicitly uses the one-defect source graph's latent left/right phase to select provenance. That additional freedom is still insufficient when it is expressed by only one spatial phase cut.

So the current boundary is:

> **Changed provenance is necessary freedom to consider, but one bit of source phase plus one cut is not a sufficient proof object for the frontier.**

The SAT recovery also separates dynamical and representational difficulty. The Rule-122/161 cases that exhausted MDD wall time were settled under the identical seed wall by compact CNF. Their earlier censoring was therefore a backend/representation boundary, not evidence that the phase-splice identities were intrinsically undecidable or anomalously deep.

## Controls and provenance

The production MDD instrument reproduced the disclosed Rule-5 positive normalization and rejected all 22 Rule-35 fresh-family candidates through `t=3`, as required by the known first horizon-3 witness. The SAT recovery independently reproduced the same semantic controls.

Canonical records:

- primary full result: `results/phase_splice_source_recoder_20260909.json`;
- primary compact summary: `results/phase_splice_source_recoder_20260909_summary.json`;
- primary full-result SHA-256: `af00ce04f134bd98ecd2d2bd7a0bf2a00b2c2c5d9b7d34c2ebcd9cc22e329138`;
- SAT recovery full result: `results/phase_splice_sat_recovery_20260910.json`;
- SAT recovery compact summary: `results/phase_splice_sat_recovery_20260910_summary.json`;
- SAT recovery full-result SHA-256: `0540fc2a4bf3801e7cd5f8dad9514022c120bda773d2591fcc78d6a17d0aa90f`.

## Next boundary

A single cut can only say "take provenance from this rail before here and that rail after here." The smallest genuinely new selector adds one more transition: use one rail by default, switch to the other over a bounded interior interval, then switch back.

The next frozen checkpoint therefore tests a **bounded repair-island source recoder** before considering multiple islands, arbitrary finite selector masks, or synthesized local repair transducers.
