# Protocol: finite interface history as local closure state — 2026-09-11

**Status:** frozen before implementation and evaluation. Nothing has been run under this protocol.  
**Program:** *Dimensional Closure and the Commutator Lift*, constructive follow-up to the accepted touching-strip interface-factor unit.  
**Authored by:** Codex / OpenAI GPT-5.6 Sol.  
**Protocol review:** pending exact-head Claude/Fable Gate 1. **No implementation or primary evaluation is authorized before Gate 1.**  
**Tracking:** issue #129.  
**Base dependency:** interface-factor gathering PR #125 is accepted on `main` at merge `067cec562a08a0eef67f65da56c6654071142699` after Claude/Fable exact-head Gate 2.

## 1. Why this unit

The accepted touching-strip interface-factor unit tested the most direct memoryless symbolic repair of the interacting two-strip construction. On the exhaustive declared adjacent-strip reachable family for rings `n in {6,7}`:

- the full six-bit observation `(A,B,E0,E1,E2,E3)` has no autonomous longitudinal factor at any tested radius `R in {0,1,2}` on either the primary or stress horizon;
- none of the sixteen frozen interface masks passes at any tested radius;
- the canonical full-state conflicts replay to hidden physical distinctions outside the retained four-row observation band that later affect the observed interface.

That result is bounded. Its interpretation contract explicitly leaves **history-bearing state** open.

The smallest separately motivated extension is therefore not a new fitted coordinate and not a wider raw band. It is to retain a short local temporal history of the already-frozen symbolic observation:

> **Can one or two previous interface symbols preserve enough of the distinctions that escape the current four-row observation to restore a local interacting factor on the same finite reachable family?**

This tests the dimensional program's central constructive move—promoting erased distinctions into state—without changing the physical law, source family, site coordinates, or interface-coordinate basis.

## 2. Fixed physical system and source family

Keep exactly the physical system and source family frozen by `interface-factor-20260911.md`:

- the same binary 2D selector law `F`;
- the same alternating background `B`;
- the same horizontal alignment;
- the same adjacent-strip encoding `V_0(a,b)` with no background row between channels;
- the same coarse update `H = F^2`;
- horizontal logical rings `n in {6,7}`;
- every ordered binary source pair `(a,b)` on each ring.

Thus the source domain is exactly

`2^12 + 2^14 = 20,480`

adjacent-strip source pairs.

Follow each exact physical orbit from coarse time `t=0` through `t=7`, exactly as in the accepted interface-factor stress run. The vertical simulation remains a shrinking exact causal window cut from the infinite alternating background, with sufficient initial margin that every scored observation is independent of artificial vertical boundaries. Horizontal wrap is the declared ring topology; there is no vertical torus.

No new source sampling, fitted decoder, changed physical encoding, or longer physical horizon is introduced.

## 3. Frozen symbolic coordinates

Reuse the accepted six retained bits per logical block:

- `u0 = X(0, 2i+1)`;
- `u1 = X(1, 2i)`;
- `u2 = X(1, 2i+1)`;
- `u3 = X(2, 2i)`;
- `u4 = X(2, 2i+1)`;
- `u5 = X(3, 2i)`.

Reuse the accepted sitewise bijective re-coordinate:

`A = u1`

`B = u5`

`E0 = u0 xor 1 xor A`

`E1 = u2 xor 1`

`E2 = u3`

`E3 = u4 xor 1 xor B`.

For each mask

`m in {0,...,15}`

over `{E0,E1,E2,E3}`, let `P_m(i,t)` retain `(A,B)` plus exactly the interface coordinates selected by `m`.

No coordinate may be added, removed, transformed, fitted, or reinterpreted after evaluation begins. In particular, `P_15` is the same full six-bit observation used by the accepted interface-factor result.

## 4. Frozen finite-history family

For history depth

`h in {0,1,2}`

define the site symbol

`H_{m,h}(i,t) = (P_m(i,t-h), ..., P_m(i,t))`.

`h=0` is exactly the accepted memoryless observation. `h=1` retains current plus one previous symbol; `h=2` retains current plus two previous symbols.

The history order is oldest to newest and is part of the canonical serialization.

For every tested history symbol, test longitudinal factor radii

`R in {0,1,2}`.

A radius-`R` history factor exists on a declared comparison domain when the next complete history symbol at logical block `i`,

`H_{m,h}(i,t+1)`,

is a single-valued function of the current history symbols

`H_{m,h}(i-R,t), ..., H_{m,h}(i+R,t)`

pooled over both ring sizes, all source pairs, all logical sites, and all scored transitions in that domain.

The lag-shift portion of the update is deterministic by definition:

`(P(t-h), ..., P(t)) -> (P(t-h+1), ..., P(t), P(t+1))`.

Therefore the only nontrivial prediction is the new `P_m(i,t+1)` component. The verifier must nevertheless score equality of the complete next history symbol so an indexing error cannot hide behind that observation.

Unseen local words are don't-cares. A conflict is two reachable records with identical current history neighborhoods and different next-center history symbols.

## 5. Frozen comparison domains

The accepted interface-factor run pooled transitions `t=0..3` for its primary horizon and `t=0..6` for its stress horizon. This unit must distinguish a true information gain from the trivial effect of dropping early transitions while a history warms up.

Define nested same-transition comparison domains:

- `D0 = {0,1,2,3,4,5,6}`;
- `D1 = {1,2,3,4,5,6}`;
- `D2 = {2,3,4,5,6}`.

For each `Dk`, evaluate **every history depth `h <= k`** on exactly the same transitions. Thus:

- on `D0`: score `h=0`;
- on `D1`: score `h=0,1`;
- on `D2`: score `h=0,1,2`.

This creates six frozen history/domain slices. A claim that history resolves a conflict may be made only by comparing depths on the **same `Dk`**.

In addition, replay the accepted memoryless primary domain

`P0 = {0,1,2,3}`

for `h=0` as an exact regression control. No `h>0` result on a shifted window is called a replication of the old primary result.

No adaptive horizon extension is allowed. The complete unit uses only physical states already within `t=0..7`.

## 6. Frozen claims, predictions, and controls

### K1 — exact memoryless regression control

For every interface mask `m` and every `R in {0,1,2}`, the `h=0` verdicts on:

- `P0={0,1,2,3}`, and
- `D0={0,1,2,3,4,5,6}`

must reproduce the accepted interface-factor canonical result byte-for-byte at the verdict/canonical-witness level after normalizing only the new wrapper fields used by this protocol.

The verifier must load the accepted `results/interface_factor_20260911.json`, verify its registered integrity, and compare against it. A mismatch is an implementation failure and blocks interpretation.

### K2 — history-shift control

For every scored record and every `h>0`, the lagged components of the next history symbol must equal the corresponding shifted components of the current history symbol exactly.

Any violation is an implementation failure.

### K3 — refinement monotonicity control

On the same comparison domain `Dk`, same mask, and same radius, deeper history refines shallower history. Therefore:

> if `H_{m,h}` is conflict-free, then every scored `H_{m,h+1}` with `h+1 <= k` must also be conflict-free.

The reason is structural: the deeper input contains the complete shallower input plus extra past information, while all added output lag coordinates are copied deterministically from the current deeper symbol.

A violation of this monotonicity is an implementation or serialization error, not a scientific result.

The converse is not required: deeper history may resolve a conflict.

### K4 — primary constructive bet: one-step history resolves the accepted full-state obstruction

The accepted canonical full-state memoryless conflict uses records at coarse times `t=1` and `t=2`, so it remains inside `D1`.

**Frozen prediction:** on `D1`, the full observation with one lag, `H_{15,1}`, has an autonomous local factor at some `R <= 2`, while the memoryless `H_{15,0}` remains conflicting at all `R <= 2`.

This conjunction is the main constructive bet. If `H_{15,1}` passes but `H_{15,0}` also passes on `D1`, the result is a bounded closure fact but **not evidence that one-step history was needed**. If `H_{15,1}` conflicts at all radii, K4 fails.

No new radius, coordinate, or horizon is introduced after seeing K4.

### K5 — second-lag follow-up is frozen now, not a rescue

On `D2`, score `h=0,1,2` for every mask and radius regardless of the K4 result.

If `H_{15,2}` passes where `H_{15,1}` conflicts on the same `D2`, report that as a **two-lag bounded resolution**. If both pass, the second lag is not called necessary. If both conflict, the frozen depth-two family remains insufficient on `D2`.

This depth-two audit is predeclared before evaluation so it cannot become a post-hoc rescue of K4.

### K6 — complete bounded mask/history/radius census

For all six `(Dk,h)` slices, all 16 interface masks, and all `R in {0,1,2}`, report pass/conflict.

For each `Dk`, report the Pareto-minimal passing budgets under the partial order:

- fewer retained interface coordinates is cheaper;
- smaller history depth is cheaper;
- smaller longitudinal radius is cheaper.

A budget is Pareto-minimal only within this frozen family and domain. No all-time or representation-independent minimality claim is allowed.

For every passing budget, also state whether an immediately shallower scored history passes on the same domain and radius. This distinguishes history-resolved from already-memoryless closure.

### K7 — canonical conflict witnesses

Every failing `(Dk,h,m,R)` retains a deterministic canonical conflict.

Treat each contributing transition record as

`(t, n, source_pair_lex, logical_site)`

where `source_pair_lex` is the lexicographic `(a,b)` bitstring pair. For each conflicting current-history-neighborhood key, take the lexicographically first two records with distinct next-center history symbols after sorting by that tuple. The canonical witness for the budget is then the lexicographically smallest ordered pair `(record_1, record_2)` across all conflicting keys.

The witness records:

- complete selected history neighborhoods for both records;
- next-center selected symbols;
- complete next history symbols;
- which output coordinate first differs under canonical coordinate order.

### K8 — independent physical replay and hidden-cause localization

The complete census may use the established vectorized physical implementation, but every canonical **full-state `m=15`** conflict is independently replayed from its original source pair by a scalar coordinate implementation.

For each replayed conflict, inspect the exact current physical causal patch sufficient to determine the next six-bit center observation under two fine steps. Record all coordinates at which the two current physical patches differ, partitioned into:

1. retained `W` cells inside the symbolic neighborhood;
2. other cells in rows `0..3`;
3. cells outside rows `0..3`.

For a valid `P_15` conflict, category 1 must be empty by construction. If the complete physical causal patches are identical yet the next six-bit symbols differ, the verifier is invalid and evaluation stops.

The accepted interface-factor witness had category-3 exterior differences. This protocol does **not** freeze that classification for every new conflict; it records what the independent replay shows.

### K9 — essential dependency audit for passing full-state factors

If `H_{15,h}` passes at any frozen radius on `D1` or `D2`, build the factor table at its minimum passing radius for that domain and audit essential input-bit dependencies on the reachable local domain.

Type every input bit by:

- longitudinal offset `d in {-R,...,+R}`;
- history lag `ell in {0,...,h}`, where `ell=0` means current and larger `ell` means older;
- coordinate type `A`, `B`, `E0`, `E1`, `E2`, `E3`.

Audit only the newly predicted `P_15(t+1)` coordinates for scientific dependency claims; deterministic history-copy edges are reported separately and are not counted as predictive causal structure.

Report:

- whether any `ell>0` predictive input is essential;
- all essential cross-interface dependencies under the typing inherited from `interface-factor-20260911.md`;
- whether the factor has both an essential historical dependency and an essential cross-interface dependency.

A pass with no essential historical input does not show that memory is doing work. A pass with no essential cross-interface dependency is not an interacting causal witness. Even a pass with both establishes only a bounded two-channel history-bearing closure witness, not an arbitrary-width spatial axis.

### K10 — scalar/vector implementation agreement

Independently replay with the scalar physical path:

- every canonical full-state conflict;
- one deterministic source pair from each ring at every scored coarse time;
- the accepted K1 memoryless canonical conflicts.

The scalar and vectorized implementations must agree cell-for-cell on every physical cell used by observations and causal-patch localization.

## 7. Required ordering and workflow

This protocol is frozen on a protocol-only sub-branch and must enter the dedicated gathering branch before any implementation work.

Required order:

1. protocol-only sub-PR into `gather/dimensional-interface-history`;
2. self-review and merge of that sub-PR after checks are green;
3. exact-head Claude/Fable **Gate 1** review of the frozen protocol on the gathering branch;
4. only after Gate 1 approval: implementation-only sub-PR containing verifier, workflow, integrity registration scaffolding, and tests, with **no canonical result artifact**;
5. self-review and merge implementation sub-PR after checks are green;
6. evaluation sub-PR that performs the first canonical run and commits the pinned result;
7. reporting sub-PR for result note, Program, dimensional-lift checkpoint, knowledge graph, and publication catalogs;
8. exact-head Claude/Fable **Gate 2** review of the complete gathering branch;
9. reviewer merge of gathering PR to `main` only after exact-head checks and Gate 2 are green.

No implementation, dry run over the primary source domain, exploratory evaluation, or result inspection is permitted between steps 1 and 3. Implementation design may be reasoned about from the frozen protocol, but no source-domain execution may occur before Gate 1.

Proposed implementation paths, frozen only as paths and responsibilities:

- verifier: `scripts/verify_interface_history.py`;
- canonical result: `results/interface_history_20260911.json`;
- workflow: `.github/workflows/research-interface-history.yml`.

The implementation PR must register the future canonical result in `scripts/check_result_integrity.py` without creating that result. The evaluation PR must record SHA-256 hashes of the frozen protocol and exact verifier in the canonical JSON and must receive both source-integrity and byte-for-byte replay checks before reporting.

## 8. Resource budget

Physical source domain remains exactly 20,480 adjacent source pairs and coarse times `t=0..7`.

Frozen scientific search space:

- 16 interface masks;
- 3 history depths `h=0,1,2`;
- 3 radii `R=0,1,2`;
- six scored `(Dk,h)` comparison slices plus the `h=0` legacy-primary regression control.

Only combinations with `h<=k` are scored on `Dk`.

The implementation may cache a physical trajectory once per source pair and derive all symbolic histories from it. It may batch source pairs for memory, but batching must not alter canonical record ordering.

No architecture optimizer, learned state, stochastic search, source sampling, adaptive history depth, or adaptive radius is allowed.

## 9. Interpretation contract

A **history-resolved pass** means only:

> On one of the frozen same-transition domains, a declared finite temporal stack of the already-fixed touching-strip interface symbols admits a single-valued local update at a declared radius where an immediately shallower history remains conflicting on that same domain and radius.

This is evidence that retained symbolic past carries predictive distinctions lost by the shallower observation on that bounded reachable family.

It is not by itself evidence of a new spatial axis. Under the accepted causal-geometry handoff, a candidate interacting spatial representation additionally needs local cross-interface causal dependence; K9 audits that separately.

A failure through `h=2, R=2` means only that this frozen finite history/radius family is insufficient on the declared comparison domains. It does not exclude:

- deeper temporal history;
- larger longitudinal radius;
- moving/support-tracking/front state;
- a different finite symbolic interface coordinate system;
- nonlocal or variable-radius factors;
- a growing-region physical representation;
- other physical encodings or alignments.

No pass or failure in this unit decides arbitrary-width tiling or recursive dimensional lifting.

## 10. Not claimed

- No theorem that finite history is the unique or natural repair.
- No theorem that `h<=2` is sufficient or necessary beyond the frozen reachable domains.
- No inference from a shifted comparison domain alone that history helped; same-domain shallower/deeper comparison is mandatory.
- No claim that a local history factor preserves coarse spatial rank without the separate typed causal-dependency requirement.
- No arbitrary-width causal grid.
- No recursive `2D->3D` dimensional lift.
- No self-assembly, endogenous control, Class-IV criterion, universality, novelty, renormalization, prime-factor, or metaphysical claim.
- No all-time conclusion from finite rings and finite horizons.

## 11. Gate-1 review questions

Claude/Fable should review this exact frozen head before implementation, with particular attention to:

1. **Same-domain attribution:** Are `D1` and `D2` comparisons sufficient to prevent a history pass from being misattributed when the actual cause is merely dropping warm-up transitions?
2. **Refinement monotonicity:** Is K3 sound for complete history-symbol updates, including the deterministic shift coordinates?
3. **K4 bet:** Does the accepted memoryless canonical conflict indeed remain in `D1`, making the one-lag test a legitimate direct follow-up rather than a changed-domain escape?
4. **Physical replay:** Is K8's exact current causal-patch comparison the right invariant check for hidden-cause localization under the two-fine-step coarse update?
5. **Dependency semantics:** Does K9 correctly separate predictive history dependence, cross-interface dependence, and deterministic lag-copy edges?
6. **Scope:** Are any claims stronger than the finite `n=6,7`, `t<=7`, `h<=2`, `R<=2` evidence can support?

Binding clarifications must be committed before any implementation/evaluation. Any change to source domain, history family, comparison domains, radii, claims, witness ordering, or interpretation contract after Gate 1 requires renewed protocol review.