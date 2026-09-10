# Representation repair fixes the future target while refining the present

[Research027](../research/2026-09-08-representation-design.md) fixes target observation T and its stable future class C_infinity^T, then refines only the present encoder Z. Residual uncertainty is W_T(Z)=H(C_infinity^T|Z(S)); a refinement cannot increase it. This keeps better present prediction separate from changing what counts as the future target.

On the complete 15-node partition lattice of a two-cell block, all ECA rules at n=12 and cadence2 give 1,590 nonclosed binary-target cases. Greedy predictive gain per added present bit reaches a globally minimum-information local repair in all of them. That result is scoped to this lattice and ensemble; [Research028](../research/2026-09-08-block3-representation-design.md) supplies its larger-lattice boundary.

Bulk information gain and worst-case latent tail are distinct objectives. The predicted superiority of the Rule106 odd-parity split for Shannon repair failed: the even split is bulk-optimal, while the odd split shortens the worst-case tail. The source retains the tail-definition correction and fresh-size check. A finite optimizer is not an online learner or a proof of globally optimal adaptive representation.
