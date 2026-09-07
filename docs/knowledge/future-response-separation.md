# Outcome counts, sets, and action maps can differ separately

**Exact counterexamples under declared finite actions.** Equal repertoire
sizes do not imply equal outcome sets. Equal outcome sets do not imply
equal maps from action words to outcomes.

For rules A=4 and B=30 on a six-cell ring, initial state 13 prepares states
35 and 4 under AB and BA, respectively. One continuation tick produces sets
{0,52} and {4,14}: equal cardinalities, disjoint members.

For reset A=0 and complement B=51, starting from all zeros, two continuation
ticks after either preparation reach both uniform states. Yet the word BB
preserves each prepared state, so its endpoints differ. This simple argument
works at any positive width; the enumeration independently replayed width 6.

The [experiment](../research/2026-09-07-future-repertoire.md) records these
examples and bounded counts across its full panel. They justify tracking
outcome identity and action response alongside counts. They do not imply
that more outcomes are more valuable or that these distinctions are unique
to complex cellular automata.
