# Finite correction caps exist, but local coordinates have a cost

Date: 2026-09-10. Evidence: exact within the stated full-shift depth/radius budgets. Candidate selection below is explicitly post-census.

Can retained correction rows compute their missing next correction? **Yes for many fixed ECA rules, at small but representation-dependent budgets.** The frozen census finds 1,094 passing and 3,514 failing budgets. Every pass is a full infinite-lattice local identity; every failure has two explicit source windows that look identical to the proposed cap and demand opposite outputs.

The useful next witness is Rule32. Keeping the derivative and first correction gives an exact autonomous two-row system with a nonconstant spatial cap. The original source is not retained. This is logical closure, not compression or an already audited physical/edit implementation.

## Protocol and reproducibility

The [protocol](protocols/local-correction-caps-20260910.md) was frozen in commit `1a012ae350e73f2091940aa79a47f9b036ed8fd3`, before this census. The [verifier](../../scripts/verify_local_correction_caps.py) was committed as `1fa5353b25f18779cf21379c491f1ec58144f15e` before evaluation. The [canonical result](../../results/local_correction_caps_20260910.json) includes every budget, minimum passing radii, certificate hashes, realized-pattern counts and conflicting source pairs. There were no protocol deviations or implementation corrections.

For all 256 homogeneous fixed ECA rules on the full infinite binary lattice, write

\[
D=I\oplus F,\qquad A_0=D,\qquad A_{j+1}=A_j\circ F\oplus F\circ A_j,\qquad B_j=D\circ F^j.
\]

For depths h=0,1,2 and spatial cap radii R=0,1,2, compare K_h=(A_0,...,A_h) targeting A_(h+1), and O_h=(B_0,...,B_h) targeting B_(h+1). This is 256 times 3 times 3 times 2 = 4,608 budgets, not independent statistical samples.

All source words of radius m=max(h+1+R,h+2) are enumerated. This contains the entire causal support of the input patch and target, with at most 11 bits and no wraparound. A consistent local map is extended by zero on unrealized tuple patches. Because every finite binary source word extends to a full configuration, consistency is sufficient for the claimed full-shift identity; a conflicting pair is a valid local obstruction.

The primary implementation composes integer-indexed truth tables. An independent evaluator uses tuple-valued shrinking evolution and recursive operator composition; it does not reuse the primary tables or distribute nonlinear F over XOR. It checks all 348,160 local-map truth entries and independently reconstructs all fibers and first conflict pairs over 2,064,384 source-window cases. The primary enumeration covers the same 2,064,384 cases. Every comparison passes.

Source words are packed left-to-right, most significant bit first. Tuple patches concatenate components j in increasing order, then positions x=-R,...,R. Cap hashes are SHA256 of one byte (0 or 1) per dense table output in ascending packed-input order, with unrealized inputs zero. A failed budget stores the first clash in ascending source-word order: the first representative of that patch and the first later opposite-target word. Enumeration continues to count all realized patterns.

## Census

Each count is the number of source rules, out of 256, passing that exact budget.

| Retained depth h | Cap radius R | Correction K_h | Observation O_h |
| --- | --- | --- | --- |
| 0 | 0 | 18 | 14 |
| 0 | 1 | 30 | 30 |
| 0 | 2 | 30 | 30 |
| 1 | 0 | 28 | 30 |
| 1 | 1 | 52 | 92 |
| 1 | 2 | 123 | 120 |
| 2 | 0 | 28 | 32 |
| 2 | 1 | 59 | 134 |
| 2 | 2 | 94 | 150 |

Taking the union over tested depths and radii, K supplies a cap for 135 rules and O for 150. These are overlapping alternatives, not 285 distinct rules. No conclusion follows here about the remaining rules at larger budgets or under other representations.

The established controls are recovered: all 16 affine ECA have constant commutator caps, and Rule232 has derivative evolution Rule128 and correction cap Rule104 on its seven realized derivative neighborhoods. These are controls, not new discoveries about the parallel Erased Distinctions program.

## More rows do not guarantee a narrower next correction

For fixed h, enlarging R can only help; the census respects that monotonicity. Increasing h changes both the coordinates and the target. A wider correction tuple can therefore require a wider cap even when its shorter predecessor already closes.

For Rule11, K_1 closes at R=2, but K_2 fails at R=2. The latter witness is the pair of 11-bit source words `00111001000` and `01111001000` (integers456 and968). Both produce packed K_2 patch28572, yet their A_3 targets are0 and1. K_1's passing cap has90 realized patterns; K_2 has192. This refutes the particular K_2 radius-two cap, not finite closure of Rule11, which the K_1 result already establishes.

The [triangular-coordinate theorem](2026-09-09-correction-future-coordinates.md) says K_h and O_h have identical whole-field fibers, not identical fixed-radius patches. Their local costs can differ in either direction: at h=1,R=2, K passes123 rules versus O's120; at h=2,R=2, O passes150 versus K's94. Neither coordinate convention uniformly dominates within these budgets. If one has whole-field closure, so does the other; an adequate radius may lie outside this census.

## A compact nonconstant cap for Rule32

Post-census inspection of small nonconstant caps identifies

\[
\boxed{A_2(S)_x=A_1(S)_{x-1}\,A_1(S)_{x+1}.}
\]

This is ECA160 applied to the top row: AND of its two spatial neighbors. Consequently

\[
A_1(F_{32}(S))=F_{32}(A_1(S))\oplus F_{160}(A_1(S))=F_{128}(A_1(S)).
\]

The last equality follows directly from 32 xor160=128 as truth-table words. The [standalone identity audit](../../scripts/verify_rule32_cap_identity.py), with its [result](../../results/rule32_cap_identity_20260910.json), independently checks the proposed formulas on every one of128 seven-bit source words, for384 identity assertions. This candidate was chosen after seeing the census, not by a preregistered ranking or a class label.

With U=A_0(S) and V=A_1(S), the closed system is

\[
U'=F_{32}(U)\oplus V,\qquad V'=F_{128}(V).
\]

For every source S, one update produces (A_0(F_32(S)),A_1(F_32(S))). Induction therefore proves the identity for every nonnegative time, without an externally supplied future row. The guarantee is for correctly prepared pairs; arbitrary (U,V) need not represent a source.

The cap is genuinely nonconstant on the represented image. Source word `0101010` gives top neighborhood111 and cap1; `0000000` gives000 and cap0. Its top neighborhoods are {0,1,2,3,4,6,7}. In particular, this is not a constant cap disguised by an off-image truth-table extension. The displayed Rule160 program is a convenient extension on the top-row input domain; it need not equal the census's zero extension on unrealized six-bit tuple patches.

Rule32 has no derivative-only cap at R<=2, while both K_1 and O_1 pass at R=1. This is a scoped depth advantage over the tested derivative-only neighborhoods, not a proof that a derivative-only cap fails at every radius, or a claim that this mathematical identity is new in the literature.

## Resource controls

| Representation | Raw bits/site | Preparation radius bound | Complete update radius bound | Generic dense last-cap bits |
| --- | --- | --- | --- | --- |
| Original source S | 1 | 0 | 1 | 8 source-rule bits; no cap |
| K_0 or O_0 at R=1 | 1 | 1 | 1 | 8 |
| K_1 or O_1 at R=1 | 2 | 2 | 1 | 64 |
| K_2 or O_2 at R=2 | 3 | 3 | 2 | 32,768 |

Generally the tuple patch has (h+1)(2R+1) bits and a worst-case dense cap has 2^((h+1)(2R+1)) bits. K's complete update also reads F of radius1, giving the bound max(1,R); O shifts its components and evaluates its last cap, giving boundR. These are upper bounds, not claims of minimal radius after simplification. All realized-pattern counts and per-budget costs are saved.

The Rule32 K_1 radius-one tuple realizes15 of64 patches. Its cap needs only the top row's two neighbors and can be represented by one eight-bit ECA word instead of the generic64-bit table; the actual top update is the single ECA128 word. Source retention still uses only one bit per site and radius-one dynamics, with A_j/B_j readout radius bounded by j+1. The two-row representation does not beat that storage baseline. Its value here is a closed derivative/correction account without retaining S, not a demonstrated information compression.

## Next physical experiment, frozen separately

The existing interpreter executes the bottom rule with program(32,60); the candidate top program is(128,240), using the first-input projection to ignore vertical data. This fits the existing table-chain syntax, but logical representability is not a substitute for a physical field and intervention audit.

The [next protocol](protocols/rule32-physical-cap-20260910.md) freezes the finite prepared strip, complete-symbol checks, and a distinction between matched native instruction edits and preservation or recovery of correction semantics. It has not been executed in this checkpoint. The planned strip has four complete logical rows including guards, hence68 occupied physical symbols per horizontal source site at scale9, before any further dimensional lift. This is prepared architecture, not self-assembly or autonomous repair.

No Class-IV criterion or novelty claim is used. Failed budgets remain available for explicit wider-radius, deeper, or differently encoded attempts.
