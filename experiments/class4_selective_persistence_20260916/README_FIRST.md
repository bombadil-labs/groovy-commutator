# Ancillary reconstruction — 2026-09-16 selective-persistence discriminator

This archive is a **best-effort reconstruction**, prepared 2026-09-17 after the
original chat context and local working state were lost.

## What is recovered numerically

The Project Library still contained:

1. the final report;
2. the complete 450-row all-conditions table (90 candidates × 5 conditions);
3. the 90-candidate cross-condition summary.

Those numerical rows are preserved here under `evidence/`. They verify exactly:

- 54/110 selected in **10/10** condition decisions;
- undisputed Class I–III representatives selected in **0/420**;
- disputed 41/106 selected in **0/10**;
- radius-2 correction selected **0/5**;
- radius-2 pure shift selected **0/5**;
- minimum positive S = `0.204989561614708`;
- minimum positive alpha = `0.683126863468290`;
- every undisputed negative with alpha > .5 has S = 0;
- largest alpha among undisputed negatives with S > .2 =
  `0.498938756887789`.

The recovered rows also satisfy to floating precision:

`S = max(0,R) * max(0,M)`

and

`alpha = log2(mean_d512 / mean_d256)`,

with the recorded strict thresholds `S > .20` and `alpha > .50`.

Run:

```bash
python reconstructed/verify_reconstruction.py
python reconstructed/class4_selective_persistence_runner.RECONSTRUCTED.py \
  --verify-recovered evidence/class4_selective_persistence_all_conditions_20260916.RECOVERED.csv
```

## What is NOT recovered byte-for-byte

The final report cites these historical protocol hashes:

- primary: `3e5c7efee950261c7e243aa1600951bd57ac163173051a97e7994ab2a3b20325`
- validation: `71fc7979c03ac93661c803496e9d53fdd02296cbed712120bf13bfe1c26d74ae`
- stress: `bd3b231e541f15ac8afac21cff0fac52845a74f01ddf06b749579293ea2c8cd2`

The corresponding original protocol bytes were not recovered. Nor were:

- the exact 2026-09-16 runner wrapper;
- the exact six fresh RNG seeds for each condition;
- the exact local definition/origin of the `radius2-correction` challenge;
- the original canonical result JSON schema/bytes.

Therefore the files under `reconstructed/` have **new hashes** and must never be
presented as matching the historical hashes.

## Why the reconstruction is still scientifically useful

The exact definitions of R and M survive in the preceding repository unit
(`scripts/class4_independent_20260915.py` and its research note). The frozen
2026-09-16 formula, thresholds, widths, densities, burn, horizon, perturbation
budget, label convention, complete numerical outcomes, and protocol SHA-256
identities survive in the report/tables.

The reconstructed runner therefore restores the measurement machinery with
only the missing historical random/input details called out explicitly.

## Suggested use for Fable

Treat:

- `evidence/*` as recovered derived evidence;
- `reconstructed/class4_selective_persistence_20260916.CANONICAL_RECONSTRUCTED.json`
  as a convenient reconstruction of the lost canonical result from that evidence;
- the three reconstructed protocols as a legible approximation of the frozen
  contracts, **not** hash-level provenance;
- simulation output from the reconstructed runner as a **new replication**,
  unless the historical seeds/control definition are later recovered.
