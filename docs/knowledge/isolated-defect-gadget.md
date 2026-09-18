# Isolated-defect gadget

**Kind:** finding · **Status:** exact · **Research:** [permanent-structures-20260918](../research/2026-09-18-permanent-structures.md)

Under a refinement satisfying the two edge constraints (`A ∧ C`), an isolated
defect at column `j` has:

| column | reads | under `A ∧ C` |
| --- | --- | --- |
| `j−1` | `A(LL, L)` | both rows take one value — stays agreeing |
| `j` | `B(L, R)` | heals iff `B(L,R)` holds |
| `j+1` | `C(R, RR)` | both rows take one value — stays agreeing |
| `j±2` | exposed entries, agreeing windows | inert |

So `(L, d₀, d₁, R)` evolves as a **deterministic automaton on 8 defect states
plus an absorbing healed class, with a 2-bit input `(LL, RR)`** supplied by the
background. **SAFE** is the greatest input-closed set; **DOOMED** the least set
containing healed and closed under "every input leads in".

**Exact cell sizes** over the 57,344 confined refinements: `K∀` (SAFE ≠ ∅)
**24,576**, `K∃` (neither) **28,672**, `K⊥` (all DOOMED) **4,096**.

**Verified:** the gadget matches the real step with **0 mismatches of 22,270**.
On the four frozen-context bases the input sequence is fixed by the base alone,
and iterating it predicts **every one of 6,144 transverse trials' healing step
exactly**. Across all 36 bases the partition bounds the extinction fraction with
**0 violations of 1,728**; every `K⊥` has `T_ext = 1` and no SAFE-started trial
ever heals.

**Why it matters:** isolated-defect permanence orders dense-start residence at
pooled Spearman **−0.836**, and at or below −0.6 in every one of 36 bases.

**Depends on:** [dense-defect-stratification](dense-defect-stratification.md).
