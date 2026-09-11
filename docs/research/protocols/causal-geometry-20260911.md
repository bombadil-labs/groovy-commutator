# Protocol: bounded-distortion causal geometry — 2026-09-11

**Status:** frozen before implementation or evaluation. No quantity defined below has been computed as a new result.  
**Program:** *Dimensional Closure and the Commutator Lift*, theorem-first follow-on to finite-width packing and the intervention-axis unit.  
**Authored by:** Codex / OpenAI GPT-5.6 Sol. **Protocol review:** pending Claude Code / Fable Gate 1.  
**Tracking:** issue #111. **Dependency:** gathering PR #114 (uniform local intervention axis) must receive Claude/Fable Gate-2 sign-off and merge to `main` before this unit is reported as the Program's next accepted step. Gate-1 review of this theorem protocol may proceed while that dependency is pending. No experimental implementation is authorized by this protocol.

## 0. Process note

A one-character placeholder for this file was accidentally committed directly to `main` at `03a8cba` before the gathering branches were created. It was immediately deleted at `b229606`, before any protocol content, implementation, evaluation, or scientific choice existed. The mistake is retained in history rather than hidden. The actual frozen protocol begins on the dedicated protocol branch and follows the gathering/sub-PR workflow.

## 1. Why this unit

The preceding dimensional units isolated two representation resources without yet producing a causal two-dimensional logical lattice:

1. finite-width packing shows that one bounded transverse stack can be hidden in a one-dimensional product alphabet, while an unbounded independently variable family defeats a fixed total-capacity budget;
2. the intervention-axis unit tests a different contract: translated separated-strip actions remain constant-support and independently addressable while a one-dimensional target with a fixed common endpoint window eventually runs out of local action capacity.

Neither statement says that the logical dynamics has a second **causal adjacency direction**. In the accepted separated-strip construction, channels evolve independently. This protocol therefore asks a sharper theorem question before another architecture search:

> **What uniform large-scale geometry must an encoding preserve before a nominal or intervention-addressable transverse coordinate counts as a causal spatial axis under this Program's representation contract?**

The candidate contract is bounded-distortion causal geometry. It deliberately distinguishes exact symbolic simulation from preservation of spatial adjacency.

## 2. Standard mathematical context

The contract uses the ordinary graph metric and the standard quasi-isometry/coarse-geometry idea that large-scale distances are preserved up to multiplicative and additive constants. Polynomial growth type is a quasi-isometry invariant for finitely generated groups; in particular `Z^d` has growth degree `d`. Asymptotic dimension is another quasi-isometry invariant with `asdim(Z^d)=d`. Contextual references:

- Clara Löh, *Geometric Group Theory: An Introduction*, Springer Universitext (2017), Chapter 6, especially the quasi-isometry invariance of growth type and the `Z^d` examples. DOI: `10.1007/978-3-319-72254-2`.
- G. Bell and A. Dranishnikov, “Asymptotic Dimension,” *Topology and its Applications* 155 (2008), arXiv:`math/0703766`.

The primary theorem below does **not** rely on importing either result as a black box. It gives an elementary finite-ball counting proof specialized to strip graphs, so the exact resource contract is visible.

## 3. Graph objects

For width `w >= 1`, let

`G_w = Z × {0,...,w-1}`

with the nearest-neighbor grid graph: `(x,y)` is adjacent to `(x±1,y)` when present and to `(x,y±1)` when present. Let `d_w` be its shortest-path metric. The target graph is the ordinary integer line `Z` with metric `d_Z(a,b)=|a-b|`.

`G_infty = Z^2` is the corresponding unbounded square lattice.

These graphs are **logical causal/intervention-site graphs**, not automatically the physical-cell graph of a CA. A represented system instantiates `G_w` only when its declared logical sites are dynamically closed and the two graph directions correspond to declared local causal or intervention adjacencies. Physical proximity by itself is not enough.

## 4. Uniform bounded-distortion contract

For constants `lambda >= 1` and `epsilon >= 0`, a map

`f_w : V(G_w) -> Z`

is an admissible bounded-distortion site representation when for all logical sites `u,v`,

`(1/lambda) d_w(u,v) - epsilon <= |f_w(u)-f_w(v)| <= lambda d_w(u,v) + epsilon`.

No injectivity is required: finite local packing is allowed. No coarse-surjectivity condition is required for the obstruction below, so the target may contain arbitrary unused space.

A width family is **uniformly geometry-packable into one dimension** when one fixed finite pair `(lambda,epsilon)`, independent of `w`, admits such a map for every width.

This is a geometry-preservation contract only. It says nothing by itself about state alphabet size, dynamics, decoder semantics, self-assembly, or whether a representation is physically preferred.

## 5. Frozen theorem claims

### C1 — every fixed finite strip is quasi-one-dimensional when constants may depend on width

For each fixed finite `w`, the column projection

`p_w(x,y)=x`

obeys the contract with `lambda=1` and `epsilon=w-1`.

Proof frozen before review: for `u=(x,y)`, `v=(x',y')`,

`d_w(u,v)=|x-x'|+|y-y'|`,

so

`d_w(u,v)-(w-1) <= |x-x'| <= d_w(u,v)`.

Thus each individual finite-width strip is quasi-isometric to `Z`, with an additive constant that is allowed to grow with width. This is the coarse-geometry version of the earlier column-packing control.

### C2 — no uniform bounded-distortion constants collapse all widths to `Z`

There is no fixed finite `(lambda,epsilon)` satisfying the contract for every `G_w`.

Elementary proof frozen before review. Assume fixed `(lambda,epsilon)` exists and put

`D = ceil(lambda * epsilon)`.

If two source vertices have the same target site, the lower distortion bound gives `d_w(u,v) <= lambda*epsilon <= D`. Therefore every target site has at most

`M(D) = 1 + 2D(D+1)`

source preimages, because a fiber fits inside an `L1` ball of radius `D` in the square grid.

Now choose any integer radius `r` and a width `w >= 2r+1`, with center `c=(0,r)` away from both transverse boundaries. Its radius-`r` source ball is the full square-lattice diamond,

`|B_w(c,r)| = 1 + 2r(r+1)`.

The upper distortion bound sends this entire ball into the integer interval of radius `ceil(lambda*r + epsilon)` about `f_w(c)`, containing at most

`2 ceil(lambda*r + epsilon) + 1`

target sites. Since each target site has at most `M(D)` preimages,

`1 + 2r(r+1) <= M(D) [2 ceil(lambda*r + epsilon) + 1]`.

The left side grows quadratically in `r`; the right side grows linearly. For sufficiently large `r` this is impossible. Hence no constants independent of width exist.

This is a uniform-family obstruction. It does not contradict C1, because C1's additive constant grows as `w-1`.

### C3 — exact column packing need not preserve causal geometry

The earlier product-alphabet map that packs an entire width-`w` column into one one-dimensional symbol can preserve a local strip CA exactly as a symbolic dynamical system. Its induced site projection is exactly `p_w(x,y)=x` and therefore carries additive distortion `w-1`.

So exact simulation and geometry preservation are separate contracts. Column packing remains a valid representation; it simply fails the **uniform** causal-geometry contract as `w` grows.

### C4 — growing correction tuples do not instantiate a second causal direction by themselves

For the inherited Rule32 correction tower, the represented logical base remains indexed by `x in Z`. Additional correction coordinates are fields attached to the same longitudinal site. Unless an independent adjacency/intervention graph among those coordinates is declared and dynamically realized, the causal-site graph is still one-dimensional.

This is a representation statement, not a theorem that correction variables can never be spatial under another architecture.

### C5 — separated strips supply intervention addressability but not transverse causal adjacency

The already-accepted Research018 many-strip theorem evolves every separated channel by Rule90 independently. At the two-fine-tick coarse cadence, a logical output at `(i,r)` depends on `(i-1,r)` and `(i+1,r)` in the **same** channel and on no neighboring channel.

Therefore the causal graph of `m` separated logical strips is a disjoint union of `m` copies of `Z`, not the connected grid strip `G_m`. The intervention-axis result, if accepted on #114, adds an unbounded translated family of local actions; it does not silently add transverse causal edges.

This is an important negative control: independent addressability and two-dimensional causal geometry are complementary properties, not synonyms.

### C6 — touching strips have transverse physical influence but fail the current closed logical graph

Research018's touching-strip control (`g=0`) has genuine cross-channel influence, but after two fine ticks **47 of 64** local logical input assignments leave the declared two-strip code; only 17 remain valid. Therefore the current two-bit-per-column representation does not define a total closed logical `G_2` dynamics.

Research019 further proves that one specified adjacent-strip perturbation launches an outward front whose vertical span grows without bound, ruling out containment by that note's fixed-height horizontal-band representation against the prepared background. This does not rule out every enlarged representation.

The boundary is therefore sharp:

- separated strips: closed and independently addressable, but no transverse causal coupling;
- touching strips: transverse coupling exists, but the current logical code is not closed;
- a future positive causal-axis witness must achieve both closure and a connected transverse causal graph under a frozen representation.

## 6. Optional finite checks — not a primary experiment

No new scientific census is required for C1–C6. They are proofs or deductions from accepted results. If an implementation is added after Gate 1, it may only serve as a theorem sanity check and must be frozen separately before execution.

Permitted checks would be limited to:

1. verify C1's inequalities on finite windows for declared small widths;
2. enumerate `L1` ball counts and the C2 counting inequality for predeclared sample `(lambda,epsilon,r,w)` tuples;
3. reconstruct the separated-strip same-channel dependency graph and the already-recorded 17/64 touching-strip closure control from source definitions.

Any attempt to search for an enlarged interacting representation, fit a metric, optimize constants, or choose an architecture from observed outcomes is **out of scope** for this unit and requires a new frozen protocol.

## 7. Interpretation contract

If Gate 1 accepts C1–C6, the bounded conclusion is:

> A family may be exactly simulable in one dimension and still fail to preserve an unbounded transverse causal geometry under uniform bounded distortion. Fixed-width packing is compatible with this statement because its distortion constants may depend on width. The current separated-strip witness supplies transverse intervention addressability but not a connected transverse causal graph; the touching-strip witness supplies physical transverse influence but not closure of the current logical code.

Under this Program, bounded-distortion causal geometry is a **candidate sufficient contract for preserving coarse spatial rank**, not a unique or representation-independent definition of physical dimension.

The next architecture-search target becomes more precise: seek a dynamically closed represented family with local transverse causal edges whose logical graph contains arbitrarily wide grid strips under one fixed representation law. Only after such a witness exists does the C2 obstruction apply directly to that represented dynamics.

## 8. Not claimed

- No intrinsic or unique definition of spatial dimension.
- No claim that quasi-isometry is the only physically meaningful geometry-preservation notion.
- No claim that every spatial system must satisfy this exact contract.
- No claim that independent intervention rank from #114 is insufficient for every notion of an axis; only that it does not by itself instantiate the connected causal graph `G_w`.
- No claim that touching strips cannot close in a larger code; Research019 excludes one fixed-height family, not all symbolic descriptions.
- No claim about self-assembly, endogenous control, Class IV, universal computation, novelty, renormalization, prime factors, or metaphysics.
- No new numerical result is created by this protocol.

## 9. Gate-1 questions for Claude/Fable

Please review this theorem protocol before any implementation or publication, especially:

1. Is the `(lambda,epsilon)` site-map contract the right minimal bounded-distortion object, or does the intended representation comparison require coarse surjectivity or a separate bounded-fiber assumption? The C2 proof is designed not to need either.
2. Is the fiber bound in C2 sound from the lower distortion inequality alone, and is the finite-ball counting proof sufficient to establish the no-uniform-width theorem without silently importing a stronger quasi-isometry result?
3. Is C1 correctly stated with `lambda=1`, `epsilon=w-1`, making the fixed-width/uniform-width distinction exact?
4. Are C4–C6 faithful to the accepted correction-tower, coupled-strip, and interface-escape results without promoting physical proximity or intervention addressability into causal adjacency?
5. Is it appropriate to keep this unit theorem-only, with no new primary evaluation, and route the next actual experiment toward a closed interacting transverse representation?

Binding clarifications belong in this protocol before any implementation or result note. A material change to the graph objects, distortion contract, theorem statements, or interpretation requires renewed Gate-1 review.
