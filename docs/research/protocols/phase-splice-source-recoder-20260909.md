# Protocol: phase-splice source recoders — 2026-09-09

**Status:** frozen before evaluating any Research034 frontier seed language under the fresh cross-phase recoder family.  
**Branch:** `research/relational-source-recoder-20260909`.  
**Working identity:** `phase-splice-source-recoder`; no public research-note number is assigned until publication.  
**Dependency:** Note 037 / `symbolic-sofic-image`, Note 036 / `sofic-defect-orbit`, Research032 symbolic causal-witness analysis, and Research034 width-3 reachable language.

## Why this checkpoint exists

Note 037 clears the explicit-graph representation wall for exact local dynamics but finds a complete negative for same-provenance temporal recurrence: all 170 Research034 frontier questions complete every test

\[
G^h=\sigma^\delta G^j,
\qquad 1\le h\le6,
\]

with zero recurrence certificates and zero censoring.

That result isolates the missing freedom. Exact language inclusion

\[
X_h(s)\subseteq X_0(s)\cup\cdots\cup X_{h-1}(s)
\]

does not require the earlier representation to come from the same initial background. It may use a different admissible source row.

The exact one-defect source graph already carries one bit of latent provenance state: a path is in its `L` phase before the unique seed edge and its `R` phase afterward. This checkpoint asks whether that phase is enough to build a useful source recoder.

> **Can a later spread defect be re-presented by splicing together the two evolved source rails on opposite sides of a newly inserted one-defect seed?**

This is the first fresh relational certificate after Note 037. It does not construct or project a sofic image graph.

## Freshness disclosure

Branch history from an abandoned pre-Note-037 scaffold contains an exploratory **single-rail normalization** idea: choose the entire common recoded background from either the left or the right evolved rail, then reinsert the original seed. A one-shot workflow for that scaffold was launched before the research direction pivoted; no canonical primary result from it was merged or published.

Therefore:

- all-left (`LL`) and all-right (`RR`) recoders are **not fresh primary evidence** here;
- they may be used only as disclosed controls or diagnostics;
- the fresh primary family consists only of the cross-phase policies `LR` and `RL` defined below;
- no hypothesis is phrased in terms of an `LL` or `RR` outcome.

No cross-phase frontier outcome has been used to design this protocol.

## Exact source language

Let

\[
G:A^{\mathbb Z}\to A^{\mathbb Z},
\qquad A=\{0,\ldots,7\},
\]

be the exact radius-one macro CA induced by three fine ECA ticks.

Fix an ordered hidden seed

\[
s=(a,b),\qquad a<b.
\]

A non-diagonal member of the exact source language consists of two scalar rails

\[
x^L,x^R\in A^{\mathbb Z}
\]

that agree everywhere except at one latent defect position, taken as the origin, where

\[
x^L_0=a,\qquad x^R_0=b.
\]

Its paired form belongs to the one-defect shift `X_0(s)`. Translating the latent defect gives the same shift language.

The all-diagonal topological-closure branch is handled separately and trivially in every theorem below: if the source rails are equal, evolve that common scalar background for the required extra time and use an all-diagonal earlier source. The new recoder therefore only needs to cover the genuine one-defect branch.

## Evolve, splice, reinsert

Choose integers

\[
k\ge1,\qquad j\ge1,\qquad t=k+j,
\]

and a seed displacement

\[
-k\le\delta\le k.
\]

From a one-defect source pair, first evolve both scalar rails for `k` macrosteps:

\[
z^L=G^k(x^L),\qquad z^R=G^k(x^R).
\]

The two rows agree outside `[-k,k]` by finite propagation.

A **phase-splice policy** is one of

\[
LR\quad\text{or}\quad RL.
\]

For `LR`, define a new paired source row `P_{k,\delta}^{LR}(x)` by

\[
P_i=
\begin{cases}
(z^L_i,z^L_i), & i<\delta,\\
s=(a,b), & i=\delta,\\
(z^R_i,z^R_i), & i>\delta.
\end{cases}
\]

For `RL`, exchange `L` and `R` in the two diagonal regions.

By construction, every `P_{k,\delta}^{LR/RL}(x)` is exactly another member of `X_0(s)`: arbitrary diagonal background, one copy of the original ordered seed, and no other off-diagonal symbol.

The recoder is shift-equivariant when the latent defect position is translated. Operationally it is a finite-state transducer: the source graph's pre-seed/post-seed phase selects which evolved rail supplies the common background, and a bounded delay/advance places the output seed at `delta`.

## Exact phase-splice certificate

A candidate `(k,j,delta,policy)` passes when

\[
\boxed{
\widehat G^{k+j}(x)
=
\widehat G^j\!\left(P_{k,\delta}^{policy}(x)\right)
}
\]

for **every** genuine one-defect source row `x` with seed `s`.

### Closure theorem

If the candidate passes, then

\[
X_{k+j}(s)\subseteq X_j(s).
\]

For the genuine one-defect branch this follows directly from the constructive recoder. For the all-diagonal closure branch, write the common source as `(u,u)` and use the all-diagonal source `(G^k u,G^k u)` at time `j`.

Since `j<k+j`, the new slice is already contained in the prior orbit union. Therefore

\[
\widehat G(U_{t-1})\subseteq U_{t-1},
\qquad t=k+j.
\]

If the earlier slices are target-safe, Note 036 gives the exact all-time certificate

\[
w_T(a,b)=\infty.
\]

Research032 and its independent horizon-6 recovery establish target safety through `t<=6` for all incoming Research034 frontier questions, so any passing candidate in the frozen range below immediately resolves every target attached to that seed language.

## Why the displacement range is enough for the fresh family

Search only

\[
|\delta|\le k.
\]

The two evolved rails can differ only inside `[-k,k]`. If `delta>k`, the entire region where the two candidate backgrounds can differ lies on the `LR` policy's left side, so the background selection reduces there to the all-left (`LL`) normalization already exposed before this protocol. Similarly `delta<-k` reduces the active region to `RR`; the `RL` case is symmetric.

Any effect of the reinserted seed outside the actual `t`-step defect cone would have to vanish identically for equality to hold. Such a candidate adds no genuinely cross-phase repair beyond the disclosed single-rail family. The declared displacement range therefore contains every candidate in which the fresh `LR/RL` phase splice is dynamically active.

This completeness statement is only for the declared cross-phase family; it is not a completeness theorem for arbitrary source recoders.

## Exact symbolic verification

No projected image graph is constructed.

For one candidate let `t=k+j`. For every output position

\[
p\in[-t,t],
\]

use one fresh reduced ordered 8-valued MDD manager over the `2t+1` arbitrary background symbols in `[p-t,p+t]`.

Within that manager:

1. build the actual left/right outputs after `t` macrosteps, fixing the latent source origin to `a` on the left rail and `b` on the right rail whenever the origin lies in the dependency window;
2. evolve both source rails only `k` steps, leaving symbolic values for positions `[p-j,p+j]`;
3. for every position `q` in that word, choose `z^L_q` or `z^R_q` according to whether `q<delta` or `q>delta` and the frozen `LR/RL` policy;
4. at `q=delta`, replace the two candidate rail values by terminal symbols `a` and `b` respectively;
5. evolve the two normalized candidate rails `j` further steps;
6. require canonical MDD-root equality with the corresponding actual `t`-step rails.

A candidate passes iff all required positions pass.

Checking `p in [-t,t]` is complete. Outside that interval the original defect cannot affect the actual paired row. The recoded seed lies in `[-k,k]`, so its `j`-step causal cone is contained in `[-t,t]`; outside the interval both candidate rails also reduce to `G^j(G^k u)=G^t u` on the shared background.

Canonical root equality inside one MDD manager is exact functional equality over all background assignments. If roots differ, extract one MDD assignment and replay it with a separate scalar macro evaluator before recording the candidate as failed.

## Frozen controls

These are semantic implementation controls, not fresh primary evidence.

### Rule 5 positive control

The abandoned single-rail design already exposed the exact Rule-5 normalization

- seed `0-2`;
- `k=2`;
- `j=1`;
- `delta=0`;
- policy `LL`.

The production implementation must reproduce that identity as a disclosed positive control. Note 037 independently establishes the stronger full-shift recurrence `G^3=G`, so this control is not new evidence.

### Rule 35 negative control

For Rule 35 / seed `2-6` / target `00000001`, the first exact target witness occurs at horizon 3.

Every `LR` and `RL` candidate with `t<=3` must fail. A pass would imply `X_t subset X_j` with all earlier slices target-safe, contradicting the known horizon-3 witness.

Any control failure blocks primary evaluation.

## Frozen primary domain

Use exactly the **22 distinct `(rule,seed)` languages** underlying the **170 Research034 survivor questions**:

- target-question split: **158 Class II + 12 Class III**;
- frontier rules: `{122,154,161,164,166,180,210,218}`;
- all twelve Rule-122/161 questions retained as sentinels.

Reconstruct the domain from the committed Research034 algorithm and assert those totals before interpreting outcomes. Do not add or remove a seed language after primary evaluation begins.

## Frozen fresh candidate family

For every frontier seed language test exactly:

\[
2\le t=k+j\le6,
\]

with

- `k>=1`;
- `j>=1`;
- `delta in [-k,k]`;
- `policy in {LR,RL}` only.

Candidate order is frozen as:

1. increasing `t`;
2. increasing `j` (therefore decreasing `k` within fixed `t`);
3. `delta` ordered by `(abs(delta),delta)`;
4. `LR` before `RL`.

Stop a seed-language search at the first passing fresh candidate. A non-certified language must exhaust every candidate unless censored.

The disclosed `LL/RR` family is not part of the fresh primary count and is not searched on frontier seeds by the primary instrument.

## Frozen resource envelope

Reuse the successful Note-037 symbolic envelope:

- maximum nonterminal MDD nodes in any one output-position check: **5,000,000**;
- maximum variables in one MDD: **13** (`t<=6`);
- maximum wall time per frontier seed language: **20 minutes**.

Crossing a ceiling is **censoring only**. Do not raise a limit after learning which seed/rule hits it.

Seed-language status:

- `phase-splice-certified`: first exact `LR/RL` candidate passes;
- `no-phase-splice-through-6`: every frozen fresh candidate fails exactly;
- `censored`: no candidate passes and some candidate is unevaluated because a resource ceiling was reached.

## Frozen primary hypothesis

Before evaluating any frontier seed under `LR/RL`:

> **At least one of the 22 Research034 frontier seed languages admits an exact cross-phase source-recoder certificate with `k+j<=6`.**

A complete zero is useful. It would show that merely exploiting the one-defect graph's left/right phase is still insufficient, despite allowing changed provenance and despite the MDD representation itself being tractable in Note 037.

No prediction is frozen for the Rule-122/161 sentinels or for the number of resolved target questions.

## Measurements

For every seed language record:

- rule, Wolfram class, seed pair and attached target IDs;
- number of fresh candidates tested;
- first exact passing `(t,k,j,delta,policy)`, if any;
- first failing output position and scalar-replayed background counterexample for each failed candidate, compacted in the publication result;
- maximum MDD nodes observed;
- elapsed wall time;
- censoring point/reason, if any.

Aggregate:

- certified seed languages;
- exact permanence resolutions among the 170 target questions;
- unresolved and censored languages/questions;
- class breakdowns;
- certificate parameter distribution;
- Rule-122/161 sentinel outcomes;
- symbolic cost compared with Note 037 and Note 036.

## Independent audit of a fresh success

If any `LR/RL` frontier candidate passes, freeze the first canonical success immediately.

Before publication, write an independent Boolean/SAT or scalar exhaustive audit that does **not** import the production MDD builder. For every required output position, encode the negation of the phase-splice identity over the exact finite fine-ECA causal cone and prove it UNSAT. Replay any SAT model scalarly.

A disagreement invalidates the certificate and blocks publication.

If all fresh candidates fail exactly, no positive-outcome audit is required beyond the Rule-5 and Rule-35 semantic controls.

## Interpretation boundaries

- A pass proves exact slice inclusion and, using the imported h<=6 safety result, exact all-time permanence for attached targets.
- A failed candidate refutes only that specific phase-splice recoder.
- Exhausting `LR/RL` does not refute `LL/RR`, arbitrary rail-selection masks, local repair functions, nondeterministic transducers, or general exact orbit inclusion.
- The source-graph phase is latent proof state, not a new physical degree of freedom in the CA.
- Censoring is representational cost, not dynamical evidence.
- No Class-IV, dimensional-lift, or arbitrary-CA claim is tested here.

## Decision rule

- If fresh cross-phase certificates appear, characterize how the latent pre/post-seed state chooses different source histories and compare the resulting closure with the Note-036 graph oracle.
- If the complete fresh family yields zero uncensored certificates, broaden the recoder from one phase cut to an exact **finite rail-selector mask** or synthesized local repair transducer while retaining the same source-language theorem.
- If symbolic MDD cost censors hard seeds, preserve the recoder family and freeze a SAT/BDD backend recovery rather than raising the node ceiling.
- Do not return to explicit projected sofic graphs or blindly increase context width.
