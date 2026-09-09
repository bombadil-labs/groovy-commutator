# The local variables arrive before the state does

Research029 identifies the **future-context quotient** as the unique coarsest uniform local representation sufficient for a complete future target. That result is exact, but apparently post-hoc: it assumes the entire future-equivalence partition is already known.

Research030 asks a more constructive question:

> **How much future must be observed before the final local representation is already determined?**

The answer on the exact block-3 ECA domain is unexpectedly sharp. The final local quotient is discovered before the full global predictive state closes in more than three quarters of nonclosed cases. Its discovery takes at most **two macrosteps in every one of 30,856 cases**, even though global history depth reaches 23. Every one of the 672 long-memory cases with `h* >= 10` discovers its final local quotient after exactly **one** macrostep.

This separates two dynamical timescales that the earlier research had treated together:

1. **representation discovery** — learning which local distinctions the future can ever require;
2. **state resolution** — learning enough history to determine which global predictive state the system is currently in.

The first can finish almost immediately while the second remains long.

## Finite-horizon future-context quotients

Fix deterministic dynamics `E`, cadence `q`, and target observation `T`. Write

\[
Y_t=T(E^{qt}(S)).
\]

Let

\[
C_h(S)=(Y_0(S),Y_1(S),\ldots,Y_h(S))
\]

be the finite observed-future word through horizon `h`.

For a local alphabet `A`, define two local symbols `a,b in A` to be **horizon-h context equivalent** when replacing `a` by `b` in any block position and every exact surrounding local context leaves `C_h` unchanged. Quotient the local alphabet by that equivalence:

\[
Q_h=A/{\equiv_h}.
\]

`Q_h` is therefore the coarsest uniform local representation sufficient to reproduce the target future through horizon `h`.

The final quotient from Research029 is

\[
Q_\infty=A/{\equiv_\infty}.
\]

Define the **quotient discovery time**

\[
d_Q=\min\{h:Q_h=Q_\infty\}.
\]

Compare this with `h*`, the history depth at which the complete global target-future partition stops refining.

## Exact monotone-certification theorem

The finite-horizon construction has a useful property that does not depend on ECA, block size three, or the empirical census.

As the target horizon grows, distinctions can be added but never revoked:

\[
\equiv_{h+1}\subseteq\equiv_h,
\]

or equivalently the quotient chain refines monotonically,

\[
Q_0\preceq Q_1\preceq Q_2\preceq\cdots\preceq Q_\infty.
\]

Because the complete future partition stabilizes at `h*` on a finite deterministic system,

\[
\boxed{d_Q\le h^*.}
\]

More importantly, `Q_h` gives a **one-sided sound certificate** for representation repair. If the currently observed quotient already refines a candidate encoder `Z`,

\[
Q_h\preceq Z,
\]

then every later quotient refines `Q_h`, so

\[
Q_\infty\preceq Z.
\]

Thus `Z` is guaranteed sufficient for the complete future. The certificate cannot later be revoked.

Conversely, every finally sufficient uniform local encoder is certified by horizon `h*` at the latest.

So `Q_h` is not merely an approximation to a hidden final answer. At each horizon it is already the **unique coarsest uniform local representation sufficient for everything seen through that horizon**, and its refinement chain is a monotone sequence of certified necessities.

The full proof is in `docs/research/proofs/finite-horizon-context-quotients.md`.

## Exact census

The frozen census reuses the complete Research028–029 block-3 domain:

- all 256 elementary cellular automata;
- periodic ring width `n=12`;
- nonoverlapping three-cell blocks;
- matched cadence `q=3`;
- all 127 canonical nonconstant binary block-3 targets;
- all 4,096 microscopic states per rule;
- exact finite target words and exact surrounding-context substitution.

There are 32,512 `(rule,target)` cases. Of these, 1,656 are already closed and 30,856 are nonclosed.

The full census, exact aggregation, independent audit, and fresh-size confirmation ran green in Actions run `34327714933`. The exact compact outputs are committed in:

- `results/finite_horizon_quotients_20260909_summary.json`;
- `results/finite_horizon_quotients_20260909_audit.json`;
- `results/finite_horizon_quotients_n15_20260909.json`.

## Finding 1: local representation usually arrives early

Among the 30,856 nonclosed targets,

\[
\boxed{23,588/30,856=76.4454\%}
\]

have

\[
d_Q<h^*.
\]

In other words, more than three quarters of cases have already discovered every local distinction that will ever be required **before** the global observed history has finished resolving the predictive state.

The median ratio is

\[
\boxed{\operatorname{median}(d_Q/h^*)=1/3},
\]

with mean approximately `0.4783`.

This is not merely a weak lead near the end of the trajectory. The final quotient is already reached by half of the eventual history depth in

\[
\boxed{23,252/30,856=75.3565\%}
\]

of nonclosed cases.

## Finding 2: representation discovery is uniformly shallow here

The most surprising bounded result is the absolute depth:

\[
\boxed{d_Q\in\{1,2\}\text{ for every nonclosed case}.}
\]

Specifically,

- `d_Q=1` for 29,480 cases;
- `d_Q=2` for 1,376 cases;
- no nonclosed case requires horizon 3 or later to discover its final local quotient.

By contrast,

\[
\max h^*=23.
\]

The four maximal-memory cases all have `h*=23` but `d_Q=1`. Their final local quotient is the full eight-symbol identity after one macrostep; the remaining 22 history steps distinguish **global configurations of already-known variables**, not new kinds of local variable.

This gives the cleanest form of the timescale separation:

> **Long predictive memory need not mean slow representation discovery.**

## Finding 3: all long-memory cases discover the quotient immediately

There are **672** nonclosed targets with

\[
h^*\ge10.
\]

Every one satisfies

\[
\boxed{d_Q=1<h^*.}
\]

Their median ratio is

\[
\operatorname{median}(d_Q/h^*)=1/11\approx0.0909.
\]

Two preregistered sentinels make this concrete at `n=12`:

- Rule 101, target `00000010`: `h*=23`, `d_Q=1`;
- Rule 106, target `00000001`: `h*=19`, `d_Q=1`.

The local alphabet has finished learning what distinctions matter after one observed macrostep, while the global predictive state remains unresolved for dozens of steps.

## Finding 4: representation information itself arrives early

Quotient equality is a strict all-or-nothing criterion, so the protocol also tracks how much of the final local representation entropy has become certified by each horizon.

At least half of the final added representation information is certified **strictly before half of `h*`** in

\[
\boxed{18,094/30,856=58.6401\%}
\]

of nonclosed cases.

This matters because early quotient discovery is not only a consequence of tiny final quotients. Much of the actual information content of the eventual representation is often established early in the predictive history.

## Exploratory Wolfram-class split

The timing effect is present across the repository's conventional classes, but becomes especially strong in the complex/chaotic labels:

| Class | Nonclosed targets | `d_Q<h*` | Half representation information before `h*/2` |
| --- | ---: | ---: | ---: |
| I | 2,254 | 70.28% | 51.82% |
| II | 23,528 | 72.19% | 52.02% |
| III | 3,296 | 98.36% | 88.23% |
| IV | 1,778 | **100%** | **100%** |

For Class IV the median `d_Q/h*` is `1/6`.

This is exploratory taxonomy, not a new Wolfram-class classifier. The exact claim is only the stated finite census. Still, it reinforces an emerging pattern: systems with long or rich observed futures can expose the **type of local distinction they need** very quickly even when those distinctions continue interacting for a long time.

## Fresh-size confirmation

A frozen `n=15` check evaluated six selected cases without reselecting targets after inspection. The primary long-memory prediction passed:

| Rule | Target | `h*` at `n=15` | `d_Q` | `d_Q/h*` |
| ---: | --- | ---: | ---: | ---: |
| 101 | `00000010` | 18 | **1** | 0.0556 |
| 106 | `00000001` | **36** | **1** | 0.0278 |
| 110 | `00000100` | 14 | **1** | 0.0714 |
| 90 | `00110011` | 2 | 2 | 1.0 |
| 24 | `01000010` | 1 | 1 | 1.0 |
| 184 | `00000001` | 2 | 1 | 0.5 |

Rule 106 is especially informative. Going from `n=12` to `n=15` makes the global target history substantially longer for this selected target, yet the quotient discovery time remains one macrostep:

\[
h^*:19\to36,
\qquad
 d_Q:1\to1.
\]

That is exactly the kind of decoupling Research030 was designed to test.

## Relation to Research029

Research029 solves the **final representation** problem: given the complete future label, the future-context quotient is the unique coarsest sufficient uniform local representation.

Research030 adds a temporal structure to that quotient:

\[
Q_0\preceq Q_1\preceq\cdots\preceq Q_\infty.
\]

Each newly separated pair of local symbols has a **birth time**: the first horizon at which some exact context proves that the future can distinguish them.

This recasts representation learning as accumulation of counterexamples to local interchangeability. A distinction need not be represented because it looks intrinsically important; it becomes mandatory when the observed future supplies a context in which substituting one local symbol for another changes the target word.

That makes the connection to Research028's predictive synergy sharper. The Rule-24 zero-gain bridge is not mysterious from the final quotient's point of view: the symbols must eventually be distinct. Research030 asks when the future first provides enough evidence to certify that necessity.

## Representation discovery versus state estimation

The main conceptual result is a separation that is easy to blur if one looks only at history depth.

A predictive state has to answer:

> **Which future-equivalence class am I in?**

A local representation has to answer:

> **Which kinds of local distinction can ever matter to those future classes?**

Research030 shows that the second question can settle dramatically earlier than the first.

A system can therefore have:

- a stable local vocabulary;
- long unresolved global history;
- continuing dynamics among already-certified local variables.

This suggests that long memory can arise from **composition and arrangement of variables whose identities are already known**, rather than from continuously discovering new primitive variables.

## What this does not establish

- `d_Q<=2` is an exact property of this finite block-3 ECA census, not a universal theorem.
- The monotone finite-horizon certification theorem assumes exhaustive exact surrounding contexts. It does not yet tell us how to certify equivalence from sparse samples.
- The quotient is uniform and local. Relational, stateful, adaptive, or nonuniform representations may have different discovery dynamics.
- The uniform full-state ensemble fixes the representation-information weighting used in the entropy curves.
- The Wolfram-class split is exploratory.
- Early local quotient discovery does not imply that prediction itself is easy; the entire point is that `h*` can remain large.

## Next question

The exact finite-horizon quotient still uses every local context. The next real learning problem is therefore:

> **Can we discover or certify the quotient from incomplete context evidence without mistaking “not yet distinguished” for “safe to merge”?**

A naive sampler cannot make that inference: absence of a witnessed distinction is not evidence of equivalence. The one-sided theorem suggests a safer direction—maintain conservative candidate distinctions and use targeted context queries or counterexample-guided refinement until a merge has a structural coverage certificate.

That begins to resemble active automata learning or CEGAR, but with the object being a local predictive quotient of dynamical futures rather than a transition machine supplied directly by an oracle.

The important new constraint is now clear: **learning the representation should exploit the fact that the local vocabulary may stabilize long before the full predictive state does.**
