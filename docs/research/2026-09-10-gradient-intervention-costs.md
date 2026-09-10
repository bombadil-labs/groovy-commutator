# Persistent loop information has an exact intervention cost

The frozen audit is complete. A simultaneous flat edit can change any chosen loop vector, and the least number of flipped stored edges is exactly the sum of the transverse cross-section sizes for the changed directions. Replication preserves the edited dynamics but multiplies edit support by the added period. Native higher-dimensional actions can select additional outcomes beyond those available through inherited actions.

These conclusions use a known initial gradient field and an externally supplied, simultaneous action interface. They establish costed revisability under that contract; they do not supply an endogenous controller. The finite full-field outcome counts also have a substantial geometry limitation: on the tested period-two tori, every nonconstant source acts bijectively on flat fields. That finite result must not be read as general reversibility of the nonlinear source laws.

## Frozen contract and reproducibility

The [protocol](protocols/gradient-intervention-costs-20260910.md) was frozen at `f69b156ccc5fb7ff75ab4c2db95924dc87cc5d90`. The [verifier](../../scripts/verify_gradient_interventions.py) was committed at `8fe109648038792d341d1f1e59c818900f110d3b` before evaluation. The first run passed without corrections or protocol deviations. The original protocol remains unchanged as a historical freeze.

Sources are 0,142,150,170,178,204,212,232,240,255. The law is the existing native full-gradient factor of ordered axial ECA evolution. Initial states and actions range over every flat edge field on (4), (2,2), and (2,2,2). An action XORs one flat mask into the initial field; evolution then runs unperturbed. Horizons are 0,1,4 macro updates. Primary budgets charge flipped stored edge bits; distinct sites owning those edges are a separate cost. Period-two positive edges remain distinct stored edges, even when their endpoints are the same pair of vertices.

The [canonical JSON](../../results/gradient_interventions_20260910.json) preserves all 1,072 masks with costs and loop changes, every sector's minimum costs and witnesses, all outcome-count distributions and extremal initial states at every budget, terminal image sizes by loop sector, and both dimensional interfaces. All counts are exact integers.

```bash
python scripts/verify_gradient_interventions.py > /tmp/gradient-interventions.json
diff -u results/gradient_interventions_20260910.json /tmp/gradient-interventions.json
```

Mask enumeration by anchored potentials and twists agrees word for word with an independent nullspace enumeration using coordinate-set plaquette equations and low-pivot binary row reduction. Their ranks are 0,3,14; the flat mask counts are 16,32,1,024.

Every native one-step transition is checked against the existing independent Boolean twisted-potential evaluator. Those complete tables are composed to the declared horizons. For every initial state and mask, the primary method finds minimum action cost per endpoint; the reference method instead grows actual reachable-outcome sets as budgets admit actions, using separately counted mask bits. Both full-field and loop-vector counts agree.

| Audit | Exact count |
| --- | ---: |
| Base one-step native/reference comparisons | 10,720 |
| Initial rule/state/action combinations | 10,498,560 |
| Base endpoint queries at horizons 0,1,4 | 31,495,680 |
| State/budget/observation count comparisons | 1,558,080 |
| Interface one-step native/reference comparisons | 480 |
| Interface action support checks | 48 |
| Interface endpoint checks | 38,400 |
| Discrepancies | 0 |

Cached table queries are counted as queries, not millions of independent CA simulations. The two evaluators use different evolution algorithms but share the declared representation and existing geometry helpers; this is computational cross-checking, not a separate research replication.

## Minimum support for changing a loop sector

Let the rectangular torus have periods $n_1,\ldots,n_d$ and $N=\prod_i n_i$ sites. Write $h(\delta)$ for the wrapping-loop vector of a flat action mask. Then

$$
\min_{\delta:\,h(\delta)=h}|\delta|
=\sum_{i:h_i=1}\frac{N}{n_i}.
$$

For the lower bound, fix a changed direction i. Its $N/n_i$ disjoint parallel wrapping loops must each contain an odd number of flipped i-edges, hence at least one. Different directions use disjoint stored edge components, so their bounds add. For attainment, flip every i-edge crossing one fixed seam for each changed direction. Every elementary square meets each selected seam an even number of times, so the resulting mask is flat. It has exactly the required loop vector and exactly the stated support.

This is an analytic statement for rectangular periodic lattices. The exhaustive census checks the prediction on the three frozen shapes; it does not infer the general formula from them. If all side lengths are L, changing k loop bits costs $kL^{d-1}$ edge flips. A loop bit may therefore persist indefinitely while requiring support across a whole transverse section to revise.

| Shape | Edge cost to change k loop bits | Minimum touched sites for any nonzero loop change |
| --- | ---: | ---: |
| (4) | k, with k at most 1 | 1 |
| (2,2) | 2k | 2 |
| (2,2,2) | 4k | 4 |

The site column reports the finite census, separately from the general edge theorem. For example, on (2,2) a two-bit loop change has minimum edge cost four. There are eight edge-minimizing masks, with first word 39. Only two masks minimize touched sites at two, with first word 60. Thus even a deterministic first edge-minimizing witness need not minimize the other resource. On (2,2,2), changing all three loop bits costs twelve edges but can use four owning sites.

Zero-loop masks are precisely gradients of periodic potential edits. They can change the field within a sector but cannot change its loop vector. There are 7,7,127 nonzero zero-loop masks respectively; the no-op is separately counted. A global complement of the potential produces the no-op gradient mask.

## Stable loop choices and distinct full-field futures

For known initial state s, budget b, and terminal observation O, define

$$
M_{O,t}(s,b)=\left|\{O(Q^t(s\oplus\delta)):\delta\text{ flat},\ |\delta|\le b\}\right|.
$$

For this deterministic, known-state, one-shot hard-budget channel, its capacity is $\log_2 M_{O,t}(s,b)$ bits. Determinism gives $I(A;O)=H(O)$; the upper bound is attained by choosing one admissible action for each distinct endpoint and making those endpoints equiprobable. This does not assign a prior to hidden states or solve a feedback or average-cost problem. The artifact reports the primary integer M, avoiding an unspecified entropy ensemble.

For the eight self-dual nonconstant sources, the terminal loop vector is $h(s)\oplus h(\delta)$ at every horizon. Consequently the number of reachable loop vectors is exactly

$$
\left|\left\{h\in\{0,1\}^d:\sum_{i:h_i=1}N/n_i\le b\right\}\right|.
$$

It is independent of initial state and time. Constants 0 and 255 send every edited field to the zero gradient after one update, leaving one full-field and one loop-vector endpoint at every positive horizon, irrespective of budget. At horizon zero the law has not acted, so constants have the same action repertoire as other sources.

Full-field observations distinguish more than loop vectors. On the four-site ring at horizons 1 and 4, the unlimited image contains:

| Sources | Full fields | Fields in loop sector 0 / 1 |
| --- | ---: | --- |
| 150,170,204,240 | 16 | 8 / 8 |
| 142,212 | 12 | 4 / 8 |
| 178,232 | 8 | 4 / 4 |
| 0,255 | 1 | 1 / 0 |

Thus loop conservation does coexist with loss of within-sector distinctions. Budget-limited counts can also depend on the initial state. For Rule232 at budget one, horizons 1 and 4 have three reachable full fields for eight initial states, four for four states, and five for four states. The corresponding loop-vector count is always two. The artifact preserves these distributions rather than replacing them with one favorable initial state.

On (2,2) and (2,2,2), all eight nonconstant sources preserve distinctness of every flat field. Their full-field outcome counts are therefore simply the number of admissible masks below budget, independent of state and horizon. For (2,2) the counts at budgets 0 through 8 are 1,1,5,5,27,27,31,31,32. For (2,2,2):

| Edge budget | Full-field outcomes | Loop-vector outcomes |
| --- | ---: | ---: |
| 0–3 | 1 | 1 |
| 4–5 | 7 | 4 |
| 6–7 | 15 | 4 |
| 8–9 | 126 | 7 |
| 10–11 | 246 | 7 |
| 12–13 | 778 | 8 |
| 14–15 | 898 | 8 |
| 16–17 | 1,009 | 8 |
| 18–19 | 1,017 | 8 |
| 20–23 | 1,023 | 8 |
| 24 | 1,024 | 8 |

This table covers horizons 0,1,4 for nonconstant sources, and horizon zero only for constants.

### Why the period-two result is special

This explanation is an analytic interpretation after the frozen audit, not a new selection criterion. Along a period-two axis of a twisted potential, left and right inputs satisfy $l=r\oplus h_i$. Rule232 is majority(l,c,r); rules178,142,212 are majority with the center, left, or right argument complemented respectively. Substituting the relation reduces each to a center or neighbor bit, possibly complemented. Rule150 reduces to $c\oplus h_i$; 170,204,240 already select an input. Thus each axial pass, within a fixed loop sector, is a translation or identity followed possibly by a global complement. The loop sector is preserved, and these operations are invertible. Their gradient factors are consequently bijections on each sector.

The 2D/3D counts are exact but largely reflect action geometry on these small tori. They do not demonstrate general nonlinear reversibility, and a larger-period comparison would need a separate protocol. The four-site ring already shows within-sector loss. No larger-period sweep was added to this unit.

## Inherited actions and native higher-dimensional choices

P replicates every old edge component along an added period-two axis and appends zero. On both (4) to (4,2) and (2,2) to (2,2,2), all masks satisfy

$$
h(P\delta)=(h(\delta),0),\qquad |P\delta|=2|\delta|.
$$

Touched-site count also doubles. For an added period m, both costs multiply by m analytically: each changed stored edge and each owning site has m distinct copies. The extra gradient component is zero.

Linearity of replication gives $P(s\oplus\delta)=Ps\oplus P\delta$. Together with the proved intertwining identity, this gives

$$
Q_{d+1}^{t}(Ps\oplus P\delta)=P(Q_d^{t}(s\oplus\delta)).
$$

All 38,400 frozen interface endpoint checks agree with independently evolved target potentials. This preserves the effect of inherited actions at the translated budget mb; it does not identify native capabilities at the same numerical budget.

The (2,2,2) native census has 1,024 masks. Only 32 are inherited from (2,2). Of the other 992, 512 change the new loop bit and 480 leave it zero while still lying outside the replicated image. Zero new loop change therefore does not imply inherited action geometry.

At inherited initial states, the following counts hold for every nonconstant source and each declared horizon:

| Source budget | Target budget | Inherited / native full-field outcomes | Inherited / native loop-vector outcomes |
| --- | --- | --- | --- |
| 2 | 4 | 5 / 7 | 3 / 4 |
| 4 | 8 | 27 / 126 | 4 / 7 |
| 6 | 12 | 31 / 778 | 4 / 8 |
| 8 | 16 | 32 / 1,009 | 4 / 8 |

The comparison holds the target cost budget fixed while changing the available action family. Native masks do not beat the replicated minimum edge cost for a specified old loop change: both need four edges per changed old bit. They offer new loop choices and additional within-sector outcomes. The full native frontier on (4,2) was not enumerated; that interface is checked only on inherited states and actions.

## Certificates, limits, and handoff

The canonical JSON SHA-256 is `89093341369ef505d6bb2d2a53cd7be00864bbb035adcd4072360c006c3d3630`. Matching primary/reference streams are:

| Stream | SHA-256 |
| --- | --- |
| One-step transitions | `d0d5016e82c35b8ff5d1a0252ab17ef1557c635b2ea888a9adfb7c74eeb9bc28` |
| Base endpoints | `2e19ff2bfa0637d75ca1e5a112b899e40fe39e85451fc87bfff8eb62254c2c78` |
| Budget counts | `16b82d6a64667c7cbdec3e085f467bb1f25a7613aa60dbefe0c9c77f81b2a881` |
| Interface endpoints | `41c489732279edf7b08e2b3f27c43b925a9e695ca1ab93f9e84f076f389283fe` |

Storage remains d bits per site. The ability to apply a distributed flat mask at once is supplied. This audit prices final simultaneous support, not a sequence of local actuator moves, transient curl defects, observation uncertainty, controller memory, preparation, or repair. It does not establish endogenous organization, intrinsic dimensional ancestry, or a canonical identification of rules with state. The [vision record](2026-09-10-dimensional-vision-and-interpretation.md) remains open, and Class IV plays no role in construction or scoring.

The user requested that this unit be finished and then research execution pause for the agreed issue queue. No new experiment is frozen or begun here. The signed agreement comments, rather than withdrawn claims in original issue bodies, define that queue:

| Issue | Remaining agreed work |
| --- | --- |
| [#61](https://github.com/bombadil-labs/groovy-commutator/issues/61#issuecomment-5622836331) | Shared closure/fiber synthesis and missing knowledge provenance. |
| [#62](https://github.com/bombadil-labs/groovy-commutator/issues/62#issuecomment-5622836947) | Archive the reproduced finite successor-set example with correlation and ensemble limits. |
| [#63](https://github.com/bombadil-labs/groovy-commutator/issues/63#issuecomment-5622837474) | Freeze the distinct hidden-state static intervention-channel comparison. |
| [#64](https://github.com/bombadil-labs/groovy-commutator/issues/64#issuecomment-5622838193) | Freeze and implement the agreed conservative online suffix learner. |
| [#65](https://github.com/bombadil-labs/groovy-commutator/issues/65#issuecomment-5622838631) | Archive the reproduced rule-field relabeling and transformed transport example. |
| [#66](https://github.com/bombadil-labs/groovy-commutator/issues/66#issuecomment-5622839348) | Descriptive cross-constructor inventory and precise intertwiner framing. |
| [#67](https://github.com/bombadil-labs/groovy-commutator/issues/67#issuecomment-5622839866) | Freeze the bounded second-lift comparison under two declared completions. |
| [#68](https://github.com/bombadil-labs/groovy-commutator/issues/68#issuecomment-5622840298) | Promote the four resonance distinctions to Concepts without upgrading evidence. |

None is a no-op: each retains concrete writing, archival, editorial, or experimental work. Agreement on scope is not completion. This audit is related to #63 and supplies the requested preceding checkpoint for #67, but completes neither issue. Future PRs should include `Closes #N` only when they complete the issue's agreed scope; genuinely redundant issues can instead be closed with a signed explanation.
