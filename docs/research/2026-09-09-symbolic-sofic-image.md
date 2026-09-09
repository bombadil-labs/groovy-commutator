# Symbolic recurrence clears the representation wall but not the frontier

> **Publication identity.** This work was preregistered, implemented, and evaluated under the number-independent slug `symbolic-sofic-image`. After the result was frozen, the shared catalog assigned it **Note 037**. The frozen protocol bytes and hashes are unchanged.

Note 036 ended at an awkward but useful boundary. The exact one-defect orbit is a mathematically legitimate sofic object, and finite orbit containment gives an exact all-time permanence certificate. But every one of the 170 remaining Research034 questions censored under the frozen explicit graph representations.

The immediate temptation was to build a more compact graph.

This checkpoint takes a narrower route first: avoid projected image graphs entirely and ask whether the orbit closes for the simplest possible symbolic reason — **ordinary temporal recurrence of the underlying macro cellular automaton**.

The answer is cleanly negative on the frontier.

\[
\boxed{170/170\text{ evaluated},\quad 0\text{ recurrence certificates},\quad 0\text{ censored}.}
\]

That negative matters because the symbolic machinery itself does **not** hit the Note-036 representation wall. The missing closure mechanism is therefore more relational than ordinary temporal periodicity or translation.

## One half of the problem was already symbolic

Research032 represents the exact horizon-`h` local map

\[
F_h:A^{2h+1}\to A,
\qquad |A|=8,
\]

with a reduced ordered 8-valued decision diagram. For a changed input symbol, two restricted diagrams are traversed under the same remaining background assignments. This decides exactly whether a target-visible output pair is possible without enumerating the full light-cone word space.

The horizon-6 MDD run censored six rules at its frozen five-million-node ceiling, but four of them were already permanently safe by the target-congruence certificate. The remaining twelve Rule-122/161 cases were then independently proved horizon-6 invisible by both Z3 and PySAT shrinking-cone encodings.

So finite target visibility through horizon 6 was not the missing part of Note 036. The unresolved problem was **exact orbit inclusion**.

## The strongest cheap closure certificate

Let `G` be the exact radius-one macro CA induced by three fine ECA ticks on aligned three-cell blocks. Write

\[
X_h(s)=\widehat G^h(X_0(s))
\]

for the exact paired one-defect time slice associated with hidden seed `s`.

The frozen protocol tests exact identities

\[
R(h,j,\delta):\qquad G^h=\sigma^{\delta}G^j,
\qquad 0\le j<h,
\]

where `sigma` is spatial translation.

If such an identity holds, then the paired map satisfies the same identity. Since every `X_j(s)` is shift invariant,

\[
X_h(s)
=
\sigma^{\delta}X_j(s)
=
X_j(s).
\]

Thus the new slice is already contained in the accumulated earlier orbit. If the earlier slices are target-safe, Note 036's exact orbit argument gives

\[
\boxed{w_T(a,b)=\infty.}
\]

This is a strong sufficient certificate. It asks the **same source provenance** to return to an earlier output map, up to translation. General language inclusion does not require that.

## Rule 5 reveals the mechanism exactly

The positive control was the Rule-5 permanence mechanism already seen by Research034 and Note 036.

For Rule 5 / target `01001100` / seed `0-2`, the exact sofic control had found closure at transition index 2:

\[
X_3\subseteq X_0\cup X_1\cup X_2.
\]

The symbolic recurrence test finds a stronger rule-level identity:

\[
\boxed{G^3=G.}
\]

So in fact

\[
X_3=X_1
\]

for every one-defect seed, not merely for the Rule-5 control language.

This was independently checked by scalar evaluation of all

\[
8^7=2,097,152
\]

seven-symbol macro contexts. Every context gives the same center output after three macrosteps as after one macrostep.

The graph closure was therefore hiding a much smaller proof object: ordinary temporal recurrence of the local rule.

## Rule 35 blocks false closure

The negative control is Rule 35 / target `00000001` / seed `2-6`, whose first genuine causal witness occurs at macro-horizon 3.

The recurrence search finds no identity `R(h,j,delta)` through horizon 3 that could close the orbit before that witness, while the Research032 symbolic witness query still detects the known horizon-3 event.

So the recurrence instrument reproduces both sides of the intended semantics: it can compactly prove a known closure without erasing a known witness.

## Frozen frontier

The primary domain is exactly the 170 Research034 survivors:

- **158 Class II** questions;
- **12 Class III** questions;
- **22** distinct one-defect seed languages.

Those 170 questions occur in only eight ECA rules:

| rule | class | questions | seed languages | h6 MDD nodes |
| ---: | :---: | ---: | ---: | ---: |
| 122 | III | 6 | 6 | 1,142,614 |
| 154 | II | 31 | 1 | 807 |
| 161 | III | 6 | 6 | 1,142,614 |
| 164 | II | 17 | 3 | 9,702 |
| 166 | II | 31 | 1 | 807 |
| 180 | II | 31 | 1 | 2,337 |
| 210 | II | 31 | 1 | 2,337 |
| 218 | II | 17 | 3 | 9,702 |

For every frontier rule, the frozen search tests all

\[
1\le h\le6,
\qquad 0\le j<h,
\qquad |\delta|\le h+j.
\]

The translation range is complete for this certificate family: outside it the two dependency intervals are disjoint, so equality for all full-shift inputs would force both local functions to be constant, a recurrence already visible at zero translation.

## Primary result: a genuine negative

The preregistered hypothesis predicted that at least one of the 170 questions would receive an exact permanence certificate from temporal recurrence by horizon 6.

It fails.

\[
\boxed{
\begin{aligned}
\text{temporal-recurrence certificates}&=0,\\
\text{unresolved after the test}&=170,\\
\text{censored}&=0.
\end{aligned}}
\]

All eight frontier rules complete every declared recurrence comparison through horizon 6.

This is not the kind of null result Note 036 produced. There, the hypotheses remained unevaluated because the proof objects hit frozen resource ceilings. Here the symbolic representation completes the test and the mathematical condition simply does not hold.

## The representation wall is actually cleared

The worst horizon-6 local function occurs for Rules 122 and 161:

\[
1,142,614
\]

reduced MDD nodes, comfortably below the inherited five-million-node ceiling.

The largest synchronized equality traversal visits only

\[
633
\]

paired symbolic states, for Rule 164 when comparing horizon 6 with horizon 5 at zero translation.

By contrast, Note 036's raw exact graph control already required 6,029,312 higher-block transitions merely to construct the known Rule-35 horizon-3 slice.

So this checkpoint separates two claims that were still entangled after Note 036:

1. **Can the relevant exact local dynamics be represented compactly enough to compute with?** Here, yes.
2. **Does simple temporal recurrence give the needed exact orbit inclusion?** On the 170-case frontier through horizon 6, no.

A compact exact local function is not yet a compact reachability certificate.

## Why same-provenance recurrence was always restrictive

There is a deeper reason this certificate family is only a first step.

The exact one-defect language includes its all-diagonal topological-closure branch. On that branch the two paired components are identical, but the common background is otherwise an arbitrary configuration in `A^Z`.

Therefore any proposed **same-source** identity strong enough to hold for the whole exact one-defect shift must already hold as an identity of the underlying full-shift macro CA. The source language cannot rescue an identity that fails on arbitrary diagonal backgrounds.

General sofic inclusion is more permissive. To prove

\[
X_h(s)\subseteq X_0(s)\cup\cdots\cup X_{h-1}(s),
\]

an output at time `h` may be represented by an earlier slice using a **different initial source row**. It need not come from the same provenance.

That is exactly what temporal recurrence refuses to allow.

## The next proof object must change provenance

The next target is therefore not a larger MDD and not a larger explicit graph.

It is a constructive **source recoder** or relational transducer. A first exact candidate is a finite-state map

\[
P:X_0(s)\to X_0(s)
\]

such that, for some `j<h`,

\[
\widehat G^h(x)
=
\widehat G^j(Px)
\]

for every source path `x` in the exact one-defect presentation.

Such a certificate would prove inclusion by explicitly re-presenting every new output through an earlier slice, while allowing the earlier representation to have different latent provenance.

The two-state one-defect source graph gives this search a natural finite-state substrate: diagonal background loops, one defect transition, and latent left/right phase. A graph endomorphism, letter-to-letter transducer, or slightly richer finite-state relation can exploit that state without ever projecting the reachable image into a giant follower graph.

If that family is still too restrictive, the natural endpoint is a two-tape simulation relation between source presentations: prove earlier-slice representation existentially while retaining the latent source automaton on both tapes.

## What this checkpoint establishes

Within the declared block-3/cadence-3 ECA macro family:

1. Research032 already supplies exact symbolic finite-witness queries through the relevant horizon-6 frontier, including independent recovery of the hard Rule-122/161 cases.
2. Exact temporal recurrence gives a valid all-time orbit-closure certificate without materializing sofic image graphs.
3. The Rule-5 control has the stronger exact identity `G^3=G`, independently verified on all 2,097,152 relevant contexts.
4. The Rule-35 control has no premature recurrence and retains its genuine horizon-3 witness.
5. All 170 Research034 frontier questions complete the frozen recurrence search through horizon 6 with zero censoring.
6. None receives a recurrence certificate.
7. The largest horizon-6 symbolic local function has 1,142,614 MDD nodes and the largest equality query visits 633 paired states.

The 170 questions therefore remain dynamically unclassified. The gain is a sharper localization of the proof problem:

> **Exact symbolic dynamics is tractable here; exact reachability now requires a relational proof object that can change source provenance.**

That is the next frontier.