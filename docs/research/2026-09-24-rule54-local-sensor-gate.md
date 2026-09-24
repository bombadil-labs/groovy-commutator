# Local G bit cannot pick a repair site on this route

2026-09-24. Authored by Codex (OpenAI). Reviewed by: none.
**Exact finite-task test of one declared local selector grammar.**

## Decision and method

The [full-field information gate](2026-09-24-rule54-g-sensor-gate.md)
found that Rule-54 G retained every successful action choice on 1,156
injured runs, but required gathering the whole field. We asked whether a
minimal translation-equivariant *site trigger* could turn that information
into the already authorized one-cell hold. The
[frozen protocol](protocols/2026-09-24-rule54-local-sensor-gate.md) reuses
the original 34-cell route, action time and target unchanged. Every site
tests the same predicate; a shared arbiter holds the site only when exactly
one site triggers, otherwise noop. No injury label, route phase, future
state or outcome is given to the controller.

Each family gets its best predicate in its **specified finite menu**:
`G_i=0/1`; `E_i=0/1` or `D_i=0/1`; or equality to one of 32 raw
five-bit neighborhoods. The raw five-bit selector reads the same source
radius two needed to compute `G_i`. A compiled raw five-bit truth table
exactly reproduces either local G predicate, with at most 32 table bits.

| Selector with unique-site arbiter | Best successes / 1,156 | Rescues beyond passive |
| --- | ---: | ---: |
| Noop / best fixed action | 340 | 0 |
| One `G_i` bit value | 340 | 0 |
| One `E_i` or `D_i` bit value | 340 | 0 |
| One five-bit raw neighborhood equality | **374** | **34** |
| Full-field G or raw source, with unrestricted central action table | 408 | 68 |

Prospective P1, that the one-bit G trigger would beat fixed noop,
**failed**. P2 held: the cheaper simple raw pattern beats it. P3 held:
the direct radius-two raw truth table reproduces both G trigger policies
on every trial, independently checked by a scalar implementation. Both
raw patterns 19 and 25 tie at 374; the frozen tie break chooses 19, with
offset order `-2,-1,0,+1,+2` corresponding to `11001`. It flags exactly
one site on 102 trials, rescues 34 passive failures, and harms zero
passive successes. The first rescue holds site 24 of the rotation-zero
trial injured at site 24. No fitted test-domain generalization follows.

After evaluation, we examined *why* the simple G predicates failed:
every decision-time G field has 4–10 ones and 24–30 zeros. Thus neither
bit value uniquely identifies a site for this arbiter on any trial.
That count is a post-evaluation explanation, not a frozen prediction.
It is a limit of a **one-bit trigger**, not proof that a richer local G
neighborhood or a global G controller cannot repair the route. The
central full-G information ceiling still equals 408.

## Cost and portfolio decision

The raw pattern requires five current source reads and one local
five-bit equality test per site. Native `G_i` depends on those same five
source bits and requires three Rule-54 passes in the direct field
construction, of which the first `E(s)` pass can be shared with the
ordinary physical update if available before selecting the held action.
That leaves **two additional passes** plus temporary fields and XORs,
or three passes if sharing is impossible. All candidates pay for the
same unique-address arbitration and held-site delivery. A pre-maintained
G field would require its own initialization, maintenance and storage.
The 32-bit compiled raw-G table is an upper bound on table storage, not
a minimum circuit or a blanket dominance proof when memory and operations
trade off.

This test supplies **no reason to expand to 255 other ECAs**. Its raw
control already obtains half of the available 68 rescues with simpler
local information, while the frozen G trigger obtains none. A cross-rule
repair statistic would additionally need a target, nonzero full-state
action gain and perturbation model chosen independently for every rule;
the Rule-54 target cannot be transplanted and interpreted as each rule's
native phenotype. The earlier Rule-110 proof that G lacks an autonomous
present-only law is about a different task and cannot substitute for a
Rule-110 repair outcome. Keep a Rule-110 feasibility preflight available
**only** when an independent Rule-110 route and intervention reason is
specified. Do not choose a richer grammar or new target to recover a
positive result from this failed prediction. This is a justified stop on
the proposed *discriminator campaign*, not a theorem that no G-based
repair policy exists.

## Reproduction and scope

- Inspected main: `4515a5e43ab329d584b306601dbe4a4e27088eb7`.
- Protocol frozen: `0cacece9ff8d72fa99bf61e6bda57e6f3713ba3f`.
- Runner and independent scalar verifier pinned before evaluation:
  `0a08aa45bb79d61c405bf488bf25b42bbbb5b96f`.
- [Canonical result](../../results/rule54_local_sensor_gate_20260924.json):
  SHA-256 `04374a9ec5b0a5c67ecdea92d2cffde6784cdba0f6d8460c43cb1267afce7970`.
  The earlier action-outcome result stays byte-for-byte unchanged at SHA-256
  `b390b49d3506b5e78e45fbcbd3de710bdcad60b3b0a6d21054e1dc276d166f75`.
- Run `python experiments/rule54_local_sensor_gate_20260924/verify.py
  results/rule54_local_sensor_gate_20260924.json` and
  `python scripts/check_result_integrity.py
  results/rule54_local_sensor_gate_20260924.json`.

The prior independent verifier checked all 40,460 underlying action
outcomes. This unit's scalar verifier separately recomputes local G from
five-bit causal cones, all predicate actions and scores. Neither is
independent peer review. These claims concern a finite, one-shot,
adapted Rule-54 route; they are not persistent glider control, a
classification theorem or a 255-rule census.

**Authorized post-selection closure:** Myk asked for one additional
frozen check of the observed patterns 19 and 25 together. The
[subsequent result](2026-09-24-rule54-two-pattern-closure.md) reaches
the full-state 408/1,156 score with no collision or harm on this
same domain. This does not revise the failed G-bit prediction or
retroactively make pattern selection independent.
