# Protocol: bounded search for a middle Rule-110 repair track

**Status:** post-hoc family selected after the parity+Groovy phase-wall result;
canonical exhaustive search definition frozen before repository publication,
2026-10-07. Exploratory scratch work informed the family choice, so this is a
descriptive exact classification, not a preregistered discovery test.

**Authored by:** GPT-5.6 Sol (OpenAI). **Reviewed by:** none.

## Question

The current exact hierarchy is:

1. block parity \(P\) alone is compressed but non-Markovian;
2. \(P+G^\circ\) exactly repairs the next parity readout but is not autonomous;
3. adding the block-phase gradient restores autonomy but reconstructs the source
   up to one global bit.

Is there a simple **middle representation** that restores present-time autonomy
without nearly reconstructing the source?

## Frozen candidate family

Use one additional Boolean track sampled once per macroblock:

\[
T_j=t(X_{2j-1},X_{2j},X_{2j+1}),
\]

where \(t\) ranges over all 256 elementary radius-one Boolean truth tables.

The present macro symbol is

\[
V_j=(P_j,G^\circ_{2j},G^\circ_{2j+1},T_j).
\]

Cadence remains two Rule-110 source steps.

This family is chosen because it matches the repository's established one-bit
repair-track vocabulary while storing only one extra bit per parity block.

## Gate A — autonomous local closure

For every track \(t=0,\dots,255\), test exact present-time closure at:

1. macro radius one;
2. macro radius two if radius one fails.

A radius-two test enumerates all \(2^{14}\) source words in the complete causal
window. Record every track whose entire next symbol

\[
V'_j
\]

is determined by the current radius-two \(V\) context.

Do not search radius three or richer tracks in this unit.

## Gate B — information retained by successful repairs

For every radius-two closing track, evaluate the global encoding

\[
X\mapsto(P(X),G^\circ(X),T(X))
\]

on periodic source rings of widths 12, 14 and 16.

Record:

- number of distinct encoded states;
- largest source fiber;
- complete fiber-size histogram;
- exact uniform-ensemble information loss
  \[
  H(X\mid P,G,T).
  \]

The scientific question is whether any successful present-time repair retains
a **nontrivial** source quotient rather than becoming essentially injective.

No threshold is fitted. Report the exact fiber structure.

## Decision

A meaningful middle candidate would need both:

- exact radius-\(\le2\) autonomous closure; and
- source fibers that remain substantially larger than the isolated finite
  complement pairs already seen in gradient-like repairs.

If all closing tracks are injective or differ from injectivity only on \(O(1)\)
source pairs as ring size grows, record the family as a negative: present-time
closure in this simple track grammar is purchased by restoring essentially the
microscopic state.

## Scope

- Rule 110 only;
- fixed block-2 parity observer and cadence two;
- 256 radius-one tracks sampled on even source sites only;
- macro radius at most two;
- finite-ring fiber counts at 12, 14, 16;
- no Class-IV inference;
- no search over arbitrary learned features.

## Planned artifacts

- scripts/experiment_rule110_middle_tracks.py
- results/rule110_middle_tracks_20261007.json
- integration into docs/research/2026-10-07-rule110-pg-closure.md
