# Reproduce the observation catalog

Primary scientific source was committed at
`15967f733af1aa167fb92a3c107145f396a7a2c6` before evaluation. The original Gate 1
review and its prospective numerical clarification are in `review/catalog-gate1.md`.
Discovery completed before the seven selected slots were committed at
`c17bc660acf22223b513f7b7e313107bacbf95f0`; confirmation began afterwards.

The downloadable archive contains the original uniform-six-field input archive,
the exact prior relation arrays and raw result, all new event data, metrics,
selection rows, native matches, provenance maps, scientific sources and review.
`CONTENTS.json` gives every member's byte length and SHA-256. Extract into an
empty directory. Commands below run from that extracted root. Python 3.12 and
NumPy 2.3.5 were used; Matplotlib is needed only to regenerate the figure.

## Primary replay without overwriting recorded results

Choose a new replay directory and keep the archived outputs intact. For example:

```bash
python scripts/observation_catalog.py discovery --unit replay-primary
```

Check that `replay-primary/shortlist.json` has the SHA-256 recorded in
`experiments/observation_catalog_20260915/confirmation-seal.json`. The compact
committed `selected-shortlist.json` is the full shortlist with only its 2,076-row
ranking table removed. It retains every selected slot, interval, group and input
hash. Copy the archived confirmation seal into `replay-primary/confirmation-seal.json`
to reuse that historical frozen selection, then run:

```bash
python scripts/observation_catalog.py confirmation --unit replay-primary
python scripts/observation_catalog.py lift --unit replay-primary --archive experiments/observation_catalog_20260915/inputs/uniform_jet6_rules.tar.gz --relation-dir experiments/observation_catalog_20260915/inputs/relations
```

Each stage refuses to overwrite an existing stage result. Discovery must be
complete before any confirmation. A censored discovery removes its shortlist;
it cannot silently authorize a smaller confirmation. Each stage has a 600-second
wall/two-GiB RSS budget. Compare scientific JSON and arrays; execution timing/RSS
records naturally differ. No scientific replay runs in automatic GitHub Actions.

## Event data schema

- `finite/wN_rRRR.npz`: `fields[24,2**N,N]`, and source `next_index` and
  `right_index`. Source integer bit x is cell x (little-endian). Three-site
  words use x-1 as the least significant bit. These arrays reconstruct every
  candidate's partition and counted temporal/spatial edges without resimulation.
- `discovery-metrics.npz`: `metrics[2,256,300,7]` for widths 7/8 and
  `aliases[256,300]`. Alias checks enumerate the complete 11-bit local domain.
- `confirmation-metrics.npz`: `metrics[256,300,7]` for width 9. The full matrix
  is diagnostic data; confirmation decisions use only the seven previously
  committed slots. No replacement selection is made from this matrix.
- Single observations have NaN in metric 7, which is inapplicable. Other finite
  cells are measured. JSON uses explicit nulls where necessary, never NaN.
- `long/rRULE_sSEED.npz`: initial state; packed developed trajectory and shape;
  primitive three-site `words[24,1026,8]`, `right_words[24,1024,8]`, the common
  `target[1024,8]`, sample sites, and a `[300,7]` metrics table. Only selected
  candidates and their constituent singles are populated; other cells are NaN.
- `lift/wN_rRRR_dD.json`: every matching native-view/root-observation partition,
  with all root aliases and counted transition witnesses. Native candidate IDs
  use the original 300-candidate catalog; only 210 candidates are eligible.
- `lift/*.npz`: decoded source states, their archive-order successor, period,
  basin and event-to-source maps. Archive order must be decoded, not assumed
  identical to the root atlas's integer order.
- `inputs/relations/*.npz`: the preserved PR259 symbolic event labels/constants
  and exact full-spatial quotient. The primary script validates their hashes
  against the pinned `inputs/previous_result.json` before using them.

## Independent reconstruction

`review/catalog_oracle.py` defines a separate integer update, Boolean projections,
tuple-count entropies, partition canonicalization, and native/provenance checks.
`review/catalog_compare.py` compares the independent events/metrics and all
selection verdicts; it does not import the primary implementation.

For a fresh independent replay, make a separate copy of the extracted tree and
rename its `review/catalog-replay` directory to `review/catalog-replay-recorded`.
This keeps recorded evidence intact while the fixed replay commands create new
outputs in the fresh copy:

```bash
python review/catalog_oracle.py --finite-panel discovery
python review/catalog_compare.py discovery
python review/catalog_oracle.py --finite-panel confirmation --confirmation-seal experiments/observation_catalog_20260915/confirmation-seal.json
python review/catalog_compare.py confirmation
python review/catalog_compare.py lift --archive experiments/observation_catalog_20260915/inputs/uniform_jet6_rules.tar.gz
python review/catalog_period_witnesses.py
python review/catalog_author_crossreview.py
```

The independent panel covers 24 finite rule/width cases, all seven selected
confirmation decisions across all rules, eight independently regenerated longer
trajectories, all 98,280 native views and all 104 completion-provenance contracts.
The signed review specifies exact coverage, errors and source hashes.
The separate period endpoint inspection is labeled post hoc in its report.

## Presentation and provenance tier

`scripts/summarize_observation_catalog.py figure` renders the saved pair-gain
matrix without refitting or scientific evaluation. `summary` packages the
recorded outcomes and reviewed source hashes for the public research note.
Automatic CI compiles the scientific/review sources and runs
`scripts/check_result_integrity.py results/observation_catalog_20260915.json`.
This fast tier checks provenance coherence; independent event reconstruction
supplies the content check.
