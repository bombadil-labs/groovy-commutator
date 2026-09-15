# Whole-state rule relations across ring arithmetic

Prospective protocol, 2026-09-15. Author: Codex (OpenAI), /root.
Independent Gate 1: pending. Implementation and evaluation follow approval.
Infrastructure: PR262. Prior data motivating this question: PR259/PR260.

## Question and scope

Myk asked for an extensible way to correlate relations between rules with
relations between rings, including prime factors and their multiplicities,
then authorized running the instrument. This first bounded study uses whole
source-state partitions. Exhaustive local-window summaries become independent
of ring length once all their causal support sites are distinct; they are a
poor probe of larger-ring arithmetic. This study does not rebuild lifted
completion contracts or claim a Class-IV classifier.

## Frozen domain

Rules: 0, 18, 30, 54, 90, 110, 126, 204. Rings: every integer 4 through 16.
Every binary source state is represented exactly once, bit i at site i.
The source population is exhaustive and unburned on every ring. There is no
random sampling or seed. Rule numbers are identifiers, never ordered physical
coordinates. Rule pairs use increasing numeric identifiers for orientation.
All 28 distinct unordered rule pairs are retained. No rule is removed after
inspection. Only two core Class-IV examples are present; this is not a class
census or a significance study.

For each rule/ring, record its complete source successor map and nine partitions:

1. Equality of whole states after t steps, for t = 1, 2, 4, 8, 16, 32 (six
   selectors). All horizons are fixed across widths.
2. Eventual attractor basin identity (cycle representative labels may be arbitrary).
3. Eventual attractor cycle length.
4. Distance in steps from the source state to its eventual cycle.

The last three are exact properties of the finite functional graph, with no
trajectory censoring. Store all label arrays. Distinct cycles of equal length
remain distinct under basin identity and deliberately coincide under the
cycle-length selector. All nine selectors are applied to every case.

## Relations and ring comparisons

For a fixed ring, two rules' partitions are aligned by the same enumerated
source states. With uniform mass per state, compute variation of information
VI(A,B) = 2H(A,B) - H(A) - H(B), in bits. The relation score is VI/n, dividing
by the source bit budget. Retain H(A), H(B), joint entropy and raw VI with the
score. This is a label-invariant partition distance, not a graph isomorphism
test or a complete invariant of structure. Raw partitions remain available.

The harness compares each rule-pair score on rings n<m, retaining both scores,
their signed difference and its absolute value. For each observation and ring
pair, the primary ring-response value is the mean absolute change over all 28
rule pairs. This gives one response per ring pair rather than counting those
28 dependent rule pairs as independent arithmetic observations. Ring pairs
also share endpoints. No IID p-values, significance thresholds, or classifier
claims are produced.

Frozen ring descriptors: all built-in `arithmetic` features from PR262,
`divisibility` at divisors 2,3,4,5, and `valuation` at primes 2,3,5. Use explicit
unique ids. The raw size gap is retained as a baseline descriptor. These are
first-order descriptive associations; they do not adjust away every size
confound or establish an arithmetic mechanism.

Discovery uses ring pairs entirely within 4..12. Confirmation uses ring pairs
entirely within 13..16; mixed pairs are retained but excluded from selection
and confirmation summaries. For each observation, compute Pearson correlation
of every descriptor with the primary ring response. Undefined/constant columns
are retained with reasons. Select at most three defined discovery associations
by descending absolute correlation, ties by feature name. Freeze this selection
before computing any data for rings 13..16. Report every candidate and every
selected confirmation coefficient, with sign agreement/disagreement; no new
selection on confirmation and no pass/fail threshold. Six confirmation ring
pairs provide only a small descriptive check. Neither selection nor sign
agreement constitutes a replicated scientific finding.

## Predictions, controls, and verification

P1 (implementation control): Rule204's future partitions are identity partitions
at every horizon/ring; Rule0's future partitions are constant. Their normalized
VI is exactly 1 up to numerical rounding. Reordering arbitrary basin labels
cannot affect VI.

P2 (known arithmetic control): Rule90 reaches zero on every source state by
horizon16 on rings4,8,16, and its horizon16 map is nonconstant at every other
tested width. This follows from the binary additive shift identity and is not
a novelty claim. Independently check its future-image entropy using GF(2)
matrix rank, rather than using the author's partition implementation.

No direction or minimum strength is predicted for a novel Class-IV-specific
arithmetic signature. Report 54/110 alongside controls and preserve negative
and undefined results. This is an exploratory use of a prospectively fixed
catalog, not confirmatory evidence for a new universal relation.

Independent review must reconstruct scalar ECA updates and functional graph
partitions on a representative panel, verify entropy/VI by a different counting
implementation, verify discovery selection and all confirmation decisions,
and inspect interpretation. The primary implementation uses the repository's
ECA lookup-table convention with axis-explicit batched updates; verify sampled
rows against `src/groovy/ca.py::apply_rule`.

## Budget, provenance, and preservation

Two sequential stages: discovery4..12, confirmation13..16. Each has a hard
wall budget of 10 minutes and a memory ceiling of 2 GiB; budget errors are
reported as incomplete, never zeros. Persist each completed case and its hash,
then complete stage summaries and the sealed discovery selection. Any partial
run is disclosed. No runs execute in automatic GitHub Actions. Freeze this
protocol, then the implementation, before evaluation. Record input/source
hashes, durations, stage state and the independent review. The new canonical
result uses the fast result-integrity gate; raw arrays and full evidence rows
are preserved in an archive. There is no automatic second research round.
