# Representation and causal-retention unit: self-review

Completed 2026-09-22 by Codex (OpenAI). Myk explicitly authorized this session
to work solo. This is **not independent review**. Base:
`30559ffcf1357c8dde828e2e620d3e7d65d01a3b`; branch:
`gather/representation-causality`.

## Scope and scientific account

- Extracted the three cases requested in issue #280. Case C verifies exact
  Boolean powers, the small-ring exception range, periodic tails, bridge
  seams, and the central mismatch. It does not extrapolate a finite crop.
- Froze the whole-field retention protocol at `5b54f39`, implemented at
  `0e5d0e2`, then evaluated. All outcomes are retained: 56 candidates refuted,
  eight surviving the finite check. No surviving candidate was called proven.
- Froze the locality follow-up at `bc7741b`, implemented at `d41b427`, then
  evaluated. All seven nonidentity survivors fail at radius one; the exact
  lower-bound proof uses two reachable neighbourhood pairs and phase rotation.
- The twelve-state requirement is conditional on a pointwise encoding,
  current/age readout, radius one and preserved atomic-update semantics.
  The account explicitly acknowledges other eight-state protocols, the
  unproved status of any larger-radius factor, and the absence of a new
  asynchronous theorem about the dimensional lift.
- Both runners share update/prefix definitions. Source hashes record that
  dependency; two executions do not constitute independent scientific review.
- The numerical investigation has stopped at its explicit boundary.

## Verification actually run

All passed locally:

1. `python scripts/verify_representation_case_studies.py --check`.
2. `python scripts/verify_nakamura_retention.py --check`.
3. `python scripts/verify_nakamura_local_retention.py --check`.
4. `python -m unittest discover -s tests -p 'test_representation_certificate_rejection.py'`
   — three corrupted-certificate rejection tests, including a periodic-tail
   change, false output bits and a false observed neighbourhood.
5. `python scripts/check_result_integrity.py` — all 64 registered results.
   This is provenance verification, not validation of every old conclusion.
6. `npm run test:research --prefix site` — 21 tests passed.
7. `npm run build --prefix site` — passed, including local links and TeX.
8. Python compilation of the three new verifiers and rejection tests;
   `git diff --check`.
9. Compared all 439 result files tracked at the base against their current git
   blob hashes: none changed. The three new reports are additions.

Both canonical numerical runs completed inside their 60-second limits. The
new checks are short enough to join the existing fast research CI; no expensive
historical census or paid manual Actions job was launched.

## Original publication failure (resolved)

The Bombadil GitHub MCP and the standard GitHub MCP returned HTTP 400
`Invalid MCP request metadata`, including on read-only operations. Direct
`git push` failed because this runtime has no GitHub push credentials.
No PR was created, no remote branch was pushed, no issue was closed, and no
remote merge is claimed. The local gathering branch and delivery bundle keep
the frozen-protocol chronology intact for an authenticated continuation.

Access recovered on 2026-09-22 after Myk refreshed the Bombadil connector.
The five commits were imported in order into [PR #282](https://github.com/bombadil-labs/groovy-commutator/pull/282),
and the imported tree exactly matches the original local head. See the
[publication record](representation-causality-publication.md) for SHA mapping.
The preceding paragraph records the state at the original failed attempt;
PR #282 supplies authoritative CI and merge status.
