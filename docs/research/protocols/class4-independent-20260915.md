# Independent Class-IV discriminator pilot

Status: frozen proposal, no scientific evaluation yet.

Authored by: Codex / OpenAI GPT-6 Astra, Myk's dimensional-lift session, 2026-09-15. Independent review: pending. Myk explicitly authorized an independent attempt and asked that Opus's implementation not be imported. His earlier Gate-1 waiver remains available, but independent prospective review is being sought. No Opus code or numerical data will be used.

## Question and scope

Can a declared combination of selective retention and continued dynamical change distinguish the two conventional Class-IV ECA symmetry families, 54 and 110, from the other ECA families? This is a finite exploratory discriminator, not a definition of Wolfram classes, proof of universality, proof of general lift behavior, or an intrinsic representation-independent invariant.

Two candidate scores are fixed below. Both must be reported; neither may be selected as if it were the only hypothesis tested. Prior conversations already exposed the target labels and failures involving 122/126. This is fresh implementation and prospective scoring, not blind hypothesis discovery. No threshold is fitted to class labels, and no claim of clean separation is permitted unless both positive families exceed every included negative on the frozen score.

## Representation and exact local objects

Binary radius-one ECA with lookup index 4*left+2*center+right. Periodic rings. Core width W=7; sensitivity widths 5 and 9. For external bits e=(left,right), Phi_e maps a W-bit block to the W outputs at exactly the same sites after one step. There is no shrinking or enlarged output window.

Loss p_e(b)=log2 count{b': Phi_e(b')=Phi_e(b)} counts ambiguity about the original block conditional on the two fixed external bits. It is observer-relative local ambiguity, not global irreversible erasure. All counts are exhaustive, with a uniform reference distribution over b.

Incoming capacity o(b)=log2 count{Phi_e(b): e in {0,1}^2}. The varied environment affects at most the two endpoints at one step. It is a descriptive control, not a bulk future count. Identity must have loss=capacity=0; a shift must have loss=capacity=1. Neither is assigned a positive selection score merely for having constant costs.

Let Q(b)=(b_1,b_2,b_{W-1},b_W). Let m(e,q)=mean_uniform[p_e(B)|Q(B)=q]. Define the residual a(e,b)=m(e,Q(b))-p_e(b). This removes the uniform conditional mean for identical external and endpoint bits. Incoming capacity is identical within each Q group, so it cancels from a within-group comparison. Let sigma be the standard deviation of a across all 4*2^W equally weighted (e,b) pairs. Retention R_W=E_visited[a]/sigma. If sigma<1e-12 set R_W=0 and record a degenerate flag. The zero is a scoring convention meaning no offered variation, not evidence of refusal.

## Candidate A: conditional retention with shape recurrence growth

For each ring N=9..14, enumerate all 2^N states and the exact functional graph. Compute maximum ordinary cycle period P_N. Quotient the states by all spatial rotations, using their least integer representative, and compute maximum cycle period Q_N of the exact quotient graph. The quotient removes rigid drift; a pure shift has Q_N=1. Save both spectra summaries.

alpha_Q is the ordinary least-squares slope of log2(Q_N) against N on 9..14. alpha_P is a diagnostic, not a substitute if alpha_Q fails. These are finite-window exponential-rate fits; they do not establish asymptotic growth or absence of recurrence. Candidate A_W = max(0,R_W)*max(0,alpha_Q). W=7 is primary; W=5,9 are sensitivity checks with no selection of the best width.

## Candidate B: useful older history with unresolved next-step variation

At a fixed spatial site let C=X_i(t), H_h=(X_i(t-h),...,X_i(t)) include h older bits and C, and Y=X_i(t+1). h=8 is primary, h=4,12 are sensitivity checks. Older history is useful only if it improves prediction over C alone on independent seed runs. This is an observation-relative temporal property, not a claim that the full ECA needs more than one state for evolution.

Split six seeds into two fixed groups of three. In each direction, train Bernoulli next-bit probabilities for contexts C and H_h on one group with Jeffreys pseudocount 1/2 per outcome. Unseen contexts predict 1/2. On the other group measure mean base-2 log loss CE_C and CE_H. Define M_cv=CE_C-CE_H, which may be negative. U is the plug-in conditional Shannon entropy H_test(Y|H_h) on those held-out seed counts. Directional score B_h=4*max(0,M_cv)*U. Report the average of the two directional scores, both M_cv values, both U values, and the corresponding plug-in I(Y;H_h|C). Do not silently clamp negative M_cv in diagnostic reporting. Cross-validation checks predictive improvement; U remains a finite-sample estimate.

This product asks for coexisting predictive information in older local history and unresolved next-step variation. It is a declared statistical score, not a conserved exchange rate. A constant, identity, or fully history-resolved periodic local sequence should have zero score. Independent temporal bits should not gain positive held-out predictability systematically. A spatial shift of an IID ring is a finite-ring control; its eventual long return is outside the tested history lengths.

## Domain, sampling, symmetry and labels

Compute every one of the 88 ECA orbits under spatial reflection and state-complement conjugation, using the minimum rule number as representative. Generate these orbits algebraically without consulting labels. No symmetry copy is an independent positive. Optional expanded 256-rule tables are transported copies and labelled as such.

Primary configuration: N=256, discard 256 steps, then count 512 consecutive transitions. Six NumPy PCG64 seeds 101,202,303,404,505,606, Bernoulli(1/2) initial bits. Store the full time series long enough to form histories at the first counted transition. Count all spatial positions. All rules share the same initial seed arrays, for paired comparisons.

Prespecified replication configuration: N=512, discard 512 steps, count 512 transitions, six fresh seeds 1101,1202,1303,1404,1505,1606. All parameters and scores remain fixed. This checks robustness to a second ring/burn-in/seed setting; it does not isolate the effects of changing each setting and supplies no new independent positive rule family.

Use the repository's archived Martinez2013/Castillo-Ramirez2023 representative labels only after feature computation. Primary positives: families 54 and 110. Exclude disputed families 41 and 106 from the primary positive/negative comparison and report them separately, without relabeling them. Keep families 122 and 126 as negatives in the primary test; their known structure is not a license to relabel misses. Report 18,22,30,45,60,90,105,122,126,146,150 individually in the Class-III comparison. Report the expanded four-family IV convention separately as sensitivity, never as a replacement for the primary target.

## Reporting and fixed predictions

For both candidates, both configurations, and every prespecified W or h: report all family scores, tied-rank AUC for the two positives vs included negatives, AUC vs Class III only, positive ranks, and every negative with a score at least the lower positive score. The latter is a descriptive separation diagnostic; it is not a fitted/deployable threshold. Report the one-factor components as ablations, not alternative winning classifiers.

Predictions: (P1 control) same-window identity/shift values and quotient shift period are exact; (P2 bet) each primary candidate has AUC>0.9 overall and >0.75 against Class III in both configurations; (P3 stronger bet) each candidate ranks both 54 and 110 above 122 and 126; (P4 robustness bet) both positive families retain positive scores and the signs of their predictive gains/retention across prespecified sensitivities. Record each failure separately. Perfect separation is not presumed. No score, sign, aggregation, class label, horizon or ring range may be changed in response to results; any later proposal requires a new named protocol and preserves this pilot.

## Verification and cost

Use the package's vectorized ECA semantics for trajectories, with batching that preserves row boundaries. Independently compare against scalar local updates on bounded toy inputs. Verify the local loss/capacity tables against direct enumeration, the zero conditional reference means, and complement/reflection covariance on transported toy contexts. For finite cycles, check quotient successor consistency on all states and controls 0,204,170 plus the accepted 54/110 ring-14 ordinary periods. Inspect histograms for correct sample totals and no overflow. Use int64 counts and exact integer graph transitions.

Run outside GitHub Actions. Hard wall budget 30 minutes total for scientific evaluation, with per-rule checkpoints and progress at most 60 seconds apart. Stop at the wall, preserve completed rules, and mark incomplete results censored; do not rank an incomplete rule population as a completed classifier. Expected cost is minutes, not a theorem-backed bound. No expensive CI replay or automatic rerun.

Freeze and commit protocol before implementation; pin implementation before evaluation. Canonical result records source SHA-256 hashes, parameters, all scores and failures. Raw count checkpoints stay available for reanalysis; recording and visualization do not change scientific scoring. A draft gathering PR preserves the unit. Final main merge requires independent Gate 2 and green relevant checks under AGENTS.md.

## Literature and interpretation

Older-history predictive gain is related to active information storage, with the immediate present conditioned out; innovation is conditional output entropy. See Lizier, Prokopenko and Zomaya, A framework for the local information dynamics of distributed computation in complex systems, https://arxiv.org/abs/0811.2690 . Exact preimage counting by de Bruijn matrices is established: Jeras and Dobnikar, Cellular Automata Preimages: Count and List Algorithm, https://rattus.info/al/files/conference.pdf . No novelty claim for these ingredients. The independent contribution under test is the explicitly declared combination and its finite ECA discrimination, if any.
