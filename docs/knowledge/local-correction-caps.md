# When can a finite correction stack compute its own missing top correction?

Revision 2026-09-10: partly answered by the [local-cap census](../research/2026-09-10-local-correction-caps.md) and the completed [Rule32 physical realization](../research/2026-09-10-rule32-physical-cap.md).

The full-shift census tests all256 fixed homogeneous ECA rules at h=0..2 and R=0..2 in correction and observation coordinates. It retains1,094 passing budgets and3,514 local conflicts. The union of passing correction budgets covers135 rules; observation budgets cover150. These bounded failures do not exclude wider neighborhoods or other representations.

Rule32 has an exact two-row logical and physical closure: U'=F_32(U) xor V and V'=F_128(V), with(U,V)=(A_0(S),A_1(S)). Its missing correction is V_left AND V_right. Stored programs and finite guards give the complete physical identity at every time. Derivative-only caps fail at tested radii0..2; no arbitrary-radius exclusion or compression claim follows.

K and O preserve identical whole-field information while requiring different local radii. Adding correction rows can make the next local cap wider; Rule11 passes h1/R2 and fails h2/R2.

The physical audit now also preserves all1,360 matched native edits. That is not semantic repair. The finite odd-ring data edits recover on extinguishing baselines, while a persistent full-lattice counterexample has indefinitely expanding top-row disagreement. Broader cap programs, arbitrary-radius classification and deliberate semantic program revision remain open. No Class-IV or novelty criterion is used.
