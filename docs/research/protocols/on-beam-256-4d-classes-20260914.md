# All-256 on-beam rule census through 4D and Wolfram-class associations

Status: frozen before implementation and evaluation; prospective independent review requested.
Authored by: Codex (OpenAI), Myk's dimensional-lift session, 2026-09-14.
Reviewed by: pending; the signed review and exact revision are recorded on the gathering PR.

## Question, provenance and scope

Myk asks: "can we compute the rules up to 4d for all 256 ECAs and see if we can infer anything about wolfram classes?" This unit computes partial native derivative rules and parent decoders on complete finite invariant source families, then explores descriptive and fixed-classifier associations with a named published class convention.

Baseline main is a2dfba2801ac6f53d7cea4306927c5b6f246f140 (6D pilot, PR #235). Reuse the exact ordered-neighborhood interner, constraint compiler and immutable completed native law in scripts/sequential_lift_6d_pilot.py. Existing results/binary_lift_20260914/rule_coverage.csv supplies the four-field native-faithful selection for every ECA, including its mask, P sign, Q formula and field order. This differs intentionally from the six-rule pilot's five-field policy for 171/233. Alphabet, radius and number of fields are constant across this census. No recipe is selected using class labels or new outcomes.

The completed automata are new finite-family zero completions. Archived full-shift/G constraints are not retained; G, arbitrary infinite-source inputs and arbitrary higher-dimensional source automata are not tested. No theorem identifying Wolfram classes is claimed.

## Population and sequential construction

Run widths 7 then 8, rules 0 through 255 in order, and floors 2, 3, 4 sequentially. Every one of 2^w source ring configurations is included, with every longitudinal cell and transverse phase. Each transverse axis has period four. Width 7 is primary; width 8 is independently resynthesized domain/metric robustness, NOT validation that width-7 native tables work on unseen inputs.

For parent X and native successor Y=H(X), D=X XOR Y. Stack four fields in the archived order (PDMQ or PDQM):
- P=X XOR shifted X;
- D;
- M=(NOT X) AND D for birth; X AND D for death; X AND (NOT D) for stay_one; (NOT X) AND (NOT D) for stay_zero;
- Q is the archived pair or directed product at the archived offsets.

At 1D, P observes horizontal offset sign, and Q observes horizontal offsets a,b. At higher floors, P's vector is (horizontal=sign, newest-existing-transverse=+1). Q's vectors are (horizontal=a, transverse=a*sign) and (horizontal=b, transverse=b*sign). Other axes are unchanged. For directed Q use exactly NOT-left AND right or left AND NOT-right from the CSV. Negative-sign rules must not reuse the positive-sign vector convention.

Compute the encoded child and its demanded successor using only the current parent native law. Compile from complete radius-two physical neighborhoods: equal physical patterns must demand equal derivative bits and equal parent bits. Phases are not runtime labels. Every unforced derivative/decoder output is zero; completed parent tables are fixed before making the next child. Derivative zero means no flip, not next-state zero.

Native consistency and decoder consistency are separate gates. Verify complete native one-step intertwining, two full native steps, parent recovery at every child phase, composed source recovery and unchanged parent-table digests. Independently build the same complete configurations using scalar original-ECA evolution and a separately implemented field constructor. One-step consistency over these complete invariant families extends to all times within each family.

Stop a path at the first failure and retain a direct physical-neighborhood conflict witness; no recipe repair or replacement after outcomes. Continue other rules within budget. Budget stops are censors, not failures. Report every rule/width path, including missing later floors.

## Measurements and partial-rule exports

Record gates, counts, wall/build/verification/export times, RSS, distinct exact physical keys and ordered-tree node counts. Preserve exact forced root-ID to derivative/decoder values, their domain, and all ordered child-node dictionaries needed to reconstruct physical neighborhoods. Leaves encode five horizontal bits; each successive level is an ordered five-tuple for the next transverse axis, oldest existing axis first and newest last. No hash alone identifies a neighborhood. Use canonical JSON and deterministic gzip (mtime=0) transported in numbered base64 text parts; retain hashes and an archive manifest. Export time is inside the budget. Off-beam defaults are metadata, not entries counted as constrained.

For every floor, record these seven features:
1. Forced-key count divided by 2^w * 4^(d-1); longitudinal translations add no further bound because all source words occur.
2. Fraction of distinct forced keys requiring derivative one.
3. Derivative-one fraction over all source/phase/position events.
4. Mean algebraic degree of phase derivative functions, divided by w.
5. Mean number of nonzero ANF coefficients of phase derivative functions, divided by 2^w.
6. Fraction of phase derivative functions with degree at most one.
7. GF(2) rank of the phase-by-source-word derivative truth matrix, divided by min(4^(d-1),2^w).

For features 4–7, fix longitudinal coordinate zero and view the encoded derivative at each transverse phase as a Boolean function of the entire source word. Source words are ascending integers with most-significant bit at position zero; phase order is tensor lexicographic order, newest axis first. The Möbius transform includes the constant coefficient in term counts. Zero and nonzero constant functions both have degree zero; zero has zero terms. Rank includes the constant truth-vector direction. These are functions PULLED BACK TO SOURCE COORDINATES, not native physical-neighborhood algebraic degrees or minimal native circuit sizes. Also preserve per-phase degree/term vectors and unnormalized ranks.

At 1D record a source baseline: source derivative event density, its ANF degree/w, ANF term count/2^w and distinct native successor configurations/2^w. Recipe baseline uses one-hot fields for the four masks, two signs, four exact Q forms and two field orders. No rule number or source truth-table bits enter a classifier.

## Class labels and inference units

Use Martínez (2013), A Note on Elementary Cellular Automata Classification, Table 2, https://arxiv.org/pdf/1306.5577v2 ; independently corroborated by Castillo-Ramirez and Magaña-Chavez (2023), A study on the composition of elementary cellular automata, Table 1, https://arxiv.org/pdf/2305.02947 . The checked-in labels JSON lists all 88 minimal representatives under reflection and state-complement conjugacy. Compute the symmetry orbits algebraically, validate all 256 rules are covered once and representatives agree with the label lists; do not copy printed equivalence tables.

This convention has Class IV representatives 41,54,106,110. Other literature uses only 54/110 (for example https://arxiv.org/html/2103.14053v2). A fixed sensitivity analysis removes the complete 41 and 106 orbits; it does not silently reassign them. Four Class-IV orbits, or two in sensitivity, cannot support a robust general Class-IV classifier.

Use an orbit as the comparison/prediction unit: average features equally over every member rule. Report raw 256-rule outcomes and within-orbit feature spreads separately. The common prediction cohort consists only of orbits for which ALL members reach 4D at BOTH widths. Report excluded orbits and failure/censor frequencies by class and recipe, with original denominators; no imputation or silent survivor-only population claim. Report descriptive orbit distributions at each floor, and the fixed birth,+1,pair:-1:2,PDMQ stratum as a recipe control with its denominators.

## Frozen exploratory analysis and predictions

For each width separately, run leave-one-orbit-out nearest-centroid classification. Standardize each feature using training-orbit mean and population standard deviation; zero-variance columns contribute zero. Average standardized training features within each class, assign held-out orbit to the nearest Euclidean centroid, and break ties by ascending class number. No hyperparameter search or trained threshold selection. Report confusion matrices, each class recall, overall accuracy and balanced accuracy (mean of the four class recalls).

Fixed feature views: source; recipe; source+recipe; lift2; lift3; lift4; all three lift floors concatenated; source+recipe+all lift floors. The primary contrast is balanced accuracy of source+recipe+all lifts minus source+recipe. Calibrate only this contrast at width 7 against 199 complete orbit-label permutations, preserving class counts, using numpy Generator(PCG64(20260914)); one-sided p=(1+count(permuted difference >= observed difference))/200. Other views and sensitivity summaries are descriptive, with no additional significance claims.

Predictions:
- P1: all 256 paths reach 4D at both widths; zero failures and zero censors.
- P2, exploratory directional expectation: Class III/IV orbit means tend to higher pulled-back degree/rank than Class I/II. No clean III/IV separation is expected from raw key counts; the earlier six-rule pilot already showed matching counts for 90/54/110 at width 7, so that observation is not a new prediction.
- P3, prospective usefulness criterion: adding lift features improves balanced accuracy by at least 0.05 at BOTH widths and width-7 permutation p<=0.05. Otherwise report this criterion as failed, weak or censored as appropriate. This tests usefulness to this fixed classifier, not creation of new information beyond the source rule. Width agreement is robustness on the same ECA universe, not independent samples.

Highlight any association only with both widths and the named class convention visible. No optimized feature selection, post-hoc alternative label set, confirmation on long trajectories, or class reassignment is part of this unit. Unexpected patterns may be recorded explicitly as post hoc.

## Controls, budget and preservation

Before the census, test the new field constructor against a scalar implementation across all mask/sign/Q/order categories on synthetic states; test reflection and state-conjugacy orbit code against full truth tables; test Möbius transformation against direct polynomial evaluation, and GF(2) rank against independent elimination on small matrices. Reuse the previous interner/default/conflict controls. Verify known positive-sign four-field pilot cases 90,54,110,157 reproduce saved forced-key counts through 4D without counting that as new evidence.

During each floor compare direct full patches at source indices 0,1,42,85,last and transverse tuples all-zero/all-one/all-three (15 events), and verify archive reconstruction for these controls. Independent Gate 2 checks implementation, raw accounting, output interpretation and a bounded fresh replay; it need not duplicate the complete scientific census unless a concrete concern requires it.

Run outside GitHub Actions. Total 15-minute cooperative wall budget including compilation, verification, feature extraction, export and analysis; 60 seconds per rule/width path; 4 GiB RSS soft ceiling. Checkpoints follow every floor/path. A numerical kernel may finish beyond its cooperative deadline; do not start new work beyond a cap. Do not auto-rerun or repair after censoring.

Freeze this protocol, recipe/class inputs and analysis definitions before experimental implementation. Commit implementation before the census. Record exact implementation/protocol/input hashes, execution environment, raw rows, exact partial rules and canonical account. Automatic CI checks hashes, archive structure and accounting only, with no scientific replay. Register the canonical result, update research/knowledge/checkpoint accounts, and obtain independent Gate 2 on the final gathering SHA before reviewer merge.
