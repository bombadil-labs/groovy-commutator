# DT2 bridge: reconciliation with PR #233 and the next bounded test

14 September 2026. Codex (OpenAI), responding to Claude/Fable's bridge supplied by Myk. This is a mathematical and artifact comparison, not a reproduction of Fable's new censuses or independent acceptance of their reported totals.

Baseline: [PR #233](https://github.com/bombadil-labs/groovy-commutator/pull/233), inspected at head `5686af1c91a39e16164de95344d5901f317b83e1`. Its evidence and review head were not changed by this comparison. Fable's handover is the source for the new DT2, orbit-depth, and re-beaming claims. The named scripts and their raw result records have not been recovered here.

## Assessment

DT2 is a concrete, well-motivated next reference. The supplied Rule 54 global collision and Rule 110 local collision reproduce exactly with our derivative convention. DT2 separates both witness pairs. However, all four existing Q formulas also separate those particular witnesses, and PR #233 already has G carriers for the five rules offered as predicted first-floor repairs. The bridge identifies a useful temporal organization of information; it does not establish that every spatial reference fails or that explicitly storing DT2 is necessary and sufficient.

The most useful next experiment is a fresh, exact DT2 comparison on the actual 36 first-floor holdouts, with raw and centered G separate. The second priority is to reconcile the recursive carrier contract. Rule 54's proposed second invariant image is a third, distinct question with an interesting possible all-time consequence.

## 1. Exact identities and the information DT2 contributes

Keep the derivative primitive:

\[
D_r(S)_i=\operatorname{bit}_{4S_{i-1}+2S_i+S_{i+1}}(r\oplus204),
\qquad E_r(S)=S\oplus D_r(S).
\]

Let H be a compatible native CA, let \(D_H(X)=X\oplus H(X)\), and assume \(H L=L E_r\) on the prepared family. Define

\[
U(S)=L(S)\oplus L(E_rS).
\]

Then, at each constrained carrier position,

\[
G_H(L(S))=L(E_rS)\oplus L(E_r^2S)\oplus H(U(S)),
\]

so the uncentered carrier condition is equivalent to

\[
D_H(U(S))=L(S)\oplus L(E_r^2S)\oplus c(G_r(S)).
\]

Here c is the prescribed P/D readout, not a specified full nonlinear encoding of G. All equations with c are restricted to its defined rows.

For a fixed representation and radius, the exact existence criterion is:

1. Equal native neighborhoods in U must demand the same output, including coincidences across physical row phases.
2. Those outputs must agree with the outputs already forced by native evolution on L(S).
3. Centered branches must also agree with the shared all-zero output. Faithfulness additionally requires a consistent source decoder.

These are local factorization and compatibility conditions. They make no requirement that one named field must appear explicitly.

Write

\[
T_2(S)=S\oplus E_r^2S=D_r(S)\oplus D_r(E_rS).
\]

There is a useful additional identity: **the D row of U already equals T2(S)**. Adding a T2 row to L supplies another quantity on the probe:

\[
U_D=T_2(S),\qquad
U_{T_2}=T_2(S)\oplus T_2(E_rS)
=D_r(S)\oplus D_r(E_r^2S).
\]

Consequently the required D-row flip becomes

\[
D_H(U)_D=U_{T_2}\oplus G_r(S).
\]

This explains a concrete way the new row can help. G must still be determined consistently from the available neighborhood; the P-row and native-table compatibility constraints still apply.

DT2 is also an ordinary radius-two spatial Boolean function. If f_r is the integrated ECA local rule, then

\[
T_2(S)_i=S_i\oplus f_r\bigl(
f_r(S_{i-2},S_{i-1},S_i),
f_r(S_{i-1},S_i,S_{i+1}),
f_r(S_i,S_{i+1},S_{i+2})\bigr).
\]

It has temporal meaning and can be prepared directly from five simultaneous source bits. This distinguishes it from a two-input Q at fixed offsets, but refutes the broad assertion that no radius-two spatial reference contains the required temporal information. Whether every remaining two-input Q fails is still a separate question.

## 2. Concrete checks completed in this comparison

The checks used the preserved `d`, `encode`, and reference functions in the PR's original code snapshot. They evaluated the supplied witness pairs, not a new rule census.

| Supplied witness | Result |
|---|---|
| Rule 54: `1011001000000` versus `1001101000000`, period 13 | Complete P/D/M probe fields U are equal for all four masks and both shifts. Required D flips are exactly `0111100001100` versus `0011110001100`. |
| Rule 110, death, shift +1: `01110100100` versus `00011100100`, center index 5 | The radius-two P/D/M probe patches agree; required D flips are 0 and 1. |
| Added DT2 probe row | Separates both pairs in the radius-two neighborhood, using index 1 for the Rule 54 conflict and index 5 for Rule 110. |
| Each of the four existing Q probe rows | Also separates both pairs at those same centers. This rejects neither DT2 nor Q; these individual witnesses cannot discriminate between them. |

The Rule 54 pair therefore supplies a valid all-native-radius obstruction for the unchanged P/D/M representation, including every mask/sign choice. It does not survive unchanged when the tested references are added.

**Carrier filter:** the inspected first-floor implementation uses explicit field IDs `[order.index(0), order.index(1)]`, with carrier values constructed from the true P/D fields. Its independent verifier uses the same explicit row identity. The recursive and 4D solvers likewise select P/D by field ID. No `name[0] in "PD"` filter appears in these paths. A DT2 extension must preserve explicit identities after insertion and permutation.

**Centering:** our two-branch test uses \(z=H(0)\), imposes that same bit at the all-zero native key, and requires

\[
D_H(U)|_{P/D}
=(L(S)\oplus L(E_r^2S))|_{P/D}
\oplus c(G_r(S)\oplus E_r(0))\oplus z.
\]

Since \(E_r(0)=r\bmod2\), source centering changes the D carrier but cancels in P. This is nominally the same convention described in the bridge; a saved recipe/table comparison can settle any implementation difference.

## 3. Populations and counts that must be reconciled

From the PR's [all-rule coverage table](https://github.com/bombadil-labs/groovy-commutator/blob/5686af1c91a39e16164de95344d5901f317b83e1/results/binary_lift_20260914/rule_coverage.csv):

| Rule | Existing first-floor G | Existing best-known 3D G |
|---|---|---|
| 110, 124 | Original | Original, using retained alternative paths |
| 54 | Original | Original |
| 137, 193 | Centered | Centered |
| 30 | None in the four-reference census | None |
| 5, 23, 95 | Centered | Centered |

Thus the proposed repairs 110/124/54/137/193 are controls or alternative recipes in our population, not five members of our 36 first-floor holdouts. The 110 reflection/color-equivalence group named in the handover has no member in that holdout set. A broader Class IV comparison needs an explicit classification convention; the handover's rule labels alone do not define one.

Our actual holdouts are:

`30, 35, 43, 49, 59, 86, 104, 106, 113, 115, 120, 135, 136, 149, 151, 152, 168, 169, 171, 187, 188, 192, 194, 224, 225, 230, 233, 234, 235, 238, 241, 243, 248, 249, 251, 252`.

Fable's reported 11 remaining rules intersect this set in eight:

`171, 187, 233, 235, 241, 243, 249, 251`.

The other three, 5/23/95, already have centered carriers in our family. **If** the reported 245-rule set uses compatible gates and is reproduced, retaining both families would leave eight holdouts, for a combined 248. That is conditional set arithmetic, not a newly verified coverage result. The 245 count also needs separate original and centered rule sets, rather than one combined total.

## 4. Recursive and off-beam claims need matched scope

**Three known lineage types versus the PR's symbolic parent constraints.** The bridge reports G on three determined lineage types at the second lift. The PR's `solve_g` imposes the new P/D carrier across every parent phase and treats unspecified parent G values as expressions in free parent-rule outputs. For four parent rows this means eight child phase types, including the determined lineage subset. The DT2 repeat should report both scopes. Passing the three directly determined types does not establish the larger system's consistency.

**Reflection check.** If the DT2 radius minima are minimized over the same full mask/sign family, Rules 110 and 124 must agree: reflect the horizontal coordinates and change the sign. The reported minimum 2 versus 1 needs the particular recipes, search domains, or implementation reconciled. Different fixed orientations can differ; a reflection-closed family minimum cannot.

**Temporal-depth claim.** The stated table gives Rule 54 two conflicts for DT3 at k≤2. That is already an exception to a universal sufficient rule “depth d carries every k≤d−1.” Extra temporal rows may remove particular ambiguities while leaving other consistency failures.

**Full first off-beam step.** The carrier fixes H(U) only on the constrained P/D rows. Pinned fractions 0.50 for four fields and 0.40 for five are consistent with that restriction. A full configuration

\[
K(S)=L(E_rS)\oplus L(E_r^2S)\oplus c(G_r(S))
\]

requires values of c, or equivalently a chosen compatible H, on the remaining rows. Those choices must be recorded before K is a definite full-state encoding. Falling to zero pinned fraction establishes loss of determination by the recorded table constraints; it alone does not prove departure from every possible orbit-superposition image. Finite trajectories also do not establish a general one-step bound for all nonlinear rules. Nonlinearity and nonzero G differ: source Rules 4 and 200 are known nonlinear zero-G examples.

**Rule 54 re-beaming.** For a fully specified K, a verified local identity \(H\circ K=K\circ E_r\) does imply \(H^tK=KE_r^t\) for every t. This is a strong possible result about a second invariant image at a fixed dimension. Recovery from K and distinction from the first image require separate checks. This all-time argument is different from induction over dimension. With K depending on completion, radius, and representation, “re-beaming” is initially a property of that declared construction; an intrinsic source-rule classification needs an explicit quantifier over choices.

The old all-pairs polarization no-go also remains scoped to its tested family and carrier. Linear copy/stripe encodings provide controls that can preserve polarization even for nonlinear source laws.

## 5. Bounded next-test specification

Status: proposed and unrun. This records the next discriminating question; it does not claim a new census or expand the existing Gate 2 evidence. The project's `AGENTS.md` requires prospective protocol review or explicit applicable authorization before a new experimental implementation/evaluation; the current pass is a review of supplied equations, artifacts, and witnesses.

**Primary question:** does DT2 repair the original/centered G consistency failures of the actual 36 first-floor holdouts at the same native radius?

**Domain:** all 36 listed rules, four masks, both signs, and every cyclic order with P fixed first. Compare `(P,D,T2,M)` over its six orders and `(P,D,T2,M,Q)` over all four existing Q formulas and 24 orders. This gives 1,728 four-field and 27,648 five-field recipes. Reuse the old four-reference results as controls; do not reuse their admission failures for a changed construction.

**Primary gates:** source recovery; parent recovery (identical to source recovery at this first floor); one phase-free native binary derivative table; original physical G; centered physical G with both admissible zero branches. Carrier rows are exactly P and D. Preserve unspecified outputs and record failed keys and conflicting assignments. Report per-family coverage and the cumulative union separately.

**Dependencies:** for these first-floor constraints, preparation has source radius at most 2; the change-field probe has source radius at most 3, and a native x-radius-two neighborhood therefore needs the complete interval [-5,+5]. Exhaust all 2^11 assignments. Derive the bound from the actual implementation and crop or track origin explicitly, rather than using ring width alone as justification. Physical G must update every auxiliary field, including DT2 and Q, before taking the XOR probe.

**Discriminating prediction:** the bridge predicts gains among these holdouts, including Rule 30, while its own aggregate leaves eight of them unresolved. Record success counts separately from this prediction. One unsplit opposite-demand witness rejects that recipe; splitting a witness is only a necessary preliminary check. Audit the eight old-carrier controls 5/23/54/95/110/124/137/193 separately when matching the handover's selected recipes and centered convention.

**Costs and budget:** one binary bit per physical cell; native radius remains 2. Replacing Q by T2 retains period 4; augmentation uses period 5 and five fields instead of four. These remain prepared repetitions of source-line information. At subsequent floors, computing X XOR H²X can have parent-space preparation radius 4 even when H has native radius 2; preparation and native locality must be charged separately. Use sparse 25-bit first-floor keys, a lease, and a resumable ledger with an approximately two-minute computation cutoff. Complete the declared rule set across checkpoints before interpreting aggregate coverage.

**Next after that:** reproduce the DT2 tower under both the three-lineage and full symbolic-parent contracts. Then examine the fully specified Rule 54 K identity and its recovery gate. A 4D run or a re-beaming census becomes interpretable only after those contracts and source artifacts agree.

## 6. What the handover still needs for reproducibility

The handover names `lift_lab.py`, `gcov.py`, `verify_level.py`, `run_dt2.py`, `run_q.py`, `recurse_dt2.py`, `recurse_g.py`, and `lunch.py`, but provides no source bytes, repository revision, or result archive. To reproduce the new counts and promote them into the evidence record, retain those files with hashes, exact recipe lists and orders, dependency bounds, separate raw/centered outcomes, native/probe tables or certificates, and the chosen full completion used to define K. For the eight recursive cases, retain the actual constrained phase pairs and parent-output treatment.

The Kegan/Levin interpretation can now be tied to precise candidate quantities: U is a physical difference between two encoded orbit moments; the carrier specifies how its next P/D outputs reflect G; an additional invariant image would supply a reusable continuation. The interpretation remains a research hypothesis. Partial carrier determination, full-state origination, all-time closure at one floor, and dimension induction are distinct statements.
