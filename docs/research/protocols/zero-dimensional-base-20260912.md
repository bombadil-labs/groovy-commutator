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

Every 0D rule is affine over GF(2), `f(x)=a x xor b`. The Groovy commutator for the one-bit derivative `D(x)=x xor 0` / change-bit formulation is therefore required to reduce to the existing affine constant behavior; this is a theorem/control statement only. The scientific content begins with the law-to-state geometry, not with rediscovering that all unary Boolean maps are affine.

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

A separately reported null control samples no layouts. Instead it asks what succeeds under an unconstrained compensated permutation algebraically: all bijective layouts must be executable if the decoder is permuted with them. This is a theorem/control and is not evidence for geometry.

## 5. Three levels of success

Do not collapse these criteria.

### S1 — static addressability

For every frozen layout and every rule word, the local interpreter returns exactly the truth-table bit indexed by the declared data address.

- Z0 domain: all 4 unary rules × both input values × both orientations.
- Z1 domain: all 256 ECA rules × all 8 address triples × every frozen geometric layout.

S1 is a lookup theorem/check. It is necessary but cheap.

### S2 — symmetry covariance

The selector construction must intertwine declared transformations rather than merely survive a recompiled decoder.

Freeze the following actions:

- 0D/1D rung: spatial reflection exchanges the two program sites and transforms the unary address by `x -> 1-x`; rule-word transport is the induced address permutation.
- 1D/2D rung: left/right reflection sends ECA address `(L,C,R)` to `(R,C,L)` and acts on the Moore ring by the corresponding spatial reflection; global state complement sends address `a` to bitwise complement `~a` and transports the truth-table word by address complement, with output complement scored separately from address complement.
- square rotations are scored as layout symmetries only when accompanied by the explicitly declared address-axis action; no rotation is called a law symmetry if the ECA input semantics are changed without transport.

For each transformation, verify the appropriate commuting square: transform-then-select equals select-then-transport-output under the declared rule action.

The primary geometric claim requires at least one frozen Z1 layout whose covariance is compatible with the same address-permutation principle used at Z0. A success based only on arbitrary decoder recompilation is classified as S1-only.

### S3 — stateful dynamical realization

Static lookup is not yet a dimensional lift. Freeze a minimal repeated-execution test in which program bits are physical state and data evolve while the interpreter remains fixed.

For Z0, use periodic 1D macro-cells containing one data bit and the two unary program bits, with a fixed clock/role convention declared by the implementation before evaluation. For all four unary rules and every binary data word on rings `n=3..8`, one macro tick must update every represented data bit by the selected unary law while restoring or preserving the program representation required for the next tick.

For Z1, do **not** invent a new 2D machine if the accepted shared-state/rule or stored-program machinery can realize the same selector contract. Before implementation, the implementer must choose exactly one of two frozen paths and record which one without source-domain execution:

- `S3-direct`: reuse the accepted shared-state/rule eight-neighbor selector as the repeated-execution control, with the new geometric layout family as the only changed program placement; or
- `S3-rail-bridge`: give an explicit conjugacy/translation from the selector program word into the accepted spatial-rail / editable-routing representation and verify repeated execution there.

The chosen path must keep rule replacement as a state edit and must not hide the rule in interpreter code. The unchosen path is not evaluated in this unit and cannot become a post-hoc rescue.

S3 passes only if both Z0 and the chosen Z1 realization repeatedly execute their represented laws under one documented law→state interpretation contract. This is still a prepared construction, not self-assembly or natural selection.

## 6. Frozen predictions and controls

### P1 — complete 0D floor (theorem/control)

The four unary maps are exactly the complete binary 0D deterministic rulespace and map to center-only ECA rules `0,204,51,255`. All four are affine.

Failure indicates a definition/implementation error.

### P2 — commutator floor (theorem/control)

Under the repository's affine commutator result, all four 0D laws have constant commutator response: zero constant term for constant-0/identity and one for negation/constant-1, under the exact convention imported from the affine result. The implementation must cite and replay the existing theorem/check rather than silently define a new commutator.

This control establishes that the commutator has no nonlinear content at the floor. It does **not** prove that spatial dimension causes nonlinearity.

### P3 — common selector addressability (theorem-like implementation control)

S1 passes for every 0D rule and all 256 ECA rules under every frozen layout. A failure blocks all interpretation.

### P4 — nontrivial shared covariance (primary structural bet)

At least one frozen Gray-ring Z1 layout, together with one Z0 orientation, satisfies the full declared reflection/complement covariance using the same address-permutation selector principle, without rule-specific decoder changes.

If only S1 passes while every Z1 geometric layout fails the covariance contract, report the cardinality match as storage-only under this hypothesis family.

### P5 — repeated stateful execution (primary constructive bet)

S3 passes on both rungs for the frozen finite domains. A pass means that rule bits can serve as persistent/reusable physical program state at both 0D→1D and 1D→2D under one documented interpretation family. A failure is scoped to the chosen architecture and finite domains.

### P6 — 0D algebra explains the axial parity anomaly (deductive comparison, frozen before evaluation)

The accepted guard-free axial constructor applies the same ECA along each added axis in sequence. For the four center-only embeddings:

- rules 0, 204, 255 are already in the accepted exact-replication family;
- rule 51 (negation) is not.

Derive, before consulting any new run output, the induced action of composing a center-only unary map once per axis. For `f(x)=x xor b`, `d` sequential axial passes produce `x xor (d b)`. Thus identity is dimension-independent, while negation alternates with dimension parity. Constants require their separately derived composition behavior. Replay the accepted axial verifier only as a regression check of that deduction.

This comparison may explain why the 0D negation embedding behaves differently in that constructor. It is **not** evidence that the axial constructor is the unique dimensional lift.

### P7 — compression target for the next rung (analytic consequence, not evaluated as success)

If P4/P5 pass, state the 2D→3D question in description-length terms. For the accepted editable-routing family, a d-dimensional program stores `8d` routing bits, so the 2D member uses 16 program bits, less than the 26-cell 3D outer shell. Verify the existing repository count/provenance for this family; do not claim compression of arbitrary 512-bit 2D truth tables.

The next protocol may then ask whether the common selector/state mechanism can carry that structured 16-bit 2D program into a 3D shell or nearby local state with acceptable interpreter/locality costs. This unit does not run that experiment.

## 7. Nulls and falsification boundaries

The following distinctions are mandatory in reporting:

1. **Cardinality null:** `2=2` and `8=8` alone are not evidence of a common mechanism.
2. **Permutation null:** any bijection between truth-table addresses and equal-sized program sites can be made executable by recompiling a decoder; that is storage capacity, not geometric structure.
3. **Prepared-program null:** a fixed interpreter plus deliberately placed program bits is an existence construction, not endogenous organization.
4. **Finite-domain null:** repeated execution on finite rings establishes only the declared domains unless an analytic proof extends it.
5. **Structured-family boundary:** `8d` routing storage concerns the accepted factorized family, not the unrestricted `2^(3^d)`-bit rule table.

A scientifically useful negative result is allowed. In particular, P4 or P5 may fail while P1-P3 hold. Do not introduce a new layout, larger shell, wider radius, added role species, or alternate repeated-execution architecture after seeing those failures. Any rescue is a new frozen unit.

## 8. Implementation and independent checks

No implementation is authorized before exact-head Gate 1.

After approval, the implementation-only sub-PR must contain no canonical result and must freeze:

- exact Z1 layout enumeration and deduplication;
- exact imported theorem/result hashes used for P2, P6, and P7;
- the selected S3 path (`S3-direct` or `S3-rail-bridge`);
- canonical ordering for rules, addresses, layouts, rings, states, and witnesses;
- a scalar reference selector independent of the optimized/table evaluator;
- permanent CI and integrity-registration scaffolding.

At least two independently implemented checks are required for every scientific claim that uses enumeration:

- tuple/Boolean scalar evaluation;
- packed/vector or existing-engine evaluation.

Covariance failures retain the lexicographically first complete witness `(r, layout, transform, address/state)` under the frozen ordering. Repeated-execution failures retain the first full represented physical state and expected/actual next state.

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

Any binding change after Gate 1 to the layout family, covariance actions, finite domains, selected S3 architecture, predictions, witness ordering, or interpretation contract requires renewed Gate 1. Implementation bug fixes that do not change those scientific choices remain implementation corrections and must be recorded before evaluation.

## 10. Interpretation contract

A positive result can establish, at most:

> The complete binary 0D law space and the complete ECA law space admit a shared prepared law-to-state selector schema across 0D→1D and 1D→2D, with specified geometric covariance and finite repeated-execution witnesses under a fixed interpreter family.

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
3. Is the frozen Gray-ring symmetry family principled enough to test geometry while avoiding an arbitrary 8! search? Should any declared covariance action be weakened, strengthened, or removed before evaluation?
4. Are S1/S2/S3 cleanly separated so static lookup cannot be reported as a dynamical lift?
5. Is the `S3-direct` versus `S3-rail-bridge` preimplementation choice sufficiently frozen to prevent architecture shopping after results?
6. Is P6's parity deduction correct for the accepted ordered-axis constructor, including constant maps?
7. Is P7 scoped correctly to the accepted factorized routing family rather than arbitrary 2D rules?
8. Are the nulls and interpretation boundary strong enough that a positive result cannot be mistaken for natural selection, intrinsic dimension, or a physics claim?

Gate 1 should be strong. Binding changes must land before any verifier or source-domain execution.