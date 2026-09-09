# Follow-up protocol: horizon-3 causal-witness counterexamples — 2026-09-09

**Status:** frozen after the complete local h<=3 census and before any selected-case witness reconstruction or larger-ring evaluation.  
**Branch:** `research/causal-witness-horizon-20260909`.

## Discovery result being frozen

The exact wrap-free local-cone census over all 256 ECA rules × 127 canonical binary block-3 targets found exactly four symbol-pair/target distinctions whose first causal witness occurs at macro-horizon 3:

| Rule | Target | Pair | Local quotient chain h=0..3 |
| ---: | --- | --- | --- |
| 35 | `00000001` | `2-6` | `00000001 -> 01234325 -> 01234526 -> 01234567` |
| 49 | `00000001` | `2-3` | `00000001 -> 01223445 -> 01223456 -> 01234567` |
| 59 | `01111111` | `1-5` | `01111111 -> 01232145 -> 01234156 -> 01234567` |
| 115 | `01111111` | `4-5` | `01111111 -> 01123345 -> 01234456 -> 01234567` |

The same census found 54 rule/target mismatches between the wrap-free local quotient and the four-macroblock periodic-ring quotient already at horizon 2, and 58 by horizon 3.

This falsifies the proposed system-size-independent `d_Q<=2` interpretation of Research030.

## Independent explicit witness audit

For each of the four frozen cases, an independently written implementation must:

1. reconstruct the exact induced radius-1 8-symbol macro rule from the original ECA without importing the primary Research031 witness helper;
2. exhaustively verify **no** context witnesses the frozen pair through horizons 0, 1, or 2;
3. find and save at least one explicit length-7 macro context in which replacing the frozen pair at one position changes the binary target at some output site after exactly 3 macrosteps;
4. verify the same witness directly at the fine ECA level over the corresponding 21-cell dependency word and 9 fine ticks;
5. record the changed output block symbols and target values.

Any failure invalidates the corresponding primary counterexample.

## Frozen periodic-size controls

Evaluate exactly the four frozen rule/target cases on periodic macro-rings of:

- `m=4` blocks (`n=12` fine cells), reproducing the original Research030 topology;
- `m=5` blocks (`n=15`);
- `m=6` blocks (`n=18`);
- `m=7` blocks (`n=21`).

Use the exact induced macro rule rather than enumerating the fine ECA when convenient; macro/fine equality is already an exact control and must be rechecked on selected states.

For each size record the quotient chain through horizon 3 and the first horizon at which the frozen pair is separated.

### Frozen predictions

- `m=4`: all four frozen pairs remain merged through horizon 3, reproducing the finite-ring miss.
- `m=7`: all four pairs separate by horizon 3, because a full seven-block horizon-3 dependency word embeds without periodic identification.
- No directional prediction is made for `m=5` or `m=6`; retain their outcomes.

Do not reselect cases after inspection.

## Symmetry audit

After the four cases are independently confirmed, test whether they form one or more standard ECA reflection/complement/conjugacy orbits. This is descriptive and must not be used to discard nonindependent cases from the exact census count.

## Decision rule

If all four counterexamples survive the independent and `m=7` checks, Research031 establishes that causal witness depth can exceed 2 in the matched block-3 ECA family and that the four-block periodic ring systematically underestimates some local predictive distinctions.

The next theoretical target is then **not** another larger-ring census. It is a finite-state/de-Bruijn method for extending causal witness search beyond horizon 3 without enumerating all `8^(2h+1)` contexts, followed by a search for the actual maximum witness horizon in this family.