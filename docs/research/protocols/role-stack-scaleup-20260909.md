# Protocol: scale the minimal role-stack witness from 2D to 3D

Date: 2026-09-09
Status: preregistered before evaluation

## Motivation

The frozen 1D -> 2D role-stack search found one nonconstant center-independent totalistic source rule with exact closure: table `(0,1,0)`, equivalent to ECA Rule 90. Its only successful geometry at each tested period is an all-zero transverse background with zero drift.

The decision boundary of that protocol requires scaling the **minimal successful geometry** before adding any new spatial freedom.

## Frozen geometry

Use transverse period three with exactly three `3 x 3` slices in the higher 3D torus:

\[
E(s)=[s,0,0],
\]

where `s` is the current lower 2D state and both guard slices are all zero. No drift is allowed.

No alternative guards, periods, offsets, blockings, or decoders are introduced in this note.

## Lower family

Use every binary center-independent totalistic radius-one Moore rule in two dimensions. A rule is a nine-bit table

\[
r=(r_0,\ldots,r_8),
\]

indexed by the number of live outer neighbors. There are exactly 512 rules.

Use the complete periodic `3 x 3` lower state space, also 512 states.

For every predecessor state `p`, define

\[
s=F_r(p),\qquad
\delta=p\oplus s,\qquad
s^+=F_r(s).
\]

The lifted 3D totalistic rule is the 27-bit table

\[
L(r,s,\delta)=[r\mid s\mid\delta].
\]

## Primary closure identity

For every source rule `r` and every predecessor state `p`, test

\[
F_{L(r,s,\delta)}(E(s)) = E(s^+).
\]

A source rule is **scale-up role-stack closed** iff the identity holds for all 512 predecessor states.

The evaluator contains no Wolfram class labels.

## Mechanism audit

Because the data slice is flanked by zero slices, every data cell addresses the first nine-entry block `r`; therefore its update should equal `F_r(s)` identically.

Each zero guard cell sees the total population `|s|` of the data slice. Save the exact set of reachable lower-state populations and the lifted table entry read by a guard for each population.

This permits a separate analytic characterization of success/failure:

- if `|s| < 9`, the guard reads `r_|s|`;
- if `|s| = 9`, the guard reads the first state-block entry `s_0`, which is one for an all-one state and therefore breaks the zero guard.

The full 3D update and this population criterion must agree for all 512 x 512 source transition cases.

## Outputs

Save:

- all 512 rule decisions;
- number of closed rules;
- reachable population sets per rule;
- first failure witness per rejected rule;
- exact agreement between direct 3D evolution and the population criterion;
- rule-table patterns shared by successful rules, without attaching external dynamical labels.

## Interpretation

This is a mechanism-scaleup test, not a Wolfram Class-IV test. The source family is 2D totalistic and has no preassigned Wolfram class labels in the evaluator.

If nontrivial rules survive, derive the algebraic success condition and ask whether it is dimension-uniform before broadening the spatial encoding.

If only constant/trivial rules survive, the Rule-90 witness is dimension-specific under this geometry and the simple role-stack operator does not recursively close.

If a large family survives, the next question is whether any successful rule actually exercises the state or derivative blocks; dormant blocks do not establish derivative-active closure.