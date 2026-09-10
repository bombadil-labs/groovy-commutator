# Find the dimensional lift operator

**Current scope, 2026-09-09.** The user clarified that Class IV is background
intuition and must not motivate reasoning. The historical class-selectivity
proposals below are retained as history, not current requirements. Success
across an entire declared family is useful; a failure applies to the tested
architecture and may admit an explicit rescue. The
[spatial Rail checkpoint](2026-09-09-spatial-rail-programs.md) now supplies a
recursive stored-program witness under explicit five-symbol, radius-nine
budgets. The current constructive target is locally editable wrapper
instructions, as stated in the [living Program](2026-09-09-dimensional-closure-program.md).

The dimensional-closure thread now has a sharper research target than “find an encoding that works for an interesting rule.”

> **Find a rule-independent dimensional lift operator, if one exists.**

The operator must be fixed without reference to Wolfram class labels or to the identity of the rule being lifted. The only rule-dependent input is the rule itself.

## The object we want

Let `R_d` denote a declared family of native rules in dimension `d`. A candidate lift is a partial map

\[
L_d : R_d \rightharpoonup R_{d+1}.
\]

Partiality is important. If every lower-dimensional rule can be sent to an arbitrary higher-dimensional simulator, liftability is architectural and cannot discriminate anything. The interesting possibility is that one fixed geometric recipe is well defined on every source rule but lands back inside the declared native rule family only for some of them.

The strongest desired structure is a dimension-uniform family

\[
L_1,L_2,L_3,\ldots
\]

built by the same recipe, so that whenever the output remains native the operation can be repeated:

\[
R_1 \xrightarrow{L_1} R_2 \xrightarrow{L_2} R_3 \xrightarrow{L_3} \cdots.
\]

The immediate practical target is an exact `1D -> 2D -> 3D` witness under one frozen recipe.

## Separate the three parts of a lift

A useful candidate operator should make three maps explicit:

1. **Spatialization `S_d`** — place the lower-dimensional rule representation into the boundary or transverse storage cells of a `(d+1)`-dimensional neighborhood.
2. **Induction `I_{d+1}`** — use a fixed local addressing/update mechanism to turn that spatialized object plus a local input into a higher-dimensional local input/output relation.
3. **Native decoding `N_{d+1}`** — determine whether that induced relation has a representation in the declared `(d+1)`-dimensional native rule language, without carrying the lower-dimensional table or an external decoder as hidden state.

Then

\[
L_d = N_{d+1}\circ I_{d+1}\circ S_d
\]

where the composition is undefined when native decoding fails.

This decomposition prevents a common trivialization. The existing eight-bit selector always defines *some* fixed 2D Boolean local rule, but that alone does not give recursive dimensional closure. The question is whether the induced relation can be represented natively in a rule language to which the same lift recipe applies again.

## “Across rules” means the operator is rule-blind

A valid candidate may not choose its geometry or decoder separately for each source rule. In particular:

- the rule-entry ordering is fixed, or a complete preregistered symmetry-reduced family is evaluated;
- address axes, bit significance, transverse directions, and layer ordering are fixed by the operator definition rather than by the source rule;
- rotations/reflections that conjugate the complete construction are coordinate equivalences, not independent evidence;
- no class label, known glider behavior, universality fact, or favored rule number is available to the operator.

If several spatializations are genuinely admissible, write the lift as `L_d^sigma` for `sigma` in a frozen family `Sigma_d`, and study the whole family. The rule-level questions can then be existential, universal, fractional, or based on recursive depth, but `sigma` cannot be selected post hoc to flatter a particular rule.

## Structural constraints that could identify the operator

Rather than search arbitrary decoders, prefer candidate lifts satisfying rule-independent constraints:

1. **Locality.** The lift uses one bounded neighborhood and no trajectory-specific history.
2. **Naturality under lattice symmetry.** Rotating or reflecting the source construction and then lifting gives the correspondingly transformed lifted rule.
3. **Rule conjugacy compatibility.** State-complement/reflection conjugacies should transform predictably rather than being broken by a numbering convention.
4. **Dimension-uniform syntax.** The same addressing/storage recipe is meaningful at `d`, `d+1`, and `d+2`.
5. **No hidden program channel.** Everything needed to apply and relift the rule is represented in the declared native object.
6. **Nontrivial native closure.** Merely expanding an induced Boolean function into its unrestricted full truth table does not count if that representation cannot itself be spatialized by the same bounded recipe.

These conditions may shrink the apparent freedom in `Sigma_d` enough to reveal a canonical operator, a small finite operator family, or an impossibility theorem.

## Why the rule language matters

For unrestricted binary radius-one rules, truth-table size grows too fast for the naive boundary-storage recurrence. A 1D ECA has eight output bits and happens to fit around a `3x3` ring, but an unrestricted 2D Moore rule has 512 truth-table bits, far more than the 26 cells of a `3x3x3` shell.

Therefore a recursively closed lift cannot simply mean “store the unrestricted truth table on the next shell” at every dimension. At least one of the following must be true:

- the native rule family is a compressed structural language rather than all possible truth tables;
- the spatial rule representation uses blocks, channels, staged updates, or another bounded architecture;
- recursive closure exists only on a selective subset whose induced rules admit unusually compact native descriptions;
- no such dimension-uniform lift exists under the declared budgets.

The third possibility is exactly where the Class-IV conjecture could become interesting: the same operator is presented with every source rule, but only a selective subset remains representable after promotion.

## The Class-IV hypothesis in operator form

Once a candidate `L` is frozen without labels, the optimistic hypothesis becomes much sharper:

\[
\operatorname{Dom}(L_1)\text{ or }\operatorname{Dom}(L_2L_1)\text{ or recursive closure depth}
\]

might coincide with, or be strongly enriched for, independently assigned Class-IV rules.

The strongest dream is not “we found a clever 2D picture of Rule 110.” It is:

> **One simple dimensional operator applies to the whole rule space, and the rules that remain native under repeated application are exactly the Class-IV rules.**

That is a falsifiable structural claim.

## Concrete research program

1. **Derive candidate operators from geometry before rule outcomes.** Start from the existing Moore-ring and layered constructions, but impose the structural constraints above.
2. **Classify genuine spatialization freedom.** Quotient complete coordinate conjugacies and keep only physically distinct choices.
3. **Define the next-dimensional native rule language before evaluation.** Avoid a decoder that is fitted separately to each induced function.
4. **Apply each frozen operator to all 256 ECAs.** Record success/failure and failure mode without class labels.
5. **Attempt a second lift wherever the first succeeds.** A `1D -> 2D` success that cannot even be typed as input to `L_2` is not recursive closure.
6. **Only then attach class labels.** Exact exclusivity, enrichment, or total failure are all publishable outcomes.

## What would count as progress before finding `L`

A useful result need not immediately produce the operator. Any of these would substantially narrow the search:

- a proof that symmetry/naturality forces only a small set of spatializations;
- a minimal native rule language closed under one known lift;
- an impossibility result for unrestricted truth-table shell storage;
- a finite exhaustive catalog of rule-blind lift schemes under a declared local budget;
- a proof that no nontrivial recursive operator exists within the Moore-ring architecture.

The research target is therefore now operator discovery, not class fitting. The Class-IV conjecture is downstream of that target.