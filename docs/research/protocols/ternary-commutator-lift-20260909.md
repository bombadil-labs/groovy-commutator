# Protocol: the ternary commutator lift

Date: 2026-09-09
Status: preregistered before evaluation

## Candidate lift operator

For a fixed deterministic evolution `F` and any configuration transformation `A`, define three descendants:

\[
L_F(A)=A\circ F,
\]

\[
R_F(A)=F\circ A,
\]

\[
C_F(A)=L_F(A)\oplus R_F(A).
\]

`L` and `R` are the two paths around the commuting square; `C` is their XOR residual.

Start from the outgoing derivative

\[
A_\epsilon=D=I\oplus F.
\]

For a word

\[
w\in\{L,R,C\}^d,
\]

define `A_w` by applying the corresponding descendant operators successively.

There are exactly

\[
3^d
\]

words of length `d`. This is the same cardinality and ternary address space as a side-three `d`-dimensional Moore block.

## Exact lift identity

For any source state `S`, define the semantic block `J_d(S)` by evaluating every `A_w(S)` for words of length `d`.

Appending one new ternary coordinate gives, for each parent word `w`:

\[
A_{wL}(S)=A_w(F(S)),
\]

\[
A_{wR}(S)=F(A_w(S)),
\]

\[
A_{wC}(S)=A_{wL}(S)\oplus A_{wR}(S).
\]

Thus the added dimension literally stores the two composition paths and their commutator residual. The all-`C` branch reproduces the previously frozen commutator tower.

This identity is algebraic and rule-independent; the census below measures when the generated role vocabulary compresses on the finite ECA substrate.

## Frozen finite substrate

Use the complete eight-cell periodic ECA state space and standard truth-table mapping.

Evaluate all 256 source rules with no Wolfram class labels loaded.

## Frozen tree depth

Enumerate every ternary word through depth six:

\[
d=0,1,2,3,4,5,6.
\]

Depth six contains 729 labeled leaves and 1,093 labeled nodes cumulatively. The depth is fixed before outcomes.

For each source rule, each descendant is represented by its complete function table on all 256 states, so equality is exact.

## Primary outputs

For every source rule record:

1. number of **distinct descendant maps at each exact depth**;
2. cumulative number of distinct maps through each depth;
3. number of new maps first appearing at each depth;
4. first depth at which no new map appears, if any;
5. whether the generated set is already **closed under all three descendants** `L,R,C` within the explored vocabulary;
6. multiplicity histogram: how many labeled ternary words collapse onto each distinct map;
7. whether the all-`C` branch agrees with the previously frozen commutator tower through level seven.

A source has **finite ternary role closure within depth six** only if some cumulative vocabulary through depth `d<=6` is closed under all three descendant operations, not merely if one level happens to add no new labeled leaf.

## Structural interpretation

The ternary lift is not yet a native higher-dimensional CA rule. It is a canonical rule-independent semantic lift whose coordinates already match the project's ternary spatial-address syntax.

A finite closed descendant vocabulary is a necessary algebraic ingredient for a bounded-dimensional autonomous realization: every composition path and residual required by evolution is already represented by one of finitely many roles.

Continued growth means the declared representation keeps requesting genuinely new correction roles.

## Anti-overfitting

- The `L/R/C` semantics are derived from the commuting square, not selected from rule outcomes.
- Depth six is frozen before evaluation.
- No rule-specific quotient, tolerance, role merge, or spatialization is fitted.
- No class labels are loaded until the full structural table is saved.

## Decision boundary

If a small source subset has finite ternary role closure, characterize the exact quotient graph and then ask whether that graph embeds into a bounded higher-dimensional local geometry.

If most rules close quickly, the lift is algebraically universal and not selective.

If many rules continue growing, compare growth signatures and fresh ring widths before interpreting them. The downstream Class-IV conjecture is tested only after the role-growth table is frozen.