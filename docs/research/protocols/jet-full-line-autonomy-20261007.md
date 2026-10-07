# Exact audit: full-line autonomy and local radius of G-anchored jet prefixes

**Date:** 2026-10-07. **Author:** GPT-6 (OpenAI).
**Status:** descriptive/reproducibility protocol following already-viewed exploratory
results in the Claude-review follow-up. This is NOT independent preregistration
and carries no classifier prediction. Independent peer review pending.

## Question

Claude's independent review of PR #328 identified an explicit period-four
half-time-shift gauge behind Rule-54's two golden equal-jet SCCs and an
eventually absorbed smaller SCC. The follow-up graph audit suggested that
the **entire** Rule-54 G-anchored jet through A5, not merely selected SCCs,
may be an autonomous full-line factor.

Construct an exact certificate for that stronger global statement and
separate it from finite-ring apparent closure.

## Fixed objects and controls

Rules 30, 54, 62, 110, all preselected from prior matched jets.
Use the existing intrinsic recurrence with no changes:

\[
A_0(S)=S\oplus H(S),\qquad
A_{k+1}(S)=A_k(H(S))\oplus H(A_k(S)).
\]

For \(m=1,\ldots,5\), let \(J_m=(A_1,\ldots,A_m)\).

Autonomy criterion on the full binary line:

\[
J_m(X)=J_m(Y)\Longrightarrow J_m(HX)=J_m(HY)
\]

for **entire current fields**. By the jet recurrence, it is equivalent to

\[
J_m(X)=J_m(Y)\Longrightarrow A_{m+1}(X)=A_{m+1}(Y).
\]

No extended jet beyond A6 and no additional rules.

## Gate A: exact full-line factor

For each rule/m:

1. Compute complete Boolean local source truth tables for A1..A6.
2. Label a binary source de Bruijn graph of 2r-bit vertices and
   2r+1-bit edges, \(r=m+1\), by the current \(J_m\) symbol.
3. Build the ordered equal-label source-pair graph and prune by
   iteratively removing vertices without compatible predecessor/successor
   to retain its bi-infinite path support.
4. Enumerate **every** length-three path inside that support. Its two
   2r+3-bit source words are precisely the dependency domain of
   \(A_{m+1}\) at the central site.
5. If any such pair has different next residual values, return the first
   exact two-word witness; otherwise certify a full-line factor.

Report core vertices/edges, three-edge paths checked, disagreeing count,
and the first witness. This is a mathematical all-configurations result for
the stated source and jet fields, not a finite-ring extrapolation.

## Gate B: minimum symmetric local radius

For each first-autonomous prefix, do not enumerate \(2^{25}\) source words
naively. Instead:

1. Enumerate all \(2^{2r+3}\) single-source windows of length 2r+3.
2. Group by the three current jet symbols on consecutive sites (-1,0,+1).
3. Retain **bad** ordered pairs with different central A_{m+1}.
4. On the full (unpruned) equal-J_m source-pair graph, compute boolean
   predecessor/successor compatibility vectors iteratively. An unpruned bad
   three-edge pair survives at jet radius R iff it extends at least R-1
   compatible edges in both spatial directions.
5. The smallest radius with no surviving bad pair is an exact minimal
   symmetric radius for A_{m+1}, hence for autonomous J_m evolution
   (lower jet fields update by radius-one H plus the next current field).

Stop at R=12 for rules whose prefixes close. For Rule 110 through A5, show
the nonautonomous witness and stop; do not search arbitrary radii.

Report count of bad pairs surviving at each radius, including the last
failing witness and first zero radius. A local radius is for the **admissible
jet image**, not an unconstrained 32-symbol full shift.

## Gate C: finite-ring control

For n=8,10,12,14,16 exhaust all periodic source states and calculate J_m
and A_{m+1} from an independent ring-step implementation. Record for every
rule/n the first closing m and count of splitting prefix classes.
These numbers can exhibit premature closure on small finite rings.

## Gate D: Rule-54 recurrent fiber dynamics

Reconstruct the full G..A5 equal-output pair graph and enumerate every
recurrent off-diagonal SCC. Verify its forward image under HxH by exhaustive
three-edge internal paths (the same full-support local contract).

For each component record:
- vertices/edges, three-edge paths, destination SCC (or diagonal), and
  next-jet violations;
- whether every paired configuration is related by a fixed spacetime
  offset \(Y=\sigma^k H^p X\) for some p>=0 and p+abs(k)<=6;
- for cycle components, a representative pair of periodic source words
  and its temporal/spatial orbit relationship;
- count essential cross-SCC *spatial* edges, so no unexamined
  heteroclinic language is silently ignored.

No claim about **unbounded** time shifts or arbitrary spacetime gauges is
justified by this p+abs(k)<=6 diagnostic.

An invariant full-line equal-jet relation implies a factor. Do not infer
that all same-jet pairs are time shifts; preimage-erasure and eventual
coalescence can be distinct mechanisms.

## Scope and stop

No 256-rule census, lift comparison, classification threshold, deeper jet,
or new observer. Preserve all failed prefixes. The scientific target is an
exact full-line factor theorem with explicit smallest local radius, and its
mechanistic hidden-fiber decomposition.

The initial outcomes motivating this protocol were already inspected; do not
present positive reproduction as a surprising preregistered confirmation.
Use separate source and verification implementations and put the HTML catch-up
report through the same provenance process.
