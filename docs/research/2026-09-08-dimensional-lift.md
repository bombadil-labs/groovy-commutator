# A dimensional rule encoding, its symmetry, and what does not yet close

The same addressing algorithm can interpret a lower-dimensional rule inside a
higher-dimensional neighborhood. For binary outer-totalistic rules, the storage
fits exactly in every positive dimension. We can also prove a symmetry of the
resulting evolving system: complementing all bits and reflecting all spatial
coordinates commutes with its update.

These are precise starting points for the user's proposed dimension-transverse
lineages. They do not yet define a recursively closed family, a change-of-scale
map, or a Class-IV criterion. In particular, the interpreter's symmetry holds
on trivial configurations too. This note separates the exact construction,
its obstructions, and the proposed research target.

## Evidence and scope

The initial [verification script](../../scripts/verify_dimensional_lift.py) was
[committed before execution](https://github.com/bombadil-labs/groovy-commutator/commit/bfc32cfa38bed44f7fbd9a1a17c41f7cb2316cb0).
A context-transport identity was added as a deductive follow-up after that
initial audit. The symmetry and obstruction arguments were derived first; this is a deductive
verification, not a class-label sweep. [Saved results](../../results/dimensional_lift_20260908_checks.json)
include parameters, source hash, the admitted ECA rules, and a commutator witness.
Run `python scripts/verify_dimensional_lift.py` from the repository root.

The proof below holds for every positive lower dimension $d$. Computational
checks cover every 2D local patch for $d=1$, an affine basis covering all 3D
local patches for $d=2$, and 200 seeded local samples each for $d=3,4$.
The derivative/commutator census is exhaustive only on a 3×3 periodic 2D grid.
It uses a different interpreter from the previous
[eight-output spatial selector](2026-09-08-shared-state-rule.md).

## The exact storage fit

Write $M=3^d$. A binary radius-one Moore neighborhood in dimension $d$ has $M$
cells, including its center. An outer-totalistic rule depends on center bit
$c$ and the count $n$ of live outer neighbors. There are $M$ possible counts,
so its table has $2M$ output bits $r_{c,n}$.

A $(d+1)$-dimensional radius-one neighborhood has three parallel layers, each
containing $M$ cells. Its two outer layers hold the $2M$ rule bits; its central
layer holds the $M$ input bits. This is an exact bijection between one local
rule/input pair and one full higher-dimensional patch, once coordinates are fixed.
A rule alone specifies only the two outer layers, not a complete configuration.

| Lower dimension | Unrestricted table bits | Outer-totalistic table bits | Two adjacent layers |
| --- | --- | --- | --- |
| 1 | 8 | 6 | 3 + 3 |
| 2 | 512 | 18 | 9 + 9 |
| 3 | 134,217,728 | 54 | 27 + 27 |

This restricts the represented rule family. In 1D, outer-totalistic means
invariance under exchanging left and right while preserving the center; it
admits 64 of the 256 elementary rules.

## The interpreter is an explicit higher-dimensional CA

Represent count $n\in\{0,\ldots,M-1\}$ with $d$ ternary digits and subtract one
from each digit to obtain $a_d(n)\in\{-1,0,1\}^d$. Choose a transverse direction
and an order for the remaining axes. Let $\sigma(c)=2c-1$.

For a higher-dimensional binary field $X$, let $c=X(x)$ and let $n$ count live
outer neighbors of $x$ in its central $d$-dimensional layer. Define:

$$
\Phi_{d+1}(X)(x)=X\bigl(x+(\sigma(c),a_d(n))\bigr).
$$

All sites update simultaneously. This law reads an instruction bit from an
adjacent layer. The same construction works for every $d$, but its coordinates
remain a declared convention. Ternary carries do not preserve every geometric
adjacency; choosing an axis order is not an isotropy theorem.

The shape of the algorithm is dimension-independent. It does not follow that
one dimension's full dynamics is a projection of the next dimension's dynamics.

## A symmetry in every dimension

Let $J$ reflect every spatial coordinate, $JX(x)=X(-x)$, and let $C$ complement
all bits. Define $H=CJ$. The exact identity is:

$$
\Phi_{d+1}H=H\Phi_{d+1}.
$$

The statement is equivariance: evolution respects this transformation. It is
not yet equality of a scalar invariant across different dimensions.

To prove it, complementing changes the center to $1-c$ and the outer count to
$M-1-n$. Ternary digits satisfy

$$
a_d(M-1-n)=-a_d(n),\qquad \sigma(1-c)=-\sigma(c).
$$

Reflecting reverses the selected offset as well. The transformed update reads
the complement of the original selected bit at the reflected site. That is
exactly $H\Phi_{d+1}(X)$. The proof applies on infinite lattices and periodic
rectangular grids. A reflection about another lattice center works by translation
symmetry as well.

This is a property of the fixed interpreter on all configurations. It cannot
by itself distinguish a special dynamical class. Uniform zero and uniform one
are fixed configurations and also satisfy the symmetry relationship.

## Changes and states have different symmetry actions

Write $F=\Phi_{d+1}$ for the complete update map and define

$$
D(X)=X\oplus F(X),\qquad G(X)=D(F(X))\oplus F(D(X)).
$$

Although states transform by $H=CJ$, their change masks obey

$$
D(HX)=J D(X).
$$

The two complements cancel in the XOR. A relation between two complemented
states therefore reflects without complementing. Sharing the bit space does
not make the two transformation actions identical.

For the usual Groovy Commutator, direct substitution gives:

$$
G(HX)\oplus JG(X)
=F(JD(X))\oplus JF(D(X)).
$$

This is a precise expression for the obstruction to that proposed covariance of
$G$. The right-hand side measures applying the state update to a reflected
change versus reflecting the updated change. It need not vanish: $F$ respects
$CJ$ but need not respect $J$ alone.

On the complete 3×3 periodic 2D system for the $d=1$ interpreter, the evolution
symmetry and derivative covariance hold on all 512 states. The commutator
covariance fails on 504. With row-major bit positions, least significant first,
one independently reproducible witness is:

| Quantity | Integer encoding |
| --- | ---: |
| $X$ | 1 |
| $F(X)$ | 16 |
| $D(X)$ | 17 |
| $G(X)$ | 24 |
| $HX$ | 255 |
| $G(HX)$ | 144 |
| $JG(X)$ | 48 |
| $G(HX)\oplus JG(X)$ | 160 |

This neither invalidates $G$ nor proves a general theory of relational loss.
It identifies exactly where treating a change as an ordinary state conflicts
with this particular symmetry. A symmetry-respecting rule for evolving changes
is a separate object to define and test, with consequences for the feedback law.

## Retaining the base state gives a different transport

A deductive follow-up defines the evolution of a change $\delta$ relative to
its base state $X$:

$$
T_X(\delta)=F(X)\oplus F(X\oplus\delta).
$$

This compares the evolved base and perturbed states. It uses their present
relationship; it does not require a recorded time history. For the symmetry
above, $T_{HX}(J\delta)=J T_X(\delta)$. The finite verifier checks every one
of the 262,144 base/change pairs on the 3×3 system.

For the particular change $\delta=D(X)$, a direct identity holds for **any**
binary update map $F$:

$$
T_X(D(X))=F(X)\oplus F(F(X))=D(F(X)).
$$

That identity is also checked at all 512 finite states. The usual Groovy
Commutator can consequently be written as

$$
G(X)=T_X(D(X))\oplus F(D(X)).
$$

It measures the difference between transporting the change with its base state
and evolving the change pattern as an ordinary state. The zero discrepancy for
context-retaining transport is built into its definition; it is not a selective
property of Class IV. A useful razor would need an additional requirement, such
as a declared bound on the context needed to reproduce that transport. That
requirement has not yet been designed or tested.

## Two obstructions to an automatic dimensional ladder

First, the higher-dimensional interpreter generally lies outside the
outer-totalistic family used to encode its input rules. Hold its center and
central layer at zero. Put one live bit at the selected count-zero position of
the lower layer: the output is one. Move that live bit to another position of
the same layer: the output is zero. Both patches have the same center and the
same total outer population. Therefore the higher-dimensional rule is not
outer-totalistic. This counterexample works for every $d\ge1$.

Second, neighboring encodings overlap. Suppose every anchor in one central
layer must read the same complete table from an adjacent layer, using the same
fixed offsets. For each offset $u$, the condition $X(x+u)=r_u$ holds at every
anchor $x$. Translations then force that entire adjacent layer to be constant,
and all entries $r_u$ to agree. Thus this direct, unblocked representation of a
uniform rule only supplies two constant tables, giving four center-only update
rules. Exhausting all 512 3×3 periodic face patterns leaves only the all-zero
and all-one faces, as predicted.

This is an obstruction for that specific one-layer-per-table architecture.
Blocks, multiple channels, varying local programs, or staged updates may allow
other encodings. A proof that a table fits in one patch is not a proof that all
patches can carry it consistently or that the program persists while evolving.

## The proposed Class-IV connection

The user supplied a parallel-session proposal: recoverable nonclosure or
persistence under exchanging rule, state, scale, and dimension might be enriched
among independently classified Class-IV systems. We preserve this as a proposed
hypothesis. No enrichment, structural characterization, or universality result
has been established here.

Three distinctions matter before choosing a score:

- An encode/decode identity can hold by construction for every admitted rule.
  The criterion must include intervening evolution and a nontrivial invariant
  or decoding constraint chosen in advance.
- The outer-totalistic domain admits **54 and 90**, but excludes **30, 106,
  and 110**. Exclusion is not a low persistence score. A test involving the
  proposed full comparison requires a broader representation. The script checks
  all 256 elementary rules and saves the complete 64-rule admitted set.
- The earlier [history-repair results](2026-09-07-history-repairability.md) are
  observation-dependent and also include strong repair for Rule 30. They do
  not independently identify Class IV. A fully observed deterministic CA also
  closes on its complete present state; nonclosure must specify the view.

The old class-label discrepancy and disputed assignments remain relevant.
Freeze the formal construction and scoring rule without fitting them to known
class exemplars, then compare with a documented label source, retaining disputes
and grouping equivalent rules. We already know familiar examples, so “blind”
means withholding labels from score design and evaluation code, not claiming
we can erase that knowledge. A correlation would be evidence for a bounded
association; exact classification and computational universality require further
arguments.

## A concrete next target

Define complete configuration spaces and explicit spatial encodings, with
compatibility of overlapping patches. For a fixed nonconstant decoding $P$,
predeclared update laws $T_d,T_{d+1}$, cadence $k$, and a nontrivial family $M$,
ask for

$$
P T_{d+1}^{k}(X)=T_d P(X)\quad\text{for every }X\in M,
$$

with $T_{d+1}^{k}(M)\subseteq M$. The lower state may include a represented rule
field if that is part of the declared model. Fix representation budgets and
exclude a constant decoder; choosing $P$ or $T_d$ after seeing each trajectory
would make the test too easy to satisfy.

This is the next dimensional-compatibility problem, ahead of the earlier
Gray-code trajectory comparison. The wider resonance hypothesis asks whether
feeding a mismatch back can generate or sustain such families. That feedback
law, its action on changes, and any branching must be specified explicitly.
We now have one symmetry and two closure obstructions against which to test it.
