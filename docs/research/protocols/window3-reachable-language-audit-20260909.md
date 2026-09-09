# Audit protocol: Research034 width-3 reachable language — 2026-09-09

**Status:** frozen after exact primary census run `34384109852` and before independent width-3 reconstruction.  
**Branch:** `research/window3-reachable-language-20260909`.

## Primary result being audited

The exact Research034 census reproduces the Research033 baseline and finds:

- Research033 edge survivors: **228**;
- new width-3 all-time permanence certificates: **58**;
- remaining after width 3: **170**;
- resolved fraction of the edge residue: **25.438596%**;
- all 58 new certificates use repository Class II rules;
- the 170 survivors split into 158 Class II + 12 Class III.

Both preregistered hypotheses pass:

1. width 3 strictly improves on nearest-neighbor edges;
2. Rule 5 / target `01001100` / seed `0-2` is certified safe at width 3.

## Independent implementation boundary

The audit must not import:

- `experiment_window3_reachable_language.py`;
- its `initial_window3`, `window3_step`, or `window3_closure` helpers;
- its row-bitset representation.

Rebuild the block-3/cadence-3 macro rule directly from the original fine ECA lookup table, construct the paired rule independently, and represent the width-3 language as a dense Boolean tensor of shape `(64,64,64)`.

For each frozen case:

1. construct the exact 704-word initial overapproximation;
2. close under every admitted length-5 de Bruijn path using the dense-tensor implementation;
3. verify the final word count and round count;
4. directly verify fixed-point closure;
5. evaluate target visibility of every admitted paired symbol.

## Case A — Rule-5 mechanism rescue

Freeze:

- ECA Rule **5**;
- target `01001100`;
- seed `0-2`;
- Research033 edge language: 230 edges in 4 rounds, target-unsafe;
- Research034 width-3 language: **1,162 words in 3 rounds**;
- width-3 vertex count: **16**;
- target-safe: **true**.

Prediction: the independent tensor construction reproduces all width-3 counts and the safety result.

This is the main mechanism case: individually permitted edges can splice into a target-visible context, while admitted 3-words forbid the required phrase.

## Case B — first width-3 survivor

Freeze:

- ECA Rule **122**;
- target `00100000`;
- seed `1-4`;
- width-3 language: **138,795 words in 8 rounds**;
- width-3 vertex count: **64**;
- target-safe: **false**.

Prediction: the independent tensor construction reproduces the count and failed safety condition.

This case is also part of the Rule-122 sentinel family below.

## Rule-122 sentinel family

Target `00100000`; all remain unresolved at width 3.

| seed | width-3 words | rounds | vertices |
| --- | ---: | ---: | ---: |
| `1-4` | 138,795 | 8 | 64 |
| `1-5` | 138,676 | 8 | 64 |
| `3-6` | 138,591 | 8 | 64 |
| `3-7` | 138,626 | 8 | 64 |
| `4-5` | 138,676 | 8 | 64 |
| `6-7` | 138,626 | 8 | 64 |

Every case must remain target-unsafe.

## Rule-161 sentinel family

Target `00000100`; all remain unresolved at width 3.

| seed | width-3 words | rounds | vertices |
| --- | ---: | ---: | ---: |
| `0-1` | 138,626 | 8 | 64 |
| `0-4` | 138,626 | 8 | 64 |
| `1-4` | 138,591 | 8 | 64 |
| `2-3` | 138,676 | 8 | 64 |
| `2-6` | 138,676 | 8 | 64 |
| `3-6` | 138,795 | 8 | 64 |

Every case must remain target-unsafe.

## Acceptance

The audit passes only if all 13 unique frozen cases (Rule 5 plus twelve Rule-122/161 sentinels) reproduce:

- 704 initial words;
- exact final word count;
- exact closure round count;
- direct fixed-point closure;
- exact safe/unsafe classification;
- exact admitted vertex count.

Any mismatch blocks publication and must be investigated before changing either the primary or independent implementation.
