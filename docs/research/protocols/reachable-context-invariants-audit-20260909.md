# Audit protocol: Research033 reachable-context invariants — 2026-09-09

**Status:** frozen after the primary exact census and before independent reconstruction.  
**Branch:** `research/reachable-context-invariants-20260909`.  
**Primary CI run:** `34381030169`.

## Primary result being audited

The frozen Research033 census reproduced the Research032 baseline exactly and found:

- 5,360 non-congruence residual pair/target distinctions;
- **0** new generated-symbol certificates;
- **5,132** adjacency-aware generated-edge certificates;
- **228** cases still unresolved after edge closure.

The first preregistered hypothesis therefore failed; the second passed.

This audit freezes representative cases before using an independent implementation.

## Independent implementation boundary

The audit must not import:

- `experiment_reachable_context_invariants.py`;
- its generated-symbol closure helper;
- its generated-edge closure helper;
- its paired-rule table.

Rebuild the block-3/cadence-3 macro rule directly from the original ECA lookup table, then construct the paired rule independently with scalar tuples/sets.

For every case:

1. reconstruct the generated symbol fixed point from diagonal paired symbols plus the seed;
2. reconstruct the nearest-neighbor edge fixed point from all diagonal-diagonal edges plus diagonal-seed and seed-diagonal edges;
3. verify fixed-point closure directly;
4. evaluate target visibility of every admitted paired symbol.

## Case A — first edge-only certificate

Freeze the lexicographically first new Research033 certificate:

- ECA Rule **1**;
- target `01001100` (primary target id 102);
- seed pair `0-2`;
- generated-symbol closure: **48 symbols**, **4 rounds**, target-unsafe;
- generated-edge closure: **153 edges**, **3 rounds**, target-safe.

Prediction: the independent reconstruction reproduces all counts and proves the edge shift contains no target-visible paired symbol.

This is the primary mechanism case showing that spatial adjacency removes spurious all-context combinations.

## Case B — first edge-language failure

Freeze the lexicographically first case still unresolved after edge closure:

- ECA Rule **5**;
- target `01001100` (primary target id 102);
- seed pair `0-2`;
- generated-symbol closure: **64 symbols**, **3 rounds**;
- generated-edge closure: **230 edges**, **4 rounds**;
- edge certificate fails because the generated edge language contains at least one target-visible paired symbol.

Prediction: the independent reconstruction reproduces those counts and the failed safety condition.

This is a negative control only. It does not assert that Rule 5 has a finite causal witness at horizon 7+.

## Cases C — Research032 Rule-122 sentinel family

Target `00100000`; all generated-symbol closures contain 64 symbols in 3 rounds and all remain unresolved after edge closure.

Freeze:

| seed pair | edge count | edge rounds |
| --- | ---: | ---: |
| `1-4` | 3528 | 6 |
| `1-5` | 3523 | 6 |
| `3-6` | 3520 | 6 |
| `3-7` | 3520 | 6 |
| `4-5` | 3523 | 6 |
| `6-7` | 3520 | 6 |

Prediction: every independent edge closure reproduces its frozen count and remains target-unsafe.

## Cases D — Research032 Rule-161 sentinel family

Target `00000100`; all generated-symbol closures contain 64 symbols in 3 rounds and all remain unresolved after edge closure.

Freeze:

| seed pair | edge count | edge rounds |
| --- | ---: | ---: |
| `0-1` | 3520 | 6 |
| `0-4` | 3520 | 6 |
| `1-4` | 3520 | 6 |
| `2-3` | 3523 | 6 |
| `2-6` | 3523 | 6 |
| `3-6` | 3528 | 6 |

Prediction: every independent edge closure reproduces its frozen count and remains target-unsafe.

## Acceptance

The audit passes only if all 14 frozen cases reproduce:

- symbol count and rounds;
- edge count and rounds;
- direct closure of the final symbol/edge language;
- the frozen safe/unsafe classification.

Any mismatch blocks publication and requires investigation before changing either implementation or interpretation.
