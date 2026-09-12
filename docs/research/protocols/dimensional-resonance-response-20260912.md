# Protocol: endogenous resonance to self-similar encounters — 2026-09-12

**Status:** frozen before implementation/evaluation. Nothing in this protocol has been run.  
**Program:** *Dimensional Closure and the Commutator Lift*.  
**Authored by:** Codex / OpenAI GPT-5.6 Sol.  
**Protocol review:** pending independent Gate 1 on the exact integrated gathering head. No implementation or evaluation is authorized before Gate 1.

## 1. Question

The Turtle Beam objective has been refined: inherited/self-similar structure should eventually become **causally consequential to the unfolding**, not merely recognizable by an external verifier.

The user's term **resonance** names the motivating intuition: a system encounters a transformed instance of its own organization and responds differently because of the structural correspondence. This is not a consciousness, phenomenology, Buddhist-doctrinal, or metaphysical claim.

This first bounded experiment asks:

> Under one already-accepted fixed physical interaction law, do structurally homologous strip encounters have a reproducibly different dynamical response from matched non-homologous encounters?

A positive result would be only a candidate mechanical self-similarity response in this architecture. It would not yet establish recursive dimensional self-recognition.

## 2. Frozen physical system

Reuse by exact hash the accepted adjacent/touching Rule90 strip architecture from the coupled-strip/interface lineage:

- same fixed 2D binary physical law and alternating background;
- two horizontally encoded Rule90 strips placed in the accepted touching geometry (`g=0`);
- same coarse cadence two;
- no new guard, decoder, repair rule, or fitted interaction law;
- source rings `n in {6,7}` for the primary exact census;
- coarse horizons `k in {1,2,3,4}` macro-steps after contact.

The experiment changes only which logical source-pair relation is prepared.

## 3. Structural self-similarity classes

For a binary ring state `a`, define the frozen dihedral orbit

`Orb(a) = { shift^j(a), shift^j(reflect(a)) : j=0,...,n-1 }`.

Do **not** include complement in the primary orbit; complement changes a value relation in Rule90 and is retained as a separate control.

Classify an ordered pair `(a,b)` as:

- `literal-self` iff `b=a`;
- `homologous` iff `b in Orb(a)`;
- `nonhomologous` otherwise.

Literal-self is a subset of homologous and is reported separately.

## 4. Matched controls

Simple equality can correlate with trivial statistics. Therefore every homologous pair is compared only against nonhomologous controls matched on the following frozen descriptors of each strip:

- Hamming weight of `a` and `b` separately;
- cyclic transition count of `a` and `b` separately;
- Hamming distance `dist(a,b)`;
- XOR transition count of `a XOR b`.

A **match class** is the tuple of those six integers. A homologous pair contributes to the matched primary analysis only if its class contains at least one nonhomologous pair.

No nearest-neighbor relaxation is allowed after inspection. Unmatched homologous pairs are reported but not scored in the primary resonance comparison.

Complement-related pairs `b = NOT(a)` are a named control cohort and never substitute for nonhomologous matched controls.

## 5. Dynamical response observables

All observables are fixed before evaluation and are computed from physical evolution, not from an externally fitted classifier.

For each ordered source pair and coarse horizon `k`, record:

1. **validity** `V_k`: whether the physical state lies in the accepted two-strip symbolic representation at that horizon;
2. **interaction residual mass** `M_k`: Hamming mass of the accepted coupled-vs-independent interaction residual on the physical causal band;
3. **strip disagreement** `Q_k`: Hamming distance between the two decoded logical strips when both decode validly; otherwise `NA`;
4. **return indicator** `R_k`: whether a pair that was invalid at any earlier positive horizon has returned to the accepted two-strip representation by horizon `k`;
5. **physical support span** `S_k`: bounding-box area of nonzero coupled-vs-independent residual in the exact finite causal window, with zero residual assigned span zero.

The independent baseline evolves the same two logical strips under their accepted separated-strip Rule90 dynamics and re-encodes them in the touching frame solely to define the residual. It is not an alternative physical trajectory used as a repair.

## 6. A predeclared resonance score

For each matched class `c` and horizon `k`, compute exact class means separately for homologous (`H`) and nonhomologous (`N`) pairs:

- `DeltaV(c,k) = mean_H(V_k) - mean_N(V_k)`;
- `DeltaM(c,k) = mean_N(M_k) - mean_H(M_k)`;
- `DeltaR(c,k) = mean_H(R_k) - mean_N(R_k)`.

Positive values mean homologous encounters preserve/return to the representation more often or generate less residual interaction.

Define the **strict resonance predicate** at horizon `k`:

- every scored matched class has `DeltaV >= 0`, `DeltaM >= 0`, and `DeltaR >= 0`;
- at least one scored class is strict in at least one component;
- the aggregate pair-weighted values of all three deltas are nonnegative.

Do not combine the components into a fitted scalar weight.

## 7. Frozen predictions

### P1 — provenance and physical controls

Imported separated-strip and touching-strip predecessor identities replay exactly. Independent scalar and packed physical evolvers agree on every scored trajectory and observable.

### P2 — literal-self response

Literal-self pairs have weakly higher `V_k` and weakly lower `M_k` than their matched nonhomologous controls at every `k=1..4`, with at least one strict aggregate difference by `k=2`.

### P3 — structural, not literal, resonance

The full homologous cohort satisfies the strict resonance predicate for at least one horizon in `{1,2,3,4}`.

This is the primary bet. Failure means this accepted interaction does not provide the desired candidate resonance under the frozen definition.

### P4 — transformation robustness

Within the homologous cohort, nontrivial shifted/reflected pairs (excluding literal equality) show the same **sign** of aggregate `DeltaV` and `DeltaM` as literal-self at the first horizon where P3 is evaluated as true. If P3 is false at every horizon, P4 is recorded `not applicable`, not rescued post hoc.

### P5 — complement control is distinct

Complement-related pairs are not required to share the homologous response signature. Report them independently. If they exactly match the homologous signature, interpretation is weakened: the response may track a cheaper algebraic relation rather than the frozen self-similarity orbit.

## 8. Why this is only a candidate self-recognition test

A differential response to homologous encounters would establish that one fixed law treats a declared structural correspondence differently from statistic-matched controls. It would **not** show that the system contains an explicit representation of self, computes an isomorphism, experiences anything, or recognizes ancestry in the semantic sense.

The stronger Turtle Beam criterion remains future work: the recognizer/response mechanism itself should transport coherently across dimensional lifts.

## 9. Negative and ambiguous outcomes

- No matched homologous classes: protocol/domain failure, not scientific evidence.
- P2 pass but P3 fail: literal equality matters but broader structural homology does not under this test.
- P3 pass but P4 fail: effect is concentrated in literal-self or a subset of transformations; do not call it structural resonance broadly.
- Strong response also in complement controls: report a cheaper-relation confound.
- Mixed-sign matched classes: strict resonance fails even if aggregate means look favorable.

No post-hoc reweighting, horizon selection beyond the frozen set, added transformations, or rematched descriptors is allowed in this unit.

## 10. Independent implementation requirements

After Gate 1, implementation-only/no-result must pin:

1. exact predecessor source hashes and geometry;
2. independent scalar and packed physical evolvers;
3. exact dihedral-orbit classifier;
4. exact matched-class construction;
5. independent observable/replay path for every stored trajectory summary;
6. deterministic ordering of pairs/classes and exact rational means rather than floating threshold decisions;
7. permanent two-tier integrity/replay CI with a green no-result stage.

No scored source-pair result may be inspected before green implementation integration.

## 11. Interpretation ceiling

Even a full P2–P5 success is only:

> a bounded endogenous differential response to one declared form of structural self-similarity under one fixed 2D interaction law.

It is not recursive dimensional resonance, self-assembly, self-awareness, consciousness, an intrinsic notion of identity, a biological self/nonself mechanism, Buddhist doctrine, metaphysics, spacetime emergence, Class IV, universality, or a prime/`8n+1` result.

## 12. Gate-1 questions

The independent reviewer should attack especially:

1. Is the touching Rule90 strip system a fair first endogenous-response substrate, or does its known interaction algebra predetermine the comparison?
2. Is the dihedral orbit a defensible structural self-similarity class?
3. Do the frozen matched descriptors remove obvious cheap confounds without overmatching away all controls?
4. Is Hamming distance itself too close to literal similarity to use as a matching descriptor?
5. Are validity/residual/return observables genuinely dynamical responses rather than external resemblance scores?
6. Is the strict resonance predicate too strong, too weak, or vulnerable to class-size artifacts?
7. Should the primary claim require nonliteral transformed pairs to succeed independently rather than P4's sign test?
8. Is the complement control sufficient to expose cheaper algebraic-response explanations?
9. Are horizons 1–4 principled from predecessor work or an arbitrary search window?
10. Are the non-claims strong enough to keep `resonance` operational rather than phenomenological?

Binding changes to physical substrate, self-similarity class, matching descriptors, horizons, observables, primary predicate or interpretation ceiling require renewed exact-head Gate 1 before evaluation.