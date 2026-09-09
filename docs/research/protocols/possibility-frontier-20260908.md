# Protocol: forgetting versus future possibility frontier — 2026-09-08

**Status:** frozen before the new observer census.  
**Branch:** `research/possibility-frontier-20260908`

## Question

Research022–025 separate information erased by an observation into two parts: distinctions that later return to observed relevance and distinctions that remain absent from the entire observed future. The motivating intuition for this checkpoint is that representation choice may therefore face two different pressures:

1. **break closure with as little forgetting as possible**; and
2. **make as many genuinely different futures compatible with the present macrostate as possible**.

These need not select the same representation.

The experiment asks whether there is a measurable Pareto frontier between **forgetting** and **future repertoire**, and whether the observer that first breaks closure is usually different from the observer that maximizes future possibility.

## Exact finite-state objects

Fix deterministic dynamics `E`, cadence `q`, observation `P`, and the uniform ensemble over every microstate `S` of a finite periodic ring. Write

\[
Y_t=P(E^{qt}(S)).
\]

Let `C_t(S)` be the equivalence class induced by the observed word `(Y_0,...,Y_t)`, and let `C_infinity` be the stable future-equivalence class obtained by exact partition refinement.

Define total information forgotten by the present observation

\[
L(P)=H(S\mid Y_0).
\]

Research025 gives the exact decomposition

\[
L(P)=I_{\rm latent}(E,P)+I_{\rm shielded}(E,P),
\]

where

\[
I_{\rm latent}(E,P)=H(C_\infty\mid Y_0)
\]

and

\[
I_{\rm shielded}(E,P)=H(S\mid C_\infty).
\]

`I_latent` has a second interpretation that is primary here. Because a stable predictive class is exactly an observed future trajectory class,

\[
\boxed{V_\infty(E,P)=H((Y_1,Y_2,\ldots)\mid Y_0)=I_{\rm latent}(E,P)}.
\]

Thus `I_latent` is the Shannon entropy of the distinguishable observed futures hidden inside the current macrostate. Call it **future repertoire**.

At finite horizon,

\[
V_t(E,P)=H(C_t\mid Y_0)
\]

is the entropy of distinguishable observed prefixes through horizon `t`; it is monotone nondecreasing and converges exactly to `V_infinity` on the finite system.

## Primary observer family

Use all 256 elementary CA rules at periodic ring width `n=12`.

For each fine rule evaluate:

1. **Identity control**, `P(S)=S`, `q=1`.
2. **Constant control**, `P(S)=0`, `q=1`.
3. Every nonconstant Boolean **block-2** observation `{0,1}^2 -> {0,1}` with matched cadence `q=2`; quotient output complementation for computation but retain all 14 names in published data.
4. Every nonconstant Boolean **block-3** observation `{0,1}^3 -> {0,1}` with matched cadence `q=3`; quotient output complementation for computation but retain all 254 names in published data.
5. The rule-relative **derivative observation** `D_A(S)=S XOR E_A(S)`, `q=1`, as a relational comparison outside the static block family.

The primary static search space for optimization is identity + constant + every block-2 and block-3 observation. The derivative is compared to that frontier but does not participate in defining the static optimum.

## Primary measurements

For each `(E,P)` record:

- `visible_bits = H(Y_0)`;
- `forgotten_bits = L(P)`;
- `future_repertoire_bits = V_infinity = I_latent`;
- `shielded_bits = I_shielded`;
- `possibility_efficiency = V_infinity / L` when `L>0`, else undefined;
- `predictive_state_bits = H(C_infinity)`;
- exact closure (`V_infinity=0`, equivalently no predictive refinement beyond `Y_0`);
- history depth `h*`;
- horizon repertoire curve `V_t` through stabilization.

The information identity

\[
H(S)=H(Y_0)+V_\infty+I_{\rm shielded}
\]

must close numerically to tolerance for every row.

## Two preregistered optimization problems

For each fine rule, over the static observer family define the **minimum closure-breaking forgetting**

\[
\lambda_{\min}(E)=\min_{P:V_\infty(E,P)>0} L(P),
\]

and retain every observer attaining it.

Separately define the **maximum future repertoire**

\[
V_{\max}(E)=\max_P V_\infty(E,P),
\]

again retaining every maximizer.

The primary tension statistic is whether the argmin set for `lambda_min` intersects the argmax set for `V_max`.

Also compute the observer(s) maximizing

\[
\eta(E,P)=V_\infty/L,
\]

which measures how much of the forgotten information remains future-relevant rather than safely shielded.

## Pareto frontier

For each rule, an observer `P` is dominated if another observer `Q` satisfies

\[
L(Q)\le L(P),\qquad V_\infty(Q)\ge V_\infty(P),
\]

with at least one strict inequality.

The nondominated observers form the **forgetting / possibility frontier**. Record its size, block-size composition, and whether derivative observations lie on or above the static frontier in the `(L,V_infinity)` plane.

Because `0 <= V_infinity <= L <= n`, identity and constant observations are exact controls at opposite forgetting extremes. Both are predicted to have zero future repertoire: the identity because it forgets nothing, the constant observation because it forgets every observed distinction including the future itself.

## Preregistered hypotheses and controls

1. `V_infinity` must equal `latent_future_relevant_bits` from the Research025 construction when evaluated on the same `(E,P)`.
2. Exact factor closure implies `V_infinity=0`.
3. Identity and constant controls both have `V_infinity=0`.
4. For every nontrivial observer, `0 <= V_infinity <= L`.
5. There should exist many rules with at least one interior observer having `V_infinity>0`; otherwise the proposed possibility axis is vacuous.
6. **Primary hypothesis:** the observer(s) minimizing closure-breaking forgetting and those maximizing future repertoire will often be different. Report the exact overlap frequency across all 256 rules; do not repair the objective definitions after inspection.
7. **Secondary hypothesis:** maximum possibility efficiency `eta` will favor observers that discard relatively little permanently shielded information, and need not coincide with either primary optimum.
8. Wolfram-class comparisons are exploratory. Do not promote a class-separation pattern into a classifier from this census.

## Selected repertoire curves

Before inspection, retain detailed `V_t` curves for rules `30, 54, 90, 106, 110, 184` under:

- the minimum-forgetting closure breaker;
- the maximum-repertoire observer;
- the maximum-efficiency observer;
- the derivative observer.

These examples cover linear, chaotic, complex, traffic-like, and previously studied hidden-mode cases. Curves are descriptive diagnostics, not additional hypothesis tests.

## Scope and nonclaims

- All exact claims concern the stated finite periodic rings.
- `V_infinity` is future repertoire relative to the chosen observation, not metaphysical indeterminism; the microscopic dynamics remains deterministic.
- Shannon entropy weights futures by the uniform microstate ensemble. Distinct-future counts may be reported secondarily but are not the primary possibility measure.
- A Pareto frontier in this finite observer family does not prove that biological, computational, or physical complexity universally optimizes the same tradeoff.
- Static block observers are a deliberately bounded representation family. Relational, dynamical, stateful, and adaptive observers may occupy different regions of the frontier.