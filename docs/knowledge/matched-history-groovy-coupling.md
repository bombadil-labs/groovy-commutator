# Rule 110's minimal predictive repairs are Groovy-readable in a matched control

Under the fixed nonoverlapping block-2 parity observer at cadence two, Rule 62
and Rule 110 require nearly the same amount of predictive history on the tested
finite rings.

Despite that match, their repair mechanisms differ.

At fresh widths 16 and 18, every nonzero Rule-110 refinement step satisfies the
exact factor

\[
(C_t,G_t^\circ)\to Y_{t+1},
\]

where \(C_t\) is the current exact predictive-history state and
\(G_t^\circ\) is the current centered Groovy field.

Thus the next distinction that must be added for exact prediction is completely
readable from the current situated-change field once the already-retained
predictive state is known.

Rule 62 fails the same factor during its first two repair steps at both fresh
widths. Exact source-state pairs with equal \(C_t\) and equal current centered
Groovy but different next observations certify the failure.

The cumulative fraction of predictive-repair information coupled to current
Groovy is exactly 1.0 for Rule 110 at both widths, versus about 0.7724 and
0.7725 for Rule 62.

This is a matched finite-domain mechanism result, not a Class-IV classifier or
an infinite-line theorem.

Source: [matched history transport](../research/2026-10-07-matched-history-transport.md).
