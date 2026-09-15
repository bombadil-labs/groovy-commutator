# Independent scientific review: factor-balanced interactions

Reviewer: Codex (OpenAI), session `/root/balanced_review`, 2026-09-15.
Primary author: separate Codex session `/root`. The reviewer authored only
independent audit code and review records, not the primary study implementation.

## Gate 1 and chronology

Gate 1 approved protocol commit `00bc0841a820e912d63a089d890745159aba75e7`
before implementation or fitting. Protocol SHA-256:
`54cac38485d3d3716713f69318d33fa7c7b546396eb320a4bdef3e211aad0ba8`.
Signed review: https://github.com/bombadil-labs/groovy-commutator/pull/266#issuecomment-5688014363.

Implementation `587d8fc9c83d74349493b8b28d4a5bf7326b36e6` preceded prediction
commit `a42df7e5c887bf5f20454340bd42d852416cc4b7` and seal commit
`8cf20c3ab61b5734bb49168368252af666221595`. Independent oracle primitives were
prepared without generating fresh CA data or fitting. Fresh verification began
only after the prediction seal was committed and the primary run was underway.
Source hashes and prediction-seal hashes match. Historical relations are a
byte-identical copy of the prior study's saved compact relations.

## Numerical verification

- Reconstructed the three band designs independently, including all cross-family
  pairs and equal total training weight per band/family-pair stratum.
- Reconstructed every feature and all 252 task target vectors from historical
  relations. Refit 756 models with augmented weighted least-squares SVD rather
  than the primary normal-equation solve. Verified coefficients, all 4,536
  predictions, clipping counts, and training errors. Maximum numerical
  discrepancy: `1.2656542480726785e-14`. Fit audit: 0.295 seconds.
- Audited all 32 fresh array archives, hashes, full future-state arrays, graph
  consistency, actual cycle closures, minimum cycle basin labels, transient
  depths, entropies, block counts, and extrema. Independently regenerated scalar
  successor maps and path-walking graph arrays for all eight rules at width 17
  and rules 54, 90, 110 at width 21: 11 cases, 7,340,032 source states.
  Other cases received complete stored-graph/future consistency verification,
  not independent regeneration of their successor maps.
- Independently checked all 24 Rule 90 width/horizon entropies against GF(2)
  matrix ranks. Checked VI invariance under bijective block renaming for the
  54/110 pair on all 36 width/observation combinations.
- Recomputed all 1,008 within-ring rule-pair relations with sorted-run entropy
  counts and independent joint-label encoding. Array/relation audit:
  301.946 seconds, peak RSS 533,100 KiB (520.6 MiB).
- Compared all 1,512 evidence rows and independently recomputed all 252 task
  scores, errors, pairwise outcomes, strict joint-win flags, and nine summary
  records. Maximum entropy/relation/scoring discrepancy:
  `1.2434497875801753e-14`. Scoring audit: 0.222 seconds.
- Source review confirms the shared primary successor builder directly compares
  four rows per fresh case (128 rows total) to `src/groovy/ca.py` updates.
  Independent scalar reconstruction additionally checks every successor in the
  specified 11-case panel without calling that builder. A separate lightweight
  reviewer control additionally compared eight deterministic source states per
  case (256 rows) directly to the core, passing in 0.499 seconds; see
  `core_row_check.py` and `core-row-verification.json`.
- Verified the rule 0/204 future-partition zero-change controls. The author
  cross-reviewed the independent path-walking graph algorithm on 200 synthetic
  functional graphs using direct walks from every start.

Independent review completed without a scientific mismatch. Total measured
numerical audit time was 302.962 seconds including the separate core-row check, outside CI. The primary confirmation
result SHA-256 is
`f3885c3925a843cc6cfef2a4e7fc1c9e5f26df63f01b0746353704af464ddb4b`.

## Findings and interpretation

The 88 strict joint improvements are correct. M2 versus M0 has 106 wins,
88 losses, 58 ties; M2 versus M1 has 98 wins, 102 losses, 52 ties. These are
252 dependent tasks, not independent trials. Basin relations have 18 joint
wins out of 28. The 54/110 pair has one joint win (basin), with MAE approximately
0.104226 / 0.074152 / 0.070599 for M0 / M1 / M2 respectively.

The report correctly bounds the finding: declared divisibility families are
balanced, other prime factors and valuations are not; extrapolation remains
confounded with size and gap; VI is a scalar projection; extra quadratic
features can change effective regularization as well as express interactions.
The 54/110 future-horizon ties at 1, 2, 8, 16, and 32 steps come from every
prediction clipping to zero. The basin models each clip three of six predictions.
These clipping facts are retained and discussed, not presented as identical
raw predictions or a dynamical invariant.

Reviewed the report, complete score tables, and plotting formula. The plot
retains all 252 tasks and colors the minimum improvement against the two
baselines; a plus marker requires a strict joint win. No test-driven replacement
model, Class-IV classification, mechanism theorem, or automatic next study is
claimed. No substantive scientific blocker remains.

## Integration status

This record completes numerical and interpretive review. Final Gate 2 sign-off
must still pin the integrated gathering head after publication/provenance changes
and confirm relevant CI checks. Archive integrity is reviewed separately once
the final archive exists. Gate 1 alone never authorizes a merge.
