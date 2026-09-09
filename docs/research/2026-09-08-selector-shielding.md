# Selector-relative shielding: interaction can create a causal diode

**Research checkpoint, 2026-09-08.** This note is deliberately unnumbered while another research session is landing work in parallel. It is stacked on the pulse-shape scattering branch and follows the frozen [shielding](protocols/selector-shielding-20260908.md) and [dyadic confirmation](protocols/selector-shielding-dyadic-20260908.md) protocols.

Research021 found a state just outside its preregistered four-site shape family with a qualitatively new fate. The upper side escapes, but the lower outer Rule-90 row remains bit-for-bit identical to the isolated lower strip even though the neighboring inner row is already strongly contaminated.

The concrete witness is

\[
A=\{-5,0\},\qquad B=\{0,1,3,4,6\},
\]

with `A` encoded in rows 0/1 and `B` in rows 2/3.

The main result of this checkpoint is an **exact reduction** of the shielding question. For an exact lower strip, the outer row reads the inner row at exactly the inner-row sites whose reference value is one. Therefore, as long as the lower half-plane is still equal, the outer row stays equal for one more tick **if and only if** the coupled inner row never turns a reference `1` into `0`.

For the witness, all directly checked inner-row damage has the opposite polarity: it is `0 -> 1`. A fresh dyadic prediction at tick 256 passed exactly under two independent update implementations. The remaining open step is to prove that this one-sided damage polarity persists for all time.

## Fixed system

Use the Research018–021 selector law

\[
F(X)(y,x)=X\bigl(y+2X(y,x)-1,\;x+X(y,x-1)+X(y,x+1)-1\bigr)
\]

against the exact alternating background

\[
B_t(y,x)=(x\bmod2)\oplus(t\bmod2).
\]

Let `C_t` be the coupled witness trajectory and `L_t` the isolated lower-strip trajectory started only from `B` in rows 2/3.

## Exact strip geometry gives a selector identity

For an isolated exact two-row strip, the physical perturbations on the inner and outer rows remain paired at every fine phase:

\[
\delta^L_t(2,q)=\delta^L_t(3,q-1).
\]

The alternating background flips between adjacent horizontal sites,

\[
B_t(q)=1\oplus B_t(q-1),
\]

so the complete physical values satisfy the diagonal complement relation

\[
L_t(2,q)=1\oplus L_t(3,q-1).
\]

The outer-row perturbations occupy only the background-zero parity. Hence any zero on row 3 has two one-valued horizontal neighbors. If

\[
L_t(3,x)=0,
\]

then the row-3 destination `(3,x)` has center zero and horizontal neighbor sum two, so its selected source is exactly

\[
(2,x+1).
\]

By the diagonal complement relation,

\[
L_t(2,x+1)=1.
\]

Conversely, if `L_t(2,q)=1`, then `L_t(3,q-1)=0`, so destination `(3,q-1)` selects `(2,q)`.

Therefore:

> **Exact selector identity.** Along an isolated exact strip, row 3 reads row 2 at exactly the horizontal sites where row 2 has value `1`. It never reads an inner-row zero.

This is stronger and cleaner than the original coordinate-set diagnostic.

## Shielding is exactly inner-row dominance

Assume at fine time `t` that the coupled and isolated trajectories agree on every row `y>=3`.

Then the complete row-3 neighborhoods are equal, so coupled and reference row-3 cells choose the same source coordinates.

- A row-3 cell with value `1` selects row 4. Those sources are equal by the lower-half-plane hypothesis.
- A row-3 cell with value `0` selects a row-2 source whose isolated value is exactly `1`, by the selector identity above.

Thus row 3 remains equal at `t+1` exactly when every isolated row-2 one remains a coupled row-2 one:

\[
C_t(2,x)\ge L_t(2,x)\qquad\text{for every }x.
\]

All rows `y>=4` remain equal automatically because their selectors and all possible source rows are already contained in the equal lower half-plane.

So, while shielding holds at time `t`,

\[
\boxed{
\text{lower half-plane equal at }t+1
\iff
C_t(2,\cdot)\ge L_t(2,\cdot)
}
\]

for this exact-strip reference.

Equivalently, coupled/reference row-2 differences may be `0 -> 1` but never `1 -> 0`.

The converse is operationally sharp: a first `1 -> 0` inner-row difference is read by the corresponding outer-row destination on the next tick, so shielding breaks one tick later.

This is the core theorem of the checkpoint. The all-time witness question is now the much narrower statement

\[
C_t(2,\cdot)\ge L_t(2,\cdot)\quad\forall t.
\]

## The two upper pulses repair damage that each creates alone

The shield is genuinely interaction-generated.

With the same lower shape `B={0,1,3,4,6}`:

- upper shape `{0}` first creates a `1 -> 0` row-2 difference at fine tick 7 and the lower boundary differs at tick 8;
- upper shape `{-5}` first creates a `1 -> 0` row-2 difference at tick 9 and the lower boundary differs at tick 10;
- the combined upper shape `{-5,0}` has no `1 -> 0` row-2 difference in the independently checked prefix through tick 256, and direct dense exploration continues the shielding through tick 512.

At the first failure of `{0}` alone, the harmful row-2 destination reads row 1 at a source that interaction has changed from reference `1` to `0`. In the combined `{-5,0}` trajectory, the nonlinear interaction residual restores that same source to `1`, preventing the negative row-2 defect.

So the second pulse is not a passive extra input. The response of the pair is not the XOR/superposition of the responses of the two pulses separately; the nonlinear residual cancels precisely the causal leakage that would break the lower boundary.

Two exploratory specificity checks, performed after the shielding lead was already known, reinforce that this is not a generic large-state effect:

- among upper pairs `{0,k}` with `-16<=k<=16`, `k!=0`, only `k=-5` remained lower-shielded through tick 48 for this `B`;
- among all 64 lower shapes contained in logical sites `0..6` and containing site `0`, only `{0,1,3,4,5}` and `{0,1,3,4,6}` remained shielded through tick 32 for upper `{-5,0}`.

These are exploratory bounded searches, not classification theorems.

## The interface has an exact dyadic form

The shielding trajectory showed a much stronger regularity at dyadic fine times.

For `t=32,64,128`, shift horizontal coordinates into the left-moving frame

\[
u=x+t.
\]

The coupled/reference difference on rows 0, 1 and 2 had exactly the same parameterized form.

Row 2:

\[
\Gamma_t^{(2)}=
\{u=2,4,\ldots,2t\}\setminus\{8\}\cup\{13\}.
\]

Row 1:

\[
\Gamma_t^{(1)}=
\{-10,0,1,4,6,11\}
\cup
\{12\le u\le2t-4:u\bmod8\in\{0,4,6\}\}.
\]

Row 0:

\[
\Gamma_t^{(0)}=
\{-9,1,6,9,12,14,16,18\}
\cup
\{24\le u\le2t-6:u\bmod8\in\{0,2\}\}
\cup
\{2t-4,2t-2,2t+1\}.
\]

After these formulas were written down, the [fresh tick-256 protocol](protocols/selector-shielding-dyadic-20260908.md) froze the complete coordinate prediction.

It passed exactly:

| Check at tick 256 | Predicted | Observed |
| --- | ---: | ---: |
| row-0 difference mass | 133 | 133 |
| row-1 difference mass | 193 | 193 |
| row-2 difference mass | 256 | 256 |
| extra coordinates | 0 | 0 |
| missing coordinates | 0 | 0 |

The dense cropped-field and independently written sparse scalar implementations agree on every complete coupled and reference field through the entire prefix: **514 complete fields and 2,257,852 changed-point comparisons**. No negative row-2 difference and no lower-half-plane difference occurs through tick 256.

The saved [result](../../results/selector_shielding_dyadic_20260908.json) retains the exact pass and source hashes.

## Why dyadic times are natural here

At even fine time `t=2^{k+1}`, the isolated lower strip has taken `2^k` coarse Rule-90 steps. Over `GF(2)`, Rule 90 has the Frobenius identity

\[
(z+z^{-1})^{2^k}=z^{2^k}+z^{-2^k}.
\]

Therefore a finite lower seed becomes two translated copies of the original seed at those coarse times. The large region between them is exact background.

The dyadic interface formula has the same decomposition:

1. a finite left contact structure locked to the left-moving Rule-90 edge;
2. an expanding period-8 wake through the middle;
3. a finite right contact structure locked to the right-moving edge.

At tick 256 the row-2 coupled state is actually a solid run of ones from `x=-246` through `x=256`. This is one visible slice of the shielding mechanism.

## Moving boundary walls have period 32

Post-confirmation analysis shows that the edge structures are not only dyadic snapshots.

In the left-moving frame `u=x+t`, a fixed interface window on rows 0/1/2 repeats with period 32:

\[
W_{t+32}(u)=W_t(u)
\]

for every directly checked `t` from 32 through 224. The analogous right-moving frame also has period 32.

Because the complete dense and sparse fields agree through tick 256, this period analysis is not an implementation disagreement, although the moving-frame observation itself is post hoc.

The period is plausibly tied to the finite inward depth of the Rule-90 edge coefficients used by the contact structure: fixed-depth binomial parities have power-of-two periods.

This suggests an exact proof route based on two traveling boundary walls plus a generated interior domain rather than on arbitrary long brute-force evolution.

## A causal-diode phase

The interaction wake contains large regions of the all-ones state.

The uniform state `X=1` is an exact fixed point of the physical law. More importantly, a cell with center value one selects vertically **downward** and, in an all-one neighborhood, diagonally down-right. Thus information in an all-one region is supplied from below; perturbations above are not read downward through that phase.

This gives a physical interpretation to the dominance lemma. The interaction between the two upper pulses and the lower strip nucleates a state whose selectors orient causal flow away from the protected boundary. The growing wake is therefore not merely extra mass. It acts as a **causal diode**.

The phrase is descriptive, not yet a general phase classification. The exact proven statement remains the selector/dominance lemma above.

## Relation to blocking words and walls

Classical one-dimensional CA theory uses **blocking words** for finite patterns that interrupt information flow, and later work considers directional/right-blocking words and blocking walls along moving curves. The present object rhymes strongly with that literature but is not literally the standard definition:

- the physical CA here is two-dimensional;
- the protected object is a particular evolving lower strip trajectory;
- the blocking structure is interaction-generated and moves with the strip edges;
- the exact criterion is selector-relative rather than purely geometric.

A useful working term is therefore **selector-relative blocking wall** or **trajectory-conditioned blocking wall** until the relation is formalized.

## What remains unproved

The frozen 1024-tick dual-kernel protocol was attempted, but the monolithic scalar implementation exceeded the local execution ceiling before producing a result. The scientific horizon and witness were not changed. A separate fresh dyadic check was used instead because tick 256 is tractable under both independent kernels.

The following are **not yet proved**:

- `C_t(2)>=L_t(2)` for all fine times;
- the dyadic row formulas for every power of two;
- the period-32 moving-wall identity for all time;
- a general classification of which pulse pairs nucleate shielding;
- that the all-ones wake is a blocking phase under arbitrary perturbations.

The strongest next move is an exact finite proof of the moving-wall / dominance invariant. A successful proof would turn the witness into the first example in the project of

\[
\text{interaction}\longrightarrow\text{new causal boundary}\longrightarrow\text{protected continuing organization}.
\]

That is closer to the original fan-out/fold-in intuition than the earlier scattering census: interaction does not merely emit more objects; it **changes which physical differences are dynamically visible to an existing object**.

The parallel observation-closure research is conceptually adjacent: both are about when discarded or nearby distinctions cease to matter for a continuing effective state. This branch does not modify that work.

The 3D hypothesis remains parked.
