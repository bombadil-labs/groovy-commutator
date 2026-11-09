# Protocol: bounded repair-island source recoders — 2026-09-10

**Status:** frozen before evaluating any Research034 frontier seed language under this fresh family.  
**Working identity:** `repair-island-source-recoder`; no public note number is assigned until publication.  
**Dependency:** Note 038 / `phase-splice-source-recoder`, Note 037 / `symbolic-sofic-image`, Note 036 / `sofic-defect-orbit`, Research032 symbolic witness safety, and Research034 width-3 frontier.

## Why this checkpoint exists

Note 038 completes an exact 22/22 negative for the first changed-provenance recoder. A single `LR` or `RL` phase cut may choose different evolved source rails on opposite sides of the reinserted defect, but it has only one selector transition.

The next question should add the smallest new spatial freedom rather than jump directly to an arbitrary transducer:

> **Can a later defect be re-presented by taking one evolved rail as the default common background, borrowing the other rail over one bounded interior repair island, and then returning to the default rail?**

This is a two-cut selector. It is the minimal finite rail-selector family not already exhausted by Note 038.

## Exact source and dynamics

Let `G` be the exact radius-one 8-symbol macro CA induced by three fine ECA ticks. For ordered hidden seed `s=(a,b)`, let `x^L,x^R` agree everywhere except at the origin, where they contain `a,b`. After `k>=1` macrosteps define

\[
z^L=G^k(x^L),\qquad z^R=G^k(x^R).
\]

The rails agree outside `[-k,k]`.

Choose:

- `j>=1`, `t=k+j`;
- seed displacement `delta in [-k,k]`;
- default rail `B in {L,R}`;
- a strict interior interval `[u,v]` with `-k < u <= v < k`.

Let `\bar B` denote the other rail. Define the common recoded background

\[
r_q=\begin{cases}
z^{\bar B}_q,&u\le q\le v,\\
z^B_q,&\text{otherwise.}
\end{cases}
\]

Then overwrite position `delta` by the original ordered seed:

\[
P_q=\begin{cases}
(a,b),&q=\delta,\\
(r_q,r_q),&q\ne\delta.
\end{cases}
\]

Every such `P` is exactly a member of the original one-defect source shift `X_0(s)`.

Exclude the ineffectual candidate `u=v=delta`, since the only flipped selector site would be overwritten by the seed.

## Freshness boundary

Intervals touching an active-cone boundary are not fresh:

- a flip interval reaching exactly one boundary reduces, on the only region where `z^L` and `z^R` may differ, to a one-cut `LR/RL` selector already exhausted by Note 038;
- a flip interval reaching both boundaries reduces to a disclosed constant-rail normalization.

Therefore the fresh primary family uses **strictly interior repair islands only**: `-k<u<=v<k`.

This adds exactly one extra selector transition relative to Note 038: default -> alternate -> default.

## Exact certificate

Candidate `(k,j,delta,B,u,v)` passes iff, for every genuine one-defect source row,

\[
\widehat G^{k+j}(x)=\widehat G^j(P_{k,\delta,B,u,v}(x)).
\]

A pass proves

\[
X_{k+j}(s)\subseteq X_j(s),
\]

including the all-diagonal closure branch by the same argument as Note 038. Since `j<t` and Research032 establishes target safety through `t<=6` for every incoming Research034 frontier question, any passing candidate in the frozen range yields exact all-time permanence for every target attached to that seed language.

## Frozen primary domain

Use exactly the same **22 distinct `(rule,seed)` languages / 170 target questions** as Notes 037-038:

- 158 Class-II target questions;
- 12 Class-III Rule-122/161 sentinel questions;
- frontier rules `{122,154,161,164,166,180,210,218}`.

No seed or target may be added or removed after fresh outcomes are inspected.

## Frozen candidate family

Search exactly

\[
2\le t=k+j\le6,
\]

with:

- `k>=1`, `j>=1`;
- `delta in [-k,k]`;
- default rail `B in {L,R}`;
- `-k < u <= v < k`;
- exclude `u=v=delta`.

This yields exactly **2,788 fresh candidates per seed language** before early termination.

Canonical candidate order:

1. increasing `t`;
2. increasing `j` (decreasing `k` within fixed `t`);
3. `delta` by `(abs(delta), delta)`;
4. increasing repair-island width `v-u+1`;
5. increasing `u`;
6. default rail `L` before `R`.

Stop a seed-language search at the first exact passing candidate. A non-certified seed must exhaust the family unless censored.

## Exact primary backend

Use the fine-ECA SAT/CNF representation validated by the Note-038 recovery, not the MDD backend.

For each candidate and each required output position `p in [-t,t]`:

1. construct the exact finite fine-bit source cone for the two original rails;
2. encode `3k` original ECA ticks to obtain the evolved `z^L,z^R` values needed by the repair-island selector;
3. assemble the recoded common background from the frozen default/island selector and reinsert `(a,b)` at `delta`;
4. encode `3j` further fine ticks for the recoded rails;
5. independently encode the original source through `3t` ticks;
6. ask Minisat22 whether either corresponding three-bit macro output can differ.

SAT means the candidate fails at that position. Decode the source background and scalar-replay both original and recoded fine-ECA evolutions before accepting the failure.

UNSAT for both rails means exact equality at that position.

A candidate passes only if every required output position is UNSAT.

The production repair-island instrument must not import the MDD builder or MDD equality code.

## Frozen output-position order

Retain Note 038's resource-order rule:

1. positions outside the reinserted seed's `j`-step future cone `[delta-j,delta+j]`, ascending;
2. positions inside that cone, ascending;
3. stop at the first exact inequality.

This affects resource behavior only, not semantics.

## Frozen controls

Before primary evaluation require:

1. the existing disclosed Rule-5 seed `0-2`, `(k=2,j=1,delta=0,LL)` positive control still passes in the shared fine-ECA CNF primitives;
2. the Note-038 Rule-35 seed `2-6` negative controls through `t<=3` still reproduce;
3. boundary-interval selector controls reduce to and agree with the corresponding previously evaluated one-cut `LR/RL` semantics, even though those boundary intervals are excluded from fresh primary counting.

Any control disagreement blocks primary evaluation.

## Frozen resource envelope

Retain comparability with Note 038:

- maximum wall time per seed language: **1,200 seconds**;
- one matrix shard per seed language;
- no post-outcome increase of the wall;
- SAT instance size is measured but not assigned an intrinsic dynamical interpretation.

A seed is `censored` if no certificate has appeared and its frozen family is not exhausted before the wall.

## Frozen primary hypothesis

Before evaluating any frontier seed:

> **At least one of the 22 Research034 frontier seed languages admits an exact bounded repair-island source-recoder certificate with `k+j<=6`.**

A complete zero is useful: it would show that adding a second selector transition is still insufficient and would justify moving to multiple repair islands, arbitrary finite selector masks, or a synthesized local repair transducer.

## Measurements

For each seed language record:

- rule, class, seed pair, target IDs;
- candidates tested / 2,788;
- first certificate if any;
- first failing position and scalar-replayed counterexample for each failed candidate in the full audit record;
- CNF variables/clauses maxima;
- wall time and censoring point.

Aggregate:

- certified / exact-negative / censored seed languages;
- exact permanence resolutions among 170 target questions;
- Class-II / Class-III breakdown;
- certificate parameter distribution;
- Rule-122/161 sentinel status;
- comparison with one-cut Note 038 costs.

As with Note 038, retain both a full audit result and a compact canonical JSON + Markdown summary.

## Independent audit of any fresh success

If a repair-island certificate appears, freeze the first canonical success before interpretation and independently re-encode it in Z3 without importing the production CNF builder. Require UNSAT for the negation of every output-position identity and scalar replay any model. A disagreement invalidates the certificate.

## Decision rule

- **Success:** independently audit; characterize the minimal island and whether it crosses the latent seed; compare against Note 038's one-cut failure.
- **Complete exact zero:** broaden to multiple islands / arbitrary finite rail-selector masks or synthesize a bounded local repair transducer.
- **Censoring:** preserve this exact family and improve search/synthesis (for example CEGIS/QBF/BDD); do not merely raise the wall.
- Do not return to explicit projected sofic graphs or enlarge the horizon merely because this family fails.
