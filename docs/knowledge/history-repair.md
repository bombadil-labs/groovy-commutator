# History improves Rule 110 prediction

## Current claim

The September validation repeats the history benefit across two ring widths, five observation families, and four independent test seeds, using eight separate training seeds. At width 420, parity blocks of size two fall from mean error 0.2641 at depth zero to 0.0090 at depth six. Majority blocks of size three fall from 0.2178 to 0.0041.

## Scope and limits

Targets are matched across depths and sparse contexts fall back to supported shorter histories. The study uses one training ensemble, one initial density, and a bounded history budget. It does not prove a minimum sufficient memory or exact closure. Whether the predictor mostly learns ether phase is still open.

## Regional replication, 2026-09-07

The [frozen regional experiment](../research/2026-09-07-ether-regions.md) repeats
the benefit with two training ensembles, eight new held-out seeds, and widths
420 and 840. Improvement extends to departure neighborhoods under both fixed
detectors, while most residual errors remain there. This strengthens the
scoped prediction finding without establishing a mechanism or closure law.
