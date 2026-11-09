# The asymptotic-closure wedge passes once and then hits the transport boundary

**Evidence:** exact finite-state enumeration on the frozen fresh-width gates.  
**Authored by:** GPT-5.6 Sol (OpenAI), 2026-10-07. **Reviewed by:** none.

The preceding width-10 experiment showed why a one-axis "long thin repair
tail" is insufficient: Rule 30 had the longest tail because its predictive
quotient was converging almost all the way to microscopic identity.

This separate protocol froze a two-axis, threshold-free hypothesis before
evaluating fresh widths. The axes were:

\[
d=\frac{h_*}{n},
\]

the predictive-repair depth as a fraction of ring width, and

\[
s=\frac{n-H_\infty}{n},
\]

the fraction of microscopic information that the stable predictive quotient
can still safely forget.

The proposed complex regime was the wedge between a transport anchor
(Rule 184: shorter repair, more compression) and a chaotic anchor
(Rule 30: longer repair, almost no compression).

The wedge passes exactly at width 12 and fails at width 14 because Rule 110
lands on the Rule-184 repair-depth boundary. The frozen protocol therefore
stops; width 16 was not evaluated.

Protocol: [asymptotic-closure wedge](protocols/asymptotic-closure-wedge-20261007.md).  
Runner: [experiment_asymptotic_closure_wedge.py](../../scripts/experiment_asymptotic_closure_wedge.py).  
Result: [asymptotic_closure_wedge_20261007.json](../../results/asymptotic_closure_wedge_20261007.json).

## Frozen geometry

At each scored width the anchors first had to satisfy

\[
d_{184}<d_{30},
\qquad
s_{30}<s_{184}.
\]

Then each candidate \(r\in\{54,110\}\) had to lie strictly inside both
intervals:

\[
d_{184}<d_r<d_{30},
\qquad
s_{30}<s_r<s_{184}.
\]

No thresholds or fitted score were permitted.

## Width 12: exact pass

| Rule | role | \(h_*\) | \(d=h_*/n\) | \(s=(n-H_\infty)/n\) |
| ---: | --- | ---: | ---: | ---: |
| 184 | transport anchor | 3 | 0.2500 | 0.2522 |
| 30 | chaotic anchor | 10 | 0.8333 | 0.00134 |
| 54 | complex candidate | 5 | 0.4167 | 0.0553 |
| 110 | complex candidate | 4 | 0.3333 | 0.0338 |
| 126 | diagnostic | 4 | 0.3333 | 0.1830 |

Both core candidates lie strictly between the anchors on both axes.

Rule 126 also lies inside the wedge. The protocol declared this a
class-specificity warning rather than a primary failure, so it was retained
openly and the width-14 confirmation proceeded.

## Width 14: exact failure

| Rule | role | \(h_*\) | \(d=h_*/n\) | \(s=(n-H_\infty)/n\) |
| ---: | --- | ---: | ---: | ---: |
| 184 | transport anchor | 4 | **0.2857** | 0.2506 |
| 30 | chaotic anchor | 10 | 0.7143 | 0.0000174 |
| 54 | complex candidate | 5 | 0.3571 | 0.0443 |
| 110 | complex candidate | 4 | **0.2857** | 0.0336 |
| 126 | diagnostic | 3 | 0.2143 | 0.1710 |

Rule 54 remains strictly inside the anchor wedge.

Rule 110 remains between the anchors on the compression coordinate, but not on
repair depth:

\[
d_{110}=d_{184}=\frac{4}{14}.
\]

The frozen prediction required a strict inequality. Therefore the width-14
gate fails and the experiment stops.

Width 16 was not evaluated.

## What survives the negative

The two axes do expose the intended two failure modes cleanly in the anchors.

Rule 30 is driven almost to microscopic identity: at width 14 its
safe-forgetting density is about \(1.74\times10^{-5}\).

Rule 184 keeps roughly one quarter of the source information safely forgotten,
while closing after four history refinements.

At width 12, Rules 54/110 genuinely occupy the finite-panel interior between
those extremes. That geometry is therefore not an artifact invented after the
fact. But one fresh width later Rule 110 shares the transport anchor's exact
repair depth, so the strict pointwise wedge is not robust.

## A structural caution exposed by the failure

This is post-hoc interpretation, not a new tested gate.

The depth \(h_*\) is integer-valued. As ring width changes, it can remain on a
plateau and then jump. Dividing by \(n\) turns those staircases into a brittle
pointwise coordinate. A genuine "asymptote" may therefore be a statement about
the **scaling sequence** of repair depth and retained compression rather than
strict ordering at every finite width.

That possibility is not evaluated here. Rescuing the result by weakening the
strict inequality, skipping width 14, or evaluating width 16 would violate the
frozen protocol.

## Scope

This result is exact for the specified observer, cadence, rule panel and
periodic widths 12 and 14. It is not an infinite-line statement, a Class-IV
classifier, or evidence of a limiting scaling law.

The result file embeds the committed runner hash. Width 16 and the all-rule
census were not run after the failed confirmation gate.
