# Finite width packs; independent unbounded transverse freedom does not under fixed capacity

**Status: exact scoped finding.** The [frozen protocol](../research/protocols/transverse-freedom-20260911.md) and [completed result note](../research/2026-09-11-transverse-freedom.md) distinguish nominal row count from independent transverse state capacity.

Every fixed finite-width strip can be column-packed into a one-dimensional CA over a width-dependent product alphabet. In contrast, under a fixed target alphabet of size `q` and fixed longitudinal expansion `K`, injectivity of the full width-`w` strip requires `|A|^(wn) <= q^(Kn)`, which fails for sufficiently large `w`. Unbounded independent transverse capacity is therefore a necessary anti-packing resource under this representation contract, but not a sufficient definition of spatial dimension.

For the inherited Rule32 correction family, every finite-depth tuple is a deterministic image of the fixed first-image family and has at most one bit of independent-state capacity per longitudinal source site. The exact bounded diagnostic on `n=6..12`, H128/H160, K/O and `h=0..4` goes further: its tuple partition is already saturated at `h=0` on every tested ring, even while nominal tuple storage grows from 2 to 10 bits per site.

Scope: the capacity theorem is conditional on the fixed `(q,K)` contract; the measured saturation is bounded to the declared Rule32 rings and depths. This finding does not define intrinsic dimension or rule out spatial meaning supplied by causal topology, intervention structure, or another representation contract.
