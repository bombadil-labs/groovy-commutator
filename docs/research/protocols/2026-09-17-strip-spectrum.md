# Protocol: periodic-strip spectrum between 1D restriction and 2D ambient dynamics

**Status:** FROZEN before implementation/evaluation  
**Date:** 2026-09-17  
**Author:** GPT-5.6 Sol, Groovy Commutator session  
**Protocol review:** none at freeze; run authorized under Myk's 2026-09-17 “make it so!” instruction for the cross-dimensional mapping program. Independent retrospective review required before merge to `main`.

## 1. Question

For a fixed 2D Life-like local law, how does dynamical behavior change as the transverse periodic strip height grows from 1 toward a genuinely 2D geometry?

The exact precursor result fixes the representation hierarchy:

- height 1 is a lossy quotient onto a reflection-symmetric ECA;
- height 2 is already injective on Life-like **rule identity**.

The present experiment asks a different question: at what strip widths do the measured **dynamics** separate and stabilize?

## 2. Fixed panel

Primary four rules:

- Life `B3/S23`;
- HighLife `B36/S23`;
- Day & Night `B3678/S34678`;
- explosive adversary `B35/S236`.

Known exact height-1 images are recorded before the run:

- Life → 22;
- HighLife → 54;
- Day & Night → 178;
- B35/S236 → 22.

Life and B35/S236 therefore form the key paired control: identical at height 1, distinct local laws by height 2.

## 3. Strip family

Use periodic vertical heights

`k = 1, 2, 3, 4, 6, 8, 12, 16`.

Horizontal width is 521 with periodic boundary. Every column is a `2^k`-state 1D symbol, but simulation remains binary on the `k × 521` strip.

Primary density: 0.5. Stress densities 0.3 and 0.7 are run only after the primary strip spectrum is saved.

## 4. Observables

Reuse the already frozen starred definitions without threshold fitting:

- center-bit `M*` from 8-step history versus current bit;
- local outer-totalistic-symbol `R*` relative to a strip-height-matched uniform predecessor reference;
- `S* = max(0,R*) max(0,M*)`;
- disturbance spreading reported both as longitudinal support span `Dx(t)` and native strip Chebyshev diameter `Dg(t)`.

Primary spreading exponent is longitudinal:

`alpha_x = log2(mean Dx(128) / mean Dx(64))`.

`alpha_g` is secondary. The longitudinal quantity is chosen before evaluation because vertical diameter is mechanically capped by strip height and would make different heights incommensurable.

## 5. Strip-height-matched `R*` reference

For each `(rule,k)`, sample uniform predecessor blocks consisting of five adjacent columns of height `k`; vertical indexing is periodic. Evolve enough of the block to compute the central site's successor rule-input symbol `(center, neighbor_count)`.

- heights 1–3: use exact enumeration (`2^(5k)` predecessor blocks: 32, 1024, 32768);
- heights 4+: use 100,000 deterministic Monte Carlo samples, doubling only on the predeclared unsupported-symbol condition up to 800,000.

This avoids comparing a strip trajectory against the full-plane predecessor ensemble.

## 6. Simulation budget

Per `(rule,k,density)`:

- burn 512;
- score 256;
- six independent trajectory seeds;
- first four train `M*`, final two test;
- 64 deterministic spatial sample sites per seed (or all cells when the strip contains fewer than 64 sites);
- disturbance: four base seeds × eight origins;
- horizons 64 and 128;
- seeds SHA-256-derived from protocol/rule/height/density/replicate/purpose.

The 521 horizontal width prevents longitudinal causal-cone wrap by t=128.

## 7. Frozen predictions

1. At `k=1`, HighLife must reproduce Rule-54 state dynamics exactly and Life/B35 must be exactly state-identical when started from the same row.
2. Life and B35 must become dynamically distinguishable at some `k>=2`; if their measured profiles remain numerically identical despite distinct state trajectories, that is a limitation of the observables.
3. The HighLife profile is allowed to leave the Rule-54 region as soon as `k>1`; the experiment measures this departure rather than assuming monotone preservation.
4. No monotonicity with height is assumed for `R*`, `M*`, or spreading.
5. If a rule's profile approaches a stable band by larger tested heights, record the empirical stabilization; do not extrapolate to the infinite plane without a separate convergence argument.

## 8. Primary outputs

Save, before interpretation:

- one row per `(rule,k,density)` with `R*`, `M*`, `S*`, `Dx64`, `Dx128`, `alpha_x`, `Dg64`, `Dg128`, `alpha_g`, extinction fraction and counts;
- exact height-1 state-equality checks;
- pairwise trajectory Hamming distances between Life and B35 under matched seeds for each height;
- a strip-spectrum table/figure after numeric bytes are fixed.

No threshold fitting, clustering, or class score is permitted.

## 9. Stopping / failure

- Any failure of the preregistered height-1 equality identities stops the run.
- Unsupported `R*` reference symbols trigger only the frozen reference-doubling schedule.
- Resource-driven budget changes must be applied uniformly across all four rules before reading the affected outputs.

## 10. Non-claims

This is not a theorem of convergence to full 2D dynamics, not a classifier, and not a claim that strip width is literally spatial dimension. It is an exact family of periodic restrictions used to study how much transverse freedom is required before particular dynamical observables change.
