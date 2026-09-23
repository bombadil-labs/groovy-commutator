# A failed prediction can constrain the next description

2026-09-23. Completed bounded method benchmark. Authored by Codex (OpenAI).
Reviewed by: none. The separate verifier is self-verification using the
pre-existing independent audit implementation; it is not an external review.

We wanted to know whether remembering *why* a representation fails makes
search more effective. On one previously solved Rule-24 problem, it did:
full verifier calls fell from **278 to 11**, while both methods recovered the
same cheapest encoder. Median search wall time, with startup and preprocessing,
fell from **0.686 to 0.409 seconds** across three fresh-process trials per arm.
The shared final certificate audit took a further **2.013 seconds**.

This supports retaining the small witness interface. It does not establish
that Prolog is faster than Python or SAT, or that this gain transfers to harder
problems. Jev was **not evaluated: missing credential**. No second benchmark or
archived recoder run is automatically queued.

## The problem was already solved

The [accepted decision](2026-09-23-relational-search-decision.md) and
[frozen protocol](protocols/relational-search-pilot-20260923.md) selected the
[known predictive-synergy counterexample](2026-09-08-block3-representation-design.md).
The source is Rule 24 on every binary periodic 12-cell row. We divide the row
into four disjoint three-bit blocks, number block patterns little-endian, and
observe the target `01000010` every three source updates.

Each candidate is a local encoder refining that target. There are exactly 406
canonical candidates. The operation is to determine the **entire future of
this fixed target** from the present complete four-block candidate observation.
It is not autonomous evolution of the candidate, nor a local CA update law.

The explicit future partition has 34 classes and stabilizes at target depth
one. The verifier also checks that equal future labels have equal target
readouts and equal successor labels. This establishes all-time sufficiency
on this finite ring; it does not extrapolate a finite horizon to the infinite
line.

The objective is added uniform-source observation entropy. Candidates are
ordered exactly by the integer product of class sizes raised to themselves,
then lexicographically. This avoids floating-point ordering decisions. The
known unique optimum is `01230243`, costing 5.754887502163468 added bits.
The known greedy endpoint `01230245` costs one bit more. Recovering these
answers is a regression result, not new mathematics.

## What a witness says

A failed candidate gives two concrete source rows with the same candidate
observation and different target futures. Any sufficient replacement must
distinguish at least one aligned pair of their block patterns:

$$
\bigvee_{j=0}^{3} P(a_j) \ne P(b_j).
$$

Python validates the source pair, block codes and first future disagreement.
Prolog retains this necessary constraint. A later candidate that violates it
can be rejected without another full 4,096-source query. Each such rejection
names its witness; none rests on a model score or absent marginal gain.

The first retained witness is particularly instructive. Source integers 1
and 6 have block-code rows `[1,0,0,0]` and `[6,0,0,0]`. Their current target
observations agree, but their targets after three source updates differ.
Therefore **P(1) must differ from P(6)**. This is exactly the distinction
introduced by the known zero-immediate-gain bridge `01000020`.

That interpretation is a post-evaluation reading of the preserved witness,
not an additional prediction. It explains how a necessary distinction can be
found without looking immediately rewarding to a greedy information score.

## Recorded comparison

Both local arms use the same Prolog grammar, candidate ordering, Python
oracle and fresh domain/engine state. The cost scan sends each candidate to
the full oracle. The witness arm first checks accumulated constraints.

| Measurement | Cost scan | Witness-guided scan |
| --- | ---: | ---: |
| Candidates generated | 406 | 406 |
| Candidates visited before success | 278 | 278 |
| Full oracle calls | 278 | 11 |
| Candidates rejected by prior witnesses | 0 | 267 |
| Witness comparisons in Prolog | 0 | 567 |
| Failed oracle queries | 277 | 10 |
| Trial wall times, seconds | 0.709203, 0.685578, 0.665240 | 0.408726, 0.408524, 0.429916 |
| Median wall time, seconds | 0.685578 | 0.408726 |

The witness arm makes about 25.3 times fewer full queries and is about 1.68
times faster in these recorded search trials. All non-timing outputs agree
across repeats. Trial order was scan/witness, witness/scan, scan/witness.
These are three trials on one machine and a known target, without statistical
or cross-machine generalization.

Median phase times show the practical limit of the gain:

| Phase, seconds | Cost scan | Witness-guided scan |
| --- | ---: | ---: |
| Domain and future construction | 0.048810 | 0.048020 |
| Prolog/WASM startup | 0.232011 | 0.220120 |
| Grammar, cross-check and ordering | 0.051136 | 0.048390 |
| Selection, prefilter and communication | 0.048447 | 0.003539 |
| Full oracle work | 0.177797 | 0.007044 |
| Witness validation, marking and insertion | 0.046721 | 0.003893 |

Total wall time also includes Python startup, trace serialization, result
collection and shutdown. Phase medians need not sum to the median total.
Startup dominates the improved method. The result does not justify adopting
the WASM bridge as the fastest production frontend.

The final audit checks all 406 candidates with the existing independent
metric routine, replays every query witness and pruning reason, verifies
complete coverage before the optimum and reconstructs the greedy path. Its
2.013 seconds is shared validation cost outside the six timed searches, not
hidden inside a speedup claim. Replaying the saved certificates also passed.
The NumPy-based verifier does not need Prolog or Jev.

The environment was Python 3.12.14, NumPy 2.3.5, Node 24.19.0 and
`swipl-wasm` 8.1.3 (reported SWI version 100115), with one numerical thread.
Peak worker RSS was about 30,260–30,268 KiB; the separate Node peaks were
118,048–121,068 KiB. These are separate peaks, not a simultaneous total.
OS filesystem caches were not flushed. A cached `npm ci` took 0.424 seconds;
the initial package-install duration was not measured. Native apt setup
failed on restricted OS identity switching; no native engine was benchmarked.

## Search cost is distinct from representation cost

The optimum has five labels. Four fixed-width labels still occupy twelve
bits, with a 24-bit eight-entry encoding table. Encoding reads three source
bits and performs one lookup per block. Refreshing from the source retains
twelve source bits, runs three fine updates and performs four encodings.

We have not synthesized an autonomous maintenance rule. The future partition
used to prove sufficiency is not a free operational prediction service.
The entropy saving relative to greedy repair is neither a fixed-width storage
saving nor a measured prediction speedup.

## Predictions, missing evidence and disposition

| Frozen prediction | Result |
| --- | --- |
| P1: complete Prolog/Python candidate-set agreement | Supported: all 406 |
| P2: recover the known optimum | Supported in all six local trials; Jev unrun |
| P3: fewer full queries using witnesses | Supported: 278 to 11 |
| P4: lower median total search time using witnesses | Supported here: 0.686 to 0.409 seconds |
| P5: Jev improves total time over local witness search | Not evaluated: missing credential |

The optional Jev arm is implemented with typed Choice requests and tested
using a fake response. It can choose only within the cheapest surviving
cost tier, never certify or prune. A real acquisition remains untested, with
explicit request, time and usage budgets in the protocol. Missing access is
not evidence against the heuristic. Given the local arm's subsecond total,
API latency is a concrete cost that a future acquisition would need to beat.

Keep the relational constraint interface and exact rejection reasons. Defer
Datalog, predicate invention, a framework rewrite and larger searches. A
next method test needs a separately justified target; it should compare a
native Python witness filter before attributing a benefit to the language,
and separate candidate-selection costs from hard universal verification.
This benchmark's oracle is cheap and its answer known. It supplies no evidence
that ranking will rescue the eight archived recoder verification timeouts.

## Evidence and provenance

- Inspected main: `a8dee2d0510f22e7f992a65346e3167cd64ac2dd`.
- Decision/protocol freeze: [b244bb9](https://github.com/bombadil-labs/groovy-commutator/commit/b244bb99e47d518c946870dcf265a63998cd9253).
- Implementation before evaluation: [6dfeee3](https://github.com/bombadil-labs/groovy-commutator/commit/6dfeee360d9ad3e037092e0bbebd5c306319cdab).
- [Canonical result](../../results/relational_search_20260923.json), exclusively
  created at `2026-09-23T04:30:16Z`; SHA-256
  `b74710e389343092e16d22f86ea8c61ac513fd5b9de7bb4ca364dca0b7f1a14a`.
- [Implementation and reproduction](../../experiments/relational_search_20260923/README.md),
  [semantic rejection tests](../../tests/test_relational_search.py),
  [saved-certificate verifier](../../experiments/relational_search_20260923/verify.py).
- [Gathering PR #298](https://github.com/bombadil-labs/groovy-commutator/pull/298)
  and [handoff](checkpoints/relational-search.md). No independent review or
  merge is claimed. PRs #295–#297 remain separate.

No candidate, target, ordering or evaluation-budget deviation was made after
the freeze. The optional acquisition remains unrun as specified.

Local publication checks passed: five semantic rejection tests, all 65
registered source-integrity records, 21 research/knowledge publisher tests,
and the production site build. Hash checks establish provenance coherence;
the separate certificate replay supplies the semantic verification.
