# When does a one-dimensional G field have an autonomous G field?

**Exact bounded result, 2026-09-23.** Authored by Codex (OpenAI).
Reviewed by: none. [PR #296](https://github.com/bombadil-labs/groovy-commutator/pull/296).

We asked which already-autonomous, present-only G fields support a second
autonomous G field, staying entirely in one dimension. We reconstructed the
36 first-generation laws from the existing census and examined their
descendants. There are two nonconstant positives: **Rules 2 and 16**, on the
fields inherited from the original source, for the two specified derived
rules tested here. **Rule 32 fails** for both of its smallest-neighborhood
derived rules. The other 33 cases have pointwise updates and constant native G.

This unit concerns present-only binary fields. Rule 30 needs three temporal
observations and is outside this unit; no claim about its recursion follows.

## What is being iterated

For source rule r, write `g = G_r` and let F be a total 1D binary rule satisfying
`F(g(S)) = g(E_r(S))` for every original source S. Form the native commutator

```
G_F(Y) = F(Y) XOR F^2(Y) XOR F(Y XOR F(Y)).
O(S) = G_F(g(S)).
```

The primary question is whether a local H satisfies `H(O(S)) = O(E_r(S))`
for every source S. This follows the actual second-generation field. We also
check the stronger question `H(G_F(Y)) = G_F(F(Y))` for every binary row Y.
The latter allows starting rows that the original G field never produces.
All statements use the infinite integer line, synchronous updates, cadence
one, no burn-in, and no temporal memory. An exact local identity holds at
every future time by substitution; it is not a finite-horizon extrapolation.

No lift or spatial encoding is used. This also differs from applying the
old G_r formula twice while keeping the original evolution rule inside it.

## Which first-level rules were used?

We recertified the 36 present-only positives and their smallest symmetric
radii. Thirty-three have radius zero; sources 2 and 16 require radius two,
and source 32 requires radius one. Every forced local-table entry is stored.

Some neighborhoods never occur in the first G field. To specify F completely,
the primary choice sets those entries to zero. A fixed sensitivity check sets
them all to one. These choices were frozen before evaluation. Both give the
same closure verdicts below, but their second-generation observations differ.
This is not invariance over arbitrary completions.

Rule 32 has exactly one unforced radius-one entry, at neighborhood 101. The
two choices are Rules 128 and 160, so in this case the check exhausts **all
radius-one completions**. We do not exclude alternatives with larger radii.

## Results

| Original source | First G update | Second G on inherited fields | Second G from arbitrary descendant rows |
| --- | --- | --- | --- |
| 33 pointwise cases | Radius zero | Yes, constant field | Yes, constant field |
| Rule 2 | Radius two, either specified F below | **Yes, nonconstant; minimum symmetric radius two** | No present-only law, for either tested F |
| Rule 16 | Reflected Rule-2 case | **Yes, nonconstant; minimum symmetric radius two** | No present-only law, for either tested F |
| Rule 32 | Rule 128 or Rule 160 | **No present-only law**, for both radius-one choices | No present-only law for either choice |

For any pointwise binary update `f(x) = a*x XOR b`, direct algebra gives
`G_f(x) = b`. Thus the 33 pointwise cases collapse at the second generation,
regardless of which pointwise completion is chosen. They are:

`0, 1, 4, 8, 12, 15, 19, 36, 51, 60, 64, 68, 72, 76, 85, 90, 102,
105, 150, 153, 165, 170, 195, 200, 204, 205, 207, 219, 221, 223, 236, 240, 255`.

The nonconstant positive chains have explicit five-input truth tables:

| Source | Fill for absent first-G neighborhoods | F truth-table integer | H truth-table integer, absent second-G neighborhoods filled with zero |
| --- | --- | --- | --- |
| 2 | 0 | `0x08400844` | `0x040c50cc` |
| 2 | 1 | `0xfcf4ccc4` | `0x010c0c0c` |
| 16 | 0 | `0x0c003100` | `0x13005b40` |
| 16 | 1 | `0xfca0ffa0` | `0x07000708` |

The five bits are positions -2 through +2, read as a binary integer with
the leftmost bit most significant; bit j of each table integer is the
output for neighborhood j. H is certified on the inherited second-G image,
not as an update for G_F on F's entire binary domain.

Each inherited positive exhausts all **32,768 source words of length 15**,
covering every dependence needed for the claimed radius-two law. Separate
unpacked arithmetic replays the identity. Conflicts at radii zero and one
establish the stated minimum symmetric radius. The second observation is
nonconstant: its radius-five truth table has 296 one-entries out of 2,048
under zero fill, and 280 under one fill (for either mirror source).

## An exact failure at the second generation

For source Rule 32 and derived F = Rule 128, periodically repeat either
source row below across the whole line:

| Source S | Second G, `G_128(G_32(S))` | Its value after one source step |
| --- | --- | --- |
| `01010101101` | `00000100001` | `10001000000` |
| `01110101101` | `00000100001` | `00000000000` |

The complete current second-G fields agree and their successors disagree.
No amount of spatial access to that current field determines its successor.
The Rule-160 alternative has a separate period-12 certificate. These are
infinite-line negatives by periodic extension, not extrapolations from
finite-ring success. Neither excludes closure with temporal memory.

For the full descendant-domain checks, explicit witnesses have periods 7
(sources 2/16, zero fill), 4 (2/16, one fill), 8 (Rule 128) and 6 (Rule 160).
The result file preserves every word and scalar replay. These full-domain
negatives are intentionally separate from the inherited positives.

## Evidence, limitations and disposition

- [Frozen protocol](protocols/groovy-1d-second-generation-20260923.md), commit
  [`9d9f2e1`](https://github.com/bombadil-labs/groovy-commutator/commit/9d9f2e154983cf57811daba0fe64036059555814).
- [Implementation](../../scripts/groovy_1d_second_generation.py) before evaluation,
  commit [`13ba2c9`](https://github.com/bombadil-labs/groovy-commutator/commit/13ba2c9aabd3c39440a6f0a1b63c894f5cd71f92).
- [Canonical result](../../results/groovy_1d_second_generation_20260923.json)
  pins the protocol, implementation and old census input, and stores the
  forced tables, observation tables, complete-cone sizes and witnesses.

The frozen search screened periods through twelve and, when no collision
occurred, checked local radii through four with a 21-bit source-cone cap.
Every selected case resolved within those bounds. The local record command
completed in under one second. Packed evaluation and separate unpacked/scalar
verification were performed by the same agent; no independent review occurred.

```
OPENBLAS_NUM_THREADS=1 python scripts/groovy_1d_second_generation.py --check
python -m pytest tests/test_groovy_1d_second_generation.py -q
```

The new narrow CI job runs those checks. Historical result bytes and the
legacy integrity registry are unchanged. The open geometry PR #295 remains
separate work; this unit neither modifies nor integrates it.

**The second generation can close nontrivially in 1D, and closure can also
fail at that generation.** There is no general self-sustaining tower theorem
here. Larger-radius first-level completions, arbitrary completions for 2/16,
memory-bearing laws such as Rule 30's, and a third generation are untested.
No speedup, complexity-class or physical interpretation is claimed.
