# Separate background and disturbance errors

## Planned experiment

Retain the existing training/test separation and matched prediction targets. Define a background detector using reference or training trajectories, validate it on pure ether and known departures, then freeze its choices before inspecting held-out prediction outcomes.

For each observation family, define how fine-cell labels map to a coarse target. Retain ambiguous regions. Compare current-only and history errors at the same positions, reporting region frequencies, coverage, and variation across seeds and widths.

## Decision this enables

The result could distinguish predominantly phase recovery from a benefit that also extends to disturbance neighborhoods. Neither outcome by itself would establish a Class IV classifier. The experiment is planned and has not been run.
