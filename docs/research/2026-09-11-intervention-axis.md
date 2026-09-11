# Transverse extent supports unbounded constant-support intervention rank under the separated-strip representation

**Research note, 2026-09-11.** Completed operational-axis unit of [Dimensional Closure and the Commutator Lift](2026-09-09-dimensional-closure-program.md). Authored by: Codex / OpenAI GPT-5.6 Sol. Protocol: [`intervention-axis-20260911.md`](protocols/intervention-axis-20260911.md). Claude Code / Fable 5.1 approved Gate 1 at integrated revision `dc363745`, with two binding clarifications applied before implementation: total target storage is unbounded in I3 while the common local endpoint window stays fixed, and image preservation is evaluated at edit time. The gathering branch was reconciled with accepted `main` before implementation. Verifier `scripts/verify_intervention_axis.py` was pinned at `c8d6c1a` and integrated at `77ae5a5` before the first primary run. Canonical result: [`results/intervention_axis_20260911.json`](../../results/intervention_axis_20260911.json), first committed by the one-shot evaluation at `eba1b0c`; permanent source-integrity and byte-for-byte replay CI is green. Final gathering review: pending Claude/Fable Gate 2.

## Question

The preceding transverse-freedom unit established a capacity distinction: every fixed finite width packs into a product alphabet, whereas independently variable unbounded width eventually exceeds any fixed total one-dimensional storage budget. That still leaves a different operational question:

> Does transverse extent provide an unbounded family of independently addressable, finite-support interventions that remain inside one dynamically closed representation, even when a one-dimensional target is allowed arbitrarily much total storage?

This unit answers that question for one already-established physical witness: the separated Rule90 strips of Research018. It does **not** define intrinsic spatial dimension.

## The physical witness

Use the fixed binary 2D law, alternating background, horizontal alignment and two-fine-tick cadence of the coupled-strips construction. Strip `r` begins at physical row `3r`, so every neighboring pair of two-row strips has one background row between it. Research018 already proved that any finite or infinite aligned collection of such strips evolves as independent Rule90 rows, and that matched logical flips remain independent under arbitrary finite action/update words.

At logical coordinate `i`, one channel action flips exactly the two physical cells representing that logical bit. For `m` channels, the `m` generators have disjoint two-cell supports.

The new operational vocabulary calls a set of generators independent at native support budget `L` when each edit has support at most `L`, maps the valid representation to itself **at the moment of the edit**, the edits commute, all subsets give distinct valid endpoints from a declared base state, and the declared dynamics preserves the representation. Native local intervention rank is the largest such `k` when a maximum is defined; an explicit set gives a lower bound.

## I1 — separated width has unbounded constant-support rank

For every finite `m`, the `m` translated strip actions witness native local intervention rank **at least `m` at support budget two**. This is an analytic consequence of the accepted many-strip/action theorem, not an extrapolation from the new finite run.

The bounded replay checks `m=1..6`, horizontal rings `n=5,7`, zero/one/fixed-seeded channel rows, every one of the `2^m` action subsets at one logical coordinate, and two coarse updates. Every endpoint is a valid encoded state; the number of distinct endpoints is exactly `2^m`; every generator changes exactly two physical cells; distinct-channel supports are disjoint; and after each coarse update the physical field equals independently evolved literal Rule90 rows.

## I2 — copied width does not have that cheap native action family

The copied control uses the same transverse layout but constrains every strip to carry the same logical row:

`D_m(s) = W_m(s,s,...,s)`.

A source-bit flip that remains inside `D_m` at edit time must toggle the matched two-cell action in every channel, for support exactly `2m`. Every proper nonempty subset leaves the copied family at edit time. Later re-entry under non-injective Rule90 dynamics is explicitly irrelevant to this instantaneous intervention-cost statement.

The bounded replay reproduces exactly that structure for every declared `m`, ring and base: only the no-action subset and the all-channel subset remain in `D_m` at edit time, and the nontrivial valid edit costs `2m` cells.

Thus nominal transverse extent and independently addressable transverse extent differ under the same ambient physical law and layout.

## I3 — a fixed one-dimensional local endpoint window eventually runs out of intervention capacity

The important Gate-1 correction separates this theorem from the previous whole-state counting theorem. The one-dimensional target may use **arbitrarily many total sites as `m` grows**. Freeze only:

- a finite target alphabet of size `q`;
- a fixed anchored core of `K` target sites for one logical longitudinal coordinate; and
- a fixed endpoint halo `R`.

Every subset of the `m` source-channel actions at that one logical coordinate must map the encoded base to a target endpoint that differs from the target base only inside the **same** `K+2R`-site window. The rest of the target may be arbitrarily large and may store arbitrary static state.

The source has `2^m` distinct reachable endpoints. The common target edit window has at most `q^(K+2R)` contents. Injectivity therefore requires

`2^m <= q^(K+2R)`.

For every fixed finite `(q,K,R)`, sufficiently large `m` violates this bound. This is a local-intervention obstruction even after total one-dimensional storage is released. It can be evaded by allowing the common edit window to grow with `m`, by assigning channels separate ever more distant edit regions, or by changing the representation contract; those resources must then be charged explicitly.

The canonical JSON includes four exact numerical examples only as implementation controls. The inequality above is the proof.

## I4 — addressability without dynamical closure is not enough

As a negative control, the verifier independently reconstructs the existing touching-strip `g=0` local census. The same instantaneous two-cell actions exist, but the two-strip code is not dynamically closed after two fine ticks on **47 of 64** local input assignments; only **17 of 64** remain valid, and all valid cases agree with independent Rule90.

The first retained invalid witness is the established pair of logical triples `100/100`: the candidate decoded outputs are both one, while physical cell `(y=2,x=0)` violates the code. This prevents the intervention-rank vocabulary from silently treating a merely editable but non-autonomous representation as an operational axis witness.

## What this adds beyond state capacity

The previous unit said that independent unbounded width needs growing total representational capacity. This unit holds total target capacity open and instead fixes the **locality of intervention endpoints**. The separated strip family still forces a resource to grow: either the common one-dimensional action window, the alphabet, or some equivalent routing/addressability resource must scale with the number of independently addressable transverse channels.

That is a **different, complementary operational distinction** from nominal row count or whole-state capacity: I3 adds content specifically when total target length is unconstrained while the common local endpoint window remains fixed. It is still representation-relative.

A useful bounded reading for the dimensional program is:

> Under the declared strip representation and action contract, transverse extent supplies an unbounded translated family of independently addressable, constant-support, dynamically preserved interventions. Copied extent does not. A one-dimensional representation with a fixed alphabet and fixed common local endpoint window cannot preserve that action family for arbitrarily many channels, even if arbitrary additional one-dimensional storage is available elsewhere.

This makes **transverse intervention independence** a concrete axis witness for the program. It is not a sufficient definition of spatial dimension.

## Process and reproducibility

Protocol integration `dc363745` preceded Gate 1. Fable's two binding clarifications were applied before implementation, and the gathering branch was reconciled with accepted `main` at `9ff73e4`. Implementation `c8d6c1a` and its permanent workflow `7f7eb64` were integrated at `77ae5a5` with no canonical result present. Only then did one-shot orchestration `130d8e5` run the pinned verifier; the bot committed the first canonical result at `eba1b0c`. Integrity registration `47ff2f6` and one-shot cleanup `7a74015` followed; evaluation was integrated at `8bffdd5` after all 18 checks, including the permanent byte-for-byte replay, were green.

During Gate 2, Claude/Fable found two publication-record issues without challenging the verifier, canonical result, or I1–I5 conclusions: the knowledge node/edge had inherited the wrong `history-repairability` provenance, and two public summaries described I3 as “stronger” than the preceding capacity theorem rather than a different resource contract. The wording was corrected, then current `main` (including the accepted ring-closure-certificate unit) was merged into the gathering branch at `3791dc7`; that reconciliation retained both programs' registries and rewrote the intervention knowledge node/edge to `intervention-axis` provenance. No verifier or result artifact changed in this correction round.

No frozen prediction, domain, representation contract, or scored control was changed after the first primary run. The one-shot runners are absent from the final tree but their commits remain in history.

## Limits

- The positive physical witness is the prepared separated-strip family under one fixed 2D law, background, alignment and supplied action interface. It does not self-assemble or choose its own interpretation.
- I1 is inherited from the exact all-gap/many-strip theorem; the new replay is bounded to `m<=6`, rings 5 and 7, and two post-action coarse updates.
- I2 is a statement about the declared copied representation and instantaneous image-preserving edits, not a representation-independent lower bound on duplicated information.
- I3 assumes one common target endpoint window for all channel-subset actions at one source coordinate. Non-spatial registers or agent state can also realize high local intervention rank under suitable physical embeddings.
- Touching strips may close under a larger representation; this unit deliberately does not introduce one.
- No intrinsic-dimension theorem, self-assembly, endogenous-control, Class-IV, novelty, universality, renormalization, prime-factor, or metaphysical claim is established.
