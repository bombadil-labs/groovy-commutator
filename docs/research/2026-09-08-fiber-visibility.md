# Which forgotten distinctions come back?

Research022–024 moved the Groovy Commutator away from a same-rule commutator test and toward a general question about lossy representations. This note asks the next exact question: **when an observation identifies two microstates, which hidden distinctions later return to the observed variables, and which remain invisible forever?**

The finite-state answer gives a useful decomposition of coarse-graining. Some discarded information is merely **latent**: it is invisible now but still lies in the causal future of the observation. Other discarded information is **shielded**: no future observation can distinguish it. The stable future-equivalence partition is the smallest exact predictive refinement of the chosen observation.

## Future equivalence

Fix deterministic dynamics `E`, cadence `q`, and observation `P`, and write

\[
Y_t(s)=P(E^{qt}(s)).
\]

Two states are future-equivalent when their entire observed futures agree,

\[
s\equiv_\infty s'
\quad\Longleftrightarrow\quad
P(E^{qt}s)=P(E^{qt}s')\quad\text{for every }t\ge0.
\]

On a finite state space, repeated history refinement stabilizes exactly at this relation. It is the coarsest forward-invariant refinement of the current observation: any exact predictive state compatible with `P` must distinguish states that eventually have different observed futures, and it need not distinguish states whose observed futures are identical forever.

This yields the exact information budget

\[
H(S)=H(P(S))+I_{\rm latent}+I_{\rm shielded}.
\]

Here `I_latent` is hidden by the present observation but restored by the minimal predictive refinement; `I_shielded` remains absent from the entire observed future.

## Exact n=12 census

The preregistered census exhausts all 256 elementary cellular automata on the 12-cell periodic ring for two observer families:

- the rule-relative derivative `D_A(S)=S XOR E_A(S)`, sampled every fine step;
- all seven output-complement classes of nonconstant two-cell Boolean block observations, sampled every two fine steps.

For each `(E,P)` the experiment counts initially hidden pairs, the exact first-visibility histogram, permanently hidden pairs, and whether permanent pairs eventually coalesce microscopically or remain physically distinct. The exact history depth from Research023 equals the largest finite first-visibility time in every case.

Every static two-cell observer leaves some pairs hidden forever. At the same time, every one of the 98 Class-IV rule/observer combinations contains some initially hidden distinctions that later return to visibility. Static block variables therefore mix safe forgetting with premature forgetting in precisely the regime where the project most wants compact effective descriptions.

The derivative observer behaves differently. Across the full derivative census, **no permanently hidden pair is coalescent**. This has a direct algebraic reason: if two trajectories have the same derivative history

\[
D_t=S_t\oplus S_{t+1}
\]

and ever share an endpoint `S_T`, then

\[
S_{T-1}=D_{T-1}\oplus S_T
\]

forces the preceding states to agree, and induction reconstructs equality all the way back to the initial state. Distinct states with identical derivative histories therefore cannot later merge. Any information the derivative forgets forever remains physically instantiated forever.

## Rule 106: the same hidden defect has two fates

The cleanest mechanism appears under Rule 106 with block-2 parity. Rule 106 has the local form

\[
E_{106}(S)_i=S_{i+1}\oplus(S_{i-1}S_i).
\]

For two trajectories with difference `delta=S XOR S'`, the difference update is

\[
\delta'_i=\delta_{i+1}
\oplus S_{i-1}\delta_i
\oplus S_i\delta_{i-1}
\oplus\delta_{i-1}\delta_i.
\]

The hidden mode is therefore a cocycle over the base trajectory: its fate depends on the common context, not only on the defect shape.

At ring width 20, the microstate pairs `1` versus `2` and `25` versus `26` begin with the same observer-null adjacent defect `{0,1}`.

For `1` versus `2`, the defect translates one coarse block per macrostep, the joint pair repeats after ten macrosteps, and parity never distinguishes the trajectories. The microscopic difference remains nonzero forever on the finite joint orbit.

For `25` versus `26`, the same adjacent defect translates in the same way for 50 macrosteps. At macrostep 51 the surrounding context causes the difference to change shape, and parity sees it for the first time. Thus the same hidden mode is permanently shielded in one context and latent in another.

An exhaustive local context audit reduces next-step leakage of the translating defect to a finite Boolean condition on nearby shared bits. That supplies a one-dimensional analogue of the selector-relative visibility mechanism found independently in the 2D strip work.

## The long memory tail is real but exceptional

At `n=20`, Rule 106 with block parity has exact history depth `h*=51`, but this is a worst-case tail rather than a typical memory time. Of 536,346,624 initially hidden unordered pairs, about 98.45% split after one macrostep. Only 60 pairs survive invisibly to the final split at step 51, and all 60 carry the same adjacent two-bit defect up to cyclic translation. Another 135,001 pairs remain hidden forever on the finite state graph.

So an effective description can have a very long exact memory because of a tiny exceptional family of coherent hidden modes. A scalar `h*` is therefore useful but incomplete; the full visibility-time distribution matters.

## A confirmed arithmetic lifetime across ring size

Exploration of the fixed `25` versus `26` witness suggested an arithmetic staircase in its first-visibility time as the even ring width changes. Before inspecting widths 102 and above, the recurrence was frozen.

Every one of the 50 fresh even widths from 102 through 200 split at the preregistered predicted time, with no formula edits. The increment sequence follows a 2-adic ruler pattern. This is strong finite evidence that the hidden-mode lifetime is organized by ring arithmetic, but it is not an all-width or infinite-lattice theorem. See the [frozen protocol](protocols/rule106-visibility-scaling-20260908.md) and [checker](../../scripts/check_rule106_visibility_scaling.py).

## What this adds to the project

The current coarse state `P(S)` is not the final object. The exact predictive quotient is the future-equivalence class of `S`. The gap between those two states is precisely the information the coarse representation discarded too early.

This gives three complementary questions:

1. **Closure:** is current observational equivalence already forward invariant?
2. **Memory:** how long can a distinction remain hidden before it exits observational equivalence?
3. **Safe forgetting:** which distinctions remain observationally equivalent forever, and what physical mechanism keeps them that way?

The concurrent [selector-shielding note](2026-09-08-selector-shielding.md) attacks the third question from the opposite direction: instead of computing future equivalence by partition refinement, it identifies state-dependent physical read geometry that can keep nearby differences causally invisible.

## Limits and next question

All exhaustive claims here concern finite periodic rings. Future-equivalence on a finite graph does not by itself prove an infinite-lattice quotient, and the confirmed Rule-106 lifetime recurrence remains a finite fresh-range result.

The strongest next mathematical target is a general local criterion for forward invariance of observational indistinguishability: a nonlinear analogue of an unobservable subspace that can explain both the Rule-106 defect-in-context and the selector-relative shielding walls.
