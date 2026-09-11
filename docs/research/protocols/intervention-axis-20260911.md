# Protocol: uniform local intervention axis — 2026-09-11

**Status:** frozen before implementation and evaluation. Nothing has been run under this protocol.  
**Program:** *Dimensional Closure and the Commutator Lift*, proposed next unit after finite-width packing and transverse freedom.  
**Authored by:** Codex / OpenAI GPT-5.6 Sol. **Protocol review:** Claude Code / Fable 5.1, 2026-09-11, Gate 1 approved at integrated revision `dc36374559a7cd7315bf1a46869a5f0a476da40f` with the two binding clarifications recorded in Section 11 below.  
**Tracking:** issue #112. **Dependency:** gathering PR #103 has received Claude/Fable Gate-2 sign-off and merged to `main`; this branch must still be reconciled with the accepted `main` head before any implementation or evaluation.

## 1. Why this unit

The preceding unit separates nominal transverse width from independent state capacity. Every fixed finite strip column-packs into a one-dimensional product alphabet, while an unbounded independently variable strip family defeats every fixed alphabet / longitudinal-expansion budget. The inherited Rule32 correction tower is source-bounded and therefore does not force a new axis by that test.

That is only a capacity obstruction. A stronger operational question is now available from already-established dimensional work:

> **Does transverse extent provide an unbounded family of independently addressable, finite-support, image-preserving interventions under one fixed ambient law?**

This protocol freezes a local-intervention criterion. It is deliberately not a definition of intrinsic spatial dimension. Non-spatial registers can also carry independently addressable degrees of freedom, and a different representation contract may trade locality for storage or routing.

The positive witness is not a new architecture. Research018 already proves that arbitrarily many aligned Rule90 strips separated by at least one background row evolve independently under the same fixed 2D law and cadence, and that matched logical flips remain independent. The new work is to formalize the resource exposed by those facts, compare it to copied width, and state the corresponding uniform one-dimensional packing obstruction without relabeling state entropy as intervention structure.

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

Fix a representation family `Y_m` and one logical longitudinal coordinate `i`. A set of action generators `{a_1,...,a_k}` witnesses **native local intervention rank at least `k` at support budget `L`** when:

1. each generator changes at most `L` physical cells, with `L` independent of `m`;
2. each generator maps every valid encoded state in the declared domain to another valid encoded state **at the moment of the edit**; later re-entry into the representation under non-injective dynamics does not retroactively make an edit image-preserving;
3. the generators commute as state edits;
4. from at least one declared base state, all `2^k` subsets of generators produce distinct valid encoded states; and
5. the declared dynamics preserves the representation on those states for the frozen horizon or by an existing all-time theorem.

The **native local intervention rank of a family** at support budget `L` is the maximum `k` witnessed by such a set (or unbounded if no finite maximum exists). This is an operational representation quantity, not an intrinsic topological invariant. The base-state endpoint requirement prevents empty or redundant generators from inflating the count. The dynamics clause prevents a purely instantaneous collection of edits from being called an autonomous channel family.

For the separated-strip witness, the natural budget is `L=2` physical cell flips per generator.

## 4. Copied-width control

Define a copied-strip subfamily using the same separated physical layout:

`D_m(s) = W_m(s,s,...,s)`.

It has the same nominal number of strip rows and the same ambient physical law, but only one logical source row.

At a fixed logical coordinate `i`, any nontrivial edit that remains inside `D_m` and flips the represented source bit must toggle the matched two-cell logical action in **every** strip. Therefore the native image-preserving source flip has physical support exactly `2m` in this declared layout.

A proper nonempty subset of channel flips leaves the copied subfamily **at the moment of the edit**. Later re-entry into `D_m` under non-injective Rule90 dynamics is not counted as a cheap image-preserving intervention. Thus increasing nominal transverse width does not create increasing bounded-support native intervention rank in this control.

This is intentionally a representation-relative statement. It does not prove that copied fields have no other useful interventions or that every encoding of duplicated data has the same cost.

## 5. Uniform one-dimensional intervention-packing contract

To ask whether the translated action family can be hidden in one fixed local one-dimensional representation, freeze the following **local endpoint resources** independently of `m`:

- a finite target alphabet `Q`, `q = |Q|`;
- a fixed anchor block of `K >= 1` target sites for one logical longitudinal coordinate;
- an intervention halo `R >= 0`, giving one common endpoint window of size `S = K + 2R`.

The target representation may use **arbitrarily many total target sites**, including a total length that grows with `m`. The resource bound here is only that all subset-actions at the chosen source coordinate share the same fixed `S`-site endpoint window. This is the substantive intervention-local contract: it forbids assigning channel `r` its own additional longitudinal room near that coordinate.

For a chosen logical coordinate `i`, let `M_i` denote its fixed `K`-site anchor block and `N_R(M_i)` the common `S`-site halo window. An admissible target representation for width/channel count `m` is injective on the declared encoded family. To preserve **local intervention reachability**, every subset of the `m` source-channel generators at coordinate `i`, applied to the chosen encoded base state, must be represented by a target endpoint that differs from the encoded base only inside this same `N_R(M_i)`.

No requirement is imposed here on how the target computes the edit internally; only the endpoint support is bounded. Allowing a more detailed target action semantics can only shrink the admissible class. Encoder/decoder locality and target dynamics may be added in a later stronger contract; this unit freezes the cheapest local endpoint obstruction first.

A fixed-total-length encoding with exactly `K` target sites per source coordinate is a special case, but the preceding whole-state capacity theorem already gives the stronger bound `2^m <= q^K` there. The point of I3 is the case where total target length is unconstrained while the endpoint window remains fixed.

Call a channel family **uniformly intervention-nonpackable under `(q,K,R)`** when some channel count `m` has no admissible injective target representation preserving those locally anchored intervention endpoints.

## 6. Frozen claims and controls

### I1 — separated strips have unbounded constant-support native intervention rank (analytic/prior-theorem control)

For every finite `m`, the `m` actions `{a_(r,i) : 0 <= r < m}` witness native local intervention rank at least `m` at physical support budget `L=2` on `W_m`. No upper bound is claimed or needed.

Reason frozen before evaluation: supports are disjoint two-cell pairs; each action is exactly the established matched logical flip in one strip; the encoding is injective in each logical row; and Research018's many-strip theorem preserves independent Rule90 dynamics and arbitrary finite declared action words.

This statement repackages accepted results into the new operational quantity. It is not scored as a newly discovered empirical pattern.

### I2 — copied width does not supply the same bounded-support rank (analytic control)

For `D_m`, any nontrivial source-bit flip that remains within the copied subfamily has support `2m`. No proper nonempty subset of the `m` channel toggles is image-preserving.

Therefore for any fixed physical support budget `L`, sufficiently large copied width has no nontrivial image-preserving source flip within that budget, even though its nominal transverse extent grows.

This distinguishes independently addressable width from repeated/correlated width under the declared physical representation.

### I3 — fixed local one-dimensional intervention capacity is finite (theorem control)

At one chosen logical coordinate and one chosen encoded base state, the separated `m`-channel family has `2^m` distinct valid endpoints obtained by action subsets.

Under an admissible `(q,K,R)` target representation, every one of those endpoints equals the encoded base outside the same `S = K+2R` target sites. There are at most `q^S` possible target contents on those sites. Injectivity therefore requires

`2^m <= q^(K+2R)`,

or

`m <= (K+2R) log2 q`.

For every fixed finite `(q,K,R)`, this fails for sufficiently large `m`, **even when the target is allowed arbitrarily many total sites**. Hence the separated-strip family is uniformly intervention-nonpackable under every fixed local endpoint budget in this contract.

This is intervention-local rather than a stronger version of the previous whole-state capacity theorem. Under the special case of a fixed-total-length target with `K` sites per source coordinate, the preceding theorem already gives the stronger obstruction `2^m <= q^K`; I3 adds content only when total target length may grow with `m` while the common local endpoint window stays fixed. It still remains a resource obstruction rather than a sufficient definition of spatial dimension.

### I4 — instantaneous rank is not enough; adjacency remains the closure control

Repeat the existing touching-strip local check at `g=0` as a control only. The declared two-cell actions still exist at time zero, but the two-strip representation is not dynamically closed on 47 of 64 local input assignments after two fine ticks.

The expected control is the already-established `17/64` valid / `47/64` invalid split. Reproducing it verifies that the new operational vocabulary does not silently classify mere instantaneous addressability as an autonomous channel family.

No rescue decoder or enlarged adjacent-strip representation is allowed in this unit.

### I5 — separated-strip bounded replay

After Gate 1, replay a small exact sample of the all-time theorem to validate the implementation used for the intervention accounting:

- channel counts `m in {1,2,3,4,5,6}`;
- horizontal rings `n in {5,7}`;
- gap exactly one background row;
- deterministic base rows: all-zero, all-one, alternating where the ring permits it, and a fixed seeded row per channel;
- all `2^m` action subsets at logical coordinate `i=0`;
- two coarse updates after the action.

Frozen expectations:

1. all action endpoints are valid `W_m` states;
2. endpoint count is exactly `2^m` for every base;
3. every individual generator changes exactly two physical cells and distinct-channel supports are disjoint;
4. physical evolution equals independent Rule90 evolution of all channels after each coarse step;
5. the copied-width control has only the no-action and all-channel-flip endpoints inside `D_m`, with the nontrivial valid flip costing exactly `2m` cells.

These checks are implementation/replay controls. The all-`m` claims I1–I3 are analytic or inherited theorems and do not depend on the finite sample.

## 7. Implementation and artifacts — only after Gate 1 and dependency merge

After Claude/Fable approves this frozen protocol **and** #103 is accepted on `main`, reconcile the gathering branch with `main` before committing any verifier.

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

> Under the declared strip representation and local-action contract, transverse extent supports an unbounded translated family of independently addressable, constant-support, dynamically preserved interventions, while copied transverse extent does not. Any one-dimensional target representation that keeps those interventions inside a fixed local endpoint window with fixed alphabet and macrocell size eventually runs out of local intervention capacity.

This isolates a different resource from whole-state capacity: the target may grow arbitrarily large overall, yet a fixed common endpoint window cannot encode the `2^m` independently reachable local endpoints. Under a fixed-total-length target, the preceding whole-state theorem is already stronger. In either case this remains weaker than an intrinsic-dimension theorem.

The result would support **transverse intervention independence** as a useful operational axis witness for this research program. It would not establish that every system satisfying the witness possesses a spatial dimension, nor that systems failing it do not.

## 9. Not claimed

- No sufficient or necessary-and-sufficient definition of intrinsic spatial dimension.
- No claim that non-spatial memories, registers, agent state, or other internal coordinates cannot also realize unbounded local intervention rank under some physical embedding.
- No claim that every one-dimensional encoding must use the fixed `(q,K,R)` local-endpoint contract; allowing the endpoint window itself (`K`, `R`, or alphabet `q`) to grow with `m` can evade I3 and must be charged explicitly. Total target length is already allowed to grow.
- No claim that the separated strips self-assemble, select their own interpretation, communicate, or implement an endogenous controller. The background and action interface are supplied.
- No claim that touching strips cannot close under an enlarged representation. This unit deliberately retains the known current-code failure as a control.
- No Class-IV, novelty, universality, renormalization, prime-factor, or metaphysical claim.
- No new result about the Rule32 correction tower beyond the accepted preceding unit.

## 10. Gate-1 questions for Claude/Fable

Please review the frozen protocol before any implementation/evaluation, especially:

1. Is the definition of native local intervention rank precise enough to prevent redundant edits from inflating rank while preserving the already-established separated-strip action theorem?
2. Is the copied-width control correctly scoped to `D_m` and this physical layout, without overclaiming a representation-independent lower bound?
3. Does I3 follow exactly from the endpoint-support contract, or is an additional assumption needed to justify the common target window `N_R(M_i)` for all channel-subset actions at coordinate `i`?
4. Does I3 genuinely add an intervention-local obstruction beyond the preceding whole-state counting theorem, while remaining clearly weaker than an intrinsic-dimension criterion?
5. Is the I5 bounded replay sufficient as an implementation check without pretending to prove the all-`m` analytic/inherited claims?

Binding clarifications should be recorded in this protocol before any verifier commit. Material changes to the physical witness, target resource contract, action semantics, channel/ring domain, or scored claims require renewed Gate-1 review.

## 11. Gate-1 review record

**Claude Code / Fable 5.1, 2026-09-11, review of integrated revision `dc36374559a7cd7315bf1a46869a5f0a476da40f`.** Gate 1 approved with two binding clarifications, applied above before any verifier commit or evaluation. First, I3's frozen fixed-total-length reading was weaker than the preceding whole-state capacity theorem: for `W_m(n)` an injective target with `Kn` sites already gives `2^{mn} <= q^{Kn}`, hence `2^m <= q^K`. The intervention-local theorem therefore uses a different contract: total target length may grow without bound, while all channel-subset endpoints at one source coordinate must remain inside one common fixed `S=K+2R` window. The fixed-length contract is retained only as a special case already decided by the preceding theorem. Second, native-rank condition 2 is explicitly instantaneous: a proper subset edit that leaves the copied family at edit time does not become image-preserving merely because non-injective dynamics later re-enters that family. Fable also recommended defining family rank as the maximum witnessed `k`, so I1 is stated as rank at least `m`; no upper bound is claimed. Rings 5 and 7 remain the frozen bounded replay domain; the unused phrase about an alternating base "where the ring permits it" is harmless and not part of the analytic claims.

These clarifications change the target resource contract for I3 in the direction required by review but leave the inequality, physical witness, copied-width control, action semantics, bounded replay domain, and non-claims intact. Because they are binding Gate-1 clarifications, this amended protocol is the reviewed contract to implement; any later material change requires renewed Gate 1.
