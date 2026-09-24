# Reference-rule G as a repair-address sensor: frozen information gate

2026-09-24. Authored by Codex (OpenAI). Reviewed by: none.
**Prospective protocol. Freeze this file before implementation and evaluation.**

## Decision

The [published-seed route gate](../2026-09-24-rule54-glider-route-gate.md)
found 68 genuinely delayed rescues by holding one cell, but an oracle given
the original injury address matches the full-state ceiling. Before searching
local G policies, ask whether the **entire** fixed-reference Rule-54 G field
of the decision-time state permits the full-state repair outcome. Failure is
decisive for every policy that reads only that G field or a slice of it.
Success would only permit, not justify, a later costed local comparison.

## Unchanged physical task

Use the canonical `results/rule54_glider_route_gate_20260924.json` unchanged:
34-cell periodic ring, Rule 54, seed `(1000)^4 10 (1110)^4`, its 34 rotations
and 34 one-bit injuries per rotation (1,156 trials). At time two, after two
Rule-54 updates, the available actions are noop or hold one addressed cell
during the next update, followed by five Rule-54 updates. Success means
membership at time eight in the 34 rotations of the clean route's time-eight
state. The saved winning-action sets are the frozen outcomes; reject missing
or altered schema, trial cardinality, width, rule, or result SHA-256.

For current state `s` at time two define `E=E54`, `D(s)=s XOR E(s)`, and
`G(s)=D(E(s)) XOR E(D(s)) = E(s) XOR E(E(s)) XOR E(s XOR E(s))`.
The reference rule is 54 regardless of the action subsequently chosen;
these counterfactual computations do not change the actual state. Only the
current state is observed, with no initial injury site, clean route phase,
history, lookahead, future target-state read or action oracle supplied.

## Observation policies and exact calculation

For each observation `o`, group all domain trials with the same `o` and
choose **one** of the 35 actions for the whole group to maximize its number
of successes; break ties by noop first and then ascending site address. Sum
the maxima across groups. This gives an exact empirical-domain upper bound
for any deterministic policy reading only `o`, with no fitted train/test
generalization claim. Compare three sensors: no observation (one action),
the entire 34-bit current source `s`, and the entire 34-bit `G54(s)`.
Count observed fibers, successful trials, and irreversible loss relative to
the source-full bound. Save a pair of trial identities and winner sets from
one G fiber with conflicting optimal actions if such a witness exists; if a
larger conflicting fiber is required, save the minimal relevant rows. Check
the winning-action sets are consistent for duplicate raw states.

Prospective P1: global G loses at least one of the 408 full-state successes.
P2: regardless of P1, G cannot outperform full raw current state on this
domain (data-processing bound). P1 failure is a real failed prediction, not
grounds for choosing another G definition, seed or endpoint after evaluation.
If G ties the full-state ceiling, the next and only possible continuation is
a separately frozen local address and **total cost** comparison. If it
loses, park G-only sensing for this task; do not scan radii or rules to
retrieve the missing source distinction.

## Resource and interpretation contract

Both full-field sensors require acquisition of all 34 source bits if G is
computed from this state. Direct raw observation requires zero additional
Rule-54 evaluations; G requires three full-ring Rule-54 evaluations per
decision (one each for `E(s)`, `E(E(s))`, `E(s XOR E(s))`), plus XORs and
temporary storage for at least intermediate 34-bit fields. A central
addressed action needs one noop/hold flag and five bits for one of 34
addresses, under either sensor. A full-field policy table can be priced
as one 34-bit key and six-bit action per observed fiber, explicitly only
an uncompressed upper bound, not a minimal circuit size. A 34-cell spatial
field is not 34 independent free input wires at one site: aggregation and
delivery to the held cell are additional nonnegative costs under both
contracts. No runtime or physically distributed policy advantage can be
concluded from information sufficiency alone. An already-maintained G cache
would require separate initialization, update, storage and access costs.

The computation should take under one minute with a 256 MiB process cap.
Do not reuse results of the previous gate as new independent validation of
its target. Preserve its canonical JSON byte for byte. Pin a runner and an
independent G evaluator/checker before evaluating; save a separate JSON
record with source SHA, implementation commit, predictions and evidence.
This is a finite-ring, one-shot observational comparison, not a local CA
controller, a class-IV discriminator, recurring maintenance, or a theorem
for arbitrary configurations.
