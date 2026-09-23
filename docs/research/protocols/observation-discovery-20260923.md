# Observation discovery from exact failed-prediction witnesses

Frozen 2026-09-23 before implementation/evaluation. Authored by Codex (OpenAI).
Reviewed by: none. Myk approved this bounded unit and integration as work ends.
Inspected main: `45c8698d2a2e3c0dfcd9bb01dee1556fde58ba15`.

## Decision and scope

Can a counterexample-guided search select which observations and simple
relations to retain, rather than merely repartitioning preselected blocks?
The consumer predicts ONE next central output bit from a finite observation.
A smaller sufficient input could guide later representation work. If relations
buy nothing against raw-bit selection, retain that negative result and stop.
This is feature selection in an explicit grammar, not unrestricted invention
of objects, emergence, enzyme discovery, or an autonomous law for the observer.

Two preselected cases, no rule sweep or post-result grammar changes:

1. Calibration: Rule 90, mandatory base `S_t[0]`, target `S_(t+1)[0]`.
   The known XOR of the two side cells supplies a positive sanity control.
2. Prospective case: Rule 30, mandatory base `G(S_t)[0]`, target
   `G(E(S_t))[0]`, where `G(S)=ES XOR E^2S XOR E(S XOR ES)`.
   Rule 30 is familiar from earlier work, but this feature-selection answer
   has not been consulted or used to tune the grammar. This is not a claim
   that the rule is an unseen external validation domain.

## Complete domain, time and geometry

Every binary seed word on sites -4..4 at time t-1 (512 words, little-endian
integer order). Evolve with the ordinary ECA convention 4*left+2*center+right.
Use shrinking valid cones; there is no periodic wraparound. Time t is obtained
by one update, so histories are legal. The target for Rule 30 depends on
S_t[-3..3], hence the seed's -4..4 cone. Every such word extends to a full-line
configuration, and exterior bits cannot affect any tested feature or target.
Thus exhaustive local checking can certify this ONE-STEP readout identity on
all full-line trajectories with a predecessor. It does not certify autonomous
observer maintenance, all-time prediction from one measurement, minimality
outside the grammar, or a law on arbitrary incompatible history rows.

## Fixed grammar and ordering

Twenty binary candidate features in this exact index order:
- indices 0..6: `S_t[x]`, x=-3..3;
- 7..12: `S_t[x] XOR S_t[x+1]`, x=-3..2;
- 13: `S_t[-1] XOR S_t[1]` (the calibration relation);
- 14..16: `S_(t-1)[x]`, x=-1..1;
- 17..19: `S_(t-1)[x] XOR S_t[x]`, x=-1..1.
Equality is the complemented XOR and provides the same partition, so it is
not a separate feature. No target-valued features or future reads are allowed.
Select zero through seven distinct features. Rank by: selected-feature count,
number of distinct raw spacetime operands of those features, number of their
past operands, number of XOR features, then ascending index tuple. Mandatory
base is the same within each case and is accounted separately below. This
ranking optimizes transmitted/retained feature count first, NOT total access
cost. Record that distinction even if the primary hypothesis succeeds.

Arms: (a) ordered full scan of all subsets up to size seven; (b) identical
ordering with validated failed-prediction witnesses pruning candidates;
(c) raw-only ordered scan, using indices 0..6 and 14..16. Also test ordinary
current raw windows of radius 0,1,2,3, with the same mandatory base.
A failed candidate returns the first encountered two ascending seed rows
having identical observation and opposing target bits. Any successful subset
must select at least one feature whose value differs on that pair. Save each
new witness and its distinguishing-feature bitmask. No witness is a heuristic.
Save the winner's reachable observation-to-output table, or explicit bounded
exhaustion. Guided and unguided arms must agree exactly on their optimum.

## Costs, predictions and stopping

Report candidate generation/order time, search time, full oracle calls,
witness comparisons, pruning, verification time and overall elapsed time.
One deterministic run per arm: no robust speedup inference from one timing.
Report 1+k retained bits, raw operands (including mandatory base support),
past buffer cells, feature XOR operations and readout-table reachable entries
and dense address capacity. Acquiring central G from a raw current row costs
five current cell reads, five rule-table evaluations and five XOR operations;
central S costs one read. No free G oracle is assumed. Past readings must be
stored from the prior step. Refresh each selected feature from its raw operands
at each query; the search supplies no compressed-state update rule. Charge
source evolution separately and equally: a dense source advances by one rule
evaluation per source cell per step. No measured physical or hardware benefit.

P1: calibration selects one feature (the explicit side XOR), while raw-only
requires at least two; this is known-answer regression, not a discovery.
P2: Rule-30 relational minimum uses fewer selected bits than raw-only.
P3: guided search uses fewer full oracle calls than scan on Rule 30.
P4: Rule-30 winner uses at least one history feature (index >=14).
P5: guided total including candidate preparation is less than unguided total
on Rule 30 in this one run. Keep all failures and not-evaluated states.

Hard cap: 120 seconds for the complete producing run and 120 seconds for
verification, outside Actions. A cap is incomplete evidence, not impossibility.
Do not extend radius, feature count, grammar, rule set or budget after results.
Freeze implementation in its own commit before first evaluation. A separately
written scalar-cone verifier checks all input rows, features, labels, witnesses,
pruned cheaper candidates, optimum table and raw/window baselines. Same-author
verification is not independent scientific review. A visual witness viewer
must show actual saved source pairs, common observations and differing targets.
