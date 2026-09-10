# Forgotten information splits into latent and shielded parts

Let S have a declared finite-state probability distribution, P(S) be the present observation, and C_infinity its complete observed-future equivalence class at a fixed cadence. Then C_infinity determines P(S), and the chain rule gives H(S)=H(P(S))+H(C_infinity|P(S))+H(S|C_infinity).

[Research025](../research/2026-09-08-fiber-visibility.md) calls the latter two terms latent and shielded information. The first is hidden now but distinguishes future observation trajectories; the second is absent from that entire observed future. The finite census uses uniform microstate weighting. Zero conditional entropy establishes a pointwise statement over the full family only when the chosen prior has full support there.

For the derivative observation at cadence one, distinct states with equal derivative histories cannot later coalesce: one shared endpoint and the common derivative sequence reconstruct equality backward. Shielding therefore does not necessarily mean that a physical distinction disappears.

The [shared account](../research/2026-09-10-shared-closure-account.md) separates this distribution-dependent budget from a known-state action channel and from endogenous control.
