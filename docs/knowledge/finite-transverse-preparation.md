# Can recursive program lifts use finitely thick prepared boundaries?

**Answered under explicit occupancy semantics, 2026-09-10.** The [finite-boundary checkpoint](../research/2026-09-10-finite-routing-boundaries.md) replaces the editable-routing family's infinite guard half-spaces by one complete guard layer on each side of the source.

The physical interpreter is unchanged. Guard data retain their values because their outward required neighbor is absent. A logical source now includes its fixed occupancy mask; missing sites are distinct from occupied zeros. This source type is invariant and can be lifted repeatedly, preserving execution, inherited one-cell edits and gated program copying.

The prepared band is three logical layers (27 physical coordinate positions) per new axis. This is finite transverse thickness, not finite total support for an infinite source. The claimed three-layer minimum is confined to the same complete-macrocell placement, all-inputs-required interpreter and one-tick contract.

The [previous question](../research/2026-09-09-editable-routing-tables.md) is therefore resolved for this declared family. Spontaneous boundaries, occupancy edits, tag repair, other boundary laws and optimized encodings remain separate questions.
