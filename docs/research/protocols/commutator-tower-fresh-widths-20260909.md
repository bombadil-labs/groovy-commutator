# Protocol: fresh-width robustness of the commutator tower

Date: 2026-09-09
Status: preregistered before evaluation

## Motivation

On the complete width-eight ECA substrate, 67 rules have no repeated correction map through tower level 256. Both frozen Class-IV starter exemplars (54 and 110) lie in that set, but so does Class-III Rule 30 and many unlabeled rules.

The tower protocol requires a fresh finite-size test before treating long tower depth as an intrinsic property.

## Frozen fresh widths

Evaluate periodic ECA rings of widths

\[
7,\quad 9,\quad 10.
\]

These are fixed before outcomes and provide two odd sizes and one even size around the original width eight.

Use the same tower horizon

\[
A_1,\ldots,A_{256}
\]

and the same recurrence as the original protocol:

\[
A_1(S)=S\oplus F(S),
\]

\[
A_{k+1}(S)=A_k(F(S))\oplus F(A_k(S)).
\]

No Wolfram class labels are loaded by the evaluator.

## Complete source family

Evaluate all 256 elementary rules at every fresh width, on the complete periodic state space of size `2^n`.

For each `(rule,width)` record:

- first zero level;
- first constant level;
- first exact functional repeat before or at level 256;
- number of distinct maps before repeat/horizon;
- right-censored status at level 256.

## Cross-width structural outputs

For every rule, record its four-width right-censored signature over widths

\[
7,8,9,10,
\]

where width eight uses the already frozen original result.

Primary summaries:

1. rules right-censored at **all four widths**;
2. rules right-censored at exactly 1, 2, 3, or 4 widths;
3. Jaccard overlaps among the four right-censored sets;
4. exact width-by-width membership for every source rule;
5. repeat periods for rules that leave the long set at a fresh width.

The evaluator does not privilege known rule numbers in scoring or stopping.

## Frozen interpretation boundary

- A rule right-censored at all four widths is a **robust long-tower candidate** within this finite horizon, not proof of infinite nonrecurrence.
- A rule whose status changes with width is finite-size-sensitive under this representation.
- The previously attached starter labels are joined only after the full structural width table is saved.

The strong Class-IV conjecture is not retuned. If Rule 30 remains robust alongside 54/110, exact exclusivity remains false. If 54/110 are stable while Rule 30 is not, that is a fresh-size distinction worth further local analysis, but not yet a classifier.

## Decision boundary

If a nontrivial robust-long subset remains, derive local/algebraic signatures that may predict membership without enumerating the whole tower.

If the long set changes heavily with width, treat tower depth primarily as a finite-world role-budget measure and return to spatial lift geometry rather than class interpretation.