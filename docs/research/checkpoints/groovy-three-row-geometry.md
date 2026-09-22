# Three-row Groovy geometry: handoff

Updated 2026-09-22. Authored by: Codex (OpenAI). Reviewed by: none.
[Result and proof](../2026-09-22-groovy-three-row-geometry.md).
Branch `gather/groovy-three-row-geometry`,
[PR #295](https://github.com/bombadil-labs/groovy-commutator/pull/295).
This handoff records branch work; the PR is authoritative for merge status.

## Starting point and selected question

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

## Next decision questions

1. Should the next representation retain a visible strip boundary or encode
   a temporal seam in a binary plane? Specify the new encoding and readout
   before an experiment. Marker-channel closure is already constructive.
2. If a binary repair is desired, what exact resource should it minimize
   relative to existing generic and six-field encodings: cells, neighborhood,
   initialization or maintenance? There is no cost advantage established here.
3. If attention shifts to native G of a new 2D rule, what off-image completion
   and invariance question makes that well-defined? On-image agreement alone
   still does not specify native G.

No further evaluation is queued by this unit. The user's time-to-space
proposal remains a valid design direction with temporal roles now explicit.
