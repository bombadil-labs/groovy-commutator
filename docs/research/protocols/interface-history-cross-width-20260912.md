# Protocol: cross-width locality of complete interface history — 2026-09-12

**Status:** frozen before implementation/evaluation. Nothing in this protocol has been run.  
**Program:** *Dimensional Closure and the Commutator Lift*.  
**Authored by:** Codex / OpenAI GPT-5.6 Sol.  
**Protocol review:** pending independent Gate 1 on the exact integrated gathering head. **No verifier or source-domain execution is authorized before Gate 1.**  
**Base:** `main` at `240b885f3c545a405488c3b7aa665d0a59093c5c`.  
**Predecessor:** accepted gathering PR #157, *full-field determinism of frozen interface history*.

## 1. Why this unit

The accepted predecessor separates two failure modes inside the same frozen touching-strip representation.

- For 183 of 192 finite-ring cells, even the **complete retained history field** does not determine the next retained field. Those are finite-ring representation-level information-loss certificates.
- For exactly nine cells, all at `D2,h=2`, the complete retained field **does** determine the next field even though every tested local factor at `R<=2` conflicts. On ring 6 the passing masks are `{11,13,15}`; on ring 7 they are `{3,5,7,11,13,15}`. In particular full `P15,h=2,D2` passes globally on both rings.

For a single finite ring, increasing radius until the entire ring is visible can always collapse the distinction between "global" and "local" whenever the global map is single-valued. That by itself would add little evidence. The next useful question is therefore **cross-width**:

> **Do the complete-history passes survive on fresh larger rings, and can one common bounded local rule explain them across several widths without using ring-specific lookup tables?**

This unit keeps the accepted physical law, touching-strip source family, coordinate map, masks, cadence, two-lag history and `D2` semantics fixed. It adds two fresh exhaustive widths and tests one predeclared radius, `R=3`, both per-width and after pooling widths under one common local table.

The unit is intentionally narrow. It does not search post hoc for a successful larger radius and does not introduce moving/support-tracking state or a new coordinate.

## 2. Frozen objects inherited unchanged

Import by exact source/result hash from the accepted #131/#157 machinery:

- the ambient fixed 2D physical law and alternating background;
- the adjacent two-strip logical source family and encoding;
- coarse cadence two;
- the six retained site coordinates `(A,B,E0,E1,E2,E3)` and mask numbering `0..15` for the four `E` bits, with `A,B` always retained;
- history depth `h=2`, represented oldest to newest;
- the predecessor's `D2` reachable-domain semantics and coarse transition horizon through the declared `t<=6` scoring window;
- canonical coordinate order: lags oldest to newest, then `A,B,E0,E1,E2,E3`, skipping masked-out interface coordinates;
- deterministic source-pair and witness ordering.

No scientific choice above may be reconstructed from memory if the accepted implementation/result supplies it directly.

### Primary masks

The primary frozen mask set is

`M_common = {11,13,15}`.

These are exactly the masks that passed complete-field determinism at `D2,h=2` on **both** accepted predecessor rings 6 and 7. No ring-7-only passing mask is promoted into the primary cross-width claim.

The ring-7-only masks `{3,5,7}` remain predecessor facts and are not evaluated as a rescue family in this unit.

## 3. Widths and complete exhaustive domains

Evaluate widths

`n in {6,7,8,9}`.

Rings 6 and 7 are predecessor regression controls. Rings 8 and 9 are the **new source-domain evidence**.

For each fresh width, exhaust the same adjacent-strip logical source-pair family used by the predecessors:

- `n=8`: all `4^8 = 65,536` ordered source pairs;
- `n=9`: all `4^9 = 262,144` ordered source pairs.

Generate physical trajectories and retained histories only through the frozen `D2,h=2` horizon. Do not sample and do not fit a subset after inspection.

## 4. Three determinism notions

Keep these separate.

### W1 — complete-field determinism on one width

For fixed `(n,mask)`, group exhaustive `D2,h=2` records by the **complete retained three-time ring history field**. The cell passes W1 iff every key has exactly one next complete retained field.

This is exactly the predecessor's global criterion, now repeated on fresh widths.

A W1 failure is a finite-ring information-loss certificate for that representation/domain. A W1 pass says only that some finite-ring global function exists.

### W2 — radius-three local determinism on one width

For fixed `(n,mask)`, form at every logical site the ordered local feature consisting of the retained three-time history symbols at offsets

`-3,-2,-1,0,1,2,3`

with periodic indexing. The target is the next retained symbol at the center site; lag shifting in the complete next history is deterministic and need not be treated as an independent target.

The cell passes W2 iff every identical radius-three feature has one next center symbol over the complete declared reachable domain.

For ring 6, offsets `-3` and `+3` refer to the same antipodal site but remain distinct ordered feature positions whose values must agree. For ring 7, the seven offsets cover the complete ring once. Do not deduplicate the ordered feature coordinates.

A W2 pass is a finite-ring, width-specific translation-equivariant radius-three factor on the reachable domain. It is not an infinite-lattice theorem.

### W3 — one pooled radius-three table across widths

For each mask, pool every W2 `(feature,target)` record from widths `6,7,8,9` **without a width tag**. The mask passes W3 iff identical radius-three history features always have the same next-center symbol across the pooled union.

A W3 pass establishes one common radius-three local table on the union of the four declared finite reachable families. A W3 failure means at least two pooled records share the same local history feature but require different next symbols; retain the canonical cross-width or same-width conflict.

Crucially, do not let the candidate rule inspect `n`, ring identity, source provenance or global state outside the seven-site window.

## 5. Predecessor deductions and controls

### C1 — accepted local failure below radius three

For all three primary masks on rings 6 and 7, the accepted #131 result already gives local conflicts through `R<=2` at `h=2,D2`. Replay those verdicts by exact imported result hash; do not recompute them as new evidence.

Therefore, if pooled W3 passes at `R=3`, radius three is automatically the minimum common radius **within the tested range `R=0..3`** for the pooled 6/7 family. Do not call it a minimum on arbitrary widths.

### C2 — whole-ring implication on the predecessor widths

For `n=6,7`, a radius-three ordered window contains every ring site (with the ring-6 antipode duplicated). The predecessor says masks `11,13,15` are globally deterministic at `D2,h=2`. Translation closure of the declared source family and shift-equivariance of the physical/observation construction imply a width-specific W2 factor exists at `R=3` for those predecessor cells.

Treat this as a theorem/regression control, not a discovery. The implementation must still verify it exactly and retain any contradiction as a blocking implementation/provenance failure.

### C3 — rotation/translation covariance

For every passing W1 cell, shifting a source pair and its complete retained history must shift the next retained field. For every passing W2/W3 table, site translation must preserve the feature-target relation. Check this directly on exhaustive records as an implementation control.

## 6. Frozen predictions

### P1 — predecessor regression controls

On rings 6 and 7, masks `11,13,15` pass W1 and W2 at `R=3`; their imported `R<=2` predecessor verdicts remain conflicts.

Failure blocks interpretation.

### P2 — fresh-width global persistence (primary bet)

All three primary masks `{11,13,15}` pass W1 on **both** fresh widths 8 and 9.

A failure is scientifically meaningful: it shows that the complete-history determinism seen on rings 6 and 7 does not persist even to the next declared exhaustive widths for that mask.

### P3 — full-state radius-three persistence (primary locality bet)

Full `P15,h=2,D2` passes W2 at `R=3` on widths 8 and 9.

This is stronger than P2. If W1 passes while W2 fails, the retained information is globally sufficient on that ring but radius three is too small.

### P4 — one common P15 radius-three table across widths (primary cross-width bet)

Full `P15,h=2,D2` passes W3 across the pooled widths `6,7,8,9`.

If P3 holds separately on every width but P4 fails, report the result as **width-dependent local factor tables within the tested family**, not as information loss.

### P5 — secondary common-mask census

Report W1, W2 and W3 for masks `11` and `13` with no directional bet beyond P2. Their results are exact descriptive comparisons frozen before evaluation.

### P6 — covariance and independent implementation controls

All translation/rotation controls and both independent implementations agree on every W1/W2/W3 verdict and canonical conflict.

A P6 failure is an implementation/provenance blocker rather than a scientific outcome.

## 7. Canonical conflicts

Use deterministic ordering.

### W1 conflict

Order exhaustive records by `(t, source_pair_lex)` within a fixed width. For a conflicting complete-history key, retain the lexicographically smallest ordered pair `(record_1,record_2)` and the first differing next-field site/coordinate under site index then frozen coordinate order.

### W2 conflict

Order local records by `(t, source_pair_lex, site_index)`. Retain the lexicographically smallest ordered pair with equal radius-three feature and differing next-center target, plus the first differing target coordinate.

### W3 conflict

Order pooled records by

`(n, t, source_pair_lex, site_index)`.

Retain the lexicographically smallest ordered pair with equal feature and differing target. Record both widths explicitly. A valid W3 conflict may be same-width or cross-width; do not preferentially select a cross-width witness if an earlier same-width witness exists.

Every stored conflict must replay through an implementation path independent of the grouping/key construction.

## 8. Independent implementation requirements

No implementation before exact-head Gate 1.

After approval, the implementation-only/no-result sub-PR must pin:

1. a packed/vectorized primary trajectory and retained-history evaluator;
2. an explicit tuple/scalar reference evaluator independent of the packed history-key representation;
3. exact W1 complete-field grouping;
4. exact W2 radius-three feature grouping;
5. exact W3 pooled grouping with **no width tag** in the scientific key;
6. predecessor result/source hashes for #131 and #157;
7. complete canonical conflict replay in the independent path;
8. permanent two-tier CI and integrity registration supporting a green no-result implementation stage.

The two implementations must agree on every fresh-width retained field used in scoring, every W1/W2/W3 verdict and every canonical witness. Any mismatch blocks evaluation.

Proposed artifacts:

- verifier: `scripts/verify_interface_history_cross_width.py`;
- result: `results/interface_history_cross_width_20260912.json`;
- workflow: `.github/workflows/research-interface-history-cross-width.yml`.

The result must hash the verifier, frozen protocol and imported predecessor artifacts used as controls.

## 9. Outcome interpretation

The protocol predeclares the useful fork:

| Fresh-width outcome | Allowed interpretation |
| --- | --- |
| W1 fails | this retained history loses predictive information on that finite width/domain |
| W1 passes, W2 fails | complete-ring information is sufficient there, but radius 3 is insufficient |
| W2 passes separately, W3 fails | each finite width has a radius-3 factor, but no single table fits the pooled declared widths |
| W3 passes | one radius-3 table fits the union of widths 6–9 on the declared reachable family |

None of the four outcomes establishes or refutes a factor on arbitrary widths or on the infinite lattice.

## 10. Nulls and non-claims

Mandatory boundaries:

- **Finite-width null:** a table that works on four finite widths may still fail at width 10 or on the full shift.
- **Whole-ring null:** on widths 6 and 7, `R=3` already sees the complete ring; those individual passes are controls, not locality discoveries.
- **Near-whole-ring null:** at `R=3`, the ordered seven-site window omits only one site on width 8 and two sites on width 9. A fresh-width W2 pass is therefore a near-global finite-ring statement, not evidence of small-radius locality. Likewise, a pooled W3 pass concerns the non-aliased part of the declared four-width families; periodic aliases are consistent by periodic lifting and cannot by themselves create a pooled conflict.
- **Reachable-family boundary:** all claims concern the frozen adjacent-strip reachable family, not arbitrary six-bit history fields.
- **History boundary:** only two lags are retained; deeper history is not tested.
- **Radius boundary:** the only new radius is `R=3`; a failure does not exclude `R>3`.
- **Representation boundary:** moving/support-tracking state, alternative coordinates and nonlocal/growing-support descriptions remain separate future protocols.
- **Geometry boundary:** even a pooled W3 pass is a finite-family local-factor result, not intrinsic dimension, a new spatial axis, or a representation-independent theorem.
- No self-assembly, endogenous control, spacetime emergence, physics/metaphysics, Class-IV, universality, renormalization or prime/`8n+1` claim.

## 11. Required workflow

Use the repository gathering/sub-PR protocol:

1. protocol-only sub-PR into `gather/interface-history-cross-width`;
2. author self-review and merge only when exact-head checks are green;
3. independent **Gate 1** on the exact integrated gathering head;
4. only after Gate 1: implementation-only/no-result sub-PR;
5. green implementation self-review and merge;
6. evaluation-only sub-PR performs the first canonical fresh-width run;
7. reporting/current-account sub-PRs preserve the failed bets and exact scope;
8. independent exact-head **Gate 2**;
9. reviewer merge to `main` only after Gate 2 and all relevant checks are green.

Any material change after Gate 1 to widths, masks, history depth/domain, `R=3`, pooled-key semantics, predictions, witness ordering or interpretation ceiling requires renewed Gate 1.

## 12. Gate-1 review questions

The independent reviewer should attack especially:

1. Is widths 8 and 9 an appropriate fresh exhaustive extension of the accepted 6/7 family, or does periodic aliasing make this comparison scientifically uninformative?
2. Is W3's pooled table without a width tag the correct finite test of a common local factor across declared widths?
3. Is `R=3` principled as the first untested radius and the first radius that sees the whole predecessor rings, without becoming a post-result radius search?
4. Does the C2 deduction really guarantee the ring-6/7 W2 controls from predecessor W1 plus translation closure/equivariance?
5. Is P2 too strong or already decided by a structural theorem? If not, are failures on fresh widths interpretable as claimed?
6. Is P4 a genuinely new cross-width claim rather than a tautology once each width passes separately?
7. Should masks 11/13 remain secondary while P15 carries the primary cross-width bet, or does that hide an important multiple-comparison issue?
8. Are the W1/W2/W3 conflict orderings sufficient to prevent witness shopping?
9. Are the independent-evaluator and predecessor-hash controls strong enough to distinguish implementation mistakes from genuine failures?
10. Are the non-claims strong enough that a four-width local table cannot be misreported as arbitrary-width/infinite-lattice closure or intrinsic dimension?

Gate 1 should be adversarial. Binding corrections must land before the verifier or any fresh-width source-domain execution, and renewed approval must name the exact integrated gathering-head SHA.
