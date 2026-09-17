# Jev Run 3 — matched operational-codebook ablation

## Purpose

Close the remaining interpretation hole in the completed Jev ECA scout.

Run 1 (`jev_raw_responses.jsonl`) used semantic feature names + operational definitions + the six frozen J1–J6 questions. Run 2 (`jev_opaque_responses.jsonl`) replaced both feature semantics and the six questions with opaque codes + one generic question. Because two things changed at once, Run 2 cannot distinguish whether J4/J5 succeeded because Jev understood the operational measurement definitions or because evocative feature names/question framing primed the result.

Run 3 changes **only the feature-name surface** while retaining operational meaning and the exact six questions.

## Frozen source

Use the exact same 88 anonymous candidate states/numeric measurements as Run 1. Do not regenerate trajectories, renormalize values, add/remove features, expose rule IDs/classes, or reorder class labels into the state.

Existing run integrity:

- 88 anonymous ECA representatives;
- 3 requests each = 264 requests;
- Run-1 returned model: `jev-1.13.0`;
- original question SHA-256 in raw records: `77f4b1924f9f39845bd200deb30931ec30586934373ef4d363309b66691cb8e6`.

Prefer the exact serialized Run-1 states if your old probe bundle contains them. Verify each rebuilt state's SHA-256 against the corresponding `state_sha256` from `jev_raw_responses.jsonl` **before renaming fields**. If those hashes do not match, stop and treat the rebuild as a new experiment rather than a matched ablation.

## Transformation

Generate one deterministic bijection from every semantic scalar/series feature key to opaque codes `f001`, `f002`, ... . Reuse the Run-2 seed/codebook (`20260916`) if the old harness has it. Otherwise generate a new mapping once, save it, and hash it; do not alter it after the first Jev request.

For each state:

1. replace the feature's short semantic key everywhere in the numeric candidate payload with its opaque code;
2. preserve every numeric raw/percentile/robust-scale value exactly;
3. preserve the label-free cohort reference exactly;
4. supply a `measurement_contract` keyed by the same opaque codes, containing the **operational definition** of what each measurement computes;
5. do **not** reveal the old short feature name in that definition.

Example:

```json
{
  "measurement_contract": {
    "f017": "Measures whether states actually visited by the trajectory preferentially occupy locally less predecessor-ambiguous same-window transitions relative to the frozen boundary-conditioned reference ensemble.",
    "f023": "Measures held-out predictive log-loss improvement from the declared finite local history over the current-bit baseline."
  },
  "cohort_reference": { "...": "unchanged Run-1 values" },
  "candidate": { "F1": { "f017": { "raw": 0.0, "percentile": 0.0, "robust_scale": 0.0 } } }
}
```

The contract should explain **how the number is operationally produced**. Avoid interpretation-loaded synonyms such as “selective memory”, “organized persistence”, “Class IV”, “complexity”, etc.

## Questions — unchanged from Run 1

Ask all six in the same request.

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

Do not edit any question after the first response.

## Repetition and output

For each of 88 aliases make three identical requests. Save every response before inspecting the positive identities.

Recommended output filename:

`jev_codebook_responses.jsonl`

Each line should contain at least:

```json
{
  "alias": "anon_001",
  "attempt": 1,
  "mode": "semantic_codebook",
  "model": "jev-1.13.0",
  "nouls": {"J1":0.0,"J2":0.0,"J3":0.0,"J4":0.0,"J5":0.0,"J6":0.0},
  "source_state_sha256": "...original Run-1 state hash...",
  "transformed_state_sha256": "...",
  "questions_sha256": "...",
  "codebook_sha256": "...",
  "status": "ok",
  "timestamp_utc": "...",
  "usage": {}
}
```

Record failures; do not silently replace a scientific request with an extra attempt.

## Model pinning

Pin `jev-1.13.0` if the API supports it. In all cases record the actual returned model. If Run 3 returns a different model family/version, do **not** interpret changes as ablation effects without also replaying the original semantic Run-1 condition on the new model.

## Do not analyze during acquisition

Do not reveal rule identities, calculate ranks, or inspect 54/110 until all requests have been saved. The primary summary remains the median yes-probability across successful attempts for each alias/question.

## Frozen interpretation

Compare Run 3 against both completed runs question-by-question, especially J4/J5.

- If Run 3 closely reproduces Run 1: operational measurement meaning is sufficient; evocative field names are unnecessary.
- If Run 3 collapses toward the generic opaque behavior: the Run-1 semantic effect depended substantially on lexical/semantic surface cues not preserved by operational definitions alone.
- If Run 3 is intermediate: both operational semantics and the original naming/frame contribute.

This run does not establish that Jev “understands” cellular automata; it is an ablation of where the semantic signal enters the frozen task.
