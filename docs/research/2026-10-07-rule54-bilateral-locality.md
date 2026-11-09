# Rule 54 J5 needs both flanks: exact two-impulse witnesses

**2026-10-07 · Post-exploratory.** Follow-up to [full-line autonomy](2026-10-07-jet-full-line-autonomy.md), PR #329. Same-author independent reproductions, *not* external peer review.

## We wondered / tried / found

**Wondered:** Is the sharp symmetric induced J5 radius six an artifact of a symmetric window, or are six sites necessary on **each** side?

**Tried:** Rebuilt the Rule-54 Boolean jet truth tables from the recurrence, its full-line paired-source graph, and the transient period-eight preimage clock in a separate implementation. Then checked two exact finite-support source pairs in a second pure-Python implementation using no graph, NumPy or periodic boundaries.

**Found:** The independent whole-line graph reproduction agrees exactly: 3,561,416 labeled pair edges, 4,316 essential pair contexts, 8,460 essential edges, 33,162 complete three-edge paths, **zero** A6 disagreements. Symmetric jet radii 1..6 leave **196196, 5428, 334, 98, 12, 0** bad contexts. Of the 12 at radius five, four persist when extending only the left observation flank, four when extending only the right, and four vanish when either flank is extended.

## Short exact proof of bilateral minimality

Let e_j be the bi-infinite, otherwise-zero source with a 1 at site j. Let H be Rule 54 and define A0=I xor H, A(k+1)=A(k)∘H xor H∘A(k); J5=(A1,..,A5).

| Which flank is necessary? | Source X | Source Y | Only current J5 mismatch sites | Central A6 values |
| --- | --- | --- | --- | --- |
| Right | e_{−6} | e_{−6} xor e_{+7} | +6,+8 | 0,1 |
| Left | e_{+6} | e_{−7} xor e_{+6} | −8,−6 | 0,1 |

For each pair A1, A3 and A5 agree **everywhere**. Only A2 and A4 disagree at the two listed sites. Thus in the first example the *entire half-line* of J5 symbols at sites ≤+5 is the same, but A6 at 0 differs. In the second, the *entire half-line* at sites ≥−5 is the same but A6 differs. Every correct induced rectangular jet window [−L,+R] must therefore satisfy **L≥6 and R≥6 separately**. The original graph's upper bound at symmetric radius six makes [−6,+6] coordinatewise minimal. No amount of context on one side can substitute for its missing sixth site on the opposite side.

There is a nonadditive, long-baseline two-impulse contribution to central A6. This is a boundary-information interaction, not evidence of typical compression or a new Wolfram-class discriminator.

## Eight-phase transient preimage clock rechecked

The fresh implementation also reconstructed the independently fixed, post-selected period-eight successor pair (00100111,01110010): **882** local candidate paired edges, **704** vertices, unique recurrent SCC **52v/58e**, SHA-256 of its ordered paired edges **8038efc7d2c33bca3b4ad5fbcc7acaa970feb7924de46c196ccd69418679cb7a**, phase populations **5,8,8,5,5,8,8,5**, eight-step counting quotient **[[1,1],[1,2]]**, and periodic path counts **24,56,144,376** at lengths 8,16,24,32. This is a counting certificate, not topological conjugacy.

Both constructions were independently implemented by the same author from the mathematical definitions, not human peer-reviewed. The entropy corollary and Rule-110 interface obstruction remain separate review questions.

## Reproduce and next gate

Pure Python finite-support witness: docs/research/reproducers/rule54_bilateral_boundary.py

Independent NumPy/SciPy source-pair graph and eight-phase clock: docs/research/reproducers/rule54_joint_independent.py

Next investigate a compact **on-image** symbolic transducer for Rule54 J5; preserve external review boundaries and avoid new census/lift/off-image expansion.
