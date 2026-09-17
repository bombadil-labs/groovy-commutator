# Rule 110 gets a fiber, and it is enriched; chirality is not

The two Life-like fiber censuses could only speak about the 64
reflection-symmetric elementary rules, because outer-totalistic rules are
left-right symmetric by construction. Rule 110, this Program's headline
Class-IV rule, had no fiber at all. This unit builds the smallest
anisotropic extension of the Life-like family whose height-one restriction
reaches every elementary rule, and repeats the census contract on it
unchanged.

The headline holds: **the fiber of 110 is enriched in the persistence ×
spreading phenotype**, at 0.543 both-positive against 0.273 for the fiber of
30, and it sits in a statistical tie at the top with the fibers of its mirror
124 and of 54. **Chirality is not detectable**: the family marks one
horizontal direction, so the fibers of 110 and of its mirror are genuinely
different sets of rules, and they are indistinguishable under this contract.
A base's own one-dimensional phenotype predicts its fiber's phenotype on
both axes, which the Life-like family had only shown for spreading.

Evidence: exact for the family, the restriction and the controls;
exploratory for the census (finite samples, one strip height, one density,
one observation contract). Protocol frozen before implementation
(`protocols/2026-09-17-handed-fiber-census.md`); runner and evaluator
committed before the run; evaluation preceded review under Myk's 2026-09-17
suspension of the cross-model gates. Protocol drafted by Claude/Fable 5.1;
reviewed, amended, implemented, run and recorded by Claude Opus 5. Third
unit of the [Class-IV Refinement Program](2026-09-17-class-iv-refinement-program.md).

## The handed family

A rule of `H` is a function `f(c, w, n₇)` of the centre cell, the **west**
neighbour, and the count of the other seven Moore neighbours; the table has
32 entries indexed `i = 16c + 8w + n₇`. The Life-like family embeds in it,
occupying `2¹⁸` of the `2³²` rules.

On a height-one strip the vertical wrap makes `c = C`, `w = L` and
`n₇ = 2L + 2C + 3R`, so the ECA's bit `4L + 2C + R` is the table's bit
`i(C, L, 2L + 2C + 3R)`. The eight indices so reached, in window order, are
`{0, 3, 18, 21, 10, 13, 28, 31}` — all distinct. The restriction is
therefore a **coordinate projection: onto all 256 elementary rules, with
every fiber exactly `2²⁴` rules**. Sampling a fiber is fixing eight bits and
drawing twenty-four.

Height two already reaches all 32 conditions, so the family is a genuine
refinement with no bolt-on freedom, exactly as in the Life-like case.
Complement conjugation preserves `H` and commutes with the restriction, so
the fiber of 137 is the conjugate of the fiber of 110 and the two carry
identical distributions by deduction. Reflection maps `H` to the
*east*-marked family instead, so the fiber of 124 is a different set of
rules and its comparison with 110 is empirical, not deducible.

All controls pass: the indices are distinct, height two is faithful, the
restriction of the Life-like embedding equals the published height-one
formula on all 262,144 rules, the embedded HighLife matches the Life-like
step at several heights and on 5,000 patches, the restriction is onto all
256, and every one of the 256 fibers reproduces its base rule at height one.

## Result

5,268 rules in 46 minutes on four workers, off GitHub Actions: nine panel
fibers at 256 rules each and the remaining 247 at twelve.

| fiber | both | spread | persist |
| --- | ---: | ---: | ---: |
| 124 (mirror of 110) | 0.555 | 0.852 | 0.629 |
| **110** | **0.543** | **0.844** | **0.629** |
| 54 | 0.531 | 0.844 | 0.594 |
| 137 (conjugate of 110) | 0.445 | 0.805 | 0.504 |
| 22 | 0.422 | 0.922 | 0.469 |
| 30 | 0.273 | 0.906 | 0.312 |
| 90 | 0.223 | 0.777 | 0.262 |
| 0 | 0.164 | 0.281 | 0.223 |
| 204 | 0.105 | 0.242 | 0.293 |

**The enrichment is on the persistence axis, not the spreading one.** Fibers
22 and 30 spread *more* than 110's does, at 0.922 and 0.906 against 0.844,
and still land far below it on the conjunction, because they persist at 0.469
and 0.312 against 0.629. Whatever the quotient at 110 confers, it is the
ability to hold a disturbance rather than to propagate one. This was not
predicted and is not something the Life-like censuses could have shown, since
persistence there was bought by birth-on-zero across the board.

- **P1, that 110's fiber is enriched: held, and not narrowly.** It beats
  every comparator, including the one the protocol flagged as risky: 30, at
  `p = 5 × 10⁻¹⁰`. The worry was that enrichment would track how much
  activity the exposed bits fix rather than the base's own dynamical class,
  since 110 fixes three survival conditions on and 30 only two, and the
  64-fiber census found survivals *lower* the fraction. It wins by a factor
  of two regardless.
- **P2, that 110 lands in the top two: held, in second place.** Excluding
  the deduced duplicate 137, the order is 124, 110, 54, then 22, 30, 90, 0,
  204. The top three differ by less than a standard error and are
  statistically indistinguishable (110 against 54, `p = 0.79`).
- **P3, that chirality is detectable: failed.** See below; the failure is
  clean and the point estimate leans the other way.
- **P4, that the symmetric ordering survives the change of family: held**
  on all three inequalities, with 54 above 22 at `p = 0.013`.
- **P5, that a base's 1D phenotype predicts its fiber: held on both arms**,
  against the drafting agent's stated expectation that the persistence arm
  would fail. Bases whose orbit representative spreads in one dimension have
  fiber spread fractions at median 0.833 against 0.500 (`p = 2 × 10⁻¹⁶`,
  38 against 218 bases); bases with 1D `S > 0` have fiber persist fractions
  at median 0.583 against 0.333 (`p = 3 × 10⁻⁹`). In the Life-like family
  persistence looked like a purely two-dimensional activity effect, bought
  by birth-on-zero. Here it tracks the base. Fibers are not independent,
  so these p-values are descriptive.
- **P6, that non-additivity replicates in eight bits: held for spreading**,
  and replicates the 64-fiber census's *shape*, not just its verdict.
  Interactions win out of sample for spread (leave-one-fiber-out log-loss
  0.671 against 0.685) and do not for both-positive (0.575 against 0.573)
  or persistence (a tie). Spreading is again the non-additive axis.

## The calibration that failed, and what it taught

P3's frozen text carried a calibration: the null pair 110/137, whose
distributions the protocol *deduces* to be identical, must not reject. It
rejected, on the both-positive fraction, at `p = 0.027`. By the frozen text
that made P3 unscorable until resolved.

Resolving it exposed a gap in this unit's own controls. The run's control 6
checked only that conjugates land in fiber(137); it never compared
observables, so it could not have caught a covariance break. The full
control (`control6_matched.py`) supplies both halves:

- the step identity `handed_step(¬S, conj R) = ¬ handed_step(S, R)` holds
  exactly, at four strip heights;
- eight fiber(110) members and their conjugates, driven by the **same seed
  stream with complemented initial states**, agree on `R*`, `M*` and
  `alpha_x` to `1.6 × 10⁻¹⁵`.

So the implementation is exactly covariant and the rejection was chance.
**The calibration itself was the flaw.** It compared two *independently
seeded* samples drawn from the same distribution, which rejects at the
nominal rate by construction, so it could never have distinguished an
implementation fault from a one-in-thirty-seven fluctuation. A null-pair
calibration has to pair the draws, not just the distributions. Future
protocols in this Program should state the matched form.

With that resolved, P3 is scored on its direct test and fails cleanly:
spread 0.844 for fiber(110) against 0.852 for fiber(124), `p = 0.81`, the
point estimate leaning opposite to the prediction. The argument for a
direction was that the two fibers differ by swapping the fixed values at two
conditions of Moore multiplicity 35 and 21, so 110's fiber fixes birth on
the commoner condition. That reasoning predicts nothing measurable here.
Under this contract, marking a direction changes *which* rules are in the
fiber without changing what the fiber is like.

## What this does and does not show

The Program's central question can now be asked of its headline rule, and
the answer is yes: the height-one quotient at 110 predicts enrichment of its
preimages. Two independent things support it rather than one. The panel puts
110's fiber at the top with 54's, and the whole census shows the base's own
one-dimensional phenotype predicting its fiber's on both axes across all 256
bases. That second result is the stronger one, because it does not depend on
any single rule being special.

Bounds. Twelve rules per fiber cannot order individual fibers; the panel
numbers are the ones with standard errors worth quoting. One strip height,
one density, one observation contract, and the observer is itself
reflection-symmetric while the family is not. Nothing here is a definition
of Class IV, and nothing is a mechanism: enrichment is a correlation between
a quotient and a phenotype, measured under one contract.

Descriptive, unscored: pooled over the 64 symmetric bases the handed family
spreads more than the Life-like family did (0.509 against 0.421) at similar
persistence (0.438 against 0.468). Fiber fractions correlate weakly with the
[forced-table](2026-09-17-forced-tables.md) invariants, the largest being
table size against spreading at Spearman 0.44.

## Deviations

The evaluator's descriptive forced-table join assumed a dictionary schema
where `invariants.json` is a list. It crashed before writing or printing any
output; the fix touched only that unscored section, and no scored result had
been read. Afterwards the evaluator was re-run to record the control-6
hashes in its provenance block, changing no analysis, no threshold and no
outcome.

## Next

Two candidates. Repeat at strip height four, now that P5 gives a
base-level prediction to test rather than a fiber ranking to reproduce.
Or ask what the fiber's *enriched members* have in common, which is the
first question in this Program that the census machinery cannot answer as
posed.

## Files

`experiments/handed_fiber_census_20260917/run.py`, `evaluate.py`,
`control6_matched.py`; `results/handed_fiber_census_20260917/`
(`rows.json`, `exactness_control.json`, `control6_matched.json`,
`summary.json` with source hashes, `handed_panel.svg`,
`handed_fiber_vs_1d.svg`).
