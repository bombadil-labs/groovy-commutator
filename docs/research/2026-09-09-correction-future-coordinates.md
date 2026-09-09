# Correction stacks are coordinates for observed futures

A commutator tower can keep producing different maps after its information has
already stopped growing. This checkpoint proves the distinction and gives an
explicit local evolution law for a prepared correction stack. It then identifies
what these results leave unresolved about **rules becoming spatial programs**.

These are deductive results with exhaustive computational audits, not a new
Wolfram-class search or a claim to have solved recursive program spatialization.

## The finite-coordinate theorem

Let X be a binary configuration space, F:X->X any deterministic evolution, and
A:X->X an observation with the same output type. F need not be linear,
invertible, or zero-preserving. Use zero-based correction indexing here:

\[
A_0=A,\qquad A_{k+1}=A_k\circ F\oplus F\circ A_k.
\]

For the original construction, A=D=I XOR F, so A_1 is the Groovy commutator.
Define two tuples of **whole configurations**:

\[
K_h(S)=(A_0(S),\ldots,A_h(S)),\qquad
O_h(S)=(A(S),A(F(S)),\ldots,A(F^h(S))).
\]

**Theorem.** There is a bijection T_h on X^(h+1), depending only on F, such that

\[
\boxed{O_h=T_h K_h.}
\]

Consequently,

\[
\boxed{\ker K_h=\ker O_h
=\bigcap_{t=0}^{h}\ker(A\circ F^t).}
\]

Here kernel means equality of represented outputs, not a linear nullspace.

**Proof.** Start from arbitrary rows U_k^0, k=0,...,h, and form a triangular array:

\[
U_k^{t+1}=F(U_k^t)\oplus U_{k+1}^t,\qquad k+t<h.
\]

Read its left edge (U_0^0,...,U_0^h). This is T_h. The inverse starts with that
edge and recursively uses

\[
U_{k+1}^t=U_k^{t+1}\oplus F(U_k^t).
\]

Both operations recover the same triangular array, without inverting F.
For U_k^0=A_k(S), the defining correction identity implies
U_k^t=A_k(F^t(S)). The left edge is exactly O_h. This proves the claim.

For example,

\[
A_1=B_1\oplus F(B_0),
\]

\[
A_2=B_2\oplus F(B_1)\oplus F(B_1\oplus F(B_0)),
\qquad B_t=A(F^t(S)).
\]

Do not distribute the last F over XOR for a nonlinear source.

This is an equality of whole-field information. At a fixed site, computing
the change of coordinates can require neighboring sites. If F has radius r,
T_h and its inverse need at most horizontal radius hr.

## The exact bridge between the two programs

The infinite correction stack identifies precisely the states with the same
entire observed future:

\[
\ker K_\infty=\bigcap_{t\ge0}\ker(A\circ F^t).
\]

This is the future-equivalence relation in
[Dynamics of Erased Distinctions](2026-09-08-dynamics-of-erased-distinctions.md).
For a finite ensemble, any probability distribution gives
H(K_h)=H(O_h), and hence

\[
H(A_{h+1}\mid K_h)
=H(A\circ F^{h+1}\mid O_h).
\]

These entropies concern the random **whole fields** on that finite ensemble.

Thus the commutator hierarchy and predictive refinement are two coordinate
descriptions of the same retained distinctions. One emphasizes transport
corrections; the other emphasizes observed continuations.

O_h is a **forward observation window anchored at S**, not a past history
already available at the same instant. The theorem does not manufacture
observations of an unknown future. The finite-word closure criterion is the
one used in [the history-lift work](2026-09-08-history-lift-closure.md), with its
declared time alignment.

## Finite closure does not require a repeated correction map

The represented tuple K_h evolves autonomously exactly when the next
correction factors through it:

\[
\boxed{A_{h+1}=g_h\circ K_h.}
\]

Indeed, its next state is

\[
(A_0,\ldots,A_h)'=
(F(A_0)\oplus A_1,\ldots,F(A_{h-1})\oplus A_h,
 F(A_h)\oplus g_h(K_h)).
\]

Equivalently, ker K_h=ker K_(h+1). The relation is then forward invariant,
so the tuple determines every future observation and every later correction.

A repeated individual map is sufficient to supply some closures, but is not
necessary. What matters is whether the next map adds a distinction to the
**joint observation**.

The width-eight audit illustrates this sharply:

| Rule | First closed correction index h, tested through 3 | Distinct maps A_0,...,A_4 | Fiber counts for K_0,...,K_4 |
| --- | ---: | ---: | --- |
| 30 | 1 | 5 | 240, 254, 254, 254, 254 |
| 54 | 2 | 5 | 100, 215, 249, 249, 249 |
| 110 | 1 | 5 | 104, 254, 254, 254, 254 |
| 184 | 3 | 5 | 46, 190, 238, 254, 254 |
| 232 | 0 | 5 | 66, 66, 66, 66, 66 |

These are exact finite-ring results, not infinite-lattice closure proofs.
Rule 232 also has the stronger existing local certificate:
D_232 evolves under Rule 128 on its image, verified on every five-cell
window in [Research022](2026-09-08-observation-closure.md). Its current
derivative is already a locally sufficient state although its first five
correction maps are distinct.

This does not invalidate the previous map censuses. It changes their
interpretation as representation budgets.

## A local spatial update exists for a prepared infinite stack

For a binary CA F of radius r in d dimensions, put U(x,k)=A_k(S)(x) for
k>=0. The fixed construction

\[
\boxed{\mathcal H_F(U)(x,k)=F(U(\cdot,k))(x)\oplus U(x,k+1)}
\]

uses the source neighborhood within a layer and one adjacent correction cell.
It has bounded radius max(r,1), independent of correction depth. For an ECA:

\[
U'_{x,k}=f(U_{x-1,k},U_{x,k},U_{x+1,k})\oplus U_{x,k+1}.
\]

The same formula at every site is a binary CA on the full (d+1)-dimensional
lattice. If its nonnegative layers are initialized to the correction stack,
those layers remain exact for all time; arbitrary negative layers cannot
influence them. Equivalently it gives an autonomous half-space realization:

\[
\mathcal H_F K_\infty=K_\infty F.
\]

The radius bound is uniform, not the source truth table: this is one
rule-independent recipe producing a law H_F for each F. Overlapping
neighborhoods pose no consistency problem for this construction.

This addresses the broad geometric question in the current Program, but has
three decisive limitations:

1. The whole infinite correction stack is supplied initially. Each fixed
   layer is locally computable, but its required encoding radius can grow
   with k. No uniformly local finite preparation has been established.
2. The bottom projection returns A(S), not necessarily S. For A=D the
   representation can be noninjective. It is not automatically an embedding
   of the complete source trajectory.
3. The source rule f occurs in the upper law. Its program bits have not been
   promoted to mutable spatial data under the original selector grammar.

A finite stack initialized through level H gives correct layer k through
time H-k, independently of arbitrary upper-boundary updates. Indefinite
finite-height evolution needs a locally computable top closure g_H or an
equally explicit boundary mechanism. The infinite stack is a control for
that problem, not its solution.

For local A and F on the full binary shift, an all-configuration factorization
A_(h+1)=g_h K_h actually guarantees that g_h has *some* finite spatial radius
on the image of K_h. To see this, K_h is a continuous surjection from a compact
space onto its compact image, hence a quotient map. The factored map g_h is
continuous and shift-equivariant. Compactness then supplies a common finite
window determining its output at the origin, and shifts supply the same rule
everywhere. Extend the local rule arbitrarily on unrealized patterns.

This is the standard compactness/local-rule argument underlying the
Curtis-Hedlund characterization; see
[Capobianco and Uustalu, sections 4–5](https://arxiv.org/abs/1012.1220).
It gives neither a small radius nor a uniform bound across h or source rules.
A factorization on one finite ring does not satisfy its premise.

## The program-inheritance requirement still matters

The attached guidance correctly emphasizes factored programs over expanded
truth tables. But one binding distinction must be explicit.

For a fixed spatial assignment sigma, the original selector is

\[
H_\sigma(X)_z=X_{z+\sigma(4X_{z-e_1}+2X_z+X_{z+e_1})},
\]

where e_1 is the horizontal unit vector and sigma selects one of the eight
surrounding offsets. More simply, in the repository's notation,
c'=n_(p[4W+2C+E]).

There is no ECA parameter R in this law. Assigning its eight outputs to a
particular neighborhood initializes the data read there; it does not create
a different global H_sigma for each R.

Consequently, keeping sigma fixed and changing the initial eight-bit table
gives 256 possible program values under one ambient law, not by itself a
lineage of 256 distinct promoted global laws. This follows directly from
[the existing selector definition](2026-09-08-shared-state-rule.md).

That is not an objection to instruction/state sharing. It identifies the
missing interface: how does a source program become a **causally active
inherited parameter of the next program**, while overlapping neighborhoods
remain consistent?

A sharp next protocol should declare, before scoring rules:

- a dimension-indexed grammar G_d and its interpretation as local laws;
- a single geometric encoding and decoder recipe defining
  L_d:G_d -> G_(d+1), rather than choosing a simulator afterward;
- which operands are fixed grammar, inherited program data, and changing
  state;
- block size, phases, alphabet, cadence, preparation locality, and allowed
  boundary resources;
- an operational preservation identity and a source-program intervention
  check at both the first and second lift.

For the intervention check, hold the declared input fixed wherever compatible
with the shared program/state geometry, change the inherited program, and
determine which decoded outputs can change. Explicitly record alias constraints
when the same cells supply both input and program. A
many-to-one lift is allowed, but a constant map into one ambient interpreter
must be reported as such. This is a necessary audit, not a demand that every
source bit remain significant forever.

The first two arrows should pass that check and exact overlap consistency
before a larger dimensional or class census. The source-binding observation
above is the smallest exact rejection of the naive frozen-decoder interpretation;
it does not reject the more careful dynamic-program interpretation.

Self-representing program grammars have precedents in
[fixed-point tile constructions](https://arxiv.org/abs/0910.2415). They are
useful background on recursive descriptions, not a proof of this particular
dimensional CA claim. No novelty claim is made here.

## Audit and reproduction

The [dependency-free verifier](../../scripts/verify_correction_future_coordinates.mjs)
can be run with Node:

```bash
node scripts/verify_correction_future_coordinates.mjs
```

Its [saved results](../../results/correction_future_coordinates_20260909.json)
record:

- all 256 evolutions and all 256 observations on a two-bit state space:
  262,144 evolution/observation/state checks and 262,144 partition comparisons;
- 65,536 arbitrary four-row words tested in both directions, including words
  not realizable as an observation sequence;
- all 256 ECAs and all 256 width-eight states: 65,536 state checks and
  1,280 horizon-partition comparisons;
- every 11-bit causal window for every ECA, with no periodic boundary:
  524,288 windows, 2,621,440 coordinate checks and 2,097,152 transport checks.

The local audit compares direct composition truth tables with independently
constructed shrinking-window trajectories and triangular differences. All
checks pass. The algebraic proofs establish the unbounded statements; the
computations audit explicit finite instances.

This checkpoint was derived after reading the prior results. Its numbers are
audits, not preregistered predictions or independent research replications.
