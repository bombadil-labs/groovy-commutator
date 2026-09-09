# Long commutator towers are partly robust and partly finite-size

The width-eight commutator-tower census found 67 ECAs with no repeated correction map through level 256. The [fresh-width protocol](protocols/commutator-tower-fresh-widths-20260909.md) froze periodic widths 7, 9, and 10 before evaluation and repeated the same complete 256-level map census on all 256 rules.

The long-tower set changes substantially with ring width:

| Width | No repeat through level 256 |
| ---: | ---: |
| 7 | 70 |
| 8 | 67 |
| 9 | 116 |
| 10 | 117 |

Only

\[
\boxed{52}
\]

rules are right-censored at all four widths. Another 22 are long at exactly three widths, 34 at exactly two, 28 at exactly one, and 120 at none.

Pairwise Jaccard overlap of the long sets ranges only from about `0.51` to `0.74`. The strongest overlap is between widths 9 and 10.

## Familiar controls

- Rule 30 is long at all four widths.
- Rule 106 is long at all four widths.
- Rule 110 is long at all four widths.
- Rule 54 is long at widths 8, 9, and 10 but **not** width 7. At width 7 its tower enters an exact period-eight cycle with `A23=A31`.
- Rule 184, a Class-II starter control, is short at widths 7 and 8 but long at widths 9 and 10.

Thus raw tower nonrecurrence at a fixed horizon is not a stable class discriminator. It is better interpreted as the correction-role budget of a particular finite world.

The strong Class-IV exclusivity hope remains false under this criterion: Rule 30 is robust-long across all four widths, while Rule 54 itself is size-sensitive.

## What survives conceptually

The **tower recurrence itself** remains exact and local in meaning:

\[
A_k(F(S))=F(A_k(S))\oplus A_{k+1}(S).
\]

What fails to be intrinsic is the finite-global question of when the complete map `A_k:X->X` repeats on a periodic ring.

The next operator search should therefore use the tower locally: ask how successive correction rules grow, whether they admit a bounded/compressed representation, and whether a higher spatial dimension can encode the two transport paths plus their residual without enumerating the whole finite state map.
