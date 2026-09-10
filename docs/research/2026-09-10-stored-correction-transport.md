# Stored instructions execute correction transport, but a zero cap does not close it

The dimensional control construction now executes the actual commutator correction-transport law. With program tuple (r,60), the unchanged physical interpreter computes

\[
U'_k(x)=F_r(U_k)(x)\oplus U_{k+1}(x).
\]

Both the ECA rule r and the transport table are stored in physical program cells. This removes the earlier interior-law limitation of keeping r only in a source-specific ambient rule.

It does **not** establish indefinite finite correction closure. A prepared finite stack remains correct inside its expected space-time triangle. A frozen zero cap can send an error down that stack, reaching the bottom at tick three in the retained example.

The next test is a local cap depending on the represented corrections, not a longer fixed padding.

## The transport instruction is word 60

The [editable table grammar](2026-09-09-editable-routing-tables.md) first computes b=F_r on a row, then reads a stored table on (b,n,s), where n is the datum in the next correction row. Under address 4b+2n+s, word 60 is

\[
h_{60}(b,n,s)=b\oplus n.
\]

It ignores the negative-axis value, though the interpreter still requires a valid data tag at that input. Therefore complete interior macrocells with tuple (r,60) implement the displayed law exactly under H_2.

The [finite-boundary construction](2026-09-10-finite-routing-boundaries.md) supplies the physical setting: five symbols, radius nine, 17 occupied sites per 2D macrocell and one tick per logical step. Here programs are held, with one homogeneous r per source case. Autonomous program changes and semantic repair after reprogramming are not included in this extension.

## The represented corrections and the finite guarantee

Use the [established correction convention](2026-09-09-correction-future-coordinates.md):

\[
A_0=I\oplus F,\qquad
A_{k+1}=A_k\circ F\oplus F\circ A_k.
\]

Here A_1 is the Groovy commutator. Prepare rows 0 through H with U_k(0)=A_k(S), and add zero-data guard rows at -1 and H+1. Give all these rows complete (r,60) programs; leave all other macrocells blank.

The two outer guard rows retain their data because an outward input is absent. Every represented correction row has the data tags needed to execute the interior law.

**Finite-transport theorem.**

\[
U_k(t)=A_k(F^t(S))\qquad\text{whenever }k+t\le H.
\]

**Proof.** The claim holds initially by preparation. If k+t+1<=H, then both rows k and k+1 are correct at t. Their physical update gives

\[
F(A_k(F^t(S)))\oplus A_{k+1}(F^t(S))
=A_k(F^{t+1}(S)).
\]

This is exactly the correction identity, with no linearity assumption. ∎

For ECA, preparing A_k has a radius bound k+1 in the initial source. Increasing H therefore increases both storage and preparation radius; the proof does not provide a pre-existing unknown future for free. The derivative representation may also be noninjective, so this is not an embedding of the complete source state.

## A stationary boundary can carry the wrong information

The zero cap is physically stable. That says nothing about whether zero equals the next required correction.

For F equal to Rule 255, F maps every field to ones. A_0(S) is the complement of S, A_1 is all ones, A_2 is all zeros and A_3 is all ones. With H=2, the cap incorrectly supplies zero instead of A_3.

Start with an all-zero source. The following table shows spatially uniform row values; the true correction rows after the first source step are always (0,1,0).

| Tick | Actual row 0 | Actual row 1 | Actual row 2 | Rows already wrong |
| --- | ---: | ---: | ---: | --- |
| 0 | 1 | 1 | 0 | None |
| 1 | 0 | 1 | 1 | 2 |
| 2 | 0 | 0 | 1 | 1, 2 |
| 3 | 1 | 0 | 1 | 0, 1, 2 |

The cap error reaches each lower row one tick later. All sites remain valid physical program/data cells; the failure is semantic, not loss of the layout.

This refutes the zero-cap choice as a universal closure for this H. It does not rule out a different cap. Rule 255 itself needs no unbounded correction stack: its constant corrections give straightforward exact alternatives.

## Separately frozen audit

This extension was frozen after the finite-boundary audit passed. Its [protocol](protocols/stored-correction-transport-20260910.md) was committed at [c48a52e](https://github.com/bombadil-labs/groovy-commutator/commit/c48a52e5d7bab7b5fa0d7b4e8125b3968506f9eb), and its [implementation](../../scripts/verify_stored_correction_transport.py) before execution at [9b509ec](https://github.com/bombadil-labs/groovy-commutator/commit/9b509ec40bc784402e5a6e746a24848ac624bd61). There were no corrections or deviations.

    python scripts/verify_stored_correction_transport.py > /tmp/stored-correction-transport.json
    diff -u results/stored_correction_transport_20260910.json /tmp/stored-correction-transport.json

The [saved result](../../results/stored_correction_transport_20260910.json) records:

- all 8,192 combinations of ECA rule and five-bit 2D data stencil, comparing the physical program interpreter with the explicit transport expression;
- all 256 rules and all eight width-three source states, prepared through H=2 and run for four ticks;
- 2,088,960 complete physical-symbol comparisons, with unchanged support and stored instructions;
- all 18,432 protected-triangle bit comparisons passing;
- 1,258 of the 2,048 finite cases showing a bottom discrepancy by tick four, outside the protected guarantee;
- the exact Rule-255 failure timeline.

The entire verifier passes **51,202 assertions**. The periodic census counts only its declared finite cases; it is not an estimate of rule prevalence, evidence of a class boundary, or a proof of infinite-lattice closure. The transport theorem supplies the general finite-triangle guarantee.

## The next test: a locally computed cap

The established finite-closure condition is

\[
A_{h+1}=g_h\circ K_h,\qquad
K_h=(A_0,\ldots,A_h).
\]

If g_h is local on the represented image, the top row can update by F(A_h) xor g_h(K_h) and the whole finite tuple closes. The next [frozen local-cap protocol](protocols/local-correction-caps-20260910.md) is not yet executed.

It compares all 256 ECA source rules, correction depths h=0,1,2 and cap radii R=0,1,2, using full causal windows on the infinite binary lattice rather than periodic closure inference. For each budget it either constructs the complete realized local cap map or retains conflicting source windows.

Two controls prevent an easy but misleading success interpretation:

1. The corresponding forward-observation tuple O_h=(D,DF,...,DF^h) has the same whole-field information as K_h. Its finite-radius closure cost can differ; that is a representation/locality comparison.
2. Retaining the original source S always gives exact source evolution with one bit per site and radius one for a fixed ECA. Deriving correction outputs still has a preparation/readout cost. An autonomous correction tuple is not automatically a storage improvement over this baseline.

A logical cap certificate would be the next result, not the end of the physical question. Its lookup-table size, program representation, permissible edits, and realization in the stored-program architecture must then be accounted for. This is the intended return from the routing control to commutator closure.
