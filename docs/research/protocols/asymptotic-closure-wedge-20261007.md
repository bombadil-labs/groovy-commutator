# Protocol: the asymptotic-closure wedge

**Status:** frozen before fresh-width evaluation, 2026-10-07.  
**Authored by:** GPT-5.6 Sol (OpenAI). **Reviewed by:** none.

## Origin and separation from the prior unit

The immediately preceding frozen unit tested a one-axis hypothesis: a long thin
tail of minimal predictive repairs should distinguish the 54/110 core from
chaotic controls. It failed at width 10 because Rule 30 had the longest tail.

That negative also exposed a distinction already present in the motivating
cartoon: Rule 30's stable predictive quotient was almost exactly microscopic
identity, while Rules 54/110 retained some nontrivial compression.

The width-10 result is therefore **exploratory input** to this new protocol.
It is not confirmation evidence. This unit freezes a two-axis hypothesis before
evaluating fresh widths.

## Fixed construction

Use exactly the same deterministic future-equivalence tower and observer as the
prior unit:

- source: elementary CA on an even periodic ring;
- observation: nonoverlapping block-2 parity;
- cadence: two source updates;
- \(C_t\): equality of observed trajectories through horizon \(t\);
- \(h_*\): first stable predictive horizon;
- \(H_\infty\): entropy in bits of the stable partition under the uniform
  finite-state ensemble.

No observer, cadence or partition definition may change after evaluation.

## Two coordinates

Define the **repair-depth density**

\[
d=\frac{h_*}{n},
\]

and the **safe-forgetting density**

\[
s=\frac{n-H_\infty}{n}.
\]

Interpretation:

- large \(d\): predictive closure continues to require new distinctions for a
  large fraction of the ring scale;
- large \(s\): the final predictive quotient still discards a nontrivial
  fraction of microscopic information.

The motivating phase-plane cartoon is:

| regime | repair depth \(d\) | safe forgetting \(s\) |
| --- | --- | --- |
| simple / transport-like | low | high |
| chaotic-to-identity | high | low |
| candidate asymptotic closure | intermediate/nonzero | intermediate/nonzero |

This is a relative finite-panel hypothesis, not a universal classification.

## Frozen rule panel

Primary anchors and candidates:

- Rule 184: transport/Class-II anchor;
- Rule 30: chaotic/Class-III anchor;
- Rules 54 and 110: core complex/Class-IV candidates.

Diagnostics only, not used to tune the primary gate:

- Rule 0;
- Rule 4;
- Rule 90;
- Rule 126.

No substitutions.

## Fresh-width gates

The width-10 values are already known and are not scored.

1. **Primary fresh gate:** \(n=12\).
2. **Confirmation:** \(n=14\), only if the primary gate passes.
3. **Stress:** \(n=16\), only if the confirmation passes.

All source states are enumerated exactly.

No all-256 census is authorized.

## Threshold-free wedge prediction

At a scored width, first require the two anchors to define the expected
opposite corners:

\[
d_{184}<d_{30},
\qquad
s_{30}<s_{184}.
\]

Then each complex candidate \(r\in\{54,110\}\) must lie strictly inside both
anchor intervals:

\[
d_{184}<d_r<d_{30},
\]

and

\[
s_{30}<s_r<s_{184}.
\]

Thus the 54/110 core must simultaneously:

1. keep requiring minimal predictive repairs longer than the transport control
   but less extensively than canonical chaos; and
2. retain more compression than canonical chaos but less than the transport
   control.

This is the entire primary decision. No weighted score or fitted boundary is
allowed.

## Decisions

**P1 — width 12.** Both Rules 54 and 110 must satisfy the strict wedge
inequalities above. If either fails, stop and record a negative.

**P2 — width 14.** If P1 passes, both candidates must satisfy the same strict
inequalities at width 14. Otherwise stop.

**P3 — width 16.** If P2 passes, repeat once at width 16 and stop regardless of
outcome. A surviving three-width wedge would justify a later, separately
authorized panel/census.

Rule 126 is retained as an observer-sensitivity diagnostic. If it also occupies
the wedge, that weakens class specificity but does not retroactively alter the
frozen anchor test; report it plainly.

## Additional recorded diagnostics

Without changing any decision, save for every panel rule and evaluated width:

- \(h_*\);
- \(H_\infty\);
- \(d\) and \(s\);
- \(A_{90}\) from the previous unit;
- total latent bits \(H_\infty-H_0\);
- exact repair-bit sequence.

These permit later interpretation without inventing a new gate.

## Hard boundaries

A failure at any fresh-width gate ends this unit. Do not:

- swap Rule 30 or 184 for a more favorable anchor;
- tune thresholds;
- rotate or combine axes;
- change the observer;
- search all 256 rules;
- reinterpret a diagnostic as the primary test.

Every finite ring eventually closes. This experiment tests a finite-size
relative geometry of the approach to closure, not literal infinite nonclosure.

A positive result would not prove Class IV, universality, an infinite-line
limit or representation independence.

## Planned artifacts

- scripts/experiment_asymptotic_closure_wedge.py
- results/asymptotic_closure_wedge_20261007.json
- docs/research/2026-10-07-asymptotic-closure-wedge.md
