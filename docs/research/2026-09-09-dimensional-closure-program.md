# Dimensional Closure and the Commutator Lift

This page is the **working synthesis** of the dimensional-lift research program. It collects the line that began with rules becoming spatial data and now asks a sharper question:

> **When two dynamical paths fail to commute, can the disagreement itself become a new spatial coordinate so that the enlarged representation closes?**

The program is parallel to [Dynamics of Erased Distinctions](2026-09-08-dynamics-of-erased-distinctions.md). That program asks when information can be forgotten safely and how a lossy representation repairs itself. This one asks what additional structure must be represented when evolution and transformation refuse to agree.

## The original dimensional observation

Two early constructions made lower-dimensional rules literal spatial data one dimension higher.

[Research011](2026-09-08-shared-state-rule.md) places the eight truth-table bits of an ECA on the eight-cell Moore ring around a 2D center. The same local patch can therefore be read as state, rule table, or both, and changing the assignment from truth-table entries to physical positions changes the induced dynamics.

[Research012](2026-09-08-dimensional-lift.md) gives a separate exact layered construction for outer-totalistic Moore rules. Two transverse layers hold the lower-dimensional rule table while the central layer carries its input neighborhood. The local interpreter is exact and symmetry-respecting, but the induced higher-dimensional rule generally falls outside the same recursively encodable family.

Those results established **rule as geometry**, not recursive dimensional closure.

## Exact intertwining supplies a baseline

The [dimensional-intertwining checkpoint](2026-09-09-dimensional-intertwining.md)
embeds every finite-radius 1D CA into a local 2D CA by the quotient encoding
E(S)(x,y)=S(x+y). For ECA, the active stencil has affine dimension two for
218 rules; a four-site coupling that vanishes on valid encoded states gives
an affinely 2D ambient rule for all 256.

The encoded fields still repeat one-dimensional information along diagonals.
One logical bit flip changes an entire diagonal. Exact trajectory
intertwining, ambient geometric dependence, and locally implementable edits
are therefore separate requirements. The result is a baseline for the
stronger program-inheritance search.

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

The ternary-block result is exact but semantic. A subsequent
[correction-coordinate checkpoint](2026-09-09-correction-future-coordinates.md)
adds an explicit local law for an infinitely prepared correction stack; it does
not establish finite local preparation or recursive spatial program inheritance.

\[
J_d
\]

tells us what the higher-dimensional coordinates **mean**. The ternary block alone does not supply such an autonomous law. For the
correction stack, the checkpoint gives the bounded local update
`U'_k = F(U_k) XOR U_(k+1)` on nonnegative layers. That construction supplies
all corrections initially and keeps the source rule in the upper law; it does
not yet meet the stronger program-spatialization target.

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

## Correction information versus correction vocabulary

The [correction-coordinate checkpoint](2026-09-09-correction-future-coordinates.md)
proves that the joint fields \((A_0,\ldots,A_h)\), with
\(A_0=D\) and \(A_{k+1}=C_F(A_k)\), are related by a bijective triangular
transformation to the observed future \((D,DF,\ldots,DF^h)\).
Their fibers are identical. A stack closes when the next correction is a
function of the joint represented state, even if individual correction maps
continue to change.

Thus full-map vocabulary growth is not itself a lower bound on the
information required for closure. This gives an exact bridge to the
future-equivalence relation in the parallel Program.

The checkpoint also isolates a program-binding requirement: for a fixed
Moore-ring decoder, changing the initial eight rule bits changes spatial
program data under one ambient selector law. Producing an inherited next
program requires an explicit additional construction; the generic
correction-stack law does not supply that interface.

## A recursively closed routing control

The [two-rail selector checkpoint](2026-09-09-selector-two-lift.md) freezes a
different physical control. A lifted rule evaluates its inherited source
program on the central slice, then uses that output to read one of the two
neighbors in the new dimension. The same Rail constructor applies again,
retaining every source instruction in a compact native grammar.

Encode the source between a positive zero half-space and a negative one
half-space. This complete encoding intertwines the dynamics if and only if
the source preserves both uniform configurations: exactly 64 ECA rules.
Every first descendant acquires that property, so all 256 descendants pass
the second interface and the 64 successful original sources continue through
every higher dimension. The proof accounts for every overlapping site and
preserves matched source bit flips.

This construction needs no source-dependent nonlocal preparation, but
supplies infinite homogeneous backgrounds and a distinguished interface.
Its program is static routing code in the law, not mutable program cells.
It also does not realize the ternary L/R/C roles. It is an exact control for
recursive syntax and spatial consistency, while the stronger active-program
requirement remains open.

## Program edits need a locality budget

The [program-edit checkpoint](2026-09-09-program-edit-locality.md) corrects an
ambiguity in the earlier next-step proposal. A finite edit of one globally
applied rule instruction cannot be implemented by finitely many target-cell
edits while changing the whole infinite source at a common finite time,
under one fixed local interpreter and a properly anchored local decoder.
Finite disagreements remain inside finite causal cones; a global rule
change has periodic witnesses with infinitely many changed outputs.

Local program-field edits remain well posed. Global rule replacement must
instead declare distributed edit support or a finite-world latency budget.
This distinction does not invalidate an internal program interpretation.

The same checkpoint quantifies the recovered stripe encoding: one source
bit edit changes an entire diagonal, and an n-by-n patch contains exactly
2n-1 independent bits. Any deterministic encoding with a fixed O(n)-site
source footprint has zero information per target area. Rich dynamics and
meaningful spatial organization remain possible; positive area entropy
cannot be demanded without supplying the corresponding input resources.

## Editable spatial programs now have a constructive witness

The [spatial Rail checkpoint](2026-09-09-spatial-rail-programs.md) realizes the
native Rail grammar with eight actual program cells beside each datum. One
uniform interpreter per dimension reads these cells. The same layout recipe
puts the program word along the newly added axis at each lift.

A separate fixed guard program, ECA 204, keeps the off-interface backgrounds
stable. This repairs the earlier 64-source restriction: every ECA starting
program and every heterogeneous native program field now has an exact lift.
One local state or instruction edit remains one physical cell edit. The
second interface works on arbitrary valid 2D program/data fields, and the
proof continues to every finite dimension.

A separately frozen extension also preserves state-gated copying of whole
program words from the left neighbor. Program values can therefore change
autonomously while the commuting identities continue to hold.

This is a witness for a declared family, with five cell symbols, radius nine,
a prepared 9^d-site macrocell layout, and infinite guard backgrounds. Eight
leaf instructions are mutable; Rail wrapper structure is fixed by dimension.
It does not encode arbitrary physical rules or realize the ternary L/R/C
roles. These architectural limits define subsequent experiments.

## Added routing contents are now spatial program data

The [editable-routing checkpoint](2026-09-09-editable-routing-tables.md) stores
one eight-bit table per axis. The original table reads the first-axis source
neighborhood; every later table reads the preceding result and its two
axis-neighbors. Both data execution and gated copying of the complete tuple
have exact physical realizations.

A lift appends the canonical selector table 172 and keeps separate guard
programs. Every native source field lifts, including arbitrary previously
edited 2D and 3D routing programs. Local proofs give every finite dimension;
the physical audit reaches dimension four. Inherited edits remain single
physical-symbol edits.

A newly introduced instruction is a new operation: editing it can change
the new-dimensional dynamics. Exactly 64 of 256 appended tables preserve
unchanged old behavior on the canonical rails, but all 256 table values are
allowed within a source being lifted next. Distinct stored programs also
need not have distinct data functions: the 65,536 two-word programs give
30,496 local data functions.

Storage is 8d+1 occupied sites per 9^d-site macrocell, still with five
symbols, radius nine and one-tick cadence. Local processing evaluates d
tables; its circuit cost is not dimension-independent. Contents are mutable;
stage order, axis assignments, protected roles and infinite guard backgrounds
remain prepared architecture. This is a scoped constructive result without
an established novelty claim.

## Finite boundaries and the return to correction closure

The [finite-boundary checkpoint](2026-09-10-finite-routing-boundaries.md)
replaces the infinite routing guards with three complete macrocell layers.
The physical rule is unchanged: guard data freeze because their outward
required inputs are absent. The native source type now explicitly retains
an occupancy mask; absent cells are not occupied zeros.

The mask lifts as Omega times {-1,0,1}, so it remains native for the next
lift. Both execution modes, program copying and inherited one-cell edits
commute for arbitrary masked source fields. This gives finite transverse
thickness, with absorbing blank exterior, not spontaneous role formation.

The [stored-correction checkpoint](2026-09-10-stored-correction-transport.md)
then returns to the original commutator. Program(r,60) physically executes
F(row) XOR the next correction row, with both instructions stored in cells.
A stack prepared through H is exact when k+t<=H. A constant zero cap does
not generally close it: the retained Rule255 example corrupts row0 at tick3
when H=2, despite an entirely valid and stable physical layout.

The [local-cap census](2026-09-10-local-correction-caps.md) now supplies exact
local certificates or conflicts for all4,608 frozen budgets. A post-census
Rule32 witness closes two rows: U'=F_32(U) XOR V and V'=F_128(V), with
nonconstant cap V_left AND V_right. This holds at every time for correctly
prepared source images. The [physical-cap checkpoint](2026-09-10-rule32-physical-cap.md)
now executes this pair with stored programs and finite guards, with a complete
all-time field identity. Matched edits execute faithfully, but a persistent
one-cell-error witness refutes general semantic recovery under this cap.
Boundary stability, information sufficiency, and recovery remain distinct.

## Clarified dimensional-beam objective

On2026-09-10 the user made the destination explicit: a recurring dimensional
construction, coherent lower-dimensional trajectories, additional native
possibilities at higher levels, and organization increasingly governed by the
program's own unfolding. "Turtle beam" names this sought continuity;
"unus mundus" is an interpretive analogy, not an established conclusion.

Correction depth, spatial dimension and time are different quantities. The
current two-row correction system occupies one plane; adding another correction
row does not add a spatial axis. The existing lift can carry the whole native
plane onward. Guarded constructions remain valuable controls and instruments,
but their prepared invariant subsets do not settle the stronger objective.

Minimum representation dimension requires a declared encoding, causal and
resource contract. In a coherent tower of total adjacent lifts, a composed
path cannot skip its intermediate levels. Under injective lifts, minimum
ancestral dimension is preserved by lifting and cannot increase under the
compatible dynamics. These deductions concern the chosen tower; an intrinsic
notion must avoid merely detecting its padding. No arithmetic-prime analogy
is established.

The [extension-freedom checkpoint](2026-09-10-extension-freedom.md) gives a
concrete diagnostic. The Rule32 image leaves98 output bits free in the broad
radius-one pair grammar. In the existing guarded table-chain grammar,128 top
program tuples induce four compatible functions; top ECA128 and160 both
preserve every encoded data trajectory while responding differently to an
off-image defect. The ambient completion is not uniquely selected by its beam.

The differing instruction bit can also circulate autonomously under existing
state-gated copying, with exact encoded data and physical program evolution.
It is dormant on that data image. Endogenous instruction change and revision
of represented data dynamics therefore remain distinct achievements.

## A guard-free dimensional comparison

The [axial-family checkpoint](2026-09-10-guard-free-axial-lift.md) applies the
same source ECA along each spatial axis in sequence. This gives a binary CA
on every ambient field in every dimension, without guards or reserved roles.
Literal copying along the new axis preserves the source dynamics exactly for
66 rules:0,255 and every even word from128 through254. The same condition is
necessary and sufficient at every interface, not just the first two checked.

Exactly24 sources have commuting axial operators, and14 satisfy both
replication compatibility and axis-permutation equivariance. Another52 preserve
the beam while retaining an axis order. The14 are constants, copies, parity,
AND/OR functions. Rule32 fails this constructor; its distinct correction-cap
closure remains valid. Axis permutations do not imply reflection symmetry.

This removes guard machinery at a cost: replication is still supplied, the
source word remains in the law, and mutable spatial programs are not retained.
One macro update costs d lattice passes or(3^d-1)/2 naive ECA lookups per
output. The replicated image has zero information per added-dimensional
volume, and a local source edit changes an infinite target line. Yet ambient
Rule128/150/254 use every site of their3^d neighborhood, so their extra axes
are actual causal inputs. This does not settle intrinsic representation dimension.

## Relation to the Class-IV hope

The original Class-IV conjecture records the intuition that motivated this
thread. On 2026-09-09 the user clarified that it must not motivate the
reasoning or construction choices. It is background, not an active selection
criterion or a planned classification gate.

Earlier closure and growth statistics already failed exclusivity tests.
The stored-program control works across all256 ECA starting programs; the
guard-free axial recipe preserves replication for66. Each count concerns its
own declared architecture and is not a Class-IV selection result.

Negative findings remain local to the attempted grammar, encoding, and
budget. Preserve them and state each proposed rescue explicitly; neither a
failed candidate nor a successful broad family settles every version of
recursive spatial-program closure.

## What is exact now

1. **Rule-as-space constructions exist.** ECA truth tables and outer-totalistic rule tables admit exact higher-dimensional spatial encodings under declared local interpreters.
2. **Derivative completion has exact recursive typing.** Rule, state, and incoming derivative occupy equal-size roles in the totalistic recursion, and the extra dimension can select among them.
3. **The commutator is a transport correction.** For any represented role, noncommutation supplies the exact residual needed to reconcile the two evolution paths.
4. **The ternary semantic lift is rule-independent.** `L/R/C` recursion gives a dimension-uniform exact semantic block for every deterministic source rule.
5. **The ternary address has a forced quotient.** `LR=RL` and `LC=CL` bound exact-depth semantic roles by `2^(d+1)-1`.
6. **Role-growth statistics are not Class-IV-exclusive.** Finite-map and intrinsic local censuses both rule out simple closure/growth statistics as the dimensional razor.
7. **Correction tuples and observed futures have identical fibers.** The exact triangular coordinate change separates joint information growth from growth in the vocabulary of individual maps. An infinitely prepared correction stack has a bounded local spatial update.

8. **A two-rail routing grammar closes recursively.** The fixed interface encoding is exact if and only if the source preserves both uniform states. All 256 ECA programs remain distinguishable through two lifts; 64 source dynamics embed through both and every subsequent lift. This retains program instructions as static routing code, not active lattice data.

9. **Editable spatial Rail programs have exact recursive realizations.** A five-symbol, radius-nine interpreter with a separate guard program preserves all native source program/data fields through both interfaces and every further finite lift. It also preserves autonomous state-gated program transport. Fixed role markers and wrapper structure remain architectural resources.

10. **Introduced routing-table contents can be edited and inherited.** One eight-bit table per axis gives exact physical execution and lifts for arbitrary native source programs, including autonomous copying of the added words. The grammar's ordered topology and prepared boundary resources remain fixed.

11. **Finite routing boundaries preserve explicit occupancy.** Three macrocell layers suffice for the unchanged interpreter and give exact recursive lifts of masked source fields, including program copying and inherited edits.

12. **Stored programs execute correction transport.** Program(r,60) gives the interior correction law and exact finite prepared triangle. A constant zero cap has an explicit failure; indefinite local cap closure is not yet established by this construction.

13. **Finite logical correction caps have exact certificates.** The all-ECA full-shift census finds1,094 passing budgets and3,514 conflicts for h=0..2,R=0..2 in K/O coordinates. Rule32 has a nonconstant two-row all-time logical closure. Different local radii do not contradict K/O whole-field fiber equivalence, and source retention remains a cheaper raw storage baseline.

14. **A finite physical correction cap now closes indefinitely.** Rule32's two-row pair is realized by stored programs(32,60)/(128,240) and finite guards. The complete identity holds at every time. All1,360 tested matched edits execute faithfully; a separate persistent-background proof shows expanding disagreement after one top data or instruction edit, so this is not general repair.

15. **Encoded compatibility leaves ambient freedom.** Exact local constraints admit multiple stored-program completions with different off-image behavior. Compatible instruction variants can move autonomously while their distinguishing bit remains dormant on the encoded data image.

16. **A guard-free binary axial family has an exact all-dimensional classification.** Literal replication intertwines every adjacent interface for exactly66 ECA sources. Exactly24 sources commute across axes and14 satisfy both properties. Uniform local recursion can preserve a beam without guards, while replication and source-law dependence remain supplied resources.

## What remains open

- Rule32's finite-height physical cap and matched-edit contract are established. Broader cap compilation and intentional semantic program revision remain open; the current law does not generally restore the undamaged represented trajectory.
- Finite-thickness routing boundaries are constructive under fixed occupancy and missing-input retention. Occupancy edits, mutable stage topology, smaller alphabets and self-maintained roles remain open.
- The relationship between correction depth, spatial dimension, growing spatial radius and minimum causal representation dimension is not yet characterized. A fixed code's ancestral rank may primarily reflect its layout.
- The guard-free replication beam is invariant for66 sources. Whether transverse differences form an autonomous dynamical state, or need base information and correction state, is the next frozen test. This is distinct from self-assembly or autonomous changes to the source law.
- Class-IV correspondence is background motivation only and does not direct the current search.

## The next theoretical target

The [next frozen protocol](protocols/transverse-difference-closure-20260910.md)
observes T(X)(x,y)=X(x,y) XOR X(x,y+1) under the unchanged axial laws for all66
compatible sources. T=0 identifies the replication beam. Ask whether T evolves
autonomously at radius0 or1 using every3-by4 source patch. Separately, complete
3-by3 periodic observation fibers can supply full-field obstructions to any
autonomous T law when they contain conflicting next observations. It is unrun.

This tests whether off-beam organization can be described by transverse
differences alone, before adding source or correction state. Preserve the
distinction between a failed local budget and an all-radius obstruction.
Commit implementation before execution and freeze any rescue separately.
Earlier stored-program and correction instruments remain useful comparisons.
C4, prime analogies and metaphysical interpretations do not select rules or
upgrade evidence.
