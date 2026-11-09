# Resource correction: enforce the two-switch seed wall inside SAT — 2026-09-10

**Status:** frozen after the first 22-way run failed to serialize seed jobs 13 and 21, and before any rerun under this correction.
**Parent protocol:** `two-switch-rail-selector-20260910.md`.

## Observed operational failure

The frozen parent protocol sets a **1,200-second wall per seed language**. The first CI implementation checked that wall before each candidate and output-position query, but called Minisat22 with an uninterruptible `solve()`. Consequently, a SAT call already in progress at the deadline could continue past the scientific wall. Twenty jobs serialized results; seed jobs 13 and 21 terminated without artifacts near the wall, so the aggregate correctly did not run.

No candidate family, seed domain, target domain, candidate order, position order, certificate criterion, or scientific outcome is changed here. No individual seed artifact from the incomplete run is used as the canonical result.

## Frozen correction

Rerun the **entire 22-seed census** from the same committed domain and candidate family.

For every output-position SAT query:

1. compute the remaining time to the seed's original 1,200-second deadline;
2. if no time remains before the solve starts, return `censored`;
3. otherwise call PySAT/Minisat22 through interruptible `solve_limited(expect_interrupt=True)`;
4. arm a timer for exactly the remaining seed time and call `solver.interrupt()` when it expires;
5. if the solver returns `None`, record `censored` with reason `seed-wall-time-during-solve`;
6. only SAT and UNSAT returned before the deadline count as exact query outcomes;
7. SAT models retain the existing independent scalar replay requirement.

GitHub's job timeout remains looser than the scientific wall and is only an infrastructure backstop.

## Interpretation

This correction makes the already-frozen resource limit executable at solver granularity. It does **not** grant more computation and cannot turn a censored candidate into a certificate or exact negative after the wall. The canonical two-switch result is the complete rerun under this corrected wall enforcement.
