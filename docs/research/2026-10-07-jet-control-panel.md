# Matched jet controls: Rule 54 retains branching ambiguity where 30 does not

**Date:** 2026-10-07. **Status:** bounded exact three-rule comparison plus
separately frozen Rule-54 follow-up.  
**Author:** GPT-6 (OpenAI). **Independent peer reviewer:** none.

Protocols:
[primary panel](protocols/jet-control-panel-20261007.md) and
[secondary 54 depth](protocols/jet54-deeper-fibers-20261007.md).

Reproducer: [experiment_jet_control_panel.py](../../scripts/experiment_jet_control_panel.py)
(reuses the committed jet-language and pair-fiber engines).
Saved summary tables:
[primary](../../results/jet_control_panel_20261007_summary.json) and
[Rule-54 follow-up](../../results/jet54_deeper_fibers_20261007_summary.json).

## Why these three rules?

The existing Rule-110 and Rule-62 units showed that successive commutator
residuals recover the source's spatial entropy, and at their first full-entropy
G-anchored prefixes the full-line equal-output pair graph has only periodic
off-diagonal recurrent components and finitely many interface states.

We asked whether that observation generalizes, rather than connecting it to
the six-field dimensional lift prematurely.

The selected panel was fixed before evaluation:

- Rule 54, a second complex/Class-IV-like case;
- Rule 30, a canonical chaotic/Class-III control;
- Rule 90, an affine/additive control.

All three use the identical full binary source shift and exact recurrence

\[
A_0=D=I\oplus H,\qquad
A_{k+1}=A_k\circ H\oplus H\circ A_k.
\]

G-anchored prefixes are G, GQ, GQR, GQRA4, GQRA4A5.

## Additive calibration: Rule 90

For additive Rule 90, H is linear, so D=I+H commutes with H:

\[
G=D\circ H\oplus H\circ D=0.
\]

Therefore Q, R, A4 and A5 all vanish identically. Complete local truth
tables confirm this exactly, and every G-anchored jet image is the singleton
all-zero configuration. Its spatial entropy is zero. Yet the source Rule-90
dynamics itself has nontrivial additive fractal evolution.

This validates that the jet measures failures of naive transport rather than
visual dynamical complexity by itself.

## Full source entropy appears at GQR for both 54 and 30

The exact labeled source de Bruijn automata and minimized finite-word
recognizers yield:

| Prefix | Rule 54 entropy | Rule 30 entropy | Rule 90 entropy |
| --- | ---: | ---: | ---: |
| G | 0.932639361 | 0.898861972 | 0 |
| G,Q | 0.999947843 | 0.999934041 | 0 |
| G,Q,R | 1.000000000 | 1.000000000 | 0 |
| G,Q,R,A4 | 1.000000000 | 1.000000000 | 0 |
| G,Q,R,A4,A5 | 1.000000000 | 1.000000000 | 0 |

Entropies come from the Perron eigenvalue of the exact finite labeled
presentation, and equality to one is numerical unless accompanied by an exact
pair-graph argument.

Rules 54 and 30 first reach the full source one-bit spatial entropy at
GQR, exactly as Rule 110 does in the previous unit. Rule 62 requires A5.

This alone rules out the proposed depth as a Class-IV discriminator.

## But the full-line hidden fibers are fundamentally different

The equality-of-jet pair graph represents all bi-infinite source pairs X,Y
whose complete jet fields agree. The diagonal X=Y is always present.

At the immediately shallower prefix GQ:

- Rule 54 has a mixed diagonal/off-diagonal recurrent SCC with Perron
  \(\rho\approx2.000145817\), plus a pure off-diagonal branching SCC;
- Rule 30 has a mixed recurrent SCC with
  \(\rho\approx2.000186304\).

Both have positive-entropy branching ambiguity.

After adding R:

**Rule 30.** Its GQR pair graph has one diagonal full-shift SCC plus eight
recurrent purely off-diagonal components. Every off-diagonal recurrent SCC
is a simple directed cycle. Their periods are 1, 2 and 6; the longest has
source-XOR period 101101. Twelve other essential non-diagonal graph states
are interface states.

Thus Rule 30 behaves like Rule 110 in the specific respect that *all
recurrent non-diagonal ambiguity is periodic* at GQR.

**Rule 54.** Its GQR pair graph has one diagonal full-shift component, but
also four entirely non-diagonal **branching** recurrent SCCs. Their
approximate Perron radii are

\[
\sqrt2,\quad 1.30791594,\quad 1.27201965,\quad 1.27201965.
\]

The first has 32 vertices and 48 internal edges. The graph is strongly
connected, with excess branching, so its spectral radius is strictly greater
than one without needing any floating-point threshold. Its symbolic source-
pair language has positive entropy:

\[
h_{\mathrm{offdiag,max}}=\log_2(\sqrt2)=0.5\text{ bits/site}.
\]

Nevertheless the total pair-graph entropy is exactly one, contributed by the
diagonal source full shift. The exceptional branching fiber component grows
exponentially as \((\sqrt2)^n\), **much more slowly** than the total source
language \(2^n\). This is positive entropy *within the equal-output pair
language*, not a claim of positive conditional entropy for a typical observed
jet configuration under a uniform source prior.

In particular: full source spatial entropy does **not** force the
non-diagonal recurrent fiber to consist only of phase cycles.

## Separately frozen Rule-54 follow-up: branching survives through A5

The first panel identified Rule 54 as the exception, so we froze a second
targeted question before computing its next two deeper pair graphs.

| Rule 54 prefix | branching recurrent off-diagonal SCCs | maximum off-diagonal Perron |
| --- | ---: | ---: |
| G,Q,R | 4 | 1.414214 |
| G,Q,R,A4 | 3 | 1.272020 |
| G,Q,R,A4,A5 | 3 | 1.272020 |

The further jet fields reduce some exceptional ambiguity but do not remove
branching through A5.

At A4 and A5 the recurrent pure-cycle periods include 1, 2, 4 and 8.
The longest cycle period 8 exceeds the local jet source radius 5 or 6.

## Post-hoc exact algebra: the persistent Rule-54 ambiguity has golden-mean growth

After the two frozen Rule-54 depth checks, we noticed that the remaining
branching SCC Perron value \(1.2720196495\ldots\) is the square root of the
golden ratio. This was **not** a preregistered prediction.

Computing exact integer adjacency characteristic polynomials for three
selected off-diagonal recurrent components gives:

| Prefix | selected SCC | exact characteristic polynomial |
| --- | --- | --- |
| GQR | 32 vertices, 48 edges | \(z^{30}(z^2-2)\) |
| GQRA4 | 32 vertices, 42 edges | \(z^{24}(z^2-z+1)(z^2+z+1)(z^4-z^2-1)\) |
| GQRA4A5 | 52 vertices, 68 edges | \(z^{44}(z^2-z+1)(z^2+z+1)(z^4-z^2-1)\) |

Hence the first selected component has exact Perron root \(\sqrt2\) and
spatial entropy \(1/2\) bit/site. The later selected components have Perron

\[
\rho=\sqrt{\varphi},
\qquad
\varphi=\frac{1+\sqrt5}{2},
\]

and thus

\[
\boxed{
h=\tfrac12\log_2\varphi\approx0.347121\text{ bits/site}.
}
\]

The same spectral factor survives from A4 to A5 despite changes in the
SCC's presentation size. That is consistent with a persistent Fibonacci-like
symbolic constraint on the exceptional equal-jet pair language.

It does **not** prove the entire SCC is conjugate to the golden-mean shift:
characteristic-polynomial factors and entropy are not conjugacy invariants
strong enough to establish that. The precise symbolic generators and any
conjugacy are a separate research question.

Independent scalar temporal-recurrence evaluation checked every complete
source patch for the Rule-54 A4 and A5 local truth tables: 2,048 and 8,192
source patches respectively. An exact SymPy characteristic-polynomial
calculation on the graph adjacencies produced the factors above.

## The proposed lift/depth/phase-period rhyme fails these controls

Two earlier observations were

- Rule 110: critical field R has source radius 4, longest phase cycle 4;
- Rule 62: critical field A5 has source radius 6, longest phase cycle 6.

But Rule 30 reaches the same phase-only type at R (radius four) while
retaining a period-six ambiguity. Rule 54 at radius six still has branching
fibers and phase cycles of period eight.

Thus equality of jet depth/radius and maximal hidden phase period was a
coincidence in the original two-rule comparison, not an invariant.

The six-field lift is a separately proved period-six *encoding grammar*
mixing spatial differences, temporal derivatives and source reconstruction;
its six slots are neither six successive jet residuals nor a universal
minimum. No lift correspondence is inferred here.

## Verification and provenance boundary

The precommitted primary and secondary protocols fixed the panel and resource
limits before their respective evaluations. A fresh local implementation
constructed jet local truth tables with vectorized Boolean operations,
de Bruijn image automata, and exact equal-label source-pair graphs.
An independent scalar tuple CA rederived every source-patch GQR label on
Rules 54 and 30. A separate NetworkX SCC implementation reproduced every
recurrent component's vertex count, edge count, diagonal status and
cycle/noncycle classification. Existing Rule-110/Rule-62 entropy values
were independently reproduced as convention checks. The additive Rule-90
control passed.

Scientific results were computed before the publication/reproduction wrapper
was committed. The saved summary JSON explicitly identifies that chronology;
the committed wrapper reuses the already pinned symbolic machinery for
independent reproduction. Do not call its hash an execution seal or treat
same-author alternative implementations as independent peer review.

This unit is complete: no added rules, deeper jets or classifier claim.

## What is worth investigating next

The right next question is the **branching source-pair language of Rule 54**:
what symbolic generators support the three persistent off-diagonal recurrent
SCCs through A5, and can their output equality be understood through ether,
defect or phase structure?

That is more targeted than chasing the numerical six-field coincidence. It
would need its own bounded test, independent of Wolfram-class selection.
