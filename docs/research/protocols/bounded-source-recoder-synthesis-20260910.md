# Protocol: bounded adaptive source-recoder synthesis — 2026-09-10

**Status:** frozen before evaluating any Research034 frontier seed under this synthesized recoder class.
**Working identity:** `bounded-source-recoder-synthesis`; no public note number is assigned until publication.
**Role:** final substantive checkpoint of the Dynamics of Erased Distinctions research program.

## Motivation and terminus

The exact one-defect permanence program has now separated finite visibility from all-time closure and tested increasingly permissive constructive recoders. Same-source temporal recurrence failed exactly through horizon 6. Cross-phase one-cut recoding then failed exactly on all 22 Research034 frontier seed languages after SAT recovery removed the MDD censoring. A hand-designed two-switch `LRL/RLR` family is being terminalized separately under its already-frozen resource envelope.

This checkpoint deliberately does **not** introduce three-switch, four-switch, or other bespoke geometries. It replaces hand-authored selector shapes with a bounded adaptive finite-state recoder and is the final recoder-family search in this program.

The question is:

> **Can a small amount of adaptive proof state choose between the two evolved source histories so that a later one-defect configuration is exactly re-presented as an earlier one?**

Whatever the outcome—certificate, exact bounded negative, or explicit computational censoring—the program proceeds to synthesis/publication rather than inventing a larger recoder family.

## Exact source and dynamics

Retain the exact block-3/cadence-3 macro CA

\[
G:A^{\mathbb Z}\to A^{\mathbb Z},\qquad A=\{0,\ldots,7\},
\]

and a one-defect source pair with ordered seed `s=(a,b)`, `a<b`, at the origin. For `k>=1`, evolve both scalar rails:

\[
z^L=G^k(x^L),\qquad z^R=G^k(x^R).
\]

They agree outside the finite defect cone `[-k,k]`.

As before choose `j>=1`, `t=k+j<=6`, and seed displacement `delta in [-k,k]`. The recoder produces a new member of `X_0(s)` and asks whether

\[
\widehat G^t(x)=\widehat G^j(P(x))
\]

for every genuine one-defect source row. The all-diagonal closure branch is handled by the same trivial evolved-background construction used in the phase-splice theorem.

## Bounded adaptive rail-selector machine

For a state budget `m`, let

\[
Q_m=\{0,\ldots,m-1\},\qquad 1\le m\le4.
\]

A candidate machine consists of two deterministic tables:

\[
\lambda:Q_m\times A^2\to\{L,R\},
\]

\[
\tau:Q_m\times A^2\to Q_m.
\]

The latent defect position provides the scan anchor. Initialize `qstate=0` at spatial position `-k` and scan the active evolved cone from left to right through `-k,-k+1,...,k`.

At each position `q`:

1. read the exact evolved paired symbol `v_q=(z^L_q,z^R_q)`;
2. if `q != delta`, set the common recoded background symbol to `z^L_q` when `lambda(qstate,v_q)=L`, otherwise `z^R_q`;
3. if `q == delta`, emit the original ordered seed `(a,b)` instead of a diagonal symbol;
4. in either case update `qstate <- tau(qstate,v_q)`.

Outside `[-k,k]` the evolved rails are equal, so the recoded common background is their shared value and no machine decision is needed.

Every machine therefore maps the genuine one-defect branch into `X_0(s)` by construction. Internal machine state is **proof state**, not an added physical degree of freedom in the CA.

The class is adaptive: unlike a fixed cut or island, rail choice may depend on the locally encountered evolved pair and on bounded left-to-right history.

## Certificate theorem

A synthesized machine is an exact certificate for `(m,t,k,j,delta,s)` iff for every one-defect source row `x`,

\[
\widehat G^t(x)=\widehat G^j(P_{m,k,delta}(x)).
\]

Then

\[
X_t(s)\subseteq X_j(s),
\]

and because `j<t`, the Note-036 orbit argument closes the accumulated orbit whenever the earlier slices are target-safe. Research032 plus its horizon-6 recovery supplies that safety for every incoming Research034 frontier target in the frozen range.

Thus one passing machine gives exact all-time permanence for every still-unresolved target attached to that seed language.

## Exact CEGIS synthesis

Machine existence is an `exists machine / forall background` problem. Use counterexample-guided inductive synthesis (CEGIS), with exact SAT on both sides.

For each fixed structural tuple `(m,t,j,delta)`:

1. start with an empty set of concrete source-background counterexamples;
2. **synthesis SAT:** solve for tables `lambda,tau` satisfying the recoder identity on every accumulated concrete background example and every required output position;
3. if synthesis is UNSAT, no machine in this bounded class satisfies all accumulated examples, hence none can satisfy the universal identity; record exact structural negative;
4. if synthesis returns a machine, freeze that machine for verification;
5. **verification SAT:** using the original fine ECA and symbolic arbitrary source background, search output positions in the frozen position order for any assignment on which actual and recoded paired outputs differ;
6. any SAT verifier model is scalar-replayed independently, then added to the synthesis example set;
7. if every output-position verifier query is UNSAT, the machine is an exact universal certificate;
8. iterate until certificate, synthesis UNSAT, or a frozen resource ceiling is reached.

The CEGIS loop is complete for the finite machine class if allowed to exhaust it: each verified counterexample eliminates the current machine, and the machine-table space is finite. Resource ceilings below may censor before that theoretical termination.

No MDD, projected sofic image graph, or bounded-ring surrogate may be used for primary verification.

## Fine-ECA verification semantics

Reuse the independently successful manual-CNF semantics from `phase-splice-sat-recovery`:

- source variables are fine bits;
- three fine ECA ticks implement one macrostep;
- actual and recoded paths are encoded separately but share the required source background;
- machine tables are fixed constants during universal verification;
- a SAT model means a concrete counterexample and must pass scalar replay;
- UNSAT for every required output position means exact functional equality.

Because machine state may depend on earlier active-cone symbols, a verifier may use the finite union source interval required to determine both the actual output at `p` and the machine scan from `-k` through the latest recoded dependency site. This is still a finite wrap-free causal cone; no periodic boundary is introduced.

## Frozen primary domain

Use exactly the 22 `(rule,seed)` languages underlying the 170 Research034 frontier questions, reconstructed from the canonical phase-splice domain hash already used by the two-switch instrument:

- 158 Class-II target questions;
- 12 Class-III Rule-122/161 sentinel questions;
- frontier rules `{122,154,161,164,166,180,210,218}`.

The final synthesis domain does not depend on whether the separate two-switch terminal run is exact-negative or censored.

## Frozen search order

For each seed language search:

1. increasing state budget `m = 1,2,3,4`;
2. increasing `t = 2,...,6`;
3. increasing `j = 1,...,t-1`, with `k=t-j`;
4. `delta in [-k,k]` ordered by `(abs(delta),delta)`;
5. within one structural tuple, CEGIS iterations in discovery order;
6. verification output positions use the inherited order: positions outside the reinserted seed's `j`-step future cone first, then inside, each ascending.

Stop a seed search at its first exact certificate. This order prioritizes minimum adaptive proof-state budget before temporal parameters.

## Frozen state and resource budget

- maximum machine states: **4**;
- maximum macro horizon: **6**;
- per-seed wall time: **1,200 seconds**;
- maximum CEGIS counterexamples for one structural tuple: **256**;
- synthesis CNF ceiling: **100,000 variables / 1,000,000 clauses**;
- verification CNF ceiling: **20,000 variables / 200,000 clauses**.

Crossing any ceiling without a certificate is censoring only. Do not raise a ceiling after inspecting which seed/rule hits it.

A worker/infrastructure failure is reported separately as infrastructure censoring and is never converted into a mathematical negative.

## Frozen controls

### Positive control: Rule 5

For Rule 5 / seed `0-2`, require the synthesizer at `m=1`, `t=3`, `k=2`, `j=1`, `delta=0` to find an exact certificate. The previously established all-left recoder belongs to this machine class, so absence of a certificate is an implementation failure.

The synthesized machine need not be syntactically all-left; only exact verification is required.

### Negative semantic control: Rule 35

Rule 35 / seed `2-6` / target `00000001` has its first exact target witness at macro-horizon 3. Therefore no valid source recoder can establish `X_3 subseteq X_j` for `j<3` while the earlier slices are target-safe.

Before frontier evaluation, require exact negative synthesis for state budgets `m=1,2` over the declared `(t=3,j,delta)` control tuples, or an independently equivalent complete negative control that covers those bounded machine classes. Any verified certificate is an implementation contradiction and blocks primary evaluation.

## Frozen primary hypothesis

Before evaluating any frontier seed:

> **At least one of the 22 Research034 frontier seed languages admits an exact adaptive rail-selector source-recoder certificate with at most four proof states and `t<=6`.**

Failure is scientifically useful: it would show that neither fixed low-switch provenance geometry nor bounded adaptive left-to-right rail selection is sufficient in the declared range.

## Measurements

For every seed language record:

- state budgets attempted;
- structural tuples attempted;
- CEGIS iterations and accumulated counterexamples;
- synthesis/verification SAT sizes and times;
- exact negative structural tuples;
- first certificate and complete `lambda,tau` table if any;
- scalar-replayed verifier counterexamples;
- censoring stage/reason and infrastructure censoring separately.

Aggregate:

- certified / exact-negative / censored seed languages and attached target questions;
- minimum proof-state budget of each certificate;
- certificate parameter distribution;
- CEGIS iteration distribution;
- Rule-122/161 sentinel outcomes;
- comparison with temporal recurrence, one-cut phase splice, and two-switch selectors.

## Independent audit of any positive result

Any fresh frontier certificate blocks publication until independently re-encoded with Z3 or an equivalently separate Boolean implementation that does not import the primary CEGIS/CNF builder. The independent audit must prove UNSAT for the negation of the full recoder identity at every required output position and scalar-replay any disagreement.

## Interpretation boundaries

- A certificate proves exact slice inclusion and all-time target permanence only for attached frontier targets whose earlier safety is imported from Research032.
- Exact bounded negative means only that no machine in the declared `m<=4`, rail-selection-only class works through `t<=6`.
- It does not rule out arbitrary local symbol repair, nondeterministic/transductive recoders, unbounded proof state, larger horizons, or general exact orbit inclusion.
- Censoring is computational/representational, not dynamical evidence.
- No Class-IV or dimensional-lift claim is tested here.

## Program terminus rule

This is the **last new recoder family** in the current Dynamics of Erased Distinctions program.

After this checkpoint:

1. independently audit any positive certificate;
2. retain exact negatives and censoring boundaries without escalating state/horizon/resource ceilings;
3. publish a program-level synthesis explaining visibility, permanence, representation cost, provenance repair, and bounded proof-state complexity;
4. mark the program complete/dormant with richer local repair and unbounded recoders listed as future work.

Do not respond to a negative or censored result by introducing a larger bespoke selector family in this program.