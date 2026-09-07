# Operation order and future repertoire: frozen protocol

This protocol is committed before the full experiment is run. Its
[machine-readable configuration](future-repertoire-20260907.json) fixes the
panel, rings, horizons, observations, metrics, and witness-selection rule.

For every initial state S on rings of width 6, 9, and 11, prepare
X = B(A(S)) and Y = A(B(S)). Here AB means the chronological sequence A then B,
so it is the composed map B after A. Use all 66 distinct pairs from the
declared 12-rule panel. The panel includes familiar nonlinear rules, additive
rules, shift/identity/complement controls, and the previously studied 184/250
drain pair; it is not a random or class-balanced sample of rule space.

For each prepared state and horizon h from 0 through 6, enumerate every word
of exactly h actions from {A,B}. Each action applies that rule synchronously
to the whole ring. There is no early stopping, action cost asymmetry, learned
controller, or intervention between cells within a tick.

Let F_w(X) be the endpoint after word w and let O be either the identity
observation or the population count. Define

\[
\mathcal R_h^O(X)=\{O(F_w(X)):w\in\{A,B\}^h\}.
\]

Compare X with Y, their sets of endpoints, and the word-indexed response maps
w to O(F_w(X)) and w to O(F_w(Y)). These are three distinct objects. The
primary readout is full-state repertoire at h=6; other horizons and population
count are declared diagnostic views. Cardinality alone discards which outcomes
exist; a set also discards which action word reaches which outcome.

Jaccard distance is one minus intersection size divided by union size. The
sets are never empty, since the empty word exists at h=0 and at least one
word exists at every later horizon. Record strict inclusion in each direction,
incomparability, equal-size/different-set cases, and equal-set/different-map
cases. Save the first witness of each declared type in lexicographic order.

Use exact integer counts, not confidence intervals over enumerated states.
Different horizons share data and rule pairs share rules. Compare widths
separately. A directional advantage under A<B is an ordering convention, not
a universal preference for one preparation.

## Interpretation boundary

This is a controlled finite system. The alternative futures come from the
declared external action choices. It does not measure viability, intrinsic
agency, or an ability to invent new actions. Differing histories have their
effects through differing complete present states. Identical complete states
must have identical future responses under the same continuation rules.

The experiment asks whether present-state discrepancy, available outcomes,
and response to action should be tracked separately. A positive separation
would justify a new instrument, not a scalar definition of wetness.
