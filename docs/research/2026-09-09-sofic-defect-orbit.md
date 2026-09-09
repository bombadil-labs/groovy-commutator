# Exact reachability hits a representation-complexity wall

> **Publication identity.** This checkpoint is **Note 036**, with canonical slug `sofic-defect-orbit`. A temporary prepublication number collided with a parallel research note and was normalized before publication. Immutable Git history and the recorded frozen source hashes preserve the preregistration; there is no alternate internal note number.

Research034 ended with a small but stubborn frontier:

\[
\boxed{170}
\]

pair/target distinctions remained unresolved after all-context congruence, nearest-neighbor grammar, and width-3 reachable-language certificates.

The obvious next idea was not another fixed window. It was to represent the **exact one-defect orbit** as a sofic shift.

That idea is mathematically sound. It also exposes a new boundary:

> **The exact reachable language can have a finite-state description in principle while the obvious exact presentations become too large to use as proof objects.**

Research036 therefore does not resolve the 170 dynamical questions. It localizes why the first exact-sofic attempt cannot yet evaluate them.

## The exact criterion

The one-defect initial set has a two-state labeled-graph presentation: arbitrary diagonal symbols before and after one hidden seed transition.

A radius-1 CA maps a sofic shift to another sofic shift through the standard higher-block image construction. Write

\[
X_t=\widehat g^t(X_0)
\]

and

\[
U_t=\bigcup_{j=0}^{t}X_j.
\]

The proof in

`docs/research/proofs/sofic-defect-orbit.md`

shows that if

\[
X_{t+1}\subseteq U_t,
\]

then

\[
\boxed{\widehat g(U_t)\subseteq U_t.}
\]

If the accumulated exact orbit is target-safe, this gives

\[
\boxed{w_T(a,b)=\infty.}
\]

without any fixed-window overapproximation.

Conversely, a target-visible label in an exact time slice is an actual finite witness.

So the scientific question is well posed. The problem encountered here is representation cost.

## The frozen controls work

Before the 170-case census, the first implementation was required to reproduce two known mechanisms.

### Rule 35: real third-step witness

For Rule 35 / target `00000001` / seed `2-6`, exact sofic slices remain invisible at horizons 0, 1, and 2 and first become target-visible at horizon 3, reproducing Research031.

### Rule 5: exact permanent orbit closure

For Rule 5 / target `01001100` / seed `0-2`, Research034 had already proved permanence with a width-3 grammar.

The exact sofic control remains invisible and, more strongly, finds a finite orbit stabilization at transition index 2: the next exact slice is already contained in the accumulated prior slices.

Thus the exact-sofic criterion is not merely formal. On a tractable permanent case it can replace a large local word grammar with finite automaton memory.

## Primary run: complete censoring

The frozen primary domain was all 170 Research034 survivors through macro-horizon 12. Horizons 7–12 were fresh for deeper-witness discovery.

The complete exact primary run is preserved in

`results/sofic_defect_orbit_20260909.json`.

It resolves **zero** cases because all

\[
\boxed{170/170}
\]

are censored before the frozen resource envelope can evaluate them.

The censoring breakdown is:

- compressed-graph state ceiling: **62** questions;
- determinization subset-state ceiling: **46**;
- image-pair-state ceiling: **62**.

Censoring occurs at transition indices:

- 0: **12** questions;
- 1: **34**;
- 2: **62**;
- 3: **62**.

Therefore both preregistered hypotheses remain

\[
\boxed{\text{inconclusive due to censoring}.}
\]

The zero observed resolutions are not failures of the hypotheses.

## Recovery 1: remove eager orbit-union determinization

The first recovery was frozen only after the complete censoring pattern was known.

The primary implementation determinized and compressed the cumulative union

\[
U_t=X_0\cup\cdots\cup X_t
\]

after each step. But this is unnecessary: a disjoint union of the exact slice graphs already presents the union exactly, and the inclusion oracle accepts nondeterministic graphs.

The lazy-union recovery therefore keeps the accumulated orbit as

\[
G_0\sqcup G_1\sqcup\cdots\sqcup G_t
\]

and determinizes only on demand inside the exact inclusion query.

The committed result is

`results/sofic_defect_orbit_lazy_20260909.json`.

Again:

\[
\boxed{170/170\text{ censored}.}
\]

But the location changes completely:

\[
\boxed{\text{all 170 censor at exact slice-image construction}.}
\]

This recovery is diagnostically successful. It eliminates cumulative-orbit representation as the active bottleneck.

## Recovery 2: stop determinizing the physical slices

The next frozen recovery asked whether right-resolving determinization of each time slice was itself the problem.

It kept the exact higher-block image as a raw nondeterministic graph and retained the lazy orbit union. No primary survivor was allowed to run until the raw presentation reproduced the known Rule-35 and Rule-5 controls under the frozen image ceilings.

It does not clear that gate.

The post-outcome diagnostic in

`results/sofic_defect_orbit_raw_control_20260909.json`

changes no threshold and gives the exact growth on **both** controls:

| horizon | raw states | raw edges |
| ---: | ---: | ---: |
| 0 | 2 | 17 |
| 1 | 144 | 1,216 |
| 2 | 10,240 | 86,016 |

Constructing horizon 3 requires

\[
\boxed{6,029,312}
\]

raw higher-block transitions, crossing the preregistered 5,000,000-transition ceiling.

For Rule 35 this is especially informative: the raw presentation becomes operationally censored **exactly while trying to construct the already-known horizon-3 witness**.

Rule 5 has the same raw presentation counts and hits the same boundary, despite its exact orbit being known to stabilize under the compressed control.

So simply replacing determinization with nondeterminism is not the answer.

## Three exact presentations, three lessons

The recovery sequence separates three sources of proof-object growth.

### 1. Eager union compression was unnecessary

Lazy union removes it completely, yet the 170-case censoring remains.

### 2. Right-resolving slice compression can explode

The primary hard cases generate tens of thousands of deterministic follower states after one macrostep.

### 3. Raw higher-block slices can explode too

Avoiding determinization trades follower-state explosion for explicit transition explosion. Even the known h3 control requires more than six million raw transitions.

The important distinction is therefore

\[
\boxed{\text{dynamical reachability complexity}\neq\text{presentation complexity}.}
\]

A finite exact sofic object exists at every fixed time. That does not mean the most literal graph presentation is the right computational representation of it.

## Relation to the finite-window hierarchy

Research033–034 progressively removed false causal possibilities by remembering more spatial composition:

\[
5360
\xrightarrow{\text{edges}}
228
\xrightarrow{\text{3-words}}
170.
\]

The sofic line attacks the same problem from the other side. Instead of retaining a wider local window, it tries to retain **stateful context** exactly.

The Rule-5 control shows why that remains promising: finite automaton state can prove exact orbit closure. The hard frontier shows why a naive explicit automaton is not yet enough.

A successful next representation probably needs both virtues:

- symbolic local constraints rather than enumerated higher-block transitions;
- latent automaton state rather than an ever-wider fixed spatial window.

## Parallel program: a related representation problem, not the same proof target

While this branch was running, the repository split its living synthesis into two parallel Programs.

[Dimensional Closure and the Commutator Lift](2026-09-09-dimensional-closure-program.md) asks whether noncommutation can be promoted into additional spatial coordinates so the enlarged dynamics closes.

This Program, [Dynamics of Erased Distinctions](2026-09-08-dynamics-of-erased-distinctions.md), asks which erased distinctions can matter again and what representation is sufficient to track them.

There is a real structural rhyme: both encounter a failure of a current representation and ask what extra state would make the relevant dynamics close. But Research036 is evidence only for the erased-distinction/reachability line. It does not establish a spatial realization of the commutator lift, and the dimensional program does not solve the sofic image problem.

Keeping the Programs separate lets that analogy remain useful without becoming a hidden premise.

## What is exact now

Within the declared block-3/cadence-3 paired ECA setting:

1. the one-defect initial language has an exact finite labeled-graph presentation;
2. every fixed-time CA image is exactly sofic;
3. finite orbit stabilization gives an exact all-time permanence certificate;
4. the Rule-35 control reproduces the known horizon-3 witness under the compressed exact presentation;
5. the Rule-5 control reaches an exact finite sofic orbit closure;
6. the primary 170-case run is completely censored under its frozen exact graph ceilings;
7. lazy union proves cumulative-union determinization is not the active bottleneck;
8. the raw-NFA control proves that removing determinization alone exposes a >6M-transition higher-block image before horizon 3.

## What remains unresolved

- None of the 170 Research034 survivors is classified by this checkpoint.
- The two original sofic hypotheses remain unevaluated because of complete censoring.
- No horizon-7+ witness is established.
- No finite sofic closure is established for a member of the 170-case frontier.
- No universal statement is made about the state complexity of CA images of sofic shifts.

## Next target: symbolic image, not more graph

The next step should **not** raise the frozen ceilings, blindly test width 4, or materialize still larger higher-block graphs.

The missing object is an exact symbolic representation of the sliding-block image—something closer to a transducer, decision diagram, symbolic relation, or target-aware quotient that can answer reachability and inclusion questions without enumerating every follower subset or every higher-block transition.

The new question is:

> **Can the exact image of the one-defect sofic shift be carried symbolically across time while preserving enough structure to decide target visibility and orbit inclusion?**

That is now the narrow computational/theoretical frontier.
