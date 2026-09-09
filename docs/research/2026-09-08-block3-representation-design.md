# Predictive synergy breaks greedy repair

Research027 found a remarkably clean constructive result: on the complete two-cell local partition lattice, greedily adding the distinction that removes the most unresolved future information per added bit found the globally cheapest exact closure repair in every one of 1,590 nonclosed cases.

Research028 deliberately makes the representation space large enough for that result to fail.

The failure is rare—only four cases out of 30,856 nonclosed block-3 targets—but exact. More importantly, the first counterexample reveals a concrete mechanism:

> **A distinction can be necessary for the cheapest predictive representation even when it has zero predictive value by itself.**

The distinction becomes valuable only in combination with another distinction. That predictive synergy is the first exact obstruction found to a purely greedy representation calculus.

## Exact block-3 search space

A three-cell local block has eight fine patterns. Its full set-partition lattice contains

\[
B_8=4140
\]

representations, but a fixed binary target `T=A|B` only permits refinements that partition `A` and `B` separately. Therefore

\[
[T,\mathrm{id}]\cong\Pi(A)\times\Pi(B).
\]

The exact target-refinement intervals are only:

| target balance | canonical targets | interval size |
| --- | ---: | ---: |
| 1 / 7 | 8 | 877 |
| 2 / 6 | 28 | 406 |
| 3 / 5 | 56 | 260 |
| 4 / 4 | 35 | 225 |

This makes a complete exact comparison feasible rather than approximate.

The frozen census evaluates all 256 elementary cellular automata on the periodic `n=12` ring, all 127 canonical nonconstant binary block-3 targets, and matched cadence `q=3`. For every nonclosed target it computes every allowed local encoder refinement, the globally minimum-information exact repair, and the Research027 greedy path.

The full census ran in sixteen disjoint CI shards. Before analyzing the new result, aggregation had to reproduce the existing Research026 block-3 controls exactly: **1,656 canonical closed targets** and **141 fine rules with at least one closed target**.

## Greedy is almost universal, but not exact

There are

\[
32,512
\]

tested `(rule,target)` cases, of which

\[
30,856
\]

are nonclosed.

The greedy closure gradient reaches a globally cheapest local exact repair in

\[
\boxed{30,852/30,856=99.9870\%}
\]

of them.

But the frozen primary hypothesis was that at least one counterexample would exist. It passes:

\[
\boxed{4\text{ exact greedy failures}.}
\]

Every failure has exactly one bit of added-information regret at `n=12`.

The complete failure set is tiny:

| rule | class | target | balance | regret |
| ---: | --- | --- | ---: | ---: |
| 24 | II | `01000010` | 2 / 6 | 1 bit |
| 24 | II | `01000110` | 3 / 5 | 1 bit |
| 231 | II | `01000010` | 2 / 6 | 1 bit |
| 231 | II | `01100010` | 3 / 5 | 1 bit |

Rules 24 and 231 are state-conjugates. Under local state complementation a three-bit code `i` maps to `7-i`, so the target string is reversed: `01000110` maps to `01100010`, while `01000010` maps to itself. The four failures therefore form a conjugacy-linked family rather than a broad complex-rule pathology.

No repository-labeled Class-III or Class-IV target produces a greedy failure in this census.

## The first counterexample

The lexicographically first case is Rule 24 with target

`01000010`.

Its local target classes are

\[
\{0,2,3,4,5,7\}\mid\{1,6\}.
\]

The exact greedy repair path is

`01000010 -> 01200210 -> 01200213 -> 01200234 -> 01230245`

and costs

\[
A_{greedy}=6.754887502163468\text{ bits}.
\]

The globally cheapest closed encoder is

`01230243`

at

\[
A^*=5.754887502163468\text{ bits}.
\]

Thus

\[
\boxed{A_{greedy}-A^*=1\text{ bit}.}
\]

The frozen beam diagnostics do not rescue the case: widths 2, 4, and 8 all miss the global optimum under the preregistered `(added information, residual W, canonical key)` ranking and first reach a still more expensive closed encoder.

## The optimal path crosses a zero-gain bridge

The greedy path begins by splitting `{2,5}` out of the large target class. This is locally sensible: it immediately removes some unresolved future uncertainty.

The globally optimal path begins differently:

`01000010 -> 01000020`.

This splits the small target class

\[
\{1,6\}\to\{1\}\mid\{6\}.
\]

By itself, the added distinction removes no measurable target-future uncertainty:

\[
\Delta W\approx4.4\times10^{-16}.
\]

A strictly myopic information-gain algorithm therefore has no reason to pay for it.

But now consider the same later split that separates `{3,7}` from the large target class.

Applied directly to the original target, its normalized predictive gain is only

\[
g_{direct}=0.012008771060640484.
\]

After the apparently useless `{1}|{6}` bridge is already present, the same split has

\[
g_{conditioned}=0.15925219276515995.
\]

The predictive value of exactly the same distinction has increased by

\[
\boxed{13.2613230747\times}.
\]

This is the mechanism the greedy rule cannot see.

## The information-theoretic form of the obstruction

For a fixed future target, if `Z'` refines present encoder `Z`, then

\[
W_T(Z)-W_T(Z')=I(C_\infty^T;Z'\mid Z).
\]

So each raw closure-repair gain is a conditional mutual information: how much the new distinction tells us about the target future given the distinctions already represented.

A diminishing-returns geometry would make a remaining distinction no more useful after unrelated detail is added. Research028 explicitly audits that condition.

It fails spectacularly:

\[
\boxed{131,593,228/166,222,336=79.17\%}
\]

of comparable same-split tests violate diminishing returns.

This is consistent with the classical fact that mutual-information objectives are not submodular in general; XOR-style synergy is a standard counterexample, while additional conditional-independence assumptions can restore submodularity. See Krause and Guestrin, [*Near-Optimal Nonmyopic Value of Information in Graphical Models*](https://mlanthology.org/uai/2005/krause2005uai-near/).

But the Groovy result is more specific and, in one sense, stranger: **diminishing returns fails almost everywhere while greedy global optimality fails almost nowhere**.

Therefore generic synergy is not the obstruction we need to classify. The interesting object is **fatal predictive synergy**: a complementary bundle of distinctions whose globally cheaper path requires paying for a distinction that looks insufficiently valuable—or completely useless—under the current representation.

## Independent audit

The first counterexample was reconstructed by a separate implementation that does not import the Research028 search or aggregation code. It:

- implements Rule 24 directly from its truth table;
- constructs explicit target future words;
- independently generates all `B_6 B_2=406` target refinements;
- tests closure as exact functional dependence of the future word on the encoder;
- recomputes every encoder entropy and the entire greedy/global comparison.

It reproduces the 406-node interval, the one-bit regret, the same greedy path, the same global optimum, the zero-gain bridge, and the `13.2613x` gain amplification exactly within the frozen tolerances.

## Fresh-size confirmation

After the independent audit passed, the Rule-24 target and mechanism were frozen before evaluating the periodic `n=15` ring.

Both confirmatory predictions pass.

Greedy remains suboptimal with exactly the same endpoint and exact global encoder:

\[
A_{greedy}=8.443609377704336,
\qquad
A^*=7.193609377704336.
\]

The regret grows to

\[
\boxed{1.25\text{ bits}.}
\]

The zero-gain `{1}|{6}` bridge remains zero within numerical tolerance. The direct and conditioned `{3,7}` gains remain

\[
0.012008771060640515
\quad\text{and}\quad
0.15925219276516045,
\]

again an amplification of

\[
\boxed{13.2613230747\times}.
\]

The exact equality of the normalized gains across `n=12` and `n=15` is striking but is not promoted into an all-size theorem. The persistence of the greedy/global ordering and the synergy inequality are the preregistered claims.

## What Research028 changes

Research027 showed that closure failure can provide a constructive local gradient for representation repair. Research028 does not overturn that result: **99.987% exact global optimality** on a much larger search space is extraordinary.

It does establish the boundary of the naive version.

A representation learner that only asks

> “Which missing distinction is most predictive right now?”

can miss a cheaper sufficient representation because some distinctions acquire predictive meaning only after other distinctions are represented.

The representation calculus therefore needs at least two kinds of structure:

1. **marginal relevance** — distinctions that immediately reduce unresolved future uncertainty;
2. **conditional complementarity** — distinctions whose value is unlocked by other distinctions.

This gives a concrete mathematical version of context dependence at the representation level. Research025 found that the fate of a hidden defect depends on its dynamical context. Research028 finds that the **value of representing a distinction depends on its representational context**.

## What remains open

- Why does greedy remain globally optimal in 30,852 cases despite pervasive diminishing-return violations?
- What separates benign predictive synergy from the four fatal cases?
- Can a computable synergy diagnostic detect a necessary zero-gain bridge without exact global search?
- Why is the failure family confined to the Rule-24/231 conjugacy pair in this finite census?
- Does the Rule-24 mechanism persist for more ring sizes or admit an all-size local proof?
- Can a search strategy explicitly preserving synergistic bundles outperform ordinary greedy and the frozen small beam searches without exploding combinatorially?

## Next theoretical target

The protocol’s decision boundary says not to escalate directly to block size four once a block-3 counterexample exists.

The next target is therefore theoretical:

> **Characterize fatal predictive synergy: the minimal interaction among erased distinctions that makes locally optimal representation repair globally suboptimal.**

A useful result would connect the exact Groovy partition geometry to conditional mutual information, submodularity or its failure, and the dynamics that generate those dependencies. Rule 24 / `01000010` is now the smallest worked counterexample against which that theory can be tested.