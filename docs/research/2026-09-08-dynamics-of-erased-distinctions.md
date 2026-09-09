# Dynamics of Erased Distinctions

This page is the **working synthesis** of the Groovy Commutator research program. It is not a chronological experiment and it is not a claim that every open mechanism has been solved. It records the smallest common theory that currently survives the exact closure work, the history and observer searches, the fiber-visibility census, and the selector-shielding results.

The current thesis is:

> **Groovy Commutator studies the dynamics of distinctions erased by a representation.**

The original derivative/evolution commutator is still one useful instrument, but it now sits inside a broader question: when a representation says two microscopic states are “the same,” does the dynamics preserve that indistinguishability? If not, how does the discarded distinction travel before it becomes visible again? If it never becomes visible, what physical structure keeps it safely outside the effective state?

## The core object: indistinguishability under dynamics

Fix dynamics `E`, cadence `q`, and a representation or observation `P`. Define the present observational relation

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

## Hidden modes have dynamics

The discarded distinctions are not abstract bookkeeping. They can propagate, decay, orbit, collide, or change shape while remaining invisible.

[Research024](2026-09-08-observer-search.md) shows this directly for Rule 106 under block parity. A coherent adjacent two-bit defect can travel for dozens of macrosteps without changing the observation. [Research025](2026-09-08-fiber-visibility.md) then finds the stronger result: the **same initial hidden defect** has two different fates in two different common contexts.

One pair remains microscopically distinct and parity-invisible forever on its finite joint orbit. Another pair carries the same translating defect for 50 macrosteps before surrounding state changes its shape and makes it visible at step 51.

For nonlinear dynamics, causal fate therefore belongs not to a defect shape alone but to the **defect-in-context**. Rule 106 makes this algebraically explicit through a context-dependent difference cocycle.

In linear systems the limiting case is simpler: observer-null differences can form an invariant subspace whose evolution is autonomous. The nonlinear relation `R_infinity` is the natural replacement for that fixed hidden subspace.

## Physical shielding: when nearby differences are not read

The [selector-shielding checkpoint](2026-09-08-selector-shielding.md) attacks safe forgetting from a complementary direction in the project’s 2D selector law.

A protected exact Rule-90 strip can remain bit-for-bit correct on its outer row even while the neighboring inner row is strongly contaminated. The reason is not geometric distance. The update rule selects a state-dependent subset of nearby source cells. The checkpoint proves an exact one-step dominance criterion: while the protected lower half-plane is still equal, `0 -> 1` inner-row damage can remain unread, while a first harmful `1 -> 0` defect is necessarily read by the protected row one tick later.

The branch then proves exact recurring moving boundary walls and an exact period-2 stripe-diode phase whose selector orientation gives one-way causal flow. These are concrete mechanisms for maintaining causal invisibility.

The all-time fate of the widening middle of the particular shielding witness remains open. A failed fresh-tail prediction also shows that short local motifs are insufficient to classify shielding: wider context can determine whether a difference eventually leaks through. That negative result agrees with the Rule-106 defect-in-context result rather than weakening it.

## Interaction can change causal visibility without reassembling objects

The strip-scattering line supplies another important constraint. [Research020](2026-09-08-pulse-scattering.md) proves that relative position alone changes exact launch timing and boundary signature, not qualitative fate, for the single-pulse family. [Research021](2026-09-08-pulse-shape-scattering.md) extends that negative result across 1,600 bounded pulse-shape encounters: all launch two persistent boundary channels.

The more interesting event appears just outside that frozen family. Interaction can generate a selector-relative shield that changes **which physical differences an existing organization reads**, even without cleanly reconstituting the interaction into a new countable set of separated organizations.

That reframes one version of the original fan-out/fold-in intuition. The novel outcome of interaction may be a **new causal boundary** rather than a new object count.

## The commutator generates a dimensional lift

The dimensional-lift line asks a complementary closure question. Safe forgetting asks when a distinction can be erased without changing the represented future. The lift asks what must be **added to the representation when two legitimate dynamical paths disagree**.

The [ternary commutator lift](2026-09-09-ternary-commutator-lift.md) gives a rule-independent exact construction. For fixed deterministic evolution `F` and any configuration transformation `A`, define

\[
L_F(A)=A\circ F,
\]

\[
R_F(A)=F\circ A,
\]

and

\[
C_F(A)=L_F(A)\oplus R_F(A).
\]

`L` and `R` are the two paths around the commuting square; `C` is their residual. Starting from the outgoing derivative `D=I\oplus F`, every word `w` in the alphabet `{L,R,C}` defines a descendant transformation `A_w`. At depth `d`, the labeled words are naturally the `3^d` ternary addresses of a side-three `d`-dimensional block.

Define the semantic block

\[
J_d(S)_w=A_w(S).
\]

Adding one dimension gives three exact slabs:

\[
J_{d+1}^{L}(S)=J_d(F(S)),
\]

\[
J_{d+1}^{R}(S)=F^{\parallel}(J_d(S)),
\]

\[
J_{d+1}^{C}(S)=J_{d+1}^{L}(S)\oplus J_{d+1}^{R}(S).
\]

So each added semantic dimension records **evolve then transform, transform then evolve, and the distinction between them**. The commutator is no longer only a scalar or field-valued diagnostic. Its residual becomes another represented coordinate, which can itself be evolved, compared, and supplied with its own residual.

The nominal ternary tree has an exact algebraic quotient. Associativity gives `LR=RL`, and left composition distributes over XOR so `LC=CL`. Therefore depth `d` has at most

\[
\boxed{2^{d+1}-1}
\]

semantically distinct descendant maps even though it has `3^d` labeled addresses. In the frozen depth-six ECA census, 107 of 256 rules saturate this bound at every tested depth with counts `1,3,7,15,31,63,127`; 33 rules reach a finite vocabulary closed under all three descendants by depth six, while 223 do not. Neither finite closure nor maximal growth is Class-IV-exclusive. The operator survives that negative classification result unchanged because its definition was frozen without class labels.

This is currently an exact **semantic dimensional lift**, not yet a native higher-dimensional cellular automaton. The open physical problem is whether a fixed bounded local `(d+1)`-dimensional rule can carry `J_d` autonomously so that projection onto the `L` face reproduces lower-dimensional evolution while the `R` and `C` faces supply the independently evolved role and the correction required for closure.

This gives the Program a third use of representation failure. A hidden distinction can sometimes be forgotten safely; a missing predictive distinction can sometimes be repaired by adding state; and a failure of two operations to commute can be **promoted into a new coordinate and recursively represented**.

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
13. **Ternary commutator lift.** For any deterministic binary evolution on the declared substrate, the `L/R/C` descendants give an exact rule-independent recursive semantic lift. Its labeled depth-`d` coordinates form a `3^d` ternary address space, while `LR=RL` and `LC=CL` force at most `2^(d+1)-1` distinct semantic roles. The frozen all-ECA depth-six census verifies the quotient, finds 33 finite closed role vocabularies, and finds 107 rules saturating the maximum growth sequence through the tested depth.

## What remains open

Several tempting generalizations are not yet earned:

- The concrete selector-shielding witness is not yet proved shielded for all time; the widening middle remains the unresolved route for eventual leakage.
- The Rule-106 2-adic lifetime recurrence is confirmed on a fresh finite range, not proved for all ring sizes or the infinite lattice.
- No general nonlinear local criterion yet tells us whether an arbitrary hidden distinction belongs to `R_infinity`.
- The static block-observer searches do not establish an optimal representation family; good effective variables may need to be relational, dynamical, stateful, or adaptive.
- The near-perfect greedy repair result has no general theorem behind it. Block-3 gives exact counterexamples, and the project does not yet know what separates benign predictive synergy from synergy that makes a local repair gradient globally wrong.
- The Rule-24 zero-gain-bridge mechanism is confirmed at `n=12` and `n=15`, not proved for all compatible ring widths.
- The ternary commutator lift is semantic. No fixed bounded native higher-dimensional CA has yet been shown to evolve the lifted block autonomously, and the finite role-growth census does not establish infinite closure or growth.
- The project has not established that the four Wolfram classes are the right organizing taxonomy for these closure profiles.

## The next theoretical targets

The current Program has three complementary proof problems.

The first remains physical **safe forgetting**:

> **Find a local criterion for forward invariance of observational indistinguishability.**

In a linear system this resembles an unobservable invariant subspace. In the nonlinear systems studied here, the corresponding object is state- or trajectory-relative: a hidden mode can be safe in one context and latent in another, and a selector can dynamically create walls that block one direction of causal influence. Rule 106 and selector shielding are the first worked examples.

The second is now constructive **representation geometry**:

> **Characterize fatal predictive synergy: when must a globally cheapest sufficient representation include a distinction whose marginal predictive value is too small—or zero—for a greedy repair rule to select?**

Research027 shows that the local closure gradient can be extraordinarily effective. Research028 proves it is not universally sufficient and supplies a minimal finite counterexample. The next useful theory should explain why 79% of tested local gain comparisons can violate diminishing returns while only four of 30,856 nonclosed block-3 targets actually defeat greedy global repair.

That shifts the representation-design problem from blind observer search toward a higher-order calculus: marginal relevance describes first-order repair, while conditional complementarity describes interactions among distinctions. A successful theory should say when those interaction terms can safely be ignored and when they must be represented explicitly.

The third is constructive **dimensional role closure**:

> **Find a native bounded higher-dimensional cellular automaton realization of the ternary commutator lift.**

The semantic operator is already rule-independent: each new coordinate stores the two paths around a commuting square and their residual. The missing theorem or construction is spatial. A successful realization must use one fixed local architecture, preserve the declared `L/R/C` meaning under evolution, and relift without adding a hidden external program or choosing a decoder separately for each source rule.

This target is downstream of the original Class-IV hope rather than tuned to it. The first algebraic closure and growth measures already fail as exact Class-IV discriminators. Any future selectivity must therefore come from the stronger native spatial-closure condition, evaluated only after the local geometry is fixed.

## How to read the record

This Program page is deliberately not a replacement for the research notes. It is a **living compression** of them. The notes retain protocols, failed predictions, exact bounds, and the historical path by which the project changed its mind. The Knowledge base keeps smaller reusable claims.

The earlier [History and possibility program](2026-09-07-history-and-possibility.md) remains an important precursor: it widened the project from prediction to available action and revisability. The present synthesis narrows one strand of that broader question into a more precise mathematical program about representations, hidden distinctions, and causal visibility.
