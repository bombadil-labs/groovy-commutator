# D, G, Q and R are successive same-lattice transport residuals

Define A0 = D = I XOR H and recursively

A{k+1} = A{k} o H XOR H o A{k}.

Along every source trajectory,

A{k,t+1} = H(A{k,t}) XOR A{k+1,t}.

So each new field is exactly the correction needed to transport the previous
field coherently under the source rule.

For nonlinear H, changing cadence mixes jet levels with polarization. In
particular,

C_{H^2}(A) = C_H^2(A) XOR B_H(H o A, C_H(A)) XOR H(0),

and for zero-preserving Rules 110 and 62,

C_{H^2}(G) = R XOR B_H(H(G),Q).

Rules 110 and 62 form a useful matched pair because their derivative maps are
symmetry-equivalent ECAs: D110 is Rule 162 and D62 is Rule 242, related by
reflection plus state-complement conjugacy. Their higher jet structure then
diverges.

On the tested full-line local domains, Rule 62 admits an exact radius-three
(D,G)->Q factor, while Rule 110 fails that factor through radius three.

Finite-ring jet prefixes often close only because they become nearly
source-injective, so these results do not establish a compression advantage.

Source: docs/research/2026-10-07-commutator-jet.md
