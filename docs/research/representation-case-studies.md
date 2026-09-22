# Three executable cases of representation failure and repair

Evidence: exact algebra and certificate extraction from existing results.
Authored by Codex (OpenAI), 2026-09-21. Reviewed by: none. Myk explicitly
authorized solo completion, evaluation and integration in this session.
The examples are not claimed as new general mathematics.

## The question we can actually answer

When a representation fails to predict what comes next, three explanations
need separating. The chosen update law may be wrong. The observation may
discard information that every possible update law needs. Or a certificate
may be valid on one state family and fail on another. These explanations
demand different repairs. A new equation can fix the first; additional
information or a changed domain is needed for the second; the third calls for
correct quantifiers before another computation.

This note gives one inspectable example of each. It replaces a large reading
assignment with three small certificates. The
[verifier](../../scripts/verify_representation_case_studies.py) reconstructs
the relevant evidence without replaying a historical census. Its
[canonical report](../../results/representation_case_studies_20260921.json)
contains the explicit obstruction words, source hashes and graph parameters.
Those hashes establish which inputs were used, while the mathematical checks
establish the claims below. Neither constitutes independent peer review.

## One notation and an explicit contract

Let E be a source cellular automaton, Q an observation of its entire state,
and X a specified invariant family. Time advances by one synchronous source
step throughout these examples. We ask whether a deterministic observed law B
exists such that

$$
QE = BQ \quad\text{on }X.
$$

Such a set map exists precisely when Q(x)=Q(y) implies QE(x)=QE(y) for every
x,y in X. If it exists, B is unique on the observed image Q(X). This statement
alone supplies neither a local rule nor a small computation: finite radius,
alphabet size and implementation cost are additional constraints. It also
does not specify what a rule should do on states outside the observed image.

For histories, define R_h by equality of the complete observed fields at
times 0 through h. Depth at most h means that this observed word determines
the observed field at time h+1. Forward invariance then permits continued
prediction. This is refinement of initial-state equivalence by **forward
observed words**, not a bound on an online observer's suffix storage. The
distinction matters particularly in case C, where “all rings” and “the full
line” quantify over different state families.

Binary words below are written left to right in spatial order. Ring words
wrap periodically. Infinite-line words in case C are specified by periodic
tails and a finite connecting word; the printed window is not itself a ring.

## A. A maximally wrong candidate law, with no information loss

**Contract:** Rule 255; every binary source configuration, on a ring or the
integer line; observation D(x)=x XOR E(x); cadence one; exact one-step identity
and its algebraic continuation. No probabilistic ensemble is needed.

Rule 255 sends every state to the all-one field, so

$$
E(x)=\mathbf1,\qquad D(x)=x\oplus\mathbf1.
$$

D is complementation and therefore invertible. Yet the two compositions in
the original Groovy commutator disagree everywhere:

$$
DE(x)=\mathbf0,\qquad ED(x)=\mathbf1,
\qquad G(x)=\mathbf1.
$$

There is nevertheless an exact autonomous observed law: B(y)=the all-zero
field. It is a radius-zero CA. Indeed, B(D(x))=0=D(E(x)) for every source
state. No extra bit, longer history, or larger spatial window is required.
The repair is to use the correct effective law instead of insisting that the
source law E also be the derivative's law.

The verifier checks all 128 states of ring seven as a reproducible control;
the displayed identities, rather than that finite check, establish the claim
on every binary configuration and every ring width. The source account is
[One representation contract, two different failures](2026-09-10-shared-closure-account.md).

The practical lesson is that nonzero G does not identify information loss.
Here G is as nonzero as possible while the observation retains every source
distinction. A score based on that disagreement must specify which property
of the proposed pair of operations it measures. It cannot silently become a
test of whether *any* autonomous effective law exists.

## B. An observation for which no present-only law can work

**Contract:** source Rule 223; radius-one observation Rule 22 applied at every
site; all configurations of the width-seven periodic ring; cadence one;
deterministic prediction of the next whole observed field from the present
whole observed field. We impose no locality restriction on B.

The extracted pair is:

| Quantity | First source | Second source |
| --- | --- | --- |
| Source state | `0011110` | `0101101` |
| Present observation Q | `0100001` | `0100001` |
| Next observation QE | `0000000` | `0100001` |

The verifier constructs all 128 source states, applies the source and
observation rules, and finds this pair deterministically. The equal inputs
and unequal required outputs refute every deterministic B on this domain.
Even a decoder allowed to inspect the whole ring cannot choose correctly
from Q alone. This is stronger than finding one candidate update table wrong.

The underlying [ring-closure certificate](2026-09-11-ring-closure-certificate.md)
records closure at widths three through six and failure at seven. Small
successful rings therefore do not settle this domain. The new extraction
checks the recorded memberships and independently reconstructs the width-seven
obstruction; it is not a rerun of every rule/observation combination.

A proposed repair must distinguish these two source situations somehow,
change the observation, or exclude at least one situation by an explicitly
declared domain restriction. Keeping the entire source trivially suffices;
that does not establish the cheapest repair. Adding a particular correction
bit is a candidate to test, not something the counterexample automatically
certifies. Likewise, a finite observation history would need its own stated
time indices and proof before being called sufficient.

## C. Every periodic ring can pass while the infinite line fails

**Contract:** source Rule 58; observation Rule 232, the majority-of-three rule;
cadence one. Compare depth-at-most-one on every finite periodic ring with that
same property on the full binary shift, all configurations on the integer
line. The observations at times zero and one are complete spatial fields.

The existing [depth-one certificate](2026-09-11-depth-one-certificate.md)
uses a graph with 256 vertices. Each vertex is a pair of four-cell binary
words. A directed edge shifts both words one cell and appends one new pair
of bits. An edge is allowed when Q and QE agree at the appropriate central
site of its five-cell word. A bi-infinite path therefore describes two full
configurations whose observations agree everywhere at times zero and one.

A seven-cell paired word spans three edges. It is violating when QE² differs
at its centre. There are 196 distinct violating endpoint pairs for this rule
and observation. A periodic ring counterexample needs such a walk to close:
for width n at least four, its final vertex must return to its initial vertex
in n-3 further edges.

Let A be the graph's Boolean adjacency matrix. The saved certificate states
A^23=A^11. The verifier reconstructs A and checks this equality with exact
integer bitsets, avoiding numerical matrix arithmetic. Multiplication by A
then repeats the powers with period twelve from exponent eleven onward. It
checks that no violating walk has the necessary return path in the finite
prefix or periodic block. This covers all n at least four, not merely all
tested widths. Rings one, two and three are checked directly. Together these
checks certify depth at most one on every finite ring.

The full line requires a different extension condition: a violating walk
needs a left-infinite admissible past and a right-infinite admissible future;
it does not need to return to where it began. The stored witness has:

| Piece | First source x | Second source y |
| --- | --- | --- |
| Left periodic tail | repeated `0011` | repeated `0011` |
| Violating seven-cell word | `0011101` | `0011110` |
| Following two bridge bits | `00` | `01` |
| Right periodic tail | repeated `100` | repeated `001` |

Interpret this table by concatenating arbitrarily many left-tail periods,
the seven-cell word, the two bridge bits, and arbitrarily many right-tail
periods. Every five-cell window, including windows crossing each seam, is an
allowed graph edge. The verifier checks all phases of both periodic tails
and every connecting edge. Periodicity then covers the unprinted infinite
parts exactly. At the centre of the seven-cell word, QE²(x)=1 and QE²(y)=0.

Thus Q(x)=Q(y) and QE(x)=QE(y) everywhere on the line, while their second
observed successors disagree. The witness is a path from vertex 15 to vertex
246 with admissible periodic extensions, but the required return is absent.
It can exist on the line without producing any periodic-ring counterexample.
The source is the [full-shift depth-two account](2026-09-11-full-shift-depth-two.md),
whose stronger depth-two conclusion is outside this extraction's claim.

The repair here is first to correct the domain of the assertion. More finite
rings would not find this failure: every one really does satisfy the weaker
claim. A visual crop likewise cannot certify the line. The graph argument
explains both the positive periodic result and the negative full-line result
with the same local objects and different global extension conditions.

## What this contributes, and the selected next comparison

Factor criteria and predictive equivalence are established ideas. Relevant
primary comparisons include
[Israeli and Goldenfeld on CA coarse-graining](https://arxiv.org/abs/nlin/0508033)
and [Shalizi and Crutchfield on predictive causal states](https://arxiv.org/abs/cond-mat/9907176).
The latter's probabilistic framework should not be identified with our
deterministic forward-word partitions without matching its assumptions.
Our contribution here is an executable, scoped account of specific witnesses
and graph certificates already obtained in this repository, including their
failure to transfer between domains. It is not a new general factor theorem.

The asynchronous connection makes one follow-up concrete: compare retained
information at a fixed local update interface. Nakamura's simulation stores
current, previous and phase; Gács's message-field refinement makes explicit
that only information neighbours actually need must survive. This motivates
the separate [bounded causal-retention unit](2026-09-21-causal-retention.md).
Its question is whether Rule 110 admits a smaller pointwise quotient while
preserving current/phase readout, radius one and update cadence. That comparison
was selected and executed under separate frozen protocols, not smuggled into
the three-case extraction. Its witnesses expose a fourth useful distinction:
whole-field necessary checks can miss a local implementation obstruction.

Reproduce this note with `python scripts/verify_representation_case_studies.py
--check`. The command fails if its reconstructed report differs from the
canonical certificate. Existing canonical files are preserved byte-for-byte.
These three cases complete the consolidation task; they do not license a new
rule census, greater refinement depth, or a renewed Class-IV feature search.
