# Four-site pulse shapes all launch both boundaries

Research020 showed that changing the **position** of two adjacent single-bit Rule-90 pulses changes their exact scattering signature but never their qualitative fate: every integer displacement launches persistent top and bottom boundary supports.

Research021 asks whether changing the finite **logical state** of the incoming strips is enough to produce a richer scattering repertoire.

Inside the frozen four-site shape family, the answer is no. Every one of the 1,600 preregistered encounters launches persistent supports in both vertical directions. None annihilates, none returns to the exact separated-strip family, and therefore this bounded family contains no candidate fold-in or fan-out under the declared organizational criterion.

The negative result is stronger than the single-pulse census but still bounded. A post-census widening immediately exposed a more interesting state just outside the frozen family: one-sided escape with a causally shielded outer Rule-90 row. That lead is recorded separately below and is not part of the Research021 claim.

## Frozen family

Use the same physical law, alternating background, phase, and adjacent two-strip encoding as Research020. For a finite logical support `S`, the even-phase strip beginning at row `j` is

\[
U_j(S)=\{(j,2i+1),(j+1,2i):i\in S\}.
\]

Translation-normalize every incoming logical shape so that its minimum occupied site is zero, then take the eight nonempty normalized shapes contained in four logical sites:

\[
\mathcal H_4=\{S\subseteq\{0,1,2,3\}:0\in S\}.
\]

For every ordered pair `(A,B)` in `H_4 x H_4`, place the lower shape at logical origin and displace the upper by every integer

\[
-12\le d\le12.
\]

That gives

\[
8\times8\times25=1600
\]

frozen initial conditions. The [protocol](protocols/pulse-shape-scattering-20260908.md) was committed before evaluation.

The dense cropped-field evolution and the independently written sparse infinite-lattice evolution had to agree on every complete changed-coordinate set at every directly simulated tick.

## Exact terminal vocabulary

The census did not infer outcomes from visual appearance.

Three kinds of terminal event were allowed:

1. **Extinction.** An empty perturbation is exactly the background trajectory forever.
2. **Separated-strip reconstitution.** After genuine departure from the original adjacent code, an even-time field that becomes a finite union of exact two-row `U_j(S)` strips separated by at least one background row stays in that family forever by the Research018 buffer theorem. One outgoing strip would be a candidate fold-in; three or more would be a candidate fan-out.
3. **Two-sided persistent escape.** The Research019/020 extreme-row identity certifies a nonempty extreme support forever once every point lies on its transmitting parity. When both top and bottom certificates have appeared, the trajectory cannot later return to the stationary-row separated-strip family.

Failure to reach a certificate by tick 128 would have remained unresolved.

## All 1,600 cases escape both ways

The primary result is maximally simple:

| Terminal status | Cases |
| --- | ---: |
| `escape-both` | **1,600** |
| `annihilated` | 0 |
| any `reconstituted-k` | 0 |
| `unresolved-through-128` | 0 |

Every one of the 64 ordered shape pairs escapes both ways at every one of the 25 frozen offsets.

Although the horizon was fine tick 128, no case needed it: the latest two-sided terminal certificate occurred at fine tick **21**.

The 25 singleton/singleton controls reproduce Research020 exactly within the shared displacement range, including its departure times, first-exterior times, and singleton/doublet boundary supports.

The saved [summary](../../results/pulse_shape_scattering_20260908_summary.json) identifies the complete raw run by SHA-256; the committed frozen instrument reproduces every trajectory.

## Shape changes the outgoing boundary signature

The qualitative fate is rigid, but the outgoing boundary channels are not.

At the first persistent top certificate, the support masses are:

- 1 cell in 1,513 cases;
- 2 cells in 86 cases;
- 3 cells in one case.

For the bottom certificate the corresponding counts are 1,506, 93, and one.

Across both sides there are **16 distinct paired normalized boundary signatures** in the frozen family. The rare three-cell examples are

\[
A=\{0,1,2,3\},\quad B=\{0,1,2\},\quad d=0
\]

with top normalized support `{0,4,6}`, and its opposite-side counterpart

\[
A=\{0,1,2\},\quad B=\{0,1,2,3\},\quad d=1
\]

with bottom normalized support `{0,2,6}`.

So finite state already carries more information into the outgoing boundary geometry than the single-pulse residue law did. What it does **not** do, in this bounded family, is change the exact terminal class.

## Independent audit

After the primary census, a second classifier was committed and then evaluated. It uses the sparse update kernel, reconstructs every initial condition independently, recomputes original-code membership, separated-strip reconstitution, and persistent extreme-support certificates, and checks every stored field digest.

It agrees on all **1,600/1,600** cases, covering

- **18,290 complete fields**;
- **439,718 changed-point comparisons**;
- every departure time;
- every first exterior time;
- every top and bottom persistent-support certificate;
- and the absence of extinction or separated-strip reconstitution.

The [audit summary](../../results/pulse_shape_scattering_20260908_audit.json) records the source hashes and zero mismatches.

## What this says about fan-out / fold-in

The original hope was that interaction might look like

\[
\text{exact organizations}\rightarrow\text{nonclosed interaction}\rightarrow\text{different exact organizations}.
\]

Research021 does not find that transition in the declared small-shape family. Increasing the logical state space from one pulse to every translation-normalized four-site support still leads to two-sided outward escape.

That is useful narrowing. Position was too weak a control parameter; **small finite state is also too weak**.

But it would be a mistake to promote that bounded regularity into an all-shape theorem.

## Post-census lead: one-sided causal shielding

After the frozen census was complete, an exploratory local-contact widening allowed six inward logical bits on each side. This is outside the Research021 family and was not preregistered as a confirmatory test.

It immediately produced valid finite adjacent-strip states whose two vertical boundaries behave differently.

One example is

\[
A=\{-5,0\},\qquad B=\{0,1,3,4,6\}.
\]

Direct evolution through fine tick 128 shows:

- the top side launches outward and reaches row `-123` by tick 128;
- the bottom side never changes below row `3`;
- the outer row `y=3` is **bit-for-bit identical at every fine tick 0 through 128** to row `3` of the isolated lower Rule-90 strip started from `B`;
- row `2` nevertheless diverges strongly from that isolated strip;
- through the same interval, those row-2 differences never occupy a source address actually selected by the row-3 update.

A second nearby lower shape, `{0,1,3,4,5}`, has the same observed shielding, and mirror examples protect the upper boundary while the lower side escapes.

This is not yet an all-time theorem. It is a much more fertile next question than continuing to enlarge the brute-force shape window blindly:

> Can interaction damage accumulate immediately beside an exact organization while remaining forever outside that organization's dynamically selected causal inputs?

If yes, the relevant boundary is not spatial separation. It is **selector-relative causal separation**.

That would connect the strip experiments back to the project's earlier neighborhood-selector and provenance results: a physical difference can be present, nearby, and growing, while remaining dynamically absent from a particular continuing process because the process never reads it.

Research022 should isolate and prove or refute that shielding mechanism.

The 3D hypothesis remains parked.
