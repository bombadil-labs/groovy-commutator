# Six-cell blocks implement Rule 90 exactly

The fixed ternary 2D interpreter admits the injective block encoding

$$
E(s_i)=\begin{pmatrix}s_i&1\\0&1\\0&1\oplus s_i\end{pmatrix},
\qquad F^2E=E\phi_{90}.
$$

Blocks tile horizontally and repeat with vertical period three. The identity
holds for every logical input on the infinite line or any ring. A logical
flip toggles two physical cells per vertical period, preserving arbitrary
matched action/update words. This is an exact simulation of an update that
combines two neighbors, beyond transport alone.

Six is the smallest block area admitting a multi-input affine elementary
target in the frozen area-at-most-six, cadence-one-to-three, fixed-frame
search. It is not an unrestricted minimality result. No arbitrary-damage
repair, universality, or compatibility through further dimensions is proved.
See the [full experiment](../research/2026-09-08-block-compatibility.md).
