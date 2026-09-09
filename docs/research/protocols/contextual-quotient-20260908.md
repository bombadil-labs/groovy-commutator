# Protocol: contextual quotient and fatal predictive synergy — 2026-09-08

**Status:** frozen after Research028 and before the new quotient/safety-margin census.  
**Branch:** `research/fatal-predictive-synergy-20260908`.  
**Dependency:** Research028 on `main`.

## Motivation

Research028 found an unusual combination:

- local diminishing returns fails in about 79% of comparable block-3 split comparisons;
- nevertheless greedy fixed-target Shannon repair reaches the globally minimum-information local repair in 30,852 of 30,856 nonclosed cases;
- the four failures form the Rule-24/231 conjugacy family;
- the first failure requires a zero-immediate-gain bridge that amplifies a later distinction's predictive value by about 13.26x.

The next task is theoretical rather than a larger brute-force search:

> **Construct the globally optimal local sufficient representation directly from future-context equivalence, and characterize greedy failure as leaving that canonical quotient.**

## General finite setup

Let `A` be a finite local fine-state alphabet and consider `m` tiled local blocks, so the finite global microstate space is

\[
X=A^m.
\]

Let

\[
C:X\to Q
\]

be any deterministic target label. In the Groovy application, `C=C_infinity^T` is the complete future-equivalence class of a fixed target observation `T`.

A uniform local encoder is a map

\[
z:A\to Z
\]

applied independently in every block. It is **sufficient for C** when there exists a function `b` with

\[
C=b\circ z^m.
\]

Equivalently, the global encoder partition `z^m` refines the partition induced by `C`.

## Future-context equivalence

Define a relation on local fine symbols:

\[
a\equiv_C b
\]

iff for every block position `j` and every exact assignment of the other `m-1` local blocks,

\[
C(x_1,\ldots,x_{j-1},a,x_{j+1},\ldots,x_m)
=
C(x_1,\ldots,x_{j-1},b,x_{j+1},\ldots,x_m).
\]

Call the quotient

\[
N(C)=A/{\equiv_C}
\]

the **future-context quotient**.

This is intentionally named rather than claimed as novel mathematics. Context equivalence yielding a minimal quotient is structurally analogous to Myhill–Nerode / syntactic congruence constructions, where two objects are equivalent when all contexts give the same observable outcome.

## Theorem target: canonical local sufficient quotient

Prove directly:

### Theorem 1 — sufficiency

`C` factors through the blockwise future-context quotient:

\[
C=\bar C\circ N(C)^m.
\]

Proof strategy: transform any two block tuples with coordinatewise equivalent symbols one coordinate at a time; each substitution preserves `C` by definition.

### Theorem 2 — coarsest local sufficiency

For any local encoder `z` sufficient for `C`,

\[
\ker z\subseteq\equiv_C.
\]

Proof strategy: if `z(a)=z(b)`, place `a` and `b` in one coordinate with an otherwise identical exact context. Sufficiency of `z^m` forces the two `C` values to agree for every coordinate and context.

Therefore `N(C)` is the unique coarsest sufficient uniform local partition.

### Corollary — information optimum

Under the uniform full-support ensemble on `A^m`, every strict refinement of a local partition strictly increases encoder entropy. Hence `N(C)` is the unique minimum-entropy sufficient local encoder.

For independent uniform blocks,

\[
H(z^m(S))=mH(z(U_A)),
\]

so the result can be read locally or globally.

## Greedy path characterization

Let `Q*=N(C)` be the canonical quotient and let `P` be a current local partition on a refinement path from target `T`.

Call `P` **Q-compatible** when `Q*` refines `P`: every current class is a union of canonical quotient classes.

A refinement cover `P -> P'` is **safe** when `P'` remains Q-compatible. It is **unsafe** when it splits at least one canonical `Q*` class.

Prove:

### Theorem 3 — exact greedy-failure criterion

For any monotone refinement-only repair path starting from a Q-compatible target:

- if every chosen cover remains safe until the path first reaches exact sufficiency, the terminal partition equals `Q*` and is globally minimum-information;
- once a path takes an unsafe cover, every later partition is a strict refinement of `Q*`, so under the uniform full-support ensemble the path cannot terminate at a global information optimum.

Thus greedy global failure is equivalent to the greedy path taking its first unsafe split.

## Safety margin

At a Q-compatible nonclosed encoder `P`, partition all available refinement covers into safe and unsafe sets.

For each cover use the frozen Research027/028 gain

\[
g(P\to P')=\frac{W_T(P)-W_T(P')}{H(P')-H(P)}.
\]

Define the **greedy safety margin**

\[
M(P)=\max_{P'\in\mathrm{safe}}g(P\to P')-\max_{P'\in\mathrm{unsafe}}g(P\to P').
\]

If no unsafe cover exists, set the unsafe maximum to `-infinity`. Respect canonical tie-breaking when gains agree within the existing tolerance; record separately whether a zero numerical margin would choose safe or unsafe.

A negative margin means an unsafe split strictly outranks every safe split and ordinary greedy must leave the canonical quotient. A positive margin means the best immediate split is safe.

## Exact block-3 census

Reuse the Research028 finite system without re-enumerating every target interval globally:

- all 256 ECA rules;
- periodic `n=12`;
- block size 3, cadence `q=3`;
- all 127 canonical nonconstant binary targets;
- complete stable target future class `C_infinity^T`.

For each target:

1. construct `Q*=N(C_infinity^T)` directly from local context signatures;
2. verify exact sufficiency of `Q*`;
3. run the frozen greedy gain rule using only covers encountered on its path;
4. classify every encountered cover as safe/unsafe relative to `Q*`;
5. record safety margins until closure or first unsafe step.

Controls:

- the future-context quotient refines the initial target;
- its encoder is exactly closed;
- for the four Research028 failure cases, its partition and entropy reproduce the stored global optimum;
- the quotient/greedy safety criterion identifies exactly the same four failures as Research028;
- for a stratified audit sample of previously successful cases, the quotient entropy reproduces the Research028 global minimum when the old exact interval search is rerun.

## Primary descriptive summaries

Across the 30,856 nonclosed block-3 target cases report:

- count/fraction of greedy paths that ever take an unsafe split;
- distribution of minimum safety margin along successful paths;
- safety margin at the first unsafe step in failures;
- number of successful cases with a diminishing-return violation but no unsafe greedy choice;
- number of successful paths with near-zero safety margin (`|M| < 1e-6`, `1e-4`, `1e-2`), to distinguish robust success from accidental near-ties;
- balance- and Wolfram-class summaries as exploratory diagnostics.

Do not redefine fatal synergy from the empirical margin distribution after inspection.

## Rule-24 worked theorem

For Rule 24 / target `01000010`, independently compute the local three-block one-macrostep target function

\[
g:A^3\to\{0,1\}
\]

obtained by applying Rule 24 for three fine steps and then the target map to the middle three-cell block.

Because Research028 finds target future depth `h*=1` at `n=12` and `n=15`, compare the local contextual-equivalence classes induced by `g` with the global future-context quotient.

Frozen calculation to verify:

\[
\{0,4\},\{1\},\{2,5\},\{3,7\},\{6\}
\]

which corresponds to encoder `01230243`, the exact Research028 global optimum.

Treat equality of this local quotient with the global quotient as a worked mechanism result, not an all-size theorem unless a separate proof of future-depth closure is supplied.

## Literature boundary

The Program may relate the future-context quotient to Myhill–Nerode / syntactic congruence by analogy and cite context-based minimal quotients. Do not claim the general context-equivalence theorem is novel without a dedicated literature review.

Likewise, mutual-information feature-selection and rough-set reduct literatures contain minimum sufficient/reduct problems and known synergy failures of greedy criteria. The Groovy contribution being tested here is the specific dynamical future-equivalence target, uniform local-partition constraint, canonical quotient construction, and exact fatal-synergy geometry.

## Scope

- Finite deterministic target `C` and uniform local encoders only.
- Entropy-optimality uses the uniform full-support ensemble for strictness; the coarsest-partition theorem itself is measure-free.
- The direct quotient requires access to the full finite target function `C`; it is not yet a scalable learning algorithm.
- The safety-margin theorem explains greedy correctness *given* `Q*`; the harder algorithmic problem is recognizing safe directions without first constructing the full quotient.

## Decision boundary

If the theorems and exact census validate, the next question is algorithmic:

> **Can local contextual signatures or low-order interaction tests predict Q-safe splits without constructing the full future-context quotient?**

That is the route from an exact finite theory toward a scalable representation-learning rule.