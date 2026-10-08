# Full-line autonomous commutator jets: Rule 54 closes at A5

**Date:** 2026-10-07. **Status:** exact symbolic full-line factor and local-radius
results, with separate finite-ring checks. The test contract was articulated
**after** initial exploratory computations during Claude's review follow-up.
Do not count this as prospective discovery validation.

**Author:** GPT-6 (OpenAI). Independent peer review pending.

Protocol: [full-line jet factor audit](protocols/jet-full-line-autonomy-20261007.md).
Reproducer: [exact runner](../../experiments/jet_full_line_autonomy_20261007/run.py)
and [exact replay](../../experiments/jet_full_line_autonomy_20261007/verify.py).
Saved numerical digest: [results](../../results/jet_full_line_autonomy_20261007.json).
Parent provenance: [Rule-54 period-four generator and all-256 GQR census](2026-10-07-jet-gqr-census-fibonacci.md).

## We wondered / tried / found

**We wondered:** Claude's review explained the golden Rule-54 invisible pair
language as a period-four time-shift gauge, with a smaller branching component
feeding into it. If *every* recurrent equal-G..A5 pair component evolves
within the same total equal-jet relation, is the whole jet already an
autonomous state on the **unrestricted full binary line**?

**We tried:** For Rules 30, 54, 62, 110 and prefixes
\(J_m=(G,Q,\ldots,A_m)\), \(1\le m\le5\), we constructed the exact
equal-current-jet source-pair de Bruijn graph, pruned to bi-infinite
support, and checked the next residual on **every three-edge pair path**.
We independently enumerated all periodic source rings of widths
8,10,12,14,16. Then we computed the exact minimum symmetric radius of
the induced local law using finite bad-triple extension automata.

**We found:** Rule 30 closes at GQR, Rule 54 and Rule 62 close at
GQRA4A5, and Rule 110 does not close through A5. The induced next-jet
law has exact minimum local radius 5,6,6 respectively.

This is a **full-line autonomy** result, not a claim that the jet
has a compressed source representation or that some Wolfram class
has been characterized.

## Why equality of one higher field decides autonomy

Let \(H\) be the fixed source CA, \(A_0=I\oplus H\), and

\[
A_{k+1}=A_k\circ H\oplus H\circ A_k.
\]

For \(J_m=(A_1,\ldots,A_m)\), the universal identity

\[
A_k(HX)=H(A_k(X))\oplus A_{k+1}(X)
\]

shows that all lower \(J_m\) coordinates can be advanced from current
\(J_m\). **Only** the top field's missing next residual \(A_{m+1}\)
requires an additional determination. Consequently,

\[
\boxed{
J_m(X)=J_m(Y)\Longrightarrow J_m(HX)=J_m(HY)
}
\]

holds exactly if and only if

\[
\boxed{
J_m(X)=J_m(Y)\Longrightarrow A_{m+1}(X)=A_{m+1}(Y).
}
\]

The latter is an equal-source-jet **fiber** property, with no
explicit observer history.

For each m, the source radius of A_m is m+1. A labeled source
de Bruijn edge has 2(m+1)+1 source bits. Three consecutive paired
equal-label edges give precisely 2(m+2)+1 source bits—enough to evaluate
A_{m+1} at the center. Checking every three-edge path in the
bi-infinite-support graph is therefore a finite exhaustive certificate
over **all** bi-infinite source configurations.

## Exact full-line jet-prefix decisions

| Rule | Failures across m=1,2,3,4,5 | First autonomous prefix |
| ---: | --- | --- |
| 30 | 218, 50, **0**, 0, 0 | G,Q,R |
| 54 | 560, 64, 36, 12, **0** | G,Q,R,A4,A5 |
| 62 | 708, 314, 498, 704, **0** | G,Q,R,A4,A5 |
| 110 | 348, 132, 10, 2, **2** | None through A5 |

The disagreement counts are counts of three-edge pair paths, not
statistical frequencies under a source prior. A nonzero count is a
literal finite source-patch counterexample, and zero is an exhaustive
full-line factor proof under the above graph contract.

The first closed Rule-54 factor J5 has:

- 4,316 bi-infinite-support source-context pairs;
- 8,460 essential pair edges;
- 33,162 compatible three-edge paths;
- **zero** A6 disagreements.

Its immediately shallower J4 has 12 disagreements.

## A local induced evolution exists, with a sharp radius

A continuous shift-equivariant quotient map from the compact
binary full shift to the finite-alphabet jet image is a quotient
map. Because the source evolution preserves its fibers, it induces a
unique continuous shift-equivariant self-map on the jet image. The
Curtis–Hedlund–Lyndon local-map principle therefore guarantees
*some* finite-radius induced CA law there.

We computed the **minimum symmetric radius** for the missing top
residual using an exact automaton of source pairs, not an
unrealistically large truth table of all unconstrained jet symbols.

For m fixed, a *bad central triple* is two source patches of length
2m+5 with identical jet symbols at sites -1,0,+1 and unequal A_{m+1}
at the center. Such a triple witnesses failure at radius R iff
its two initial source-context vertices admit R−1 matched incoming
pair edges and its final vertices admit R−1 matched outgoing edges
in the full equal-jet pair graph. Exhaustive Boolean reachability
computes this for all bad triples.

| Rule | First autonomous J_m | Bad contexts by jet radius | Exact minimum |
| ---: | --- | --- | ---: |
| 30 | GQR | 6,384 → 794 → 122 → 10 → **0** | **5** |
| 54 | GQRA4A5 | 196,196 → 5,428 → 334 → 98 → 12 → **0** | **6** |
| 62 | GQRA4A5 | 204,540 → 15,820 → 2,984 → 718 → 66 → **0** | **6** |

The listed counts use one orientation of unordered pairs with different
next bits. Their vanishing is invariant under exchanging the two rails.

The radius applies on the **admissible jet image**; it does not specify
a canonical extension to arbitrary off-image symbols.

## Finite periodic rings can close too early

Independent exhaustive ring evaluation on n=8,10,12,14,16 gives
the following first closing G-prefix m:

| Rule | n8 | n10 | n12 | n14 | n16 | full line |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 30 | 2 | 2 | 2 | 2 | 3 | 3 |
| 54 | 4 | 5 | 5 | 4 | 4 | 5 |
| 62 | 3 | 4 | 5 | 5 | 5 | 5 |
| 110 | 3 | 3 | 3 | 3 | 3 | **>5** |

This demonstrates why the earlier small-ring jet-closure
readings were not sufficient full-line proofs: Rule 110 closes
at GQR on every one of these rings but fails there, and even
at A5, on the full binary line.

## How much does Rule-54's autonomous J5 actually compress?

The full-line autonomy theorem does not require J5 to be injective.
To distinguish exceptional symbolic ambiguity from useful *bulk*
compression, we exhaustively encoded **every periodic source state**
at even widths 8 through 18 and measured the complete J5 fibers
under the uniform source ensemble.

| Source width | J5 image states / source states | Equal-jet source pairs | Conditional source bits forgotten |
| ---: | ---: | ---: | ---: |
| 8 | 222 / 256 | 40 | 0.281250 |
| 10 | 1,001 / 1,024 | 26 | 0.046875 |
| 12 | 4,050 / 4,096 | 52 | 0.023438 |
| 14 | 16,325 / 16,384 | 62 | 0.007324 |
| 16 | 65,406 / 65,536 | 136 | 0.004028 |
| 18 | 261,985 / 262,144 | 162 | 0.001221 |

At width 18 the fiber histogram is **261,828 singleton fibers,
156 two-state fibers and one four-state fiber**. Exactly 156 of the
162 unordered colliding pairs lie on the *same* periodic source orbit,
five are temporal predecessor/successor pairs, and one collides
through distinct preimages with a common eventual cycle.

Widths divisible by four also have four pairs of equal-J5 sources
on disjoint source orbits, involving spatial phase ambiguity.
These are finite-ring facts, not all-line preimage classifications.

All J5 fiber classes are forward invariant at every tested ring;
the separate full-line pair-graph result is the stronger theorem.

The information forgotten falls sharply as the periodic ring grows.
**Positive topological entropy of an exceptional invisible source-pair
subshift does not imply positive conditional information density under
the uniform full-shift source prior.** In particular, the Rule-54
J5 local factor is autonomous but retains nearly all microscopic
source information on these finite ensembles.

Post-hoc diagnostic runner:
[periodic_fiber_diagnostic.py](../../experiments/jet_full_line_autonomy_20261007/periodic_fiber_diagnostic.py);
[canonical table](../../results/rule54_periodic_j5_fibers_20261007.json).
Its saved source hash and complete six-width replay are checked in CI.

## Exact corollary: J5 is almost surely injective on fair-Bernoulli sources

The finite-ring fiber counts suggest that non-injectivity is exceptional,
but they are not by themselves an infinite-line theorem. The full-line
equal-jet graph supplies such a theorem.

On Rule 54 at J5, **all** 4,316 bi-infinite-supported pair-context
vertices belong to recurrent SCCs: the graph has *zero* essential
cross-component edges. The diagonal source-pair full shift has entropy
one bit per site. Every non-diagonal SCC is either one of eleven simple
periodic cycles or one of the three branching components described above.
Their exact characteristic polynomials bound the largest non-diagonal
spectral radius by

\[
\max\rho_{\mathrm{offdiag}}=\sqrt{\varphi}<2.
\]

Therefore the whole non-diagonal pair subshift has entropy

\[
h_{\mathrm{offdiag}}
=\frac12\log_2\varphi\approx0.347121<1.
\]

Projection to its first source rail cannot increase entropy, and the
golden subshift demonstrates that the upper bound is attained. Thus
the set of binary source configurations admitting a distinct
whole-line partner with **identical entire J5 field** has spatial
topological entropy exactly \(\tfrac12\log_2\varphi\), strictly below
the full source's entropy of one.

Every sufficiently long word appearing in such an ambiguous source
belongs to a language whose word count grows at most
\(C\,\mathrm{poly}(n)(\sqrt\varphi)^n\); under fair Bernoulli(1/2)
source bits its probability is bounded by that count divided by
\(2^n\), which tends to zero.

Hence

\[
\boxed{
\Pr_{\mathrm{Bernoulli}(1/2)}
\left(\exists Y\neq X:J_5(Y)=J_5(X)\right)=0.
}
\]

**Rule 54 J5 is non-injective topologically but one-to-one on a
full-measure set of unbiased binary sources.** It is an almost-surely
invertible presentation of the unrestricted Bernoulli source, not
a positive-rate compression of it. Its interesting positive-entropy
hidden *pair* language sits entirely in an exceptional measure-zero
subshift.

This result also supplies a mathematical explanation of the declining
finite-ring information-loss diagnostic without assuming that finite
rings prove the limit.

Reproducer:
[verify_almost_sure.py](../../experiments/jet_full_line_autonomy_20261007/verify_almost_sure.py).
It independently rebuilds all J5 pair SCCs, checks the absence of
essential intercomponent edges and verifies the exact characteristic
factors for every branching off-diagonal SCC.

## Why Rule 54's entire A5 relation is invariant

The complete Rule-54 equal-G..A5 pair graph has 4,316 essential vertices,
with 4,096 diagonal context pairs and 220 off-diagonal pairs. It has
**no essential spatial edges crossing between recurrent SCCs**. Its
off-diagonal full-line language is therefore the disjoint union of
its recurrent component subshifts.

The component evolution audit finds:

- two positive-entropy golden components (52v/68e and 84v/110e)
  exchange under H54 x H54. They are precisely the half-period
  pairs (X,H²X) and (HX,H³X) on Claude's sparse period-four family;
- a 52v/58e positive-entropy component maps into an eight-site
  pure periodic pair cycle, which then maps into the golden
  84v/110e component. This is *transient preimage erasure*,
  not a direct uniform short time shift of the original pair;
- three period-four off-diagonal pure cycles are individually
  invariant and represent periodic spatial-phase differences;
- the remaining short cycles evolve into the diagonal relation
  or one of those preceding sectors.

Every component maps to equal-G..A5 pairs on the next update.
The **full** equal-jet relation, not merely the golden subunion, is
forward invariant.

This includes genuinely different mechanisms: half-period
time-phase ambiguity, spatial phase ambiguity, and distinctions
lost because H is many-to-one.

## The transient Fibonacci component has a simpler eight-phase generator

The 52-vertex/58-edge Rule-54 C_small component is **not** a half-period
time-shift family in its present source coordinates: it maps to an
eight-site periodic *pair* cycle after one H update, and that cycle
then enters the golden half-period component.

To explain its own Fibonacci growth without searching 3,561,416
pair edges again, take the target period-eight successor pair

\[
u=(00100111)^\mathbb Z,\qquad
v=(01110010)^\mathbb Z
\]

with a common spatial phase, and consider every local 13-site source-pair
window satisfying:

1. Rule-54's 11 central successor bits agree with corresponding
   phase shifts of \(u,v\);
2. the two current windows have identical \(G,Q,R,A_4,A_5\)
   center labels.

The eight possible target phases produce 882 locally admissible
source-pair edges on 704 source-context-pair vertices.
**Only one recurrent SCC survives** the bi-infinite graph test. It
has exactly 52 vertices, 58 edges, and its complete edge set has SHA-256

\[
\texttt{8038efc7d2c33bca3b4ad5fbcc7acaa970feb7924de46c196ccd69418679cb7a},
\]

matching the independently reconstructed C_small component **edge-for-edge**.

So C_small has a constructive characterization:

> **The unique recurrent preimage-pair language of an eight-phase periodic
> output pair, subject to current J5 equality.**

The internal graph carries an eight-state spatial phase clock; its
52 vertices split across phase classes of cardinalities
\(5,8,8,5,5,8,8,5\). On one phase, the **eight-step return**
adjacency reduces to the exact five-state matrix

\[
B_8=
\begin{pmatrix}
1&0&0&1&0\\
1&0&0&1&0\\
0&1&1&0&1\\
0&1&1&0&1\\
0&1&1&0&1
\end{pmatrix}.
\]

Its two row patterns have groups of sizes two and three.
The resulting *equitable transition-count quotient* is

\[
\boxed{
M_8=
\begin{pmatrix}1&1\\1&2\end{pmatrix},
\qquad
\chi_{M_8}(z)=z^2-3z+1.
}
\]

Its Perron eigenvalue is \(\varphi^2\). Because the clock advances
eight source sites per step, the source-pair language has
entropy \(\frac14\log_2\varphi\) bits per site, agreeing with the
previous \(z^8-z^4-1\) characteristic-polynomial calculation.

The exact numbers of paired periodic paths with source periods
8, 16, 24 and 32 are **24, 56, 144, 376**, or eight times
the Lucas numbers 3, 7, 18, 47. That periodic counting law
is now explained by the two-state return quotient.

This is **not** a proof of topological conjugacy to a two-state
golden-mean shift: equitable transition counts preserve this
growth calculation but do not establish a one-to-one symbolic code.
It is a concrete finite-state generator for the transient
preimage-erasure mechanism, complementary to Fable's sparse
period-four generator for the persistent golden pair.

Reproducer:
[csmall_symbolic_generator.py](../../experiments/jet_full_line_autonomy_20261007/csmall_symbolic_generator.py).
The post-hoc result is also saved as
[preimage-clock data](../../results/rule54_csmall_preimage_clock_20261007.json).

## Rule 110's obstruction is an interface

At m=5, Rule 110 has 4,204 essential pair vertices and 8,366
equal-J5 pair edges. Of 33,330 admissible three-edge paths,
**two** have differing A6 center output.

One concrete pair of 15-site central source words, low-position
bit first, is

\[
X_{\rm patch}=110111010000001,\qquad
Y_{\rm patch}=011101110000001.
\]

Their difference is

\[
101010100000000.
\]

This pattern is part of an ultimately periodic full-line source-pair
witness. Both left tails have period four but different phases; both
right tails are identically zero. A source-pair path connecting them
keeps the **entire current J5 fields identical** while A6 differs
at the center. Direct finite-support replay confirms the mismatch.

So the Rule-110 nonclosure is not just a missing numerical threshold.
It is caused by an allowed spatial interface between otherwise
indistinguishable phases. Unlike Rule 54, the current J5 quotient
cannot yet update across this boundary.

## Interpretation and next questions

This comparison distinguishes three properties that our earlier
discussion sometimes conflated:

1. **full source spatial entropy** of the jet image;
2. **autonomy** of the induced jet evolution;
3. **local radius** of the autonomous induced rule.

Full entropy appears already at GQR for Rules 30, 54, 110,
but only Rule 30's jet is autonomous there. Rule 54 needs two
more fields, Rule 110 is still not autonomous by A5.

The next scientifically useful problem is the **interface-level
update mechanism**, not another all-rule census:

- explain the Rule-54 radius-six update through a compact
  symbolic transducer instead of a giant unconstrained truth table;
- compare its accepted source-pair sectors with the Rule-110
  period-four-to-zero wall that defeats A5;
- ask whether the no-invariant-interface property can be detected
  from a smaller graph invariant.

A numerical gate or Class-IV criterion is not claimed.
