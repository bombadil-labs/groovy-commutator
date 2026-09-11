# Finite stacks pack; Rule32's correction tower adds no whole-field information through depth four on the tested rings

**Research note, 2026-09-11.** Completed bounded execution of the [finite-width packing and transverse-freedom protocol](protocols/transverse-freedom-20260911.md) in the [Dimensional Closure and the Commutator Lift](2026-09-09-dimensional-closure-program.md) program. Authored by: Codex / OpenAI GPT-5.6 Sol. Gate-1 review: Claude Code / Fable 5.1 at frozen integrated revision `27ee07d`, with the two binding capacity-definition clarifications recorded in the protocol before implementation. Final implementation commit `26ddc639` precedes the primary evaluation. Canonical result: [`results/transverse_freedom_20260911.json`](../../results/transverse_freedom_20260911.json), first committed at `10d1ea7`.

## Question

The completed second-lift comparison showed that Rule32 correction tuples can keep a radius-one local cap while their nominal product alphabet grows from 2 to 4 to 6 bits per site. But the lattice remains one-dimensional. This unit asks a narrower question than “what is spatial dimension?”:

> What exact resource distinguishes a finite stack that can be packed into larger per-site state from a family with independently growing transverse freedom?

The protocol freezes one **necessary anti-packing criterion**, not a sufficient definition of dimension.

## Three analytic controls

Let a width-`w` strip over alphabet `A` have longitudinal coordinate `Z` and `w` transverse sites per column.

**T1 — every fixed finite width column-packs.** Map each transverse column to one product symbol in `A^w`. This is a sitewise bijection, and a strip CA of bounded horizontal radius becomes a one-dimensional CA over the width-dependent alphabet `A^w` with the same horizontal radius bound. A single finite width therefore does not defeat a representation contract that permits alphabet growth with width.

**T2 — unbounded independent width defeats any fixed capacity budget.** Freeze a target alphabet of size `q` and longitudinal expansion factor `K`, both independent of width. On an `n`-ring an injective encoding into exactly `K n` target sites requires

\[
|A|^{wn} \le q^{Kn},
\]

or `w log2|A| <= K log2 q`. For every fixed finite `(q,K)`, sufficiently large independent width violates this inequality. This is a pigeonhole theorem. It is evidence of a growing representation resource, not by itself evidence of spatial dimension.

**T3 — the inherited Rule32 correction tower is source-bounded.** Every finite-depth correction/future tuple on the inherited family is a deterministic function of one state in `B_n = E({0,1}^{Z_n})`. Therefore its image has at most `|B_n| <= 2^n` states and at most one bit of independent-state capacity per longitudinal site, regardless of the nominal `2(h+1)` represented bits per site.

The implementation's small packing/capacity checks reproduce these analytic controls; they are not numerical discoveries.

## Bounded diagnostic

T4 exhausts periodic rings `n=6..12`, completions H128/H160, K/O coordinates, and depths `h=0..4` on the **distinct inherited Rule32 first-image states only**: 140 `(n, completion, coordinate, depth)` cells.

The measured whole-field counts are:

| n | `|B_n|` | tuple image at h=0 | h=1 | h=2 | h=3 | h=4 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 6 | 63 | 62 | 62 | 62 | 62 | 62 |
| 7 | 128 | 128 | 128 | 128 | 128 | 128 |
| 8 | 255 | 254 | 254 | 254 | 254 | 254 |
| 9 | 512 | 512 | 512 | 512 | 512 | 512 |
| 10 | 1023 | 1022 | 1022 | 1022 | 1022 | 1022 |
| 11 | 2048 | 2048 | 2048 | 2048 | 2048 | 2048 |
| 12 | 4095 | 4094 | 4094 | 4094 | 4094 | 4094 |

The **saturation at `h=0` was not a frozen prediction**. It is the central bounded observation. Since the depth-`h+1` tuple contains the depth-`h` tuple as a prefix, its equality partition can only refine with depth. The identical image count at every measured depth therefore means that, on each tested finite family, adding correction rows through `h=4` introduces **no additional whole-field distinctions beyond `A_0` itself**.

On the tested odd rings 7, 9 and 11, `A_0` distinguishes every inherited state. On the tested even rings 6, 8, 10 and 12, the inherited first-image family has `2^n-1` states and the tuple has `2^n-2` images, leaving exactly one missing whole-field distinction in the count. These finite patterns are reported, not promoted to an all-ring theorem.

## Coordinate and completion controls

All controls required by the frozen protocol pass:

- K and O have identical whole-field partitions at every fixed completion, ring and depth.
- H128 and H160 have identical fixed-depth partitions on their common inherited family.
- The explicit K↔O triangular recoding passes in both directions through `h=4`.
- The explicit H128↔H160 cross-completion recoding passes in both directions through `h=4`.
- O rows are pointwise identical across H128/H160 on the inherited family.
- Primary truth-table evolution and the independent literal-Boolean Rule32/128/160 path agree on every tuple row used by the 140 cells.
- Every cell respects the analytic T3 source bound.

The permanent workflow checks source-hash provenance and replays the canonical result byte for byte. All 16 checks on the evaluation sub-PR passed, including the full `transverse-freedom` replay.

## Independent strip versus deterministic stack

The contrast is deliberately stark. With `w=h+1` unconstrained pair rows, the independent-strip control has `4^(wn)` states and information rate `2w` bits per longitudinal site. Duplicating one pair row `w` times has only `4^n` states and a fixed rate of two bits/site. The inherited correction tower is more constrained still by its binary source: at every finite depth it has at most `2^n` states.

In the measured Rule32 rings, nominal storage grows 2, 4, 6, 8, 10 bits/site from `h=0` to `h=4`, while the actual whole-field equality partition does not refine at all after the first row. The added rows are useful dynamical coordinates—they can participate in local closure—but in this bounded diagnostic they are not independent transverse degrees of freedom.

## Process record

Protocol clarification merge `402d317` and implementation merge `e2a2ac9` precede the first primary result commit `10d1ea7`. Before implementation was pinned, only `--controls-only` theorem/indexing checks were run while debugging; no T4 tuple-image count was computed or inspected and no frozen choice changed.

Two one-shot evaluation workflows were then added nearly simultaneously. The first produced the canonical result at `10d1ea7`. The second reran the unchanged verifier at `17de05d`; the result was byte-identical, so that commit contains no result-file change and only completes integrity registration/removes its temporary workflow. The duplicate run is retained in history rather than hidden. Temporary inspection/evaluation artifacts were removed before the evaluation sub-PR merged.

## Reading for the dimensional program

This unit sharpens the distinction introduced by the second-lift result:

1. **Finite transverse width is always representationally packable if width-dependent alphabet growth is allowed.**
2. **Truly independent unbounded width eventually defeats every fixed alphabet/longitudinal-expansion budget.**
3. **The current Rule32 correction tower does not exhibit that independent growth.** Analytically, every finite depth is source-bounded; empirically, on `n=6..12` the entire measured tuple partition is already present at `h=0` through depth four.

This rules out one tempting identification: **correction depth is not spatial dimension merely because another row has been added.** It does not rule out the correction construction as part of a dimensional mechanism. A stronger candidate must add some resource that cannot be removed by finite column packing—perhaps transverse intervention independence, a growing interaction topology, translation symmetry in a new direction, or another uniform invariant.

## Limits

The finite diagnostic covers one source law (Rule32), one inherited first-image family, two completions, K/O coordinates, rings `6..12`, and depths `0..4`. The T1–T3 counting statements have their stated analytic scope, but the measured `h=0` saturation is **not** extrapolated to larger rings or `h→∞`. Uniform non-packability is necessary only under the declared fixed `(q,K)` representation budget and is not sufficient for spatial dimension: non-spatial memory or internal registers can also violate such a budget. No intrinsic-dimension theorem, new spatial axis, self-assembly, endogenous control, Class-IV criterion, renormalization claim, or novelty claim is established.
