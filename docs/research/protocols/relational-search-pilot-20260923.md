# Protocol: a relational search pilot on the known Rule-24 repair

Frozen before implementation and evaluation, 2026-09-23. Authored by Codex
(OpenAI). Reviewed by: none. Myk authorized implementation and formalization
of the decision. Base main: `a8dee2d0510f22e7f992a65346e3167cd64ac2dd`.

## Question and decision

Does a Prolog representation of candidate encoders and accumulated conflict
witnesses reduce the cost of recovering an already known exact optimum?
Can optional Jev ranking improve on the cost-ordered witness loop? A win
justifies considering a second independently chosen bounded benchmark; a
loss or missing Jev score does not justify more compute on archived problems.

## Exact contract and known answer

- Rule 24; every binary state on a periodic 12-cell ring (4,096 states).
- Disjoint blocks of three cells, with little-endian codes 0 through 7.
- Fixed target encoder `01000010`; cadence three source updates.
- Candidate encoder P maps the eight block codes to canonical finite labels
  and refines the target. All 406 such partitions are included.
- Required output: the entire future of the fixed target observation at this
  cadence, read from the complete present four-block P observation. This is
  target-future sufficiency, not autonomous evolution of P or a local CA rule.
- Use `scripts/audit_block3_representation_design.py` to construct the source
  transition and explicit target future words. Partition stabilization,
  confirmed by a forward-consistency check, certifies the all-time finite-ring
  target. Stop after 64 refinement steps if it has not stabilized.
- Historical answer: optimum `01230243`, added observation entropy
  5.754887502163468 bits; greedy endpoint `01230245`, one additional bit.
  These are known regression targets, not prospective discoveries.

The objective is the historical uniform-source entropy H(P)-H(T) of the
four-block observation. Sort candidates by descending integer
`product(class_size ** class_size)`, then lexicographic encoder. This gives
exact entropy ordering without floating-point ties: local entropy is
`3 - log2(product)/8`. Neither entropy nor label count is runtime cost.

## Grammar and oracle

SWI-Prolog enumerates restricted-growth label lists of length eight and
rejects those that merge distinct target classes. The resulting set must
equal the independent Python audit's 406-element interval.

The Python oracle checks every source state. A failure returns concrete source
states a,b with equal complete P observations and different target futures,
their four block codes, and the first differing target time. Any sufficient
encoder must distinguish at least one aligned block-code pair in this witness.
Prolog records that disjunctive requirement. Every rejection retains the
witness responsible; it must be replayable independently.

No candidate is pruned merely because its current marginal information gain
is zero. The grammar, target and oracle remain identical across arms.

## Arms

1. **Cost scan:** try candidates in exact entropy/lexicographic order using
   the complete oracle, without witness-based prefiltering; stop at the first
   sufficient candidate.
2. **Witness-guided cost scan:** same ordering and oracle, but use accumulated
   witnesses to reject incompatible candidates cheaply before a full query.
   Stop at the first sufficient candidate. This retains optimality because
   all skipped candidates have actual conflicts.
3. **Jev-ranked witness scan (conditional on access):** retain the same witness
   constraints and exact cost ordering. Within the cheapest surviving cost
   tier, supply up to eight lexicographically first candidates to one Choice
   question. Jev selects which to query next. Its choice never rejects an
   encoder or crosses a cost tier. If the tier has one candidate, use it
   directly. Invalid or missing choices fall back to lexicographic order and
   are recorded. A run with an API error/fallback is incomplete for a claim
   about Jev's advantage.

Jev receives the target definition, candidate class memberships and storage,
and at most the four most recent concrete conflict witnesses with operational
descriptions. Do not supply the known optimal or greedy encoders, historical
results, rule number, or reference to this benchmark. This does not establish
freedom from training contamination. Model scores are search advice only.

## Budgets, execution and costs

- Pin the implementation before recording results. Preserve canonical bytes;
  every output uses exclusive creation and source hashes.
- Run each local arm three times from fresh engine/domain state, alternating
  arm order. Record every run and summarize medians, not the best run.
- At most 406 full oracle calls per arm run; a hard 120-second wall per run.
  A timeout is a resource limit, never a mathematical negative.
- Run the Jev arm once if a credential is present; otherwise record
  `not_evaluated: missing_credential` and preserve an executable acquisition
  path. At most six requests, eight choices/request, 8,000 serialized request
  bytes each, a 20-second request timeout and a 180-second arm wall. After the
  request cap, continue cost order and record budget fallbacks separately.
  Record usage/model per response. Do not retry or launch a broad scout.
- Measure full elapsed time including domain/future construction, Prolog/WASM
  startup, grammar generation, ordering, process communication, witness work,
  optional API work and oracle calls. Installation is setup, recorded
  separately. Also record phase times, full-query counts, witness comparisons,
  candidate visits, pruning counts, and peak child/parent RSS when available.
- Charge each arm its own preprocessing; do not reuse the first arm's oracle
  data or warm process for the other. Keep final independent audit outside
  timed search and report its cost separately.

Representation accounting: encoding reads three source bits per block and
uses an eight-entry label table. Four fixed-width output labels cost
`4*ceil(log2(number_of_labels))` bits; report table bits too. This benchmark
does not synthesize an autonomous maintenance rule. Refreshing from a running
source retains the 12 source bits, performs three source steps, and re-encodes
the four blocks. Future partition construction is proof work, not a free
operational prediction oracle. No storage or prediction speedup is claimed.

## Frozen predictions and acceptance

- P1: Prolog's candidate set equals the existing complete 406 encoders.
- P2: both local arms recover the known minimum objective and named optimum;
  optional Jev must recover the same objective when it completes.
- P3: witness filtering reduces full oracle calls relative to cost scan.
- P4: median total wall time is lower with witness filtering. This may fail
  because the finite oracle is cheap and the frontend has overhead.
- P5: Jev improves total elapsed time over the local witness strategy. Mark
  unscored if access is missing or errors make the arm incomplete. A single
  acquisition is exploratory even if its time is lower.

Audit successful encoders with the existing independent metric function;
replay every returned witness and every recorded pruning reason; verify no
cheaper encoder was omitted and that all three local repeats agree on the
non-timing results. Confirm the known greedy regret. Tests must catch a
forged witness and an incomplete candidate stream. No extrapolation beyond
this ring, target, grammar or hardware/backend follows.

Keep all predictions, including failures and not-evaluated values. Publish
the decision, code, result, limitations and handoff in a gathering PR. Stop
after this comparison. No full census, larger ring, recoder recovery or
automatic second benchmark follows.
