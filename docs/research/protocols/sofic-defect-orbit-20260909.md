# Protocol: exact sofic defect-orbit closure — 2026-09-09

**Status:** frozen before evaluating any of the 170 Research034 width-3 survivors.  
**Branch:** `research/sofic-defect-orbit-20260909`.  
**Dependency:** Research034 composable-context / width-3 reachable-language result on `main`.

## Question

Research034 leaves 170 pair/target distinctions unresolved after a hierarchy of exact sufficient permanence certificates:

- Research032 all-context congruence: `5,360` residual;
- Research033 nearest-neighbor paired grammar: `228` residual;
- Research034 length-3 paired grammar: `170` residual.

Every fixed-width language is still an outer approximation. It can splice locally admitted words into globally unreachable rows.

The next question is:

> **Can the exact orbit of the one-defect regular language be represented directly as a finite-state sofic shift, so that a survivor is resolved either by an actual deeper witness or by finite stabilization of its exact forward orbit closure?**

This checkpoint does **not** increase the window width and does not assume a universal finite-state closure exists.

## Exact initial sofic shift

Let the paired macro alphabet be

\[
B=A\times A,
\qquad |A|=8,
\qquad |B|=64.
\]

Let

\[
D=\{(a,a):a\in A\}
\]

be the diagonal alphabet and fix one target-hidden seed paired symbol `s=(a,b)`.

Use a two-state labeled graph `G_0(s)`:

- state `L` has one self-loop labeled by every symbol in `D`;
- state `R` has one self-loop labeled by every symbol in `D`;
- one edge `L -> R` is labeled by `s`.

Its bi-infinite label shift consists exactly of:

- arbitrary all-diagonal paired configurations; and
- arbitrary diagonal backgrounds with exactly one occurrence of `s`.

The all-diagonal branch is the topological closure of the one-defect set and is target-safe by construction.

## Labeled-graph semantics

For a finite directed graph `G` with edge labels in `B`, let

\[
X(G)\subseteq B^{\mathbb Z}
\]

be the set of labels of bi-infinite paths.

Before any language operation, trim the graph to states that lie on some path from a directed cycle to a directed cycle. After trimming, every finite path extends to a bi-infinite path.

The finite block language `L(G)` is therefore exactly the set of finite words labeling finite paths in the trimmed graph.

For subshifts,

\[
X(G_1)\subseteq X(G_2)
\iff
L(G_1)\subseteq L(G_2).
\]

Language inclusion is decided exactly by on-the-fly subset determinization of both labeled graphs. A nonempty endpoint subset is accepting; the empty subset rejects. A BFS over the product of subset states either proves inclusion or returns a shortest counterexample block.

No bounded block-length approximation is permitted for inclusion/equality claims.

## Exact CA image of a sofic shift

Let the paired radius-1 rule be

\[
\widehat g:B^3\to B.
\]

Given a trimmed labeled graph `G`, construct its exact image graph `I(G)` as follows.

A state of `I(G)` is a composable pair of input edges

\[
(e_{i-1},e_i).
\]

Every composable input-edge triple

\[
e_{i-1},e_i,e_{i+1}
\]

induces an output edge

\[
(e_{i-1},e_i)
\to
(e_i,e_{i+1})
\]

labeled

\[
\widehat g(\ell(e_{i-1}),\ell(e_i),\ell(e_{i+1})).
\]

After trimming,

\[
\boxed{X(I(G))=\widehat g(X(G)).}
\]

This is the standard higher-block presentation of a radius-1 sliding-block image.

## Exact right-resolving compression

Raw image graphs can grow rapidly. After each image and union operation, the production implementation may replace a presentation by an exact right-resolving presentation with the same finite block language.

Procedure:

1. trim to the bi-infinite core;
2. treat every remaining graph state as a possible finite-word start and accept state;
3. determinize by subset construction, starting from the set of all states;
4. discard the empty/dead subset;
5. optionally minimize states with identical continuation languages;
6. trim the resulting transition graph again to its bi-infinite core.

Because the source language is factorial and bi-extendable, the resulting labeled graph presents exactly the same subshift.

Every compression step must be guarded by exact bidirectional block-language inclusion against the uncompressed graph on the bounded sentinel cases before it is trusted in the primary census.

## Exact defect orbit

Define exact time slices

\[
X_t(s)=\widehat g^t(X_0(s)),
\]

and cumulative orbit shifts

\[
U_t(s)=\bigcup_{j=0}^t X_j(s).
\]

A finite union of sofic shifts is sofic; represent `U_t` by disjoint graph union followed by exact right-resolving compression.

At each macro-time `t`:

1. inspect `X_t` for a target-visible paired-symbol label;
2. if one exists, an actual causal witness exists at time `t`;
3. construct `X_{t+1}=I(X_t)` exactly;
4. test whether

\[
X_{t+1}\subseteq U_t.
\]

If the inclusion holds, then

\[
\widehat g(U_t)
=
\bigcup_{j=1}^{t+1}X_j
\subseteq U_t,
\]

so `U_t` is an exact forward-invariant orbit closure.

If `U_t` is target-safe, then

\[
\boxed{w_T(a,b)=\infty.}
\]

This is stronger than Research034's finite-window certificate: no unreachable context has been added except the harmless all-diagonal closure branch.

## Witness extraction

A target-visible label in an exact time-slice graph is already an existence proof, but every newly discovered finite witness at macro-horizon `>=7` must be independently reconstructed before publication.

Freeze the first event immediately and use an independent SAT/SMT shrinking-cone encoding at the original fine-ECA level to:

1. prove no witness exists at earlier horizons not already settled by Research032;
2. produce an explicit `(2t+1)`-block shared context with the frozen seed pair at one axis;
3. replay `3t` fine ECA ticks;
4. confirm target divergence.

Do not infer a witness from failure of sofic stabilization or from a language-inclusion counterexample.

## Baseline controls

Before interpreting any Research034 survivor, the production implementation must pass:

### Positive witness control

Research031's canonical horizon-3 event:

- Rule **35**;
- target `00000001`;
- seed pair `2-6`.

The exact sofic time slices must be target-safe at horizons 0, 1, and 2 and first become target-visible at horizon **3**.

### Permanent-safety control

Research034's Rule-5 mechanism:

- Rule **5**;
- target `01001100`;
- seed `0-2`.

Research034 already proves `w=infinity`. Therefore **no exact sofic time slice may ever become target-visible** at any evaluated horizon. Finite sofic stabilization is not required by this control.

### Survivor baseline

The primary instrument must reproduce Research034 exactly:

- width-3 survivors: **170**;
- survivor split: **158 Class II + 12 Class III**;
- all twelve Rule-122/161 hard-family questions remain in the input set.

For every evaluated survivor and every exact time slice through horizon 6, target visibility must be absent, reproducing Research032's finite-horizon null.

## Fresh evaluation horizon

Evaluate exact sofic slices and cumulative orbit closure through macro-horizon

\[
\boxed{H=12}
\]

unless a case resolves earlier or hits a frozen resource ceiling.

Thus horizons 7–12 are fresh for finite-witness discovery.

A case is classified as:

- `finite-witness(t)` if first target visibility occurs at exact time `t`;
- `finite-sofic-closure(t)` if `X_{t+1} subset U_t` and `U_t` is target-safe;
- `unresolved-through-12` if neither occurs through horizon 12;
- `censored` if an exact resource ceiling is reached.

## Frozen resource ceilings

The method is exact but finite-state presentations can blow up.

Freeze per `(rule,seed)`:

- maximum compressed graph states: **200,000**;
- maximum compressed graph edges: **2,000,000**;
- maximum subset states created by one determinization/compression: **500,000**;
- maximum subset-pair states explored by one inclusion test: **2,000,000**;
- CI wall-clock budget per case/shard: operationally **20 minutes**.

Exceeding a ceiling is **censoring**, never evidence for permanence, non-stabilization, or absence of a witness.

Exact implementation optimizations are allowed after censoring, but semantic definitions, horizon 12, and the frozen scientific hypotheses may not change after outcomes are inspected.

## Frozen primary hypotheses

Frozen before any Research034 survivor is evaluated by the sofic instrument:

1. **Exact sofic closure adds information beyond width 3.** At least one of the 170 Research034 survivors is resolved by horizon 12, either by an actual finite witness or by finite target-safe sofic orbit stabilization.
2. **Finite-window danger is sometimes purely spurious.** At least one of the 170 survivors receives a finite-sofic-closure certificate without any target-visible exact time slice.

No prediction is frozen for the number of deeper finite witnesses.

No prediction is frozen for the Rule-122/161 hard families.

No prediction is frozen for whether all 170 cases resolve.

## Measurements

For every distinct `(rule,seed)` underlying the 170 target questions record:

- repository Wolfram class;
- target IDs carried by the seed language;
- exact time-slice presentation states/edges by horizon;
- cumulative-orbit presentation states/edges by horizon;
- shortest inclusion-counterexample block length when `X_{t+1}` is not yet contained in `U_t`;
- first target-visible horizon per target, if any;
- first safe stabilization horizon per target, if any;
- determinization and inclusion subset-state counts;
- censoring reason, if any.

Aggregate:

- finite-witness resolutions;
- finite-sofic-closure resolutions;
- unresolved-through-12;
- censored cases;
- class breakdowns;
- Rule-122/161 sentinel status.

## Independent audit

After the census, freeze before independent reconstruction:

- the first new finite witness, if any;
- the first finite-sofic-closure certificate, if any;
- the first unresolved non-censored case;
- all Rule-122/161 sentinels that resolve or exhibit qualitatively distinct graph behavior.

Audit finite witnesses with an independent fine-ECA SAT/SMT light-cone solver.

Audit finite-sofic-closure cases with a separately written labeled-graph implementation that independently checks:

1. exact `G_0` language;
2. exact sliding-block image semantics for every time slice through stabilization;
3. exact block-language inclusion `X_{t+1} subset U_t`;
4. target safety of the stabilized union.

Any mismatch blocks publication.

## Interpretation boundaries

- Finite sofic stabilization is sufficient for permanent invisibility but is not guaranteed to occur for every permanently invisible defect.
- Failure to stabilize through horizon 12 does not imply a finite witness exists.
- Censoring is computational, not dynamical.
- A language-inclusion counterexample is a new admissible context block, not necessarily a target witness.
- The construction is exact for the declared matched block-3/cadence-3 ECA paired dynamics; no universal decidability or finite-state theorem for arbitrary CA is claimed.
- The 3D hypothesis remains parked.

## Decision rule

- If any horizon-7+ finite witness appears, freeze and audit the earliest canonical event before broad interpretation.
- If finite-sofic closure resolves cases, compare automaton-state cost against fixed-width word counts and characterize the state memory responsible for excluding spurious compositions.
- If most cases censor or remain unresolved, analyze graph-state growth and move toward a purpose-built reachability invariant rather than simply increasing width or horizon.
