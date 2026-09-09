# Protocol: fiber residence and causal visibility — 2026-09-08

**Status:** frozen before the full census.  
**Branch:** `research/fiber-visibility-20260908`

## Motivation

Research022–024 reframed the Groovy Commutator as a question about lossy representations. Research023 measured the history depth needed to restore exact closure, and Research024 exhibited a Rule-106 defect that remains invisible to block-2 parity for 50 macrosteps before re-entering the observed variables at step 51.

Concurrent selector-shielding work supplies the complementary idea: a physical difference can remain nearby yet be dynamically unread by the continuing process. This protocol asks for an observer-independent finite-state version of that distinction.

## Definitions

Fix deterministic dynamics `E`, cadence `q`, and an observation `P`. Write

\[
Y_t(s)=P(E^{qt}(s)).
\]

For two microstates define the **first visibility time**

\[
\tau_P(s,s')=\min\{t\ge 0:Y_t(s)\ne Y_t(s')\},
\]

with `tau=infinity` when their observed trajectories are identical forever.

For each `t`, let `K_t` be the unordered pairs with identical observed histories through time `t`,

\[
K_t=\{\{s,s'\}:Y_j(s)=Y_j(s')\ \text{for}\ 0\le j\le t\}.
\]

Let

\[
R_t=|K_t|.
\]

Then `R_t-R_(t+1)` is exactly the number of initially conflated pairs whose first visibility time is `t+1`. On a finite deterministic state space the sequence stabilizes. Its limit

\[
R_\infty
\]

counts **permanently observationally equivalent pairs**.

We distinguish:

- **latent pairs:** finite positive first visibility time;
- **permanently hidden pairs:** `tau=infinity`;
- among permanently hidden pairs, **drained/coalescent** pairs whose microtrajectories eventually become equal;
- **persistent shielded** pairs whose microtrajectories remain distinct on the eventual joint orbit while their observations remain identical.

The exact finite-history depth `h*` from Research023 is predicted to equal the largest finite first-visibility time whenever any pair eventually becomes visible.

## Primary census A: static block-2 observers

For every elementary CA rule `A in 0..255`, use matched cadence `q=2` and each of the seven canonical output-complement classes of nonconstant two-cell Boolean observations from Research024:

`NOR`, `x AND NOT y`, `NOT y`, `NOT x AND y`, `NOT x`, `XOR`, `NAND`.

Exhaust the complete periodic state space at ring width `n=12`.

For every `(A,P)` record:

- initial hidden pair count `R_0`;
- permanent hidden pair count `R_infinity`;
- eventually visible pair count `R_0-R_infinity`;
- fraction of initially hidden pairs that ever become visible;
- the complete first-visibility histogram;
- maximum finite first-visibility time;
- `h*` from the same partition refinement;
- whether the residence partition stabilizes immediately (`h*=0`).

Controls:

1. the `h*` values must reproduce the Research024 block-2 atlas at `n=12`;
2. the 92 rules with at least one memoryless block-2 observer must reproduce the Research024/scale-rhyme domain;
3. when `h*=0`, no initially hidden pair may later become visible (`R_0=R_infinity`).

## Primary census B: rule-relative derivative observer

For every ECA rule at `n=12`, use

\[
P_A(S)=S\oplus E_A(S),\qquad q=1.
\]

Record the same residence statistics. The derivative `h*` distribution must reproduce Research023.

This compares a static block statistic with a relational observation built from the dynamics itself.

## Targeted mechanism controls

### Latent control: Rule 106 / block-2 parity

At `n=20`, `q=2`, reproduce the Research024 exact result `h*=51` and witness microstates `25` and `26`. Their observations must agree through macro time 50 and split at 51 while the microscopic difference remains an adjacent two-site translating defect through time 50.

### Persistent-shield control: Rule 90 / block-2 parity

At `n=20`, compare microstates `0` and `3`. Block-2 parity must remain equal for all time by the exact Rule-90 factor relation. Independently iterate the finite joint state until repeat and require:

- the two microstates never coalesce before the joint repeat;
- the difference remains nonempty;
- the joint orbit repeats with nonzero difference.

This is the finite-state analogue of information that remains physically present but permanently outside the chosen observation.

## Secondary witness search

After the primary census is frozen, search selected `(E,P)` pairs for minimal-Hamming representatives of permanently hidden classes and classify their joint finite-state fate as coalescent or persistent-shielded. This is exploratory unless separately frozen.

## Nonclaims

- `tau=infinity` means forever on the stated finite periodic system, not on the infinite lattice.
- Persistent observational equivalence need not arise from the same selector mechanism as the concurrent 2D shielding work.
- Pair counts depend on the uniform finite-state ensemble and are not claimed as asymptotic measures.
- The census studies whether discarded distinctions return to the chosen observation, not whether they are physically unimportant to every possible observable.
