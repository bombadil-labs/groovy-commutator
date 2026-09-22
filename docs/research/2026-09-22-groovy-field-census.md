# When can the Groovy field run on its own? A full-line census

Date: 2026-09-22. First results of [The Groovy Field](2026-09-22-groovy-field-program.md).
Authored by: Claude Code (Opus 5.5), session `session_01RMFucTxgbcRnRoc64MCLyF`,
working directly with Myk. Reviewed by: none.

**Evidence.** Every verdict below is exact on the full infinite line unless
marked otherwise. A "law" is certified by an explicit local table checked
against every source window of its causal support; a "no law" by an explicit
pair of eventually periodic configurations verified by a separate
implementation. A handful of laws the decider finds but whose tables exceeded
the certification budget are reported as *decider only*. Finite rings were
used only as a consistency check (no disagreements in 512 checks).

## Short answers

1. **Can the Groovy field run on its own?** For 140 of the 256 elementary
   rules, yes: its next value is a local function of its last one to four
   values. For 109 rules it cannot with four steps of memory, and 7 are
   unresolved within the computation budget.
2. **Does memory help?** A lot. Only 36 rules close with no memory at all;
   64 more need two steps, 32 need three (including Rules 30 and 106) and 8
   need four. Rules 54 and 110 do not close with four.
3. **What is missing?** Two kinds of things. Most often the Groovy field
   cannot tell **which background** it is in: two different periodic
   backgrounds, or two shifts of the same one, produce identical Groovy
   fields. Otherwise it misses a **finite hidden defect** that stays invisible
   for a few steps and then surfaces.
4. **Cheapest repair?** Every rule is closed at memory one by some single
   extra bit per cell. For Rule 110, 82 of the 256 possible one-bit tracks work
   with no memory and 220 with two steps. Marking runs of `111` is one of them.
5. **One repair for every rule?** Yes, and it is informative. Adding the
   **spatial gradient** of the source (`Sᵢ₋₁ ⊕ Sᵢ`, one bit per cell) with two
   steps of memory closes the Groovy field of **all 256 rules**. The gradient
   is the source with exactly one bit removed: global complement, the D0 bit.
   No one-bit track that forgets more than that works universally.
6. **Reachable states?** Letting the rule run one step first lowers the
   needed memory for 45 rules, but did not rescue any rule that had no law
   with four steps of memory. Rule 110 still has no law after one or two
   steps of burn-in, and it has an exact obstruction on its limit set.
7. **Finite rings?** Not trustworthy here: Rule 110's Groovy field with three
   steps of memory is deterministic on every finite ring (a pair-graph
   result, checked directly up to 16 cells) and fails on the infinite line (the tails ... 000 and ... 111 are indistinguishable to G).
8. **The repaired Rule 110 system** is a radius-3 cellular automaton on four
   bit-tracks that runs autonomously and forgets exactly one distinction on
   finite rings.
9. **A new lift?** "Groovy field + gradient rail, two steps" is a uniform
   operator for all elementary rules. It is a *quotient* of the existing
   six-field lift: it keeps the Groovy field and one rail, and drops exactly
   the D0 bit the Groovy field can never see.

## Two exact facts behind the lift question

**G never sees the D0 bit.** On a uniform configuration `c^Z` every rule acts
as a one-cell map `u(c) = φ(ccc)`. All four one-cell maps are affine, and
`G(c^Z) = u(c) ⊕ u(u(c)) ⊕ u(c ⊕ u(c))` equals the same constant for `c = 0`
and `c = 1` (constant maps give `u`, the identity gives 0, the swap gives 1).
So for every rule the Groovy field is identical on the all-zeros and all-ones
backgrounds. This is the concrete form of the six-field lift's section 8:
restricted to D0, Groovy is only the ℤ₂ grading bit. Whether forgetting D0
matters depends on the rule.

**G lives inside the six-field lift.** With rows `F2 = X ⊕ H(X)` and
`F3 = X ⊕ H²(X)`, `G = F2 ⊕ F3 ⊕ H(F2)` (checked for all 256 rules). The
six-field rails `F0 = X ⊕ τX` and `F1 = 1 ⊕ X ⊕ τ⁻¹X` are gradients. So the
universal Groovy repair found below is built from pieces of the six-field
lift, minus the retained source row `F5 = X`.

## G alone: how much memory does it need?

Minimum memory `k` for a certified local law, all 256 rules:

| Memory k | Rules | Count |
| --- | --- | ---: |
| 1 | 0 1 2 4 8 12 15 16 19 32 36 51 60 64 68 72 76 85 90 102 105 150 153 165 170 195 200 204 205 207 219 221 223 236 240 255 | 36 |
| 2 | 3 5 10 13 17 18 23 24 27 29 33 34 42 47 48 50 55 63 66 69 71 77 80 83 95 111 112 117 119 125 126 127 128 129 132 138 154 160 171 174 175 178 179 187 189 191 201 208 210 222 231 232 235 237 239 241 243 244 245 247 249 251 253 254 | 64 |
| 3 | 9 26 30 38 39 46 52 53 56 57 65 82 86 98 99 106 108 116 120 131 139 145 147 155 163 177 190 203 209 211 217 246 | 32 |
| 4 | 45 75 89 94 101 123 146 183 | 8 |
| none ≤ 4 | 109 rules, including 54 and 110 | 109 |
| unresolved | 104 107 109 121 122 135 149 (graph over size cap at k = 3 or 4) | 7 |

"None ≤ 4" means certified counterexamples at k = 1, 2, 3, 4; it is not a
proof that no finite memory works. Mirror-image rules agree in every row, as
they must.

Rule 30's Groovy field is a **third-order autonomous system**: three
consecutive Groovy fields determine the next one, by a local rule. I did not
find this recorded elsewhere in the repository.

## What the Groovy field fails to see

Each counterexample is a pair of configurations with identical Groovy
histories and different next Groovy field. Classifying how their two ends
differ (one certified witness per failing case, so these describe an example
obstruction, not every obstruction):

| Kind of hidden difference | at k = 1 | at the last failing k |
| --- | ---: | ---: |
| different periodic background, not related by a shift ("other") | 82 | 90 |
| finite hidden defect, same background on both sides | 64 | 48 |
| same background, shifted ("phase") | 26 | 37 |
| all-zeros vs all-ones ("uniform swap", the D0 bit) | 22 | 23 |
| mixtures of the above | 26 | 22 |

As memory grows, finite defects get resolved and background identity
(including phase) becomes the dominant thing the Groovy field cannot see.

The rule's action on D0 correlates with how badly this hurts. Among the 64
rules that fix both uniform states (so the D0 bit persists forever), 42 have
no law with four steps of memory; among the 64 that send both uniform states
to 0, 22 do. This is a count, not a theorem.

## Repairs with one extra bit per cell

A *track* is any Boolean function of a cell and its two neighbours (256
choices), added to the Groovy field as one extra bit per cell.

- **Every rule** is closed at memory 1 by at least one track. The only
  tracks that work for every rule at memory 1 are the six that copy or
  invert a single source cell (tracks 15, 51, 85, 170, 204, 240): retaining
  the source.
- **At memory 2 the gradient becomes universal.** Tracks 60 (`l ⊕ c`), 102
  (`c ⊕ r`) and their complements 195, 153 close all 256 rules. On the full
  line, pairs of configurations with the same gradient history are equal or
  globally complementary, and for every rule the decider finds complementary
  pairs that the repaired system cannot separate: it forgets the D0 bit and
  nothing else (the non-separation is a decider result, not certified by a
  witness).
- **The derivative is a good but not universal repair.** Adding `D` itself
  (track `φ ⊕ 204`) closes 128 rules at memory 1 and 180 at memory 2, but
  never Rule 110.
- 108 memory-1 laws found by the decider need a table radius above 8 and are
  recorded as decider-only; no conclusion above depends on them.

## Rule 110 in detail

- **G alone:** no law at memory 1–4 on all states; none at memory 1–3 after one
  or two steps of burn-in. On its limit set, the temporally periodic sources
  `011010` and `011100` already share `G = 110000` and have different next
  fields (from the PR #293 review).
- **Tracks:** 82 close at memory 1, 220 at memory 2, 222 at memory 3, and 34
  never close at memory ≤ 3 — including `D` (track 162) and the run-of-`000`
  marker (track 1). For every track that still fails at memory 2, the recorded
  counterexample is background blindness (28 phase, 8 other), never a finite
  defect.
- **Why the run-of-`000` marker fails but run-of-`111` works:** its surviving
  counterexamples are the period-4 background `(0111)^∞` against its
  two-cell shift `(1101)^∞`. That background contains no `000`, so the marker
  cannot see its phase; `111` runs mark it.
- **The repaired system** (G plus the run-of-`111` track, two steps):
  a radius-3 law on four bit-tracks with 1,195 realized neighbourhood patterns.
  Run as a cellular automaton from lifted initial data alone, it reproduced G
  and the track computed from the true source at every step on rings of 40,
  64 and 101 cells. On rings of 8–16 cells it merges exactly one pair of
  source states (the two phases of `(01)ⁿ` on even rings), whose futures are
  identical — a quotient that discards only a distinction that never matters.

![Rule 110 source (left), Groovy field (centre) and run-of-111 track (right), 120 steps on a 160-cell ring after 40 steps of burn-in](assets/groovy-field-rule110.png)

## Data and reproduction

Results in `results/groovy_field_20260922/`:
[`validate`](../../results/groovy_field_20260922/validate.json),
[`tracks110`](../../results/groovy_field_20260922/tracks110.json),
[`census`](../../results/groovy_field_20260922/census.json),
[`reachable`](../../results/groovy_field_20260922/reachable.json),
[`taxonomy`](../../results/groovy_field_20260922/taxonomy.json),
[`rule110_lift`](../../results/groovy_field_20260922/rule110_lift.json) and the
[`summary`](../../results/groovy_field_20260922/summary.json) with sanity checks
and source hashes.

```bash
pip install -e . pytest
for s in validate tracks110 taxonomy census; do python scripts/groovy_field_suite.py $s; done
python scripts/groovy_field_suite.py reachable --jobs 2
python scripts/groovy_field_rule110_lift.py
python scripts/groovy_field_summarize.py
python -m pytest tests/test_groovy_field.py
```

About 25 minutes on four cores. Budgets: pair graphs over 15 million edges
are recorded as unresolved; tables up to radius 8 (21-bit source windows).
Two-step burn-in data are heavily censored by the edge cap (118 rules
unresolved) and are not interpreted.

## Limits

- "No law with memory ≤ 4" is not "no law at any memory".
- Tracks are radius-one and one bit; richer repairs are untested.
- The universal gradient repair is not a compression: it stores nearly the
  whole source. Its content is that exactly one bit — D0 — can be dropped
  from the source for every rule once the Groovy field is kept.
- One-step burn-in results depend on the edge cap for 4 rules; two-step
  results are not used.
