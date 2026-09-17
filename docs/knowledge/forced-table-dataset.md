# The first-floor forced tables of all 256 ECAs are cached, ring-free

For each elementary rule, the affine-oriented first lift forces between 768
and 3,072 of the 2³⁵ entries of the child table (110: 1,374; 54: 1,200; 90:
3,072), computed from every nine-bit source word with no key collisions.
Every rule's key set has affine hull dimension 30, its six phase sheets are
equal in size with phase-independent `(hull, h₂, h₃)`, and the ANF degree
of the forced output is at most cubic (4 affine, 51 quadratic, 201 cubic).
Pairwise cohabitation: 30,320 of 32,640 pairs compatible, 17,926
nonvacuously; exactly reflection-invariant and complement-covariant; the
affine rules form a compatible clique. Every one of the 1,164 commuting
pairs of the full sweep cohabits, but the conflict metric's AUC for
commute-versus-rest (0.537) does not beat truth-table Hamming distance
(0.527), so the frozen bet that the lift metric predicts pair regimes
failed. On an eight-rule panel, second-floor cohabitation equals first-
floor cohabitation on all 28 pairs. Maximal-clique enumeration of the
nonvacuous graph is censored (tens of millions of cliques) and
uninformative.

Use: label-free per-rule and per-pair primitives. The `(h₂, h₃, partners)`
triple identifies the symmetry orbit, so anonymous probes must receive
coarse summaries only.

Source: [forced-table dataset](../research/2026-09-17-forced-tables.md).
