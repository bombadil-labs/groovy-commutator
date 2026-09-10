# Frozen protocol: editable routing tables in every dimension

Date: 2026-09-09. This extends the spatial Rail program note after the user authorized making the added instructions editable. Class-IV labels do not inform the construction. This is an exact construction/audit, not a novelty claim or a hypothesis about a privileged physical dimension.

## Declared program language

A dimension-d program is a tuple P=(r,h_2,...,h_d) of d eight-bit words.
At a logical site x, all stages use that site's P:
- b_1 = r[4 S(x-e_1) + 2 S(x) + S(x+e_1)].
- b_j = h_j[4 b_(j-1) + 2 S(x+e_j) + S(x-e_j)], j=2,...,d.
- The new datum is b_d.

Every routing table has all eight entries editable. Its ordered place in the chain and its associated spatial axis are fixed architectural syntax. This is 8d bits, not an arbitrary (2d+1)-input truth table.

Two complete state updates are declared: hold P, or copy the entire old P_(x-e_1) when old S_x=1 and retain P_x otherwise. Data and programs update simultaneously. These modes are fixed interpreter policies.

The canonical added word is M=172: M(b,n,s)=n when b=0, s when b=1.
The first-input projection word is 240. The identity source word is 204.

## Physical layout and total interpreter

Use B,D0,D1,P0,P1, scale nine and one tick per logical step.
In macrocell 9x+{0,...,8}^d:
- the D datum is at 9x;
- bit q of word j (zero-based j=0,...,d-1) is at 9x+(q+1)e_(j+1);
- all other sites are B.

There are 8d+1 occupied sites, 9^d total sites and 9^d-(8d+1) blanks.
This changes the previous last-axis-only placement: the original byte is now along the first axis and each new byte occupies its own added axis. Coordinates, allocation and decoder are explicit. One payload edit still changes one physical symbol.

A D cell reads every word's eight P cells and data at 0 and +/-9e_j. If every required tag is valid, evaluate the chain and retain the D tag; otherwise retain the old symbol. The physical implementation must use a selector-tree evaluator independently of the integer-indexed logical evaluator.

In hold mode P retains itself. In copy mode a P site examines all offsets -k e_j, k=1,...,8 and j=1,...,d. If exactly one position has a D tag, that is its owner. If that owner is D1 and offset -9e_1 has a P tag, copy that symbol; otherwise retain. B always remains B.

On canonical fields a P slot has one owner; other axes retain its nonzero within-block slot coordinate and cannot contain D. The read radius remains nine. The rule is total on malformed fields, without claiming layout repair.

## Lift and guard

Let Q_d=(204,172,...,172). Lift a source pair (P_x,S_x) to (P_x appended with 172,S_x) at new coordinate k=0. At k>0 place (Q_(d+1),0), and at k<0 place (Q_(d+1),1).

Predicted identities for both modes:
- H_d J_d = J_d U_d on all canonical source fields.
- U_(d+1) Ehat_d = Ehat_d U_d on every dimension-d program/data field.
- Physical E_d=J_(d+1) Ehat_d J_d^{-1} consequently intertwines physical updates.

Q_d preserves uniform zero/one by induction. The appended M returns the old source output on the interface's data pair (0,1). Constant guard programs and the constant appended byte are preserved under first-axis copying. The second lift accepts arbitrary edited 2D fields, not just first-lift images. The proof should iterate to every finite d.

## Two action contracts and a retained failure test

Inherited datum/word-bit edits commute with the lift and have single-symbol support. Editing an introduced word is a valid operation in the new dimension. It need not have a lower-dimensional counterpart or preserve the previous lift image. After that edit, the entire new programmed state remains a valid source for the next lift.

Test the stronger, generally false requirement that every possible appended table preserves the same source evolution with the same (0,1) rails. It holds for all sources iff a[1]=0 and a[5]=1: predicted 64 of 256 appended tables. Retain witnesses for each failure. Only M=172 is used for the canonical lift. This is not a restriction on the 256 possible routing words in a source being lifted.

On the canonical interface only addresses 1 and 5 of the newly added table are read. Its other six entries can become causally active on arbitrary new-dimensional data fields. Require explicit arbitrary-field witnesses; do not call dormant interface entries active there.

## Representation versus behavioral identity

Different stored tuples can compute the same local data function. A constant outer table can suppress the inner result, and complementing an inner function while swapping the outer table's b=0/b=1 halves produces aliases.

Predict exactly 30,496 distinct local data functions among 65,536 two-word programs:
16 functions independent of the old three inputs, plus 254 nonconstant inner functions times 240 unequal outer half-pairs divided by two. Exhaust this count. It concerns the one-step data function, not equivalence of complete stored-program states or their response to edits/copying.

Instruction causality means each physical instruction slot has an explicit context in which its edit changes the next datum. It does not mean every instruction is active in every enclosing program.

## Frozen finite audit

1. Check all 256 eight-bit tables on all eight inputs in every stage of dimensions 1,2,3,4 (20,480 physical evaluations). Use constant upstream output and first-input-projection downstream stages to isolate a routing stage.
2. For every dimension/stage/table/address above, flip the addressed physical program symbol and require a changed output, with exactly that one stored symbol changed (20,480 witnesses).
3. Enumerate all 65,536 2D programs and all 32 data stencils through the independent logical evaluator, collect exact local truth tables, check the predicted 30,496 distinct functions and their complement/swap alias.
4. Enumerate every appended byte, both possible inner outputs, and the fixed rails. Retain the predicted 64 neutral words and a (word,inner_output,actual,expected) witness for every failing word. Check M=172 explicitly.
5. Check the canonical lift on all 256 one-word programs and eight data stencils, comparing layers -2..2. At the second interface, check all 65,536 two-word programs and 32 stencils at the central layer; guard layers depend only on the old central datum and can be exhaustively checked separately. Also check Q_d for d=1,...,4 on both uniform states.
6. Exhaust physical word copying at every slot in d=1,...,4 for all own/left payload bits and owner datum values (640 cases). Check missing/multiple owners, invalid neighbor tags, malformed D inputs and B retention. Include owners on different axes.
7. In both hold and copy modes, compare complete physical fields with independent logical evolution and the canonical lift:
   - 8 heterogeneous width-five 1D sources, three ticks, with both 2D and 3D targets;
   - 16 arbitrary 3-by-3 2D program/data sources, four ticks, with a 3D target;
   - 8 arbitrary 2-by-3-by-2 3D sources, three ticks, with a 4D target.
   Use seeds 1..case_count, LCG recurrence (1664525*w+1013904223) mod 2^32, one advance per program word using bits 16..23, then one advance per datum using bit 31, in lexicographic site/stage order.
   Before each tick flip one source datum and one bit in EVERY source program word at the chosen site; apply all corresponding edits physically to source and targets. Site coordinate is (tick+axis) mod source period; bit address is (tick+3*word_index) mod eight.
   Record autonomous source-word changes per stage after interventions, require routing words to change in the copy-mode higher-dimensional families, and require no autonomous program changes in hold mode.
8. Use periodic boundaries only in source directions. Initialize added directions to radius ticks+2, discard one logical guard layer per tick and retain core [-2,2]. Exact sparse-map equality includes all stored P/D tags and the implied blank complement because B remains B.
9. Include a targeted edited-2D-source witness: edit an added table's entry that is dormant on (0,1) rails, choose 2D data that reads that entry, and verify its causal change and its inherited effect after a 3D lift.

Commit this protocol before implementation/evaluation. Commit implementation before execution; record any corrections or deviations, keep this protocol unchanged. Save canonical sorted JSON and require byte-for-byte CI reproduction. The general arbitrary-field/all-time result rests on the local proofs, not finite samples.

## Interpretation and next boundary

Success answers local editability of introduced table contents in the declared fixed-depth chain. It does not establish arbitrary editable syntax, arbitrary program synthesis, self-organized roles, compact storage, independent new-dimensional information, or scientific novelty. The next direction must be chosen from remaining concrete constraints after assessing this result, not from a demand for a Class-IV signature.
