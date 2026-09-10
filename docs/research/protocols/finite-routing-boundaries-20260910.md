# Frozen protocol: finite routing boundaries with explicit occupancy

Date: 2026-09-10. This follows the editable-routing note and the approved plan to reduce prepared boundary resources before returning to commutator correction closure. No Class-IV or novelty criterion is used.

## Fixed physical law; expanded typed source space

Do not change verify_editable_routing_tables.py or its total physical interpreter H_d in either hold/copy mode. Retain B,D0,D1,P0,P1, scale nine, radius nine and the program tuple (r,h2,...,hd).

The native source is now (Omega,P,S), with an arbitrary fixed subset Omega of Z^d, a d-word program and a datum at each occupied logical site. Encode complete scale-nine macrocells only at sites in Omega: D at 9x, eight P slots along each axis, all other sites B. Missing macrocells are entirely B.

Logical dynamics V_d:
- Omega is fixed.
- A datum updates by the existing table-chain evaluator only if all required +/-e_j neighbor sites belong to Omega; otherwise it retains its value.
- Hold retains P. Copy replaces the complete P_x with old P_(x-e1) iff old S_x=1 and x-e1 belongs to Omega; otherwise retain P_x.
- All reads use the old state. Only datum/program payload edits at occupied sites are in the action contract. No occupancy edits, creation, or tag repair are claimed.

The expected physical realization is H_d J_d = J_d V_d. Occupancy is already encoded by B versus D/P, not an additional physical alphabet symbol. The decoder must retain that distinction; B is not logical zero.

## Finite lift

Set Omega' = Omega times {-1,0,1}.
At (x,0), store (P_x appended with M=172, S_x).
At (x,+1), store (Q_(d+1),0); at (x,-1), store (Q_(d+1),1), where Q_d=(204,172,...,172).
Everything outside Omega' is blank.

Predicted identity: V_(d+1) Ehat_d = Ehat_d V_d in both modes, for every occupied-source field.
- New guard data retain themselves because the outward new-axis neighbor is absent.
- Central data have all old-axis neighbors iff the source did. If complete, the new table receives (b,0,1) and returns b; otherwise both retain the old datum.
- Central copies have exactly the same left-neighbor presence and gate as the source; the appended word is constant.
- Guard copies either copy the same constant tuple or retain it at a missing left neighbor.

This is a new boundary mechanism under the unchanged total law: missing inputs freeze a datum. It is not external clamping and not self-organization. The guard truth table need not execute to stabilize the guard datum.

Because arbitrary masks are native, the same construction can repeat: Omega times {-1,0,1}^k. It accepts edited masked fields, not only canonical images of the first lift.

## Resource and minimality claims to prove

Each lift prepares three occupied macrocells per occupied source macrocell. After k lifts from dimension d, the occupied-site count per initial occupied logical cell is 3^k [8(d+k)+1].
The added-axis support is three logical layers, or 27 physical coordinate positions for the complete-macrocell layout; all sites beyond that band are blank. For an infinite source this is finite transverse thickness, not finite total support.
The full allocated macrocell volume per initial occupied site is 3^k 9^(d+k). The background outside is the uniform absorbing B state.

An inherited data/instruction edit still changes one physical cell per represented target; it does not edit the guards. Preparation reads one source macrocell, including its occupancy. Inverting J_d is block-local on the declared image.

At least three new-axis macrocell layers are needed for a changing central datum under this unmodified all-inputs-required interpreter, fixed coordinate placement and one-tick contract: the central site needs both its +/-e_new data neighbors. This is not a lower bound for other laws, encodings, cadences or partial guard layouts.

## Two retained failure controls

A. Missing-as-zero completion: replace absent old-dimensional macrocells with occupied (Q_d,0) before lifting, while decoding back only original occupied sites. An isolated source datum should retain itself, while the completed neighborhood can update it. Test all 256 ECA words and both central data values with absent left/right neighbors. Predict 256 of 512 data cases fail, and exactly 64 words pass both data cases (bit0=0, bit2=1). Retain all failure records and the concrete word-255, datum-zero witness. Hold mode supplies the full census; that witness also fails copy mode because its old gate is zero.

B. Insufficient guard thickness: under the same interpreter, use new-axis layer sets {0}, {-1,0}, {0,1}. Test word 255 on an all-zero width-three source. Its source datum changes to one; a missing transverse neighbor freezes the target central datum at zero. Retain these three failures. The full {-1,0,1} construction is the predeclared rescue, not a post-outcome change.

## Frozen audit

1. Verify the occupied-source local datum update and its lift for all 256 ECA words, both central data values, and each left/right status in {absent,0,1}: 4,608 cases. Compare physical source center, physical target center, and both target guards to the independent logical rule. Present neighbors carry identity programs. Data behavior is common to hold/copy; program behavior is audited separately.
2. Run both retained failure controls exactly as above.
3. Exhaust local program copying with present/absent left macrocell, owner datum 0/1 and own/left payload 0/1 for every slot of every stage in dimensions 1..4 (1,280 cases). Reuse the unchanged physical interpreter; do not replace its type guards by an idealized logical operation.
4. In both modes, run each of these six field families with eight deterministic seeds and four ticks:
   - full width-five 1D torus, targets 2D,3D,4D;
   - width-five 1D torus occupied at positions 0,1,3, targets 2D,3D;
   - full 3-by-3 2D torus, targets 3D,4D;
   - 3-by-3 2D torus missing (0,0) and (1,2), targets 3D,4D;
   - 2-by-3-by-2 3D torus missing (0,0,0) and (1,2,1), target 4D;
   - nonperiodic finite 1D support {0,1,2,4}, targets 2D,3D.
   Generate all occupied sites in lexicographic order using seed 1..8 and LCG (1664525*w+1013904223) mod 2^32; advance once per stage, use bits16..23, then once per datum, use bit31.
   Before each tick choose occupied source site at sorted index tick mod |Omega|, flip its datum and one bit (tick+3*stage) mod eight in each source word. Apply exactly matched physical edits in source and targets.
   Compare all occupied D/P symbols, the fixed occupied support, and the entire implied blank complement after every tick; there is no shrinking halo, clamp, or discarded guard layer.
   Count autonomous source-program changes per stage after interventions; require every stage to change in each copy-mode family and no stage to change in hold mode. Count data changes separately.
5. In both modes, take the first seed of the full width-five 1D family, lift it to 2D, then edit guard datum (0,1) and entry0 of that guard's routing table. Treat this altered 2D field as a source and lift it into 3D. Verify complete fields through four ticks, without requiring continued correspondence to the old 1D source.
6. Verify occupancy decoding, one-cell inherited edit support, exact 3^k macrocell growth and full physical support cardinality in every field case. Verify the B-center rule on a neighborhood containing nonblank cells in every dimension through four.

Commit protocol before implementation, and implementation before execution. Save sorted canonical JSON, including retained failures, with no protocol rewriting. Record corrections/deviations explicitly. CI must reproduce it byte-for-byte. General arbitrary-field/all-time claims rest on the local proofs.

## Next research target

After this boundary unit, return to correction closure. Formulate a bounded local closure experiment on K_h=(A_0,...,A_h), with A_0=D=I xor F and A_(j+1)=A_j F xor F A_j. Distinguish a closed tuple from a repeated individual correction map. Compare against retaining the complete source and against the equivalent forward-observation tuple, while counting preparation radius, storage, update radius and allowed edits. Do not infer infinite-lattice closure from finite-ring collisions. This protocol does not predeclare the results of that next experiment.
