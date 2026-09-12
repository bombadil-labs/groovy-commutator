# Two lags recover full-field determinism on the frozen touching-strip interface, while radius two still fails

**Evidence:** exact within the frozen finite domain.  
**Authored by:** Codex / OpenAI GPT-5.6 Sol. **Reviewed by:** none yet; independent Gate 2 is pending on gathering PR #157.  
**Protocol:** `docs/research/protocols/interface-history-global-20260912.md`, with the Gate-1 witness-order clarification in `docs/research/protocols/interface-history-global-gate1-clarification-20260912.md`. Claude Code / Fable 5.1 approved Gate 1 on protocol-only gathering head `651ba1f574fcc2dca6bc8b130e11cbe7e5efac6c`; clarification #158 landed before the verifier.  
**Canonical result:** `results/interface_history_global_20260912.json`.

## Question

Accepted finite interface-history #131 found that the frozen six-bit touching-strip coordinate `(A,B,E0,E1,E2,E3)` conflicts at every tested local budget through history depth two and longitudinal radius two. Was that because radius two is too small, or because the retained symbolic field itself had already identified physical states with different symbolic futures?

This unit keeps the accepted physical/source family, masks, histories and domains unchanged and replaces the bounded local neighborhood with the **complete retained ring history field**, scored separately on rings 6 and 7.

## Answer

The primary bet was wrong on both rings.

For the full six-bit observation `P15`, two retained lags on `D2`, the complete retained ring history **does determine** the next complete retained field on both `n=6` and `n=7`. Yet the accepted predecessor still has conflicts at every radius `R=0,1,2` for that same representation and domain.

So, on these finite rings and this frozen reachable family, the `P15,h=2,D2` obstruction is **not representation-level information loss**. The needed information is present globally; its bounded locality scale is unresolved.

This does not prove any local factor at radius greater than two, any translation-equivariant rule, or any arbitrary-width/infinite-lattice closure.

## Frozen family

The protocol imports #131 without changing the represented system:

- touching-strip physical law and exhaustive declared source-pair family;
- source rings `n=6,7`, scored separately;
- coarse transitions through `t=6`;
- mandatory `A,B` plus the same 16 masks over `E0..E3`;
- history depths `h=0,1,2`;
- same-domain comparisons `D0/h0`, `D1/h0,h1`, `D2/h0,h1,h2`;
- complete-field single-valuedness as the only new scoring object.

There are exactly `2 × 6 × 16 = 192` primary cells.

## Exact outcome

### G1 and G3 controls pass

The accepted #131 source hashes, full-state local verdicts and canonical local witnesses replay exactly. Same-domain history monotonicity has no violation.

The packed whole-field implementation and an independently written explicit-tuple implementation agree on all 192 global verdicts and canonical conflict pairs.

### G4: the primary nondeterminism bet fails on both rings

The frozen bet predicted a global conflict for `P15,h=2,D2` on each ring. Instead:

- ring 6: **pass**;
- ring 7: **pass**.

There is therefore no canonical global conflict for this cell on either ring.

Combined with #131, the finite result is sharp: radius two is insufficient, but the complete retained two-lag field is sufficient on the tested rings/domain.

### G5: the full-state ladder changes only at two lags on D2

The `P15` ladder is identical on rings 6 and 7:

| Domain / history | Global verdict |
| --- | --- |
| `D0 / h0` | conflict |
| `D1 / h0` | conflict |
| `D1 / h1` | conflict |
| `D2 / h0` | conflict |
| `D2 / h1` | conflict |
| `D2 / h2` | **pass** |

No trend is inferred across different domains. Within a domain, the frozen monotonicity control applies.

### G6: only nine of 192 cells pass

Every global pass occurs at `D2,h=2`.

- ring 6: masks `{11,13,15}` pass;
- ring 7: masks `{3,5,7,11,13,15}` pass.

Thus 9 cells pass and 183 conflict.

The Pareto-minimal passing representations under `(retained interface-bit count, history depth)` are:

- ring 6: masks 11 and 13 at `h=2`, each retaining three interface bits in addition to mandatory `A,B`;
- ring 7: masks 3 and 5 at `h=2`, each retaining two interface bits in addition to mandatory `A,B`.

These ring-specific minima are finite-domain facts, not evidence for a canonical mask or an infinite-lattice representation.

### G7: every global conflict independently replays

All 183 conflicting cells have independently replayed canonical witnesses. For each, the two records have literally equal complete retained histories, differing next retained fields, and a real current physical difference outside the retained information on the shared physical-coordinate domain.

A differing finite replay-window shape is never counted as hidden information. The primary and reference implementations agree on every one of the 192 cells.

### G8: the predecessor's local failures split into two kinds

For the 183 globally conflicting cells, the frozen finite-ring label is `information-loss certified on this finite ring/domain`: no increase of spatial radius alone can repair that exact retained representation there.

For the nine global passes, including full `P15,h=2,D2` on both rings, the label is `global-information present; bounded locality unresolved`: the complete field determines the next field while the accepted radii through two do not.

This split is the main result of the unit.

## What this changes

The accepted #131 result could not distinguish insufficient radius from information erased by the symbolic coordinate. This audit shows that both phenomena occur inside the same frozen family.

Most tested representations truly remain globally nondeterministic: 183 of 192 cells identify histories with different next retained fields. But two lags on `D2` cross a threshold for a small set of masks, including the full six-bit state on both rings. For those cells, short history has not made the local factor visible at radius two, but it has restored enough information at the level of the complete ring.

That is a reason to keep **history depth**, **retained information** and **spatial locality radius** as separate resources. It is not permission to choose a larger radius post hoc inside this unit. A minimal-radius follow-up, if pursued, requires its own frozen protocol.

## Evaluation history and reproducibility

Protocol-only #156 and clarification-only #158 preceded implementation. Implementation-only #159 pinned `scripts/verify_interface_history_global.py`, permanent two-tier CI and the future result-integrity registration with no canonical result present; exact final implementation head `ca5c9c8ca1db5092d1768b9944d24e9a8ad1713d` passed all 26 applicable checks and merged as `1163d7b0898fa3e9e0e68c9b26fe3ccf8fc2a9bb`.

Evaluation #160 then ran the unchanged integrated verifier once on the frozen source domain and committed the canonical result. Temporary one-shot evaluation and inspection artifacts were removed; the final evaluation diff contained only `results/interface_history_global_20260912.json`. The permanent workflow replayed that JSON byte for byte on the cleaned evaluation head and all five exact-head checks passed.

Reproduce from the repository root:

```bash
python scripts/check_result_integrity.py results/interface_history_global_20260912.json
python scripts/verify_interface_history_global.py
```

## Boundaries

This result is bounded to rings `n=6,7`, the declared touching-strip reachable family, coarse transitions through `t=6`, history depth `h<=2`, the frozen 16 masks and complete retained ring fields.

A global pass is only finite-ring single-valuedness on the reachable set. It does **not** establish a bounded-radius factor, translation-equivariance, a uniform rule across ring sizes, or an infinite-lattice theorem.

A global conflict is likewise bounded to the declared finite ring/domain. The unit does not exclude deeper history, moving/support-tracking state, alternative coordinates, growing-support descriptions or additional physical variables.

No recursive `2D->3D` lift, intrinsic dimension, self-assembly, endogenous control, Class IV, universality, renormalization, spacetime emergence, physics, metaphysics, prime or `8n+1` claim follows.
