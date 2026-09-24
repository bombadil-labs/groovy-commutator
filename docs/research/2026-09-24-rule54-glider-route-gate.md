# A delayed held site can restore a published Rule-54 route

2026-09-24. Authored by Codex (OpenAI). Reviewed by: none.
**Exact finite eligibility result. This is not a G policy or a glider-survival theorem.**

## The question and the independent target

We needed a maintenance target chosen before inspecting candidate Groovy
selectors. [Martínez, Adamatzky and McIntosh (2014), Table 3](https://arxiv.org/html/1410.3096v1)
encode Rule-54 ether phases `e1=1000` and `e2=1110`, a right-moving
junction `e1-10-e2` and a left-moving junction phase `e2-e1`. We froze the
34-cell ring seed `(1000)^4 10 (1110)^4` and the exact endpoint route
*before* writing or running code. The ring includes both junctions. The
paper describes gliders on an infinite line; this finite-ring adaptation
and its eight-step trajectory are our own test and are not independently
certified as two gliders throughout.

The [frozen protocol](protocols/2026-09-24-rule54-glider-route-gate.md)
uses all 34 rotations of the seed, each with one of 34 one-bit injuries
at time zero: **1,156 trials**, all distinct initially. After two ordinary
Rule-54 updates, a controller seeing all 34 current bits can allow the
usual Rule-54 update or **hold one chosen site's bit** for that one update
(local Rule 204 instead of Rule 54). Five more Rule-54 updates follow.
Success is reaching any rotation of the undamaged seed's Rule-54 state at
time eight. There are 34 target rotations. This is strict route recovery
at the endpoint, not a general-purpose glider detector.

## Frozen comparison

| Policy at time two | Successful trials / 1,156 |
| --- | ---: |
| Passive Rule 54, no hold | 340 |
| Best one fixed site or noop across all trials | 340 (noop) |
| Best action chosen from the full decision-time state | **408** |

There are 1,054 distinct decision-time states. **68** initially injured
trials fail passively but have a winning held-site action; each has exactly
one such action. The prospective P1 (some passive failures), P2 (some
delayed rescues) and P3 (full-state advantage over one fixed action) all
held. P0 passed a separate scalar Rule-54 truth-table replay: it reproduced
every domain row and all **1,156 × 35** action outcomes, target rotations,
counts and the first witness. These are exact results under this finite
contract, not confidence estimates.

The first rescue has rotation zero, initial injury at cell 24 and a hold
at cell 24 at time two. Its full nine-state trace is saved in the
[canonical result](../../results/rule54_glider_route_gate_20260924.json).
The policy changes one cell's *update rule* for one tick; it never directly
edits the state to the desired answer.

## Important post-evaluation diagnostic

A separate [saved diagnostic](../../results/rule54_glider_route_gate_20260924_analysis.json)
checks when the 68 rescued runs rejoin the undamaged route. **None** is on
that route just after the held update at time three; **all 68 first rejoin
at time seven** and stay on it at the time-eight endpoint. Thus this
finite gain is a delayed dynamical return, unlike the earlier Rule-54
target that admitted only immediate static correction. This timing check
was performed *after* evaluation; it was not a frozen prediction.

The same diagnostic reveals a powerful simpler explanation: every one of
the 68 rescuing actions holds the **original injury site**. If that site
were supplied as an extra, exogenous oracle, always holding it at time two
would succeed on exactly **408** trials, matching the full-state optimum
without harming any passive success. The injury address was **not**
available to the declared controller. Its reconstruction, storage and
address delivery must be priced in any future comparison. This result
supports a repair *opportunity*, not a special benefit of G or a novel
feedback mechanism. Relative to the clean seed's rotation, the 68 rescued
injuries occur only at sites **24 or 26** (34 each); this concentration is
also a post-evaluation observation, not a frozen target or a basis to retune.

## Costs, limits and decision

The full-state upper bound sees 34 bits at decision time and chooses among
35 actions (at least six address/control bits for an external choice). The
trial computation enumerates all 1,156 sources and 35 actions, with eight
updates per action in the naïve accounting. The finite route has 34 states
at the endpoint. No policy is learned or implemented as an autonomous local
selector; no recurring damage, multiple holds, unlimited persistence,
unbounded ring or Class-IV advantage was tested. A global addressed hold
is a generous full-information feasibility bound, not itself an
uncoordinated local CA controller.

This passes the H3 **full-state feasibility gate**, but the injury-site
oracle saturates its reward. The next decision is narrow: can a declared
causal G sensor choose the same holds with less *total* access, storage and
computation than raw local sensing of the damaged source, while also
comparing with the known-injury-site oracle? First freeze that sensor and
the local address-coordination rule. If simple raw sensing is sufficient
at equal or lower cost, park the G-feedback advantage claim. Do not expand
the seed or outcome window after seeing this positive result.

## Evidence and reproduction

- Main inspected: `40e559ea80d0ca1ef76e8cfce2e2652b9d885f97`.
- Protocol frozen: `a7292eb975d0bc9c89853569abf737aa80622e3d`.
- Runner and independent scalar verifier pinned: `88584bf5bb2bdf8f285abc2037fe25d5ce67cd55`.
- Original one-shot [canonical JSON](../../results/rule54_glider_route_gate_20260924.json):
  SHA-256 `b390b49d3506b5e78e45fbcbd3de710bdcad60b3b0a6d21054e1dc276d166f75`.
- Run `python experiments/rule54_glider_route_gate_20260924/verify.py results/rule54_glider_route_gate_20260924.json`.
- Run `python experiments/rule54_glider_route_gate_20260924/analyze.py results/rule54_glider_route_gate_20260924.json /tmp/rule54-route-analysis.json`
  to reproduce the explicitly post-evaluation diagnostic. No canonical
  result bytes were changed for it. Separate implementations by the same
  author and green CI are verification, not independent scientific review.
