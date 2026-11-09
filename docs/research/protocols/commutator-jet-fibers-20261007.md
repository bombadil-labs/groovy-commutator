# Protocol: residual fibers of the full-entropy commutator jet

**Status:** descriptive exact follow-up, frozen before canonical pair-graph
evaluation on 2026-10-07. Directional synchronization scratch results from the
parent unit motivated this question; they are not scored as fresh predictions.

**Authored by:** GPT-5.6 Sol (OpenAI). **Reviewed by:** none.

## Question

The G-anchored jet language reaches the full one-bit source spatial entropy
within the tested tower:

- Rule 110 by \(J_{110}=(G,Q,R)\);
- Rule 62 by \(J_{62}=(G,Q,R,A_4,A_5)\).

Full entropy does not imply injectivity. What source distinctions remain hidden
behind these jet fields?

For a sliding-block jet map \(\pi:S\mapsto J\), analyze the exact fiber product

\[
\mathcal F_\pi
=
\{(X,Y):\pi(X)=\pi(Y)\}.
\]

The diagonal \(X=Y\) is trivial. The non-diagonal part is the residual latent
state still erased by the jet.

## Fixed primary factors

- Rule 110: \(J=(G,Q,R)\), source radius 4.
- Rule 62: \(J=(G,Q,R,A_4,A_5)\), source radius 6.

Controls immediately below full entropy:

- Rule 110: \(J=(G,Q)\).
- Rule 62: \(J=(G,Q,R,A_4)\).

No other rules or jet depths.

## Exact pair presentation

For each factor, use the same source de Bruijn presentation as the parent
language unit.

Construct the ordered pair graph:

- a vertex is a pair of source de Bruijn contexts \((u,v)\);
- an edge is a pair of source edges \(u\to u'\), \(v\to v'\);
- retain the edge exactly when the two source edges carry the same jet symbol.

This graph presents all source pairs with equal jet output.

Prune to the **bi-infinite support**: vertices and edges lying on some path
with infinite continuation in both spatial directions. Use exact finite-graph
reachability/SCC logic.

## Recurrent hidden ambiguity

Separate diagonal and non-diagonal structure.

For the non-diagonal bi-infinite support, record:

- vertices and edges;
- strongly connected components containing a cycle;
- Perron entropy of every recurrent component;
- maximum non-diagonal recurrent entropy;
- whether every recurrent non-diagonal component is a simple directed cycle;
- periods and source-XOR words of all such cycle components when finite enough
  to serialize compactly.

Interpretation:

- positive non-diagonal recurrent entropy means an extensive hidden source
  language survives the jet;
- zero-entropy cycles mean persistent ambiguity is phase/gauge-like;
- acyclic paths connecting recurrent components represent finite or domain-wall
  interfaces between asymptotic ambiguity sectors.

No complexity-class interpretation is attached.

## Heteroclinic / domain-wall support

After removing recurrent non-diagonal SCC interiors, inspect essential
non-diagonal vertices that lie on paths between recurrent SCCs.

Record:

- count of such interface vertices;
- which recurrent SCCs can connect to which;
- shortest representative source-pair path for each ordered SCC connection;
- XOR difference word along that representative interface.

This is intended to detect the phase-wall mechanism already seen in the
parity+Groovy obstruction.

## Directional synchronization

Independently compute one-sided source-context subset automata in both spatial
directions for the same jet factor.

Record:

- minimum compatible source-context count reachable from the full context set;
- whether a singleton context is reachable;
- minimum word length achieving the minimum, when <=64;
- one witness jet word and compatible source contexts.

This is finite-word directional synchronization, not a bi-infinite preimage
degree theorem.

## Local inverse search

For each primary factor, exhaust exact jet windows of radius \(R=0,1,2,3,4\)
and ask whether they determine the central source bit on the complete source
causal window.

Stop at first passing radius. A failure through four is bounded only; the pair
graph remains the exact full-line ambiguity presentation.

## Decisions / interpretation boundaries

This is descriptive rather than a pass/fail classifier.

The important alternatives are:

1. **positive-entropy hidden fiber:** the raw jet still erases an extensive
   latent field;
2. **zero-entropy phase fiber:** the jet captures the full information rate but
   misses only phase/gauge sectors and their interfaces;
3. **diagonal only:** the jet is injective on the full line.

Finite periodic collisions are not by themselves enough to distinguish these.

## Hard boundaries

- Rules 110 and 62 only.
- Four fixed factors listed above.
- No deeper jet field.
- No Class-IV census.
- No claim that a compact pair graph is the same thing as source compression.
- Do not infer infinite-line injectivity from finite-ring fibers; the pair graph
  is the infinite-line object.

## Planned artifacts

- scripts/experiment_commutator_jet_fibers.py
- results/commutator_jet_fibers_20261007.json
- docs/research/2026-10-07-commutator-jet-fibers.md
