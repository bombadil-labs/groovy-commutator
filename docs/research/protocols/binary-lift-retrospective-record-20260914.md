# Binary lift unit: retrospective methods and authorized deviations

Status: evaluation complete. Gate 2 accepted 2026-09-14 (Claude/Fable, exact head a641df751bc81b50947b8ea7bd1c4d9d2ae8203f, PR #233). **This is a retrospective record, not a preregistered protocol.**

Authored by: Codex (OpenAI), dimensional-lift local working session, 2026-09-14. Reviewed by: Claude/Fable (Gate 2, accepted 2026-09-14). Intended independent reviewer: Claude/Fable, arranged by Myk.

## Authority and chronology

**Protocol review: none at freeze; run authorized by Myk 2026-09-14.** There was no formal Gate 1 freeze or independent pre-evaluation review. The required exception wording records Myk's explicit confirmation; it does not imply a review or repository commit before the experiments.

Myk had authorized bounded local experiments, explicitly suspending the usual commit/PR/review cadence. On 2026-09-14, after seeing the results, Myk instructed this session:

> We have skipped the Gate 1 protocol but that's fine, say myk approved the exception and let's prepare this as a gate 2 PR with known deviations.

Authorization source: Myk's message in the dimensional-lift ChatGPT working session on 2026-09-14. This quoted record is the portable authorization reference; no public conversation URL is available. Evaluation preceded independent review. The exception does **not** waive independent Gate 2 review before merging into main.

## Mission and actual experimental contract

Seek a common, nontrivial, recursively reusable binary lift for all 256 ECA source rules. Source radius is 1; the native lifted radius is at most 2. Source derivative is primitive, `table(r XOR 204)`, and evolution integrates it by XOR. Original and centered commutators are distinct diagnostics.

The four-field family uses P, D, a transition mask M and a two-input reference Q. All four physical row phases must share one unlabeled binary local rule. Recovery, native evolution and commutator preservation are separate gates. The prepared transverse axes have period four; their information comes from the source line. G is prescribed on P/D only, and recursively on nested P/D.

Experiments used exhaustive dependency windows and sparse local-table consistency, cached identical cases, and symbolic unspecified parent outputs. The search adapted to its observed failures. It was not a preregistered test of fixed predictions.

## Sequence preserved by this import

| Stage | Question and actual domain | Outcome |
|---|---|---|
| Earlier binary reference and recursion | Initially inherited the old three-row admission filter; fixed paths later reached 4D | Historical baseline only: 113 faithful 4D paths, 105 recursive-G passes |
| Fresh symmetric census | All 256 rules × 8 mask/sign choices × 2 Q placements × 6 cyclic orders | 254 faithful, 131 original-G, 205 centered-G rules |
| Decoder diagnosis | Every symmetric recipe for Rules 23/232 | Exact complete-image complement collisions |
| Directed repair | All 384 new directed recipes for Rules 23/232 | Both holdouts acquire faithful first floors |
| Full directed census | All 24,576 recipes in a reflection-closed directed pair | Four-reference union: 256 faithful, 133 original-G, 220 centered-G rules |
| Universal 3D census | One first-floor-selected path per rule, aligned across reflection pairs | 256 native/source/parent passes; 200 selected G passes out of 220 eligible |
| G collision diagnosis | All 36 first-floor holdouts; 6,912 recipes, 3,040 faithful | 29 rules remain blocked in every faithful recipe even with row identity supplied |

The first-floor censuses each enumerate all 2^11 source assignments per recipe. The new 3D census uses all 2^13 assignments with the appropriate origin. The old 4D sample uses all 2^16 assignments for each selected path. The source intervals are dependency windows; the results are not claims based only on periodic source-ring sampling.

## Known deviations and corrections

1. **Gate 1 and staged repository chronology were skipped.** The work was implemented and evaluated locally under Myk's exception. This import preserves original source/output bytes and hashes but cannot supply missing historical commit ordering. There are no invented protocol, implementation or evaluation sub-PRs.
2. **Selection was adaptive.** References, masks, layouts and orientations were explored after earlier outcomes. Reported coverage is a union over an explicit tested family. Earlier successful alternatives raise the best-known 3D G count from 200 to 206; they do not change the frozen selection's score.
3. **An obsolete admission filter was discovered and removed.** New four-row constructions initially inherited old three-row rejections. The completed fresh censuses account for every rule and variant in their stated domains. The import preserves both the earlier limited data and the correction.
4. **Author verification is not independent-agent review.** Separate scalar/cropped implementations and alternate constraint solvers checked concrete risks, but they were produced in the same author session. Checks were exhaustive on their listed selected cases, not an independent replay of every candidate in every census. Fable's Gate 2 review remains pending.
5. **Some historical verification summaries contain cumulative supplements.** The 3D top-level verification combines the original 62 eligible-rule check with the later two-rule parent-constraint supplement; its current totals are 64 eligible rules, plus all 36 no-carrier native/recovery checks. Original subrecords are preserved. Timings and old labels are not rewritten to pretend one uninterrupted run.
6. **Terminology was corrected.** Directed mismatch Q is not globally complement-odd in the strict Boolean sense; complementation exchanges the directed relations. Self-reflecting ECAs use an orientation convention, not a reflection-fixed signed recipe.
7. **Completion freedom is conditional.** Original versus centered G and the all-zero native output are separately handled. Successful 3D paths for Rules 157/199 impose rank-one constraints on free parent outputs; success does not always leave every completion free.
8. **CI registration is scoped to this unit.** The dedicated fast workflow registers this result with the existing `check_result_integrity.py` engine through the release wrapper. It avoids changing the shared legacy registry, whose path triggers can launch unrelated historical replays on merge. The new workflow checks every changed unit input; scientific replay remains outside Actions.
9. **The phase-oracle conclusion is conditional on original admission.** Only the 3,040 recipes already faithful under the uniform unlabeled gates enter the G diagnosis. The statement about 29 rules is limited to those recipes. The 3,872 initially unfaithful recipes were not retested under labels; the result does not exclude every labeled architecture or newly eligible labeled recipe. The imported notes make this scope explicit rather than promoting an overly broad “labels cannot repair the family” reading.

## Reproducibility and review scope

The [bundle guide](../../../experiments/binary_lift_20260914/README.md) lists the exact commands and included runs. The [manifest](../../../results/binary_lift_20260914/bundle_manifest.json) identifies every archived member, unchanged code file and archive part by SHA-256. Base64-wrapped compressed evidence makes the import self-contained through the repository connector's text-file interface; extraction recovers the original bytes.

The [canonical account](../../../results/binary_lift_20260914.json) is generated from those saved records. Its checksum/accounting check is not a new scientific experiment or a replay of every local case. The local replay command runs the original targeted author verifiers and the complete collision diagnosis, checking the latter's two certificate logs byte for byte. Wall times and cumulative reporting wrappers are not claimed to reproduce byte for byte.

Gate 2 should assess the definitions, coverage accounting, cached-case identities, dependency-window bounds, physical-G equations, symbolic parent completions, exact failure witnesses, and the limits stated in the three research notes. It should also assess the publication package and the deviations above. The prospective new-Q experiment remains unrun.

## Completion criteria and non-claims

This unit is reviewable when its preserved evidence unpacks, its generated account matches the archive, its documented local checks pass, its notes/catalog/knowledge/Program/checkpoint agree, and its deviations remain visible. Acceptance additionally requires independent sign-off on the final gathering head and relevant green checks.

No universal G-preserving lift, induction over dimension, unique completion, arbitrary independent higher-dimensional source data, intrinsic-dimensional theorem, or Class-IV discriminator is claimed. Copy/stripe constructions remain meaningful controls: faithful evolution and G preservation alone do not establish the nontriviality sought by the broader program.
