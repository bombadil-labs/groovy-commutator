# Uniform six-field on-beam cache and timing comparison

Status: frozen design before implementation and primary evaluation.

Authored by: Codex (OpenAI), Myk's dimensional-lift session, 2026-09-14. Reviewed by: pending independent Gate 1. Myk has explicitly waived Gate 1 in this session and now authorizes recomputing the cache with the new operator, computing only needed work and comparing timings; that authorization persists. Prospective independent review is requested and its actual chronology will be recorded.

## Question and scope

Rebuild the complete all-256 on-beam cache through 4D under the one six-field operator supplied by Myk in three Fable screenshots. No corresponding implementation was present in main or the current branch/PR listing at freeze. This is Codex's implementation of that supplied definition, not an assertion that Fable's unpublished implementation has been read.

Baseline main: bbe6d8b677544d7521fee572e8fcd04328971967. Prior reference: scripts/on_beam_256_4d.py and experiments/on_beam_256_4d_20260914/run, unchanged. That four-field census passed all 512 paths and took 232.9179514890002 seconds, with summed build/verification/export stages 86.915/92.805/32.183 seconds. Its failed class-improvement prediction and its exact archived rules remain unchanged.

Primary population: all 256 ECA sources; all binary source words at width 7 and 8; all longitudinal positions and transverse phases; floors 2,3,4. Complete invariant finite families, newly synthesized immutable native laws. No full-shift, recursive G, arbitrary native higher-dimensional C or dimension-induction claim.

## Exact supplied operator

A parent X has native rule H. Let Y=H(X), Z=H(Y), D=X XOR Y and T=X XOR Z. Six fields in this exact order are:
- F0 = X XOR tau(v+)X
- F1 = X XOR tau(v-)X
- F2 = D
- F3 = T
- F4 = X AND D
- F5 = X AND (1 XOR D)

At parent dimension 1, v+ = +e1 and v- = -e1. Above dimension 1, v+ = +e1 + ek and v- = -e1 + ek, where ek is the newest existing axis. Both transverse offsets are +1. Define tau(v)X(p)=X(p+v). Stack these six fields along a new axis, periodic with period 6. Physical array order is [source batch, newest transverse axis, ..., original line].

The child native derivative is constrained by L(X) XOR L(H(X)); native neighborhood radius 2 along the original line and radius 3 along every lifted axis. Keys contain exactly ordered physical bits, never external phase labels. The global aligned decoder F4 XOR F5 equals X algebraically. We additionally test the same stronger immediate-parent uniform local decoder used in the previous census, with desired X at every new-axis phase. If that stronger decoder fails while evolution/aligned decoding pass, preserve and distinguish that failure; do not call it a counterexample to the weaker screenshot decoder.

All unforced native derivative and uniform-decoder outputs default to zero (derivative zero means identity/no flip). Complete and freeze each native parent before generating its child. The image family plus its recipe policy is explicit metadata in C; the construction is not advertised as a bare-table generator for arbitrary C.

## Demand-driven work and cache boundaries

Do not enumerate any off-beam binary neighborhood space or search recipes. Operate one rule/width path at a time. Keep an immutable native-law cache keyed by exact materialized parent configurations. Reuse a known configuration's neighborhood keys and computed successor; content equality, not array identity alone or a lossy hash, justifies reuse.

All source words form one invariant family. When a computed native successor is exactly equal to a batch reindexing of that family, its physical keys may be reused by the same reindexing: neighborhoods never cross the source-batch axis. This equality must be checked, and all native evolution still evaluates the current parent table. The original ECA is an independent oracle for verification, not a replacement for parent evolution at runtime.

Shared symbolic construction of fields and reuse of temporal intermediates are permitted. Export, metrics, decoding and repeated verification reuse existing arrays/keys where justified. Metrics are computed only for successful requested floors. Stop later floors of a path after a native inconsistency, decoding failure or budget censor; preserve the exact obstruction. No adaptation of field order, radii or domain after results.

## Exact cache artifact

Preserve each forced physical partial rule and decoder, with no arbitrary off-beam conclusions. Use a lossless grid-referenced representation: packed complete finite image family, one representative flat cell index per unique physical neighborhood, packed derivative/decoder outputs, radius/shape/ordering metadata and source-phase derivative truth matrix. Each representative expands directly to the exact physical patch; family and indices are data, not a supplied phase label in the native rule.

The in-memory exact tuple DAG may be reconstructed on demand from those stored bits and indices. This avoids storing the much larger expanded DAG transport used previously. All root representatives must map back to their recorded native keys and cover the forced key set exactly. Raw outputs, member/archive hashes and reproduction code are public in the repo. The full gzip artifact is delivered durably to Myk, privately if necessary; do not add a large base64 archive to every Git checkout.

This is a changed lossless representation. Any export/storage saving must be attributed separately, not solely to a better operator. Persist the old cache; no destructive replacement.

## Correctness and independent controls

Before primary evaluation:
- Compare the six fields and all six algebraic child flip formulas to independent scalar construction on deterministic toy binary arrays in dimensions 1-3. Both comparison vectors and F4/F5 recovery must be checked.
- Mixed-radius ordered neighborhood keys: compare every cell on small deterministic grids to direct physical patches, including periodic repeats and phase shifts. Test cache hits, misses, reindexing and caller mutation boundaries.
- Round-trip every exported field and representative on bounded examples.
- Reproduce selected old four-field floor counts using the new cache engine, without changing its scientific definition.
- Known Boolean-degree/rank controls and class-symmetry controls reuse the previous frozen implementation.

At every primary successful floor:
- Zero contradictory outputs per physical native key; aligned decoder exact; separately report uniform local decoder consistency.
- Two native steps agree on every cell with an independently encoded original-ECA orbit.
- Immediate-parent and composed source decoding recover the original word, with native parent completion hashes unchanged.
- Direct patch/serialized expansion checks on source indices 0,1,42,85,last; phase tuples all zero, all one, all last, with longitudinal position 0.
- Verify source/phase permutation reuse against an uncached physical-key evaluation on a fixed bounded sample.

Native conflict witnesses retain source words, physical event coordinates and identical expanded patches with opposite required outputs. Censors retain the last completed floor and reason.

## Timing and comparison

Use perf_counter and process peak RSS. Record end-to-end wall time plus exclusive stages for construction (parent stepping, fields, neighborhood construction, constraint reduction), verification, source-phase metrics, and lossless export. Record cells, forced keys, key-builder calls/cache hits, retained bytes and artifact sizes by floor. No scientific evaluations in Actions.

Primary historical comparison: all 256 rules, both widths, all three floors against the preserved four-field run, with comparable success/verification goals. Report absolute time and time per native constraint cell. State explicitly that period, neighborhood, temporal fields, caching, representation and run time differ; this is an end-to-end engineering comparison, not isolation of operator choice.

Bounded controlled comparison: fixed rules 0,30,90,110 at width 7 through 4D. Three fresh cold-cache repetitions for each of old-four-field and uniform-six-field, alternating which family runs first by repetition. Use the same optimized engine, verification and new export representation; report per-rule medians and pooled medians. This isolates the workload difference under the same backend on the selected controls, not all-rule performance.

Additionally time repeated native neighborhood-key requests with reuse enabled and disabled on these same frozen configurations (three requests per floor); compare every returned key's expanded physical meaning. This is a key-computation microbenchmark, not an end-to-end speedup claim. No sweeping optimization choices after seeing the timings.

## Class analysis

Reuse the previous labels, reflection/conjugacy orbits, orbit averaging, source baselines and seven feature definitions. Normalize phase counts using 6^(d-1), and rank by min(phase count,2^width). These remain source-coordinate degree/term/rank statistics, not minimum native-circuit complexity.

There is one constant recipe. Compare source, lift2, lift3, lift4, lift_all, and source+lift_all using the previous fixed leave-one-orbit-out nearest-class-centroid method with training-only scaling. Use only orbits complete at both widths, report exclusions, and censor four-class prediction if a class has fewer than two complete orbits. Preserve the previous sensitivity excluding entire 41 and106 orbits. Report descriptive associations and paired differences to the previous cache; do not select features, retune a model or run a new significance search. No new permutation test is necessary for this timing/cache request.

## Predictions and budget

P1: all 256 source paths pass native evolution through 4D at both widths under the supplied recipe. Uniform local immediate-parent recovery is a stronger separately scored prediction.
P2: cached repeated requests avoid physical-key reconstruction and are faster on median than uncached requests.
P3: end-to-end time per native constraint cell is lower than in the historical four-field census. Absolute wall time is not predicted because the six-field family is larger.
Class patterns are descriptive; no new claim of improved class classification is preregistered.

Cooperative total budget: 20 minutes primary science plus 5 minutes bounded timing controls, 120 seconds per rule/width path, 4 GiB RSS. Archive finalization must still preserve partial outputs on timeout; total-budget checks cover finalization explicitly. Unexpected native conflicts are failures, not occasions to reselect recipes. Stop at the frozen budget and report unresolved cases. Any scientific change requires a new dated protocol and run rather than editing the frozen output.

Final integration follows gathering/sub-PR chronology, a canonical hash-bound account, fast provenance/accounting CI and independent exact-head Gate 2.
