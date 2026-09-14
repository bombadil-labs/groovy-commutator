# Temporal periods contain shape recurrence and spatial drift

For a periodic state of a translation-equivariant deterministic map on a finite ring, let p be its least temporal period, d its least spatial period, and q the first positive return time up to translation. If that return shifts the state by a modulo d, then $p=q\,d/\gcd(d,a)$. The number of temporal cycles in its translation family is $\gcd(d,a)$.

At ring size 14, complete enumeration gives q=13 and a=12 for both Rule 110 period-91 cycles. All four Rule 54 period-112 cycles have q=16, with two cycles at a=10 and two at a=4. All have d=14. Thus the six temporal cycles form three translation families, each with seven positional repetitions. This is exact for these selected rules and this ring, and independently checked at all 630 target temporal phases.

The factor 13 remains after removing spatial drift; that does not make it independent of ring size or establish a prime-distribution law. Further ring sizes and arithmetic comparisons are unrun. An injective one-step commuting lift preserves p, but identifying q and a across dimensions also requires a compatible spatial translation action.

Source: [the orbit drift record](../research/2026-09-14-orbit-drift.md), including the general derivation, exact cycles, controls, independent reconstruction and runtime provenance. This entry introduces a separate dynamical statistic; its empirical claim does not depend on the native lift-cache results. No dependency edge to those results is asserted.

Authored by: Codex (OpenAI), Myk's dimensional-lift session, 2026-09-14. Reviewed by: independent Codex agent `orbit_drift_review` for scientific reproduction; final exact-head review and integration tracked in [gathering #245](https://github.com/bombadil-labs/groovy-commutator/pull/245).
