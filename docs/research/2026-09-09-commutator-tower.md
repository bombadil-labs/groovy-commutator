# The commutator becomes a tower of correction roles

The fanout-role result turns the Groovy commutator from a scalar diagnostic into a constructive object. If

\[
D(S)=S\oplus F(S),
\]

then

\[
G(S)=D(F(S))\oplus F(D(S))
\]

is exactly the correction required to transport the derivative:

\[
D(F(S))=F(D(S))\oplus G(S).
\]

Applying the same idea recursively gives a canonical hierarchy

\[
A_1=D,
\]

\[
A_{k+1}(S)=A_k(F(S))\oplus F(A_k(S)).
\]

Each next level is the correction needed to transport the previous level as though it were an ordinary state.

The [protocol](protocols/commutator-tower-20260909.md) was frozen before evaluation. The [verifier](../../scripts/verify_commutator_tower.py) evaluates every map exactly on the complete eight-cell ECA state space and follows the tower through level 256 with no Wolfram class labels loaded.

## The first exact census

Across all 256 ECAs:

- the known zero-commutator rules terminate immediately at `A2=0` (Rule 204 already has `A1=0`);
- many rules enter short exact cycles;
- **67 rules have no functional repeat through level 256**;
- the 256 rules split into **156 distinct complete tower signatures** under the frozen zero/constant/repeat and first-16 image-size diagnostics.

The 67 right-censored rules are:

`22, 25, 26, 27, 28, 29, 30, 31, 41, 45, 54, 56, 57, 61, 62, 63, 67, 70, 71, 74, 75, 82, 83, 86, 87, 88, 89, 97, 98, 99, 101, 103, 106, 107, 109, 110, 111, 118, 119, 120, 121, 124, 125, 134, 135, 141, 148, 149, 152, 154, 158, 159, 163, 167, 169, 173, 177, 181, 188, 194, 197, 210, 214, 215, 225, 229, 230`.

This is a bounded statement: those towers have at least 256 distinct correction maps on the eight-cell ring. No claim of infinite nonrecurrence follows.

## Why this matters for dimensional lifting

A zero tower level means the correction hierarchy terminates: the previous role can be transported under the source rule with no further residual. A repeated tower means only a finite recurrent vocabulary of correction maps is needed on this finite substrate. A long unrepeated tower means the attempt to treat successive residuals as ordinary state keeps generating new roles.

That is directly relevant to the dimensional-lift problem. A higher-dimensional encoding needs enough represented channels to carry whatever corrections are required to make evolution of the lower roles autonomous. The tower measures the algebraic role budget before we ask how to embed those roles in space.

## Frozen starter-label comparison

Only after the complete structural table was saved were the repository's pre-existing `WOLFRAM_CLASS` starter labels attached. They contain 11 textbook exemplars, not a complete 256-rule classification:

| Class | Labeled controls | No repeat through 256 |
| --- | ---: | ---: |
| I | 2 | 0 |
| II | 4 | 0 |
| III | 3 | 1 |
| IV | 2 | 2 |

The sole long-tower Class-III starter is Rule 30. Both Class-IV starters, Rules 54 and 110, are long-tower rules. Rules 0/250 (I), 4/108/184/232 (II), and 18/126 (the other III controls) all repeat before the horizon.

This **falsifies exact Class-IV exclusivity at this criterion** because Rule 30 is a false positive. It is nevertheless the first class-blind dimensional-role diagnostic in this branch on which both frozen Class-IV exemplars fall on the nontrivial side while no Class-I/II starter does.

The labeled sample is far too small to treat that pattern as a classifier. The protocol's decision boundary therefore applies: test fresh ring sizes before interpreting tower length as intrinsic.

## Next question

Does the long-tower set persist when the finite substrate changes, especially for Rules 30, 54, 106, and 110? If the property is stable across ring widths, characterize the correction hierarchy locally or algebraically. If membership changes substantially with width, tower length is another finite-world representation effect rather than the dimensional closure signal we seek.
