# Recovery protocol: raw-NFA exact sofic slices — 2026-09-09

**Status:** frozen after the lazy-union recovery left all 170 Research034 survivors censored at exact slice-image construction, and before evaluating any raw-slice recovery outcome.  
**Branch:** `research/sofic-defect-orbit-20260909`.  
**Publication identity:** this protocol belongs to public **Note 036** with canonical slug `sofic-defect-orbit`. A temporary prepublication number collided with a parallel note and was normalized; no alternate note number is canonical.

## Why a second recovery is needed

The primary `sofic-defect-orbit` method represented each exact sofic time slice by a determinized right-resolving graph and eagerly determinized the cumulative orbit union. The complete primary run censored all 170 questions.

The first frozen recovery removed eager union determinization by keeping the accumulated orbit as a lazy disjoint union of exact slice graphs. It again left all 170 questions censored, now **all at the slice-image stage**.

Thus cumulative-union representation is no longer the identified bottleneck. The remaining question is whether exact slice propagation itself requires determinization.

It does not.

## Exact representation change

For a labeled graph `G` presenting a sofic shift, the standard radius-1 higher-block image graph `I(G)` already presents the exact CA image:

\[
X(I(G))=\widehat g(X(G)).
\]

Determinizing `I(G)` changes only the presentation, not the language. Target visibility depends only on edge labels, and the exact block-language inclusion oracle accepts nondeterministic labeled graphs directly.

Therefore this recovery keeps every physical time slice as the **trimmed raw higher-block NFA** and never determinizes it.

Define

\[
G_0=\text{the exact two-state one-defect graph},
\]

\[
G_{t+1}=I(G_t)
\]

with no right-resolving compression.

The accumulated orbit remains the lazy disjoint union

\[
U_t^{\rm lazy}=G_0\sqcup\cdots\sqcup G_t.
\]

Closure is tested exactly by

\[
X(G_{t+1})\subseteq X(U_t^{\rm lazy}).
\]

If inclusion holds and no target-visible label has occurred in any exact slice, the remaining target receives the exact all-time certificate `finite-sofic-closure(t)`.

A target-visible label in `G_t` is an exact finite witness at time `t`.

## Frozen domain and hypotheses

Use exactly the same 170 Research034 width-3 survivors and the same macro-horizon

\[
H=12.
\]

The original frozen hypotheses remain unchanged:

1. at least one of the 170 survivors is resolved by exact sofic analysis by horizon 12;
2. at least one survivor receives a target-safe finite sofic closure certificate without any target-visible exact time slice.

The primary and lazy-union runs did not falsify these hypotheses because every case was censored.

## Exact raw-image construction

For each trimmed source graph:

1. enumerate composable pairs of source edges `(e0,e1)` as image states;
2. for every composable source triple `(e0,e1,e2)`, add an image edge
   `(e0,e1) -> (e1,e2)` labeled by the paired macro rule applied to the three source labels;
3. normalize duplicate labeled transitions;
4. trim to the bi-infinite core.

No subset construction, determinization, minimization, sampling, or bounded-word approximation is permitted for the time slices.

## Semantic controls

Before the 170-case census, require:

### Rule 35 positive witness

For Rule 35 / target `00000001` / seed `2-6`, raw exact slices must be target-safe at horizons 0,1,2 and first target-visible at horizon 3.

For the bounded horizons where the original right-resolving control is tractable, raw and compressed image presentations must be bidirectionally block-language equivalent.

### Rule 5 permanent control

For Rule 5 / target `01001100` / seed `0-2`, raw exact slices must remain target-invisible through the bounded control horizon.

The raw-slice lazy-union inclusion must recover the same bounded finite orbit closure seen by the original exact control.

### Primary-domain regression

- reproduce exactly 170 Research034 survivors;
- reproduce class split 158 Class II + 12 Class III;
- no target visibility may occur through horizon 6 for any evaluated survivor.

Any failure blocks the census.

## Frozen resource ceilings

Retain the existing image-construction ceilings, now applied directly to the raw NFA:

- maximum composable input-edge-pair states in one raw image: **1,000,000**;
- maximum pre-normalization raw image transitions: **5,000,000**.

Retain the lazy-union bounds:

- maximum summed lazy-union states: **1,000,000**;
- maximum summed lazy-union edges: **10,000,000**.

Retain the exact inclusion bound:

- maximum subset-pair states explored by one inclusion query: **2,000,000**.

Crossing any limit is censoring only. Do not raise ceilings after outcomes.

## Measurements

For every survivor record:

- exact raw slice states/edges/labels by horizon;
- raw image pair-state and pre-normalization transition counts;
- lazy-union state/edge totals;
- exact inclusion result and explored subset-pair states;
- shortest inclusion counterexample block length when applicable;
- first target-visible horizon;
- finite closure horizon;
- censoring stage/reason/horizon.

Aggregate finite witnesses, finite closures, unresolved-through-12, censored cases, class breakdowns, horizon distributions, and Rule-122/161 sentinel outcomes.

## Independent-audit rule

If a new horizon-7+ witness appears, freeze the earliest canonical event immediately for independent fine-ECA SAT/SMT replay before publication.

If a finite sofic closure appears, freeze the earliest canonical case for a separately written raw labeled-graph audit checking every slice image and the final inclusion.

If all 170 remain censored, no independent outcome audit is required beyond the frozen controls; publish the exact censoring boundary and identify the dominant raw-NFA operation.

## Decision rule

- If raw slices resolve cases that compressed slices censored, characterize determinization as proof overhead rather than physical-language complexity.
- If raw image pair/edge growth dominates, move toward a symbolic transducer/image representation rather than increasing window width or resource ceilings.
- If inclusion dominates, target simulation/bisimulation or a language quotient.
- If non-censored cases survive unresolved through 12, publish them as genuine bounded exact-sofic survivors; do not infer permanence or a future witness.
