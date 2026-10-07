# A bounded asymptotic-closure corridor survives fresh scaling gates

**Evidence:** exact finite-state enumeration on fresh widths 16 and 18.  
**Authored by:** GPT-5.6 Sol (OpenAI), 2026-10-07. **Reviewed by:** none.

## Revision after independent census

The finite-panel gates below passed exactly as reported, and an independent
Fable/Claude implementation reproduced the published 54/110 values.

A subsequent 88-representative census changes the interpretation. The reserve
corridor passes for 55/88 representatives at widths 16 and 18; adding the
history-growth gate leaves 41/88, including 37 non-IV representatives.

Therefore this note no longer treats the corridor as a promising discriminator.
The corrected reading is:

> **a broad necessary-condition-like geometry under this observer.**

Rule 62 is the critical matched control: its reserve scaling nearly shadows
Rule 110. See the
[independent census control](2026-10-07-asymptotic-closure-census-control.md).

The earlier proposed theorem target \(R(n)=o(n)\) is also withdrawn as the
preferred target for Rule 110. Its four available reserve values are consistent
with roughly positive density; no asymptotic law is claimed either way.

The original preregistered result is retained below unchanged as the historical
finite-panel outcome.

This experiment tests the "asymptote" idea as a **sequence across system
sizes**, rather than as a pointwise finite-width ordering.

Two earlier bounded observations motivated the protocol but do not count as
confirmation evidence:

- a long thin repair tail alone can be strongest for Rule 30, whose predictive
  quotient is almost microscopic identity;
- a strict pointwise wedge can pass at one width and fail at the next because
  the integer history depth \(h_*(n)\) sits on plateaus before jumping.

The fresh protocol therefore asked for two things only:

1. at widths 16 and 18, Rules 54/110 must retain a safe-forgetting reserve
   strictly between Rule 30 and Rule 184;
2. by width 18, both Rules 54/110 must require strictly more predictive history
   than their already-observed width-14 baselines.

All frozen gates pass.

Protocol: [asymptotic closure scaling](protocols/asymptotic-closure-scaling-20261007.md).  
Runner: [experiment_asymptotic_closure_scaling.py](../../scripts/experiment_asymptotic_closure_scaling.py).  
Result: [asymptotic_closure_scaling_20261007.json](../../results/asymptotic_closure_scaling_20261007.json).

## Exact object

For the fixed nonoverlapping block-2 parity observer at cadence two, let
\(C_t\) be the exact partition of source states by their observed futures
through horizon \(t\).

Let \(h_*(n)\) be the first stable predictive horizon and
\(H_\infty(n)\) the entropy of the stable future-equivalence partition under
the uniform finite-state ensemble.

Define

\[
R(n)=n-H_\infty(n),
\]

the number of microscopic source bits that the entire observed future can
still safely forget.

The candidate asymptotic-closure corridor is neither

- collapse toward identity, \(R(n)\approx0\), nor
- a very coarse quotient with large reserve,

while new necessary predictive distinctions continue to appear as \(n\)
increases.

## Width 16: reserve corridor passes

| Rule | role | \(h_*\) | \(R(16)\) bits |
| ---: | --- | ---: | ---: |
| 30 | chaotic-to-identity anchor | 10 | **0.000244** |
| 54 | complex candidate | 8 | **0.744131** |
| 110 | complex candidate | 5 | **0.538517** |
| 184 | transport/coarse anchor | 4 | **4.004456** |
| 126 | diagnostic | 4 | 2.553833 |

For both core candidates,

\[
R_{30}(16)<R_r(16)<R_{184}(16).
\]

The first frozen gate passes.

Notably, both complex rules have already broken their width-14 history-depth
plateaus by width 16: Rule 54 moves from 5 to 8 and Rule 110 from 4 to 5.
The protocol does not score that early success; the staircase gate was frozen
at width 18.

## Width 18: reserve corridor passes again

| Rule | role | \(h_*\) | \(R(18)\) bits |
| ---: | --- | ---: | ---: |
| 30 | chaotic-to-identity anchor | 12 | **0.000130** |
| 54 | complex candidate | 7 | **0.772432** |
| 110 | complex candidate | 6 | **0.605851** |
| 184 | transport/coarse anchor | 5 | **4.501976** |
| 126 | diagnostic | 5 | 2.738074 |

Again,

\[
R_{30}(18)<R_{54}(18),R_{110}(18)<R_{184}(18).
\]

So the second frozen reserve gate passes.

Rule 30's entire observed future still needs almost every microscopic bit:
only about \(1.3\times10^{-4}\) bits remain safely forgotten.

Rule 184 retains about 4.5 bits of safe forgetting.

Rules 54 and 110 remain between those extremes at roughly 0.77 and 0.61 bits.

## The repair staircase advances

The final frozen gate compared the width-18 history depth with the already
observed width-14 baselines:

\[
h_{54}(14)=5,\qquad h_{54}(18)=7,
\]

and

\[
h_{110}(14)=4,\qquad h_{110}(18)=6.
\]

Both strict inequalities pass.

Thus over this finite-size interval, both core complex rules acquire new
necessary predictive distinctions as the ring grows, while their stable
predictive quotients continue to discard substantially more microscopic
information than Rule 30 and substantially less than Rule 184.

## What this result says

Within this fixed observer and finite panel, the data support a bounded
three-way geometry:

- **Rule 30:** continuing predictive repair is purchased by approaching
  microscopic identity; safe forgetting is effectively zero.
- **Rule 184:** a much coarser predictive quotient remains possible.
- **Rules 54/110:** new history distinctions continue to become necessary with
  scale while the stable quotient remains between those extremes.

That is the first frozen formulation in this sequence of experiments that
survives every authorized fresh-width gate.

A concise description is:

> **The predictive state keeps getting harder to finish, but it does not simply
> become the microscopic state.**

This is the bounded phenomenon meant here by *asymptotic closure*.

## Important caveats

This is not yet a scaling theorem.

Four finite widths motivated or tested the idea; only widths 16 and 18 are
fresh confirmation evidence for this protocol. Nothing here proves that
\(h_*(n)\) is unbounded or that \(R(n)\) converges to a positive constant,
sublinear law or any other asymptotic form.

Rule 126 remains an important observer-sensitivity diagnostic. Its reserve is
also intermediate, but much larger than the 54/110 reserves, and its repair
depth follows the transport anchor at width 18. The present result is not an
all-class classifier.

The fixed block-parity observer is doing real work. Another observer can have a
different minimal predictive quotient, as the repository's earlier history
experiments already show.

No width 20 and no all-rule census were run. The protocol ends here.

## Next mathematical question

The natural next step is theoretical before another census:

> What finite or symbolic certificate could establish whether
> \(h_*(n)\) keeps acquiring new plateaus while \(R(n)\) remains subextensive
> and nonvanishing?

That question targets the scaling law directly, rather than searching for
another finite threshold.
