# Fresh-range pulse-scattering law protocol — 2026-09-08

## Status and purpose

This protocol is frozen **after** inspecting the Research020 census on
`-64 <= d <= 64` and **before** evaluating any displacement outside that
range. It is therefore a confirmatory follow-up, not part of the original
census.

The first census suggested that encounter geometry does not choose between
escape and confinement for this pulse family. Instead, every observed
encounter eventually leaves the four-row adjacent code, while relative
horizontal displacement controls the launch time and the shape of the two
extreme fronts.

This follow-up tests the resulting arithmetic scattering law on a fresh,
non-overlapping displacement range.

## Fixed system and pulses

Keep exactly the Research020 law, alternating background, adjacent strips,
phase, and single-bit pulses. The lower pulse remains at logical index 0 and
the upper pulse at index `d`:

\[
\delta_0(d)=\{(0,2d+1),(1,2d),(2,1),(3,0)\}.
\]

No decoder, law, alignment, or pulse shape is fitted to the new range.

## Fresh domain

Test every integer

\[
d\in[-256,-65]\cup[65,256].
\]

None of these 384 displacements occurs in the discovery census.

For each `d`, simulate only until the first tick on which a changed cell lies
outside rows 0 through 3. Before that event, also record the first even tick at
which the complete field is no longer in the original adjacent code `V_0`.

Two already-committed implementations must agree on every complete changed
coordinate at every simulated tick:

1. the cropped dense physical-field update from
   `experiment_pulse_scattering.py`;
2. the independent sparse infinite-lattice scalar update from
   `audit_pulse_scattering.py`.

## Frozen predictions

### First adjacent-code departure

For positive `d`, predict

\[
T_{\rm depart}(d)=
\begin{cases}
d,& d\equiv0\pmod2,\\
d+1,& d\equiv1\pmod2.
\end{cases}
\]

For negative `d`, write `n=-d>0` and predict

\[
T_{\rm depart}(d)=
\begin{cases}
n+2,& n\equiv0\pmod2,\\
n+1,& n\equiv1\pmod2.
\end{cases}
\]

The sign asymmetry is part of the prediction.

### First exterior-row change

For positive `d`, predict

\[
T_{\rm ext}(d)=
\begin{cases}
d+6,& d\equiv0\pmod4,\\
d+3,& d\equiv1\pmod4,\\
d+4,& d\equiv2\pmod4,\\
d+3,& d\equiv3\pmod4.
\end{cases}
\]

For negative `d`, again write `n=-d` and predict

\[
T_{\rm ext}(d)=n+6+(n\bmod2).
\]

Thus negative even displacements add 6 fine ticks and negative odd
displacements add 7.

### Extreme-front multiplicity

At the first exterior tick, predict equal top and bottom extreme-row masses

\[
m(d)=
\begin{cases}
2,& d<0\text{ and }d\equiv1\pmod4,\\
1,& \text{otherwise}.
\end{cases}
\]

The `m=2` cases are the discovery census's former singleton-certificate
exceptions.

### Generalized persistent-front certificate

Research019 proved, for a topmost changed row `r`,

\[
\delta_{t+1}(r-1,x)=B_t(x)\,\delta_t(r,x-1),
\]

and analogously at the bottom,

\[
\delta_{t+1}(r+1,x)=(1\oplus B_t(x))\,\delta_t(r,x+1).
\]

A post-census deduction generalizes the singleton witness. If a nonempty
extreme-row support `A` lies entirely on the transmitting parity —
`B_t(a+1)=1` for every top-row `a in A`, or `B_t(a-1)=0` for every bottom-row
`a in A` — then the whole support translates outward by one diagonal step.
The same parity condition is invariant at the next tick, so the shape repeats
forever by induction.

The fresh-range prediction is that **both** first exterior rows satisfy this
certificate for every tested displacement. Therefore every fresh encounter is
predicted to have proved two-sided unbounded vertical escape at its first
exterior tick, whether the extreme shape is a singlet or doublet.

## Acceptance criteria

The predicted scattering law passes this fresh test only if, for all 384
new displacements:

- dense and sparse implementations agree on every changed coordinate through
  first exterior change;
- observed `T_depart` equals the frozen formula;
- observed `T_ext` equals the frozen formula;
- top and bottom extreme masses both equal `m(d)`; and
- both extreme rows satisfy the generalized persistent-front certificate.

Save every per-displacement observed and predicted scalar, plus the actual
first-exterior extreme coordinates and canonical field digest. Any mismatch is
reported individually; do not repair the formula in place.

## Nonclaims

A successful test supports this exact single-pulse scattering family, not
arbitrary pulse shapes, phases, adjacent logical data, or laws. The formulas
may motivate an all-integer proof, but finite validation alone is not such a
proof. Front multiplicity carrying residue information is not by itself a
logical gate or a complete scattering algebra.
