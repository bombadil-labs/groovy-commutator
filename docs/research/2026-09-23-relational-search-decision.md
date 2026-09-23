# Decision: relational search with explicit witnesses

2026-09-23. **Accepted for a bounded pilot by Myk.** Authored by Codex
(OpenAI). Reviewed by: none. Acceptance authorizes the pilot; it does not
establish a performance advantage or authorize a broad search campaign.

## Why this decision

We want to discover which distinctions an observation must retain for a
specified operation. Each concrete failure can constrain later candidates.
The vocabulary of candidates, the strategy for selecting them, and the exact
verification backend are separate choices. Changing programming languages
alone does not resolve a hard proof query.

The repository already has SAT/CEGIS in the
[bounded source-recoder work](2026-09-10-erased-distinctions-terminus.md).
Its eight unresolved cases stalled in universal verification. We will not
restart that campaign to demonstrate a new frontend. The same record also
shows that changing an exact encoding can change resource use dramatically.

## Decision and division of responsibility

1. **Use a small typed relational grammar.** Start with explicit finite
   encoders and their domains, not unrestricted Prolog programs. Every
   candidate names the information it reads and the operation it must support.
2. **Prototype the grammar and witness constraints in SWI-Prolog.** Retain
   canonical descriptions and checkable rejection reasons. The pilot uses the
   official `swipl-wasm` package, pinned by a lockfile, so it needs no system
   installation. Startup and cross-process costs count.
3. **Reuse exact Python/SAT verification where appropriate.** The first
   benchmark is finite, so its existing exhaustive Python certificate is a
   stronger and simpler baseline than adding a new SAT encoding. The SAT
   interface remains the option for later symbolic contracts, not a mandatory
   detour for this case.
4. **Treat Jev as a search-order heuristic.** It may rank supplied candidates;
   it cannot certify, reject, or silently remove a candidate. Preserve requests,
   responses, actual model, costs and missing results. Compare against an
   explicit inexpensive ordering. A Jev score is not a mathematical probability
   that a candidate is correct.
5. **Defer Datalog and predicate invention.** Datalog becomes useful if the
   witness/dependency collection needs richer recursive queries. Learning new
   named predicates is a possible later grammar change, not an accomplished
   capability of this finite-table pilot.

Classify the problem before refining: erased state, insufficient permitted
access, or an unspecified extension of a partial rule require different work.
Unknown or timed-out verification is never a negative result.

## First comparison

Use the already solved [Rule-24 predictive-synergy case](2026-09-08-block3-representation-design.md):
periodic width 12, cadence three, target `01000010`, and all 406 canonical
block-three refinements. A purely greedy information-gain repair is known to
miss the optimum. This makes it a useful regression against discarding
temporarily unhelpful distinctions. The objective and answer are already
known; this is a method benchmark, not a new mathematical discovery.

Compare the same cost-ordered candidate stream with and without accumulated
witness constraints. An optional Jev arm changes only selection within an
equal-cost tier. All arms retain the same complete grammar and exact verifier.
The [frozen protocol](protocols/relational-search-pilot-20260923.md) states
budgets, hypotheses, measurements and stopping rules.

A gain in verifier calls alone is insufficient to claim a speedup. Charge
domain construction, grammar generation, witness evaluation, engine startup,
serialization, ranking and final verification. Measure search cost separately
from the information-theoretic objective and actual representation storage.

## Consequences and limits

This creates a small testable interface, not a second research platform. No
new census, larger ring, larger recoder budget, dimensional lift, or automatic
continuation is authorized by the decision. Successful finite examples do not
establish infinite-line closure or universal search efficiency.

The conceptual impetus is Myk's [Thinking Like a Function](https://myk.pub/thinking-like-a-function-16):
make a formerly implicit dependency explicit when an operation requires it.
The engineering lineage includes [CEGAR](https://www.cs.cmu.edu/~emc/papers/Conference%20Papers/Counterexample-guided%20Abstraction%20Refinement.pdf),
[SWI-Prolog tabling](https://www.swi-prolog.org/pldoc/man?section=tabling),
[TypeSafe's typed Jev judgments](https://docs.typesafe.ai/api), and
[Souffle provenance](https://souffle-lang.github.io/provenance).
The related [PR #297](https://github.com/bombadil-labs/groovy-commutator/pull/297)
distinguishes state loss from native-rule completion. It remains a separate
unmerged unit, as do PRs #295 and #296.
