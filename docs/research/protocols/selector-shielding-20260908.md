# Selector-relative shielding protocol — 2026-09-08

## Status

Frozen before any new evaluation beyond the exploratory fine-tick-128 observation recorded in the pulse-shape scattering note.

This follow-up is stacked on the Research021 pulse-shape branch. It deliberately does **not** claim the next project research number because another session is working in parallel.

## Question

Research021 found, outside its preregistered four-site census, a finite adjacent-strip encounter in which interaction damage appears immediately beside the lower Rule-90 organization while the lower outer physical row remains exactly equal to its isolated evolution through fine tick 128.

The concrete witness is

\[
A=\{-5,0\},\qquad B=\{0,1,3,4,6\},
\]

with `A` encoded in rows 0/1 and `B` in rows 2/3 at even phase.

This follow-up asks two nested questions.

1. **Witness shielding.** Does row 3 of the coupled evolution remain exactly equal to row 3 of the isolated lower-strip evolution for all time, despite differences on row 2?
2. **Selector mechanism.** Can any such persistence be reduced to an exact invariant saying that the coupled/reference differences never occupy source addresses actually selected by the row-3 update?

A finite-horizon pass is evidence only. An all-time claim requires a local induction, finite-state reduction, or equivalent exact argument.

## Fixed physical law and background

Use the same binary 2D law as Research018–021,

\[
F(X)(y,x)=X\bigl(y+2X(y,x)-1,\;x+X(y,x-1)+X(y,x+1)-1\bigr),
\]

with exact alternating background

\[
B_t(y,x)=(x\bmod2)\oplus(t\bmod2).
\]

At even phase, encode a finite logical support `S` in the two-row strip beginning at row `j` by

\[
U_j(S)=\{(j,2i+1),(j+1,2i):i\in S\}
\]

as a perturbation of `B_0`.

Define the coupled initial perturbation

\[
\delta^{C}_0=U_0(A)\cup U_2(B),
\]

and the isolated lower reference

\[
\delta^{L}_0=U_2(B).
\]

The reference is an exact Rule-90 strip trajectory by the existing strip theorem.

## Exact shielding observables

At every fine tick compare the **complete physical states**, equivalently the perturbations relative to the common analytic background.

Let

\[
C_t=\delta^C_t\triangle\delta^L_t
\]

be the coupled/reference difference set.

Record:

- whether row 3 is identical: `C_t ∩ ({3}×Z) = ∅`;
- whether the entire lower exterior half-plane is identical: `C_t ∩ ({3,4,5,...}×Z) = ∅`;
- the row-2 contamination support
  \[
  Q_t=\{x:(2,x)\in C_t\};
  \]
- the row-3 destination cells whose selector reads from row 2;
- the exact row-2 source addresses selected by those destinations;
- the intersection between those selected source addresses and `Q_t`.

The selector for destination `(3,x)` in a state `X_t` reads

\[
s_t(x)=\bigl(3+2X_t(3,x)-1,\;x+X_t(3,x-1)+X_t(3,x+1)-1\bigr).
\]

When coupled and reference rows 3 are equal, they have the same horizontal selector and the same choice between source rows 2 and 4. Define the vulnerable row-2 source set

\[
V_t=\{x':s_t(x)=(2,x')\text{ for some }x\}.
\]

Then `Q_t ∩ V_t = ∅`, together with equality of the other selected sources, is an exact one-step shielding condition. The research question is whether this condition is itself invariant for the witness and whether it admits a finite local characterization.

## Frozen finite-horizon validation

Before attempting a proof, extend the exploratory observation to fine tick 1024 unless an exact counterexample occurs earlier.

Use both already-audited update kernels from Research020:

1. the cropped dense physical-field update;
2. the independently written sparse infinite-lattice scalar update.

They must agree on the complete changed-coordinate set for both the coupled and isolated trajectories at every directly simulated tick.

For every tick through the stopping time require and record separately:

- dense/sparse equality for the coupled field;
- dense/sparse equality for the isolated field;
- row-3 equality between coupled and isolated fields;
- lower-half-plane equality for rows `y>=3`;
- `Q_t`, `V_t`, and `Q_t∩V_t`;
- whether row 2 itself differs;
- canonical digests of the full coupled and reference perturbations.

If row 3 first differs, stop and save the complete predecessor state and selected source responsible for the first failure. That is an exact finite counterexample to all-time shielding.

If row 3 remains equal through tick 1024, report only finite-horizon survival; do not call it proved.

## Post-validation proof search

Only after the frozen horizon result is saved may exploratory analysis inspect the local structure of `Q_t` and `V_t` and propose an invariant.

Preferred proof routes, in order:

1. a parity/residue invariant for `Q_t` and `V_t`;
2. a finite-state automaton for the row-2/row-3 interface in a suitable moving or Rule-90 phase frame;
3. a finite causal-template exhaustion that covers every reachable interface state;
4. a direct induction using the selector law and exact Rule-90 edge/interior identities.

Any proposed finite-state closure must be checked for reachability, not merely for all syntactically possible local bit patterns.

## Mirror control

If the lower shielding witness survives the frozen validation, test the reflected upper-shielding counterpart under the exact geometric symmetry used by the implementation. The mirror is a control on the mechanism, not a separate discovery family.

## Nonclaims

This protocol concerns one declared witness and its mirror. It does not establish shielding for arbitrary pulse shapes, arbitrary adjacent strips, other phases, other laws, or all one-sided-escape states.

`Q_t∩V_t=∅` is initially a diagnostic identity, not yet an explanatory theorem. The goal is to determine whether it closes under the dynamics.

The observation-closure work in the parallel session is related conceptually but is not modified by this branch. The 3D hypothesis remains parked.
