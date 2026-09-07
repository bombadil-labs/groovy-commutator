# Compare fixed and revisable compiled primitives

**Completed bounded implementation, 2026-09-07.** The original
[proposal](../research/2026-09-07-revisable-primitives.md) became an exact
oracle resource model comparing primitive-only, frozen, replacement, and
revisable libraries. It explicitly prices compilation, physical execution,
dispatch, retained traces, and patches. All arms retain the base operations.

The [first experiment](../research/2026-09-07-costed-primitives.md) enumerates
294,912 configurations on three ring widths. The
[local-map follow-up](../research/2026-09-07-macro-local-equivalence.md)
repeats 98,304 configurations with program equivalences valid at every width.
Revision's advantage is narrow and price-dependent; finite-size shortcuts
are preserved with their failed generalizations.

The implementation assumes known dynamics, free planning, given inherited
constructions, and one library transition. It does not execute the broader
proposal's learning/discovery component. Repeated changes and returning tasks
are the next extension.
