# Protocol: matched predictive history, different Groovy transport

**Status:** frozen before fresh widths 16/18 are evaluated, 2026-10-07.  
**Authored by:** GPT-5.6 Sol (OpenAI). **Reviewed by:** none.

## Why Rule 62 versus Rule 110

An independent Fable census of the block-2-parity predictive-refinement
measure shows that Rule 62 (Class II) nearly shadows Rule 110 (Class IV) in
safe-forgetting reserve and history depth over widths 12--18.

This makes the pair a useful matched control: hold the **amount of required
predictive history** approximately fixed and ask whether that history has a
different relationship to situated change.

The pair was selected after seeing the census. This protocol therefore does
not use the 62/110 compression similarity itself as confirmation evidence.

## Exploratory metric selection

Before this protocol was frozen, widths 12 and 14 were used only to choose a
mechanistically interpretable quantity.

For a source rule \(H\), use the established nonoverlapping block-2 parity
observer \(P\) at cadence \(q=2\). Let \(C_t\) be the exact partition of source
states by observed trajectories through horizon \(t\).

Let the centered Groovy field on the current microstate be

\[
G_H^\circ(X)
=
G_H(X)\oplus H(0)
=
B_H(X,D_HX).
\]

At coarse horizon \(t\), write

\[
X_t=H^{2t}(X),
\qquad
Y_{t+1}=P(H^2X_t).
\]

The exact question at a nonclosed repair step is:

> Does \((C_t(X),G_H^\circ(X_t))\) determine \(Y_{t+1}\)?

Equivalently, whenever two source states have the same current predictive
history label and the same current centered Groovy field, must their next
block-parity observations agree?

On exploratory widths 12 and 14, Rule 110 satisfied this exact factor condition
at every nonzero repair step, while Rule 62 failed it at early repair steps.
Those outcomes motivated the fresh test below and are not scored.

## Information summary

For interpretation, also record

\[
\Delta_t=H(C_{t+1})-H(C_t),
\]

the information cost of the next minimal predictive repair, and

\[
J_t
=
I\!\left(
G_H^\circ(X_t);
Y_{t+1}
\mid C_t
\right).
\]

Then

\[
\gamma_t=J_t/\Delta_t
\]

when \(\Delta_t>0\).

The exact factor condition above is equivalent to \(\gamma_t=1\). Define the
cumulative Groovy-coupled repair fraction

\[
\Gamma
=
\frac{\sum_t J_t}{\sum_t\Delta_t}.
\]

Entropy values are diagnostic summaries of the exact finite partitions; the
factor/witness condition carries the primary result.

## Fresh widths

Evaluate exactly:

1. \(n=16\);
2. \(n=18\), only if the width-16 primary separation passes.

Enumerate every source state. No other rule is scored in the primary test.

## P1 — Rule 110 Groovy sufficiency at width 16

For every nonzero minimal-repair step before closure under Rule 110,

\[
(C_t,G_t^\circ)\to Y_{t+1}
\]

must be a deterministic factor.

## P2 — Rule 62 contrast at width 16

Rule 62 must have at least one nonzero repair step with an exact counterexample:
two source states with equal \(C_t\) labels and equal current \(G^\circ\), but
different next block-parity observations.

If P1 or P2 fails, stop before width 18.

## P3/P4 — fresh replication at width 18

Repeat the same two requirements at width 18:

- Rule 110: Groovy suffices at **every** nonzero repair step;
- Rule 62: Groovy fails to suffice at **at least one** nonzero repair step.

Both must hold.

## Witness contract

For every failed factor step, save the lexicographically first pair of source
states witnessing

\[
C_t(x)=C_t(y),
\qquad
G^\circ(H^{2t}x)=G^\circ(H^{2t}y),
\]

but

\[
P(H^{2(t+1)}x)\ne P(H^{2(t+1)}y).
\]

Also save their current microstates, current dynamical displacements, current
Groovy fields and next observations.

## Interpretation boundary

A pass would establish only a **matched mechanistic separation**:

> Under the same fixed observer, Rule 110's newly necessary predictive
> distinctions are completely readable from the current situated-change field
> \(G^\circ\), while Rule 62 requires some additional historical distinction
> not present in that field.

It would not establish:

- that this property is unique to Class IV;
- that \(G\) is a universal sufficient statistic;
- an infinite-line result;
- a Class-IV classifier or universality theorem.

The exploratory canonical census already shows many rules can have
\(\Gamma=1\) on smaller widths. This experiment is specifically about the
matched 62/110 pair, not prevalence across classes.

## Hard stop

After width 18, stop regardless of outcome. Do not add Rules 54, 94, 73 or any
all-rule census inside this protocol. A broader specificity test would require
a separate decision.

## Planned artifacts

- scripts/experiment_matched_history_transport.py
- results/matched_history_transport_20261007.json
- docs/research/2026-10-07-matched-history-transport.md
