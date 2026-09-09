# An encoding cannot supply independent area information from a linear input footprint

If an n-by-n target patch is determined by a fixed set of at most Cn source sites over a finite alphabet A, it can take at most |A|^(Cn) values. Its information per target area therefore tends to zero.

The quotient-stripe encoding has exactly 2^(2n-1) possible n-by-n patches. A fixed-interface two-rail patch has exactly 2^n. Both counts are proved and enumerated in the [research checkpoint](../research/2026-09-09-program-edit-locality.md).

The statement depends on the footprint assumption. Additional independent fields, a larger source footprint, or a different resource-accounted construction changes the problem. Zero area information does not imply simple temporal dynamics or absence of meaningful spatial organization.

The [intertwining baseline](../research/2026-09-09-dimensional-intertwining.md) and [routing control](../research/2026-09-09-selector-two-lift.md) remain valid. Their ambient stencil geometry should not be conflated with independent area information.
