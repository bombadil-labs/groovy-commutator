# Two raw local patterns close this one-shot repair task

2026-09-24. Authored by Codex (OpenAI). Reviewed by: none.
**Exact finite-domain, post-selected controller. No G-specific advantage.**

## Why this was a legitimate final check

The [single-pattern gate](2026-09-24-rule54-local-sensor-gate.md)
found two raw five-bit neighborhoods, 19 and 25, that each rescued 34
injuries without harming passive successes. Myk then explicitly asked
to test their OR together. Their selection followed the earlier
evaluation, so this is a narrow **post-selection follow-up**, not a blind
prediction, independent validation or a reopened search. The prior stop
on richer pattern searches remains in force.

We [froze the OR protocol](protocols/2026-09-24-rule54-two-pattern-closure.md)
before implementing or testing it. On the original 34-cell Rule-54
route, each site at time two reads its raw bits at offsets -2 through
+2 and flags exactly when the five-bit pattern is 19 (`11001`) or 25
(`10011`) in left-to-right order. The same existing arbiter holds a
site for the next update only if exactly one flag was emitted; otherwise
the CA performs the ordinary update. No injury address, clean phase,
future state or G computation is supplied. The 1,156 trials, action
timing, target and 35 available outcomes per trial are unchanged.

| Frozen policy | Successful trials / 1,156 | Extra rescues over passive | Harms to passive successes |
| --- | ---: | ---: | ---: |
| Noop / best fixed | 340 | 0 | 0 |
| Raw 19 alone | 374 | 34 | 0 |
| Raw 25 alone | 374 | 34 | 0 |
| **Raw 19 OR 25, unique-site arbiter** | **408** | **68** | **0** |
| Full-state action ceiling | 408 | 68 | 0 |

Across all 1,156 trials the two patterns **never flag on the same
trial**, so the combined policy has no competing-site cases. It holds
a site in 204 trials; 68 are additional rescues, and the rest preserve
passive successes. Prospective *within this post-selected follow-up*,
P1 (match the ceiling without harm) and P2 (no competing flags on the
68 salvageable passive failures) both held. All 68 rescues were already
shown to hold the originally injured site; the controller infers that
address from current raw local bits rather than receiving it.

The independent scalar verifier checks the selected flags and replays
the physical Rule-54 hold and five subsequent updates for every one of
the three new policies on each trial. It reproduces the prior single
pattern scores, the 408 ceiling, the absence of collisions and harms,
and all recorded rescues. The canonical source bytes are preserved.

## What this closes and what it leaves open

This gives an explicit, translation-equivariant **local detector plus
shared address arbiter** that saturates the full-state reward on the
selected finite route. Each site needs five current raw bits, two
five-bit equality tests, and one emitted flag. The same centralized
unique-address aggregation and address delivery from the prior policy
contract is still required, so this is not an uncoordinated local CA
rule. There is no extra G evaluation, G storage or observer history.
The ten literal pattern bits and two tests describe this implementation,
not a minimal circuit certificate.

The earlier fact that the *whole* Rule-54 G field is task-sufficient
remains true, but now a direct raw local controller also reaches 408
under the same physical intervention. That removes any proposed
G-specific gain for this **particular one-shot task**. It does not
prove that G never helps another task or that this controller tolerates
repeated injuries, works on larger rings, or follows an infinite-line
glider. A broad ECA sweep still lacks independent, comparable native
maintenance targets and positive action-feasibility gates. **Stop this
repair benchmark here.** A future maintenance question should select
a disturbance process and target independently, before choosing a sensor.

## Provenance

- Inspected main: `cd9f2bccdd53fa744c434745235d4186b9d44216`.
- Frozen follow-up protocol: `66d2acca21667f48472bb50b9942a8f074469c78`.
- Pinned runner and independent scalar verifier:
  `a52a7ecc3d51a13c366015d78fdb74e4ea185b10`, before evaluation.
- [Canonical result](../../results/rule54_two_pattern_closure_20260924.json):
  SHA-256 `88f948fe3afcc919355692fbebec5b7866ec665830504a6b686bbad1d2aeaa97`.
  It records the exact prior result hashes and full per-trial rescue list.
- [Gathering PR #310](https://github.com/bombadil-labs/groovy-commutator/pull/310).
- Run `python experiments/rule54_two_pattern_closure_20260924/verify.py
  results/rule54_two_pattern_closure_20260924.json` and
  `python scripts/check_result_integrity.py
  results/rule54_two_pattern_closure_20260924.json`.

The independent replay is a separate implementation by the same
author, not peer review. Our seed is a finite-ring adaptation inspired
by published Rule-54 glider encodings, not a verified persistent
two-glider trajectory.
