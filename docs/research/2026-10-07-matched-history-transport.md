# Matched history, different relationship to Groovy: Rule 62 versus Rule 110

**Evidence:** exact exhaustive enumeration on fresh widths 16 and 18.  
**Authored by:** GPT-5.6 Sol (OpenAI), 2026-10-07. **Reviewed by:** none.

An independent census showed that Rule 62 and Rule 110 are unusually well
matched on the amount of predictive history required by the established
block-2-parity observer. Their safe-forgetting reserves differ by only about
one hundredth of a bit at widths 16 and 18, and their history depths are close.

That makes the pair useful for a different question:

> **If two rules need nearly the same amount of history, is that history about
> the same thing?**

The answer is no on this bounded test.

For Rule 110, every newly necessary predictive distinction at widths 16 and 18
is already readable from the **current centered Groovy field** once the
currently retained predictive history is known.

For Rule 62, the first two predictive repairs at both widths contain additional
information not present in current Groovy. Exact counterexamples certify the
difference.

Protocol: [matched history transport](protocols/matched-history-transport-20261007.md).  
Runner: [experiment_matched_history_transport.py](../../scripts/experiment_matched_history_transport.py).  
Result: [matched_history_transport_20261007.json](../../results/matched_history_transport_20261007.json).

## Exact construction

Use the nonoverlapping block-2 parity observer \(P\) at cadence two.

Let \(C_t\) be the exact partition of source states by their observed
trajectories through coarse horizon \(t\), and let

\[
X_t=H^{2t}(X).
\]

The current centered Groovy field is

\[
G_H^\circ(X_t)=B_H(X_t,D_HX_t).
\]

At every nonclosed refinement step ask whether

\[
\boxed{
(C_t(X),G_H^\circ(X_t))
\longmapsto
P(H^2X_t)
}
\]

is a deterministic factor.

If yes, the current situated-change field contains all the distinction needed
for the next minimal predictive repair, given what history has already been
retained.

If no, there exist two states with the same predictive-history state and the
same current centered Groovy field that nevertheless require different next
macro-observations.

## Width 16

Rule 110 requires five nonzero predictive repairs.

The exact factor passes at **all five**:

| repair step | added predictive bits | Groovy-coupled fraction |
| ---: | ---: | ---: |
| 0 | 5.559121 | 1.000 |
| 1 | 1.752723 | 1.000 |
| 2 | 0.134649 | 1.000 |
| 3 | 0.014501 | 1.000 |
| 4 | 0.000488 | 1.000 |

Thus

\[
\Gamma_{110}(16)=1.
\]

Rule 62 requires four nonzero repairs. Its first two fail the exact Groovy
factor:

| repair step | added predictive bits | Groovy-coupled fraction | factor? |
| ---: | ---: | ---: | :---: |
| 0 | 5.310237 | 0.70225 | no |
| 1 | 1.915329 | 0.93772 | no |
| 2 | 0.228905 | 1.000 | yes |
| 3 | 0.016503 | 1.000 | yes |

Cumulatively,

\[
\Gamma_{62}(16)=0.77240,
\]

leaving about \(1.7004\) predictive-repair bits not carried by current Groovy.

An exact first-step witness is:

- source states: 60 and 204;
- same current block-parity history label: 0;
- same centered Groovy field: 34;
- different next observations: 6 and 14.

So current Groovy is genuinely insufficient for that Rule-62 repair.

## Width 18

The fresh replication is stronger, not weaker.

Rule 110 has six nonzero predictive repairs, and every one again satisfies the
exact factor:

\[
\Gamma_{110}(18)=1.
\]

Rule 62 again fails its first two repairs:

\[
\Gamma_{62}(18)=0.77255,
\]

with about \(1.9116\) uncoupled repair bits.

The same tiny first-step witness survives unchanged:

- source states 60 and 204;
- same predictive label 0;
- same centered Groovy 34;
- next observations 6 and 14.

A second-step fresh-width witness is also saved in the canonical result.

## What this establishes

The matched pair controls for a major failure of the preceding asymptotic-
closure idea.

Rule 62 and Rule 110 can look nearly identical in **how much** predictive
history their stable quotients require, while differing sharply in **what that
history is tracking**.

On this finite observer:

- Rule 110's entire minimal predictive-repair sequence is readable from current
  situated-change information \(G^\circ\) plus the predictive state already
  retained;
- Rule 62 needs additional historical context that current \(G^\circ\) does not
  encode during its early repairs.

That is a mechanistic separation, not another amount-of-history threshold.

A useful phrasing is:

> **For Rule 110 in this experiment, history repairs prediction by resolving
> situated change. For Rule 62, some predictive history is about something
> else.**

## What this does not establish

This is not a Class-IV discriminator.

The metric was selected after exploratory widths 12 and 14, and the protocol
explicitly forbade a broader rule census. Other rules can also have complete
Groovy-coupled repair under related finite tests.

The result does not establish an infinite-line factor, observer independence,
or that Groovy is a universal sufficient statistic.

It does establish the specific matched contrast at two fresh widths, with
exact witnesses on the negative side.

## Next question

The next useful move is structural rather than another threshold:

> **Why does Rule 110 satisfy the factor
> \((C_t,G_t^\circ)\to Y_{t+1}\) at every repair step?**

A local or symbolic proof of that identity, or a small counterexample beyond
the tested finite domains, would be more valuable than immediately scoring all
256 ECAs.
