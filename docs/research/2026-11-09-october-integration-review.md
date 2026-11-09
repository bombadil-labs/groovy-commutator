# Review and integration of the October 2026 gathering branches

**Date:** 2026-11-09. **Reviewer:** Claude (`claude-fable-5-2`), designated by
Myk as reviewer for this housekeeping pass. **Reviewed revisions:** the heads
of pull requests 316 and 318 through 329 as they stood on 2026-10-08 (listed
below). This is a reproduction-and-consistency review. It is not a line-by-line
audit of roughly 28,000 added lines, and the limits are stated at the end.

## Why this unit exists

`main` stopped on 2026-09-25 with no queued work. Thirteen draft pull requests
from 2026-10-06 to 2026-10-08 then sat unmerged, most of them stacked on one
another instead of on `main`, and most marked `Reviewed by: none`. A reader
following the agent guide could not find the project's newest results. This
unit reviews that work, combines it into one branch based on `main`, records
what was checked, and applies the corrections the review produced.

## What was integrated

| Pull request | Head | Unit | Prior review |
| --- | --- | --- | --- |
| 316 | `cocycle-lift-20261006` | Typed difference geometry; near-ring reading; Rules 4 and 200 | none |
| 318, 319, 320 | `asymptotic-closure`, `-wedge`, `-scaling` | Reserve corridor under block parity, and its census control | independent census by Claude (Fable) |
| 321, 322 | `matched-history-transport`, `rule110-pg-closure` | Rule 62 against Rule 110; parity plus Groovy is a readout, not a state | none |
| 323 | `rule110-latent-q` | Exact future-equivalence bound on any repair of parity plus Groovy | none |
| 324, 325, 326, 327 | `commutator-jet`, `-language`, `-fibers`, `jet-control-panel` | The commutator jet and its hidden fibres | none |
| 328 | `jet-gqr-256-fibonacci` | 256-rule census; Rule 54's all-depth invisible pair language | `claude-fable-5-1`, changes applied |
| 329 | `jet-full-line-autonomy` | Full-line autonomous jets and sharp radii | `claude-fable-5-1`, changes not applied |

The closed pull request 317 froze a protocol that was never evaluated; its one
file is not integrated and its branch is recorded in
[the branch disposition](archive/branch-disposition-2026-11-09.md).

The seven independent heads were merged in dependency order with merge commits,
so every original commit is preserved. Conflicts occurred only in shared
ledgers and registries: the findings and direction pages, one checkpoint, the
knowledge and program registries, and the integrity registry. They were
resolved by keeping both sides. One program summary could not be combined
mechanically and was rewritten by hand.

## What was run

All of the following pass on the combined branch.

- `scripts/check_result_integrity.py`: every registered result.
- All eleven verifiers the October work added, including both independent
  pair-graph replays for the jet units.
- The Python test suite: all 79 pass, once the relational-search experiment's
  pinned `swipl-wasm` Node package is installed.
- The site's research tests and build.

Three environment facts were needed to get there, and each is a finding:

1. On a default Windows checkout the integrity check reports 95 failures,
   because line-ending conversion changes the hashed bytes. In a checkout with
   conversion disabled it reports none. This predates October.
2. `scipy`, `sympy` and `pytest` were required and not declared in
   `requirements.txt`.
3. Two hashed runners import the Unix-only `resource` module. They were run
   with a stand-in on Windows; the runners themselves are hashed and were not
   edited.

## Independent recomputation

Separate integer-coded code, written from the knowledge entries' definitions
and not from the units' own scripts, is kept as
[the review reproducer](reproducers/review_october_20261109.py) and
[the census reproducer](reproducers/review_census_20261109.py). Every check
agrees with the notes.

| Unit | Claim recomputed | Result |
| --- | --- | --- |
| 316 | Rules 4 and 200 are idempotent, XOR to the identity and annihilate each other | exact, 12-cell ring |
| 316 | Centered `G` equals the distributivity defect `R(𝟙, D)` of the centered rule, and `G(0) = H(0)` | all 256 rules |
| 318 to 320 | Reserve of the stable block-parity quotient for Rules 30, 54, 110 and 184 at widths 16 and 18 | all eight values to the printed precision; depths 7 and 6 at width 18 |
| 318 to 320 | Imported census: 55 of 88 in the corridor, 41 of 88 with growth | exact match, same 41 rules |
| 321 | Whole-field parity plus centered `G` determines the next parity for Rule 110 and not for Rule 62 | widths 12, 14, 16 |
| 323 | The coarsest autonomous refinement of parity plus `G` has `2^n − 2` classes and merges only the uniform and alternating pairs | every even width 6 to 18 |
| 324 | `D_110` is Rule 162 and `D_62` is Rule 242 | exact |
| 324 | Cadence identity `C_{H²}(G) = R ⊕ B_H(H∘G, Q) ⊕ H(0)` | all 256 rules; also derived by hand |
| 329 | Rule 54's five-field jet keeps 261,985 of 262,144 states at width 18 | exact match |
| 329 review | Bits forgotten by `(G,Q,R)` at width 20 | matches the review's four figures |

The jet recurrence `A_k(HX) = H(A_k X) ⊕ A_{k+1}(X)` is the definition of
`A_{k+1}` rearranged. It is an identity and needs no check; the notes use it
correctly as an induction step.

## Findings

**1. A knowledge page contradicted its own registry entry.** The page for the
asymptotic-closure corridor was still titled as a positive result, "survives
fresh scaling tests", although the registry summary and the unit's own census
control had downgraded it on 2026-10-07. Corrected with a dated revision
paragraph.

**2. The imported census had no code in the repository.** It was a result file
supplied from outside. It now has a reproducer that matches it exactly.

**3. The second jet review was never applied.** Pull request 329's review
confirmed every tested claim and asked for five changes, chiefly that
almost-sure injectivity arrives at `(G,Q,R)` and that autonomy on this panel
concerns a measure-zero set. They are now a dated
[addendum](2026-10-07-jet-full-line-autonomy.md#review-addendum-2026-11-09);
the reviewed text is unchanged.

**4. The direction page had become a ledger and carried a merge scar.** The
jet branch's copy contained a sentence cut off mid-line by an earlier merge.
The page is archived verbatim and rewritten short.

**5. Stacking defeated the agent guide.** Seven pull requests targeted other
gathering branches. The guide asks for branches based on `main`; nothing
enforced it, and the stack is why a month of work was invisible from `main`.

**6. Four working notes and one result file are unregistered.** They are
listed in the addendum above and left as working records.

No finding changes a scientific conclusion of the October units. Findings 1
and 3 change how two of them should be read.

## What this review did not do

- It did not re-derive the full-line pair-graph certificates. Those rest on the
  two `claude-fable-5-1` reviews and on the units' own independent replays,
  which pass here.
- It did not read every protocol for freeze-order claims. The earlier review
  already found that git history cannot substantiate the freeze ordering for
  pull request 328, and the same caution applies to the rest of that day's
  work: treat "frozen before evaluation" language from 2026-10-07 as
  descriptive.
- It did not check the typed-difference note's cohomological remarks, the
  near-ring prior-art attribution, the Rule-110 cubic normal form, the 256-track
  search, the latent-Q field constructions, or any HTML report.
- Ring-level agreement is not a full-line proof. Each row of the table above
  is exactly as strong as its stated domain.

## Disposition

Integrated into `main` by Myk's instruction of 2026-11-09. The thirteen pull
requests are closed as merged through the integration pull request, which
contains their head commits.
