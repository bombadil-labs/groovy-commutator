# Generated reachable-context invariants for a one-defect paired cellular automaton

This note gives the exact finite-language controls used by Research033.

## Setup

Let

\[
g:A^3\to A
\]

be a radius-1 one-dimensional cellular automaton on a finite alphabet `A`. Its paired dynamics is

\[
\widehat g:(A\times A)^3\to A\times A,
\]

\[
\widehat g((a,a'),(b,b'),(c,c'))=(g(a,b,c),g(a',b',c')).
\]

Fix a target observation

\[
T:A\to O.
\]

A paired symbol `(u,v)` is **target-visible** when `T(u) != T(v)`.

Write

\[
D=\{(a,a):a\in A\}
\]

for the diagonal paired alphabet and fix one target-hidden seed

\[
s=(a,b),\qquad T(a)=T(b).
\]

The admissible initial configurations are arbitrary diagonal backgrounds with exactly one occurrence of `s`.

## 1. Generated symbol closure

Initialize

\[
S_0=D\cup\{s\}.
\]

Define

\[
S_{n+1}=S_n\cup\{\widehat g(x,y,z):x,y,z\in S_n\}.
\]

Because `A x A` is finite, the ascending sequence reaches a fixed point `S_*`.

### Theorem 1 — all reachable paired symbols lie in `S_*`

Every paired symbol appearing at any site and time in any admissible one-seed trajectory belongs to `S_*`.

### Proof

At time zero every site contains a symbol in `S_0` by construction.

Assume every site of a row lies in `S_n`. Each next-row site is obtained by applying `g_hat` to three symbols from `S_n`, hence lies in `S_{n+1}`.

Induction over time proves the claim, and `S_n` is contained in `S_*` for every `n`. ∎

### Corollary 1 — symbol safety certificate

If `S_*` contains no target-visible paired symbol, then

\[
\boxed{w_T(a,b)=\infty.}
\]

No admissible trajectory can ever expose the seed to the target.

## 2. Relation to the Research032 congruence certificate

Suppose `R` is a target-respecting congruence of `(A,g)` in the paired sense and contains both the diagonal and the seed.

Because a congruence is closed under componentwise application of `g`, every symbol generated from `D union {s}` remains in `R`. Therefore

\[
S_*\subseteq R.
\]

If `R` is target-safe, `S_*` is target-safe as well.

Hence every Research032 congruence certificate must also be a generated-symbol certificate. Research033 uses this implication as an exact implementation control.

The converse need not hold abstractly because `S_*` is not required to be an equivalence relation.

## 3. Generated nearest-neighbor edge language

The symbol closure forgets spatial compatibility: once two paired symbols have been generated anywhere, it allows them to appear next to any other generated symbols.

Track adjacency explicitly.

Let an edge set

\[
E\subseteq (A\times A)^2
\]

define the one-step shift of finite type `X_E` consisting of all bi-infinite rows whose adjacent symbol pairs are edges of `E`.

For the exact one-seed initial language, initialize

\[
E_0=(D\times D)\cup(D\times\{s\})\cup(\{s\}\times D).
\]

Given `E_n`, consider every allowed length-4 path

\[
p_0\to p_1\to p_2\to p_3.
\]

Its two adjacent output cells are

\[
q_0=\widehat g(p_0,p_1,p_2),
\qquad
q_1=\widehat g(p_1,p_2,p_3).
\]

Adjoin the output edge `q_0 -> q_1`. Iterating this monotone operation reaches a finite fixed point `E_*`.

## 4. Edge-language theorem

### Theorem 2 — every reachable adjacent pair lies in `E_*`

Every adjacent pair appearing in any admissible one-seed trajectory belongs to `E_*`.

### Proof

Every adjacent pair in an admissible initial row is either diagonal-diagonal, diagonal-seed, or seed-diagonal, so lies in `E_0`.

Assume every adjacent pair of one row lies in `E_n`. Any pair of adjacent cells in the next row depends on four consecutive input symbols. Since every input adjacency is in `E_n`, those four symbols form an allowed length-4 path in the edge shift. The construction of `E_{n+1}` therefore includes the corresponding output edge.

Induction proves the claim. ∎

### Theorem 3 — the fixed-point edge shift is forward invariant

\[
\boxed{\widehat g(X_{E_*})\subseteq X_{E_*}.}
\]

### Proof

Take any row in `X_{E_*}`. Every consecutive four-symbol word is an allowed length-4 path in `E_*`. At the fixed point the output edge associated with every such path is already in `E_*`. Therefore every adjacent pair of the image row is allowed, so the image row also belongs to `X_{E_*}`. ∎

### Corollary 2 — edge safety certificate

If no vertex incident to an edge of `E_*` is target-visible, then

\[
\boxed{w_T(a,b)=\infty.}
\]

The exact initial one-defect language lies inside a target-safe forward-invariant shift.

## 5. The edge certificate is at least as strong as the symbol certificate

Let `V(E_*)` be the vertices incident to the fixed-point edge set.

### Theorem 4

\[
V(E_*)\subseteq S_*.
\]

### Proof

The vertices of `E_0` are contained in `D union {s}=S_0`.

Whenever a new edge is generated, each endpoint is `g_hat` applied to a triple of vertices already present in the previous edge language. If those vertices lie in `S_n`, both output endpoints lie in `S_{n+1}`.

Induction over edge-closure rounds gives the result. ∎

Therefore target-safety of `S_*` implies target-safety of `E_*`. The edge certificate can only add cases; it cannot revoke a valid symbol certificate.

## 6. Why failure remains inconclusive

The one-step edge shift remembers adjacent compatibility but can still splice longer words that never co-occur in an actual trajectory.

Thus a target-visible vertex in `E_*` may be produced only through a length-4 path assembled from individually permitted edges that is globally unreachable from the one-seed initial language.

Failure of the edge certificate therefore does **not** imply a finite witness.

The natural hierarchy continues with length-`k` window languages. A width-`k` language stores allowed words of length `k`; its image closure is generated from allowed words of length `k+2`. Increasing `k` removes progressively more spurious context splicing at the cost of a larger finite-state representation.

Research033 stops at the nearest-neighbor level. Its unresolved residue is the target for the next higher-order de Bruijn invariant.
