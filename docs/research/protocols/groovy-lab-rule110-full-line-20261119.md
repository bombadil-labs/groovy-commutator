# Groovy lab: Rule 110 two-epoch full-line audit

**Status:** queued in the bounded Groovy research batch, 2026-11-19. No result yet. This branch starts from main. It follows the [reviewed loss pilot](https://github.com/bombadil-labs/groovy-commutator/pull/331) as a contrasting case but does not depend on that branch. The [finite-ring result](https://github.com/bombadil-labs/groovy-commutator/blob/4883bd96975a45dec29274630f3b134e309ed3d6/docs/research/2026-10-07-rule110-latent-q.md) at the pinned #330 tree is the input.

**Question:** Does matching (P,G) at epochs 0 and 1 on the unrestricted full binary line leave only the two known unordered periodic pairs, in addition to the diagonal? Fix Rule 110, H as its synchronous step, F=H², fixed parity blocks P_j=X_{2j} xor X_{2j+1}, G retained at every site. Use G as defined in the pinned source.

**Decision:** Yes would lift the finite-ring certificate to the line and prove that any deterministic autonomous augmentation retaining (P,G) has no other collisions. An explicit additional compatible full-line pair would refute the *two-epoch* certificate, not necessarily all-time observability. This answers whether a small finite observation horizon is enough to resolve nearly all hidden distinctions. Recover the known pairs (all zeros versus all ones, and the two alternating phases) as controls.

**Method and bar:** Construct the exact block-aligned source-pair graph for equality of both epochs. Analyze all bi-infinite paths, including paths between recurrent components, and justify local radius and coordinate alignment. Supply a compact reproducer and explicit classification or extendible witness. A sampled ring census is not a certificate. Independently rederive and review the same pinned target before synthesis. Use a draft only; no direct main changes or rollout.

**Stop:** One bounded check and at most one operational recovery. No deeper horizon, feature search, wider census, or automatic next unit. A resource or access failure is unresolved, not a negative result. Preserve a checkpoint that explains what was last verified.
