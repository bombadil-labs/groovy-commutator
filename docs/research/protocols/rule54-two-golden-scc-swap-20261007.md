# Post-primary frozen continuation: the two golden Rule-54 fiber components

**Date:** 2026-10-07. **Status:** frozen after the original stage-2 outcomes
but **before** testing this narrower two-component invariance property.
This is selected from a visible result and therefore exploratory,
not independently preregistered confirmation.

**Author:** GPT-6 (OpenAI). Independent peer review pending.

## Why this is distinct

The original frozen Rule-54 study found three pure off-diagonal branching
G,Q,R,A4,A5 pair-language SCCs, with Perron roots approximately:

- 1.2720196495 (52 vertices, 68 edges);
- 1.1278384856 (52 vertices, 58 edges);
- 1.2720196495 (84 vertices, 110 edges).

Every component remained invisible at the next time step.
None was individually source-evolution invariant and their **three-component
union** failed (the middle-rate component evolves toward another SCC).

The two maximal-Perron components each passed the original *three-component*
union check, with counterexamples to individual invariance witnessing
movement between them.

We therefore select **exactly those two sqrt(phi)-rate components**, call
them C_plus (52 vertices, 68 edges) and C_minus (84 vertices, 110 edges),
and test whether they form a closed pair under Rule-54 evolution.

The selection is expressly post-primary; no later component addition,
deletion, threshold change or deeper jet is permitted in this unit.

## Exact gate

For all bi-infinite pair configurations presented by C_plus and C_minus,
respectively, prove or refute

\[
(H_{54}\times H_{54})(C_+)\subseteq C_-,
\qquad
(H_{54}\times H_{54})(C_-)\subseteq C_+.
\]

Use exact enumeration of all 3-edge source-pair paths inside each SCC,
representing every possible 15-bit paired source patch; apply Rule54
componentwise to obtain a 13-bit paired successor patch and test that its
equal-jet pair edge lies *inside the other declared SCC*.

- Record exact counts of length-three paths.
- Record exact target-component histograms.
- Save first lexicographic counterexample if either inclusion fails.
- Reimplement the source-rule evolution and local jet equality independently
  on all these paths (not merely 100 samples).
- Record exact 52/68 and 84/110 component counts and validate the
  characteristic factor z^4-z^2-1 / Perron sqrt(phi) as previously established.
- Test no other SCC as a replacement.

If both inclusions hold, the union C_plus ∪ C_minus is a full-line
invariant source-pair subshift with exponential pair-language growth rate
sqrt(phi), strictly >1. Since both components sit inside equality of
G..A5, source evolution preserves equality of G along every forward
trajectory. Induct on

\[
A_{k+1}(x)=A_k(Hx)\oplus H(A_k(x))
\]

to conclude **all future levels A_k, k>=1, are equal** for source pairs in
the union. This is an all-depth invisibility theorem *for this exceptional
positive-entropy pair language*, not a general Rule54 compression theorem,
not a claim of positive typical conditional entropy, and not a recurrence
for individual source configurations.

If either inclusion fails, report an exact bounded negative and stop; no
more SCCs or jet levels.
