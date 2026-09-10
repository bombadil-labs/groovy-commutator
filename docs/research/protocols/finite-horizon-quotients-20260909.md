# Protocol: finite-horizon future-context quotients — 2026-09-09

**Status:** frozen before evaluation.  
**Branch:** `research/finite-horizon-quotients-20260909`  
**Dependency:** Research029 / future-context quotient theorem.

## Question

Research029 assumes the complete future-equivalence label `C_infinity` is already known. In that setting the representation-design problem has a canonical answer: compute the future-context quotient directly.

The practical problem is harder:

> **Can the canonical quotient, or at least the safety of individual representation edits, be learned before the complete future is known?**

This note studies the exact finite-horizon quotients that approach the final quotient as longer target futures are revealed.

## Setup

Fix deterministic microscopic dynamics `E`, cadence `q`, and a local target observation `T` applied uniformly to nonoverlapping blocks. On a finite periodic system write

\[
Y_t=T(E^{qt}(S)).
\]

Let

\[
C_h(S)=(Y_0,Y_1,\ldots,Y_h)
\]

be the observed target word through horizon `h`, viewed only as its induced partition of microscopic states. Let `C_infinity` be the stable complete future-equivalence partition and let `h*` be the least horizon at which

\[
C_{h*}=C_\infty.
\]

For every horizon, construct the Research029 future-context quotient

\[
Q_h = A/{\equiv_{C_h}}
\]

on the local fine alphabet `A`.

`Q_infinity` denotes the quotient of `C_infinity`.

## The finite-horizon quotient theorem

The following claims are frozen as mathematical controls and should be proved independently of the ECA census.

### Monotone refinement

Because `C_{h+1}` refines `C_h`, contextual equivalence can only be lost as the horizon grows:

\[
\equiv_{C_{h+1}}\subseteq\equiv_{C_h}.
\]

Therefore

\[
\boxed{Q_0 \preceq Q_1 \preceq \cdots \preceq Q_\infty}
\]

where `P \preceq Q` means `Q` refines `P`.

### Finite convergence

Since `C_h` stabilizes at `h*`,

\[
\boxed{Q_{h*}=Q_\infty.}
\]

Define the **quotient discovery time**

\[
d_Q = \min\{h:Q_h=Q_\infty\}.
\]

Then necessarily

\[
\boxed{d_Q\le h^*.}
\]

Strict inequality is allowed: the local sufficient representation can stabilize while the global predictive partition continues refining.

### Sound edit certification

Let `Z` be any candidate local partition. Call it **finally safe** when `Q_infinity` refines `Z`, meaning `Z` has not split any distinction that the final canonical quotient still merges.

If at some finite horizon

\[
Q_h\text{ refines }Z,
\]

then `Q_infinity` also refines `Z`. Thus

\[
\boxed{Q_h\preceq Z \;\Longrightarrow\; Z\text{ is finally safe}.}
\]

This certificate is monotone: once certified, an edit remains certified at every later horizon.

### Eventual completeness

If `Z` is finally safe, then at `h*`, `Q_{h*}=Q_infinity` refines `Z`. Therefore every finally safe edit is certified after finite time.

Define its **certification time**

\[
\tau_{cert}(Z)=\min\{h:Q_h\text{ refines }Z\}.
\]

Then

\[
\tau_{cert}(Z)<\infty \iff Z\text{ is finally safe}.
\]

This makes `{Q_h}` a sound and complete finite-time certification process for refinement safety on a finite deterministic target system.

## Primary exact census

Reuse the complete Research028–029 block-3 domain:

- all 256 ECA rules;
- periodic ring width `n=12`;
- nonoverlapping block size 3;
- matched cadence `q=3`;
- all 127 canonical nonconstant binary target partitions up to output complement;
- uniform ensemble over all 4,096 microscopic ring states.

For every target, compute exact `C_h` partitions from `h=0` through `h*`, then construct `Q_h` directly from exact context substitution.

## Primary measurements

For every `(rule,target)` record:

- `hstar`;
- final quotient `Q_infinity`;
- `quotient_discovery_time = d_Q`;
- whether `d_Q < hstar`;
- the complete quotient chain, compressed to horizons at which it changes;
- number of local quotient classes at every change horizon;
- local quotient entropy `H(Q_h(U_A))` under uniform local fine symbols;
- global encoder entropy `m H(Q_h(U_A))`, where `m=n/3=4`;
- final added representation information relative to `Q_0`;
- fraction of that final added information certified by horizon `h`;
- birth/certification time of every final quotient distinction.

For already closed targets, expect `Q_0=Q_infinity` and `d_Q=0`.

## Distinction birth times

For each unordered pair of local symbols `(a,b)` that are separated in `Q_infinity`, define

\[
\tau_{split}(a,b)=\min\{h:a\not\equiv_{C_h} b\}.
\]

By monotonicity, once separated they never re-merge.

These birth times provide an exact local chronology of which hidden distinctions become predictively necessary when.

## Representation-information curve

Let

\[
R_h = H(Q_h(U_A))-H(Q_0(U_A)),
\qquad
R_\infty=H(Q_\infty(U_A))-H(Q_0(U_A)).
\]

When `R_infinity>0`, define

\[
\rho_h=R_h/R_\infty.
\]

`rho_h` is the fraction of the final local representation information that finite-horizon evidence has already certified.

Report the earliest horizons at which `rho_h` reaches 25%, 50%, 75%, 90%, and 100%.

## Preregistered hypotheses

1. **Theorem controls:** quotient chains are monotone, `d_Q <= h*`, certifications never revoke, and every final-safe candidate is certified by `h*`.
2. **Primary empirical hypothesis:** there exist many nonclosed cases with `d_Q < h*`; the local canonical representation can stabilize before the complete global predictive partition.
3. **Early-information hypothesis:** for a substantial fraction of nonclosed targets, at least half of final representation information is certified strictly before `h*/2`.
4. **Long-tail hypothesis:** large `h*` need not imply equally late quotient discovery. In particular, some long-memory targets should have a small `d_Q/h*` ratio because late history refines global state distinctions without introducing new local context distinctions.
5. Class comparisons are exploratory only.

Do not change these criteria after inspecting the full census.

## Mechanism cases frozen before evaluation

Retain detailed chains for:

- the four Research028/029 fatal-synergy targets in Rules 24 and 231;
- Rules 30, 54, 90, 106, 110, and 184 under selected block-3 targets already used in Research026–028 where applicable;
- any target with maximal `h*` in the frozen domain, selected only after the primary aggregate as a descriptive extreme and labeled post-census.

For the Rule24/231 failures, ask when the quotient first certifies the zero-immediate-gain bridge distinction from Research028. No directional prediction is frozen for its exact horizon.

## Independent audit

An independently written audit must reconstruct selected `Q_h` chains directly from explicit finite observed words rather than importing the primary quotient-chain helper. It must verify:

- exact contextual equivalence at every reported change horizon;
- monotone refinement;
- equality with `Q_infinity` at `d_Q`;
- at least one case with `d_Q<h*` if the primary empirical hypothesis passes;
- the four fatal-synergy mechanism chains.

## Scope and nonclaims

- All empirical claims are exact for the stated finite periodic systems only.
- The monotone quotient/certification theorem is finite and deterministic but not specific to ECA.
- `Q_h` uses exhaustive exact contexts. It is not yet a practical local sampling algorithm.
- Knowing `C_h` exactly may itself be expensive; this note asks what information is theoretically available at finite horizon, not how to estimate it cheaply from sparse data.
- A finite-horizon quotient is intentionally under-refined relative to the final quotient. It certifies that certain merges remain safe so far and that certain splits are definitely required; it does not certify that currently merged symbols will remain merged forever.
- No block-4 scale-up is attempted here.

## Decision rule for the next note

If `d_Q` is often substantially smaller than `h*`, the next problem is to infer `Q_h` from **partial contexts or sampled trajectories** while preserving one-sided safety guarantees.

If instead `d_Q` almost always equals `h*`, the exact finite-horizon hierarchy is still mathematically useful, but the practical inference route should shift toward local causal certificates such as defect/read geometry rather than waiting for quotient stabilization.
