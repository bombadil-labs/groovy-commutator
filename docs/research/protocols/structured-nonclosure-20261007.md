# Protocol: structured nonclosure and predictive refinement

**Status:** frozen before evaluation, 2026-10-07.  
**Authored by:** GPT-5.6 Sol (OpenAI). **Reviewed by:** none.

## Question

The repository already defines the exact forward-future refinement

\[
R_t=\bigcap_{j=0}^{t}(E^q\times E^q)^{-j}(R_0)
\]

for an observation \(P\), with stable relation \(R_\infty\) giving the minimal
exact predictive quotient on a finite deterministic domain.

This unit asks a different question from the earlier memory-depth census:

> **How does a representation fail to close while it is being refined, and do
> Class-IV-like rules show persistent but structurally compressible residuals?**

The motivating hypothesis is:

\[
\boxed{
\text{complex dynamics repeatedly require new distinctions, but the residual
distinctions retain a compact reusable grammar.}
}
\]

This is a bounded falsification test, not a definition of Wolfram Class IV.

## Fixed observation and cadence

Use the established nonoverlapping block-2 parity observer on even periodic
rings:

- source: elementary cellular automaton \(H\);
- cadence: \(q=2\) source steps;
- observation \(P\): XOR each adjacent pair into one macrocell;
- macro width: \(m=n/2\).

This observer is chosen before evaluation because the 2026-09-08 history-lift
study already showed that it produces nontrivial memory scaling and puts all
repository-labeled Class-IV rules in its growing-memory group. The present
unit does not tune the observer.

## Frozen rule panel

The primary panel is deliberately mechanistic rather than label-balanced:

| Rule | role |
| ---: | --- |
| 0 | constant Class-I control |
| 4 | nonlinear idempotent / simple Class-II-like control |
| 90 | additive exact-factor control |
| 184 | transport/traffic Class-II control with known observer-dependent memory |
| 30 | canonical chaotic Class-III control |
| 126 | strongly spreading Class-III-like control |
| 54 | core complex/Class-IV rule |
| 110 | core complex/Class-IV rule |

No rule may be replaced after outcomes are viewed.

## Widths and decision order

1. **Primary exact gate:** ring \(n=10\).
2. **Fresh-width confirmation:** ring \(n=12\), evaluated only after the
   metric definitions and primary predictions below are frozen.
3. **Stress width:** ring \(n=14\), run only if the primary gate produces at
   least one qualitative separation worth checking.

All states on each ring are enumerated exactly.

No all-256 census is permitted in this unit. A later census requires a new
decision after this bounded panel.

## Exact refinement profile

Let \(C_t\) be the partition of source states by the complete observed word

\[
(P(S),P(E^qS),\ldots,P(E^{qt}S)).
\]

Compute it by deterministic partition refinement until the partition stabilizes
at \(C_\infty\). For the uniform finite-state ensemble record:

- class count \( |C_t| \);
- partition entropy \(H(C_t)\);
- new bits \(H(C_{t+1})-H(C_t)\);
- latent bits \(H(C_\infty)-H(C_t)\);
- stable predictive quotient size and entropy;
- first stable depth.

The stable partition is the exact minimal future-equivalence quotient for this
declared finite system and observer. Entropy is only a uniform-ensemble coding
cost; the partition itself carries the exact result.

## Residual grammar at each failed closure

For every class \(c\in C_t\), let

\[
O_c=\{P(E^{q(t+1)}S):S\in c\}.
\]

If \(|O_c|>1\), that class still fails closure at horizon \(t\).

Define its nonzero next-observation residual masks

\[
\mathcal R_c=\{y\oplus y':y,y'\in O_c,\ y\neq y'\}.
\]

Let

\[
\mathcal R_t=\bigcup_c\mathcal R_c.
\]

These are exact macro-level distinctions that the current compressed history
still cannot predict.

Record:

- number of split classes;
- \(|\mathcal R_t|\);
- fraction of all nonzero \(m\)-bit masks represented,
  \[
  \rho_t=|\mathcal R_t|/(2^m-1);
  \]
- cyclic-translation quotient \(\mathcal R_t/C_m\): canonicalize each mask by
  its lexicographically minimum cyclic rotation and count distinct orbits;
- translation compression ratio
  \[
  \kappa_t=|\mathcal R_t/C_m|/|\mathcal R_t|;
  \]
- Hamming-weight distribution of the canonical residual motifs.

This is a deliberately narrow and exact notion of "structured/compressible":
many residual masks being translations of a small motif vocabulary, and/or
remaining spatially sparse. It is not Kolmogorov complexity and is not a
universal compression claim.

## Frozen qualitative predictions

The experiment is allowed to fail.

**P1 — trivial/additive closure controls.**
Rules 0 and 90 should close with very shallow refinement under this established
observer. Their residual grammar should disappear correspondingly quickly.

**P2 — chaotic saturation.**
At least one of Rules 30/126 should, before closure on the primary width, show
a residual repertoire that is substantially less translation-compressible than
Rules 54/110 at a matched nonzero-refinement horizon. This prediction is
qualitative; the result table must show raw counts and no threshold will be
invented after evaluation.

**P3 — structured persistence for the core complex pair.**
Rules 54 and 110 should both exhibit more than one nonzero refinement step at
\(n=10\), while retaining a residual motif vocabulary smaller than the full
nonzero macro-mask space at each of those steps.

**P4 — fresh-width survival.**
Any apparent 54/110 versus 30/126 separation used to motivate continuation
must preserve its direction at \(n=12\). If it reverses or collapses, the
Class-IV interpretation stops.

## Primary decision / hard stop

The unit is considered a **negative for the hypothesis** if either:

1. Rules 54/110 are not distinguishable from the chaotic controls in the joint
   profile of continued refinement plus residual motif compression at \(n=10\);
   or
2. an apparent primary separation does not preserve direction at \(n=12\).

On a negative, write the result and stop. Do not search new observers, new
thresholds, new rule panels, or new residual metrics in this unit.

If a qualitative separation survives \(n=10\) and \(n=12\), run \(n=14\) as a
stress test and then stop. Do not launch the 256-rule census automatically.

## Scope and non-claims

- Every finite ring has a finite predictive quotient. "Avoid closure" here
  means a refinement profile that continues to require structured new
  distinctions over the tested finite scales, not literal infinite nonclosure.
- This unit does not establish an infinite-line result.
- It does not identify a unique minimal online suffix memory.
- It does not prove that cyclic-translation compression is the correct or only
  notion of residual structure.
- It does not infer computational universality or biological adaptation.
- The Class-IV language is a mechanistic hypothesis about the frozen 54/110
  core, not a relabeling of disputed rules or a universal classifier.

## Planned artifacts

- scripts/experiment_structured_nonclosure.py
- results/structured_nonclosure_20261007.json
- docs/research/2026-10-07-structured-nonclosure.md

Update FINDINGS / Program / knowledge only if the bounded result changes the
current account.
