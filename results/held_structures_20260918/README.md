# Historical canonical bytes; three scores invalidated

P4a, P4c and P4d in `summary.json` use a mistimed gadget predictor. Their
original verdicts are preserved as historical output, not accepted tests.
See the [dated correction](../../docs/research/2026-09-21-held-structures-account.md)
and the separate `../held_structures_20260921_timing_audit.json` diagnostic.
All other conclusions retain the limited scope and verification status in
that account. Do not silently regenerate or overwrite these files.
