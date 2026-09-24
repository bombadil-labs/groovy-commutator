# A one-step Groovy observer invents a cycle

2026-09-24. Authored by Codex (OpenAI). Reviewed by: none.
**Status: completed exact six-cell finite-ring test; no feedback policy tested.**

## Question and frozen test

Could the one-step transition graph of the original Rule-30 Groovy field
report a repeating observation that no actual Rule-30 trajectory repeats?
We [froze the question, bounds and predictions](protocols/observer-orbit-preflight-20260924.md)
at commit `dd5abe650aeb2b11c5cc889dc510e2e94cf73a59`, pinned the
[implementation](../../experiments/observer_orbit_preflight_20260924/run.py)
at `3a466968113fd342e5b45c032d682239b75d0aa1`, and then enumerated
all 64 states of one periodic six-cell ring. The one-step graph has one
boolean edge `O(s) -> O(E(s))` for each distinct observed transition,
including edges from transient source states. `C_k` counts rooted closed
walks of length `k` in that graph; `R_k` counts distinct periodic observed
words realized forever by an actual source cycle. We tested `k=1..6`.

| Observer | Graph vertices / edges | `C_1..C_6` | `R_1..R_6` | `C-R` |
| --- | ---: | --- | --- | --- |
| Original whole-field `G(s)` | 37 / 58 | 10, 16, 28, 40, 40, 70 | 1, 1, 1, 1, 1, 1 | 9, 15, 27, 39, 39, 69 |
| Valid `G` history `(G(s), G(E(s)), G(E²(s)))` | 58 / 58 | 1, 1, 1, 1, 1, 1 | 1, 1, 1, 1, 1, 1 | 0 throughout |
| Source identity `O(s)=s` | 64 / 64 | 3, 3, 3, 3, 3, 3 | 3, 3, 3, 3, 3, 3 | 0 throughout |

The source has three fixed-point cycles (`0`, `21`, `42`) and 61 transient
states. All its recurrent source states have `G=0`. The smallest primitive
phantom word is the one-symbol cycle `G=9`. Source `s=10` witnesses the
graph edge `9 -> 9`: the actual source evolves `10 -> 27 -> 9 -> 63 -> 0`,
while its observed Groovy values start `9 -> 9 -> 45 -> 0 -> 0`.
The observer graph can repeat the first edge by silently switching its
hidden source witness each time. No single source can stay at `G=9`.
The exact original-source table, every graph edge and source cycle, the
first witness and all predictions are in the
[canonical result](../../results/observer_orbit_preflight_20260924.json).

The prospective prediction P1 held. The prior-result history calibration
P2 and identity implementation control P3 held. The valid three-row history
is available after **two source updates and three whole-field G reads**;
it is not a free time-zero sensor or a cheaper representation. The result
charges 64 source states and at most six graph powers; it measures neither
controller cost nor an advantage over another observer. The independent
[scalar verifier](../../experiments/observer_orbit_preflight_20260924/verify.py)
recomputes Rule 30 using its truth table, G, the source cycles, graph matrix
powers and witnesses from the saved record. Run it with
`python experiments/observer_orbit_preflight_20260924/verify.py results/observer_orbit_preflight_20260924.json`.

## What follows

This establishes a particular finite graph overcount, not a full-line
theorem, a Class-IV test, quantum uncertainty or useful feedback. The
zeta function merely packages these orbit counts. No selector, rule-switching
policy, mobile-structure target, resource comparison or prime-related claim
was tested. The [program](2026-09-24-observer-orbit-program.md) retains
H3 as contingent: a follow-up first needs an independently meaningful target
and a fully priced causal controller versus a clocked/static baseline. Do
not enlarge ring size or search rule schedules merely to amplify this result.

## Reproduction and provenance

The canonical JSON was written once after the two freeze commits; its
SHA-256 is `189a60e6c37e43b7bb12c6e7bdc242cf424ba28ab9d4a0ce4d43109593687d6a`.
The [separate provenance seal](../../results/observer_orbit_preflight_20260924_seal.json)
registers that unchanged result and the frozen protocol, runner and verifier
in the fast integrity check. Run the independent verifier above and
`python scripts/check_result_integrity.py results/observer_orbit_preflight_20260924_seal.json`.
The verifier is a separate implementation by the same author, not an
independent peer review. The runner's 30-second alarm and 256 MiB address
space cap were never approached by the bounded enumeration.
