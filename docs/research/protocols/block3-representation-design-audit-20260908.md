# Audit protocol: first block-3 greedy counterexample — 2026-09-08

**Status:** frozen after the full Research028 census and before an independent audit or any fresh-size evaluation.  
**Discovery run:** GitHub Actions `34308263175`.  
**First counterexample:** Rule 24, target partition `01000010`, periodic `n=12`, cadence `q=3`.

## Purpose

The primary Research028 census found four greedy/global-optimality disagreements among 30,856 nonclosed block-3 target cases. The lexicographically first is Rule 24 with target `01000010`.

This audit must independently reconstruct the future target words and representation costs without importing the Research028 experiment or aggregation code.

## Frozen discovery claims to audit

For target

`01000010`

(the target classes are `{0,2,3,4,5,7}` and `{1,6}`), the census reports:

- target residual future entropy `W = 0.6887218755408675`;
- greedy exact repair cost `6.754887502163468` added bits;
- global minimum exact repair cost `5.754887502163468` added bits;
- exact greedy regret `1` bit;
- greedy final repair `01230245`;
- a globally optimal repair `01230243`.

The first greedy split is

`01000010 -> 01200210`,

which separates `{2,5}` from the large target class and has positive immediate predictive gain.

The globally optimal path begins instead with

`01000010 -> 01000020`,

which separates the small target class `{1,6}` into `{1}` and `{6}`. The census reports essentially zero immediate decrease in `W` for this first split.

## Synergy mechanism to audit

Let `s` be the split that separates `{3,7}` from the large target class.

Applied directly to the target it gives encoder

`01020012`.

Applied after the zero-gain `{1}|{6}` split it gives

`01020032`.

The independent audit must compute both raw and cost-normalized predictive gains. The frozen discovery values are:

- direct split `{3,7}`: `ΔW ≈ 0.03308281331130125`, `g ≈ 0.012008771060640643`;
- after `{1}|{6}` is already present: `ΔW ≈ 0.4387218755408666`, `g ≈ 0.15925219276515995`.

Thus the same distinction becomes more than an order of magnitude more predictive after another distinction is present. This is the candidate predictive-synergy obstruction to greedy repair.

## Independent method

1. Implement ECA Rule 24 directly from its eight-entry truth table; evolve the exact `2^12` state set for three fine steps per macrostep.
2. Implement the target and named encoder partitions directly from their eight local labels.
3. Construct explicit target future words until the target partition stabilizes; do not call the Research028 partition-refinement implementation.
4. For each named encoder compute `W_T(Z)` from explicit `(Z(S), target-future-word(S))` rows.
5. Enumerate every local refinement of target `01000010` independently as a product of set partitions of its two target classes. Verify the expected interval size `B_6 B_2 = 406`.
6. Determine exact closure by asking whether the complete target-future word is a function of the encoder state.
7. Recompute the globally minimum added encoder entropy among all closed refinements.
8. Reconstruct the frozen greedy path using the same stated one-step gain rule and canonical tie-breaking, but from the independently calculated table.

## Acceptance

The audit passes only if all of the following hold:

- interval size is exactly 406;
- the named global encoder `01230243` is closed;
- no closed refinement has lower added information than `5.754887502163468` within `1e-9`;
- the independent greedy path closes at added cost `6.754887502163468` within `1e-9`;
- regret is exactly 1 bit within `1e-9`;
- the `{1}|{6}` first split has zero predictive gain within `1e-9`;
- the `{3,7}` split has strictly greater predictive gain after the `{1}|{6}` split than before it.

## Interpretation boundary

A successful audit establishes this finite counterexample and its conditional-information synergy mechanism. It does not establish that every greedy failure is caused by the same motif, nor that the target classes `{1,6}` or `{3,7}` have an intrinsic semantic meaning outside this Rule-24 finite system.

No fresh-size claim is made in this protocol. A size-validation protocol may be frozen only after this audit passes.