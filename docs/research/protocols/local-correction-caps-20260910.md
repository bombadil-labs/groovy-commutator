# Frozen next experiment: local correction caps versus observation and source controls

Date: 2026-09-10. Status: planned, not executed. This follows the stored correction-transport checkpoint. Its bounded goal is a local factorization census; a physical cap realization is a subsequent task.

## Domain and budgets

For each of the 256 homogeneous fixed ECA laws F on the full infinite binary lattice, define D=I xor F, A_0=D, A_(j+1)=A_j F xor F A_j and B_j=D F^j.
Compare K_h=(A_0,...,A_h) with O_h=(B_0,...,B_h), for h=0,1,2.
For each tuple, test radius R=0,1,2 at the output site.

The cap target is A_(h+1) for K_h and B_(h+1) for O_h. A pass means the target bit is a function of the tuple's (2R+1)-site input patch for every initial source configuration. The corresponding tuple update also uses F of radius one (K) or a shift of components (O). Report both the cap radius and complete-update radius.

Source program r is fixed per case. A computed cap is source-conditioned code; do not claim its table is already a mutable instruction in the existing physical grammar.

## Exhaustive local certificates

A_j and B_j have radius at most j+1. Enumerate every source word on radius

    m = max(h+1+R, h+2).

This covers the full dependence of input patch and target. The largest radius is five, or 11 source bits. No periodic boundary is used.

For each tuple input patch, collect target values:
- one value: the local mapping is consistent;
- both values: retain the first two conflicting source windows and their distinct target bits, in deterministic ascending source-word order.

A consistent map, extended by zero on unrealized input patterns, supplies an exact local cap on the represented image. A conflict refutes only that h,R budget, not larger radius/depth or a different representation. Do not upgrade a finite-window failure to failure of arbitrary whole-field factorization.

Compute correction maps by truth-table composition and independently audit reported certificates using direct shrinking-window evolution/operator recursion. Do not distribute nonlinear F across XOR.

## Controls and reporting

- Recover the established Rule-232 h=0 radius-one derivative closure: D evolves under Rule128. The correction cap is Rule104 on valid derivative neighborhoods because 232 xor128=104.
- Recover constant commutator caps for affine sources, including Rules0,90,204.
- Compare the first passing radius in the tested range for K_h and O_h; report all unsuccessful budgets as bounded failures.
- Report raw represented bits per site (h+1), tuple-patch bits ((h+1)(2R+1)), realized patch counts, preparation radius bound (h+1), cap radius, and worst-case dense cap-table bits (2^((h+1)(2R+1))).
- Source-retention control: S has one bit per site, updates under radius-one F, and permits readout of A_j/B_j with the stated j+1 radius bound. This is an exact baseline, not evidence that correction representations are useless.
- The K/O coordinate change preserves whole-field fibers, not necessarily fixed-radius patches. Interpret different cap radii as local organization of the same whole-field information.
- Record deterministic certificate hashes and realized-pattern counts; the verifier must reconstruct cap tables. Save explicit conflict pairs for every failed budget. Preserve the frozen controls and no class labels.
- Use an exact JSON result with no unbounded or novelty claims. Commit implementation before evaluation; record corrections/deviations rather than rewriting this protocol. CI reproduces the result.
- Do not alter the parallel Erased Distinctions workstream. Reference its already established closure results as controls instead of reclassifying them as new findings.

## Next decision

After the census, identify a nonconstant cap beyond the known derivative-closure controls that has a compact representable program, or record that none was found within budget. Then freeze its physical implementation and instruction-edit contract separately. A successful local lookup factorization alone does not establish that the existing table-chain interpreter can execute the cap.
