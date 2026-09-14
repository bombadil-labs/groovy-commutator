# Every ECA has a faithful centered-G binary first floor in the extended family

Status: exhaustive finite-domain finding, independently replicated from scratch (exact match). Gate 2 accepted 2026-09-14 (Claude/Fable, exact head a641df751bc81b50947b8ea7bd1c4d9d2ae8203f, PR #233). Updated 2026-09-14.

The [DT2 census](../research/2026-09-14-binary-lift-dt2.md) repairs28 of 36 old centered-G holdouts, and the [complement census](../research/2026-09-14-binary-lift-complements.md) repairs the final eight. Retaining previous recipes gives256 faithful,156 original-G and256 centered-G first floors at native radius two.

One shared five-row recipe works for the final eight: P,D,1 XOR T2,M,Q, with the birth mask and directed-right Q. Native and probe key sets are disjoint. The complement moves native neighborhoods while leaving temporal XOR probes unchanged; T2 and row polarity address different consistency problems.

This is a union of source-dependent recipes with binary cells, source-radius-two preparation, period-four/five transverse repetition and P/D-only G carriers. Off-image outputs remain free. No new recursive or independent-higher-dimensional-information result follows. The original-G fixed-point obstruction means centering is a substantive part of this contract.
