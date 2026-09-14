# One six-field operator rebuilds the cache through 4D

Status: exhaustive native evolution/recovery checks on the stated finite domains; exploratory performance and class comparisons. Final independent review and integration are tracked in [gathering PR #241](https://github.com/bombadil-labs/groovy-commutator/pull/241).

Authored by: Codex (OpenAI), Myk's dimensional-lift session. Reviewed by: independent collaborating agent `/root/independent_pilot_review` at prospective Gate 1 and for the bounded checks below; final sign-off is pinned to the gathering head before merge.

The supplied uniform six-field operator works for all 256 ECA sources through 4D on both complete source rings tested. Rebuilding the exact on-beam cache took **361.819 seconds**, versus **232.918 seconds** for the preceding four-field cache. The new computation covers 3.071 times as many native constraint cell events and achieves 1.977 times the historical throughput, but is **55.3% slower in total**. A single recipe removes recipe selection; it does not remove the cost of constructing native physical tables.

The exact archive is 23.2% smaller and peak process memory is 10.2% lower. These gains accompany a new cache and serialization implementation, as well as the operator change. They are not a causal estimate of the operator alone. The preceding cache and its scientific results remain intact.

## Scope and chronology

Myk supplied the operator definition in three screenshots and requested a timed cache rebuild, computing work only as needed. The definition was transcribed exactly; no unpublished implementation from Fable was available or is claimed inspected.

The [protocol](protocols/uniform-jet6-cache-20260914.md) was independently approved on 2026-09-14 at `ba12237a108ccbe89d6b28e37812d71e84cebf38`: [signed Gate 1](https://github.com/bombadil-labs/groovy-commutator/pull/241#issuecomment-5670437763). That approval was recorded at `c78bce9098a46baf26014eecb9c59099fff52830` before experimental implementation. The scientific implementation is frozen at **`47f0f658bb1162253753d4a12554c375329cb0b4`**; the primary run began at **2026-09-14T20:45:23Z**. Baseline main is `bbe6d8b677544d7521fee572e8fcd04328971967`, which includes the completed [four-field census](2026-09-14-on-beam-256-4d-classes.md).

Implementation sub-PR [#242](https://github.com/bombadil-labs/groovy-commutator/pull/242) was merged into the gathering branch with a merge commit. Evaluation, accounting and reporting follow that frozen implementation. The new unit obtained prospective review despite Myk's continuing permission to waive Gate 1. No scientific source, recipe, domain, scoring or budget was changed after primary evaluation began.

## The operator and the rule it must support

Let $H$ be the fixed native parent rule, $Y=H(X)$, $Z=H^2(X)$, $D=X\oplus Y$, and $T=X\oplus Z$. The new transverse axis repeats these six fields:

| Phase | Field |
| --- | --- |
| 0 | $X\oplus\tau_{v_+}X$ |
| 1 | $X\oplus\tau_{v_-}X$ |
| 2 | $D$ |
| 3 | $T$ |
| 4 | $X\land D$ |
| 5 | $X\land(1\oplus D)$ |

The translation convention is $\tau_vX(p)=X(p+v)$. At parent dimension one, $v_+=e_1$ and $v_-=-e_1$. At parent dimension $k\geq2$, they are $e_1+e_k$ and $-e_1+e_k$: **both** use +1 along the newest existing axis. Array order is source batch, newest transverse axis first, original line last. The source batch is never part of a native neighborhood.

The same six-field recipe is used for every source and every tested floor. Its aligned decoder is the algebraic identity $F_4\oplus F_5=X$. This run additionally tests a stronger uniform local decoder at every new-axis phase. Native evolution and that stronger decoder are separate consistency tests; a failure of the stronger decoder alone would not disprove existence of later native lifts.

The child flip mask must satisfy

$$
\Delta_{k+1}(L_k(X))=L_k(X)\oplus L_k(H_k(X)).
$$

The target includes $H_k^3(X)$ through its two-step field. Native physical neighborhoods have radius two along the original line and radius three along each lifted axis, or $5\cdot7^{d-1}$ physical bits at child dimension $d$. Period-six repetition makes some physical offsets equal, but their ordered positions are retained in the exact key representation.

This equation specifies the demanded outputs on the encoded family. It does not by itself prove that one phase-free local rule can realize every demand. The implementation explicitly tests that equal physical neighborhood keys demand equal flip bits and equal decoder bits, then freezes those tables. Unforced flip entries are zero (no flip), and unforced decoder entries are zero. Neither phase labels, source word identities nor an ECA oracle are inputs to the native runtime law.

## Work performed and reused

For each of the 256 rules at widths seven and eight, the run includes every source word, every longitudinal position and every transverse phase through 2D, 3D and 4D. There are 512 paths and 1,536 lifted floors. Width eight constructs its own native laws; it is not a test of the width-seven law on a larger input family.

The implementation keeps immutable family arrays and caches within a specific law, shape, axis order and radius. Each native law is evaluated once over its complete finite family. Its computed successor states are matched back to that family by exact row bytes, allowing later states and physical keys to be reindexed. Production successors come from the frozen native rule. The independently evolved ECA trajectory is used only as a reference check.

Each floor builds its complete family keys once. A second, uncached key construction on four selected source states checks that reuse. The recorded two physical-key calls per floor therefore do not mean two full-family builds. Repeated requests reuse arrays and native successors; no off-beam truth-table space is enumerated. Constructing each requested forced domain still requires its first physical-key census.

Every floor verifies native consistency, uniform immediate-parent recovery, aligned recovery, two complete native steps against an independent whole-family oracle, composed source recovery, immutable parent hashes, 15 direct physical-patch checks and exact export representation. Since the complete finite family is invariant under the source ECA, verified intertwining extends evolution to all times within that family.

| Quantity | Four-field baseline | Uniform six-field |
| --- | ---: | ---: |
| Passing paths through 4D | 512 | 512 |
| Passing native laws and uniform decoders | 1,536 | 1,536 |
| Failed / censored paths | 0 / 0 | 0 / 0 |
| Native constraint cell events | 63,307,776 | 194,445,312 |
| Direct physical-patch checks | 23,040 | 23,040 |
| Primary wall time | 232.918 s | 361.819 s |
| Peak process RSS | 197,550,080 bytes | 177,426,432 bytes |
| Compressed archive | 132,520,034 bytes | 101,773,778 bytes |

No finalization budget was exceeded. All preregistered native, stronger-recovery, repeated-key-cache and lower-time-per-cell predictions pass. Absolute speedup was not a preregistered prediction, and was not observed.

## Timings and their limits

The primary wall time includes construction, verification, exports and fixed class analysis. Matched controls ran afterward and took another **13.722 seconds**. Post-run author accounting, archive inspection, independent review and the later archive reader are outside both timings. The environment was Python 3.12.14 and NumPy 2.3.5 on Linux; the full record is in [execution.json](../../experiments/uniform_jet6_cache_20260914/run/execution.json).

| Summed primary stage | Four-field baseline | Uniform six-field |
| --- | ---: | ---: |
| Construction | 86.915 s | 287.581 s |
| Verification | 92.805 s | 27.410 s |
| Export | 32.183 s | 36.894 s |
| Six-field feature measurement | — | 0.819 s |

Stage sums omit small orchestration and finalization costs. Construction dominates the new run. In the historical comparison, periods change from four to six and transverse radii from two to three; cache reuse, serialization and execution time also differ. The 1.977 throughput ratio is a useful engineering observation, not an isolated operator speedup or a hardware benchmark.

The preregistered matched controls run rules 0, 30, 90 and 110 at width seven through 4D, with both operators using the new backend, three fresh-path repeats each and alternating mode order. The old control retains its archived recipe and original radius. Path timings exclude the separate repeated-key microbenchmark.

| Rule | Four-field median | Six-field median |
| --- | ---: | ---: |
| 0 | 0.10950 s | 0.34788 s |
| 30 | 0.13279 s | 0.44652 s |
| 90 | 0.13706 s | 0.44096 s |
| 110 | 0.12674 s | 0.45238 s |
| Median of the four per-rule medians | 0.12976 s | 0.44374 s |

That aggregate ratio is **3.420**: six fields are slower on these selected matched-backend cases. The raw JSON calls this statistic `pooled_median_seconds`, but it is specifically the median of per-rule medians, not the median of all twelve runs. This small control set does not estimate every rule's speed ratio.

Repeated-key requests are much cheaper after caching. Across the 36 six-field floor cases, median cached and uncached request times are 0.02154 ms and 13.89589 ms; the median of paired uncached/cached ratios is 606.47. These requests retrieve an already computed index and must not be presented as a 606-fold end-to-end speedup. First construction, output volume and native-table reconstruction remain costs.

Reviewer inspection found a dormant control-budget limitation: the key microbenchmark is outside the path timeout handler, so expiry there could prevent the benchmark metadata from finalizing. It was not triggered; all 24 control paths and 72 control floors completed. Frozen scientific code is retained. A future budget-handling correction must not rewrite this run's provenance.

## Class relationships under one recipe

The class convention, seven lift features, source features, orbit grouping and fixed nearest-centroid classifier are reused from the preceding note. The primary comparison uses the common complete cohort: all 88 reflection/complement-conjugacy orbits at both widths under both operators, with class counts I/II/III/IV of 8/65/11/4. No orbit is excluded for failure. Whole-orbit holdout and training-only scaling are retained; there is no feature search, relabeling, permutation test or hyperparameter tuning in this unit.

The table reports balanced accuracy. Both operators use the same feature views. Recipe features are omitted on **both** sides because the new recipe is constant.

| Feature view | Old, width 7 | New, width 7 | Old, width 8 | New, width 8 |
| --- | ---: | ---: | ---: | ---: |
| Source only | 40.20% | 40.20% | 32.91% | 32.91% |
| 2D | 46.06% | 39.13% | 48.33% | 43.67% |
| 3D | 52.66% | 43.96% | 56.47% | 35.82% |
| 4D | 48.50% | 50.59% | 50.77% | 47.85% |
| All 2D–4D features | 55.35% | 41.98% | 56.86% | 46.15% |
| Source + all lift features | 55.35% | 44.34% | 56.86% | 51.93% |

The fixed all-lift classifier loses **13.37 and 10.71 percentage points** under the new operator. Source-plus-lift improves on source alone by 4.14 and 19.02 points under the new operator, but remains below the matched old-operator view. This source-only incremental baseline differs from the earlier source-plus-recipe prediction, which failed; the new comparison does not reverse that earlier negative finding.

The frozen sensitivity omits the 41 and 106 orbits, leaving two Class IV representatives. New all-lift balanced accuracy is 47.47%/52.01%, versus 62.72%/64.61% under the old operator. New source-plus-lift increments become -7.07/+20.30 points. The width-seven sign change reinforces the fragility of an inference from so few Class IV orbits.

At 4D, mean source-coordinate degree and phase rank retain the broad ordering: Class IV is highest in both; Class III has higher rank but lower degree than Class II. The new orbit-averaged class means are:

| Class | Degree / width, width 7 | Degree / width, width 8 | Normalized rank, width 7 | Normalized rank, width 8 |
| --- | ---: | ---: | ---: | ---: |
| I | 0.552 | 0.528 | 0.239 | 0.148 |
| II | 0.607 | 0.567 | 0.335 | 0.208 |
| III | 0.556 | 0.525 | 0.450 | 0.282 |
| IV | 0.784 | 0.744 | 0.555 | 0.331 |

These functions are pulled back to the original source bits. They do not measure minimum native-rule degree or circuit complexity. The rank denominator also changes with representation: the old 4D family has 64 phase functions and divides rank by 64; the new one has 216 and divides by $\min(216,2^w)$, which is 128 or 216 at these widths. A lower normalized rank across operators therefore need not mean lower raw rank. Class distributions overlap, and the measurements are not proved symmetry-invariant fingerprints. A uniform recipe makes the comparison easier to interpret, but does not create a clean Wolfram-class boundary.

## Exact cache and selective loading

The preserved archive is `uniform_jet6_rules.tar.gz`, containing 1,536 members named, for example, `w7/rule110/d4.json`. Its exact SHA-256 is:

```text
766e4db7083fbdb551bc4aee66abc554079c5d118905f6d65aa5e5372c9418d1
```

The lossless `grid-referenced-physical-partial-rule-v1` format stores the packed image family, shape and radii, one representative flat index per distinct physical key, packed flip and decoder outputs, and source-phase truth tables. A representative points to the exact physical patch in the stored grid; it is not a replacement input to the local law. Representatives cover the forced domain exactly. Unforced outputs have the recorded deterministic zero completion.

The exact archive was delivered privately to Myk. Public code, raw floor/path records, the complete [member manifest](../../experiments/uniform_jet6_cache_20260914/run/archive_manifest.json) and archive/member hashes remain in the repository. This preservation arrangement was specified before evaluation; there is no new post-evaluation storage deviation. The private archive is not downloaded in CI.

The post-run [reader](../../scripts/read_uniform_jet6_cache.py) streams to one requested member and constructs that rule's physical index only on its first native use. Merely inspecting metadata does not build the index. A gzip stream may still have to decompress preceding members; selective loading does not provide constant-time random access. Repeated native requests reuse the constructed law. For example, with the supplied archive in the current directory:

```bash
python scripts/read_uniform_jet6_cache.py uniform_jet6_rules.tar.gz w7/rule110/d4.json
```

```python
import sys
sys.path.insert(0, "scripts")
from read_uniform_jet6_cache import read_member

cache = read_member("uniform_jet6_rules.tar.gz", "w7/rule110/d4.json")
grid = cache.grid[[42]]  # One encoded source word, retaining the batch axis.
next_grid = cache.step(grid)  # Builds only this member's native index on first use.
parent = cache.recover(grid)
```

## Post-run radius argument: a uniform formula needs a variable neighborhood

After the timed evaluation, Myk asked whether algebraic special cases can accelerate a uniform operator and whether radius-one roots hide a parameter. The following is an analytic argument, not a preregistered prediction or another experimental run. The author and independent reviewer checked it separately.

Algebraic simplification is compatible with one mathematical operator. For example, put $W=H(Z)$ and $K=Y\land T$. The six child flip rows simplify exactly to

$$
(D\oplus\tau_{v_+}D,\ D\oplus\tau_{v_-}D,\ T,\ D\oplus Z\oplus W,\ D\oplus K,\ K).
$$

The pinned implementation already uses these cancellations. A compiled implementation can further specialize identities or reuse subexpressions wherever equality is established on its declared domain. Such optimizations preserve the formula; an optimization valid only on the encoded image must not silently change a promised off-image completion.

The six-field definition accepts any binary local parent $H$. Its neighborhood is nevertheless part of the automaton's specification. For a root of radius $r$, directly computing $H(X)$, $H^2(X)$ and $H^3(X)$ from raw source bits has dependency bounds $r$, $2r$ and $3r$. These bounds do not by themselves give the child's necessary radius: the lift already stores enough information to recover $X=F_4\oplus F_5$, $Y=X\oplus F_2$ and $Z=X\oplus F_3$. With row phase supplied, the next six fields need only those values, their comparison translations, and one local evaluation $H(Z)$. Establishing a phase-free local realization is a separate obligation.

There is, however, an exact lower bound that rules out a child radius independent of the parent. On the infinite line take the parent shift

$$
H(X)_i=X_{i+r},\qquad r\geq1.
$$

All six lifted rows in a horizontal radius-$R$ neighborhood depend only on source coordinates in

$$
[-R-1,R+1]\ \cup\ [r-R,r+R]\ \cup\ [2r-R,2r+R].
$$

When $R<r$, coordinate $3r$ is absent. The all-zero source and a source containing only one 1 at $3r$ therefore produce identical child neighborhoods, even if every transverse row and the row phase are visible. But the next phase-three output is $X_r\oplus X_{3r}$, which differs between those sources. No child rule of horizontal radius less than $r$ can realize the lift's demanded evolution. Conversely, the lift commutes with horizontal translation, so shifting the entire child by $r$ works. The minimum horizontal radius for this example is exactly $r$.

In particular, **a radius-three shift defeats a fixed child horizontal radius two**: a source difference at position 9 is invisible to the current local patch but changes its next phase-three output. The argument also fits a sufficiently long periodic ring (width 13 already suffices for this example). The width-seven/eight census must not be treated as a test of that infinite-line distinction, because periodic aliasing can expose the otherwise distant bit.

This refutes radius-independent generality of the screenshot's fixed horizontal neighborhood beyond its stated ECA setting. It does not refute the six-field lift formula. A generator may derive the child neighborhood from the parent neighborhood while remaining a pure function of a fully specified C. What remains open is an adequate phase-free neighborhood bound and consistency argument for general parents; neither the radius-two ECA tests nor the on-image conjugacy equation supplies it automatically.

## Verification and remaining question

The [canonical account](../../results/uniform_jet6_cache_20260914.json) binds the frozen implementation, protocol, prior inputs, raw results, accounting verifier and reader by hashes. The author verifier checks all 1,536 archive members and recomputes every saved source-phase metric, with 12 bounded native-reader floors. Cheap accounting verifies all summary counts and repeats the fixed class analysis from saved measurements; it does not rerun the CA construction.

The independent reviewer checked every serialized family against a separately constructed ECA/six-field oracle, 25,203,648 representative flip/decoder outputs, 25,362,432 source truth bits, 512 source baselines and 48 literal held-orbit model fits. Independent physical replay covered six selected floors, 36,120 native updates and 36,120 decoder cells, with separate field, patch and cache-isolation controls. All 72 matched-control floor results and timing medians were also checked. This is not a second complete independent forced-key consistency census. The [review script](../../review/uniform_jet6_review.py) and [review evidence](../../review/uniform_jet6_review.json) preserve the bounded scope; the final signed review pins applicability to the gathering head.

Author accounting and archive verification passed. Local site validation was unavailable in the partial MCP materialization because `site/package.json` was absent; the existing site checks validate the complete repository in CI before integration. The new automatic job runs only the accounting command below, with no archive, CA synthesis, scientific replay or independent review script in Actions:

```bash
python scripts/verify_uniform_jet6_cache.py
# Optional local archive verification:
python scripts/verify_uniform_jet6_cache.py --archive uniform_jet6_rules.tar.gz
```

To reproduce the scientific computation separately, use pinned implementation `47f0f658bb1162253753d4a12554c375329cb0b4`, run `python scripts/uniform_jet6_cache.py --self-test`, then supply a new output directory to `--output` and the pinned SHA to `--implementation-commit`. This computation is not repeated automatically, and new runtime measurements must not overwrite this execution record.

The result establishes this recipe's finite-family native evolution and recovery through 4D. It does not establish recursive G, a pure generator from arbitrary bare higher-dimensional C, all infinite inputs, dimension induction, intrinsic dimensional floors, or fast construction at extremely high dimension. The construction still carries an explicit finite family and completion policy. The next performance question is whether a compact, uniformly local rule evaluator can replace forced-key enumeration; a shared formula for the lift alone has not supplied that evaluator.
