# One local trigger and one addressed hold: frozen Rule-54 comparison

2026-09-24. Authored by Codex (OpenAI). Reviewed by: none.
**Freeze before implementation/evaluation.**

## Why this gate

The [full-field G information gate](../2026-09-24-rule54-g-sensor-gate.md)
ties full-state access on the original 1,156-trial delayed-repair task, but
it does not implement a local controller or show a G-specific advantage.
Test one transparent translation-equivariant local-address grammar first.
If it cannot beat fixed noop, or a matched raw implementation achieves at
least its score with an adequate total-cost contract, stop the proposed
G-specific repair discriminator here; no Rule-110 adaptation or ECA sweep
is justified by this observation alone. A positive result is not a Class-IV
classifier; Rule 110 requires its own independent action-feasibility target.

## Physical contract and grammar

Reuse without alteration the canonical `results/rule54_glider_route_gate_20260924.json`
(SHA-256 `b390b49d3506b5e78e45fbcbd3de710bdcad60b3b0a6d21054e1dc276d166f75`):
34-cell periodic Rule 54, all 34 rotations of the prior seed, all 34
one-bit injuries each, decision at time two, noop or hold one addressed
site during the time-two-to-three update, target membership at time eight.
The saved 35 action outcomes per trial are the outcome oracle for scoring
only, never controller input. Reject a mismatched source SHA, schema or
domain cardinality. No clean route phase, injury address, future state,
history or per-trial adapted program may enter the sensor.

Let `s` be the current time-two state, `E=E54`, `D(s)=s XOR E(s)` and
`G(s)=E(s) XOR E(E(s)) XOR E(s XOR E(s))`, all computed with the reference
Rule 54 *before* choosing the hold. At each site `i` use the same Boolean
trigger from one of these frozen grammars:

- `G_i=0` or `G_i=1` (plus never trigger);
- `E_i=0` or `E_i=1`, and `D_i=0` or `D_i=1` (one-pass controls);
- one exact raw five-bit pattern `s[i-2..i+2]=p`, for each of 32 patterns,
  plus never trigger;
- compile each of the two G-bit predicates directly as a 32-entry raw
  five-bit truth table (two *specified* controls, no predicate search).

Every cell emits one trigger flag. The shared arbiter selects the unique
triggered site's address and holds it; if zero or multiple sites trigger,
it chooses noop. The same arbiter and physical hold operation are used by
all arms. Each grammar is optimized over its finite stated menu on *all*
1,156 cases; ties prefer never trigger then lower bit/pattern. Also report
the best fixed score and the full-state ceiling from the source result,
trigger uniqueness frequency, held-action wins and losses versus noop,
the best policy's gain relative to 340, and one explicit trial witness for
each policy score that differs from fixed. No training/generalization claim.

Prospective P1: the best single-site G-bit trigger rescues at least one
additional case beyond the best fixed action. P2: a one-pass E or D trigger,
or a single raw five-bit equality, matches or beats G's best score. P3:
the compiled raw-G truth table matches each G trigger's actions exactly
for every trial (algebraic calibration). Preserve failed predictions.

## Cost and stopping rule

Every `G_i` has raw spatial radius at most two. Its compiled direct
five-bit truth table therefore reads the *same* source footprint as native
G and needs one local lookup per site, with at most 32 stored output bits.
Native G may reuse the native `E(s)` update, but it still needs `E(E(s))`
and `E(s XOR E(s))`, two additional full-ring passes, XORs, scheduling
before the hold, and intermediate storage or equivalent recomputation.
Charge three E passes if the ordinary update cannot be reused. E and D
controls each need the existing E pass and at most radius-one source
reads; raw equality needs five raw reads and a five-bit comparison at each
site. All use the same one-flag-per-cell address arbitration, whose
aggregation and delivery are nonzero physical costs. The native source
rule's eight-bit table is shared; a direct compiled 32-bit G table is an
uncompressed upper bound, not a proven minimal circuit. An already
maintained G field needs initialization, one-step maintenance, storage
and access; none is free under this contract. If table bits and update
operations trade off, record that trade rather than asserting dominance.

Under the fixed single-site grammar, if G has no advantage over the
cheaper one-pass or simple raw controls, stop the candidate. If G has a
score advantage over those controls, its compiled raw equivalent still
sets the *same-footprint* performance floor: continue only if a concrete
hardware/memory contract demonstrates a lower **total** cost for native
G. Do not expand the trigger grammar, change the intervention, choose new
seed/ring/endpoint or sweep 255 other rules post hoc to save the hypothesis.
The computation is an exact bounded evaluation expected under 60 seconds
and 256 MiB. Pin runner and an independent scalar sensor/action verifier
before evaluating; save result and source hashes separately from the
unchanged prior canonical JSON.
