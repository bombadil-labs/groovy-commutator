# Dense defect stratification

**Kind:** finding · **Status:** exact · **Research:** [dense-defect-algebra-20260918](../research/2026-09-18-dense-defect-algebra.md)

At height two both rows of a column read one table entry each:

```
row r at column j reads   16*x_r[j] + 8*x_r[j-1] + x_r[j+1] + 2*s_{r'}(j)
```

where `s` is a row's three-cell popcount. With `Δ_j = s₁(j) − s₀(j)`, the stratum of
**both** reads at once is decided by `|Δ|`:

| `\|Δ\|` | both rows read | pairs |
| --- | --- | ---: |
| 0 | exposed — owned by the base ECA | 6 |
| 1 | lit | 15 |
| ≥ 2 | dark | 7 |

Enumerating the 64 six-bit windows gives 8 trivially agreeing cases and 28 unordered
pairs, with **no mixed pair**. This *characterizes* the single-defect algebra's
8/14/10 entry partition rather than enumerating it.

GF(2) ranks are 11 (lit) and 7 (dark) over 24 free entries, so exactly **64**
completions satisfy every free constraint — one per connected component. Under any
base and such a completion, disagreement survives only through blind (`Δ = 0`)
columns.

Two exact corollaries:

- **β-all-hold ⇔ totalistic** (exactly 16 rules), and then γ holds too. A totalistic
  base with a fully-constrained completion collapses *any* state to agreement in one
  step.
- Under **204 and 51**, width-two anti-phase runs with agreeing flanks are fixed for
  every `A ∧ C` completion, and under a fully-constrained completion the residual is
  exactly those runs of the initial disagreement field:
  `agree = 1 − 2·N_ap(x₀)/W`, expectation `0.9375` at density ½. The two bases give a
  bit-identical median, because the residual depends on the initial field and not on
  which of them runs.

**Why the last point matters:** it kills the reading that the identity exception is
about the base contributing no mixing. Rule 51 flips every cell every step and
behaves identically; totalistic rule 0 heals everything. Four bits of the base decide
it, not activity.

**Depends on:** [invariant-beam](invariant-beam.md) — the `Δ = 0` reads are exactly
the height-one exposed indices.
**Required by:** [defect-algebra](defect-algebra.md) — its twelve constraints are a subset of
the fifteen lit pairs, and its 8/14/10 partition is this stratification restricted to a
one-cell perturbation. The stratification was found second; the dependence runs first.
