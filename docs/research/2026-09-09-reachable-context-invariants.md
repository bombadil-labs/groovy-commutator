# The context is in the edges

Research032 ended with a sharply defined residue. In the matched block-3 ECA family, 52,712 local pair/target distinctions had no finite causal witness through horizon 6. A target-respecting algebraic congruence proved 47,352 of them permanently invisible.

That left

\[
\boxed{5,360}
\]

cases in between:

- no witness through the searched horizon;
- no all-context congruence proof of permanent invisibility.

Research033 asks why the congruence proof fails.

The answer is overwhelmingly spatial.

A one-defect trajectory cannot realize every algebraically imaginable juxtaposition of paired symbols. Once nearest-neighbor compatibility is retained, almost the entire residue becomes provably safe:

\[
\boxed{5,132/5,360=95.7463\%}
\]

receive exact all-time invisibility certificates.

Only

\[
\boxed{228}
\]

remain unresolved.

The main lesson is simple:

> **For hidden distinctions, knowing which local states exist is not enough. The causal question can depend on which states are allowed to sit next to one another.**

## The paired defect dynamics

For the exact block-3/cadence-3 macro rule

\[
g:A^3\to A,
\qquad A=\{0,\ldots,7\},
\]

consider two worlds simultaneously. Their paired local rule is

\[
\widehat g:(A\times A)^3\to A\times A.
\]

The diagonal paired symbols

\[
D=\{(a,a):a\in A\}
\]

represent places where the two worlds agree. A hidden seed `(a,b)` is inserted at one site into an otherwise arbitrary diagonal background.

For target `T`, a paired symbol `(u,v)` is visible when

\[
T(u)\ne T(v).
\]

A causal witness exists exactly when some admissible one-seed paired trajectory eventually reaches a visible paired symbol.

Research032's congruence certificate overapproximated those trajectories by demanding safety under every algebraically related local context. Research033 replaces that with generated languages beginning from the actual one-seed initial condition.

## Level 1: generated symbols do not help

The first frozen idea was to drop the equivalence-relation requirement but still forget spatial arrangement.

Start with

\[
S_0=D\cup\{s\}
\]

and close under every triple:

\[
S_{n+1}=S_n\cup\widehat g(S_n^3).
\]

If the fixed point `S_*` is target-safe, the seed is permanently invisible.

This certificate is exact and strictly less structured than a congruence. The preregistered prediction was that it would recover at least one of the 5,360 cases that congruence missed.

It does not.

\[
\boxed{0\text{ new generated-symbol certificates}.}
\]

The first frozen hypothesis fails.

This is informative. The main cost of the Research032 congruence was **not** the formal requirement that the safe relation be reflexive, symmetric, and transitive. At the level where every generated symbol may be combined with every other generated symbol, the congruence result was already effectively tight on this residual family.

## Level 2: preserve adjacency

The next representation remembers which paired symbols may be neighbors.

Let `E` be a directed graph on the 64 paired symbols. Its paths describe a one-step shift of finite type.

The exact one-defect initial language has edges

\[
E_0=(D\times D)\cup(D\times\{s\})\cup(\{s\}\times D).
\]

For every allowed length-4 path

\[
p_0\to p_1\to p_2\to p_3,
\]

the radius-1 paired rule produces the adjacent output edge

\[
\widehat g(p_0,p_1,p_2)
\to
\widehat g(p_1,p_2,p_3).
\]

Adjoin every such edge and iterate to a fixed point `E_*`.

The proof in `docs/research/proofs/reachable-context-invariants.md` establishes two exact facts:

1. every adjacency that can occur in a real one-seed trajectory is contained in `E_*`;
2. the edge shift defined by `E_*` is forward invariant.

Therefore, if every vertex admitted by `E_*` is target-invisible,

\[
\boxed{w_T(a,b)=\infty.}
\]

This is an exact all-time certificate, not a finite simulation.

## Exact census

The corrected primary run is Actions run `34381601120`.

Before accepting any new result, the aggregate reproduces the Research032 controls exactly:

- 52,712 pair/target distinctions with no finite witness through horizon 6;
- 47,352 target-congruence certificates;
- 5,360 non-congruence residual cases;
- 930 distinct `(rule, seed-pair)` generated languages underlying those residual target questions.

The new hierarchy then gives:

| certificate level | newly resolved from the 5,360 residue |
| --- | ---: |
| generated symbols | **0** |
| nearest-neighbor edge language | **5,132** |
| still unresolved | **228** |

Thus

\[
\boxed{95.7462686567\%}
\]

of the entire Research032 residue is proved permanently invisible as soon as spatial adjacency is retained.

The second frozen hypothesis — that edge closure would strictly improve on symbol closure — passes dramatically.

The compact exact aggregate is committed at

`results/reachable_context_invariants_20260909.json`.

## A minimal mechanism example

The first canonical edge-only certificate is:

- Rule 1;
- target `01001100`;
- hidden seed `0-2`.

Its unrestricted generated-symbol closure contains 48 paired symbols and is target-unsafe. So a representation that remembers only **which paired symbols can be generated** cannot prove the defect invisible.

Its generated nearest-neighbor language stabilizes after three closure rounds with **153 edges** and is target-safe.

The distinction is therefore permanent even though the symbol alphabet alone appears unsafe.

What disappeared was not a state. What disappeared was a **spatial juxtaposition**: the unsafe combinations needed to expose the defect cannot be assembled while respecting the generated adjacency grammar.

That is the constructive meaning of the title:

> **the missing context is in the edges.**

## Negative control: adjacency is not always enough

The first surviving case is close enough to make a useful control:

- Rule 5;
- the same target `01001100`;
- the same seed `0-2`.

Here the symbol closure reaches all 64 paired symbols. The edge language stabilizes at **230 edges**, but it still admits target-visible paired symbols.

So the edge certificate correctly refuses to prove permanence.

That failure remains inconclusive. A one-step edge shift can splice individually allowed adjacencies into longer words that are never jointly reachable. Rule 5 may therefore have a deeper finite witness, or it may require a higher-order invariant to prove permanent invisibility.

Research033 does not choose between those possibilities.

## The residual family gets highly concentrated

The 5,132 new edge certificates split, using the repository's existing Wolfram labels, as:

- Class I: **232**;
- Class II: **4,900**.

The 228 survivors are:

- Class II: **216**;
- Class III: **12**.

No Class I case survives the edge invariant in this residual family.

The twelve Class-III survivors are exactly the Rule-122 and Rule-161 cases that were already the hard MDD-censored/alternate-solver family in Research032:

- six Rule-122 seeds under target `00100000`;
- six Rule-161 seeds under target `00000100`.

This continuity is mechanistically interesting but remains descriptive. The repository's Wolfram labels are not promoted here as a universal classifier.

## Independent audit — and a bug it caught

The first independent audit was written as a scalar implementation that does **not** import the primary language-closure helpers. It rebuilds the block-3 macro rule from shrinking fine-ECA cones, constructs paired dynamics with Python tuples/sets, and verifies the final edge fixed points directly.

That audit immediately found a real bug in the primary generated-symbol implementation.

Paired-symbol IDs were stored as `int16`, so flattened indices of the form

`4096*x + 64*y + z`

could overflow before indexing the 64^3 paired-rule table.

Crucially:

- the independent audit reproduced every frozen **edge** count and edge safety classification;
- the mismatch appeared in generated-symbol round counts;
- the issue was fixed by widening symbol IDs to `np.intp`;
- the entire 256-rule census was rerun from the corrected source hash.

The corrected run reproduces the scientific result exactly:

- 0 symbol-only improvements;
- 5,132 edge certificates;
- 228 survivors;
- identical class breakdown and representative edge graphs.

The correction history is preserved in

`docs/research/protocols/reachable-context-invariants-index-correction-20260909.md`.

After the corrected aggregate was frozen, the independent audit was rerun on fourteen preregistered cases:

- the first edge-only certificate;
- the first unresolved case;
- all twelve Rule-122/161 sentinels.

It passes

\[
\boxed{14/14}.
\]

The exact audit output is committed at

`results/reachable_context_invariants_20260909_audit.json`.

## What this changes in the research picture

Research025 already showed that the fate of a hidden distinction depends on physical context.

Research028 showed that the value of representing a distinction depends on representational context.

Research033 makes the word **context** more structural:

> **A hidden distinction can look causally dangerous when local states are treated as freely combinable, yet become provably harmless once the grammar of admissible spatial relationships is represented.**

This is stronger than saying locality matters. The sufficient state is not only a list of local variables; it can require a language of allowed relations among them.

In that sense, representation design has moved from

\[
\text{state alphabet}
\]

to

\[
\boxed{\text{state alphabet + spatial grammar}.}
\]

## What remains open

Research033 is exact for the declared matched block-3/cadence-3 ECA macro family, but its edge language is still an overapproximation.

The remaining 228 cases may contain:

- genuine finite witnesses at horizon 7 or later;
- permanently invisible defects whose safety depends on length-3 or longer spatial constraints;
- both.

The edge certificate cannot decide which.

Nothing here establishes a universal finite witness bound for cellular automata, and graph size is not claimed as an intrinsic complexity measure.

## Next question: the de Bruijn hierarchy

The natural next representation keeps allowed words of length three rather than only adjacent pairs.

For window width `k`, start from every `k`-word appearing in a one-defect diagonal background. Close the language under every `(k+2)`-word admitted by its current overlaps, because a radius-1 CA maps such a word to a `k`-word one step later.

The hierarchy is then

\[
\text{symbols}
\to
\text{edges}
\to
\text{length-3 words}
\to\cdots
\]

with progressively less spurious context splicing.

Research033 has already shown that the first spatial step is enormous:

\[
5360\to228.
\]

The next question is whether one more unit of context collapses the remaining frontier — or finally reveals a defect whose witness really does live beyond the desert.
