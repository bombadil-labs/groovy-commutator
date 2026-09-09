# Protocol: can incoming derivative replace the lower center state?

Date: 2026-09-09
Status: preregistered before evaluation

## Motivation

The original layered dimensional lift stores a binary outer-totalistic lower-dimensional rule in the two transverse outer slices of a radius-one higher-dimensional Moore neighborhood. The central slice supplies the lower-dimensional input neighborhood, including its center state.

A new proposal replaces that center state by the **incoming derivative** that produced it:

\[
\delta_t = c_{t-1}\oplus c_t.
\]

The question is whether the lower rule plus the present outer-neighbor state contains enough information to reconstruct the missing current center. If so, the derivative is not merely extra storage: it is a sufficient replacement for the center variable in the dimensional interpreter.

This protocol evaluates that question exactly in the smallest nontrivial control family: one-dimensional binary radius-one outer-totalistic rules. This is a 64-rule family and is intentionally evaluated without Wolfram class labels.

## Frozen lower rule family

A 1D outer-totalistic rule is specified by six bits

\[
r_{c,n},\qquad c\in\{0,1\},\quad n\in\{0,1,2\},
\]

where `c` is the current center and `n` is the number of live left/right neighbors. These are exactly the 64 reflection-symmetric ECAs.

No rule is excluded based on dynamics or class.

## Exact causal window

A current radius-one triple is determined from a previous radius-two five-cell word

\[
(a,b,c,d,e)\in\{0,1\}^5.
\]

Under source rule `r`, define

\[
L_t=r_{b,a+c},\qquad
C_t=r_{c,b+d},\qquad
R_t=r_{d,c+e}.
\]

The incoming center derivative is

\[
\delta_t=c\oplus C_t.
\]

The present outer-neighbor count is

\[
n_t=L_t+R_t\in\{0,1,2\}.
\]

The derivative-centered higher-dimensional patch exposes `n_t` through the noncenter cells of its central slice and exposes `delta_t` at the center. The stored rule planes provide all six `r_{c,n}` values.

## Primary reconstruction criterion

For each rule, enumerate all 32 previous five-cell words and collect the relation

\[
(n_t,\delta_t)\mapsto C_t.
\]

A rule has **exact derivative-center reconstruction** iff this relation is single-valued on every reachable pair `(n_t, delta_t)`.

Equivalently, there exists a deterministic decoder

\[
D_r:\{0,1,2\}\times\{0,1\}\to\{0,1\}
\]

such that for every valid one-step local history

\[
D_r(n_t,\delta_t)=C_t.
\]

The decoder is not fitted to individual trajectories. It is the exact functional relation induced by the complete local transition set for that rule.

## Stronger evolution criterion

Whenever reconstruction is exact, define the derivative-centered next-state output

\[
Y_{t+1}=r_{D_r(n_t,\delta_t),n_t}.
\]

Check on all 32 previous five-cell words that

\[
Y_{t+1}=r_{C_t,n_t},
\]

which is the ordinary source update applied to the reconstructed present local state. This equality should follow mechanically once reconstruction succeeds; the verifier records it separately as an implementation audit.

## Outputs

For every one of the 64 source rules, save:

- its six-bit outer-totalistic table and corresponding ECA rule number;
- number of reachable `(n_t, delta_t)` observation pairs;
- ambiguous observation pairs and witnesses when present;
- whether exact center reconstruction holds;
- the induced decoder table when it exists;
- evolution-audit failures, if any.

Aggregate outputs include the number of reconstructible rules and the distribution of ambiguity counts.

## Anti-overfitting / interpretation

- No Wolfram class labels are loaded by the evaluator.
- No spatialization, tolerance, cadence, or decoder convention is changed per rule.
- This 64-rule control family cannot by itself test the unrestricted Class-IV hypothesis because familiar rules such as 30, 106, and 110 are outside the outer-totalistic domain.
- A positive result means incoming derivative plus present outer-neighbor count is sufficient to replace the current center state in this declared layered architecture.
- A negative result identifies exact hidden-state ambiguity and motivates either additional represented history or a different lift architecture.
- Class comparisons, if any, occur only after the structural table is frozen.

## Immediate next step

If any nontrivial rules reconstruct exactly, derive the local higher-dimensional interpreter explicitly and then test overlap-consistent spatial realizations. If none do, characterize the ambiguity algebraically before enlarging the represented context.