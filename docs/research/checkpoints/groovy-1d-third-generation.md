# One further 1D G: handoff

Updated 2026-09-23. [Result note](../2026-09-23-groovy-1d-third-generation.md).
Continuing [PR #296](https://github.com/bombadil-labs/groovy-commutator/pull/296)
on `gather/groovy-1d-second-generation`. Authored by Codex; Reviewed by: none.
Inspected main `a8dee2d0510f22e7f992a65346e3167cd64ac2dd`; inspected prior
PR head `6628c14577acdba01a363457160add329eedb80c`. PR #295 remains separate.

## Request and result

Myk asked whether Rules 2 or 16 extend another recursive G. Followed exactly
one further inherited generation, with both previously fixed F completions
and H's zero-fill primary / one-fill alternative. No lift or memory search.

Both mirror rules give the same four-case pattern (F fill, H fill):

- (0,0): exact no-present-only-law witness, period seven.
- (0,1): exact no-present-only-law witness, period ten.
- (1,0): nonconstant third G, minimum symmetric update radius four.
- (1,1): local conflicts at radii zero through four, no periodic collision
  through twelve; **unresolved at larger radii**, not a global negative.

Each positive is checked over all 2^21 source cones; its update table is
stored in the result. Each of eight composed third observations was also
checked directly by unpacked triple-G evaluation over its unreduced 21-bit
support. Four negative witnesses are checked by scalar nested G. All third
fields differ from their second fields; no stationary recursion was found.

This is existence under explicit rules. The completion choice now changes
the closure verdict. The source rules are mirror equivalents. No fourth
generation, arbitrary-completion theorem, Rule-30 result or speedup follows.

## Evidence and continuation

Protocol commit `4c93804f9dc70031c07a3b4704eac4aca56e1505` precedes implementation
commit `8c7559cf5b6d34bae2cb662f1f5271eac35eb627`, which precedes evaluation.
New record: `results/groovy_1d_third_generation_20260923.json`.
The second-generation JSON and its pinned script/protocol are unchanged.
The follow-up hashes those inputs too; preserve old bytes if later correcting.

Replay with `OPENBLAS_NUM_THREADS=1 python scripts/groovy_1d_third_generation.py --check`.
Consult PR #296 for current checks and integration; it remains a draft unless
Myk separately directs integration. CI/self-checks are not scientific review.

Local validation passed: third-generation canonical replay in 12.23 seconds,
second-generation replay, all 14 combined semantic tests, 64 historical
integrity records, 21 research-site tests and the production site build.
The initial site check caught a duplicate catalog display label; the new
entry now has a unique label and the rerun passed. No scientific result or
pinned implementation changed during publication.

## Next decisions

The requested extra generation is complete; nothing further is queued.
If Myk continues, distinguish (1) a fourth generation of the explicit
successful branch, (2) a structural reason for closure independent of chosen
unused entries, and (3) a question about the unresolved (1,1) branch that
justifies a new bound or method. Do not silently switch among them.
