# Unspecified completions dominate the response-capacity test

Does replacing raw cohabitant counts with distinct responses and retained source information produce a Class-IV discriminator? This bounded test fails. Four fixed hash completions give every one of the 88 tested representatives the maximum score at both widths and every measured horizon. Adding four simple completion policies changes the scores but does not separate 54/110; identity outranks both at the primary horizon.

Evidence: exploratory. Authored by Codex (OpenAI), Myk's dimensional-lift session. The preceding [independent discriminator failure](2026-09-15-class4-independent.md) and the cohabitation discussion motivated this new test. Myk authorized it with "let's do it", waived repeated Gate 1/protocol ceremony and requested one final push. This note preserves a new failed candidate; no earlier result or class label was changed.

## Construction and exact observation

The input is the accepted uniform six-field cache, dimension 2, all minimum ECA symmetry representatives and complete width-seven/eight source families. The beam has 6×W cells with vertical period six and horizontal period W. Its physical neighborhood has vertical radius three and horizontal radius two. The forced flip-mask table is preserved exactly. Native evolution and source recovery are verified on all 2^W source states.

A probe flips the cell at column zero in one of the six rows. This is a changed cell in a periodic fundamental domain, with repeating copies on the infinite lattice. It is not an isolated defect on an infinite background. The six probe rows and all source states are included, with horizontal translates covered by the complete source ensemble.

For a given perturbed configuration, let u count the distinct queried physical keys not fixed by the beam table. Each key contributes one independent binary flip-mask choice, shared by every occurrence of that key. Different assignments differ at an output cell containing a changed key. Therefore the exact number of distinct one-step responses over all binary local completions is 2^u. Unqueried table entries contribute nothing to this count.

Only five horizontal positions times six distinct vertical positions can be affected, so u≤30. The observed u values span 18–30 at width seven and 16–30 at width eight. Per-rule means of the log2 response count range from 27.914 to 30 bits at both widths. Thus even this single-cell probe exposes many response choices. The radius covers the entire vertical period; that geometry is a substantial part of the exposure.

All completions agree on the complete invariant unperturbed beam. The checked one-step equality and closure establish that they agree at every later time there. This gives a precise distinction between unassigned entries and entries that a perturbation can actually use.

## Fixed longer-horizon comparison

Eight completion policies retain the same forced table. On unforced entries, four set the flip mask to zero, one, the central bit, or its complement; the last two produce constant-zero or constant-one output off the forced domain. Four more take the low bit of SplitMix64 of the physical key with fixed seeds 1701–1704. A chosen policy remains fixed throughout a trajectory. It has no access to phase, source index, time or class label.

We measured full child-state endpoints at times 1,2,4,8. Time four at width seven is primary; width eight and the other times are prespecified checks. Within each bank and horizon, policies are identified when their endpoint maps agree on the entire source/probe panel. Equal maps are counted once. Uniform weighting over these observed behavioral classes removes duplicate policies from the law prior, but it remains a finite experimental prior, not a uniform distribution over all completions.

Let S be the uniform W-bit source state, J the known probe row, A the uniform behavioral completion class, and Y the endpoint. The fixed quantities are:

- M=I(S;Y|J)/W: source information retained when the observer does not know which completion acted.
- F=H(Y|S,J): distinguishable response diversity across the completion classes, in bits.
- T=M F/log2(B): the candidate score, using the original bank size B=8 or B=4 in the denominator.

Known-completion retention I(S;Y|A,J)/W, per-policy entropies, quotient counts, M alone and F alone are also retained. Structured-only and hash-only four-policy banks were specified before execution. "Past" here is the initial source state, not an unbounded prehistory. Different counterfactual completions are different automata, each deterministic; no single fixed rule branches spontaneously.

## Results

All 176 rule/width evaluations completed in 45.748 seconds outside Actions, with peak resident memory 59,884 KiB. No trajectory was rerun. There are 704 endpoint panels and 2,112 bank/horizon metric sets.

| Root representative | Full bank, W=7, t=4 | Full bank, W=8, t=4 | Hash bank, either width, t=4 |
| --- | ---: | ---: | ---: |
| 0 | 0.738188 | 0.708710 | 1.000000 |
| 54 | 0.750000 | 0.749674 | 1.000000 |
| 110 | 0.750000 | 0.750904 | 1.000000 |
| 204, identity | 0.751194 | 0.753898 | 1.000000 |

The hash result holds for **every tested representative at all four horizons and both widths**, with M=1 and F=2. Its class AUC is 0.5. Each finite source/policy pair remains distinguishable at a fixed probe row, so this observer can decode the entire source and distinguish the hash policy's response. This is a measured property of the finite endpoint tables, not evidence of organized memory or computation by every root ECA.

The full bank always has F=3 and eight behavioral classes. Its primary overall AUC is 0.702381 at W=7 and 0.761905 at W=8; Class-III AUC is 0.590909 and 0.636364. At W=7, 54 and 110 tie at average rank 26.5, with 40 negatives tying or exceeding their score. At W=8, their ranks are 31 and 12, with 29 negatives at or above the lower positive. These ranks use the two primary positives and 84 included negative representatives. Disputed 41/106 remain separate; 122/126 remain negatives.

Across all evaluated rule/width/horizon cases, the full-bank score equals (1+structured-bank score)/2 to within 3.4e-16. Independent audit establishes the mechanism on all 4,224 probe-conditioned panels: the hash source/policy map is injective, and hash and structured output supports never overlap. The endpoint therefore identifies the bank; retained information is the equally weighted mixture of perfect hash retention and structured retention. With response entropy maximal, the stated score identity follows. The hash policies add no class ordering here.

P1, agreement on the invariant unperturbed beams, passes at both widths. P2, clean separation under the full bank, fails twice. P3's strict wins over the listed simple/additive controls pass only 13 of 40 comparisons. P4, clean separation under each four-policy bank, fails all four cases. Every failed comparison, sensitivity, ablation and disputed-rule score remains in the result. No best horizon, completion bank, threshold or revised score was selected after the run.

## Interpretation and boundary

This candidate largely measures the response structure supplied by the completion. A root rule may erase its original source on the beam while a compatible extension preserves distinguishable images of those source states after a perturbation. The output has 6W bits for W source bits and at most three bits identifying the sampled policy. Global distinguishability within that small ensemble is therefore a weak requirement for organized dynamics. It does not demand an economical, local or robust decoder.

The experiment supports abandoning this candidate as a root Class-IV discriminator. It does not prove that every statistic of completion families must fail or that cohabitation is irrelevant. It tests compatible completions of each individual beam table, not the entire pairwise cohabitation graph across different beams. The eight-policy bank is small and deliberately includes erasing policies; hash laws are fixed probes, not independent empirical samples of a universal completion distribution.

Two modeling questions remain separate. On a fully specified invariant beam, completion freedom produces no additional unperturbed futures. Outside that beam, a chosen completion supplies new dynamics. A next discriminator would need an explicit reason those dynamics belong to the property being attributed to the root, or would keep the actual rule fixed and perturb its inputs. This run did not test that next proposal.

Widths seven/eight are finite-domain checks, not new independent positive families. Scores refer to the chosen minimum representatives and physical orientation; covariance of the hash bank under root reflection/complement is not established. The sole positive convention is still the two core families 54/110. Nothing here establishes a universal Wolfram class definition, an infinite-lattice response theorem, or a dimensional-lift extension theorem.

## Reproduction, corrections and independent audit

The [local design](protocols/response-quotient-20260915.md) and [source freeze](../../experiments/response_quotient_20260915/local-source-freeze.json) were recorded before execution, under Myk's authorization. The [exact executed runner](../../experiments/response_quotient_20260915/frozen_runner.py) is preserved byte-for-byte. The [current runner](../../scripts/response_quotient_20260915.py) differs only in two reporting lines: a NumPy Boolean cast and the zero-padded archive record locator.

All trajectories and metric checkpoints completed before JSON rejected a NumPy Boolean in a P3 comparison. The [recovery script](../../scripts/summarize_response_quotient_20260915.py) rebuilds the report from saved checkpoints without simulating. It asserts the exact two-line source difference, verifies all endpoint/input hashes, and corrects 114 input locators to the archive's zero-padded names. The original checkpoints remain unchanged. These were reporting defects, not changed scientific calculations.

- [Complete canonical result](../../results/response_quotient_20260915.json): every endpoint digest, metric, comparison, failure, parameter and source hash.
- [Independent verifier](../../review/response_quotient_independent.py) and [audit report](../../review/response_quotient_independent.json): saved-endpoint and input-record reconstruction, analytic/scalar controls, metrics and failure accounting. No author metric functions are imported; no full trajectory replay is required.
- [Raw archive manifest](../../experiments/response_quotient_20260915/raw-archive.json): all input records, endpoint arrays, immutable checkpoints and execution metadata. Extract the archive at the repository root to restore the run directory.

Author controls cover physical keys against explicit tuple neighborhoods, all completion policies against scalar arithmetic, shared-key response counting, state packing and identity/erasure/XOR information examples. The XOR control distinguishes conditional recoverability with a known policy from recoverability with an unknown policy. Automatic CI performs bounded controls and source integrity only. Independent audit and final integration are recorded on the gathering PR; no prospective independent approval or extra scientific execution is implied.

The independent audit passed all 704 endpoint panels, 2,112 metric sets and every ranking/prediction, with maximum numerical discrepancy 4.44e-16. It reconstructed all 202,752 u values and checked decoding and invariant-family successors for all 33,792 source states. Both reporting corrections and all corrected locators were verified. This is independent recomputation of saved evidence and bounded scalar controls, not a second complete scientific trajectory execution.
