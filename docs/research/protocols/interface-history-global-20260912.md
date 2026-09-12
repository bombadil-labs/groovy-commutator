# Protocol: full-field determinism of the frozen interface history — 2026-09-12

**Status:** frozen before implementation/evaluation. Nothing in this protocol has been run.  
**Program:** *Dimensional Closure and the Commutator Lift*.  
**Authored by:** Codex / OpenAI GPT-5.6 Sol.  
**Protocol review:** pending independent Gate 1 on the exact integrated gathering head. **No verifier or source-domain execution is authorized before Gate 1.**  
**Base:** `main` at `b5021cfb21658ad40c8a380e9eb525d402934daf`, after Claude/Fable Gate 2 and reviewer merge of finite interface-history PR #131.  
**Predecessors:** accepted touching-strip interface factor #125 and accepted finite interface history #131.

## 1. Question

The accepted interface-factor unit showed that the frozen six-bit touching-strip coordinate `(A,B,E0,E1,E2,E3)` has no local autonomous factor through radius two on the declared `n=6,7` reachable family. The accepted interface-history unit then showed that adding one or two temporal lags of those same symbols still leaves **every** frozen local budget through radius two conflicting.

Those results deliberately left two different explanations open:

1. the retained symbolic field may contain enough information globally, but the required factor may need a radius larger than two; or
2. the retained symbolic field itself may identify physically distinct states with different next symbolic fields, in which case **no spatial radius at all** can rescue that representation on the tested ring.

This unit asks the cheapest question that separates those cases:

> **For the same frozen touching-strip coordinate and history depths `h<=2`, does the complete retained symbolic field determine the next complete symbolic field on rings 6 and 7?**

This is a full-field determinism audit, not a new spatial encoding and not a search over larger local radii. It changes only the scoring object from a bounded local neighborhood to the entire retained ring field.

## 2. Frozen physical and symbolic family

Import the accepted source family and exact coordinate from #131 without change:

- the same touching-strip physical law and encoder;
- source rings `n in {6,7}`;
- the same exhaustive declared source-pair family for each ring;
- coarse times through `t=6`;
- current six-bit symbol `P_15=(A,B,E0,E1,E2,E3)` and all interface masks `m=0..15`, where `A,B` are always retained and the four `E` bits are selected by the mask;
- history depths `h=0,1,2`;
- the same domains `D0=t0..6`, `D1=t1..6`, `D2=t2..6`;
- the same oldest-to-newest history ordering and symbol bit order frozen in #131.

No new physical state, moving frame, support tracker, decoder, radius, lag depth, mask, source ring, time horizon or source configuration is introduced in this protocol.

For each mask `m`, write `P_m(t) in Sigma_m^n` for the complete ring of retained current symbols at coarse time `t`. For history depth `h`, define the complete retained history field

`H^global_{m,h}(t) = (P_m(t-h), ..., P_m(t))`.

This is the **whole ring field**, not a local neighborhood around one site.

## 3. Full-field determinism

Fix one ring size `n`, one transition domain `Dk`, one allowed depth `h<=k`, and one mask `m`.

The retained representation is **globally deterministic on that frozen domain** iff for every two records `x,y` in the exhaustive declared reachable family,

`H^global_{m,h}(x) = H^global_{m,h}(y)`

implies

`P_m(x_next) = P_m(y_next)`.

Equivalently, the map from complete retained history fields to the next complete retained field is single-valued on the declared reachable set.

A **global conflict** is a pair of records with equal complete retained history fields and different next complete retained fields.

This criterion allows an arbitrary nonlocal deterministic factor on the finite ring. Therefore:

- a **conflict** proves that no local radius, including a radius covering the whole ring, can determine the next retained field from this representation on that ring/domain;
- a **pass** proves only finite-ring full-field determinism. It does **not** prove a bounded-radius local factor, a uniform rule across ring sizes, or an infinite-lattice factor.

## 4. Same-domain comparison rule

Preserve the predecessor's attribution rule exactly.

- On `D0`, score only `h=0`.
- On `D1`, score `h=0,1` on the same set of transitions.
- On `D2`, score `h=0,1,2` on the same set of transitions.

No claim that history helps may compare a deeper history on `Dk` with a shallower history on a larger warm-up domain. This prevents a false pass caused merely by dropping early transitions.

Ring sizes are scored separately. Records of different `n` are never compared as equal global fields.

## 5. Frozen predictions and controls

### G1 — accepted local-result regression

Before scoring any new global verdict, replay the accepted #131 canonical source hashes and the full-state `P15` local verdicts on `D0/D1/D2` at `R=0,1,2`.

Expected: all accepted full-state local cells remain conflicting, with the #131 canonical local witnesses unchanged under the imported ordering.

A mismatch is an implementation/provenance failure and blocks interpretation.

### G2 — global determinism census

For every ring `n in {6,7}`, every domain/depth pair

- `(D0,h0)`,
- `(D1,h0)`, `(D1,h1)`,
- `(D2,h0)`, `(D2,h1)`, `(D2,h2)`,

and every mask `m=0..15`, classify the complete retained field as **pass** or **conflict**.

There are `2 * 6 * 16 = 192` primary global cells.

For every conflicting cell retain:

- ring size, domain, history depth and mask;
- the lexicographically first pair of exhaustive source records under the frozen ordering;
- the equal complete retained history field;
- the two differing next complete retained fields;
- the first differing site and symbol coordinate in canonical order;
- the complete current physical states needed for independent replay.

### G3 — history-refinement monotonicity control

Within a fixed ring, domain and mask, global determinism is monotone under adding retained history:

- if `h=0` passes on `D1`, then `h=1` must pass on `D1`;
- if `h=0` passes on `D2`, then `h=1` and `h=2` must pass on `D2`;
- if `h=1` passes on `D2`, then `h=2` must pass on `D2`.

Reason: equality of a deeper complete history implies equality of every shallower retained field, while the lag coordinates of the next history are deterministic copies of the current retained fields.

Any violation is an implementation error.

### G4 — primary falsifiable bet: full `P15` remains globally nondeterministic

Freeze before evaluation:

> On **both** rings `n=6` and `n=7`, the complete full-state two-lag field `H^global_{15,2}` on `D2` still has at least one global conflict.

If G4 holds, then on those finite rings and the frozen domain, failure of the full six-bit coordinate through two lags is not merely a radius-two problem: even the complete retained field loses distinctions needed for the next retained field.

If G4 fails on either ring, report that ring as globally deterministic at `(P15,h=2,D2)` and do not reinterpret the predecessor's local conflicts as information loss there. The positive result would instead show that, on that ring/domain, enough information exists globally but not within radius two.

### G5 — shallower full-state ladder

Report the exact six-cell ladder for `P15` separately on each ring:

`D0/h0`, `D1/h0`, `D1/h1`, `D2/h0`, `D2/h1`, `D2/h2`.

No monotone trend across **different domains** is assumed. Within the same domain only G3 applies.

### G6 — mask census and minimal globally deterministic representations

For each ring/domain, report every passing `(mask,h)` pair.

If the passing set is nonempty, compute its Pareto-minimal elements under:

1. retained interface-bit count `popcount(mask)`;
2. history depth `h`.

`A,B` are mandatory and do not enter the interface-bit count.

If no global cell passes, report the Pareto set as empty. Do not add a new mask or deeper history after seeing the outcome.

### G7 — physical replay of global conflicts

Every canonical global conflict must be independently replayed from the complete physical source states with a scalar/reference physical update path distinct from the packed/grouping implementation used to discover conflicts.

For each conflict verify:

1. the complete retained histories are literally equal at every site and lag;
2. the next retained complete fields differ exactly as recorded;
3. the complete current physical fields are not identical;
4. at least one current physical difference lies outside the information retained by the equal symbolic field.

This is a consistency/localization control. It does not prove that every omitted physical bit is individually causally necessary.

A conflict with identical complete physical current states is an implementation failure.

### G8 — relation to bounded local failure

For every global **conflict**, classify the predecessor's local failure as `information-loss certified on this finite ring/domain`: no larger local radius can repair the frozen representation because the entire retained ring field is equal.

For every global **pass** whose accepted `R<=2` local cell conflicts, classify it as `global-information present; bounded locality unresolved`: the complete field determines the next field, but radius two does not.

These labels are bookkeeping for the frozen finite rings. They are not claims about an infinite lattice.

## 6. Independent implementation requirements

No implementation is authorized before exact-head Gate 1.

After approval, the implementation-only/no-result sub-PR must contain:

- exact imported hashes for the accepted #131 protocol, verifier and canonical result;
- the same source enumeration and symbol encoder used by #131, with a provenance check rather than a silent fork;
- a primary grouping implementation that hashes complete history fields and tests whether each key maps to one next field;
- an independently written scalar/reference path that constructs histories as explicit tuples of per-site symbols and checks canonical conflict witnesses without using the primary packed key;
- deterministic canonical ordering for rings, domains, depths, masks, source records, sites and symbol coordinates;
- result-integrity registration and a permanent workflow that is green in the implementation-only stage while the canonical result is absent, then replays byte-for-byte after evaluation.

The two implementations must agree on every stored canonical witness and on every one of the 192 global pass/conflict verdicts once evaluation is authorized.

## 7. Canonical artifact

Proposed paths:

- verifier: `scripts/verify_interface_history_global.py`;
- canonical result: `results/interface_history_global_20260912.json`;
- workflow: `.github/workflows/research-interface-history-global.yml`;
- eventual result note: `docs/research/2026-09-12-interface-history-global.md`.

The result file must record source hashes, all 192 verdicts, the P15 ladders, Pareto sets, every canonical global conflict, G1-G8 verdicts and the exact implementation revision.

## 8. Interpretation ceiling

A negative G4 result on one or both rings would mean only:

> On the declared finite touching-strip reachable family, the complete frozen six-bit interface field with two retained lags is not sufficient to determine its own next complete field on that ring/domain; therefore no increase of spatial radius alone can repair that representation there.

A positive G4 result on a ring would mean only:

> On that finite ring/domain, the complete two-lag full interface field is sufficient globally even though the accepted bounded local radii through two fail; a locality scale larger than two remains possible and unmeasured.

Neither outcome establishes:

- any infinite-lattice or arbitrary-width theorem;
- any all-time closure result beyond the declared coarse horizon;
- anything about history depth `h>2`;
- anything about moving/support-tracking state, alternative coordinates, growing-support descriptions or additional physical variables;
- a uniform finite local radius across ring sizes;
- a recursive `2D->3D` dimensional lift;
- intrinsic dimension, self-assembly, endogenous control, Class IV, universality, renormalization, spacetime emergence, physics or metaphysics;
- any connection to primes or `8n+1`.

This unit deliberately answers the **larger-radius versus information-loss** fork before spending another cycle designing a new coordinate.

## 9. Workflow and dependency

Use the normal gathering/sub-PR protocol:

1. protocol-only sub-PR into `gather/interface-history-global`;
2. author self-review and merge only after exact-head checks are green;
3. independent **Gate 1** on the exact integrated gathering head;
4. only after Gate 1: implementation-only/no-result sub-PR;
5. author self-review and merge implementation when green;
6. evaluation sub-PR performs the first canonical source-domain run;
7. reporting/current-account sub-PRs integrate the result without rewriting earlier accepted records;
8. independent exact-head **Gate 2**;
9. reviewer merge to `main` only after Gate 2 and green exact-head checks.

Any material change after Gate 1 to the physical/source domain, coordinate, masks, history depths, domains, global-determinism criterion, G4 bet, witness ordering or interpretation ceiling requires renewed Gate 1.

## 10. Gate-1 review questions

The independent reviewer should attack especially:

1. Is complete-field single-valuedness the correct finite-ring test for distinguishing insufficient bounded radius from information already lost by the retained representation?
2. Does scoring rings 6 and 7 separately avoid false equalities or false differences caused by field length?
3. Is the same-domain history comparison inherited correctly from #131?
4. Is G3 monotonicity sound for complete-field histories?
5. Is G4 a legitimate predeclared bet rather than a claim already implied by #131's radius-two conflicts? In particular, could the accepted local conflicts disappear once the entire retained ring is visible?
6. Is the 192-cell census complete without adding post-result masks, radii or histories?
7. Does G7 independently validate global conflicts without quietly importing the primary packed-key implementation?
8. Are the G8 labels scoped tightly enough that `information-loss certified` cannot be misread as an infinite-lattice impossibility theorem?
9. Is a global pass correctly treated as a nonlocal finite-ring fact rather than evidence for a bounded local factor?
10. Are the non-claims strong enough to keep moving/support-tracking state and alternative coordinates genuinely open for later separately frozen work?

Gate 1 should be adversarial. Binding corrections must land before implementation or any source-domain execution, and approval must name the exact integrated gathering-head SHA.
