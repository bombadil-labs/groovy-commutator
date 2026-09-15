# Unspecified entries change what cohabitation means

Comparing completed tables can erase genuine compatibility between lifted partial rules. In this audit of the current six-field D2 cache, 20,944 of 32,640 distinct root pairs admit a common completion after combining the width-seven and width-eight constraints. No pair has identical individually completed tables under any of four fixed default policies. The two predicates answer different questions.

Evidence: exact on the specified finite source families. Authored by: Codex (OpenAI), Myk's dimensional-lift session, 2026-09-15. Independently reviewed by: Codex collaborating agent `/root/response_review`, 2026-09-15, after evaluation under Myk's standing Gate 1 approval. Final integration requires signed review of the publication head. The [frozen protocol](protocols/partial-cohabitation-20260915.md), [implementation](../../scripts/partial_cohabitation_20260915.py) and [canonical result](../../results/partial_cohabitation_20260915.json) preserve scope and execution provenance.

## What was audited

The uniform six-field cache stores forced physical-neighborhood entries separately from its default. Its default is a **zero flip mask**, meaning retain the current cell. That is different from setting the next cell to zero, which requires a flip mask equal to the center bit. The source [reader](../../scripts/read_uniform_jet6_cache.py) preserves the forced domain; no cache information was lost and no lift had to be rebuilt.

The historical cohabitation implementation associated with the dialogue's approximate 39% pair count and clique 48 was not found in the inspected main-branch directories or PR search. GitHub code search returned incomplete results. The supplied discriminator handoff points to a separate Claude workspace. Consequently this audit does **not** establish that the historical code confused unspecified entries with zeros, nor reproduce or invalidate those numbers. The present six-field/radius contract also differs from older constructions. The scope of this audit is its explicitly named current cache.

Inputs are all 256 ECA roots at D2 and complete source rings of widths 7 and 8 from the [preserved uniform-six-field archive](2026-09-14-uniform-jet6-cache.md). Child grids have six transverse rows; their native neighborhood is seven rows by five columns, with radius [3,2]. A key is the actual row-major 35-bit neighborhood, not a rule-specific interned identifier. All pinned flip entries are validated against the archived source-indexed successor, with source recovery and scalar physical-key checks. Decoder requirements are separate and do not enter native-rule cohabitation.

These source families are finite and invariant. The period-six preparation means even many ambient physical neighborhoods cannot occur on a beam. Complete enumeration of these rings is not complete enumeration of arbitrary infinite source states. Nor does native-rule cohabitation require one common decoder.

## Compatibility, completion cost and distance

Fix one common finite neighborhood and let M be its number of binary input patterns (here M = 2^35). A partial flip rule P assigns a bit on its forced domain K_P. Its completion family Ext(P) contains every full local Boolean rule extending those assignments, with no additional symmetry or other extension restrictions.

Two partial rules cohabit exactly when

$$
P(q)=Q(q)\quad\text{for every }q\in K_P\cap K_Q.
$$

Forced zero is a commitment just as forced one is. Unspecified is neither. If P and Q are compatible, their union defines a partial rule and

$$
|\operatorname{Ext}(P)\cap\operatorname{Ext}(Q)|
=2^{M-|K_P\cup K_Q|}.
$$

Thus the fraction of P's completions that can also host Q is

$$
\frac{|\operatorname{Ext}(P)\cap\operatorname{Ext}(Q)|}
{|\operatorname{Ext}(P)|}
=2^{-|K_Q\setminus K_P|}.
$$

Admitting Q costs exactly one additional truth-table commitment per key it pins outside P's support. Any conflict instead makes the common completion family empty. These are counts of independent table assignments, not measurements of a system's past memory or future behavior. Pairwise compatibility also suffices for a whole collection: no key receives contradictory demands, so the union extends to a single common rule. Additional restrictions on allowed completions could invalidate that implication.

Post-evaluation analytic observation, without a new score or evaluation: let c(P,Q) be the number of conflicting shared entries. Then

$$
\min_{f\in\operatorname{Ext}(P),\,g\in\operatorname{Ext}(Q)}d_H(f,g)=c(P,Q).
$$

Every conflicting entry forces one disagreement. At every other entry, at least one compatible shared value can be chosen, achieving the lower bound. This distance is independent of default fill, although it still depends on the chosen neighborhood and forced source families. It is a symmetric minimum separation between sets; it need not satisfy the triangle inequality. For example a rule pinning q to zero and another pinning q to one both have zero separation from a rule leaving q free, but separation one from each other.

## Results

All 512 archived records validate. Each root's two-width assignments agree wherever they overlap, allowing a consistent pooled partial rule for every root. The full comparison took **4.299774 seconds**, including archive verification and record extraction, with peak resident memory **68,972 KiB**. No new lifts or trajectories were generated.

| Forced source domain | Compatible pairs | Fraction of all 32,640 pairs | With shared pinned entries | With no shared entries |
| --- | ---: | ---: | ---: | ---: |
| Width 7 | 22,528 | 69.020% | 15,865 | 6,663 |
| Width 8 | 20,954 | 64.197% | 14,753 | 6,201 |
| Pooled widths 7 and 8 | 20,944 | 64.167% | 14,743 | 6,201 |

For each domain, **all four** individually completed-table equality counts are zero: no-flip, flip, output-zero and output-one. Equality was checked using deviation sets from each common policy; outside the union of forced domains both tables use the same policy and already agree. Every reported compatible pair would therefore be a false conflict if individually completed equality were substituted for partial cohabitation. This is a demonstration of a bad substitute, not evidence that the unavailable older code used it.

The difference is visible at one actual key. For roots 0 and 1, physical key 1,048,544 is forced to flip by root 0 and unspecified by root 1. They cohabit, but root 1's no-flip completion disagrees at this key. Forcing it to flip in a shared completion is allowed.

Width 7 has 1,584 edges absent at width 8; width 8 has ten absent at width 7. Pooling retains exactly their 20,944 common edges in this experiment. The two rings' constraint sets are not nested. In general, cross-width constraints could remove additional edges even when an edge exists separately at both widths; none do here. Adding constraints to a fixed partial rule can remove compatibility, never add it. This is a reason to keep source-domain size explicit in any future statistic.

## What this says about the Class-IV proposal

Raw compatibility still does not isolate the two primary Class-IV families. Pooled counts, excluding self:

| Root | Compatible partners | Partners with shared pinned entries |
| --- | ---: | ---: |
| 0 | 255 | 127 |
| 204 (identity) | 127 | 127 |
| 54 | 183 | 81 |
| 110 | 157 | 52 |
| 122 | 184 | 94 |
| 126 | 184 | 81 |

Identity does not lead this raw count, but rule 0 does. Removing vacuous overlaps also leaves rule 0 above 54 and 110. The historical identity-winning metric is a different, unavailable calculation and is not silently replaced. The archived class convention is retained, with 54/110 reported as the two core positives and disputed 41/106 kept separate. All per-root counts and descriptive class summaries are preserved; no threshold or classifier was fitted.

Post-run inspection of the frozen pair matrix finds that 54 and 110 agree at 24 shared pinned entries (12 zeros, 12 ones) and disagree at one. They are incompatible under the pooled contract, with minimum completion separation one. The independent audit identifies key 553,910,272: 54 requires a flip, 110 requires no flip. Width seven alone has 13 shared agreements and no conflict; width eight exposes the contradiction. Rules 54 and 126 instead agree on all 103 shared entries; admitting 126 into the 54 completion family costs 1,176 additional pins, while the reverse costs 1,020. Compatibility therefore does not mean cost-free admission. These examples illustrate the definitions; they do not establish a class mechanism or authorize changing the pinned dynamics to improve compatibility.

The older claim that every complement pair cohabits is not imported. Under this current contract, 64 of 128 distinct output-complement pairs cohabit in every tested domain. Boolean conjugation is different: 117 of 120 pairs cohabit at width 7, and 112 at width 8 or pooled. Counts under another recipe, radius, decoder requirement or complement convention cannot be transferred without checking those assumptions.

## Evidence and continuation

The result records every original member hash, source and label hashes, every root's counts, all cross-width consistency checks and example witnesses. A compact raw archive preserves the 512 physical partial tables, 97,920 pair rows, source freeze and independent audit. Its identity and every member digest are in the [raw archive manifest](../../experiments/partial_cohabitation_20260915/raw-archive.json). The [independent dictionary/set audit](../../review/partial_cohabitation_independent.py) reproduces all 97,920 pair records and 391,680 completed-equality predicates without importing the author's comparison implementation. It also checks every original member digest and independently reconstructs 44 selected physical tables, with decoder and successor checks. Exhaustive 729 small partial-table pairs confirm the count and minimum-distance formulas. Its [report](../../review/partial_cohabitation_independent.json) records the passing audit, which took 18.840258 seconds without new lifts or trajectories.

Automatic CI runs only semantic toy controls and source/input integrity. Full archive extraction and pair evaluation run outside Actions. The preserved original cache remains the authoritative input for a fresh replay; the smaller raw bundle supports independent analysis of the extracted tables.

The useful result is a clean account of shared constraints, additional commitments and unavoidable conflicts. Arbitrary completions should remain explicit simulation choices. A subsequent scientific question is what the specific conflicting neighborhoods mean dynamically, under a fixed native rule and source-domain contract. No dynamic discriminator, new threshold, broader-radius test or maximum-clique search is established by this unit. The preceding [completion-response failure](2026-09-15-response-quotient.md) remains unchanged.
