# A symbolic light cone finds a desert after the third step

Research031 found the first causal-witness horizon that the four-block torus had hidden: four symmetry-related block-symbol distinctions are invisible through macro-horizon 2 and become target-visible for the first time at horizon 3.

The obvious next experiment would have been to enumerate larger and larger light cones.

That is the wrong scaling law.

For the matched block-3 ECA system, an explicit horizon-`h` search ranges over

\[
8^{2h+1}
\]

dependency words. Horizon 6 would mean more than \(5\times 10^{11}\) words for each local rule.

Research032 replaces those explicit words with an exact symbolic automaton. The resulting search reproduces every Research031 witness, reaches horizon 6 over the full ECA-derived macro family, and finds a striking gap:

\[
\boxed{\text{no new causal-witness births at horizons }4,5,\text{ or }6.}
\]

This does **not** prove that horizon 3 is maximal. It does something more useful methodologically: it separates three kinds of unresolved distinction.

1. distinctions with a finite witness already found;
2. distinctions with an exact all-time algebraic certificate of invisibility;
3. distinctions that remain unresolved and need a stronger reachability-aware invariant.

The symbolic search turns the last category from an exponential context ocean into a finite research target.

## Exact symbolic instrument

For every ECA rule, Research031 constructs the exact radius-1 macro rule

\[
g:A^3\to A,
\qquad A=\{0,\ldots,7\},
\]

where one macrostep is three fine ECA ticks on aligned three-cell blocks.

At horizon `h`, one output block is therefore a deterministic local function

\[
F_h:A^{2h+1}\to A.
\]

Instead of enumerating its \(8^{2h+1}\) inputs, Research032 represents \(F_h\) by a reduced ordered **eight-valued decision diagram**.

A node asks for one input symbol and has eight children. Two standard reductions are applied:

- a node whose eight children agree is replaced by that child;
- identical `(variable, children)` nodes are hash-consed into one node.

The macro rule is composed symbolically over these diagrams. With the variable order fixed, the resulting rooted DAG represents the complete local light-cone function exactly.

The formal argument is in:

`docs/research/proofs/causal-witness-symbolic-automaton.md`.

Reduced decision diagrams and symbolic automata are standard machinery. The research object here is not the data structure itself but the **shortest target-relative causal witness horizon of an erased local distinction**.

## Exact same-context witness queries

A causal witness must compare two worlds with the **same surrounding context** and only one changed local symbol.

For a candidate pair `a,b` and one input axis `k`, restrict the symbolic function twice:

\[
x_k=a,
\qquad
x_k=b.
\]

Then traverse the two restricted DAGs synchronously, assigning every remaining variable identically on both sides.

The reachable leaf pairs

\[
(u,v)\in A^2
\]

are exactly the output pairs obtainable from contexts that differ only by `a` versus `b` at that axis.

A binary target `T` witnesses the distinction at that horizon iff some reachable leaf pair satisfies

\[
T(u)\ne T(v).
\]

OR-ing over all `2h+1` axes gives the exact existential witness relation at horizon `h`.

This recovers the brute-force light-cone semantics without enumerating the light-cone words.

## Frozen protocol and evidence chronology

The protocol was frozen after a bounded prototype. To keep the evidence boundary explicit, the following had already been observed before the production run:

- the Rule-35 horizon-3 witness could be reproduced symbolically;
- an exploratory all-rule horizon-4 pass showed zero new births;
- an exploratory horizon-5 pass over Rules 0–63 showed zero new births.

Those observations were recorded in the protocol and treated only as reproducibility controls.

The fresh tests were:

- horizon 5 on Rules 64–255;
- conditional on a zero result, horizon 6 on all 256 rules.

The frozen production instrument also imposed a hard ceiling of **5,000,000 MDD nodes per rule/horizon**. Exceeding it was preregistered as censoring, never as evidence of no witness.

## Regression through horizon 3

Before any deeper result was accepted, the symbolic automaton had to recover Research031 exactly.

It did.

The only horizon-3 births are again:

| Rule | Target | Pair |
| ---: | --- | --- |
| 35 | `00000001` | `2-6` |
| 49 | `00000001` | `2-3` |
| 59 | `01111111` | `1-5` |
| 115 | `01111111` | `4-5` |

Thus the new instrument is anchored to the independently audited wrap-free light-cone result rather than merely agreeing with itself.

## Complete birth distribution through horizon 6

There are

\[
256\times 28\times 127
=
910,336
\]

unordered block-symbol-pair / binary-target questions in the frozen family.

The exact first-witness counts through horizon 6 are:

| First causal witness horizon | Pair/target distinctions |
| ---: | ---: |
| 0 | 458,752 |
| 1 | 396,098 |
| 2 | 2,770 |
| 3 | **4** |
| 4 | **0** |
| 5 | **0** |
| 6 | **0** |

After horizon 3,

\[
857,624
\]

pair/target distinctions have a finite witness and

\[
52,712
\]

remain unresolved.

No additional birth occurs in the next three macrosteps.

The zero at horizon 4 reproduces the pre-freeze exploratory result.

The complete horizon-5 production run also finds zero births. Its Rules 64–255 portion was fresh confirmation; Rules 0–63 reproduce the declared pilot.

The horizon-6 result was entirely fresh.

## Phase 1: exact horizon-5 symbolic census

Actions run `34371277608` executed the frozen horizon-5 workload in eight rule shards.

It passed:

- the exact four-event Research031 regression;
- zero horizon-4 births;
- zero horizon-5 births in the previously inspected Rules 0–63;
- **zero fresh horizon-5 births in Rules 64–255**;
- zero censored rules under the five-million-node ceiling.

The exact aggregate is committed at:

`results/causal_witness_automaton_h5_20260909.json`.

## Symbolic compression

The reduced automaton compresses the raw context space dramatically.

At horizon 5, an explicit dependency-word table contains

\[
8^{11}=8,589,934,592
\]

contexts.

Among the 192 rules that still required horizon-5 evaluation:

- median core decision-diagram size: **357 nodes**;
- largest core diagram: **158,077 nodes**, Rule 122;
- median query-expanded size: **761.5 nodes**;
- largest query-expanded size: **1,404,965 nodes**.

The symbolic state counts are representation- and variable-order-dependent, so they are not promoted as intrinsic complexity measures. But computationally the compression is the difference between a feasible exact census and an impossible explicit one.

## Phase 2: fresh horizon 6 and the symbolic frontier

The fresh horizon-6 run was Actions run `34371971934`.

The raw context space at this horizon would contain

\[
8^{13}=549,755,813,888
\]

words per local rule.

The symbolic run again found **zero new births** among every rule it completed.

For 186 rules that completed horizon 6:

- median core diagram: **475 nodes**;
- largest completed core diagram: **548,427 nodes**, Rule 18;
- median query-expanded size: **918 nodes**;
- largest query-expanded size: **4,833,483 nodes**.

But six rules hit the frozen five-million-node ceiling:

\[
\boxed{\{122,126,129,146,161,182\}}.
\]

Therefore the MDD phase by itself was correctly reported as a **censored null**, not a full-family null.

The exact phase-2 aggregate is:

`results/causal_witness_automaton_h6_20260909.json`.

This is an important result about the instrument itself. Deep causal-witness search can become symbolically difficult even when no new witness has yet appeared.

## An all-time congruence certificate

The censored result motivated a stronger question:

> Can some unresolved distinctions be proved invisible forever without searching another horizon?

Fix a target `T` and begin with its kernel

\[
K_T=\{(a,b):T(a)=T(b)\}.
\]

Define a descending relation refinement. A pair `(a,b)` survives one round only when substituting `a` for `b` in **any one argument** of the macro rule always produces outputs that remain related under the previous round:

\[
g(a,x,y)\;R\;g(b,x,y),
\]

\[
g(x,a,y)\;R\;g(x,b,y),
\]

\[
g(x,y,a)\;R\;g(x,y,b)
\]

for every `x,y`.

Starting from `K_T`, iterate to a fixed point.

On the finite eight-symbol alphabet this terminates. The iteration preserves equivalence, and at the fixed point the relation is a target-respecting congruence of the macro rule.

### Infinity theorem

If

\[
a\,R_\infty\,b,
\]

then two configurations differing only by `a` versus `b` are componentwise `R_\infty`-equivalent initially. Congruence compatibility preserves componentwise equivalence under every macrostep, while `R_\infty` refines the target kernel.

Therefore their complete target spacetime fields agree:

\[
\boxed{
a\,R_\infty\,b
\Longrightarrow
w_T(a,b)=\infty.
}
\]

This is a sufficient certificate, not a necessary characterization. It quantifies over arbitrary related local contexts, including some contexts that may never arise dynamically from a single defect.

## Most unresolved distinctions are already provably permanent

The exact congruence census gives:

\[
\boxed{47,352}
\]

permanently invisible pair/target distinctions among the 52,712 still unresolved after horizon 5.

That is

\[
\boxed{89.8315\%}.
\]

Only

\[
\boxed{5,360}
\]

unresolved distinctions remain outside this simple all-time certificate.

The fixed-point refinement takes at most four rounds anywhere in the complete family.

The exact artifact is:

`results/causal_witness_congruence_20260909.json`.

This changes the interpretation of the 52,712 unresolved cases. Most are not merely “we have not searched deeply enough.” They are **proved never to have a causal witness**.

## Recovering the six MDD-censored rules

The congruence certificate completely resolves four of the six rules censored by the horizon-6 MDD:

| Rule | h=5 unresolved | Congruence-certified |
| ---: | ---: | ---: |
| 126 | 21 | 21 |
| 129 | 21 | 21 |
| 146 | 21 | 21 |
| 182 | 21 | 21 |

Those rules cannot contain a horizon-6 birth.

Only Rules 122 and 161 retained uncertified cases:

- Rule 122: six pairs, all under target `00100000`;
- Rule 161: six pairs, all under target `00000100`.

The recovery protocol froze those **12 pair/target cases** before any alternate solver was evaluated.

## Independent recovery of the h=6 null

The MDD ceiling was not raised.

Instead, the 12 frozen cases were encoded directly at the original fine-ECA level.

A horizon-6 macro witness has:

- 13 initial block symbols;
- 39 initial fine cells;
- 18 fine ECA ticks;
- one final three-cell output block.

For each pair/target case and each of the 13 possible changed-block positions, two fine causal cones were constrained equal everywhere except the changed block, and the final target bits were required to differ.

That gives

\[
12\times13=156
\]

exact axis queries.

Two independent encodings were used:

1. Z3 over paired shrinking fine-ECA cones;
2. a hand-built CNF solved by Minisat22 through PySAT.

They agree **axis by axis**.

Both report:

\[
\boxed{12/12\text{ cases UNSAT at horizon 6}.}
\]

No horizon-6 witness exists in the MDD-censored remainder.

The exact outputs are committed as:

- `results/causal_witness_h6_z3_20260909.json`;
- `results/causal_witness_h6_pysat_20260909.json`.

Combined with the 250 rules settled directly by MDD or congruence, this recovers the complete full-family horizon-6 null.

## What the “desert” means

The observed finite witness spectrum currently has a peculiar shape:

\[
0,\;1,\;2,\;3,\;\underbrace{\varnothing,\varnothing,\varnothing}_{4,5,6}.
\]

Research031 taught us not to turn a finite search horizon into a universal maximum. So Research032 **does not** claim:

\[
w_T(a,b)\le3\text{ or }\infty.
\]

There are still 5,360 pair/target distinctions that:

- have no witness through horizon 6;
- are not covered by the simple target-congruence certificate.

Some may have witness horizon 7 or later. Some may be permanently invisible for subtler dynamical reasons.

The gap is therefore a new research object, not a theorem of absence.

## A useful hierarchy of evidence

Research032 gives a clearer classification for a local erased distinction:

### Finite witness

An explicit context establishes

\[
w_T(a,b)=h.
\]

### Algebraically permanent

A target-respecting macro-rule congruence establishes

\[
w_T(a,b)=\infty.
\]

### Dynamically unresolved

No witness has been found through the searched horizon, but the algebraic congruence is too strong to certify infinity.

The third category is now only 5,360 cases in the complete family.

That is the correct next target.

## Relation to the broader program

The research now separates four different questions that were initially easy to conflate:

1. **hidden-mode lifetime:** how long a particular erased difference stays hidden in one context;
2. **causal witness horizon:** how deep some context must be before it can expose a local distinction;
3. **representation discovery time:** when the complete local vocabulary of distinctions has been learned on a specified context domain;
4. **global state-resolution depth:** how much observed history identifies the global predictive state.

Research032 adds a fifth axis:

5. **symbolic proof complexity:** how difficult it is to represent or certify the relevant context space exactly.

Those quantities need not track one another.

## What is exact now

For the declared ECA / block-size-3 / cadence-3 / 127-target family:

- the reduced MDD implements the same causal-witness relation as the exhaustive Research031 light-cone search through horizon 3;
- exactly four pair/target distinctions are first witnessed at horizon 3;
- no new pair/target distinction is first witnessed at horizons 4, 5, or 6;
- the horizon-5 result is complete with no MDD censoring;
- the fresh horizon-6 MDD pass censors six rules at the frozen five-million-node ceiling;
- four censored rules are completely discharged by an exact all-time congruence certificate;
- the remaining 12 h=6 cases are independently UNSAT in Z3 and Minisat22 on all 156 changed-block axes;
- 47,352 of 52,712 h=5-unresolved distinctions have exact `w=infinity` congruence certificates;
- 5,360 remain unresolved through h=6 without that certificate.

## What remains open

- Horizon 7+ has **not** been searched.
- The 5,360 non-congruence unresolved distinctions are not known to be finite-witness or permanently invisible.
- The MDD node count is sensitive to variable ordering and representation choice.
- The target-congruence relation is sufficient but may be strictly smaller than true permanent causal equivalence because it permits dynamically unreachable related contexts.
- Nothing here establishes a universal witness-horizon bound for cellular automata.
- The result is exact for the stated matched block-3 ECA macro family.
- The 3D hypothesis remains parked.

## Next question: reachable-context invariants

The next step should **not** be “raise the node ceiling and run horizon 7.”

The congruence certificate fails on 5,360 cases because it asks for invariance under every algebraically allowed related context. But a single local defect does not generate every such context.

The right next object is therefore the **paired macro CA**

\[
\widehat g:
(A\times A)^3\to A\times A,
\]

together with the language of pair configurations reachable from:

- diagonal background pairs everywhere;
- one non-diagonal seed pair.

We want a finite-state, forward-invariant language that contains all reachable defect configurations while avoiding every target-visible pair.

If such an invariant exists, it proves `w=infinity` without demanding a full algebraic congruence. If no such invariant can contain the dynamics, its counterexample should point toward a deeper finite witness.

That is the actual de-Bruijn tunnel.

Research032 built the headlamp.
