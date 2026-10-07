# Frozen unit: all-256 GQR hidden-fiber census and Rule-54 invariance gate

**Date:** 2026-10-07. **Author:** GPT-6 (OpenAI). **Review:** pending.
**Status:** frozen before this unit's census and source-pair invariance computations.
**Dependency:** the bounded Rule54/30/90 jet control result in draft PR #327.

## Scientific question

The earlier selected panel showed:
- Rule 30/110: first full-source-entropy jet (G,Q,R) leaves only
  periodic recurrent off-diagonal source-pair components;
- Rule 54: at (G,Q,R), and still at (G,Q,R,A4,A5), some off-diagonal
  recurrent SCCs branch, with selected Perron root sqrt(phi) at A4/A5;
- Rule 90: G and higher residuals are identically zero.

We will establish a *base rate* for branching equal-GQR fibers over **all 256**
elementary rules, then attempt a **separate, targeted dynamical invariance
certificate** for the already identified Rule-54 golden-mean-like components.
The census is not a Class-IV classifier. No rule/threshold selection or
further census after observing results.

## Stage 1: fixed all-256 exact GQR census

For each ECA r in 0..255:

1. Compute exact radius-two, radius-three, radius-four source truth tables
   for G=A1, Q=A2, R=A3 using
   A0=I XOR H, Ak+1=Ak o H XOR H o Ak.
2. Build the binary-source de Bruijn graph with state words of 8 bits
   (256 states), 9-bit source words as edges, and 3-bit edge output
   (G,Q,R) at the center. Use all 512 source words.
3. Form the **ordered** equal-output source-pair graph. Its vertices
   are source-context pairs (u,v), with a paired edge iff source
   edges receive identical GQR labels. Record exact edge counts.
4. SCC-decompose the graph. Recurrent means SCC contains a directed
   cycle. Classify:
   - diagonal recurrent components;
   - mixed recurrent components containing both diagonal/off-diagonal;
   - pure off-diagonal recurrent components;
   - **branching** if the SCC contains more internal edges than vertices
     (including parallel transitions), equivalently is not a single
     simple directed cycle;
   - cycle-only if every recurrent off-diagonal component is a simple
     directed cycle.
5. Report the 256-rule histogram: any branching recurrent off-diagonal
   component, mixed vs pure, cycle-only, no off-diagonal recurrence,
   and zero-G cases. Include the exact sorted rule sets in machine data.
   Deduplicate reflection/conjugacy classes *only as a secondary
   diagnostic*, never instead of the literal 256-rule denominator.
6. Record GQR image local alphabet size, source word labels, max cycle
   period on each rule, and SCC counts. Do not infer topological entropy
   of the image from number of local symbols; no universal spectral
   computation or higher-jet entropy sweep is part of this census.

Controls: Rule 90 (all-zero GQR), Rule 30 (off-diagonal cycle-only at GQR),
Rule 54 (pure branching SCCs at GQR), Rule 110 (cycle-only), Rule 62
(mixed/branching at GQR). Mismatches mean implementation failure and must be
diagnosed before interpretation.

**Resource cap:** at most the 256 rules and GQR source radius four, no
per-rule enlargement. The pair graph has at most 65,536 possible vertices
and 262,144 paired edges per rule. Preserve run timing and peak RSS.

## Stage 2: Rule-54 persistent Fibonacci SCCs

The target was fixed from #327 *before this 256-rule census*: the three
strongly connected pure off-diagonal **branching** components of the Rule-54
equal-output jet pair graph at G,Q,R,A4,A5, in particular the components
with Perron root sqrt(phi).

Regenerate Rule-54 exact A1..A5 local truth tables and the equal-output
radius-six pair graph with 12-bit source-context pairs, 13-bit source
windows as source edges. Recurrent SCCs are identified by their exact
vertex/edge lists, with canonical lexicographic identifiers. Resource cap
5 million source-pair edges / 2 GiB working RAM (same as prior unit).

For each targeted recurrent branching component C, regarded as the
spatial sofic/SFT language of all bi-infinite paths in its internal edge
graph, check two distinct claims:

**I — next-time observability:** does the image of *every* pair in C under
(H54 x H54) still have identical G,Q,R,A4,A5 fields everywhere?

**II — component invariance:** is that evolved pair again a path inside the
same C? A pass for II is a self-contained all-time certificate:
(HxH)(C) subseteq C and C consists of equal-jet source pairs.

Compute both by exhaustive **length-three consecutive internal pair-edge
paths**. A source context vertex covers 12 cells; a path of three paired
edges covers 15 source cells. Rule 54 has radius 1, so the evolved
central 13-cell paired word (positions 1..13) contains the full
G..A5 source dependency at time t+1. This test covers every local
possibility in C, including all bi-infinite source pairs presented by it.
If necessary use live-path pruning within C to avoid counting paths that
cannot extend bi-infinitely (a recurrent SCC has this property automatically).

For each component record:
- exact vertex count, edge count, Perron estimate and phase language;
- total admissible three-edge pair paths tested;
- claim I pass/fail, with the **lexicographically first 15-bit paired
  counterexample** and first changed jet field when false;
- claim II pass/fail, with first evolved 13-bit paired source edge not in C;
- if I passes but II fails, avoid claiming all-time invisibility.
  Also examine whether the image lies in the **union** of *all three*
  target components (same testing contract), but do not expand to
  arbitrary newly chosen components to rescue.
- if an invariant *union* passes, prove by induction all future jet fields
  agree for pairs in that union, using
  Ak+1(S)=Ak(H(S)) XOR H(Ak(S)) and same-field equality.
- if none pass, record exact obstruction. No blind A6, A7… sweep.

For a candidate invariant set C, the all-order proof must explicitly
distinguish equality of source derivatives from equality of G onward.
The inductive base is A1..A5 equality and invariance under HxH; it then
implies all A_k (k>=1) agree at t=0. This is a proof about jet equality,
not necessarily every source coordinate or future S.

**Stage 2 independence:** use a second direct Boolean evaluator to verify
at least 100 deterministically selected three-edge path witnesses and
all failed first counterexamples. A same-author verifier is not peer review.
Verify the exact SCC membership sets against #327 saved component counts
and characteristic-polynomial factors for the target sqrt(phi) components.

## Stopping and reporting

Stage 1 finishes all 256 rules, Stage 2 only the declared Rule-54 components.
No live Class-IV labels, rule list selection by score, lift comparison,
random seeds, unplanned deeper jets, or numerical-threshold "rescue."

Separate:
- recurrent pair-language entropy from conditional source entropy;
- one-step equality from forward invariant relation;
- pair graph description from canonical minimal machine;
- finite exact result from theoretical generalization.

Write a compact narrative: "we wondered X, tried Y, found Z" with
controls, counterexamples, failure cases, resource figures and instructions.
Publish source runner and canonical JSON in draft PR; do not merge to main.
