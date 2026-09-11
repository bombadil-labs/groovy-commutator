# Invariants Across Representation Contracts

This page is the **working synthesis** of a third research program, opened on 2026-09-10 after the review conversation recorded in issues #61–#68. It is not a chronological note and it claims no result of its own yet. It records the question, the objects the question is about, what the existing record already says, and the first frozen protocol.

Authored by: Claude Code, Fable 5.1. Reviewed by: none (opened at the user's request while Codex was inactive; the first protocol is the first thing to review).

The thesis is:

> **A represented dynamics has properties that belong to the dynamics and properties that belong to the interpreter. The program asks which is which, by declaring the admissible changes of interpreter, what each one transports, and what each one costs.**

## Why a third program

The two living Programs meet at one object. [Dynamics of Erased Distinctions](2026-09-08-dynamics-of-erased-distinctions.md) asks which distinctions a representation may forget; [Dimensional Closure and the Commutator Lift](2026-09-09-dimensional-closure-program.md) asks what must be added when evolution and transformation disagree. Both keep the [representation contract](../knowledge/representation-contract.md): law, state family, and interpreter stated together.

Two results on 2026-09-10 showed that the contract has teeth the record had not yet used:

- The [rule-field relabeling note](2026-09-10-rule-field-relabeling.md) exhibits an exact local symmetry of rule-field systems. A uniform rule is a nonuniform field in another labeling, and the transport rule must transform with the decoder or decoded dynamics change. The quiescence-selection statistic of established result 8 is not invariant under it.
- The [second-lift completion protocol](2026-09-10-second-lift-completion-protocol.md) records a theorem-backed fact: on a shared invariant family, changing the ambient completion is an invertible local recoding of the correction coordinates. Retained information and factor existence at fixed depth cannot depend on the completion; local coordinates and cap radius can.

Both say the same thing from different sides. A statement about a represented dynamics is only a statement about the dynamics if it survives the admissible re-interpretations, and "survives" has to be made precise: preserved outright, preserved after transporting some companion object, or changed in a way that is a real physical cost.

The first counterexample was found during review before any protocol existed. Swapping the symbols 0 and 1 conjugates Rule 0 to Rule 255. Under the repository's definition, `G ≡ 0` for Rule 0 and `G ≡ 1` for Rule 255. So "the commutator of an affine rule is its bias" (established result 1) is correct, and the bias is not invariant under the simplest relabeling. The reason is that the derivative `D = 𝟙 ⊕ F` is a difference, invariant under relabeling, while `F` is a map on labeled states; feeding one into the other mixes two conventions. Whether the commutator is invariant depends on what is transported with the dynamics. That is the shape of every question in this program.

## The objects

- **A represented dynamics** is a tuple `(lattice, alphabet, family B, law F, observation P, cadence q, completion H, costs)`, as the second-lift protocol types it.
- **An admissible transformation** `T` acts on some of those components and is declared with three things: which components it transports and how; whether it is invertible on the family; and its cost in touched sites, information, and locality. Transformations are not assumed to form one group. Relabelings, reflections, completions agreeing on a family, and invertible local recodings with a locality budget are different operations with different reach.
- **A property** `Π` of a represented dynamics is classified relative to `T` as **preserved** (`Π(T·) = Π(·)`), **covariant** (`Π(T·) = T_Π(Π(·))` for a declared transport `T_Π` of the property's value), or **changed**. A covariant property with an unstated `T_Π` is the usual way a convention gets mistaken for a result.

No single group is assumed, no "intrinsic" invariant is claimed, and invariance under a declared family is not the dimensional beam: a projection may discard, a constant projection discards everything, and classifying invariants leaves organization, repair, and native capability open. Those remain the other Programs' questions.

## What the record already says

| Property | Transformation | Status in the record | Source |
| --- | --- | --- | --- |
| Closure of `(P, F)` | any invertible relabeling of the observation with conjugated update | preserved, by algebra | [vision note](2026-09-10-dimensional-vision-and-interpretation.md), [shared closure account](2026-09-10-shared-closure-account.md) |
| Retained information and factor existence at fixed correction depth | change of completion on a shared invariant family | preserved, by the triangular coordinate theorem | [correction coordinates](2026-09-09-correction-future-coordinates.md), [second-lift protocol](2026-09-10-second-lift-completion-protocol.md) |
| Literal correction maps, cap radius, cap cost | change of completion | changed | same |
| Decoded rule-field dynamics | local Z2 relabeling with covariant transport | preserved | [rule-field relabeling](2026-09-10-rule-field-relabeling.md) |
| Quiescence-selection gradient | local Z2 relabeling | changed (convention-dependent) | same, established result 8 |
| Wrapping-loop parity | replication to a new axis | preserved | [gradient loop invariants](2026-09-10-gradient-loop-invariants.md) |
| Commutator bias of affine rules | global complement conjugation | changed (`c ↦ c ⊕ M𝟙 ⊕ 1`; Rule 0 ↦ Rule 255) | [audit note](2026-09-11-representation-invariants-audit.md) |
| Native commutator field | complement conjugation | covariant iff self-dual; covariant for all rules with the derivative transported as a state | same |
| Commutator class, derivative closure, cap budgets | reflection | preserved | same |
| Local-cap minimum radius, K | complement conjugation | covariant with a bounded radius cost: shift 0, 1 or 2 over the whole census at `R ≤ 4`, never a loss of existence | [extension](2026-09-11-cap-census-complement-extension.md), [shift census](2026-09-11-cap-shift-census.md) |
| Local-cap pass table, O | complement conjugation | preserved at every radius (`B_j = D∘F^j` is a difference) | [shift census](2026-09-11-cap-shift-census.md) |
| Cap radius, K and O | 2-block recoding (forward radius 1, inverse 0) | covariant, cost at most one unit, zero in 665 of 674 cells | [recoding note](2026-09-11-higher-block-recoding.md) |
| Derivative, commutator, derivative closure | 2-block recoding | preserved componentwise (algebra; run is a control) | same |
| Possibility-frontier census summaries | complement, reflection | preserved, by closure of the observer family (deduction) | same |
| Sweep regime labels | reflection, complement | 95% / 94% stable; not an invariance | same |

Nothing in that table is new. The program's first job is to make the table complete and exact for the transformations the repository already uses implicitly.

## First unit: complete

[Representation invariants audit](protocols/representation-invariants-audit-20260910.md), frozen 2026-09-10, run 2026-09-11, reported in the [audit note](2026-09-11-representation-invariants-audit.md). Five of six predictions held. The failed one, a radius bound for the local-cap census under complement conjugation, omitted that the target correction row transforms too; its correction is post hoc and is the next protocol's prediction. Exact findings: the native commutator is complement-covariant iff the rule is self-dual, and transporting the derivative as a state restores covariance for all 256 rules; reflection preserves the commutator classification, derivative closure, and all 4,608 cap budgets; the derivative-closure set is the same 30 rules at rings 6, 8, 10; sweep regime labels are 95% and 94% stable while the raw statistics behind them are under 30% equal. The protocol's original text follows.

The protocol It declares two global transformations of elementary CA (complement conjugation and reflection) and their composite, states what each transports and costs, and audits six existing claims against them with predictions frozen before running: the commutator classification of established result 1, pointwise commutator covariance, derivative-observation closure, the local correction-cap census, and the five-regime pair labels of the full sweep. The last of these is a sampled-seed result and is expected to be only approximately invariant; the protocol says so.

## Second unit: complete

[Cap census complement extension](protocols/cap-census-complement-extension-20260911.md), frozen and run 2026-09-11, reported in the [extension note](2026-09-11-cap-census-complement-extension.md). All four predictions held. The first audit's failure was a budget artifact: every cap the census could not see at `R ≤ 2` exists at radius 3, and complement conjugation costs at most two units of cap radius on these cells. The radius budget is part of the representation contract.

## Third unit: complete

[Cap shift census](protocols/cap-shift-census-20260911.md), frozen and run 2026-09-11, reported in the [shift census note](2026-09-11-cap-shift-census.md). All six predictions held over all 256 rules at `R ≤ 4`: O caps are exactly complement-invariant, K caps shift by at most two, no cap is created or destroyed, reflection is exact. A post-hoc observation: the depth-0 cap set of either kind is exactly the derivative-closure set from the first audit. The global relabelings are now exhausted; the next transformation type is a local recoding with a locality budget or a change of completion.

## Fourth unit: complete

[Higher-block recoding](protocols/higher-block-recoding-20260911.md), frozen and run 2026-09-11, reported in the [recoding note](2026-09-11-higher-block-recoding.md). The first transformation of a local, alphabet-changing type. All four predictions held: cap radius within `[mpr − 1, mpr]` and unchanged in 665 of 674 cells; derivative, commutator and closure preserved componentwise; the Research026 observer family closed under complement and reversal, so that census is covariant by deduction. Remaining undeclared types: change of completion (runs under the second-lift protocol) and non-injective coarse-graining (the Erased Distinctions object).

## What would count as progress

- A property currently listed as "established" that turns out to be changed by an admissible transformation, with the transport that restores it named. That is a correction, not a loss.
- A property preserved under a family of transformations broad enough to serve as an equivalence notion for primitives in the planned learning-and-revising-primitives program, so that a learner cannot count a coordinate change as a discovery.
- A cost accounting that lets the other Programs say "this is representation-dependent, and that dependence is what the system exploits" without confusing it with a claim about the dynamics.

## What is not claimed

No novelty claim: CA simulation and conjugacy theory are standard, and the opening literature comparison will cite CA simulation and communication-complexity obstructions so that the Erlangen-style framing remains a guide. No Class IV claim; Class IV is background only. No intrinsic-dimension, prime-analogy, or metaphysical claim. Every result of this program is scoped to a declared transformation family and a declared property.

## Checkpoints

The program's dated checkpoints are in [`checkpoints/representation-invariants.md`](checkpoints/representation-invariants.md).
