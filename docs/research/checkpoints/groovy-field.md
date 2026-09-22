# The Groovy Field: checkpoint

Updated 2026-09-22. [Program](../2026-09-22-groovy-field-program.md),
[census and evidence limits](../2026-09-22-groovy-field-census.md).
Branch `claude/relaxed-shannon-o7cl11`,
[PR #294](https://github.com/bombadil-labs/groovy-commutator/pull/294), open for
Claude's review of Codex's fixes at Myk's request. Do not merge before Myk's
direction. Original inspected head: `7c55ffa8d9925c5041498c2c7915bb2d51d78a02`;
base main: `fa826725f4e36a5d8fb98f3d8512c150ebd5e2d9`.

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
bounded CI job runs the regressions and audit; the full census is not in CI. Review of the authored fixes
is pending Claude. The prior Codex review applies only to the original head;
self-checks are not independent approval.

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

## Next decision questions

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
