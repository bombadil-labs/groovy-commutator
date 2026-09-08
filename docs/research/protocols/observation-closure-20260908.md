# Protocol: observation closure and derivative factor census

**Date:** 2026-09-08  
**Branch:** `research/closure-defect-20260908`  
**Status:** preregistered before the new enumeration

## Question

The existing Groovy commutator asks, for an elementary cellular automaton
`E_A` and derivative observation `D_A(S)=S XOR E_A(S)`, whether the observed
change mask evolves under the **same** rule:

\[
D_A E_A(S) \stackrel{?}{=} E_A D_A(S).
\]

The broader question is whether an observation supports **any autonomous
dynamics at all**. For an observation `P` and observed successor

\[
Y=P(S), \qquad Z=P(E^q(S)),
\]

we call the observation **exactly closed** on the tested state space when
`Z` is a deterministic function of `Y`:

\[
P(s_1)=P(s_2) \Longrightarrow P(E^q(s_1))=P(E^q(s_2)).
\]

Equivalently, there exists an induced map `B` on observed states such that

\[
P E^q = B P.
\]

This separates three questions that the same-rule commutator conflates:

1. **closure:** does any deterministic induced dynamics `B` exist?
2. **local rule closure:** is an induced `B` an elementary CA rule?
3. **self-similarity:** can `B` be the original rule `A`?

## Primary exact measurements

The microstate ensemble is the uniform enumeration of every binary state on a
periodic ring. For each observation we group microstates by `Y=P(S)` and
inspect the set/distribution of observed successors `Z`.

We record:

- `closure_entropy_bits = H(Z | Y)` under the uniform microstate ensemble;
- `closure_error = 1 - sum_y max_z count(y,z) / |X|`, the whole-state error
  of the optimal deterministic predictor `Y -> Z` under that ensemble;
- `ambiguous_observation_fraction`, the fraction of observed states with more
  than one possible observed successor;
- `same_rule_state_error`, the fraction of microstates for which the
  same-rule prediction disagrees with the observed successor;
- `same_rule_bit_error`, mean Hamming density of that disagreement;
- all elementary CA rules `B` satisfying the exact factor identity on the
  tested ring.

`H(Z|Y)=0` is the primary criterion for exact closure. The entropy is a graded
finite-state diagnostic when closure fails; it is not claimed to be an
asymptotic invariant.

## Experiment A: derivative observation

For every ECA rule `A in 0..255`:

\[
P=D_A, \qquad D_A(S)=S\oplus E_A(S), \qquad q=1.
\]

Discovery is exhaustive at ring width `n=12`. Every rule that is exactly
closed there, and every exact ECA factor `B` found there, is rechecked at
`n=16`.

This experiment directly compares the generalized closure criterion with the
existing Groovy commutator. It also searches all 256 ECA rules for an
alternative effective rule `B`, rather than assuming `B=A`.

### Preregistered expectations

- The known `G=0` rules should be same-rule factors and therefore exactly
  closed.
- The known constant-`G=1` rules are the sharpest test of the abstraction.
  For affine maps with bias one, algebra suggests
  `D_A E_A = E_(255-A) D_A`; therefore at least the nondegenerate members of
  this set should have zero closure defect despite a nonzero same-rule
  commutator.
- We do **not** assume that variable `G` implies nonclosure. Finding a rule
  with variable `G` but exact closure under `B != A` would be a stronger
  separation between commutation and closure.

## Experiment B: recover block-2 scale-rhyme as closure

For every ECA rule `A` and every nonconstant Boolean block map
`h:{0,1}^2 -> {0,1}`, use nonoverlapping two-cell blocks and

\[
P=h, \qquad q=2.
\]

At `n=12`, compute exact closure without assuming any form for the induced
map. Separately search all ECA rules `B` for

\[
h E_A^2 = E_B h.
\]

Because every nonconstant two-bit block map is surjective blockwise, an exact
induced map is unique on the full coarse state space. The existing
`experiment_scale_rhyme.py` reports 404 verified `(A,h,B)` triples at its
first census/recheck. This experiment should recover the same factor relation
within the same finite-ring scope. A disagreement is treated as an
implementation or definition problem, not a discovery.

We also mark the stricter fixed-point condition `B=A`, which is the user's
"coarse-grain then iterate under the existing ruleset" formulation.

## Follow-up gate

Only after A and B pass their internal controls do we extend the observation
family. The first extension will be one of:

- exhaustive three-cell Boolean block maps with `q=3`, or
- history-conditioned closure for derivative/block observations,

chosen from the first-pass result. This prevents a large sweep from hiding a
bad definition.

## Scope and nonclaims

- Exactness is exact only on the enumerated periodic rings; `n=16`
  rechecks reduce but do not eliminate finite-ring accidents.
- Positive conditional entropy is ensemble-dependent and is not called an
  information-theoretic invariant of the infinite CA.
- No Wolfram-class diagnostic is preregistered here.
- ECA-factor failure does not imply that no larger-radius, larger-alphabet,
  stochastic, or history-dependent effective dynamics exists.
- The experiment treats the **failure of closure** as data rather than merely
  rejecting an observation.
