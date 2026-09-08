# Observer search: hidden information has a lifetime

**Research checkpoint, 2026-09-08.** Research022 reframed the Groovy
Commutator as an observation-closure problem, and Research023 showed that an
instantaneously nonclosed observation can become exact after finite observed
history. This checkpoint turns the observer itself into the experimental
variable.

The main question is deliberately simple:

> **For a fixed fine rule, which lossy variables make the observed dynamics
> easiest to close?**

The first search space is exhaustive but small: every nonconstant Boolean map
from a nonoverlapping two-cell block to one bit. The result is not a universal
winner. Different observations expose different effective dynamics, and for a
particularly hard symmetry family the required macro-memory can be traced to a
literal traveling defect that the observer cannot see.

That gives a mechanistic reading of the history depth from Research023:
**macro-memory can be the lifetime of discarded but still causally active
information.**

## Exact search object

For ECA rule `A`, two-cell Boolean observer `P_h`, and matched cadence `q=2`,
define

\[
Y_t=P_h(E_A^{2t}(S)).
\]

As in Research023, let `h*` be the least nonnegative integer for which an exact
deterministic map exists,

\[
Y_{t+1}=F(Y_t,Y_{t-1},\ldots,Y_{t-h_*}),
\]

for every microstate on the finite periodic ring. `h*=0` is ordinary factor
closure.

There are 14 nonconstant Boolean maps `{0,1}^2 -> {0,1}`. They form seven
output-complement pairs. If `Q=1-P`, then the entire observed history is merely
bitwise relabeled, so `P` and `Q` have exactly the same closure defect and
memory depth. We therefore search seven canonical classes and retain both names:

| Pair id | Canonical observer | Output complement |
| ---: | --- | --- |
| 1 | NOR | OR |
| 2 | `x AND NOT y` | `x IMPLIES y` |
| 3 | `NOT y` | `y` |
| 4 | `NOT x AND y` | `y IMPLIES x` |
| 5 | `NOT x` | `x` |
| 6 | XOR | XNOR |
| 7 | NAND | AND |

The core census exhausts all 256 ECA rules at ring widths
`n=8,10,12,14,16`. The complete state spaces are enumerated; there is no fitted
predictor or error threshold.

## Finding 1: there is no universal static coarse variable

At `n=12`, **92/256 rules** admit at least one memoryless two-cell observer.
That exactly matches the 92 fine rules participating in the block-2
scale-rhyme factor atlas from Research022.

But no individual observer comes close to covering all 92. The exact
memoryless counts for each canonical class are:

| Observer | Exact rules at n=12 | Class I | Class II | Class III | Class IV |
| --- | ---: | ---: | ---: | ---: | ---: |
| NOR / OR | 37 | 11 | 26 | 0 | 0 |
| directional pair 2 | 26 | 6 | 20 | 0 | 0 |
| projection pair 3 | 28 | 8 | 12 | 8 | 0 |
| directional pair 4 | 26 | 6 | 20 | 0 | 0 |
| projection pair 5 | 28 | 8 | 12 | 8 | 0 |
| XOR / XNOR | 20 | 6 | 6 | 8 | 0 |
| NAND / AND | 37 | 11 | 26 | 0 | 0 |

The union is much larger than any one column. A macrovariable that is exact for
one dynamical law may be poor for another.

This is the first direct experimental reason not to treat "the coarse-graining"
as a fixed generic operation. Closure belongs to `(E,P,q)`, not to `E` alone
and not to `P` alone.

## Finding 2: optimizing the observer helps, but does not erase memory

Across the seven observer classes, **154/256 fine rules** have at least one
observer whose measured `h*` is unchanged at `n=12,14,16`. This is only an
empirical plateau, not an infinite-lattice theorem.

If each fine rule is allowed to choose the two-cell observer with smallest
`h*` at `n=16`, the distribution is:

| best `h*` at n=16 | Rules |
| ---: | ---: |
| 0 | 92 |
| 1 | 36 |
| 2 | 4 |
| 3 | 30 |
| 4 | 38 |
| 5 | 28 |
| 6 | 20 |
| 7 | 4 |
| 17 | 4 |

The scaling of the best-at-`n=16` observer still separates strongly by the
repository's Wolfram labels:

| Class | winner has an n=12,14,16 plateau | winner grows | other |
| --- | ---: | ---: | ---: |
| I | 16 | 8 | 0 |
| II | 122 | 70 | 0 |
| III | 12 | 12 | 2 |
| IV | 0 | **14** | 0 |

So observer search does not make the Class-IV cases memoryless. This is
especially notable beside Research023, where the **rule-dependent derivative
observer** has bounded whole-state memory on every labeled Class-IV rule over
the same size range. A fixed static block statistic and a relational observer
built from the dynamics are doing qualitatively different jobs.

That does not establish a special theorem about Wolfram classes. It does say
that "search over static block averages/statistics" is too narrow a model of
macrovariable discovery for the cases we care about most.

## Class-IV extension: four rules are exceptionally hard

The two-cell search was pushed to `n=18` for all 14 labeled Class-IV rules.
The table reports the *best observer at each size*, so the identity of `P` may
change as `n` changes.

| Rule | best `h*` at n=8,10,12,14,16 | best `h*` n=18 | n=18 canonical winner(s) |
|---:|:---|---:|:---|
| 41 | 3,3,4,6,7 | 7 | 1 |
| 54 | 3,3,3,4,4 | 7 | 3,5,6 |
| 97 | 3,3,4,6,7 | 7 | 1 |
| **106** | **3,5,13,15,17** | **49** | 2,6 |
| 107 | 3,3,4,6,7 | 7 | 7 |
| 110 | 3,3,4,4,5 | 5 | 3,5 |
| **120** | **3,5,13,15,17** | **49** | 4,6 |
| 121 | 3,3,4,6,7 | 7 | 7 |
| 124 | 3,3,4,4,5 | 5 | 3,5 |
| 137 | 3,3,4,4,5 | 5 | 3,5 |
| 147 | 3,3,3,4,4 | 7 | 3,5,6 |
| **169** | **3,5,13,15,17** | **49** | 4,6 |
| 193 | 3,3,4,4,5 | 5 | 3,5 |
| **225** | **3,5,13,15,17** | **49** | 2,6 |

The hard quartet `{106,120,169,225}` is not an arbitrary list: it is exactly
the reflection / black-white-conjugation symmetry orbit of Rule 106.

For Rule 106, block-2 parity is still exact only after

\[
h_*(18)=49,
\]

and a separate `n=20` audit gives

\[
h_*(20)=51.
\]

The jump from 17 at `n=16` to 49 at `n=18` is therefore not a one-size numerical
blip. We do **not** infer an asymptotic formula from these sizes; the sharp
change is treated as a phenomenon to explain.

## Finding 3: the memory is a traveling observer-invisible defect

The Rule-106 `n=20` parity case admits an explicit exact witness.

Consider microstates `25` and `26`, whose occupied sites are

\[
S_a=\{0,3,4\},\qquad S_b=\{1,3,4\}.
\]

They differ only by flipping the adjacent pair

\[
S_a\triangle S_b=\{0,1\}.
\]

Block-2 parity cannot see this difference because both bits of one block are
flipped together.

Under the two-microstep cadence, the difference support obeys the exact formula

\[
\delta_t=\{-2t,\,-2t+1\}\pmod {20}
\]

for every `0 <= t <= 50`.

So the hidden difference is not a diffuse statistical uncertainty. It is an
**adjacent two-bit defect translating by exactly one coarse block per macro
step**. The two trajectories have identical parity observations

\[
Y^a_t=Y^b_t
\]

for every `t=0,...,50`, even while the microscopic difference continues to move
around the ring. At `t=51` the difference changes shape from two sites to three
and the parity observations finally split.

This pair is an ambiguity witness for history depth 50, while exhaustive
partition refinement proves `h*=51`.

That gives a concrete causal interpretation of the closure memory:

> **The macrostate must remember enough past to account for hidden distinctions
> that are still propagating and can later re-enter the observer's visible
> variables.**

For this example, the memory timescale is literally the lifetime of a coherent
observer-invisible traveling defect before it changes shape.

This is very close in spirit to the concurrent pulse-scattering / causal-
shielding work, but it should not be conflated with it. The present witness is a
1D ECA difference field under a block observer; the strip work studies exact
organizations in the separate 2D selector law. What they share is the sharper
notion of **observer- or selector-relative causal invisibility**: a physical
difference can exist, move, and remain causally live while a chosen process or
representation does not read it.

## Spatial locality is a separate cost

A global `h*` allows the history rule to inspect the whole observed ring. A
small temporal depth therefore does not automatically mean a simple local
macrodynamics.

A targeted `n=16` probe of the best two-cell observers for Class IV found that,
at their minimal global history depth, exact local rules generally need radius
3 or 4 on an eight-cell macro-ring. In other words, many of these "best"
static block descriptions are nearly global spatially as well as temporally
costly.

This reinforces the Research023 conclusion that temporal memory and spatial
range must remain separate coordinates of the closure profile rather than be
collapsed into one score.

## Exploratory block-3 probe: more expressive static observers help, but drift

After the block-2 census, an exploratory search examined all 127
output-complement classes of nonconstant three-cell Boolean observers for the
14 Class-IV rules at `n=9,12,15`, with cadence `q=3`.

No memoryless Class-IV factor appeared. Ten of the fourteen rules initially had
at least one fixed observer whose short-size memory appeared to plateau. A
selected `n=18` follow-up broke those fixed-observer plateaus.

Rule 110 is illustrative. The simple truth table `90`, whose algebraic normal
form is

\[
P(x,y,z)=x\oplus z,
\]

ignores the center cell and remembers only the relation between the two outer
cells. It has `h*=4,4,4` at `n=9,12,15`, but rises to `6` at `n=18`. Re-searching
all three-cell observers at `n=18` finds a different optimum with `h*=5`.

The full all-observer `n=18` scan was not completed for all 14 rules, so this is
an exploratory lead rather than a Research024 asymptotic claim. The useful
message is already clear: increasing observer expressivity can reduce memory,
but the **identity of the best observer can itself depend on system size**.

## Revised picture

The project now has a hierarchy of increasingly adequate macro descriptions:

1. same-rule commutation, `P E^q = E P`;
2. memoryless factor closure, `P E^q = B P`;
3. exact finite-history closure;
4. bounded spatially local finite-history closure;
5. observer search over candidate representations;
6. potentially, representation families that are themselves relational,
   dynamical, or stateful.

The current experiment strongly argues for level 6. Static block maps can be
useful, but the derivative results show that a rule-relative relational
representation may expose a dramatically shorter effective memory than any
small static block statistic.

A more useful formulation of "coarse-graining" for Groovy may therefore be:

> **Find a representation that forgets as much micro-detail as possible while
> preserving a compact sufficient state for the future.**

The failure modes are not just scalar errors. They have dynamics of their own:
hidden distinctions can drain, propagate, orbit, collide, or later become
visible. The Groovy remainder is increasingly looking like the physics of those
hidden modes.

## Next experimental target

The strongest next step is no longer another blind observer sweep. It is a
**hidden-defect census**:

- for each `(E,P)` with nonzero memory, extract minimal pairs of microstates that
  share the same observed history but eventually split;
- evolve their difference field;
- classify whether the hidden distinction translates, expands, decays,
  collides, or changes shape;
- compare first-visible time with `h*` and spatial range;
- then ask whether augmenting `P` with the hidden defect's conserved/transported
  feature collapses the required memory.

That would turn observer search from brute-force representation selection into
**constructive discovery of missing state variables**.

## Artifacts

- `scripts/experiment_observer_search.py` — exhaustive block-2 observer census;
- generated `results/observer_search_block2_20260908.csv`;
- generated `results/observer_search_rule_summary_20260908.csv`;
- `results/observer_search_block2_20260908_summary.json`;
- `results/observer_search_classiv_n18_20260908.csv` — exact Class-IV extension;
- `scripts/check_observer_hidden_defect.py` — targeted exact Rule-106 mechanism
  audit;
- `results/observer_hidden_defect_rule106_n20_20260908.json` — compact witness summary; the checker regenerates the full trace.

All whole-state claims are exact for the stated finite periodic rings. Plateau,
growth, and "hard" language describe the tested size sequences; no infinite-
lattice memory theorem is claimed here.
