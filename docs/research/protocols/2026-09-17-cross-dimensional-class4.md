# Protocol: cross-dimensional selective persistence and spreading

**Status:** FROZEN before implementation/evaluation  
**Date:** 2026-09-17  
**Author:** GPT-5.6 Sol, Groovy Commutator session  
**Protocol review:** none at freeze; run authorized by Myk 2026-09-17 in project chat (“make it so!”). Independent retrospective review is still required before merge to `main`.

## 1. Question

Does the ECA lead discovered by the Jev-guided work — selective predictive persistence together with sustained disturbance spreading — survive a change of dimension and representation?

This experiment asks two distinct questions and will not collapse them:

1. **Phenotype transfer.** Do independently established complex 2D Life-like cellular automata occupy a similar region of a dimension-neutral persistence × spreading profile, while simple and explosive/chaotic controls separate by mechanism?
2. **Mapping transfer.** When a known exact cross-dimensional restriction exists, which measurements are preserved or transform predictably under it?

This is not a universal definition of Class IV, a classifier-accuracy study, or a claim that all glider-bearing rules belong to one class.

## 2. Prior evidence and source freeze

The motivating ECA result was frozen and prospectively validated on 2026-09-16:

- `S = max(0,R) * max(0,M)` with an ECA-only threshold `S > 0.20`;
- sustained spreading gate `alpha_512 > 0.50`;
- 54/110 passed all five fresh conditions;
- fast-spreading Class-III-like controls had `S = 0`, while high-S Class-II-like controls failed spreading.

The old numerical thresholds are **not** transported into 2D.

Repository source SHA for this new unit: `4ff191cb46bd9e0a9b349487aa3875486932ac9d`.

External facts fixed before implementation:

- Conway Life: `B3/S23`.
- HighLife: `B36/S23`; LifeWiki records that an infinitely long line / width-1 cylinder emulates ECA Rule 54, and separately records an explicit Rule-110 unit-cell construction.
- Day & Night: `B3678/S34678`; LifeWiki records self-complementarity, a rich spaceship/puffer/oscillator ecology, and an explicit Rule-110 unit cell.
- `B35/S236` is fixed as an adversarial explosive/chaotic control: Eppstein describes growing chaotic regions and many gliders/spaceships; later literature explicitly contrasts it with Life-like Class-IV behavior.

The known Rule-110 constructions are **context only** in this first experiment. We do not implement a macrocell simulator here because doing so would confound measurement transfer with an engineered encoding. The exact HighLife width-1 restriction is the primary mapping control.

## 3. Fixed rule panel

### Complex exemplars (descriptive target set)

- Conway Life `B3/S23`
- HighLife `B36/S23`
- Day & Night `B3678/S34678`

These are not treated as IID positive samples and no accuracy estimate is allowed.

### Mechanism/adversarial control

- `B35/S236` — explosive/chaotic rule with many propagating structures.

### Synthetic simple controls

- `B/S` — all-dead map.
- `B/S012345678` — identity map (live survives, no births).
- `B012345678/S` — bit-complement map (dead always born, live always dies), period two.
- `B012345678/S012345678` — one-step all-live attractor.

### 1D calibration controls

- ECA 54 and 110 — prior core phenotype.
- ECA 5 and 62 — prior high-persistence / insufficient-spread confounders.
- ECA 122 and 126 — prior high-spread / zero-selective-persistence controls.

## 4. Dimension-neutral observables

The 2D test uses new starred observables. They are inspired by the prior ECA quantities but are not asserted to be algebraically identical.

### 4.1 `R*`: selective visitation of low-preimage local situations

At a site, define the rule-input symbol:

- in 1D ECA: the full three-bit radius-one neighborhood (`0..7`);
- in 2D outer-totalistic rules: `(center_bit, live_neighbor_count)` (`2 × 9 = 18` possible symbols).

Construct a **uniform predecessor reference** for the next-step rule-input symbol at the center:

- 1D: exhaustively enumerate all five-bit predecessor windows;
- 2D: Monte Carlo sample a frozen number of independent uniform 5×5 predecessor patches, evolve each one step only where needed to recover the central 3×3 successor patch, then encode its center rule-input symbol.

For reference symbol `z`, let `p_ref(z)` be its probability and define surprisal `q(z) = -log2 p_ref(z)` for supported symbols. The reference mean and standard deviation are taken under `p_ref`.

On burned trajectories, sample rule-input symbols and define

`R* = (mean_trajectory q(z) - mean_reference q(z)) / max(sd_reference q(z), 1e-12)`.

Thus `R* > 0` means the realized trajectory preferentially visits locally rarer / lower-preimage rule-input situations than a uniform predecessor ensemble. It is a selective-visitation statistic, not generic entropy.

### 4.2 `M*`: held-out temporal-history predictive gain

For each sampled site-time event, target the **next center bit**.

- baseline feature: current center bit only;
- history feature: the length-8 center-bit history ending at the current time.

Fit empirical Bernoulli predictors on training seeds only using Jeffreys smoothing (`Beta(1/2,1/2)`). Evaluate mean log loss on held-out seeds.

`M* = baseline_test_logloss - history_test_logloss` in bits/event.

Positive `M*` means temporal history retains predictive value beyond the current bit. Using center-bit history makes the definition identical in 1D and 2D and avoids giving the predictor the deterministic full local neighborhood.

### 4.3 `S*`

`S* = max(0,R*) * max(0,M*)`.

No threshold on `S*` is frozen for 2D. Primary comparisons use coordinates and ranks.

### 4.4 `alpha*`: disturbance spreading

Create a paired trajectory differing by one flipped site after burn-in. Let `D(t)` be the mean diameter of the XOR-support using the graph metric induced by the native neighborhood:

- 1D radius-one ECA: circular distance on the ring;
- 2D Moore-neighborhood rules: toroidal Chebyshev (`L_infinity`) distance.

Use horizons `t1=64`, `t2=128` for the first cross-dimensional run and define

`alpha* = log2(D(128) / D(64))`

when both diameters are positive. If both are equal and nonzero, `alpha*=0`; if the disturbance has vanished by both horizons, record `alpha*=0` and `extinct=true`. Grid sizes are chosen so the causal cone cannot wrap before `t2`.

This shorter horizon is a computationally bounded cross-dimensional probe and is **not** numerically equated with the old `alpha_512`.

## 5. Simulation protocol

### 1D calibration

- ring width: 521;
- densities: primary `0.5`, stress `0.3`, `0.7`;
- burn: 512 steps;
- scored trajectory: 256 steps;
- six independent seeds per condition;
- first four seeds train `M*`, last two test it;
- disturbance: 8 origins × 4 base seeds = 32 paired trials per rule/condition.

### 2D panel

- torus: `263 × 263` (strictly larger than `2*128+1`);
- densities: primary `0.5`, stress `0.3`, `0.7`;
- burn: 512 steps;
- scored trajectory: 256 steps;
- six independent seeds per condition;
- first four seeds train `M*`, last two test it;
- trajectory sampling: deterministic subsampling capped at 100,000 events per rule/condition;
- `R*` uniform predecessor reference: 100,000 frozen 5×5 samples per 2D rule;
- disturbance: 8 origins × 4 base seeds = 32 paired trials per rule/condition.

Seeds are derived deterministically from SHA-256 of `(protocol_id, rule_name, condition, replicate, purpose)`.

## 6. Exact mapping control: HighLife width-1 cylinder

Before reading any phenotype result, exhaustively evaluate all eight `(left,center,right)` triples under `B36/S23` on a one-row torus where Moore-neighborhood offsets wrap and therefore count repeated positions.

The preregistered expected truth table is ECA Rule 54:

`111,110,101,100,011,010,001,000 -> 0,0,1,1,0,1,1,0`.

This is prior art / an implementation sanity check, not new evidence of Class-IV transfer.

Then run paired random 1D histories through:

- native ECA 54; and
- the HighLife width-1 cylinder implementation.

Require byte-for-byte state agreement for every tested tick. Failure invalidates cross-dimensional mapping claims until fixed.

The starred observables may then be computed on the same histories through both representations. Because the configurations are bit-identical under the width-1 restriction, `M*`, trajectory symbol sequences after the appropriate symbol recoding, and spreading histories should agree up to the explicitly different local-symbol representation. We report which quantities are exactly invariant and which require a representation map.

## 7. Predeclared qualitative predictions

These are falsifiable but deliberately weaker than a 2D threshold classifier.

1. ECA 54/110 should remain in the joint positive-`S*` / sustained-spread region under the starred surrogate often enough to justify proceeding. If both lose the relation completely, the 2D generalization is stopped and reported as a failed surrogate.
2. ECA 5/62 should tend toward higher `S*` than spreading; ECA 122/126 should tend toward spreading without positive `S*`. Exact old thresholds are not expected to reproduce.
3. `B35/S236` should show strong spreading. If it also matches the complex exemplars on selective persistence, then the proposed phenotype does not distinguish the intended Life-like complex regime from this chaotic/glider-rich adversary.
4. At least two of Life, HighLife, Day & Night are expected to show both positive selective predictive persistence and sustained spreading under at least the primary condition. Failure is informative and no post-hoc retuning is allowed inside this protocol.
5. The simple synthetic controls should not jointly occupy the high-`S*` / sustained-spread region.

## 8. Primary evaluation

For each rule and condition report separately:

- `R*`, `M*`, `S*`;
- `D(64)`, `D(128)`, `alpha*`, extinction fraction;
- median and range across seeds/trials;
- raw event/trial counts.

Primary graphical analysis is a scatter of `S*` versus `alpha*`, with rule names shown only after all numeric results are saved.

No learned boundary, AUC, threshold optimization, or weighted composite is permitted in this first 2D experiment.

## 9. Failure and stopping rules

- Any HighLife-width-1 mismatch with Rule 54 stops mapping interpretation.
- If `M*` has fewer than two held-out seeds with usable events, that rule-condition is censored.
- If the 2D predecessor-reference Monte Carlo leaves any trajectory-visited local symbol unsupported, increase the **reference sample count only** using a predeclared doubling schedule (200k, 400k, 800k); do not alter rules, trajectories, or scoring.
- If memory/runtime requires reducing the simulation budget, record the deviation before reading outcomes and rerun all panel members under the same reduced budget.
- No rule may be dropped because its outcome is inconvenient.

## 10. Non-claims

This experiment does not establish:

- a universal definition of Class IV;
- equivalence of 1D and 2D Wolfram classifications;
- that gliders imply selective predictive persistence;
- that Turing universality implies the phenotype;
- that a Rule-110 macrocell simulation transfers generic ambient behavior;
- that the project’s affine-oriented lift has generic 2D Class-IV ambient dynamics;
- novelty over the broad information-storage × spreading literature.

## 11. Next gate if the experiment survives

Only after this result is saved:

1. form anonymous mixed 1D/2D profiles and rerun frozen Jev J1–J6 without exposing dimension/rule/class;
2. compare natural HighLife/Day-&-Night embeddings against the project’s affine-oriented 54/110 lifts;
3. test whether any surviving quantity is invariant/covariant under both kinds of representation change;
4. separately study natural ambient completions of the affine-oriented lift.
