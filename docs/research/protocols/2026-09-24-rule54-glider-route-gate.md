# Frozen gate: can a full-state rule switch repair a published glider route?

2026-09-24. Authored by Codex (OpenAI). Reviewed by: none.
Freeze this protocol on a gathering branch **before implementation or
evaluation**. Preserve failures. One seed, ring width, horizon and action
set; do not retune after seeing outcomes.

## Why this target

Martínez, Adamatzky and McIntosh, [*Complete Characterization of Structure
of Rule 54*](https://arxiv.org/html/1410.3096v1), Table 3, specify ether
words `e1=1000`, `e2=1110`, a right-moving junction `e1-10-e2` and a
left-moving junction phase `e2-e1`. These are published independently of G.
On a periodic ring a transition from e1 to e2 also needs a return junction.
Use one canonical configuration comprising both:

`S = (1000)^4 10 (1110)^4` (34 cells, leftmost character is cell zero).

The cited constructions concern infinite-line glider phases. This finite
ring and exact phase layout are *our* test adaptation; do not label its
whole trajectory a verified two-glider solution merely from Table 3. The
task is exact return to the undamaged finite-ring **route** at the endpoint,
up to spatial rotation. It is a deliberately strict trajectory-preservation
proxy, not a general glider detector or a Class-IV test.

## Exact domain, actions and success

Synchronous Rule 54 with radius one, periodic 34-cell boundary and update
`E_54`. Cell indices increase left to right in the displayed word; rotations
are cyclic shifts in that order. Source trials are all 34 spatial rotations
of `S`, each injured at one of the 34 addressed cells **at time zero**:
1,156 `(rotation, injury-site)` trials, including any duplicate physical
configurations but retaining their trial multiplicities. All trials carry
the same exogenous goal; the hidden original rotation/injury index is not
given to the controller. The clean endpoint `c8=E_54^8(S)` is computed
using only Rule 54, and the target `T8` is all rotations of `c8`. Count
distinct target states as an audit. No trial outcome changes this target.

Evolve each injury through two ordinary Rule-54 updates to `s2`. At time
two allow one action: `noop`, or at one site `i` **hold** the current bit
instead of using Rule 54 for the single transition `s2 -> s3`. Formally,
`y=E_54(s2)` and a hold replaces only `y[i]` by `s2[i]`. Thereafter use
ordinary Rule 54 for five more updates to `s8`. A hold that does not change
`y[i]` is still counted as an addressed action. Success means `s8 in T8`.
No action before time two, no second action, no rule switch anywhere else.
The full-state upper bound sees all 34 bits of `s2` and may choose among
35 possible actions. Compare it with passive/noop and the best single fixed
action chosen once for all trials; fixed-action baselines pay the same
single intervention opportunity. This is a spatially addressed,
single-site choice between Rule 54 and identity 204, not a global rule swap.

Count passive successes; trials with any winning action; and the subset
rescued despite passive failure. Record the best fixed action and its
successes, the full-state upper-bound successes, distinct decision-time
states, collision of distinct action sets on the same state if any, and the
lexicographically first rescued trial with its action and full path. Record
source strings, transitions and outcomes sufficient for independent replay.
The full-state optimum is an upper bound on any coarser sensor under these
same actions; a positive result does **not** establish a realizable local
G-policy, nor a fair comparison with global address signaling.

## Frozen predictions and stop

- P0 (consistency): all 1,156 trials, 35 actions, shifts and target
  membership reproduce using a second scalar Rule-54 implementation.
- P1 (prospective): at least one one-bit injury misses `T8` passively.
- P2 (prospective): at least one passively failing injury is rescued by
  the held-site action at time two.
- P3 (prospective): the full-state optimum has more successes than the
  best globally fixed action.

If P0 fails, withhold interpretation until the contract and code agree.
If P1, P2 or P3 fails, report the exact negative and park this case for H3.
If they hold, *only then* consider freezing a separate, costed sensor and
repeated-disturbance protocol. Do not change seed, ring length, action,
delay or endpoint to force a rescue. One-shot return does not establish
ongoing maintenance or glider survival at every intermediate step.

## Execution and cost ceiling

Write the protocol to git before coding; commit runner and separately
implemented verifier before running. Run once to a new result JSON with
implementation SHA pinned; never overwrite. Limit source evaluation to
1,156 trials × 35 actions × 8 transitions and signal timeout 60 seconds,
memory 256 MiB. The verifier independently checks all action outcomes,
the domain and the witness. Keep these small checks off expensive Actions.
The control access cost is at most 34 state bits plus one 6-bit address at
the decision, two prior updates, one held transition, five later updates;
offline construction of the full-state policy and delivery of the address
are not free. A subsequent G-based policy must price G acquisition, state
and rule tables, controller memory and local access at the same cadence.
