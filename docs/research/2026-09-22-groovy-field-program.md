# The Groovy Field

**Research program, opened 2026-09-22 at Myk's request.** Authored by: Claude
Code (Opus 5.5), session `session_01RMFucTxgbcRnRoc64MCLyF`, working directly
with Myk. Reviewed by: none. Status: living.

The Groovy field `G(S) = D(E(S)) ⊕ E(D(S))` has so far been studied as a
*measurement* of a cellular automaton: a signature of where "evolve, then
describe" disagrees with "describe, then evolve". This program asks whether
it is also a *state*: can the Groovy field, perhaps with a little help, run
as a dynamical system of its own, and what does the help it needs tell us
about the information it throws away?

It grew out of [PR #293](2026-09-22-rule110-g-autonomy.md), which proved that
Rule 110's Groovy field cannot predict its own next value, and a follow-up
exploration showing that one extra bit per cell plus two steps of history
repairs that exactly. The first results are in the
[census note](2026-09-22-groovy-field-census.md).

## The questions, in plain English

1. **Can a rule's Groovy field run on its own?** If you are only shown the
   Groovy field, never the underlying cells, can you always compute what the
   Groovy field will be next? For which rules?
2. **Does a short memory help?** If not from the present field alone, can a
   few past Groovy fields fill the gap? How many steps of memory, and is
   there a rule for which no finite memory ever suffices?
3. **What exactly is missing?** When the Groovy field cannot predict itself,
   which difference between two underlying states is it failing to see? Can
   we name that lost distinction for each rule?
4. **What is the cheapest repair?** What is the smallest extra piece of
   information about the cells — one bit per cell, computed from a cell and
   its two neighbours — that makes the Groovy field self-sufficient?
5. **Is there one repair that works for every rule?** A single recipe would
   be a general operator: a uniform way of turning any cellular automaton into
   a closed "Groovy system".
6. **Does the answer depend on where you look?** Do the obstructions only
   involve states the rule can never actually produce (Gardens of Eden), or do
   they survive in the states the rule really reaches after running for a
   while?
7. **Do finite rings tell the truth?** Several earlier results in this
   repository held on every finite ring but failed on the infinite line. Is
   that happening here too, and why?
8. **What does the repaired system look like?** As a cellular automaton in
   its own right, what are its rules, how big is its neighbourhood, what does
   it forget about the original, and does it show structure (gliders,
   backgrounds) of its own?
9. **Is this a new dimensional lift?** The repaired system stacks copies of
   the Groovy field (and the extra bit) from consecutive times into one state,
   which is a lift of sorts. How does it relate to the
   [affine-oriented six-field lift](2026-09-17-affine-oriented-lift-theorem.md),
   and does the lift's lesson about the zero-dimensional base **D0** — the
   spatially uniform layer, where only a single ℤ₂ bit survives — tell us what
   the Groovy field is missing?
10. **Can it be iterated?** If the repaired system is itself a cellular
    automaton, it has its own Groovy field. Does repeating the construction
    give a tower, as the six-field lift does?

## Method

Every question above is posed on the **full infinite line** unless it says
otherwise, for all 256 elementary rules, at one source step per update.
The decisive tool is exact:

- **Decider.** For an observation (G, optionally plus one extra track) and a
  memory length `k`, pairs of configurations whose observation histories agree
  everywhere form a subshift of finite type. A counterexample to "the next
  observation is determined by the last `k`" exists exactly when a finite
  graph has a bi-infinite path through a disagreeing window. By
  compactness (Curtis–Hedlund–Lyndon), when no counterexample exists, the law
  is automatically local.
- **Certificates.** No verdict is recorded on the decider's word alone. Every
  "law" is certified by an explicit table checked against every source window
  in its causal support; every "no law" by an explicit pair of eventually
  periodic infinite configurations, verified by a separate tuple
  implementation. Finite-ring brute force is used only as a consistency check.
- **Code.** [`src/groovy/groovy_field.py`](../../src/groovy/groovy_field.py),
  [`scripts/groovy_field_suite.py`](../../scripts/groovy_field_suite.py),
  [`scripts/groovy_field_rule110_lift.py`](../../scripts/groovy_field_rule110_lift.py),
  [`scripts/groovy_field_summarize.py`](../../scripts/groovy_field_summarize.py),
  tests in [`tests/test_groovy_field.py`](../../tests/test_groovy_field.py).
  The whole suite runs in minutes on a laptop.

Two exact facts frame the lift question:

- **G sits inside the six-field lift.** With the six-field rows
  `F2 = X ⊕ H(X)` and `F3 = X ⊕ H²(X)`, `G = F2 ⊕ F3 ⊕ H(F2)`. So G is a local
  function of the existing lift; a closed Groovy system is a *quotient* of that
  construction, keeping only what the Groovy field needs.
- **G is blind to D0 whenever the rule's uniform map makes it so.** On a
  uniform configuration `c^Z` the rule acts as a one-cell map
  `u(c) = φ(ccc)`, and `G(c^Z) = u(c) ⊕ u(u(c)) ⊕ u(c ⊕ u(c))` is a constant.
  When that constant is the same for both `c`, the Groovy field cannot tell
  the two uniform backgrounds apart at all.

## Stages

| Stage | Question(s) | State |
| --- | --- | --- |
| 1. Rule 110 repairs: every radius-one extra track, memory 1–3 | 3, 4 | complete |
| 2. All 256 rules: G alone (memory ≤ 4) and every one-bit track (memory ≤ 2, then 3) | 1, 2, 4, 5 | complete |
| 3. Reachable states: G alone after one and two steps of burn-in | 6 | complete |
| Taxonomy: classify each counterexample by how its two tails differ | 3, 9 | complete |
| 4. The Rule 110 repaired system as a CA | 8 | complete |
| 5. Towers: the Groovy field of the repaired system | 10 | open |
| 6. A general operator beyond one-bit, radius-one tracks | 5, 9 | open |

Results and their evidence level are in the
[census note](2026-09-22-groovy-field-census.md); the current state and next
decisions are in the [checkpoint](checkpoints/groovy-field.md).

## Non-claims

- No compression or speed claim. Retaining the source (one bit per cell)
  always closes trivially; the repaired Groovy systems are larger. Their
  interest is structural: they identify what the Groovy field loses.
- No Class-IV, universality or physics claim.
- Finite-ring checks are consistency checks, never evidence for a line claim.
