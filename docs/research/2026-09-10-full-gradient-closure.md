# Both spatial differences restore closure for four nonlinear rules

Keeping horizontal and vertical differences gives an autonomous gradient law for **10 of the 66 compatible axial ECA sources**, compared with six for transverse differences alone. The newly admitted rules are **142,178,212,232**: majority functions with zero or one input negated. The other 56 sources still have complete identical gradient observations with different next gradients. Their remaining global complement ambiguity is causally consequential.

This is a separately declared observation comparison under the same ordered binary laws. It retains more information and costs two component bits per site. It does not retroactively change the [transverse-only result](2026-09-10-transverse-difference-closure.md), select a canonical representation, or supply a preferred law outside the gradient image. The [vision and interpretation contract](2026-09-10-dimensional-vision-and-interpretation.md) remains the research guide.

## Frozen experiment and reproducibility

The [protocol](protocols/full-gradient-closure-20260910.md) is present at main commit `e1a1ef7002615977c1cbb5477dc051d38765009e`. The [verifier](../../scripts/verify_full_gradient_closure.py) was committed at `33d19a2ef629eeacdbea4ec4ccfdf3749e1aaffc` before evaluation. No implementation corrections or protocol deviations were needed. Full-field extension checks, including the omitted corner, were part of this frozen implementation.

Keep $G_r=F_{r,2}\circ F_{r,1}$ for 0,255 and every even source word from 128 through 254. Observe

$$
J(X)=(T_x(X),T_y(X)),\qquad
T_i(X)(z)=X(z)\oplus X(z+e_i).
$$

Here gradient means nearest-neighbor spatial differences. The earlier outgoing-time derivative $D=I\oplus F$ is a different observation.

Test $J\circ G_r=Q_r\circ J$ on every infinite binary field, with radius-zero and radius-one candidate caps. The [canonical JSON](../../results/full_gradient_closure_20260910.json) contains exact rule lists, complete caps on reachable neighborhoods, all first failure witnesses, complement checks, finite aliasing, full-field certificates, and independent checksums.

```bash
python scripts/verify_full_gradient_closure.py > /tmp/full-gradient-closure.json
diff -u results/full_gradient_closure_20260910.json /tmp/full-gradient-closure.json
```

## Exact classification

The passing source set is

```text
0,142,150,170,178,204,212,232,240,255
```

All 10 close at radius one. Exactly 0,204,255 close at radius zero. Every other source in the 66-rule domain has a full-field obstruction, so a larger observation neighborhood cannot rescue it.

Let $M(l,c,r)$ be the majority of its three binary inputs. The comparison is:

| Source rule | Source function | Transverse-only closure | Full-gradient closure |
| --- | --- | --- | --- |
|0,255 | Constant | Yes | Yes |
|170,204,240 | Copy right, center, left | Yes | Yes |
|150 | $l\oplus c\oplus r$ | Yes | Yes |
|142 | $M(1-l,c,r)$ | No | Yes |
|178 | $M(l,1-c,r)$ | No | Yes |
|212 | $M(l,c,1-r)$ | No | Yes |
|232 | $M(l,c,r)$ | No | Yes |
|Remaining 56 tested sources | Other compatible ECA functions | No | No |

For the nonlinear rules, the closed update jointly uses both derivative components. Applying the old source rule separately to each component is not the claimed construction. The underlying axial law is still ordered; admitting both components does not make these four source operators commute across axes. The earlier [axis-order census](2026-09-10-guard-free-axial-lift.md) remains valid.

## The information that remains hidden

If $J(X)=J(Y)$, their XOR is unchanged along both lattice directions. Because the square lattice is connected,

$$
Y=X\quad\hbox{or}\quad Y=\overline X.
$$

Thus the complete observation forgets only a global complement choice. The transverse-only observation forgot an independent baseline bit per column. This change of information, rather than a relabeling of the same observation, permits the four additional nonlinear sources.

The gradient law closes precisely when that remaining ambiguity stays invisible after evolution. The criterion below establishes this on the infinite lattice, without promoting finite non-conflict to a global theorem.

## A complete local complement criterion

For a binary finite-radius CA with local rule $g$, define

$$
k(p)=g(p)\oplus g(\overline p).
$$

If $k$ is constant over all source patches, $G(\overline X)=G(X)\oplus k$ everywhere. The next gradients therefore agree for both representatives of every observation fiber. Constant value0 and constant value1 both suffice; the former includes constant laws and must not be conflated with self-duality.

Conversely, suppose $k$ takes both values. Put witnessing patches far enough apart in one infinite configuration that their source windows are disjoint. The field $G(X)\oplus G(\overline X)$ then takes different values at those two sites. Along a lattice path between them, some edge has unequal endpoint values. Therefore the two next gradients differ, despite $J(X)=J(\overline X)$. No function of the complete gradient alone can predict both.

This proves an exact factor criterion. For the nonconstant sources in the current66-rule family, uniform zero and uniform one are fixed, so $k$ can be constant only with value1. The condition is **self-duality**:

$$
G(\overline X)=\overline{G(X)}.
$$

Self-duality of the source ECA implies self-duality of every axial pass and their composition. The converse follows here by restricting the two-dimensional law to copied one-dimensional inputs: exact replication intertwining recovers the original source law, so self-duality of the composite forces self-duality of the source.

The eight self-dual sources preserving both uniform states are142,150,170,178,204,212,232,240. One complement pair of truth-table entries is fixed by the uniform-state requirement; the other three pairs each admit two choices, giving eight. Adding constants0 and 255 gives the 10-rule classification, independently explained by the exhaustive local audit.

## How the radius-one gradient law is constructed

The three overlapping 3-by-3 source windows needed for $J(G(X))(0,0)$ occupy a4-by-4 block minus its upper-right corner:15 source bits. The nine observed sites each carry two outgoing differences, for 18 observation bits. Their edge graph is connected, so a realizable observation determines the 15 source bits up to a common complement.

Integrate those local differences after choosing the corner source value to be zero. Evaluate the three source windows and take the two output differences. For a passing rule, changing that temporary corner choice complements all reconstructed source bits and leaves the output differences unchanged. This is a local evaluation convention, not a retained absolute source bit or a prepared guard row.

The local edge graph has four independent plaquette constraints. Exactly $2^{14}=16,384$ of its $2^{18}=262,144$ possible bit patterns are realized; each has two source preimages. The verifier checks all 32,768 source assignments for each rule. Caps are encoded only on reachable neighborhoods: index i represents the gradient of source word2i, fixing bit0 to zero, and each table entry is a packed two-bit output. Radius-zero tables use the current central pair as their index.

The direct two-dimensional evaluator reconstructs15 local source values from 18 edges and evaluates three G windows, each requiring four ECA lookups in the naive axial tree. The saved reachable cap instead uses4,096 packed bytes per passing radius-one rule, with a declared observation-to-table index. These are explicit implementation choices rather than constant processing across dimensions.

The 245,760 unreachable neighborhoods remain outside this claim. In the unrestricted radius-one four-symbol CA grammar, their two output bits leave $2^{491,520}$ ambient completions agreeing on the full gradient image for each passing source. This is a count of unconstrained local truth tables, not of symmetry-respecting or physically preferred realizations. We have not selected one of those completions.

## Every failure has a complete-field witness

A failed radius-one budget supplies two15-bit patches with equal complete local gradients and different next central pairs. Connectedness forces those source patches to be complements. Fill the omitted corner with0 in the first and 1 in the second, then repeat the resulting4-by-4 tiles across the plane. The complete sources remain complements and their full gradient fields agree.

The three causal windows lie inside the original15-site support. Consequently the certified different next central pairs survive the extension. The verifier independently checks every output cell, all current and next gradient components, both omitted-corner values, and the central predictions for all 56 failed sources. This proves failure of every deterministic update on J alone, including nonlocal ones.

For example, AND128 has local source witnesses16383 and 16384, completed to periodic source words16383 and 49152. Their common full gradient word is3835691008; next gradient words are43690 and 0. The central next pairs are2 and 0, where the low bit is the horizontal component and the high bit the vertical one. OR254 uses the same input pair and reverses those two next outputs.

## Finite controls and independent audit

On the 3-by-3 periodic lattice,12 sources appear functional: the true10 plus AND128 and OR254. Their outputs become uniform on that torus, hiding the obstruction. Majority232, also uniform on that small torus, now has a genuine infinite-lattice closure established separately. The finite dataset retains these distinctions.

The primary integer truth-table pipeline is audited by a Boolean shrinking-array evaluator memoized on Boolean tuples, with separate coordinate extraction from every15-site source. The memoized tables cover all 512 G windows per source; memoization avoids repeating identical Boolean contractions while every larger source patch is checked. Native periodic passes are independently compared with recursive local evaluation.

| Audit | Exact amount |
| --- | ---: |
|15-site source windows | 2,162,688 |
|Source-window/budget checks, R=0 and 1 | 4,325,376 |
|Independent Boolean G windows | 33,792 |
|Complement patch pairs | 33,792 |
|3-by-3 periodic macro updates | 33,792 |
|Periodic output-cell comparisons | 304,128 |
|Passing-cap site predictions | 59,904 |
|Passing-cap component predictions | 119,808 |
|4-by-4 witness-extension macro updates | 112 |
|Witness-extension output-cell comparisons | 1,792 |

All primary and independent streams agree. Their local SHA-256 is `015d77e9049764d37b81041c3e86e7729c21f06594ae299ab976c3a6961d5ffa`; the complement, periodic, and extension hashes are included in the canonical result. Its complete file digest is `9a137928c87222a7414bd56a172f49f026d5593944d1903c47f6be01a699085b`.

## What continues through the dimensional tower

There is an analytic consequence beyond the two-dimensional computation. Write $J_d$ for all d nearest-neighbor differences. Its full-field fibers on the connected infinite lattice are again global-complement pairs. Each of the eight self-dual sources has self-dual axial composites in every dimension; the two constants also factor. The same local integration argument constructs $Q_{r,d}$ on valid gradient neighborhoods with Moore radius at most one.

For replication R along a new axis, its induced gradient embedding P copies the old components and appends a zero component:

$$
J_{d+1}R_d=P_dJ_d.
$$

Combining this with binary replication intertwining gives

$$
Q_{r,d+1}P_d=P_dQ_{r,d}
$$

on valid gradient fields. This is a proof consequence, not an exhaustive computation in higher dimensions. The gradient tower retains the source dynamics modulo a global bit flip; it does not recover the absolute binary source state. Storage is d component bits per site, and local integration/evaluation work grows with dimension. Replication and the chosen interpretation remain supplied resources.

## The next question: loop information

Local gradient consistency and a periodic source's global consistency are different. On a wrapped lattice, XOR differences around a full wrapping loop can carry information invisible to a single plaquette. The [next frozen protocol](protocols/gradient-loops-and-dimensional-compatibility-20260910.md) will examine that information, the actual dimensional gradient implementation, and the replication interfaces. It is unrun.

This is a concrete candidate for the user's question about invariants across the tower, with its boundary topology declared. It will distinguish loop parities, local curl, and representability by a periodic source. It will not identify those boundary sectors with intrinsic dimension, prime factors, or spontaneous organization, and it requires no arbitrary update on curl-violating neighborhoods.
