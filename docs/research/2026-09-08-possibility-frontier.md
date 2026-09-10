# Possibility lives on a forgetting frontier

Research022–025 asked which distinctions a representation erases, which of those distinctions return to causal relevance, and which can be forgotten safely. This note turns that decomposition around.

The motivating question is:

> **Does a useful representation sit between two different pressures: breaking predictive closure with as little forgetting as possible, and keeping as many genuinely different futures open as possible?**

On the finite ECA systems tested here, the answer is yes in a precise representation-relative sense. The observer that first breaks closure and the observer that maximizes future repertoire are different for almost 90% of rules with any tested closure-breaking representation, and for every repository-labeled Class-III and Class-IV rule.

The important caveat is that the microscopic system remains deterministic. “Possible futures” here means **distinct observed future trajectories compatible with the same present macrostate**, not physical indeterminism.

## Future repertoire was already hiding inside Research025

Fix deterministic dynamics `E`, cadence `q`, and observation `P`, and write

\[
Y_t=P(E^{qt}(S)).
\]

Let `C_t` be the partition of microstates by their observed word `(Y_0,\ldots,Y_t)`, and let `C_\infty` be the stable future-equivalence partition.

Research025 decomposed information forgotten by the current observation as

\[
H(S\mid Y_0)=I_{\rm latent}+I_{\rm shielded}.
\]

The latent term has an exact second reading:

\[
\boxed{V_\infty(E,P)=H(C_\infty\mid Y_0)=H((Y_1,Y_2,\ldots)\mid Y_0)=I_{\rm latent}.}
\]

`V_infinity` is the Shannon entropy of distinguishable observed futures hidden inside the present macrostate. We call it **future repertoire**.

At finite horizon,

\[
V_t(E,P)=H(C_t\mid Y_0)
\]

measures how much future distinction has become available by horizon `t`. It grows monotonically until the finite predictive partition stabilizes.

This gives an exact triangle:

\[
\boxed{\text{forgotten bits}=\text{future-repertoire bits}+\text{shielded bits}.}
\]

So forgetting is not one thing. Some of it stores future differentiation; some of it removes distinctions that the chosen observed future will never use.

## The two optimization problems

The [frozen protocol](protocols/possibility-frontier-20260908.md) distinguishes two questions over a bounded static observer family.

The first asks for the **least forgetting that breaks closure**,

\[
\lambda_{\min}(E)=\min_{P:V_\infty(E,P)>0}H(S\mid P(S)).
\]

The second asks for the **largest future repertoire**,

\[
V_{\max}(E)=\max_P V_\infty(E,P).
\]

A third quantity measures the quality of the forgetting,

\[
\eta(E,P)=\frac{V_\infty}{H(S\mid P(S))}=1-\frac{I_{\rm shielded}}{H(S\mid P(S))}.
\]

`eta` is the fraction of forgotten information that remains future-relevant.

These objectives need not agree. Low-loss closure breaking wants the smallest perturbation of a sufficient state description. Maximum repertoire wants the largest unresolved family of future trajectories. Maximum efficiency wants forgotten distinctions to be almost entirely latent rather than dead.

## Exact observer census

The primary census exhausts all 256 ECA rules on the periodic 12-cell ring.

The static family contains:

- the identity observation;
- a constant observation;
- all 14 nonconstant Boolean maps on nonoverlapping two-cell blocks, with matched cadence `q=2`;
- all 254 nonconstant Boolean maps on nonoverlapping three-cell blocks, with matched cadence `q=3`.

Output complements are exact relabelings, so only 7 block-2 and 127 block-3 complement classes need independent computation. The rule-relative derivative is measured separately as a relational observer but does not define the static optimum.

The implementation reproduces the existing exact closure controls:

- 92 fine rules have a closed block-2 observation;
- 202 canonical block-2 factors, corresponding to the known 404 complement-paired triples;
- 141 fine rules have a closed block-3 observation;
- 1,656 canonical block-3 factors, corresponding to the known 3,312 complement-paired triples;
- 30 derivative observations close exactly.

The [independent audit](../../results/possibility_frontier_20260908_audit.json) also reconstructs selected future partitions directly from explicit observed words and verifies every block-map complement as an exact bitwise relabeling.

## Finding 1: the two optima usually disagree

Of the 256 fine rules, 247 have at least one tested static observation with positive future repertoire.

Among those 247:

- **25** have some observer that simultaneously minimizes closure-breaking forgetting and maximizes future repertoire;
- **222** do not.

Thus

\[
\boxed{89.88\%}
\]

of rules with a tested closure breaker separate the two objectives.

The disagreement is complete in the more dynamically complex repository classes:

| Wolfram label | Rules with a breaker | Same observer can optimize both |
| --- | ---: | ---: |
| I | 18 | 2 |
| II | 189 | 23 |
| III | 26 | **0** |
| IV | 14 | **0** |

For every Class-III and Class-IV rule, the minimum-forgetting and maximum-repertoire poles are distinct in this observer family.

The minimum forgetting needed to break closure is usually small relative to the available static coarse-grainings:

- 236 rules break closure at 6 forgotten bits;
- 8 require about 7.132 forgotten bits;
- 3 first break at 8 forgotten bits;
- 9 never break closure under any tested static observation.

But maximum repertoire usually lies elsewhere: 171 rules maximize it with a block-3 observer, while 76 maximize it with block-2.

This is the first direct support for the intuition that **“make closure fail as cheaply as possible” and “leave the richest future open” are different representation-selection pressures**.

## Finding 2: future repertoire is not monotone in forgetting

Two trivial endpoints are exact controls.

With identity observation,

\[
L=0,\qquad V_\infty=0.
\]

Nothing is forgotten, so the present microstate has one deterministic future.

With a constant observation,

\[
L=12,\qquad V_\infty=0.
\]

Everything is forgotten, including every future distinction visible to that same observation.

The interesting region therefore lies between fidelity and oblivion.

More importantly, this is not only an endpoint effect. Across the **interior** forgetting levels supplied by the block-2/block-3 observer family:

- 227/256 rules have a nonmonotone best-repertoire curve;
- 20 are strictly increasing across the interior levels;
- 9 are nondecreasing but not strict.

So “forget more” is not a general recipe for producing more possibility. The structure of the erased distinction matters.

The nondominated `(forgotten bits, future-repertoire bits)` points form a genuine Pareto frontier. Across the 256 rules the frontier contains between 1 and 7 distinct objective points, with a median of 4.

## Finding 3: complex rules turn forgotten bits into future differentiation

Wolfram-class comparisons were explicitly exploratory, but the ordering is striking.

Among rules with a closure breaker, the median maximum future repertoire is:

| Class | Median `V_max` |
| --- | ---: |
| I | 3.289 bits |
| II | 5.443 bits |
| III | 7.319 bits |
| IV | **8.361 bits** |

The median best possibility efficiency is:

| Class | Median max `eta` |
| --- | ---: |
| I | 0.478 |
| II | 0.742 |
| III | 0.940 |
| IV | **0.967** |

In this bounded representation family, Class-III/IV rules are unusually good at turning information erased now into distinctions that later reappear in the observed future, rather than into permanently shielded information.

The location of the maximum also shifts with the conventional class labels. For nontrivial rules, the median forgetting level at maximum repertoire rises from about 7.13 bits in Class I, to 8 bits in Class II, 8.75 bits in Class III, and 9.83 bits in Class IV.

This should **not** be promoted into a Wolfram-class classifier. The observer family is highly structured, symmetry relatives are not independent replications, and the matched cadence changes with block size. But the pattern suggests a more precise version of an “edge of chaos” intuition worth testing later:

> complex dynamics may support representations in which a large fraction of what is hidden now remains available as structured future differentiation.

## A clean Class-IV split

All 14 labeled Class-IV rules show the same qualitative optimizer structure:

- the minimum-forgetting closure breaker is block-2;
- the maximum-repertoire observer is block-3;
- the maximum-efficiency observer is block-2;
- no minimum-forgetting observer is also a maximum-repertoire observer.

For Rule 110 at `n=12`, for example, a balanced block-2 projection forgets 6 bits and hides about

\[
5.993
\]

bits of distinguishable future, leaving only about `0.0068` bits permanently shielded:

\[
\eta\approx0.99886.
\]

The maximum-repertoire block-3 observer forgets about `9.826` bits and exposes about

\[
8.361
\]

bits of future repertoire. It creates more absolute possibility, but less efficiently: about 1.465 forgotten bits are permanently irrelevant to its future.

So there are two genuinely different “good” descriptions:

- one lies close to the **minimum-loss / nearly-pure-latency** edge;
- the other opens a **larger absolute future repertoire** by forgetting substantially more.

Rule 106 gives the same separation with much longer memory: its block-2 efficiency optimum has `h*=13`, while its block-3 repertoire maximum has `h*=19` on the 12-cell ring.

## Fresh size check

After the `n=12` winners were known, a [fresh-size protocol](protocols/possibility-frontier-size-validation-20260908.md) froze six pairs of observers before evaluating the 18-cell ring.

The rules were 30, 54, 90, 106, 110, and 184.

All **6/6** predictions passed:

- both frozen observations remain nonclosed;
- the `n=12` maximum-repertoire observer still has strictly greater `V_infinity` than the frozen minimum-forgetting breaker;
- the minimum-forgetting observer still forgets fewer bits.

Rule 184 is a useful control because both competing observations are block-2 maps. At `n=18`, its minimum breaker forgets 9 bits and carries about 6.297 bits of future repertoire; the competing block-2 map forgets about 10.698 bits and carries about 7.958 bits of future repertoire.

So the observed tension is not merely an artifact of comparing block size 2 against block size 3.

## The derivative occupies a different part of the frontier

The derivative observation is rule-relative and therefore excluded from the static optimization. Comparing it afterward is informative.

For every Class-I and Class-IV rule, and for most Class-II/III rules, the derivative point is not dominated by any tested static observation in the `(forgetting, repertoire)` plane. It often forgets much less than a static block map while converting nearly all of that forgotten information into future relevance.

For 10 of the 14 Class-IV rules, derivative possibility efficiency exceeds the best static efficiency.

This reinforces the earlier observer-search result: a relational variable built from the dynamics can occupy a qualitatively different region of representation space than fixed block statistics.

## Relation to classical entropy of dynamical partitions

There is established mathematics directly underneath `V_t`.

An observation defines a partition `xi` of state space. Repeated observation of a trajectory corresponds to the joined refinement

\[
\xi\vee E^{-q}\xi\vee\cdots\vee E^{-qt}\xi.
\]

The entropy of this joined partition is exactly `H(C_t)`, so

\[
V_t=H\!\left(\bigvee_{j=0}^{t} E^{-qj}\xi\right)-H(\xi).
\]

This is standard partition-refinement machinery from ergodic theory. Kolmogorov–Sinai entropy studies the asymptotic **rate** of growth of such joined-partition entropy under an invariant measure.

The present experiment is different in three ways:

1. the finite deterministic systems eventually saturate instead of sustaining a positive asymptotic rate;
2. the uniform initial microstate ensemble is not assumed to be invariant under a noninvertible ECA;
3. the research object is the **observer-selection frontier** between present forgetting and accumulated future refinement, not the entropy rate of a fixed partition.

So `V_t` has classical ancestry; the particular possibility/forgetting optimization is the new project question. See Yakov Sinai's [Kolmogorov–Sinai entropy overview](https://www.scholarpedia.org/article/Kolmogorov-Sinai_entropy) for the standard partition-entropy construction.

## Relation to predictive compression

The information bottleneck and predictive rate-distortion traditions ask for compressed representations that preserve information relevant to a target or future. That is close to the minimum-sufficient-state side of the Groovy program.

The possibility objective here deliberately looks at the complementary side. It asks how much **future distinction remains unresolved inside the current representation**.

There is another important difference: `P` defines both the current macrostate and what counts as a distinguishable future macrotrajectory. This is not ordinary compression against a fixed external target variable.

A useful way to say the tension is therefore:

> predictive compression asks which distinctions must be kept now to know the future; the possibility frontier asks which distinctions can be left unresolved now while still producing many different futures later.

The two views meet at future equivalence. For nearby compression formalisms see Tishby, Pereira, and Bialek's [information bottleneck](https://arxiv.org/abs/physics/0004057) and Marzen and Crutchfield's [causal rate-distortion](https://arxiv.org/abs/1412.2859).

## Revised interpretation

Research025 gave

\[
\text{forgotten}=\text{latent}+\text{shielded}.
\]

Research026 gives the latent term another name:

\[
\boxed{\text{latent information}=\text{future repertoire hidden in the present}.}
\]

This makes the representation problem explicitly multi-objective.

One pole seeks a compact predictive state by removing safely forgettable distinctions and restoring latent ones.

Another seeks a present macrostate compatible with a rich family of distinguishable continuations.

Neither identity nor oblivion achieves the latter. Future possibility appears in the interior, and for most rules there is no single tested observer that simultaneously reaches the minimum closure-breaking loss and the maximum repertoire.

So the emerging picture is:

\[
\boxed{\text{a representation negotiates between closure and possibility by choosing which distinctions to resolve now}.}
\]

## What this does not yet establish

- The minimum closure-breaking loss is relative to a restricted family of local block observations. Over arbitrary state partitions it can be trivialized by merging a tiny number of states, so locality/description complexity must remain part of any general theory.
- `V_infinity` is observer-relative future diversity, not action-dependent agency or metaphysical free choice.
- The class ordering is exploratory.
- The block-2/block-3 comparison changes cadence with spatial scale; the primary frontier is over `(P,q)` scale descriptions.
- A finite ECA frontier does not imply that natural systems optimize the same objectives.

## Next question

The most interesting next move is no longer simply “find a local certificate for safe forgetting.”

We now have two dual design problems:

1. **predictive closure:** find the smallest state description that restores every distinction needed by the future;
2. **possibility preservation:** find a compact present description that leaves the richest structured family of futures unresolved.

A theory of useful representations may need both.

The obvious next experiment is to enlarge the observer family *constructively*: use the latent/shielded defect mechanics from Research025 and selector shielding to add or remove state variables, then ask whether those adaptive representations move along the Pareto frontier in a controlled way rather than by blind observer search.
