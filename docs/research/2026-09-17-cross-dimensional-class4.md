# Cross-dimensional selective persistence: generic 2D soup is not a simple continuation of the ECA phenotype

**Status:** prospective finite experiment under the no-review-at-freeze authorization; independent retrospective review pending.  
**Date:** 2026-09-17  
**Authored by:** GPT-5.6 Sol. **Reviewed by:** none.  
**Protocol review:** none at freeze; run authorized by Myk 2026-09-17 before implementation/evaluation.

## Question

Does the Jev-derived ECA mechanism — selective predictive persistence together with sustained disturbance spreading — transfer directly to known complex 2D Life-like cellular automata under generic random-soup trajectories?

## Answer

Only partially. The new dimension-neutral surrogate reproduces the intended ECA mechanism controls, and it cleanly distinguishes the explosive `B35/S236` adversary as almost pure spreading. But generic 2D soup does **not** put Life, HighLife, and Day & Night into one stable common quadrant across densities.

The stronger result came from the mapping controls: representation matters. HighLife on a width-1 periodic cylinder is exactly ECA Rule 54, yet one of the three proposed coordinates (`R*`) changes under the natural outer-totalistic observation map because that map is many-to-one. The dynamics are identical; the selective-retention statistic is observer-relative.

A follow-up exact strip analysis then showed that height 1 is a lossy quotient of Life-like rule identity, while height 2 already determines the complete 18-bit outer-totalistic rule. This motivates measuring a strip-width spectrum instead of treating “1D” and “2D” as two unrelated endpoints.

## Frozen observables

The experiment used new starred observables; old ECA thresholds were not transported:

- `R*`: standardized preference for rule-input symbols that are rarer under a uniform predecessor reference;
- `M*`: held-out log-loss gain from an eight-step center-bit history over the current bit alone;
- `S* = max(0,R*) max(0,M*)`;
- `alpha* = log2(D(128)/D(64))` from single-bit perturbation support diameter in the native graph metric.

The full protocol is `docs/research/protocols/2026-09-17-cross-dimensional-class4.md`.

## Full frozen run

Conditions used densities 0.5, 0.3, and 0.7. The 1D calibration used width 521; the 2D panel used 263×263 tori, six trajectory seeds, held-out seed evaluation for `M*`, a frozen predecessor-reference sampler, and 32 perturbation trials per rule/condition.

Median and range across the three densities:

| Rule | `S*` range | median `S*` | `alpha*` range | median `alpha*` | reading |
|---|---:|---:|---:|---:|---|
| ECA 54 | 0.233–0.243 | 0.235 | 0.954–1.057 | 0.974 | joint persistence + spread |
| ECA 110 | 0.185–0.206 | 0.192 | 0.619–0.707 | 0.627 | joint persistence + spread |
| ECA 5 | 0.408–0.558 | 0.553 | 0 | 0 | persistence-only control |
| ECA 62 | 0.133–0.158 | 0.156 | -0.015–0.636 | 0.354 | horizon/ensemble-sensitive near miss |
| ECA 122 | 0 | 0 | 1.019–1.023 | 1.020 | spread-only control |
| ECA 126 | 0 | 0 | 1.007–1.009 | 1.009 | spread-only control |
| Life | 0 | 0 | 0.410–0.679 | 0.558 | some spread, no positive `R*` |
| HighLife | 0.011–0.033 | 0.022 | 0.558–0.621 | 0.608 | weak persistence + moderate spread |
| Day & Night | 0.035–0.421 | 0.133 | 0–0.888 | 0 | strongly ensemble-sensitive |
| B35/S236 | 0.00005–0.00014 | 0.00007 | 0.995–0.998 | 0.996 | almost pure spreading |
| synthetic simple controls | 0 | 0 | 0 | 0 | trivial dynamics |

Important: `alpha*` is a 64→128 horizon statistic, not the old 256→512 statistic. Rule 62 crossing into stronger short-horizon spread at density 0.3 is therefore a real warning against treating the two measures as interchangeable.

## What survived the preregistered predictions

- The starred surrogate retained the intended 54/110, persistence-only, and spread-only ECA geometry qualitatively.
- `B35/S236` spread strongly at every density while carrying essentially zero `S*`, supporting a distinction between explosive propagation and selective predictive persistence.
- At the primary density 0.5, HighLife and Day & Night had positive `S*` together with nonzero spreading; Life did not.
- The 2D exemplar set was **not stable across density**. Day & Night lost long-horizon spreading after burn at densities 0.3 and 0.7, while Life never gained positive `R*`.

Therefore the result does not support a simple substrate-independent threshold definition of Class IV under generic random soup.

## Exact HighLife → Rule 54 mapping control

On a one-row Moore cylinder, the eight neighbor positions collapse with multiplicity:

`neighbor_count = 3*left + 2*center + 3*right`.

For HighLife `B36/S23`, exhaustive evaluation of the eight triples gives ECA Rule 54. A random 521-cell configuration evolved byte-for-byte identically for 256 ticks under native Rule 54 and width-1 HighLife.

The natural outer-totalistic local observer is not injective on ECA neighborhoods:

- `001` and `100` both map to `(center=0, neighbors=3)`;
- `011` and `110` both map to `(center=1, neighbors=5)`.

On the exact same Rule-54 trajectory, the finite audit gave:

- `R*` under the full ECA-neighborhood observer: 0.4015225733;
- `R*` under the outer-totalistic pushforward observer: 0.3599304425.

The state dynamics have not changed. `R*` changed because the observation algebra changed. In contrast, the center-bit histories/targets used by `M*` and the longitudinal XOR support used by spreading are identical under this conjugacy.

This is the main conceptual correction from the experiment: **selective retention is a property of dynamics relative to an observation map, not an invariant scalar attached to a CA in isolation.**

## Exact periodic-strip restriction

For any Life-like outer-totalistic rule, put the 2D CA on a periodic strip of height `k`. Treat each vertical column as one symbol. The result is exactly a 1D radius-one CA over an alphabet of size `2^k`.

### Height 1

Only six local conditions are realizable:

`B0, B3, B6, S2, S5, S8`.

Therefore the height-1 restriction forgets the other 12 rule bits. Exhaustive enumeration of all `2^18 = 262,144` Life-like rules shows:

- exactly 64 distinct ECA images;
- these are exactly the left/right-reflection-symmetric ECAs;
- every image has exactly `2^12 = 4096` Life-like preimages.

Panel images:

- Life `B3/S23` → ECA 22;
- HighLife `B36/S23` → ECA 54;
- Day & Night `B3678/S34678` → ECA 178;
- `B35/S236` → ECA 22.

So Life and the explosive adversary are **literally the same 1D rule at strip height 1**.

### Height 2

Exhaustive local enumeration shows that all 18 `(center state, neighbor count 0…8)` conditions are realizable on a two-row periodic strip. Hence the induced four-state radius-one strip CA exposes every birth/survival bit.

Consequently:

> The height-2 periodic-strip restriction is injective on the entire Life-like outer-totalistic rulespace.

This is an exact finite/local statement about rule identity, not a claim that two-row dynamics reproduce full-plane phenomenology.

## Interpretation

The failed-simple-transfer and exact strip results point in the same direction.

There is no single scalar “Class-IV essence” that obviously survives a jump from an ECA table to generic 2D soup. What survives depends on **which relation is being preserved**:

- exact state conjugacy preserves bit histories and longitudinal perturbation fields;
- coarse observation can alter a retention statistic without changing the underlying trajectory;
- width-1 restriction can erase most of a 2D rule table;
- width 2 already restores full local-law identity, while still constraining global geometry severely.

The next experiment therefore studies the **strip-width spectrum**: how the same fixed 2D local law changes its measured dynamical phenotype as progressively more of the transverse dimension is admitted.

## Files

- `experiments/cross_dimensional_class4_20260917/run.py`
- `experiments/cross_dimensional_class4_20260917/strip_restriction.py`
- `results/cross_dimensional_class4_20260917/crossdim_full.json`
- `results/cross_dimensional_class4_20260917/crossdim_full.csv`
- `results/cross_dimensional_class4_20260917/mapping_control.json`
- `results/cross_dimensional_class4_20260917/strip_restriction_exact.json`

## Limits

The broad organization/information × spreading idea has extensive prior art. No novelty claim is made here. The strip-restriction algebra is exact, but its relationship to existing strip/cylinder CA literature has not yet been searched deeply enough for a novelty claim.
