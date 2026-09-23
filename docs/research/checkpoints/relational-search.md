# Relational search: bounded pilot handoff

2026-09-23. Authored by Codex (OpenAI). Reviewed by: none.

## Current state

Myk authorized the [decision](../2026-09-23-relational-search-decision.md) and
one implementation pilot. The [completed result](../2026-09-23-relational-search-pilot.md)
supports reusing exact conflict witnesses on the known Rule-24 finite-ring
problem: 278 full queries become 11, retaining the same optimum. The first
conflict forces the known zero-immediate-gain distinction. See the note for
timing, setup and representation costs. Jev is unscored because no credential
was present; its executable arm is preserved. No paid request was made.

Inspected main was `a8dee2d0510f22e7f992a65346e3167cd64ac2dd`. The gathering
branch is `gather/relational-search-pilot`, [PR #298](https://github.com/bombadil-labs/groovy-commutator/pull/298).
Protocol/decision commit: `b244bb99e47d518c946870dcf265a63998cd9253`.
Implementation pin: `6dfeee360d9ad3e037092e0bbebd5c306319cdab`.
Evaluation followed both. The canonical result's hashes pin all implementation
inputs; its bytes must not be overwritten by a timing rerun or Jev acquisition.

Current scope is complete and awaiting Myk's review/merge direction. Tests
and certificate checks are verification, not independent scientific review.
The decision is accepted for a bounded pilot, not for broad language adoption.

Local verification passed: all six saved certificates and their shared
independent finite audit, five semantic rejection tests, all 65 registered
source-integrity records, 21 research/knowledge publisher tests and the site
production build. The narrow three-minute CI job checks saved certificates
and toy controls; it does not rerun timed searches or call Jev. Remote check
status is attached to the gathering PR's current head.

## Resume safely

- Read the result note, then the [runner README](../../../experiments/relational_search_20260923/README.md).
  It gives tests, saved-certificate verification and a fresh-output run command.
  Do not launch a new empirical unit simply to continue this handoff.
- Preserve concurrent draft PRs #295 (geometry), #296 (recursive 1D G) and
  #297 (operation-dependent descriptions). They were unchanged when checked.
  Their findings and agenda additions require reconciliation if integrated
  together; they are not silently incorporated into this main-based branch.
- Keep the archived hard recoder campaign parked. Its universal verification
  bottleneck was not measured or repaired here. No larger ring, census,
  predicate invention or Datalog migration is queued.

## Next decisions, not automatic experiments

1. If we pursue another method benchmark, what independently chosen operation
   and oracle make candidate-search cost materially important?
2. Can a native Python witness frontend keep the same certificates with less
   startup/communication overhead? This control precedes any claim that the
   programming language caused the gain.
3. Is there a workload where Jev's ranking could repay its acquisition cost?
   Missing credentials leave that question unanswered; acquire only under a
   bounded contract and preserve the current not-evaluated record.
