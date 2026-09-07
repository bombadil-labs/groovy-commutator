# History beats the tested wider-snapshot estimator

## Current finding

A radius-one history at seven observed times has lower held-out aggregate
error than a radius-ten current-only snapshot in every seed comparison of
the Rule 110 regional experiment. Both contexts contain 21 input bits.
Both predictors use training-majority lookup with minimum-support-five backoff.

## Limit of the comparison

History contexts have better training coverage. At width 840, majority-5
histories have 92.1% supported coverage and 2.27% error, versus 43.8% and
19.46% for wide snapshots. Equal input counts do not match effective information
or sampling difficulty. This result describes the fixed estimator and budget;
it does not prove that temporal information is irreducible to spatial context.

The discriminating follow-up is a fixed-width training-budget experiment,
including supported-subset diagnostics and estimators that share information
across contexts. See [the regional experiment](../research/2026-09-07-ether-regions.md).
