# Protocol: matched commutator jets for Rules 54, 30, and 90

**Date:** 2026-10-07. **Status:** frozen before evaluation.  
**Author:** GPT-6 (OpenAI). **Reviewed by:** none.

## Question

The existing Rule-110 and Rule-62 units found that iterating the same-lattice
commutator field

\[
A_0=D_H=I\oplus H,\qquad A_{k+1}=A_k\circ H\oplus H\circ A_k
\]

progressively recovers source spatial entropy, and at the first full-entropy
G-anchored prefix the residual source-pair fiber has only zero-entropy recurrent
off-diagonal phase cycles and interfaces.

Is this pattern exceptional to 110/62, or does it arise in other dynamical
regimes? Hold the entire construction and source domain fixed, and add three
preselected controls:

- Rule 54: independent complex/Class-IV-like comparison;
- Rule 30: canonical chaotic/Class-III comparison;
- Rule 90: additive linear control with a predicted identically zero G field.

No rule substitution, screening, or all-rule census.

## Stage A: exact local commutator fields

Compute local source truth tables for G,Q,R,A4,A5 for all three rules, using
full source windows of radii 2,3,4,5,6. Record exact activity fraction,
minimum source radius, ANF degree, and ANF support size. Check the identity
\(G_{90}\equiv0\) analytically and against the truth tables. Any mismatch is a
stop-and-debug outcome, not a theory failure.

## Stage B: exact finite-word spatial language

For each rule and G-anchored prefix G through GQRA4A5, construct the binary
source de Bruijn graph of width \(2r\) contexts with \(r=m+1\) for the deepest
field \(A_m\). Label its source edges with the sitewise jet symbol.

The graph presents the exact full-shift image language. Determinize from all
source contexts, remove unreachable states, and minimize the deterministic
finite-word-language automaton (with an implicit rejecting sink). Compute exact
allowed-word counts for lengths 1..16 and numerical topological entropy from
the integer labeled graph's spectral radius. Report the DFA state count as
presentation size, not information compression.

For each rule, select the **first** tested prefix whose spatial entropy is one
bit/site within numerical tolerance \(10^{-9}\), provided the pair-graph check
below confirms no positive-entropy off-diagonal recurrent component. A floating
point entropy value alone is not a proof of injectivity or finite fiber degree.

If no such prefix occurs through A5, record that endpoint; do not extend.

The Rule-90 expectation is that every G-anchored prefix is the constant-zero
language, with topological entropy zero. This follows algebraically because
H90 is additive and D90=I+H90 commutes with H90.

## Stage C: exact source-pair fiber structure

Compute an equal-label source de Bruijn pair graph and prune to bi-infinite
support, then SCC-decompose it, for:

1. the first full-entropy prefix, if any;
2. its immediately shallower prefix, if any;
3. if there is no full-entropy prefix through A5, the A5 prefix (subject to
   the resource gate).

Classify diagonal SCCs, mixed positive-entropy SCCs, and recurrent off-diagonal
SCCs with spectral radius 1 and directed-cycle structure. Record interface
states, periods and source-XOR phase differences.

**Resource gate:** skip any requested graph if predicted equal-label paired
edge count exceeds 5,000,000 or estimated working memory exceeds 2 GiB. Mark
the case "resource-censored," not "no hidden ambiguity." Do not increase the
budget after viewing results.

Rule 90 has the exact analytic pair-language answer: all source pairs are
allowed because G,Q,... vanish, so the pair language is the full four-symbol
shift with entropy 2 bits/site. Verify its local table control but do not
materialize a large redundant pair graph.

If the first full-entropy prefix has only zero-entropy recurrent off-diagonal
components, compare its maximum hidden phase period to the deepest jet
field's source radius as a **descriptive** diagnostic. The previously observed
equalities (Rule 110: 4=4, Rule 62: 6=6) are not a frozen hypothesis for this
panel and should not be retrofitted as a universal theorem.

## Independence and comparison

Use a fresh implementation of jet local truth tables. Cross-check its source
convention and known Rule-110 / Rule-62 local fields against the existing
canonical data where practical, without scoring those old cases as new
confirmation. Preserve source maps, raw numerical metrics, and witnesses.
Any substantive contradiction with a prior note is a correction task.

A numerical estimate of one does not prove a full-line one-to-one map.
A positive-entropy pair graph does not by itself establish Class III/IV.
A compact sofic presentation is not compressed microstate information.

## Stopping rule

After the three-rule panel through A5 and bounded paired-fiber checks, stop.
No lift modification, class prevalence claims, rule sweeps, fresh observables,
or deeper jets in this unit.

## Planned artifacts

- scripts/experiment_jet_control_panel.py
- results/jet_control_panel_20261007.json
- docs/research/2026-10-07-jet-control-panel.md

This is a bounded comparator for the existing Rule-110/62 claims, not a
retrospectively optimized discriminator.
