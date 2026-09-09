# Follow-up protocol: bulk entropy versus memory-tail repair — 2026-09-08

**Status:** frozen after the primary `n=12` partition-lattice run exposed the Rule-106 split, before the all-rule tail census and before any `n=18` evaluation.  
**Branch:** `research/representation-design-20260908`.

## Discovery that motivates the follow-up

The primary representation-design protocol predicted that, for Rule 106 under block-2 parity, the first closure-directed split favored by the known long-lived `10 <-> 01` hidden defect would also maximize the Shannon residual-entropy reduction.

That prediction failed.

At `n=12`, both one-split refinements add exactly 3 visible bits. Splitting the even-parity class `{00,11}` leaves slightly less fixed-target residual future entropy than splitting the odd-parity class `{10,01}`.

A post-result diagnostic then inspected the **maximum residual target-history depth** after each split and found the opposite ordering: the defect-oriented odd-class split appeared in the first exploratory implementation to reduce the worst-case residual history depth from 13 to 4, while the Shannon-optimal even-class split left it at 13. The audit correction below replaces that provisional value with the full-future result 13 -> 7.

This follow-up freezes that newly exposed distinction before measuring it systematically.

## Fixed-target residual memory depth

Keep the fixed-target setup from the primary protocol. For binary future target `T` and present encoder refinement `Z <= T`, define

\[
m_T(Z)
\]

as the least nonnegative history depth such that the entire future target trajectory is determined by `Z(S)` together with target observations through that depth.

Equivalently, initialize the predictive partition with `Z(S)` rather than `T(S)` and refine it by successive future target states until no further split occurs.

Controls:

- `m_T(T)` equals the ordinary `h*` of target `T`;
- `m_T(identity)=0`;
- if `W_T(Z)=0`, then `m_T(Z)=0`;
- refinement of `Z` cannot increase `W_T`, but no monotonicity of `m_T` is assumed beyond the identity endpoint.

## Audit correction before publication

The first exploratory implementation of `m_T(Z)` incorrectly reused the ordinary history-closure stopping rule: it stopped at the first future step that did not split the current `(Z, T_1, ..., T_t)` partition. That shortcut is valid when the same observation defines both the current state and every history symbol, but it is **not** valid when `Z` is a one-time present encoder and `T` defines the future semantics. A temporary plateau can split again later.

An independently written explicit-future audit caught this before Research027 was published. The corrected definition used for the full census and CI is:

\[
 m_T(Z)=\min\left\{t:\;\sigma(Z,T_1,\ldots,T_t)
 =\sigma(Z,C_\infty^T)\right\},
\]

where `C_infinity^T` is first computed from the complete stable target-future partition. Equivalently, `m_T(Z)` is the first horizon at which the encoder plus target history has recovered **all** target-future distinctions, not the first local plateau.

This correction changes the initial Rule-106 exploratory tail values from `13 -> 4` to **`13 -> 7`** for the odd-class split at `n=12`. The qualitative separation survives: the even split is still bulk/Shannon-optimal and leaves the worst-case tail at 13, while the defect-oriented odd split is tail-optimal. The fresh-size prediction below remained qualitative and was evaluated only with the corrected full-future definition for publication.

## Two first-split objectives

For each nonclosed binary target with at least two possible one-split refinements, compare:

1. **bulk-optimal split** — maximizes
   \[
   g_{bulk}=\frac{W_T(T)-W_T(Z)}{H(Z)-H(T)};
   \]
2. **tail-optimal split** — minimizes `m_T(Z)`, with ties broken first by lower `W_T(Z)` and then canonical partition order.

Record whether the optimizer sets intersect, the residual entropy and residual memory of each choice, and the added visible information.

The primary follow-up statistic is the fraction of eligible `(rule,T)` cases for which bulk-optimal and tail-optimal first splits differ.

Wolfram-class comparisons remain exploratory.

## Rule-106 confirmatory prediction

Freeze the specific `n=12` Rule-106 parity result as the discovery case:

- bulk-optimal split: split `{00,11}`;
- tail-optimal split: split `{10,01}`.

Before evaluating `n=18`, predict that the same qualitative separation survives:

1. the odd-parity `{10,01}` split has strictly smaller `m_T(Z)` than the even-parity `{00,11}` split;
2. the even-parity split has no larger `W_T(Z)` than the odd-parity split.

Both inequalities must hold for the follow-up to pass. Do not reselect a different refinement after inspection.

## Interpretation boundary

This follow-up distinguishes **ensemble-weighted predictive uncertainty** from **worst-case latent lifetime**. A split can be excellent for the rare longest-lived mode while being slightly worse in Shannon-average information terms.

Do not call either objective universally superior. The purpose is to determine whether representation repair is already genuinely multi-objective even after future semantics have been fixed.
