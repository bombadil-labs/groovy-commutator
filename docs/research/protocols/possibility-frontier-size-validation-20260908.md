# Fresh-size possibility-frontier validation — 2026-09-08

**Status:** frozen after the preregistered `n=12` census and before evaluating `n=18` for the cases below.

## Purpose

The `n=12` possibility-frontier census found that the observer minimizing closure-breaking forgetting usually differs from the observer maximizing future repertoire. This follow-up does not re-optimize at a new size. It asks whether the **ordering of the already-selected observers** survives on a fresh larger ring.

## Fixed cases

Use periodic ECA rings of width `n=18`, exact exhaustive state spaces, and the same matched cadences as the discovery census.

The observers below were selected by the frozen `n=12` objectives before this protocol was written:

| Fine rule | Minimum-forgetting closure breaker at n=12 | Maximum-repertoire observer at n=12 |
| ---: | --- | --- |
| 30 | block2 truth table 3 | block3 truth table 1 |
| 54 | block2 truth table 3 | block3 truth table 1 |
| 90 | block2 truth table 7 | block3 truth table 30 |
| 106 | block2 truth table 6 | block3 truth table 127 |
| 110 | block2 truth table 3 | block3 truth table 64 |
| 184 | block2 truth table 3 | block2 truth table 4 |

Truth-table integers use the same little-endian neighborhood-code convention as the Research026 primary experiment. Output complements are equivalent relabelings and are not separately tested.

## Frozen predictions

For every one of the six fine rules:

1. both fixed observations remain nonclosed at `n=18`;
2. the fixed `n=12` maximum-repertoire observer still has strictly greater
   
   \[
   V_\infty=H(C_\infty\mid Y_0)
   \]
   
   than the fixed minimum-forgetting closure breaker;
3. the minimum-forgetting observer still forgets fewer bits than the maximum-repertoire observer. For Rule 184 this is not a block-size tautology: both are block-2 maps with different output balance.

Record `forgotten_bits`, `future_repertoire_bits`, `shielded_bits`, `possibility_efficiency`, and `hstar` for both fixed observers.

## Acceptance

The six-case ordering prediction passes only if all six satisfy prediction 2 exactly as stated. Individual failures are retained; do not substitute a newly optimized `n=18` observer after evaluation.

## Nonclaims

- A pass does not show that the global optimum observer itself is size-invariant.
- This is a targeted robustness check, not a fresh 256-rule census.
- Exactness is for the `n=18` periodic ring only.