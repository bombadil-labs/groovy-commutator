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
