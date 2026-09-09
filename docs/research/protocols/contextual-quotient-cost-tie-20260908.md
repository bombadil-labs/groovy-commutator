# Follow-up protocol: cost-aware zero-gain ties — 2026-09-08

**Status:** frozen after deriving the future-context quotient and targeted reconstruction of the four Research028 failures, but before evaluating the new policy across the full block-3 census.  
**Branch:** `research/fatal-predictive-synergy-20260908`.

## Discovery

Research028's frozen greedy rule breaks exact gain ties canonically by partition key. The future-context quotient analysis reconstructs all four Research028 failures as **zero-margin** events: at the first unsafe choice, no unsafe cover has strictly larger predictive gain than every Q-safe cover.

In the Rule-24 `01000010` case, after the first positive safe split the path reaches `01200210`. The best safe and unsafe next splits both have mathematically zero immediate predictive gain. Canonical key order chooses unsafe `01200213`; Q-safe `01200230`, which separates `{1}|{6}`, costs less added entropy and later unlocks the high-value `{3,7}` split.

Targeted reconstruction shows the same qualitative zero-margin structure in all four known Rule-24/231 failures. This is discovery, not a fresh test.

## Frozen alternative policy

At current encoder `P`, compute every one-step closure gain

\[
g(P\to P')=\frac{W_T(P)-W_T(P')}{H(P')-H(P)}.
\]

Define **cost-aware greedy**:

1. let `g_max` be the maximum available gain;
2. collect every cover satisfying
   
   \[
   g_{max}-g(P\to P')\le10^{-10};
   \]
3. among that gain-tied set, choose the cover with the smallest added present entropy
   
   \[
   H(P')-H(P);
   \]
4. break any remaining tie by canonical partition key.

The gain tolerance, entropy secondary key, and canonical fallback are frozen before the full-census evaluation.

## Full-census prediction

Evaluate exactly the same 30,856 nonclosed block-3 target cases as Research028.

Predict that cost-aware greedy will:

- eliminate all four canonical-tie failures;
- introduce **no new failures** among the 30,852 cases previously solved by canonical greedy;
- therefore reach the canonical future-context quotient in
  
  \[
  \boxed{30,856/30,856}
  \]
  
  cases.

Retain any counterexample. Do not alter the policy after inspection.

## Secondary measurements

Report:

- number of cases where cost-aware and canonical greedy take different paths;
- number where they take different paths but both reach the contextual quotient;
- number of zero-margin steps encountered by each policy;
- number of cases with strictly negative safety margin along the canonical greedy path;
- minimum positive safety margin among successful canonical paths;
- near-zero successful cases at thresholds `1e-6`, `1e-4`, and `1e-2`.

## Interpretation boundary

A 100% result would establish exactness only for the frozen finite block-3 census. It would not prove cost-aware greedy is universally optimal.

If it passes, Research028's correct interpretation should be sharpened: predictive synergy creates zero-gain bridge requirements, but at block size three the known global failures arise from **ambiguous zero-gain choices**, not from an unsafe split with strictly superior marginal gain.

The stronger theoretical question would then be whether a future example exists with genuinely negative safety margin, where every locally best split is quotient-unsafe.