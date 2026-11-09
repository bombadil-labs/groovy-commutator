# Rule 54 has a positive-entropy source-pair ambiguity invisible to every higher jet

On the binary full line define the intrinsic commutator residual tower

\[
A_0=I\oplus H,\qquad
A_{k+1}=A_k\circ H\oplus H\circ A_k.
\]

The full ECA G,Q,R equal-output source-pair census finds branching recurrent
off-diagonal components in 228/256 rules; this is not a Class-IV discriminator.

A separate exact source-pair graph calculation for Rule 54 at the
(G,Q,R,A4,A5) prefix gives two pure off-diagonal strongly connected languages,
C_plus (52 vertices/68 edges) and C_minus (84/110), each with
Perron root sqrt(phi), and hence positive spatial *pair-language* entropy
(log2(phi))/2.

Every admissible 15-bit paired source patch from C_plus evolves under
(H54 x H54) to an edge internal to C_minus, and vice versa. The exact local
check exhausts 110 and 178 three-edge paths, respectively, with independent
scalar recurrence checks. Therefore

\[
(H_{54}\times H_{54})(C_+)\subseteq C_-,
\qquad
(H_{54}\times H_{54})(C_-)\subseteq C_+.
\]

Their union is forward-invariant, and pairs in it have identical G through
A5. Because the current G field agrees at *every future time*, induction
using

\[
A_{k+1}(X)=A_k(HX)\oplus H(A_k(X))
\]

proves that every higher residual A_k, k>=1, also agrees on these
distinct source pairs.

This is an **all-depth invisibility theorem for an exceptional invariant
positive-entropy source-pair language**, not a result about positive
conditional hidden entropy for a typical source, not a Class-IV
discriminator, and not a dimensional-lift theorem.

The two-component choice was a post-primary exploratory selection after
the originally frozen union of three branching SCCs failed. The exact
inclusion claim was separately frozen before evaluation.

Source: [census and invariant pair-language certificate](../research/2026-10-07-jet-gqr-census-fibonacci.md).
