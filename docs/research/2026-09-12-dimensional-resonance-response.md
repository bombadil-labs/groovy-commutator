# Transformed homologues do not show a uniform mutual-transparency response — 2026-09-12

**Evidence:** exact within the frozen finite source family and horizons.  
**Program:** *Dimensional Closure and the Commutator Lift*.  
**Authored by:** OpenAI GPT-5.6 Sol. **Reviewed by:** pending independent Gate 2 on gathering PR #173.

## Question and answer

Does the already-accepted touching Rule90 strip interaction respond in a uniformly “mutual-transparency” direction when the two logical sources are nonliteral transformed homologues, compared with nonhomologous pairs matched on cheap source statistics?

**No under the frozen primary test.** On the primary ring-7 census, the strict transformed-homologue response predicate fails at every genuinely dynamical horizon `k=2,3,4` (and also at the predecessor-control horizon `k=1`). The failure is not that every response contrast vanishes: residual mass and vertical-span contrasts vary across matched classes, but their signs disagree from class to class, while validity and return contrasts are zero throughout. The predeclared requirement that every scored class move weakly in the mutual-transparency direction is therefore not met.

This is a negative result for one operational response hypothesis, not evidence that every homology-sensitive statistic is absent.

## Frozen setup

The governing protocol stack is:

- `protocols/dimensional-resonance-response-20260912.md`;
- `protocols/dimensional-resonance-response-gate1-refreeze-20260912.md`;
- `protocols/dimensional-resonance-response-gate1-null-clarification-20260912.md`;
- `protocols/dimensional-resonance-response-gate1-approval-20260912.md`.

Independent Claude/Fable Gate 1 approved exact protocol head `15787fa8a2671f899e1d974aff8753386e423cfc` before implementation. Source-only implementation #196 and physical-verifier implementation #204 were integrated with no physical-response result before evaluation. Canonical evaluation #207 used the unchanged pinned verifier and produced `results/dimensional_resonance_response_20260912.json`.

The physical substrate is the accepted touching adjacent Rule90-strip construction on logical rings `n in {6,7}`. The primary relation is nonliteral cyclic-shift/reflected-shift homology. Controls are exact descriptor matches on source weights, transition counts, Hamming distance and XOR transition count. Ring 7 has 18 scored classes containing 532 homologous and 588 matched-control ordered pairs. Ring 6 has two classes with 24/24 pairs and is retained as a small-family control, not as the primary bet.

At horizon `k`, the response is measured on the exact finite causal window using:

- `V_k`: whole-field validity relative to the independent re-encoded baseline;
- `M_k`: residual Hamming mass;
- `S_k`: inclusive vertical residual span;
- `R_k`: return-by-horizon after an earlier invalid horizon.

Positive matched contrasts are defined in the predeclared **mutual-transparency** direction: homologues preserve/return more often or create less residual mass/span. A ring/horizon strict-passes only when every scored class has all four contrasts nonnegative and at least one class is strict in at least one component.

## Controls

All implementation/provenance controls pass.

- The exact touching-strip predecessor table reproduces **17/64** locally valid six-bit words.
- Exhaustive `k=1` physical validity and residual mass agree with that predecessor table.
- Packed and independent scalar physical-response paths agree for every scored and descriptive pair.
- The source census exactly reproduces the Gate-1 freeze: ring 6 has 2 classes / 24 homologues / 24 controls; ring 7 has 18 classes / 532 homologues / 588 controls.
- Every positive `R_k` witness independently replays an earlier invalid horizon followed by a valid horizon; frozen R5 therefore passes.

The canonical result records SHA-256 hashes of the verifier and protocol/source inputs, and the fast source-integrity tier passes on the exact evaluation head.

## Primary ring-7 result

The strict primary predicate is false at every horizon:

| horizon | strict primary predicate | pair-weighted `DeltaM` | pair-weighted `DeltaS` | `DeltaV` pattern | `DeltaR` pattern |
| --- | --- | ---: | ---: | --- | --- |
| `k=1` | false | `263/798` | `0` | all classes zero | all classes zero |
| `k=2` | false | `-187/266` | `61/798` | all classes zero | all classes zero |
| `k=3` | false | `30/133` | `22/399` | all classes zero | all classes zero |
| `k=4` | false | `21/19` | `25/798` | all classes zero | all classes zero |

Thus frozen **R2 is false**: `R2_dynamic_strict_pass_horizons = []`.

The pair-weighted averages alone hide the decisive structure. Per-class signs are mixed:

- `k=2`: mass has 10 negative / 8 positive classes; span has 7 negative / 7 positive / 4 zero.
- `k=3`: mass has 7 negative / 11 positive; span has 8 negative / 7 positive / 3 zero.
- `k=4`: mass splits 9 negative / 9 positive; span has 8 negative / 7 positive / 3 zero.

Validity and return contrasts are zero in every scored ring-7 class at every horizon. The primary hypothesis therefore fails because the transformed relation does not induce a uniform response direction across matched source classes under these observables.

The frozen tag splits also expose heterogeneity rather than one hidden aggregate effect. For example, at `k=2` the “both” cohort has positive mass/span contrasts while reflection-only has negative mass/span contrasts; at `k=4` their mass signs reverse. No sign agreement among shift/reflection tags was predeclared, and none is inferred post hoc.

## Placebo and small-ring controls

Frozen R4 is **not applicable**, because its antecedent is an actual ring-7 strict pass and no such pass occurs. Descriptively, all 503 distinct joint-shift-orbit-preserving placebo label assignments also have zero strict passes at every horizon. That fact does not rescue R2 or convert the negative primary result into positive selectivity evidence.

Ring 6 strict-passes at `k=4`, with pair-weighted `DeltaM=1/2`, `DeltaS=7/4`, and zero validity/return contrasts. This was explicitly frozen as a small-family control with only two scored classes and overlapping shift/reflection symmetries. It is not promoted over the predeclared ring-7 primary test.

The independent scalar replay finds two return witnesses, both ring-6 literal-self descriptive pairs (`010101/010101` and `101010/101010`) that are invalid and then valid again by horizon 2. Ring 7 has no return witness in the scored/descriptive replay.

## What changed in the working account

This experiment rules out a simple version of the proposed resonance criterion: **nonliteral structural homology does not, by itself, produce a uniform matched mutual-transparency response in this finite touching-strip system.** The result is useful precisely because the protocol exposed class-level and transform-tag heterogeneity instead of allowing a favorable aggregate mean to stand in for a general response.

A later experiment could ask a different preregistered question—for example whether some response statistic is transform-specific rather than uniform, whether another fixed interaction law supports a cleaner effect, or whether a response can be transported through an actual dimensional lift. Those are new protocols, not rescues of this one.

## Limits and non-claims

The exact domain is the exhaustive finite `n=6,7` touching-strip source family, horizons `k=1..4`, the frozen source matching, causal window, observables and sign convention. Reflection is an analyst-supplied homology transform, not a physical symmetry of the substrate. The result does not establish absence of every possible self-similarity-sensitive observable or interaction architecture.

Nothing here establishes consciousness, phenomenology, semantic self-recognition, autonomous discovery of homology, endogenous control, self-assembly, intrinsic dimension, recursive Turtle-Beam resonance, spacetime/physics, metaphysics, Class IV, universality, renormalization, or any prime/`8n+1` relation.
