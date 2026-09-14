# DT2 repairs 28 of the 36 first-floor G holdouts

Authored by: Codex (OpenAI), dimensional-lift working session, 2026-09-14. Reviewed by: Claude/Fable (Gate 2, accepted 2026-09-14). Status: exhaustive local evaluation, independently replicated from scratch. Gate 2 accepted 2026-09-14 (Claude/Fable, exact head a641df751bc81b50947b8ea7bd1c4d9d2ae8203f, PR #233). Protocol review: none at freeze; run authorized by Myk 2026-09-14. This note records the completed DT2 cycle before the subsequent complement repair. The DT2 / temporal-depth hypothesis was supplied by Claude/Fable via Myk; the census domain, implementation and evaluation are this session's. See `experiments/binary_lift_20260914/dt2-bridge-reconciliation.md` for the reconciliation against Fable's supplied (unreproduced) material.

Adding the two-step change field **T2 = S ⊕ E²S** alongside Q gives faithful native evolution and local recovery for all 36 previously unresolved source rules, with original G for 23 and centered G for 28. Retaining earlier constructions raises known first-floor coverage to **256 faithful / 156 original G / 248 centered G**. These are unions over available recipes, not a single fixed recipe or a new DT2 census over all 256 rules.

| Family, tested on the 36 holdouts | Recipes | Native alone | Native + recovery | + original G | + centered G |
|---|---:|---:|---:|---:|---:|
| P, D, T2, M | 1,728 | 36 | 29 | 8 | 18 |
| P, D, T2, M, Q | 27,648 | 36 | 36 | 23 | 28 |
| New-family union | 29,376 | 36 | 36 | 23 | 28 |

Each G column requires native evolution and recovery in the same recipe. Different columns may select different recipes. First-floor parent recovery is the source-recovery gate.

| Cumulative first-floor coverage | Before | After |
|---|---:|---:|
| Faithful native evolution + recovery | 256 | 256 |
| Also original G on P/D | 133 | 156 |
| Also centered G on P/D | 220 | 248 |

## Construction and exact contract

The source derivative is primitive:

\[
D_r(S)_i=\operatorname{bit}_{4S_{i-1}+2S_i+S_{i+1}}(r\mathbin{\oplus}204),
\qquad E_r(S)=S\oplus D_r(S).
\]

The fields are

\[
P_s(S)_i=S_i\oplus S_{i+s},\qquad D(S)=D_r(S),\qquad
T_2(S)=D_r(S)\oplus D_r(E_rS)=S\oplus E_r^2S.
\]

Here s is −1 or +1. The mask M ranges over birth `(1−S)D`, death `SD`, stay-one `S(1−D)`, and stay-zero `(1−S)(1−D)`. Q ranges over the existing reflection-closed formulas:

\[
S_{i-2}S_{i+1},\quad S_{i-1}S_{i+2},\quad
S_{i-2}(1-S_{i+1}),\quad(1-S_{i-1})S_{i+2}.
\]

For an ordering π of the four or five fields, the encoding L repeats those rows transversely: `L(S)[i,y] = field_π[y mod p](S)[i]`. All cyclic orders are tested with P fixed first: six at period four, twenty-four at period five.

A single binary derivative table h on 5×5 neighborhoods must satisfy native evolution `H(L(S)) = L(E_r S)`, with `H(X)=X⊕h(X)`. One phase-free decoder must recover S_i at every row position. No row labels are inputs to either table.

The source commutator is

\[
G_r(S)=D_r(E_rS)\oplus D_r(S)\oplus D_r(D_rS).
\]

The carrier c applies P_s to a field on the P row and copies the field on the D row. It is unspecified on T2, M, and Q. With `U=L(S)⊕L(E_rS)`, the original-G constraint is

\[
h(U)=L(S)\oplus L(E_r^2S)\oplus c(G_r(S))
\quad\text{on P/D only}.
\]

The centered test separately requires `G_H(L(S))⊕h(0)=c(G_r(S)⊕E_r(0))`. Both choices of the shared bit `h(0)` are tested, including consistency with every native constraint. This adds the source zero-background correction on D and the native zero correction on both carrier rows. No free native outputs are silently completed with zeros. The implementation selects carrier fields by exact IDs P=0 and D=1, so T2 is never mistaken for a D carrier.

## What was learned

The new original-G carriers are:

`30, 35, 43, 49, 59, 86, 104, 106, 113, 115, 120, 136, 152, 168, 188, 192, 194, 224, 230, 234, 238, 248, 252`.

Centered G additionally repairs:

`135, 149, 151, 169, 225`.

The remaining eight rules are **171, 187, 233, 235, 241, 243, 249, 251**. All are odd, and all have faithful five-field recipes. Every tested recipe fails both original G and both centered branches when the full native/recovery/carrier contract is imposed.

T2 and Q contribute complementary information. Removing Q leaves seven of these 36 rules without recovery and reduces G coverage from 28 to 18. Thus storing T2 alone is not sufficient for the full contract. This supports the bridge's predicted cumulative 248-rule coverage, while leaving its reported 245-rule DT2-family census unreproduced: this run only tests our actual 36 holdouts.

The useful mechanism is visible directly in the probe:

\[
U_D=T_2(S),\qquad U_{T_2}=T_2(S)\oplus T_2(E_rS)
=D_r(S)\oplus D_r(E_r^2S).
\]

The new row exposes a temporal difference that the G demand uses. However, T2 is itself a spatial Boolean function of source radius two for a radius-one ECA. These results do not prove that every spatial-reference repair fails, or that storing T2 is necessary and sufficient for every possible lift.

For the remaining eight, the saved first centered contradictions cover 4,716 faithful recipes and both zero branches. Of these 9,432 certificates, 9,422 are native/probe collisions and ten are P-probe/D-probe collisions. This classifies the first recorded conflicting key for each branch; it does not rule out additional collision types at other keys. It points toward native/probe compatibility as the next question, rather than automatically adding temporal depth.

## Exhaustiveness and verification

The primary sparse C++ census evaluates all 29,376 recipes on all 2¹¹ assignments to source coordinates [−5,+5]. Preparation has source radius two; the temporal probe reaches radius three, so a radius-two native patch needs radius five. Only dependency-safe central patches and outputs are used. No old admission filter is inherited. Runtime was 18.86 seconds with two workers; compilation took 1.31 seconds.

A separate Python implementation uses the integrated ECA table on shrinking source windows. It passed:

- Reconstruction of every one of the **80,388 negative certificates**, including identical neighborhoods and opposite required outputs.
- Reflection checks for all **29,376** recipe records.
- Complete gate comparisons on **292** selected records, covering every passing rule/family/mode, every faithful geometry, and each faithful mask/reference/sign combination: **1,460** decisions.
- **2,117,632 direct physical-G cell evaluations** and **5,189,632 native next-cell evaluations** on the selected successful branches.

Verification took 3.89 seconds. This is independent implementation within the author session, with exhaustive checks on the stated selections; it is not a second full census or an independent reviewer sign-off. Earlier controls are retained from saved results, not presented as new DT2 runs.

## Costs, limits, and next questions

The alphabet remains one bit per cell and native locality remains 5×5. T2 replaces Q at period four or augments it at period five. The respective patches contain 20 or 25 distinct prepared bits. Preparation has source radius two, and all rows still contain only information derived from the source line. At subsequent floors, computing `X⊕H²X` may have parent-space preparation radius four even if H has native radius two; that cost cannot be conflated with native locality.

G is constrained only on P/D. Auxiliary probe outputs and unobserved table entries remain free unless another explicit constraint fixes them. No DT2 recursion was run here. The previous best-known 3D G count remains 206; the older 4D baseline remains 113 faithful paths, 105 preserving recursive G. No indefinite induction or independent higher-dimensional information is established.

Ranked next questions:

1. For all eight remaining rules, does complete separation of native, P-probe, and D-probe constraint sets reveal an information ambiguity or a compatibility obstruction? Use the cached recipes; do not infer a full classification from only their first witnesses.
2. Which smallest binary relation separates the resulting opposite-demand neighborhoods while retaining recovery and native evolution? Reject candidates that leave their target witness unchanged.
3. Once a repaired carrier is understood, does DT2 reuse satisfy the full symbolic-parent recursive contract, as distinct from the bridge's three determined lineage types? Resolve that contract before a 4D run.

Unchanged failed recipes are retired. The current result does not justify further radius growth or a dimension climb.

## Reproducibility

The checkpoint includes `ca_lift_lab/audit_dt2_holdouts.cpp`, `run_dt2_holdouts.py`, and `verify_dt2_holdouts.py`; the run directory `ca_lift_lab/runs/dt2_holdouts_36/` contains the frozen protocol, hashed manifest, every recipe and failure certificate, aggregate results, verification, and remaining-witness classification. Rebuild command: `g++ -O3 -std=c++17 audit_dt2_holdouts.cpp -o audit_dt2_holdouts`. The Python runner handles whole-rule checkpoints and refuses changed source when resuming.


Repository evidence: [extension guide](../../experiments/binary_lift_20260914/EXTENSION.md), [canonical accounting](../../results/binary_lift_20260914_extension.json), [all-rule current coverage](../../results/binary_lift_20260914_extension/rule_coverage.csv), and [authorization/deviations](protocols/binary-lift-extension-record-20260914.md). The earlier [four-reference](2026-09-14-binary-lift-family.md) and [3D/4D](2026-09-14-binary-lift-recursion.md) datasets retain their original scopes.
