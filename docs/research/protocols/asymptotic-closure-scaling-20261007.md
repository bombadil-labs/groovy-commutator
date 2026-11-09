# Protocol: asymptotic closure as a scaling sequence

**Status:** frozen before widths 16/18 are evaluated, 2026-10-07.  
**Authored by:** GPT-5.6 Sol (OpenAI). **Reviewed by:** none.

## Why this is a new test

Two bounded precursor tests are already known to the author:

1. at width 10, a long thin repair tail by itself is not Class-IV-specific;
   Rule 30 has the longest tail and its predictive quotient is almost identity;
2. a pointwise two-axis wedge passes at width 12 but fails at width 14 because
   Rule 110 ties Rule 184 in integer repair depth.

Those outcomes are exploratory inputs here, not confirmation evidence.

The width-14 failure exposes a mathematical issue with a pointwise
"asymptote": the minimal history depth \(h_*(n)\) is integer-valued and can sit
on plateaus before jumping. A genuine asymptotic claim should concern the
**sequence across system sizes**, not strict interiority at every width.

## Fixed observer and exact objects

Use the same established construction:

- elementary CA source;
- even periodic ring of width \(n\);
- nonoverlapping block-2 parity observation;
- cadence \(q=2\);
- exact future-equivalence tower \(C_t\);
- \(h_*(n)\): first stable predictive horizon;
- \(H_\infty(n)\): entropy of the stable predictive partition under the uniform
  finite-state ensemble.

Define the absolute safe-forgetting reserve

\[
R(n)=n-H_\infty(n).
\]

This is the number of source-state bits, in Shannon coding cost under the
uniform finite domain, that the entire observed future never needs.

## Frozen primary rules

- Rule 30: chaotic-to-identity anchor;
- Rule 184: transport/coarse anchor;
- Rules 54 and 110: core complex candidates.

Rules 0, 4, 90 and 126 may be recorded as diagnostics but do not enter the
primary decision.

No substitutions.

## Previously observed baseline, not scored

From the prior exact units:

At width 14,

\[
h_{54}=5,\qquad h_{110}=4.
\]

Across widths 10--14, Rule 30's reserve is already near zero, while Rule 184's
reserve is much larger than the 54/110 reserves.

These facts motivated the present hypotheses and cannot count as new evidence.

## Fresh widths

Evaluate exactly:

1. \(n=16\);
2. \(n=18\), only if the width-16 reserve corridor below passes for both
   candidates.

All \(2^n\) source states are enumerated.

No width 20 and no all-rule census are authorized.

## P1 — fresh reserve corridor at width 16

For each \(r\in\{54,110\}\),

\[
R_{30}(16)<R_r(16)<R_{184}(16).
\]

Both candidates must pass. Otherwise stop before width 18.

This encodes "neither collapse to microscopic identity nor extensive
coarse forgetting" without a fitted numeric threshold.

## P2 — reserve corridor survives width 18

If P1 passes, require for each complex candidate

\[
R_{30}(18)<R_r(18)<R_{184}(18).
\]

Failure ends the unit.

## P3 — the repair staircase advances

If P1 and P2 pass, require both complex candidates to have acquired at least
one additional necessary history distinction by width 18 relative to the
already observed width-14 baseline:

\[
h_{54}(18)>5,
\qquad
h_{110}(18)>4.
\]

This is deliberately a four-cell width interval, allowing a plateau at width
16. It asks whether closure continues to recede as the system grows rather
than requiring a jump at every finite width.

## Interpretation

A pass would establish only a bounded scaling pattern on this fixed observer:

- new predictive distinctions appear at larger system size for both 54/110;
- their stable quotient continues to forget more information than Rule 30's;
- it forgets less than Rule 184's.

That would be evidence for a candidate **asymptotic-closure corridor**, not a
Class-IV theorem.

A failure is complete for this formulation. Do not rescue by extending to
width 20, changing anchors, normalizing \(R\), or weakening the staircase
condition.

## Saved diagnostics

For every evaluated primary and diagnostic rule save:

- \(h_*(n)\);
- \(H_\infty(n)\);
- \(R(n)\);
- safe-forgetting density \(R(n)/n\);
- repair-bit sequence;
- the previous long-tail \(A_{90}\) statistic.

## Scope

Finite periodic rings only. No infinite-line claim, universality claim,
representation independence, or classifier claim.

## Planned artifacts

- scripts/experiment_asymptotic_closure_scaling.py
- results/asymptotic_closure_scaling_20261007.json
- docs/research/2026-10-07-asymptotic-closure-scaling.md
