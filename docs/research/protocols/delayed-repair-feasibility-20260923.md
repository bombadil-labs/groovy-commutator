# Does delayed one-flip control improve passive return?

2026-09-23. Authored by Codex (OpenAI). Reviewed by: none.
Frozen against main `69c9121c627b15952d57b179a1bc6b0c95ccb29a` and
the separately published, still-draft [target preflight PR #300](https://github.com/bombadil-labs/groovy-commutator/pull/300),
head `f5885cf00fd246c9ff224b98ecf9ecc3203c0a7d`.
Its canonical result SHA256 is
`02213ca3dd688ca4c3451751b867f3310a63d65c6866a8f485cf370c00e3b2f1`.
The target and its passive 36/96 return count are **prior evidence**, not
fresh predictions. This branch starts from main and depends scientifically
on PR #300; merge that prerequisite before this unit if both are accepted.

## Decision

Target eligibility does not establish that an intervention has any value.
Before searching for a compressed observer, ask whether an external controller
with the *whole current state* can improve membership in the selected target
after an obligatory two-step delay. Compare doing nothing, one fixed action,
the full-state policy and static correction at the action time. A negative
full-state gain stops this controller line. A gain that only maps immediately
into the target is static correction, not dynamical assistance. A positive
full-state gain beyond fixed action and static correction permits a separately
specified observer question but does not mandate one.

## Frozen contract and exhaustive check

- Synchronous Rule 54 on a periodic binary ring of length 12, integer bit `i`
  = cell `i`. The fixed target is exactly the eight integers
  `[273, 546, 1092, 1911, 2184, 3003, 3549, 3822]` from PR #300.
- Initial source domain: all *unique* states outside this target at Hamming
  distance one from any target state; the prior result counts 96. Weight each
  distinct source once, regardless of how many parent phases/sites produce it.
- From each source `s`, run two unmodified steps to `y = E²(s)`. At that
  instant the external controller may observe all 12 current bits (or use no
  observation). Choose exactly one action: noop or flip one of the 12 addressed
  cells at `y`. Then run two more Rule-54 steps. Success is target membership
  at that four-step endpoint. No retry, memory, costs of a learned controller,
  intermediate injury, or endogenous goal is assumed.
- Exhaust all 96 sources and 13 actions. Report passive noop successes, the
  best *one globally fixed action* across sources (lowest action index on a
  tie, with noop indexed first), and the full-state policy's achievable
  successes (choose lowest successful action index per observed `y`). Count
  which initially passive-failing sources can be rescued, how many distinct
  decision-time `y` states there are, and how many successful interventions
  land in the target immediately versus land outside and enter it within two
  steps. Give a concrete witness for each relevant strict gain. This is
  logical resource accounting, not a runtime speed claim.

Check target invariance, exactly 96 outside injuries and prior passive 36/96
before classifying the intervention. Compute the graph with an explicit local
Rule-54 implementation, then audit every cell transition and action outcome
using `groovy.ca.apply_rule_int` in a separate script. Bound evaluation and
audit to 30 seconds each. If a check or time cap fails, report invalid or
resource-limited results, never a mathematical negative. No encoder search,
new target selection, other horizon, rule, ring or action grammar follows from
this protocol.

## Predictions frozen before evaluation

- P1 (prior consistency): passive noop succeeds for 36 of 96 sources.
- P2 (uncertain): a full-state decision at step two improves on passive noop
  for at least one source.
- P3 (uncertain): at least one *rescued* passive-failing source has a successful
  flip whose immediate postaction state is outside the target. This witnesses
  a real subsequent return, not just immediate static correction.
- P4 (uncertain): a full-state decision succeeds for more sources than the
  best one globally fixed action under this exact uniform source accounting.

Record all four outcomes even if P2 fails. The finite result cannot establish
spontaneous agency, natural purpose, optimal observation or larger-ring facts.
