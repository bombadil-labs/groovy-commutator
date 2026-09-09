# One trajectory can obey local laws in two dimensions

A one-dimensional cellular automaton can be embedded into two dimensions so that its projected states evolve exactly under a fixed, translation-invariant two-dimensional cellular-automaton rule. The commuting square is literal:

$$
F_2E=EF_1.
$$

For elementary cellular automata, a particularly simple diagonal-stripe embedding already gives a two-dimensional dependency stencil that is irreducibly two-dimensional for 218 of the 256 rules. A second construction extends every ECA to a full 2D rule whose essential dependency sites have affine dimension two, while leaving the encoded 1D evolution unchanged.

This is a positive answer to the motivating question in a precise sense: after projection, the same dynamical process can be regarded as following a different local law on a different-dimensional state space. It is also literally a Groovy-Commutator-shaped relation, with the representation map replacing the original derivative/coarse-graining map.

The important qualification is that the diagonal-stripe image still has only one-dimensional independent degrees of freedom. The strongest unresolved version asks whether exact cross-dimensional commutation can coexist with irreducibly two-dimensional *encoded state complexity*, not merely an irreducibly two-dimensional ambient rule.

## The cross-dimensional commutator

Let $F_1$ be the global update of a 1D CA, let $E$ encode a 1D configuration into a 2D configuration, and let $F_2$ be a 2D CA update. For binary systems define

$$
K_E(s)=F_2(E(s))\oplus E(F_1(s)).
$$

Then $K_E(s)=0$ for every source state exactly when the diagram commutes:

$$
\begin{array}{ccc}
X_{1D} & \xrightarrow{F_1} & X_{1D}\\
\downarrow E && \downarrow E\\
X_{2D} & \xrightarrow{F_2} & X_{2D}.
\end{array}
$$

If $E$ is injective and its image $M$ is invariant under $F_2$, then

$$
F_2|_M=EF_1E^{-1}.
$$

Thus the 2D rule restricted to the encoded family is dynamically conjugate to the original 1D rule. The ambient 2D rule may nevertheless have additional behavior away from $M$.

This is the central distinction: the projected evolution is not merely a picture of the 1D trajectory. It is an orbit of a bona fide 2D CA.

## A general construction

The ECA result is a special case of a simple lattice-quotient construction.

Let $A$ be a finite alphabet and let a 1D CA $F_1:A^{\mathbb Z}\to A^{\mathbb Z}$ have finite neighborhood $N\subset\mathbb Z$ and local rule

$$
f:A^N\to A.
$$

Choose a surjective group homomorphism

$$
L:\mathbb Z^2\to\mathbb Z.
$$

For the concrete construction below, use $L(x,y)=x+y$. Define the embedding

$$
E_L(s)(z)=s(L(z)).
$$

Because $L$ is surjective, $E_L$ is injective. Its image consists of 2D configurations constant on cosets of $\ker L$; for $L(x,y)=x+y$, those are anti-diagonal stripes.

For each logical neighborhood offset $n\in N$, choose one physical representative $\sigma(n)\in\mathbb Z^2$ satisfying

$$
L(\sigma(n))=n.
$$

Now define the 2D local rule

$$
F_2(X)(z)=f\left(\bigl(X(z+\sigma(n))\bigr)_{n\in N}\right).
$$

On an encoded state,

$$
X(z+\sigma(n))=s(L(z)+n),
$$

so directly

$$
F_2(E_L(s))(z)=F_1(s)(L(z))=E_L(F_1(s))(z).
$$

Therefore

$$
F_2E_L=E_LF_1
$$

for every source state. No finite experiment is needed for the general identity; it is an algebraic consequence of the construction.

The construction works for any finite-radius 1D CA, not only binary ECAs. It also generalizes immediately from $\mathbb Z^2\to\mathbb Z$ to suitable quotient maps between other lattice dimensions.

## The simplest ECA lift is already spatially 2D

For an ECA local rule $f(l,c,r)$, use

$$
E(s)(x,y)=s(x+y)
$$

and define

$$
F_2^{\mathrm{active}}(X)(x,y)
=f\bigl(X(x-1,y),X(x,y),X(x,y+1)\bigr).
$$

The west, center, and north cells represent logical offsets $-1,0,+1$ respectively. Hence

$$
F_2^{\mathrm{active}}E=EF_1
$$

for all 256 ECAs.

For any ECA whose left, center, and right inputs are all essential, those three physical dependency sites are noncollinear. The rule therefore has affine dependency dimension two: no fixed lattice change of basis plus uniform moving frame can place all of its essential reads on a single line.

The exhaustive source-rule audit finds **218 of 256 ECAs** with all three logical inputs essential. Rules 30, 54, and 110 are among them. Rule 90 is not: it ignores the center input, so its active lift has only affine dimension one despite spanning two directions relative to the output cell. Thus, for the 218-rule family, the two-dimensional dependence is active on the encoded trajectory itself; it is not merely an unused ambient direction.

For example, a Rule-110 source state becomes diagonal stripes. At every physical cell the 2D rule reads west, self, and north. Those three bits are exactly the Rule-110 left, center, and right inputs of the corresponding logical site. The resulting 2D field remains in the stripe family forever and is exactly the encoded Rule-110 future.

## A genuinely different ambient 2D rule for every ECA

Some ECAs ignore one or more logical inputs, so no lift that merely relocates their essential source inputs can force a two-dimensional essential stencil. A larger 2D rule can nevertheless contain the 1D dynamics as an invariant subsystem.

Keep the same diagonal embedding and start with the horizontal base rule

$$
B_f(X)(x,y)=f\bigl(X(x-1,y),X(x,y),X(x+1,y)\bigr).
$$

Encoded states satisfy the local equalities

$$
X(x+2,y)=X(x+1,y+1)
$$

and

$$
X(x-2,y)=X(x-1,y-1).
$$

For binary states define

$$
\begin{aligned}
F_2^{\mathrm{strong}}(X)(x,y)=B_f(X)(x,y)
&\oplus X(x+2,y)\oplus X(x+1,y+1)\\
&\oplus X(x-2,y)\oplus X(x-1,y-1).
\end{aligned}
$$

Both added pairs cancel on every encoded state, so

$$
F_2^{\mathrm{strong}}E=EF_1.
$$

Away from the encoded family, however, all four added sites are essential. They occupy two distinct parallel anti-diagonals, so their union has affine dimension two. The exhaustive local audit confirms this for **all 256 ECAs**, including constant rules.

This demonstrates an important freedom: specifying the induced law on an invariant encoded family does not uniquely specify the ambient higher-dimensional law. Many genuinely different 2D extensions can agree perfectly on the projected 1D dynamics while disagreeing elsewhere.

The extra four-site coupling in this particular universal construction is dormant on valid encoded states, so it is a proof of ambient-rule freedom, not yet a proof that every source rule can exercise irreducibly 2D coupling along its encoded orbit.

## Computational audit

The protocols were committed before their respective evaluations:

- [initial intertwining protocol](protocols/dimensional-intertwining-20260909.md);
- [stronger affine-dimension follow-up](protocols/dimensional-intertwining-strong-20260909.md), added after noticing that the first linear-rank criterion was too permissive under moving frames.

The [verifier](../../scripts/verify_dimensional_intertwining.py) exhaustively checks all 256 ECA truth tables and audits selected complete periodic state spaces. The checked-in [summary](../../results/dimensional_intertwining_20260909_summary.json) records:

| Check | Result |
| --- | ---: |
| ECA rules | 256 |
| Active-lift local intertwining failures | 0 |
| Active lifts with linear directional rank 2 | 228 |
| Active lifts with affine dependency dimension 2 | 218 |
| Universal four-site-gate local failures | 0 |
| Universal four-site-gate rules with affine dimension 2 | 256 |
| Selected periodic construction/state comparisons | 2,160 |
| Selected periodic failures | 0 |

The periodic audit covers Rules 0, 30, 54, 90, 110, and 255 on square tori of widths 3 through 6, over every source state at each width. These finite checks audit the implementation; the exact identities above establish the infinite-lattice claims.

Run:

```bash
python scripts/verify_dimensional_intertwining.py
```

## Relation to existing CA simulation language

There is established literature comparing cellular automata through simulations, encodings, and rescalings. Delorme, Mazoyer, Ollinger, and Theyssier's *Bulking II* formalizes several CA simulation quasi-orders, while Sablik and Theyssier emphasize that higher-dimensional CA have dynamical phenomena not present in 1D. The present construction should therefore not be presented as a novelty claim about CA simulation in general. Its value here is that it gives the Groovy Commutator program an especially transparent exact cross-dimensional commuting square and separates several notions of what it means for the higher-dimensional rule to be genuinely higher-dimensional.

- Delorme, Mazoyer, Ollinger, Theyssier, [*Bulking II: Classifications of Cellular Automata*](https://arxiv.org/abs/1001.5471).
- Sablik, Theyssier, [*Topological Dynamics of Cellular Automata: Dimension Matters*](https://arxiv.org/abs/0811.2731).

No claim of novelty for the lattice-quotient construction has been established here.

## Three increasingly strong meanings of “the 2D space follows its own rule”

The experiments and proof suggest a useful hierarchy.

1. **Ambient 2D rule.** A fixed local 2D CA has the projected trajectory as an invariant orbit. This is always achievable by the quotient construction.
2. **Active 2D stencil.** Essential dependencies of the 2D rule span the plane and are exercised on encoded states. The simple active ECA lift achieves this for the 218 rules essential in left, center, and right.
3. **Intrinsic 2D encoded state.** The encoded family itself possesses independent two-dimensional degrees of freedom, rather than being a redundant copy of a 1D configuration along fibers of a quotient map. This note does not achieve that.

The first two already answer the motivating question positively in substantial senses. The third is the more interesting research frontier.

## Why this is Groovy-Commutator-shaped

The original commutator asks whether two operations can be exchanged without changing the result. Here the operations are **evolve** and **change representation/dimension**:

$$
K_E=F_2E-EF_1
$$

or XOR in the binary case. A zero residual says that evolution is representation-independent across the declared dimensional change, provided each representation is allowed its own law.

That is a direct generalization of the project's earlier same-rule question. Instead of asking whether a transformation $P$ commutes with one update $F$,

$$
PF=FP,
$$

we ask whether $P$ *intertwines two different updates*,

$$
PF_1=F_2P.
$$

The natural next object is therefore not only a commutator but an **intertwining residual**: how much of the higher-dimensional state is required before a local $F_2$ can make that residual vanish?

## Next research target

The quotient construction makes existence too easy if arbitrary redundant embeddings and arbitrary ambient extensions are allowed. The next experiment should therefore freeze stronger constraints before searching:

- a local or block-local 1D-to-2D encoding rather than unrestricted global stripe replication;
- a bounded 2D neighborhood, preferably radius-one Moore or von Neumann;
- no dormant off-manifold gate whose only purpose is to certify ambient dimensionality;
- a requirement that both spatial directions carry independently variable encoded information or causal influence;
- a fixed decoder and cadence;
- exact closure under the 2D rule on the whole encoded family, not selected trajectories.

Then ask whether there exist pairs $(F_1,F_2)$ with

$$
F_2E=EF_1
$$

under those stronger conditions, and how common they are.

A particularly sharp version is: **can a 1D CA be represented by a 2D invariant family with genuine two-dimensional local degrees of freedom, while its decoded evolution remains exactly the original 1D law?**

That is no longer answered by diagonal stripes. It is the next place where cross-dimensional commutation might become selective rather than universal.
