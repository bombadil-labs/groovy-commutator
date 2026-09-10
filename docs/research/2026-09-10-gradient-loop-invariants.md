# Loop information survives gradient evolution and dimensional lifting

The eight nonconstant sources in the full-gradient family preserve every wrapping-loop parity. The two constant sources erase those parities in one update. Native gradient execution agrees with independently evolved twisted binary potentials in all declared 1D, 2D, and 3D cases, and replication preserves the old loop bits while appending zero.

This supplies a specific invariant across the chosen dimensional tower. Its scope matters: loop bits belong to the declared periodic boundary topology, not to intrinsic dimension, prime factors, or a representation-independent physics. The [vision record](2026-09-10-dimensional-vision-and-interpretation.md) remains the guiding contract. The intervention question added in discussion is now a [separately frozen next experiment](protocols/gradient-intervention-costs-20260910.md), not a result of this audit.

Update 2026-09-10: the separately frozen [intervention audit](2026-09-10-gradient-intervention-costs.md) is now complete. It establishes minimum loop-changing support, inherited action costs, and native outcome counts under an explicit external action interface. The future-tense discussion below records the earlier freeze.

## Frozen setup and reproducibility

The [protocol](protocols/gradient-loops-and-dimensional-compatibility-20260910.md) is frozen at main commit `9e5de20f127f7a0047f3d6201abe7f83cd131981`. The standalone [verifier](../../scripts/verify_gradient_loops.py) was committed at `bf62df70e71c6a8c5825f430b78e6868735e69d1` before evaluation. The first execution passed without implementation corrections or protocol changes.

Sources remain 0,142,150,170,178,204,212,232,240,255. A macro update applies the original binary ECA along axis 0, then axis 1, and so on. The native state contains all d outgoing spatial differences per site. No class, visual behavior, or post-hoc rule selection enters the experiment.

The [canonical JSON](../../results/gradient_loops_20260910.json) contains every observed loop-sector transition by rule, shape, and tick; one four-tick certificate per initial loop sector and rule; geometry ranks; exact counts; and matching independent checksums.

```bash
python scripts/verify_gradient_loops.py > /tmp/gradient-loops.json
diff -u results/gradient_loops_20260910.json /tmp/gradient-loops.json
```

## Flat fields, periodic potentials, and loop sectors

Write a gradient field as a binary value on each positive oriented lattice edge. Flatness means XOR around every elementary square is zero. On the infinite cubical lattice, integrate along a path from an anchor: cancelling backtracks and interchanging adjacent coordinate steps changes no integral because each square has zero XOR. Thus a flat field has a binary potential unique up to global complement.

For a periodic field with periods $n_i$, define $h_i$ as the XOR along one full wrapping loop in direction i. Moving the loop transversely changes its sum by a strip of zero-curl squares, so its parity is independent of the base point. The potential on the infinite cover satisfies

$$
X(z+n_i e_i)=X(z)\oplus h_i.
$$

A periodic binary potential exists exactly when all the loop bits vanish. A nonzero loop vector is not a failure of local consistency: it describes a flat periodic edge field whose binary potential is twisted, rather than periodic with those same periods. It is still a gradient on the infinite cover. Consequently the existing local gradient law determines its update without choosing any values on curl-violating neighborhoods.

On a torus with N sites, an anchored tile potential contributes N-1 bits and its loop vector contributes d more. Taking differences, with the loop bit added across each seam, gives every flat edge field exactly once. Integration recovers the anchored potential and the loop bits, proving uniqueness and completeness. There are $2^{N-1+d}$ flat fields, separated into $2^d$ loop sectors of $2^{N-1}$ fields each.

The verifier independently row-reduces all plaquette constraints over binary arithmetic, checks that their nullspace has that dimension, and verifies injectivity, reconstruction, base-point independence, and global-complement ambiguity for every enumerated field. This avoids assuming the parameterization is exhaustive merely because its outputs are flat.

| Periodic shape | Stored edge bits | Plaquette rank | Flat fields | Loop sectors | Fields per sector |
| --- | ---: | ---: | ---: | ---: | ---: |
| (4) | 4 | 0 | 16 | 2 | 8 |
| (2,2) | 8 | 3 | 32 | 4 | 8 |
| (2,2,2) | 24 | 14 | 1,024 | 8 | 128 |

These finite shapes use lexicographic site ordering, with the last coordinate fastest. This word convention is explicit in the JSON and differs from some earlier local-window conventions. On period-two axes, the two positive edges between a pair of vertices are distinct stored edges of the periodic lattice; they are not collapsed into one undirected edge.

## Why the loop vector is preserved or erased

The [full-gradient factor theorem](2026-09-10-full-gradient-closure.md) supplies a constant complement response $\kappa$ for the macro law G:

$$
G(X\oplus 1)=G(X)\oplus\kappa.
$$

Translation covariance then gives, for either value of $h_i$,

$$
G(X)(z+n_i e_i)
=G(X\oplus h_i)(z)
=G(X)(z)\oplus\kappa h_i.
$$

Therefore the output loop vector is $h'=\kappa h$. The eight nonconstant sources 142,150,170,178,204,212,232,240 have self-dual axial composites in every dimension, so $\kappa=1$. Constants 0 and 255 have $\kappa=0$. This is an all-dimensional proof for arbitrary finite periods, independent of the small-torus audit and valid for every time by iteration.

| Source family | Loop evolution after any positive number of updates |
| --- | --- |
| Eight nonconstant self-dual sources | Every initial loop bit persists |
| Constants 0 and 255 | All loop bits become zero |

Preserving a loop vector does not preserve the full state, imply reversibility, or prevent loss of distinctions within a sector. It is one conserved observation, not a census of all invariants. The two constants remain controls, not post-hoc exclusions from the original ten-rule experiment.

## Native evolution and independent reference

At each site the native evaluator reads all outgoing edges based at Moore radius-one sites. It integrates the resulting connected local graph, evaluates the d+1 source windows needed for the next edge components, and discards its temporary potential. Every distinct rule/neighborhood is evaluated under both anchor choices, and the output must agree. Non-flat local neighborhoods are rejected; no ambient extension is invented.

The independent reference starts from a tile potential and declared twists. It constructs a Boolean source halo explicitly, including negative-coordinate and positive seam crossings, then contracts it with successive Boolean truth-table passes. It retains enough output halo to read the next edges across seams directly. Output twists are inferred from independently evaluated endpoint differences, not assigned from the loop-preservation prediction. The resulting tile and inferred twists supply the reference for the next tick. Constants therefore do not accidentally retain old twists.

The native evaluator uses integer rule indexing, recursive local evaluation, and graph integration. The reference uses Boolean truth tables and shrinking coordinate arrays; it does not call native integration or native local evolution. Both streams check their actual outputs against each other before checking the predicted invariant.

| Dimension | Local edge reads | Reconstructed potential vertices |
| --- | ---: | ---: |
| 1 | 3 | 4 |
| 2 | 18 | 15 |
| 3 | 81 | 54 |

In general these are $d3^d$ reads and $3^d+d3^{d-1}$ vertices. Radius one does not imply dimension-independent storage or processing. Memoization saves repeated local work in this finite audit: 1,068 distinct integrated neighborhoods and 10,680 rule/neighborhood evaluations, each tested with both anchors. This is not a claim to have enumerated every 3D local neighborhood.

## Exact execution counts and dimensional interfaces

All 1,072 initial fields are run under all ten rules for four ticks: 10,720 initial rule/field cases and 42,880 base macro updates. Repeated states at later ticks count as checks, not as independent initial states.

For the interfaces, P copies existing edge components along a new axis of period two and appends a zero component. Both (4) to (4,2) and (2,2) to (2,2,2) are tested over their entire source ensembles. Native target evolution is checked against both embedded source evolution and a separate target twisted-potential reference. Every target plaquette and wrapping loop is checked after every tick.

| Audit | Count |
| --- | ---: |
| Base initial rule/field cases | 10,720 |
| Base macro updates | 42,880 |
| Base output-component comparisons | 995,840 |
| Interface initial rule/field cases | 480 |
| Interface ticks, each computing source and target updates | 1,920 |
| Interface target-component comparisons | 40,960 |
| Discrepancies | 0 |

The inherited loop vector becomes $(h,0)$ under P. Binary replication intertwining on the infinite cover, followed by the gradient factor, proves $Q_{d+1}P=PQ_d$ for these flat fields. The finite audit verifies implementations at two interfaces; it does not substitute a finite census for the all-dimensional proof.

Matching native/reference SHA-256 streams are `a46b0fc488c1ab585cb709ae90e40ee486ea4eab68113249133d4f2b5fc34833` for base evolution and `b8f631e6267a0860e1beb4dac6f1e22398399fb21db0223b70b645c3a878e2a8` for interfaces. The canonical result file SHA-256 is `01ee83d4ca970c071cf8b6761e66d62209222b9e3c56eae61fc8c1ceb9e3b0d5`.

## Persistence is not yet revisability

The user proposed a third axis alongside erased history and possible futures: what can actually be steered. This experiment establishes persistence of specified information; it contains no action interface or controller, and therefore measures neither intervention power nor empowerment.

The next question is whether that persistent information is affordably revisable. The [next frozen protocol](protocols/gradient-intervention-costs-20260910.md) declares edits as XOR masks that keep edge fields flat, counts changed edges and touched sites, and distinguishes edits inside the inherited image from native target edits. It compares distinguishable terminal fields with distinguishable loop vectors under a known initial state and one explicitly bounded intervention.

A periodic potential edit has zero loop change. Changing a loop sector requires a different class of flat edit. The next protocol will test its minimum support and the cost of lifting an intervention. It allows leaving the replicated image while staying within the defined flat-state domain; it does not silently choose dynamics for arbitrary curl defects. Simultaneous edit support is not an implementation of local sequential control, and no endogenous mechanism has yet been supplied.
