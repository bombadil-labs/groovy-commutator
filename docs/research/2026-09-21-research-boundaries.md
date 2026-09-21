# What we can prove, what we cannot infer, and where this project contributes

**Research synthesis, 2026-09-21.** Authored by Codex (OpenAI).
Reviewed by: none; integrated under Myk's reset-specific review suspension.
This is a source-based scope guide, not a new theorem or an exhaustive survey.
The active agenda is [START_HERE](START_HERE.md).

## The productive question

Fix dynamics `E`, an observation `Q`, a positive cadence `q` and an invariant
state family `X`. We seek an autonomous observed law `F` such that

\[
Q E^q = F Q \quad\text{on }X.
\]

Such a set map exists on `Q(X)` exactly when equal present observations have
equal next observations. A pair with `Q(x)=Q(y)` but different successors
refutes every deterministic present-only factor on that domain. The factor is
unique on the observed image; locality, finite radius and extension to ambient
states are extra requirements. A failure of the *prescribed* same-law equation
is weaker: it may only mean that the effective law changed.

This connects the project to factor maps, coarse-graining and predictive-state
equivalence. It gives us objects that can be proved or refuted without solving
the generic future of a universal CA. The repository's
[shared closure account](2026-09-10-shared-closure-account.md) already makes
this distinction. Its scope is more useful than searching for a universal
scalar signature of “Class IV.”

## Which limits actually apply?

| Question and quantifiers | Status | Practical consequence |
| --- | --- | --- |
| A fixed finite-time observation of a finite-radius CA | Its finite light cone determines it. | Compute exactly when the domain is affordable. |
| Eventual behavior on a specified finite ring | A finite state graph is decidable by exhaustive analysis. | Potentially exponential cost; no automatic statement about the line. |
| A rule-level label on the fixed list of 256 ECAs | Any well-defined assignment is a finite table. | General classification undecidability does not forbid this table, but does not define the labels or make a fitted score explanatory. |
| Arbitrary CA under specified unbounded behavioral classifications | Important formal versions are undecidable. | A universal terminating classifier needs an exact property and theorem, not a visual analogy. |
| A fixed universal rule on arbitrary encoded inputs, with an unbounded horizon | Encoded halting/reachability questions can remain undecidable. | Fixing the rule does not fix the computational input or bound its future. |
| An explicit factor, invariant family, finite-state obstruction or restricted observable | Often admits exact positive and negative certificates. | This is the main opening for useful work here. |

The first three rows follow from locality and finite-state reasoning. For the
unbounded rows, the hypotheses matter:

- **Classification:** [Culik and Yu (1988)](https://www.complex-systems.com/abstracts/v02_i02_a02/)
  prove undecidability for formal CA classification questions, including
  eventual quiescence for all finite-support configurations. Finite support
  on an unbounded lattice is not a fixed finite ring. Their formal classes
  are not a license to assert that every visual Wolfram-class judgment is
  mathematically impossible.
- **Limit sets:** [Guillon and Richard (2010)](https://richardg.users.greyc.fr/publis/Guillon-Richard_2010.pdf)
  refine Rice-style results for properties of CA limit sets. In the fixed
  binary setting, surjectivity is the nontrivial decidable exception, up to
  complement. These theorems concern their specified limit-set properties
  and rule families; they do not say that all dynamical properties are
  undecidable or that a fixed radius-one catalogue is undecidable.
- **Universality:** [Cook (2004)](https://wpmedia.wolfram.com/sites/13/2018/02/15-1-1.pdf)
  constructs universal computation in Rule 110 using structured encodings.
  That establishes computational capability, not the prevalence or character
  of behavior under an IID initial ensemble.
- **Complexity:** [Neary and Woods (2006)](https://mural.maynoothuniversity.ie/id/eprint/15737/)
  establish P-completeness of the standard finite Rule 110 prediction problem.
  Under `P ≠ NC`, this obstructs a general efficient parallel predictor in
  that model. It is not an unconditional theorem that every trajectory or
  observable requires literal step-by-step simulation.

“Computational irreducibility,” worst-case hardness, undecidability, empirical
unpredictability and statistical complexity must not substitute for one
another in a claim. Nor does a solver timeout establish any of them.

## Prior art and the contribution we still need to articulate

| Established research | What it licenses here | What we must add or avoid claiming |
| --- | --- | --- |
| [Israeli and Goldenfeld, computational irreducibility and coarse-graining](https://arxiv.org/abs/nlin/0508033) | Complex and universal microscopic dynamics can admit exact simpler descriptions. | Factor existence alone is not a new idea; give the particular factor, obstruction or cost advantage. |
| [Song and Grochow, CA coarse-graining searches](https://arxiv.org/abs/2012.12153) | Algorithmic searches can improve the finite block-size frontier. | Failure through a bounded block size is not impossibility at every size. Compare contracts before comparing counts. |
| [Shalizi and Crutchfield, causal states](https://arxiv.org/abs/cond-mat/9907176) | Predictively equivalent histories define minimal predictive descriptions under stated assumptions. | Our deterministic forward equivalence on initial states is not automatically the same object as a probabilistic causal-state model or online suffix learner. |
| [Rupe and Crutchfield, local causal states](https://arxiv.org/abs/1801.00515) | Domains, defects and coherent structures can be identified relative to local predictive organization. | Merely finding particles is not a Class-IV discriminator; compare with existing domain/particle accounts before inventing another score. |
| [Feldman, McTague and Crutchfield, complexity–entropy diagrams](https://arxiv.org/abs/0806.4789) | Multiple statistical dimensions can reveal structure. | No universal one-dimensional “edge of chaos” ranking follows. |
| [Capobianco, induced cellular automata](https://arxiv.org/pdf/0711.3841) | Embedding CA into a larger underlying group has established constructions. | Cross-dimensional existence is not the novelty claim; distinguish the six-field grammar, binary phase decoding and memory bounds. |

These are comparison targets, not a claim that the repository has completed a
priority search. The specific census, witness, graph restriction or encoding
may be useful even when its organizing definition is classical.

## The strongest repository results

**Exact representation distinctions.** The
[erased-distinctions account](2026-09-08-dynamics-of-erased-distinctions.md)
separates closure from same-law commutation. Rule 255 is a decisive example:
its derivative observation is invertible complementation, its Groovy
commutator is constantly one, and its effective derivative law is constantly
zero. The representation loses no information despite maximal same-law error.

**Certificates across domains.** A
[finite pair graph](2026-09-11-ring-closure-certificate.md) certifies closure
for all ring sizes under the stated local observations. At greater refinement
depth, closed walks and bi-infinitely extendable paths differ. The
[full-line witnesses](2026-09-11-full-shift-depth-two.md) show why checking
periodic states is insufficient for those depth claims. PR #229's
[carrying-component restriction](2026-09-14-depth-three-onset.md) also makes
an exact onset computation affordable: under observation 232 the depth-three
onset is 65, realized by rules 94 and 133. Its failed bets under observations
4 and 32 stay in the record. The useful result is the certificate and cost
reduction, not an invitation to extend every depth ladder.

**A completed construction.** The
[affine-oriented lift](2026-09-17-affine-oriented-lift-theorem.md) supplies a
locally recoverable binary representation of any finite-memory binary CA one
dimension higher, recursively through every finite depth. Its existence
question is closed under its contract. The
[proof's sections 33–34](proofs/affine-oriented-lift-proof-state-20260917.md)
already discuss prior art and the simpler `001`/`011` period-three necklace.
Further lifting work needs a stated resource advantage over that baseline and
ordinary stored history, including any cost of preprocessing the encoding.
Faithful simulation does not establish spontaneous formation, restoration
after perturbation, optimality or a unique ambient completion.

**An obstruction to overinterpretation.** The
[native commutator completion audit](2026-09-15-commutator-completion.md)
shows that difference configurations can leave the constrained beam, so
native lifted commutators can read unconstrained table entries even while
on-beam dynamics is fixed. This is a limit on that observable, not a
failure of faithful representation or of transported algebra.

**Restricted mechanisms.** Equal-row invariance and
[defect algebra](2026-09-18-defect-algebra.md) explain behavior in a specified
refinement family. They do not yet explain Class IV. The
[held-structures account](2026-09-21-held-structures-account.md) now makes the
ninth unit's partial validity explicit rather than treating every stored
score as evidence.

## What a useful next result looks like

A reader should be able to name a contract, inspect a certificate or witness,
understand the closest prior method and say what decision the result changes.
The [three-case task](NEXT_TASK.md) is designed to produce that account from
evidence already paid for. A general classifier, another rule catalogue or a
larger solver budget is not the default continuation. The mathematics can
remain open after a line stops receiving computation.
