# Protocol: width-3 reachable paired language — 2026-09-09

**Status:** frozen before evaluating any of the 228 Research033 edge-language survivors.  
**Branch:** `research/window3-reachable-language-20260909`.  
**Dependency:** Research033 reachable-context invariants on `main`.

## Question

Research033 leaves exactly 228 pair/target distinctions in the matched block-3/cadence-3 ECA family after the nearest-neighbor paired-language invariant:

- 5,360 Research032 non-congruence residual distinctions;
- 5,132 receive exact all-time nearest-neighbor edge-language certificates;
- 228 remain unresolved because the edge shift still admits at least one target-visible paired symbol.

The edge shift is still an overapproximation: individually allowed adjacencies can be spliced into longer words that never occur jointly in a one-defect trajectory.

The next question is:

> **Does remembering allowed length-3 paired words remove enough spurious context to certify additional permanent invisibility?**

This note tests only width 3. It does not search a deeper causal horizon and it does not adapt the window width after seeing outcomes.

## Exact paired macro dynamics

Reuse the exact matched block-3 macro rule

\[
g:A^3\to A,
\qquad A=\{0,\ldots,7\},
\]

and its paired rule

\[
\widehat g:(A\times A)^3\to A\times A.
\]

Let

\[
B=A\times A,
\qquad |B|=64,
\]

and let

\[
D=\{(a,a):a\in A\}
\]

be the diagonal paired alphabet. A hidden seed is one non-diagonal paired symbol

\[
s=(a,b),
\qquad T(a)=T(b),
\]

inserted into an otherwise arbitrary diagonal background.

## Width-3 initial language

Let

\[
W_0\subseteq B^3
\]

contain every length-3 word appearing in a one-defect diagonal initial row.

Equivalently,

\[
W_0
=
D^3
\cup
(\{s\}\times D\times D)
\cup
(D\times\{s\}\times D)
\cup
(D\times D\times\{s\}).
\]

Because the seed is non-diagonal, these sets are disjoint and

\[
|W_0|=8^3+3\cdot8^2=704.
\]

The shift defined by `W_0` is an overapproximation of the exact one-seed language: it can admit multiple defects if they are sufficiently separated. That is acceptable for a sufficient safety certificate.

## Width-3 closure

Given a current language

\[
W_n\subseteq B^3,
\]

admit a length-5 word

\[
p_0p_1p_2p_3p_4
\]

iff all three consecutive length-3 windows lie in `W_n`:

\[
(p_0,p_1,p_2),
(p_1,p_2,p_3),
(p_2,p_3,p_4)
\in W_n.
\]

Its three-cell image is

\[
q_0=\widehat g(p_0,p_1,p_2),
\]

\[
q_1=\widehat g(p_1,p_2,p_3),
\]

\[
q_2=\widehat g(p_2,p_3,p_4).
\]

Define

\[
W_{n+1}
=
W_n\cup
\{(q_0,q_1,q_2):p_0\ldots p_4\text{ is admitted by }W_n\}.
\]

Because `B^3` is finite, this monotone sequence reaches a fixed point `W_*`.

## Width-3 invariance theorem

Every length-3 window appearing in any admissible one-seed paired trajectory belongs to `W_*`.

Moreover, the shift of finite type

\[
X_{W_*}
=
\{x\in B^\mathbb Z:\text{every consecutive 3-word of }x\text{ lies in }W_*\}
\]

is forward invariant under the paired CA:

\[
\boxed{\widehat g(X_{W_*})\subseteq X_{W_*}.}
\]

Reason: every output 3-window depends on one input 5-word; every consecutive input 3-window is admitted by `W_*`; fixed-point closure therefore already contains the output 3-word.

For target `T`, if no paired symbol appearing in any word of `W_*` is target-visible, then

\[
\boxed{w_T(a,b)=\infty.}
\]

This is an exact all-time certificate.

## Hierarchy control

Project the width-3 language to nearest-neighbor edges. Every initial edge is contained in the Research033 `E_0`, and every generated width-3 word projects to edges that the Research033 edge closure admits.

Therefore the vertex set admitted by `W_*` is contained in the vertex set admitted by the Research033 fixed-point edge shift `E_*`.

Consequences:

1. every Research033 edge certificate must also be width-3 safe;
2. width 3 may certify additional cases but cannot revoke an edge certificate;
3. the new primary evaluation may be restricted to the 228 Research033 survivors after reproducing that exact count.

Any hierarchy violation is an implementation error.

## Computational representation

Represent `W` as 4,096 rows indexed by the first two paired symbols, each row a 64-bit mask of allowed third symbols.

For a fixed pair `(b,c)`:

- collect the output-symbol set produced by every allowed predecessor triple `(a,b,c)`;
- for every allowed central triple `(b,c,d)`, collect the output-symbol set produced by allowed successor triples `(c,d,e)`;
- group successor outputs by the central output `g_hat(b,c,d)`;
- OR the resulting Cartesian products into output 3-word masks.

This is exactly equivalent to enumerating admitted length-5 words but avoids iterating over all `64^5` possibilities.

No approximation, pruning, random sampling, or heuristic language minimization is permitted in the primary result.

## Baseline controls

Before interpreting width-3 outcomes, the production instrument must reproduce the committed Research033 totals exactly:

- Research032 non-congruence residual: **5,360**;
- Research033 edge certificates: **5,132**;
- Research033 edge survivors: **228**;
- survivor class split: **216 Class II + 12 Class III**;
- the twelve Class-III survivors are exactly the frozen Rule-122/161 sentinel families.

The first Research033 unresolved control must also reproduce:

- Rule 5;
- target `01001100`;
- seed `0-2`;
- 230-edge nearest-neighbor fixed point;
- edge certificate fails.

## Frozen primary hypotheses

Frozen before width-3 evaluation:

1. **Width 3 strictly improves on edges.** At least one of the 228 edge-language survivors receives an exact width-3 permanence certificate.
2. **Rule-5 splice hypothesis.** Rule 5 / target `01001100` / seed `0-2` is certified safe at width 3. This predicts that its Research033 failure is caused by an impossible longer phrase assembled from individually allowed edges.

No prediction is frozen for the final survivor count.

No prediction is frozen for the Rule-122/161 sentinel families.

## Measurements

For every distinct `(rule,seed)` language among the 228 residual target questions record:

- repository Wolfram class;
- seed pair;
- Research033 edge count and rounds;
- width-3 fixed-point word count and rounds;
- target IDs entering the width-3 evaluation;
- target IDs newly certified;
- target IDs still unresolved;
- maximum and median per-row mask occupancy descriptively;
- whether the seed is one of the Rule-122/161 sentinels.

Aggregate:

- new width-3 certificates;
- survivor count;
- class breakdown of certificates and survivors;
- distinct `(rule,seed)` languages evaluated.

## Resource boundary

A width-3 language has at most

\[
64^3=262,144
\]

words, so the state space itself is finite and explicitly bounded.

The production algorithm may optimize exact set operations, but it may not change the language semantics.

CI timeout is operational censoring only. If any shard exceeds the frozen runtime envelope, report it as censored and optimize the exact implementation without interpreting missing cases as failures or survivors.

Do not skip dense Rule-122/161 cases.

## Independent audit

After the exact census, freeze before independent reconstruction:

- the first new width-3 certificate, if any;
- the Rule-5 mechanism case;
- the first case still unresolved after width 3, if any;
- all twelve Rule-122/161 sentinel cases.

Use an independently written scalar or sparse de-Bruijn implementation that does not import the production width-3 closure helper.

For every frozen case it must verify:

1. the exact initial 704-word language;
2. the final word count and round count;
3. direct fixed-point closure under every admitted length-5 path;
4. target safety/unsafety;
5. the hierarchy relation to the independently reconstructed Research033 edge language.

Any mismatch blocks publication.

## Interpretation boundaries

- A width-3 safety result proves `w=infinity` exactly for that rule/target/seed.
- Failure remains inconclusive: a 3-window shift can still splice individually valid 3-words into longer globally unreachable phrases.
- Do not infer a horizon-7 witness from width-3 failure.
- Do not infer a universal finite-width bound.
- Counts are exact only for the matched block-3/cadence-3 ECA macro family and 127 canonical binary targets.
- The 3D hypothesis remains parked.

## Decision rule

- If width 3 certifies all 228 cases, characterize the resulting finite-context permanence theorem candidate before testing width 4 elsewhere.
- If a nonempty residue survives, the next theoretical object is the width-4 de Bruijn language or a reachability-minimal automaton, not a blind horizon sweep.
- If Rule 5 is rescued, characterize the forbidden 3-word/5-word mechanism explicitly.
- If Rule 5 survives, retain the failed mechanism prediction and use the first successful width-3 case instead.
