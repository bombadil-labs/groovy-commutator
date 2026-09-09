# A spatial program needs an explicit edit budget

The recovered [dimensional-intertwining checkpoint](2026-09-09-dimensional-intertwining.md) is useful because it makes two hidden costs visible. Its source bits are replicated along infinite diagonals, and its two-dimensional fields contain only a one-dimensional amount of independent information.

Together with locality, this sharpens the next program-inheritance question:

- A finite change of physical cells cannot replace a globally applied source rule everywhere in bounded time under a fixed local interpreter and local decoder.
- A deterministic encoding whose n-by-n output patch reads only O(n) source sites cannot supply positive independent information per target area.

These are elementary locality and counting results, derived below. They constrain particular proposed requirements; they do **not** rule out recursively inherited spatial programs. The current research target must distinguish global program replacement, local program-field edits, and the resources supplied by an encoding.

## Review and correction of the previous proposal

The [two-rail checkpoint](2026-09-09-selector-two-lift.md) suggested requiring a finite source-program edit to become an edit of program cells under the same interpreter. That is a good requirement for a **program attached to a finite region or individual site**. Its globally uniform interpretation is too strong if the physical edit must also have finite support and the whole infinite source must switch rules at a common finite time.

This qualification was missing from the proposal. The two-rail theorem and its 64-rule result remain unchanged. Here we correct the next-step specification before treating it as a selection test.

“An eight-bit rule” is a compact description. Changing one bit of that description can still request a change at infinitely many spatial locations. Description length and physical edit support are different resources.

## Finite disagreement stays inside a finite cone

Let U be a CA on a finite alphabet over Z^D, with Chebyshev radius R. For two configurations X and Y, define their disagreement support

\[
A(X,Y)=\{z:X(z)\ne Y(z)\}.
\]

Locality gives

\[
A(U^tX,U^tY)\subseteq A(X,Y)+[-Rt,Rt]^D.
\]

**Proof.** A site whose entire read neighborhood agrees between X and Y produces the same output. Thus one update can add disagreement only within radius R of the old disagreement set. Iterate this inclusion t times. ∎

Let a fixed decoder read source site i within radius rho of a target anchor a(i). Require the anchor family to be **proper**: only finitely many source anchors lie in any bounded target region. Ordinary block and interface decoders satisfy this condition.

If X and Y differ at finitely many sites, then their decoded states after any common finite time t can differ only at anchors within distance Rt+rho of that finite set. Hence they differ at finitely many source sites.

Proper anchoring matters. A decoder that broadcasts the same target bit to infinitely many source sites does not meet it.

## Obstruction to finite-support global reprogramming

Suppose C(r,S) represents source configuration S running ECA rule r. Assume:

1. one fixed target CA U is used for every r;
2. one fixed, properly anchored local decoder pi is used for every r;
3. one source tick has a common finite target cadence tau, with
   \(\pi U^\tau C(r,S)=F_r(S)\);
4. a permitted change of one global rule instruction is implemented by finitely many cell edits, so C(r,S) and C(r',S) differ on a finite set.

These assumptions cannot hold for all ECA sources and instruction changes.

**Proof.** Suppose r and r' differ at truth-table address q. Write its bits as (l,c,rbit), and repeat the period-three word with S(3j)=c, S(3j-1)=l, and S(3j+1)=rbit. The neighborhood at every site 3j is q. Therefore F_r(S) and F_r'(S) disagree at every site 3j, an infinite set.

Assumption 4 and the finite-cone lemma imply that the two decoded outputs at time tau disagree only finitely often. Assumption 3 says those outputs are F_r(S) and F_r'(S), a contradiction. ∎

The argument already works for one pair of distinct local rules with a periodically repeatable distinguishing patch. It does not depend on a particular higher dimension, source dynamical class, or target computational power.

Allowing arbitrarily large but finite common startup time does not fix the infinite-lattice contradiction. It can fix a finite-world implementation, where the required time may grow with the region being reprogrammed.

### A finite-world edit/latency bound

For N source sites at unit-spaced anchors on a line, let m physical cells be edited. At time t, each edited cell can affect at most 2(Rt+rho)+1 decoded line sites. Thus if the requested source operation changes K next-output sites,

\[
K\le m\bigl(2(Rt+\rho)+1\bigr).
\]

The same upper bound holds on a periodic line, though it is loose once the cone wraps around. For Rule 0 changed to Rule 1 on an all-zero source, K=N: this is a one-instruction global edit. Fixed latency then requires edit support growing linearly with N; fixed edit support requires latency growing with N.

This bound assumes the declared line geometry. Other anchor geometries need their own cone/coverage calculation. It is not a universal linear lower bound for every placement in every dimension.

## Local program edits remain well posed

The repository already has nonuniform CA rule fields. For a retained field P_i of ECA programs, write

\[
S'_i=P_i[4S_{i-1}+2S_i+S_{i+1}],\qquad P'_i=P_i.
\]

This is one fixed interpreter on the complete state (P,S). Replacing one instruction of P_j is a finite local operation. Its immediate state effect is confined to site j, and later state effects propagate through ordinary source neighborhoods. Replacing that instruction in **every** P_i is a distributed operation.

The audit checks this contrast directly. On the same periodic witnesses used above, a global instruction change affects all sites congruent to zero modulo three, while a program edit at site zero changes exactly that site's next state.

This is a clarification of an existing source model, not a new solution of the spatial lift. Representing the rule field in target cells, preserving its declared operations, and giving the induced next program the same native syntax remain constructive tasks.

Finite program objects governing finite regions, replicated program fields, and expanding regions reached by signals are all admissible directions. Their support, synchronization, and latency must be stated. A uniform ambient CA does not invalidate an internal program interpretation.

## The recovered encoding has a measurable edit cost

For the quotient encoding E(S)(x,y)=S(x+y), changing S(j) changes exactly

\[
\{(x,y):x+y=j\}.
\]

That is an infinite diagonal. On the n-by-n torus it contains exactly n cells.

For the two-rail encoding, changing S(j) changes only the interface cell (j,0); through two lifts it changes only (j,0,0).

| Property | Quotient stripes | Two-rail interface |
| --- | --- | --- |
| Exact source dynamics | All 256 ECAs | 64 ECAs under the frozen encoding |
| Support of one source-state bit edit | Infinite diagonal; n sites on an n-by-n torus | One target cell |
| Source program location | Part of the target law | Part of the target routing law |
| Prepared geometry | Replicated source data on quotient fibers | Opposite homogeneous half-spaces |
| Mutable target program cells established | No | No |

Both results are worth keeping. Trajectory intertwining alone does not record the cost of realizing an action.

## Independent information cannot be supplied by dimensional notation

An n-by-n stripe patch indexed by 0<=x,y<n depends on exactly the source bits S(0),...,S(2n-2). Every one of those bits occurs in the patch and can vary independently. Therefore the number of possible binary patches is exactly

\[
P_{\rm stripe}(n)=2^{2n-1}.
\]

An n-by-n two-rail patch intersecting the fixed interface reads exactly n source bits; all other cells are fixed by the background. Thus

\[
P_{\rm rail}(n)=2^n.
\]

Both have vanishing information per target area:

\[
\frac{\log_2 P(n)}{n^2}\longrightarrow0.
\]

For the shift-invariant stripe image this is zero two-dimensional topological entropy. For the fixed-interface family we only assert the displayed anchored patch-count limit; that family is not invariant under translations perpendicular to its interface.

**General footprint bound.** If a deterministic encoding's n-by-n patch is determined by a fixed set of at most Cn source sites from a finite alphabet A, then

\[
P_E(n)\le |A|^{Cn}.
\]

There are only that many possible input assignments. Dividing its logarithm by n^2 proves the same zero-area-information limit. More generally, O(n^d) input sites cannot supply positive information per n^D output volume when D>d.

This is conditional on the footprint bound. Supplying additional independently variable fields, reading a quadratic number of source sites through a different geometry, or charging an evolving construction process changes the problem. A factor model with additional target state also differs from a pure deterministic encoding.

Zero spatial entropy does not mean simple temporal dynamics, lack of computation, or absence of meaningful higher-dimensional organization. “Irreducibly 2D” should therefore not be silently equated with positive area entropy or ambient stencil rank.

## Audit and provenance

The [protocol](protocols/program-edit-locality-20260909.md) was committed at [d665bc9](https://github.com/bombadil-labs/groovy-commutator/commit/d665bc9ecd3cf15ee2842f8531996a4a4516b872) before the audit ran. Its predictions were derived algebraically before enumeration; no criteria or bounds changed afterward.

Run from the repository root:

    python scripts/verify_program_edit_locality.py > /tmp/program-edit-locality.json
    diff -u results/program_edit_locality_20260909.json /tmp/program-edit-locality.json

The [script](../../scripts/verify_program_edit_locality.py) reuses the recovered intertwining verifier's actual 2D laws for the propagation audit. The [saved result](../../results/program_edit_locality_20260909.json) reports:

| Audit | Scope | Result |
| --- | --- | --- |
| Global instruction-change witnesses | 256 rules, 8 bits, widths 9/15/21: 6,144 cases | Every repeated address is a disagreement |
| Single-site program-field edits | 2,048 cases at width nine | Exactly one next-output cell changes |
| Stripe state-edit support | 135 cases, widths 2 through 16 | Exactly n edited target cells |
| Distinct patch enumeration | Sides 1 through 7, both encodings | Exact predicted counts |
| Actual 2D finite propagation | 64 field cases, four ticks, side 21 | 89,600 outside-cone comparisons pass |

All 104,220 assertions pass. The field audit uses two laws, eight source rules, and four deterministic fields. The maximum observed distances are four for the radius-one active law and eight for the radius-two strong law. Finite examples audit implementation; the proofs establish the general statements.

No novelty claim is made for finite-speed propagation or the counting bound. The existing [intertwining note](2026-09-09-dimensional-intertwining.md) supplies simulation-literature context. [Capobianco and Uustalu](https://arxiv.org/abs/1012.1220) provide a primary-source treatment of local CA behavior; the specific operational assumptions and deductions here are stated and proved above.

## Revised constructive target

The next spatial-program candidate should declare:

1. **Program scope:** an individual site, a finite region, or a distributed rule field.
2. **Action support and latency:** which source program/state edits are allowed and what physical support and time they require.
3. **Preparation footprint:** all independent inputs and their spatial support, including program replicas and auxiliary fields.
4. **Recursive representation:** what the first induced program is and how the identical native grammar represents it at the second interface.
5. **Compatibility:** one global encoded field, a fixed decoder, and commuting evolution/action diagrams throughout the declared family.

For a global uniform rule replacement, permit an explicitly distributed edit or a finite-world latency budget. For finite local program edits, begin with local program fields or finite program-bearing regions. These are operationally different experiments.

The next construction remains open. The immediate gain is a well-posed target: ask which program operations survive a spatial lift at a stated cost, without demanding instantaneous global influence or unprovided independent information.
