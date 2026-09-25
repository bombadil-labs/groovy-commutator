# When could a rule schedule buy something?

**Status:** exact contract and decision, with a post hoc read of an already
saved local table. No new empirical protocol, rule search or dynamical run.
Inspected main `7e3ee102119f9e0c8757388ee93a6ad8e316e0ae`, after
[PR #312](https://github.com/bombadil-labs/groovy-commutator/pull/312),
and no open PRs or issues. Reviewed by: none.

## The interface that decides the answer

Take three fixed synchronous uniform ECA maps `A`, `B`, `C` on arbitrary
binary configurations of the two-sided 1D line. The open-loop program
repeats them in that order. It starts at phase zero, takes no input between
updates, and exposes one output after every third step. Its epoch map is

```
F = C∘B∘A,             S_(3k) = F^k(S_0)  for every k ≥ 0.
```

This is an equality of *whole configurations for every source and every
epoch*, by definition and induction. `F` is a binary radius-at-most-three
CA because three radius-one dependency cones compose. If the task only
reads those epoch outputs, the schedule and `F` have identical successes,
failures, periodic points and error responses for matched initial states.
No new endpoint-only performance trial can distinguish them. Choosing
30→54→110 versus 30→110→54 chooses **different** maps `F`; the earlier
finite-ring cycle difference says nothing about one schedule outperforming
its *own* fused map.

The [saved 128-entry local tables](../../results/order_image_gate_20260925.json)
make the bound tight for both selected Rule-30 prefixes: their outputs
depend on all seven source positions. For 30→54→110, changing just the
leftmost bit distinguishes patches 12/13 and changing just the rightmost
distinguishes 0/64. For 30→110→54, the corresponding patch pairs are 4/5
and 0/64. These are exact post hoc checks of the saved tables, not a
frozen efficiency experiment. Both fused rules have minimum **symmetric
radius three on the full line**; a smaller symmetric-radius local lookup
cannot produce the same epoch map. This does not prove a minimum table
representation, circuit size or runtime.

## Fair implementations of that same interface

| Realization | State and programming | Local access and updates | What it exposes |
| --- | --- | --- | --- |
| Open-loop schedule | One source bit per site; ordered program of three 8-entry ECA tables; global three-phase clock if updates must be selected over time. | Three radius-one updates per epoch; account for clock/broadcast and intermediate writes. | All three successive rows if requested. |
| Fused epoch rule | One source bit per site; up to 128 entries in a direct radius-three truth table, or any equivalent program, including the original three-table recipe. | One logical radius-three epoch update; a direct lookup reads seven bits per site. Physical realization and latency depend on the machine. | Epoch rows; it does not specify intermediate rows by itself. |
| Fixed multitrack CA | Source bit plus a three-valued phase label at each site (six logical local states, naively three binary storage bits); initialize labels uniformly. | One fixed radius-one local rule steps `(s_i,q_i)` by `E_(r_q)` at that site and increments `q_i mod 3`. Charge phase storage/initialization and intermediate writes. | Exactly the scheduled rows on the synchronized phase subspace. Off that subspace is a separately chosen completion. |

The ordered ECA lookup entries total 24 bits of uncompressed *global
program* data. A direct fused truth table has 128 entries for a genuine
radius-three rule. This is a comparison of two encodings, **not a
24-versus-128 information or hardware lower bound**: a fair fused
implementation may store the same 24-bit recipe and evaluate it internally,
and the schedule also needs phase selection when individual steps matter.
Conversely a direct fused lookup may trade larger wiring/table storage for
fewer serial update rounds. Storage, access radius, communication, update
count and latency cannot be collapsed into one cost without a hardware or
observer contract. The phase can be a shared external clock or replicated
local state; it cannot be charged to one design and waived for its control.

## Decision gate before another experiment

A proposed consumer must specify, **before selecting more rules**:

1. The source family and independent task/output. Is a result read only
   every three updates, or do intermediate rows or mid-epoch interventions
   matter? If epoch-only, behavioral comparisons with `F` terminate in
   exact equality.
2. The allowed physical locality, read/write cadence and clock mechanism.
   If a device only permits radius-one updates, say how the fused map
   would be implemented under the same constraint, and price broadcasts
   and temporary state for both.
3. The comparison score: initialization, per-site source reads, stored
   program bits, selector/phase storage, intermediate writes, latency and
   output access. Include the fused rule *as an optimized implementation
   of the same three-table recipe*, as well as a direct lookup if relevant.
4. A stopping decision: which measured tradeoff would make the schedule
   useful to a real consumer, and what result would park it?

The current project has no downstream consumer requiring intermediate
access, a restricted radius-one device, or an externally specified
maintenance task for these selected rules. The preceding local-image
certificate and cycle witnesses do not supply one. **Decision: park
composition as an application program now.** Preserve it as an exact
mathematical diagnostic and a possible compact search grammar for
higher-radius rules, but do not run another schedule census, prefix search
or Class-IV test to manufacture a use. A concrete consumer can reopen a
bounded cost comparison under this contract.
