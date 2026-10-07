# Nonlinear Rules 4 and 200 have zero commutator

Rules 4 and 200 are nonlinear cubic ECAs whose self-commutators vanish on the
complete five-cell local domain.

The 2026-10-06 typed-difference audit now explains the mechanism and completes
the ECA classification. Let

\[
P=H_4,\qquad Q=H_{200}.
\]

As global maps,

\[
P\oplus Q=I,\qquad
P^2=P,\qquad
Q^2=Q,\qquad
PQ=QP=0.
\]

Thus Rules 4 and 200 are complementary orthogonal idempotents. Since

\[
D_P=I\oplus P=Q,\qquad D_Q=P,
\]

their Groovy commutators vanish by mutual annihilation:

\[
G_P=QP\oplus PQ=0,
\qquad
G_Q=PQ\oplus QP=0.
\]

Their local ANFs are

\[
H_4=c\oplus lc\oplus cr\oplus lcr,
\qquad
H_{200}=lc\oplus cr\oplus lcr,
\]

so both remain genuinely cubic.

An exact ANF classification over all 256 ECA truth tables and every complete
radius-two source word proves that identically flat centered Groovy occurs for
exactly the 16 affine rules plus Rules 4 and 200. There are no other nonlinear
ECA exceptions.

The four maps \(\{0,P,Q,I\}\) also form a four-element Boolean ring under XOR
and composition inside the larger cellular-automaton near-ring.

Sources:
[original affine-converse correction](../research/2026-09-07-affine-converse.md);
[typed difference geometry](../research/2026-10-06-typed-difference-geometry.md);
[CA near-ring interpretation](../research/2026-10-06-ca-nearring-interpretation.md).
