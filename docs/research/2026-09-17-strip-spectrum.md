# Strip spectrum: when added transverse freedom reveals and changes a Life-like rule

**Status:** exploratory computational result plus exact finite local-law statements; final independent review pending.  
**Date:** 2026-09-17  
**Author:** GPT-5.6 Sol, Groovy Commutator session.  
**Protocol:** `docs/research/protocols/2026-09-17-strip-spectrum.md`, frozen before implementation/evaluation.  
**Protocol review:** none at freeze; run authorized by Myk 2026-09-17 in the project conversation (“make it so!”), under the repository no-review-at-freeze exception. Independent review remains required before merge to `main`.

## Question

Instead of jumping directly from a one-dimensional restriction to an effectively unbounded two-dimensional plane, what happens if a fixed Life-like outer-totalistic rule is placed on periodic strips of increasing height?

This asks two deliberately separate questions:

1. **local-law visibility:** how much of the original 18-bit Life-like rule can be recovered from the induced one-dimensional column CA at strip height `k`?
2. **dynamical phenotype:** how do the predeclared starred selective-persistence and longitudinal-spreading measurements vary as transverse degrees of freedom are added?

The experiment does **not** assume monotonic convergence with height, and it does not use a Class-IV decision threshold.

## Exact restriction structure

A binary Life-like Moore-neighborhood rule on a periodic strip of height `k` is exactly a one-dimensional radius-one CA whose alphabet is the `2^k` possible vertical columns. A local update receives a left column, center column, and right column and returns the next center column.

### Height 1 is a 12-bit-forgetting quotient

At height one, vertical periodicity makes only six outer-totalistic local conditions reachable:

- dead center: `B0`, `B3`, `B6`;
- live center: `S2`, `S5`, `S8`.

Consequently the induced ECA number is

\[
r_1
= B_0 + 18 B_3 + 32 B_6 + 4 S_2 + 72 S_5 + 128 S_8.
\]

The map depends on six of the 18 rule bits and forgets twelve. Exhaustive enumeration of all `2^18 = 262144` Life-like rules gives exactly **64** ECA images, precisely the left-right-reflection-symmetric ECAs, with **4096 = 2^12** Life-like preimages per image.

For the experimental panel:

| 2D rule | rulestring | height-1 ECA |
|---|---|---:|
| Life | `B3/S23` | 22 |
| HighLife | `B36/S23` | 54 |
| Day & Night | `B3678/S34678` | 178 |
| explosive control | `B35/S236` | 22 |

Thus Life and `B35/S236` are **exactly the same dynamical rule at height 1**, despite their very different full-plane behavior. HighLife's height-1 identity with Rule 54 reproduces the known cylinder relation.

### Height 2 is already faithful to the full Life-like local law

Exhaustive enumeration of the height-two strip's `4^3 = 64` triples of left/center/right columns shows that every one of the 18 outer-totalistic conditions

\[
(c,n),\qquad c\in\{0,1\},\quad n\in\{0,\ldots,8\},
\]

occurs at some row of some local column triple. Therefore every birth bit `B0...B8` and every survival bit `S0...S8` can be read from the induced four-state radius-one local table.

Hence:

\[
\boxed{
\text{Life-like rule}\;\longmapsto\;\text{height-2 strip CA}
\text{ is injective.}
}
\]

This is an exact statement about local-rule identity, not about generic dynamics. It also gives a sharp pair-distinction valuation for this rule family: a pair of distinct Life-like rules is distinguishable either already at height 1 or, if it lies in the same 4096-rule height-1 fiber, necessarily at height 2. There are `64 * C(4096,2) = 536739840` unordered distinct pairs in the latter category, about **1.562%** of all unordered pairs of Life-like rules.

The exhaustive record is `results/cross_dimensional_class4_20260917/strip_restriction_exact.json`.

## Dynamic protocol

Rules:

- Life `B3/S23`;
- HighLife `B36/S23`;
- Day & Night `B3678/S34678`;
- explosive/chaotic adversary `B35/S236`.

Periodic strip heights:

\[
k\in\{1,2,3,4,6,8,12,16\}.
\]

Longitudinal width is 521. The primary initial density is 0.5; stress densities 0.3 and 0.7 were run only after the primary record had been saved. Each condition uses six seeded trajectories, burn-in 512, and 256 scored transitions.

The starred observables are the frozen dimension-neutral surrogates from the parent protocol:

- `R*`: standardized selective visitation of locally lower-preimage rule-input situations, relative to a strip-height-matched uniform predecessor reference;
- `M*`: held-out log-loss gain from eight steps of the center cell's own bit history over the current center bit alone;
- `S* = max(0,R*) max(0,M*)`;
- `alpha_x = log2(Dx(128)/Dx(64))`, using longitudinal perturbation-support span. Longitudinal span is primary because vertical graph diameter is mechanically capped by strip height.

No 1D numerical selection threshold is imported.

## Primary density-0.5 spectrum

| h | rule | R* | M* | S* | alpha_x |
|---:|---|---:|---:|---:|---:|
| 1 | Life | -0.100 | 0.130 | 0.000 | 0.973 |
| 1 | HighLife | 0.378 | 0.588 | 0.222 | 0.896 |
| 1 | Day & Night | -0.270 | 0.000 | 0.000 | 0.000 |
| 1 | B35/S236 | -0.107 | 0.130 | 0.000 | 0.981 |
| 2 | Life | 0.085 | 0.132 | 0.011 | 0.992 |
| 2 | HighLife | 0.211 | 0.570 | 0.121 | 1.315 |
| 2 | Day & Night | -0.045 | 0.697 | 0.000 | 0.000 |
| 2 | B35/S236 | -0.518 | 0.133 | 0.000 | 0.980 |
| 3 | Life | -0.097 | 0.130 | 0.000 | 1.025 |
| 3 | HighLife | 0.261 | 0.623 | 0.162 | 1.142 |
| 3 | Day & Night | 0.130 | 0.886 | 0.115 | 0.000 |
| 3 | B35/S236 | 0.117 | 0.346 | 0.040 | 0.034 |
| 4 | Life | 0.830 | 0.131 | 0.109 | 0.968 |
| 4 | HighLife | 1.532 | 0.707 | 1.083 | 0.767 |
| 4 | Day & Night | 2.218 | 1.121 | 2.487 | 0.349 |
| 4 | B35/S236 | 1.525 | 0.128 | 0.195 | 0.998 |
| 6 | Life | 0.473 | 0.204 | 0.096 | 0.908 |
| 6 | HighLife | 0.312 | 0.099 | 0.031 | 0.934 |
| 6 | Day & Night | 3.152 | 1.095 | 3.450 | 0.047 |
| 6 | B35/S236 | 0.177 | 0.012 | 0.002 | 0.956 |
| 8 | Life | -0.640 | 0.094 | 0.000 | 0.195 |
| 8 | HighLife | 0.420 | 0.009 | 0.004 | 0.186 |
| 8 | Day & Night | 3.840 | 0.120 | 0.460 | -0.052 |
| 8 | B35/S236 | 0.111 | 0.003 | 0.000 | 0.985 |
| 12 | Life | -0.645 | 0.181 | 0.000 | 0.030 |
| 12 | HighLife | 0.447 | 0.025 | 0.011 | 0.178 |
| 12 | Day & Night | 3.890 | 0.086 | 0.336 | 0.000 |
| 12 | B35/S236 | 0.080 | 0.002 | 0.000 | 0.989 |
| 16 | Life | -0.671 | 0.102 | 0.000 | 0.043 |
| 16 | HighLife | 0.393 | 0.037 | 0.014 | 0.169 |
| 16 | Day & Night | 3.983 | 0.096 | 0.384 | -0.503 |
| 16 | B35/S236 | 0.077 | 0.003 | 0.000 | 0.998 |

The main observation is **non-monotonicity**. Added transverse freedom does not make any one scalar smoothly approach a two-dimensional limit over these finite widths.

- HighLife begins as exact Rule 54 dynamics at `k=1`, remains strongly spreading through roughly `k=6`, and has a pronounced selective-persistence peak at `k=4`; by `k>=8` its random-strip ensemble has little temporal-history gain and much weaker longitudinal damage growth.
- Life spreads nearly ballistically through `k=6`, has modest positive selective-persistence only around `k=2,4,6`, and largely loses both under the burned random ensemble at several larger widths.
- Day & Night develops extremely large positive `R*` and `S*` at intermediate/larger widths but usually little long-horizon longitudinal disturbance growth after burn-in. Its two coordinates decouple rather than forming a stable “complex quadrant.”
- `B35/S236` is the cleanest spreading-only adversary at moderate and large widths: `alpha_x` returns to about one while `M*` and therefore `S*` fall almost to zero.

## Density stress

The 0.3 and 0.7 runs preserve the qualitative non-monotone picture but also expose strong ensemble dependence.

Examples:

- HighLife's `k=4` persistence peak appears at all three densities (`S*` about 1.01, 1.08, 1.15), while its spreading varies substantially.
- Day & Night at `k=6` has `S*` about 2.01, 3.45, 1.62 across densities 0.3, 0.5, 0.7, but `alpha_x` is respectively about 0, 0.047, and 1.021. The same local rule and strip height can therefore occupy very different spreading regimes under different initial ensembles.
- `B35/S236` remains close to ballistic longitudinal spreading (`alpha_x` roughly one) at most heights/densities while its `S*` tends toward zero at larger heights.
- Life has a notable large-height density effect: at `k=16`, density 0.3 gives `alpha_x≈0.924`, while densities 0.5 and 0.7 give about 0.043 and -0.053 respectively.

The complete stress record is `results/cross_dimensional_class4_20260917/strip_spectrum_stress.json`.

## Life versus B35/S236: hidden distinction becomes immediately dynamical

Life and `B35/S236` are identical at height one because both restrict to ECA 22. Matched initial states therefore remain exactly identical for every measured time at `k=1`.

At `k=2`, the newly exposed rule bits make the trajectories disagree after **one update**. Mean normalized Hamming disagreement at `t=1` is:

- density 0.3: about 0.072;
- density 0.5: about 0.147;
- density 0.7: about 0.224.

By `t=256` it is about 0.486, 0.466, and 0.473 respectively. Thus the height-two local-law injectivity is not a merely formal distinction for this pair: the added transverse degree immediately activates hidden rule differences and leads to macroscopically different trajectories.

This is a particularly clean example of a lower-dimensional quotient hiding distinctions that become explicit when one more transverse degree is available.

## Relation to the HighLife → Rule 54 bridge

The parent unit independently verifies that width-one HighLife is byte-identical to native ECA Rule 54 for 256 ticks on a random 521-cell state.

That bridge also exposed a measurement issue that matters here. `M*` and longitudinal damage spreading are exact under the state conjugacy because they depend only on the identical bit histories and XOR support. `R*` is **not** invariant: its local observation alphabet changes. The natural outer-totalistic observer identifies reflected ECA neighborhoods (`001` with `100`, and `011` with `110`), changing the predecessor reference and hence the retention score.

Therefore `R*` should be treated as a statistic of

\[
(\text{dynamics},\;\text{observation algebra},\;\text{reference ensemble}),
\]

not as an intrinsic scalar of the dynamics alone.

This distinction helps explain why a cross-dimensional phenotype cannot be established merely by comparing raw `R*` values.

## Observer chain rule: the hidden distinction can be retained as a residual coordinate

A post-hoc algebraic audit makes the observer dependence of `R*` more structured.

Let `Z` be a fine local symbol, `Y=phi(Z)` a deterministic coarse observation, `Q` the frozen fine reference distribution, `Q_Y` its pushforward, and `P` the trajectory distribution. Define the **unstandardized selective-surprisal gap**

\[
\Delta_Q(P)
=
\mathbb E_P[-\log_2 Q(Z)]
-
\mathbb E_Q[-\log_2 Q(Z)].
\]

Because

\[
-\log Q(Z)
=
-\log Q_Y(Y)
-
\log Q(Z\mid Y),
\]

there is an exact chain rule

\[
\boxed{
\Delta_Q(P)
=
\Delta_{Q_Y}(P_Y)
+
\left(
\mathbb E_P[-\log Q(Z\mid Y)]
-
\mathbb E_Q[-\log Q(Z\mid Y)]
\right).
}
\]

So a coarse observer does not force us to call the missing selectivity “gone.” It separates into a coarse-visible coordinate plus a **within-fiber residual** describing selection among distinctions the coarse observer identifies.

On the exact Rule-54 → width-one-HighLife observation map:

- fine gap: `0.2350280407` bits;
- coarse-visible gap: `0.2519276328` bits;
- within-fiber residual: `-0.0168995921` bits;
- reconstruction error: about `1.1e-16` bits.

The currently reported standardized `R*` does not inherit this additivity because each observer divides by a different reference standard deviation. This suggests that future cross-representation work should retain the unstandardized gap and its conditional residuals, rather than expecting one normalized retention scalar to be invariant.

For comparison, the ordinary KL chain rule

\[
D_{KL}(P\|Q)
=
D_{KL}(P_Y\|Q_Y)
+
\mathbb E_{P_Y}D_{KL}(P(Z\mid Y)\|Q(Z\mid Y))
\]

is monotone under coarse-graining. In this particular Rule-54 trajectory the conditional KL residual is numerically zero to floating precision, so `D_KL` is exactly unchanged by merging the reflected neighborhoods. That is a property of this trajectory/reference pair, not a general invariance claim.

The saved audit is `results/cross_dimensional_class4_20260917/observer_chain_rule.json` and the reproducer is `experiments/cross_dimensional_class4_20260917/observer_chain_rule.py`.

## What this supports

The strip program supports a stronger and more precise framing than the original “do known 2D Class-IV rules occupy the 54/110 quadrant?” question:

1. **Dimensional restriction defines exact quotients of rule identity.** In the Life-like family, height one forgets twelve local-law bits; height two recovers all of them.
2. **Added transverse freedom can activate previously invisible distinctions immediately.** Life and `B35/S236` are an exact witness.
3. **Dynamical phenotype across strip width is a spectrum, not a monotone scalar.** Persistence and spreading can peak at different widths and respond differently to the initial ensemble.
4. **Some observables are mapping-stable while others are observer-relative.** Bit-history prediction and support spreading transport cleanly through the exact HighLife/Rule-54 state conjugacy; the current retention statistic does not.

This is strongly suggestive of treating strip height as an observation/representation scale or filtration parameter. It does **not** prove that strip height is the same object as the project's affine-lift floor valuation.

## Limits and non-claims

- The dynamic results use finite strips, finite time, and Bernoulli initial ensembles.
- “Class IV” is not defined or inferred from these measurements.
- No threshold was tuned to separate 2D rules.
- Large `R*` or `S*` does not by itself imply localized computation, gliders, universality, or a Wolfram class.
- `alpha_x` is a finite 64→128 longitudinal growth exponent, not the old ECA `alpha_512` observable.
- The exact height-one/height-two restriction statements are specific to binary Moore outer-totalistic Life-like rules and periodic strips as defined here.
- Novelty of the exact restriction/floor observation has not been established by a dedicated prior-art search.

## Reproduction

Exact local-law restriction:

```bash
python experiments/cross_dimensional_class4_20260917/strip_restriction.py \
  --output results/cross_dimensional_class4_20260917/strip_restriction_exact.json
```

Primary strip spectrum:

```bash
python experiments/cross_dimensional_class4_20260917/strip_spectrum.py \
  --phase primary \
  --output-dir results/cross_dimensional_class4_20260917
```

Stress strip spectrum:

```bash
python experiments/cross_dimensional_class4_20260917/strip_spectrum.py \
  --phase stress \
  --output-dir results/cross_dimensional_class4_20260917
```

Expensive research replays should remain off automatic CI under repository policy.

## Next questions

1. Formalize the restriction maps `Res_k` as a filtration of local rule spaces and ask which algebraic/dynamical quantities are functorial under `Res_k`.
2. Replace or augment `R*` with an observation-covariant quantity whose transformation under coarse-graining can be stated explicitly.
3. Test natural macrocell embeddings such as documented Rule-110 simulations in HighLife/Day & Night, where both spatial and temporal rescaling are nontrivial.
4. Only after those mapping questions are pinned down, return anonymous cross-dimensional profiles to Jev; otherwise Jev may simply learn artifacts of the observer choice.
