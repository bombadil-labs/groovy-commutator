# Protocol: constructive representation design on a local partition lattice — 2026-09-08

**Status:** frozen before evaluation.  
**Branch:** `research/representation-design-20260908`  
**Dependency:** stacked on Research026 / `research/possibility-frontier-20260908`.

## Question

Research026 found a genuine forgetting / future-repertoire frontier, but it still searched over a catalog of complete observers. The next question is constructive:

> **Can the latent/shielded decomposition tell us how to edit a representation, one local distinction at a time, toward predictive closure or toward greater unresolved future repertoire?**

The experiment uses the complete lattice of local partitions of a two-cell block. This makes “refine” and “coarsen” exact operations rather than metaphors.

## Local representation lattice

A two-cell fine block has four patterns

`00, 10, 01, 11`

using the repository's little-endian block-code convention. A local representation is a set partition `pi` of these four patterns. Macro-symbol names are irrelevant; only the partition matters.

There are exactly Bell(4)=15 such partitions:

- one four-symbol identity partition;
- six three-symbol partitions;
- seven two-symbol partitions;
- one constant partition.

Apply `pi` independently to six nonoverlapping two-cell blocks of the periodic `n=12` ring. Use matched cadence `q=2`.

Write `pi' <= pi` when `pi'` refines `pi`: every class of `pi'` lies inside a class of `pi`. A **cover edit** splits one local macro-symbol into exactly two symbols; the reverse edit merges exactly two symbols.

This lattice contains the seven output-complement classes of Boolean block-2 observers from Research024–026, but also inserts the six one-split intermediate representations between a binary observer and the local identity.

## Part A: diagonal self-observation graph

For every ECA rule and every one of the 15 local partitions, use the same representation both for the present macrostate and for future observations. Measure the Research026 quantities

\[
L(\pi)=H(S\mid P_\pi(S)),
\]

\[
V(\pi)=H(C_\infty^\pi\mid P_\pi(S)),
\]

and

\[
Q(\pi)=L(\pi)-V(\pi),
\]

where `V` is future repertoire / latent information and `Q` is permanently shielded information.

For every cover edge record

\[
\Delta L=L(\pi_{coarse})-L(\pi_{fine}),
\qquad
\Delta V=V(\pi_{coarse})-V(\pi_{fine}).
\]

Because editing `pi` also changes what counts as a distinguishable future, **no monotonicity of `V` is assumed on diagonal edits**. Count refinement edges for which adding present detail unexpectedly *increases* future repertoire. This is a direct test of target drift under observer refinement.

Controls:

- identity has `L=V=0`;
- constant has `L=12,V=0`;
- the seven binary nodes reproduce the Research026 block-2 values exactly;
- the forgetting / repertoire information identity closes for all 15 nodes.

## Part B: decouple present encoding from future semantics

For representation design, fix a binary target observation `T` and allow the **present encoder** `Z` to refine it locally.

The future semantics remain fixed to the original target trajectory

\[
T_0,T_1,T_2,\ldots,
\qquad T_t=T(E^{2t}(S)).
\]

Let `C_infinity^T` be the exact future-equivalence class under this fixed target. For any local encoder partition `Z <= T`, define residual predictive uncertainty

\[
W_T(Z)=H(C_\infty^T\mid Z(S)).
\]

and added present information

\[
A_T(Z)=H(Z(S))-H(T(S)).
\]

`W_T(T)=V(T)` and `W_T(identity)=0`.

Unlike the diagonal objective, refinement of `Z` with `T` fixed must monotonically decrease `W_T` by ordinary conditioning. Any violation is an implementation error.

Evaluate all seven canonical binary targets for every ECA rule, and every one of their local refinements in the 15-node partition lattice.

## Closure-directed edit gradient

For a refinement cover `Z -> Z'`, define

\[
g_{close}=\frac{W_T(Z)-W_T(Z')}{H(Z')-H(Z)}
\]

when the denominator is positive.

Starting from each nonclosed binary target, repeatedly choose the cover split with largest `g_close`; ties are broken canonically by partition encoding. Stop when `W_T=0`.

Because the full interval `[T, identity]` is tiny, compute the globally optimal local closure repair exactly:

\[
A_T^*=\min_{Z<T:\,W_T(Z)=0} A_T(Z).
\]

Record whether greedy repair attains `A_T^*`, its excess information cost when it does not, and the number of split edits required.

This tests whether the closure defect supplies a useful **local repair gradient** rather than merely diagnosing failure.

## Possibility-directed edit gradient

Read the same fixed-target lattice in reverse. Starting from local identity, a merge forgets some present information while leaving the future semantics `T` fixed. Define

\[
g_{poss}=\frac{W_T(Z')-W_T(Z)}{H(Z)-H(Z')}
\]

for a coarsening cover `Z -> Z'`.

This is the amount of unresolved target-future entropy opened per bit forgotten now.

For every target, compute the exact nondominated frontier in

\[
(F_T(Z),W_T(Z)),\qquad F_T(Z)=H(S\mid Z(S)),
\]

and compare the greedy possibility-ascent path from identity with that frontier. Record whether every greedy node is nondominated and whether greedy reaches the best `W_T` available at each attained forgetting level.

## Mechanism preregistration: Rule 106 parity

Rule 106 under block-2 parity is the primary mechanism control.

Parity partitions the four local patterns as

\[
\{00,11\}\;|\;\{10,01\}.
\]

Research024–025 found a long-lived hidden adjacent defect that flips `10 <-> 01`. Before evaluation, predict:

> **The better first closure-directed split for Rule 106 parity will split the odd-parity class `{10,01}` rather than the even-parity class `{00,11}`.**

Measure the exact `W_T` reduction and `g_close` of both possible one-split refinements. If the prediction fails, retain the failure.

Also report the analogous first-split choice for Rules 30, 54, 90, 110, and 184 without preregistered directionality.

## Fresh-size mechanism check

If the Rule-106 first-split prediction passes at `n=12`, freeze the winning split before evaluating `n=18`. At `n=18`, require only that the same split still reduces fixed-target residual uncertainty more than the competing one-split refinement. Do not reselect after inspection.

## Primary summaries

Across all 256 rules and seven binary targets report:

1. fraction of nonclosed targets for which greedy closure repair is globally information-optimal;
2. distribution of greedy excess information cost;
3. fraction of greedy possibility-path nodes lying on the exact fixed-target Pareto frontier;
4. diagonal cover edges where refinement increases `V` because future semantics changed;
5. Rule-106 parity mechanism result and, if triggered, fresh-size confirmation;
6. Wolfram-class comparisons only as exploratory summaries.

## Scope and nonclaims

- All exact claims concern finite periodic rings and the declared local two-cell partition family.
- The full local identity is always available as a closure repair; this does not imply the repair is compact on larger blocks or infinite lattices.
- Fixed-target `W_T` is a design objective with future semantics held constant. Research026's diagonal `V(P)` instead lets the representation define both present state and future distinctions. The distinction between these two problems is part of the experiment.
- Greedy success in a 15-node lattice would motivate, not prove, scalable representation-learning algorithms.
- The experiment does not yet learn arbitrary new local features from raw defect traces; it tests whether exact defect-derived gradients are informative enough to navigate a complete small representation lattice.
