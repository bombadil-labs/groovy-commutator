# When a description becomes reusable

**Proof and visual comparison, 2026-09-23.** Authored by Codex. Reviewed by:
none. [Interactive comparison](../../site/reusable-descriptions.html).
The browser examples are small enough to inspect directly. The proofs below
separate a forced state refinement from a choice of rule extension.

We were curious what makes a description usable as a system in its own right.
We tried the same question on arithmetic and on a one-dimensional Groovy
field. We found that two different things can be missing: distinctions between
states, or a rule specifying what to do with states the new operation creates.
Those failures require different repairs.

## 1. The common test: preserve the required operations

Given an observation Q and an operation f on source states, an operation on
observations exists exactly when equal observed inputs always give equal
observed outputs. For a binary operation this means

\[
Q(a)=Q(a'),\quad Q(b)=Q(b')
\quad\Longrightarrow\quad Q(f(a,b))=Q(f(a',b')).
\]

This is the usual compatibility condition for a congruence; see Burris and
Sankappanavar, *A Course in Universal Algebra*, chapter II, section 5
([author-hosted text](https://www.math.uwaterloo.ca/~snburris/htdocs/UALG/univ-algebra.pdf)).
The unary version is the repository's
[existing factor criterion](2026-09-10-shared-closure-account.md).
Neither criterion is a new theorem here. Locality and cost are extra demands.

Supporting one operation does not establish compatibility with another.
Nor does a well-defined operation on an observed image automatically assign
values outside that image. The two examples make these limits visible.

## 2. Arithmetic: the necessary state is a remainder

Let p be a prime, K a positive integer, and M=p^K. On integers define

\[
c_K(n)=\min(v_p(n),K),\qquad c_K(0)=K.
\]

Here v_p counts factors of p. The cap makes the readout finite; zero is
divisible by every power, so its capped value is K. Fix increment T(n)=n+1,
cadence one, and require the exact readout at every future time for every
integer. A present-state encoding R must retain c_K and have a deterministic
update. No stochastic model or average-case exception is used.

**Sufficiency.** The residue r=n mod M determines c_K(n), and increments by
`r -> (r+1) mod M`. It also supports addition and multiplication of residues.
All these operations are well-defined. The p-exponent readout by itself
already supports multiplication via capped addition of the exponents, but
generally fails for addition or increment.

**Necessity.** Suppose a and b have different residues modulo M. Choose the
nonnegative t<M for which a+t is divisible by M. Then

\[
c_K(a+t)=K,\qquad c_K(b+t)<K.
\]

If R(a)=R(b), deterministic updates would keep their R states equal for all
t, and the retained readout would agree. This is a contradiction. Therefore
every such R must distinguish all M residues. Two equal residues have equal
complete readout futures, so the residue partition is exactly the unique
coarsest sufficient present-state partition, up to relabeling.

This also proves minimality when both addition and multiplication are
required: addition by the encoded constant one includes increment, and the
residue representation supplies both binary operations. For p=2, K=3 the
minimal state has eight possibilities and needs three binary bits in a
fixed-length encoding. This is a state-count bound, not an entropy estimate.

The display starts with four readout groups: capped counts 0, 1, 2, and 3+.
Refining by equal forward words through 0, 1, 2, and 3 increments yields
4, 6, 7, and 8 groups. At the last stage every successor group is determined.
The refinement procedure derives a representation from known dynamics. It
does not give an online suffix-memory bound or a predictor with free access
to future data. Once derived, its operational state is the remainder.

**Costs and meaning.** For p=2 with binary input, initialization reads the K
low bits, retained state is K bits, and a ripple increment can touch K bits in
the worst case. The capped readout scans low bits until the first one or the
cap. Addition/multiplication require their ordinary modular computation; no
unit-cost unbounded arithmetic or speedup is claimed. The extra state
distinctions come from the input, not a fresh source of information.

The same proof applies to each prime p. The nested residue representations
are familiar modular arithmetic, related to the standard p-adic construction.
This unit supplies no result about the distribution of primes. Removing the
cap makes every pair of distinct integers distinguishable by some future
increment/readout, so there is no finite-state exact solution to that
uncapped all-integers contract.

## 3. Rule 32: evolution is fixed but native G is not

Let E be binary Rule 32 on the full integer line. Its output is one precisely
on neighborhood 101. Write Q=G_32, with the repository's convention

\[
G_E(S)=E(S)\oplus E^2(S)\oplus E(S\oplus E(S)).
\]

Rule 32 only flips a zero between two ones. Thus S XOR E(S) fills every
101 hole and contains no 101 afterward. To check that no new hole is made,
consider a zero that remains: its neighbors cannot change, because their
Rule-32 updates would require that center to have been one. If both neighbors
were one, the center would have been filled. Consequently

\[
E(S\oplus E(S))=0,\qquad Q(S)=E(S)\lor E^2(S).
\]

The two terms in the OR are disjoint. Moreover Q(S) is itself the hole-filled
version of E(S), so Q's image excludes 101. Source evolution obeys

\[
Q(E(S))=F_{128}(Q(S))=F_{160}(Q(S)).
\]

The two radius-one rules differ only on 101: Rule 128 returns zero there and
Rule 160 returns one. The accompanying verifier proves the identity on every
length-seven source cone (128 cases), the complete support of both sides.
It also verifies that all seven other three-bit image patterns occur. This
is an exact full-line certificate, not extrapolation from a small ring.
The radius-one factor was already established in the
[Groovy census](2026-09-22-groovy-field-census.md); the two completions are
also recorded in [draft PR #296](https://github.com/bombadil-labs/groovy-commutator/pull/296).

The display uses the periodic seven-cell source S=0101010. Its Q field is
Y=0011100. Both rules give FY=0001000 and F²Y=0000000. But their difference
Y XOR FY is 0010100, containing a 101 neighborhood that valid Q fields exclude.

| Quantity | Rule 128 | Rule 160 |
| --- | --- | --- |
| Y | 0011100 | 0011100 |
| FY | 0001000 | 0001000 |
| F²Y | 0000000 | 0000000 |
| Y XOR FY | 0010100 | 0010100 |
| F(Y XOR FY) | 0000000 | 0001000 |
| Native G_F(Y) | 0001000 | 0000000 |

This exact periodic example is also a full-line witness by repetition.
The displayed computation holds for the finite source word with zero tails
as well. Its job is to exhibit completion dependence, not nonclosure of Y.

**What repair means here.** In the radius-one total-rule class, exactly one
truth-table bit is unspecified. Choosing its value completes the rule, but
both choices remain compatible with every valid Q trajectory. Observing more
valid trajectories or adding their history cannot infer that bit. A fixed
recipe may select it deterministically; this adds no per-state source
information. It remains a convention not forced by valid-field dynamics.

The cost of specifying this interface is one rule-table bit; there are two
possible total rules. This is not a one-bit state-repair theorem, a statement
about all larger-radius completions, or a preference for either choice.
It is the same type of boundary as the earlier
[native completion audit](2026-09-15-commutator-completion.md), now in a tiny
1D example that can be read cell by cell.

## 4. Source XOR is a separate lost-state question

Can we define an operation H with `H(Q(A),Q(B)) = Q(A XOR B)` for all source
rows? Here the answer is no, even with unlimited spatial access.

On the same seven-cell periodic domain, Q(0000000)=Q(1111111)=0000000.
Use B=0101010, with Q(B)=0011100. Then

| Source pair | Observed input pair | Observed source XOR |
| --- | --- | --- |
| 0000000, B | 0000000, 0011100 | 0011100 |
| 1111111, B | 0000000, 0011100 | 0111110 |

Identical observed inputs demand different outputs. This is precisely a
failure of the binary compatibility test. It connects the arithmetic and CA
questions through lost distinctions, independently of the native completion
example. Any globally sufficient repair retaining Q and supporting source
XOR must distinguish these two uniform sources. The witness alone does not
prove that one added bit, or any particular local repair, suffices globally.

Native XOR of observed rows is already defined as a binary-array operation.
It need not represent source XOR or stay inside Q's image. Indeed, for this
rule the transported *source change* has Q(S XOR E(S))=0, while the native
observed change Q(S) XOR F(Q(S)) can be nonzero. Requiring all source-XOR
pairs is stronger than requiring only the source change along a trajectory.
The operation vocabulary is part of the scientific question.

## 5. What this changes

The next order of description is partly forced by its required operations.
For the arithmetic contract, exactly the residue distinctions are necessary.
For the CA native-G contract, no amount of valid-trajectory data selects the
unforced rule bit. For transported source XOR, erased distinctions do matter.
These are three precise outcomes, not a universal recipe for adding context.

The general mechanisms already exist in quotient and factor theory. The
contribution of this unit is a proof-backed interactive bridge, a compact CA
witness, and clear operational boundaries. It introduces no higher-dimensional
lift, recursive-G continuation, learning claim, or new prime theorem.

## Verification and provenance

- [Frozen scope](protocols/reusable-descriptions-20260923.md): commit
  `6b8037f413a13f23753ff0a52b32519b5035500a`.
- Scalar Python and JavaScript model before recorded verification: commit
  `488c880add56e32096a35b04b284a116f43f1fef`.
- [Evidence](../../results/reusable_descriptions_20260923.json) pins both
  implementations and the protocol. It contains all four arithmetic controls
  (K=1..4), the worked CA fields, and the source-XOR witness.
- [Python verifier](../../scripts/verify_reusable_descriptions.py) uses cropped
  scalar cones for full-line checks; the [browser model](../../site/src/lib/reusable-description-model.mjs)
  uses periodic row arithmetic for the displayed examples. Their complete
  example records agree. These are self-checks, not independent review.

Run `python scripts/verify_reusable_descriptions.py` and
`node --test site/scripts/reusable-descriptions.test.mjs` for the bounded
verification. The scope ends here; the [handoff](checkpoints/reusable-descriptions.md)
records publication, visual checks, and the next decision questions.
