# The commuting square generates a ternary dimensional lift

The dimensional-lift search now has a rule-independent algebraic candidate that does not begin by choosing a favored spatial encoding.

For fixed evolution `F` and any configuration transformation `A`, define

\[
L(A)=A\circ F,\qquad R(A)=F\circ A,
\]

and their residual

\[
C(A)=L(A)\oplus R(A).
\]

These are the two paths around a commuting square and the exact discrepancy between them. Starting from the discrete derivative

\[
A_\epsilon=D=I\oplus F,
\]

a ternary word `w` in `{L,R,C}^d` names one descendant transformation `A_w`.

The [protocol](protocols/ternary-commutator-lift-20260909.md) freezes this operator and evaluates all descendants through depth six on the complete width-eight state space of all 256 ECAs, with no Wolfram class labels loaded.

## One new dimension is one commuting square

Appending a ternary digit to an existing semantic coordinate gives

\[
A_{wL}(S)=A_w(F(S)),
\]

\[
A_{wR}(S)=F(A_w(S)),
\]

\[
A_{wC}(S)=A_{wL}(S)\oplus A_{wR}(S).
\]

So the new coordinate literally distinguishes the two composition paths and their residual. The all-`C` ray is exactly the previously measured commutator tower.

This is why the construction naturally suggested a `3^d` side-three spatial block: every semantic coordinate sprouts `L`, `R`, and `C` children.

## The nominal ternary cube has a universal quotient

The labeled tree contains `3^d` words at depth `d`, but two identities hold for **every** `A` and **every** update `F`:

\[
L(R(A))=R(L(A)),
\]

because both sides are `F o A o F`, and

\[
L(C(A))=C(L(A)).
\]

The second identity follows because precomposition by `F` distributes over XOR.

Thus `L` commutes past both `R` and `C`. Every labeled ternary word has a canonical representative

\[
L^k w,\qquad w\in\{R,C\}^{d-k}.
\]

The number of possible canonical roles at exact depth `d` is therefore at most

\[
\sum_{m=0}^d 2^m = 2^{d+1}-1.
\]

The universal ceiling through depth six is

\[
1,3,7,15,31,63,127.
\]

This quotient is forced before the source rule is inspected. Further identifications below it are genuinely rule-dependent on the declared finite substrate.

## Exact depth-six census

Exactly **107 of 256** ECAs attain the universal ceiling at every depth through six. Their semantic role vocabulary therefore expands as fast as this algebra permits within the tested horizon.

At the other end, **33 of 256** rules generate a cumulative descendant vocabulary that becomes exactly closed under all three operations `L`, `R`, and `C` by depth six.

The first closure depths are:

| First closed depth | Rules |
| ---: | ---: |
| 0 | 1 |
| 1 | 9 |
| 2 | 5 |
| 3 | 10 |
| 4 | 4 |
| 5 | 2 |
| 6 | 2 |
| not closed by 6 | 223 |

The 33 bounded-closure rules are:

`0, 1, 4, 8, 12, 19, 23, 32, 36, 51, 55, 64, 68, 72, 76, 90, 105, 128, 132, 136, 150, 165, 192, 200, 204, 219, 223, 232, 236, 239, 251, 253, 255`.

The all-`C` branch is checked directly against the original commutator-tower recurrence at every evaluated depth.

## What this says about the lift problem

The construction separates two questions that previous experiments mixed together.

First, **dimension raising has a canonical semantic operation**: expose the two orderings of `A` and `F` plus their residual. No Class-IV label or arbitrary table placement is required to define that operation.

Second, a finite-dimensional autonomous realization requires a **quotient of the descendant vocabulary**. If all children of all represented roles are already identified with roles in a finite set, the semantic system is closed. If genuinely new descendants continue to appear, the representation asks for more role coordinates.

The observed width-eight closure table is not yet a theorem about infinite ECAs. It is an exact finite-substrate result. Nor does a closed semantic vocabulary yet prove that it embeds as a local higher-dimensional CA state.

The next step is to inspect the quotient graphs of the 33 closed rules and, separately, the maximally expanding 107-rule family. The important spatial question is whether the universal `L/R/C` semantics can be represented by a fixed local geometry whose symmetry quotient matches these algebraic identifications rather than by a decoder fitted per rule.
