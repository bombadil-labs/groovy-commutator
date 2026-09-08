# History lift: when a lossy observation becomes a state again

**Research checkpoint, 2026-09-08.** This is a stacked continuation of
[observation closure](2026-09-08-observation-closure.md). That work separated
ordinary factor closure,

\[
P E^q = B P,
\]

from the stricter same-rule condition \(P E^q = E P\). The present experiment
asks what happens when \(P(S_t)\) is *not* a sufficient state by itself:
**can finite observed history restore exact deterministic closure?**

The answer is yes surprisingly often, but the scaling of the required memory
matters. The main new object is therefore not merely a closure defect but a
**memory spectrum attached to the triple \((E,P,q)\)**.

## Exact definition

Let

\[
Y_t=P(E^{qt}(S)).
\]

For a finite periodic ring, define \(h_*\) as the least nonnegative integer for
which there exists a deterministic map \(F_h\) satisfying

\[
Y_{t+1}=F_h(Y_t,Y_{t-1},\ldots,Y_{t-h})
\]

for every microstate and every time. Equivalently, when all microstates are
enumerated at time zero, no two microstates with the same observed word
\((Y_0,\ldots,Y_h)\) may have different \(Y_{h+1}\).

Thus:

- \(h_*=0\) is ordinary observation closure.
- \(h_*>0\) means the observation is non-Markovian as an instantaneous state,
  but becomes deterministic after state augmentation by finite history.
- Growth of \(h_*\) with ring width is evidence that the apparent closure is
  global/finite-size rather than bounded-memory local physics.

The test is exact and set-valued: no classifier, fitted probability, seed, or
error threshold enters the definition. The implementation uses partition
refinement over the complete finite state space.

We measure two observers:

1. **Derivative observation** for each fine rule \(A\):
   \(P_A(S)=D_A(S)=S\oplus E_A(S)\), with \(q=1\).
2. **Block-2 parity**: nonoverlapping pairs are XORed to one macrocell, with
   \(q=2\), matching the scale-rhyme cadence.

Both are exhaustively scanned at ring widths \(n=8,10,12,14,16\).

## Finding 1: derivative history closes every tested finite ring

For the derivative observer, every one of the 256 ECA rules has finite
\(h_*\) at every tested width. The largest value at \(n=16\) is 14.

The more important result is the scaling split:

| derivative \(h_*\) behavior over n=8,10,12,14,16 | Rules |
| --- | ---: |
| Stabilized across n=12,14,16 | 192 |
| Monotone growing | 56 |
| Small nonmonotone / ring-arithmetic variation | 8 |

The 30 memoryless rules at \(n=12\) exactly reproduce the 30 exact derivative
closures from the parent observation-closure experiment. History therefore
extends that result rather than changing its meaning.

Representative memory-depth sequences:

| Rule | Wolfram class | derivative \(h_*\) at n=8,10,12,14,16 | reading |
| ---: | :---: | :--- | :--- |
| 30 | III | 1, 1, 1, 1, 1 | bounded one-step memory |
| 41 | IV | 1, 1, 1, 1, 1 | bounded one-step memory |
| 54 | IV | 2, 2, 2, 2, 2 | bounded two-step memory |
| 106 | IV* | 1, 1, 1, 1, 1 | bounded one-step memory |
| 110 | IV | 1, 1, 1, 1, 1 | bounded one-step memory |
| 184 | II | 3, 4, 5, 6, 7 | approximately \(n/2-1\) |
| 28 | II | 5, 7, 9, 11, 13 | \(n-3\) on tested sizes |
| 78 | II | 4, 6, 8, 10, 12 | \(n-4\) on tested sizes |
| 136 | I | 6, 8, 10, 12, 14 | \(n-2\) on tested sizes |

`IV*` retains the repository's full-table label; prior notes record the
literature dispute over Rule 106 on periodic rings.

This distinction is crucial. Saying “all finite rings eventually close with
history” would hide two different mechanisms:

- **bounded causal memory**: a fixed amount of observed past appears sufficient
  as the system grows;
- **extensive memory**: the required past grows with system size and behaves
  more like global reconstruction than a finite macro state variable.

A natural future statistic is a memory-density or scaling exponent such as
\(\limsup h_*(n)/n\), but five ring widths are not enough to estimate an
asymptotic limit.

## Finding 2: complexity class is not the memory class

For the derivative observer, the scaling split by the repository's full
Wolfram labels is:

| Class | stabilized last 3 | monotone growing | nonmonotone |
| --- | ---: | ---: | ---: |
| I | 16 | 8 | 0 |
| II | 138 | 48 | 6 |
| III | 24 | 0 | 2 |
| IV | 14 | 0 | 0 |

Every labeled Class-IV rule is empirically stabilized by \(n=12\), and no
Class-III rule shows monotone growth in this scan. The obviously extensive
examples are Class I/II. This is the reverse of a naive “more complex fine
rule requires more macro memory” hypothesis.

It should not be promoted into a Class-IV detector: the stabilized set is much
larger than Class IV, symmetry relatives are not independent replications,
and the result changes sharply when the observer changes.

## Finding 3: changing the observer changes the memory physics

Block-2 parity gives a very different scaling census:

| block-2 parity \(h_*\) behavior | Rules |
| --- | ---: |
| Stabilized across n=12,14,16 | 100 |
| Monotone growing | 148 |
| Nonmonotone / ring-arithmetic variation | 8 |

All 256 tested finite rings still close within the deeper bound \(h\le n+4\),
but most no longer look bounded over these sizes. All 14 Class-IV rules are in
the monotone-growing group for this observer.

The cleanest demonstration that memory belongs to \((E,P,q)\), not to \(E\)
alone, is Rule 106:

\[
\begin{array}{c|ccccc}
n & 8 & 10 & 12 & 14 & 16\\\hline
D_{106} & 1 & 1 & 1 & 1 & 1\\
\text{block-2 parity} & 3 & 5 & 13 & 15 & 17
\end{array}
\]

The same fine dynamics is bounded-memory under one observation and nearly
system-sized-memory under another.

Other contrasts go the other direction. Rule 184's derivative memory grows
3,4,5,6,7, while block-2 parity needs only 2,3,3,4,4. A coarser observer can
therefore require *less* history than a higher-resolution relational observer.

Rule 90 remains the crystalline control: both derivative and dyadic parity are
memoryless at every tested size, consistent with its exact factor identities.

## Finding 4: global history closure need not be spatially local

Whole-state \(h_*\) allows \(F_h\) to inspect the entire observed ring. To ask
whether history restores a *local* effective law, we also tested next observed
bits using radius-r neighborhoods across the observed history.

At \(n=12\), restricting to history depths \(h\le6\):

| exact derivative closure within h<=6 | rules |
| --- | ---: |
| global whole-state history | 226 |
| local radius 1 history | 180 |
| local radius 2 history | 218 |
| local radius 3 history | 222 |
| local radius 4 history | 226 |

So temporal memory and spatial range trade off. Every global derivative closure
visible by depth 6 can be represented by radius 4 or less on the 12-cell ring,
but radius 1 is insufficient for 46 of them.

Examples among complex rules:

| Rule | global \(h_*\) | r=1, h<=6 | r=2 | r=3 | r=4 |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 30 | 1 | unresolved | 4 | 2 | 2 |
| 41 | 1 | unresolved | 5 | 3 | 2 |
| 54 | 2 | unresolved | 2 | 2 | 2 |
| 106 | 1 | unresolved | 4 | 2 | 2 |
| 110 | 1 | unresolved | 5 | 4 | 3 |
| 184 | 5 at n=12 | 5 | 5 | 5 | 5 |

Thus “finite-memory closure” is not synonymous with “a small-radius CA with
memory.” A useful generalized closure profile needs both temporal depth and
spatial range.

## Matched-target control: history really contributes information

A separate exact control fixes the target transition at \(Y_6\to Y_7\) on the
12-cell derivative system, then reveals older observations behind \(Y_6\).
This avoids crediting history merely because a deeper-history test predicts a
later, more collapsed state.

With history depth at most 6:

- 106 rules are already closed from \(Y_6\) alone;
- 120 are nonclosed at \(Y_6\) but become exactly deterministic when older
  observed states are supplied;
- 30 remain unresolved within this depth.

So the large repair effect is not only a moving-target artifact. Past observed
states genuinely distinguish microstate fibers that the current observation
merges and that later matter again.

## Interpretation: coarse-graining creates memory

The parent experiment reframed the Groovy Commutator as a closure question:
when does information discarded by \(P\) come back to affect the future?
This experiment adds the next layer:

> **When instantaneous coarse variables are not a sufficient state, their path
> can be. Coarse-graining generally turns Markovian microdynamics into
> non-Markovian observed dynamics.**

That makes history augmentation a kind of conditional fine-graining. It does
not reconstruct every lost micro detail; it restores exactly the distinctions
among hidden states that matter for future observed evolution.

This suggests a hierarchy:

1. **same-rule closure:** \(P E^q = E P\);
2. **memoryless factor closure:** \(P E^q = B P\);
3. **finite-memory closure:** \(Y_{t+1}=F(Y_t,\ldots,Y_{t-h})\);
4. **local finite-memory closure:** the same with bounded spatial radius;
5. **extensive-memory closure:** exact only when memory/range grows with system
   size;
6. **persistent nonclosure:** if any examples survive larger-size/deeper tests.

The experiments here strongly populate levels 2–5. They do not yet establish
an infinite-lattice example of level 6.

A compact candidate for the generalized Groovy object is therefore a
**closure profile** of an observation:

\[
\Gamma(E,P,q;n)=\bigl(\Delta_0,\ h_*(n),\ r_*(n;h),\ \text{same-rule?}\bigr),
\]

with the structured remainder field retained rather than reduced only to
scalar entropy. The original commutator is one distinguished slice of this
larger profile.

## What to pull next

Three directions now look especially fertile:

1. **Observer search.** Exhaust all 14 nonconstant block-2 maps (then selected
   block-3 maps) and ask which observations minimize closure defect, memory
   scaling, and spatial range for each fine rule. This turns coarse-graining
   into a search for sufficient macro variables rather than a fixed projection.
2. **Causal-window proofs for bounded cases.** Rules 30, 41, 54, 106, and 110
   have tiny derivative \(h_*\) across all tested sizes. Their exact identities
   may admit finite local proofs, separating true bounded-memory factors from
   finite-ring evidence.
3. **Connect memory to defect transport.** The concurrently developed pulse
   scattering / causal shielding work studies how remainder information moves.
   The obvious question is whether extensive \(h_*\) corresponds to a defect
   that must physically traverse the ring before the observation becomes
   sufficient.

## Artifacts

- `scripts/experiment_history_lift_closure.py`
- generated `results/history_lift_derivative_scaling_20260908.csv`
- generated `results/history_lift_block2_parity_scaling_20260908.csv`
- generated `results/history_lift_derivative_locality_20260908.csv`
- generated `results/history_lift_derivative_matched_target_20260908.csv`
- `results/history_lift_closure_20260908_summary.json`

All reported finite-ring claims are exhaustive over the corresponding state
spaces. The asymptotic language (bounded, extensive, parity-sensitive) is an
empirical description of the tested size sequence, not a theorem about the
infinite lattice.
