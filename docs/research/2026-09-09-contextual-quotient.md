# The future-context quotient is the canonical repair target

Research028 found an awkward boundary: greedy representation repair was globally optimal in 30,852 of 30,856 nonclosed block-3 cases, yet four exact counterexamples survived. The first counterexample crossed a distinction with zero immediate predictive gain before another distinction became valuable.

Research029 asks what separates that tiny fatal set from the enormous background of benign predictive synergy.

The answer has two layers.

First, there is a **canonical representation** hiding underneath the repair problem. For any complete future-equivalence label, context substitution induces a unique coarsest uniform local sufficient quotient. This is a theorem, not an ECA regularity.

Second, the exact block-3 census finds no case in which immediate gain strictly forces greedy away from that quotient. All four known greedy failures occur at a zero safety margin, where a safe and unsafe refinement are tied to numerical tolerance. In this domain, fatal predictive synergy is therefore **tie-sensitive rather than strict**.

## The future-context quotient

Let the local alphabet be `A`, let a global configuration consist of `m` tiled local symbols, and let

\[
C:A^m\to Q
\]

be any deterministic target label. For the research application, `C` is the complete future-equivalence label of a fixed observed trajectory.

Define two local symbols `a,b in A` to be context-equivalent,

\[
a\equiv_C b,
\]

when replacing `a` by `b` in **every coordinate and every exact assignment of all other coordinates** leaves `C` unchanged.

Let

\[
q:A\to A/{\equiv_C}
\]

be the resulting quotient.

The full proof is in [Future-context quotient: canonical uniform local sufficiency](proofs/future-context-quotient.md). Its central characterization is

\[
\boxed{C\text{ factors through }z^m\iff \ker z\subseteq\equiv_C}
\]

for every uniform local encoder `z:A -> Z`.

Therefore:

1. `q` is sufficient for `C`;
2. every other sufficient uniform local encoder refines `q`;
3. `q` is the **unique coarsest sufficient uniform local partition**, up to output relabeling;
4. under any full-support local distribution, every strict sufficient refinement carries strictly more encoder information.

Under the uniform product ensemble used by the ECA experiments, `q` is therefore the unique minimum-entropy uniform local sufficient encoder.

This is structurally analogous to Myhill–Nerode/context-congruence constructions: indistinguishability under every admissible context induces a canonical minimal quotient. No novelty claim is made for that abstract pattern. The Groovy-specific move is to take `C` to be a complete dynamical future-equivalence label and study the geometry of repairing a lossy representation toward that quotient.

## Greedy repair now has an exact safety criterion

Suppose the current target partition `P` is coarser than `q`, and repair proceeds only by refinement.

Call a current partition **q-compatible** when `q` refines it. A child refinement is **safe** when it remains q-compatible and **unsafe** when it splits a pair that the canonical quotient keeps merged.

Then a refinement-only path that stops at first closure obeys

\[
\boxed{\text{globally minimum-information}\iff\text{no unsafe step is ever taken}.}
\]

The forward logic is simple but important. A safe closed endpoint must be both coarser than or equal to `q` and, by sufficiency, finer than or equal to `q`; therefore it is exactly `q`. An unsafe split can never be undone by later refinement, so any eventual closed endpoint is a strict refinement of `q` and therefore costs more information.

The **first unsafe split is an irreversible certificate of future regret**.

This replaces Research028's empirical question — “why did greedy fail here?” — with a structural one: **when does the immediate-gain rule choose an unsafe edge?**

## A safety margin for fatal synergy

At a q-compatible nonclosed partition `P`, let

\[
G_s(P)=\max_{P'\,\mathrm{safe}}g(P\to P'),
\qquad
G_u(P)=\max_{P'\,\mathrm{unsafe}}g(P\to P'),
\]

where `g` is the frozen Shannon closure-repair gain from Research027–028. Define

\[
M(P)=G_s(P)-G_u(P).
\]

Then:

- `M(P) > 0`: every maximum-gain edit is safe;
- `M(P) < 0`: every maximum-gain greedy policy is forced unsafe — **strict fatal predictive synergy**;
- `M(P) = 0`: safe and unsafe maximum-gain edits coexist — **tie-sensitive fatal predictive synergy**.

Generic complementarity is not enough. Research028 found diminishing-return violations in about 79% of comparable local gain tests, but almost all of that synergy is harmless to global greedy repair. Fatality requires synergy to move the chosen path outside the quotient-compatible region.

## Exact block-3 census

The frozen [Research029 protocol](protocols/contextual-quotient-20260908.md) evaluates all 256 ECA rules, all 127 canonical block-3 binary targets, periodic width `n=12`, and matched cadence `q=3`.

The fresh CI execution [34322446640](https://github.com/bombadil-labs/groovy-commutator/actions/runs/34322446640) reproduces the full Research028 domain:

- 32,512 total `(rule,target)` cases;
- 1,656 already closed targets;
- 30,856 nonclosed targets;
- 141 fine rules with at least one closed target.

The safety result is exceptionally sharp:

\[
\boxed{\text{strictly negative safety-margin cases}=0.}
\]

Across all 30,856 nonclosed targets, the frozen canonical greedy rule is **never strictly tempted toward an unsafe edit**.

Its four failures are exactly the Research028 Rule-24/231 family:

| Rule | Target | Canonical quotient | Failure margin |
| ---: | --- | --- | ---: |
| 24 | `01000010` | `01230243` | `-5.47e-16` |
| 24 | `01000110` | `01230453` | `0` |
| 231 | `01000010` | `01230243` | `-5.47e-16` |
| 231 | `01100010` | `01230453` | `0` |

The tiny negative values are floating-point residue far inside the frozen `1e-10` equality tolerance. All four are **zero-margin failures**.

The smallest genuinely positive canonical safety margin anywhere in the successful cases is about

\[
0.0010322449040430074,
\]

so the four failures are not merely the low end of a continuous near-zero cloud in this finite domain. They sit on the equality boundary itself.

## The frozen cost-aware tie prediction failed

After the four zero-margin failures were isolated, a second protocol froze a simple tie policy: within the existing gain tolerance, choose the tied refinement with the smallest added encoder entropy before falling back to canonical ordering.

The prediction was that this would repair all four known failures without introducing new ones.

It did repair the Rule-24/231 sentinel family. But the full census found

\[
\boxed{2\text{ cost-aware greedy failures}.}
\]

The canonical and cost-aware paths differ in 1,682 nonclosed cases, so the heuristic is not merely relabeling the original path.

This is a useful negative result. **No generic local tie heuristic has been justified by the quotient theorem.** The theorem says exactly which edges are safe; it does not say that safety can always be reconstructed from immediate gain plus immediate information cost.

The right lesson is therefore not “use a better tie-break.” It is:

> **Greedy is guaranteed by quotient compatibility, not by a universal local tie convention.**

## Independent audit

The CI aggregate is followed by an independently written stratified audit that returns to the complete Research028 partition intervals for selected targets, including the four counterexamples and multiple Rule-30/110 controls across target balances.

For every audited case it requires the directly constructed future-context quotient to be:

- closed for the complete target future;
- equal in information cost to the exhaustive global optimum;
- the **unique** global minimum-entropy closed partition.

The audit passes in the fresh CI run.

So Research029 has two independent evidence layers:

1. a general proof characterizing all sufficient uniform local encoders;
2. an exhaustive ECA census measuring how the frozen greedy gain field sits relative to that canonical quotient.

## Relation to existing theory

The quotient theorem has clear classical relatives.

Myhill–Nerode theory builds minimal automata by identifying states or words that no continuation can distinguish; analogous context congruences appear for trees and other compositional structures. Minimal sufficient statistics likewise arise from the coarsest partition that preserves a target. The present proof is a finite deterministic specialization of that general pattern to a **uniform local encoder repeated over a tiled state**.

On the optimization side, feature-selection literature has long noted that synergistic variables can defeat greedy relevance criteria: a feature may be weak alone and informative conditionally on another selected feature. Research028 gives an exact dynamical instance of that phenomenon. Research029 adds a canonical target partition against which such mistakes can be labeled safe or irreversible.

The project-specific object is therefore not “synergy exists” or “context equivalence gives minimal quotients.” It is the conjunction:

\[
\boxed{\text{future equivalence} + \text{uniform local quotient} + \text{repair-path geometry}.}
\]

## Revised interpretation

Research027 said:

> closure failure can supply a constructive local repair gradient.

Research028 added:

> predictive synergy can make that gradient globally wrong.

Research029 now says:

> **there is a canonical destination, and greedy regret occurs exactly when the repair path irreversibly leaves the region compatible with it.**

In the entire exact block-3 domain tested here, immediate gain never strictly forces that departure. The only canonical failures sit on a tie boundary.

That explains why generic synergy can be pervasive while greedy failure remains extraordinarily rare.

## Limits

- The quotient theorem assumes a uniform local encoder `z` applied independently at every tiled coordinate. Stateful, nonuniform, overlapping, adaptive, and relational encoders are outside the theorem.
- The entropy-minimality corollary assumes full support; the partition-minimality theorem does not.
- The zero-negative-margin result is an exact finite-domain census, not a theorem for larger blocks or other dynamical systems.
- The frozen cost-aware tie heuristic failed in two cases and is not promoted.
- Constructing the exact quotient currently requires the complete target future-equivalence label `C_infinity`. That can be as hard as the predictive problem we ultimately want to solve.

## Next question

The representation-design problem has changed again.

If complete future equivalence is already known, the canonical quotient can be constructed directly and greedy repair is unnecessary. The practical research problem is therefore:

> **Can the future-context quotient, or at least its safe/unsafe boundary, be inferred before the complete future is known?**

That suggests a new direction: approximate contextual equivalence from bounded horizons, local defect traces, or progressively refined predictive distinctions, and ask when those approximations certify safe greedy steps.

The goal is no longer merely to find a good representation. It is to learn **which distinctions may still be merged without sacrificing any future distinction that matters** — and to know when the evidence for that claim is sufficient.