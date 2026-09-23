# Prediction and repair: completed finite baseline

Updated 2026-09-23. Authored by Codex (OpenAI). Reviewed by: none.

Myk authorized the proposed prediction-to-repair unit ("Make it so").
Inspected main: `a8dee2d0510f22e7f992a65346e3167cd64ac2dd`.
Work is on `gather/prediction-repair`,
[draft PR #299](https://github.com/bombadil-labs/groovy-commutator/pull/299).
It is not merged. Preserve separate unmerged PRs #295–#298; their shared agenda
edits will need reconciliation at integration, not overwriting by branch age.

## What finished

The [frozen protocol](../protocols/prediction-repair-20260923.md) was published in
`5927301ffae6e6d9af94398712df3b5fb3124485`, then implementation in
`5f70e244372d305d93fd8905cbdc9722ee4622a5`, before evaluation. No Jev or paid API.

Rule 54, periodic n=12, four stripe phases `(0011)^3`, all 52 intact/one-bit
injured states; observe once, noop or flip one addressed cell, success after
four updates. Exhaust all 4,140 partitions of three-bit blocks. Minimize local
alphabet, not arbitrary sensor cost. Exact result:

- Prediction of the entire passive target-membership future needs 2 labels,
  unique encoder `01101001` (parity); 496 encoders pass.
- Repair and joint sufficiency each need 4 labels, unique encoder `01233210`
  (adjacent differences); the same 39 encoders pass both.
- The repair view merges exactly 26 complementary pairs on S. Its policy
  succeeds on 52/52, using the same 48 one-bit corrections as full-state access.
- The target has no incoming transitions from outside: refinement `[2,2]`.
  Delayed success is equivalent to immediate correction. This is static
  error correction, not autonomous recovery or endogenous purpose.
- P1–P4 supported; P5 failed. All successful-action sets are singletons;
  every failure therefore has a pair obstruction. The three-way toy control
  validates software capability only.
- Post-evaluation algebra: the repair view is not a refinement of parity;
  task sufficiency is different from preserving the old sensor's literal labels.

Read the [result note](../2026-09-23-prediction-repair.md) for the witness, costs,
proof boundary and figure. Do not describe prediction as full-state forecasting
or the controller as spatially local. Do not infer an infinite-line theorem.

## Evidence and verification

Canonical `results/prediction_repair_20260923.json`, SHA256
`bba465222ddb694c36e4d7eb85b2af603862b3db58cbd65f3e257aa644a9c064`.
The adjacent `_audit.json` checks all 4,096 transitions, 52 states, 4,140
encoders and three guided searches with separate algorithms by the same author.
Evaluation and audit took about 0.25 and 0.41 seconds, below their 120-second
caps. These timings do not establish an algorithm or language advantage.
Canonical bytes, implementation and protocol are hash-registered and retained.
Five toy semantic tests check the non-pairwise action-intersection issue and
pass. All 65 registered results pass the fast provenance check; all 21 site
tests and the production build pass. The post-evaluation encoder identities,
complement pairs and singleton-action claim were checked against the saved
tables. Current-head CI status is on PR #299. Green checks are verification,
not external review.

## Next decisions; no automatic follow-up

1. Does a proposed next target admit genuine passive return paths from outside?
   Establish that eligibility before spending on observer optimization. This
   stripe target does not; changing delay alone cannot fix it.
2. Is the next question about externally controlled repair, or about maintenance
   by constraints inside the system? State the intervention and cost contracts;
   these are distinct claims and need distinct evidence.
3. At Myk's direction, reconcile and integrate the completed gathering PRs.
   Their status is not permission to resume every archived next-step proposal.

Stop this unit. No larger ring/rule/horizon census, injury sweep, stronger
agency claim or new external review gate is authorized by its positive result.
