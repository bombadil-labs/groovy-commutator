# Added routing instructions can be edited, executed, and lifted again

The next construction makes the contents of every added routing instruction explicit program data. A dimension-d program now has d eight-bit tables: the original ECA table and one table for each added axis. Every table entry occupies one physical cell.

The complete system still lifts exactly: execution, inherited local edits, and state-gated copying of whole programs commute with the same construction. This holds for arbitrary native source program/data fields, including fields whose added routing tables have already been edited. Local proofs establish every finite dimension; the frozen audit checks physical execution through dimension four.

The remaining fixed resources are clear: the order of the table chain, its axis assignments, protected symbol roles, a prepared scale-nine layout, and infinite guard backgrounds. Table contents are editable; arbitrary syntax and geometry are not.

## What changed from the previous checkpoint

The [spatial Rail witness](2026-09-09-spatial-rail-programs.md) stored eight ECA leaf bits but made each added selector a fixed part of the interpreter. The new grammar stores the added selector's truth table as another eight physical program bits.

This also changes storage placement. Instead of putting the single inherited word along the last axis, put word j along axis j. The original table remains on the first axis; each lift adds a new program ray on its new axis. Inherited program cells then keep their old coordinates, extended by a zero coordinate.

The five-symbol alphabet, scale nine, radius nine, and one-step cadence remain. The occupied allocation grows from nine sites to 8d+1 sites per macrocell. The full macrocell allocation remains 9^d.

## Native programs are ordered chains of editable tables

A program at dimension d is

\[
P=(r,h_2,\ldots,h_d)\in\{0,\ldots,255\}^{d}.
\]

For a binary data field S, evaluation at x starts with

\[
b_1=r[4S(x-e_1)+2S(x)+S(x+e_1)].
\]

For j=2,...,d, use the previous stage and two neighbors along the next axis:

\[
b_j=h_j[4b_{j-1}+2S(x+e_j)+S(x-e_j)].
\]

The updated datum is b_d. Every stage reads the program of the updated site; neighboring programs can differ arbitrarily.

Write this data update as T_d(P,S), where P is now a spatial field of such tuples. The complete held system is

\[
U_d^{\rm hold}(P,S)=(P,T_d(P,S)).
\]

The copy system uses the same data update and simultaneously sets

\[
P'_x=
\begin{cases}
P_{x-e_1},&S_x=1,\\
P_x,&S_x=0.
\end{cases}
\]

All reads use the old state. The entire tuple is copied, including every routing word. The hold/copy policy remains architectural.

The canonical routing table is

\[
M(b,n,s)=
\begin{cases}
n,&b=0,\\
s,&b=1.
\end{cases}
\]

Under the displayed bit addressing, M is word 172. A lift appends this one fixed word; it never fits a routing table separately to a source.

## Every instruction is an actual physical cell

Use the alphabet B,D0,D1,P0,P1. At logical site x, reserve the macrocell

\[
9x+\{0,\ldots,8\}^d.
\]

Place the datum at 9x. With program words numbered j=1,...,d and bit addresses q=0,...,7, place the program symbol at

\[
9x+(q+1)e_j.
\]

Every remaining site is B. These rays are disjoint: a program site has exactly one nonzero coordinate modulo nine. Call this encoding J_d.

![Two-dimensional physical layout: the original rule's eight cells lie on the positive first-axis ray, and the added routing table's eight cells lie on the positive second-axis ray. The interpreter first evaluates the original rule on L,C,R, then evaluates the stored routing table on that output and N,S.](assets/editable-routing-tables-20260909.svg)

| Resource | 1D | 2D | 3D | 4D |
| --- | ---: | ---: | ---: | ---: |
| Mutable program bits per logical site | 8 | 16 | 24 | 32 |
| Occupied program/data sites | 9 | 17 | 25 | 33 |
| All sites per macrocell | 9 | 81 | 729 | 6,561 |
| Blank sites | 0 | 64 | 704 | 6,528 |
| Alphabet size | 5 | 5 | 5 | 5 |
| Chebyshev radius | 9 | 9 | 9 | 9 |
| Physical ticks per logical tick | 1 | 1 | 1 | 1 |

One-tick execution treats a local CA transition as atomic. It does not assert constant local circuit complexity as d grows: a datum reads 8d program cells and 2d+1 data cells and evaluates d tables. The table order and axis addressing remain part of the dimension-specific interpreter.

The source preparation footprint is one logical cell per macrocell. J_d is injective with a block-local decoder on its canonical image. Every declared data or program-bit edit changes exactly one physical symbol.

## The uniform physical law

A D cell reads all d program words and its data taps at zero and +/-9e_j. If every required tag is valid, it evaluates the chain and retains the D tag. If a required tag is absent, it retains its old symbol.

B always stays B. In hold mode, P keeps its symbol.

In copy mode a P cell scans offsets -k e_j for k=1,...,8 and all axes. If exactly one scanned position has a D tag, it is the owner. If that owner is D1 and offset -9e_1 contains a P tag, copy that symbol; otherwise retain the old P.

This defines a total five-symbol CA H_d in either mode. The rule reads stored tags and relative offsets, not absolute coordinates.

**Physical realization theorem.** For m equal to hold or copy,

\[
H_d^mJ_d=J_dU_d^m.
\]

**Proof.** Each canonical D cell finds exactly the program tuple and data neighbors specified by T_d. At a program cell 9x+k e_j, the scan along axis j finds its owner 9x. No other backward offset on that axis reaches a D site because consecutive D sites are nine apart. A scan along another axis retains the nonzero j-coordinate modulo nine, so cannot find a D.

Thus all 8d program cells of a macrocell have the same old owner datum. Their reads at -9e_1 address corresponding slots of the left macrocell, so a gated copy moves the entire tuple coherently. Tags persist, and all blank sites remain blank. Every physical site matches the encoding of the complete logical update. ∎

This is a canonical-layout result. The malformed-input behavior is explicit and audited; it is not a recovery or self-assembly claim.

## The same lift accepts arbitrary edited routing programs

Let

\[
Q_d=(204,172,\ldots,172).
\]

The ECA leaf 204 copies the central datum. Every subsequent M selector preserves a uniform field because both candidates have the same value. Therefore Q_d fixes uniform zero and uniform one.

Define the complete logical lift by

\[
\widehat E_d(P,S)(x,k)=
\begin{cases}
(P_x\mathbin{\|}172,S_x),&k=0,\\
(Q_{d+1},0),&k>0,\\
(Q_{d+1},1),&k<0.
\end{cases}
\]

Here the vertical bar denotes appending a word. Both guard programs and guard data are source-independent, prepared infinite backgrounds.

**Lift theorem.** For both modes, on every native dimension-d program/data field,

\[
U_{d+1}^m\widehat E_d=\widehat E_dU_d^m.
\]

**Proof.** On the interface, the appended table receives (b_d,0,1), and M returns b_d. This is exactly the arbitrary source computation, including any previously edited routing tables.

In a neighboring guard layer, the inner guard evaluates a uniform old-dimensional field and returns its value. The outer M therefore selects outward, away from the arbitrary interface datum. In more distant guard layers both candidates already have the same value. All guard data remain correct.

For copying, the gate and left neighbor of an interface program lie in that same interface. Copying the old tuple with its appended constant 172 equals copying the old tuple and then appending 172. Guard programs are constant along the first axis, so copying leaves them unchanged. Retention is immediate. ∎

Consequently the physical lift

\[
\mathcal E_d=J_{d+1}\widehat E_dJ_d^{-1}
\]

satisfies

\[
H_{d+1}^m\mathcal E_d=\mathcal E_dH_d^m.
\]

The proof is independent of d. In particular, an arbitrary 2D program field can be edited and then lifted to 3D; an arbitrary edited 3D field can be lifted to 4D. It is not necessary for a source to have been produced by the preceding lift.

## Inherited edits and newly available edits are different contracts

An inherited datum or program-bit edit maps to the corresponding physical cell with an appended zero coordinate. It commutes with the lift. Together with the evolution identity, this preserves any finite sequence of inherited edits and execution steps.

A newly introduced routing table has no corresponding instruction in the old source. Editing it is a valid new-dimensional operation, but can change the new system's relationship to the old source. The edited system remains a valid source for the next lift.

The frozen stronger test asks whether an arbitrary appended table a could retain the old evolution on the same (0,1) rails. At the interface its output is a(b,0,1). Therefore:

\[
a(0,0,1)=0,\qquad a(1,0,1)=1
\]

are necessary and sufficient for preserving every source. These fix entries 1 and 5, leaving exactly 64 of the 256 tables.

The [saved result](../../results/editable_routing_tables_20260909.json) retains a counterexample for each of the other 192 appended words. For example, changing entry 1 of M from zero to one breaks an interface whose inner result is zero. This failure concerns replacing the canonical lift instruction while demanding unchanged old dynamics. It does not exclude any routing word from a source being lifted.

Only entries 1 and 5 are read on the prepared interface. The other six entries are dormant there. They have causal witnesses on arbitrary higher-dimensional data.

One explicit witness edits entry zero of the 2D routing word: take leaf zero and data L=C=R=N=S=0. M outputs zero; M with entry zero flipped outputs one. Its edit is the P cell at (0,1). After lifting to 3D, the corresponding cell is (0,1,0) and the same zero-to-one output change survives. On the original (0,1) rails, that entry-zero edit has no data effect.

## Stored programs need not have distinct data behavior

There are 65,536 stored two-word programs but exactly **30,496 distinct one-step local data functions**.

To count them, split the outer table into two four-entry halves g_0(n,s), g_1(n,s). If the halves are equal, or the inner ECA is constant, the output is one of 16 functions of n,s alone.

Otherwise there are 254 nonconstant inner functions and 16 times 15 unequal ordered pairs of outer halves. Complementing the inner function and swapping the two halves leaves the result unchanged. This is the only ambiguity: at a transverse input where the halves differ, the output as a function of the old three inputs identifies the inner function up to complement. Hence

\[
16+\frac{254\cdot240}{2}=30{,}496.
\]

The complete enumeration confirms this count and every complement/swap alias.

The stored tuples remain distinct program states. This count quotients only the local data-update function; it does not quotient the full state containing the program or establish equivalent responses to later instruction edits.

Likewise, instruction editability does not mean every entry is causally active in every program. A constant outer table suppresses the inner result. The audited claim is that each stored table entry has a context in which its one-cell edit changes the output. Upstream constant tables can supply either input bit; downstream first-input projection tables, word 240, carry the result onward.

## Reproducible evidence

The [protocol](protocols/editable-routing-tables-20260909.md) was committed at [68f8437](https://github.com/bombadil-labs/groovy-commutator/commit/68f8437ef7166e6fa85ddc812d77b4c5381d31ac). The [verifier](../../scripts/verify_editable_routing_tables.py) was committed before execution at [8c8c6be](https://github.com/bombadil-labs/groovy-commutator/commit/8c8c6be10d416a9218c0be26e1223ba62772c01c). The protocol had no deviations and the implementation needed no corrections.

Run from the repository root:

    python scripts/verify_editable_routing_tables.py > /tmp/editable-routing-tables.json
    diff -u results/editable_routing_tables_20260909.json /tmp/editable-routing-tables.json

The logical evaluator uses integer LUT indexing; the physical evaluator reads spatial symbols and reduces selector trees. The CI workflow reproduces the canonical JSON byte-for-byte.

| Audit | Result |
| --- | --- |
| Every eight-bit table on every input, isolated at every stage in dimensions 1 through 4 | 20,480 physical evaluations pass |
| One-cell causal instruction edits in those contexts | 20,480 witnesses pass |
| Full 2D local data census | 65,536 programs times 32 stencils; 30,496 distinct functions |
| Complete complement/swap check | All 65,536 aliases agree |
| Appended-table neutrality | Exactly 64 pass; 192 failure witnesses retained |
| First lift, all local source programs/stencils and layers -2 through 2 | 10,240 comparisons pass |
| Arbitrary two-word second-interface source patches | 2,097,152 comparisons pass |
| Uniform and adjacent guard checks | All 40 pass |
| Exhaustive local program copying in dimensions 1 through 4 | All 640 cases pass |
| Malformed-layout checks | All 128 pass |

Both modes also pass whole physical-field comparisons:

| Source family, per mode | Cases | Ticks each | Target dimensions | Compared symbols |
| --- | ---: | ---: | --- | ---: |
| Heterogeneous width-five 1D rings | 8 | 3 | 2D and 3D | 170,360 |
| Arbitrary 3-by-3 2D tori | 16 | 4 | 3D | 124,992 |
| Arbitrary 2-by-3-by-2 3D tori | 8 | 3 | 4D | 73,728 |

Before every tick, the audit flips one datum and one bit in every source program word, with exactly matched physical edits. Deterministic seeds and bit schedules are in the protocol. In copy mode, autonomous source-word changes by stage are [59], [219,219], and [82,82,77] for the three families. These are measured after external interventions and during execution itself. Hold mode has zero autonomous program changes.

Only source directions are periodic. Added directions start with radius ticks+2 and shrink by one guard layer each tick, retaining core [-2,2]. Exact sparse-map equality compares every occupied value and tag plus the implied blank complement. Across both modes there are 64 field cases, 272 target timepoints and 738,160 compared symbols.

The entire audit passes **2,236,434 assertions**. Whole-field assertions compare many symbols together; neither assertions nor correlated timepoints are independent scientific samples. Arbitrary-field and all-time claims follow from the proofs.

## Significance and the next boundary

Exact encoded CA simulation is an established framework. Ollinger's [survey of intrinsic universality](https://arxiv.org/abs/0906.3213) describes commuting encodings, block simulation, and universal constructions. Its usual rescaling definitions concern a fixed spatial dimension; our dimensional embedding and program-edit contract must be compared separately. This checkpoint does not establish novelty or intrinsic universality for arbitrary CA.

The contribution to this research program is specific: the previous fixed routing contents can be made spatially editable and autonomously transported without increasing the five-symbol alphabet or radius. The proof gives an explicit costed family and distinguishes inherited edits from new-dimensional interventions.

Remaining resources and questions:

- Table contents vary, but the ordered chain, axis assignments, owner rule and hold/copy policy remain fixed.
- The layout and protected roles are prepared. No self-assembly, tag repair or unrestricted program synthesis has been established.
- Infinite homogeneous guard backgrounds and exponentially sparse macrocells remain supplied resources.
- The source still supplies its own information. These lifts do not create independent new-dimensional information.
- This control family does not realize the ternary L/R/C commutator-correction roles.

A useful next bounded target is the **transverse preparation budget**: replace the infinite guard half-spaces with an explicitly finite-thickness arrangement, while stating its boundary rule and preserving execution, edits, and recursive source typing. Boundary cells that freeze because inputs are absent must be counted as part of that architecture. This is a proposed next experiment, not a result of the present audit.
