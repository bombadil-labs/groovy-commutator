# Cross-width interface history: width eight persists; width nine loses complete-field determinism

**Evidence:** exact within the frozen finite domain.  
**Authored by:** Codex / OpenAI GPT-5.6 Sol. **Independent review:** Gate 1 approved by Claude Code / Fable 5.1 on exact protocol-only head `7cc4bbae2eb5af50e133b8a8eaf44fb55db358a8`; Gate 2 was approved by Claude Code / Fable 5.1 on exact final head `0b569f3a7206f394640a919ea40c8e77b67c41dd`; the reviewer merged PR #164 into `main` as `8b8c62d0e3219c156b086b56c3a1158fba4b4792` under the reviewer-merges rule.  
**Protocol:** `docs/research/protocols/interface-history-cross-width-20260912.md`, with the Gate-1 near-whole-ring clarification integrated before implementation in #165.  
**Canonical result:** `results/interface_history_cross_width_20260912.json`.

## Question

Accepted #157 found that complete retained two-lag history is globally deterministic for nine finite-ring cells on rings 6 and 7 even though every tested local factor through `R<=2` conflicts. Does that global sufficiency survive on fresh larger rings, and can one common radius-three local table explain the declared widths without seeing ring identity?

The frozen continuation keeps the touching-strip physical law, source family, six-bit coordinate, cadence, `D2,h=2` semantics and mask numbering unchanged. It tests only masks `{11,13,15}`, because those are exactly the masks globally deterministic on **both** predecessor widths. Widths 6/7 are controls; widths 8/9 are fresh exhaustive evidence. The only new radius is `R=3`.

## Answer

The finite continuation breaks at width 9.

All three masks pass complete-field determinism (W1) and width-specific radius-three determinism (W2) on width 8. On width 9, all three masks fail **complete-field determinism itself**, and therefore no increase of spatial radius can repair those exact retained representations on that frozen finite ring/domain.

The pooled width-blind radius-three test (W3) also fails for all three masks. Thus every predeclared constructive bet is false.

This is not an arbitrary-width or infinite-lattice no-go. It is an exact finite statement: the two-lag retained information that suffices globally through width 8 no longer suffices globally at width 9 for the three common masks.

## Frozen domain

- same accepted touching-strip physical law and exhaustive ordered source-pair family;
- same six-bit site coordinate `(A,B,E0,E1,E2,E3)`;
- mandatory `A,B` and primary masks `{11,13,15}`;
- history depth `h=2`, domain `D2`, coarse transitions `t=2..6`;
- widths `n in {6,7,8,9}`;
- widths 6/7 as imported predecessor controls;
- fresh exhaustive widths 8 and 9 (`4^8` and `4^9` ordered source pairs);
- only new spatial radius `R=3`;
- W3 scientific key contains no width tag.

`R=3` sees the whole ring on widths 6 and 7, omits one site on width 8, and omits two on width 9. The Gate-1 clarification therefore binds every fresh-width W2 pass as **near-whole-ring** finite evidence, not small-radius locality.

## Exact outcome

### Controls

All imported predecessor verdicts replay. Widths 6 and 7 pass W1 and the theorem/regression W2@R3 control for masks 11, 13 and 15. The packed primary and independently written explicit/reference path agree on every retained field used for scoring, all 27 W1/W2/W3 verdicts and all canonical conflicts. Translation covariance passes.

Every stored conflict replays through the independent physical/observer path. There are nine stored scientific conflicts in the final result.

### Fresh width 8

For masks 11, 13 and 15:

- W1 complete-field determinism: **pass**;
- W2 radius-three local determinism: **pass**.

So the global two-lag sufficiency seen on widths 6/7 survives one fresh exhaustive width, and a seven-site history window is enough there. Because this window omits only one site, the W2 result is near-global.

### Fresh width 9

For masks 11, 13 and 15:

- W1 complete-field determinism: **conflict**;
- W2 radius-three local determinism: **conflict**.

The W1 failures are the stronger result. Two records can have literally equal complete retained three-time ring histories and different next complete retained fields. Therefore **no larger spatial radius alone can repair that exact retained representation on width 9 and the frozen D2 domain**.

For all three masks, the canonical W1 conflict occurs at `t=6` between source-pair records with equal complete retained history but a first differing next-field coordinate at site 8, coordinate `B`.

### Pooled W3

All three masks fail the one-table pooled radius-three test across widths 6–9.

- mask 11: canonical conflict uses `n=6` and `n=7`;
- mask 13: canonical conflict uses `n=6` and `n=7`;
- mask 15 / full P15: canonical conflict uses `n=7` and `n=9`.

The P15 witness is especially useful because it directly shows a shared seven-site two-lag feature requiring different next-center outputs across two declared widths while the scientific key cannot inspect width.

A pooled failure does not by itself imply information loss, because two width-specific factors could disagree. Here width 9 independently fails W1, so the P15 pooled failure coexists with an actual complete-field information-loss certificate on that fresh width.

## Frozen predictions

All three primary bets fail:

- **P2** — masks 11/13/15 retain W1 on both fresh widths 8 and 9: **false** because width 9 conflicts.
- **P3** — P15 passes W2@R3 on both fresh widths: **false** because width 9 conflicts.
- **P4** — one pooled width-blind P15 R3 table works across widths 6–9: **false**.

The negative outcomes were scored exactly as frozen; no larger radius, deeper history, new coordinate or support-tracking rescue was introduced after seeing them.

## Process and failed evaluation preserved

The protocol-only unit #163 integrated before implementation and received independent Gate 1. Clarification-only #165 recorded the reviewer's near-whole-ring null before any verifier existed.

Implementation-only/no-result #166 then pinned the verifier and permanent workflow and passed all 27 applicable checks before source-domain evaluation.

The first evaluation attempt, #167, executed the unchanged scientific verifier and produced provisional branch evidence, but the permanent workflow failed before integrity/replay because the implementation-stage `--self-test` still required the canonical result file to be absent. The run was preserved and closed unmerged.

Implementation-only #169 changed only that workflow plumbing: the no-result self-test runs only while the result is absent, allowing permanent integrity and byte-for-byte replay once a canonical result exists. No protocol, scientific verifier semantics, source domain or result logic changed.

Corrected evaluation #170 then regenerated the result independently from the corrected pinned stage. Its cleaned final diff contains only `results/interface_history_cross_width_20260912.json`, and all exact-head checks are green including permanent byte-for-byte replay.

## What this changes

The accepted #157 result showed that local failure through radius two did not imply information loss: on widths 6 and 7, some two-lag retained fields were globally sufficient. The cross-width continuation now shows that this sufficiency is itself finite-width dependent.

The important distinction is therefore not merely “local versus global.” The same retained coordinate/history budget can move through three regimes across declared finite widths:

1. globally sufficient and whole-ring local by construction (widths 6/7 at R3);
2. globally sufficient and near-whole-ring local (width 8);
3. globally insufficient (width 9).

That is evidence against treating a few finite-ring successes as a stable width-independent closure law. It is **not** evidence that width 9 is a universal threshold or that all larger widths fail.

## Boundaries

This result is bounded to the declared touching-strip reachable family, widths 6–9, `D2,h=2`, masks `{11,13,15}`, coarse transitions through `t=6`, and the single new radius `R=3`.

Do not infer:

- monotone failure for widths `n>9`;
- arbitrary-width, full-shift or infinite-lattice non-closure;
- failure of deeper history, moving/support-tracking state, alternative coordinates, nonlocal/growing-support descriptions or added physical variables;
- intrinsic or representation-independent dimension;
- a new spatial axis, recursive dimensional lift, self-assembly or endogenous control;
- Class IV, universality, renormalization, spacetime/physics/metaphysics, or prime/`8n+1` claims.

## Reproduction

From the repository root after the result is present:

```bash
python scripts/check_result_integrity.py results/interface_history_cross_width_20260912.json
python scripts/verify_interface_history_cross_width.py
```

The dedicated permanent workflow performs fast integrity checks on applicable pull requests and byte-for-byte result replay on result changes, `main`, manual dispatch and the repository's scheduled replay cadence.
