# Finite routing boundaries work when absence remains explicit

The editable-program lift no longer needs infinite guard half-spaces. One occupied guard layer on each side of the source plane suffices under the **unchanged** five-symbol, radius-nine interpreter. Every cell beyond the three-layer band is blank.

The guards stay fixed because their outward data neighbor is absent: the existing all-inputs-required rule retains a datum when a required input is missing. This is autonomous boundary behavior, but still prepared architecture. It does not establish self-assembly or remove protected roles.

Repeated lifting requires a corresponding representation change. An absent macrocell is not a zero-valued occupied macrocell. Making occupancy explicit gives a native masked source family, and its complete program/data evolution, inherited edits, and program copying commute with the same finite lift in every finite dimension.

A separate [correction-transport note](2026-09-10-stored-correction-transport.md) now returns to the original commutator question. Finite routing boundaries are not automatically valid correction closures.

## The unchanged interpreter and the expanded source type

The [editable-routing construction](2026-09-09-editable-routing-tables.md) uses B,D0,D1,P0,P1, scale nine and a dimension-d program tuple P=(r,h_2,...,h_d). Each word has eight editable entries.

In a complete macrocell, D is at 9x and bit q of word j is at 9x+(q+1)e_j. A D cell evaluates its table chain only when its entire program and all required data neighbors have valid tags. Otherwise it retains its old symbol. A blank B stays B. Program cells retain their bits or copy the corresponding left-macrocell bit under the owner datum gate.

That total physical law already specifies what happens at a missing input. We keep it unchanged.

A native source now consists of

\[
(\Omega,P,S),
\]

where Omega is an arbitrary fixed subset of Z^d. Each x in Omega has a complete d-word program and a binary datum. Every macrocell outside Omega is entirely B. Denote this encoding by J_d.

The logical update V_d is:

- Omega remains fixed.
- If all sites x+/-e_j belong to Omega, update S_x by the existing table-chain evaluator.
- Otherwise retain S_x.
- In hold mode retain P_x.
- In copy mode, copy the complete old P_(x-e_1) exactly when S_x=1 and that left site is present; otherwise retain P_x.

Data and program updates are simultaneous. Occupancy is represented by existing B versus D/P symbols, not by a sixth symbol. A source can have finite support, holes, or full support. We allow payload edits only at occupied sites; occupancy edits and incomplete-program layouts are outside this action contract.

## Physical realization remains exact

For either update mode m,

\[
H_d^mJ_d=J_dV_d^m.
\]

**Proof.** A D cell finds all its required data taps precisely when the corresponding logical neighbors are present. Its own complete program is present by definition. Thus it computes the declared logical value or retains its datum exactly as V_d requires.

A program cell has exactly one owner: along its own ray, consecutive possible D positions are nine apart; scanning another axis cannot eliminate its nonzero slot coordinate modulo nine. Deleting entire macrocells cannot introduce a second owner. The left program bit is present exactly when the left macrocell is present. Therefore all program bits copy coherently or remain fixed. D/P tags and B are preserved, so the occupied mask is invariant. ∎

The decoder reads occupancy, program and datum from one macrocell. J_d is injective on the declared typed family and has a block-local inverse.

## Three layers give the finite lift

Let M=172 be the selector satisfying M(b,0,1)=b, and let Q_d=(204,172,...,172). Define

\[
\Omega'=\Omega\times\{-1,0,1\}.
\]

At occupied target sites, put

\[
\widehat E_d(\Omega,P,S)(x,k)=
\begin{cases}
(Q_{d+1},1),&k=-1,\\
(P_x\mathbin{\|}172,S_x),&k=0,\\
(Q_{d+1},0),&k=1.
\end{cases}
\]

All other macrocells are blank. The notation in the central row appends the fixed word to the source program.

| New-axis layer | Contents | Update mechanism |
| --- | --- | --- |
| Below -1 | B only | B is absorbing |
| -1 | Complete guard program, datum 1 | Missing outward neighbor freezes datum |
| 0 | Inherited program plus M, source datum | Same old-neighbor availability as source |
| +1 | Complete guard program, datum 0 | Missing outward neighbor freezes datum |
| Above +1 | B only | B is absorbing |

**Finite-lift theorem.** For both modes and every native masked source field,

\[
V_{d+1}^m\widehat E_d=\widehat E_dV_d^m.
\]

**Proof.** A central site has all old-axis data neighbors exactly when the source site did. Its new-axis neighbors are present. If an old neighbor is missing, both source and target retain the datum. Otherwise the new selector receives (b,0,1) and returns the source result b.

Each new guard site lacks its outward neighbor and therefore retains its prescribed datum, regardless of the guard table's output. Guard tuples are constant along the first axis. A guard program either copies an identical left tuple or retains its own when that neighbor is absent.

At the central plane, the left-neighbor presence and old datum gate match the source. Copying a tuple with its constant appended M is the same as copying the source tuple and appending M afterward. The occupied support is the unchanged product mask. ∎

The associated physical lift

\[
\mathcal E_d=J_{d+1}\widehat E_dJ_d^{-1}
\]

therefore intertwines H_d and H_(d+1). No external clamp, discarded guard layer, evolving halo, or source-specific interpreter is used.

In the old infinite-background construction, guard table semantics maintained the guard data. Here missing-input retention does that work. The choice Q_d keeps program words uniform and comparable to the earlier construction; its uniform-state data behavior is not needed to freeze these finite guards.

## Why it can lift again

After one lift the mask is Omega times {-1,0,1}. This is itself a valid native mask, so a second lift produces

\[
\Omega\times\{-1,0,1\}^2.
\]

Induction gives any finite number k of lifts. Missing old-axis neighbors remain missing at the next central plane; the next lift does not silently fill them with ordinary zero cells.

The theorem accepts any payload-edited masked field as its source. The audit includes editing a first lift's guard datum and a routing-table entry, then treating that altered 2D field as a new source for a 3D lift. Its relation to the original 1D source need not survive that new operation; the new 2D-to-3D identity does.

Inherited datum and instruction edits have one-cell physical support. Their coordinates acquire zero in the added dimension. They do not change guard payloads or occupancy. Any finite word of these edits and execution steps is preserved.

## Preparation budget and scoped minimality

Each lift creates three occupied target macrocells per occupied source macrocell. Starting at dimension d and lifting k times gives

\[
3^k\bigl(8(d+k)+1\bigr)
\]

occupied physical sites per original occupied logical site. The corresponding full macrocell allocation is 3^k 9^(d+k).

For a 1D source:

| Number of lifts | Final dimension | Macrocells per original site | Occupied physical sites per original site |
| --- | ---: | ---: | ---: |
| 0 | 1 | 1 | 9 |
| 1 | 2 | 3 | 51 |
| 2 | 3 | 9 | 225 |
| 3 | 4 | 27 | 891 |

The complete-macrocell layout spans physical coordinates -9 through 17 on each new axis: 27 coordinate positions. Everything beyond that band is the absorbing B background. This is finite transverse thickness, not finite total support when the original source is infinite. For finite Omega, total nonblank support is finite.

Preparation reads one source macrocell, including its occupancy. Guard values are independent of source program/data values; their locations depend locally on presence. The alphabet remains five, radius nine, and cadence one. Local circuit work still grows with dimension.

Under this unmodified all-inputs-required interpreter, fixed placement and one-tick contract, a changing central datum needs occupied data neighbors at both new-axis offsets. The encoding therefore needs at least the three macrocell layers -1,0,+1. This is a scoped lower bound, not an optimum over other laws, partial guard layouts, alphabets or cadences.

## Failed variants retained

**Missing-as-zero completion.** Consider an isolated occupied source cell. It lacks its left and right data neighbors, so retains its datum. Filling those missing sites with ordinary occupied zeros changes the computation.

For source program 255 and datum zero, the isolated source remains zero. After zero completion the source computation becomes one, and the lifted central datum becomes one. The old gate is zero, so this counterexample also applies in copy mode.

The frozen census checks every ECA word and both isolated central data values. Exactly 256 of 512 data cases fail. Exactly 64 words agree for both tested data values, characterized by bit0=0 and bit2=1. These counts describe this local completion control, not a rule classification.

**Too few guard layers.** For Rule 255 on an all-zero width-three source, the source changes to ones. With layer sets {0}, {-1,0}, or {0,1}, the target central datum is frozen by a missing new-axis neighbor and remains zero. All three fail; {-1,0,1} passes this witness.

Both failures and the successful occupancy-preserving three-layer construction were declared before evaluation. The results do not exclude alternative boundary mechanisms.

## Audit and reproduction

The [protocol](protocols/finite-routing-boundaries-20260910.md) was frozen at [c7072fb](https://github.com/bombadil-labs/groovy-commutator/commit/c7072fb1143d1b545f21a89fd47cb3ddc858846d). The [implementation](../../scripts/verify_finite_routing_boundaries.py) was committed before execution at [cc6f59f](https://github.com/bombadil-labs/groovy-commutator/commit/cc6f59ffff405ba9dc6fded49862fa62471fcf8d). Neither needed a correction or protocol deviation.

The verifier calls the unchanged physical interpreter from the editable-routing note and independently specifies occupancy-aware logical evolution.

    python scripts/verify_finite_routing_boundaries.py > /tmp/finite-routing-boundaries.json
    diff -u results/finite_routing_boundaries_20260910.json /tmp/finite-routing-boundaries.json

The [saved result](../../results/finite_routing_boundaries_20260910.json) has **26,619 passing assertions**, including:

- 4,608 local program/data/neighbor-presence cases, comparing the source, central lift and both guards;
- 1,280 exhaustive presence-sensitive program-copy cases through dimension four;
- both failed controls, with all 256 missing-as-zero failure witnesses retained;
- 96 complete field cases, 768 target timepoints and 981,696 compared physical symbols;
- two additional edited-guard continuation cases, comparing 11,040 symbols.

The six field families include full and holed 1D/2D tori, a holed 3D torus, and a nonperiodic four-site source. Both modes use eight frozen seeds and four ticks per family, with matched datum and every-stage instruction edits before each tick. All copy-mode families show autonomous source-program changes at every stage. The holed 1D data are pinned by missing neighbors, as expected; other families include autonomous data changes.

Every retained physical symbol, occupancy decoder and support count is compared. The omitted complement is B and remains B by the literal center rule. No halo is cropped and no boundary is reset. Finite periodic checks audit the construction; arbitrary-mask and all-time claims rest on the proofs.

## What this establishes and what follows

Finite transverse preparation is now constructive for complete macrocells with fixed occupancy and missing-input retention. Protected tags, axis assignments, prescribed programs and absorbing exterior remain architectural resources. We have not established occupancy edits, self-maintained roles or a source-independent minimum encoding cost.

The next stage is the original correction problem. The [stored-transport result](2026-09-10-stored-correction-transport.md) puts the commutator's interior update into this same physical interpreter. It also retains a failed finite correction cap. That separates finite geometry from indefinitely sufficient correction information.
