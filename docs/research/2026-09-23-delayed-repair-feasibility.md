# Waiting two steps makes this one-flip repair impossible

2026-09-23. Authored by Codex (OpenAI). Reviewed by: none.
Exact finite Rule-54 result with a separate scalar replay by the same author;
no independent scientific review and no larger-ring or biological claim.

## Why ask this question?

The [target preflight, merged PR #300](https://github.com/bombadil-labs/groovy-commutator/pull/300)
found an invariant eight-state target on the 12-cell periodic Rule-54 ring.
Some of its one-bit injuries return without help, while others do not. We
asked whether this makes **delayed intervention** meaningful before spending
effort finding a compressed view of the state. An observer cannot improve a
task for which even a full-state controller has no useful action.

The [frozen protocol](protocols/delayed-repair-feasibility-20260923.md)
fixed the target to `[273, 546, 1092, 1911, 2184, 3003, 3549, 3822]`
from PR #300, counted each of its 96 outside one-bit injuries once, and
allowed no action until **two** unmodified CA steps had passed. The external
controller could then see all 12 bits and either do nothing or flip one
addressed cell. Success meant membership in the target after two more steps.
This is a one-shot external policy on a chosen finite target.

## Exact comparison

| Controller at step two | Successes among 96 initial injuries |
| --- | ---: |
| Do nothing | 36 |
| Best one globally fixed action (noop) | 36 |
| Best action given all 12 current bits | 36 |

There are 88 distinct decision-time states from the 96 injuries. For each
of the **60 injuries that miss the endpoint passively**, none of the 13
possible actions succeeds. For the remaining 36, noop already succeeds.
Thus every state with a winning action has noop among its winners. Some
initial injuries reach the same decision-time state; identical current
states have identical action sets. The full-state
upper bound offers **zero improvement**, so no coarser observation can help
under these actions and this endpoint.

The frozen P1 consistency check (36 passive successes) held. The three new
predictions failed: P2 expected at least one rescued injury; P3 expected a
rescued injury with a postaction state outside the target; P4 expected a
full-state advantage over the best fixed action. Each failed because there
were no rescued injuries at all. These failures remain in the canonical
result. This does not say that all possible interventions are futile: it
rules out one flip at the specified two-step decision point on this state
domain and four-step endpoint.

The producing implementation checked 96 × 13 = 1,248 action outcomes using
Rule-54 bit arithmetic. A separate scalar implementation checked all 4,096
single-step transitions, target invariance, the 96 injuries and every action
outcome. Both finished below their 30-second caps. Full-state access requires
12 current bits and an externally supplied addressed action; the target has
eight 12-bit states. The comparison charges the same action timing and
one-flip budget to every policy. It measures logical success, not runtime,
energy, a learned policy's construction cost or robustness to new injuries.

## Decision

The preflight's passive-return mixture was a necessary check, not a
sufficient reason to search sensors. This particular delayed repair setting
has no useful action. Park this branch of the maintenance inquiry; do not
change delay, target or rule simply to obtain a positive result. A future
unit needs a separately motivated operation (such as a specified repeating
disturbance or a constraint enforced inside the dynamics), together with
passive and full-state baselines before any representation search.

## Evidence and provenance

- Inspected main: `69c9121c627b15952d57b179a1bc6b0c95ccb29a`.
- Scientific prerequisite: [integrated PR #300](https://github.com/bombadil-labs/groovy-commutator/pull/300),
  result SHA256 `02213ca3dd688ca4c3451751b867f3310a63d65c6866a8f485cf370c00e3b2f1`.
- [Protocol commit](https://github.com/bombadil-labs/groovy-commutator/commit/58ae1451e80b9f5565626f74f31b77cc85adba68) before implementation and evaluation.
- [Implementation commit](https://github.com/bombadil-labs/groovy-commutator/commit/4d1f51681b3708bb52adff94347367fe2f9fbc1a) before evaluation.
- [Canonical result](../../results/delayed_repair_feasibility_20260923.json),
  SHA256 `0f31c5d037550dab35bc09289acccd04457685a6dc3b30cb82521f801b246857`.
- Recheck: `python experiments/delayed_repair_feasibility_20260923/verify.py results/delayed_repair_feasibility_20260923.json`.
  `python scripts/check_result_integrity.py` checks source hashes only.
  [PR #301](https://github.com/bombadil-labs/groovy-commutator/pull/301)
  contains this unit, integrated after PR #300 on which it depends scientifically.
