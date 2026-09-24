# Observer-relative orbit dynamics: a bounded program

2026-09-24. Authored by Codex (OpenAI). Reviewed by: none.
**Status: first bounded test completed; H3 remains contingent. No Class-IV or quantum result.**
The [observation/law taxonomy](2026-09-24-observation-law-taxonomy.md) fixes
our vocabulary. The zeta function is a generating function for periodic-orbit
counts, not a new source of information about a finite system.

## What we want to distinguish

An observer can report an apparent repeating pattern even when the hidden
source cannot follow that pattern forever. A model that retains history may
rule out these phantom cycles. A later, separate construction question is
whether an observer's retained expectation can locally choose future rules
and maintain a specified organization more efficiently than an external
clock. These are different claims; success on one does not establish the
other or define Wolfram Class IV.

For a finite ring with deterministic update `E` and observation `O`, let
`A[u,v]=1` exactly when **some** source `s` has `O(s)=u` and `O(E(s))=v`.
The one-step observer graph can concatenate edges witnessed by different
sources. Its number of rooted closed walks of length `k` is `tr(A^k)`.
Let `R_k` count the distinct length-`k` periodic observed words that a
*single actual source trajectory* realizes forever. Then
`P_k = tr(A^k) - R_k >= 0` counts phantom observed periodic words, with
their starting phase counted. A positive `P_k` has a concrete witness: a
closed observed word, its individual source-backed edges, and a certificate
that no recurrent source trajectory produces that word. The Artin–Mazur
zeta/Euler product repackages `tr(A^k)` or `R_k`; those counts and witnesses
carry the scientific content.

## Ranked hypotheses and decisions

| Hypothesis | First bounded test or prerequisite | What failure changes |
| --- | --- | --- |
| **H1: one-step observation can invent recurrence.** On the frozen six-cell Rule-30 ring, the whole native `G` field's one-step graph admits a phantom primitive cycle of period at most six. | Exhaustive 64-state test in the [frozen protocol](protocols/observer-orbit-preflight-20260924.md). | If no such cycle exists, record the negative at this size/period and stop this example. Do not select a new ring after viewing outcomes. |
| **H2: sufficient retained history removes the false cycles.** A valid three-row `G` history has no phantom cycles on that ring. | Same exact domain; calibration against the established full-line third-order local law, plus an identity-observer control. | A failure indicates a contract or implementation error, or a misunderstood older claim. Resolve that before interpreting H1. This is a check of prior knowledge, not an independent discovery. |
| **H3: expectation can be operational rather than only descriptive.** A fully specified, locally maintained observer can choose the next rule from information available at that time and sustain an independently defined mobile-structure task under a fixed resource budget. | **Contingent**, not evaluated here. Freeze the selector, target, state family, horizon and open-loop controls in a separate protocol first. Count observer memory, G acquisition, rule storage, updates and local access. | If the target is absent, leaks future information, or is matched by a simpler clocked/fixed-track baseline, park that policy. Do not infer Class IV from a zeta difference. |

H1 outranks H3 now: it tests whether a naive observer's recurrent repertoire
is even the repertoire of the source. H2 catches a false computation and
shows why retaining history can matter; a three-row register is **not** yet
a predictive model with a specified expectation update. Neither requires searching
rules, selectors or metrics. The earlier Rule-30 result says three G rows
admit an exact local law on the full line; it does **not** predetermine H1's
finite-ring orbit counts. See the [Groovy-field census](2026-09-22-groovy-field-census.md).

**First test, completed:** [the exact six-cell result](2026-09-24-observer-orbit-preflight.md)
found nine phantom fixed words in the one-row G graph, including `G=9`;
the valid three-row history and identity controls had no phantoms through
period six. This supports H1 at the specified ring and validates H2 as a
prior-result calibration there. It offers no evidence for H3 and does not
queue a feedback experiment without an independently specified target.

**H3 causal prerequisite, exact:** [the rule-choice obstruction](2026-09-24-feedback-causality.md)
shows that the simultaneous instruction “choose a rule from its own G” can
have either no solution or multiple solutions, even using the two constant
ECAs on any ring. Choose a fixed-reference counterfactual G or a suitably
lagged realized-path residual before specifying a controller; these are
different sensors with different costs and meanings. This clears a policy
definition, not H3's independent target or empirical test.

**H3 feasibility gate, completed:** a [published Rule-54 junction-pair
route](2026-09-24-rule54-glider-route-gate.md) gives a concrete target
independent of the G selector. A delayed held-site update rescues 68/1,156
one-bit injuries beyond passive Rule 54 and the best fixed addressed
action. All rescued runs first rejoin the clean route four steps after
the held update. Yet holding the originally injured site, if supplied
by an oracle, exactly matches the full-state upper bound. This is
one-shot full-state feasibility, not H3's claimed G advantage or
indefinite maintenance. Any sensor follow-up must compare G with raw
local fault localization and price address coordination.

**H3 information gate, completed:** [the fixed-reference G sensor
comparison](2026-09-24-rule54-g-sensor-gate.md) finds that the whole
G field still permits all 408 successes on the same 1,156 cases while
collapsing 1,054 raw states into 850 observation fibers. The prospectively
predicted information loss failed. G must first read all 34 raw bits and
perform three Rule-54 evaluations in total (two additional if the
physical update's first pass can be reused). No local selector or cheaper
feedback mechanism has been shown; matched raw-local access and total
address-coordination costs are the only reason to continue H3 here.

**H3 local trigger gate, completed:** [the matched one-site
comparison](2026-09-24-rule54-local-sensor-gate.md) found no dynamic
rescue from either `G_i` bit trigger (340/1,156), whereas a five-bit raw
source pattern with the same source radius and address arbiter gets
374/1,156. The global G information result still stands; this specific
policy has no G advantage. Park the proposed cross-rule H3
discriminator campaign; independent Rule-110 feasibility and comparable
rule-specific targets would be prerequisites to any future small panel.

## Scope and prior art

Every finite deterministic map has a rational orbit zeta function. A
periodic rule schedule adds a phase; a local feedback policy is itself a
fixed CA on source plus controller tracks. Our comparison must count those
resources and the trajectories, not just contrast two attractive diagrams.
Finite-ring cycles do not establish a full-line or Class-IV theorem; zeta
counts ignore transient behavior and glider collisions unless these enter
a separately defined observable. Do not take an unnormalized ring-size limit
of `tr(A^k)` as though it were automatically a full-line zeta function.

The primary mathematical starting point is
[Artin and Mazur, *On periodic points*](https://www.mathnet.ru/eng/mat444).
The CA comparison has prior work on
[temporally nonuniform rules](https://arxiv.org/abs/2411.17421) and
[CA with memory](https://arxiv.org/abs/1406.2277).
Wolfram's [ruliad](https://writings.stephenwolfram.com/2021/11/the-concept-of-the-ruliad/)
and [observer theory](https://writings.stephenwolfram.com/2023/12/observer-theory/)
are conceptual neighbors; their all-rules multiway physics claims are not
premises of this finite deterministic test.

## Continuation gate

After the first exact unit, retain the result and its failed predictions in
[FINDINGS](FINDINGS.md). An H3 protocol requires an independently declared
maintenance task, local causal selector, equal-budget clocked and static
baselines, and a result that changes the design decision. There is no
automatic all-ECA census, unbounded zeta calculation, or prime-distribution
claim. Update this page with links to dated evidence, keeping its original
hypotheses intact.
