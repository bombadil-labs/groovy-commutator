# Dynamics of Erased Distinctions

This page is the **working synthesis** of the Groovy Commutator research program around coarse-graining, memory, and representation repair. It is not a chronological experiment and it is not a claim that every open mechanism has been solved. It records the smallest common theory that currently survives the exact closure work, the history and observer searches, the fiber-visibility census, and the selector-shielding results.

The current thesis is:

> **Groovy Commutator studies the dynamics of distinctions erased by a representation.**

The original derivative/evolution commutator is still one useful instrument, but it now sits inside a broader question: when a representation says two microscopic states are “the same,” does the dynamics preserve that indistinguishability? If not, how does the discarded distinction travel before it becomes visible again? If it never becomes visible, what physical structure keeps it safely outside the effective state?

## The core object: indistinguishability under dynamics

Fix dynamics `E`, positive cadence `q`, and a representation or observation `P` on a declared family X with E^q(X) contained in X. All pairs and iterations below are restricted to that family. Define the present observational relation

\[
R_0=\{(s,s'):P(s)=P(s')\}.
\]

Let pair dynamics be

\[
F=E^q\times E^q.
\]

The distinctions that can be forgotten forever by this observation are exactly

\[
\boxed{R_\infty=\bigcap_{t\ge0}F^{-t}(R_0).}
\]

A pair in `R_infinity` remains observationally indistinguishable for its entire future. A pair in `R_0` but not `R_infinity` is only temporarily hidden: eventually the discarded distinction returns to the observed variables.

This formulation compresses several research threads into one object.

- **Closure** asks whether `R_0` is already forward invariant.
- **History lift** computes successive refinements of `R_0` until they stabilize at `R_infinity`.
- **Memory depth** measures the longest finite residence time inside present indistinguishability.
- **Fiber visibility** separates latent distinctions from permanently shielded ones.
- **Selector shielding** searches for local physical mechanisms that make portions of `R_infinity` invariant.

## Shared representation contract

Revision 2026-09-10: the [shared account](2026-09-10-shared-closure-account.md)
records the synthesis agreed with the dimensional workstream. With the family
and cadence fixed, an autonomous factor exists exactly when equal present
observations have equal next observations. It is unique on the observed image;
locality and off-image extension are additional requirements. A candidate-law
error instead compares one proposed law with the actual observed update. Use
XOR only when the observation space has the required binary-group structure.

For Rule255, D is invertible complementation, D(E(s)) is zero, E(D(s)) is one,
and G is everywhere one. The actual derivative factor is constant zero: there
is maximal same-rule disagreement without any erased-information failure.
The dimensional Program also tests factor existence directly through its
transverse/full-gradient observations, so the two Programs are not partitioned
into disjoint kinds of defect. Existing findings and evidence labels are unchanged.

The R_t below describes forward observed-word partitions of initial states,
using the same cadence. It is not itself an online suffix learner or an
adaptive observer's stored state. The new knowledge entries in the shared
account make the Research022–028 and Research035 provenance explicit.

## Closure is not the same as commutation

The original Groovy comparison asks whether

\[
PE^q=EP.
\]

That is a particularly strong self-similarity condition: the same rule survives the change of representation. The more general closure condition is

\[
PE^q=BP
\]

for some induced dynamics `B` on the observed state. Equivalently,

\[
F(R_0)\subseteq R_0.
\]

[Research022](2026-09-08-observation-closure.md) shows that this distinction is substantive. Derivative observations can have a maximally nonzero same-rule commutator and still be perfectly autonomous under a different effective rule. Exact block-factor searches recover the earlier scale-rhyme relations as ordinary observation closure.

So a nonzero Groovy commutator does not by itself mean the representation failed. It may mean only that the effective law changed.

## When closure fails, coarse-graining creates memory

If `R_0` is not forward invariant, two states that look identical now can have different observed futures. A present-only macrostate is then not a sufficient state variable.

Define

\[
R_t=\bigcap_{j=0}^{t}F^{-j}(R_0).
\]

The descending chain

\[
R_0\supseteq R_1\supseteq R_2\supseteq\cdots\supseteq R_\infty
\]

adds exactly the observed history needed to distinguish hidden microscopic contexts that can still matter. [Research023](2026-09-08-history-lift-closure.md) computes this refinement exactly on finite ECA rings and finds both bounded causal memory and memory that grows with system size. Temporal memory and spatial range trade off: a globally sufficient history need not admit a small-radius local rule.

This gives a physical reading of non-Markovian coarse dynamics:

> **History is required when a representation erased a distinction before that distinction finished exerting causal influence.**

## The minimal predictive quotient and safe forgetting

The stable relation `R_infinity` defines the smallest exact predictive state space compatible with `P` on the finite system. It restores every hidden distinction that can ever change the observed future and keeps collapsed every distinction the observed future can never use.

[Research025](2026-09-08-fiber-visibility.md) turns this into an exact information budget,

\[
\boxed{H(S)=H(P(S))+I_{\rm latent}+I_{\rm shielded}.}
\]

- `H(P(S))` is what the observer represents now.
- `I_latent` is information hidden now but required by the minimal predictive refinement.
- `I_shielded` is information absent from the entire future of the chosen observation.

The last term is a precise notion of **safe forgetting** relative to an effective description.

This is stronger than asking how much information a coarse-graining loses. The important question is **which lost distinctions remain in the causal future of the variables we intend to keep**.

## Closure and possibility are different representation objectives

Research025's latent term also has a direct possibility interpretation. If `C_infinity` is the stable future-equivalence class, then

\[
V_\infty(E,P)=H(C_\infty\mid P(S))
\]

is the entropy of distinguishable observed future trajectories compatible with the present macrostate. In other words,

\[
\boxed{I_{\rm latent}=\text{future repertoire hidden in the present}.}
\]

[Research026](2026-09-08-possibility-frontier.md) uses this to separate two representation-selection objectives:

1. forget as little as possible while making present closure fail;
2. choose a representation under which the present macrostate remains compatible with the largest repertoire of distinct futures.

Across the exact `n=12` static block-observer census, 247 of 256 ECA rules admit at least one closure-breaking observation. For 222 of those 247, the least-forgetting closure breaker and the maximum-repertoire observer are different. No repository-labeled Class-III or Class-IV rule has a tested observer that optimizes both.

The extremes both have zero repertoire: identity forgets nothing and therefore leaves no macro-level ambiguity, while a constant observation forgets every distinction including the future itself. Possibility therefore lives in an interior region of representation space, and for most rules its best value is not monotone in the amount forgotten.

This adds a second design pressure to the Program. A representation can be good because it is a compact sufficient state for prediction, or because it preserves a rich structured family of still-distinguishable continuations. Useful representations may need to negotiate between those objectives rather than maximizing one scalar notion of compression.

## Constructive repair meets predictive synergy

[Research027](2026-09-08-representation-design.md) turns closure failure into a constructive problem. With future semantics fixed, let `Z` refine present target `T` and define

\[
W_T(Z)=H(C_\infty^T\mid Z(S)).
\]

A one-step refinement gain is the unresolved future information removed per added present bit. On the complete two-cell local partition lattice, greedily taking the best such split finds the globally minimum-information exact repair in all 1,590 nonclosed cases tested. Closure failure therefore supplies a real local representation gradient.

[Research028](2026-09-08-block3-representation-design.md) finds the first exact boundary of that result. On the much larger block-3 repair intervals, greedy remains globally optimal in 30,852 of 30,856 nonclosed cases—**99.987%**—but fails exactly four times. All four failures belong to the Rule-24/231 conjugacy family.

The first counterexample reveals why. An optimal path first adds a distinction with essentially zero immediate predictive gain. Once that distinction is present, the predictive gain of another fixed split increases by a factor of about `13.26`. In information-theoretic form, for a refinement `Z'` of `Z`,

\[
W_T(Z)-W_T(Z')=I(C_\infty^T;Z'\mid Z).
\]

So the value of a missing distinction can depend strongly on which other distinctions are already represented. The cheapest sufficient representation may require crossing a **zero-gain bridge** that a purely myopic gradient will never choose.

Research028 explicitly tests local diminishing returns and finds violations in about 79% of comparable same-split cases, even though greedy global failure is extremely rare. Generic synergy is therefore common but usually benign. The sharper theoretical object is **fatal predictive synergy**: conditional complementarity strong enough to make a locally inferior representation path globally cheaper. An independent implementation reproduces the first counterexample, and a frozen `n=15` test preserves the same greedy failure and `13.26x` gain amplification.

The later causal-witness line sharpens the same issue. Research031 shows that finite periodic topology can hide genuinely admissible predictive contexts. Research032 replaces explicit light-cone enumeration with a symbolic witness automaton, while Research033 and Research034 progressively constrain unresolved cases by the grammar of reachable paired contexts. Research036 then attacks the remaining frontier from the complementary direction: represent the exact one-defect orbit as a sofic shift rather than widening a local context window. The exact criterion works on bounded controls, but the obvious explicit graph presentations hit severe proof-object growth. The resulting hierarchy now separates not only real from spurious causal possibility, but **dynamical reachability from the complexity of representing reachability**.

Research037 then separates the representation problem from the closure mechanism itself. Reduced decision diagrams carry every declared temporal-recurrence test across the full 170-case frontier with zero censoring, but no frontier rule satisfies `G^h = sigma^delta G^j` through horizon 6. Rule 5 does satisfy the stronger control identity `G^3=G`. The result is a genuine negative rather than another resource boundary: compact exact local dynamics is available, but the missing reachability certificate must allow an output to be re-presented from **different source provenance**.

## Hidden modes have dynamics

The discarded distinctions are not abstract bookkeeping. They can propagate, decay, orbit, collide, or change shape while remaining invisible.

[Research024](2026-09-08-observer-search.md) shows this directly for Rule 106 under block parity. A coherent adjacent two-bit defect can travel for dozens of macrosteps without changing the observation. [Research025](2026-09-08-fiber-visibility.md) then finds the stronger result: the **same initial hidden defect** has two different fates in two different common contexts.

One pair remains microscopically distinct and parity-invisible forever on its finite joint orbit. Another pair carries the same translating defect for 50 macrosteps before surrounding state changes its shape and makes it visible at step 51.

For nonlinear dynamics, causal fate therefore belongs not to a defect shape alone but to the **defect-in-context**. Rule 106 makes this algebraically explicit through a context-dependent difference cocycle.

In linear systems the limiting case is simpler: observer-null differences can form an invariant subspace whose evolution is autonomous. The nonlinear relation `R_infinity` is the natural replacement for that fixed hidden subspace.

## Physical shielding: when nearby differences are not read

The [selector-shielding checkpoint](2026-09-08-selector-shielding.md) attacks safe forgetting from a complementary direction in the project’s 2D selector law.

A protected exact Rule-90 strip can remain bit-for-bit correct on its outer row even while the neighboring inner row is strongly contaminated. The reason is not geometric distance. The update rule selects a state-dependent subset of nearby source cells. The checkpoint proves an exact one-step dominance criterion: while the protected lower half-plane is still equal, `0 -> 1` inner-row damage can remain unread, while a first harmful `1 -> 0` defect is necessarily read by the protected row one tick later.

The branch then proves exact recurring moving boundary walls and an exact period-2 stripe-diode phase whose selector orientation gives one-way causal flow. These are concrete mechanisms for **safe forgetting by causal shielding** rather than by a global observer congruence.

## Interaction can rewrite the causal boundary

The scattering work originally asked whether hidden structure could interact to create, erase, or reorganize effective objects.

The single-pulse line proves a rigid all-displacement scattering law for one exact family. The broader small-shape census then preregisters five named fates: extinction, exact reconstitution, fan-out, fold-in, and persistent-channel scattering. In 1,600 frozen mixed-shape cases it finds **none** of the first four, but every case launches both top and bottom persistent boundary channels.

That null result is informative: fan-out and fold-in should not be imported into the ontology merely because the words are suggestive. For the tested architecture the robust outcome is a pair of persistent outward causal channels, not clean multiplication or reassembly of the original encoded units.

The more interesting event appears just outside that frozen family. Interaction can generate a selector-relative shield that changes **which physical differences an existing organization reads**, even without cleanly reconstituting the interaction into a new countable set of separated organizations.

That reframes one version of the original fan-out/fold-in intuition. The novel outcome of interaction may be a **new causal boundary** rather than a new object count.

## What is exact now

The program should distinguish its stable results from its motivating language. The following are exact within their stated finite or local domains:

1. **Closure versus self-similarity.** A representation can close under an induced law `B` even when it does not commute with the original law. Exact derivative and block-factor identities establish concrete examples.
2. **Finite predictive refinement.** On the tested finite deterministic systems, repeated observed-history refinement stabilizes at future equivalence, and the exact history depth equals the longest finite visibility time.
3. **Derivative noncoalescence.** Distinct states with identical derivative histories cannot later coalesce.
4. **Rule-106 context dependence.** The same observer-null adjacent defect is permanently shielded in one common context and latent in another. Its local difference evolution has an exact context-dependent formula.
5. **Rule-106 finite scaling confirmation.** A frozen arithmetic lifetime prediction for one latent defect passed all 50 fresh even ring widths from 102 through 200.
6. **Selector/dominance theorem.** For the declared exact lower-strip reference, one-step shielding is equivalent to preservation of the row-2 reference ones.
7. **Moving shielding walls.** The left and right boundary-wall recurrences established in the shielding checkpoint are exact for all future time within their proved moving-frame domains.
8. **Stripe diode.** The reported period-2 stripe phase is an exact phase with directional selector behavior.
9. **Bounded scattering laws.** The single-pulse all-displacement law and the 1,600-case small-shape census are exact within their declared architectures.
10. **Possibility frontier.** In the frozen static observer family at `n=12`, 222 of 247 rules with any closure breaker separate the least-forgetting closure breaker from the maximum-future-repertoire observer; all six frozen observer pairs preserve that ordering on the fresh `n=18` validation.
11. **Constructive local repair.** On the complete two-cell partition lattice, greedy fixed-target Shannon repair reaches the globally minimum-information exact closure repair in all 1,590 nonclosed target cases, while bulk-entropy and worst-case-tail repair already select different first edits in 326 cases.
12. **Predictive-synergy obstruction.** On the complete block-3 target-refinement intervals, greedy remains globally optimal in 30,852 of 30,856 nonclosed cases but has four exact one-bit-regret failures in the Rule-24/231 conjugacy family. The first counterexample independently audits and persists at `n=15`; a zero-immediate-gain distinction amplifies a later split's predictive gain by about `13.26x`.
13. **Reachable-context refinement.** Symbolic light-cone and finite-state language constructions progressively eliminate false predictive possibilities introduced by periodic or insufficiently composable context approximations; Research032–034 provide exact finite certificates for the stated horizons and language widths.
14. **Exact sofic orbit criterion and representation boundary.** Every fixed-time image of the one-defect sofic shift has an exact finite labeled-graph presentation, and finite orbit containment gives an exact all-time permanence certificate. Bounded controls reproduce the known Rule-35 horizon-3 witness and a finite exact Rule-5 orbit closure. On the 170 Research034 survivors, however, the frozen explicit-graph methods are completely censored: lazy union localizes the bottleneck to slice imaging, while the raw higher-block control requires 6,029,312 transitions before constructing the known horizon-3 witness.
15. **Symbolic recurrence clears the graph wall but does not close the frontier.** Exact MDD local functions recover the Rule-5 mechanism as `G^3=G` and complete every frozen identity/translation recurrence test through horizon 6 on all 170 Research034 survivors. None receives a recurrence certificate and none is censored. The next exact proof object must therefore be relational: it must permit an earlier-slice representation with different latent source provenance.

## What remains open

Several tempting generalizations are not yet earned:

- The concrete selector-shielding witness is not yet proved shielded for all time; the widening middle remains the unresolved route for eventual leakage.
- The Rule-106 2-adic lifetime recurrence is confirmed on a fresh finite range, not proved for all ring sizes or the infinite lattice.
- No general nonlinear local criterion yet tells us whether an arbitrary hidden distinction belongs to `R_infinity`.
- The static block-observer searches do not establish an optimal representation family; good effective variables may need to be relational, dynamical, stateful, or adaptive.
- The near-perfect greedy repair result has no general theorem behind it. Block-3 gives exact counterexamples, and the project does not yet know what separates benign predictive synergy from synergy that makes a local repair gradient globally wrong.
- The Rule-24 zero-gain-bridge mechanism is confirmed at `n=12` and `n=15`, not proved for all compatible ring widths.
- The 170 cases left after Research034 remain dynamically unclassified. Research036 supplies an exact sofic criterion but hits an explicit-graph representation boundary. Research037 clears that computational wall for the narrower temporal-recurrence certificate and obtains a complete negative through horizon 6: none of the 170 closes by ordinary time recurrence or translation. This still does not imply a future witness or rule out a more general relational orbit-inclusion certificate.
- The project has not established that the four Wolfram classes are the right organizing taxonomy for these closure profiles.

## The next theoretical targets

This Program currently has three complementary proof problems.

The first remains physical **safe forgetting**:

> **Find a local criterion for forward invariance of observational indistinguishability.**

In a linear system this resembles an unobservable invariant subspace. In the nonlinear systems studied here, the corresponding object is state- or trajectory-relative: a hidden mode can be safe in one context and latent in another, and a selector can dynamically create walls that block one direction of causal influence. Rule 106 and selector shielding are the first worked examples.

The second is constructive **representation geometry**:

> **Characterize fatal predictive synergy: when must a globally cheapest sufficient representation include a distinction whose marginal predictive value is too small—or zero—for a greedy repair rule to select?**

Research027 shows that the local closure gradient can be extraordinarily effective. Research028 proves it is not universally sufficient and supplies a minimal finite counterexample. The later context-language results suggest that representation repair and causal certification may ultimately share a common object: a sufficiently rich grammar of distinctions whose combinations are actually reachable.

That shifts the representation-design problem from blind observer search toward a higher-order calculus: marginal relevance describes first-order repair, conditional complementarity describes interactions among distinctions, and reachable-context languages constrain which apparent interactions can occur at all.

The third is exact **relational reachability**:

> **Construct a finite-state source recoder or simulation relation that proves earlier-slice representation without projecting the reachable image into an explicit follower graph.**

Research036 proves that exact sofic orbit closure is the right semantic object but that literal finite-graph presentations hit different computational walls. Research037 shows that reduced decision diagrams can carry the exact local dynamics cheaply enough across the full frontier, while ordinary temporal recurrence still resolves none of the 170 cases. The missing flexibility is provenance: general inclusion may represent a time-`h` output by an earlier slice generated from a different admissible source row. The next candidate is therefore a transducer or graph endomorphism over the exact two-state one-defect source language, eventually generalized to a two-tape simulation relation if a deterministic recoder is too restrictive.

## Parallel program

The separate [Dimensional Closure and the Commutator Lift](2026-09-09-dimensional-closure-program.md) Program follows a different but related question: when evolution and transformation disagree, can their residual be promoted into an additional spatial coordinate so that the enlarged representation closes? The two Programs share notes and algebra, but maintain distinct proof targets.

## How to read the record

This Program page is deliberately not a replacement for the research notes. It is a **living compression** of them. The notes retain protocols, failed predictions, exact bounds, and the historical path by which the project changed its mind. The Knowledge base keeps smaller reusable claims.

The earlier [History and possibility program](2026-09-07-history-and-possibility.md) remains an important precursor: it widened the project from prediction to available action and revisability. The present synthesis narrows one strand of that broader question into a more precise mathematical program about representations, hidden distinctions, and causal visibility.

## Open direction: sound approximation after closure fails

The [archived Rule110 example](2026-09-10-successor-set-archive.md) compares exact whole-field successor sets with sound local Cartesian products on the eight-cell ring. The general question remains open: which ordered representation domains preserve useful precision at a declared resource cost? Whole-field correlations, cell-frequency metrics and prior-weighted entropy bounds are distinct. This is a reproduced exploratory example; new substrates and infinite-lattice claims require a separate frozen protocol.

## Planned execution: representation empowerment census

The [frozen no-op/flip protocol](protocols/representation-empowerment-20260910.md) and its [registered experiment](../knowledge/representation-empowerment-planned.md) add a control question to the existing repertoire frontier. The [publication checkpoint](2026-09-10-representation-empowerment-protocol.md) records observer/cadence provenance and the exact-input capacity certificate. Implementation and new numerical evaluation remain planned and unrun.

The controller sees only P(S_0), with a uniform prior within its fiber, and receives a declared future readout after one intervention. Uniform-action information and optimized capacity are distinct; both use the original macrostate weights. Research026's observer-specific cadence is preserved. This is independent of issue64's learner and uses a different information/action contract from the completed gradient audit.
