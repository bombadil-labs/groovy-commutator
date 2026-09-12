# Gate-1 refreeze: dimensional resonance response — 2026-09-12

**Status:** superseding protocol-only correction after independent Gate-1 rejection. No implementation/evaluation is authorized until renewed exact-head Gate 1.  
**Program:** *Dimensional Closure and the Commutator Lift*.  
**Parent protocol:** `docs/research/protocols/dimensional-resonance-response-20260912.md`.  
**Rejected head:** `c4d14cc657c61d56850a889032096f9fcffd52c4`.  
**Independent reviewer:** Claude Code / Fable 5.1.  

The physical substrate, ring sizes and horizons remain the accepted touching-Rule90 system. This refreeze replaces the parent matching semantics, primary cohorts, response domains and null calibration before any run.

## 1. Scientific question

Does an already-related, nonliteral structural homologue receive a reproducibly different **physical interaction response** from nonhomologous source pairs matched on cheap source statistics?

`Resonance` remains motivational shorthand only. The scored content is differential validity/residual/return behavior of transformed strip pairs. No consciousness, semantic recognition or phenomenology is claimed.

## 2. Frozen substrate

Retain unchanged:

- accepted touching adjacent Rule90 strips under the same fixed 2D physical law and alternating background;
- logical ring sizes `n in {6,7}`;
- exhaustive ordered source pairs `(a,b)`;
- preparation at coarse time `t=0` with strips already touching;
- scored coarse horizons `k in {1,2,3,4}` after contact;
- independent baseline `V_0(phi90^k(a), phi90^k(b))`.

The `k=1` response is a theorem/tabulation regression against the accepted 17/64 touching-local validity table. Any genuinely new dynamical interpretation is reserved for `k>=2`, when the wake can leave the original four-row band.

## 3. Primary homology relation

Literal self-pairs are **not** part of the matched primary claim because Hamming-distance matching makes them unmatchable by construction. They remain an unmatched descriptive cohort only.

The primary homologous set consists of **nonliteral dihedral transforms**:

`b != a` and `b` is a cyclic shift and/or a reflected cyclic shift of `a`.

For reporting, every homologous pair is tagged as:

- `shift-capable`: `b` is a nontrivial cyclic shift of `a`;
- `reflection-only`: reflection-related but not shift-related;
- `both`: both relations hold.

The aggregate primary cohort is their union. Report shift-capable, reflection-only and both tags separately so reflection cannot hide behind the true shift symmetry of the substrate.

A logical one-site shift is an exact symmetry of law plus period-two background. Reflection is **not** assumed to be a substrate symmetry; it is retained only as a declared structural-homology transform.

## 4. Frozen matched-control descriptors

For each ring separately, assign every ordered nonliteral pair to the exact descriptor class

`C(a,b) = (weight(a), weight(b), transitions(a), transitions(b), Hamming(a,b), transitions(a XOR b))`.

A primary homologous pair is scored only if its class contains at least one nonhomologous pair. All nonhomologous pairs in that same class form its matched-control pool. Classes never pool ring identities.

### Pre-run source-family census

The following census uses **source bits only**; it does not evolve the physical system or inspect any response variable. It is frozen here to expose matching power before evaluation.

For `n=6` there are exactly **2 scored descriptor classes**, each with 12 homologous and 12 nonhomologous controls:

- `(2,2,4,4,4,4)`: 12 / 12;
- `(4,4,4,4,4,4)`: 12 / 12.

All scored `n=6` homologues carry the `both` tag because the small-ring symmetries overlap.

For `n=7` there are exactly **18 scored descriptor classes**, containing **532 homologous pairs** and **588 matched controls** in total. The exact class table is frozen below as `(descriptor : H / C ; shift-capable / reflection-only / both)`:

- `(2,2,4,4,2,2): 14 / 28 ; 0 / 0 / 14`
- `(2,2,4,4,2,4): 14 / 28 ; 0 / 0 / 14`
- `(2,2,4,4,4,4): 14 / 42 ; 0 / 0 / 14`
- `(3,3,4,4,2,2): 14 / 28 ; 0 / 14 / 0`
- `(3,3,4,4,2,4): 42 / 56 ; 0 / 28 / 14`
- `(3,3,4,4,4,2): 14 / 28 ; 0 / 14 / 0`
- `(3,3,4,4,4,4): 98 / 28 ; 84 / 14 / 0`
- `(3,3,4,4,4,6): 28 / 28 ; 0 / 14 / 14`
- `(3,3,4,4,6,2): 28 / 28 ; 0 / 14 / 14`
- `(4,4,4,4,2,2): 14 / 28 ; 0 / 14 / 0`
- `(4,4,4,4,2,4): 42 / 56 ; 0 / 28 / 14`
- `(4,4,4,4,4,2): 14 / 28 ; 0 / 14 / 0`
- `(4,4,4,4,4,4): 98 / 28 ; 84 / 14 / 0`
- `(4,4,4,4,4,6): 28 / 28 ; 0 / 14 / 14`
- `(4,4,4,4,6,2): 28 / 28 ; 0 / 14 / 14`
- `(5,5,4,4,2,2): 14 / 28 ; 0 / 0 / 14`
- `(5,5,4,4,2,4): 14 / 28 ; 0 / 0 / 14`
- `(5,5,4,4,4,4): 14 / 42 ; 0 / 0 / 14`.

Any implementation mismatch with this source-only census blocks evaluation.

## 5. Exact physical response domain

At coarse horizon `k`, compare the physical state after `2k` fine ticks to the independent re-encoded baseline on the **same exact finite causal window**:

- all `2n` horizontal ring columns;
- vertical rows `[-2k, 3+2k]` relative to the prepared rows `0..3`.

Radius-one finite propagation guarantees the physical field outside this window remains the corresponding background, so no response mass is silently discarded.

Pin all response variables to this common window.

## 6. Frozen response variables

For each ordered pair and horizon:

1. **Validity `V_k`**: 1 iff the complete physical field equals `V_0(phi90^k(a), phi90^k(b))` on the exact causal window, hence everywhere by the finite-propagation background guarantee.
2. **Residual mass `M_k`**: Hamming mass of physical XOR residual relative to that independent baseline on the exact causal window.
3. **Residual span `S_k`**: vertical span of nonzero residual cells within the same window, with 0 for empty residual.
4. **Return-by-horizon `R_k`**: 1 iff there exist `1 <= u < v <= k` with `V_u=0` and `V_v=1`. This is monotone in `k` and is identically zero at `k=1`.

The sign convention is **mutual transparency**: a homologous pair is called resonance-like when it tends to preserve the declared representation more, produce less residual mass/span, or return after departure more often than its matched controls. This is one operational convention, not the definition of resonance in general.

## 7. Per-class contrasts and pair-weighted aggregates

For each scored descriptor class `c`, ring and horizon, compute class means over homologous pairs and matched controls with each ordered pair weighted equally:

- `DeltaV(c,k) = mean_H(V_k) - mean_C(V_k)`;
- `DeltaR(c,k) = mean_H(R_k) - mean_C(R_k)`;
- `DeltaM(c,k) = mean_C(M_k) - mean_H(M_k)`;
- `DeltaS(c,k) = mean_C(S_k) - mean_H(S_k)`.

Positive values therefore point in the mutual-transparency direction.

Also report pair-weighted global contrasts per ring/horizon by averaging directly over all scored homologous pairs and all scored controls, **not** by giving each descriptor class equal weight.

Per-class sign counts `positive / zero / negative` must be reported for every component and horizon.

## 8. Primary predicate

A ring/horizon satisfies the strict primary predicate iff:

- every scored descriptor class has `DeltaV >= 0`, `DeltaM >= 0`, `DeltaS >= 0`, and `DeltaR >= 0`; and
- at least one class is strict in at least one component.

Because this predicate is deliberately brittle, a failure is reported as a pattern of per-class signs rather than as absence of all differential response.

The primary bet is restricted to the **nonliteral transformed-homologue cohort**. Literal-self pairs are descriptive only and cannot supply the sign reference for the primary claim.

## 9. Frozen placebo/null calibration

Within each scored descriptor class, order all pairs lexicographically by `(a,b)` and form the binary label vector marking the actual homologous subset. Construct placebo labelings by every **distinct nontrivial cyclic rotation** of that label vector, preserving exactly the homologous/control counts and every matched descriptor.

For each placebo labeling, recompute the same class contrasts and strict predicate. Across the ring, use rotation index `r` simultaneously in every class after reducing `r` modulo that class's label length; deduplicate identical global placebo label assignments.

Report, for every horizon:

- number of distinct placebo assignments;
- fraction satisfying the strict predicate;
- actual predicate verdict and its rank relative to the placebo distribution for each pair-weighted contrast.

This is a deterministic matched-label placebo, not a probabilistic p-value and not evidence of semantic recognition.

## 10. Complement control sharpened

For the descriptive complement cohort `(a, NOT a)`, use the exact Rule90 identity

`phi90(NOT a) = phi90(a)`.

Thus the independent baseline becomes literal-self after one step even though the source-time pair is maximally Hamming-distant. Report the same physical response variables for this cohort without forcing it into the primary descriptor matching.

Frozen interpretation fork:

- if complement response rapidly approaches the literal-self descriptive profile after `k>=1`, the observable is tracking **baseline-trajectory convergence** more than source-time homology;
- if it remains distinct while transformed homologues show the primary signature, source-time structural relation remains a live explanation within this finite substrate;
- either outcome is descriptive and does not establish semantic self/nonself recognition.

No directional bet is imposed on this control before evaluation.

## 11. Frozen predictions

### R1 — provenance and `k=1` theorem control

The implementation exactly reproduces the accepted 17/64 one-update validity table and residual formulas. `k=1` is reported as a deterministic predecessor consequence, not a new emergence result.

### R2 — transformed-homologue differential response

At least one of the genuinely dynamical horizons `k in {2,3,4}` satisfies the strict primary predicate on ring 7.

Ring 6 is retained as an exact small-family control but is not part of this primary bet because it has only two scored classes and overlapping shift/reflection symmetries.

### R3 — symmetry split

Report shift-capable, reflection-only and both-tagged homologues separately. No sign agreement between them is predeclared. A reflection-only disagreement cannot be averaged away inside the primary report.

### R4 — placebo selectivity

At any horizon where the actual ring-7 strict predicate passes, fewer than 10% of distinct placebo labelings also pass it. This threshold is frozen before physical evaluation.

### R5 — return is genuinely post-departure

Any positive `R_k` witness must replay a prior horizon with `V=0` and a later horizon with `V=1` under the exact whole-field validity definition. Failure blocks the return statistic.

## 12. Independent implementation requirements

Before evaluation, implementation-only/no-result must pin:

- two independent physical-evolution paths already available in the touching-strip lineage;
- exact source-only matching-census replay above;
- whole-field validity and common-window residual calculations;
- deterministic placebo-label construction;
- independent scalar replay for every reported strict/negative class boundary and every return witness;
- canonical ordering of pairs/classes/witnesses;
- permanent two-tier result integrity/replay with a green no-result stage.

No physical response result may be inspected before that stage is green and integrated.

## 13. Interpretation ceiling

Even a full R2/R4 pass establishes only differential physical response to a declared transformed-homology relation in this finite touching-strip substrate under matched source statistics.

Do **not** report it as consciousness, phenomenology, semantic self-recognition, Buddhist doctrine, intrinsic dimension, self-assembly, endogenous control, general free-lunch behavior, recursive Turtle-Beam resonance, physics/metaphysics, Class IV, universality, spacetime emergence, or any prime/`8n+1` claim.

The substrate is 2D and the homology transform is supplied by the analyst. Whether such a response itself transports across dimensional lifts is a separate future protocol.

## 14. Renewed Gate-1 questions

The independent reviewer should verify especially:

1. Does the source-only matched-class census reproduce exactly and provide enough ring-7 support for the frozen predicate?
2. Is the nonliteral dihedral relation defensible once shift-capable/reflection-only/both cohorts are exposed separately?
3. Are the exact causal window and V/M/S/R definitions unambiguous and physically complete?
4. Is the cyclic-label placebo a fair deterministic calibration or can lexicographic ordering manufacture selectivity?
5. Is the ring-7 R2 bet genuinely open beyond the known `k=1` table?
6. Is the 10% R4 threshold meaningful enough to retain, or should it be struck before implementation?
7. Does the complement fork correctly exploit `phi90(NOT a)=phi90(a)` without smuggling in a directional prediction?
8. Are the nonclaims strong enough that a positive differential response cannot be reported as consciousness or semantic self-recognition?

This refreeze materially changes matching semantics, cohorts, response definitions, null calibration and predictions. **Renewed exact-head Gate 1 is required.**