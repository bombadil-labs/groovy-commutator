# Correction protocol: Research033 generated-symbol index width — 2026-09-09

**Status:** frozen after independent audit exposed the bug and before rerunning the primary census.  
**Branch:** `research/reachable-context-invariants-20260909`.

## What failed

The first independent scalar audit reproduced the Research033 edge-language counts and safety classifications exactly, including:

- Rule 1 / target `01001100` / seed `0-2`: 153 edges, 3 rounds, target-safe;
- Rule 5 / same target and seed: 230 edges, 4 rounds, target-unsafe;
- all twelve Rule-122/161 sentinel edge counts and safety failures.

But it disagreed with the primary generated-symbol **round counts** for Rules 1 and 5.

Inspection found an implementation bug in the primary symbol closure: paired-symbol IDs were stored as `int16`, so the flattened lookup expression

`4096*x + 64*y + z`

could overflow for IDs above 7 before indexing the 64^3 paired-rule table.

## Scope

The bug affects only `generated_symbol_closure` in `experiment_reachable_context_invariants.py`.

The edge closure uses `np.argwhere` / `np.flatnonzero` indices with platform integer width and does not use the overflowing `int16` flattened triple arithmetic. The independent scalar audit reproduced every frozen edge count it checked, but the entire primary census will still be rerun after the fix.

## Fixed implementation

Store generated symbol IDs in `np.intp` before forming flattened triple indices.

Do not change:

- the frozen Research033 scientific protocol;
- the Research032 residual family;
- the edge-language definition;
- the frozen hypotheses;
- the sharding or aggregation rules.

## Rerun requirement

Rerun all 256 rules from the corrected source hash.

Before interpreting the corrected result, the aggregate must again reproduce exactly:

- 52,712 finite-witness-absent cases through h=6;
- 47,352 Research032 congruence certificates;
- 5,360 non-congruence residual cases.

The corrected run supersedes the preliminary Research033 aggregate from Actions run `34381030169` for every generated-symbol measurement. Edge-language counts from that run remain preliminary until the corrected full rerun agrees.

After the corrected aggregate is promoted, update the audit expectations from that result and rerun the independent scalar audit. Preserve this correction in the publication note.
