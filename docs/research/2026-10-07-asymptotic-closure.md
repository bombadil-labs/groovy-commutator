# Long thin repair tails are not Class-IV-specific

**Evidence:** exact finite-state enumeration on the frozen primary domain.  
**Authored by:** GPT-5.6 Sol (OpenAI), 2026-10-07. **Reviewed by:** none.

We wondered whether the Class-IV-like regime could be characterized as
**asymptotic closure**: most predictive information is repaired early, while
small additional distinctions remain necessary for a long sequence of later
horizons.

The exact future-equivalence tower already gives a canonical minimal repair
sequence. If \(C_t\) groups microstates by their observed trajectories through
horizon \(t\), then \(C_{t+1}\) is the coarsest refinement that retains exactly
the extra distinction needed for one more observed future step.

The frozen test used nonoverlapping block-2 parity at cadence two on the
width-10 periodic ring and compared Rules 0, 4, 90, 184, 30, 126, 54 and 110.
The primary prediction failed, so the protocol stopped before widths 12 and 14.

Protocol: [asymptotic closure](protocols/asymptotic-closure-20261007.md).  
Runner: [experiment_asymptotic_closure.py](../../scripts/experiment_asymptotic_closure.py).  
Canonical result: [asymptotic_closure_20261007.json](../../results/asymptotic_closure_20261007.json).

## The frozen quantity

Let \(H_t\) be the entropy of the exact partition \(C_t\) under the uniform
finite-state ensemble, \(h_*\) the first stable horizon and
\(H_\infty=H_{h_*}\).

The total predictive information restored by history is

\[
L=H_\infty-H_0.
\]

Let \(t_{90}\) be the first horizon at which 90% of \(L\) has been restored.
The frozen long-tail statistic was

\[
A_{90}=\frac{h_*-t_{90}}{h_*}.
\]

A large \(A_{90}\) means that most of the repair sequence happens after the
representation already contains 90% of the information it will ultimately
need: a long sequence of cheap but still necessary refinements.

## Primary result

| Rule | role | \(h_*\) | \(t_{90}\) | \(A_{90}\) | \(H_\infty/n\) | safely forgotten bits |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 0 | constant control | 0 | 0 | 0.000 | 0.5000 | 5.0000 |
| 4 | idempotent/simple | 1 | 1 | 0.000 | 0.7265 | 2.7348 |
| 90 | additive factor control | 0 | 0 | 0.000 | 0.5000 | 5.0000 |
| 184 | traffic/transport | 3 | 2 | 0.333 | 0.7479 | 2.5215 |
| 30 | chaotic control | **10** | 2 | **0.800** | **0.9996** | **0.0039** |
| 126 | spreading chaotic control | 2 | 2 | 0.000 | 0.7953 | 2.0470 |
| 54 | core complex | 3 | 2 | 0.333 | 0.9500 | 0.4996 |
| 110 | core complex | 4 | 2 | 0.500 | 0.9669 | 0.3312 |

The control prediction passed: Rules 0 and 90 close immediately.

The primary Class-IV prediction did not. It required both Rules 54 and 110 to
have strictly larger \(A_{90}\) than both chaotic controls. Rule 30 instead has
the strongest long thin tail in the panel:

\[
A_{90}(30)=0.80
>
A_{90}(110)=0.50
>
A_{90}(54)=0.333.
\]

The protocol therefore stops at width 10. Widths 12 and 14 were not evaluated.

## What Rule 30 is doing

Rule 30's exact repair increments are

\[
4.1558,\;0.6743,\;0.06836,\;0.01953,\;0.01953,\;0.01953,\;
0.00977,\;0.00977,\;0.00977,\;0.00977
\]

bits.

So the asymptotic shape is real: after a huge first repair, tiny distinctions
keep becoming necessary for eight more repair steps after the 90% point.

But its limit is almost the complete microscopic state. The stable quotient
contains

\[
H_\infty=9.99609375
\]

bits out of the original 10. Only \(0.00390625\) source bits remain safely
forgotten.

This is the key negative. A long thin predictive-repair tail by itself does
not identify the hoped-for intermediate regime. Canonical chaos can exhibit
an even stronger tail simply because the predictive quotient is converging
toward microscopic identity.

## What the negative suggests, without rescuing this protocol

Before evaluation, the motivating cartoon already distinguished two ways to
avoid easy closure:

1. the representation may keep refining because it is being forced toward the
   full microstate;
2. it may keep refining while retaining a nontrivial compressed quotient.

The frozen primary statistic tested only the first coordinate: tail length
after most information had been restored. Rule 30 falsifies its Class-IV
specificity.

Post hoc, the saved diagnostics point directly at the omitted second
coordinate. Rule 30 combines the longest tail with essentially zero
safe-forgetting reserve, whereas Rules 54/110 retain about 0.50 and 0.33 bits
respectively on this finite ring. Rule 184 retains much more, about 2.52 bits,
but has a shorter tail.

That pattern motivates a **separate fresh-width hypothesis**: complex behavior
might occupy an intermediate wedge between rapid compressed closure and long
repair that collapses to identity. This note does not test that new hypothesis,
and the present protocol is not reopened to do so.

## Scope and provenance

The claim is exact only for the declared width-10 finite ring, fixed observer,
cadence and panel. It is not an infinite-line result or a Class-IV definition.

The research protocol was committed before outcomes were inspected. After that
freeze, an exploratory implementation produced the primary numbers before the
canonical runner was committed; the self-contained canonical runner implements
the frozen definitions and records the same outcome. This ordering is preserved
as a procedural deviation rather than presented as a pre-implementation run.

The canonical result embeds the SHA-256 of the committed runner. No width-12,
width-14 or all-rule evaluation was performed after the failed primary gate.
