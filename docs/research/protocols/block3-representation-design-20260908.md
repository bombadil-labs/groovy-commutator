# Protocol: block-3 constructive representation design — 2026-09-08

**Status:** frozen before block-3 evaluation.  
**Branch:** `research/block3-representation-design-20260908`.  
**Dependency:** Research027 on `main`.

## Question

Research027 found that a greedy fixed-target Shannon-information gradient reaches the globally minimum-information closure repair in all 1,590 nonclosed binary-target cases on the complete two-cell local partition lattice.

The next question is whether that result survives a representation space large enough to contain genuine search structure:

> **At block size three, does the local closure-defect gradient still find globally cheapest exact repairs, and what lattice geometry explains success or failure?**

The primary preregistered falsification target is that the 100% greedy-optimal result will **not** survive unchanged at block size three. Retain the result if it does.

## Fine local state and binary targets

A three-cell block has eight fine patterns, coded `0..7` in the repository's little-endian convention. A binary target is an unordered bipartition

\[
T=A\mid B
\]

of those eight patterns. Output complementation is only a macro-symbol relabeling, so evaluate the 127 canonical nonconstant bipartitions once.

Canonical target counts by class balance are:

| balance | canonical targets | exact refinement-interval size |
| --- | ---: | ---: |
| 1 / 7 | 8 | `B_1 B_7 = 877` |
| 2 / 6 | 28 | `B_2 B_6 = 406` |
| 3 / 5 | 56 | `B_3 B_5 = 260` |
| 4 / 4 | 35 | `B_4 B_4 = 225` |

Here `B_k` is the Bell number. The factorization follows because an encoder refining `T` independently partitions `A` and `B`:

\[
[T,\mathrm{id}]\cong \Pi(A)\times\Pi(B).
\]

Thus the full eight-pattern partition lattice has `B_8=4140` nodes, but the exact repair interval for a fixed binary target has at most 877 nodes.

## Finite system

Use all 256 elementary cellular automata on the periodic ring `n=12`, so four nonoverlapping three-cell blocks tile the ring exactly. Use matched cadence

\[
q=3.
\]

For each fine rule and target `T`, compute the complete stable target-future partition

\[
C_\infty^T
\]

under `T(E^{3t}(S))` from the uniform ensemble over all `2^12` microstates.

All claims are exact for this finite periodic system and declared representation family.

## Fixed-target repair objective

For any local encoder partition `Z` refining `T`, define

\[
W_T(Z)=H(C_\infty^T\mid Z(S))
\]

and added present information

\[
A_T(Z)=H(Z(S))-H(T(S)).
\]

`W_T(T)` is the target's unresolved future repertoire and `W_T(identity)=0`.

A refinement cover `Z -> Z'` splits exactly one current local encoder class into two. Its Shannon closure-repair gain is

\[
g_{close}(Z\to Z')=
\frac{W_T(Z)-W_T(Z')}{H(Z')-H(Z)}.
\]

## Primary greedy/global test

Starting from each nonclosed target `T`, repeatedly take the available refinement cover with maximal `g_close`; ties are broken by canonical partition encoding. Stop at the first encoder with `W_T=0`.

Because every exact interval contains at most 877 nodes, enumerate the entire interval and compute the globally cheapest local exact repair

\[
A_T^*=\min_{Z\le T:\,W_T(Z)=0}A_T(Z).
\]

For every nonclosed `(rule,T)` record:

- greedy added-information cost;
- global minimum cost;
- absolute and relative regret;
- number of greedy edits;
- every globally optimal encoder;
- whether greedy reaches a global optimum.

### Primary hypothesis

There exists at least one block-3 `(rule,T)` case for which greedy repair is not globally information-optimal.

Report the exact success fraction regardless of outcome. If no counterexample exists, do not alter tie-breaking or objective definitions after inspection.

## First counterexample protocol

If greedy failure occurs, freeze the lexicographically first counterexample ordered by `(rule, canonical target)` and publish:

1. the greedy path and each local gain;
2. one globally optimal path;
3. the first decision at which the paths diverge;
4. the information regret introduced by that decision;
5. whether a beam of width `2`, `4`, or `8`, ranked by cumulative added information then residual `W`, recovers a global optimum.

Beam-search results are descriptive unless their ranking rule is implemented before the first full census result is inspected.

## Diminishing-returns audit

The perfect block-2 greedy result may reflect hidden structure in the fixed-target conditional-entropy objective. Test a local diminishing-returns condition before interpreting another high greedy-success rate.

Take a **coarser** encoder `Z_c` and a refinement `Z_f <= Z_c` that leaves some local class `C` unsplit in both. Let the same binary split operation `s:C -> C_1|C_2` be a valid cover at both encoders. Define

\[
\Delta_s W(Z)=W_T(Z)-W_T(sZ).
\]

A diminishing-returns-compatible comparison satisfies

\[
\Delta_s W(Z_c)\ge \Delta_s W(Z_f).
\]

That is: after adding unrelated present detail elsewhere, the same remaining split should not become *more* valuable.

Record exact counts of tested comparable same-split pairs and violations. Also record the cost-normalized gain ordering using `g_close` as a secondary diagnostic.

This is **not** asserted to be lattice submodularity in the formal sense; it is a preregistered local diagnostic intended to identify whether greedy success correlates with diminishing returns.

## Balance-stratified summaries

Report greedy success, regret, closure rate, target `h*`, and diminishing-return violations separately for target balances `1/7`, `2/6`, `3/5`, and `4/4`.

Wolfram-class comparisons remain exploratory. In particular, report but do not promote whether Class-IV rules fail greedy repair more often or at different target balances.

## CI execution

The instrument must be shardable by fine-rule interval and emit self-describing artifacts containing:

- ring width and cadence;
- exact rule interval;
- schema version;
- source and protocol hashes;
- per-target exact summaries;
- counterexample details when present.

CI aggregation must reject gaps, overlaps, mixed schemas, mixed ring sizes/cadences, or mixed source/protocol hashes before evaluating scientific summaries.

Because the full workload is substantially larger than Research027, use staged CI:

1. **sentinel validation** on Rules `30,54,90,106,110,184` across all 127 targets;
2. if the instrument and resource profile are sound, full 256-rule sharded validation without changing scientific definitions.

The sentinel phase is an implementation/resource gate, not a hypothesis test; do not revise the objective definitions from its outcomes.

## Exact controls

- canonical binary-target count is exactly 127;
- refinement-interval sizes equal `877,406,260,225` by target balance;
- fixed-target refinement never increases `W_T`;
- identity has `W_T=0`;
- every globally optimal repair found by enumeration has `W_T=0`;
- for block-3 Boolean targets already measured in Research026, the base target `W_T(T)` and `h*` reproduce the earlier block-3 values exactly;
- output-complement targets are exact relabelings and need not be recomputed independently.

## Scope and nonclaims

- Exactness is finite-ring and block-3-local.
- A greedy counterexample does not show that closure-guided repair is useless; it measures where one-step information gain ceases to be globally sufficient.
- Another 100% greedy result would not prove greedy optimality for arbitrary block size.
- The diminishing-returns audit is diagnostic, not a theorem about the partition lattice.
- The experiment still selects among local set-partition refinements; it does not yet synthesize arbitrary relational or stateful features.

## Decision boundary after the census

If greedy failures exist, the next theory target is to characterize the minimal obstruction and compare exact, beam, and defect-guided search.

If greedy remains globally optimal throughout, stop escalating brute force and pursue a proof or counterexample construction from the conditional-entropy / partition-refinement geometry.