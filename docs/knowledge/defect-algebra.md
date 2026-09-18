# One-step healing on the beam is three pairwise bit-equalities; twelve in all, rank eleven

Take a state on the [invariant beam](invariant-beam.md) of a height-two strip
and flip one cell of the second row. Exactly six reads change: both rows at
the flipped column and its two neighbours. **None of the post-flip reads
lands on an exposed entry** — the arithmetic cannot turn the beam's `3R` term
into an exposed index — so the damage is carried entirely by free table
entries, the ones the base rule does not own.

Whether the defect heals in one step is a conjunction of three pairwise
equalities between free entries, each depending on the surrounding five-cell
window only through a two-cell window of its own:

| block | reads | governs | index gap |
| --- | --- | --- | ---: |
| `A` | the two cells left | leftward growth | 1 |
| `B` | the cells either side | isolated survival | 14 |
| `C` | the two cells right | rightward growth | 6 |

Twelve equalities, GF(2) rank **eleven**. So refinements fall into 2,048
signature classes of 8,192 each; the universal healers form a
thirteen-dimensional subspace, about one in two thousand; and the expected
one-step healing rate under a uniform refinement is exactly `1/8`.

**Edge lemma.** For any defect configuration, the column west of the leftmost
defect reads exactly the `A` pair and the column east of the rightmost reads
the `C` pair, regardless of the cluster's interior; an isolated defect reads
`B` at its own column. The factorization therefore governs every step, not
only the first.

Corollaries, each fixing an outcome outright: if `A` or `C` never holds, a
defect never dies and transverse extinction is zero; if both always hold, a
single defect is confined to its column forever; if all twelve hold, every
defect dies immediately.

Status: exact within stated bounds — height two on this family's cylinder,
single-cell defects on the beam. Re-derived from the read-index definition and
verified by enumeration as a gating control of the
[defect-algebra unit](../research/2026-09-18-defect-algebra.md): six perturbed
reads with none exposed, fourteen lit and ten dark entries, the factorization
for all three blocks, rank eleven, cell sizes exactly 8,192, and a simulated
step matching the violated-constraint count on 256 random pairs.

## Why it matters

It puts the refinement's contribution in a readable basis. Regressed on the
twelve exclusive-ors, transverse stability has cross-validated `R²` of 0.37
to 0.43 in every base; regressed on the twenty-four raw bits it is negative in
every base. The non-additivity recorded two units earlier was never an absent
effect, only the wrong coordinates.

It also very nearly answers what makes a refinement attract trajectories onto
the beam: refinements built to satisfy all twelve sit on the beam in 83 to 96
percent of trials in seven of eight bases, and never under the identity rule.

## Bounds

Healing an isolated defect is not the same as beam residence from a dense
random start. One base breaks the correspondence entirely, and in three bases
refinements that provably never heal an isolated defect are nonetheless closer
to the beam than typical ones. What sets residence beyond the healing
signature is open.
