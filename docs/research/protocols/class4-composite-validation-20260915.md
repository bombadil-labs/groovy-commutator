# Composite discriminator: prospective validation after discovery

Status: frozen proposal before composite evaluation and before fresh runs.

Authored by Codex / OpenAI GPT-6 Astra on 2026-09-15. Independent prospective review pending. Parent gathering #247. The original two-candidate pilot is preserved in evaluation sub-PR #249 at `e397151d8bea012f8f06a8e467e64332194df303`.

## Discovery record and reason for this extension

The frozen original primary A=positive conditional retention times positive shape-cycle growth had AUC 0.9821 in both configurations and still admitted 122/126. Original primary B=held-out older-history predictive gain times residual next-step variation had Class-III AUC 1.0 in both configurations but admitted Class-II families (11/46 in primary; 9/11/46/134 in replication). Both primary candidates failed perfect separation. All original scores and failures remain fixed; no original prediction is rewritten.

The complementary failure patterns motivate testing a conjunction. This is a post-discovery hypothesis, not something independently predicted before the original study. No composite score has yet been calculated. New configurations supply fresh trajectories, not new independent positive rule families. The labels, positive families, small-ring graph information and two components were already known. Even success cannot establish a universal Class-IV definition.

## Fixed scores and comparisons

Reuse the original exact definitions, counting, smoothing, folds, and degeneracy conventions with primary W=7 and h=8. Do not fit coefficients, signs, a threshold, or a preferred window. Let R be retention, alpha_Q the finite ring-9..14 slope of log2 maximum rotation-quotient period, and B the original averaged two-direction temporal score.

Primary composite C=max(0,R)*max(0,alpha_Q)*B = A*B.

Prespecified simpler rival D=max(0,alpha_Q)*B removes the retention factor. Report it as a rival/ablation, not a concealed replacement for C. Also report the other factor deletions: A (remove B), B (remove R and alpha), and max(0,R)*B (remove alpha). All coefficients are one; these are explicit statistical products, not conserved information exchange rates. A factor is not deemed necessary if deleting it preserves the claimed separation.

First compute these products on the saved original data and label every such result discovery/post hoc. Do not change any formula based on that computation. Then compute on all 88 symmetry families in both fresh configurations below.

## Fresh domain and fixed budget

Validation v1: N=384, discard 1536 steps, count 1024 consecutive transitions; PCG64 seeds 7001,7002,7003,7004,7005,7006. Validation v2: N=768, discard 3072 steps, count 1024 transitions; seeds 8001,8002,8003,8004,8005,8006. Bernoulli(1/2) initial states; all spatial positions; first three vs last three seeds in both directions. All 88 minimum representatives of the same reflection/complement-conjugation orbits.

Use only W=7/h=8 in these new runs. Sensitivity widths/histories remain those already evaluated in the original pilot; no new best-window selection. Reuse the exact original per-rule alpha_Q/alpha_P and graph spectra rather than rerunning identical graphs. Their source/result hashes must be pinned and verified. The new experiment tests longer and larger trajectories, not robustness of the small-ring growth fit.

The original implementation is frozen at `ae5bf688920d4ea27d7c84ad99768b5e34b90eb4`, script SHA-256 `363c3bfa531712583a134d1056b085eaa286506ad653f4d46a8f196d6e0dc7d2`. A separate runner may call those exact functions; it must not mutate their definitions or globals. Parameter dictionaries passed to functions are the declared new configurations. The label-free scientific run writes all scores before a separate report step joins the inherited labels. Raw counts, per-rule checkpoints, implementation hash and timings are preserved.

Hard wall 15 minutes for this extension, outside GitHub Actions, with signal-enforced timeout and per-rule checkpoints. No new run or formula revision follows a failure in this extension under this protocol. Stop and report the outcome. This is the last scientific execution in the current bounded attempt; any future research is a separate proposal.

## Predictions, reporting and interpretation

Primary positives remain 54/110; disputed 41/106 remain excluded from the primary classification population and are separately reported. 122/126 remain negatives. Compute all AUCs, positive tied ranks, exact score margins (minimum positive minus maximum included negative), and list every negative at or above the lower positive score, for C and D and every deletion. Show all 88 scores and component values for both fresh configurations. Report class-label convention sensitivity separately as in the parent.

V1 stronger bet: C ranks both positives above all included negatives in each fresh configuration. V2 weaker bet: C and D each have AUC>0.95 overall and >0.9 against Class III in both fresh configurations. V3 ablation bet: D also separates both positives completely in each new configuration, testing whether selective retention is unnecessary for this finite separation. V4: both directions of the held-out history gain stay positive for both positive families, with R and alpha_Q also positive.

A single negative tie or exceedance falsifies the corresponding perfect-separation bet. No alternative class label is offered as rescue. No confidence interval treating cells/times as independent. Distinguish repeatability across trajectories from evidence across rule families (still two positives). Data-derived cutoffs are descriptive margins only; do not present a deployable threshold or universal class test. If a score succeeds it is a finite, explicitly scoped candidate with a mathematical definition, not a theorem that Wolfram Class IV is equivalent to that score.

## Review and integrity

Independent prospective review of this extension precedes its new runner and fresh evaluation. The original pilot's scientific source bytes and canonical JSON remain unchanged. Preserve protocol, implementation, evaluation and interpretation boundaries through sub-PRs. Source hashes include the original pilot result and scientific source as well as this protocol and runner. Final independent review must recompute saved metrics from raw counts and check all failure accounting. Only bounded controls and source-hash accounting run in CI; no automatic scientific replay.
