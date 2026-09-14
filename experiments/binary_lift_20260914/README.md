# Binary ECA lift evidence and review guide

This is the retrospective import of Myk's authorized local dimensional-lift series. Independent Gate 1 review was skipped; independent Gate 2 review is pending. See the [authorization and deviations](../../docs/research/protocols/binary-lift-retrospective-record-20260914.md).

Read the [family note](../../docs/research/2026-09-14-binary-lift-family.md), [recursion note](../../docs/research/2026-09-14-binary-lift-recursion.md), and [obstruction note](../../docs/research/2026-09-14-binary-lift-g-obstructions.md). The [canonical account](../../results/binary_lift_20260914.json) lists exact rule sets; the [CSV](../../results/binary_lift_20260914/rule_coverage.csv) gives all 256 selected recipes and their separate gate statuses.

## Contents

`ca_lift_lab/` preserves 43 original code/requirements files without source edits. The data archive contains 77 original files (about 90 MB before compression), including both complete 24,576-case first-floor censuses, their input cache, all 256 selected 3D paths, the 206 best-known G paths, the historical 113-path 4D baseline, the complete collision certificates, and the original verification records. The [manifest](../../results/binary_lift_20260914/bundle_manifest.json) gives every path, size and SHA-256.

Archive parts are concatenated base64 of one deterministic tar.xz. This keeps the repository import compatible with its text-file connector and self-contained; no signed download URL or external storage is needed. The extraction helper verifies all parts and every recovered member. Original data are not renormalized to disguise adaptive selection, timing fields or cumulative verification supplements.

The original scripts' `ROOT` is their own lab directory. Run them in an extracted working copy, since many write outputs or refuse an existing output directory. The supplied wrapper handles that isolation.

## Fast checks from the repository root

```bash
python scripts/verify_binary_lift_release.py --integrity
python scripts/verify_binary_lift_release.py --check
```

The first command registers this unit's result with the existing shared integrity engine and verifies source/input hashes. The second also unpacks the archive and recomputes the published coverage and obstruction account from the original records. These are provenance/accounting checks, not a fresh scientific census. Both run automatically in this unit's bounded workflow.

## Local scientific replay

Use Python 3.12 or later and install the recorded dependency:

```bash
python -m pip install -r experiments/binary_lift_20260914/ca_lift_lab/requirements.txt
python scripts/verify_binary_lift_release.py --replay
```

This extracts a disposable copy, repeats the original targeted independent author checks for fresh symmetric and directed first floors, the universal 3D selection and Rules 23/232, and reruns the complete G-collision diagnosis plus the phase-oracle supplement. It asserts byte equality of the two full collision certificate logs. It does not assert byte equality for wall times or cumulative reporting wrappers, and does not claim a second full independent census of every first-floor recipe. The scientific replay is never triggered by this unit's CI workflow.

To inspect or run a different verification scope explicitly:

```bash
python scripts/verify_binary_lift_release.py --extract /tmp/binary-lift-review
cd /tmp/binary-lift-review/ca_lift_lab
python verify_binary_4d.py --run runs/binary_4d --rules 14 110 54 57 --workers 3 --name review_verification
```

The extraction destination must be empty. The historical 4D check is optional and local. All scientific code and saved full candidate records are available for the reviewer to choose broader checks. Do not mistake running the release account from saved data for replaying the scientific experiment.

## Review questions

1. Do the exact dependency windows, cyclic phase coverage and packed neighborhoods support the stated native/recovery identities?
2. Do original/centered physical-G constraints transport only the declared P/D carriers, leaving other parent outputs symbolic?
3. Are cached versus new cases, selected versus best-known paths, and the older 4D population accounted for separately?
4. Do the source-loss and probe-loss witnesses establish exactly their stated scopes?
5. Do the exception, retrospective status and remaining proof boundaries remain visible in every current-account surface?

The next Boolean-Q witness-filter experiment is unrun. This import is a record of completed work, not authorization to resume an unbounded search.
