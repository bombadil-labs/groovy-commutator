# Resource correction: supervise the two-switch SAT worker process — 2026-09-10

**Status:** frozen after the solver-interrupt rerun again failed to serialize seed 13, and before any process-supervised rerun.
**Parent protocol:** `two-switch-rail-selector-20260910.md`.
**Prior correction:** `two-switch-rail-selector-wall-enforcement-20260910.md`.

## Observed infrastructure failure

The first correction moved the frozen 1,200-second per-seed wall inside each Minisat22 solve with `solve_limited(expect_interrupt=True)` and `solver.interrupt()`. On the complete rerun, 21 of 22 seed workers serialized results, including seed 21 which had failed to serialize in the first run. Seed 13 still exited near the scientific wall without an artifact, so aggregation correctly remained blocked.

This is an execution/serialization failure, not a scientific outcome. No incomplete-run artifact is promoted to the canonical census.

## Frozen process-supervision correction

Rerun the complete 22-seed census again with the same domain, 2,788-candidate LRL/RLR family, order, SAT encoding, controls, and **1,200-second scientific wall per seed**.

Each seed worker is now a child process supervised by a small parent:

1. the child retains the existing solver-granularity 1,200-second wall;
2. the parent starts its clock before launching the child;
3. the parent may allow at most five additional seconds solely for interrupt handling, process shutdown, and JSON serialization;
4. an exact `two-switch-certified` or `no-two-switch-through-6` child result is accepted only if the parent observes completion no later than 1,200 seconds;
5. a child-reported `censored` result may be serialized during the shutdown allowance;
6. if the child is still alive after the shutdown allowance, the parent terminates it and writes a canonical `censored` result with reason `seed-wall-process-supervisor`;
7. a non-timeout child crash, malformed output, control failure, or provenance mismatch remains a CI failure and is **not** converted into censoring.

The supervisor is therefore allowed to preserve a censoring event after the wall, but never to promote computation performed after the wall into an exact scientific outcome.

## Interpretation

This changes no hypothesis, certificate family, candidate order, solver representation, or resource budget. It only makes the already-frozen seed wall robust to a SAT worker that fails to return from its interrupt path. The canonical two-switch result remains the first complete 22-seed rerun that serializes every seed as exact-negative, certified, or scientifically censored under the unchanged wall.
