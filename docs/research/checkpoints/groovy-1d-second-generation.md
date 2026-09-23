# 1D second-generation G: handoff

Updated 2026-09-23. [Result note](../2026-09-23-groovy-1d-second-generation.md).
[PR #296](https://github.com/bombadil-labs/groovy-commutator/pull/296), branch
`gather/groovy-1d-second-generation`. Authored by Codex; Reviewed by: none.
Inspected main: `a8dee2d0510f22e7f992a65346e3167cd64ac2dd`.
PR #295 was the only open PR at inspection and remains separate, unmerged.

## Subsequent direct request

Myk asked for one further generation after this unit closed. The
[third-generation handoff](groovy-1d-third-generation.md) now records that
completed follow-up in the same PR. The scope and next-decision text below
preserve the second-generation unit's state before that request.

## Selected question and result

Myk explicitly redirected attention to 1D autonomous G fields and their own
G fields. We selected the 36 present-only binary cases; 33 had pointwise
updates in the old census, leaving only 2/16/32 for nontrivial checking.
This avoids a new memory census and answers a concrete recursion question.

Reconstructed and independently replayed all 36 first-stage positive tables.
Pointwise updates have constant native G by algebra. With the frozen
zero-fill and one-fill minimal-radius rules, 2 and 16 have nonconstant
inherited second-G laws of minimum symmetric radius two. Each was checked
over every 15-bit source cone. Rule 32 fails on inherited fields for both
radius-one completions, Rules 128/160, with period-11/12 witnesses.
All six full-descendant-domain checks fail with periodic witnesses.

The two completions give different second observations even when their
closure verdict agrees. There is no arbitrary-completion invariance claim.
Rule 30 and every other memory-bearing first-level law are outside this
present-only unit. A third generation is untested, not automatically queued.

## Durable evidence

- Protocol before implementation: `9d9f2e154983cf57811daba0fe64036059555814`.
- Implementation before evaluation: `13ba2c9aabd3c39440a6f0a1b63c894f5cd71f92`.
- `results/groovy_1d_second_generation_20260923.json` pins source/input hashes,
  preserves every forced table, second-observation table and witness.
- Replay: `OPENBLAS_NUM_THREADS=1 python scripts/groovy_1d_second_generation.py --check`.
- Targeted tests: `python -m pytest tests/test_groovy_1d_second_generation.py -q`.
- Narrow `recursion-certificate` CI checks the new evidence; historical
  canonical bytes and the legacy integrity registry remain unchanged.

Consult the PR for current checks and integration status. No review or merge
is inferred from self-verification. Do not overwrite its hash-pinned script
or result if a later correction is necessary; preserve a versioned correction.

Local verification passed: canonical replay, nine targeted semantic tests,
all 64 historical integrity records, 21 research-site tests and the site
production build. The result's packed evaluation and unpacked/scalar replay
are independent arithmetic implementations within this session, not a
separate scientific reviewer.

## Next decisions, if Myk chooses to continue

1. Does a requested recursion concern present-only binary fields or a
   temporal-memory rule such as Rule 30? The latter is still a 1D question.
2. For the positive 2/16 chains, is the scientific target a third inherited
   generation or a property independent of the first-law completion?
3. For Rule 32, is a specified temporal-memory question justified by the
   second-generation information loss? Larger spatial radius for H alone
   cannot repair either preserved whole-field collision.

Stop this unit here. No spatial lift, completion census, memory search or
automatic recursive tower follows from these results.
