# The closure defect can design its own repair

Research026 showed that representation choice has a forgetting / future-possibility frontier. This note asks a more constructive question:

> **Can the distinctions responsible for closure failure tell us how to edit the representation, instead of forcing us to search blindly over complete observers?**

On the complete local partition lattice of a two-cell block, the answer is strongly yes for one natural objective and importantly plural for another. A greedy Shannon-information repair finds the globally minimum-information local closure repair in every nonclosed case tested. But the edit that best repairs average predictive uncertainty often differs from the edit that kills the rare longest-lived hidden mode.

The expensive census is the project’s first CI-native research workload. The committed protocols and shardable instrument were evaluated by GitHub Actions in eight disjoint rule shards, then aggregated, independently audited, and checked on a frozen fresh-size Rule-106 case. The first green validation run was [34305510238](https://github.com/bombadil-labs/groovy-commutator/actions/runs/34305510238); the final clean PR reruns the same frozen workload against `main`.

## A local lattice of representations

A two-cell fine block has four patterns, in repository order,

`00, 10, 01, 11`.

A local representation is a partition of those four patterns into macro-symbol classes. There are exactly `Bell(4)=15` such partitions, from the local identity through six three-symbol partitions, seven binary partitions, to the constant partition.

This gives exact notions of **refinement** and **coarsening**. A one-step refinement splits one current macro-symbol into two. Rather than replacing an observer wholesale, Research027 can therefore ask which *single distinction* should be restored next.

The primary census uses all 256 elementary cellular automata on the periodic `n=12` ring, matched cadence `q=2`, and all seven canonical binary target partitions.

## Fix the future semantics before repairing the present

There is a subtle distinction between changing a representation and repairing one. If the same edited map defines both the present state and the future observations, refinement changes what counts as a distinguishable future. More detail now can even reveal more future repertoire simply because the target semantics changed.

For constructive repair, Research027 therefore fixes a binary target `T` and edits only the present encoder `Z`. Let `C_infinity^T` be the complete stable future-equivalence partition of the target trajectory. Define

\[
W_T(Z)=H(C_\infty^T\mid Z(S)).
\]

`W_T(Z)` is the unresolved target-future information left after seeing the augmented present encoder. Refining `Z` cannot increase it. The local identity always has `W_T=0`.

For a one-split refinement `Z -> Z'`, define the closure-repair gain

\[
g_{close}=\frac{W_T(Z)-W_T(Z')}{H(Z')-H(Z)}.
\]

This asks how much unresolved future uncertainty an added present bit removes.

## Greedy closure repair is globally optimal on this lattice

Across the full exact census there are **1,590 nonclosed `(rule,target)` cases**. Starting from each binary target, repeatedly choose the available one-split refinement with maximum `g_close`, stopping at exact fixed-target closure.

Because the local lattice is tiny, the globally minimum added-information repair can also be computed exhaustively.

The result is exact:

\[
\boxed{1590/1590}
\]

Greedy Shannon closure repair reaches the globally minimum-information local repair in every nonclosed case.

Within this bounded representation family, the closure defect is therefore not merely diagnostic. It provides a **constructive local gradient** toward a sufficient state description.

This does not prove greedy repair scales to larger representation lattices. It gives a clean base case against which such algorithms can be tested.

## The first preregistered mechanism prediction failed

Rule 106 under block-2 parity was the mechanism control. Parity groups the four local patterns as

\[
\{00,11\}\;|\;\{10,01\}.
\]

Research024–025 had identified a long-lived hidden defect that flips `10 <-> 01`. Before evaluation, the primary protocol predicted that splitting this odd-parity class would be the better first Shannon closure repair.

That prediction failed.

Splitting the **even** class `{00,11}` removes slightly more ensemble-weighted residual future entropy per added present bit. The rare, spectacular traveling defect does not dominate the Shannon mass of closure failure.

The failure exposed a second repair objective rather than killing the mechanism story.

## Bulk repair and tail repair are different objectives

The follow-up protocol was frozen before the all-rule tail census. Instead of minimizing average residual future entropy, measure the least target-history depth needed after a present refinement to recover the **entire** stable target-future partition. This is the worst-case residual latent-memory tail.

An independent audit caught an important implementation error before publication: for a one-time encoder `Z`, a temporary no-split plateau does not imply that later target observations cannot split the partition again. The corrected tail is the first horizon that reaches the full stable future-equivalence partition, not the first local plateau. The protocol retains the original provisional value and the correction.

With the corrected definition, the full census finds that bulk-optimal and tail-optimal first splits disagree in

\[
\boxed{326/1590 = 20.5\%}
\]

of nonclosed cases.

For repository-labeled Class-IV target cases the disagreement is

\[
\boxed{60/98 = 61.2\%}.
\]

Whenever they disagree, the tail-oriented edit deliberately accepts a worse Shannon-average repair in exchange for eliminating the longest-lived hidden mode sooner.

## Rule 106 makes the tradeoff concrete

For Rule 106 parity at `n=12`:

| Present encoder | Bulk residual | Worst-case target tail |
| --- | --- | ---: |
| parity target | baseline | 13 |
| split `{00,11}` | **bulk-optimal** | 13 |
| split `{10,01}` | slightly worse bulk repair | **7** |

The defect-oriented split is not the Shannon-optimal first move, but it directly attacks the coherent hidden mode that generated the long memory tail.

A fresh-size protocol froze these two edits before the exact `n=18` evaluation. The result preserves the qualitative separation:

| Present encoder | Worst-case target tail at `n=18` |
| --- | ---: |
| parity target | 49 |
| bulk-optimal even split | 49 |
| defect-oriented odd split | **19** |

The even split remains no worse in bulk residual entropy, so the fresh test supports the intended tradeoff rather than merely finding a generally superior refinement.

## Why this changes the research direction

The project can now move beyond asking whether a representation closes and beyond searching catalogs of candidate observers. On this small exact lattice, we can **edit the representation in the direction indicated by its failure**.

But “the direction” is not unique. At least two repair objectives are already distinct:

1. **bulk predictive repair** — remove the most ensemble-weighted unresolved future information per added present bit;
2. **tail repair** — eliminate the rare longest-lived latent mode as quickly as possible.

Research026 had already separated predictive closure from future possibility. Research027 shows objective pluralism *inside closure repair itself*. A representation may be excellent on average while retaining a tiny pathological tail, or may spend extra state bits specifically to kill that tail.

This suggests that a mature representation calculus will be multi-objective, with quantities such as information cost, average predictive uncertainty, worst-case memory depth, future repertoire, locality, and update complexity all available as explicit design coordinates.

## CI as part of the evidence pipeline

The corrected full census was intentionally moved out of the local scratch environment once its runtime became inconvenient. The scientific protocol does not depend on CI: the experiment script accepts explicit rule intervals and remains locally runnable. GitHub Actions only supplies parallel execution and artifact transport.

The validation workflow executes:

- eight disjoint 32-rule shards;
- exact coverage aggregation with gap/overlap/source-hash rejection;
- an independently written explicit-future Rule-106 audit;
- the frozen `n=18` confirmation.

See [Research CI](CI.md) for the project’s execution policy.

## Limits

- The 100% greedy result is exact only on the complete 15-node two-cell local partition lattice. Larger blocks may contain traps where locally best information gain is not globally cheapest.
- The uniform finite-state ensemble determines the Shannon weighting. A different state distribution can change the bulk-optimal split.
- Worst-case tail is only one risk-sensitive objective; other tails or quantiles may matter.
- The result does not yet learn arbitrary features from raw defect traces. It chooses among exact local partition edits.
- Class comparisons remain exploratory and symmetry-related rules are not independent replications.

## Next question

The next step should test whether the constructive gradient survives when the local representation space becomes large enough that exhaustive search is no longer trivial.

A natural progression is block size three: compare greedy repair against exact global optima where feasible, then introduce beam or defect-guided search when the partition lattice becomes too large. The Rule-106 result suggests retaining separate bulk and tail objectives rather than collapsing them into one scalar score.
