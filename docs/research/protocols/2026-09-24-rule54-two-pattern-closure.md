# Two selected raw patterns under one arbiter: frozen closure check

2026-09-24. Authored by Codex (OpenAI). Reviewed by: none.
**Prospective for this follow-up only.** The two patterns were selected
after the preceding evaluation; this is not independent validation.

## Decision and authorization

The [local Rule-54 gate](../2026-09-24-rule54-local-sensor-gate.md) found
that raw five-bit patterns 19 and 25 each rescue 34 of the 68 injuries
recoverable by unrestricted full-state action, with no harmed passive
successes. Myk subsequently asked to test the specifically proposed
`19 OR 25` combination once. This narrow user-authorized follow-up
supersedes the earlier stop instruction **only for this combination**.
No new pattern search, changed target, alternative arbitration or revised
score threshold is authorized by this protocol. Neither outcome revives
a G-specific advantage or a cross-rule discriminator program.

## Frozen physical and policy contracts

Keep the original canonical Rule-54 one-shot repair outcomes exactly:
`results/rule54_glider_route_gate_20260924.json` with SHA-256
`b390b49d3506b5e78e45fbcbd3de710bdcad60b3b0a6d21054e1dc276d166f75`.
The 34-cell periodic seed, 34 rotations × 34 initial one-bit injuries,
two ordinary steps, one addressed held-site update, five ordinary steps
and time-eight rotated clean-route target do not change. No rotation,
injury index, target membership or outcome table enters the selector.
Also pin the selected single-pattern result
`results/rule54_local_sensor_gate_20260924.json` SHA-256
`04374a9ec5b0a5c67ecdea92d2cffde6784cdba0f6d8460c43cb1267afce7970`.
Reject either source if its SHA, schema, rule, width or trial identities
disagree with this contract.

At decision time two, each site reads the five current bits at offsets
`[-2,-1,0,+1,+2]`, encoded with the leftmost bit as the low-order bit.
Emit one flag if and only if that five-bit integer is **19 or 25**.
The very same unique-site arbiter used before holds the sole flagged
site; zero or two-or-more flags cause noop. The flag and action are
translation-equivariant; no pattern priority or injury-address oracle.

Exact evaluation over all 1,156 frozen trials reports success score,
number of unique-trigger trials, rescues beyond noop, passive successes
harmed, cases with both patterns at different sites, and a concrete
trial/address witness for every collision or harm if present. Separate
`19` and `25` policy scores must reproduce the previous result (374 each);
noop must reproduce 340 and the full-state upper bound 408.

**Prospective P1:** `19 OR 25` reaches the 408/1,156 full-state ceiling
with no harmed passive successes. **P2:** on all 68 salvageable
passive failures, the two triggers never fire at distinct sites on the
same trial. A failed prediction remains failed. Even if both hold, this
is an in-domain, post-selected finite controller, not a held-out
phenotype test. If either fails, keep the collision/harm witness and
stop without searching a third pattern or priority convention.

## Costs and evidence

Each site reads five source bits, tests equality to two fixed constants
(10 literal pattern bits in a direct pair of five-bit comparators), and
emits one trigger bit; the arbiter and address delivery are unchanged.
One step of Rule 54 remains required for the physical update, with no
additional G computation, history rail or stored G field. These literal
costs do not establish a globally minimal circuit. The upper bound's
central action table gathers all 34 bits and encodes an addressed hold.
The proposed finite controller has not been shown to work after repeated
disturbances, outside this ring/seed, or on arbitrary Rule-54 trajectories.

Budget under 30 seconds and 256 MiB for the small exact check. Pin a
runner and independent scalar verifier before evaluation; store one
new hash-registered JSON without changing either prior canonical result.
Integrity hashes document provenance, while the independent verifier
must check actions, scores, collisions and recorded witnesses.
