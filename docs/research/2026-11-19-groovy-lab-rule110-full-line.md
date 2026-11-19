# Rule 110: two snapshots identify almost every source, not every source

**Result:** exact, scoped. The proposed universal full-line extension fails. Two distinct nonperiodic sources can give the same entire parity and Groovy fields at every epoch. Nevertheless, the same two snapshots identify a fair-IID source almost surely on the line, and the two previously known unordered collision pairs are the only ones on **every even ring**, not just the seven tested widths.

## Fixed question and definitions

The [frozen protocol](protocols/groovy-lab-rule110-full-line-20261119.md) extends the [original finite-ring study](https://github.com/bombadil-labs/groovy-commutator/blob/4883bd96975a45dec29274630f3b134e309ed3d6/docs/research/2026-10-07-rule110-latent-q.md) as scoped there: synchronous Wolfram Rule 110 step `H`, epoch `F=H²`, fixed block parity `P[j]=X[2j] xor X[2j+1]`, and full microscopic `G=H(X) xor H²(X) xor H(X xor H(X))`. Compare two complete snapshots of `(P,G)`, before and after one epoch. No locality of an inverse or one-snapshot reconstruction is claimed.

## A full-line ambiguity that no future observation resolves

Take aligned two-bit blocks, with the seam just before site 0:

```
X: ... 00 00 | 01 01 01 ...
Y: ... 11 11 | 10 10 10 ...
```

The two block parities agree: zero to the left and one on the right. Rule 110 gives the following local calculation. Both `G` and `F` have radius at most two, so the only windows that can cross the seam have centers −2, −1, 0, and 1. In the constant or alternating tails, both fields are zero.

| Site | X window | Y window | G (both) | F (both) |
| ---: | :---: | :---: | ---: | ---: |
| −2 | 00000 | 11111 | 0 | 0 |
| −1 | 00001 | 11110 | 0 | 1 |
| 0 | 00010 | 11101 | 1 | 1 |
| 1 | 00101 | 11010 | 0 | 0 |

The sources match under the observer at epoch zero and become the *same microscopic configuration* at epoch one. All later observations therefore also agree. The seam is not a new periodic collision; it is a path between distinct recurrent components, which is why a cycles-only calculation misses it.

## What holds despite that counterexample

The ordered block alphabet has eight symbols: all pairs of two-bit source blocks with equal block parity. A five-symbol word (ten sites) determines the epoch-zero and epoch-one outputs of the central block. At epoch one the widest test is `G(F(X))` of radius four per site; combined over two sites, its source window fits exactly. Admit a directed edge from the four-symbol prefix to the four-symbol suffix iff the two source words match on these outputs. Bi-infinite paths in this graph are exactly the compatible full-line pairs.

Enumerating all 8⁵ words admits 4,904 edges. Repeatedly discard edges whose origins have no predecessor or whose targets have no successor. A retained edge can extend independently in both directions, so the fixed point is exact and retains edges *between* recurrent components. It has 1,088 edges: 1,024 within the diagonal and 64 incident to an off-diagonal vertex. The only cyclic off-diagonal edges are four self-loops, one for each ordering of the two periodic pairs. No retained edge leaves the diagonal.

- **Fair-IID source:** Every non-diagonal compatible path stays off the diagonal to its left and eventually occupies one of the four self-loops toward minus infinity. Thus both sources have an eventually constant or alternating far-left tail. That event has fair-IID probability zero. So the two snapshots determine a fair-IID source almost surely; a deterministic autonomous representation retaining `(P,G)` must make any two sources that it identifies agree on both snapshots. Thus it cannot forget a positive rate under that prior. This is a statement about entire fields, not bounded decoding radius or finite-window error rates.
- **Even periodic rings:** Every paired periodic extension gives a closed walk. It is either diagonal or one of the four off-diagonal constant loops. Both unordered periodic pairs coalesce at the first epoch, so the classification applies to all later observations as well. For the uniform prior on an even ring of width `n≥2`, the residual entropy of this quotient is exactly `4/2^n` bits per source ring.
- **What survives indefinitely:** The seam coalesces at epoch one; not every two-snapshot collision does. Two retained ordered windows have unequal epoch-one microscopic central blocks, and each extends to an actual full-line pair. In fact, any compatible pair that has not coalesced by epoch one must disagree at epoch two. Its far-left tails become identical under `F`; if epoch two also matched, the pair starting at epoch one would be a two-snapshot collision with a common far-left tail, which the graph excludes. Hence all-time equivalence is exactly equality of the initial observed fields and microscopic coalescence by epoch one. This is a consequence of the same graph, not a widened numerical search.

## Reproduction and decision

Run `node docs/research/reproducers/groovy_lab_rule110_full_line_20261119.mjs` from the repository root. It uses only Node’s standard library. It enumerates and prunes the graph, tests the cycle inventory, checks both directions of each standard periodic pair, and evaluates the explicit seam using the local Rule 110 truth table. The code under review is commit `a508970275f40626d1a52e98910e6c6e93c58cc4`. A separate assistant referee rederived the pair graph with a separate implementation before inspecting that commit; this is independent assistant reproduction, not external peer review.

**Decision:** close this bounded unit. The small-ring observation is true on every even ring and fair-IID almost surely on the line, but does not yield a universal full-line inverse. No automatic next research unit.
