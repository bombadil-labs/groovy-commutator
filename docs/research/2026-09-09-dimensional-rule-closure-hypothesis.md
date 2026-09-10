# Dimensional rule closure: the Class-IV hypothesis

This note records a deliberately strong conjecture before the dimensional-closure operator is finalized:

> **Perhaps Wolfram Class IV, and only Class IV, consists of rules whose rule table can be promoted into the next spatial dimension by the project's existing rule-as-geometry construction and there become a native rule that can itself be promoted again.**

The claim is intentionally optimistic. It is not currently supported by evidence.

## Why the conjecture is interesting

The project already has two exact rule-as-geometry facts.

An unrestricted elementary cellular automaton has eight truth-table output bits. Those eight bits fit exactly on the eight-cell ring around the center of a 3x3 Moore neighborhood. The existing selector construction uses a three-bit line through the center as an address and reads the corresponding ring cell as the output bit.

A separate dimensional construction works for binary outer-totalistic radius-one Moore rules. A d-dimensional neighborhood has `M=3^d` cells and such a rule has `2M` output bits. In d+1 dimensions, the two outer `M`-cell layers hold exactly those `2M` rule bits while the middle layer holds the lower-dimensional input neighborhood.

Both constructions make a lower-dimensional rule literal spatial data one dimension higher. Neither yet establishes a recursively closed dimensional ladder.

## The distinction that matters

The previous `dimensional-intertwining` branch answered a different and much easier question: whether a 1D CA can be embedded as an invariant subsystem of some 2D CA. It can, very generally. That result is retained as a side result but is not evidence for the present conjecture.

Here the higher-dimensional rule must arise from the **specific spatialized rule representation itself**. We do not get to invent an arbitrary simulator after seeing the lower-dimensional rule.

The desired shape is

```
R_1 --spatialize--> geometric object in 2D --decode natively--> R_2
 |                                                        |
 evolve                                                   spatialize
 |                                                        |
 v                                                        v
...                                                     3D object
```

and, in the strongest form, the promotion should continue:

`R_1 -> R_2 -> R_3 -> ...`.

The open technical problem is to define the middle `decode natively` arrow canonically enough that it is not merely another externally supplied interpreter.

## Spatialization is a family, not a single map

There is not one canonical way for a rule table to become space. The spatialization itself has degrees of freedom, and the earlier selector census already showed that changing the truth-table-entry-to-position assignment can change the induced dynamics.

For the unrestricted ECA Moore-ring lift, let `sigma` denote a bijection from the eight truth-table addresses to the eight surrounding cells. There are

`8! = 40,320`

labeled assignments. The physical square has the eight-element dihedral symmetry group `D4`; consistently rotating or reflecting the entire construction is a coordinate equivalence rather than new evidence. Because `D4` acts freely on labeled bijections, the unrestricted assignment space has

`40,320 / 8 = 5,040`

geometric orbits before considering any additional decoder conventions.

Even the much narrower convention "write rule entries 0 through 7 consecutively around the perimeter" is not unique. It has eight choices for where entry 0 first materializes and two traversal directions, for 16 labeled placements. Modulo actual square symmetries, two distinct geometric cases remain: entry 0 begins on an edge-center or on a corner. A one-step cyclic shift around the eight-site ring is not a symmetry of the square lattice because it exchanges those geometric roles.

Other declared choices can enlarge the family further: which three-cell line supplies the input address, axis orientation, bit significance along that line, and in higher-dimensional layered constructions the transverse direction, axis ordering, and rule-entry ordering within storage layers. Some of these are related by full coordinate conjugacies; others are genuine interventions when the rest of the construction is held fixed.

The closure question should therefore first be written as a relation

`Q(R, sigma)`

between a rule and an admissible spatialization, not immediately as a predicate of the rule alone. Natural rule-level summaries include:

- **existential liftability:** does any preregistered `sigma` close?;
- **universal liftability:** do all admissible `sigma` close?;
- **liftability fraction:** what fraction of symmetry-inequivalent `sigma` close?;
- **best closure depth:** what is the strongest recursive level attained over the frozen family?;
- **geometry sensitivity:** how concentrated are successful lifts in particular spatialization orbits?

For the Class-IV conjecture, the most naive hope is existential: perhaps Class-IV rules are exactly those for which at least one natural spatialization closes nontrivially. But this must be tested over a frozen, class-blind family rather than by selecting a favorable placement after seeing the labels.

## Why Class IV is a plausible target but not a premise

Wolfram's original Class IV is the regime of long-lived localized structures and complex interactions, often described as lying between simple periodic behavior and disordered chaos. It is therefore tempting to imagine dimensional closure as another expression of the same balance: enough regularity to preserve a rule representation, enough nontriviality for that representation to remain dynamically active rather than collapse or randomize.

That intuition is not a derivation. Published classifications of boundary rules vary, and the four Wolfram classes are qualitative. The project will therefore freeze its primary labels and run the dimensional measurements blind to them.

## What would count as a striking success

The strongest outcome would be a class-blind structural property `Q(R)` derived from the existing rule-as-geometry construction such that, on symmetry-inequivalent ECAs,

`Q(R) = true` exactly for the repository's frozen Class-IV representatives,

with their reflected/complemented conjugates behaving accordingly.

A weaker but still interesting result would be strong enrichment of Class IV or concentration on the Class-II/Class-III boundary without exact exclusivity.

A negative result is also useful: if the natural dimensional closure properties are universal, symmetry-controlled, or distributed broadly across the rule space, then dimensional promotion is not the missing Class-IV razor.

## Guardrail

The accompanying preregistered protocol forbids using Class-IV labels to choose the lift geometry, decoder convention, score, tolerance, orientation, or search objective. The dimensional object must be defined first; class labels are attached only after the structural table is frozen.

When multiple spatializations are admissible, the full frozen family or a mathematically declared symmetry reduction must be evaluated. A post-hoc favorable `sigma` does not count as evidence for the Class-IV hypothesis.