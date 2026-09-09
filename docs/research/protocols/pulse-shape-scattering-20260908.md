# Pulse-shape scattering census protocol — 2026-09-08

## Status

Frozen before evaluating any member of the shape census below.

Research020 established an exact scattering law for one upper and one lower **single-bit** Rule-90 pulse in the fixed adjacent-strip architecture: every integer relative displacement launches persistent outward extreme supports. Relative position changes the timing and boundary signature, not the qualitative fate.

Research021 changes one thing: the finite logical state carried by each incoming strip. The physical law, background, strip encoding, phase, vertical placement, and interpretation of exact reconstitution remain fixed.

## Question

Can the logical **shape/state** of two finite adjacent-strip organizations change their qualitative scattering fate?

In particular, does this bounded shape family contain exact witnesses of:

- annihilation;
- reconstitution into one separated Rule-90 strip after genuine interaction (`candidate fold-in`);
- reconstitution into two separated strips (`transmission/reassembly`);
- reconstitution into three or more separated strips (`candidate fan-out`);
- or persistent outward boundary channels without separated-strip reconstitution?

The labels `candidate fold-in` and `candidate fan-out` refer only to the exact organizational criterion below. They do not imply a general logical gate, universality, or a theory of individuation.

## Fixed physical system

Use the Research018–020 binary 2D law

\[
F(X)(y,x)=X\bigl(y+2X(y,x)-1,\;x+X(y,x-1)+X(y,x+1)-1\bigr)
\]

against the alternating exact background

\[
B_t(y,x)=(x\bmod2)\oplus(t\bmod2).
\]

At even phase, a finite logical set `S` encoded in the two-row strip beginning at row `j` has perturbation

\[
U_j(S)=\{(j,2i+1),(j+1,2i):i\in S\}.
\]

The upper strip occupies rows 0/1 and the lower strip rows 2/3.

For an ordered pair of logical shapes `(A,B)` and relative displacement `d`, initialize

\[
\delta_0(A,B,d)=U_0(A+d)\cup U_2(B),
\]

where `A+d={a+d:a in A}`. The lower shape is the translation anchor.

## Frozen logical shape family

Translation-normalize each finite shape so that its minimum occupied logical index is zero. Enumerate every nonempty normalized shape contained in four logical sites:

\[
\mathcal H_4=\{S\subseteq\{0,1,2,3\}:0\in S\}.
\]

There are exactly eight shapes:

- `{0}`
- `{0,1}`
- `{0,2}`
- `{0,3}`
- `{0,1,2}`
- `{0,1,3}`
- `{0,2,3}`
- `{0,1,2,3}`

Keep the upper/lower ordering. Thus there are 64 ordered shape pairs. Do not quotient by reflection, strip exchange, complement, or any post-hoc symmetry.

## Frozen displacement and time domain

For every ordered `(A,B)` pair enumerate every integer

\[
-12\le d\le12.
\]

The census therefore contains

\[
8\times8\times25=1600
\]

initial conditions.

Attempt direct evolution through fine tick 128 inclusive unless an exact terminal certificate below is reached earlier.

The displacement window is a bounded discovery family, not a claim that larger offsets are equivalent. Research020 already shows that contact parity can retain arithmetic information about displacement.

## Complete-field cross-check

At every directly simulated tick, evolve the same perturbation with both already-established Research020 implementations:

1. the cropped dense physical-field update;
2. the independently written sparse infinite-lattice scalar update against analytic `B_t`.

They must agree on the **complete changed-coordinate set** at every tick. Any disagreement invalidates the run.

This reuses two update kernels independently audited in Research020; the new variables are the finite shape state and outcome classification.

## Original adjacent-code membership

At even ticks, `V_0` membership means the complete perturbation is still exactly two logical Rule-90 strips in rows 0/1 and 2/3 with the declared paired-cell encoding. Membership is tested on the whole physical field, not just a decoder.

Record the first even tick strictly after zero on which `V_0` fails. Call it `T_depart`.

Also record the first tick containing any changed cell outside rows 0 through 3.

## Exact separated-strip reconstitution

At an even tick, call the perturbation a finite union of separated Rule-90 strips iff its nonempty rows partition into adjacent pairs `(j,j+1)` such that:

1. distinct row pairs have at least one entirely background row between them;
2. top-row changes occur only at odd columns;
3. bottom-row changes occur only at even columns; and
4. within each pair, `(j,2i+1)` is changed iff `(j+1,2i)` is changed.

This is the finite-pulse form of the exact `U_j(S)` encoding. Research018 proves that row pairs separated by at least one background row then evolve independently as Rule 90 forever.

Count a **post-interaction reconstitution** only at an even tick strictly after the trajectory has first left `V_0` or changed an exterior row.

If such a state appears, record every strip row pair and logical support and terminate the trajectory with an exact certificate:

- one strip: `reconstituted-1` / candidate fold-in;
- two strips: `reconstituted-2` / transmission or reassembly;
- three or more strips: `reconstituted-k` / candidate fan-out.

Because the separated-strip union is invariant under the fixed law, no later finite simulation is required for that fate.

## Exact extinction certificate

If the perturbation becomes empty, the physical state equals the exact background trajectory. Extinction is permanent. Record `annihilated` and terminate.

## Generalized persistent extreme-support certificate

Reuse the exact Research019/020 extreme-row identities. If row `r` is the topmost changed row at fine time `t`,

\[
\delta_{t+1}(r-1,x)=B_t(x)\,\delta_t(r,x-1).
\]

If `A` is the horizontal support of that row and

\[
B_t(a+1)=1\quad\text{for every }a\in A,
\]

then the whole nonempty support translates one row upward and one column right forever, preserving its shape.

Likewise, for the bottommost support `C`, if

\[
B_t(c-1)=0\quad\text{for every }c\in C,
\]

then it translates one row downward and one column left forever.

Record the first top and bottom persistent-support certificates separately. If both have appeared, terminate with `escape-both` unless a separated-strip reconstitution certificate occurred first at the same tick.

A persistent outward extreme support is incompatible with later reconstitution into the stationary-row separated-strip family: its extreme row changes vertically at every fine tick, while every exact separated Rule-90 strip remains in its fixed row pair. Thus a two-sided persistent-support certificate is an exact terminal fate for the present classification.

Do not infer confinement from failure to find a persistent-support certificate.

## Frozen primary status

Assign one terminal descriptive status using the first applicable exact event:

1. `annihilated`;
2. `reconstituted-k` for a post-interaction exact separated-strip union;
3. `escape-both` after both persistent extreme-support certificates;
4. `unresolved-through-128` otherwise.

Also retain first top-only and bottom-only persistent-support times even when the trajectory remains unresolved at the horizon.

## Recorded observables

For each case retain at least:

- canonical identifiers for `A`, `B`, and `d`;
- perturbation mass and bounding box per directly simulated tick;
- complete-field digest per tick;
- `V_0` membership at even ticks;
- first `V_0` departure and first exterior-row time;
- first top and bottom persistent-support times;
- extreme supports at their first certificates, normalized by horizontal translation as well as in absolute coordinates;
- extinction time if any;
- post-interaction separated-strip reconstitution time and complete strip logical supports if any;
- terminal status and stopping reason.

## Frozen controls

The 25 cases with `A=B={0}` must reproduce Research020 within this displacement window:

- no annihilation;
- no post-departure separated-strip reconstitution;
- the Research020 departure and first-exterior formulas;
- the Research020 singleton/doublet persistent extreme-support signatures.

Any control failure invalidates the census.

## Post-census analyses

Only after the complete census and cross-check are frozen may exploratory analysis ask:

- which shape pairs admit distinct primary fates as `d` changes;
- whether any exact fold-in, fan-out, annihilation, or transmission witnesses exist;
- the smallest witness under total logical mass, span, then lexicographic tie-break;
- whether persistent boundary-support signatures cluster by shape invariants, displacement residues, or Rule-90 contact state;
- whether distinct incoming `(A,B,d)` states share the same exact outgoing separated-strip state or boundary signature;
- whether a smaller contact-template description appears possible.

Any new all-offset or all-shape law inferred from the bounded census requires a separately frozen validation or proof.

## Nonclaims

This experiment does not classify shapes wider than four normalized logical sites, offsets outside `[-12,12]`, other phases, vertical gaps, backgrounds, encodings, or physical laws. Failure to reconstitute by tick 128 does not prove that no other symbolic description exists. Persistent boundary channels are not automatically `fan-out`; candidate fan-out requires exact reconstitution into more than two separated strip organizations under the declared criterion.

The 3D hypothesis remains parked.
