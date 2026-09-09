# Dimensional Closure and the Commutator Lift

This page is the **working synthesis** of the dimensional-lift research program. It collects the line that began with rules becoming spatial data and now asks a sharper question:

> **When two dynamical paths fail to commute, can the disagreement itself become a new spatial coordinate so that the enlarged representation closes?**

The program is parallel to [Dynamics of Erased Distinctions](2026-09-08-dynamics-of-erased-distinctions.md). That program asks when information can be forgotten safely and how a lossy representation repairs itself. This one asks what additional structure must be represented when evolution and transformation refuse to agree.

## The original dimensional observation

Two early constructions made lower-dimensional rules literal spatial data one dimension higher.

[Research011](2026-09-08-shared-state-rule.md) places the eight truth-table bits of an ECA on the eight-cell Moore ring around a 2D center. The same local patch can therefore be read as state, rule table, or both, and changing the assignment from truth-table entries to physical positions changes the induced dynamics.

[Research012](2026-09-08-dimensional-lift.md) gives a separate exact layered construction for outer-totalistic Moore rules. Two transverse layers hold the lower-dimensional rule table while the central layer carries its input neighborhood. The local interpreter is exact and symmetry-respecting, but the induced higher-dimensional rule generally falls outside the same recursively encodable family.

Those results established **rule as geometry**, not recursive dimensional closure.

## The target is a rule-independent lift

The research therefore shifted from finding favorable encodings for particular rules to finding one operator that is fixed before rule outcomes.

The desired shape is

\[
L_d:\mathcal R_d\rightharpoonup\mathcal R_{d+1},
\]

with the same geometric and semantic recipe across the entire source family. A useful lift may be partial: the operator is presented to every rule, while only some outputs may remain native enough to lift again.

This rule-blindness is essential. The original optimistic Class-IV conjecture is downstream of the operator search, not a criterion used to choose the operator.

## Provenance showed what the missing center can mean

The ECA Moore-ring picture has eight rule bits around one distinguished center. Filling that center with the incoming derivative suggested a rule/state/change architecture.

The derivative-completed construction exposed two exact facts:

- an ECA rule plus one derivative bit fills all nine entries of a 2D center-independent totalistic rule table;
- in the recursive totalistic family, three equal-size blocks—rule, state, derivative—fit exactly into the next-dimensional table because \(3^{d+1}=3\cdot3^d\).

The extra dimension can therefore act as a three-way selector among rule, state, and change.

But the simplest spatial role-stack realizations do not recursively close on changing trajectories. The derivative is useful context, but it does not by itself make the old layered interpreter autonomous.

## The commutator becomes a correction role

The fanout experiments clarify the obstruction. Let

\[
D(S)=S\oplus F(S).
\]

The Groovy commutator is

\[
G(S)=D(F(S))\oplus F(D(S)).
\]

Rearranging gives

\[
D(F(S))=F(D(S))\oplus G(S).
\]

So the commutator is not merely a score saying that derivative and evolution disagree. It is **exactly the correction field required to transport the derivative as if it were an ordinary state**.

Applying the same idea again generates a correction hierarchy. This led first to the commutator tower and then to the more canonical ternary lift.

## The commuting square grows a ternary coordinate

[Research035](2026-09-09-ternary-commutator-lift.md) defines, for any represented transformation `A`,

\[
L_F(A)=A\circ F,
\]

\[
R_F(A)=F\circ A,
\]

and

\[
C_F(A)=L_F(A)\oplus R_F(A).
\]

Starting from the outgoing derivative \(D=I\oplus F\), every word over the alphabet `{L,R,C}` defines a descendant role. At depth \(d\), the labeled descendants are naturally indexed by the \(3^d\) coordinates of a side-three \(d\)-dimensional block.

Define

\[
J_d(S)_w=A_w(S).
\]

Then adding one semantic dimension gives three exact slabs:

\[
J_{d+1}^{L}(S)=J_d(F(S)),
\]

\[
J_{d+1}^{R}(S)=F^{\parallel}(J_d(S)),
\]

\[
J_{d+1}^{C}(S)=J_{d+1}^{L}(S)\oplus J_{d+1}^{R}(S).
\]

So every added dimension stores **evolve then transform, transform then evolve, and the difference between them**.

This is the first rule-independent, dimension-uniform lift operator produced by the program.

## The ternary space has an algebraic quotient

The \(3^d\) labeled coordinates are not all semantically independent. Associativity gives

\[
LR=RL,
\]

and left composition distributes through XOR, giving

\[
LC=CL.
\]

Therefore exact depth \(d\) has at most

\[
\boxed{2^{d+1}-1}
\]

distinct semantic roles.

The frozen all-ECA census respects this bound. On the finite eight-cell substrate, 107 rules saturate the maximum sequence through depth six, while 33 reach a finite closed role vocabulary within that horizon. An intrinsic infinite-lattice local-rule census confirms broad rule-dependent growth without relying on torus recurrence.

Neither finite closure nor maximal growth is Class-IV-exclusive. That negative result is useful: the operator survives because it was derived class-blindly, while those simple algebraic statistics are eliminated as the hoped-for discriminator.

## Semantic lift versus physical lift

The current result is exact but semantic.

\[
J_d
\]

tells us what the higher-dimensional coordinates **mean**. It does not yet supply one bounded native \((d+1)\)-dimensional CA whose ordinary local evolution preserves that meaning autonomously.

This distinction is now the central boundary of the program.

A successful physical realization must:

- use one fixed local architecture across source rules;
- preserve the declared `L/R/C` roles under evolution;
- reproduce lower-dimensional evolution on the appropriate projection;
- carry the correction information needed for the next step without an external history or program channel;
- remain well typed when lifted again.

The local ternary census also shows that retaining the entire `L/R/C` vocabulary may be stronger than necessary. For transport of a represented role `A`, the identity

\[
A(F(S))=F(A(S))\oplus C_F(A)(S)
\]

requires only the role and its correction. This points toward a **correction-stack realization** rather than a literal physical copy of the full ternary tree.

## Relation to the Class-IV hope

The motivating conjecture was deliberately strong: perhaps Class IV, and only Class IV, supports recursive dimensional closure.

Several candidate criteria have already failed that exclusivity test:

- literal overlapping rule-ring tilings collapse to constants or small spatial crystals;
- simple rule/state/derivative role stacks do not recursively close on changing trajectories;
- finite commutator-tower length is sensitive to ring size;
- ternary role closure and maximal role growth both include rules from multiple Wolfram classes.

None of those failures falsifies the stronger native-spatial-closure conjecture, because none is yet the final physical lift.

The discipline remains unchanged: fix the higher-dimensional architecture first, then attach class labels.

## What is exact now

1. **Rule-as-space constructions exist.** ECA truth tables and outer-totalistic rule tables admit exact higher-dimensional spatial encodings under declared local interpreters.
2. **Derivative completion has exact recursive typing.** Rule, state, and incoming derivative occupy equal-size roles in the totalistic recursion, and the extra dimension can select among them.
3. **The commutator is a transport correction.** For any represented role, noncommutation supplies the exact residual needed to reconcile the two evolution paths.
4. **The ternary semantic lift is rule-independent.** `L/R/C` recursion gives a dimension-uniform exact semantic block for every deterministic source rule.
5. **The ternary address has a forced quotient.** `LR=RL` and `LC=CL` bound exact-depth semantic roles by `2^(d+1)-1`.
6. **Role-growth statistics are not Class-IV-exclusive.** Finite-map and intrinsic local censuses both rule out simple closure/growth statistics as the dimensional razor.

## What remains open

- No fixed bounded native higher-dimensional CA realization of the ternary or correction-stack lift has been established.
- It is unknown whether a bounded Euclidean geometry can carry the required correction roles without hidden external state.
- The relationship between correction depth, spatial dimension, and growing within-dimension radius is not yet characterized.
- No native dimensional-closure criterion has yet earned comparison against a complete Wolfram-class taxonomy.

## The next theoretical target

The immediate proof problem is constructive:

> **Find a fixed local higher-dimensional CA realization of the commutator correction lift.**

The semantic operator is already known. The next task is to make it physical: determine whether the correction required to transport a lower-dimensional role can be stored in adjacent spatial channels so that one ordinary higher-dimensional update advances the whole represented system and leaves it ready to lift again.

If that succeeds, dimensional projection stops being an analogy. It becomes an explicit commuting diagram implemented in space.
