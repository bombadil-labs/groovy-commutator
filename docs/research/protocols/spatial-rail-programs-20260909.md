# Frozen protocol: spatial Rail programs with a separate guard program

Date: 2026-09-09. This protocol follows the user's clarification that Class IV is background motivation only. No class label or desired selectivity informs this construction. An architecture-specific failure is not a general obstruction; revisions must state what changes and retain the previous result.

## Native programs and complete logical dynamics

G_1 consists of eight-bit ECA programs r, with address q=4l+2c+rbit. G_(d+1) consists of Rail(p), p in G_d. Equivalently a dimension-d program has eight editable leaf bits and d-1 fixed Rail constructors.

At each logical site x there is a program P_x in G_d and one binary datum S_x. Programs are retained between explicit edits:

    U_d(P,S) = (P, T_d(P,S)).
    T_1(P,S)(x) = P_x[4 S(x-e1) + 2 S(x) + S(x+e1)].
    T_(d+1)(P,S)(x,k) =
        S(x,k+1) if evaluation of P_(x,k)'s inner program
                      on the central d-dimensional data slice is 0,
        S(x,k-1) otherwise.

Every nested evaluation uses the program of the updated site, not a neighbor's program. This is a family with program retention, not arbitrary autonomous self-modification. Program edits are external finite local operations on this same state; they do not select a new ambient law.

## Physical storage and fixed interpreter

Use the same five-symbol alphabet in every dimension:

    B, D0, D1, P0, P1.

For each logical x in Z^d, its physical macrocell is 9x + {0,...,8}^d. Put D(S_x) at 9x and the eight program bits P(q) at 9x+(q+1)e_d, q=0,...,7. Every other site is B. Thus the program word is laid along the last spatial axis at every dimension.

The uniform physical CA H_d has Chebyshev radius nine:
- B and P symbols copy themselves.
- A D site reads its eight P slots in the positive last-axis direction and data symbols at offsets 0 and +/-9 e_j.
- If all required slots/taps have their declared types, evaluate the dimension-d Rail program from the eight stored payloads and the data taps, and retain the D tag.
- On malformed input, retain the center symbol.

The tag is explicit stored state, never inferred from absolute coordinates. The complete ambient CA is defined on every five-symbol field. The theorem concerns the invariant canonical macrocell layout. It uses one physical tick per logical tick, no hidden clock, no external clamp, and no unrestricted truth-table compiler.

Storage costs: 9^d physical cells per logical cell, nine occupied symbols, 9^d-9 blanks; five-symbol alphabet; radius nine. This generous fixed layout is a proof-oriented first candidate, not an optimized binary radius-one realization.

Let J_d denote this layout. It is injective and has a block-local decoder on its image. One source datum edit or one program-bit edit changes one physical symbol.

## Two predeclared boundary variants

For the logical lift into dimension d+1, use data S at k=0, zeros at k>0, and ones at k<0. Program constructors gain one Rail wrapper.

Variant A, repeated source programs: copy each source P_x to every transverse layer, wrapped in Rail. This requires infinitely many target program edits for one source-program edit. At d=1 it has the earlier endpoint obstruction; for homogeneous ECA sources exactly 64 are predicted to pass.

Variant B, separate guard program: at k=0 retain the source program's eight bits, wrapped in Rail. At every other layer use the fixed guard g=204, with the native number of Rail wrappers. The guard is chosen because ECA 204 is the identity, not from its dynamical class. No guard fitting by source is allowed.

More generally the first-interface guard condition is g(000)=0 and g(111)=1. This predicts 64 admissible guard words and success for every source program field when one is used. At subsequent interfaces every Rail program already preserves both uniform values, so the same g=204 works.

Call Variant B Ehat_d. The complete target identities to prove are

    U_(d+1) Ehat_d = Ehat_d U_d
    H_d J_d = J_d U_d.

The physical dimensional lift is J_(d+1) Ehat_d J_d^{-1} on the canonical layout. This takes an arbitrary valid dimension-d programmed field as source, not just one previously produced by a lift.

## Inheritance and interventions

The program object at the data interface is Rail(p); its eight leaf payloads occupy exactly the eight new-axis program cells. Dimension fixes the wrapper depth; wrapper choices are not extra mutable instructions.

With every transverse data pair set to (0,1), nested selectors recover any desired source leaf bit. Require a counterfactual witness for each of eight local program-bit changes at dimensions one, two, and three, under the same H_d.

Under Variant B a local program or datum edit maps to one edited target symbol at each interface. Preserve arbitrary finite sequences of evolution and declared local payload edits by the two commuting identities. Edits of role tags or arbitrary malformed layouts are outside the action contract.

## Fixed audit

Use an independent scalar logical evaluator and a physical symbol/coordinate interpreter.

1. Exhaust all 256 programs and all effective binary data stencils at dimensions 1,2,3: 8,32,128 stencils respectively. Check physical/logical agreement and all source-instruction recovery witnesses.
2. Check Variant A for all 256 homogeneous sources and the three interface positions -1,0,1 plus distant backgrounds; retain its 64-rule result and its nonlocal program-edit support.
3. For every pair (source r, guard g), enumerate all eight first-interface source neighborhoods and layers -2..2. Predict all 256 sources pass for exactly the 64 two-quiescent guard words. Use g=204 for subsequent experiments.
4. At the second interface exhaust all 256 source-program words and all 32 effective 2D data patches at layers -2..2. These patches are arbitrary valid source fields, not only first-lift images.
5. Physical field audit: width-three source rings, all 256 homogeneous programs and all eight source states, through three ticks and both lifts. Use five transverse logical layers [-2,2] as the compared core, initialize enough guard layers to shrink safely each tick. Compare all data and all eight program payloads of every retained macrocell, and canonical tags/blanks.
6. Repeat a bounded heterogeneous-program/action audit on width-five sources: 16 deterministic program/state fields, four ticks, one data flip and one instruction flip before every tick. Verify both physical lifts against direct source evolution.
7. Test the second interface independently on arbitrary 3-by-3 programmed source tori: 32 deterministic program/data fields, three ticks, with matched local edits. This supplies an implementation check for the stronger arbitrary-source theorem.
8. Verify the physical malformed-layout rule on missing program slots, bad data taps, and every center-symbol class. This checks the declared total CA, without claiming error correction.

Record every protocol deviation and implementation correction. Save canonical sorted JSON; CI must reproduce it byte-for-byte. Do not report a successful native program-family construction as a preferred physical encoding, self-reproduction, a Class-IV discriminator, or a binary radius-one result.
