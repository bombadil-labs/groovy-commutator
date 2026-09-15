# Observation catalog — independent Gate 1 review

Reviewer: Codex (OpenAI), /root/relations_review, 2026-09-15.
Reviewed protocol commit: `aaa0c3fcef7d500ec0a1bd5fd342658e8056019b`.
Reviewed protocol SHA-256: `d499a764efceaca64468f35a7a08eac894c1539d362a41b7face168be43ac856`.
Scope: the complete frozen observation catalog, discovery/confirmation selection, bounded native views, and completion-relation provenance audit in gathering PR #260 / protocol sub-PR #261.

**Gate 1 approved before implementation/evaluation.** The original selection/RNG ambiguities have been resolved in the reviewed revision. No scientific implementation has been reviewed or approved by this protocol-only gate.

The 24 primitive definitions are coherent, including the sign convention for spatial shifts, local input perturbations for sensitivities, and `U XOR V XOR F(X XOR U)` for the commutator. Eleven source bits suffice for every primitive's three-site word: the largest support is a two-step future shifted by two cells and sampled one additional cell from the center. Singles and unordered pairs give 300 nominal observations; per-rule partition aliases do not change their attempted multiplicity.

The seven measurements use a consistent event ensemble. The refinement gain is conditional mutual information; the common-target and complementary-gain definitions are valid. Retrospective support, larger pair observation budgets, dependent trajectory sampling, finite rings and disputed rule orbits are explicitly distinguished from causal prediction or independent class evidence.

The shortlist is fully mechanical: candidate-specific normalization ranges include all 256 rules at both discovery widths; negative overlap is scored per symmetry orbit; metric seven excludes null singles; incomplete discovery cannot yield a shortlist or confirmation. Fixed intervals and slots must be committed with discovery hashes before width-nine or longer-trajectory confirmation. Fresh PCG64 generators with the specified uint8 draw create paired rule comparisons at each seed.

Native observations use certified on-family successors and exact source-state partitions, retaining aliases and transition witnesses. The omitted native sensitivity/G queries are explicitly **not guaranteed determined by the on-family constraints, and therefore omitted**. The protocol correctly avoids claiming that every individual omitted query is completion-dependent; some are already forced.

Completion provenance counts are scoped to free-event blocks, with fixed events excluded, overlapping categories retained separately, and absent denominators marked not applicable. Equal partitions under a common source successor transport their transition relation up to the recorded symbol relabeling; this does not establish independent discovery or a native factor theorem.

The three per-stage 600-second/two-GiB budgets, censoring rule, outside-Actions execution, full raw preservation and hash checks are suitable. All separation claims remain bounded and exploratory, based on only two core positive symmetry families. No native-view match may rescue a failed confirmation claim.

Before seeing results, the independent replay panel is fixed as follows: roots `{0,4,18,30,54,90,110,147}`, widths seven/eight/nine, all 300 candidates and all seven measurements. Independently verify every shortlist/confirmation verdict from the complete saved tables; replay selected longer-run observations for roots 30/54/110 and the radius-two challenge, both seeds; and inspect native phase matches and completion-provenance witnesses directly. Record completed verification coverage and discrepancies. The primary author will cross-review the independent replay contribution; the reviewer will review the primary code and exact final publication head separately at Gate 2.

## Prospective numerical-convention confirmation

Before any scientific evaluation, reviewed revision `9cba5b33d4c84a7e655d17652a89936e4112b153`, protocol SHA-256 `e5ddef3d78f7bc6336e37a530cf52ebe037c7208f65d05aeeab9d917d282f7dc`. The header now records the earlier approval. Candidate ranges at or below `1e-10` count as zero before normalization; negative roundoff in theoretically nonnegative entropy/information/gain values may be clipped to zero. These numerical clarifications are approved prospectively and do not change the catalog, domain, thresholds or selection policy. A raw violation below `-1e-10` should fail validation rather than be concealed by clipping. This confirms Gate 1 applicability; separately reported implementation/preservation findings remain for the author to resolve before running affected stages.
