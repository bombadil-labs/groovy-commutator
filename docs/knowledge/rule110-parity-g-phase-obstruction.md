# Rule 110 parity+Groovy hides a phase wall that future Groovy can reveal

For Rule 110 under nonoverlapping block-2 parity at cadence two, current
centered Groovy is sufficient to correct the **next parity readout**, but the
complete current pair \((P,G^\circ)\) is not an autonomous state.

An explicit infinite-line pair has identical entire current parity and Groovy
fields while its next Groovy fields differ. The two source configurations differ
by a half-line blockwise complement mask, exposing the missing distinction as a
hidden **block phase domain wall**.

The next parity readout on the seven required literal coordinates has exact
minimum algebraic degree three. Among all cubic off-image extensions, the
sparsest ANFs have nine monomials.

Adding the block-phase gradient

\[
\Phi_j=X_{2j}\oplus X_{2j+2}
\]

repairs full present-time autonomy:

\[
W_j=(P_j,G^\circ_{2j},G^\circ_{2j+1},\Phi_j)
\]

has an exact radius-two induced law on the full admissible Rule-110 source
image.

But this repair is nearly microscopic. \(P\) and \(\Phi\) alone reconstruct
the source up to one global complement bit, so the autonomous repair retains
all but at most one source bit on a connected line or ring.

This specializes the earlier Groovy-field result that source gradients are a
universal repair and connects directly to the six-field lift's gradient rails.

The resulting hierarchy is exact:

1. parity alone is compressed but needs history;
2. parity + centered Groovy repairs the next parity readout but is not
   self-updating;
3. parity + Groovy + block-phase gradient is autonomous but nearly reconstructs
   the microscopic source.

Source: [Rule 110 parity-G closure](../research/2026-10-07-rule110-pg-closure.md).
