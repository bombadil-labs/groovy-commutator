# Dimensional rule closure: the Class-IV hypothesis

This checkpoint records a deliberately strong conjecture before the dimensional-closure operator is finalized:

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
