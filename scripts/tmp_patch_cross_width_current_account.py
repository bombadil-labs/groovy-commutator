from pathlib import Path

PROGRAM = Path('docs/research/2026-09-09-dimensional-closure-program.md')
CHECKPOINT = Path('docs/research/checkpoints/dimensional-lift.md')

program = PROGRAM.read_text()
section = '''## Cross-width continuation breaks at width nine

The [cross-width interface-history audit](2026-09-12-interface-history-cross-width.md) keeps the accepted touching-strip representation at `D2,h=2`, restricts to the three masks `{11,13,15}` that were globally deterministic on both predecessor rings, and asks two stronger finite questions: whether complete-field determinism persists on fresh exhaustive widths 8 and 9, and whether one width-blind radius-three local table works across widths 6–9.

The result is a sharp finite-width split. On width 8, all three masks remain globally deterministic and all three admit the frozen `R=3` local factor. On width 9, all three masks fail complete-field determinism itself, so no increase of spatial radius alone can repair those exact retained representations on the frozen `D2,h=2` domain. Consequently every pooled W3 test fails. For P15, the canonical pooled conflict is genuinely cross-width (`n=7` versus `n=9`); masks 11 and 13 already have pooled conflicts between the predecessor widths 6 and 7 even though each width separately admits a width-specific `R=3` factor there.

All three predeclared constructive bets fail. The finding does not establish a monotone threshold at width nine, arbitrary-width failure, full-shift or infinite-lattice obstruction, or intrinsic dimension. `R=3` is whole-ring on widths 6/7 and near-whole-ring on widths 8/9, so the width-8 passes are near-global finite-ring facts rather than evidence of small-radius locality. The width-nine W1 conflicts are stronger only on those exact finite reachable domains: complete retained two-lag history has become insufficient there.

'''
anchor = '## Relational rank separates available directions from law-used directions'
if '## Cross-width continuation breaks at width nine' not in program:
    if anchor not in program:
        raise SystemExit('program insertion anchor missing')
    program = program.replace(anchor, section + anchor, 1)

item = '''26. **Cross-width two-lag determinism persists through width eight and fails at width nine.** For the frozen `D2,h=2` touching-strip masks `{11,13,15}`, widths 6/7 retain their accepted W1 passes and theorem/regression `R=3` passes; all three masks also pass both W1 and W2 at fresh width 8. At fresh width 9, all three masks fail W1 and therefore also fail W2, with independently replayed canonical conflicts. The pooled width-blind W3 table fails for all three masks; P15 has a canonical n=7 versus n=9 conflict. These are finite reachable-family results. They do not establish a width-nine threshold, arbitrary-width/full-shift/infinite-lattice failure, or intrinsic dimension.

'''
open_anchor = '## What remains open'
if '26. **Cross-width two-lag determinism' not in program:
    if open_anchor not in program:
        raise SystemExit('program exact-results anchor missing')
    program = program.replace(open_anchor, item + open_anchor, 1)

old = '- The relationship between correction depth, spatial dimension, growing spatial radius and minimum causal representation dimension is not yet characterized.'
new = '- The relationship between correction depth, history depth, spatial dimension, growing spatial radius and minimum causal representation dimension is not yet characterized. The cross-width interface-history result adds a finite warning: the same two-lag representation that is globally sufficient through width eight can become globally insufficient at width nine, so neither successful finite closure nor one fitted radius should be promoted to an arbitrary-width law.'
if old in program:
    program = program.replace(old, new, 1)
PROGRAM.write_text(program)

checkpoint = CHECKPOINT.read_text()
cp = '''## Checkpoint 2026-09-12: cross-width two-lag closure persists through width eight and fails at width nine; gate-2 pending

Read `docs/research/2026-09-12-interface-history-cross-width.md`. This unit keeps the accepted #131/#157 touching-strip representation fixed at `D2,h=2`, restricts to masks `{11,13,15}` that passed globally on both predecessor rings, adds fresh exhaustive widths 8 and 9, and tests only the predeclared new radius `R=3` plus one pooled width-blind local table.

- Protocol-only #163 integrated at `7cc4bbae2eb5af50e133b8a8eaf44fb55db358a8` and received independent Claude/Fable Gate 1 there. Clarification-only #165 recorded the required near-whole-ring null before implementation without renewed Gate 1.
- Implementation-only/no-result #166 merged as `ac7ffbb9440a68b8e8956daeee7c07581e75be52` after all 27 exact-head checks were green. It pins independent physical/reference retained-field generation, packed versus tuple grouping for W1/W2/W3, width-blind W3 keys, translation covariance, predecessor controls, canonical conflict replay, permanent workflow and future integrity registration.
- First evaluation #167 executed the unchanged verifier and produced provisional branch evidence, but the permanent replay workflow was necessarily red because an implementation-stage `--self-test` still asserted that the canonical result must be absent. The run was preserved and closed unmerged. Implementation-only #169 changed only that workflow plumbing and merged as `62b3849d2e206c76b84104a695d8079e5f1581cd`; no scientific code, result logic or protocol changed.
- Corrected evaluation #170 regenerated the result independently from the corrected pinned stage. Its cleaned exact head `6ed7a0a00dea00efc770e55d1a215e949c2d3194` contains only `results/interface_history_cross_width_20260912.json`; all five checks, including permanent integrity and byte-for-byte replay, are green. It integrated as `ea247435705349ad936653d05e617187929c3928`.
- Exact result: widths 6/7 pass W1 and theorem/regression W2@R3 for masks 11/13/15; fresh width 8 also passes W1 and W2 for all three masks. Fresh width 9 fails W1 and W2 for all three masks. Therefore P2 and P3 are false.
- Pooled W3 fails for masks 11/13/15, so P4 is false. P15's canonical pooled conflict is cross-width (`n=7` versus `n=9`); masks 11/13 have earlier pooled conflicts between `n=6` and `n=7`. All nine stored W1/W2/W3 conflicts independently replay; primary/reference retained fields and all 27 verdicts agree; translation covariance and predecessor controls pass.
- Interpretation: on the frozen reachable family, two-lag complete-field determinism persists through width 8 but is already lost at width 9 for all three common masks. A width-9 W1 conflict rules out every spatial-radius-only rescue for that exact retained representation/domain. It does **not** establish monotone failure for widths above 9, an arbitrary-width/full-shift/infinite-lattice obstruction, or intrinsic dimension.
- `R=3` is whole-ring on widths 6/7 and near-whole-ring on widths 8/9, omitting only one and two sites respectively. Width-8 W2 success is therefore near-global finite-ring evidence, not small-radius locality.
- **Review state:** canonical evaluation and result reporting are integrated on the gathering branch; this current-account sub-PR updates the living Program/checkpoint. Exact-head independent Gate 2 and reviewer merge remain required before acceptance on `main`.

'''
cp_anchor = '## Checkpoint 2026-09-12: complete two-lag fields recover global determinism'
if '## Checkpoint 2026-09-12: cross-width two-lag closure' not in checkpoint:
    if cp_anchor not in checkpoint:
        raise SystemExit('checkpoint insertion anchor missing')
    checkpoint = checkpoint.replace(cp_anchor, cp + cp_anchor, 1)
CHECKPOINT.write_text(checkpoint)
