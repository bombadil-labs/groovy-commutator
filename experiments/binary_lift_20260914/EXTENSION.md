# DT2 and row-complement extension to the binary lift unit

The [DT2 note](../../docs/research/2026-09-14-binary-lift-dt2.md) and [complement note](../../docs/research/2026-09-14-binary-lift-complements.md) add completed local work after PR #233's original review baseline. Myk authorized both evaluations and this integration; independent Gate 2 review remains pending. See [authorization and deviations](../../docs/research/protocols/binary-lift-extension-record-20260914.md).

The cumulative first-floor family has **256 faithful, 156 original-G and 256 centered-G** source rules. The final eight share one five-row recipe, P/D/(1 XOR T2)/M/Q. This is a first-floor recipe-union result; the original 3D and 4D data remain unchanged.

## Preserved evidence

The [extension manifest](../../results/binary_lift_20260914_extension/bundle_manifest.json) preserves 29 original files: all 29,376 DT2 recipes, all 202,752 polarity recipes and their failure certificates, frozen protocols, manifests, verification records, shared-recipe selection and eight sparse rule/decoder exports. Seven scientific code files are imported without edits, alongside the existing baseline code. The additional archive contains 81,840,450 original bytes compressed to 2,025,748 bytes, transported as 16 base64 text parts. Parts are storage encoding, not separate experiments.

The original archive, original canonical account and original verification wrapper are unchanged. The [updated canonical account](../../results/binary_lift_20260914_extension.json) and [all-rule first-floor CSV](../../results/binary_lift_20260914_extension/rule_coverage.csv) expose the cumulative union without replacing the original selected-path table.

The [bridge reconciliation](dt2-bridge-reconciliation.md) is retained as a dated pre-DT2 context record. Its then-pending predictions and unchanged-PR statements describe that earlier point; the two result notes provide the current account. Fable's separate recursive/re-beaming experiments are not represented as reproduced results here.

## Fast automatic checks

```sh
python scripts/verify_binary_lift_extension.py --integrity
python scripts/verify_binary_lift_extension.py --check
```

The first registers source/input hashes with the existing integrity engine. The second also validates archive membership and content, recomputes all coverage sets from saved recipes, checks all 6,528 zero-polarity controls, validates the shared recipe and exports, and reproduces the published account and CSV. These are preservation/accounting checks, not new scientific evaluations. The existing bounded evidence workflow runs them automatically.

## Independent implementation checks, off CI

```sh
python -m pip install -r experiments/binary_lift_20260914/ca_lift_lab/requirements.txt
python scripts/verify_binary_lift_extension.py --replay
```

This extracts a disposable copy and runs the cropped-source DT2 verifier, the cropped-source complement verifier and the common-recipe export check. It does not rerun the primary censuses. Wall times need not reproduce; the full input records and code hashes are fixed. Primary C++ census compilation additionally requires a C++17 compiler.

For inspection or explicitly chosen additional local work:

```sh
python scripts/verify_binary_lift_extension.py --extract /tmp/binary-lift-extension
```

The destination must be empty. The two runners resume completed whole-rule cases, so rerunning them on an already complete directory is a cache/accounting operation, not a fresh census. Preserve the archived records; use a separate disposable run directory when seeking a new evaluation.

## Reviewer focus

Check the source dependency intervals, phase-dependent polarity masks, unchanged probe/carrier demands, both centered zero branches, joint recovery/native/G gates, exact scope of independent checks, and the original-G fixed-point argument. The common recipe is a post hoc selection. Only P/D carriers are specified; no independent transverse information, unique off-image completion or induction theorem is claimed.
