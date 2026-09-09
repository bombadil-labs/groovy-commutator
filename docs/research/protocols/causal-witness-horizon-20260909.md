# Protocol: causal witness horizon for local predictive distinctions — 2026-09-09

**Status:** frozen before evaluation.  
**Branch:** `research/causal-witness-horizon-20260909`  
**Dependency:** Research029–030 future-context quotients.

## Question

Research030 found that every nonclosed block-3 ECA target on the `n=12` ring reaches its final local future-context quotient by macro-horizon 2, even though global predictive history reaches 23; selected `n=15` cases preserve the separation.

The next question is whether that shallow quotient-discovery horizon is a finite-ring accident or a consequence of local causal geometry:

> **If two local symbols can ever be distinguished by the future target, how far into the future must one look before some finite surrounding context can witness that distinction?**

## Matched-scale macro dynamics

For an ECA of fine radius `r=1`, block size `b=3`, and cadence `q=3`, one three-cell output block after three fine ticks depends on exactly nine fine input cells:

`3 + 2*q*r = 9`.

Those nine cells are exactly three aligned three-cell input blocks. Therefore every ECA induces an exact radius-1 macro cellular automaton

`G : A^Z -> A^Z`,

on the eight-symbol block alphabet `A={0,...,7}` before the binary target map is applied.

This fact is algebraic and system-size independent.

## Infinite/local causal witness definition

Fix a binary block target `T:A->{0,1}` and induced radius-1 macro CA `G`.

For local symbols `a,b in A`, define the **causal witness horizon**

`w_T(a,b)`

as the least macro-time `t>=0` for which there exists a finite initial macro-context, identical except for `a` versus `b` at the origin, such that the target spacetime fields differ somewhere by time `t`.

If no such context exists, set `w_T(a,b)=infinity`.

Because `G` has radius 1, a witness at time `t` can be checked on a finite initial interval. For a target difference at output site `j` with `|j|<=t`, only the initial interval `[j-t,j+t]` matters; taking the union over possible affected output sites gives the sufficient witness window `[-2t,2t]`, of width `4t+1` macro-symbols.

The protocol will verify this finite-cone reduction independently against large periodic rings before using it as the local/infinite reference.

## Local witness quotient

For every horizon `h`, define a local relation

`a ~^loc_h b`

iff **no** finite causal-cone context witnesses a target difference through time `h`.

Let `L_h` be the corresponding partition when the relation is an equivalence relation. Independently verify reflexivity, symmetry, and transitivity in every computed case; if transitivity fails, retain the pairwise relation rather than forcing a partition.

The eventual local relation is

`~^loc_infinity = intersection_h ~^loc_h`.

## Connection to Research030

Research030's ring quotient `Q_h^(n)` uses complete periodic-ring contexts. For a ring with `m=n/b` macroblocks, a finite witness cone is wrap-free through horizon `h` whenever the required context interval embeds without identification.

The protocol will not assume that the `n=12` observation `d_Q<=2` is already system-size independent. Instead it compares:

1. exact local causal-cone witness horizons;
2. periodic-ring quotient chains at `n=12,15,18` where feasible;
3. the final Research030 quotients on the original domain.

## Primary theorem target

Prove the following locality statement independently of the census:

> If a symbol pair has a target witness by macro-time `t`, then it has a witness supported entirely inside the initial macro-interval `[-2t,2t]`.

This is a direct light-cone theorem and gives a finite exact search for each fixed horizon.

Do **not** preregister a universal small upper bound on `w_T(a,b)`. The empirical `d_Q<=2` result motivates the search but is not evidence that arbitrary local CA admit such a bound.

## Primary exact experiments

### A. Original block-3 ECA domain, local cone rather than ring

For all 256 ECA rules and all 127 canonical nonconstant binary block-3 targets:

- compute all pair witness relations through horizons `h=0,1,2,3` by exhaustive local-cone context search;
- compare the horizon-0/1/2 local relations with the corresponding `n=12` Research030 quotient chain;
- record every pair first distinguished at each horizon;
- record whether any pair merged through `h=2` is distinguished at `h=3`.

The central preregistered test is:

> **Does the local, wrap-free calculation preserve the empirical `d_Q<=2` phenomenon, or do horizon-3 witnesses appear once the ring artifact is removed?**

A single exact horizon-3 witness falsifies the system-size-independent `<=2` conjecture.

### B. Larger periodic controls

For all cases implicated by any local/ring mismatch, evaluate the same target at periodic widths `n=15` and `n=18` where exact state enumeration is feasible.

Freeze any larger-width target/rule cases before inspecting those results.

### C. Macro-rule structural audit

For every ECA, explicitly construct its induced radius-1 macro rule `g:A^3->A` and independently verify on random and exhaustive small configurations that one macro step equals three fine ECA steps under block encoding.

Measure whether witness-depth behavior can be predicted from simple macro-rule properties such as:

- argument sensitivity of `g`;
- target class balance;
- one-step image partition;
- pairwise defect branching count.

These are exploratory diagnostics only.

## Ring-artifact prediction

Before evaluation, retain both possibilities:

- **Locality hypothesis:** no horizon-3 local witnesses occur; the `d_Q<=2` phenomenon survives removal of periodic wrap and becomes a serious theorem target for this ECA/block-3 family.
- **Ring-artifact hypothesis:** at least one pair has no ring-visible distinction by horizon 2 on `n=12` but gains a local causal-cone witness at horizon 3 or later.

Do not alter the search family after seeing which branch wins.

## Independent audit

An independently written scalar implementation must verify:

1. the exact block macro rule against three fine ECA steps;
2. every reported horizon-3 counterexample, if any, by explicit paired finite configurations;
3. selected no-horizon-3 cases by exhaustive context counts;
4. any larger-width frozen confirmation.

## Literature positioning

Before publication, compare the construction to finite-state distinguishability / Myhill–Nerode refinement, local congruences of cellular automata, observability of symbolic dynamical systems, and light-cone/de Bruijn methods. Do not claim novelty for partition refinement or finite-state distinguishability itself.

The Groovy-specific question is the **timescale and geometry of predictive local distinctions under a lossy target observation**, especially its separation from global predictive memory.

## Scope and nonclaims

- Exact local-cone claims concern the declared ECA/block-3/cadence-3 family unless explicitly proved more generally.
- `n=12` and `n=15` periodic results do not establish an infinite-lattice bound.
- A finite witness horizon is an existential context statement; it does not say a distinction becomes visible quickly in typical contexts.
- A short witness horizon does not imply short global memory.
- The 3D hypothesis remains parked.

## Decision rule

If horizon-3 local witnesses exist, characterize the smallest counterexample and determine how witness depth scales with block size/cadence before attempting learning from sparse contexts.

If no horizon-3 witnesses exist across the complete local ECA/block-3 family, shift from census to proof search: identify the macro-rule property forcing two-step completeness, then test that property outside ECA.