# A damaged Rule-54 pattern can sometimes return on its own

2026-09-23. Authored by Codex (OpenAI). Reviewed by: none.
This is an exact result on a finite periodic ring, independently audited with
the repository's scalar CA transition implementation. It does not establish
self-repair, purpose or a useful controller.

## Question and choice

Our earlier 12-cell Rule-54 stripe target never admitted a trajectory back
from outside. That made its four-step repair task static correction. We asked a
smaller question before searching for another observation: **does the same
one-bit injury setting contain any invariant, nonconstant target with both
spontaneous early returns and injuries still outside at step four?** A negative
answer would park this setting; a positive answer would supply an eligible
target for a separately specified task. This exact preflight outranked another
encoder search because return dynamics are a prerequisite for the proposed
delayed-repair interpretation.

The [frozen protocol](protocols/return-target-eligibility-20260923.md)
defined targets as spatial-rotation closures of global Rule-54 cycles of
length at least two, on a periodic 12-cell ring. It excluded uniform states
and considered all distinct one-bit injuries outside each target. The four-step
passive return test has no intervention or sensor; we also classified later
returns and trajectories that never return on this finite graph.

## Exact result

There are **seven** targets in the frozen family. Five have at least one
injury that returns within four steps and at least one still outside then.
The smallest eligible target has eight states, including binary
`100010001000` in cell-index order, and generating temporal period four.
Its states as integer-encoded cell bits are
`[273, 546, 1092, 1911, 2184, 3003, 3549, 3822]`.

| Target | Outside one-bit injuries | Back in target by step 4 | First return after step 4 | Never returns |
| --- | ---: | ---: | ---: | ---: |
| Old four-phase stripe | 48 | 0 | 0 | 48 |
| Selected eight-state target | 96 | 36 | 48 | 12 |

For a concrete witness, state 17 first returns to the selected target at
step two. State 275 first returns only at step ten. The 12 injuries counted in
the last column have no route to the target under repeated deterministic
Rule-54 updates. The protocol's P1 old-target check, P2 existence of an early
return, and P3 mixed-outcome target all passed. Selecting the smallest
eligible target makes it reproducible; its size is not a claim of natural
organization or optimality.

The producing script enumerates all 4,096 transitions once, extracts cycles,
closes them under rotation, and computes first-hit distances through reverse
graph search. A separate scalar implementation rechecks every transition,
independently extracts the complete target family and follows each injury
forward until it returns or repeats. The latter agrees on all seven family
rows, not only the selected example. Both runs completed within the 30-second
caps. These are tiny finite enumerations; we measured no physical repair,
sensor cost, computation advantage or infinite-lattice behavior.

## What changes next

The static-target obstruction in the earlier study is specific to its stripe
target, not to every target on this ring. A future maintenance question can
use the selected target, but must first state **whose intervention**, which
states are sensed, the available actions, their timing and cost, and what
counts as a gain over passive return and full-state access. A four-step
membership endpoint alone must not count naturally returning cases as a
controller's achievement. This preflight alone does not justify another
representation search.

## Reproduction and provenance

- Inspected main: `69c9121c627b15952d57b179a1bc6b0c95ccb29a`.
- [Protocol commit](https://github.com/bombadil-labs/groovy-commutator/commit/b44a27ccfda26cb75421649512e27ad1e222cef5) before implementation and evaluation.
- [Implementation commit](https://github.com/bombadil-labs/groovy-commutator/commit/fd2c76ebe083636a8779a0c1e1b3e2085e85ddbe) before evaluation.
- [Canonical result](../../results/return_target_20260923.json), SHA256 `02213ca3dd688ca4c3451751b867f3310a63d65c6866a8f485cf370c00e3b2f1`.
- `python experiments/return_target_20260923/verify.py results/return_target_20260923.json`
  independently audits the complete result; `python scripts/check_result_integrity.py`
  checks source hashes only. [Draft PR #300](https://github.com/bombadil-labs/groovy-commutator/pull/300)
  holds this gathering unit pending Myk's merge direction.
