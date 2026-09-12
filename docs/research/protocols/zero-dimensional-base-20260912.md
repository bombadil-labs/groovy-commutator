# Protocol: zero-dimensional base and shared law-to-state selector — 2026-09-12

**Status:** proposed and frozen before implementation/evaluation. Nothing in this protocol has been run.  
**Program:** *Dimensional Closure and the Commutator Lift*.  
**Authored by:** Codex / OpenAI GPT-5.6 Sol.  
**Protocol review:** pending independent Gate 1 on the exact integrated gathering head. **No implementation or source-domain evaluation is authorized before Gate 1.**  
**Base:** `main` at `06b6732423d5ed01a2d996bc9d7fe25cef7af50d`.

## 1. Why this unit

The dimensional program already has two distinct achievements that should not be conflated:

1. low-dimensional rule/state cardinality coincidences: a binary radius-one 0D rule has two truth-table bits, matching the two outer cells of a 1D radius-one neighborhood; a binary ECA has eight truth-table bits, matching the eight outer cells of a 2D Moore neighborhood;
2. an explicit all-finite-dimensional stored-program/routing construction whose higher-dimensional laws are compositionally represented rather than stored as unrestricted flat truth tables.

The cardinality coincidence breaks at the next raw-table step: a general binary 2D radius-one Moore rule has 512 truth-table bits whereas the outer shell of a 3D 3x3x3 neighborhood has 26 cells. That mismatch by itself does not decide the structured tower, because the accepted routing construction uses a factorized program family rather than arbitrary 512-bit laws.

The smallest missing question is therefore at the bottom of the tower:

> **Can one common, fixed law-to-state addressing mechanism realize both 0D→1D and 1D→2D, rather than merely exploiting the separate cardinality equalities 2=2 and 8=8?**

This unit installs 0D as an explicit base case and tests structural reuse before asking the 2D→3D compression question. It does not replace, reinterpret, or retroactively score prior dimensional units.

## 2. Canonical 0D objects

Take the 0D binary configuration space to be the one-point lattice with one bit `x ∈ {0,1}`. A deterministic local law is a map `f:{0,1}->{0,1}`. The complete 0D rulespace is therefore the four unary Boolean maps:

- `00`: constant 0;
- `01`: identity;
- `10`: negation;
- `11`: constant 1.

Under the canonical center-only ECA embedding, these are rules `0`, `204`, `51`, and `255` respectively: the left and right ECA inputs are ignored.

Every 0D rule is affine over GF(2), `f(x)=a x xor b`. The implementation must import the repository's existing affine-commutator convention exactly rather than introduce a new 0D derivative convention. P2 below is therefore a theorem/regression control on the four center-only ECA embeddings, not a new definition of the Groovy commutator.

## 3. Common selector schema

For a binary local rule with `k` address bits, let its truth-table word be

`T : {0,1}^k -> {0,1}`.

A **selector realization** consists of:

- a fixed set `S` of `2^k` physical program sites;
- a fixed bijection `lambda:{0,1}^k -> S` assigning configuration addresses to program sites;
- a fixed local interpreter that, given address bits `a ∈ {0,1}^k` in declared data sites and program bits `T(a')` at all sites `lambda(a')`, outputs the bit stored at `lambda(a)`.

The same schema must be instantiated without changing its semantic rule between the two rungs:

### Rung Z0: 0D→1D

- `k=1`;
- the one data/address bit is the center site of a radius-one 1D neighborhood;
- the two program sites are the two outer sites;
- the program bits are `(f(0), f(1))` in an orientation fixed before evaluation.

### Rung Z1: 1D→2D

- `k=3`;
- the address bits are the declared ordered ECA inputs `(L,C,R)`;
- the eight program sites are the outer cells of a 3x3 Moore neighborhood;
- the program bits are the eight ECA truth-table outputs in a layout fixed before evaluation.

The interpreter may depend on the declared spatial geometry and the fixed rung-independent selector recipe, but it may not contain the selected rule as hidden external data. Replacing a rule word must require changing only the program-state bits, not interpreter code.

## 4. Frozen candidate layouts

Because truth-table addresses and spatial addresses are different objects, this unit does not pretend that cardinality supplies a canonical layout. It freezes a small hypothesis family and scores all members, rather than choosing a successful layout after inspection.

### Z0 layouts

Both 1D orientations are frozen:

- `Z0-A`: address 0 on the left outer site, address 1 on the right;
- `Z0-B`: address 0 on the right outer site, address 1 on the left.

These are reflection partners and serve as a conjugacy control.

### Z1 layouts

Freeze the complete dihedral orbit of one reference assignment of the eight addresses `000..111` around the Moore ring, together with global address complement. The reference ordering is clockwise from north:

`000,001,011,010,110,111,101,100`.

This is the 3-bit binary-reflected Gray cycle. The frozen family consists of every distinct layout generated by the eight square symmetries and optional bitwise address complement. Duplicate layouts are deduplicated before evaluation and their generating symmetries retained as provenance.

This family is chosen before evaluation because it preserves nearest-neighbor adjacency of successive Gray addresses on the ring and exposes rotation/reflection/complement covariance. It is **not** claimed to be uniquely natural. Arbitrary 8! layouts are deliberately excluded from the primary claim because successful arbitrary permutation plus a compensating decoder would establish only storage capacity.

A separately reported null control samples no layouts. Instead it records the algebraic fact that any bijective placement is executable if the decoder is compensated by the inverse placement. That null is not evidence for geometry.

## 5. Three levels of success

Do not collapse these criteria.

### S1 — static addressability

For every frozen layout and every rule word, the local interpreter returns exactly the truth-table bit indexed by the declared data address.

- Z0 domain: all 4 unary rules × both input values × both orientations.
- Z1 domain: all 256 ECA rules × all 8 address triples × every frozen geometric layout.

S1 is a lookup theorem/check. It is necessary but cheap.

### S2 — symmetry covariance

The selector construction must intertwine declared transformations rather than merely survive a rule-specific recompiled decoder.

Freeze the following actions:

- **Z0 reflection:** physical reflection exchanges the two program sites. On configuration addresses this induces `x -> 1-x` only for the reflected *layout coordinates*; the transported rule word is reindexed by that address permutation. This is a covariance of the encoding contract, not a claim that unary logical input itself physically complements under reflection.
- **Z1 left/right reflection:** ECA address `(L,C,R)` maps to `(R,C,L)` and the Moore ring is reflected across the corresponding axis; the rule word is reindexed by the induced address permutation.
- **Z1 global data complement:** address `a` maps to bitwise complement `~a`; address-complement transport of the truth-table word and optional output complement are scored as distinct operations and must not be conflated.
- **Square rotations:** scored only when accompanied by an explicitly declared permutation of the three address roles. A rotation is not called a law symmetry when it changes ECA input semantics without transport.

For each declared transformation, verify the appropriate commuting square: encode/transport then select equals select under the transported address/rule contract.

The primary geometric claim requires at least one frozen Z1 layout whose covariance is compatible with the same general principle used at Z0: spatial action induces an address permutation, and the stored truth table transforms by reindexing under that permutation. A success based only on arbitrary per-rule decoder recompilation is classified as S1-only.

### S3 — stateful dynamical realization

Static lookup is not yet a dimensional lift. This criterion asks whether the stored program can participate in repeated execution while the interpreter stays fixed.

**Gate-1 boundary:** the exact physical macrocell/clock realization is itself part of the scientific architecture and must not be left to post-review implementation choice. Gate 1 must either (a) approve one exact repeated-execution architecture already present in accepted repository machinery for each rung, or (b) require this criterion to move to a separately frozen follow-up protocol. No source-domain execution may occur while S3's physical architecture is unresolved.

For Z0, the preferred minimal target is a periodic 1D representation carrying one data bit and the two unary program bits per logical site, with program retention/restoration and update cadence specified entirely before execution. For all four unary rules and every binary data word on rings `n=3..8`, one macro tick should update every represented data bit by the selected unary law while preserving the representation required for another tick.

For Z1, the preferred target is to reuse accepted repository machinery rather than invent a new machine. Candidate bridges for Gate 1 to choose between are:

- `S3-direct`: the accepted shared-state/rule eight-neighbor selector, if it can be shown to satisfy the same stored-program contract under a frozen layout; or
- `S3-rail-bridge`: an explicit conjugacy/translation from the selector program word into the accepted spatial-rail / editable-routing representation.

Gate 1 must reject architecture shopping: either select one exact route and freeze all semantic resources before implementation, or split S3 out of this unit. The unchosen route cannot become a post-result rescue.

## 6. Frozen predictions and controls

### P1 — complete 0D floor (theorem/control)

The four unary maps are exactly the complete binary 0D deterministic rulespace and map to center-only ECA rules `0,204,51,255`. All four are affine.

Failure indicates a definition/implementation error.

### P2 — commutator floor (theorem/regression control)

Replay the repository's accepted affine-commutator theorem/check on the four center-only ECA embeddings `0,204,51,255` under the **existing repository convention**. Record the exact imported theorem/result source and its expected constant response for each rule before implementation execution. Do not infer or redefine those constants from a new 0D-specific derivative.

The intended scientific statement is only that the complete 0D law space lies in the affine sector, so the accepted affine theorem leaves no nonlinear commutator structure at the floor. It does **not** prove that spatial dimension causes nonlinearity.

### P3 — common selector addressability (theorem-like implementation control)

S1 passes for every 0D rule and all 256 ECA rules under every frozen layout. A failure blocks all interpretation.

### P4 — nontrivial shared covariance (primary structural bet)

At least one frozen Gray-ring Z1 layout, together with one Z0 orientation, satisfies the full declared covariance family using the same spatial-action→address-permutation→rule-reindexing principle, without rule-specific decoder changes.

If only S1 passes while every Z1 geometric layout fails the covariance contract, report the cardinality match as storage-only under this hypothesis family.

### P5 — repeated stateful execution (conditional constructive bet)

P5 is active only if Gate 1 freezes an exact S3 physical architecture on both rungs. Under that frozen architecture, repeated stateful execution passes on both rungs for the declared finite domains. A pass means that rule bits can serve as persistent/reusable physical program state at both 0D→1D and 1D→2D under one documented interpretation family. A failure is scoped to the frozen architecture and finite domains.

If Gate 1 instead requires S3 to become a separate follow-up, this unit makes **no P5 claim** and cannot report static S1/S2 success as a dynamical lift.

### P6 — 0D algebra and the axial negation mismatch (deductive comparison, frozen before evaluation)

The accepted guard-free axial constructor applies the same ECA along each added axis in sequence. For the four center-only embeddings, accepted results place rules `0`, `204`, and `255` in the exact-replication family, while rule `51` is outside it.

Before consulting any new run output, derive the induced action of sequentially composing the center-only unary map under the constructor's exact dimensional convention, including the base-source pass count and every added-axis pass. The tempting shorthand `f^d` is **not frozen as correct** until that convention is reconciled with the accepted constructor. For affine unary maps `f(x)=a x xor b`, ordinary functional composition is elementary; however, whether the relevant exponent is `d`, `d+1`, or another count is a repository-definition question that Gate 1 must check against the accepted axial protocol.

Replay the accepted axial verifier only as a regression check of the resulting deduction. The comparison may explain rule 51's mismatch in that constructor; it is not evidence that the constructor is unique or natural.

### P7 — compression target for the next rung (analytic consequence, not evaluated as success)

If P4 and, when active, P5 pass, state the 2D→3D question in description-length terms. The accepted editable-routing construction stores one eight-bit table per declared axis in its native program tuple; its checkpoint describes `d` editable eight-bit tables (`8d` program bits) and the associated physical macrocell costs. Under that convention, the 2D native tuple has 16 program bits, which is below the 26-cell outer shell of a 3D radius-one Moore neighborhood.

This is **not** compression of an arbitrary 512-bit 2D rule table. The implementation must cite the accepted routing note/checkpoint and preserve all interpreter, role, locality, and physical-storage costs. This unit does not test 2D→3D shell storage.

## 7. Nulls and falsification boundaries

The following distinctions are mandatory in reporting:

1. **Cardinality null:** `2=2` and `8=8` alone are not evidence of a common mechanism.
2. **Permutation null:** any bijection between truth-table addresses and equal-sized program sites can be made executable by compensating the decoder; that is storage capacity, not geometric structure.
3. **Prepared-program null:** a fixed interpreter plus deliberately placed program bits is an existence construction, not endogenous organization.
4. **Finite-domain null:** repeated execution on finite rings establishes only the declared domains unless an analytic proof extends it.
5. **Structured-family boundary:** `8d` routing-table syntax concerns the accepted factorized family, not the unrestricted `2^(3^d)`-bit rule table; physical storage and interpreter costs remain explicit.

A scientifically useful negative result is allowed. In particular, P4 or active P5 may fail while P1-P3 hold. Do not introduce a new layout, larger shell, wider radius, added role species, or alternate repeated-execution architecture after seeing those failures. Any rescue is a new frozen unit.

## 8. Implementation and independent checks

No implementation is authorized before exact-head Gate 1.

After approval, the implementation-only sub-PR must contain no canonical result and must freeze or record, as required by Gate 1:

- exact Z1 layout enumeration and deduplication;
- exact imported theorem/result hashes used for P2, P6, and P7;
- whether S3/P5 remains in this unit and, if so, its exact approved physical architecture;
- canonical ordering for rules, addresses, layouts, rings, states, and witnesses;
- a scalar reference selector independent of the optimized/table evaluator;
- permanent CI and integrity-registration scaffolding.

At least two independently implemented checks are required for every scientific claim that uses enumeration:

- tuple/Boolean scalar evaluation;
- packed/vector or existing-engine evaluation.

Covariance failures retain the lexicographically first complete witness `(r, layout, transform, address/state)` under the frozen ordering. Repeated-execution failures, if P5 is active, retain the first full represented physical state and expected/actual next state.

Canonical result path proposed: `results/zero_dimensional_base_20260912.json`.  
Verifier path proposed: `scripts/verify_zero_dimensional_base.py`.  
Workflow path proposed: `.github/workflows/research-zero-dimensional-base.yml`.

## 9. Required workflow

Use the repository gathering/sub-PR protocol:

1. protocol-only sub-PR into `gather/dimensional-zero-base`;
2. author self-review and merge of that sub-PR when exact-head checks are green;
3. independent **Gate 1** review of the exact integrated gathering head;
4. only after Gate 1: implementation-only/no-result sub-PR;
5. self-review and merge implementation sub-PR when green;
6. evaluation sub-PR for the first canonical run;
7. reporting sub-PR for the dated result note, dimensional Program page/checkpoint, knowledge/catalog updates, and any AGENTS result summary warranted by the evidence;
8. independent **Gate 2** on the exact final gathering head;
9. reviewer merge of the gathering PR to `main` only after Gate 2 and exact-head checks are green.

Any binding change after Gate 1 to the layout family, covariance actions, finite domains, active S3 architecture, predictions, witness ordering, or interpretation contract requires renewed Gate 1. Implementation bug fixes that do not change those scientific choices remain implementation corrections and must be recorded before evaluation.

## 10. Interpretation contract

A positive S1/S2 result can establish, at most:

> The complete binary 0D law space and the complete ECA law space admit a shared prepared law-to-state selector schema across 0D→1D and 1D→2D, with specified geometric covariance under a fixed interpretation family.

Only if P5 is active and passes may the result additionally claim finite repeated stateful execution of that represented program under the exact frozen physical architectures.

It would not establish:

- that the Gray-ring layout is unique, natural, or physically selected;
- that arbitrary 2D rule tables fit a 3D shell;
- that the factorized routing family is universal among higher-dimensional laws;
- intrinsic spatial dimension, self-assembly, endogenous control, emergence of spacetime, a physical theory, or metaphysical conclusions;
- any connection to the separate `8n+1` prime observation beyond a shared numerical motif unless a later protocol specifies an actual mathematical map.

A negative result is also bounded to the frozen selector/layout/architecture family. It does not disprove all law-as-state dimensional lifts.

## 11. Gate-1 review questions

The independent reviewer should attack the following points before implementation:

1. Is the 0D definition and center-only ECA embedding canonical enough for a base-case control?
2. Does the selector schema genuinely state one semantic mechanism at `k=1` and `k=3`, or have rung-specific details smuggled in two different constructions?
3. Is the frozen Gray-ring symmetry family principled enough to test geometry while avoiding an arbitrary 8! search? Are the reflection/complement/rotation actions stated as genuine encoding covariances rather than accidental logical symmetries?
4. Are S1/S2/S3 cleanly separated so static lookup cannot be reported as a dynamical lift?
5. Should S3/P5 be frozen now to one exact accepted architecture, or split into a follow-up rather than leaving physical design freedom after Gate 1?
6. Does P2 correctly defer to the existing affine-commutator convention rather than inventing a 0D derivative?
7. What is the exact pass count in P6 under the accepted ordered-axis constructor, and does it actually explain rule 51's exclusion from the exact-replication family?
8. Is P7 scoped correctly to the accepted factorized routing family, with syntax bits distinguished from total physical storage/interpreter cost?
9. Are the nulls and interpretation boundary strong enough that a positive result cannot be mistaken for natural selection, intrinsic dimension, or a physics claim?

Gate 1 should be strong. Binding changes must land before any verifier or source-domain execution.