# Editable spatial programs survive two lifts, including autonomous transport

**Follow-up, 2026-09-09:** the [editable-routing note](2026-09-09-editable-routing-tables.md) answers the next question below for table contents: every added selector becomes an eight-bit spatial program. This original construction, its smaller storage budget, and both frozen results remain unchanged.

One fixed selector construction now gives an exact **1D → 2D → 3D** realization with programs stored in physical cells. It works for every ECA starting program and for arbitrary heterogeneous program fields. A local instruction edit changes one physical program cell, and the same program grammar applies again at the second interface.

A separately frozen extension also works when live sites autonomously copy their left neighbor's program. The programs need not remain fixed during evolution.

The result is conditional on an explicit architecture: five cell symbols, radius nine, a prepared macrocell layout, and homogeneous guard backgrounds. The native language is an ECA leaf word wrapped in one Rail constructor per added dimension. Its leaf bits are mutable; the wrapper structure is fixed by dimension. This is a constructive witness for that declared family, not a binary radius-one or marker-free result.

The user's Class-IV intuition played no role in this construction, census, or interpretation. Success for all 256 sources is a positive outcome. The rescue below changes a specific failed boundary choice and preserves its negative result.

## The repair: separate the source program from the guard program

The [earlier routing note](2026-09-09-selector-two-lift.md) used the source program throughout the target background. Its interface encoding worked only when that program preserved uniform zero and uniform one: 64 ECA rules.

Here source instructions are explicit spatial data. That lets the background carry a different, fixed program. We choose ECA 204 because it is the center projection, f_204(l,c,r)=c. This choice is independent of the source.

At the data interface, the target carries the inherited source program. Everywhere else it carries the guard program. The guard keeps the two uniform backgrounds stable, even when the source program would not. A source-program edit changes its interface copy only.

This is the full repair. It does not replace the interpreter separately for each source, expand a higher-dimensional truth table, or prepare the source's future.

## The native selector grammar

Let

\[
\mathcal G_1=\{\operatorname{ECA}(r):0\le r<256\},
\qquad
\mathcal G_{d+1}=\{\operatorname{Rail}(p):p\in\mathcal G_d\}.
\]

Write p_d(r)=Rail^(d-1)(ECA(r)) and let phi_d(r;S,x) be its output at x.

At dimension one,

\[
\phi_1(r;S,x)=r[4S(x-e_1)+2S(x)+S(x+e_1)].
\]

At the next dimension, first evaluate the inner program on the central slice. Use its output b to select a data neighbor in the new direction:

\[
\phi_{d+1}(r;S,(x,k))=
\begin{cases}
S(x,k+1),&b=0,\\
S(x,k-1),&b=1.
\end{cases}
\]

The same eight leaf bits remain in the program. Its interpretation gains one explicit Rail constructor. Every nested evaluation uses the program of the updated site; neighboring sites may have entirely different programs.

For a program field P and binary data field S, define the complete logical dynamics

\[
U_d^{\rm hold}(P,S)=(P,T_d(P,S)),
\qquad
T_d(P,S)(x)=\phi_d(P_x;S,x).
\]

Here P_x denotes the eight-bit word in the dimension-d native type. The complete state includes that word. A homogeneous P recovers one source program; an instruction edit at one site creates a heterogeneous field without changing U_d.

The second update mode is

\[
P'_x=
\begin{cases}
P_{x-e_1},&S_x=1,\\
P_x,&S_x=0,
\end{cases}
\qquad
S'=T_d(P,S).
\]

Call it U_d^copy. Both updates use the old state. The selected hold/copy mode is a fixed architectural policy, not a mutable instruction in the eight-bit word. This is the existing state-gated nonuniform program-transport model, extended to the native Rail family; the source transport idea is not new here.

## A physical cell layout, with every role explicit

Use the same alphabet in every dimension:

\[
\mathcal A=\{B,D0,D1,P0,P1\}.
\]

B is blank; D0/D1 carry one data bit; P0/P1 carry one program bit. These are stored symbols, not externally supplied coordinate labels.

For logical site x in Z^d, reserve the macrocell

\[
9x+\{0,\ldots,8\}^d.
\]

Place its datum at 9x. Place program bit q at

\[
9x+(q+1)e_d,\qquad q=0,\ldots,7.
\]

All other sites are B. Call this encoding J_d. At each lift the instruction word is laid along the newly added axis. Distinct macrocells have disjoint program storage; data dependencies are shared through the neighboring data cells.

![The physical 2D read stencil: eight program cells lie between the center datum and its positive transverse neighbor. The interpreter reads left, center, and right data to select a program bit, then that bit selects the positive or negative transverse datum.](assets/spatial-rail-programs-20260909.svg)

| Resource | Dimension 1 | Dimension 2 | Dimension 3 |
| --- | ---: | ---: | ---: |
| Physical sites per logical macrocell | 9 | 81 | 729 |
| Occupied data/program sites | 9 | 9 | 9 |
| Blank sites | 0 | 72 | 720 |
| Alphabet size | 5 | 5 | 5 |
| Chebyshev update radius | 9 | 9 | 9 |
| Physical ticks per logical tick | 1 | 1 | 1 |

The eight program payloads are stored explicitly. The common grammar and ambient dimension determine the fixed number of Rail wrappers; no wrapper counter is stored. Changing wrapper structure locally is outside this language's action contract. Eight bits do not represent arbitrary higher-dimensional programs. Native closure here concerns the declared programmed family and its canonical layouts; it does not encode the unrestricted physical CA on every malformed five-symbol field.

## One uniform physical interpreter per dimension

The dimension-uniform recipe defines a physical CA H_d.

A D cell reads its eight program slots and the data cells at offsets 0 and +/-9e_j. If their types are valid, it evaluates the native program and retains its D tag. If a required type is absent, it retains its old symbol.

In hold mode, P cells retain their symbols. B cells always retain B.

In copy mode, a P cell examines the eight positions immediately behind it along the last axis. If exactly one has a D tag, that cell is its owner. If the owner is D1 and the position nine cells to the left has a P tag, it copies that program symbol; otherwise it retains its own.

This gives a total CA on every five-symbol field, including malformed ones. The theorem uses the invariant canonical layout. It does not claim repair or spontaneous formation of that layout.

**Physical realization theorem.** In either mode m,

\[
H_d^m J_d=J_d U_d^m.
\]

**Proof.** Every canonical D cell finds exactly its own eight program bits and the neighboring logical data cells. Its selector result is therefore T_d(P,S).

In copy mode, a program slot is k cells ahead of its owner for exactly one k in 1,...,8. The next D site on that line is nine cells away, so the owner in the backward eight-site interval is unique. All eight slots see the same old S_x, and their reads at -9e_1 are the corresponding slots of P_(x-e_1). The whole word therefore moves coherently under the declared gate.

D and P tags persist, and every B remains B. Thus every site, including the blank complement, matches J_d of the complete updated logical state. The argument works on one global field with overlapping read neighborhoods. ∎

## A lift of complete program-and-data fields

For a guard word g, define Ehat_d,g by

\[
\widehat E_{d,g}(P,S)(x,k)=
\begin{cases}
(P_x,S_x),&k=0,\\
(g,0),&k>0,\\
(g,1),&k<0.
\end{cases}
\]

The target words have their dimension-(d+1) interpretation: P_x becomes Rail(p_d(P_x)); the guard becomes p_(d+1)(g).

The source-dependent preparation reads one logical source cell, or one physical source macrocell. Guard program/data values are independent of the source. The backgrounds are infinite and prepared; their stability is supplied by the same autonomous update, not external clamping.

**Guard theorem.** For either hold or copy mode, the identity

\[
U_{d+1}^m\widehat E_{d,g}
=\widehat E_{d,g}U_d^m
\]

holds for every source program/data field if and only if the inner guard program satisfies

\[
\phi_d(g;0^\infty)=0,\qquad
\phi_d(g;1^\infty)=1.
\]

**Proof.** At k=0, the two new-axis data neighbors are 0 and 1, so the outer selector returns precisely the inner source computation. Program retention is immediate. In copy mode, the gate and left program neighbor lie in this same interface, giving exactly the source program update.

At |k|>=2 both candidate data neighbors have the background value, so the data remains correct. At k=1 the inner guard sees uniform zero and must select outward, away from the arbitrary source datum. At k=-1 it sees uniform one and must also select outward. These are exactly the two displayed conditions, and choosing the opposite source bit supplies a failure witness if either fails.

Guard program words are constant along the first axis. Both retention and state-gated copying therefore leave them equal to g. This proves the complete program/data identity. ∎

For d=1, exactly 64 guard words satisfy the condition. **Every** source program works with any one of these guards. In particular, g=204 works for all sources.

For d>=2, every Rail program preserves both uniform data values: its two candidate neighbors are equal on a uniform field. Thus the same g=204 works at every subsequent interface.

A different program-update law would also have to preserve its chosen guard program on both data backgrounds. The copy proof does not silently extend to arbitrary program rewriting.

## The first two lifts and all finite continuations

On the canonical physical state space, define

\[
\mathcal E_d=J_{d+1}\widehat E_{d,204}J_d^{-1}.
\]

The two theorems give

\[
H_{d+1}^m\mathcal E_d=\mathcal E_dH_d^m.
\]

J_d is injective with a block-local inverse on its image. The physical lift therefore preserves complete source evolution and has a fixed decoder and one-tick cadence.

The second identity applies to **every valid dimension-two program/data field**, not only fields produced by the first lift. Applying the same construction again gives an exact physical 1D → 2D → 3D chain. Induction gives any finite number of further lifts in this declared family.

## Programs remain identifiable and locally editable

At any dimension, choose the three first-axis data bits to address q and set every transverse data pair to (0,1). Every Rail wrapper then returns its inner result. The final output is the physically stored leaf bit r_q.

Consequently all 256 programs remain distinct at every dimension. Flipping one physical program symbol changes the output on this witness, under the same H_d. Program interpretation is causally active.

A data edit at logical x changes the single D symbol at 9x. An instruction edit q changes the single P symbol at 9x+(q+1)e_d. Under Ehat each becomes the corresponding edit at (x,0), so both evolution and declared local edits intertwine. Any finite sequence of those operations is preserved.

In copy mode, the program can subsequently change and move because of the data state. The audit counts these autonomous changes separately from externally applied edits. Program synthesis, arbitrary mutation of the grammar, and a locally changing interpreter are not established.

## The failed boundary choice is preserved

The retained-program baseline repeats the source program across every added layer. At the first lift its guard is therefore the source itself, reproducing the earlier 64-source endpoint condition.

That baseline also makes one source-program edit affect an infinite line of target program words. A separate fixed guard repairs both issues:

| Retained-program boundary choice | Source programs that pass | Support of one program edit |
| --- | ---: | --- |
| Repeat the source program in every layer | 64 of 256 homogeneous ECA sources | Infinite transverse line |
| Put g=204 off the data interface | All 256; also arbitrary program fields | One target program cell |

These are two different initial encoding choices under the same interpreter. The second was derived and frozen before its census. It is an architecture-specific rescue, not evidence that the earlier failure was universal.

The autonomous-copy extension was frozen separately after the retained-program result passed; it uses only the separate-guard encoding.

## Reproducible evidence

The [main protocol](protocols/spatial-rail-programs-20260909.md) was frozen at [7e3d58c](https://github.com/bombadil-labs/groovy-commutator/commit/7e3d58ca1eb9ab21a0b446fb622eead543f5f811). The [transport extension](protocols/spatial-rail-transport-20260909.md) was frozen at [7d2db9e](https://github.com/bombadil-labs/groovy-commutator/commit/7d2db9eef4e682e4926553138193852a8548c252), after the first result and before its own execution. Neither protocol changed after evaluation.

Run from the repository root:

    python scripts/verify_spatial_rail_programs.py > /tmp/spatial-rail-programs.json
    diff -u results/spatial_rail_programs_20260909.json /tmp/spatial-rail-programs.json
    python scripts/verify_spatial_rail_transport.py > /tmp/spatial-rail-transport.json
    diff -u results/spatial_rail_transport_20260909.json /tmp/spatial-rail-transport.json

The [main verifier](../../scripts/verify_spatial_rail_programs.py) compares an integer-LUT logical evaluator with a physical symbol/coordinate selector interpreter. Its [saved result](../../results/spatial_rail_programs_20260909.json) includes:

| Check | Result |
| --- | --- |
| Exhaustive physical/local data evaluation | 2,048 / 8,192 / 32,768 comparisons in dimensions 1 / 2 / 3 |
| Physical instruction-edit witnesses | All 6,144 pass |
| Source/guard matrix | 65,536 pairs; 2,621,440 layer comparisons |
| First-interface guards | Exactly 64 guard words, each admitting all 256 sources |
| Arbitrary second-interface patches | All 40,960 comparisons pass |
| All homogeneous width-three source fields, three ticks, both lifts | 2,048 cases; 9,897,984 symbol values compared |
| Heterogeneous width-five fields with edits, four ticks | 16 cases; 224,640 symbol values compared |
| Arbitrary 3-by-3 program/data fields at the second interface, with edits | 32 cases; 62,208 symbol values compared |
| Malformed-layout checks | All 51 pass |

The main audit has 109,876 assertions; whole-field equality assertions compare many symbols at once. Symbol counts are not asserted to be independent scientific samples.

The [transport verifier](../../scripts/verify_spatial_rail_transport.py) and [result](../../results/spatial_rail_transport_20260909.json) add 192 exhaustive local program-update cases and 12 malformed-layout checks. Complete field comparisons pass for the same 16 heterogeneous and 32 arbitrary-second-interface fields. They include **129 and 349 autonomous source-program changes**, respectively, measured after external edits and during the update itself. All 974 extension assertions pass.

Periodic boundaries are used only in source directions. Added directions are initialized with sufficient guard layers and shortened each tick, retaining the core [-2,2]. Exact sparse-map equality checks every occupied program/data symbol and the entire implied blank complement. The general all-time and arbitrary-field claims rest on the proofs.

## What is now open

This result establishes native program inheritance for an explicit, restricted stored-program family. Its costs and fixed structure remain visible:

- Five symbols encode protected data/program roles; the layout is prepared.
- The physical radius is nine and blank allocation grows as 9^d per macrocell.
- The eight leaf bits are editable, but Rail wrapper structure and addressing conventions are fixed by dimension.
- Guard programs and data occupy prepared infinite backgrounds.
- The construction does not realize the ternary L/R/C correction roles or prove a special physical dimension.

The next focused extension is to make an introduced Rail instruction itself locally editable, while preserving the same geometry and action contract. That will require counting additional instruction bits and testing the changed guard conditions. Reducing the role alphabet or layout overhead is a separate experiment.

Failures of those variants should be recorded with their precise budget and revisited through explicit changes. The present rescue is a concrete reason to keep that distinction.
