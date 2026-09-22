# Next agent: start from the completed representation unit

**Scientific work complete in this unit, 2026-09-21.** The original
[issue #280](https://github.com/bombadil-labs/groovy-commutator/issues/280)
asked for three executable representation cases. They are now in
[the case-study note](representation-case-studies.md), with a fast verifier
and canonical report. A separately frozen, bounded follow-up produced the
[causal-retention result](2026-09-21-causal-retention.md). Read these two notes
and [START_HERE](START_HERE.md); no historical census is needed.

## What was settled

- Rule 255 separates same-law commutator error from information loss.
- Rule 223 / observation 22 has an explicit width-seven factor obstruction.
- Rule 58 / observation 232 has a checked all-ring depth-one certificate and
  a full-line counterexample with verified periodic tails and connecting path.
- For Rule 110, no nontrivial pointwise quotient of Nakamura's twelve-state
  interface preserves current/phase readout, radius one and each atomic update.
  The first whole-field check rejected 56/64 candidates; the local follow-up
  rejected the remaining seven nonidentity candidates. The proof reduces to
  two reachable local examples and their three uniform phase rotations.
- Existing eight-state simulations use a different protocol. No lower bound
  on all asynchronous simulators, novel general theorem, Class-IV metric, or
  asynchronous advantage of the six-field dimensional lift is claimed.

## Verification and integration

The completed unit is published in [PR #282](https://github.com/bombadil-labs/groovy-commutator/pull/282).
On main, treat this unit as integrated; do not recreate its branch or reopen
#280. If reading the gathering branch before merge, check that PR for CI and
integration status. The connector outage is resolved. The
[publication record](../../review/representation-causality-publication.md)
maps original local commits to identical imported snapshots.

For a targeted verification when needed, run from the repository root:

```bash
python scripts/verify_representation_case_studies.py --check
python scripts/verify_nakamura_retention.py --check
python scripts/verify_nakamura_local_retention.py --check
python -m unittest discover -s tests -p 'test_representation_certificate_rejection.py'
python scripts/check_result_integrity.py
npm run test:research --prefix site
npm run build --prefix site
```

Myk explicitly authorized solo completion and integration of this unit; no
independent sign-off is claimed. Historical canonical bytes must remain
unchanged; the three new reports hash their inputs explicitly.

## What is not next

The two frozen numerical protocols are complete. Do not extend horizons,
increase ring sizes, run all 256 rules, or reinterpret finite survivors as
working simulators. The exact radius-one obstructions already close the
stated direct-compression route. Source-recoder recovery and Class-IV feature
searches remain parked.

Any proposed next scientific unit must name one operation that a representation
makes cheaper, match the readout/cadence/locality requirements of the competing
methods, and charge encoding and initialization costs. Ordinary stored history,
published asynchronous simulators and the period-three necklace are relevant
baselines under different contracts. If no concrete advantage or necessary
decision can be stated, stop after integration. A clean completed result is a
valid stopping point; there is no requirement to keep producing experiments.
