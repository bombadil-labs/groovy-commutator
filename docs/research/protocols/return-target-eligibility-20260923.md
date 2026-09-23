# Can one-bit damage return to a Rule-54 target on its own?

2026-09-23. Authored by Codex (OpenAI). Reviewed by: none.
Protocol frozen against main `69c9121c627b15952d57b179a1bc6b0c95ccb29a`
before writing the search implementation or evaluating its outcomes.

## Decision

The prior prediction/repair target has no incoming transitions. Before
another observer search, check whether the same small Rule-54 setting offers
even one nontrivial target where damaged states can return passively, while
other damages do not return within the stated horizon. If one exists, record
one reproducibly selected candidate for a separately specified intervention
contract. If none exists, stop this one-bit, 12-cell, four-step line. Do not
redesign the target after seeing the outcome or launch a representation search.
The comparison baseline is the four rotations of `(0011)^3`, whose outside
states were previously shown never to enter its target set.

## Fixed finite contract

- Dynamics: synchronous elementary Rule 54 on all 4,096 binary states of a
  periodic 12-cell ring, bit `i` denoting physical cell `i`.
- Candidate targets: enumerate all directed cycles of the global transition
  map having temporal period at least two. For each cycle, take the union of
  its states under all 12 spatial rotations. Deduplicate equal unions; retain
  only proper subsets of the full state space that contain no uniform state.
  This defines the entire fixed candidate family. Every target is invariant.
- Injury domain for target `V`: unique states outside `V` differing in exactly
  one bit from *some* state in `V`, with neither the original phase nor the
  injury site supplied as an observation. No action is applied in this check.
- Return time: the first positive number of CA steps after injury at which a
  state belongs to `V`. Classify a state as early if it returns within four
  steps; separately distinguish returns after four from states that never
  return under the deterministic finite map.
- Eligibility: a nonempty injury domain with both an early return and a state
  that has not returned by step four. This is only a prerequisite for a
  potentially nontrivial delayed repair task, not evidence of controllability,
  self-maintenance, autonomy or an efficient representation.
- Deterministic selection among eligible targets: smallest number of target
  states, then smallest generating temporal period, then lexicographically
  sorted list of target state integers. The ordering chooses a compact example,
  not an optimum for biological or computational usefulness.

Enumerate every state transition once, all cycles, their rotation closures and
the one-bit boundary; report family counts and return-time class counts.
Record the selected target and its earliest-return witnesses, including a
nonreturn-by-four witness, if it exists. Audit the complete global transition
table with `groovy.ca.apply_rule_int`, recompute the target invariance and
injury classification independently of the enumeration algorithm. No
stochastic sampling, external solver, larger ring, other rule, observer grammar,
intervention policy or runtime-speed comparison is in scope. Bound both
evaluation and audit to 30 seconds on this fixed 4,096-state space. If either
exceeds the cap, report a resource limit, not a negative mathematical result.

## Predictions before evaluation

- P1: the old stripe target has no one-bit outside injury returning within
  four steps. This is a baseline consistency prediction from prior evidence.
- P2: at least one candidate target has an outside one-bit injury returning
  within four steps.
- P3: at least one candidate target is eligible under the mixed-outcome
  definition above.

Preserve these keys and failed predictions. A passing exact finite audit
establishes only the stated 12-cell Rule-54 facts; it says nothing general
about larger rings, infinite lines or naturally chosen organizations.
