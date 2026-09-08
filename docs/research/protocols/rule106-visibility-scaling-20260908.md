# Fresh Rule-106 hidden-defect lifetime scaling protocol — 2026-09-08

**Status:** frozen after exploratory inspection of even ring widths `n=12..100`, before evaluating any `n>=102`.

## Fixed pair and observer

Use ECA Rule 106 on an even periodic ring, sampled every two fine steps (`q=2`). Observe nonoverlapping block-2 parity. Compare initial microstates

- `a=25`, occupied sites `{0,3,4}`;
- `b=26`, occupied sites `{1,3,4}`.

Their initial difference is the observer-null adjacent block flip `{0,1}`.

Let `tau(n)` be the first macro time at which their block-parity observations differ.

## Discovery pattern

Direct pair evolution on every even width `12 <= n <= 100` produced a piecewise arithmetic staircase. Group widths in triples

\[
n\in\{12+6m,14+6m,16+6m\},\qquad m\ge0.
\]

Freeze the prediction

\[
\tau(n)=n+a_m,
\]

where

\[
a_0=1
\]

and, for `m>=1`,

\[
a_m=a_{m-1}+8\,4^{\nu_2(m+1)}-2.
\]

Here `nu_2(k)` is the exponent of 2 dividing `k`.

The first offsets are

`1,31,37,163,169,199,205,715,721,751,757,883,889,919,925,...`.

The increment sequence is therefore a 2-adic ruler pattern:

`30,6,126,6,30,6,510,6,30,6,126,...`.

No all-width theorem is claimed from discovery.

## Fresh domain

Evaluate every even ring width

\[
102\le n\le200.
\]

For each width:

1. evolve the fixed pair under Rule 106 with a direct periodic bit-vector implementation independent of the exhaustive state-map machinery;
2. require block-parity equality for every macro time `0 <= t < tau_pred(n)`;
3. require the first inequality exactly at `tau_pred(n)`.

The implementation should use the exact Rule-106 identity

\[
E_{106}(S)_i=S_{i+1}\oplus(S_{i-1}S_i)
\]

rather than a fitted transition table.

## Acceptance

The frozen scaling law passes only if all 50 fresh even widths split for the first time at the predicted time. Report every mismatch; do not repair the recurrence after evaluation.

## Nonclaims

A successful finite fresh-range test does not prove the recurrence for arbitrary ring width or the infinite lattice. The pattern may reflect periodic-ring arithmetic rather than an intrinsic infinite-system timescale. A proof would require a separate analysis of the moving defect and shared context dynamics.
