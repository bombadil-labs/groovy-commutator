# Protocol: asymptotic closure under minimal predictive repair

**Status:** frozen before evaluation, 2026-10-07.  
**Authored by:** GPT-5.6 Sol (OpenAI). **Reviewed by:** none.

## Question

For a deterministic system observed through a lossy representation, the
repository already defines the exact future-equivalence tower

\[
C_0 \preceq C_1 \preceq C_2 \preceq \cdots \preceq C_\infty,
\]

where two microstates are equivalent in \(C_t\) iff their observed trajectories
agree through horizon \(t\).

This tower has a useful optimality property: for the declared future semantics,
\(C_{t+1}\) is the coarsest refinement of \(C_t\) that restores exactly the
distinctions required by one additional observed future step. No search over
candidate repairs is needed.

The hypothesis is therefore:

> **Class-IV-like dynamics approach predictive closure asymptotically: most
> required information can be compressed early, yet small additional
> distinctions remain necessary for a long and growing sequence of horizons.**

On every finite ring the tower eventually closes. The claim being tested is
the *shape and finite-size scaling of the approach*, not literal infinite
nonclosure.

## Fixed observer

Use the established nonoverlapping block-2 parity observer:

- elementary CA source rule \(H\);
- even periodic source ring of width \(n\);
- cadence \(q=2\) source updates;
- observation \(P\): XOR each adjacent pair, producing \(n/2\) macro bits.

This observer is fixed before evaluation. The 2026-09-08 history-lift study
already showed nontrivial memory scaling under it, including growing finite-ring
memory for the repository's Class-IV-labelled rules.

## Frozen rule panel

| Rule | role |
| ---: | --- |
| 0 | constant Class-I control |
| 4 | nonlinear idempotent/simple control |
| 90 | additive exact-factor control |
| 184 | ballistic/traffic Class-II control |
| 30 | canonical chaotic Class-III control |
| 126 | strongly spreading Class-III control |
| 54 | core Class-IV/complex rule |
| 110 | core Class-IV/complex rule |

No substitutions after evaluation.

## Width gates

1. Primary: \(n=10\).
2. Confirmation: \(n=12\), only if the primary complex-vs-chaotic ordering
   below survives.
3. Stress: \(n=14\), only if the ordering also survives \(n=12\) and is not
   already explained by the Rule-184 transport control.

No all-256 census is authorized by this protocol.

## Exact quantities

For the uniform ensemble of all \(2^n\) source states, let \(H_t\) be the
Shannon entropy in bits of the exact partition \(C_t\). Let \(h_*\) be the
first stable horizon and \(H_\infty=H_{h_*}\).

Define

\[
L=H_\infty-H_0
\]

as total latent predictive information restored by history, and

\[
\Delta_t=H_{t+1}-H_t
\]

as the exact information cost of the next minimal repair.

For \(L>0\), define the resolved fraction

\[
F_t=\frac{H_t-H_0}{L}.
\]

Let \(t_{50},t_{90},t_{99}\) be the first horizons with
\(F_t\ge .50,.90,.99\).

The primary asymptote-shape quantity is

\[
A_{90}=\frac{h_*-t_{90}}{h_*},
\]

the fraction of the repair sequence that occurs **after 90% of all ultimately
necessary predictive information is already represented**.

A large \(A_{90}\) means a long thin tail: closure is already close in
information distance, yet additional distinctions keep becoming necessary.

Also record, without thresholding:

- full sequence \(H_t\) and \(\Delta_t\);
- \(h_*\), \(t_{50},t_{90},t_{99}\);
- depth density \(h_*/n\);
- stable entropy density \(H_\infty/n\);
- safe-forgetting reserve \(n-H_\infty\);
- mean repair cost \(L/h_*\);
- last nonzero repair cost;
- number of nonzero repair steps after \(t_{90}\).

These are exact finite-state quantities. Entropy is a coding summary of an
exact partition, not a claim about stochastic source dynamics.

## Frozen predictions and decisions

**P1 — controls.** Rules 0 and 90 should close immediately or nearly
immediately. Failure is an implementation/contract alarm.

**P2 — primary complex-vs-chaotic ordering.** At \(n=10\), both Rules 54 and
110 must have \(A_{90}\) strictly greater than both Rules 30 and 126. If not,
the proposed Class-IV asymptotic-closure signature fails and the unit stops
without width 12.

**P3 — fresh-width survival.** If P2 passes, the same strict ordering must hold
at \(n=12\). If it reverses or ties, stop and record a negative.

**P4 — transport confound.** If P2 and P3 pass but Rule 184 matches or exceeds
the weaker of Rules 54/110 on both \(A_{90}\) and \(h_*/n\) at both widths,
then the result is not Class-IV-specific under this observer. Record that
confound and stop without width 14.

**P5 — stress.** Only if P2-P4 survive, run \(n=14\). The same direction must
persist to justify any later broader program.

No threshold may be tuned after viewing outcomes. In particular, 90% is frozen
before evaluation and may not be replaced by another percentile to rescue the
hypothesis. The 50% and 99% horizons are diagnostics only.

## Interpretation boundary

A positive bounded result would mean only that the frozen 54/110 pair has a
longer thin tail of minimal predictive repair than the frozen chaotic and
transport controls under this observer and finite-size sequence.

It would not establish:

- a definition or classifier of Class IV;
- infinite-line nonclosure;
- computational universality;
- a unique minimal online suffix memory;
- a representation-independent complexity measure.

A negative result is scientifically complete for this formulation. Do not
switch observers, panels, percentiles, or repair metrics inside this unit.

## Planned artifacts

- scripts/experiment_asymptotic_closure.py
- results/asymptotic_closure_20261007.json
- docs/research/2026-10-07-asymptotic-closure.md
