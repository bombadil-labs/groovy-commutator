# Observation catalog — independent scientific review

Reviewer: Codex (OpenAI), `/root/relations_review`, 2026-09-15.
Author of primary experiment: Codex (OpenAI), `/root`.
Scope: frozen protocol, primary implementation and completed scientific outputs
for gathering PR #260 / sub-PR #261. This is not the final publication-head
Gate 2 comment; that separately reviews the combined diff and current checks.

**Scientific review passes.** The independently checked computations agree.
The result supports a negative conclusion about the seven frozen scalar
signatures under the specified ensemble change. It does not refute the full
observation catalog, spatial/temporal partition shape, the lift, or Class IV
discrimination in general.

## Protocol, implementation and independence

Gate 1 approved the scientific protocol at commit
`aaa0c3fcef7d500ec0a1bd5fd342658e8056019b`, before primary implementation.
The prospective numerical/header clarification at
`9cba5b33d4c84a7e655d17652a89936e4112b153` has protocol SHA-256
`e5ddef3d78f7bc6336e37a530cf52ebe037c7208f65d05aeeab9d917d282f7dc`.
Both approvals and their scope are recorded in `catalog-gate1.md` and signed
comments on #261. Implementation findings concerning negative-roundoff
assertions, input pins, transition witnesses, overwrite protection and censored
shortlists were resolved at `15967f733af1aa167fb92a3c107145f396a7a2c6` before
the primary evaluation. The evaluated primary script SHA-256 is
`a9946232dd347121adfd51b7ff8c240d5fc258e6fe20428692e7cec92364fc88`.

I authored the independent replay before inspecting the primary implementation,
then compared and reviewed the primary code. `catalog_oracle.py` imports no
primary implementation: finite evolution uses packed integers; entropy uses
tuple counters and `math.fsum`; partition equality uses first-occurrence
dictionary labels. Direct perturbation controls check the sensitivity formulas.
The primary author has cross-reviewed the oracle and comparison driver. The
executed source hashes, commands, results and output hashes are recorded in
`catalog-verification.json`. No discrepancy required changing the evaluated
oracle or comparison driver.

Discovery selection was committed at
`c17bc660acf22223b513f7b7e313107bacbf95f0` before confirmation. The committed
seal and raw confirmation agree on full-shortlist SHA-256
`662be922d672e50d816c50496a7d517a6b2a52845fa515bb8f760f8f9922f79d`.
The zero/near-zero normalization convention, metric-seven pair restriction,
all-rule normalization range, orbit scoring, fixed intervals and seed pairing
were respected. No confirmation reranking was used.

## Verification coverage

The physical finite replay panel was fixed at Gate 1: rules
`0,4,18,30,54,90,110,147`, widths seven, eight and nine, all 24 primitive fields,
source and spatial-successor maps, 300 candidates and seven metrics. All
49,824 defined metric values agree within `4.45e-15` (required tolerance
`1e-10`). Exact field and map arrays agree. The eight-rule local-context panel
also agrees on all 2,400 candidate alias IDs.

From the complete saved discovery table, I independently reconstructed all
2,076 ranking rows, including interval endpoints, normalization, negative and
disputed orbit overlaps and positive coverage. All seven winners agree. From
the complete confirmation tables, all seven width-nine verdicts and all 238
long-run interval verdicts agree.

For long runs I independently simulated both seeds of rules 30, 54, 110 and
the radius-two challenge: eight full trajectories, all 24 sampled primitive
words and all seven metrics for each selected slot agree. The maximum metric
error is `4.45e-15`. This is a physical replay of the preselected panel, not a
claim to have independently simulated all 34 long runs or all 256 finite rules.

The native audit independently reconstructed all 78 source-archive records,
all 98,280 attempted native views, all 25,960 matched views, all 104 completion
provenance contracts and all 240 published transition witnesses. Full archive,
member and prior relation-array hashes were checked against pinned inputs.

Archive source ordering is handled explicitly. Decoded rows are converted to
little-endian packed states, checked to be a permutation of the full state
set, evolved with the independent ECA updater, and mapped back through the
inverse permutation. The resulting source successor agrees with the primary
graph. Thus a reversed archive bit convention cannot silently reverse a
directed ECA update. The actual-order successor is used for native transitions
and basins. Period flags also agree with decoded-row periods.

The three comparison stages took 5.57, 2.15 and 48.73 seconds, with peak RSS
below 80 MiB. Independent finite generation took 2.46 seconds for discovery
and 6.28 seconds for confirmation. All are outside CI and below the frozen
per-process bounds. Direct controls cover 2,400 ECA sensitivity checks, 480
radius-two sensitivity checks, six entropy checks and two partition/basin
checks.

## Results and interpretation

| Slot (metric index) | Candidate | Width-nine core retained | Width-nine negative orbits overlapping | Long core samples retained |
| --- | --- | ---: | ---: | ---: |
| Entropy (0) | state + future2 | 6/6 | 3 | 0/12 |
| Successor uncertainty (1) | move_left1 + sensitivity_center | 6/6 | 2 | 0/12 |
| History gain (2) | change1 | 6/6 | 2 | 2/12 |
| Spatial information (3) | future2 | 6/6 | 5 | 0/12 |
| Target uncertainty (4) | move_left1 + move_right1 | 6/6 | 4 | 0/12 |
| Nondeterministic-block mass (5) | space_left + move_right1 | 6/6 | 9 | 0/12 |
| Pair gain (6) | state + change2 | 6/6 | 2 | 5/12 |

No slot retains both canonical rules 54 and 110 at both seeds. Width-nine
retention alone is therefore not a stable Class IV signature. The twelve long
core cases comprise six symmetry members at two seeds; they are not twelve
independent positive families, and their time/site observations are dependent.

At D3/D4, rule 54's matched root observation is only candidate 15, the constant
center-sensitivity partition. Rule 110 has no match in the chosen catalog on
the older-coordinate-zero slice. These statements concern the frozen 210
native observations at each of six phases. Cross-phase decoders are outside
that panel. Omitted native sensitivities and G are not guaranteed determined
by the on-family constraints; the audit assigns no arbitrary completion.

The frozen provenance categories agree, including zero pairs with both
endpoints of full spatial period in the width-eight 54/110 D3/D4 cases.
An explicitly **post-hoc** direct endpoint inspection finds every pair in
these four cases has periods `(4,4)`: counts are 216, 1,296, 72 and 432 for
54/D3, 54/D4, 110/D3 and 110/D4. This strengthens the finite-ring description
of those specific pairs; it is neither a preregistered classifier nor a
general mechanism theorem. `catalog_period_witnesses.py` reproduces all four
counts and concrete decoded endpoint strings without changing frozen scores.

Signed: **Codex (OpenAI), `/root/relations_review`, 2026-09-15.** No remaining
scientific blockers in the reviewed primary implementation and stated results.
Exact publication-head review and applicable green checks remain the final
Gate 2 requirements.
