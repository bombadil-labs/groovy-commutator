# A Groovy field can have its own rule, but Rule 110's does not

Date: 2026-09-22. Evidence: exact local identities and a periodic counterexample
that extends to the full infinite line. Authored by Codex; independent review
and integration are recorded on [PR #293](https://github.com/bombadil-labs/groovy-commutator/pull/293).

We asked whether observing only a CA's Groovy field could leave a complete
dynamical system: could its next field be computed without the source state?
The answer depends on the source rule. The existing Rule-32 example says yes:
its Groovy field follows Rule 128. **For Rule 110 on arbitrary binary
configurations, the answer is no.** Two configurations produce exactly the
same entire Groovy field and different next fields. Inspecting farther away
cannot recover information that is absent everywhere in the observation.

This is a direct test of the user's proposed autonomous-observable direction.
It does not require a dimensional lift or a census of many rules. It closes
one precise candidate while retaining a known positive example.

## The question and its decisive test

Let E be the synchronous source CA, and use the repository definitions

\[
D(S)=S\oplus E(S),\qquad
G(S)=D(E(S))\oplus E(D(S))
     =E(S)\oplus E^2(S)\oplus E(S\oplus E(S)).
\]

The state family is the full binary integer line, with fixed spatial
alignment. We observe original-source G once per source step, without burn-in,
history, a prepared background or extra state. The question is whether any
deterministic function B on the realized G fields satisfies

\[
G(E(S))=B(G(S))\quad\text{for every }S.
\]

By the [observation-factor criterion](../knowledge/observation-factor.md), this
requires equal current G fields to imply equal next G fields. B need not be
an elementary CA, local, translation invariant, or computationally efficient
for this necessary condition to hold. A violation rules out all such B.

## A three-site certificate

Use Wolfram Rule-110 indexing: a neighborhood (l,c,r) reads truth-table bit
4l+2c+r. Repeat each displayed word periodically in both directions. Column
positions have the same alignment in both rows.

| Source S | E(S) | D(S) | Current G(S) | Next G(E(S)) |
| --- | --- | --- | --- | --- |
| 001 | 011 | 010 | **010** | **010** |
| 011 | 111 | 100 | **010** | **000** |

The underlying source orbit is especially small:

\[
(001)^\infty\ \xrightarrow{E}\ (011)^\infty
\ \xrightarrow{E}\ (111)^\infty
\ \xrightarrow{E}\ (000)^\infty.
\]

The first two source states look identical through G, but only the second is
about to change its G field to zero. For a direct arithmetic check,
E(010)=110 and E(100)=101 on these rings, so

\[
G(001)=011\oplus111\oplus110=010,\qquad
G(011)=111\oplus000\oplus101=010,\qquad
G(111)=000.
\]

Let p repeat a finite word to the infinite line. A homogeneous local CA
satisfies E(p(s))=p(E_n(s)), where E_n is the cyclic update on that word's
length. XOR and composition preserve this identity, so G also commutes with
p. The table therefore supplies two actual infinite configurations with
equal complete observations and unequal successors. B would have to send the
same input (010)^infinity to both (010)^infinity and the zero field, which is
impossible. **This is an infinite-line obstruction proved by a finite
certificate, not an extrapolation from finite-ring statistics.**

Any refinement that retains G and claims autonomous evolution on this domain
must distinguish these two sources. In particular, it needs at least two
distinct refined states above this G field. That necessary distinction does
not establish that one extra bit, or any chosen finite history, is sufficient
for all Rule-110 configurations.

## What the bounded evaluation did

The independently reviewed [protocol](protocols/rule110-g-autonomy-20260922.md)
fixed controls, three local budgets and an early-stopping ring search before
implementation. The [canonical result](../../results/rule110_g_autonomy_20260922.json)
retains every outcome and skipped budget.

| Stage | Complete work performed | Outcome |
| --- | --- | --- |
| Known Rule-32 control | All 128 seven-bit causal words | G_32 E_32 = E_128 G_32 |
| Known Rule-90 control | All 32 five-bit causal words | G_90 is identically zero |
| Rule-110 radius 0 | All 128 seven-bit source words | Conflicting successors |
| Rule-110 radius 1 | All 128 seven-bit source words | Conflicting successors |
| Rule-110 radius 2 | All 512 nine-bit source words | Conflicting successors |
| Periodic ring lengths 1 and 2 | All 2 and 4 states respectively | No G collision with unequal successors on those rings |
| Periodic ring length 3 | First 4 of 8 states, lexicographic order | Certificate above; stop |
| Ring lengths 4 through 16 | Not run after the certificate | No claim about their enumeration |

Three is the smallest common ring length admitting this obstruction; that
claim uses the completed smaller rings, not the stopped larger budgets.
The local conflicts alone would refute only their tested radii. The periodic
certificate is what eliminates every G-only present-state law.

The primary evaluation took about 0.012 seconds on this machine and reported
12,416 KiB peak resident memory, within its 120-second/1-GiB limits. These are
execution records, not performance comparisons with source simulation.
[Execution metadata](../../experiments/rule110_g_autonomy_20260922/execution.json)
pins implementation commit `232662516b858eabb4743dce9f8ef2c76847bec6` and the
result digest. The scientific result records protocol and evaluator hashes.

The 001/011 candidate was hand-derived after the protocol froze and before
the evaluator was implemented or run. It was disclosed to the reviewer and
user before execution. The retained P1 conjecture is supported by the exact
counterexample; it is not represented as a blind prediction. The
[review chronology](../../experiments/rule110_g_autonomy_20260922/review.md)
preserves that distinction and both review gates.

The primary local evaluator uses shrinking causal words and its ring search
uses packed integers. The independent [certificate verifier](../../scripts/verify_rule110_g_autonomy_certificate.py)
replays cyclic tuples and directly evaluates periodic causal windows. Neither
the proof nor its check needs a larger search.

```bash
python scripts/verify_rule110_g_autonomy.py --integrity
python scripts/verify_rule110_g_autonomy.py --check
python scripts/verify_rule110_g_autonomy_certificate.py
```

## What this changes

The [Rule-32 identity](2026-09-10-local-correction-caps.md) remains an exact
nonconstant example of a derived field with its own local law. With U=D_32(S)
and V=G_32(S), the already established prepared-pair dynamics are

\[
U'=E_{32}(U)\oplus V,\qquad V'=E_{128}(V).
\]

Thus “a derived field can be a state in its own right” is a mathematical
possibility with a concrete example. It is not guaranteed by having defined
a derivative or a commutator. For Rule 110, G merges sources whose distinction
matters one step later. Even unlimited spatial access to that same observation
cannot repair the loss.

Stop searching for a larger present-only G rule on the full Rule-110 shift.
A specified invariant source family, retained context, different observation
or different cadence would be a different question. None is tested or queued
here. Any follow-up should first name the distinction it proposes to retain
and the scientific decision that a success or counterexample would change.
