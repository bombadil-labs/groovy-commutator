# Six fixed binary recipes retain native evolution and recovery through 6D

Status: completed bounded computation; independent Gate 2 pending.
Authored by: Codex (OpenAI), Myk's dimensional-lift session, 2026-09-14. Reviewed by: none at this records revision.
Protocol review: none at freeze; run authorized by Myk 2026-09-14. Myk explicitly overrode Gate 1 before implementation and evaluation. Evaluation preceded independent review.

## Result and its exact scope

All six paths, for source rules **90, 54, 110, 157, 171 and 233**, pass native evolution, immediate-parent recovery and composed source recovery through 6D. Every intermediate floor passes: **30 of 30**, with no failure or censoring. The run took **92.112 seconds** outside GitHub Actions, with **1,197,015,040 bytes** peak process RSS (about 1.20 GB or 1.11 GiB).

The domain is every one of the **128 states of a width-seven source ring**, including every longitudinal position and every transverse phase combination. It is a complete finite invariant family, not a sampled trajectory population and not a full-shift certificate. Four-field recipes have transverse period four; the complemented temporal recipes have period five.

These are **newly synthesized native tables on that finite family**, using the published recipes. They do not retain the archived native tables' full-shift or G constraints. Each unforced derivative output is fixed to zero before the next lift; earlier native tables are never revised. No recursive G claim is made. No 256-rule 6D claim, arbitrary independently specified higher-dimensional input claim, or dimension-induction theorem follows.

The [protocol](protocols/sequential-lift-6d-pilot-20260914.md) was committed as 9d310d995caa97fe01d3db7d3e90a678973445a1 after Myk's explicit override. The [scientific implementation](../../scripts/sequential_lift_6d_pilot.py) was committed as 3b9aef11f78b7a23760c52de20cc43b83ce3fe02 before the run. Implementation sub-PR [#236](https://github.com/bombadil-labs/groovy-commutator/pull/236) is part of gathering [#235](https://github.com/bombadil-labs/groovy-commutator/pull/235).

## What repeats

Rules 90, 54 and 110 use the saved P/D/M/Q birth-mask, positive-sign, symmetric Q(-1,+2) recipe. Rule 157 uses the corresponding stay-one mask. Rules 171 and 233 use the published shared P/D/A2/M/Q recipe, with birth mask, A2=1 XOR X XOR H²(X), and Q=(NOT shifted-minus-one X) AND shifted-plus-two X.

The spatial vector is horizontal at the first lift. At subsequent lifts it also crosses the newest existing transverse axis. Each new coordinate repeats the same chosen field order. Binary alphabet and native radius two are unchanged.

The current object explicitly contains its fully specified native rule, its complete finite admissible family and its immutable recipe policy. The construction computes parent successors using that native rule and constructs a new phase-free native law and decoder from physical neighborhoods. It never queries the original ECA to execute an upper law.

This is a deterministic construction on those **decorated finite objects**. The initial recipe policy is declared and retained; no claim is made that a general lift can infer it from an arbitrary bare native-rule table. Above the initial source level, original-ECA computation appears only in the separate reference verifier; the production 1D base law is the original ECA.

## Verification and what the finite family proves

The run checks **11,886,336 native constraint cells**, every immediate-parent decoding constraint, two full native evolution steps per source configuration and floor, and composed decoding back to the original source. The separate source-based encoding implementation agrees on every complete compared configuration.

The original source set contains all seven-bit words, so it is invariant under each source ECA. Exact one-step intertwining on this complete family therefore extends to **all times within the family**. Decoding establishes injectivity on that family. Immediate-parent decoding has radius two; the composed source decoder may have larger effective radius.

Exact ordered tuple interning represents full 5^d-bit physical neighborhoods. Each identifier denotes an equality-checked tuple of child identifiers, with five-bit binary leaves. Physical phases never enter the native key as labels. Dict hash collisions cannot merge unequal keys, and appending cached identifiers does not change old identifiers or rule outputs.

The author self-test compared all 336 explicit patches on a synthetic 3D tensor, obtaining 81 distinct patterns, and checked conflicting-output rejection and unspecified-zero behavior. During the run, **450** separately extracted full physical patches match the compressed trees. An independent reviewing agent additionally checked 402 scalar patches in synthetic 2D/3D/4D tensors, 1,024 default-completion cases, translation equivariance and cache stability. This is independent bounded verification, not an independent full rerun.

Radius two observes every transverse coordinate of each period-four/five torus. In 6D the five-field paths have 400,000 distinct forced keys, the full 128-source-state by 3,125-phase count after longitudinal translations are identified. The rich observations make this a useful finite compatibility test, not evidence that equally small local descriptions will work on arbitrary inputs.

## Measured construction cost

These times construct one level for the entire 128-state family. They include parent-native evaluations, encoding and native/decoder compilation, and exclude the subsequent verification. They are one-run measurements, not a benchmark distribution or a universal asymptotic law.

| Lift | Four fields, four rules | Five fields, two rules |
|---|---:|---:|
| 1D to 2D | 1.98–2.56 ms | 2.58–2.80 ms |
| 2D to 3D | 14.82–16.93 ms | 23.57–24.12 ms |
| 3D to 4D | 87.71–112.13 ms | 184.35–188.61 ms |
| 4D to 5D | 0.508–0.625 s | 1.463–1.598 s |
| 5D to 6D | 3.321–3.758 s | 12.152–13.855 s |

At fixed source width and population, a p-field preparation has p^(d-1) physical fields per source site at dimension d. Thus a new dimension multiplies explicit state storage by p. Native compilation and verification have additional costs.

An arbitrary radius-two binary local rule receives 5^d neighborhood bits. Its unrestricted truth table has 2^(5^d) entries, so expanding the entire truth table is doubly exponential in dimension. This pilot stores only forced keys and a deterministic zero default. Ordered subpatch sharing avoids repeatedly writing all 5^d bits for each event, but the number of prepared phases still grows exponentially.

A pure generator is not necessarily a cheap generator. A nested symbolic descriptor could stay compact if it shares prior descriptions, while expanding states, compiling native laws, proving constraints or evaluating particular outputs could still be expensive. Extremely high-dimensional exploration requires a structural theorem or an efficient symbolic rule family, not extrapolation of these finite tables.

## Light cones and next boundary

For a full radius-r Moore neighborhood, the bounding backward dependency region of one output cell after T steps contains (2rT+1)^d sites. Restricting to its light cone removes irrelevant regions but still leaves exponential dependence on d. Actual dependence can be smaller for a particular rule. Sparse-defect methods also need a known evolving background; these prepared periodic families need not be sparse or quiescent.

There is no failed native/recovery floor to repair in this pilot. The next open question is whether the generator can preserve its guarantees as the declared source domain is enlarged, eventually using an input-independent local argument. Arbitrary higher-dimensional native automata and dimensional-floor recognition are separate, unrun questions. Recursive centered G remains untested here.

## Preserved evidence and reproduction

- [Canonical account](../../results/sequential_lift_6d_20260914.json).
- [Per-floor records](../../experiments/sequential_lift_6d_20260914/run/floors.jsonl), [raw summary](../../experiments/sequential_lift_6d_20260914/run/summary.json), and [execution environment](../../experiments/sequential_lift_6d_20260914/run/execution.json).
- [Cheap accounting verifier](../../scripts/verify_sequential_lift_pilot.py), registered in the shared integrity checker.

```sh
# Hash integrity and exact reconstruction from saved records; no scientific replay:
python scripts/verify_sequential_lift_pilot.py
# Bounded implementation controls:
python scripts/sequential_lift_6d_pilot.py --self-test
# Explicit off-CI replay, using the pinned implementation and an empty destination:
python scripts/sequential_lift_6d_pilot.py --output /tmp/sequential-lift-replay --implementation-commit 3b9aef11f78b7a23760c52de20cc43b83ce3fe02
```

Automatic CI only checks preserved hashes and reconstructs the canonical account. Raw timings are retained; replay times are not expected to match byte for byte. The scientific implementation and frozen protocol remain unchanged after evaluation. No recipes were searched or repaired after observing outcomes.
