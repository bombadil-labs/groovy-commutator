# Protocol: coexistence and interaction of two finite strips

Freeze before evaluation. Keep the ternary 2D law F, alternating background
B(y,2i)=0, B(y,2i+1)=1, and U's horizontal alignment from Research017.
Place independent logical rows a,b in strips starting at y=0 and y=2+g,
with g=0,1,2,3,4 background rows between. A strip beginning at y=j has
rows j=(0,1 XOR s_i), j+1=(s_i,1). All other rows remain B. Call the combined
injective encoding V_g(a,b). No horizontal phase search or fitted decoder.

## Complete local comparison

At cadence two, exhaust all 64 assignments to
(a_left,a_center,a_right,b_left,b_center,b_right), bit indices0..5 in that order.
Initial columns -2..3 and rows -4..g+7 shrink twice to output columns0..1,
rows -2..g+5. This covers every possibly changed vertical row and the complete
horizontal causal cone for a central output block. The result extends to all
logical inputs and widths by locality, for each tested gap.

Decode candidate a' and b' from the even-column cells in the lower row of
each strip, but accept a pair only if the ENTIRE physical output equals its
V_g encoding, including all constant cells and background rows. Report:

1. Whole code preserved for every input, with the exact 64-entry pair table.
2. Whether that update equals independent Rule90 on each row.
3. When the code fails, all failed input indices and deterministic witnesses.

Record the complete physical outputs and the composition residual
C_g = F^2 V_g(a,b) XOR V_g(phi90(a),phi90(b)). Enumerate every physical output
and residual cell's Boolean algebraic normal form. Record essential input
variables, mixed monomials involving both rows, and cross-strip influence
on each strip's physical cells. These are physical interaction measures;
invalid outputs are not silently promoted to a logical gate or coupled rule.

Save the first-tick central-block field as well. Use its exact formulas to
explain any minimum separating gap. Any all-gap or arbitrary-number-of-strips
claim requires a local buffer-row argument, not extrapolation from g<=4.

## Independent audit and finite actions

Commit both local instruments before evaluation. An independent Boolean
truth-set implementation represents the 64 inputs by bits of uint64 words
and uses an explicit multiplexer, with its own encoder and validity check.
Compare every output, residual, validity decision, influence list and ANF;
independently recover coefficients by subset parity and reconstruct truth
tables. Retain negative outcomes.

For gaps1/2, if an exact independent update is established, corroborate four
coarse steps for all pairs of logical states on rings of widths5/7. At gap1
and width5, enumerate all length-three action words over no action, top-cell0
flip, bottom-cell0 flip, and both. Logical flips change the two designated
physical cells only. Sufficient vertical causal padding avoids a vertical
torus; horizontal wrap is exactly the declared logical ring. Compare every
fine physical field with the independently packed Boolean update and every
coarse state with package Rule90 applied separately to each logical row.

The local identity plus matched-action identities then establish arbitrary
finite action words by induction. Their finite tests are corroboration.
If separated independence fails, retain its counterexample and skip that
case's action-preservation claim.

## Scope

The question is how the given representations compose in a single unchanged
physical law. It is not a search over all possible inter-strip couplings,
an experiment on 3D, or proof of computational universality. If adjacent
strips leave this code, a larger representation may still describe them;
no unrestricted impossibility claim follows. Any follow-up beyond this
protocol must be marked as such.
