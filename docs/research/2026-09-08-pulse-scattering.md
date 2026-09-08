# Every single-pulse encounter launches outward fronts

For the fixed adjacent-strip architecture, changing only the horizontal displacement of one upper and one lower Rule-90 pulse does **not** produce a menu of annihilation, confinement, and reconstitution outcomes. The position census found something more rigid: every tested displacement eventually leaves the four-row adjacent code and launches persistent extreme-row supports in both vertical directions.

A fresh non-overlapping range obeys exact arithmetic formulas for the departure time, first exterior-row time, and extreme-front multiplicity. A subsequent finite contact-template audit reduces the result to the possible local Rule-90 edge geometries and supports the all-integer statement for this single-pulse family.

This is the first useful scattering law in the project. It is also a negative result for the original fan-out/fold-in search: **single-bit pulse position alone is too rigid a control parameter**. The next useful variation is pulse shape/state.

## Fixed system

Keep the binary 2D law from Research018/019,

$$
F(X)(y,x)=X\bigl(y+2X(y,x)-1,\;x+X(y,x-1)+X(y,x+1)-1\bigr),
$$

with alternating background

$$
B_t(y,x)=(x\bmod2)\oplus(t\bmod2).
$$

The upper Rule-90 strip occupies rows 0/1 and the lower strip rows 2/3. Put one lower logical pulse at index 0 and one upper logical pulse at integer index $d$. At even phase the complete perturbation is

$$
\delta_0(d)=\{(0,2d+1),(1,2d),(2,1),(3,0)\}.
$$

The [frozen discovery protocol](protocols/pulse-scattering-20260908.md) varies only $d$. The physical law, background, pulse shapes, vertical placement, horizontal phase, and sampling conventions stay fixed.

## Discovery census: position does not choose the qualitative fate

The frozen domain was every integer

$$
-64\le d\le64,
$$

with direct evolution through fine tick 192 unless an exact extinction or persistent singleton-tip certificate terminated the run earlier.

The preregistered primary labels were:

| Frozen status | Displacements |
| --- | ---: |
| `escape-both` | 113 |
| `unresolved-through-192` | 16 |
| annihilated | 0 |
| post-departure separated-strip reconstitution | 0 |

The 16 unresolved cases were not confined. They were exactly

$$
d=-3,-7,-11,\ldots,-63,
$$

for which the first exterior row contains a **doublet** rather than the singleton required by the original certificate. The original protocol therefore did the right thing by leaving them unresolved.

The independent sparse scalar audit agrees with the primary changed-coordinate fields on **7,399 complete ticks and 21,287,358 changed points** across the full discovery domain. The primary trajectory file was materialized per displacement after a monolithic process exceeded the execution ceiling; the frozen per-displacement logic and criteria were unchanged. The scalar audit's hardest shard was similarly subdivided only for execution and then reaggregated.

The [summary](../../results/pulse_scattering_20260908_summary.json), [independent audit](../../results/pulse_scattering_20260908_audit.json), and [compact primary observables](../../results/pulse_scattering_20260908_primary_metrics.json) retain the result. The publication file stores the frozen per-tick scalar and membership observables in columnar arrays rather than repeating JSON field names; its column schema is embedded in the file. Full top/bottom support coordinates and per-tick coordinate digests were used during the run and independent audit but are not duplicated in this smaller publication copy; first-event extreme coordinates are retained in the fresh-range and proof-audit records.

## The singleton certificate generalizes to any transmitting extreme support

Research019 proved that if row $r$ is the topmost changed row at time $t$,

$$
\delta_{t+1}(r-1,x)=B_t(x)\,\delta_t(r,x-1),
$$

and for the bottommost changed row,

$$
\delta_{t+1}(r+1,x)=\bigl(1\oplus B_t(x)\bigr)\,\delta_t(r,x+1).
$$

The earlier witness used a singleton extreme cell. The same argument does not require a singleton.

Let $A$ be the horizontal support of a nonempty topmost changed row. If

$$
B_t(a+1)=1\qquad\text{for every }a\in A,
$$

then the next topmost support is exactly $A+1$, one row higher. Every point keeps the same transmitting parity, so the whole support repeats this diagonal translation forever. The bottom statement is analogous: if $B_t(a-1)=0$ for every bottom support point, the full support translates one row down and one column left forever.

Applying this generalized certificate at the first exterior tick resolves all 16 former doublet exceptions. **All 129 discovery displacements have proved two-sided unbounded vertical escape.** The extreme supports are singletons in 113 cases and doublets in 16.

This does not say that the growing interior wake is simple. It says that its two outer boundary channels are exact and permanent once launched.

## An arithmetic scattering law

The discovery census suggested exact launch-time formulas.

For $d>0$,

$$
T_{\rm depart}(d)=
\begin{cases}
d,&d\equiv0\pmod2,\\
d+1,&d\equiv1\pmod2,
\end{cases}
$$

while for $d\le0$, write $n=-d\ge0$ and

$$
T_{\rm depart}(d)=
\begin{cases}
n+2,&n\equiv0\pmod2,\\
n+1,&n\equiv1\pmod2.
\end{cases}
$$

The first exterior-row time is

$$
T_{\rm ext}(d)=
\begin{cases}
d+6,&d>0,\ d\equiv0\pmod4,\\
d+3,&d>0,\ d\equiv1\pmod4,\\
d+4,&d>0,\ d\equiv2\pmod4,\\
d+3,&d>0,\ d\equiv3\pmod4,\\
n+6+(n\bmod2),&d\le0,\ n=-d.
\end{cases}
$$

At that tick the top and bottom extreme supports have the same mass,

$$
m(d)=
\begin{cases}
2,&d<0\text{ and }d\equiv1\pmod4,\\
1,&\text{otherwise}.
\end{cases}
$$

Their locations also form a small residue-sensitive alphabet:

| Displacement class | Top support at first exterior tick | Bottom support |
| --- | --- | --- |
| even $d$ | $\{d+4\}$ | $\{d-3\}$ |
| positive odd $d$ | $\{d+3\}$ | $\{d-2\}$ |
| negative $d\equiv3\pmod4$ | $\{d+1\}$ | $\{d\}$ |
| negative $d\equiv1\pmod4$ | $\{d+3,d+5\}$ | $\{d-4,d-2\}$ |

Here the supports list horizontal coordinates; the first exterior rows themselves are $y=-1$ and $y=4$. Each listed support satisfies the transmitting-parity condition and therefore propagates outward forever with its shape preserved.

The scattering data are therefore not just “escape happened.” Relative position leaves an exact arithmetic signature in *when* the boundary channels launch and, for one residue class, in their multiplicity.

## Fresh range: every frozen prediction passes

After the discovery formulas were written down, the [fresh-range protocol](protocols/pulse-scattering-residue-20260908.md) froze a non-overlapping domain,

$$
d\in[-256,-65]\cup[65,256].
$$

That gives 384 new displacement values. For every one, the dense physical-field implementation and the independently written sparse scalar implementation were required to agree on every changed coordinate through first exterior change, while the observed departure time, exterior time, extreme mass, and transmitting parity had to match the frozen formulas.

All **384/384** cases pass. The two implementations agree on **64,032 complete fields** comprising **4,677,264 changed-point comparisons**. Of the fresh cases, 336 launch singleton extreme supports and 48 launch doublets, exactly as predicted. There are no formula failures.

Together with the discovery range, the computation directly checks every integer displacement from $-256$ through $256$, while preserving the discovery/confirmation split. The saved [fresh-range result](../../results/pulse_scattering_20260908_fresh_range.json) contains every observed and predicted scalar, the actual extreme coordinates, and a canonical field digest.

## Why this is not merely a 513-case pattern

The finite validation suggests the law; the all-integer step comes from the local contact geometry.

Before the two logical fronts overlap, each single Rule-90 pulse has the usual edge facts: the outer coefficient is always one, and the first inward coefficient is the coarse-time parity. At first contact, every integer displacement therefore reduces to one of four oriented edge geometries with one binary edge-parity parameter. The longest relevant post-contact causal depth is eight fine ticks.

The post-census [contact-template verifier](../../scripts/verify_pulse_scattering_templates.py) exhausts all three deeper inward bits on each logical row across that full causal depth. For each of the eight direction/parity templates, all $2^6=64$ assignments give the same departure/exterior result and a transmitting extreme support. That is **512/512 contact assignments**.

Negative even displacement has one special interaction one coarse tick before the coincident-edge template. The verifier separately exhausts 128 assignments and shows that this interaction cancels exactly back into the expected $V_0$ Rule-90 image before the final contact. Thus it changes the delay but not the eventual launch.

The verified local outcomes are:

| Contact template | Edge parity | Exterior offset | Top support | Bottom support |
| --- | ---: | ---: | --- | --- |
| positive-even | 0 | 6 | $\{4\}$ | $\{-3\}$ |
| positive-even | 1 | 8 | $\{4\}$ | $\{-3\}$ |
| positive-odd | 0 or 1 | 4 | $\{4\}$ | $\{-1\}$ |
| negative-odd | 0 | 8 | $\{2\}$ | $\{1\}$ |
| negative-odd | 1 | 8 | $\{4,6\}$ | $\{-3,-1\}$ |
| negative-even | 0 or 1 | 6 | $\{4\}$ | $\{-3\}$ |

The contact time and Rule-90 edge parity are fixed by the sign and residue of $d$. Substituting them into these finite templates gives the formulas above. Because every integer displacement reaches one of these templates, and every template reaches a transmitting top and bottom support, the result extends beyond the finite validation range:

> **For every integer relative displacement $d$, one upper and one lower single-bit Rule-90 pulse in this fixed adjacent-strip architecture leave the original adjacent code and launch nonempty extreme supports that propagate vertically outward forever.**

This is an exact statement about this pulse family, not a universality claim.

## What happened to fan-out / fold-in?

The first scattering experiment was deliberately conservative: keep both pulse shapes fixed and vary only relative position. That parameter turns out to control **delay and boundary signature, not qualitative fate**.

Within the frozen discovery census there is:

- no annihilation;
- no post-departure exact reconstitution into separated Rule-90 strips;
- no position that remains vertically confined;
- no position-dependent choice between those fates.

So displacement alone does not give the hoped-for fan-out/fold-in repertoire. Instead it gives something arguably more useful: a clean incoming-family / interaction / outgoing-boundary law on which a richer scattering theory can be built.

The two outward extreme supports are exact outgoing channels. The interior wake is additional unresolved structure. For this family the channel count does not increase: two incoming pulses produce a top and bottom boundary channel. The doublet class shows that an outgoing channel can nevertheless carry a nontrivial shape bit tied to arithmetic residue.

## The next experiment should vary pulse shape

The position census has removed one degree of freedom from the mystery. The next control parameter should be the logical state of the incoming organizations.

A useful finite search is to normalize translations and enumerate small nonempty logical pulse shapes $A$ and $B$ in the two adjacent strips, then vary their relative displacement only far enough to cover distinct first-contact geometries. For each encounter, record:

- extinction;
- departure from $V_0$;
- exact separated-strip reconstitution;
- persistent top/bottom boundary supports and their shapes;
- additional persistent fronts if they appear;
- whether the same incoming shapes at different offsets share a scattering signature;
- whether distinct incoming states map to the same outgoing signature, or one state maps to several exact outgoing organizations.

That is where candidate fold-in and fan-out become state-dependent rather than merely geometric. The current result gives both a baseline and a cheap exact certificate for recognizing one important outgoing channel.

The 3D hypothesis remains parked.
