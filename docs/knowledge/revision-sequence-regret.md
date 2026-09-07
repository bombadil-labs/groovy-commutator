# A locally cheaper revision can cost more after a return

For rules 4/30, inherited AABB, target ABAB, dispatch price one, and a free
trace, a reactive revision costs fifteen on a changed job where retaining
the old macro costs sixteen. When the old task returns, the revised path
costs twelve instead of ten. It loses one unit over the two jobs.

The [replayed example](../research/2026-09-07-returning-tasks.md) isolates a
sequence effect from the cost of retaining a trace. The former transformation
remains reachable; its cost changes. A full-hindsight planner keeps AABB.

More available revision operations weakly help an oracle with a free trace,
but a reactive policy need not use those operations well over time. This is
a bounded counterexample, not a theorem that revision usually harms adaptation.
