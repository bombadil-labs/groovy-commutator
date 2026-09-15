# Reproduce the relation audit

The bundle contains the complete, unchanged original 98 MiB input archive,
its original manifest, full-input D2 tables, both implementations, every
primary/replay symbolic event array, the primary census and transfer records,
and their independent comparison. Python 3.12 and NumPy are sufficient.

From the extracted `gc-relations` directory, inspect the preserved
`experiments/commutator_relations_20260915/result.json` and
`review/comparison.json`. Compare the saved results without re-evaluating:

```bash
python review/compare_relations.py
```

For a fresh physical primary run, work on a COPY of the extracted bundle.
Move the existing unit's `result.json`, `records`, `census.json`,
`execution-freeze.json` and `run.log` aside before running:

```bash
python scripts/commutator_relations.py --archive inputs/uniform_jet6_rules.tar.gz --manifest inputs/archive_manifest.json
```

Run the independent replay into a new directory:

```bash
python review/replay_portable.py --archive inputs/uniform_jet6_rules.tar.gz --manifest inputs/archive_manifest.json --full experiments/beam_discriminator_loop_20260915/round01/tables.npz --prior results/commutator_completion_20260915.json --output review/fresh-replay
```

The path-only launcher leaves the executed replay source unchanged and
supplies its input/output paths. To compare a fresh pair of runs, move the
old `review/replay` directory aside and put the fresh replay at that path;
the comparator uses the canonical primary and replay paths. Execution times,
fresh NPZ byte hashes and runtime metadata can differ; the comparator checks
scientific partitions, constants, orbit counts and signed transfer counts.

Primary run: 44.08 seconds, 189,092 KiB peak RSS. Independent replay:
148.97 seconds, 125,324 KiB peak RSS. Neither run used GitHub Actions.
The ten-minute, 2 GiB bounds are per scientific process. Input preservation,
download, packaging, review, comparison and site build are separate work.

The protocol and its original freeze are unchanged. recovery.md and
review/gate1-review.md record prospective review in the resumed session.
The finite D3/D4 contracts, separate widths and fixed seven address readouts
remain the boundaries of the result. See the accompanying repository note
`docs/research/2026-09-15-commutator-relations.md` for interpretation.
