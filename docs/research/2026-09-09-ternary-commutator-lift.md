# The commuting square grows a ternary spatial address

The dimensional-lift search asked for a rule-independent operator rather than a favorable encoding chosen per source rule. The commutator-role work now supplies one exact semantic candidate.

For a fixed deterministic evolution `F` and a configuration transformation `A`, define

\[
L_F(A)=A\circ F,
\]

\[
R_F(A)=F\circ A,
\]

and

\[
C_F(A)=L_F(A)\oplus R_F(A).
\]

Start from the outgoing derivative

\[
A_\epsilon=D=I\oplus F.
\]

For every word `w` over the alphabet `{L,R,C}`, let `A_w` be the corresponding descendant. A word of length `d` is naturally a ternary coordinate in a side-three `d`-dimensional block.

The [protocol](protocols/ternary-commutator-lift-20260909.md) froze this construction and depth six before evaluation. The [verifier](../../scripts/verify_ternary_commutator_lift.py) evaluates complete function tables on all 256 states of the eight-cell ECA substrate with no Wolfram class labels loaded. The committed summary records the full-result SHA-256 so the structural table is fixed before label comparison.

## The exact lift identity

Define the semantic block

\[
J_d(S)_w=A_w(S),\qquad w\in\{L,R,C\}^d.
\]

Appending one ternary coordinate gives three slabs:

\[
J_{d+1}^{L}(S)=J_d(F(S)),
\]

\[
J_{d+1}^{R}(S)=F^{\parallel}(J_d(S)),
\]

\[
J_{d+1}^{C}(S)=J_{d+1}^{L}(S)\oplus J_{d+1}^{R}(S),
\]

where `F^parallel` applies the original one-dimensional rule independently to each represented role pattern.

The added dimension therefore stores exactly the two paths around the commuting square and their residual. The all-`C` line is the previously studied commutator tower.

This identity is algebraic and applies to every deterministic rule. It is already a dimension-uniform semantic lift. What remains open is whether its semantic block can evolve autonomously under a native bounded higher-dimensional CA rule.

## The nominal 3^d tree has a forced quotient

A post-evaluation deduction explains a striking regularity in the census. Composition is associative, so

\[
L_FR_F=R_FL_F.
\]

Also, `L` distributes through XOR, giving

\[
L_FC_F=C_FL_F.
\]

Thus every ternary word can be rewritten with all `L` symbols moved through the `R/C` suffix. At exact depth `d` there are therefore at most

\[
\sum_{j=0}^{d}2^j=2^{d+1}-1
\]

semantically distinct descendant maps, despite the `3^d` labeled ternary addresses.

The frozen census respects this bound at every rule and depth. **107 of 256 ECAs saturate it at every tested depth**, with the exact sequence

\[
1,3,7,15,31,63,127.
\]

So the ternary spatial address contains forced redundancy. That redundancy is not a defect in the operator; it is an algebraic quotient induced by the commuting square itself.

## Finite role closure through depth six

A cumulative role vocabulary counts as closed only if applying `L`, `R`, or `C` to every represented map stays inside the vocabulary.

Across all 256 ECAs:

- **33** reach exact finite ternary-role closure by depth six;
- **223** do not;
- closure depths are `0:1`, `1:9`, `2:5`, `3:10`, `4:4`, `5:2`, `6:2`;
- **225** rules are still adding new maps at depth six;
- the all-`C` branch agrees with the previously frozen commutator tower throughout the tested depth for every rule.

This is not a claim that the 223 nonclosed sources have infinite role vocabularies. Depth six is the frozen boundary.

## Frozen starter-label comparison

Only after the structural table and its hash were fixed were the repository's existing textbook starter labels consulted.

| Class | Rule | Closure through depth 6 | Exact-depth role counts |
| --- | ---: | --- | --- |
| I | 0 | depth 1 | `1,1,1,1,1,1,1` |
| I | 250 | no | `1,3,7,15,28,45,75` |
| II | 4 | depth 1 | `1,1,1,1,1,1,1` |
| II | 108 | no | `1,3,7,15,29,52,73` |
| II | 184 | no | `1,3,7,15,31,63,127` |
| II | 232 | depth 4 | `1,3,7,11,11,11,11` |
| III | 18 | no | `1,3,7,14,26,42,72` |
| III | 30 | no | `1,3,7,15,31,63,127` |
| III | 126 | no | `1,3,7,14,26,47,78` |
| IV | 54 | no | `1,3,7,15,31,63,127` |
| IV | 110 | no | `1,3,7,15,31,63,127` |

Both Class-IV starters exhibit maximal semantic growth, but so do Rule 30 and Class-II Rule 184, along with many unlabeled rules. Finite closure and maximal depth-six growth therefore both fail as exact Class-IV discriminators.

That negative classification result does not weaken the operator result: the `L/R/C` lift was derived without labels and survives unchanged.

## What the operator changes

The original derivative-completed proposal suggested that a new dimension might carry rule, state, and change. The ternary commutator lift supplies a more canonical recursion: every new dimension carries **left path, right path, residual**.

It also explains why a fixed-dimensional autonomous realization is the hard part. To advance `J_d(S)` one step, its required future is literally the `L` slab of `J_{d+1}(S)`. Unless the role vocabulary closes or can be compressed, indefinite evolution keeps asking for deeper roles.

So dimension and correction depth become two presentations of the same bookkeeping problem.

## Next question

The protocol's decision boundary now applies. Because most rules continue growing, test the role-growth signatures on fresh periodic widths before interpreting them as intrinsic. More importantly, search for a native spatial realization of the exact slab identity:

> Can a fixed local higher-dimensional CA carry the `L/R/C` block so that projection onto its `L` face reproduces lower-dimensional evolution while the `R` and `C` faces supply the independently evolved role and the correction needed to keep the representation autonomous?

That is now the concrete dimensional-lift problem.