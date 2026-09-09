# Protocol correction: finite-horizon partition-order notation — 2026-09-09

**Status:** frozen before CI confirmation and before the `n=15` fresh-size evaluation.  
**Applies to:** `finite-horizon-quotients-20260909.md`.

The primary protocol defines

\[
P\preceq Q
\]

to mean **`Q` refines `P`**.

In the “Sound edit certification” section, the prose correctly states the intended condition:

> if `Q_h` refines a candidate local partition `Z`, then `Q_infinity` also refines `Z`, so `Z` is finally safe.

One boxed formula reverses that order symbol. The correct implication is

\[
\boxed{Z\preceq Q_h\;\Longrightarrow\;Z\text{ is finally safe}.}
\]

Equivalently, in words:

\[
Q_h\text{ refines }Z\;\Longrightarrow\;Q_\infty\text{ refines }Z.
\]

This is a notation-only correction. It does not change the intended theorem, measurements, hypotheses, code-level refinement predicate, or acceptance criteria.
