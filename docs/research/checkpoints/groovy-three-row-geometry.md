# Three-row Groovy geometry: handoff

**Integration update, 2026-09-23:** Myk authorized reconciliation and merging
of PRs #295–#299. On main, this unit is integrated. The
[combined account](../2026-09-23-research-integration.md) and
[current handoff](../NEXT_TASK.md) supersede the branch-publication status and
proposed work ordering below. The remaining record preserves the unit’s
original inspection, evidence and verification chronology.

Updated 2026-09-22. Authored by: Codex (OpenAI). Reviewed by: none.
[Result and proof](../2026-09-22-groovy-three-row-geometry.md).
Branch `gather/groovy-three-row-geometry`,
[PR #295](https://github.com/bombadil-labs/groovy-commutator/pull/295).
This handoff records branch work; the PR is authoritative for merge status.

## Latest follow-up: a constant fourth row works

Myk asked to keep exploring after the raw-three-row negative. The
[new result](../2026-09-22-groovy-separator-lift.md) completes a separately
frozen comparison of separators 0 and 1. Both give uniform binary 2D laws
on x=-6..6, y=-2..1, at one source step per update, over every source state
and every vertical phase.

- Protocol: [`28475d0`](https://github.com/bombadil-labs/groovy-commutator/commit/28475d0de55491f86299cbcd704c9538d5805db2).
  Graph/search implementation: [`628c1ac`](https://github.com/bombadil-labs/groovy-commutator/commit/628c1acffce1fe932125d3fe1252e4038418fa81).
- The exact 16-node graph proves the maximum ones run in G_30 is three.
  Thus an all-ones separator has a local four-bit marker test. Source zero
  proves there is no corresponding zero-run bound.
- `results/groovy_four_row_separator_20260922.json` retains stage one, including
  the then-pending positive construction and zero-table test. Do not edit that
  chronology. No zero-separator collision was found for periods 1..12.
- Construction/table implementation before evaluation:
  [`19b011f`](https://github.com/bombadil-labs/groovy-commutator/commit/19b011fc7017e428af6bfb502a7be5cbf5b2c562).
  `results/groovy_separator_lift_20260922.json` settles both candidates.
- The ones rule reuses the 164,477-key marked history table and explicitly
  decodes phase; `src/groovy/separator_lift.py` provides its total local rule
  and finite periodic-plane step. An independent unpacked Boolean replay checks
  2^21 complete source words in all four phases (8,388,608 cases).
- The zero law has 657,893 forced 52-bit keys with matching packed/unpacked
  digest `1cb4e0c97e4f708af70e7f6538f08930b5b4589c6a92e0367a9f86b5f45a3149`.
  Phases need not be individually identifiable when all readings agree on the
  next bit. This refines the earlier marker-oriented interpretation.
- The note gives a general necessary-and-sufficient phase-fiber compatibility
  criterion by compactness; this is a post-evaluation proof deduction. It also
  charges four stored bits per source column, initialization, table preparation,
  maintenance and local access. No speed or global optimality claim follows.

Fast follow-up verification (in addition to the original checks below):

```
OPENBLAS_NUM_THREADS=1 python scripts/groovy_four_row_separator.py --check
OPENBLAS_NUM_THREADS=1 python scripts/verify_groovy_separator_lift.py --check
python -m pytest tests/test_groovy_separator_lift.py -q
```

Local follow-up verification passed: graph/search replay, complete-cone replay
in 6.90 seconds, 20 combined geometry regression cases, 64 existing integrity
records, 21 research-page tests and site build. The note records the minor
execution-order deviation (fixed zero screening before construction replay);
all candidates and decision criteria remained frozen.

All historical records and their implementation hashes remain intact. New
records use the same narrow CI workflow instead of triggering unrelated
historical workflows through the central registry. Review status remains none;
current verification and integration status are in PR #295.

## Preceding unit: starting point and selected question

Inspected/fetched main `a8dee2d0510f22e7f992a65346e3167cd64ac2dd` (merged #294).
No open PRs or issues at inspection. Read AGENTS, current direction, next task,
findings, Groovy Field checkpoint/program and the existing affine-lift contract.
Preserved all other worktrees and previous canonical evidence.

Myk explicitly requested the geometric follow-up: can Rule 30's three remembered
G rows become spatial rows governed by one binary uniform 2D rule? This outranks
the earlier proposed derivative-of-G test because it directly tests the user's
representation claim. The frozen contract repeats the raw rows vertically,
includes every vertical phase, and requires one source step per new update.

## Work and evidence

- Protocol before implementation/evaluation:
  [`5fdd928`](https://github.com/bombadil-labs/groovy-commutator/commit/5fdd92803f74cecae8e429a61025506bd0197073).
- Pinned implementation:
  [`a354d42`](https://github.com/bombadil-labs/groovy-commutator/commit/a354d42ff678c6528ee3c7840ef3c3bc57d2a6dd).
- Canonical evidence: `results/groovy_three_row_geometry_20260922.json`.
  It pins protocol, implementation and CA-engine hashes.
- Exhausted source periods 1..10; at period 11, stopped after 498 sources /
  1,492 phase cases with identical full input planes and unequal successors.
  The primary run and replay each took under one second locally.
- Sources `00010011110` and `00111110001` are consecutive Rule-30 states.
  Their G trace is A,B,C,A,B', with B != B'. The note proves the equivariance
  contradiction and derives a general necessary condition for raw period-k
  history encodings. This lemma is post-evaluation algebra, not a prediction.
- Independent scalar Boolean verification agrees with the numpy search.
  This is implementation independence within one author, not independent
  scientific review. The narrow CI workflow replays the certificate and
  semantic regressions; no historical census is dispatched.

## Decision and limitations

Closed: **raw, unlabelled, vertically period-three Rule-30 G encoding, full
source family, one-step cadence**. Every neighborhood radius fails. The planned
21-bit cone test is explicitly not evaluated because it cannot change this
result. Do not increase period/radius or run other rules to rescue this contract.

The marked memory-three theorem stands. Finite strips with boundaries,
different encodings, markers, enlarged alphabets, other cadences and restricted
source families are outside this negative. A static marker channel suffices by
construction with a four-state alphabet; no minimal repair is claimed.
This is an on-image ambiguity, not the earlier off-image completion problem.

Verification commands:

```
OPENBLAS_NUM_THREADS=1 python scripts/groovy_three_row_geometry.py --check
python -m pytest tests/test_groovy_three_row_geometry.py -q
python scripts/check_result_integrity.py
npm run test:research --prefix site
npm run build --prefix site
```

Local verification passed: exact bounded replay and scalar certificate check,
six semantic regression cases, shared result integrity, all 21 research-page
tests and the site build. The unit-specific checker covers the new record;
the shared checker covers old registered evidence. Remote CI status is in the
PR. Do not call self-checks a review or assume merge authorization.

## Next decision questions after the four-row repair

1. Which operation on this spatial history is worth studying beyond exact
   source emulation? Specify its output and geometry. The four-row realization
   now exists; another generic existence construction would add little.
2. Does that operation justify optimizing stored cells, locality or access
   relative to named tracks and existing lifts? The four-row construction has
   explicit costs, but no performance advantage or global minimality result.
3. If attention shifts to native G of a new 2D rule, what off-image completion
   and invariance question makes that well-defined? On-image agreement alone
   still does not specify native G.

No further evaluation is queued by this unit. The user's time-to-space
proposal now has exact four-row binary realizations, with both uniquely marked
and harmlessly ambiguous temporal roles.
