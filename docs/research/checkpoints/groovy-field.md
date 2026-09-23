# The Groovy Field: checkpoint

Updated 2026-09-23. [Program](../2026-09-22-groovy-field-program.md),
[census and evidence limits](../2026-09-22-groovy-field-census.md).
The geometry and recursion units are consolidated in the
[2026-09-23 integration](../2026-09-23-research-integration.md).
[START_HERE](../START_HERE.md) governs the current agenda; these completed
program units do not automatically queue deeper recursion or a new census.
Preceding census branch `claude/relaxed-shannon-o7cl11`,
[PR #294](https://github.com/bombadil-labs/groovy-commutator/pull/294). Myk
authorized merging after the completed review below; on main, treat this unit
as integrated. The PR records the resulting merge commit. Original inspected head: `7c55ffa8d9925c5041498c2c7915bb2d51d78a02`;
base main: `fa826725f4e36a5d8fb98f3d8512c150ebd5e2d9`.

## Completed 1D follow-up: third-generation G

Myk requested one further generation for 2/16. The
[third-generation handoff](groovy-1d-third-generation.md) records the result: the
first-one / second-zero branch gives a nonconstant radius-four law for both;
other tested branches fail or remain unresolved beyond radius four. The
requested follow-up is complete, and no fourth generation is queued.

## Preceding unit: 1D second-generation G

Myk redirected the question to autonomous 1D fields and their own G fields.
The [bounded present-only unit](../2026-09-23-groovy-1d-second-generation.md)
is complete in [PR #296](https://github.com/bombadil-labs/groovy-commutator/pull/296).
See its [handoff](groovy-1d-second-generation.md): 33 pointwise cases have
constant native G, 2/16 close nontrivially on inherited fields for the two
specified derived rules, and 32 fails for both radius-one completions.
The full descendant-domain negatives are not substituted for the inherited
question. Rule 30's memory-bearing system is outside the unit. The next
questions below are historical census proposals; the latest handoff governs
this completed unit's possible follow-up.

## Completed geometric unit: temporal rows as binary geometry

Myk asked to test whether the three ordered Rule-30 G rows can instead run
as unlabelled spatial rows. The [first note](../2026-09-22-groovy-three-row-geometry.md)
records an exact period-11 whole-plane collision. The separately frozen
[constant-row repair](../2026-09-22-groovy-separator-lift.md) succeeds for either
constant: four binary rows support a uniform 13-by-4 rule at cadence one.
G never contains 1111, so a ones separator is locally recognizable. A zero
separator also closes without uniquely naming every temporal phase. See the
[handoff](groovy-three-row-geometry.md) for certificates and the completion record.
[PR #295](https://github.com/bombadil-labs/groovy-commutator/pull/295) preserves
protocol, implementation and evaluation chronology. Authored by: Codex
(OpenAI). Reviewed by: none. The PR carries current integration status.
This closes the raw-three-row negative and the two four-row repair candidates.

## What changed after review

The original review found a real certificate-checker gap and several
interpretive overclaims. Codex fixed the verifier to validate binary words,
periods and defect metadata, then check the explicit bi-infinite extensions,
including both seams. Schema-v2 writers retain complete negative witnesses,
positive-check parameters and uncertified/resource-limit reasons, record source
hashes, and refuse to overwrite existing artifacts before starting a run.

The new unit-specific manifest pins every original result and source revision,
plus a separate bounded audit. All 220 retained memory-1 negative witnesses
pass the corrected verifier. Eight selected witnesses establish the lower
memory bounds for Rules 30/54 and Rule-110 failures at memory 3/5. Independent
unpacked exhaustive checks cover all 2,097,152 source windows for each headline
law: Rule 30 at k=3, radius 6; Rule 54 at k=5, radius 4. The scalar SCC check
certifies no Rule-110 memory-3 periodic counterexample at any ring size,
while a stored infinite-line witness demonstrates failure there.

Also corrected: gradient-only complement fibers versus repaired histories;
valid marked-beam factors versus ambient quotients; selected-witness taxonomy
versus a mechanism claim; the conditional 19/21 complement count; burn-in and
limit-set memory bounds; missing track-57 evidence; and the summary's ambiguous
burn-in key. The four-track Rule-110 table is undefined on an explicit XOR
state, so a native-G tower needs off-image dynamics specified first.

Fast verification:

```bash
python scripts/verify_groovy_field_audit.py --check
python -m pytest tests/test_groovy_field.py -q
python scripts/check_result_integrity.py
npm run test:research --prefix site
npm run build --prefix site
```

Local verification passed: 32 targeted regressions, the bounded audit, shared
result integrity, all 21 research-page tests and the site build. A dedicated
bounded CI job runs the regressions and audit; the full census is not in CI.

[Claude approved `8e7d55d`](https://github.com/bombadil-labs/groovy-commutator/pull/294#issuecomment-5784102034)
and corrected the seven decider-only labels in `74c2970`. Codex reviewed that
two-document change and independently reran the seven stated decisions: Rule
109 at k=3; 104, 107, 121, 122, 135 and 149 at k=4. All returned `law`, while
the preserved census marks each `?`. Edge counts were respectively 53,116;
1,219,530; 705,882; 705,882; 619,404; 593,408; 593,408. The replay took 1.34
seconds. All six CI checks passed on `74c2970`.

Codex's final documentation changes clarify the graph-size range (Rule 109's
k=3 graph is smaller than the others) and record completed review/merge
authorization. These closing documentation edits are self-checked, not a new
independent approval. Code, canonical data and the integrity manifest are
unchanged by the follow-up. No further census was run.

## What remains bounded or unresolved

The original census/follow-ups are exploratory exact computations, not
preregistered predictions. Through k=4: 140 rules have local laws, 109 have
reported negative witnesses, and seven are decider-only laws (Rule 109 at
k=3, the others at k=4; tables not certified within the radius budget, graphs
well under the edge cap). At k=5 among the other
116: Rule 54 has a replayed law; ten are decider-only; 55 have reported
counterexamples; 50 exceed the graph cap. There are also 108 decider-only
memory-1 track entries and eight intermediate G-only `?` entries in the
original census. Do not convert these into failures or certified positives.

Original serializers discarded most witness strings and all positive tables.
The audit covers the retained negatives and selected headline claims, not all
of that missing evidence. Original JSON and figure bytes are unchanged, as are
the original source hashes (which refer to `7c55ffa`, not today's verifier).
A full replay would take about 40 minutes on four cores and needs a specific
reason. Two-step burn-in is censored for 118 rules. The limit-set witness only
excludes Rule-110 memory-1 closure, not arbitrary memory.

## Historical census questions; not a work queue

1. **Towers:** what off-image completion and invariance claim would make native
   G of a repaired history system well-defined and scientifically useful?
   Specify this before generalizing the decider or running a tower census.
2. **Finite memory:** can one exhibit a bounded, explicitly parameterized family
   of Rule-110 witnesses for all k? A single k=5 failure is not such a proof.
3. **Repair fibers:** which distinctions does a specified repaired history
   retain on the full line? Track-only fiber counts cannot answer that; avoid
   calling the gradient repair a global-complement quotient.

The keep/swap cross-tabulation is an observation to explain if a concrete
mechanism emerges, not a reason to launch a further census. No new broad
computation is queued by this correction pass.
