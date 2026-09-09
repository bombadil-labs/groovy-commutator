# Protocol: symbolic defect normalization — 2026-09-09

**Status:** frozen after instrument design on previously published controls and before evaluating any Research034 survivor with this certificate family.  
**Branch:** `research/symbolic-sofic-image-20260909`.  
**Working identity:** numberless; assign a public research-note number only after the checkpoint is complete.  
**Dependency:** Research032 exact causal-witness analysis, Research033–034 reachable-language invariants, and Note 036 `sofic-defect-orbit` on `main`.

## Why this is narrower than “symbolic sofic image”

Note 036 established an exact sofic-orbit criterion but found that explicit image presentations are unusable on the 170-case frontier: the compressed, lazy-union, and raw-NFA variants all hit frozen presentation ceilings.

One half of the desired symbolic representation already exists. Research032’s reduced 8-ary MDD represents the exact local map

\[
G^t:A^{2t+1}\to A
\]

for the induced block-3/cadence-3 macro CA. Restricting one input axis to the two seed values while sharing every other variable is exactly the finite-witness question for a one-defect paired slice. The independently recovered horizon-6 null therefore already supplies exact symbolic target-visibility information through `t=6`.

The unresolved task is **symbolic orbit inclusion / permanence**.

This checkpoint does not attempt general projected-language inclusion. It tests a stronger constructive certificate: can an evolved spread defect be normalized back into the original one-defect form inside a future kernel, so that a later exact slice is represented by an earlier slice without materializing either projected image graph?

## Exact setup

Let

\[
G:A^{\mathbb Z}\to A^{\mathbb Z},\qquad A=\{0,\ldots,7\}
\]

be the exact radius-1 macro CA induced by three fine ECA ticks.

Fix an ordered hidden seed

\[
s=(a,b),\qquad a<b.
\]

For an arbitrary background `x in A^Z`, let `P_s(x)` be the paired row whose two rails agree with `x` everywhere except at the distinguished origin, where the first rail is forced to `a` and the second to `b`.

Let

\[
X_t(s)=\widehat G^t(X_0(s))
\]

be the exact one-defect paired time slice used in Note 036.

The distinguished origin is latent provenance, not an observed coordinate. Because `X_0(s)` is shift-invariant, any fixed displacement of the reinserted seed still denotes a member of the same one-defect language.

## Rail-normalization map

Choose:

- a normalization time `k >= 1`;
- an earlier-slice depth `j >= 1`;
- a source rail `r in {left,right}`;
- a seed displacement `delta` with `-k <= delta <= k`.

For an initial one-defect pair `P_s(x)`, evolve only the chosen scalar rail for `k` macrosteps:

\[
z=G^k(P_s(x)_r).
\]

Define `N_{s,delta}(z)` to be the paired row obtained by using `z` as the common diagonal background, then forcing the original seed values `(a,b)` at position `delta`.

Thus `N_{s,delta}(z)` is **exactly a member of `X_0(s)`**: one occurrence of the original seed in an otherwise diagonal arbitrary background.

A candidate `(k,j,delta,r)` passes when the following identity holds for **every** background `x`:

\[
\boxed{
\widehat G^j\!\left(N_{s,\delta}(G^k(P_s(x)_r))\right)
=
\widehat G^{k+j}(P_s(x)).
}
\]

Call this a **rail-normalization certificate**.

## Closure theorem

If a rail-normalization certificate holds, then

\[
X_{k+j}(s)\subseteq X_j(s).
\]

Proof: for every source row in `X_0(s)`, the normalized row is another member of `X_0(s)` and its `j`-step image equals the original row’s `(k+j)`-step image. Taking all source rows gives the inclusion.

Let `t=k+j`. Since `j<t`,

\[
\widehat G(U_{t-1})=X_1\cup\cdots\cup X_t
\subseteq U_{t-1},
\]

because `X_t subset X_j subset U_{t-1}`. Therefore, if `X_0,...,X_{t-1}` are target-safe, the target is permanently invisible.

This is an exact sufficient certificate for the original one-defect language. Failure is inconclusive: general orbit inclusion may hold without any certificate in this family.

## Exact symbolic verification

No projected image graph is constructed.

For one candidate let `t=k+j`. A radius-1 CA implies that output site `p` at time `t` depends only on the `2t+1` initial symbols in `[p-t,p+t]`.

For every spatial output position

\[
p\in[-t,t],
\]

construct one reduced ordered 8-ary MDD over those `2t+1` background variables. Within the same canonical MDD manager:

1. build the actual first-rail and second-rail local outputs after `t` steps, fixing the initial origin to `a` or `b` when it lies in the local window;
2. evolve the chosen rail only `k` steps, leaving a symbolic word of length `2j+1` corresponding to positions `[p-j,p+j]`;
3. if `delta` is in that word, replace the corresponding symbolic value by terminal `a` on one candidate rail and terminal `b` on the other;
4. evolve both normalized candidate words `j` further steps;
5. require canonical root equality between each actual rail and its normalized candidate rail.

The candidate passes iff all `2t+1` output positions pass.

Why this finite check is complete: outside `[-t,t]` the actual two rails are equal because the original one-site defect cannot propagate farther than `t`, while the normalized seed lies within the time-`k` cone and its `j`-step effect is also contained in `[-t,t]`. Both constructions otherwise follow the same chosen evolved background.

Canonical MDD root equality is exact functional equality over all assignments; no sampling or bounded word language is used.

## Frozen candidate family

Search only

\[
2\le t=k+j\le6,
\]

with

- `k >= 1`;
- `j >= 1`;
- `k+j=t`;
- `delta in [-k,k]`;
- `r in {left,right}`.

This bound is chosen before primary evaluation because Research032 already establishes target invisibility through horizon 6 for the incoming Research034 frontier. A passing certificate at `t<=6` can therefore convert that finite exact null into an all-time certificate without any new finite-witness search.

Candidate order is frozen for canonical reporting and resource behavior:

1. increasing `t`;
2. increasing `j`;
3. displacements ordered by `(abs(delta), delta)`;
4. `left` before `right`.

Within one candidate, check output positions outside the candidate seed’s `j`-step cone `[delta-j,delta+j]` first, in ascending order, then positions inside the cone in ascending order. A proved inequality at any position is an exact counterexample and immediately fails that candidate.

Stop a seed-language search at the **first passing candidate** in this frozen order; later candidates are not needed to establish the exact closure and are recorded as untested. If no candidate passes, exhaust the family unless the seed-language wall-time ceiling is reached. Candidate status counts therefore describe the tested prefix for certified languages and the complete family for uncensored non-certified languages.

## Frozen primary domain

Use exactly the **22 distinct `(rule,seed)` one-defect languages** underlying the **170 Research034 survivor target questions**.

The production script reconstructs this domain from the frozen Research034 algorithm (`scan_research034`) rather than trusting a hand-copied survivor list. The complete aggregate must assert totals `22` seed languages, `170` target questions, and target-question class split `158 Class II + 12 Class III` before interpreting outcomes. Do not add or remove seed languages after primary evaluation begins.

This reconstruction is a deterministic replay of already published Research034 classifications, not a new choice of primary cases.

For every incoming target attached to a seed language, retain the Research032/034 assertion that no finite witness exists through horizon 6. The new instrument is not allowed to redefine or recompute the incoming target family after seeing normalization outcomes.

## Published controls and design disclosure

The certificate family was designed using only previously published controls, not the 170-case primary outcomes.

### Rule 5 positive closure control

For Rule 5 / seed `0-2`, Note 036’s exact graph oracle already establishes closure at transition index 2. During instrument design, the exact graph relation was localized further to

\[
X_3\subseteq X_1.
\]

An exploratory exact MDD check then found the concrete normalization

- `k=2`;
- `j=1`;
- `delta=0`;
- `rail=left`.

The production instrument **must** reproduce this identity. This is a disclosed implementation control, not a fresh prediction.

### Rule 35 positive-witness exclusion control

For Rule 35 / seed `2-6` / target `00000001`, the exact first witness occurs at horizon 3 while horizons 0–2 are target-safe.

Therefore no rail-normalization certificate with `t<=3` may pass: such a certificate would imply forward closure before the known horizon-3 witness. The production instrument must reject every frozen-family Rule-35 candidate with `t=2` or `t=3`.

A failure of either control blocks primary evaluation.

## Frozen resource envelope

Reuse Research032’s symbolic ceiling:

- maximum nonterminal MDD nodes in any one output-position identity check: **5,000,000**.

Additional operational ceilings:

- maximum wall time per `(rule,seed)` language: **20 minutes**;
- maximum `t`: **6**;
- maximum variables in one MDD: **13**;
- no candidate-family expansion after primary outcomes are inspected.

Each output-position check uses a fresh MDD manager. Crossing the node or wall-time ceiling is **censoring**, never evidence that the identity fails or that the dynamics is complex.

Candidate classification:

- `pass`: every required pointwise identity is proved;
- `fail`: at least one exact pointwise inequality is found;
- `censored`: a resource ceiling is reached before pass/fail is established.

Seed-language classification:

- `certified`: at least one candidate passes;
- `no-certificate-in-frozen-family`: every candidate fails exactly;
- `censored`: no candidate passes and at least one candidate remains censored.

## Frozen primary hypothesis

Before evaluating any of the 22 survivor seed languages:

> **At least one Research034 survivor seed language admits a rail-normalization certificate with `k+j<=6`, converting at least one of the 170 finite-horizon-safe target questions into an exact all-time permanence certificate.**

A null result is scientifically useful. It would rule out this simple “choose one evolved rail, erase the spread defect, reinsert the original seed” normal form as the missing symbolic inclusion witness across the frozen frontier, without ruling out richer symbolic transducers, piecewise normalizers, target-aware quotients, or general exact orbit inclusion.

No prediction is frozen for the Rule-122/161 sentinel families.

## Measurements

For every `(rule,seed)` language record:

- attached Research034 target IDs;
- candidate status counts over the tested prefix;
- first canonical passing candidate, if any;
- first exact failing output position and a compact counterexample assignment when practical;
- MDD node counts by checked output position;
- maximum node count and elapsed time;
- censoring candidate/position/reason, if any.

Aggregate:

- certified seed languages;
- exact permanence resolutions among the 170 target questions;
- no-certificate and censored seed languages;
- class breakdowns;
- Rule-122/161 sentinel outcomes;
- distribution of certificate `(t,k,j,delta,rail)` parameters.

## Independent audit rule

If any primary seed language is certified, freeze the first canonical success immediately.

Before publication, verify that success with a separately written fine-ECA Boolean encoding that does **not** import the MDD transition builder. For every required output position, encode the negation of the claimed normalization identity over the exact `3(2t+1)` fine initial bits and prove it UNSAT with an independent SAT/SMT backend. Replay any SAT counterexample scalarly.

A disagreement blocks the certificate and publication claim.

If the primary family has no passing certificate, no independent positive-outcome audit is required beyond the two frozen semantic controls.

## Interpretation boundaries

- A passing certificate proves exact slice inclusion and, with the imported finite safety bound, exact permanence.
- A failed candidate is only a failure of that specific normalization map.
- Exhausting the frozen family does **not** prove that `X_t` is absent from the earlier orbit union.
- Censoring is representation cost, not dynamical evidence.
- The method keeps the one-defect source row as latent provenance; it does not construct a general symbolic presentation of the projected sofic image.
- The finite-witness half is imported from Research032 rather than claimed as new work.
- No claim is made for arbitrary CA, arbitrary sofic shifts, or arbitrary factor-map inclusion.

## Decision rule

- If survivor certificates appear, characterize the kernel repair that lets a spread defect collapse back to one-defect normal form and compare its proof cost with Note 036’s explicit graphs.
- If only simple Class-II cases certify, test whether the mechanism is tied to eventual local image collapse before broadening the family.
- If the 22-language frontier is uncensored but no certificate appears, move to a richer exact symbolic relation: multiple repair patches, piecewise/transducer normalizers, or target-aware inductive refinement.
- If MDD censoring dominates, preserve the family and change only the symbolic backend under a separately frozen recovery protocol; do not raise the node ceiling post hoc.
