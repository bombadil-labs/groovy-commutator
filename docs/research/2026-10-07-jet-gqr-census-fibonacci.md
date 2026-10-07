# An invariant positive-entropy invisible jet relation in Rule 54

**Date:** 2026-10-07. **Status:** exact finite-graph/full-line symbolic
result, no independent peer review yet. **Author:** GPT-6 (OpenAI).

**Protocols:** [frozen all-256 census and initial invariance gate](protocols/jet-gqr-census-fibonacci-invariance-20261007.md);
[separately frozen post-primary golden-component test](protocols/rule54-two-golden-scc-swap-20261007.md).

**Reproduction:** [runner and verifier](../../experiments/jet_gqr_256/README.md);
[all-256 canonical data](../../results/jet_gqr_256_20261007.json);
[Rule-54 invariance certificate](../../results/rule54_golden_invariance_20261007.json).

## We wondered / tried / found

**We wondered:** Is Rule 54's persistent branching equal-jet ambiguity rare,
and can its Fibonacci-like pair language actually persist indefinitely rather
than merely surviving through the fifth residual?

**We tried:** (1) an exhaustive exact GQR pair-SCC classification on the
full binary source shift for every ECA; (2) an exact full-line inclusion test
of each of Rule 54's three previously discovered branching A5 source-pair
components under H54 x H54; (3) after the initial union test failed, a new
explicitly post-primary test of the two components with golden growth.

**We found:** GQR branching is very common. But **two distinct,
positively entropic Rule-54 equal-jet source-pair subshifts map into one
another under source evolution**. This makes their union forward invariant
and establishes that all higher intrinsic commutator residuals are identical
for every pair in this union. The proof does not require enumerating A6,
A7, or any deeper field.

## Definitions and exact graph contract

For any elementary CA H, define

\[
A_0(S)=D(S)=S\oplus H(S),\qquad
A_{k+1}(S)=A_k(H(S))\oplus H(A_k(S)).
\]

The G-anchored jet prefix is \((A_1,\ldots,A_m)=(G,Q,R,\ldots)\).

For each prefix, its site symbol is a function of a finite source window.
The equal-output **source-pair de Bruijn graph** has source-context pairs as
vertices and a paired edge whenever its two source edges have the same
sitewise jet label. A bi-infinite path is therefore precisely a pair of
whole-line source configurations with identical entire current jet fields.

A recurrent SCC with internal branching presents a positive-spatial-entropy
source-pair language; a simple directed cycle has zero entropy. SCCs are not
automatically probabilistic causal states.

## All 256 elementary rules at G,Q,R

At GQR, the deepest field R has source radius four. Every rule was evaluated
on all 512 source words of length nine. The source-pair graph has at most
65,536 context-pair vertices and 262,144 paired edges.

| Exact category | ECA rules |
| --- | ---: |
| Any branching recurrent component containing off-diagonal source pairs | 228 |
| Mixed (diagonal + off-diagonal) branching recurrent component | 217 |
| Purely off-diagonal branching recurrent component | 80 |
| Pure branching with **no mixed** branching | 11 |
| Only periodic recurrent off-diagonal components | 28 |
| Identically zero uncentered G,Q,R fields | 10 |

The counts overlap where stated: the 80 pure-branching rules are included
among the 228 with any branching. All 256 rules retain at least one
off-diagonal recurrent ambiguity in this contract.

The eleven with a pure branching component but no mixed branching are:

\[
\boxed{\{47,54,56,98,107,117,121,122,123,151,183\}}.
\]

Rule 54 belongs here; Rule 30 and Rule 110 belong to the 28 cycle-only
cases; Rule 62 retains a mixed branching component; additive Rule 90 has an
identically zero higher residual tower.

The criterion is **not** invariant in every standard ECA
reflection/conjugacy orbit: nine of the 88 orbits contain both branching
and cycle-only representatives under the present uncentered G definition.
Do not report orbit-level class statistics without accounting for this.

The original intuition that "branching is a Class-IV property" therefore
fails plainly. The existence of **separate** branching ambiguous-pair
components is less common but still not unique to Rule 54.

## Initial Rule-54 A5 test: every branching component survives one step

The G,Q,R,A4,A5 equal-output graph for Rule 54 has 3,561,416 paired
edges before pruning and three pure off-diagonal recurrent branching SCCs.

| Component | Vertices | Edges | Perron root | Three-edge paths |
| --- | ---: | ---: | ---: | ---: |
| C_plus | 52 | 68 | 1.2720196495 | 110 |
| C_small | 52 | 58 | 1.1278384856 | 74 |
| C_minus | 84 | 110 | 1.2720196495 | 178 |

A pair of three consecutive internal edges contains 15 source bits on
each rail, exactly the causal support needed for one Rule-54 source
update and a complete 13-bit successor jet window.

All **362** admissible internal three-edge paths were checked.
For all three SCCs the evolved pair still had equal G through A5.

However, none was individually invariant. The image of C_small lies in
another SCC outside the three-component union, so the originally frozen
three-component invariance hypothesis fails.

This negative is preserved; it motivated, but does not retrospectively
validate, the next selection.

## Post-primary exact theorem: the golden pair components exchange

We separately froze C_plus (52/68) and C_minus (84/110), the two components
sharing the maximal Perron root. Exact characteristic polynomials are:

\[
\chi_+(z)=z^{44}(z^2-z+1)(z^2+z+1)(z^4-z^2-1),
\]

\[
\chi_-(z)=z^{76}(z^2-z+1)(z^2+z+1)(z^4-z^2-1).
\]

Their shared Perron root is exactly

\[
\rho=\sqrt{\varphi},
\qquad\varphi=\frac{1+\sqrt5}{2}.
\]

Both present genuinely branching positive-entropy paired-source languages:

\[
\boxed{
h(C_+)=h(C_-)=\tfrac12\log_2\varphi
\approx0.347121\text{ bits/site}.
}
\]

**The exact inclusion certificate is:**

- All 110 three-edge paths in C_plus evolve into a paired source edge
  internal to C_minus.
- All 178 three-edge paths in C_minus evolve into an edge internal to
  C_plus.

Both complete path sets were also independently re-evaluated with a
plain scalar temporal CA recurrence, not just the vectorized jet tables.

Consequently, on the full binary line,

\[
\boxed{
(H_{54}\times H_{54})(C_+)\subseteq C_-,
\qquad
(H_{54}\times H_{54})(C_-)\subseteq C_+.
}
\]

This is an exact two-cycle of **inclusions**, not a claim that either
map is invertible or surjective. Set \(C=C_+\cup C_-\). Then
\((H_{54}\times H_{54})(C)\subseteq C\).

### Proof that all higher jets remain equal

By construction, pairs \((X,Y)\in C\) have identical whole-line fields

\[
A_j(X)=A_j(Y),\quad j=1,\ldots,5.
\]

Because C is forward invariant, for every \(t\ge0\),

\[
A_1(H^tX)=A_1(H^tY).
\]

Induct on k. Assume for every t that
\(A_k(H^tX)=A_k(H^tY)\). Then the universal recurrence yields

\[
\begin{aligned}
A_{k+1}(H^tX)
&=A_k(H^{t+1}X)\oplus H(A_k(H^tX))\\
&=A_k(H^{t+1}Y)\oplus H(A_k(H^tY))\\
&=A_{k+1}(H^tY).
\end{aligned}
\]

Thus

\[
\boxed{
\forall (X,Y)\in C,\ \forall k\ge1,\quad A_k(X)=A_k(Y).
}
\]

Since every recurrent component of C is purely off-diagonal, each
such pair consists of genuinely distinct source configurations.

The proof establishes a **positive-entropy invariant source-pair relation
erased by the entire G-anchored commutator tower**. No deeper jet census is
needed.

## What this does not prove

- Not a general all-ECA theorem, or a Class-IV discriminator.
- Not that a *typical* Rule-54 source configuration has positive
  conditional entropy given its jet; these positively entropic paired
  families are exceptional relative to the full one-bit entropy source.
- Not that the source dynamics are conjugate to the golden-mean shift:
  a characteristic factor and growth rate alone are insufficient.
- Not that the two SCCs are exchanged bijectively or that every source
  orbit enters this subsystem.
- Not a special numerical relation to the six-field dimensional lift.

## Verification and next unit

The C++17 256-rule engine and an independent JavaScript SCC implementation
agree on every reported census field (full-table weighted checksum
617287869 modulo 1,000,000,007). Earlier SciPy pair-graph checks independently
agreed for Rules 30, 54, 62 and 110. The Rule-54 A5 checker uses a
separately implemented scalar CA on **every** admissible three-edge path.
Exact SymPy characteristic polynomials confirm the golden Perron root in
both swapping SCCs.

The same-author checks are reproducibility evidence, not independent
peer review. Draft PR #328 is not merged.

A better next question than A6 is:

> Identify a small, explicit source-pair generator for C_plus and C_minus,
> prove the H54 two-cycle directly from its symbolic production rules,
> and determine whether the resulting Fibonacci-like language can be
> related to Rule-54's known ether/defect structure.

That would turn the graph certificate into a conceptual theorem, with
independent peer review as the next credibility gate.
