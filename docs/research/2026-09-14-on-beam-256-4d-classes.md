# Do lifted on-beam rules reveal Wolfram classes?

Status: exploratory class associations; exhaustive native evolution/recovery checks on the stated finite domains. Gate 2 is tracked in [gathering PR #238](https://github.com/bombadil-labs/groovy-commutator/pull/238).

Authored by: Codex (OpenAI), Myk's dimensional-lift session. Reviewed by: independent collaborating agent at prospective Gate 1; completed-unit review is recorded at the exact gathering head before merge.

All 256 ECA sources lift through 4D on both complete source rings tested. The lifted measurements show class-related structure, but fail the preregistered incremental classification criterion. In particular, high source-coordinate algebraic degree does not consistently accompany Class III. Native table size is also a poor discriminator.

## Scope and provenance

The [protocol](protocols/on-beam-256-4d-classes-20260914.md) was independently approved before implementation and evaluation: reviewed SHA `07d8d61c2dd7e71ce7d4eafb01b58cbdd168d935`, [signed Gate 1](https://github.com/bombadil-labs/groovy-commutator/pull/238#issuecomment-5669803413), 2026-09-14. The approval was recorded at `7651bb93`; implementation was frozen at `4e7bd6d01956600552a6d5c08aba7d441eaedd19`. The primary run began at 2026-09-14T19:56:49Z from that implementation. This unit has prospective review despite the preceding six-rule pilot's authorized Gate 1 exception.

Baseline main was `a2dfba2801ac6f53d7cea4306927c5b6f246f140`, after the [6D pilot](2026-09-14-sequential-lift-6d-pilot.md). The source-dependent four-field recipe for every rule is taken unchanged from [the saved coverage CSV](../../results/binary_lift_20260914/rule_coverage.csv). No recipe was reselected from these outcomes. There are 19 recipe combinations; the fixed birth/+1/pair(-1,2)/PDMQ stratum contains 64 rules. Unlike the preceding six-rule pilot, this unit uses the archived four-field recipes for 171 and 233 too.

The negative-sign extension is explicit: P shifts horizontally by sign and by +1 along the newest transverse axis; a Q offset a shifts horizontally by a and transversely by a times sign. M uses the selected birth, death, stay-one or stay-zero mask. Controls compare these formulas to a scalar field constructor, including negative signs and directed Q.

## What was computed

For each width 7 and 8, all 256 rules and every source word (128 or 256 words), the construction recursively creates 2D, 3D and 4D families with period four along each new axis. Each floor synthesizes a binary radius-two native derivative and an immediate-parent decoder from full physical neighborhoods. Ordered five-tuple DAGs losslessly represent the 5^d neighborhood bits; neither phase labels nor source coordinates are runtime inputs to the native law.

Each parent law is deterministically completed and fixed before construction of its child. Unforced derivative entries are zero, meaning **no flip**, and unforced decoder entries are zero. The finite family is invariant because it includes every source word and the original ECA step stays on the same ring. The verified one-step intertwining and decoding therefore extend to all times within that family. Two complete native steps, composed source recovery, immutable parent hashes and an independent whole-state encoding oracle were also checked at each floor.

| Quantity | Observed |
| --- | ---: |
| Paths through 4D | 512 / 512 |
| Native floors and decoders | 1,536 / 1,536 |
| Failures / censored paths | 0 / 0 |
| Native constraint cell events | 63,307,776 |
| Direct physical-patch/export checks | 23,040 |
| Total local wall time, including exports and analysis | 232.918 s |
| Peak process RSS | 197,550,080 bytes |
| Compressed exact rule archive | 132,520,034 bytes |

During final review, Myk supplied a proposed uniform six-field, period-six construction. This completed four-field census does not evaluate that new construction; its class associations and timings must not be transferred to it. A common recipe would remove a source of variation in a future comparison.

These are newly synthesized native tables on finite invariant families. They do not retain the earlier symbolic full-shift/G constraints. This does not establish recursive G, arbitrary infinite inputs, arbitrary native higher-dimensional automata, a bare-C generator, or dimension induction. The current construction carries the explicit finite family and recipe policy. Width eight resynthesizes the laws; it tests robustness of the construction and measurements, not generalization of the width-seven completed law.

## Class convention and independent units

Labels were frozen from Martínez's [A Note on Elementary Cellular Automata Classification](https://arxiv.org/pdf/1306.5577v2), Table 2, and checked against Castillo-Ramirez and Magaña-Chavez's [A study on the composition of elementary cellular automata](https://arxiv.org/pdf/2305.02947), Table 1. This convention places representatives 41, 54, 106 and 110 in Class IV. Class assignments are published behavior labels, not a claim that the small rings in this experiment independently establish those behaviors.

Reflection and state-complement conjugacy were computed algebraically, giving 88 symmetry orbits. The orbit counts for I/II/III/IV are 8/65/11/4; expanded rule counts are 24/192/26/14. Features are averaged equally across members of an orbit; one whole orbit is held out per prediction. All 88 orbits qualified at both widths, with no exclusions. Treating the 256 rule numbers as independent examples would inflate the effective sample.

A frozen sensitivity removes the entire 41 and 106 orbits, retaining 54 and 110 as the two Class IV representatives. It does not relabel those excluded orbits. With only four primary and two sensitivity Class IV examples, apparent recall differences are fragile.

## What the measurements mean

The native rule is a partial function on its forced physical neighborhood domain. We preserve that domain, its derivative outputs, and decoder outputs, without interpreting the arbitrary off-beam completion as observed behavior.

Seven features are measured at every lifted floor: normalized forced-key count, forced-key flip fraction, event-weighted flip fraction, mean algebraic degree, mean algebraic-normal-form term count, affine-phase fraction, and GF(2) rank across phases. The last four are **pulled back to the original source bits** at longitudinal position zero: each phase supplies one Boolean function of all source bits. They measure the lifted rule in source coordinates, not the minimum polynomial degree or circuit size of its partially specified native rule. Constants have degree zero; the zero function has zero terms.

At 4D there are 64 phase functions. Rank counts independent truth-table rows under XOR. Degree measures the largest number of source variables appearing together in an algebraic-normal-form term, then averages over phases. These are distinct properties: many independent functions can each have low degree.

## Results by class

The table reports means of orbit averages at 4D; degree is divided by width, and rank by 64. Both are bounded by one.

| Class | Degree, width 7 | Degree, width 8 | Rank, width 7 | Rank, width 8 |
| --- | ---: | ---: | ---: | ---: |
| I | 0.652 | 0.642 | 0.643 | 0.655 |
| II | 0.742 | 0.719 | 0.790 | 0.800 |
| III | 0.682 | 0.652 | 0.938 | 0.942 |
| IV | 0.885 | 0.858 | 0.969 | 0.975 |

The rank tendency in P2 is supported descriptively; its general higher-degree expectation for III/IV is only partly supported. Class III's mean degree lies below Class II at every measured dimension and both widths. Class IV has the highest all-recipe mean degree at every measured dimension and width, but the class distributions overlap. At width eight, the Class II rank range is 0–1 and its degree range is 0–0.915, containing the Class IV means.

Holding the declared recipe fixed retains the main 4D pattern. Degree means for I/II/III/IV are 0.654/0.756/0.667/0.878 at width seven and 0.646/0.737/0.639/0.851 at width eight; rank means are 0.642/0.813/0.897/0.964 and 0.654/0.826/0.900/0.974. That stratum has 8/25/5/3 represented orbits and does not eliminate every encoding or sampling effect. Within-orbit ranges are preserved in the analysis; the measurements are not symmetry-invariant fingerprints under this recipe policy.

A concrete comparison from the saved raw rows illustrates why key count alone is insufficient. These individual-rule examples are post hoc illustrations, not a newly scored hypothesis:

| Rule (published class) | Forced keys, 2D | 3D | 4D | Mean source degree, 4D | Rank out of 64, 4D |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0 (I) | 443 | 2,025 | 8,097 | 0.813 | 15 |
| 90 (III) | 507 | 2,025 | 8,097 | 3.031 | 61 |
| 54 (IV) | 475 | 2,025 | 8,097 | 6.078 | 61 |
| 110 (IV) | 457 | 2,025 | 8,097 | 6.375 | 63 |

All four have the same 4D key count. Rule 90 is distinguishable from 54/110 by degree, even though their ranks are close. This motivates examining degree and rank together; it does not establish a class boundary.

## Frozen prediction comparison

The classifier is leave-one-orbit-out nearest class centroid, with training-only feature scaling, equal class treatment and fixed tie handling. There is no fitted feature selection or hyperparameter search. Balanced accuracy is the mean of the four class recalls; a label-independent predictor has a 25% expectation.

| Feature view | Width 7 | Width 8 |
| --- | ---: | ---: |
| Source derivative and image features | 40.20% | 32.91% |
| Encoding recipe | 34.60% | 34.60% |
| Source + recipe | 42.74% | 42.35% |
| 2D measurements | 46.06% | 48.33% |
| 3D measurements | 52.66% | 56.47% |
| 4D measurements | 48.50% | 50.77% |
| All 2D–4D measurements | 55.35% | 56.86% |
| Source + recipe + all lifts | 40.58% | 40.20% |

**P1 passes; P3 fails.** Adding the lift features reduces balanced accuracy by 2.155 percentage points at both widths. P3 required an improvement of at least five points at both widths and a one-sided global label-permutation p at most 0.05 at width seven. The observed p is 0.595 over the frozen 199 permutations. This null assumes global orbit-label exchangeability; it is not a conditional test preserving the baseline source-label relationship, and is not a test of information creation.

The lift-only result is descriptively encouraging, but does not rescue P3. More dimensions are not monotonically better: 3D alone scores above 4D alone at both widths. In the sensitivity omitting 41/106, all-lift balanced accuracy is 62.72%/64.61%, but incremental performance remains negative (−8.36/−6.85 points). The two Class IV core orbits predict each other under the all-lift view; many Class II/III orbits are also predicted as IV. Confusion matrices and paired held-out predictions are saved, so high Class IV recall must not be read as high precision.

These statistics concern a fixed summary and classifier. They do not show that lifted rules contain no useful class information, or that classification cannot improve with other methods. No post hoc classifier tuning was performed.

## Preservation, verification and replay

The [canonical account](../../results/on_beam_256_4d_20260914.json) binds the scientific implementation, protocol, labels, recipes, raw records, archive manifest and post-run accounting verifier by SHA-256. [Raw floors](../../experiments/on_beam_256_4d_20260914/run/floors.jsonl), [paths](../../experiments/on_beam_256_4d_20260914/run/paths.jsonl), [analysis](../../experiments/on_beam_256_4d_20260914/run/analysis.json), [execution](../../experiments/on_beam_256_4d_20260914/run/execution.json) and [manifest](../../experiments/on_beam_256_4d_20260914/run/archive_manifest.json) are preserved without edits.

The exact archive contains 1,536 canonical JSON members named `w7/rule000/d2.json` through the corresponding width-eight/floor-four cases. Every member includes the signed column-delta DAG, forced derivative and decoder bit streams, source-phase truth matrix, and recipe. The scientific module's `restore_partial` decodes it; `expand_saved` expands a root to the exact ordered physical bits.

**Post-evaluation storage deviation:** the unchanged 132,520,034-byte gzip archive was delivered to Myk as a private, durable downloadable artifact. Its generated base64 transport parts are not committed to main, to avoid roughly 177 MB of additional Git checkout on every CI job. The public repository supplies reproduction code and complete archive/member/transport-part hashes, not public access to those privately preserved bytes. Scientific files, definitions and outcomes were not changed. The archive SHA-256 is `a64ea2e7ecd7b54bf3f3bf68e9fb0fa3cf49eecdc8a997768be5c664d76f8fce`.

The post-run accounting verifier checks all raw rows and rescores the frozen analysis. With an explicit archive path it also streams every member, verifies all hashes and binary shapes, checks DAG references and bit padding, and recomputes source-phase degree, term count, rank and flip statistics. Automatic CI performs the first tier only; it does not fetch or validate external archive bytes or rerun CA synthesis.

```bash
python scripts/verify_on_beam_256_4d.py
python scripts/verify_on_beam_256_4d.py --archive /path/to/partial_rules.tar.gz
```

For complete local scientific reproduction, use the pinned implementation with Python 3.12 and NumPy 2.3.5:

```bash
python scripts/on_beam_256_4d.py --self-test
python scripts/on_beam_256_4d.py --output /tmp/on-beam-replay --implementation-commit 4e7bd6d01956600552a6d5c08aba7d441eaedd19
```

Use a new output directory; do not overwrite the preserved run. Archive and analysis bytes are deterministic; wall-clock/RSS/provenance metadata are not. The run also produces numbered base64 transport parts; concatenating their decoded bytes in manifest order reconstructs the gzip, which must match the recorded archive hash. No replay runs in GitHub Actions.

Implementation controls passed before evaluation: 192 scalar field cases, 12 earlier-pilot floor cases, exhaustive symmetry checks, known Möbius/rank controls, and lossless export controls. Independent review separately checked the classifier against literal training-only fits and the signed DAG codec. A separate implementation then verified every archive member and all 253 transport parts, all saved source-phase metrics, all 512 source baselines, every fixed model view and all 199 permutations. It executed 24 bounded fresh floors from the exports for rules 3, 77, 179 and 232 at both widths; this is not a full native census replay. The [review script](../../review/on_beam_256_4d_review.py) and [review evidence](../../review/on_beam_256_4d_review.json) preserve that independent verification. A dormant implementation limit was noticed after launch: a deadline during final archive splitting would escape the censor handler. It was not triggered; this run finished well within its 900-second total budget. The pinned code is retained unchanged.

## Next question

The useful object for further work is the sequence of forced domains, output functions and decoders across dimensions, with off-beam choices left explicit. This census suggests investigating the joint evolution of source-coordinate degree and rank, and separately seeking compact native rules valid on their forced domains. Any new feature search should be a new exploratory unit, followed by a frozen robustness test. Neither a Wolfram-class theorem nor general lift induction follows from this census.
