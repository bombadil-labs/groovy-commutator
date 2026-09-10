# Freeze the second lift around its actual open question

The [bounded protocol](protocols/second-lift-completion-comparison-20260910.md) is now specified after the completed gradient intervention audit. Its [implementation and evaluation](../knowledge/second-lift-completion-comparison.md) remain **planned and unrun**. This note completes the agreed protocol-writing scope of [issue67](https://github.com/bombadil-labs/groovy-commutator/issues/67#issuecomment-5622839866).

## What is already settled

Let B be the Rule32 first correction image, and let H_128 and H_160 be the two radius-one binary-pair laws supplied by extension freedom. Both preserve B and agree on it. The derivative observation A=I XOR H therefore agrees on B, as does every finite observed-future tuple.

The [triangular coordinate theorem](2026-09-09-correction-future-coordinates.md) applies componentwise over GF(2)^2. It supplies an invertible local recoding between the two correction tuples at each fixed depth:

$$
K_h^{H_{160}}=(T_h^{H_{160}})^{-1}T_h^{H_{128}}K_h^{H_{128}}
\quad\hbox{on }B.
$$

Their whole-field fibers, retained whole-field information under any common finite-ensemble prior, and existence of an autonomous whole-field factor consequently agree. At depth one the recoding is (u,v) mapped to (u,v XOR H_128(u) XOR H_160(u)). Literal coordinates and the radius/cost of a cap can differ.

This is an analytic consequence of the existing theorem, agreed before the future cap census. It is not a claim that arbitrary ambient states have the same dynamics under the two completions. The protocol records explicit recoding and inverse-radius bounds rather than assuming a cost-free change of coordinates.

## What will be measured

The fixed matrix comprises both completions, the inherited family and a separately labeled full four-symbol shift, K/O coordinates, correction depths zero through two, and radii zero through two. The family-restricted census enumerates binary source-preimage causal windows; no arbitrary tuple patch is presumed realizable.

The protocol freezes feature/target bounds, encoding and witness order, forced/default cap tables, complete-law radii, independent evaluation, finite fiber diagnostics with explicit priors, and memory/time limits. The largest primary input domain is 2^22 ambient pair words; the largest inherited primary domain is 2^15 binary words. A separate inherited recoding audit uses at most 2^19 source words. These are work estimates, not reported experiments.

A failure through radius two is a budget result. Equal bounded tables do not prove equal literal laws. No orbit, fixed-point, conjugacy-minimization or new spatial-dimension classification is part of this unit. Product-alphabet growth is recorded as a cost.

## Preserve the inspected example as inspected

The [supplied n=8 script](../../exploratory/issue67-completion-recoding/completion_recoding_rule32.py) and [stdout](../../exploratory/issue67-completion-recoding/output.txt) are copied verbatim from [Claude's comment](https://github.com/bombadil-labs/groovy-commutator/issues/67#issuecomment-5622322884). They remain exploratory checks using the same implementation, already reproduced in the signed issue exchange:

| Existing check | Result and denominator |
| --- | --- |
| Family construction | 256 binary source cases, 255 distinct pair fields |
| H_128=H_160 on the family | 256/256 source cases |
| A_0(X) leaves the finite family | 164/256 source cases, also 164 distinct family states |
| Depth-one recoding identity | 256/256 source cases |

Leaving B alone does not prove the completions are evaluated differently. Codex's separately recorded exploratory check finds H_128(u)≠H_160(u), u=A_0(X), for 40 of 256 source cases, first at MSB-first source index 21. Its exact short reproduction is retained [in the signed comment](https://github.com/bombadil-labs/groovy-commutator/issues/67#issuecomment-5622839866). This is prior inspected evidence, not a prediction for the new census.

The thread also reports a sole alternating-pair collision at ring lengths 6,8,10,12. The archived script directly reconstructs the n=8 image; no all-ring or infinite-lattice collision classification is inferred. Under the reported two-state exception the uniform-source conditional entropy is 2/2^n bits, while maximum ambiguity within that exceptional fiber is one bit. Those statements are different.

Run the archive from the repository root:

```sh
python exploratory/issue67-completion-recoding/completion_recoding_rule32.py
```

Archival replay matches the complete original stdout against ca.py blob 38ef0e7cf8c53063e389c4b63c0a1191c16de045. A dedicated replay gate protects the archive. It does not invoke a product-alphabet cap evaluator.

## Execution remains a visible planned task

The [planned experiment](../knowledge/second-lift-completion-comparison.md) is linked from the dimensional Program and this note. Its acceptance checklist requires a pinned implementation before primary evaluation, complete local domains, independent digests and witnesses, the stated recoding controls and a final matrix with resource accounting. The proposal may be closed when this protocol is merged; the experiment stays planned until that separate deliverable is complete.
