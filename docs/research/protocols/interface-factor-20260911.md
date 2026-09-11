# Protocol: touching-strip interaction residual as local interface state — 2026-09-11

**Status:** frozen before implementation and evaluation. Nothing has been run under this protocol.  
**Program:** *Dimensional Closure and the Commutator Lift*, first constructive unit after the bounded-distortion causal-geometry theorem.  
**Authored by:** Codex / OpenAI GPT-5.6 Sol.  
**Protocol review:** none at freeze; **run authorized by Myk 2026-09-11** while Claude/Fable is unavailable. Claude/Fable retrospective review remains required.  
**Tracking:** issue #123. **Base dependency:** causal-geometry PR #122 is accepted on `main` under the same explicitly recorded temporary retrospective-review exception.

## 1. Why this unit

The dimensional program has now separated several things that can imitate an added axis:

- finite product coordinates can be packed into a one-dimensional alphabet;
- unbounded independent state width defeats a fixed total-capacity budget;
- separated Rule90 channels have unbounded constant-support intervention addressability even when total target storage is released;
- arbitrarily wide **connected** grid strips cannot all preserve one fixed bounded-distortion geometry when represented on a line.

What is still missing is constructive rather than definitional. Research018 gives the near-miss:

- separated strips are dynamically closed and independently addressable but do not causally interact;
- touching strips causally interact but the original two-bit-per-channel code leaves its representation on 47 of 64 local inputs after one coarse update.

Research019 tried the obvious raw-band enlargement: retain all six variable physical bits in the original four rows. That representation contains every first coarse output but does not remain a fixed-height physical band; one reachable witness grows an outward wake with unbounded transverse span. Therefore this unit does **not** retry “keep more fixed rows.”

Instead it asks the open question Research019 explicitly left behind:

> **Can the information in the touching-strip interface be a finite local symbolic state even while the full physical disturbance expands outside the observed band?**

A positive answer would be the first closed interacting two-channel logical representation in this lineage. A negative answer within the frozen budget would give an exact witness to which omitted physical distinctions re-enter the interface dynamics.

## 2. Fixed physical system and source family

Keep the exact binary 2D selector law `F`, alternating background `B`, horizontal alignment, and coarse cadence two from Research018/019. Let

`H = F^2`

be one coarse update.

Use the adjacent-strip encoding `V_0(a,b)` with no background row between the two Rule90 strips. Horizontal direction is periodic on logical rings

`n in {6,7}`.

For each ring, enumerate **every** ordered pair of binary logical rows `(a,b)`, so the source counts are `2^(2n)`:

- `n=6`: 4,096 source pairs;
- `n=7`: 16,384 source pairs.

For each source pair, follow the exact physical orbit from coarse time `t=0` through `t=7`. The scored transitions are `t -> t+1` for

`t in {0,1,2,3,4,5,6}`.

The vertical simulation window is a shrinking exact causal window cut from the infinite alternating background, with enough initial margin that rows needed by every scored observation remain unaffected by artificial boundaries. Horizontal wrap is the declared ring topology; there is no vertical torus.

No source sampling, fitted state, or architecture selection occurs.

## 3. The six-bit observation and vertex/interface coordinates

Research019's `W` observation keeps six variable cells per two-column logical block. For logical block `i`, write

- `u0 = X(0, 2i+1)`;
- `u1 = X(1, 2i)`;
- `u2 = X(1, 2i+1)`;
- `u3 = X(2, 2i)`;
- `u4 = X(2, 2i+1)`;
- `u5 = X(3, 2i)`.

The original adjacent code has

`(u0,u1,u2,u3,u4,u5) = (1 xor a, a, 1, 0, 1 xor b, b)`.

Re-coordinate these same six bits as two **vertex bits** and four **interface-correction bits**:

`A = u1`

`B = u5`

`E0 = u0 xor 1 xor A`

`E1 = u2 xor 1`

`E2 = u3`

`E3 = u4 xor 1 xor B`.

This is a sitewise bijective coordinate change of the six retained bits. On every original `V_0(a,b)` state,

`E0=E1=E2=E3=0`.

The `E` coordinates measure departure from the canonical adjacent two-strip code relative to the currently observed vertex bits. They are called **interface correction** only in this declared coordinate sense. The protocol does not assume that every component equals the earlier composition-residual polynomial at every later time.

Crucially, the observation remains defined even after physical cells outside rows 0..3 differ from background. This unit asks for predictive sufficiency of the symbolic field; it does not require exact reconstruction of the whole physical field.

## 4. Frozen observation family

Vertices `A,B` are always retained. For each mask

`m in {0,...,15}`

over the four interface bits `{E0,E1,E2,E3}`, define `P_m` to retain `(A,B)` plus exactly the interface coordinates selected by `m`.

Thus:

- `m=0` is the vertex-only observation;
- `m=15` is the full six-bit vertex+interface observation;
- all fourteen intermediate masks are frozen in advance, so a smaller successful interface state can be reported without a post-result coordinate rescue.

For every mask test longitudinal factor radii

`R in {0,1,2}`.

A radius-`R` factor exists on the declared reachable domain when the next selected symbol at block `i` is a single-valued function of the current selected symbols at blocks `i-R,...,i+R`, pooled over:

- both ring sizes;
- every source pair;
- every logical site;
- every scored coarse transition in the relevant horizon.

Unseen local words are don't-cares. A conflict is two reachable records with identical selected current neighborhoods and different selected next-center symbols.

## 5. Primary and stress horizons

The **primary frozen prediction domain** pools transitions

`t in {0,1,2,3}`.

The **stress domain** pools all transitions

`t in {0,1,2,3,4,5,6}`.

The primary horizon is scored separately so later physical wake growth cannot erase whether the interface coordinates first succeed as a finite symbolic state. The stress horizon is predeclared now; it is not an adaptive extension after inspecting primary results.

## 6. Frozen claims, predictions, and controls

### J1 — coordinate sanity control

At `t=0`, every source state has all four interface bits zero. Converting between the raw six retained bits and `(A,B,E0,E1,E2,E3)` must be exactly invertible on every recorded symbol at every horizon.

This is an implementation control, not a discovery.

### J2 — first-step physical control

At the first coarse update (`t=0 -> 1`), the complete physical output of every adjacent-strip source remains inside Research019's four-row `W` band; no exterior-row difference is present yet. The implementation independently checks this against the fixed background.

At the next coarse time (`t=2`), exterior changes must exist for at least one reachable source, reproducing the established fact that symbolic observation and exact fixed-height physical representation are different questions.

No exact ring-level count is frozen from Research019; only existence/nonexistence of exterior change at these two times is a control.

### J3 — primary constructive bet: full interface state locally closes

**Frozen prediction:** on the primary horizon `t=0..3`, the full observation `P_15` has an autonomous local factor at some radius `R <= 2` on the pooled `n=6,7` reachable domain.

This is the main falsifiable constructive bet. It is deliberately stronger than the already-known one-step containment and may fail once omitted wake information becomes causally relevant.

If all `R<=2` conflict, J3 fails. No larger radius, new coordinate, front variable, fitted decoder, or changed horizon is introduced in this unit.

### J4 — stress survival is reported, not predicted

Whether `P_15` remains locally closed through the full stress horizon `t=0..6` is reported. A primary pass followed by a stress failure is a meaningful finite-lifetime symbolic closure result, not a protocol failure.

### J5 — frozen interface-coordinate census

For every one of the 16 interface masks and every `R=0,1,2`, report primary-horizon and stress-horizon pass/conflict.

If one or more budgets pass, report:

- minimum retained interface-bit count;
- all inclusion-minimal passing masks at each horizon;
- minimum passing radius for each passing mask.

These are bounded census facts. They are not promoted to an all-time minimal-state theorem.

### J6 — canonical conflict witnesses

Every failing mask/radius retains a deterministic canonical conflict. Treat each contributing record as the tuple

`(t, n, source_pair_lex, logical_site)`

where `source_pair_lex` is the lexicographic `(a,b)` bitstring pair. For each conflicting local-neighborhood key, take the lexicographically first two records with distinct next-center symbols after sorting by that tuple. The canonical witness for the mask/radius is then the lexicographically smallest ordered pair

`(record_1, record_2)`

across all conflicting keys.

Thus witnesses may come from different coarse times or ring sizes; the total order remains deterministic across the pooled domain.

For the full observation `P_15`, any primary or stress conflict is independently replayed from its two original source pairs. The result records whether the two conflicting physical current states differ outside rows `0..3` inside the next-step physical causal neighborhood of the observed center.

This distinction is central: if omitted exterior wake state separates the two cases, the failure identifies a concrete hidden cause rather than merely saying that a table collided.

### J7 — typed essential-dependency graph for passing full state

If `P_15` passes at any frozen radius on either horizon, build the factor table on its **minimum passing radius** and audit essential coordinate dependencies on the reachable local domain.

Input variables are typed by:

- longitudinal offset `d in {-R,...,+R}`;
- coordinate type `A`, `B`, `E0`, `E1`, `E2`, `E3`.

An input bit is essential for an output coordinate when two observed local neighborhoods differ only in that input bit and produce different output bits.

Report all essential edges. A **transverse/interface causal edge** is any essential dependence crossing the vertex/interface typing, or an `A` output depending on `B`-side/interface information, or a `B` output depending on `A`-side/interface information.

A passing factor with no such edge is closure but not an interacting causal witness. A passing factor with at least one such edge is a **bounded two-channel interacting closure witness**.

Even that does not establish an arbitrarily wide grid: tiling many channels requires a separate frozen protocol.

### J8 — independent physical replay controls

The verifier uses one vectorized physical implementation for the complete census. Independently, a scalar coordinate implementation replays:

- every canonical `P_15` conflict witness;
- one deterministic passing source from each ring at every scored horizon;
- the J2 exterior-change controls.

The independent path must agree cell-for-cell on every physical cell needed by the observations and witness causal patches.

## 7. Artifacts and implementation order

After this protocol commit is integrated into the gathering branch, implementation may proceed under Myk's explicit authorization despite absent cross-model Gate 1.

**Ordering requirement:**

1. frozen protocol commit and integration;
2. verifier/workflow commit with no canonical result present;
3. first primary execution;
4. canonical result commit;
5. result note / Program / checkpoint / knowledge integration;
6. merge under the temporary exception, with Claude/Fable retrospective review debt recorded.

Proposed verifier:

`scripts/verify_interface_factor.py`

Canonical result:

`results/interface_factor_20260911.json`

Permanent workflow:

`.github/workflows/research-interface-factor.yml`

The canonical JSON must record SHA-256 hashes of the protocol and verifier. The result must be registered in `scripts/check_result_integrity.py` and receive both the repository's fast source-integrity tier and byte-for-byte replay tier.

No saved Research018/019 result table is imported as primary truth. Established counts/formulas may be used only as explicitly labeled controls and are independently recomputed where scored.

## 8. Resource budget

Primary source domain is exactly:

`2^(12) + 2^(14) = 20,480`

adjacent source pairs across rings 6 and 7.

Each pair is followed for seven coarse transitions. The implementation may batch source pairs for memory, but batching must not change ordering or scoring.

Frozen search space:

- 16 interface masks;
- 3 longitudinal radii;
- 2 horizons (primary and stress).

No architecture optimizer, learned representation, stochastic search, or source sampling is allowed.

## 9. Interpretation contract

A primary pass of `P_15` means only:

> On the exhaustive declared adjacent-strip reachable domain through coarse transition 3, the six-bit vertex+interface observation has a single bounded local update even though the physical trajectory need not remain inside the observed four-row band.

A stress pass extends that bounded statement through transition 6.

A typed essential cross-interface dependency would additionally show that the closed two-channel factor is not merely two independent vertex processes plus inert bookkeeping.

A failure of `P_15` within `R<=2` means only that these six local coordinates are not predictively sufficient at the frozen radius/horizon. It does not exclude:

- larger longitudinal radius;
- moving-front coordinates;
- a different finite symbolic interface state;
- a growing-region description;
- other physical encodings or alignments.

The scientific value of a failure is the retained hidden-cause witness: it tells us whether information that escaped the raw band later re-enters the interface dynamics.

## 10. Not claimed

- No arbitrary-width causal grid from a two-channel success.
- No recursive 2D->3D dimensional lift.
- No claim that the selected six-bit observation is natural, minimal, or unique outside the frozen census.
- No claim that fixed-height physical containment can be repaired; Research019 already disproves that for its witness.
- No self-assembly, endogenous control, Class-IV criterion, universality, novelty, renormalization, prime-factor, or metaphysical claim.
- No all-time conclusion from a finite stress horizon.

## 11. Review exception record

Claude/Fable is unavailable at freeze. Myk explicitly authorized the dimensional-lift program on 2026-09-11 to proceed in **post-merge retrospective-review mode** if Codex judged the next proposed work worth doing. Codex judged this constructive interface-factor test worth doing because it directly targets the missing conjunction identified by the accepted program: closure plus transverse causal interaction, and because it tests a symbolic possibility explicitly left open by Research019 rather than retrying its refuted fixed-height-band representation.

Recorded authorization:

`Protocol review: none at freeze; run authorized by Myk 2026-09-11.`

This is not a substitute for cross-model review. Claude/Fable retrospective review remains owed after merge; any substantive finding follows the repository correction path.