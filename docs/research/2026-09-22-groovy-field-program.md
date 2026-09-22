# The Groovy Field

**Research program, opened 2026-09-22 at Myk's request.** Authored by: Claude
Code (Opus 5.5), session `session_01RMFucTxgbcRnRoc64MCLyF`, working directly
with Myk. Original head `7c55ffa` reviewed by Codex/Astra in
[PR #294](https://github.com/bombadil-labs/groovy-commutator/pull/294#pullrequestreview-5283253213).
Codex's `8e7d55d` corrections were [approved by Claude](https://github.com/bombadil-labs/groovy-commutator/pull/294#issuecomment-5784102034);
Codex then reviewed Claude's `74c2970` follow-up. Status: living.

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
10. **Can it be iterated?** The repaired law is initially defined only on
    valid observation histories. XOR can leave that domain, so a native Groovy
    field requires a declared off-image completion. After specifying one, is
    any tower result invariant to that choice?

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
- **Evidence.** The original run used exhaustive local-table checks for laws
  and finite-interior tuple checks for negative witnesses; the serializers
  retained only some certificates. Graph-cap and decider-only entries are
  unresolved or uncertified, not theorems. The corrected witness checker
  verifies the actual infinite extensions and their seams. The bounded
  [review audit](../../scripts/verify_groovy_field_audit.py) replays all 220
  retained memory-1 witnesses, selected higher-memory witnesses, two headline
  laws independently, and an all-ring SCC proof. It does not recertify the
  unretained evidence. New runs retain full witness and failure records.
- **Code.** [`src/groovy/groovy_field.py`](../../src/groovy/groovy_field.py),
  [`scripts/groovy_field_suite.py`](../../scripts/groovy_field_suite.py),
  [`scripts/groovy_field_rule110_lift.py`](../../scripts/groovy_field_rule110_lift.py),
  [`scripts/groovy_field_summarize.py`](../../scripts/groovy_field_summarize.py),
  [`scripts/groovy_field_followups.py`](../../scripts/groovy_field_followups.py),
  tests in [`tests/test_groovy_field.py`](../../tests/test_groovy_field.py).
  The original full suite and follow-ups took about 40 minutes on four cores;
  CI runs only the bounded audit and regressions.

Two exact facts frame the lift question:

- **G sits inside the six-field lift.** With the six-field rows
  `F2 = X ⊕ H(X)` and `F3 = X ⊕ H²(X)`, `G = F2 ⊕ F3 ⊕ H(F2)`. So G is a local
  function of the existing lift on valid marked beams. The corresponding
  history factor is on the source-realizable subshift, not arbitrary ambient
  binary configurations or unmarked beams.
- **G is always blind to D0.** On a uniform configuration `c^Z` the rule
  acts as a one-cell map `u(c) = φ(ccc)`, which is affine, and
  `G(c^Z) = u(c) ⊕ u(u(c)) ⊕ u(c ⊕ u(c))` is the same constant for `c = 0`
  and `c = 1`. No rule's Groovy field can tell the two uniform backgrounds
  apart, even with their future G histories. This is not global complement
  invariance on nonuniform states. A gradient alone has complement-pair fibers;
  G and history may split them. The repaired fibers have size at most two, and
  the uniform pair shows that the maximum is attained.

## Latest geometric follow-up

Codex (OpenAI), at Myk's request on 2026-09-22; Reviewed by: none.
The [raw-three-row test](2026-09-22-groovy-three-row-geometry.md) distinguishes
ordered temporal closure from a uniform binary spatial encoding. Rule 30's
three raw G rows, repeated vertically without phase labels, have an exact
whole-plane collision at one-step cadence. No neighborhood enlargement fixes
that encoding. A marker channel gives a larger-alphabet construction from the
known law; a different binary geometry remains a separate design question.
The [unit handoff](checkpoints/groovy-three-row-geometry.md) records the frozen
protocol, certificate and stopping decision.

## Stages

| Stage | Question(s) | State |
| --- | --- | --- |
| 1. Rule 110 repairs: every radius-one extra track, memory 1–3 | 3, 4 | bounded run complete; see evidence limits |
| 2. All 256 rules: G alone (memory ≤ 4) and every one-bit track (memory ≤ 2, then 3) | 1, 2, 4, 5 | bounded run complete; see evidence limits |
| 3. Reachable states: G alone after one and two steps of burn-in | 6 | bounded run complete; see evidence limits |
| Taxonomy: classify each counterexample by how its two tails differ | 3, 9 | bounded run complete; see evidence limits |
| 4. Rule 110 dynamics on valid histories | 8 | bounded run complete; see evidence limits |
| Follow-ups: output complement vs D0; universal repairs at memory 3; G alone at memory 5 | 2, 5, 9 | bounded run complete; see evidence limits |
| 5. Towers: the Groovy field of the repaired system | 10 | requires an off-image completion contract |
| 6. A general operator beyond one-bit, radius-one tracks | 5, 9 | open |
| Raw three-row geometry: Rule-30 temporal roles as spatial rows | 8, 9 | closed negative for the unlabelled period-three encoding; no repair search queued |

Results and their evidence level are in the
[census note](2026-09-22-groovy-field-census.md); the current state and next
decisions are in the [checkpoint](checkpoints/groovy-field.md).

## Non-claims

- No compression or speed claim. Retaining the source (one bit per cell)
  always closes trivially; the repaired Groovy systems are larger. Their
  interest is structural: they identify what the Groovy field loses.
- No Class-IV, universality or physics claim.
- Finite-ring checks are consistency checks, never evidence for a line claim.
- A completed bounded run can contain unresolved or uncertified outcomes.
  “No law through memory five” is not “no finite memory works.”
