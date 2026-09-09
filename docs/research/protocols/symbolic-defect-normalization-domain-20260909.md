# Frozen domain addendum: symbolic defect normalization — 2026-09-09

**Status:** frozen after the published-control gate passed and after an input-only replay of Research034, before evaluating any rail-normalization candidate on a Research034 survivor.  
**Parent protocol:** `symbolic-defect-normalization-20260909.md`.

## Purpose

The parent protocol freezes the primary domain as the 22 distinct `(rule,seed)` languages underlying the 170 Research034 survivor target questions. This addendum records the deterministic Research034 replay used only to shard that already-published domain efficiently.

No symbolic defect-normalization outcome was computed during this replay.

## Reconstructed primary rules

Replaying `scan_research034` over all 256 ECA rules gives survivor seed languages only in:

`{122, 154, 161, 164, 166, 180, 210, 218}`.

The exact accounting is:

| Rule | Wolfram class | survivor seed languages | survivor target questions |
| ---: | :---: | ---: | ---: |
| 122 | III | 6 | 6 |
| 154 | II | 1 | 31 |
| 161 | III | 6 | 6 |
| 164 | II | 3 | 17 |
| 166 | II | 1 | 31 |
| 180 | II | 1 | 31 |
| 210 | II | 1 | 31 |
| 218 | II | 3 | 17 |
| **Total** |  | **22** | **170** |

Thus the target-question class split is exactly **158 Class II + 12 Class III**, matching Research034 and Note 036.

## Sharding rule

Run one primary shard for each of the eight rules above. The aggregate must require exactly this rule set and must again assert:

- 22 seed languages;
- 170 target questions;
- 158 Class II target questions;
- 12 Class III target questions.

Any mismatch invalidates the primary aggregate.

The rule list is an execution partition of the previously frozen domain, not a new scientific filter. Do not add or remove a rule after normalization outcomes are inspected.
