# Reusable descriptions: handoff

Updated 2026-09-23. Authored by Codex. Reviewed by: none.
Gathering branch: `gather/reusable-descriptions`, based on inspected main
`a8dee2d0510f22e7f992a65346e3167cd64ac2dd`. PRs #295 and #296 remain separate,
unmerged, and unchanged. Inspected #296 head:
`405c298243ad69f5230e06ac887f83342cd6e0e9`.

## Request and outcome

Myk requested the proposed visual comparison of arithmetic and CA descriptions.
The [account](../2026-09-23-reusable-descriptions.md) supplies an exact minimal
arithmetic repair, a native-G completion witness, and a separate source-XOR
obstruction. The latter two must not be conflated.

- Capped prime-exponent readout under increment forces residues modulo p^K.
  The display uses p=2, K=3: eight states, three bits. This is a familiar
  arithmetic result with a short necessity/sufficiency proof, not new prime
  distribution research. Forward-word refinement is not online suffix memory.
- Rule 32's G image excludes 101. Rules 128 and 160 give the same exact
  evolution on that image but different native G on the fixed source 0101010.
  A single radius-one rule bit is free. More valid trajectory history cannot
  determine a rule choice that never affects those trajectories.
- Source XOR does not descend through G_32: two identical observed input pairs
  yield different observed XORs. This says a source distinction must return
  for that operation; it does not certify a globally sufficient one-bit repair.

## Evidence and publication

Scope commit: `6b8037f413a13f23753ff0a52b32519b5035500a`.
Mathematical implementations before recorded verification:
`488c880add56e32096a35b04b284a116f43f1fef`.
Evidence: `results/reusable_descriptions_20260923.json`, pinning the scope,
Python verifier and JavaScript model. Preserve those bytes.

Commands: `python scripts/verify_reusable_descriptions.py` and
`node --test site/scripts/reusable-descriptions.test.mjs`. The Python verifier
exhausts 128 complete seven-bit cones; the JS example record agrees exactly.
The site entry is `site/reusable-descriptions.html`; its fragment, theme-aware
diagram styles and view logic are shared with the conversation preview.
`node site/scripts/export-reusable-descriptions.mjs /workspace/name.html`
exports that self-contained preview. No external data or network call is used.

Published for review in [draft PR #297](https://github.com/bombadil-labs/groovy-commutator/pull/297).
This unit remains unmerged; no independent review has been requested or claimed.

Local verification completed:

- Python exact verifier; all three JavaScript evidence/model tests.
- All 22 research-site tests and production build.
- All 64 existing result-integrity records; canonical result bytes unchanged.
- Real Chromium interaction checks for all four arithmetic refinements and
  all three CA stages. Desktop and 360/320-pixel layouts have no horizontal
  overflow; desktop and 320-pixel screenshots were visually inspected.
- Built site route returns HTTP 200, loads its dynamic module, and supports
  both controls without page errors. The inline comparison uses the same
  source markup, mathematical model, view logic and diagram styles.

Authoring checks first caught a missing handoff and an unsupported top-level
await; both were repaired. The absent default browser binary was worked around
with a local Chromium package, and the visual checks then passed. No such
implementation failure changed a mathematical claim or result byte. Remote
check status remains available on the PR; green self-checks are not review.

## Next decisions

The proof/explainer unit has a fixed stopping point. No new census is queued.

1. Which operation is the next consumer actually asking a derived CA to
   support: autonomous evolution, native difference/G, or transported source
   XOR? These have different requirements.
2. If transported source XOR is required, can an explicit small local
   refinement of G_32 supply it together with evolution, or is retaining the
   source unavoidable under that precise contract? A complete-source track is
   the trivial baseline; resolving one witness is not enough.
3. Does the visual comparison make a further proof target clear to Myk? Keep
   prime-distribution and larger recursive-tower claims outside this unit.
