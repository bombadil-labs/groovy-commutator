# Independence horizon

**Kind:** finding · **Status:** exact · **Research:** [permanent-structures-20260918](../research/2026-09-18-permanent-structures.md)

Under `A ∧ C` the **defect set never grows** (0 violations of 2,048). But a
cluster perturbs the **agreeing background** around it: its flanks take
`a(LL,L)` and `c(R,RR)`, which need not equal what the base rule would produce.
That perturbation travels at **speed one**.

**Two clusters separated by `s` agreeing columns evolve independently for
`t < s`, and not beyond.**

| separation | 4 | 6 | 8 | 12 | 16 | 24 | 32 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| first mismatch step, minimum | 4 | 6 | 8 | — | — | — | — |
| trials with any mismatch in 128 steps | 8/36 | 3/36 | 5/36 | 0 | 0 | 0 | 0 |

**No fixed separation gives all-time independence**, because the perturbation
spreads without bound; it does not bite within 128 steps once `s ≥ 12`.

**Established by refuting two successive stronger claims.** The drafting agent
claimed 1-clusters independent at separation 2; the executing session corrected
that at freeze to 2-clusters at separation ≥ 3; **the control refuted that too**,
15 violations of 72 across 13 bases. The corrected claim passes at 0 of 216.

**Methodological point, the reason the earlier checks missed it:** they drew
refinements uniformly from the confined set, which is dominated by fast-healing
classes, so defects healed before any perturbation could travel. The refuting
control used a `K∃` refinement with `|DOOMED| = 2`, where defects persist.
**Verify on the adversarial cell, not a random draw.**

**Depends on:** [isolated-defect-gadget](isolated-defect-gadget.md).
