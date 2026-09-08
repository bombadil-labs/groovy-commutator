# Pulse-scattering census protocol — 2026-09-08

## Question

For the fixed adjacent-strip architecture of Research018/019, hold the physical
law, background, pulse shapes, vertical placement, horizontal phase, and
sampling conventions fixed. Vary only the relative horizontal displacement of
two single logical Rule-90 pulses.

Does encounter geometry determine qualitatively different exact fates — in
particular annihilation, certified unbounded escape, or exact reconstitution
into separated strip organizations after the initial adjacent-strip code has
failed?

This is a scattering census for one declared pulse family. It is not a search
over laws or decoders.

## Fixed physical system

Use the same binary 2D law as Research018/019:

\[
F(X)(y,x)=X\bigl(y+2X(y,x)-1,\;x+X(y,x-1)+X(y,x+1)-1\bigr).
\]

The background is

\[
B_t(y,x)=(x\bmod 2)\oplus(t\bmod 2).
\]

At even phase, a single active logical bit at index `i` in a two-row Rule-90
strip beginning at row `j` differs from the background at exactly

\[
(j,2i+1),\qquad (j+1,2i).
\]

Put the upper strip at rows 0/1 and lower strip at rows 2/3. Fix the lower
pulse at logical index 0 and put the upper pulse at logical index `d`. Thus

\[
\delta_0(d)=\{(0,2d+1),(1,2d),(2,1),(3,0)\}.
\]

Research019's unbounded-escape witness is the member `d=1`.

## Frozen census domain

Enumerate every integer displacement

\[
-64\le d\le64.
\]

Attempt direct evolution through fine tick 192 inclusive. If an exact
extinction or persistent-tip certificate is reached earlier, the simulator may
terminate that trajectory because its primary fate is then fixed for all future
times; it must retain the certificate state and first time. The primary
implementation uses a finite array/cropped causal rectangle with analytic
background padding and no physical torus. The independent audit uses an
infinite-lattice sparse perturbation implementation against the analytic
background and does not share the primary update routine.

The census range and horizon are descriptive bounds, not a theorem about all
integer displacements. Exact certificates defined below may support all-time
claims for individual trajectories.

## Recorded observables

For every displacement and every directly simulated tick record at least:

- perturbation mass `|delta_t|`;
- top, bottom, left, and right changed coordinates and bounding box;
- vertical and horizontal span;
- whether any cell lies outside the original rows 0 through 3;
- whether the complete even-phase field belongs to the original adjacent
  two-strip code `V_0`;
- whether the complete even-phase field is a finite union of **separated exact
  strips**, as defined below.

After an exact terminal/certificate event, later per-tick metrics need not be
materialized; the saved result must distinguish analytic continuation from
directly simulated observations.

Also record first times for extinction, original-code departure, exterior-row
change, certified top escape, certified bottom escape, two-sided certified
escape, and post-departure separated-strip reconstitution when present.

## Exact all-time escape certificate

Use the extreme-row identities already proved in Research019. If row `r` is
the topmost changed row at time `t`,

\[
\delta_{t+1}(r-1,x)=B_t(x)\,\delta_t(r,x-1).
\]

For the bottommost changed row,

\[
\delta_{t+1}(r+1,x)=(1\oplus B_t(x))\,\delta_t(r,x+1).
\]

A **top tip certificate** is present when the topmost changed row is a
singleton `(r,x)` and `B_t(x+1)=1`. Then the next top row is the singleton
`(r-1,x+1)`, and the same polarity condition repeats forever. A **bottom tip
certificate** is present when the bottommost changed row is a singleton
`(r,x)` and `B_t(x-1)=0`; then `(r+1,x-1)` repeats forever.

Once either certificate appears, report escape in that direction as proved
for all later times, not merely observed through tick 192. A two-sided escape
certificate requires both directions (not necessarily first appearing at the
same tick).

Do not infer indefinite confinement from failure to find a certificate.

## Exact extinction

If `delta_t` is empty, the state equals `B_t`; because the alternating
background is an exact trajectory, extinction is permanent. Record this as an
all-time annihilation certificate.

## Exact separated-strip reconstitution

At an even tick, call the complete perturbation a finite union of separated
Rule-90 strips iff its nonempty rows can be partitioned into adjacent pairs
`(j,j+1)` such that:

1. different pairs have at least one completely background row between them;
2. in each pair, top-row changes occur only at odd columns;
3. bottom-row changes occur only at even columns; and
4. for every logical index `i`, `(j,2i+1)` is changed iff `(j+1,2i)` is
   changed.

This is exactly the finite-pulse form of the proven strip encoding `U(s)`.
With at least one background row between strip pairs, Research018 proves that
such strips evolve independently as Rule 90 thereafter.

A **post-interaction reconstitution** is counted only if it occurs at an even
tick strictly after the trajectory has first left the original adjacent code
or changed an exterior row. Record the number of separated strips and each
strip's logical pulse mass.

Interpretation labels, if observed:

- zero strips / empty field: annihilation;
- one separated strip after departure: candidate fold-in;
- two separated strips after departure: candidate transmission/reconstitution;
- more than two separated strips after departure: candidate fan-out.

The words `candidate fold-in` and `candidate fan-out` refer only to this exact
organizational criterion. They do not by themselves establish computation,
logical gates, universality, or a general individuation principle.

## Original adjacent-code membership

At even ticks, `V_0(a,b)` membership requires all changes to lie in rows 0--3
and, block by block, to have the original two-strip pattern:

- row 0 changes only at odd `x=2i+1`, paired with row 1 at even `x=2i`;
- row 2 changes only at odd `x=2i+1`, paired with row 3 at even `x=2i`.

This check uses the entire perturbation, not only decoded logical bits.

## Primary outcome table

For each `d`, assign one descriptive status using this precedence:

1. `annihilated` if exact extinction occurs;
2. `reconstituted-k` if a post-departure separated-strip union appears, with
   `k` the number of strips;
3. `escape-both`, `escape-top`, or `escape-bottom` if the corresponding
   all-time tip certificate appears;
4. `unresolved-through-192` otherwise.

Keep the underlying first-time fields so alternate summaries can be produced
without rerunning the experiment. In particular, a trajectory may both
reconstitute at one time and later escape if the reconstitution criterion was
implemented incorrectly; because separated strips are invariant, that would
signal a bug and must fail validation.

## Secondary structure tests

After the complete census is frozen, exploratory analysis may inspect whether
outcome and first-certificate time correlate with:

- sign and absolute value of `d`;
- parity or residue classes;
- binary / 2-adic structure of `|d|`;
- first contact of the independently evolving Rule-90 pulse supports.

These are post-census pattern searches unless separately preregistered. Any
closed-form law suggested by them must be checked on a fresh displacement
range before being promoted beyond a conjecture.

## Independent audit

Before the first successful census output, commit two instruments:

1. the primary padded-array implementation;
2. an independent sparse infinite-lattice perturbation implementation that
   evaluates the selector law by scalar coordinate lookup against `B_t`.

The audit must agree on every changed coordinate for every `d` through the
earlier of tick 64 or an exact terminal/certificate event, and on every
classification/certificate field at the primary trajectory's stopping time.
For trajectories still unresolved after tick 64, continue the independent
audit through tick 192. If full-coordinate audit through all directly simulated
ticks is inexpensive, retain it.

Any implementation correction made after a failed run must be committed before
rerunning and documented in the final research note.

## Nonclaims

This experiment does not establish behavior for all displacements, arbitrary
pulse shapes, arbitrary adjacent logical rows, other phases or alignments,
other backgrounds, or other physical laws. Failure to reconstitute within the
frozen horizon is not proof that no compact symbolic description exists.
The 3D hypothesis and the separate boundary/individuation thread remain parked.
