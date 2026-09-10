# Conservative online suffix learner: implementation checkpoint

Issue #64's agreed online arm is implemented as a deliberately conservative sequence learner. This checkpoint records an instrument, **not a new cellular-automaton result**.

The frozen contract is in [protocols/conservative-online-suffix-learner-20260910.md](protocols/conservative-online-suffix-learner-20260910.md). The implementation lives in [src/groovy/online_suffix.py](../../src/groovy/online_suffix.py); [scripts/check_conservative_online_suffix.py](../../scripts/check_conservative_online_suffix.py) exercises hand-checkable traces.

The learner keeps one global suffix depth and a successor-set table. It predicts before recording the new successor. An unseen key or an already-conflicting key causes abstention. Only a wrong **definite** prediction raises the depth, after which the table is rebuilt from retained raw history. History is not reset by refinement.

Held-out evaluation freezes the training depth and table, starts a fresh history for each held-out trajectory, and disables recording/refinement. The concrete harness advances exactly once per prediction and exposes only observations to the learner.

The instrument reports actual storage and work counts: retained history, table keys/key symbols/successor entries, prediction key materialization, record operations, changed successor insertions, rebuild windows/key symbols, and rebuild insertions.

The deterministic checks cover predict-before-record ordering, refinement gating, retained history, frozen held-out state, single harness advancement and exact resource counters. They are implementation tests only; no Rule106, Research028, or broader ECA evaluation is performed here.

Coarsening/merge, variable-depth trees, the oracle-assisted partition learner, and any theorem relating suffix depth to Research023 visibility/memory depth remain explicitly deferred. No eventual-determinization or optimality claim is made.

## Integration review

The final implementation constructs each prediction key once and reuses it for recording, so key-symbol accounting covers the actual tuple construction. Directly constructed frozen models defensively copy caller-owned mappings and successor sets, as does the training freeze path. Focused checks cover both contracts.

Primary review also compared every length-eight binary observation trace against an independent prefix-table reference: all 256 traces agreed on predictions, refinement depth, successor tables and prediction key-symbol counts. This is bounded implementation validation on abstract sequences, not a new CA research result.
