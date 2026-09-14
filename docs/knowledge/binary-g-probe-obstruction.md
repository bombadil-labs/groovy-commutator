# A recoverable encoding can have an ambiguous commutator probe

Status: retrospective finding, independently replicated. Gate 2 accepted 2026-09-14 (Claude/Fable, exact head a641df751bc81b50947b8ea7bd1c4d9d2ae8203f, PR #233).

For a physical commutator-preserving lift, the native derivative rule must be consistent both on encoded-state neighborhoods and on neighborhoods of their changes. Recovery from the encoded state does not imply sufficiency of the latter input.

The [complete first-floor diagnosis](../research/2026-09-14-binary-lift-g-obstructions.md) isolates same-D-field opposite-output demands in 2,432 faithful recipes. Among recipes already faithful under the uniform unlabeled gates, 29 of the 36 G holdout rules remain blocked even with a separate native rule for each known row phase. Initially unfaithful recipes were not retested under labels. The certificates constrain the stated radius-two recipes; they do not refute all encodings or all larger radii.

The prospective repair must separate the contradictory pairs through its temporal derivative and remain compatible with native evolution. Merely complementing Q leaves its temporal derivative unchanged and cannot repair these same-field witnesses.

## Revision 2026-09-14: post-PR extension

The [DT2 comparison](../research/2026-09-14-binary-lift-dt2.md) and [complement repair](../research/2026-09-14-binary-lift-complements.md) distinguish two mechanisms: retain necessary probe distinctions, then ensure compatibility with native evolution. A row complement leaves the probe unchanged but moves the native keys; this repairs the last eight for centered G and does not contradict the earlier same-field no-go.
