# Fresh-size validation: finite-horizon quotient discovery at n=15 — 2026-09-09

**Status:** frozen after the exact `n=12` discovery census and before evaluating any selected case at `n=15`.  
**Branch:** `research/finite-horizon-quotients-20260909`.

## Purpose

The primary `n=12` census found an unexpectedly large separation between the horizon required to discover the final **local future-context quotient** and the horizon required to recover the complete **global predictive state**.

Across the discovery domain, every nonclosed block-3 target reached its final local quotient by macrostep 2, and 29,480/30,856 reached it by macrostep 1. Long-memory examples were especially extreme.

This fresh-size check asks whether selected examples preserve that separation on the periodic 15-cell ring without reselecting targets after inspection.

## Fixed setup

- periodic ECA ring width `n=15`;
- nonoverlapping block size 3, so five local blocks;
- matched cadence `q=3`;
- uniform ensemble over all `2^15=32,768` microscopic states;
- exact future partition refinement and exact context substitution.

## Frozen cases and predictions

| Rule | Target | n=12 `h*` | n=12 `d_Q` | n=15 prediction |
| ---: | --- | ---: | ---: | --- |
| 101 | `00000010` | 23 | 1 | `d_Q=1` and `d_Q<h*` |
| 106 | `00000001` | 19 | 1 | `d_Q=1` and `d_Q<h*` |
| 110 | `00000100` | 13 | 1 | `d_Q=1` and `d_Q<h*` |
| 90 | `00110011` | 2 | 2 | `d_Q=2` |
| 24 | `01000010` | 1 | 1 | `d_Q=1` |
| 184 | `00000001` | 2 | 1 | `d_Q=1` and `d_Q<h*` |

The three long-memory predictions for Rules 101, 106, and 110 are the primary fresh-size test. All three must preserve `d_Q=1` with `h*>1` to pass the primary prediction.

Rule90 is deliberately stronger and may fail: it tests whether one of the rare two-step quotient-discovery cases remains genuinely two-step at a larger ring rather than collapsing to one-step discovery.

## Measurements

For each fixed case record:

- exact `hstar`;
- exact `quotient_discovery_time`;
- final quotient;
- quotient change chain;
- local quotient entropy at each change;
- `d_Q/h*` when nonclosed;
- horizons for 50%, 90%, and 100% of final representation information.

## Acceptance

Primary fresh-size validation passes only if Rules 101, 106, and 110 all have:

\[
d_Q=1<h^*.
\]

The other three predictions are retained individually and do not alter the primary acceptance criterion.

## Nonclaims

- Six fixed targets do not establish all-width stability.
- A pass does not imply every block-3 target has `d_Q<=2` at `n=15`.
- Exactness is for the finite periodic 15-cell ring only.
- Do not replace a failed target with a newly selected example after evaluation.
