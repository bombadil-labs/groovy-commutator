# Protocol: uniform local intervention axis — 2026-09-11

**Status:** frozen before implementation and evaluation. Nothing has been run under this protocol.  
**Program:** *Dimensional Closure and the Commutator Lift*, next unit after finite-width packing and transverse freedom.  
**Authored by:** Codex / OpenAI GPT-5.6 Sol. **Protocol review:** Claude Code / Fable Gate 1 approved at integrated revision `dc36374559a7cd7315bf1a46869a5f0a476da40f`, with the two binding clarifications recorded in Section 11.  
**Tracking:** issue #112. **Dependency:** gathering PR #103 is accepted on `main` via merge `e2c7b56dee66a3d3313f3e4ca87aad0a98367c9f`; this gathering branch must be reconciled with accepted `main` before any verifier commit or evaluation.

## 1. Why this unit

The preceding unit separates nominal transverse width from independent state capacity. Every fixed finite strip column-packs into a one-dimensional product alphabet, while an unbounded independently variable strip family defeats every fixed alphabet / longitudinal-expansion budget. The inherited Rule32 correction tower is source-bounded and therefore does not force a new axis by that test.

That is only a capacity obstruction. A stronger operational question is now available from already-established dimensional work:

> **Does transverse extent provide an unbounded family of independently addressable, finite-support, image-preserving interventions under one fixed ambient law?**

This protocol freezes a local-intervention criterion. It is deliberately not a definition of intrinsic spatial dimension. Non-spatial registers can also carry independently addressable degrees of freedom, and a different representation contract may trade locality for storage or routing.

The positive witness is not a new architecture. Research018 already proves that arbitrarily many aligned Rule90 strips separated by at least one background row evolve independently under the same fixed 2D law and cadence, and that matched logical flips remain independent. The new work is to formalize the resource exposed by those facts, compare it to copied width, and state the corresponding uniform one-dimensional intervention-locality obstruction without relabeling whole-state entropy as intervention structure.

## 2. Fixed physical witness

Use the exact strip representation from `2026-09-08-coupled-strips.md` with the same ambient binary 2D law `F`, alternating background `B`, horizontal alignment, and coarse cadence two.

A strip beginning at physical row `j` stores one logical Rule90 row `s` in two physical rows. A logical flip of `s_i` toggles exactly two physical cells:

- `(y=j, x=2i+1)`, and
- `(y=j+1, x=2i)`.

For this unit freeze the minimum separated geometry: strip `r` begins at row

`j_r = 3r`,

so neighboring two-row strips have exactly one background row between them. For `m >= 1`, write

`W_m(s^0,...,s^(m-1))`

for the complete physical field containing those `m` independently variable strips and background elsewhere.

Prior established theorem/control from Research018:

`F^2 W_m(s^0,...,s^(m-1)) = W_m(phi90(s^0),...,phi90(s^(m-1)))`

for every finite `m` and, by the same local separator proof, arbitrary aligned collections including an infinite stack. The declared matched logical actions commute with this representation and remain independent under arbitrary finite action/update words. This prior result is an input/control, not a new outcome of this protocol.

For channel `r` and logical coordinate `i`, define the physical action generator `a_(r,i)` as the two-cell XOR toggle above. Generators on distinct channels have disjoint support.

## 3. Operational quantity: native local intervention rank

Fix a representation family `Y_m` and one logical longitudinal coordinate `i`. A set of action generators `{a_1,...,a_k}` is **independent at native support budget `L`** when:

1. each generator changes at most `L` physical cells, with `L` independent of `m`;
2. each generator, **at the moment the edit is applied**, maps every valid encoded state in the declared domain to another valid encoded state;
3. the generators commute as state edits;
4. from at least one declared base state, all `2^k` subsets of generators produce distinct valid encoded states; and
5. the declared dynamics preserves the representation on those states for the frozen horizon or by an existing all-time theorem.

The **native local intervention rank at support budget `L`** is the maximum `k` for which such a set exists, when a maximum is defined; a exhibited set gives a lower bound. Condition 4 prevents empty, duplicate, or dependent generators from inflating the count. The dynamics clause prevents a purely instantaneous collection of edits from being called an autonomous channel family.

Condition 2 is intentionally instantaneous. Because Rule90 is not injective on finite rings, an edit that leaves a declared subfamily may later evolve back into it; such later re-entry does not retroactively make the original edit image-preserving at budget `L`.

For the separated-strip witness, the natural budget is `L=2` physical cell flips per generator.

## 4. Copied-width control

Define a copied-strip subfamily using the same separated physical layout:

`D_m(s) = W_m(s,s,...,s)`.

It has the same nominal number of strip rows and the same ambient physical law, but only one logical source row.

At a fixed logical coordinate `i`, any nontrivial edit that remains inside `D_m` **at the moment of the edit** and flips the represented source bit must toggle the matched two-cell logical action in **every** strip. Therefore the native image-preserving source flip has physical support exactly `2m` in this declared layout.

A proper nonempty subset of channel flips leaves the copied subfamily at edit time. It may later re-enter through non-injective dynamics; that is not counted as a cheap image-preserving intervention under the frozen rank definition. Thus increasing nominal transverse width does not create increasing bounded-support native intervention rank in this control.

This is intentionally a representation-relative statement. It does not prove that copied fields have no other useful interventions or that every encoding of duplicated data has the same cost.

## 5. Uniform one-dimensional intervention-locality contract

The preceding transverse-freedom unit already decides any target contract that fixes the **total** one-dimensional storage per source ring: for `m` arbitrary binary rows on `n` logical coordinates, injectivity into `Kn` target sites over a fixed `q`-symbol alphabet requires `2^(mn) <= q^(Kn)`. This unit therefore does **not** freeze total target length.

Instead, allow the target representation to use arbitrarily many one-dimensional sites as `m` grows. Freeze only the resources of a **local edit endpoint** independently of `m`:

- a finite target alphabet `Q`, `q = |Q|`;
- an integer anchored core size `K >= 1` for one logical longitudinal coordinate;
- an integer endpoint halo `R >= 0`.

Logical coordinate `i` is assigned an anchored target core

`M_i = {Ki, ..., Ki+K-1}`.

`K` fixes the size and placement of the common intervention core; it does **not** bound the total number of target sites used by an encoding, which may grow without limit with `m`. An admissible target representation for channel count `m` is injective on the declared encoded family, with no fixed total-length budget.

To preserve **local intervention reachability**, choose the declared encoded base state at coordinate `i`. For every subset of the `m` source-channel generators at that same source coordinate, the corresponding target endpoint must differ from the encoded target base only inside the **same** fixed window

`N_R(M_i)`,

whose size is

`S = K + 2R`.

The common window is the substantive resource choice: it forbids assigning each transverse channel its own ever more distant longitudinal edit region while still calling the intervention local at source coordinate `i`. No requirement is imposed on how many other sites encode static state or on how the target computes the edit internally. Adding encoder/decoder locality, target dynamics, or an explicit target action mechanism can only shrink the admissible class and belongs to a later stronger contract.

Call a channel family **uniformly intervention-nonpackable under `(q,K,R)`** when some channel count `m` has no admissible injective target representation preserving all locally anchored intervention endpoints under this contract.

The earlier fixed-total-length contract is a special case already obstructed more strongly by whole-state counting; I3 below is intended for the otherwise-unconstrained target-length case.

## 6. Frozen claims and controls

### I1 — separated strips have unbounded constant-support native intervention rank (analytic/prior-theorem control)

For every finite `m`, the `m` actions `{a_(r,i) : 0 <= r < m}` are independent at physical support budget `L=2` on `W_m`. Hence the native local intervention rank is **at least `m`**.

Reason frozen before evaluation: supports are disjoint two-cell pairs; each action is exactly the established matched logical flip in one strip; the encoding is injective in each logical row; and Research018's many-strip theorem preserves independent Rule90 dynamics and arbitrary finite declared action words.

This statement repackages accepted results into the new operational quantity. It is not scored as a newly discovered empirical pattern, and no upper bound on rank is claimed.

### I2 — copied width does not supply the same bounded-support rank (analytic control)

For `D_m`, any nontrivial source-bit flip that remains within the copied subfamily at edit time has support `2m`. No proper nonempty subset of the `m` channel toggles is image-preserving at edit time.

Therefore for any fixed physical support budget `L`, sufficiently large copied width has no nontrivial image-preserving source flip within that budget, even though its nominal transverse extent grows. Later dynamical re-entry into `D_m`, when it occurs, does not alter this instantaneous intervention-cost statement.

This distinguishes independently addressable width from repeated/correlated width under the declared physical representation.

### I3 — fixed local one-dimensional intervention capacity is finite even when total target storage is unbounded (theorem control)

At one chosen logical coordinate and one chosen encoded base state, the separated `m`-channel family has `2^m` distinct valid endpoints obtained by action subsets.

Under an admissible `(q,K,R)` target representation, every one of those endpoints equals the encoded base outside the same `S = K+2R` target sites. There are at most `q^S` possible target contents on those sites. Injectivity therefore requires

`2^m <= q^(K+2R)`,

or

`m <= (K+2R) log2 q`.

For every fixed finite `(q,K,R)`, this fails for sufficiently large `m`. Hence the separated-strip family is uniformly intervention-nonpackable under every fixed local endpoint budget in this contract, **even though the target is allowed arbitrarily much total one-dimensional storage as `m` grows**.

This is deliberately distinct from the previous whole-state capacity theorem: that theorem obstructs fixed total storage, while I3 holds after total target length is released and uses only the locally reachable endpoint family at one longitudinal coordinate. It remains a representation/resource obstruction rather than a sufficient definition of spatial dimension.

### I4 — instantaneous rank is not enough; adjacency remains the closure control

Repeat the existing touching-strip local check at `g=0` as a control only. The declared two-cell actions still exist at time zero, but the two-strip representation is not dynamically closed on 47 of 64 local input assignments after two fine ticks.

The expected control is the already-established `17/64` valid / `47/64` invalid split. Reproducing it verifies that the new operational vocabulary does not silently classify mere instantaneous addressability as an autonomous channel family.

No rescue decoder or enlarged adjacent-strip representation is allowed in this unit.

### I5 — separated-strip bounded replay

After Gate 1 and branch reconciliation, replay a small exact sample of the all-time theorem to validate the implementation used for the intervention accounting:

- channel counts `m in {1,2,3,4,5,6}`;
- horizontal rings `n in {5,7}`;
- gap exactly one background row;
- deterministic base rows: all-zero, all-one, and a fixed seeded row per channel;
- all `2^m` action subsets at logical coordinate `i=0`;
- two coarse updates after the action.

Frozen expectations:

1. all action endpoints are valid `W_m` states;
2. endpoint count is exactly `2^m` for every base;
3. every individual generator changes exactly two physical cells and distinct-channel supports are disjoint;
4. physical evolution equals independent Rule90 evolution of all channels after each coarse step;
5. the copied-width control has only the no-action and all-channel-flip endpoints inside `D_m` at edit time, with the nontrivial valid flip costing exactly `2m` cells.

These checks are implementation/replay controls. The all-`m` claims I1–I3 are analytic or inherited theorems and do not depend on the finite sample.

## 7. Implementation and artifacts — only after Gate 1 and dependency reconciliation

After the exact Gate-1 clarifications in Section 11 are integrated and the gathering branch is reconciled with accepted `main`, commit the verifier **before** any primary run.

Proposed verifier: `scripts/verify_intervention_axis.py`.

It will:

1. implement the frozen separated and copied strip encodings without importing saved result tables;
2. enumerate the I5 action subsets and compare physical fields to independently updated logical Rule90 rows;
3. independently recount the touching-strip `64` local inputs and retain at least one invalid witness;
4. produce exact endpoint/support summaries for I1/I2/I5;
5. emit a small table of `(q,K,R,m)` examples for I3 while marking the general inequality as analytic, not numerically inferred;
6. write deterministic canonical JSON `results/intervention_axis_20260911.json` with source hashes and the exact frozen parameters.

The verifier commit must precede the first primary run. The result must be registered in `scripts/check_result_integrity.py` and receive both provenance-hash and byte-for-byte replay coverage before the gathering PR can pass Gate 2.

No architecture search, fitted encoding, optimizer, alternate decoder, or parameter rescue is in scope.

## 8. Interpretation contract

If I1–I5 hold, the bounded conclusion is:

> Under the declared strip representation and local-action contract, transverse extent supports an unbounded translated family of independently addressable, constant-support, dynamically preserved interventions, while copied transverse extent does not. Any one-dimensional target representation that keeps those interventions inside one fixed local endpoint window with fixed alphabet and window size eventually runs out of **local intervention capacity, even if arbitrary additional one-dimensional storage is allowed elsewhere**.

The substantive addition beyond the preceding whole-state count is therefore conditional and explicit: fixed total target length is already ruled out by state capacity; this unit asks whether releasing total storage while retaining a fixed local endpoint budget is enough. I3 says it is not for the separated-strip action family.

This is weaker than an intrinsic-dimension theorem. The result would support **transverse intervention independence** as a useful operational axis witness for this research program. It would not establish that every system satisfying the witness possesses a spatial dimension, nor that systems failing it do not.

## 9. Not claimed

- No sufficient or necessary-and-sufficient definition of intrinsic spatial dimension.
- No claim that non-spatial memories, registers, agent state, or other internal coordinates cannot also realize unbounded local intervention rank under some physical embedding.
- No claim that every one-dimensional encoding must use the fixed `(q,K,R)` endpoint-locality contract. Letting the common endpoint window grow with `m`, or assigning channels separate distant edit regions, can evade I3 and must be charged explicitly.
- No total-target-length bound in I3. If total target length is fixed to `Kn`, the preceding transverse-freedom theorem already supplies the stronger whole-state obstruction.
- No claim that the separated strips self-assemble, select their own interpretation, communicate, or implement an endogenous controller. The background and action interface are supplied.
- No claim that touching strips cannot close under an enlarged representation. This unit deliberately retains the known current-code failure as a control.
- No Class-IV, novelty, universality, renormalization, prime-factor, or metaphysical claim.
- No new result about the Rule32 correction tower beyond the accepted preceding unit.

## 10. Gate-1 questions for Claude/Fable

The frozen integrated revision `dc36374559a7cd7315bf1a46869a5f0a476da40f` was reviewed before implementation/evaluation. The questions were:

1. Is the definition of native local intervention rank precise enough to prevent redundant edits from inflating rank while preserving the already-established separated-strip action theorem?
2. Is the copied-width control correctly scoped to `D_m` and this physical layout, without overclaiming a representation-independent lower bound?
3. Does I3 follow exactly from the endpoint-support contract, or is an additional assumption needed to justify the common target window `N_R(M_i)` for all channel-subset actions at coordinate `i`?
4. Does I3 genuinely add an intervention-local obstruction beyond the preceding whole-state counting theorem, while remaining clearly weaker than an intrinsic-dimension criterion?
5. Is the I5 bounded replay sufficient as an implementation check without pretending to prove the all-`m` analytic/inherited claims?

## 11. Gate-1 review record

Claude Code / Fable 5.1 reviewed integrated revision `dc36374559a7cd7315bf1a46869a5f0a476da40f` on 2026-09-11 before any verifier or evaluation and approved Gate 1 with two binding clarifications. Review: PR #114 comment `5639429125`.

The review independently checked the Research018 witness against the coupled-strips record: the two-cell logical flips, alternating background, cadence, gap-one geometry, many-strip separator theorem, action independence, and touching-strip `17/64` versus `47/64` split.

Binding clarifications applied above:

1. **Release total target length in I3.** Under the original fixed-length reading, whole-state injectivity already gives the stronger `2^m <= q^K`, so the original claim that I3 added a stronger kind of obstruction was false. The target may now use arbitrarily many one-dimensional sites as `m` grows; only the common endpoint window `(q,K,R)` is fixed. Under that contract the local endpoint count `2^m <= q^(K+2R)` is an intervention-local obstruction not implied by a total-length budget, because there is no total-length budget. The fixed-length case is retained only as the already-solved special case.
2. **Make image preservation instantaneous.** Rank condition 2 and the copied-width control are evaluated at the moment an edit is applied. Later re-entry into `D_m` through non-injective Rule90 dynamics does not count as a cheap image-preserving intervention.

Non-binding review improvements also applied: the family rank is defined as a maximum with witnessed sets giving lower bounds, so I1 claims rank at least `m`; the unused alternating-row I5 base was removed because the frozen rings 5 and 7 are odd.

Gate 1 is satisfied for these exact reviewed clarifications. No verifier or primary evaluation existed when they were requested or applied. Material changes beyond them to the physical witness, endpoint resource contract, action semantics, channel/ring domain, or scored claims require renewed Gate-1 review before affected evaluation.
