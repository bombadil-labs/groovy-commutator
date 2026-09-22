# Independent result audit: Rule-110 original-G autonomy

Reviewer: Sol (gpt-5.6-sol), agent `/root/g_autonomy_review`, 2026-09-22.
This is the independent result audit requested after Gate 1. Final integrated-head
review remains pending until the result, note, catalog and handoff are published.

## Pinned evidence

- Reviewed protocol: `ad38b4937321501889b6b8a1caab4e4bfb54052e`.
- Frozen primary implementation: `232662516b858eabb4743dce9f8ef2c76847bec6`,
  whose sole parent is the reviewed protocol commit.
- Canonical result bytes at audit time:
  `d4be4bef70fe7073328c46e061722752bbc33eec7992a2f5d10e90ddfa0bcdc4`.
- Primary source hashes in the result match the current protocol and evaluator
  and the corresponding blobs at the frozen implementation commit.
- `execution.json` names the frozen implementation, matches the canonical
  result hash, and records about 0.012 seconds wall time and 12,416 KiB peak RSS,
  within the frozen 120-second and 1-GiB budgets.

The period-three `001`/`011` collision candidate was hand-derived by the
author after protocol freeze but before execution and disclosed before this
audit. It is therefore not a blind prediction. The result preserves that
chronology in `prediction_context`; the computation verifies the candidate
and the frozen first-witness ordering.

## Independent method and findings

The standalone
`scripts/verify_rule110_g_autonomy_certificate.py` does not import the primary
evaluator. It implements Wolfram-indexed ECA updates with literal tuples in two
forms: shrinking finite causal words and cyclic rings, including the aliased
neighbors at widths one and two. Original G is computed directly as

`E(S) XOR E^2(S) XOR E(S XOR E(S))`.

The audit established all of the following:

1. The complete Rule-32 control passes on 128 seven-cell source words:
   `G_32 E_32 = E_128 G_32`. The Rule-90 control has `G_90=0` on all 32
   five-cell source words.
2. Independent reconstruction of all 768 frozen local cases exactly matches
   the canonical radius-zero, radius-one and radius-two records, including
   realized-patch counts, complete required-target sets and canonical first
   conflict pairs.
3. Exhaustive tuple-valued cyclic checks find no collision at ring widths one
   and two. Their state counts and distinct-G counts match the result.
4. Lexicographic enumeration at width three first collides after four states.
   Both retained traces replay exactly:

   | Source | E | D | G | next G |
   | --- | --- | --- | --- | --- |
   | `001` | `011` | `010` | `010` | `010` |
   | `011` | `111` | `100` | `010` | `000` |

5. The infinite-line transfer was checked independently without treating a
   finite-ring pass as positive evidence. For each of the three spatial phases
   of `(001)^Z` and `(011)^Z`, an explicit seven-cell periodic source window
   supplies the complete radius-three support. Shrinking tuple updates give
   complete present G periods `010` for both sources and next-G periods `010`
   and `000`. Periodic repetition therefore gives equal complete G fields and
   unequal next G fields on the full binary line. This refutes every
   deterministic `B` on `G_110(X)`, regardless of B's locality.
6. Rings four through sixteen are correctly marked `not_run_after_witness`;
   no larger search was performed in this audit.

## Primary implementation inspection

The primary evaluator's finite-word orientation, rule-bit indexing and G
formula agree with the mathematical contract. Its local slices cover exactly
the union of the radius-R observed patch and radius-three target support. The
packed cyclic shifts agree with the independent tuple implementation,
including widths one and two. The first-representative collision logic,
lexicographic order, immediate stopping rule, result statuses and arbitrary
zero extension field comply with the protocol. The two controls gate the
target result. Resource exhaustion is reported as censored rather than as a
scientific negative.

The primary `--integrity` and `--check` modes both passed against the preserved
result. The independent verifier passed in portable default mode and in
`--history` mode; the latter explicitly checked implementation ancestry and
committed source blobs. Python compilation and `git diff --check` also passed. I found no
definition, orientation, causal-support, manifest or protocol-compliance bug.

## Review disposition

**Result audit: pass, with no blockers.** The exact conclusion supported by
the certificate is that Rule 110's original present-only G field has no
deterministic autonomous successor law on the full binary line. The local
radius failures are subordinate bounded facts; the period-three whole-field
collision supplies the unrestricted negative result. Final Gate 2 approval is
reserved for the exact published head so its prose and integration claims can
be checked against this evidence.
