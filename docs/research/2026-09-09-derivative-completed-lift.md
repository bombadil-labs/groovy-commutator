# The missing center completes a rule/state/change lift

The user proposed filling the distinguished center left by the ECA eight-bit Moore-ring spatialization with the incoming derivative that produced the current lower-dimensional center value.

That idea does more than fill one cell. It exposes an exact recursive counting and addressing structure.

No Wolfram class labels were used in deriving or checking the results below.

## The base coincidence becomes a bijection

An unrestricted ECA has eight output bits. A binary center-independent totalistic 2D Moore rule has one output for each possible number of live outer neighbors, `0..8`, so it has nine rule bits.

Define the base completed lift by

\[
L_1(R,\delta)=(R_0,R_1,\ldots,R_7,\delta),
\]

where `delta` is the incoming discrete derivative

\[
\delta_t(x)=S_{t-1}(x)\oplus S_t(x).
\]

Formally, the 256 ECA tables times the two derivative values give

\[
256\cdot2=512,
\]

exactly the full 2D center-independent totalistic rule space. The verifier confirms that `(R,delta) -> L_1(R,delta)` is a bijection onto all 512 such 2D rules.

If `delta` must actually occur at some local ECA transition, 254 of the 256 ECAs realize both derivative values. Only Rule 204, the center identity, has derivative always zero, and Rule 51, NOT-center, has derivative always one. The dynamically realizable base lifts therefore cover 510 of the 512 totalistic 2D rules.

This breadth means the base completion is not itself a Class-IV discriminator.

## A recursively typed native family

Let `T_d` be the binary center-independent totalistic radius-one Moore rules in dimension `d`.

A d-dimensional Moore neighborhood contains `3^d` cells including its center, hence `3^d-1` outer neighbors. Their live count has exactly

\[
M_d=3^d
\]

possible values. Therefore every rule in `T_d` is represented by exactly `M_d` bits.

A local side-three d-dimensional state block also has `M_d` bits, and so does its incoming derivative block. The next dimension has

\[
M_{d+1}=3M_d.
\]

Thus the three co-typed objects

\[
(\text{rule},\text{state},\text{incoming derivative})
\]

fit exactly into one `(d+1)`-dimensional totalistic rule table:

\[
L_d(r,s,\delta)=r\;\Vert\;s\;\Vert\;\delta.
\]

This works without padding for every positive `d` in the totalistic family. The unrestricted ECA `8+1 -> 9` construction is a special bootstrap into that recursive family.

## The extra dimension is a three-way selector

The concatenation has an exact local interpretation.

Fix `M=3^d`. Let a `(d+1)`-dimensional radius-one neighborhood have a central d-dimensional slice whose outer-neighbor count is `n`. Let each of its two transverse outer slices be uniform, and let `q` be the number of those slices that are all one.

Each live transverse slice contributes exactly `M` live outer neighbors. Therefore the higher-dimensional outer-neighbor count is

\[
j=qM+n.
\]

The lifted totalistic rule reads table entry `j`. Because the table is concatenated into three `M`-bit blocks,

\[
L_d(r,s,\delta)_{qM+n}=
\begin{cases}
r_n,&q=0,\\
s_n,&q=1,\\
\delta_n,&q=2.
\end{cases}
\]

So the transverse population selects one of three semantic roles:

- no live transverse slice: apply the lower-dimensional rule;
- one live transverse slice: read the stored state block;
- two live transverse slices: read the stored derivative block.

This is an exact index identity, not a finite empirical pattern. The verifier checks representative index realizations through dimensions one to three.

It also mirrors the earlier dimensional interpreter, where a count selected a coordinate through ternary addressing, but now the most significant ternary digit selects **rule/state/change**.

## A useful inverse view

For `d>=1`, any next-dimensional totalistic table of `3M` bits can be split uniquely into three `M`-bit blocks. Under the declared role order this gives a formal inverse decomposition

\[
r'\longleftrightarrow(r,s,\delta).
\]

If the derivative is required to be dynamically genuine, then not every triple is admissible. Writing the predecessor block as

\[
p=s\oplus\delta,
\]

the dynamic consistency condition is

\[
s=F_r(p)=F_r(s\oplus\delta).
\]

Thus derivative-completed lifting suggests a native structural test on the higher-dimensional rule itself: split its table into rule/state/change thirds and ask whether those blocks describe an actual lower-dimensional transition.

This is a promising closure equation. It still describes a rule-plus-transition object, not yet a static rule-only lineage.

## The self-substrate shortcut collapses

Because `T_d` rule tables and side-three d-torus states have the same number of bits, one tempting shortcut is to use a rule table as its own state.

That control is analytically too simple. On a side-three d-torus, the radius-one Moore outer neighborhood of each cell is every other cell exactly once. If the rule-state has total population `p`, then a zero cell sees count `p` and a one cell sees count `p-1`.

Therefore one self-update can only send the state to

\[
0,\qquad1,\qquad r,\qquad\neg r.
\]

The exhaustive 2D census over all 512 totalistic rules confirms the collapse. Among the 510 nonconstant tables, 128 map to themselves, 128 to their complements, 127 to zero, and 127 to one; the two constant tables are fixed.

So identifying the rule with the entire minimal state is not the missing nontrivial dynamics.

## What remains genuinely open

The derivative completion has produced a concrete candidate syntax, but the research target is now dynamical rather than representational.

We need an overlap-consistent higher-dimensional state architecture in which the three count bands are exercised as rule/state/change and in which

\[
\text{lift}\circ\text{evolve}
\]

can be compared exactly with

\[
\text{evolve}\circ\text{lift}.
\]

The key question is whether the lower transition context encoded by `(s,delta)` becomes internally recoverable after lifting, or whether an external history channel is still required.

If it becomes internally recoverable, we have a genuine recursive rule/state/change operator. If not, the result still identifies precisely what information the putative lift is missing.

The Class-IV conjecture remains downstream. No class claim follows from the universal storage identity or the three-way selector theorem.

## Evidence

- [preregistered derivative-completed protocol](protocols/derivative-completed-lift-20260909.md)
- [structural verifier](../../scripts/verify_derivative_completed_lift.py)
- [saved checks](../../results/derivative_completed_lift_20260909.json)
