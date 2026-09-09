# Exact sofic orbit closure for a one-defect paired cellular automaton

This note records the representation-independent statements used by the sofic defect-orbit line. The computational presentations may censor; the statements below do not depend on a particular determinization or graph-minimization strategy.

## Setup

Let

\[
\widehat g:B^3\to B
\]

be a radius-1 cellular automaton on a finite paired alphabet `B`.

Let `G_0` be a finite labeled graph whose bi-infinite label shift

\[
X_0=X(G_0)
\]

is the topological closure of the admissible one-defect initial configurations. For the Groovy block-3 construction, `G_0` has two diagonal phases and one seed-labeled transition between them.

Define exact time slices

\[
X_t=\widehat g^t(X_0).
\]

## 1. Sliding-block images of sofic shifts are sofic

Given a finite labeled presentation `G` of `X(G)`, construct a higher-block graph `I(G)` whose states are composable pairs of edges of `G`.

Every composable triple

\[
e_{i-1},e_i,e_{i+1}
\]

induces an edge

\[
(e_{i-1},e_i)\to(e_i,e_{i+1})
\]

labeled by

\[
\widehat g(\ell(e_{i-1}),\ell(e_i),\ell(e_{i+1})).
\]

After trimming to the bi-infinite core,

\[
\boxed{X(I(G))=\widehat g(X(G)).}
\]

### Reason

A bi-infinite path in `G` supplies every overlapping length-3 input neighborhood, hence a bi-infinite path in `I(G)` labeled by the CA image. Conversely, every bi-infinite path in the trimmed higher-block graph is an overlapping sequence of composable source-edge triples and therefore lifts to a source path in `G` whose image labels are exactly the presented output row.

Thus each exact time slice `X_t` is a sofic shift.

## 2. Finite orbit unions are sofic

Define

\[
U_t=\bigcup_{j=0}^{t}X_j.
\]

A disjoint union of finite labeled presentations presents the union of their label shifts, so every finite `U_t` is sofic.

No determinization is required for this fact.

## 3. Finite orbit stabilization is an exact all-time certificate

Suppose

\[
X_{t+1}\subseteq U_t.
\]

Then

\[
\widehat g(U_t)
=
\bigcup_{j=1}^{t+1}X_j
\subseteq U_t.
\]

Therefore

\[
\boxed{\widehat g(U_t)\subseteq U_t.}
\]

So `U_t` is an exact forward-invariant closure of the one-defect orbit.

If every paired symbol appearing in `U_t` is invisible to target observation `T`, no later time can contain a target-visible pair. Hence

\[
\boxed{w_T(a,b)=\infty.}
\]

This certificate contains no fixed-window splicing approximation: it reasons about the exact finite orbit slices themselves.

## 4. Exact finite witnesses

If an exact time-slice presentation `X_t` contains a target-visible paired-symbol label, then some admissible one-defect trajectory contains that label at macro-time `t`. Therefore an actual finite causal witness exists at `t`.

For new horizons, an explicit source context should still be independently reconstructed before publication; the labeled-graph existence statement itself is exact.

## 5. Presentation complexity is separate from language existence

The theorems above establish that finite labeled presentations exist for each fixed time slice and finite orbit union. They do **not** bound the size of convenient explicit presentations.

Three exact operations can each create large proof objects:

- right-resolving determinization of a nondeterministic slice;
- explicit higher-block image construction;
- exact language-inclusion products.

A resource ceiling reached by any of these is computational censoring, not a statement about the dynamical fate of the hidden distinction.

Research036 is primarily a record of this boundary: the exact sofic criterion is sound, but the tested explicit graph presentations do not evaluate the frozen 170-case hypotheses within their preregistered resource envelope.

## 6. Relation to finite-window invariants

Research033–034 construct finite-type outer approximations

\[
X_{W_*^{(2)}}\supseteq X_{W_*^{(3)}}\supseteq\cdots
\]

to the true reachable defect language. The sofic orbit construction attacks the complementary side: represent exact temporal images with automaton state rather than increasing spatial window width.

Neither hierarchy is assumed to dominate the other computationally. A future symbolic image representation may combine them: local word constraints for spatial composability, plus latent automaton state for constraints that are not efficiently expressible at a fixed window width.
