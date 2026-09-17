# Measurement provenance used for this reconstruction

The exact byte-identical 2026-09-16 runner was not recovered.

However, the preceding scientific implementation remains in the GitHub repository:

- `scripts/class4_independent_20260915.py`
- `docs/research/2026-09-15-class4-independent.md`
- `results/class4_independent_20260915.json`
- `scripts/class4_composite_20260915.py`
- `results/class4_composite_20260915.json`

The 2026-09-15 research note explicitly defines the retained measurements later
used by the 2026-09-16 discriminator:

## Selective retention R

For W-bit block b and its two external bits e, evolve the same W positions one
step. `p_e(b)` is log2 of the number of W-bit predecessors yielding the same
W-bit output with e fixed. Let Q(b) be the first two and last two block bits.
The boundary-conditioned reference is the uniform mean ambiguity over blocks
with Q fixed. R is the visited mean `(reference - p_e(b))` divided by the
uniform standard deviation over all `(e,b)`. W=7 was the declared primary
window.

## Predictive gain M

At a site, C=current bit; H=C plus h older bits; Y=next bit. Six trajectory
seeds are split 3/3. For both train/test directions, estimate P(Y|C) and P(Y|H)
using Jeffreys 0.5 smoothing per output, evaluate held-out cross entropy, and
take gain CE(C)-CE(H). The 2026-09-16 discriminator uses h=8 and the mean of
the two fold-direction gains.

The reconstructed runner implements these definitions directly rather than
inventing new proxies.

## Spreading

The 2026-09-16 surviving report defines alpha_512 as
`log2(mean_support_diameter_512 / mean_support_diameter_256)` across
96 single-bit perturbation trials = 16 origins × 6 burned trajectory states.
The exact original origin-selection code was not recovered. The reconstructed
runner uses 16 evenly spaced origins and a minimal cyclic support span; any run
with it is a fresh replication unless the historical origin convention is
independently recovered.
