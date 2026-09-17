# The base sets history gain, the completion sets retention

The handed census found rule 110's refinement fiber enriched on the
persistence axis rather than the spreading one. Persistence is a
conjunction of two things: retention (`R*`, how much a site's own state
predicts its successor beyond the reference) and history gain (`M*`, how
much eight steps of its past adds). This unit asks which of the two the
source rule confers on its refinements, and which the refinement chooses
for itself.

The answer is a clean dissociation. **The base sets history gain; the
completion sets retention.** Holding a completion fixed and varying the
base, 110 beats 30 on history gain for 87% of completions while their
retention difference is null. Across the whole grid the variance in history
gain is dominated by the base and the variance in retention by the
completion. And history gain does not merely fail to transfer between
distant bases, it **anticorrelates**: a completion that buys rule 110
history gain costs rule 30 history gain.

Evidence: exploratory. One strip height for the main grid, one density, one
observation contract, eight bases. Protocol frozen before implementation
(`protocols/2026-09-18-matched-completion-persistence.md`); runner and
evaluator committed before the run; evaluation preceded review under Myk's
2026-09-17 suspension of the cross-model gates. Protocol drafted by
Claude/Fable 5.1; reviewed, amended and executed by Claude Opus 5. Fourth
unit of the [Class-IV Refinement Program](2026-09-17-class-iv-refinement-program.md).

**Standing of the predictions.** Every prediction here was informed by a
132-evaluation pilot that measured the same observables in the same bases,
with thresholds set around what the pilot saw. The canonical completions
come from a disjoint seed namespace and none of the pilot's are reused, so
this is a **pre-registered out-of-sample replication**, not a set of blind
bets. It is reported as such. One prediction failed in exactly the way that
distinction predicts.

## The design

Because the handed family's height-one restriction is a coordinate
projection, a 24-bit completion is **one object shared by every fiber**:
`embed(r, u)` exists for every base `r` and every completion `u`. That makes
a matched grid possible. Eight bases `{110, 54, 22, 5, 30, 90, 0, 204}` ×
512 completions at height two, with every seed keyed on the completion and
the stream and never on the rule table, so all eight bases start from the
same initial states, score the same sites and disturb the same origins. Base
5 is the recovered discriminator's persistence-only control (one-dimensional
`M = 0.976`, `alpha = 0`), included so that history-gain inheritance can be
told apart from Class-IV-ness. Plus a 64-completion replicate tier on an
independent stream as the noise floor, and a 128-completion arm at height
four. 5,632 evaluations, 49.7 minutes, four workers, off GitHub Actions.

## Result

| base | `M* > 0` | `R* > 0` | persist | spread | both |
| --- | ---: | ---: | ---: | ---: | ---: |
| 110 | 0.986 | 0.580 | 0.574 | 0.818 | 0.473 |
| 5 | 0.980 | 0.674 | 0.668 | 0.299 | 0.219 |
| 22 | 0.984 | 0.453 | 0.445 | 0.928 | 0.422 |
| 54 | 0.975 | 0.596 | 0.590 | 0.846 | 0.516 |
| 0 | 0.822 | 0.258 | 0.242 | 0.342 | 0.176 |
| 204 | 0.785 | 0.287 | 0.232 | 0.229 | 0.082 |
| 90 | 0.564 | 0.521 | 0.254 | 0.779 | 0.201 |
| 30 | 0.467 | 0.568 | 0.299 | 0.896 | 0.250 |

History-gain positivity separates the bases sharply, from 0.986 down to
0.467. Retention positivity is comparatively flat, 0.674 down to 0.258, and
its ordering is different: rule 30, near the bottom on history gain, sits
mid-table on retention.

**Variance components** (degrees-of-freedom adjusted; raw `η²` in brackets):

| observable | base | completion |
| --- | ---: | ---: |
| history gain `M*` | **0.0396** [0.361] | 0.0116 [0.185] |
| retention `R*` | 0.0217 [0.126] | **0.0348** [0.310] |
| spreading `alpha_x` | **0.0808** | 0.0364 |

Spreading is base-dominated too, so the completion-dominated observable is
retention specifically, not "everything except history gain."

- **P1 held.** With the completion held fixed, `M*(110) > M*(30)` for 87.1%
  of the 512 completions (bet: at least 85%), while the paired retention
  difference is null: sign fraction 0.488 inside the required `[0.40, 0.60]`
  and mean difference 0.011, well inside 0.10.
- **P2 held, far more strongly than bet.** Retention transfers from 110 to
  30 at Spearman 0.680; history gain transfers at **−0.414**. The bet asked
  for a gap of 0.40 and got 1.09. The negative sign was not predicted and is
  the sharper finding: the same completion pushes the two bases' history
  gain in opposite directions.
- **P3 failed, by 0.042 on one of four thresholds.** History-gain transfer
  from 110 to 54 is 0.558 against a required 0.60. The 16-completion pilot
  saw 0.81. This is precisely the regression that the replication framing
  anticipated, and it is the clearest argument in this unit's favour for
  having refused to call these blind bets. The cluster structure the
  prediction was reaching for survives its own thresholds: transfers from
  110 run positive to 54 (0.558), 5 (0.543) and 22 (0.454), negative to 30
  (−0.414) and 90 (−0.254), and near zero to 0 (0.061) and 204 (0.055).
- **P4 held on both arms**, including the one the drafting agent expected to
  fail. **This was not decided by the freeze amendment**, and saying so
  matters: the raw `η²` fractions give the same verdict on both arms. The
  degrees-of-freedom adjustment sharpened the history-gain ratio from 1.9×
  to 3.4× and removed the risk that an artifact would decide a prediction,
  but full scale corrected the pilot's contrary ordering on its own.
- **P5 failed as a conjunction while its halves came apart informatively.**
  History gain is **not bit-additive at all**: cross-validated `R²` of a
  ridge fit on the 24 completion bits is negative in every one of the eight
  bases (best −0.02). Retention is partly additive, up to 0.271 in base 22,
  which breaches the 0.25 ceiling. Test-retest is 0.955 or better for history
  gain and retention in every base; the single value under 0.90 is spreading
  in base 110 at 0.842, a noisier log-ratio observable. So the completion's
  effect is real and reliable, and the reason it resists a 24-bit linear
  model differs by observable.
- **P6 failed, and the control that broke it is the one put there for the
  purpose.** At height four, base 5 overtakes 110 on mean history gain, 0.290
  against 0.277, and the paired sign fraction against 30 is 0.688 against a
  required 0.75. Base 5 is the persistence-only control, with one-dimensional
  history gain 0.976 against 110's 0.903. Height two cannot separate them
  because both sit at the ceiling (0.980 and 0.986). So **history-gain
  inheritance tracks one-dimensional history gain, not Class-IV-ness** —
  exactly the confound base 5 was included to expose, and it exposed it.

## What this does and does not show

The Program asked whether a source rule confers a susceptibility on its
refinements. It does, and this unit says which susceptibility: the base
confers history gain, and it does so in a way no linear reading of the
completion bits can reproduce. Retention is the refinement's own business.
That is a decomposition of the previous unit's headline, not a restatement
of it.

It also removes rule 110's claim to be special on this axis. P6's failure is
the honest version of that: whatever makes a base confer history gain is
visible in its one-dimensional history gain, and a Class-II persistence-only
rule does it slightly better than 110. The enrichment is real; the
explanation is not Class-IV-ness.

Bounds. Eight bases, not 256; the transfer matrix's cluster structure is
descriptive and its thresholds failed. One contract, one density, height two
for the main grid with height four only on a 128-completion arm. Nothing here
is a mechanism: a variance decomposition says where the variation lives, not
why. The negative transfer between 110 and 30 is the most interesting object
in the unit and it is entirely unexplained.

## Deviations

The evaluator's descriptive height-four censoring count assumed a boolean
where `selective_r` returns the unsupported symbols as a list. It crashed
before writing or printing any output, and the fix touched only that
reporting line. No rule was censored: all 1,024 height-four evaluations used
the Monte Carlo reference with every symbol supported.

## Next

The negative transfer wants an explanation, and it is the first question in
this Program whose answer would be a mechanism rather than a distribution.
A cheap first cut: whether the sign of the transfer between two bases is
predicted by their one-dimensional history gains, over all 28 pairs of the
present panel or a wider one.

## Files

`experiments/matched_completion_20260918/run.py`, `evaluate.py`;
`results/matched_completion_20260918/` (`rows.json`, `controls.json`,
`summary.json` with source hashes).
