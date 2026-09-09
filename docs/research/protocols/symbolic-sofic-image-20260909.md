# Protocol: symbolic temporal-recurrence closure — 2026-09-09

**Status:** frozen before evaluating any Research034 frontier survivor under this certificate.  
**Branch:** `research/symbolic-sofic-image-20260909`.  
**Working identity:** `symbolic-sofic-image`; no public research-note number is part of this frozen protocol. Publication numbering is recorded separately after the result.  
**Dependency:** Note 036 / `sofic-defect-orbit`, Research032 symbolic causal-witness search and h=6 recovery, Research034 width-3 reachable language.

## Why this checkpoint exists

Note 036 established an exact orbit-closure criterion for the one-defect paired language, but every one of the 170 Research034 survivor questions censored under the frozen explicit graph representations. Lazy orbit union localized the active bottleneck to exact slice imaging, and a raw-NFA recovery crossed the five-million-transition ceiling while trying to construct the already-known Rule-35 horizon-3 witness.

The finite-witness half of the problem is already symbolic. Research032 represents the exact local time-`h` map by a reduced 8-ary decision diagram and asks whether two initial symbols can yield target-distinct outputs under a shared background. Its h=6 recovery independently proved the remaining twelve Rule-122/161 cases UNSAT with Z3 and PySAT.

So the new question is narrower:

> **Can an exact all-time orbit-closure certificate be obtained from symbolic local-map recurrence, without constructing the projected sofic time slices at all?**

This is deliberately a strong sufficient certificate. Failure does not reject symbolic orbit inclusion; it only rules out the simplest constructive recurrence family before a more general source recoder/transducer is introduced.

## Exact macro dynamics

For every ECA rule, block size three and cadence three induce the exact radius-one macro CA

\[
G:A^{\mathbb Z}\to A^{\mathbb Z},
\qquad A=\{0,\ldots,7\}.
\]

Let

\[
F_h:A^{2h+1}\to A
\]

be the exact local function giving the macro symbol at the origin after `h` macrosteps.

For the paired system used by Note 036,

\[
\widehat G(x,y)=(Gx,Gy).
\]

For a hidden seed pair `s=(a,b)`, let `X_0(s)` be the exact one-defect paired shift: arbitrary diagonal background, one occurrence of `s`, plus its all-diagonal topological-closure branch. Define

\[
X_h(s)=\widehat G^h(X_0(s)).
\]

## Symbolic temporal recurrence

For integers `0 <= j < h` and a spatial translation `delta`, say that the macro rule has recurrence

\[
R(h,j,\delta)
\]

when the two global maps agree exactly:

\[
G^h = \sigma^{\delta}G^j.
\]

Equivalently, for every bi-infinite macro configuration `x`,

\[
F_h(x_{-h},\ldots,x_h)
=
F_j(x_{\delta-j},\ldots,x_{\delta+j}).
\]

No sampling or bounded-ring surrogate is allowed: this is equality of the finite local functions on all assignments in the union dependency interval.

### Paired-orbit theorem

If `R(h,j,delta)` holds, then for every seed `s`

\[
\widehat G^h = \sigma^{\delta}\widehat G^j
\]

and therefore

\[
X_h(s)=\sigma^{\delta}X_j(s)=X_j(s),
\]

because every `X_j(s)` is shift invariant.

Hence

\[
X_h(s)\subseteq X_0(s)\cup\cdots\cup X_{h-1}(s).
\]

The Note-036 orbit argument then makes the accumulated orbit through `h-1` forward invariant. If those earlier slices are target-safe, the target receives the exact all-time certificate

\[
w_T(a,b)=\infty.
\]

This certificate is rule-level rather than seed-level: one recurrence may resolve several of the 170 target/seed questions at once.

## Finite translation range

For a candidate `R(h,j,delta)`, the left local map depends on `[-h,h]` and the translated right map on `[delta-j,delta+j]`.

Search exactly

\[
|\delta|\le h+j.
\]

This range is complete for this recurrence family. If the intervals are disjoint (`|delta| > h+j`) and the two functions agree for every full-shift assignment, each side must be constant because it depends on an independent variable set. In that case the same recurrence is already witnessed at `delta=0`.

Thus no larger translation can add a nonconstant recurrence missed by the declared search.

## Exact symbolic equality test

Reuse the reduced ordered 8-valued MDD representation from Research032 for each `F_h`.

For two roots built at horizons `h` and `j`, compare them by a memoized synchronous traversal while assigning each MDD variable its physical coordinate:

- horizon-`h` variable `v` has coordinate `v-h`;
- horizon-`j` variable `v` has coordinate `delta + v-j`.

At each pair of nonterminal nodes, branch on the least physical coordinate inspected by either root; a root that does not inspect that coordinate is held fixed across all eight values. Two terminal leaves are equal iff their macro symbols are identical.

The traversal returns exact equality or one explicit counterexample macro word in the union dependency interval.

Do not materialize a higher-block image graph, follower-subset graph, or projected sofic slice anywhere in the primary instrument.

## Previously known controls

The controls below are not fresh primary evidence.

### Rule 5 positive closure control

For Rule 5, the existing exact sofic control found

\[
X_3\subseteq X_0\cup X_1\cup X_2
\]

at transition index 2.

Before any frontier evaluation, require the symbolic recurrence instrument to recover the stronger identity

\[
\boxed{R(3,1,0):\quad G^3=G.}
\]

Independently audit this control by direct scalar evaluation of all

\[
8^7=2,097,152
\]

seven-symbol macro contexts, comparing the center output after three macrosteps with the center output after one macrostep.

The Rule-5 target `01001100` / seed `0-2` is already known target-safe, so this recurrence must reproduce the Note-036 finite closure mechanism without any sofic-image construction.

### Rule 35 negative/witness control

For Rule 35 / target `00000001` / seed `2-6`, Research031 and Note 036 establish first target visibility at macro-horizon 3.

Require:

1. the recurrence search finds no `R(h,j,delta)` with `1 <= h <= 3`, `j<h`, and the declared translation range that would close the orbit before the known horizon-3 witness;
2. the existing Research032 exact MDD witness query still reconstructs the horizon-3 witness.

Any contradictory recurrence is an implementation failure.

## Frozen primary domain

Use exactly the Research034 frontier:

- **170** unresolved target/seed distinctions;
- **22** distinct `(rule,seed)` one-defect languages;
- class split **158 Class II + 12 Class III**;
- the twelve Rule-122/161 questions retained as sentinels.

No case may be added or removed after recurrence outcomes are inspected.

Research032 plus its independent h=6 recovery establishes that this frontier has no finite target witness through macro-horizon 6. Therefore any exact recurrence with

\[
1\le h\le6
\]

immediately yields an all-time permanence certificate for every still-unresolved target attached to that `(rule,seed)` language.

## Frozen search

For every distinct ECA rule represented in the 22 frontier seed languages:

1. construct exact symbolic local functions `F_0,...,F_6` as needed;
2. for each `h=1,...,6`;
3. for each `j=0,...,h-1`;
4. for each integer `delta` with `|delta| <= h+j`;
5. test `R(h,j,delta)` exactly;
6. record the lexicographically first recurrence by `(h,j,abs(delta),delta)` and all recurrences found at the same earliest `h`;
7. apply that rule-level recurrence to every Research034 frontier target/seed question for the rule.

Stop building deeper horizons for a rule once a recurrence is found, because the target questions for that rule are then permanently resolved.

## Frozen resource ceilings

Retain Research032's representation ceiling:

- maximum reduced MDD nodes in one horizon-local function: **5,000,000**.

Add before primary evaluation:

- maximum synchronized comparison-state pairs for one recurrence query: **5,000,000**;
- maximum saved counterexample assignment width: **33 macro variables** (the largest union interval possible for `h<=6` under the declared translation range).

Crossing either computational ceiling is **censoring only**. Do not raise a ceiling after learning which rules hit it.

A rule can be classified `no-recurrence-through-6` only if every declared candidate comparison through horizon 6 completed exactly. Otherwise its recurrence status is `censored` unless it resolved before censoring.

## Frozen primary hypothesis

Before evaluating any of the 170 frontier distinctions:

> **At least one Research034 frontier distinction receives an exact all-time permanence certificate from a symbolic temporal recurrence by horizon 6.**

This hypothesis may fail. A complete zero is scientifically useful: it would show that Note 036's missing compact proof object cannot usually be reduced to ordinary temporal periodicity/translation of the underlying macro CA.

No prediction is frozen for the number of resolved rules or for the Rule-122/161 sentinel families.

## Measurements

For every frontier rule record:

- horizons successfully built;
- MDD node count and build time per horizon;
- every tested `(h,j,delta)` until resolution/censoring;
- synchronized comparison-state count;
- first counterexample width for failed recurrence candidates;
- first exact recurrence, if any;
- whether the rule was censored and at which stage.

For the 170 target/seed questions aggregate:

- exact recurrence permanence certificates;
- unresolved-through-recurrence-6;
- censored questions;
- class breakdowns;
- Rule-122/161 sentinel status.

Do not interpret MDD or comparison-state size as intrinsic dynamical complexity.

## Independent audit of fresh recurrence claims

If a frontier recurrence is found, freeze the earliest canonical event before interpretation.

Audit it with a separately written Boolean/SAT formulation that does **not** import the MDD implementation:

1. create one finite source macro word covering the union dependency interval;
2. encode the original fine ECA for `3h` ticks to compute the horizon-`h` output block;
3. independently encode `3j` ticks for the translated horizon-`j` output block from the same initial word;
4. require the two three-bit macro outputs to differ;
5. prove the formula UNSAT.

For small enough union widths, also perform direct exhaustive scalar replay.

A recurrence that fails independent audit is invalid and blocks publication.

## Interpretation boundaries

- A recurrence success is an exact all-time certificate, not a heuristic.
- Failure to find recurrence through horizon 6 does **not** imply a finite witness exists.
- Failure does **not** refute symbolic sofic inclusion; it only rejects this identity/translation recoder family within the frozen horizon.
- Censoring is representational, not dynamical.
- The primary result concerns the matched block-3/cadence-3 ECA macro family only.
- No Class-IV claim is tested here.
- The dimensional-lift Program is unrelated evidence and remains untouched.

## Decision rule

- If the recurrence family resolves frontier cases, characterize the smallest exact temporal identities and compare their symbolic cost with the explicit sofic graphs that censored.
- If the complete frontier yields zero recurrences, move to a genuinely nontrivial **source recoder**: a finite-state transducer/graph endomorphism `P:X_0(s)->X_0(s)` satisfying `G^h = G^j o P` on the one-defect source language.
- If MDD construction or equality comparison censors the hard rules, preserve that boundary and target a SAT/BDD or transducer representation that does not require the full local-function MDD.
- Do not respond to a negative result by raising graph ceilings or blindly increasing window width.
