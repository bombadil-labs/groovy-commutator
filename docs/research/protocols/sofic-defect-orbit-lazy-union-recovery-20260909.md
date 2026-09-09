# Recovery protocol: lazy exact sofic orbit union — 2026-09-09

**Status:** frozen after the complete primary `sofic-defect-orbit` run `34388121180` was reaggregated as 170/170 censored, and before evaluating any lazy-union recovery outcome.  
**Branch:** `research/sofic-defect-orbit-20260909`.  
**Dependency:** frozen `sofic-defect-orbit` exact sofic protocol and censor-aware primary summary.

## Why recovery is needed

The primary exact sofic instrument evaluates the 170 Research034 survivors with exact labeled-graph time slices and exact block-language inclusion. It also eagerly compresses the cumulative orbit union

\[
U_t=X_0\cup\cdots\cup X_t
\]

after every newly discovered slice.

The complete primary run establishes no finite witness and no finite sofic closure before a frozen resource ceiling, but **all 170 questions are censored**. Therefore neither preregistered scientific hypothesis is evaluated.

The exact censoring breakdown is:

- `compressed-graph-states`: 62 questions;
- `determinization-subset-states`: 46 questions;
- `image-pair-states`: 62 questions;
- censoring transition index: 12 at 0, 34 at 1, 62 at 2, 62 at 3.

The twelve Rule-122/161 hard-family questions are among the earliest determinization-censored cases.

## Algorithmic observation

Eager determinization of `U_t` is **not required by the mathematics**.

The physical time-slice recurrence is

\[
X_{t+1}=\widehat g(X_t),
\]

so propagation requires only the current exact slice `X_t`.

The closure query is

\[
X_{t+1}\subseteq U_t.
\]

A finite union of sofic shifts is represented exactly by the disjoint union of their labeled graphs. The existing exact inclusion oracle already accepts nondeterministic labeled graphs and performs subset construction on demand.

Therefore the recovery keeps

\[
U_t^{\rm lazy}=G_0\sqcup G_1\sqcup\cdots\sqcup G_t
\]

as an **uncompressed disjoint union of exact slice presentations** for inclusion queries only.

No language is changed:

\[
X(U_t^{\rm lazy})=X_0\cup\cdots\cup X_t.
\]

## Recovery algorithm

For each frozen `(rule,seed)` underlying the same 170 Research034 target questions:

1. construct exact compressed slice `X_0` exactly as in the primary instrument;
2. keep a list of exact slice graphs `[X_0]`;
3. at time `t`, inspect `X_t` for target-visible labels;
4. construct `X_{t+1}` with the same exact image+compression routine and the same frozen per-slice ceilings;
5. build a **raw disjoint union** of `X_0,...,X_t` without determinizing or compressing it;
6. test exact block-language inclusion
   \[
   X_{t+1}\subseteq X_0\cup\cdots\cup X_t
   \]
   with the same on-demand NFA inclusion oracle;
7. if inclusion holds and no prior exact slice was target-visible, classify remaining targets `finite-sofic-closure(t)`;
8. otherwise append `X_{t+1}` to the slice list and continue through horizon 12.

Target safety of the accumulated orbit needs no union graph: it is exactly the union of the per-slice visible-target masks already inspected.

## Semantic equivalence control

On every case that the primary instrument reached before censoring, the recovery must reproduce exactly:

- each exact slice graph language;
- each per-slice target-visible mask;
- each inclusion result that was computed before primary censoring.

Graph presentations may differ only if bidirectional block-language inclusion proves equality.

## Frozen resource ceilings

Keep every original primary ceiling for slice construction:

- compressed slice states: 200,000;
- compressed slice edges: 2,000,000;
- image pair states: 1,000,000;
- image determinization subset states: 500,000;
- pre-trim image/determinization transitions: 5,000,000.

Keep exact inclusion subset-pair ceiling:

- 2,000,000 subset-pair states per inclusion query.

Add one recovery-specific ceiling before outcomes:

- maximum **raw lazy-union graph states: 1,000,000**;
- maximum **raw lazy-union graph edges: 10,000,000**.

These bounds cover only the sum of already accepted exact slice presentations. Crossing them is censoring.

Do not raise any ceiling after seeing recovery outcomes.

## Freshness and hypotheses

This is a recovery of the already-frozen Note 036 / `sofic-defect-orbit` hypotheses, not a new hypothesis-generating experiment.

The original two hypotheses remain:

1. at least one of the 170 Research034 survivors is resolved by exact sofic analysis by horizon 12;
2. at least one survivor receives a target-safe finite sofic closure certificate without an exact target-visible slice.

The primary run did **not** falsify either hypothesis because all 170 cases were censored.

The recovery evaluates them only for the subset not censored by the lazy-union method. If any case remains censored, absence of a success among censored cases cannot count as falsification.

## Finite-witness rule

A finite witness is reported only when an exact time-slice graph contains a target-visible paired symbol.

If a new horizon-7+ event appears:

- freeze the earliest canonical event immediately;
- stop broad interpretive claims about witness depth until an independent fine-ECA SAT/SMT audit proves the event and excludes earlier horizons;
- language-inclusion counterexamples remain merely new orbit blocks, not witnesses.

## Recovery outputs

Report:

- finite witnesses and horizons;
- finite sofic closures and horizons;
- unresolved-through-12;
- censored questions;
- censoring stage/reason/horizon;
- number of slice graphs accumulated;
- total lazy-union states/edges by horizon;
- inclusion subset-pair states and shortest counterexample length;
- Rule-122/161 sentinel outcomes.

Explicitly compare recovery censoring against the primary 170/170 censoring result.

## Decision rule

- If recovery resolves cases, freeze the first witness/closure/a surviving case for independent audit before publication.
- If lazy union eliminates determinization censoring but slice-image ceilings remain dominant, the next target is exact slice representation/minimization rather than orbit-union representation.
- If inclusion itself becomes the dominant ceiling, move toward a simulation/bisimulation or language-quotient certificate rather than eagerly determinizing the union.
- If 170/170 remain censored, publish Note 036 / `sofic-defect-orbit` as a proof-complexity boundary and do not interpret either frozen hypothesis as false.
