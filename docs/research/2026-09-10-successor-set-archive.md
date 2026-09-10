# Successor sets and local product approximations

This checkpoint archives the already inspected Rule110 example from [issue62](https://github.com/bombadil-labs/groovy-commutator/issues/62#issuecomment-5614870127), under the [signed scope](https://github.com/bombadil-labs/groovy-commutator/issues/62#issuecomment-5622836947). Its status remains **exploratory, reproduced using the same implementation**. Archival replay is not preregistration or an independent algorithmic audit.

## Declared object

The concrete domain is every binary state on the periodic eight-cell ring, with one synchronous Rule110 step F. Cell i has neighbors i-1 and i+1 modulo 8; integer states are enumerated MSB first. The observation is P(s)=s XOR F(s), equivalently elementary Rule162.

For each reachable observed field y, the exact transformer is the deterministic set-valued function

$$
B_{\mathrm{set}}(y)=\{P(F(s)):P(s)=y\}.
$$

It returns sets of **complete fields**. A single-valued factor exists precisely when every reachable row is singleton. Here 50 of 104 rows are singleton; the other54 fail that condition. A nonsingleton row remains an exact description of the alternatives, whose usefulness depends on the task.

The radius-R table returns all successor bits seen at a cell with a given current P-window, pooling every state and position on this ring. Its product across the eight cells defines a set of complete fields. The archived script asserts that every exact successor belongs to this product for every reachable y and R. Equal cardinalities then certify equality because containment has already been checked. Unseen windows have no certified entry.

## Reproduced counts

The exact relation has 104 reachable observations, mean row size 127/52 and maximum 6. Means in this table give each reachable y equal weight.

| Radius | Windows | Singleton windows | Determined cell occurrences | Product equals exact | Mean product size | Maximum |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 2 | 0 | 0/2048 | 0/104 | 256 | 256 |
| 1 | 8 | 5 | 832/2048 | 2/104 | 1457/52 | 256 |
| 2 | 27 | 22 | 1216/2048 | 10/104 | 421/52 | 32 |
| 3 | 72 | 58 | 1376/2048 | 38/104 | 301/52 | 32 |

Cell-occurrence counts use all 256 concrete states times8 cells, weighting an observed field by its fiber size. They do not use uniform observed-field weights. At radius 3 the ratio of mean product size to mean exact size is 301/127; this is a cardinality ratio, not an entropy ratio.

The product forgets output correlations. Singleton-cell frequency therefore does not replace whole-field precision. The table is certified only on this eight-cell ring. Larger rings or the infinite lattice need complete causal-window enumeration or a separate extension argument.

## Probability convention

For Z=P(F(S)) and Y=P(S), every conditional prior satisfies

$$
H(Z\mid Y=y)\leq\log_2|B_{\mathrm{set}}(y)|.
$$

An aggregate bound must use the same p(y) on both sides. Equality at y requires a uniform conditional distribution over its distinct successor fields. A uniform prior over concrete states in the fiber generally weights successors by multiplicity and need not meet that condition. No prior-free Shannon decomposition is supplied by a preorder.

## Archive and replay

The [script](../../exploratory/issue62-successor-sets/successor_sets_rule110_D.py) and [stdout](../../exploratory/issue62-successor-sets/output.txt) are copied verbatim from Claude's supplied comment above. Run from the repository root after installing the package:

```sh
python exploratory/issue62-successor-sets/successor_sets_rule110_D.py
```

Codex previously reproduced every printed number against commit f69b156ccc5fb7ff75ab4c2db95924dc87cc5d90, as recorded [in the issue](https://github.com/bombadil-labs/groovy-commutator/issues/62#issuecomment-5621678841). Archival replay against main 25dc5652c15f4dfbaef982dd75d54768a326aa64 also matches the complete stdout. The core ca.py blob is 38ef0e7cf8c53063e389c4b63c0a1191c16de045. A dedicated CI job compares replay stdout byte-for-byte and retains the script's containment assertions. This preserves the explored example; it does not run a new comparison.

## Remaining Program question

Which ordered representation domains provide useful sound approximations when exact closure fails, at what resource and precision costs? This example supplies one finite product domain, ordered by inclusion, and a comparison with its exact successor relation. It does not settle the general preorder proposal. A new observer, substrate or infinite-lattice claim requires a separate frozen protocol.

See the [shared closure account](2026-09-10-shared-closure-account.md) for factor existence and the candidate-law distinction.
