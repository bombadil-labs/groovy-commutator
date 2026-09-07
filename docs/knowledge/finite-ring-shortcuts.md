# Finite-ring program equivalence need not generalize

For A=4 and B=30, ABBBA and AABBBA each implement the same transformation as
ABBAABBA on a six-cell periodic ring. Each equality fails on 11,264 of the
131,072 assignments to an unrestricted 17-cell causal window. The first
counterexample has integer encoding 16, with bit i denoting cell i and the
center at cell eight.

These were valid finite-ring results. They cannot be promoted to arbitrary
configurations without checking the wider scope. The
[local-map audit](../research/2026-09-07-macro-local-equivalence.md) supplies
explicit counterexamples and repeats the macro cost comparison using
programs whose equivalence holds at every ring width.
