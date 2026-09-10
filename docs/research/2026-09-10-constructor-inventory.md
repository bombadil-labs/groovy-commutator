# Compare the constructors before intersecting their rule sets

This is the descriptive inventory approved in [issue66](https://github.com/bombadil-labs/groovy-commutator/issues/66#issuecomment-5622839348). It extracts saved results and computes set intersections. It runs no CA census, changes no source evidence label, and makes no new prediction.

## Four declared sets

| Symbol | Count | Constructor and criterion | Substrate and budget |
| --- | --- | --- | --- |
| T8 | 33 | Cumulative L/R/C role vocabulary closes | All binary maps on the periodic eight-cell ring; tested through depth 6 |
| T∞ | 21 | Cumulative intrinsic local L/R/C vocabulary closes | Infinite one-dimensional binary lattice; tested through depth 4 |
| G | 10 | Full-gradient observation admits a radius-one factor for the ordered two-axis macro law | Infinite two-dimensional lattice; among the 66 replication-compatible sources |
| A | 14 | Axial replication is faithful and the axis-update order is independent | Local 1D→2D and 2D→3D interfaces; intersection of 66 compatible and 24 axis-order rules |

The explicit sets are:

- **T8:** 0, 1, 4, 8, 12, 19, 23, 32, 36, 51, 55, 64, 68, 72, 76, 90, 105, 128, 132, 136, 150, 165, 192, 200, 204, 219, 223, 232, 236, 239, 251, 253, 255.
- **T∞:** 0, 1, 4, 8, 12, 19, 36, 51, 55, 64, 68, 72, 76, 200, 204, 219, 223, 236, 239, 253, 255.
- **G:** 0, 142, 150, 170, 178, 204, 212, 232, 240, 255.
- **A:** 0, 128, 136, 150, 160, 170, 192, 204, 238, 240, 250, 252, 254, 255.

The four saved sources are [finite role summary](../../results/ternary_commutator_lift_20260909_summary.json), [intrinsic role summary](../../results/local_ternary_lift_20260909_summary.json), [full-gradient result](../../results/full_gradient_closure_20260910.json), and [axial result](../../results/guard_free_axial_lift_20260910.json). Their checksums and field selections are recorded in the [inventory output](../../results/constructor_inventory_20260910.json) and [extractor](../../scripts/extract_constructor_inventory.py).

T∞ is the intrinsic counterpart of the T8 experiment, with its own smaller depth budget. Absence from T∞ means no closure certified within that budget, not a proof of perpetual nonclosure. The [intrinsic note](2026-09-09-local-ternary-lift.md) separately proves why Rule90's radius growth exposes finite-ring identifications. Neither full L/R/C vocabulary closure nor axis-order independence is a prerequisite for every faithful dimensional representation.

## Every pairwise intersection

| Pair | Count | Rules |
| --- | --- | --- |
| T8 ∩ T∞ | 21 | 0, 1, 4, 8, 12, 19, 36, 51, 55, 64, 68, 72, 76, 200, 204, 219, 223, 236, 239, 253, 255 |
| T8 ∩ G | 5 | 0, 150, 204, 232, 255 |
| T8 ∩ A | 7 | 0, 128, 136, 150, 192, 204, 255 |
| T∞ ∩ G | 3 | 0, 204, 255 |
| T∞ ∩ A | 3 | 0, 204, 255 |
| G ∩ A | 6 | 0, 150, 170, 204, 240, 255 |

For completeness, T8 ∩ G ∩ A is {0,150,204,255}, while T∞ ∩ G ∩ A is {0,204,255}. Already G ∩ A={0,150,170,204,240,255}; a prediction that either triple is contained in those six is a set identity using inspected data. The original prediction was withdrawn.

These memberships concern different observations, constructors, substrates and budgets. They are not evidence that one shared dimensional tower satisfies all the criteria.

## Retain the nonlinear comparisons

| Rule | T8 | T∞ within budget | G | A |
| --- | --- | --- | --- | --- |
| 142 | No | No | Yes | No |
| 178 | No | No | Yes | No |
| 212 | No | No | Yes | No |
| 232 | Yes | No | Yes | No |

Axis-order independence excludes all four nonlinear gradient sources. It answers an additional symmetry question and needs a scientific reason to be imposed; it does not disqualify their gradient factors. Rule232's T8 membership also illustrates why finite-role closure should not silently stand in for intrinsic local closure.

## The precise intertwining question

Given source dynamics F on X, target dynamics H on Y, and an encoding E:X→Y, the equation is

$$
E\circ F=H\circ E.
$$

An exact dimensional representation supplies a dimension-changing local E and the relevant family and cadence. A commuting pair A,B on a shared space is the special case F=H=A and E=B, giving BA=AB. Taking E to be identity instead requires F=H.

There are 16 affine binary elementary rules in total, eight of them linear. The six rules in G ∩ A are affine controls in the present comparison. No irreducible linear representation framework has been supplied for the nonlinear configuration dynamics, so this inventory invokes no Schur inference about the form of invariants.

## Unrun direction: conserved densities

A conserved-quantity search remains separate work. Before running it, freeze the source domain, radius, coefficient ring, density grammar, treatment of time parity, equivalence of densities and independent verification. A wrapping-loop parity control belongs only if that representation can express it; arbitrary scalar additive-density grammars need not do so. This inventory supplies neither such a protocol nor a classification.

## Reproduce the bookkeeping

From the repository root, using only the Python standard library:

```sh
python scripts/extract_constructor_inventory.py --check results/constructor_inventory_20260910.json
```

The extractor reads the four saved JSON files, checks their internal count/intersection consistency, records SHA256 provenance and emits all six pairwise intersections plus both triples and the nonlinear comparison rows. CI checks the same extraction against the saved inventory. It never imports a CA evaluator or class labels.
