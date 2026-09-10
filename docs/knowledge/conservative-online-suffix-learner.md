# Conservative online suffix learner

**Status:** implemented research instrument; no new CA evaluation in this checkpoint.  
**Protocol:** [conservative-online-suffix-learner-20260910.md](../research/protocols/conservative-online-suffix-learner-20260910.md).  
**Checkpoint:** [2026-09-10-conservative-online-suffix-learner.md](../research/2026-09-10-conservative-online-suffix-learner.md).  
**Issue:** #64.

The learner keeps a single global suffix depth and a successor-set table over observed histories. It predicts before the next observation is delivered. Unseen and conflicting keys cause abstention. Only a wrong definite prediction raises the suffix depth; rebuilding reuses retained raw observation history.

A frozen held-out model carries only the learned depth and table. Each held-out trajectory starts a fresh observation history and cannot modify the training model. The harness advances the concrete dynamics exactly once per scored prediction. Storage and work are reported as concrete counts rather than asymptotic claims.

This is not the Research023 future-relation chain, and no theorem equates suffix depth with visibility or memory depth. Coarsening/merge and the oracle-assisted partition learner remain deferred.
