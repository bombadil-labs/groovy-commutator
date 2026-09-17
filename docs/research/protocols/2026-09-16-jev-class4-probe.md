# Protocol: Jev semantic feature probe for an independent ECA Class-IV signal

**Status:** FROZEN / UNRUN / pending independent Gate-1 review  
**Date:** 2026-09-16  
**Author:** GPT-5.6 Sol, Groovy Commutator session  
**Protocol review:** none at freeze; **do not implement or evaluate until reviewed, unless Myk explicitly authorizes the repository's no-review-at-freeze exception.**

## 1. Question

Does the already accumulated Groovy Commutator evidence contain a **second Class-IV signal** for the conventional ECA core families 54 and 110, independent of the finite predictors and composites already discovered?

This is an exploratory feature-discovery study. It is **not** a new definition of Wolfram Class IV, a claim of unseen-rule generalization, or a test of Jev's general scientific reasoning ability.

The target question is deliberately narrower than “can Jev classify Class IV?” because the repository already contains finite ECA separators. The purpose is to discover whether semantic combinations of *other primitive measurements* point to a small explicit relation worth distilling and testing mathematically.

## 2. Source freeze

Repository: `bombadil-labs/groovy-commutator`  
Pinned main SHA:

`4ff191cb46bd9e0a9b349487aa3875486932ac9d`

Primary source records:

- `docs/research/2026-09-15-class4-independent.md`
- `results/class4_independent_20260915.json`
- `results/class4_composite_20260915.json`
- `docs/research/2026-09-15-commutator-history.md`
- `results/commutator_history_20260915.json`
- `docs/research/2026-09-15-partial-cohabitation.md`
- `results/partial_cohabitation_20260915.json`

Optional class-blind atlas extension, only if an extractor can be written without using the catalog's label-selected slots:

- `docs/research/2026-09-15-observation-catalog.md`
- `results/observation_catalog_20260915.json`

Known finite-predictor controls:

- `docs/research/2026-09-15-beam-discriminator-loop.md`
- `results/beam_discriminator_loop_20260915.json`

The TypeSafe integration must follow the TypeSafe agent skill and current SDK semantics. At freeze:

- skill source: `typesafe-ai/skills`, `skills/typesafe-ai/SKILL.md`
- observed skill commit: `65a39f393687675ce170e6094757de20370365b9`
- observed Python SDK source commit: `420ef4ffb612d5a539a1e0f0fe883ff6770340af`
- current SDK default model alias: `jev-latest`
- API credential source: environment variable `TYPESAFE_API_KEY`

The harness records the actual returned model name and usage for every request. No API key is written to files or logs.

## 3. Domain and labels

Unit of analysis: the **88 minimum ECA representatives under reflection/complement conjugation** already used by the Class-IV research program.

Primary positives:

- representative family 54
- representative family 110

Primary negatives:

- the 84 representatives labeled Wolfram Class I–III in the inherited label file.

Disputed representatives 41 and 106:

- excluded from all primary scores and thresholds;
- reported descriptively after the primary results are fixed.

Symmetry partners are not additional independent positives.

Because there are only **two undisputed positive families**, no ordinary estimate of classifier generalization accuracy is permitted. AUC/ranks are descriptive finite-panel statistics only.

## 4. Leakage exclusions

The primary Jev state MUST NOT contain:

- ECA rule number;
- binary truth table;
- rule name;
- Wolfram class;
- spacetime image or textual description naming a rule;
- symmetry-family identity;
- any class-conditioned rank or AUC;
- any feature selected by inspecting the 54/110 labels;
- any post-hoc Class-IV composite score.

### Known successful channels withheld from primary discovery

The primary feature state additionally excludes:

1. recurrence residual `q` and disturbance-spreading exponent `alpha_T` from the beam discriminator loop;
2. the known finite selection flag `0 < q < 1/2 and alpha_T > 1/2`;
3. quotient-cycle-growth slope(s) `alpha` used in the retention/history composite program;
4. derived composites `A`, `B`, `C`, `D` or any later product/threshold selected after inspecting Class-IV results;
5. the seven observation-catalog slots selected specifically to minimize overlap with negative classes.

These quantities may appear only in **post-primary positive-control/interpretation runs**.

## 5. Primary primitive feature families

Only measurements with complete coverage of the 88 representative families may enter the primary profile.

### F1 — selective retention / local history primitives

From the independent Class-IV program, retain primitive values only:

- retention `R` for each declared trajectory condition;
- held-out local predictive gain `M` for each declared condition/direction aggregate;
- residual conditional uncertainty `U` for each declared condition/direction aggregate.

Do not supply the model the formulas or values of `A`, `B`, `C`, `D`, or quotient-cycle growth.

### F2 — commutator-history primitives

From the commutator-history program:

- held-out predictive gain from older `G` samples beyond the current local `G` neighborhood;
- per-held-out-seed values when available;
- label-free summaries: mean, minimum, maximum, range.

No baseline Class-IV selection flag or recurrence/spreading features enter this family.

### F3 — partial-rule / cohabitation primitives

From the exact pooled-width partial-cohabitation audit:

- compatible-partner fraction;
- fraction of partners with shared pinned support;
- non-vacuous-compatible fraction;
- any per-root forced-domain size or support count already present in the canonical result;
- class-blind summaries of pairwise conflict count / additional-pin cost, if present with complete 88-representative coverage.

No clique, hand-selected partner identity, or class-conditioned statistic is permitted.

### F4 — optional observation-atlas distribution summaries

This family is allowed only if the implementation extracts it **without using any label-selected observation slot**.

For each rule and each generic measurement type (entropy, next uncertainty, refinement gain, spatial information, common-target uncertainty, branching mass, complementary gain), summarize the distribution across the complete observation catalog using class-blind fixed functionals:

- minimum;
- 25th percentile;
- median;
- 75th percentile;
- maximum;
- mean;
- standard deviation.

Observation aliases may be deduplicated exactly as recorded by the catalog, but no 54/110-based selection is allowed.

If the canonical result does not contain sufficient class-blind per-rule values to construct this family reproducibly, F4 is omitted rather than regenerated post hoc.

## 6. Label-free normalization

Before any Jev call, every scalar feature is transformed using **all 88 representatives without class labels**.

For scalar `x`:

- retain the raw value;
- compute empirical percentile rank in `[0,1]`, with average ranks for ties;
- compute robust centered scale `(x - median) / max(IQR, epsilon)` with `epsilon=1e-12`.

Missing values are represented explicitly as `null`; no class-dependent imputation is allowed.

Condition-series features also receive only these predetermined class-blind summaries:

- mean;
- minimum;
- maximum;
- range.

No polynomial products, ratios, threshold searches, or feature selection occur before Jev.

## 7. Primary Jev state

Each candidate request receives one anonymous structured JSON state:

```json
{
  "measurement_contract": {
    "retention": "...definition...",
    "predictive_gain": "...definition...",
    "residual_uncertainty": "...definition...",
    "commutator_history_gain": "...definition...",
    "cohabitation": "...definition..."
  },
  "cohort_reference": {
    "feature_medians_and_iqrs": "...label-free cohort summaries..."
  },
  "candidate": {
    "F1": "...raw, percentile, robust-scale values...",
    "F2": "...",
    "F3": "...",
    "F4": "optional"
  }
}
```

There is no rule identifier anywhere in this object.

All independent questions are asked in the **same request**, as recommended by the TypeSafe skill.

## 8. Frozen Jev questions

Each is a `Noul` question. The returned yes-probability becomes a reusable semantic feature. Questions do not mention Wolfram classes.

### J1 — retained-history-with-openness

**Instructions:**  
“Does the anonymous candidate profile show that information from earlier states remains measurably useful while the observed local dynamics also retains nontrivial residual uncertainty across conditions, rather than collapsing toward either complete predictability or unstructured uncertainty?”

**Criteria:**  
“Answer yes only when the history-related measurements and residual-uncertainty measurements jointly support this pattern across more than one recorded condition. Residual uncertainty alone is not evidence of response capacity.”

### J2 — constrained-but-nonrigid

**Instructions:**  
“Does the anonymous candidate profile show a nontrivial structural constraint regime: neither nearly vacuous compatibility with other partial rules nor near-total isolation/rigidity?”

**Criteria:**  
“Use only the cohabitation/support measurements. Favor profiles with substantial shared constraints and meaningful exclusions; do not equate high compatibility by itself with structure.”

### J3 — cross-channel-coherence

**Instructions:**  
“Do the independent retention, history, commutator-history, and partial-rule measurements coherently indicate the same nontrivial intermediate dynamical regime rather than one isolated extreme statistic?”

**Criteria:**  
“Answer yes only when at least two independent measurement families support the interpretation and no available family strongly contradicts it.”

### J4 — persistent-organization

**Instructions:**  
“Does the profile provide evidence for organization that persists across changed trajectory conditions rather than appearing only in one finite setting?”

**Criteria:**  
“Use stability or systematic change across the recorded conditions. Do not infer persistence from a single high score.”

### J5 — selective-memory

**Instructions:**  
“Does the profile suggest selective retention of dynamically relevant information rather than either indiscriminate memory of everything or rapid erasure?”

**Criteria:**  
“Use retention together with predictive-history evidence. A high memory score without evidence of selectivity is insufficient.”

### J6 — balanced-capacity

**Instructions:**  
“Taken as a whole, does this anonymous profile occupy a structured middle regime in which constraints, historical dependence, and remaining local alternatives coexist?”

**Criteria:**  
“Do not answer yes merely because values are numerically near cohort medians. The evidence must be a coherent combination of the named measurements.”

No question may be edited after the first response is obtained.

## 9. Prompt-name control

Run the primary calls twice on the identical numeric data:

### Semantic condition
Use the field names and measurement definitions above.

### Opaque condition
Replace every feature name with a frozen random code (`f001`, `f002`, ...), but provide a neutral statement that the values are independent measurements of one deterministic dynamical system. Do **not** provide semantic definitions.

Questions J1–J6 are replaced in the opaque condition by one generic `Noul`:

> “Does this anonymous multivariate profile exhibit a coherent, non-extreme pattern across several independent measurements rather than being dominated by one coordinate or one extreme?”

This is a diagnostic, not expected to be semantically equivalent to the six primary questions.

The codebook from semantic names to opaque codes is generated once from seed `20260916` and frozen before evaluation.

## 10. API repetition and provenance

For each of 88 candidates:

- make **three** identical semantic requests;
- make **three** identical opaque requests.

Each request records:

- SHA-256 of the exact serialized state;
- SHA-256 of the exact question specification;
- returned model name;
- token usage;
- all Noul probabilities;
- UTC timestamp;
- attempt number;
- SDK version if available.

No retry result is silently substituted for a failed scientific request. SDK transport retries may occur according to the SDK policy, but request-level failures are recorded. A candidate with fewer than two successful attempts in a condition is marked censored for that condition.

Primary score per Jev feature = median yes-probability across successful attempts.

## 11. Primary evaluation

Primary evaluation occurs only after every Jev response has been saved.

For each J1–J6 separately, report:

- rank of 54;
- rank of 110;
- lower-positive rank;
- number of undisputed negatives scoring at or above the lower positive;
- finite-panel AUC against all undisputed negatives;
- finite-panel AUC against Class III negatives only;
- scores of hard controls 9, 30, 73, 90, 122, 126;
- disputed 41/106 scores separately.

No weighted combination of J1–J6 is part of the primary experiment.

### Pair-rank null

Using the fixed Jev scores, enumerate all `C(86,2)` or appropriate pairs among undisputed representatives and compare the observed `{54,110}` pair to the distribution of arbitrary two-rule pairs on:

- worse-member rank;
- mean rank;
- minimum pairwise AUC.

This is a finite combinatorial reference, not an IID p-value.

## 12. Predeclared signal levels

For an individual J-question:

- **strong independent signal:** both 54 and 110 are in the top 5 undisputed representatives and no more than 3 undisputed negatives are at or above the lower positive;
- **moderate signal:** both are in the top 10 and no more than 8 negatives are at or above the lower positive;
- **no useful signal:** otherwise.

These labels are descriptive gates for whether to attempt mathematical distillation. They are not claims of classifier accuracy.

A signal is called **stable** only if each core positive's three request probabilities have range <= 0.10 and the median ranking conclusion is unchanged when any one attempt is removed.

## 13. Positive and contamination controls — only after primary freeze is evaluated

### C1 — known-predictor restoration
Restore the previously successful recurrence/spreading and quotient-cycle quantities. This checks whether Jev's judgments change when known finite ECA signal is made available. It is not new evidence.

### C2 — rule-ID contamination
Give Jev only a rule number and ask whether it is conventionally Class IV. This measures possible memorization/contamination. It cannot invalidate the anonymous primary state but informs interpretation.

### C3 — label-aware reference prompt
Provide anonymous positive-reference profiles and negative cohort summaries and ask one explicit “positive-reference-like” Noul. This is supervised prompt classification and is reported separately from the primary semantic features.

### C4 — random-label reference control
Repeat C3 over at least 100 deterministic random two-positive label assignments using seed `20260916`. Compare the real pair's finite ranking to this null.

## 14. Classical controls

Using exactly the same primary primitive feature table and no known successful withheld channels:

- univariate rank scan;
- pairwise monotone threshold scan;
- L2 logistic regression;
- depth-2 decision tree;
- random forest with fixed hyperparameters.

Because there are only two positive families, these are exploratory descriptive controls. No hyperparameter tuning on the labels is permitted.

The main comparison is whether Jev-derived semantic features point to a compact primitive subset or interaction not already obvious in these controls.

## 15. Distillation rule

Jev never becomes the final Class-IV discriminator.

If a predeclared Jev feature reaches moderate or strong signal:

1. inspect only the primitive inputs associated with that frozen question;
2. search for a small explicit relation using fixed-complexity candidates:
   - one threshold;
   - conjunction of two thresholds;
   - ratio/difference of two primitives;
   - depth-2 Boolean rule over thresholded primitives;
3. freeze that mathematical candidate before any new trajectory/ring data are generated;
4. validate prospectively on genuinely fresh conditions;
5. retain hard controls 9, 73, 122, 126 and the wider-radius challenge where applicable.

If Jev only rediscovers a known withheld channel after C1, record it as a replication/control, not a new discriminator.

## 16. Failure criteria

The study fails to find an independent signal if:

- no J1–J6 feature reaches the moderate gate;
- apparent separation depends on one unstable API attempt;
- the result vanishes under trivial normalization changes already specified by the protocol;
- the semantic result is reproduced equally by many random two-positive assignments in C4;
- or the only successful information enters through a known withheld predictor.

A negative outcome is publishable and should stop recombining these same measurements without a new hypothesis.

## 17. Non-claims

This experiment does not establish:

- a universal definition of Class IV;
- generalization beyond ECAs;
- causal mechanisms;
- that Jev “understands” cellular automata;
- statistical independence of symmetry-related rules, trajectory samples, or measurements;
- unseen positive-family validation;
- novelty relative to prior literature.

Any resulting mechanism or novelty claim requires a separate prior-art search before promotion.

## 18. Required review before implementation/evaluation

An independent collaborating agent should review:

1. leakage exclusions;
2. whether any primitive feature was already selected using the target labels;
3. the six frozen Noul questions;
4. the low-positive-count interpretation;
5. the control ordering;
6. whether the success gates invite overfitting;
7. whether the optional observation-atlas extraction is genuinely class-blind.

Material changes after Gate 1 require renewed review.

