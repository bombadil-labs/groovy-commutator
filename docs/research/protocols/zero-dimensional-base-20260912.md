# Protocol: zero-dimensional base and shared law-to-state selector — 2026-09-12

**Status:** frozen before implementation/evaluation; revised after independent Gate-1 review. Nothing in this protocol has been run.  
**Program:** *Dimensional Closure and the Commutator Lift*.  
**Authored by:** Codex / OpenAI GPT-5.6 Sol.  
**Protocol review:** Claude Code, Fable 5.1 reviewed gathering head `ca5a34addafebbc1feba91f1a1a35edbcc24a615` on 2026-09-12 and required binding corrections B1–B3 plus clarifications C1–C2. This revision incorporates them and requires renewed independent Gate 1 on the exact integrated gathering head before implementation or evaluation.  
**Base:** `main` at `06b6732423d5ed01a2d996bc9d7fe25cef7af50d`.

## 1. Why this unit

The dimensional program already has two distinct achievements that must not be conflated:

1. low-dimensional rule/state cardinality coincidences: a binary radius-one 0D rule has two truth-table bits, matching the two outer cells of a 1D radius-one neighborhood; a binary ECA has eight truth-table bits, matching the eight outer cells of a 2D Moore neighborhood;
2. an explicit all-finite-dimensional stored-program/routing construction whose higher-dimensional laws are compositionally represented rather than stored as unrestricted flat truth tables.

The raw cardinality match breaks at the next rung: a general binary 2D radius-one Moore rule has 512 truth-table bits whereas the outer shell of a 3D `3x3x3` neighborhood has 26 cells. That does not decide the structured tower, because the accepted routing construction uses a factorized program family rather than arbitrary 512-bit laws.

This unit asks a smaller bottom-of-tower question:

> **Are the 0D→1D and 1D→2D shell constructions genuinely instances of one local selector semantics, once role overlap, geometric symmetry, and the distinction between static lookup and repeated dynamics are made explicit?**

The unit is deliberately an **exact local base-case audit**. Stateful repeated execution is removed from this unit and reserved for a separately frozen follow-up after this structural audit is accepted. A positive result here is therefore not a dynamical dimensional lift.

## 2. Canonical 0D floor

Take the 0D binary configuration space to be the one-point lattice with one bit `x in {0,1}`. A deterministic local law is a map `f:{0,1}->{0,1}`. The complete 0D rulespace is the four unary Boolean maps:

- `00`: constant 0;
- `01`: identity;
- `10`: negation;
- `11`: constant 1.

Under the canonical center-only ECA embedding, these are rules `0`, `204`, `51`, and `255`: left and right ECA inputs are ignored.

Every 0D rule is affine over GF(2), `f(x)=a x xor b`. The existing repository affine-commutator theorem therefore applies to the four center-only embeddings without defining a new 0D derivative. Under that accepted convention the expected constant Groovy responses are frozen as:

- rule `0`: `G=0`;
- rule `204`: `G=0`;
- rule `51`: `G=1`;
- rule `255`: `G=1`.

This is a theorem/regression control. It establishes that the complete 0D law space has no nonlinear commutator structure under the existing convention; it does not establish that spatial dimension causes nonlinearity.

## 3. One selector semantics, with role overlap explicit

For a binary local rule with `k` address bits, let its truth-table word be

`T : {0,1}^k -> {0,1}`.

A **local selector realization** is a tuple `(P,A,S,lambda)` where:

- `P` is a fixed physical neighborhood;
- `A=(a_0,...,a_{k-1})` is an ordered list of `k` physical address sites in `P`;
- `S` is a set of `2^k` physical program sites in `P`;
- **address sites and program sites are allowed to overlap**; that overlap is a declared physical resource and is reported, not hidden;
- `lambda:{0,1}^k -> S` is a fixed bijection from configuration addresses to program sites;
- the fixed interpreter reads the address word from `A` and returns the current physical bit at `lambda(address)`.

Equivalently, for a physical patch `X`,

`Select_lambda(X) = X[lambda(a(X))]`.

The semantic rule is identical at both rungs. What changes with geometry is the neighborhood `P`, the number of address bits `k`, and the unavoidable overlap between address and program roles.

### Rung Z0: 0D→1D

Use the 1D radius-one patch `(L,C,R)`:

- `k=1`;
- `A=(C)`;
- `S={L,R}`;
- `A intersect S` is empty;
- both bijections are frozen: `Z0-A` maps `0->L,1->R`; `Z0-B` maps `0->R,1->L`.

For a prepared unary law, `(L,R)=(f(0),f(1))`; the center remains an independently choosable unary input.

### Rung Z1: 1D→2D

Use the radius-one `3x3` Moore patch with surrounding positions numbered clockwise from north as in the accepted shared-state/rule construction:

- `k=3`;
- `A=(W,C,E)` so the address is `q=4W+2C+E`;
- `S` is the eight-cell outer Moore shell;
- `A intersect S={W,E}` has size two;
- `lambda` assigns the eight ECA addresses to the eight shell sites.

Thus `W` and `E` are deliberately **dual-role cells**: they are both stored truth-table bits and two of the three current address bits. This is not an implementation accident; it is the accepted selector construction's defining self-reference.

Consequently, unlike Z0, an arbitrary fixed ECA rule word and an arbitrary three-bit address are not independent physical degrees of freedom in one `3x3` patch. The local claim is therefore evaluated over **physical patches**, not over an impossible Cartesian product of 256 rule words and eight independently supplied addresses.

### Exact role-overlap lower bound

A single-layer binary patch with `|P|` sites cannot hold `k` declared address roles and `2^k` program roles disjointly unless `k+2^k <= |P|`. Therefore any such selector must have role overlap at least

`max(0, k + 2^k - |P|)`.

For the two frozen rungs:

- Z0: `1+2-3=0`, and the construction attains zero overlap;
- Z1: `3+8-9=2`, and the accepted `(W,C,E)` selector attains exactly two overlapping roles.

This is a capacity theorem about this single-layer shell architecture, not an intrinsic-dimensional lower bound.

## 4. Frozen layout family

Truth-table addresses and spatial positions are different objects. Cardinality alone does not supply a canonical placement.

### Z0

Both orientations `Z0-A` and `Z0-B` are retained. Physical reflection swaps them. This is only an encoding-conjugacy control; 0D logical data has no spatial reflection, and the induced layout address swap must not be described as a nontrivial covariance of the unary law.

### Z1

Freeze the complete dihedral orbit of one reference assignment of addresses `000..111` around the Moore shell, together with optional global address complement. The reference ordering clockwise from north is

`000,001,011,010,110,111,101,100`.

This is the 3-bit binary-reflected Gray cycle. Duplicate layouts are deduplicated and their generating transformations retained as provenance.

The Gray family is a predeclared geometric hypothesis family because successive ring positions differ in one address bit. It is not claimed to be unique or natural. An arbitrary bijection plus a compensating decoder is the permutation null, not geometric evidence.

## 5. Frozen exact questions

This unit separates five questions that earlier drafts conflated.

### S1 — physical selector identity

For every frozen layout and every binary physical patch, decode the program word from the declared program sites, decode the address from the declared address sites, and verify that the local output equals the bit at the addressed program site.

- Z0: all `2^3=8` physical three-cell patches under both orientations;
- Z1: all `2^9=512` physical Moore patches under every frozen Gray-family layout.

S1 is an implementation/theorem control. It does **not** mean every Z1 program word can be independently applied to every ECA address in one physical patch.

### S2 — selector meta-rule structure

Treat the fixed selector itself as a Boolean local rule on the physical patch.

Frozen predictions:

- each Z0 orientation has all three physical inputs essential and algebraic degree exactly two;
- its polynomial can be independently derived from the multiplexer formula, e.g. for `Z0-A`, `L xor (L C) xor (R C)` over GF(2);
- every frozen Z1 layout has all nine physical inputs essential and algebraic degree exactly four;
- the accepted shared-state/rule theorem gives exactly six quartic terms for every Z1 layout because six shell/program cells are not address variables while `W,E` are dual-role address/program cells.

The comparison `degree = k+1` at `k=1` and `k=3`, together with essentiality of every physical site, is reported as a property of this selector semantics. It is not evidence that arbitrary future rungs obey the same formula.

### S3 — geometric symmetry obstruction and classification

Do **not** score a vacuous transform-then-reindex covariance. Any spatial permutation can be compensated by reindexing the decoder, which is the permutation null.

Instead compare independently defined transformations of ECA address space with independently defined square-shell symmetries.

Let:

- `M(L,C,R)=(R,C,L)` be ECA left/right mirror;
- `C(L,C,R)=(1-L,1-C,1-R)` be address complement;
- `MC` be their composition.

Frozen analytic controls before enumeration:

1. `M` has four fixed addresses (`000,010,101,111`). Every nonidentity reflection of the eight-site Moore shell fixes exactly two shell sites. Since conjugacy preserves cycle type, **no layout whatsoever** can make an ECA mirror equal a shell reflection.
2. `C` and `MC` are fixed-point-free involutions with cycle type `2^4`. Among nonidentity `D4` shell actions only the 180-degree rotation has cycle type `2^4`; quarter-turns have two 4-cycles and reflections have two fixed sites.
3. For the reference Gray layout, the 180-degree antipodal pairs are
   `000<->110`, `001<->111`, `011<->101`, `010<->100`.
   These are neither the complement pairs nor the mirror-complement pairs. Dihedral images and global address complement preserve that mismatch.

**Frozen prediction:** for every layout in the declared Gray family, the intersection between induced `D4` address permutations and the four-element ECA transformation group generated by `M` and `C` is the identity only.

The verifier enumerates this as an independent regression of the hand proof and retains complete permutation/cycle-type tables. A pass is a **negative geometric result**: the Gray shell placement does not make the familiar ECA mirror/complement group into literal square symmetries.

### S4 — 0D algebra inside the accepted axial constructor

For the accepted guard-free axial constructor

`G_{r,d}=F_{r,d} o ... o F_{r,1}`,

a center-only rule acts pointwise on every axial pass. Therefore a center-only unary map `f` induces exactly `f^d` on the `d`-dimensional field.

For the four 0D embeddings:

- rule `204`: `f=id`, so `G_{204,d}=id`;
- rule `51`: `f=NOT`, so `G_{51,d}` alternates with dimension parity;
- rule `0`: every positive power is constant 0;
- rule `255`: every positive power is constant 1.

This parity fact does **not** explain why rule 51 is absent from the accepted exact-replication family. The interface condition uses `u_r(b)=f_r(b,b,b)`; for a center-only law, `u_r=f`. Exact replication requires the appended-axis action to fix every attainable inherited output. Identity and the two constants satisfy that condition on their attainable outputs; negation fixes no bit, so rule 51 fails every interface uniformly.

Replay of the accepted axial verifier is only a regression check of this deduction. No uniqueness or naturalness is inferred.

### S5 — structured next-rung storage fact

The accepted editable-routing construction stores `d` editable eight-bit tables, i.e. `8d` native program bits, plus separately accounted data/interpreter/physical-layout costs. Therefore its native 2D program tuple contains 16 routing bits, below the 26 cells of a 3D radius-one Moore shell.

This is a fact about the accepted factorized routing family. It is **not compression of an arbitrary 512-bit 2D truth table**, does not show those 16 bits already have a valid 3D shell interpreter, and does not establish a recursive shell law.

## 6. Frozen predictions and controls

### P1 — complete 0D floor

The four unary Boolean maps are the complete binary deterministic 0D rulespace and embed as ECA `0,204,51,255`. All four are affine.

### P2 — commutator floor

The imported affine theorem returns constants `(0,0,1,1)` for ECA `(0,204,51,255)` respectively. Any mismatch is an implementation/provenance failure.

### P3 — minimum role overlap

The disjoint-role lower bound is zero at Z0 and two at Z1, and the frozen constructions attain those minima. This explicitly replaces the rejected disjoint-role Z1 schema.

### P4 — common selector local structure

S1 and S2 hold on the complete frozen physical domains. In particular the Z0 selector has degree two/all three inputs essential and the Z1 selector has degree four/all nine inputs essential under every frozen layout.

A failure blocks the claim that the two rungs instantiate the same local selector semantics.

### P5 — no nontrivial Gray/ECA symmetry identification

S3's hand-derived obstruction and Gray-family prediction hold exactly: no nonidentity element of the ECA group `<M,C>` is induced by a `D4` shell symmetry on any frozen Gray-family layout.

This is intentionally a negative prediction. It replaces the rejected prior bet that a nontrivial covariance should exist.

### P6 — corrected axial deduction

The accepted ordered-axis constructor gives `f^d` for center-only laws; rule 51's dimension-parity dynamics are a corollary, while its exact-replication failure is explained separately by `u_51=NOT` having no fixed bit.

### P7 — scoped routing-storage comparison

The accepted editable-routing family uses `8d` native routing bits, hence 16 at `d=2`; this statement remains strictly separate from total physical storage and from arbitrary 512-bit 2D laws.

### P8 — stateful execution is deferred

This unit makes **no repeated-execution claim** for a prepared law/state representation. Any Z0/Z1 repeated-execution bridge must be a new frozen protocol with one exact architecture selected before its Gate 1. Static selector success in this unit cannot be reported as a dynamical dimensional lift.

## 7. Nulls and claim boundaries

Mandatory reporting distinctions:

1. **Cardinality null:** `2=2` and `8=8` alone establish no common mechanism.
2. **Generic multiplexer null:** `Select_lambda` is an abstract lookup recipe; shared algebra alone does not establish a spatially natural construction.
3. **Permutation null:** arbitrary placement plus compensated decoder reindexing is storage capacity, not geometric covariance.
4. **Role-overlap cost:** the Z1 shell fit works only because two cells are simultaneously program and address state. This resource must remain visible.
5. **Prepared-state boundary:** program bits are deliberately present; nothing here self-assembles or selects a program.
6. **Local-only boundary:** this unit does not establish repeated global execution, all-time preservation, or an intertwining of represented trajectories.
7. **Structured-family boundary:** `8d` concerns accepted routing syntax, not the unrestricted `2^(3^d)`-bit rule table or total physical implementation cost.
8. **Prime-motif boundary:** no connection to the separate `8n+1` observation is claimed without a later explicit mathematical map.

A failed P4 or P5 remains useful. Do not add layouts, extra layers, wider neighborhoods, new role species, or a dynamical rescue after seeing the result. Any such change is a separately frozen unit.

## 8. Implementation and independent checks

No implementation or source-domain execution is authorized before renewed exact-head Gate 1.

After approval, an implementation-only sub-PR must contain no canonical result and must freeze:

- exact Gray-family layout enumeration and deduplication;
- canonical ordering for physical patches, layouts, transformations, and witnesses;
- exact imported theorem/result hashes used for P2, P4's accepted Z1 comparison, P6, and P7;
- a scalar tuple/Boolean selector and an independently implemented packed/table evaluator;
- ANF/essential-input computation by two independent paths for P4;
- direct cycle-type/permutation comparison plus exhaustive layout enumeration for P5;
- permanent CI and result-integrity scaffolding.

Every enumerated scientific claim requires agreement between the independent implementations. Any mismatch stops evaluation.

Canonical failures retain the lexicographically first complete witness under the frozen ordering. For P5 the canonical record includes layout, shell action, induced address permutation, candidate ECA transformation, and cycle decomposition.

Proposed artifacts:

- verifier: `scripts/verify_zero_dimensional_base.py`;
- result: `results/zero_dimensional_base_20260912.json`;
- workflow: `.github/workflows/research-zero-dimensional-base.yml`.

## 9. Workflow

Use the repository gathering/sub-PR protocol:

1. protocol correction sub-PR into `gather/dimensional-zero-base`;
2. author self-review and merge after exact-head checks are green;
3. renewed independent **Gate 1** on the exact integrated gathering head;
4. only after Gate 1: implementation-only/no-result sub-PR;
5. self-review and merge implementation sub-PR when green;
6. evaluation sub-PR for the first canonical run;
7. reporting sub-PR for dated result note, dimensional Program/checkpoint, knowledge/catalog updates, and any warranted AGENTS summary;
8. independent exact-head **Gate 2**;
9. reviewer merge of the gathering PR to `main` only after Gate 2 and exact-head checks are green.

Any post-Gate-1 change to selector semantics, role contract, layout family, P1–P8, domain, scoring, witness ordering, or interpretation ceiling requires renewed Gate 1.

## 10. Interpretation contract

A positive unit can establish, at most:

> The complete binary 0D floor and the accepted 1D/ECA shared-shell construction instantiate one overlap-permitted local multiplexer semantics at the first two law/state cardinality matches; the exact overlap cost, local Boolean structure, and failure of the frozen Gray geometry to realize nontrivial ECA mirror/complement symmetries are characterized.

It cannot establish:

- a stateful or repeated dynamical dimensional lift;
- a unique, natural, or physically selected law/state layout;
- arbitrary `2D->3D` shell encoding;
- compression of arbitrary 512-bit 2D rules;
- intrinsic dimension, self-assembly, endogenous control, spacetime emergence, a physical theory, or metaphysical conclusions;
- a connection to `8n+1` or primes.

A negative result is bounded to the declared selector/layout architecture and does not disprove other law-as-state lifts.

## 11. Gate-1 review questions after the first correction round

The independent reviewer should verify the exact corrected head, especially:

1. Does the overlap-permitted `(P,A,S,lambda)` schema genuinely cover both rungs without hiding the Z1 `W/E` dual role?
2. Is the role-overlap lower bound stated and scoped correctly, and does the accepted Z1 construction attain the minimum two-cell overlap?
3. Is P4 now a meaningful shared-selector structural comparison rather than an impossible Cartesian product of rule words and independent addresses?
4. Is P5's fixed-point/cycle-type obstruction correct, including the claim that the frozen Gray family has identity-only intersection with `<M,C>`?
5. Is S4/P6 now correctly split between the true `f^d` parity statement and the actual `u_51=NOT` interface-failure mechanism?
6. Is deferring all S3/P5-style repeated execution to a separate future protocol sufficient to eliminate architecture shopping from this unit?
7. Are P2 and P7 correctly grounded in accepted repository results and scoped to their actual conventions/costs?
8. Are the interpretation ceiling and nulls strong enough that a positive local-selector audit cannot be reported as a dynamical or intrinsic-dimensional result?

Binding corrections must land before any verifier or evaluation. Renewed approval must name the exact integrated gathering-head SHA.
