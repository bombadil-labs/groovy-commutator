# Factor-balanced arithmetic interactions, with individual rule pairs retained

Prospective protocol, 2026-09-15. Author: Codex (OpenAI), /root.
Gate 1 pending. No new CA evaluation or model fitting has occurred.
User authorization: “Let's try it!” following the completed PR262/PR264 study.

## Question and scope

Does combining arithmetic selectors improve held-out prediction of how a
particular rule pair's partition relationship changes between rings?
The previous study averaged across rule pairs and used a narrow confirmation
range in which selected descriptors lost support. This study balances a declared
factor-family grid across size bands and retains every rule-pair result.
It remains a scalar projection of stored partitions, not a complete shape
invariant or a Class-IV classifier. Historical sizes4..16 were already examined;
only the new sizes17,18,20,21 provide fresh empirical confirmation.

## Domain and balancing (chosen using ring arithmetic alone)

Keep rules0,18,30,54,90,110,126,204 and the same nine observations from PR264:
whole future-state equality at t=1,2,4,8,16,32; eventual basin; eventual cycle
length; transient distance to the eventual cycle. Keep exhaustive, uniformly
weighted binary source states, alignment by source-state identity, cadence1,
no burn-in, and full ECA rules. Preserve complete successor and partition arrays.

Define the family of ring n as (1[2 divides n],1[3 divides n]). The four
families are neither, 2-only, 3-only, and both. This does not identify
“neither” with primality in general. We do not claim to balance every prime
factor or prime exponent. Valuations are additional predictors, not balanced
strata. The finite domain cannot supply fresh powers of two cheaply.

Historical band A: every size4..9; historical band B: every size10..16.
Fresh band C: exactly17,18,20,21, one member of each declared factor family.
Within each band retain unordered ring pairs from DIFFERENT families. All six
unordered family-pair strata have support in every band. Ring pairs from the
same family and cross-band pairs are outside this scoring domain, not missing
observations. Counts are13 training pairs in A,17 in B,6 test pairs in C.
All28 unordered rule pairs and all9 observations remain separate tasks.

Training gives equal total weight to each of the12 (band,family-pair) strata,
and divides that weight equally among its actual ring pairs. Test gives each
of its six strata equal weight. Size ranges and within-stratum size gaps still
differ; the comparison is predictive extrapolation, not a causal isolation of
arithmetic. No prime-family relabeling or ring replacement follows inspection.

## Targets and frozen models

For each rule pair (a,b), observation o and ring n, use the same normalized
partition distance R_o(a,b;n)=VI(A,B)/n as PR264. Labels are aligned by source
state before VI; renaming partition blocks changes nothing. Target on n<m is
y=abs(R_o(a,b;m)-R_o(a,b;n)). Keep each rule pair's targets separately.

Use three nested models, separately fitted for each of the252 (rule pair,
observation) tasks. Every model includes an unpenalized intercept.

Size features: c=(n+m)/42 and g=(m-n)/21, then c,g,c²,g²,cg.
Arithmetic main features (v_p means the exponent of prime p in n):

- (1[2|n]+1[2|m])/2;
- (1[3|n]+1[3|m])/2;
- (v2(n)+v2(m))/8 and abs(v2(n)-v2(m))/4;
- (v3(n)+v3(m))/4 and abs(v3(n)-v3(m))/2.

M0 uses only the five size features. M1 adds the six arithmetic main features.
M2 adds every product a_i*a_j with i<=j of those six arithmetic features
(21 degree-two terms, including squares). This is a finite catalog of selector
interactions, not a hand-picked winning combination. It excludes size/arithmetic
cross-products in this unit. No model-specific feature selection is performed.

Fit each model by minimizing sum_i w_i(y_i-b-x_i beta)² + 0.01*sum beta²,
where weights sum to1 and follow the balanced strata above. No data-dependent
scaling, hyperparameter search, or penalty on the intercept. Predict all six
fresh ring pairs, saving both unclipped predictions and predictions clipped
to[0,1]. Score the clipped predictions. Freeze model coefficients, predictions,
training inputs and their hashes in a committed seal BEFORE generating any
fresh-ring successor maps or observations.

## Evaluation and reporting

For every task and model report test MAE and RMSE over the six equally weighted
fresh pairs, plus the individual predictions, errors, training fit errors,
and clipping counts. Primary comparison: M2 versus BOTH M0 and M1 on MAE.
A strict improvement requires an absolute MAE reduction greater than1e-12;
differences within1e-12 are ties. Preserve each task's outcome and effect size.
Report per-observation counts of improvements/ties/losses, alongside the full
28-rule-pair table and the specific54/110 pair. Do not select a replacement
model or observation using test performance. Aggregate counts describe
dependent tasks, not independent trials or a class-level significance test.

The prospective scientific question is whether M2 beats both simpler models
on the fresh band, including whether any gain is broad or concentrated in a
few rule pairs. No improvement is presumed. Mixed and negative outcomes remain
results. No IID p-values or Class-IV label assignments are produced.

## Controls and independent verification

1. Before fitting, assert all six family-pair strata in every band and exact
   equal total training weight per (band,stratum). This is a design check only.
2. Rule0/204 future-partition relation is exactly1, so its ring-change target
   is zero at all six future horizons. All three models must predict zero up
   to numerical precision for those tasks.
3. Rule90 future-image entropy must match an independent GF(2) rank calculation
   for every new horizon/ring, avoiding reliance on the partition implementation.
4. Directly verify new batched CA rows against the core update convention,
   all source/array hashes, and VI invariance under block-label renaming.
5. Independent reviewer checks the full fitting/weighting/prediction/scoring
   pipeline with a different linear-algebra construction, independently
   reconstructs new scalar successor maps and graph/VI quantities on a
   representative panel (all eight rules at width17; rules54/110/90 at width21),
   checks full arrays at those cases, and checks stored graph consistency and
   all relations throughout the full new panel. No unseen confirmation arrays
   may be inspected or generated before the prediction seal.

## Resource and provenance contract

Reuse historical arrays and metrics with original hashes; do not modify PR264
outputs. Fresh stage comprises32 rule/ring cases. Generate fresh widths in
ascending order, all eight fixed rules per width, checkpointing every complete
case. Frozen implementation and reviewed protocol precede model fitting.
Training stage budget:120seconds. Fresh generation+scoring budget:900seconds,
3GiB address space and checked resident memory. A budget error is incomplete,
not zero; disclose partial coverage and do not quietly change the panel.
Independent verification runs separately off CI with its own reported cost.

No scientific evaluation or independent replay runs in automatic CI. Commit
compact results and the usual fast hash-integrity registration, preserve all
raw data/model inputs/predictions/evidence/review in an archive, and update
the research account. No automatic third experiment follows this unit.
