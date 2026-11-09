# Terminal reporting rule: two-switch infrastructure censoring — 2026-09-10

**Status:** frozen after repeated seed-worker serialization failures and before the terminal rerun.
**Parent protocol:** `two-switch-rail-selector-20260910.md`.
**Prior resource corrections:** `two-switch-rail-selector-wall-enforcement-20260910.md`, `two-switch-rail-selector-process-wall-20260910.md`.

## Why this checkpoint exists

The frozen two-switch family contains 2,788 exact `LRL/RLR` candidates per seed across the 22 Research034 frontier seed languages. Multiple complete CI attempts reproduced passing controls and successful artifacts for most seeds, but seed workers 13 and/or 21 repeatedly exited without an artifact before the frozen 1,200-second scientific wall. Solver-granularity interruption and an outer process supervisor did not make that failure mode fully reliable.

A missing artifact is **not** a mathematical result. It must not be relabeled as `censored` under the scientific wall, and it must not block the research program indefinitely.

## Frozen terminal rule

Run the complete unchanged 22-seed census one final time with the same:

- domain and source hash;
- 2,788-candidate `LRL/RLR` family;
- candidate and output-position order;
- fine-ECA CNF semantics and scalar replay;
- Minisat22 backend;
- 1,200-second scientific wall per seed;
- Rule-204 positive and Rule-35 negative controls.

For each seed:

1. if the worker serializes `two-switch-certified`, `no-two-switch-through-6`, or scientific `censored`, retain that result exactly;
2. if the worker exits or is killed without a valid artifact, record **`infrastructure-censored`** for that seed;
3. `infrastructure-censored` is not evidence for or against any two-switch candidate and is reported separately from scientific censoring;
4. the aggregate must complete with all 22 seed identities and all 170 target questions accounted for, even when one or more seeds are infrastructure-censored;
5. no further watchdog/backend engineering is authorized for this hand-designed two-switch family after this terminal rerun.

## Decision rule

- Any exact certificate still requires independent audit before acceptance.
- If no certificate appears, publish the exact-negative and censored partitions honestly and move to the final bounded finite-state source-recoder synthesis checkpoint.
- The two-switch family is terminalized after this run regardless of outcome.
