# A prefix can filter rule order, but the selected nonconstant prefix does not erase it

**Status:** exact full-line local-map certificate, plus a bounded decision to
stop. This is a follow-up to the [composition-phase note](2026-09-25-rule-composition-phase.md),
not a new claim about recurrent cycles or an ECA complexity statistic.
Inspected main `bf938190b9c492e8017dd530bdf498d5b02caa4e` (PR #311
merged). Reviewed by: none.

## Question and scope

Fix `B=E_54`, `C=E_110`. Could a first evolution rule `A` remove the
distinctions on which `B` then `C` differs from `C` then `B`? The
[frozen protocol](protocols/2026-09-25-order-image-gate.md) chose the
identity Rule 204, Rules 30, 90 and 54, and constant Rule 0 **before**
evaluation. These are uniform synchronous ECA rules on arbitrary binary
configurations of the two-sided infinite line. Output is the center bit
after *three* updates. No invariant subshift or orbit restriction is
assumed. A line segment's seven source bits determine this output exactly.

The protocol was published at `91f0b73e819a4a8ff3a0a311370ed45c7944d5c8`
before the pinned implementation at
`1a51e22fcbe9cb2abb4d7717a6d013be4670fb32`. The [canonical
result](../../results/order_image_gate_20260925.json) has SHA-256
`af55c1bd4f0dbc08c90b0121e2f3d76319f8297080028277492a67200c7df549`.
It saves both complete 128-bit composed local tables for each prefix, their
XOR, the complete 32-bit pair-defect table, every reachable five-bit
middle word and the first differing source witness. Bit zero denotes the
leftmost site within each patch; a result-table character at offset `p`
corresponds to seven-bit source patch number `p`.

## Exact result

The order defect `K_(54,110)(u)=E_110(E_54(u)) XOR E_54(E_110(u))`
is one at the center of **13 of 32** five-bit intermediate words:
`6, 8, 11, 14, 15, 18, 22, 23, 24, 25, 26, 27, 30`.

| First rule `A` | Reachable five-bit middle words | Defect-positive middle words reachable | Differing seven-bit source patches | First source witness (left to right) |
| --- | ---: | ---: | ---: | --- |
| 204 (identity) | 32 / 32 | 13 / 13 | 52 / 128 | `0011000`, outputs 1 vs 0 |
| 30 | 32 / 32 | 13 / 13 | 52 / 128 | `1010000`, outputs 1 vs 0 |
| 90 | 32 / 32 | 13 / 13 | 52 / 128 | `1110000`, outputs 1 vs 0 |
| 54 | 29 / 32 | 12 / 13 | 43 / 128 | `0001000`, outputs 0 vs 1 |
| 0 (constant) | 1 / 32 | 0 / 13 | 0 / 128 | no witness |

Rule 54's missing middle words are `13, 21, 22`; only `22` is
defect-positive. Thus Rule 54 removes *some* contexts where the order of
54 and 110 can be observed, while leaving 12 other such contexts. The
predeclared Rule 54 question has a partial-filter result, **not** complete
order blindness. Rule 0 makes the two schedules identical only by erasing
every source distinction, so it is a control rather than a useful selective
representation. All explicit predictions for Rules 0, 204, 30 and 90 held.

The equal `52` counts for 204, 30 and 90 have a local explanation: each
five-bit middle word has exactly four seven-bit preimages under those
specific local rules, so 13 defect-positive words give `13 × 4 = 52`
source patches. Identity ignores two exterior bits. Rule 30 and Rule 90
are left-permutive, permitting the five prescribed output bits to be
solved successively from two freely chosen boundary bits. **Local
five-word coverage is not a claim that the global CA is injective or
surjective.** The fractions in the table count local words, not a measured
probability for any chosen distribution of initial configurations.

## Why this is a full-line result

For any prefix `A`, exactly seven source bits can influence the center after
three radius-one steps. The complete table of 128 source words therefore
proves equality at every site for *all* infinite configurations when it is
zero, and any nonzero entry can be embedded in a two-sided infinite
configuration to give a disagreement. In particular the Rule 30 witness
`1010000` proves that the two selected triple compositions differ as
**maps on the full line**, extending the earlier finite-ring *map
difference* conclusion. The earlier unequal periodic-cycle counts remain
finite-ring facts only; a one-step local witness says nothing about
infinite-line recurrence.

The scalar local LUT calculation was independently checked against the
library vectorized ECA update on an 11-cell periodic ring for every source
word and both composed outputs, first with zero exterior bits and then
with one exterior bits. Exterior bits have no path into the center in
three steps. The comparison also verifies at each input that the
post-prefix discrepancy equals the stored pair defect at its middle
five-bit output. Hash registration checks provenance, not the argument.

## What to do next

The exact equality gate is cheap: calculate the pair defect on 32 local
five-words, then compare its nonzero set with the chosen prefix's local
image. For these prefixes, no selective full erasure appeared. The
identity and Rule 0 bound the trivial possibilities; Rules 30/90 preserve
all local order distinctions, Rule 54 removes one of thirteen. No
additional prefixes were selected after evaluation.

Do **not** treat fewer differing source patches as greater fitness,
prediction quality or useful abstraction. Any follow-up needs a task and
a source distribution or invariant family, with a downstream readout and
the directly fused seven-bit CA as baseline. Three ECA evaluations and
any phase or control information are real costs. Without such a consumer,
this exact diagnostic is the result and the line stops here.
