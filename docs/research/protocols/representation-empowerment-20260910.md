# Protocol: closure, repertoire, and empowerment as distinct representation objectives — 2026-09-10

**Status:** frozen before numerical evaluation of this protocol.  
**Issue:** #63.  
**Scope:** static `n=12` ECA observer census only; no dimensional-lift or adaptive-observer claim.  
**Dependencies:** Research025 (`fiber-visibility`), Research026 (`possibility-frontier`), and the existing Research026 observer census. The separately frozen gradient-intervention protocol has a different action/outcome contract and is not numerically pooled with this experiment.

## Question

Research026 already separates two objectives for a lossy representation `P`:

1. **closure breaking / repair cost** — how little extra information is needed to obtain an autonomous factor;
2. **future repertoire** — how much stable-future uncertainty remains after observing the present macrostate.

This protocol adds a third, intervention-relative objective:

3. **revisability / empowerment** — how much a controller that sees only the current macrostate can deliberately select among future classes using a declared action interface.

The experiment asks whether the observer that maximizes future repertoire also maximizes accessible control over those futures.

## Frozen domain

Reuse the committed Research026 `n=12` static observer census and its saved observer list unchanged. Do not add, delete, or tune observers after evaluation begins.

The primary rule denominator is the **247 ECA rules for which Research026 found at least one closure-breaking observation**. The remaining nine rules may be retained as labeled controls but do not enter the frozen majority prediction.

For every `(rule, observer)` pair, use the same source ring, ECA update law, observer semantics, and stable future-equivalence construction already used by Research025/026.

## Initial-state distribution

The initial concrete microstate is uniform on the complete `2^12` ring state space:

\[
p(S_0=s)=2^{-12}.
\]

For a macrostate `y=P(S_0)`, therefore

\[
p(y)=|P^{-1}(y)|/2^{12},
\]

and the conditional hidden-state prior is uniform within the fiber:

\[
p(s\mid y)=1/|P^{-1}(y)|.
\]

Do **not** substitute a prior uniform over macrostates. That is a different experiment.

## Frozen intervention channel

The action alphabet is exactly

\[
A=\{\mathrm{noop},\mathrm{flip}_0\}.
\]

- `noop` leaves the ring unchanged.
- `flip_0` XOR-flips concrete cell 0 exactly once at intervention time.
- No other site, multi-bit, repeated, state-dependent, or learned action is allowed.

The controller receives only the current macrostate `y=P(S_0)`. It does not receive the hidden concrete state. Its policy is `pi(a | y)` and must be conditionally independent of the hidden state given `y`.

After the one-shot intervention the dynamics is autonomous under the original ECA rule; there are no further actions.

## Outcome variables and time indices

Let

\[
S_1=F(a(S_0)),\qquad S_{r+1}=F(S_r).
\]

Report both finite-horizon conventions below; the first is primary.

### Persistence-oriented finite horizon `C_h`

For `h in {1,2,4}`,

\[
C_h=(P(S_1),\ldots,P(S_h)).
\]

The observation of the immediately edited state is excluded. A flip does not receive credit merely because `P(a(S_0))` changes at intervention time.

### Initial-observation-inclusive control `C_h^+`

For the same horizons,

\[
C_h^+=(P(a(S_0)),P(S_1),\ldots,P(S_h)).
\]

This convention is the finite-horizon analogue of the existing `R_infinity` future class, which includes the initial observation.

### Stable future class `C_infinity`

`C_infinity(a(S_0))` is the existing stable future-equivalence class of the post-action state under the unperturbed `(F,P)` dynamics. It is an **idealized readout of the complete future observation sequence**, not a finite-horizon physical sensor.

Compute the stable relation once for `(F,P)` and evaluate the two post-action states in that relation. Do not redefine the relation separately for each action.

## Per-macrostate information quantities

For each reachable macrostate `y`, exact enumeration defines the rational channel

\[
W_y(c\mid a)=\Pr(C=c\mid A=a,P(S_0)=y)
\]

for each frozen outcome variable `C` above.

Retain the complete exact rational channel matrix in the audit output.

Report two distinct quantities.

### Fixed-prior action information

With `p(noop)=p(flip_0)=1/2`, report

\[
I_{unif}(y)=I(A;C\mid y).
\]

This is mutual information under the declared uniform action prior. It is **not** called empowerment.

### Capacity / empowerment

Report

\[
Cap(y)=\max_{\pi(a\mid y)} I(A;C\mid y).
\]

Because the action alphabet is binary, `0 <= Cap(y) <= 1` bit.

For each observer and outcome convention, aggregate with the frozen macrostate weights:

\[
\overline{I}_{unif}=\sum_y p(y)I_{unif}(y),\qquad
\mathcal E(P)=\sum_y p(y)Cap(y).
\]

`E(P)` is the primary empowerment/revisability score for comparing observers in this protocol.

## Frozen capacity numerics

Enumeration makes `W_y` exact; it does **not** make a floating-point capacity optimizer exact.

Handle exact degenerate channels before numerical optimization:

- identical action rows => capacity exactly `0`;
- disjoint output supports => capacity exactly `1` bit.

For every remaining binary-input channel:

1. run Blahut-Arimoto in double precision;
2. stop when the gap between the Arimoto lower bound and `max_a D(W(.|a) || q_k)` is at most `1e-9`;
3. iteration cap: `10^4`;
4. retain the floating-point lower/upper bracket and flag iteration-cap hits;
5. round the final input distribution to an explicit rational;
6. re-evaluate the lower and upper expressions using interval arithmetic with directed outward rounding at the exact rational channel entries;
7. retain this outward-rounded interval as the capacity certificate;
8. list every macrostate for which the certified interval is wider than the floating-point bracket by more than `1e-9`.

Observer rankings are considered numerically resolved only when the certified intervals separate the compared values. Otherwise report a tie/overlap; do not break it with midpoint values.

## Exact controls

The implementation must satisfy all of these before primary interpretation.

1. **Pointwise shielding control.** If
   `C_infinity(s) = C_infinity(flip_0(s))`
   for every `s in P^{-1}(y)`, then `Cap(y)=0` exactly.
2. **Fiber-permutation control.** If `flip_0` permutes the entire fiber `P^{-1}(y)`, then under the frozen uniform-fiber prior the two action rows are identical and `Cap(y)=0` exactly, even when individual states change future class.
3. **Identical-row control.** Any exact rational channel with equal rows returns exactly zero capacity.
4. **Disjoint-support control.** Any exact rational binary-input channel with disjoint action supports returns exactly one bit.
5. Reproduce the committed Research026 closure/repertoire values before adding the intervention column; a mismatch blocks the new census.

The first two controls deliberately distinguish pointwise lack of leverage from population-level channel indistinguishability.

## Frozen measurements

For every `(rule, observer)` retain:

- Research026 forgetting / closure-break status;
- Research026 stable future repertoire `V_infinity = H(C_infinity | P(S))`;
- complete rational action-to-outcome channels for `C_1,C_2,C_4`, `C_1^+,C_2^+,C_4^+`, and `C_infinity`;
- per-`y` `I_unif` and capacity brackets/certificates;
- weighted observer-level `I_unif` and empowerment scores;
- exact-zero control classifications;
- numerical-overlap/tie flags.

Aggregate by **rules**, not by rule-orbit counts or macrostate counts.

## Frozen primary prediction

Before running the new intervention census:

> Among the 247 Research026 rules admitting a closure-breaking observer, the observer(s) maximizing stable future repertoire `V_infinity` and the observer(s) maximizing certified `C_infinity` empowerment `E(P)` differ for a strict majority of rules.

A rule counts as a separation only when the certified maximizing sets are disjoint. Numerical overlap counts conservatively against the prediction.

This prediction concerns the static Research026 observer family only. Earlier physical-cap and neutral-program examples are motivation, not evidence for this count.

## Interpretation boundaries

- Empowerment is relative to the declared action interface, controller information, hidden-state prior, outcome variable, and horizon.
- `C_infinity` is a complete-future equivalence class, not an ordinary finite-horizon sensor.
- Repertoire measures passive future uncertainty; empowerment measures action-addressable future variation. Neither implies the other.
- A high score does not establish an endogenous controller, agency, biological function, or optimal behavior.
- The gradient-intervention audit has different actions, controller information, and outcomes and is not numerically comparable without a new bridge protocol.
- No Class-IV, dimensional-lift, or novelty claim is made here.

## Decision rule

- If the majority prediction passes, record closure, repertoire, and empowerment as empirically distinct representation objectives on this census.
- If it fails, retain the exact joint distribution and characterize whether repertoire and empowerment coincide, overlap, or separate only in specific rule/observer families.
- Numerical ambiguity is reported as ambiguity, not resolved by increasing precision after inspecting which rules are close.

No adaptive observer is introduced by this protocol; #64 is a separate research object.
