# Protocol: symbolic causal-witness automaton — 2026-09-09

**Status:** frozen after a bounded exploratory prototype and before the fresh horizon-5/6 evaluation.  
**Branch:** `research/causal-witness-automaton-20260909`  
**Dependency:** Research031 causal witness horizon.

## Question

Research031 makes fixed-horizon causal-witness search exact by enumerating every dependency word of length `2h+1`. That search is exponential in horizon:

\[
8^{2h+1}
\]

for the matched block-3 ECA macro alphabet.

The next question is:

> **Can the same exact witness relation be represented symbolically so that deeper horizons can be searched without enumerating every light-cone word?**

The immediate scientific target is the first witness horizon beyond 3, if one exists. A secondary target is the growth law of the symbolic state representation itself.

## Exact macro system

Reuse the Research031 construction. For every ECA rule, block size 3 and cadence 3 induce an exact radius-1 cellular automaton

\[
g:A^3\to A,
\qquad A=\{0,\ldots,7\}.
\]

At macro-horizon `h`, one output symbol is a deterministic function

\[
F_h:A^{2h+1}\to A.
\]

Research031 evaluates `F_h` by explicit enumeration through `h=3`. Research032 represents `F_h` as a reduced ordered multi-valued decision diagram.

## Reduced 8-ary decision automaton

Use variables

\[
x_0,x_1,\ldots,x_{2h}\in A
\]

in fixed left-to-right order.

A decision node is

\[
(v;c_0,\ldots,c_7),
\]

meaning “inspect variable `x_v`; if its value is `j`, continue at child `c_j`.” Leaves are the eight output symbols in `A`.

Apply the standard two reductions:

1. if all eight children are identical, replace the node by that child;
2. hash-cons identical `(variable, children)` nodes so they are represented once.

The resulting rooted DAG is a canonical reduced ordered 8-valued decision diagram for the chosen variable order. It is equivalently a finite acyclic automaton recognizing context classes that induce the same remaining local computation.

## Symbolic CA composition

Start with one decision node for each input variable. To apply one macrostep, compose the local rule `g` with three adjacent symbolic functions.

For symbolic roots `u,v,w`, define `Apply_g(u,v,w)` recursively:

- if all three are leaves, return `g(u,v,w)`;
- otherwise inspect the least next variable among the three roots, recurse on its eight common assignments, then reduce/hash-cons the resulting node.

Repeated local composition shrinks the symbolic row by two roots per macrostep. After `h` steps one root remains and represents `F_h` exactly.

Memoize all apply operations.

## Exact pair-witness query

Fix an input-symbol pair `a,b` and an input axis `k`.

Restrict the root for `F_h` to

\[
x_k=a
\]

and

\[
x_k=b.
\]

The two restricted MDDs still share all other variables. Traverse them synchronously under identical remaining assignments. The reachable leaf pairs

\[
(u,v)\in A^2
\]

are **exactly** the output-symbol pairs obtainable from contexts identical except for `a` versus `b` at axis `k`.

For a binary target `T`, the pair is witnessed at `(h,k)` iff some reachable leaf pair satisfies

\[
T(u)\ne T(v).
\]

OR over all axes `k=0,...,2h` to obtain the exact target-witness mask for `(a,b)` at horizon `h`.

Thus the symbolic automaton computes the same existential relation as Research031 without enumerating all `8^(2h+1)` words.

## Adaptive evaluation

For each ECA rule maintain the cumulative set of pair/target distinctions already witnessed.

At each horizon:

1. build the reduced MDD for `F_h`;
2. compute all 28 unordered input-pair target masks;
3. record newly born pair/target distinctions;
4. if every pair/target distinction that can ever be distinguished under the tested target family is already witnessed, stop that rule and do not construct deeper MDDs.

This adaptive rule is important: symbolic complexity can grow quickly for some induced macro rules, but those same rules may already have no unresolved target distinctions.

## Discovery already observed before this freeze

The following are **exploratory pilot observations**, not preregistered confirmation results:

- the MDD construction reproduces the Rule-35 horizon-3 witness from Research031;
- a complete prototype pass over all 256 rules found **zero newly born pair/target distinctions at horizon 4**;
- a prototype pass over Rules 0–63 found **zero newly born pair/target distinctions at horizon 5**;
- horizon-4 MDD size is highly heterogeneous: median state count is small, while a few rules have much larger symbolic functions;
- large symbolic functions can nevertheless terminate early because all target distinctions were already witnessed at shallower horizons.

These observations must be reproduced by the committed production instrument but are labeled discovery rather than fresh evidence.

## Frozen primary tests

### A. Exact regression through horizon 3

Across all 256 rules × 127 canonical binary block-3 targets, reproduce Research031 exactly:

- the same horizon-0/1/2 relations;
- exactly four horizon-3 pair/target births;
- exactly the rules `{35,49,59,115}` and their frozen target/pair cases.

Any mismatch invalidates the symbolic implementation.

### B. Reproduce the exploratory horizon-4 null result

Run all 256 rules through horizon 4 and confirm or reject the pilot result of zero new horizon-4 births. This is a reproducibility control, not fresh confirmation.

### C. Fresh horizon-5 test

Rules `64..255` have not been inspected at horizon 5 before this protocol was frozen.

Primary fresh question:

> **Does any pair/target distinction first appear at horizon 5 among Rules 64–255?**

A single exact event passes the “deeper witness exists” branch and freezes that event immediately for audit.

If the count is zero, record the zero without extrapolating to all horizons.

### D. Fresh horizon-6 test

If and only if the fresh horizon-5 test is zero, evaluate horizon 6 adaptively for **all 256 rules**. No horizon-6 outcome has been inspected before this freeze.

Again, a single new event stops interpretation and triggers witness audit.

### E. Optional deeper continuation

If horizon 6 is also empty, horizons 7 and 8 may be attempted only under a frozen symbolic-state resource ceiling. A budget exceedance is reported as **censored**, never as evidence of no witness.

Default per-rule MDD node ceiling:

\[
5,000,000.
\]

Do not alter the ceiling after seeing which rule hits it.

## State-growth measurements

For every constructed `(rule,horizon)` record:

- reduced MDD node count;
- build time;
- number of memoized symbolic apply states;
- number of synchronized paired-MDD states visited by witness queries;
- unresolved pair/target count after the horizon;
- newly born distinction count.

Report distributions by horizon and the worst rules descriptively.

Do not equate MDD size with intrinsic dynamical complexity; it is representation- and variable-order-dependent.

## Witness extraction

For any newly born distinction at horizon `h>=4`, the production MDD must save:

- ECA rule;
- target;
- input pair;
- changed axis;
- one explicit `2h+1`-symbol context word for each side;
- resulting macro output pair;
- binary target values.

Replay that context under the original fine ECA for `3h` fine ticks.

## Independent audit

For any newly born horizon-5+ event, use an independently written constraint/SAT or scalar symbolic implementation that does **not** import the production MDD reduction/apply code. It must verify:

1. no witness exists at all earlier horizons claimed absent;
2. the saved witness works at the claimed horizon;
3. fine-ECA replay matches the macro output.

If no horizon-5/6 births occur, independently audit the MDD against the explicit Research031 brute-force calculation through horizon 3 plus selected direct evaluations of `F_4` on random and adversarial contexts.

## Relation to de Bruijn / automata methods

De Bruijn graphs, pair graphs, preimage automata, symbolic traces, and finite-state distinguishability are established cellular-automata machinery. Research032 does not claim novelty for those ideas or for reduced decision diagrams.

The project-specific object remains:

> **the shortest causal depth at which a chosen lossy target can witness an erased local distinction, and its separation from hidden-mode lifetime and global predictive memory.**

The MDD is an exact computational instrument for that object.

## Scope and nonclaims

- The committed search concerns the matched block-3/cadence-3 ECA-induced macro family.
- A finite null search through horizon `H` does not certify `w_T(a,b)=infinity`.
- Reduced-MDD size depends on variable ordering and is not a universal invariant.
- No universal finite-state bound is assumed for arbitrary cellular automata.
- The 3D hypothesis remains parked.

## Decision rule

- If a horizon-5 or horizon-6 birth exists, stop the broad sweep and characterize the minimal new witness mechanism before searching deeper.
- If no new birth appears through horizon 6, analyze why horizon 4–6 are empty despite unresolved permanent-looking equivalences, and attempt a finite-state invariant / recurrence certificate before spending heavily on horizon 7+.
- If symbolic state growth itself becomes the limiting object, preserve that result rather than silently changing algorithms or budgets.
