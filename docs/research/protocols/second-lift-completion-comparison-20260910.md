# Second-lift completion comparison: frozen protocol

Date: 2026-09-10. Version: issue67 protocol v1. Status: **frozen design; implementation and evaluation planned, not run**.

This protocol implements the [signed issue67 scope](https://github.com/bombadil-labs/groovy-commutator/issues/67#issuecomment-5622839866) after the completed [gradient intervention audit](../2026-09-10-gradient-intervention-costs.md). The [research checkpoint](../2026-09-10-second-lift-completion-protocol.md) records the analytic result and prior exploratory work. Closing the proposal issue completes protocol writing; it does not complete the [planned experiment](../../knowledge/second-lift-completion-comparison.md).

## 1. Typed input and constructor

An object records its spatial lattice, alphabet Q=GF(2)^k, invariant admissible family B, complete family update, total local ambient completion H, observation/encoding, cadence and costs. This protocol keeps the lattice Z and cadence one. XOR is componentwise on Q.

Define A_0=I XOR H, A_(j+1)=A_j H XOR H A_j and the whole-field tuples K_h=(A_0,...,A_h), O_h=(A_0,A_0 H,...,A_0 H^h). These are forward tuples anchored at the current input, not a past-history learner.

For K coordinates, a passing (h,R) supplies a radius-R top function g with A_(h+1)=g K_h on B. The complete tuple update is

$$
K_h'=(H(A_0)\oplus A_1,\ldots,H(A_{h-1})\oplus A_h,H(A_h)\oplus g(K_h)).
$$

At h=0 only the last component is present. Its ambient radius bound is max(1,R) for the radius-one H used here. The resulting object has alphabet GF(2)^{k(h+1)}, family K_h(B), identity observation of that tuple, and the specified completed tuple law. For O coordinates, test the final future A_0 H^(h+1) against O_h; update by shifting the rows and appending the learned final row. That full update has radius R.

The recipe is algebraically well typed on product alphabets. A bounded cap is still a requirement for this particular finite-tuple constructor. A failed cap budget does not reject every autonomous representation. Injectivity is recorded through fibers rather than a “no literal source bit” filter. Alphabet growth and correction depth are resources; neither adds a spatial axis here.

## 2. Fixed Rule32 first image and the two total laws

On the full infinite binary shift, let F=F_32, D=I XOR F, G=D F XOR F D, and E(S)=(D(S),G(S)). Fix B=E(full shift). The map E has radius at most two. The next input alphabet is Q=GF(2)^2, with X=(U,V) at each horizontal site.

The two total radius-one laws are

$$
H_{128}(U,V)=(F_{32}(U)\oplus V,F_{128}(V)),\qquad
H_{160}(U,V)=(F_{32}(U)\oplus V,F_{160}(V)).
$$

These are choices of ambient completion even though both are already total. The [extension-freedom proof and local certificate](../2026-09-10-extension-freedom.md) establish H_128 E=E F and the absence of top pattern101 in G(S). Since F_160(V) XOR F_128(V) is the indicator V_left(1+V_center)V_right of that pattern, H_160 E=E F too. Both laws therefore preserve B and agree there at every time. They can differ on the full four-symbol shift.

Realizability means membership in the full E image. Merely forbidding101 in V is not used as a sufficient test.

## 3. The invariant control is a theorem

On a shared invariant B where H=H', A_0^H and A_0^{H'} agree, and their O_h tuples agree for every finite h. The [triangular theorem](../2026-09-09-correction-future-coordinates.md), applied componentwise, gives

$$
O_h=T_h^H K_h^H=T_h^{H'}K_h^{H'},\qquad
K_h^{H'}=(T_h^{H'})^{-1}T_h^H K_h^H.
$$

Thus the whole-field fibers of K_h^H and K_h^{H'} on B are equal, and existence of a whole-field autonomous factor at that fixed h is completion-independent. This includes any declared probability law on a finite ensemble, with no entropy prior needed for the fiber identity.

Construct T by U_j^(t+1)=H(U_j^t) XOR U_(j+1)^t, reading the left edge; invert by U_(j+1)^t=U_j^(t+1) XOR H(U_j^t). Each direction has radius at most h for these H. The cross-completion recoding and its inverse consequently have radius at most 2h, with h(h+1) whole-field applications of a two-component H or H' per cross-recoding direction. At h=1 the sharper formula is

$$
(u,v)\longmapsto(u,v\oplus H(u)\oplus H'(u)),
$$

of radius at most one in both directions.

These are constructive upper bounds, not minimum radii or gate-complexity lower bounds. A complete local tuple law of radius r transfers through the conservative recoding bounds to radius at most r+4h. Identical bounded pass tables do not imply identical literal correction maps. Failure within R≤2 does not prove nonexistence of every radius or of a whole-field factor.

The control does not apply between H_128 and H_160 on the full four-symbol shift, where their source dynamics differ. O-coordinate tables on B must be identical between the completions; a discrepancy is an implementation failure, not a scientific exception to the theorem.

## 4. Frozen primary matrix and order

Run exactly both completions (128, then 160), both domains (inherited B, then ambient Q^Z), both coordinates (K, then O), h=0,1,2 and R=0,1,2, in that lexicographic order: 72 budget cases.

For each budget enumerate all centered causal input windows. For K, group the radius-R K_h window by its central A_(h+1) output. For O, group the radius-R O_h window by central A_0 H^(h+1). Pass exactly when each realized key has one target symbol. Otherwise retain exact target sets and a canonical conflict witness.

Report every case, not just the smallest passing radius. Report the smallest passing R in the declared set or “none through 2”; keep K's cap radius separate from its max(1,R) complete-law radius. Compare literal tables only with their coordinate, domain and encoding stated.

There is no directional prediction of which completion has cheaper caps. Theorem-backed equalities and previously inspected finite controls are identified in advance as such. No class labels, rule selection, orbit search or fixed-point classification enter.

## 5. Complete causal-window bounds

H has radius1, A_j has radius at most j+1, and A_0 H^j has radius at most j+1. For either coordinate system the feature/target union therefore needs pair-field radius

$$
\rho(h,R)=\max(R+h+1,h+2).
$$

For the inherited domain, compose with E and enumerate every binary source window of radius rho+2. Apply literal local rules on shrinking windows; never wrap a local causal window around a ring. Every source word extends to a global binary configuration, so every enumerated feature/target is realizable in B; conversely every relevant B patch has such a source restriction. Extra conservative input bits cause duplicate records, not spurious keys.

For the ambient domain, enumerate every Q word of radius rho. There are no E-image constraints. The bounds per completion and coordinate system are:

| h | R | Pair radius rho | Source radius for B | Binary source words | Ambient pair words |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 2 | 4 | 512 | 1,024 |
| 0 | 1 | 2 | 4 | 512 | 1,024 |
| 0 | 2 | 3 | 5 | 2,048 | 16,384 |
| 1 | 0 | 3 | 5 | 2,048 | 16,384 |
| 1 | 1 | 3 | 5 | 2,048 | 16,384 |
| 1 | 2 | 4 | 6 | 8,192 | 262,144 |
| 2 | 0 | 4 | 6 | 8,192 | 262,144 |
| 2 | 1 | 4 | 6 | 8,192 | 262,144 |
| 2 | 2 | 5 | 7 | 32,768 | 4,194,304 |

These are combinatorial work estimates, not measured results. The inherited total is 64,512 words and the ambient total 5,031,936 words for one completion/coordinate system; all four combinations total 20,385,792 word-case evaluations without reuse. Maximum single case: 32,768 binary source words or 4,194,304 pair words. Implementations may cache mathematically identical expressions but must preserve the complete domain and counts.

## 6. Canonical encoding, witnesses and off-image completion

Enumerate source bits MSB first from leftmost site to rightmost. Encode a pair (U,V) by symbol 2U+V, and enumerate ambient words as MSB-first base-four words. Feature keys concatenate sites from -R to R; at each site concatenate coordinate rows j=0 through h, each with U before V. Read the resulting bit word MSB first. The maximum key width is 30 bits; target symbols are two-bit pairs.

For each key retain its four-bit target-membership mask. A pass has one set bit. For a conflict choose the smallest key with multiple targets, its two smallest target symbols, and the smallest enumerated preimage word for each. Save the source/pair words, realized feature patch, both targets and the evaluation convention. The witness concerns that local radius only; it is not a full-field ambiguity witness.

A passing cap uses the unique forced symbol on every realized key and symbol 0=(0,0) on every unrealized key. Specify it as a sorted reachable-key table plus this total default; do not choose a simpler completion after viewing results. K's lower rows follow the fixed correction formula in section1. O's lower rows shift. Save both the cap table and complete-law description. This canonical completion is part of the output object and does not remove the distinction between its inherited family and ambient states.

Canonical table records are sorted by unsigned key, using four little-endian bytes for the key followed by one byte for the target-membership mask. Include record count, coordinate/domain/budget, default convention and SHA256 in a JSON manifest. On pass the mask determines the cap output; on failure it describes the exact observed relation. Keep source and implementation commit hashes. No timestamps belong in semantic table hashes.

## 7. Verification before accepting a census

Freeze and commit the implementation before primary evaluation. A separate verification path must use literal truth-table/shrinking-window evaluation rather than importing the primary evaluator's composition/cap routines.

Before primary evaluation, verify the first image locally by enumerating the 128 seven-bit source windows needed for a radius-one E patch and next central pair; recover both H_q E=E F and forbidden top101. These are existing exact controls. Verify the bit/symbol ordering with hand-checkable constant words and the already archived MSB-first n=8 example. These are controls, not unrun predictions.

During the complete run:

1. Independently compute each case's feature/target digest over its entire causal domain. Require agreement with the primary path.
2. Replay every saved conflict witness independently, checking equal input keys and unequal targets.
3. For every passing table, independently verify every causal window against its forced output and the complete next tuple law. Local completeness then establishes all-site, all-time preservation of the declared encoded family.
4. Audit K↔O in both directions against directly prepared tuples, for each completion. A central check needs pair radius 2h+1, or binary preimage radius 2h+3 on B; at h=2 these are five and seven. Enumerate those complete domains (at most 4^11 ambient words or 2^15 source words). Audit cross-completion recoding in both directions **on B only**: radius at most 2h acting on K_h(X) needs pair radius 3h+1 and binary source radius 3h+3, at most seven and nine respectively. Enumerate all 2^19 source words at the largest depth. Arbitrary-tuple invertibility is also an algebraic control; do not add a census over its larger tuple alphabet.
5. On inherited inputs require pointwise O_h and O-next equality between completions. Compare whole-field fibers in the finite diagnostic below as a theorem-backed check. Do not compare local K patches as if whole-field fiber equivalence forced their equality.

The recoding padding bound in item 4 covers evaluating cross recoding (radius≤2h) on K_h(X) (radius≤h+1). For the inverse composition one can verify each recoding against the other's directly prepared K_h on these domains and invoke the established two-sided triangular algebra; a brute-force nested radius4h circuit is not silently assumed to fit the smaller window. Report which check was performed.

Any independent disagreement blocks acceptance and is recorded with a minimal reproducible case. Correctness fixes retain the frozen matrix and are documented; changing the domain, scoring, completion or radius budget requires an explicit protocol revision before the affected run.

## 8. Finite whole-field diagnostics and priors

After local acceptance, run h=0,1,2 on all 256 binary source states of the n=8 ring, deduplicating X=E(S) to the 255 distinct family states for family-domain fiber counts. Keep the original 256-source weighting as a separately named measure. Compute complete K_h and O_h fields, their equality partitions, image sizes and fiber-size histograms. Both completions must give the same partitions on B.

A separate ambient diagnostic uses all 4^4 pair states on the n=4 ring for each completion. Its small periodic geometry is an implementation diagnostic only, not a substitute for local infinite-lattice enumeration or a reason to apply completion invariance off B.

If entropies are reported, label H(X|K_h(X)) under uniform distinct X separately from H(S|K_h(E(S))) under uniform binary S. Do not normalize a single exceptional collision into “one bit lost everywhere.” The earlier reported sole alternating-pair collision implies 2/2^n bits under the uniform binary source prior, while its maximum exceptional-fiber ambiguity is one bit. Only the inspected ring sizes have that reported classification.

## 9. Feasibility, stopping rules and deliverables

Use chunks of at most 65,536 words. Primary grouping can use fixed-width numeric arrays and sorted keys; avoid millions of Python dictionary entries or a dense table over all 2^30 possible keys. For the largest primary case, a uint32 key, uint8 target and uint32 preimage index cost about 36MiB before sorting/work buffers. Reserve at most 2GiB per active case. The separate inherited recoding control's largest binary domain has 2^19 source words. These finite counts indicate a practical bounded task; no timing measurement is claimed.

Run at most one large ambient case per worker. A four-hour per-case limit or memory limit yields **incomplete**, never “no cap.” Preserve resumable counts/digests and the last completed case. Do not reduce a domain or pick a favorable completion to make the report finish. Implementation benchmarking must use control cases and remain labeled engineering work; primary outputs stay uninspected until the implementation commit is pinned.

The planned deliverable includes: the pinned protocol and implementation commits; exact matrix and table artifacts; independent digests and witnesses; recoding formulas/cost bounds; complete-vs-cap radius columns; finite fiber diagnostics with priors; resource accounting and all deviations. The later PR updates the experiment from planned only when these acceptance checks are complete.

Orbit/fixed-point classification, minimum conjugacy searches, new spatial axes, larger rule cohorts, learner/coarsening policies and endogenous controllers remain outside this protocol.
