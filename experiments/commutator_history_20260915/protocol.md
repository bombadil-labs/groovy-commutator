# Direct commutator-history augmentation

Frozen before evaluation, 2026-09-15. Owner: Codex /root.
Protocol review: none at freeze; run authorized by Myk 2026-09-15 through the standing Gate 1 approval and instruction to iterate locally and publish at the end. Independent retrospective review is required before integration.

## Question and observable

Does explicit history of the actual commutator add useful predictive information, and does adding this information improve the frozen recurrence/spreading discriminator from PR #255?

For a native trajectory S[t+1]=E(S[t]), define D[t]=S[t] XOR S[t+1] and G[t]=D[t+1] XOR E(D[t]). This is the error of the closure predictor E(D[t]) for the next observed change mask D[t+1]. Trace G(S[t]), not the different trajectory E^t(G(S[0])). All native evolutions and off-trajectory evaluations use the specified root rule; there is no off-beam completion.

## Fixed inputs and controls

Reuse immutable R6 native trajectories for all 88 ECA symmetry representatives, width 2039, burn 2048, 1032 saved frames and seeds 6041511..6041514. Reuse all 12 R10 trajectories: radii 1,2,3, correction absent/present, seeds 6041541/6041542. The larger-radius family has no assigned Wolfram labels. Preserve the archived q, alpha and selected flags; do not refit them.

Train on seed 6041511 for ECAs and 6041541 for the radius family. Use source times 16..479 for fit, 528..1025 for velocity selection, and every valid source time 16..1025 on all other seeds for evaluation. Four extra steps are needed for the target and two native steps to calculate G. G therefore has 1030 frames. Train/selection source and target native-frame supports are separated. Test seeds are independent initial realizations, not unseen rule families. All prior baseline results were already seen; these G measurements were not.

The test includes the four additional reflection/conjugation variants of the two core ECA symmetry families (six labeled rules in total), generated from matched transformations of the saved trajectories, to check whether the commutator-based augmentation depends on bit convention. It does not presume G itself has complement covariance.

## Models and fixed decision

Target: the bit G[t+4, x+4v]. Five velocities are considered, in tie-breaking order 0, -r/2, +r/2, -r, +r. All used time differences are multiples of four, so displacements are integers. The current-only model conditions on the complete radius-r neighborhood of G[t] around x. Three nested extensions add the bits G[t-4,x-4v], G[t-8,x-8v], G[t-16,x-16v], respectively. Estimate conditional probabilities by count tables with the Krichevsky-Trofimov binary prior: (ones+1/2)/(total+1).

Fit all tables on the fit interval. Choose v solely by maximum selection-interval reduction in bit log loss for the three-history-bit model relative to current-only. Freeze the tables and selected v, then evaluate each held-out seed. Report all four losses, all incremental gains, commutator density/entropy and count-table coverage. Keep negative gains.

The primary memory criterion is a held-out reduction greater than 0.01 bits per target. The augmented decision is the original selected flag AND this criterion. This threshold and the geometry are fixed before the G results; no threshold search is allowed in this unit. Report all 88 representatives, all additional core variants and all wider-radius cases. With the original baseline already separating the undisputed ECA families in R6, improvements can only concern robustness/interpretation and the disputed or unclassified challenges; do not claim unseen-rule accuracy gains.

Periodic ECA inputs use their original boundary. R10 calculations use open-window E(D), and crop at least 17r cells from either side of the G array before history/target scoring, so no rolled or padded value can enter a scored context. Radii scale the current neighborhood and candidate velocities; the historical feature count stays three.

Negative control: independently permute complete time slices of G (preserving each spatial frame) for ECA representatives 30,54,73,106,110,126 and all six R10 rule families. Permutation generator seed is the native seed plus 9000000. Fit, select and evaluate the same pipeline. This is a temporal-organization control, not a claim of iid residuals or a complete null distribution.

## Checks, budget and interpretation

Check the G formula against exhaustive scalar five-cell contexts for all 256 ECAs and against direct open-window evaluation for the wider-radius family. Confirm known constant-G controls and current-state/target index alignment. Independent review must recompute representative count tables and the final summaries, including every core and wider-radius result. Preserve packed G histories and sufficient count tables, input/source hashes, wall times and environment.

Run outside Actions, with a 10-minute local analysis budget. If over budget, retain a checkpoint and report scope rather than alter the statistic. Automatic CI is compilation and fixed provenance only.

Positive predictive gain is finite observed memory under this observation/model. It is not proof of causal memory, optimal predictability, asymptotic behavior, beam invariance or Class IV specificity. Raw G depends on the differentiation convention; the matched core-orbit checks are mandatory. A negative result rejects this specific finite augmentation, not every use of commutator history.
