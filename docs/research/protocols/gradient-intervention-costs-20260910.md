# Frozen next experiment: intervention cost and usable gradient futures

Date: 2026-09-10. Status: planned, not executed. The preceding loop experiment establishes native gradient dynamics and the loop-sector invariant for eight nonconstant sources, with two erasing constant controls. This protocol tests a distinct action interface; it does not modify the frozen loop experiment or claim an endogenous controller.

## Fixed law, state, action, and observation contract

Keep sources 0,142,150,170,178,204,212,232,240,255 and ordered axial macro cadence. Use every flat edge field on shapes (4), (2,2), and (2,2,2), exactly as in the loop audit. The initial full edge field is known. An action is one simultaneous XOR mask delta applied at time zero. Admit every mask whose plaquette curl vanishes; then adding it to any flat state remains flat. Do not evolve a curl-violating intermediate or choose an off-domain extension.

The primary action cost is the number of flipped stored edge bits, with a hard per-action budget b. Also record the number of distinct sites owning those edges. These are separate costs. The external ability to address and apply a distributed mask simultaneously is supplied, not explained. No sequential actuator, feedback policy, stored controller, expected-cost budget, or unknown-state prior is implied.

Observe either the full terminal edge field or only its loop vector, at horizons t=0,1,4. Both observations must be reported. Keep the difference between information that is stable over time and information that can be intentionally revised explicit.

## Complete mask and minimum-cost census

Enumerate all 16, 32, and 1,024 flat masks respectively, using anchored potentials and loop vectors. Independently check the plaquette constraints and completeness via their binary rank. Record each mask word, loop change, flipped-edge count, and touched-site count. For every loop change, save the minimum edge cost, number of minimizers, and a deterministic first witness; separately report minimum touched-site cost rather than assuming the same minimizer.

Frozen prediction: on a rectangular periodic lattice with N sites, the least edge cost for loop change h is the sum of N/n_i over directions whose h_i is one. Derive a lower bound from the disjoint parallel wrapping loops, and construct a matching seam mask. This prediction concerns simultaneous flat edits and edge count, not the time or intermediate defects needed to implement them. Zero-loop masks are exactly gradients of periodic potential edits; they cannot change a loop sector. Keep the no-op separate from nonzero zero-loop edits.

## Usable futures under hard budgets

For every initial state s, every rule, and every flat action delta, calculate Q^t(s XOR delta) at t=0,1,4. Use independently verified transition tables to avoid reevaluating identical CA steps, but count every state/action/horizon query. There are 10,498,560 initial rule/state/action combinations and 31,495,680 endpoint queries. Do not select initial states or actions by interesting-looking outputs.

For each shape, rule, horizon, and budget b from zero through d*N, report the number of distinct reachable full fields and reachable loop vectors. Preserve the distribution of these counts over all initial fields, and deterministic first states attaining each extremum. An efficient exact implementation can first record the minimum action cost producing each endpoint, then count endpoints below each budget. Independently check direct action-set counts against that method. Preserve all discrepancies and matching evaluator checksums.

Primary results are integer reachable-outcome counts, not entropies assigned to an unspecified ensemble. For this known-state, deterministic, one-shot channel with a hard action-set constraint, maximizing mutual information over action probabilities gives log2 of the number of distinct terminal observations: choose one action representative for each endpoint and make endpoints uniform. Any channel-capacity interpretation must state this contract. It is not a claim about feedback empowerment, uncertain hidden states, or average-cost optimization.

The frozen loop prediction is persistence of each action-selected loop sector at positive horizons for the eight self-dual rules, versus a single zero-loop outcome for constants. The within-sector full-field repertoire is unpredicted and must remain separately visible.

## Dimensional cost and controlled compatibility

Use the same interfaces (4) to (4,2) and (2,2) to (2,2,2). Lift an action by literal gradient replication P. Check all source masks: P appends zero loop change, doubles flipped-edge cost, and doubles touched-site count because the added period is two. State the general added-period multiplier analytically. Compare this inherited action family with the native mask census on the target shape (2,2,2); do not imply that the full native frontier on (4,2) was enumerated.

For all source state/action pairs, all ten rules, and t=0,1,4, check Q_target^t(P(s) XOR P(delta)) = P(Q_source^t(s XOR delta)), using independent target reference evolution. This adds 38,400 interface endpoint checks. The new minimum-cost frontier may use native actions outside the replicated image; classify that fact rather than treating it as failure. Distinguish controlled compatibility with a translated budget from equality of capabilities at the same numerical budget.

## Decision and publication

Commit implementation before execution. Preserve exact budgets, failures, minimum-cost witnesses, action profiles, endpoint-count distributions, and independent certificates in canonical JSON reproduced by CI. Account for topology, d bits per site, copied support, and externally supplied action geometry.

The result can establish persistence, revisability under this action set, and costed availability of distinguishable futures. It cannot show that the CA autonomously creates a controller, optimizes empowerment, restores arbitrary damage, or discovers a representation. A sequential, local, or endogenous control mechanism would be a separate frozen experiment. Keep Class IV and metaphysical or prime analogies out of selection and scoring.
