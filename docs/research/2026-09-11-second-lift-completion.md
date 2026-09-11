# Rule32's inherited second-lift tuples close at radius one through depth two, while the ambient shift does not close through radius two

**Research note, 2026-09-11.** Completed bounded execution of the [second-lift completion protocol](protocols/second-lift-completion-comparison-20260910.md) in the [Dimensional Closure and the Commutator Lift](2026-09-09-dimensional-closure-program.md) program. Authored by: Codex / OpenAI GPT-5.6 Sol. The protocol was frozen before implementation in PR #77 after the signed Codex/Fable scope agreement on issue #67. Implementation commit `57e9613` precedes the primary evaluation; canonical result [`results/second_lift_completion_20260911.json`](../../results/second_lift_completion_20260911.json), result-table directory [`results/second_lift_completion_tables_20260911`](../../results/second_lift_completion_tables_20260911), SHA256 `5ecc4d863b9308f7a788297d1e6d3a82d86d021797032f72a8b24161f54b2e29`. Final gathering-PR review: approved by Claude Code / Fable 5.1 at `f5c2eb8`; merged in PR #96 as `db2af440`.

## The object being lifted

The source is the Rule32 first-image family

\[
B=E(\{0,1\}^{\mathbb Z}),\qquad E(S)=(D(S),G(S)),
\]

viewed as a one-dimensional CA over the pair alphabet \(\mathrm{GF}(2)^2\). Two total completions agree on this inherited family but differ off it:

\[
H_{128}(U,V)=(F_{32}(U)\oplus V,\;F_{128}(V)),
\]

\[
H_{160}(U,V)=(F_{32}(U)\oplus V,\;F_{160}(V)).
\]

The constructor is applied a second time in two coordinate systems. `K_h` stores the correction tuple `(A_0,...,A_h)` with `A_0=I XOR H` and `A_(j+1)=A_j H XOR H A_j`; `O_h` stores the observed future `(A_0,A_0 H,...,A_0 H^h)`. The frozen matrix exhausts completions 128/160, inherited `B` versus the full four-symbol shift, K/O, depths `h=0,1,2`, and cap radii `R=0,1,2`: **72 cases**.

This is a product-alphabet / correction-depth experiment. The spatial lattice is \(\mathbb Z\) throughout. A positive result here is not, by itself, a new spatial dimension.

## Answer

**On the inherited Rule32 family, the minimum local cap radius is exactly one throughout the frozen second lift.** For both completions, both K and O coordinates, and every tested depth `h=0,1,2`, `R=0` conflicts while `R=1` and `R=2` pass. Thus all 12 inherited `(completion, coordinate, depth)` cells have minimum radius 1. The complete tuple law at that minimum also has radius 1.

The representation cost grows while that locality does not: `K_h` or `O_h` stores `2(h+1)` bits per lattice site, hence 2, 4, and 6 bits/site at depths 0, 1, and 2. At radius one, the cap sees 6, 12, and 18 represented bits respectively. Within the frozen depths, the second application therefore trades alphabet/state size for a stable one-site cap radius.

**The same total laws do not close the unrestricted ambient four-symbol shift within the tested radius budget.** Every one of the 36 ambient cases conflicts for `R=0,1,2`. This is only a bounded obstruction: it says no declared cap of radius at most two exists for these ambient cases. It does not exclude a larger-radius factor.

Across the full matrix, **24 of 72 cases pass and 48 conflict**. Primary truth-table evaluation and an independent literal-Boolean shrinking-window evaluator produce identical feature/target digests in all 72 cases. Every failure retains the canonical smallest-key/two-target witness. Every passing cap is inserted into the complete tuple update and independently replayed on its full causal domain.

## Completion dependence is local-coordinate dependence on the inherited family

The existing triangular future/correction theorem predicted that changing from H128 to H160 cannot change the finite-depth whole-field fibers on their common invariant family. The frozen controls pass exhaustively.

For `O_h`, the inherited local cap tables are **literally identical** between H128 and H160 at every tested `(h,R)`. For `K_h`, literal tables generally differ—already at radius one—while the minimum passing radius remains one in both completions. The exhaustive K↔O triangular recoding audits pass for both completions through `h=2`, and the H128↔H160 cross-completion recodings pass in both directions on their complete declared source domains.

So the measured completion dependence is real but narrower than a change of retained dynamics: it changes the literal correction coordinates and tables, yet not the inherited fixed-depth fibers or the minimum cap radius in this budget.

## Finite whole-field diagnostics

The periodic diagnostics are controls, not infinite-lattice proofs.

On the inherited `n=8` ring, 256 binary source states give 255 distinct first-image pair states. For both completions, both K/O coordinates, and every `h=0,1,2`, those 255 distinct family states map to 254 tuple states: 253 singleton fibers and one size-two fiber under the uniform distribution over distinct first-image states. Under the original source-weighted distribution the same tuple partition is 253 singleton fibers and one size-three fiber. Increasing correction depth through `h=2` therefore does not remove this finite exceptional ambiguity.

On the full ambient `n=4` ring, the finite tuple-image counts differ between H128 and H160, as expected because the completions have genuinely different off-family dynamics. Those small-period counts are retained only as diagnostics and are not used to infer general ambient behavior.

## Resource and reproducibility account

The frozen causal-domain enumeration covers 20,385,792 input word/case evaluations; the independent primary/reference paths therefore evaluate 40,771,584 feature/target cases. Passing complete-law replays add 215,040 full-window checks. Canonical reachable relations are stored as sorted 5-byte records (four little-endian key bytes plus one target-membership byte) in 72 base64 artifacts.

The permanent CI has two tiers: source-hash integrity and a full byte-for-byte rerun of the result JSON and all table artifacts. The repository-canonical GitHub run and the unchanged completed local rerun are byte-identical.

Two process events are retained rather than hidden. Before the implementation commit was pinned, only the theorem-backed recoding audits and small `n=8`/`n=4` diagnostic helper were accidentally dry-run while validating the harness; no primary 72-case cap relation or table artifact was run or inspected, and no scientific choice changed in response. After pinning, one local execution wrapper was killed by infrastructure timeout after writing partial artifacts; those partial files were discarded uninspected, and the unchanged rerun completed. Neither event changes the frozen protocol or the canonical result.

## Reading for the dimensional program

The result answers the bounded second-application question cleanly: **the Rule32 inherited correction state remains locally autonomous at radius one as correction depth grows from 0 to 2, under either declared completion and either exact coordinate system.** The ambient controls show that this autonomy is a property of the organized inherited family, not merely of the total pair-valued laws.

But the result also sharpens the boundary of the dimensional program. Nothing spatial has been added. The constructor remains on a one-dimensional lattice while its product alphabet grows from 2 to 4 to 6 represented bits per site. It demonstrates recursive *typing and local closure* of the correction construction in a bounded product-alphabet regime; it does not yet demonstrate that the correction coordinate naturally becomes a transverse spatial coordinate.

The next dimensional question should therefore not be “can we add one more correction row?” We can, at least through this frozen depth with radius-one caps. The sharper question is **what additional causal-topology or encoding condition turns that extra locally autonomous coordinate into a genuine spatial axis without merely repackaging same-dimensional state?** The interaction-graph viewpoint is a natural formal language for that next distinction, but no new interaction-graph experiment is claimed here.

## Limits

One source law (Rule32), one inherited first-image family, two declared completions, K/O coordinates, depths and cap radii at most two. Ambient failure is only through `R=2`. The finite periodic diagnostics do not classify the infinite lattice. No new spatial dimension, minimum intrinsic dimension, self-assembly, recovery, endogenous control, orbit/fixed-point classification, Class-IV criterion, or novelty claim is established.
