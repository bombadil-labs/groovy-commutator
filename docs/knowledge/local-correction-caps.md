# When can a finite correction stack compute its own missing top correction?

Revision 2026-09-10: partly answered by the [local-cap census](../research/2026-09-10-local-correction-caps.md). All256 fixed homogeneous ECA rules were tested at h=0,1,2 and cap radius R=0,1,2 on complete infinite-lattice causal windows. There are1,094 passing budgets and3,514 saved local conflicts across correction and observation coordinates. The union of passing correction budgets covers135 rules; observation budgets cover150.

Rule32 has an exact two-row logical closure: U'=F_32(U) xor V and V'=F_128(V), with (U,V)=(A_0(S),A_1(S)). The nonconstant missing correction is V_left AND V_right. Induction gives every time, not merely a finite trajectory check. Derivative-only caps fail at tested radii0..2; this does not exclude larger radius.

A larger correction tuple can require a wider cap even when a smaller tuple closes: Rule11 passes h1/R2 and fails h2/R2. K and O preserve the same whole-field information but arrange local inputs differently. Source retention still uses one bit per site; this is not a compression result.

The physical strip and instruction-edit/repair contract are [frozen separately](../research/protocols/rule32-physical-cap-20260910.md), not yet executed. Arbitrary-radius classification, broader cap programs, and semantic recovery after instruction edits remain open. No Class-IV or novelty criterion is used.
