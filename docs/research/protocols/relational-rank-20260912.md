# Protocol: relational rank and the first used spatial direction — 2026-09-12

**Status:** frozen before implementation/evaluation; revised after independent Gate-1 review. Nothing in this protocol has been run.  
**Program:** *Dimensional Closure and the Commutator Lift*.  
**Authored by:** Codex / OpenAI GPT-5.6 Sol.  
**Protocol review:** Claude Code, Fable 5.1 reviewed exact gathering head `ad304465e053a04e41ee7af76ceb68339cce7ac0` on 2026-09-12 and required three binding corrections. This revision incorporates them and requires renewed exact-head Gate 1 before implementation or evaluation.  
**Base:** `main` at `06b6732423d5ed01a2d996bc9d7fe25cef7af50d`.  
**Predecessor:** zero-dimensional base-case gathering PR #136. Its protocol has independent Gate-1 approval and its first canonical evaluation has been produced on its gathering branch, but #136 is not yet accepted on `main` when this revision is frozen.

## 1. Why this unit

The dimensional program has repeatedly learned that **more named coordinates do not automatically mean more independent spatial relation**:

- literal replication into an added axis gives a higher-dimensional ambient lattice while the inherited image remains constant along the new direction;
- Rule32 correction stacks can add represented bits per site without adding corresponding whole-field distinction capacity;
- fixed-width or multi-channel systems can carry arbitrarily many local bits/actions while remaining longitudinally one-dimensional under a declared representation budget;
- native higher-dimensional target states can support possibilities and interventions absent from the inherited image.

The user's phrase **"dependent origination"** motivates the question but is not a mathematical result, Buddhist-doctrinal claim, or physics claim of this protocol. The operational translation is narrower:

> **Can we distinguish the number of spatial translation directions that act nontrivially on a declared state family from the number of displacement directions actually used by a declared local law?**

This protocol introduces two deliberately separate, representation-relative quantities:

1. **translation rank** `rho_T`: the free rank of lattice translations acting nontrivially on a declared state family;
2. **causal displacement rank** `rho_C`: the integer rank spanned by essential input offsets of a declared local update law.

The first Gate-1 review exposed an important simplification: for the accepted ordered-axis constructor, the target essential-offset set is not an empirical mystery. It is exactly the Cartesian product of the source essential-offset set with itself. Consequently the proposed 256-rule rank classification is a **theorem control**, not a falsifiable discovery. This correction is part of the scientific content of the unit.

The aim is not to define intrinsic dimension once and for all. It is to make these two ranks precise, expose their dependence on the declared family/presentation, prove the ordered-axis product theorem, replay it exhaustively, and compare the resulting exact bookkeeping with already accepted dimensional families.

## 2. Translation rank of a declared state family

Let a declared state family `B` lie in configurations over the infinite lattice `Z^D`. Let `tau_v` denote translation by `v in Z^D`.

Define the **setwise translation group**

`H_B = { v in Z^D : tau_v(B) = B }`.

Define the **pointwise translation kernel**

`K_B = { v in H_B : tau_v(x) = x for every x in B }`.

Both are abelian subgroups of `Z^D`. Define

`rho_T(B) = rank_Q((H_B / K_B) tensor Q)`.

The primary statements below use infinite families, not a fixed finite torus. `rho_T` is explicitly **family- and presentation-relative**: changing which translated copies count as members of the declared family can change the rank even when the underlying configurations are closely related.

### T0 — zero-dimensional floor

For the binary 0D state set `{0,1}` on the one-point lattice, the translation group is trivial:

`rho_T = 0`.

### T1 — full shifts

For the full binary shift on `Z^d`,

`H_B = Z^d`, `K_B = {0}`, and `rho_T = d`.

The verifier records the `d=1,2` instances as theorem controls; the general formula is analytic.

### T2 — literal replication image

Let `P_d` literally replicate a `d`-dimensional configuration along one new axis into `Z^(d+1)`, as in the accepted guard-free axial control. On the copied image:

- every inherited-axis translation acts as before;
- translation by the new basis vector fixes **every** copied configuration.

Therefore the new-axis generator lies in `K_B` and

`rho_T(P_d(B_d)) = rho_T(B_d)`

for the full inherited source family. In particular the copied 1D beam inside `Z^2` has rank 1 while the full 2D target shift has rank 2.

This is deliberately a simple control: ambient coordinate count rises while inherited translation rank does not.

### T3 — product alphabets and correction coordinates

Changing the per-site alphabet or stacking finitely many represented coordinates over the same `Z` lattice does not, by itself, add a translation generator. The full product shift `(A^m)^Z` has `rho_T=1` for every finite `m`.

The accepted Rule32 correction-stack findings are imported only as comparison evidence: represented bits/site can grow while the representation remains longitudinally one-dimensional. This unit does not reclassify correction depth as spatial dimension.

### T4a — anchored many-channel control

For each finite `m>=1`, define `S_m` on `Z^2`: arbitrary binary values live on the horizontal tracks

`y = 0,2,4,...,2(m-1)`

and every other site is fixed to a declared background symbol. The track positions are part of the declared family.

Then horizontal translations preserve `S_m`, no nonzero vertical translation preserves the anchored finite track set, and no nonzero horizontal translation fixes every arbitrary track configuration. Hence

`H_{S_m} = Z e_x`, `K_{S_m}={0}`, `rho_T(S_m)=1`.

This is paired with, but not identified with, the accepted intervention-axis result: arbitrarily many independently addressable channels/actions can coexist with rank-one anchored translation structure.

### T4b — translation-closed contrast

The first Gate-1 review correctly noted that T4a builds the anchoring choice into the family. Freeze the contrast

`S'_m = union_{v in Z^2} tau_v(S_m)`.

Now every lattice translation maps `S'_m` to itself, while no nonzero translation fixes every member:

`H_{S'_m}=Z^2`, `K_{S'_m}={0}`, `rho_T(S'_m)=2`.

T4a/T4b are reported together. They are not competing measurements of an intrinsic object; they demonstrate that `rho_T` is sensitive to the declared family/presentation. A report that quotes one without the other fails the protocol.

## 3. Causal displacement rank of a local law

Let a translation-equivariant binary CA on `Z^D` have finite neighborhood offsets `N subset Z^D` and local Boolean rule `g`.

An offset `v in N` is **essential** when there exist two local patches differing only at `v` on which `g` gives different outputs. Let `E(g)` be the set of essential offsets.

Define

`rho_C(g) = rank_Z < E(g) >`,

the rank of the subgroup of `Z^D` generated by the essential displacement vectors measured **from the output site at the origin**. The center offset `0` contributes no rank.

Use the offsets themselves, not pairwise differences between essential offsets. Pairwise differences would incorrectly assign rank zero to a pure shift, whose one nonzero displacement is exactly the causal direction this quantity is intended to retain.

Examples:

- a constant, identity, or center-negation rule has `rho_C=0`;
- a pure one-cell shift has `rho_C=1` even though only one input is essential;
- essential offsets spanning two non-collinear directions give `rho_C=2`.

`rho_C` is invariant under invertible integer changes of lattice basis because those preserve subgroup rank. It is not claimed invariant under arbitrary block encodings, alphabet changes, or nonlocal interpreters.

## 4. Ordered-axis product theorem

Let an ECA source rule `r` have source essential-offset set

`E_r subset {-1,0,+1}`.

The accepted ordered-axis 2D local composite is

`G_{r,2} = F_{r,2} o F_{r,1}`,

with the first pass acting along one axis and the second pass along the other.

### Theorem: exact essential-offset product

For every ECA rule,

`E(G_{r,2}) = E_r x E_r subset Z^2`.

**Proof frozen before implementation.**

1. If either coordinate of `(i,j)` is not essential for `r`, changing the corresponding source cell cannot affect the relevant first-pass value or cannot affect the second-pass output. Thus no offset outside `E_r x E_r` is essential.
2. Take `(i,j) in E_r x E_r`. Because input `i` is essential, there is a one-dimensional neighborhood in row `j` where toggling its `i`-th input toggles that row's first-pass output. Because input `j` is essential, there is an outer neighborhood of first-pass values where toggling the `j`-th intermediate input toggles the final output.
3. Any nonconstant Boolean local rule is surjective onto `{0,1}`. The other rows are disjoint source variables, so choose each independently to realize the other outer intermediate values required by the second sensitivity witness. Use the first sensitivity witness on row `j`.
4. The resulting two `3x3` source patches differ only at `(i,j)` and have different final outputs. Therefore every `(i,j) in E_r x E_r` is essential.

So equality holds; there is no hidden cancellation class to discover in the census.

### Rank consequence

The theorem immediately gives the complete target-rank classification.

- If `E_r` is empty or `{0}`, `rho_C(G_{r,2})=0`. These are exactly ECA `{0,51,204,255}`.
- If `E_r` is a singleton nonzero offset, `E_r x E_r` is one nonzero diagonal displacement and target rank is 1. These are exactly `{15,85,170,240}` under the repository bit convention (`15=not L`, `85=not R`, `170=R`, `240=L`).
- If `|E_r|>=2`, the product spans rank 2:
  - if `0` and a nonzero `a` lie in `E_r`, then `(a,0)` and `(0,a)` are independent;
  - if `E_r={-1,+1}`, then `(-1,-1)` and `(-1,+1)` are independent.
  Thus every remaining 248 ECA has target rank 2.

A `1->0` causal-rank transition is therefore impossible in this constructor.

This theorem replaces the original protocol's proposed "minimal-collapse bet." The exhaustive census below is a regression/audit of this deduction, not evidence discovered after looking at the result.

## 5. Frozen exact census and controls

### C0 — 0D / center-only controls

Under the canonical center-only ECA embeddings `{0,51,204,255}`, there is no essential nonzero displacement, so `rho_C=0`.

### C1 — complete ECA source census

For all 256 ECA rules on `Z`, compute essential offsets in `{-1,0,+1}`.

**Theorem/control:** exactly `{0,51,204,255}` have source `rho_C=0`; every other rule has source `rho_C=1`.

### C2 — complete 1D→2D axial target replay

For every `r in 0..255`:

1. evaluate the accepted ordered-axis `G_{r,2}` on all `2^9=512` Moore patches;
2. determine all nine essential offsets by exact single-variable influence checks;
3. compute `rho_C` by exact integer rank;
4. compare the essential-offset set with the theorem prediction `E_r x E_r`;
5. retain complete discrepancies if any.

Any discrepancy between the independently implemented evaluators or between the enumerated essential set and `E_r x E_r` is an implementation/theorem failure and blocks interpretation. It is not scored as an interesting failed scientific bet.

### C3 — analytic named controls

- `{0,51,204,255}`: target rank 0.
- `{15,85,170,240}`: explicit one-input diagonal formulas, target rank 1.
- rule `90`: its two-pass composite is parity of the four diagonal corners, target rank 2.
- rule `150`: its two-pass composite is parity of all `3x3` cells, target rank 2.

These formulas are checked independently before relying on aggregate counts.

## 6. Cross-comparisons to accepted dimensional families

After the exact replay, report set intersections and contingency counts against accepted guard-free axial classifications:

- the 66 exact literal-replication-compatible sources;
- the 24 axis-commuting sources;
- the 14 satisfying both;
- the 16 affine ECA sources.

Import the accepted canonical result/source and hash it. These are exact descriptive cross-tabs, not independent samples and not statistical enrichment tests. No p-values, natural-selection language, or post-hoc selectivity claim is allowed.

Also report each rule's causal-rank transition. By theorem the only possible labels here are:

- `0->0` for the four center-only rules;
- `1->1` for the four noncentral unary projection/complement rules;
- `1->2` for the remaining 248.

The earlier allowed `1->0` label is removed because the product theorem excludes it.

## 7. Relational-lift profile: bookkeeping, not a new classification

Define for a declared adjacent lift

`(rho_T(source family), rho_T(inherited image), rho_T(target family), rho_C(target local law))`.

### R0 — 0D→1D center-only embedding

For each 0D center-only law:

`(0,0,1,0)`.

The target full shift makes one translation direction available; the inherited unary law uses no nonzero displacement.

### R1 — accepted 1D→2D axial setting

For the full 1D source family, copied image, and full 2D target:

`(1,1,2,rho_C(G_{r,2}))`.

The first Gate-1 review correctly observed that, for this constructor, the last component contains **no information beyond the source essential-offset set** because `E(G_{r,2})=E_r x E_r`. The unit must state this negative result explicitly. The profile is useful only as bookkeeping that keeps available translation rank separate from law-used displacement rank; it is not a newly selective dimensional invariant.

A 2D lattice remains 2D even for identity dynamics. `rho_C` measures dependency directions used by a local law, not the ontology or intrinsic dimension of the lattice.

## 8. What this does and does not test

The unit separates quantities that earlier discussion risked conflating:

| Quantity | Control showing it is distinct |
| --- | --- |
| stored bits / alphabet size | finite product alphabets and correction stacks need not raise `rho_T` |
| independent channel/action count | anchored `S_m` can have arbitrarily many channels while `rho_T=1` |
| declared-family translation rank | `S_m` has rank 1 but its translation closure `S'_m` has rank 2 |
| ambient coordinate count | literal replication adds an ambient coordinate while copied-image `rho_T` is unchanged |
| causal displacement rank | ordered-axis target rank is determined exactly by `E_r x E_r` |

A successful replay supports the correctness and usefulness of these definitions and the product theorem in the declared constructor. It does **not** establish:

- intrinsic or representation-independent spatial dimension;
- that `rho_T` or `rho_C` is a unique or sufficient definition of dimension;
- that causal rank must equal ambient lattice dimension;
- that every higher-dimensional law uses every available direction;
- that the ordered-axis product theorem generalizes to other lift architectures;
- self-assembly, endogenous control, renormalization, spacetime emergence, a physical ontology, or metaphysical conclusions;
- a mathematical equivalence to Buddhist dependent origination;
- any connection to the separate `8n+1` prime motif.

## 9. Dependency on the zero-dimensional base-case unit

This protocol is intentionally queued while #136 completes.

- `rho_T`, `rho_C`, T4a/T4b, and the ordered-axis product theorem do not depend on a positive #136 result.
- Historical motivation involving the 0D floor and center-only embedding may be treated as accepted program context only after #136 is accepted on `main`.
- Implementation may proceed after this protocol's own renewed Gate 1 because it requires no #136 output.
- **Primary evaluation may not begin until #136 is accepted on `main` or explicitly reconciled.** If #136 materially changes an assumption used here, amend this protocol and obtain renewed Gate 1 before evaluation.

## 10. Implementation and independent checks

No implementation or source-domain execution is authorized before renewed exact-head Gate 1.

After approval, the implementation-only/no-result sub-PR must freeze:

- exact imported source/result hashes for guard-free axial, transverse-freedom/correction-stack comparison, and intervention-axis comparison;
- the exact ordered-axis convention used for `G_{r,2}`;
- canonical rule ordering `0..255`, Moore-offset ordering, and discrepancy ordering;
- a scalar tuple/Boolean ECA + axial evaluator;
- an independently implemented packed/table evaluator over all 512 target patches;
- essential-variable tests in both implementations;
- exact integer rank computation with no floating-point tolerance;
- permanent CI and result-integrity scaffolding.

For essential nonzero offsets `E subset Z^2`:

- rank 0 iff `E` is empty;
- rank 1 iff `E` is nonempty and every pair has zero `2x2` determinant;
- rank 2 otherwise.

The independent evaluators must agree on all `256*512` target outputs, every essential-offset verdict, every rank, and every comparison to `E_r x E_r`.

Translation-rank statements are theorem-backed. Finite tori, if used at all, are regression illustrations and never definitions of `rho_T`.

Proposed canonical paths:

- verifier: `scripts/verify_relational_rank.py`;
- result: `results/relational_rank_20260912.json`;
- workflow: `.github/workflows/research-relational-rank.yml`.

## 11. Frozen predictions and scoring

- **P1:** T0/T1 controls give `rho_T=0,1,2` at the 0D, 1D-full-shift and 2D-full-shift examples.
- **P2:** literal 1D→2D replication preserves inherited-image `rho_T=1` inside a rank-2 full target.
- **P3:** finite product alphabets remain rank 1 on `Z`; anchored `S_m` is rank 1 while translation-closed `S'_m` is rank 2. This paired control explicitly demonstrates presentation dependence.
- **P4:** source ECA census: exactly `{0,51,204,255}` have source `rho_C=0`; all other ECA have source `rho_C=1`.
- **P5:** ordered-axis product theorem: for every source, enumerated target essential offsets equal `E_r x E_r`; target ranks are 0 for four center-only rules, 1 for `{15,85,170,240}`, and 2 for the other 248.
- **P6:** rules 90 and 150 and all eight unary controls match their explicit formulas/ranks.
- **P7:** exact cross-tabs against the accepted 66/24/14/16 source families are reported descriptively only.
- **P8:** relational-lift profiles are reported as bookkeeping, together with the explicit negative statement that their target `rho_C` component is determined by source essential offsets in this constructor.

P1–P6 are theorem/regression controls. A mismatch blocks interpretation and triggers implementation/proof debugging; it is not a post-hoc opportunity to substitute a new dimensional criterion. P7 contains exact descriptive counts but no predeclared enrichment bet.

## 12. Required workflow

Use the repository gathering/sub-PR protocol:

1. protocol-correction sub-PR into `gather/dimensional-relational-rank`;
2. author self-review and merge after exact-head checks are green;
3. renewed independent **Gate 1** on the exact integrated gathering head;
4. only after Gate 1: implementation-only/no-result sub-PR;
5. implementation self-review and merge when green;
6. wait for #136 acceptance/reconciliation before primary evaluation;
7. evaluation sub-PR performs the first canonical run;
8. reporting sub-PR updates the dated note, dimensional Program/checkpoint, knowledge/catalog entries, and any warranted AGENTS summary;
9. independent exact-head **Gate 2**;
10. reviewer merge to `main` only after Gate 2 and exact-head checks are green.

Any material change after Gate 1 to the rank definitions, declared families, product theorem, axial domain, imported cross-comparisons, discrepancy ordering, or interpretation ceiling requires renewed Gate 1.

## 13. Renewed Gate-1 review questions

The independent reviewer should verify the corrected exact head, especially:

1. Is `rho_T = rank((H_B/K_B) tensor Q)` well-defined and correctly scoped for the infinite families used here?
2. Do T4a/T4b fairly expose, rather than hide, the dependence of `rho_T` on the declared family/presentation?
3. Is `rho_C` correctly based on essential offsets from the output origin, with the pure-shift control ruling out pairwise-difference definitions?
4. Is the proof `E(G_{r,2})=E_r x E_r` complete for every nonconstant Boolean ECA, including the independent realizability of the outer sensitivity context? Are constants and center-only maps handled correctly?
5. Does the stated rank consequence exhaust all subsets of `{-1,0,+1}` without a missed rank-one or cancellation case?
6. Are the repository rule IDs/formulas for `{15,85,170,240}`, 90 and 150 correct under the accepted bit convention?
7. Does the corrected relational-lift profile now state strongly enough that, for this constructor, target `rho_C` adds no information beyond the source essential-offset set?
8. Are the 66/24/14/16 cross-tabs worth retaining as descriptive bookkeeping without implying enrichment or selectivity?
9. Is the #136 dependency strong enough to prevent contradictory predecessor evidence from being ignored while allowing implementation to queue after Gate 1?
10. Are the non-claims strong enough that "dependent origination" cannot be mistaken for evidence, doctrine, intrinsic dimension, or a physics claim?

Binding corrections must land before implementation or source-domain execution. Renewed approval must name the exact integrated gathering-head SHA.
