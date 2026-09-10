# A third representation objective: the control channel is now specified

The [parallel-agent protocol](protocols/representation-empowerment-20260910.md) completes the proposal-writing scope of [issue63](https://github.com/bombadil-labs/groovy-commutator/issues/63#issuecomment-5622837474). The [named representation-empowerment census](../knowledge/representation-empowerment-planned.md) is **planned and unrun**. This checkpoint registers the work and records the source and certification contract; it reports no new channel measurement.

## Preserve the observer and its clock

The prior [Research026 note](2026-09-08-possibility-frontier.md), [implementation](../../scripts/experiment_possibility_frontier.py), [summary](../../results/possibility_frontier_20260908_summary.json), and [independent audit](../../results/possibility_frontier_20260908_audit.json) fix the static census. These source references were reviewed at main 40ee57a5672df36a6793a5bcdd720e1cc565212e before the new evaluation.

Its objects are observer/cadence pairs (P,q), not observations alone. Identity and constant controls use q=1; block-two observations use q=2; block-three observations use q=3. The static family is identity, constant, all 14 nonconstant two-bit maps and all 254 nonconstant three-bit maps. Output complements permit the original 7/127 representative reduction, provided the implementation preserves the induced outcome relabeling. The rule-relative derivative is a separate prior diagnostic and is not added to the static optimum.

Write E for one fine ECA update and T=E^q for the given observer's macro step. One action occurs before the first T step. Finite outcomes observe T(a(S_0)),...,T^h(a(S_0)); the initial-inclusive variant also includes P(a(S_0)). The stable future class uses the same T. Thus h is a macro-observation horizon and hq is its fine-tick duration. Reusing the old stable class while silently changing its sampling clock would change the question.

The original 247-rule breaker denominator and prior repertoire-optimum conventions are retained. The nine other rules are controls. The frozen majority prediction is still unrun.

## Information available to the controller

The action set is {noop,flip_0}. The controller sees only y=P(S_0); it cannot condition its choice on the hidden microstate. Uniform concrete states induce uniform within-fiber priors and macrostate weights proportional to fiber size.

Exact enumeration yields rational action-to-outcome channels. Uniform-action mutual information and optimized channel capacity are separate columns. Identical action rows give zero capacity, including either pointwise shielding or a flip that permutes the full fiber under its uniform prior. Disjoint supports give one bit. These statements concern the defined channel and do not construct an endogenous controller.

The separately completed gradient intervention audit uses a known-state interface, different actions and different outcomes. Its numerical values are not pooled with this experiment. The conservative learner in issue64 is also independent of this static channel.

## Make the capacity certificate explicit

After the floating-point Blahut-Arimoto search, retain an explicit rational input law p and form the exact rational mixture m(c)=sum_a p(a)W(c|a). The certification expressions are

$$
L=I(p,W)=\sum_a p(a)D(W_a\Vert m),\qquad
U=\max_a D(W_a\Vert m),\qquad L\leq\operatorname{Cap}(W)\leq U.
$$

Use base-two logarithms and directed outward rounding. Zero-probability summands contribute zero; a positive W_a(c) with m(c)=0 gives an infinite divergence and an unresolved upper certificate. An interior rational p avoids that support loss. A floating-point optimizer stopping rule alone is not a proof of capacity.

Aggregate certificate intervals with the same exact p(y) weights used for scores. An unresolved overlap must not be broken using midpoint values. The later implementation commit must pin its rationalization and interval precision before primary evaluation, and retain all certificates and numerical-limit flags as the protocol requires.

## What closing the proposal means

The protocol, planned-work entry, research catalog and Erased Distinctions Program now point to one named deliverable. The implementation must be committed before the new census, reproduce the old closure/repertoire controls, and satisfy the exact and numerical checks. Only that later completed result can move the experiment out of planned status.

No new numerical result, observer-selection rule or evidence upgrade is supplied here.
