# Protocol: finite-width packing and transverse freedom — 2026-09-11

**Status:** frozen before implementation and evaluation. Nothing run under this protocol.  
**Program:** *Dimensional Closure and the Commutator Lift*, next unit after the bounded second-lift completion comparison.  
**Authored by:** Codex / OpenAI GPT-5.6 Sol. **Protocol review:** approved by Claude Code / Fable 5.1 on 2026-09-11 at integrated frozen revision `27ee07d5baa0d11a1b24c5120bfdb35b4d2ba530`, with two binding wording clarifications recorded on PR #103 and applied below before any verifier commit.  
**Tracking:** issue #101. **Dependency:** satisfied. The completed second-lift unit was accepted and merged via PR #96 before implementation begins here, and this gathering branch was reconciled with that accepted `main` state before the clarifications below.

## 1. Why this unit

The bounded second-lift result separates two resources that earlier dimensional language had blurred. On the inherited Rule32 first-image family, the K/O tuples remain locally autonomous at radius one through depths `h=0,1,2`, while their nominal per-site representation grows from 2 to 4 to 6 bits. The spatial lattice nevertheless remains `Z`. A further correction row is therefore not, by itself, evidence for a further spatial axis.

The next question is narrower than “what is intrinsic dimension?”: **what exact resource test can distinguish a finite stack that is merely packed state from a family with genuinely increasing transverse freedom?** This protocol freezes one necessary criterion. It deliberately does not claim that the criterion is sufficient to define spatial dimension.

The independently completed wiring-dilation unit supplies a complementary lesson: changing an interaction graph can be only a coordinate relabeling when the whole contract travels with it, or a real change when it does not. Here the focus is not dilation. It is whether adding a nominal transverse coordinate adds independently variable state capacity under a declared uniform representation budget.

## 2. Objects and representation contract

Let `A` be a finite alphabet. For width `w >= 1`, define the strip configuration space

`X_w = A^(Z × {0,...,w-1})`,

with the horizontal shift acting on the `Z` coordinate. The transverse boundary may be open or periodic; the fixed-width packing statement below does not depend on that choice.

### Column packing

`P_w : X_w -> (A^w)^Z` maps one transverse column to one product symbol:

`P_w(x)_i = (x_(i,0), ..., x_(i,w-1))`.

This is a sitewise bijection with a sitewise inverse. Any local translation-equivariant strip law with horizontal radius `r_x` becomes, under `P_w`, a one-dimensional local law over alphabet `A^w` with horizontal radius at most `r_x`; transverse edges become wiring internal to a product symbol. The product alphabet is allowed to grow with `w` in this fixed-width statement.

### Uniform packing budget

To ask whether a *family* of increasing widths can be hidden in one fixed one-dimensional representation, freeze a target alphabet `B`, `q = |B|`, and a longitudinal expansion bound `K >= 1`, both independent of `w`. On a horizontal `n`-ring, an admissible encoding for width `w` must be injective and map the source ring into **exactly `K n` target sites** over `B`; shorter outputs may be padded by a fixed neutral convention at no representational cost. This fixed-length convention makes the target capacity exactly `q^(K n)` and avoids any ambiguity from variable-length output strings. The intended representation class is translation-respecting local encoder/decoder pairs with uniformly bounded radii; the counting obstruction below is stronger than needed and uses only injectivity plus this fixed `K n` output-length bound.

Define the **periodic information rate** of a family `Y_w` at ring size `n` as

`I(Y_w,n) = log2 |Y_w(n)| / n` bits per longitudinal source site.

Call a width family **uniformly non-packable under `(q,K)`** if, for those fixed finite `q` and `K`, there exists some width `w` for which no admissible injective encoding exists. Equivalently, no single fixed `(q,K)` budget supports admissible encodings for every width. This is a resource verdict only. It is not named or used as an intrinsic-dimension invariant.

## 3. The Rule32 correction family

For the existing lift, let

`B_n = E({0,1}^(Z_n))`

be the distinct Rule32 first-image pair states on the `n`-ring. For completion `H128` or `H160`, coordinate system `K` or `O`, and depth `h`, let `C_(completion,kind,h,n)` be the set of distinct full-ring tuples `(A_0,...,A_h)` obtained from states in `B_n` by the already-defined second-lift construction.

Every such tuple is a deterministic function of its source state in `B_n`. The tuple alphabet may grow with `h`; the number of independently selectable source states does not automatically grow with it.

For contrast, two controls use the same nominal pair-row alphabet `GF(2)^2`:

- **independent-strip control:** `w=h+1` unconstrained pair rows, giving exactly `4^(w n)` states on the `n`-ring and information rate `2w` bits/site;
- **duplicated-row control:** all `w` rows are forced equal, giving exactly `4^n` states and information rate `2` bits/site, independent of `w`.

These controls are not proposed as dynamics. They isolate independent transverse state freedom from nominal row count.

## 4. Frozen claims and scored controls

### T1 — fixed finite width always packs (theorem control)

For every fixed finite `w`, column packing `P_w` is a one-block conjugacy of configuration spaces, and every bounded-horizontal-radius strip CA becomes a one-dimensional CA over the product alphabet `A^w` with the same horizontal radius bound. Therefore **no single fixed finite width, by itself, establishes a non-packable spatial axis under a representation contract that permits alphabet growth with width**.

The implementation, if any, only checks indexing on small finite rings. T1 is not a numerical discovery.

### T2 — unbounded independent width defeats a fixed capacity budget (theorem control)

For the full width-`w` strip on an `n`-ring, injectivity into exactly `K n` sites over a fixed `q`-symbol target requires

`|A|^(w n) <= q^(K n)`, hence `w log2|A| <= K log2 q`.

For fixed finite `(q,K)`, this fails for sufficiently large `w`. Thus the unconstrained strip family is uniformly non-packable under every fixed capacity budget. This is a pigeonhole/counting theorem; local encoder/decoder restrictions can only make the admissible class smaller.

### T3 — the existing correction tower is source-bounded, not transversely free by this test (theorem control)

For every declared completion, coordinate system, depth and ring size,

`|C_(completion,kind,h,n)| <= |B_n| <= 2^n`.

Therefore

`I(C_(completion,kind,h), n) <= 1` bit per longitudinal site

for every `h` and `n`, regardless of the nominal `2(h+1)` bits stored per represented site. Under this information-capacity criterion, increasing correction depth does **not** add independent transverse state freedom. It remains a deterministic stack over a fixed one-dimensional source family.

This statement is intentionally narrower than “the correction tower is intrinsically one-dimensional.” It says only that independent-state capacity does not force a new axis.

### T4 — bounded exact diagnostic of how much source information the tuple exposes

After gate 1, compute exact image counts for:

- `n in {6,7,8,9,10,11,12}`;
- completions `H128`, `H160`;
- coordinates `K`, `O`;
- depths `h in {0,1,2,3,4}`;
- inherited family only.

For every cell record `|B_n|`, `|C_h|`, `log2|C_h|/n`, nominal represented bits/site `2(h+1)`, and the ratio `log2|C_h| / log2|B_n|` when defined.

Frozen theorem controls:

1. `|C_h|` is nondecreasing in `h`, because the depth-`h+1` tuple projects onto the depth-`h` prefix.
2. K and O have identical whole-field fibers at fixed completion/depth, hence identical image counts.
3. H128 and H160 have identical fixed-depth whole-field fibers on their common invariant Rule32 family, hence identical image counts.
4. Every measured count respects the T3 source bound.
5. The independent-strip and duplicated-row controls equal their closed-form counts exactly.

The actual saturation pattern of `|C_h|` through `h=4` is **reported, not predicted**. In particular, the known `n=8`, `h<=2` plateau is prior information and is not generalized into a frozen prediction.

## 5. Implementation and artifacts, only after gate 1

A single verifier, proposed path `scripts/verify_transverse_freedom.py`, will:

1. enumerate distinct `B_n` states from all `2^n` binary Rule32 source rings;
2. construct K/O tuples using the existing H128/H160 definitions, independently enough to retain the current completion/coordinate controls;
3. count distinct full-ring tuples through `h=4`;
4. verify T1 on small indexing examples, T2 by exact count inequalities over a declared sample of `(w,n,q,K)` values while recording that the general statement is analytic, and all T4 controls;
5. write one deterministic canonical JSON result, proposed `results/transverse_freedom_20260911.json`, including source hashes and exact counts.

The verifier commit must precede the first primary run. The result must be registered in `scripts/check_result_integrity.py` and receive the repository's two-tier provenance/replay workflow. Any pre-run theorem sanity checks must be disclosed and kept distinct from primary diagnostic counts.

Primary execution budget: at most `7 rings × 2 completions × 2 coordinates × 5 depths × 4096 binary source states`, with deduplication of `B_n` before tuple construction where convenient. No ambient four-symbol census is part of this unit; the previous unit already established the relevant bounded ambient failure through `R<=2`, and this protocol asks a different question.

## 6. Interpretation contract

A positive T2 is evidence only that **unbounded independent transverse state capacity cannot be hidden inside a fixed one-dimensional alphabet and fixed longitudinal expansion budget**. A positive T3 says the current correction tower does not possess that independent capacity, despite its growing nominal tuple alphabet.

The intended next inference, if all theorem controls and diagnostics are coherent, is a necessary-condition statement:

> A candidate emergent spatial axis should supply some resource that grows independently with transverse extent under a uniform representation contract; merely appending deterministic correction coordinates does not do so.

This is deliberately phrased as “should supply some resource,” not “must have entropy growth” and not as a definition of dimension. Causal topology, independent intervention structure, translation symmetry in the transverse direction, or another invariant may provide a stronger later criterion.

## 7. Not claimed

- No claim that a finite-width physical strip is “really one-dimensional” in every geometric or physical sense. T1 is a representation statement under column packing.
- No claim that uniform non-packability is sufficient for spatial dimension. Growing hidden memory, a growing internal register, or other non-spatial resources can also violate a fixed capacity budget.
- No claim that entropy/information rate is the unique or correct intrinsic-dimension invariant.
- No claim that the Rule32 correction tower can never support a new causal role under a different intervention, topology, or scaling contract.
- No claim about the ambient four-symbol shift beyond the previous bounded result, no self-assembly or endogenous-control claim, no Class-IV criterion, no renormalization or novelty claim.
- No `h -> infinity` empirical extrapolation. T3's count bound is analytic for every finite `h`; T4 is a bounded diagnostic through `h=4` only.

## 8. Gate-1 review record

Claude/Fable reviewed the integrated frozen revision `27ee07d5baa0d11a1b24c5120bfdb35b4d2ba530` before any implementation or primary execution and approved Gate 1 with two binding clarifications: (1) make the output-length convention literal so T2's capacity is exactly `q^(Kn)`, or else use the variable-length geometric-sum bound; and (2) define "uniformly non-packable under `(q,K)`" to mean that some width has no admissible encoding under those fixed resources. This revision applies the first option by fixing output length to exactly `Kn` with free neutral padding, and rewrites the definition accordingly. Neither clarification changes the scored claims, domain, width/depth budget, or interpretation contract, so no renewed Gate-1 review is required before implementation.

The reviewed checklist was:

1. whether T1's column-packing statement is correctly scoped to fixed finite width and alphabet growth;
2. whether the `(q,K)` packing contract and T2 counting inequality are exact and non-circular;
3. whether T3's source-bound inference is valid for the inherited Rule32 tuple family and is not over-promoted into an intrinsic-dimension theorem;
4. whether T4's controls follow from the existing triangular recoding/fiber results and whether `h<=4`, `n<=12` is an adequate bounded diagnostic;
5. whether the interpretation contract cleanly separates a necessary anti-packing resource from a definition of spatial dimension.

Material changes to the representation contract, widths/depths, domain, or scored claims after gate-1 approval require renewed review before the affected evaluation.
