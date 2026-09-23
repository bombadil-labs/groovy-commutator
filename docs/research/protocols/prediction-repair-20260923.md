# Protocol: distinctions needed to predict and to repair

Frozen before implementation and evaluation, 2026-09-23.
Authored by Codex (OpenAI). Reviewed by: none. Myk approved the proposed
prediction-to-repair unit. Canonical current AGENTS.md governs review;
historical review procedures are not reactivated by this new protocol.
Inspected main: `a8dee2d0510f22e7f992a65346e3167cd64ac2dd`.

## Decision and motivation

Can an observation sufficient to predict a specified organization's passive
future omit distinctions needed to choose a successful repair? If so, find
the smallest permitted observation for each task and an exact obstruction
explaining the difference. If not, preserve that negative outcome and stop.
This tests a scientific use for the witness interface from
[PR #298](https://github.com/bombadil-labs/groovy-commutator/pull/298), not
another language-performance benchmark. Use native Python for this small
finite grammar; no Prolog-versus-Python speed claim or Jev acquisition.

The broader motivation is competence under disturbance and information
relevant to persistence. The goal and controller here are externally supplied.
An observation supporting a controller does not by itself establish an
agent, endogenous purpose, self-maintained constraints or biological meaning.
We want one inspectable mechanism before considering those stronger claims.

## Fixed physical contract

- Source: elementary Rule 54, synchronous, binary periodic ring of 12 cells.
  Cell i is bit i of the integer encoding; local rule index is 4L+2C+R.
- Organization V: all spatial rotations of `(0011)^3`, where strings are
  written in increasing cell-index order. There are four phases. Applying
  Rule 54 exchanges `0011` and `1100` (and their rotations), so V is invariant.
  This is a nonconstant whole-ring pattern, not a localized organism.
- Initial domain S: every v in V, either undamaged or with exactly one bit
  flipped. Include every damage site and every phase; deduplicate states.
  No damage-location or original-phase side channel is supplied to the observer.
- Controller observes once at time zero. Allowed actions A are noop (code 0)
  or one bit flip at site i (code i+1). No second action or observation.
- Repair succeeds exactly when E^4(a(s)) belongs to V. The endpoint is four
  physical updates after intervention; it does not include the immediate
  post-action state. Since V is invariant, endpoint membership entails
  subsequent unperturbed persistence on this ring. There is no recurring damage.
- All states in S have a successful action: undo the single flip, or do
  nothing when undamaged. If the executable control violates this, stop invalid.

## Observations, costs and comparison

An encoder P maps the eight little-endian three-bit patterns to canonical
labels. Q_P(s) is the complete ordered four-label row on nonoverlapping blocks
starting at cell 0. Include all 4,140 partitions of the eight patterns. No
translation-equivariance or locality requirement is imposed on the controller;
it reads the complete label row and addresses a site on the fixed ring.

Primary cost is the number k of local labels, with lexicographic P as a
deterministic tie-break. "Minimum" always means minimum local alphabet in
this grammar, domain and control contract. Report all minimum encoders, not
only the first. This does not optimize arbitrary global sensors or circuits.

For every P, evaluate three predicates:

1. **Predict:** Q_P(s) determines the entire passive sequence
   `1[E^t(s) in V]`, t >= 0, for s in S. Cadence one is held fixed.
2. **Repair:** for every observation fiber B in S, the common successful
   action set `intersection_{s in B} W(s)` is nonempty, where
   `W(s)={a: E^4(a(s)) in V}`. This is exactly existence of a deterministic
   observation-based single-action controller that succeeds for every s.
3. **Joint:** both properties hold. A controller need not preserve an exact
   prediction of every microscopic trajectory; the passive target is V membership.

Repair-only need not determine passive futures. Compare all three optima and
the overlap of successful encoder sets, not just their costs. Identity is
an information upper bound, and constant observation is the blind control.
Record the best fixed action's success count, noop's success count, full-state
minimum-flip policy and each selected successful policy's flip count on
uniform S. For each observation fiber choose noop if allowed, otherwise the
lowest numbered common successful action.

Report fixed-width storage `4*ceil(log2(k))` output bits and
`8*ceil(log2(k))` encoder-table bits. Also record the essential input bit
positions of P (which truth-table arguments can change its output), their
straight-line read count over four blocks, the controller's occupied entries,
and a concrete sparse-table bound counting keys and four-bit action codes.
No compression, runtime, energy or endogenous-controller advantage follows
from a smaller alphabet. Source evolution still updates all 12 cells. The
observer has no history maintenance in this single-observation experiment.

## Exact algorithms and witnesses

Construct all 4,096 source transitions and the delayed action outcome table.
Compute passive future equivalence on the full finite ring by partition
refinement from V membership. Require stabilization and forward consistency;
cap refinement at 64 rounds and report a resource limit otherwise. Only then
restrict labels to S. S need not itself be forward invariant. No finite-horizon
prefix is called an entire future without this certificate.

A predictive failure has two states with equal Q_P and different passive
target futures; save the first differing target time. A repair failure is a
set of states with equal Q_P and empty common successful-action intersection.
Reduce it deterministically to an inclusion-minimal set by deletion. Do not
claim minimum cardinality. Every feasible replacement must split that set
across at least two observation fibers. This is a necessary constraint; a
model score never supplies a rejection.

For each of the three tasks, scan candidates by k/lex order, accumulating
validated witnesses and using them to reject later candidates before a full
oracle call. Preserve every rejected candidate's witness ID. Compare the
selected answer and every rejection with an independent complete 4,140-row
audit using explicit future words and direct grouping/action intersections.
Record oracle calls and witness comparisons, with no timing-speed hypothesis.

Toy control: successful-action sets `{a,b}`, `{b,c}`, `{a,c}` intersect
pairwise but have empty total intersection. The control must reject their
joint observation fiber. It illustrates why pair-only pruning is insufficient;
it is not evidence that this CA realizes a three-state obstruction.

## Frozen predictions and stopping rule

- P1: the full-state observation can predict and repair every state in S;
  V is invariant and the candidate grammar has exactly 4,140 encoders.
- P2: at least one predictive encoder fails repair. This is the primary
  proposed separation; an explicit witness is required.
- P3: the minimum joint alphabet is strictly larger than the minimum
  prediction alphabet. This stronger claim may fail even if P2 holds.
- P4: some repair-sufficient encoder is lossy on S: its complete observation
  merges at least two source states. This may fail; local label compression
  alone is not enough to score it.
- P5: at least one naturally arising minimal repair witness requires more
  than two states. The toy control does not score this prediction.

One rule, one ring, one organization, one damage family, one action budget,
one delayed horizon. No radius, rule, ring or horizon sweep; no redesign after
seeing an unwelcome result. Cap evaluation at 120 wall seconds and independent
verification at 120 seconds. A timeout is a resource limit, not a negative.
Pin code before evaluating; create every output exclusively, with source
hashes. Preserve all predictions, including failures and censored states.
No expensive Actions or external API requests. A short saved-certificate
verification and semantic toy tests may run automatically.

## Deliverable and prior art

Publish the exact comparison, a readable obstruction and a small visual
explanation, along with code, canonical evidence, costs and current handoff.
Keep separate draft PRs #295–#298 unchanged. Do not merge without Myk's direction.

This is a finite controlled-state abstraction problem, adjacent to
[Givan, Dean and Greig's action-preserving reductions](https://cs.brown.edu/people/tdean/publications/archive/GivanetalAIJ-03.pdf).
The motivation draws on [Fields and Levin's competence framework](https://pmc.ncbi.nlm.nih.gov/articles/PMC9222757/),
[Deacon's account of information and maintenance](https://anthropology.berkeley.edu/sites/default/files/whatismissingfromtheories.pdf),
and [Kolchinsky and Wolpert's intervention-based semantic information](https://arxiv.org/abs/1806.08053).
We are not reproducing their full definitions or claiming a new general
theory of agency. The earlier [empowerment endpoint audit](../2026-09-22-representation-empowerment-disposition.md)
motivates the fixed delayed endpoint and common physical action interface.
