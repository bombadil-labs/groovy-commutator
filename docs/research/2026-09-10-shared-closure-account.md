# One representation contract, two different failures

An observation can support exact autonomous dynamics even when the particular update law we tried is wrong. This is the common account agreed in [issue61](https://github.com/bombadil-labs/groovy-commutator/issues/61#issuecomment-5622836331): distinguish failure of a candidate law from failure of every possible factor law, and ask which initially hidden distinctions become visible under the declared dynamics.

This is a synthesis of existing results and the signed discussion with Fable/Claude. No experiment is added or rerun, no evidence label is upgraded, and no new renormalization interpretation is claimed. [Research022](2026-09-08-observation-closure.md) already establishes the central distinction. The purpose is to state it consistently across both Programs and give Research022–028 and Research035 explicit knowledge provenance.

## Fix the domain and the clock

Let F be deterministic dynamics, q a positive integer cadence, and X a declared nonempty family satisfying $F^q(X)\subseteq X$. Write $T=F^q|_X$. An observation $P:X\to Y$ induces the equivalence relation

$$
R_0=\ker P=\{(s,u)\in X^2:P(s)=P(u)\}.
$$

Here kernel means equal observations, without assuming linearity. The law, family, observation and cadence are all part of the contract. A claim about a periodic ring, a constrained image or an infinite lattice must name that domain; results do not transfer between them merely because rule numbers match.

## Factor existence and uniqueness on the image

A deterministic factor $B:P(X)\to P(X)$ exists with $PT=BP$ exactly when

$$
\ker P\subseteq\ker(PT).
$$

Necessity follows by applying B to equal observations. For sufficiency define $B(P(s))=P(T(s))$; the inclusion makes this independent of which representative s is chosen. Forward invariance makes the output belong to $P(X)$. The definition also proves uniqueness on that image.

This is existence of a whole-state function. Locality, radius, alphabet, computational cost and membership in a chosen model family are additional requirements. Values outside $P(X)$ are not determined by the factor identity. The [extension-freedom checkpoint](2026-09-10-extension-freedom.md) and [full-gradient result](2026-09-10-full-gradient-closure.md) keep those distinctions explicit.

## The error of a particular candidate law

For a well-typed candidate $B_{\rm cand}$, compare the two maps $PT$ and $B_{\rm cand}P$. Their disagreement set is

$$
\{s\in X:P(T(s))\ne B_{\rm cand}(P(s))\}.
$$

If the observation space has the required binary-group structure, its pointwise error field can be written

$$
\Delta_{P,B_{\rm cand}}(s)=P(T(s))\oplus B_{\rm cand}(P(s)).
$$

For general observations retain the map pair or disagreement set; subtraction or XOR is not automatic. Empty disagreement for some candidate establishes closure. Nonempty disagreement for the candidate we happened to try does not refute closure. A same-rule comparison also requires the source rule to be well typed on the observed space.

The original Groovy quantity is the binary special case $P=D=I\oplus F$, $q=1$, and $B_{\rm cand}=F$. Its correction field reconciles those particular transport paths. If factor closure fails, every candidate must disagree somewhere, but one candidate's error does not identify all distinctions responsible for that failure.

### Rule255 separates the two questions

For Rule255, $F(s)=\mathbf1$ and $D(s)=s\oplus\mathbf1$. D is invertible and erases no distinctions. Nevertheless

$$
D(F(s))=\mathbf0,\qquad F(D(s))=\mathbf1,\qquad G(s)=\mathbf1.
$$

The actual derivative factor is $B(y)=\mathbf0$. Thus maximal same-rule disagreement can coexist with an invertible observation and exact factor closure. This is a direct algebraic example, already covered by the bias-flip family in Research022.

## When hidden distinctions become visible

Use the same map T and family X throughout:

$$
R_t=\bigcap_{j=0}^{t}(T\times T)^{-j}(R_0),\qquad
R_\infty=\bigcap_{j\ge0}(T\times T)^{-j}(R_0).
$$

$R_t$ identifies initial states with equal observed words through time t. $R_\infty$ identifies states whose complete observed futures agree. It is the coarsest forward-invariant equivalence relation refining $R_0$: any invariant relation contained in $R_0$ stays inside every inverse image in the intersection. Consequently ordinary factor closure is equivalent to $R_0=R_\infty$.

On a finite X, partition refinement stabilizes after finitely many strict refinements. This exact finite-state property does not supply a size-independent memory or radius bound on an infinite lattice. [Research023](2026-09-08-history-lift-closure.md) distinguishes those costs, and [Research024](2026-09-08-observer-search.md) shows that observer choice changes the finite memory profile.

These are forward observed-word partitions of initial states. Their relation to prediction from a completed history window is exact under the stated domain and cadence. They are not themselves an online suffix learner, an adaptive partition algorithm, or its memory-state implementation; the latter is the separate scope of issue64.

## Information budgets need a probability law

For a finite random initial state S with a declared distribution, let C be its $R_\infty$ class. Both C and P(S) are deterministic functions of S, and C determines P(S). The chain rule gives

$$
H(S)=H(P(S))+\underbrace{H(C\mid P(S))}_{I_{\rm latent}}
+\underbrace{H(S\mid C)}_{I_{\rm shielded}}.
$$

[Research025](2026-09-08-fiber-visibility.md) uses the uniform microstate ensemble for its finite census. Full support matters if entropy zero is used to infer closure over the entire declared family; a prior assigning zero weight to a conflicting state can hide that failure.

[Research026](2026-09-08-possibility-frontier.md) calls the latent term future repertoire. It measures unresolved observed futures under that prior. Intervention power needs an action interface as well. The completed [gradient intervention audit](2026-09-10-gradient-intervention-costs.md) uses a different contract: the full state is known, actions are simultaneous flat masks, and a hard support budget restricts the deterministic channel. These quantities must not be substituted for one another.

## How the Programs meet

The dimensional work studies candidate-law correction through its correction rows and factor existence through the transverse/full-gradient tests. Erased Distinctions studies factor closure, future refinement, visibility and representation repair. Neither Program is confined to only one kind of defect.

The [correction/future coordinate theorem](2026-09-09-correction-future-coordinates.md) supplies a concrete bridge: finite correction tuples and observed-future tuples have identical whole-field fibers under an explicit triangular recoding. [Research035](2026-09-09-ternary-commutator-lift.md) concerns the vocabulary of individual L/R/C maps; growth of that vocabulary alone does not measure the information retained jointly or establish a minimum physical dimension.

The approved synthesis does not equate a factor with an RG fixed point or a correction with an irrelevant operator. Such correspondences require a defined renormalization map and scaling behavior. No Schur, gauge/curvature, Class-IV selection, or novelty claim follows from this account.

## Provenance added to the knowledge graph

| Research record | Reusable account |
| --- | --- |
| 022: observation closure | [Factor existence versus candidate-law disagreement](../knowledge/observation-factor.md) |
| 023: history lift | [Predictive future refinement](../knowledge/predictive-future-refinement.md) |
| 024: observer search | [Observer-dependent causal visibility](../knowledge/observer-dependent-visibility.md) |
| 025: fiber visibility | [Latent and shielded information budget](../knowledge/latent-shielded-budget.md) |
| 026: possibility frontier | [Closure and repertoire objectives](../knowledge/closure-repertoire-frontier.md) |
| 027: representation design | [Fixed-target representation repair](../knowledge/fixed-target-representation-repair.md) |
| 028: predictive synergy | [The finite obstruction to greedy repair](../knowledge/predictive-synergy.md) |
| 035: ternary lift | [Ternary role algebra](../knowledge/ternary-role-algebra.md) |

These entries cite the existing chronological records. Their definitions, domains, finite bounds, failed predictions and exploratory extensions remain in those records. Both Program pages link this shared account, and the knowledge graph records only explicit prerequisite relations justified by the definitions.
