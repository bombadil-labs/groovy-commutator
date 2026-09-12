# Protocol: relational rank and the first used spatial direction — 2026-09-12

**Status:** frozen before implementation/evaluation. Nothing in this protocol has been run.  
**Program:** *Dimensional Closure and the Commutator Lift*.  
**Authored by:** Codex / OpenAI GPT-5.6 Sol.  
**Protocol review:** pending independent Gate 1 on the exact integrated gathering head. **No implementation or source-domain evaluation is authorized before Gate 1.**  
**Base:** `main` at `06b6732423d5ed01a2d996bc9d7fe25cef7af50d`.  
**Predecessor:** zero-dimensional base-case gathering PR #136. Its protocol has independent Gate-1 approval at `c46a6f7d4c13a56512b20832be4f1b2489a50f78`, but no canonical #136 result exists when this protocol is frozen.

## 1. Why this unit

The dimensional program has repeatedly learned that **more named coordinates do not automatically mean more independent spatial relation**:

- literal replication into an added axis gives a higher-dimensional ambient lattice while the inherited image remains constant along the new direction;
- Rule32 correction stacks can add represented bits per site without adding corresponding whole-field distinction capacity;
- fixed-width or multi-channel systems can carry arbitrarily many local bits/actions while remaining longitudinally one-dimensional under a declared representation budget;
- native higher-dimensional target states can support possibilities and interventions absent from the inherited image.

The user's phrase **"dependent origination"** motivates the question but is not a mathematical or Buddhist-doctrinal claim of this protocol. The operational translation is narrower:

> **Can we distinguish the number of spatial relation directions available to a represented state family from the number of relation directions actually used by its local law?**

This protocol introduces two deliberately separate ranks:

1. **translation rank** `rho_T`: how many independent lattice-translation directions act nontrivially on a declared state family;
2. **causal displacement rank** `rho_C`: how many independent displacement directions are spanned by essential inputs of a declared local update law.

The aim is not to define intrinsic dimension once and for all. It is to test whether these ranks cleanly reject known false positives—extra bits, copied axes, and parallel channels—and to census what the accepted guard-free 1D→2D axial constructor actually does with its second ambient direction.

## 2. Translation rank of a state family

Let a declared state family `B` lie in configurations over the infinite lattice `Z^D`. Let `tau_v` denote translation by `v in Z^D`.

Define the **setwise translation group**

`H_B = { v in Z^D : tau_v(B) = B }`.

Define the **pointwise translation kernel**

`K_B = { v in H_B : tau_v(x) = x for every x in B }`.

Both are abelian subgroups of `Z^D`. Define

`rho_T(B) = rank_Q( (H_B / K_B) tensor Q )`.

Thus torsion, if present in some periodic presentation, contributes no free translation direction. The primary statements below use infinite families, not a fixed finite torus.

Interpretation inside this protocol only:

- `rho_T=0`: no nontrivial translation direction acts on distinguishable states in the family;
- `rho_T=1`: one independent translation direction acts nontrivially;
- and so on.

This is a **presentation-relative symmetry/action rank**. It is not asserted to be intrinsic topological dimension under arbitrary encodings.

### T0 — zero-dimensional floor

For the binary 0D state set `{0,1}` on the one-point lattice, the translation group is trivial, so

`rho_T = 0`.

### T1 — full shifts

For the full binary shift on `Z^d`, `H_B = Z^d` and `K_B = {0}`, so

`rho_T = d`.

This is a theorem control for `d=1,2` and the general formula is recorded analytically.

### T2 — literal replication image

Let `P_d` be literal replication of a `d`-dimensional configuration along one new axis into `Z^(d+1)`, as in the accepted guard-free axial control. On the copied image:

- every old-axis translation acts as before;
- translation by the new basis vector fixes **every** copied configuration.

Therefore the new-axis generator lies in `K_B` and

`rho_T(P_d(B_d)) = rho_T(B_d)`

for the full inherited source family. In particular the 1D→2D copied beam has `rho_T=1`, while the full 2D target shift has `rho_T=2`.

This is the first central control: **ambient coordinate count rises while inherited translation rank does not.**

### T3 — product alphabets and correction coordinates

Changing the per-site alphabet or stacking finitely many represented coordinates over the same `Z` lattice does not, by itself, add a translation generator. The full product shift `(A^m)^Z` has `rho_T=1` for every finite `m`.

The accepted Rule32 correction-stack results are imported only as a comparison: represented bits/site grow with correction depth while the whole-field image remains source-bounded and lives on the same longitudinal lattice. This protocol does not reclassify correction depth as spatial dimension.

### T4 — many anchored parallel channels

For each finite `m>=1`, define a clean control family `S_m` on `Z^2`: arbitrary binary values live on the `m` horizontal tracks

`y = 0, 2, 4, ..., 2(m-1)`

and every other site is fixed to a declared background symbol. The track positions are anchored as part of the family.

Then horizontal translations preserve `S_m`; nonzero vertical translations do not preserve the anchored track set. Hence

`H_{S_m} = Z e_x`, `K_{S_m}={0}`, and `rho_T(S_m)=1`

for every finite `m`.

This control is paired, but not identified, with the accepted intervention-axis result: separated Rule90 channels can support intervention rank at least `m` under the declared support budget. Thus **arbitrarily many independently addressable channels/actions need not imply translation rank greater than one.**

## 3. Causal displacement rank of a local law

Let a translation-equivariant binary CA on `Z^D` have finite neighborhood offsets `N subset Z^D` and local Boolean rule `g`.

An offset `v in N` is **essential** when there exist two local patches that differ only at `v` and for which `g` gives different outputs.

Let `E(g)` be the set of essential offsets. Define the **causal displacement rank**

`rho_C(g) = rank_Z < E(g) >`,

the rank of the subgroup of `Z^D` generated by the essential displacement vectors, measured from the output site at the origin. The center offset `0` contributes no rank.

Examples:

- a constant, identity, or center-negation rule has `rho_C=0`;
- a pure one-cell shift has `rho_C=1` even though only one input is essential;
- a rule with essential offsets spanning two non-collinear directions has `rho_C=2`.

`rho_C` is invariant under invertible integer changes of lattice basis because such maps preserve subgroup rank. It is **not** claimed invariant under arbitrary block encodings, alphabet changes, or nonlocal interpreters.

This rank is about directions the **law uses on the full ambient shift**. It is deliberately not identified with `rho_T` for arbitrary constrained subfamilies.

## 4. Frozen causal-rank census

### C0 — the 0D / center-only controls

Under the center-only ECA embeddings of the four 0D laws `{0,51,204,255}`, only the center site can be essential. Therefore all four have

`rho_C = 0`.

This means the canonical 0D→1D embedding opens an available 1D translation direction in the target full shift (`rho_T: 0→1`) while these inherited laws themselves still use no nonzero displacement (`rho_C=0`). That distinction is an interpretation of the declared ranks, not a claim that spacetime emerges.

### C1 — complete ECA source census

For all 256 ECA rules on `Z`, compute the essential offsets in `{-1,0,+1}`.

**Theorem/control prediction:** exactly the four center-only rules `{0,51,204,255}` have `rho_C=0`; every other ECA has `rho_C=1`.

A mismatch is an implementation error.

### C2 — complete 1D→2D axial target census

For every ECA source rule `r`, form the accepted guard-free ordered-axis 2D local composite

`G_{r,2} = F_{r,2} o F_{r,1}`,

using the repository's exact axis convention. Its output at one site is a Boolean function of the `3x3` Moore patch, so the complete local domain has only `2^9=512` patches.

For every `r in 0..255`:

1. evaluate `G_{r,2}` on all 512 patches;
2. determine all nine essential offsets by exact single-variable influence checks;
3. compute `rho_C(G_{r,2}) in {0,1,2}` from those offsets;
4. retain the complete essential-offset set and rank.

This census is the primary new evidence of the unit.

### C3 — minimal-collapse bet

Freeze the following falsifiable classification before evaluation:

- `rho_C=0` exactly for `{0,51,204,255}`;
- `rho_C=1` exactly for the four off-center unary projections/complements `{15,85,170,240}`;
- every other ECA source has `rho_C(G_{r,2})=2`.

Rationale frozen before execution:

- constants and center-only maps remain center-only after the two axial passes;
- rules 170/240 are right/left projections and 85/15 their complements; two ordered axial passes collapse them to a single diagonal dependency, so rank one is expected;
- nonlinear or multi-input sources are expected to leave essential displacements spanning both axes, but this last step is the actual bet and may fail through cancellation or composition identities.

If C3 fails, report every counterexample and its complete essential-offset set. **Do not repair the classification after inspection.** A failed C3 is a useful result.

### C4 — fixed controls inside the 2D census

Regardless of C3:

- rules `0,51,204,255` must replay as rank-zero controls;
- rules `15,85,170,240` must be checked against the explicit diagonal one-input formulas before relying on the rank-one expectation;
- rule `150` (three-input parity) must have `rho_C=2`; its axial composite is the parity of the `3x3` patch;
- rule `90` must have `rho_C=2`; its axial composite has the four diagonal corners as essential parity inputs.

Any failure of these analytic controls blocks interpretation.

## 5. Frozen cross-comparisons to accepted dimensional families

After the C2 census, report exact set intersections and contingency counts against the already accepted guard-free axial classifications:

- the 66 exact literal-replication-compatible sources;
- the 24 axis-commuting sources;
- the 14 satisfying both;
- the 16 affine ECA sources.

The implementation must import the accepted result artifact or an exact repository source for these sets and hash it. Do not silently reconstruct a remembered list if the canonical artifact is available.

These are **descriptive exact cross-tabs**, not independent samples and not statistical enrichment tests. No p-values or claims of natural selection are allowed.

Also report each rule's transition

`rho_C(r in 1D) -> rho_C(G_{r,2} in 2D)`.

The allowed labels are only:

- `0->0`;
- `1->0`;
- `1->1`;
- `1->2`.

No monotonicity theorem is assumed. A `1->0` rule, if any, is a genuine composition collapse and must be retained.

## 6. Relational-lift profile

For this protocol define, purely as bookkeeping, the **relational-lift profile** of a declared adjacent lift as

`(rho_T(source family), rho_T(inherited image), rho_T(target family), rho_C(target local law))`.

For the two base cases:

### R0 — 0D→1D center-only embedding

For each of the four 0D laws:

`(0, 0, 1, 0)`

where the inherited 0D state itself has no translation action, the full 1D target makes one direction available, and the center-only law uses no nonzero displacement.

### R1 — 1D→2D literal-replication/axial setting

For the full 1D source family and its copied image inside the full 2D target:

`(1, 1, 2, rho_C(G_{r,2}))`.

Thus every rule opens an **available** second target translation direction at the family level, while only rules with `rho_C=2` are labeled, inside this protocol, as **using full causal rank two**.

These labels are deliberately weaker than "is genuinely two-dimensional." A 2D lattice remains 2D even for identity dynamics; `rho_C` measures use of displacement directions by the local law, not the ontology of the lattice.

## 7. What this does and does not test

The protocol is designed to separate several quantities that earlier discussion risked conflating:

| Quantity | Example that can increase it while `rho_T` stays 1 |
| --- | --- |
| stored bits / alphabet size | product alphabet, correction stack |
| independent channel count | `m` anchored tracks |
| intervention rank | separated Rule90 strip actions |
| ambient coordinate count | literal replication into an added axis |
| causal displacement rank | may increase under the 2D axial composite; this is censused |

A positive separation among these quantities supports only the usefulness of the definitions.

The unit does **not** establish:

- intrinsic or representation-independent spatial dimension;
- that `rho_T` or `rho_C` is the unique correct definition of dimension;
- that causal rank must equal ambient lattice dimension;
- that every higher-dimensional law uses every available direction;
- self-assembly, endogenous control, renormalization, spacetime emergence, a physical ontology, or a metaphysical interpretation;
- a mathematical equivalence to Buddhist dependent origination;
- any connection to the separate `8n+1` prime motif.

## 8. Dependency on the zero-dimensional base-case unit

This protocol is intentionally drafted before #136 has a canonical result so the next research cycle can be reviewed in advance.

- Its definitions of `rho_T` and `rho_C`, the C1/C2 census, and the imported older controls do **not** depend on a positive #136 result.
- The shared historical motivation from #136—0D floor, center-only embedding, and local selector roles—may be cited only after #136 is accepted on `main`.
- Implementation may proceed after this protocol's own Gate 1 because the verifier can be written without #136 output.
- **Primary evaluation may not begin until #136 is either accepted on `main` or explicitly reconciled.** If #136 produces a material correction to the 0D floor/embedding assumptions used here, amend this protocol before evaluation and obtain renewed Gate 1.

This dependency prevents a surprising predecessor result from being silently papered over while allowing protocol and implementation work to queue ahead.

## 9. Implementation and independent checks

No implementation is authorized before exact-head Gate 1.

After Gate 1, the implementation-only/no-result sub-PR must freeze:

- exact imported result/source hashes for guard-free axial, transverse-freedom/correction-stack comparison, and intervention-axis comparison;
- the exact ordered-axis convention used for `G_{r,2}`;
- canonical rule ordering `0..255`, Moore-offset ordering, and witness ordering;
- a scalar tuple/Boolean evaluator for ECA and axial composition;
- an independently implemented packed/table evaluator over all 512 2D patches;
- exact essential-variable tests in both implementations;
- exact integer rank computation for essential offsets without floating-point tolerance;
- permanent CI and result-integrity scaffolding.

For the 2D rank calculation, with essential nonzero offsets `E subset Z^2`:

- rank 0 iff `E` is empty;
- rank 1 iff `E` is nonempty and every pair of vectors in `E` has zero 2x2 determinant;
- rank 2 otherwise.

The two independent local evaluators must agree on all `256 * 512` target outputs, every essential-offset verdict, and every rank. Any disagreement blocks evaluation.

Translation-rank controls are theorem-backed. The verifier records their group generators/kernels and checks explicit witness configurations where useful; finite tori are regression checks only and are not used to define `rho_T`.

Canonical paths proposed:

- verifier: `scripts/verify_relational_rank.py`;
- result: `results/relational_rank_20260912.json`;
- workflow: `.github/workflows/research-relational-rank.yml`.

## 10. Frozen predictions and scoring

- **P1:** T0/T1 full-shift translation-rank controls hold (`rho_T=0,1,2` at 0D/1D/2D).
- **P2:** literal replication preserves inherited translation rank: 1D source/image both rank 1 inside a rank-2 full target.
- **P3:** finite product-alphabet depth and anchored channel multiplicity do not raise `rho_T` above 1 under the declared families.
- **P4:** ECA causal-rank control: exactly `{0,51,204,255}` have source `rho_C=0`, all other ECA have source `rho_C=1`.
- **P5:** C3 minimal-collapse bet for the 2D axial composite: rank-zero exactly four center-only rules, rank-one exactly `{15,85,170,240}`, all remaining rules rank two.
- **P6:** analytic 2D controls for rules 90 and 150 have rank two and the eight unary/projection controls match their frozen ranks/formulas.
- **P7:** report exact cross-tabs of target `rho_C` against the accepted 66/24/14/16 source families, with no sampling/enrichment interpretation.
- **P8:** relational-lift profiles are reported exactly as bookkeeping; no profile is promoted to an intrinsic-dimension theorem.

A P5 failure is scientific evidence, not an implementation failure, unless one of P4/P6 or the independent-evaluator checks also fails.

## 11. Required workflow

Use the repository gathering/sub-PR protocol:

1. protocol-only sub-PR into `gather/dimensional-relational-rank`;
2. author self-review and merge after exact-head checks are green;
3. independent **Gate 1** on the exact integrated gathering head;
4. only after Gate 1: implementation-only/no-result sub-PR;
5. implementation self-review and merge when green;
6. wait for #136 acceptance/reconciliation before primary evaluation;
7. evaluation sub-PR performs the first canonical run;
8. reporting sub-PR updates the dated note, dimensional Program/checkpoint, knowledge/catalog entries, and any warranted AGENTS summary;
9. independent exact-head **Gate 2**;
10. reviewer merge to `main` only after Gate 2 and exact-head checks are green.

Any material change after Gate 1 to the rank definitions, declared families, axial domain, C3 bet, imported cross-comparisons, witness ordering, or interpretation ceiling requires renewed Gate 1.

## 12. Gate-1 review questions

The independent reviewer should attack this protocol before implementation:

1. Is `rho_T = rank((H_B/K_B) tensor Q)` well-defined and appropriately scoped for the infinite families used here? Is `H_B` setwise symmetry the right group, or does it accidentally reward/penalize anchored encodings?
2. Does T2 correctly give copied images the old rank rather than the ambient target rank, and is that distinction useful rather than tautological?
3. Is the anchored-track T4 control fair, or should a different many-channel family be frozen to avoid building rank one into the anchoring convention?
4. Is `rho_C` as the rank of essential displacement vectors the right local notion? Should it use offsets themselves, differences of offsets, or another declared subgroup before we run anything?
5. Is the C3 minimal-collapse classification mathematically plausible and genuinely falsifiable? Are the expected rank-one rules `{15,85,170,240}` correct under the repository's ECA bit convention?
6. Do the rule-90 and rule-150 analytic controls follow from the exact ordered-axis convention?
7. Are the 66/24/14/16 cross-tabs scientifically useful without inviting post-hoc enrichment claims?
8. Does the relational-lift profile cleanly separate available translation rank from used causal rank, or is it merely renaming ambient dimension and dependency span?
9. Is the #136 dependency strong enough to prevent contradictory predecessor evidence from being ignored while still allowing useful implementation work to proceed?
10. Are the non-claims strong enough that the interpretive phrase "dependent origination" cannot be mistaken for evidence, doctrine, or a physics claim?

Gate 1 should be strong. Binding corrections must land before implementation or any source-domain execution, and renewed approval must name the exact integrated gathering-head SHA.