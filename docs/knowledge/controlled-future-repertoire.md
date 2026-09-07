# Controlled future repertoire

For a state X, allowed actions A and B, observation O, and exactly h action
ticks, define

\[
\mathcal R_h^O(X)=\{O(F_w(X)):w\in\{A,B\}^h\}.
\]

This set records reachable observed endpoints under the declared external
choices. Its cardinality counts endpoints; its members identify them. The
word-indexed response map additionally records which sequence reaches which
endpoint.

The [finite experiment](../research/2026-09-07-future-repertoire.md) separates
these descriptions. An exactly-h budget does not imply nested sets as h
increases. Changing the action vocabulary, observation, or stopping rule
changes the definition. Comparing different rule pairs also changes the
allowed actions.

This operational definition does not by itself measure viability, autonomy,
the value of an outcome, or the ability to invent a new operation.
