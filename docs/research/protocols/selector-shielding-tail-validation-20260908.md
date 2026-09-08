# Fresh shielding-tail validation — 2026-09-08

## Status

Frozen after the 512-case targeted shielding-family census and its post-census decision-tree analysis, but before evaluating any lower state containing logical site 7 or 8.

## Discovery law being tested

For upper state

\[
A=\{-5,0\},
\]

the discovery family contained all lower states `B subset {0,...,6}` with `0 in B`.

Across all 64 such lower states, the first negative inner-row defect obeyed the exact decision tree

\[
T_{\rm neg}=4 \quad\text{if } b_1=0,
\]

\[
T_{\rm neg}=5 \quad\text{if } b_1=1\text{ and }(b_2=1\text{ or }b_3=0),
\]

\[
T_{\rm neg}=8 \quad\text{if } b_1=1,b_2=0,b_3=1\text{ and }(b_4=0\text{ or }(b_5=b_6=0)),
\]

\[
T_{\rm neg}=15 \quad\text{if }(b_1,b_2,b_3,b_4)=(1,0,1,1)\text{ and }b_5=b_6=1,
\]

with no negative defect through fine tick 64 exactly when

\[
(b_1,b_2,b_3,b_4)=(1,0,1,1),\qquad b_5\oplus b_6=1.
\]

In every unshielded discovery case the first lower-half-plane difference occurred exactly one fine tick after the first negative row-2 defect.

## Fresh family

Keep `A={-5,0}`. Enumerate the same 64 assignments of bits `b1,...,b6`, with `b0=1`, and append one of three nonempty tail patterns:

- `{7}`;
- `{8}`;
- `{7,8}`.

Thus every validation state contains at least one logical site absent from the discovery family. The fresh domain has

\[
64\times3=192
\]

cases.

## Frozen predictions

The bits at sites 7 and 8 are predicted to be irrelevant to the first shielding decision through tick 64.

For every fresh case:

1. `T_neg` must equal the discovery decision tree above;
2. if `T_neg` is finite, the first lower-half-plane difference must occur at `T_neg+1`;
3. if the discovery tree predicts no negative defect, neither a negative row-2 defect nor a lower-half-plane difference may occur through tick 64.

Therefore exactly **6/192** fresh cases are predicted to be `shielded-through-64`: the two good six-bit prefixes crossed with the three tail patterns.

No formula may be repaired after seeing the fresh results.

## Implementation audit

Use the same dense and independently written sparse kernels as the discovery census. They must agree on every complete coupled and reference changed-coordinate field through tick 64. Execution may be sharded by tail pattern without changing the frozen domain or predictions.

## Nonclaims

Success establishes finite-horizon locality with respect to sites 7 and 8 for this alignment. It does not prove arbitrary-tail irrelevance, all-time shielding, or an infinite logical language. Those require a contact-cone proof or further fresh validation.
