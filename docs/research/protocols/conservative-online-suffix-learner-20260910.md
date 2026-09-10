# Protocol: conservative online suffix learner — 2026-09-10

**Status:** implementation contract frozen before any new research evaluation.  
**Issue:** #64.  
**Scope:** online suffix learner only. Coarsening/merge and the oracle-assisted partition learner are deferred.

## Purpose

Implement the agreed conservative learner as a concrete research instrument without attaching the withdrawn Research023 visibility-depth or optimality claims to it. The harness owns concrete states and dynamics. The learner receives only the declared observation sequence.

This unit is an implementation note, not a new ECA census. Explicit deterministic traces are implementation checks, not research evaluation.

## Frozen learner state

At training time the learner stores:

- a global suffix depth `h`, initialized to `1` and never decreased;
- retained raw observation history `raw`;
- a table from length-`h` suffix keys to the **set** of observed successor observations;
- counters for prediction outcomes, rebuilds, and actual work/storage.

No padding is used. A key exists only when at least `h` current/history observations are available.

A key with no recorded successor produces `ABSTAIN_UNSEEN`. A key with more than one recorded successor produces `ABSTAIN_CONFLICT`. A key with exactly one recorded successor makes that definite prediction.

## Frozen update order

For each concrete transition `S_t -> S_{t+1}` the harness:

1. exposes `y_t = P(S_t)` to the learner;
2. the learner appends `y_t` to retained history and predicts **before** seeing `y_{t+1}`;
3. the harness advances the concrete dynamics exactly once and exposes `y_{t+1}`;
4. the learner scores the old prediction against `y_{t+1}`;
5. the learner records `key -> y_{t+1}` under the current depth;
6. **only if a definite prediction was wrong**, increment `h` by one and rebuild the table from the retained history plus the just-seen `y_{t+1}`.

Already-conflicting keys may therefore continue to cause abstention indefinitely. That is intentional. No eventual determinization, minimum-depth, or optimality claim follows.

The just-seen `y_{t+1}` is carried forward as the next current observation by the harness. The concrete transition function is not called again merely to obtain that observation.

## Rebuild semantics

A rebuild at depth `h` scans the available observation sequence once by start index. For every full window of `h` observations followed by a successor, insert that successor in the set for the corresponding tuple key.

Retained history is **not reset** on rebuild. Consequently a rebuild does not imply `h-1` fresh startup abstentions. Startup abstention is determined only by the actual `len(history) < h` test.

## Held-out evaluation

After training, freeze exactly:

- the final global `h`;
- an immutable copy of the training successor table.

For every held-out seed/state trajectory:

- start a **fresh empty raw history**;
- keep the frozen training `h` and table;
- run the same predict-before-outcome ordering;
- disable recording, refinement, and rebuilds;
- advance the concrete harness exactly once per scored prediction.

Held-out evaluation reports the same prediction outcomes and resource accounting, but cannot mutate the frozen training model.

## Resource accounting

Report actual counts rather than asymptotic claims:

### Current storage

- retained training-history symbols;
- table key count;
- total symbols stored across tuple keys;
- total distinct successor entries across all keys.

### Cumulative work

- predictions attempted;
- key symbols materialized for prediction;
- training record operations;
- successor insertions that changed a table set;
- rebuild count;
- rebuild windows scanned;
- tuple-key symbols materialized during rebuilds;
- rebuild successor insertions.

Held-out runs report local history retained during that evaluation and key-materialization work while leaving training storage unchanged.

## Explicit implementation checks

Before this instrument is used for new research evaluation, a deterministic check script must cover at least:

1. **predict before record:** a previously learned singleton can be contradicted and is scored wrong before the new successor is inserted;
2. **refine only on wrong definite prediction:** unseen and conflict abstentions never trigger refinement;
3. **history survives rebuild:** increasing `h` reconstructs keys from earlier observations instead of resetting history;
4. **held-out freeze:** evaluation starts with fresh history and cannot alter frozen training depth/table;
5. **single harness advance:** exactly one concrete transition call occurs per prediction;
6. **resource accounting:** exact storage/work counters match hand-checkable traces.

These are implementation tests only. They do not count as evidence about ECA behavior.

## Deferred work

Not part of this issue deliverable:

- any `k`-step coarsening or merge heuristic;
- a variable-depth suffix tree;
- the oracle-assisted partition learner;
- class identities across oracle splits/merges;
- a theorem relating suffix depth to Research023 memory/visibility depth;
- claims of eventual determinization or optimality;
- a new Rule106 or Research028 evaluation.

Any such extension requires its own frozen protocol or explicit issue-scope change.
