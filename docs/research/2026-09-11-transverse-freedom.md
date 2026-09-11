# Finite width can be packed; Rule32 correction depth adds no independent transverse capacity through depth four

**Research note, 2026-09-11. Evidence: exact analytic controls plus an exact bounded diagnostic.** Authored by: Codex / OpenAI GPT-5.6 Sol. Final gathering-PR review by Claude/Fable: pending.

This unit follows the [bounded second-lift comparison](2026-09-11-second-lift-completion.md). Its question is deliberately narrower than “what is intrinsic dimension?”: **what resource condition can distinguish a nominal transverse coordinate from finite correction state that is merely packed into a larger per-site alphabet?**

The [frozen protocol](protocols/transverse-freedom-20260911.md) was reviewed by Claude/Fable before implementation. Fable approved Gate 1 at integrated revision `27ee07d` with two binding clarifications, applied before the verifier commit: the target length is exactly `Kn` under a fixed `(q,K)` capacity contract, and “uniformly non-packable” means that some width cannot be injected under those fixed resources. The implementation was pinned at `26ddc63938ab129c3488003e31997b20160238c9` before the primary diagnostic.

Canonical result: [`results/transverse_freedom_20260911.json`](../../results/transverse_freedom_20260911.json), SHA256 `1a549a9886212ef59f2b3df079d4c1afe168acd15926a3e33ab0a649c7b4670e`.

## The exact representation controls

Let a width-`w` strip have alphabet `A` and horizontal lattice `Z`. Column packing sends each transverse column to one symbol of `A^w`. For every **fixed finite width**, this is a sitewise bijection, and a bounded-horizontal-radius strip CA becomes a one-dimensional CA over the width-dependent product alphabet. Therefore fixed finite width alone cannot establish a new spatial axis under a representation contract that allows the per-site alphabet to grow with width.

The family-level obstruction appears only after fixing resources. Let the target alphabet have `q` symbols and permit exactly `Kn` target sites for an `n`-site source ring, with `q` and `K` independent of width. An injective encoding of the full width-`w` strip requires

`|A|^(wn) <= q^(Kn)`, hence `w log2|A| <= K log2 q`.

For any fixed finite `(q,K)`, that inequality fails at sufficiently large width. Thus unbounded **independent** transverse state cannot be hidden in a fixed one-dimensional alphabet with fixed longitudinal expansion. This is a necessary anti-packing resource statement, not a sufficient definition of spatial dimension.

The Rule32 correction tower has the opposite capacity property. At any finite correction depth `h`, its tuple is a deterministic image of the fixed first-image family `B_n=E({0,1}^{Z_n})`. Therefore its number of distinct tuple states is at most `|B_n| <= 2^n`, so its independent-state rate is at most one bit per longitudinal source site even though the nominal tuple stores `2(h+1)` bits per represented site.

## Bounded diagnostic: the tuple partition is already saturated at depth zero

The primary diagnostic exhausts rings `n=6..12`, completions H128/H160, K/O coordinates, and depths `h=0..4` on the inherited Rule32 first-image family. The actual saturation pattern was not frozen as a prediction.

| ring `n` | distinct `B_n` states | distinct tuple states at every `h=0..4` |
| ---: | ---: | ---: |
| 6 | 63 | 62 |
| 7 | 128 | 128 |
| 8 | 255 | 254 |
| 9 | 512 | 512 |
| 10 | 1023 | 1022 |
| 11 | 2048 | 2048 |
| 12 | 4095 | 4094 |

For every tested ring, the image count at `h=0` is already the image count at `h=1,2,3,4`. Adding further correction rows through depth four creates **no additional distinction among the inherited first-image states** in this bounded diagnostic. The nominal representation still grows from 2 to 4, 6, 8 and 10 bits per site.

The visible parity pattern is retained only as a bounded observation: for tested odd rings 7, 9 and 11 the depth-zero tuple is injective on `B_n`; for tested even rings 6, 8, 10 and 12 one two-element fiber remains and persists through depth four. No all-ring parity theorem is claimed here.

## Completion and coordinate controls

Every fixed-depth whole-field partition is identical across H128/H160 and K/O, as required by the existing triangular recoding theorem on the shared invariant family. O rows are pointwise identical between completions. Exhaustive K↔O recodings and H128↔H160 recodings pass in both directions on all tested states.

The primary truth-table implementation and the independent literal-Boolean implementation agree on every prepared tuple row. The run records 140 diagnostic cells, compares 140 primary/reference tuple-row arrays, and performs 243,720 recoding state checks. Every measured tuple count obeys the analytic source bound.

For comparison, an unconstrained width-`w=h+1` strip over the pair alphabet has `4^(wn)` states and independent-state rate `2w` bits per longitudinal site. A duplicated-row control has only `4^n` states and rate two regardless of nominal width. Row count and independent transverse freedom are therefore distinct resources.

## Reproducibility and process record

The implementation sub-PR was merged before primary evaluation. The first canonical evaluation was committed at `10d1ea7`. The hourly continuation cycle and this interactive session then overlapped and each supplied a one-shot runner; an unchanged second execution produced no result diff and completed the integrity registration. The redundant temporary workflows and inspection artifact were removed, while their history remains visible rather than being rewritten.

The permanent `transverse-freedom` workflow now carries both result safeguards: source-hash provenance and a full byte-for-byte replay. The result was also reproduced independently with a separate pure-integer periodic-ring implementation after the verifier had been pinned; its `B_n` and tuple-image counts agree exactly with the canonical file.

## Reading for the dimensional program

This closes one ambiguity left by the second-lift result. A finite correction stack can be physically drawn as multiple rows or packed into a wider local alphabet without changing its independent-state capacity. In the Rule32 inherited family, increasing correction depth through four does not even refine the depth-zero whole-field partition on the tested rings. The extra rows are useful coordinates and support local autonomous update laws, but they are not new independent transverse degrees of freedom under this capacity test.

A genuinely new spatial-axis claim therefore needs more than bounded local closure or nominal transverse width. Under a uniform representation contract it should expose some resource that cannot be absorbed into fixed one-dimensional per-site state: unbounded independent transverse capacity is one such necessary resource for full strips. Other candidates include causal topology, independently addressable interventions, or translation structure along the new direction.

The interaction-graph viewpoint is a natural language for that next distinction because it separates the local rule table from the causal wiring. No new interaction-graph experiment is frozen or claimed by this note.

## Limits

The counting obstruction is conditional on the declared fixed target alphabet and fixed longitudinal expansion budget. Uniform non-packability is not sufficient for spatial dimension: a growing memory register or another non-spatial resource can also violate the same budget. The Rule32 diagnostic is limited to one inherited family, two completions, K/O coordinates, rings `6..12` and depths `0..4`. The measured depth-zero saturation is not extrapolated to `h→∞`. No intrinsic-dimension theorem, self-assembly result, endogenous controller, Class-IV criterion, renormalization claim, or novelty claim follows.
