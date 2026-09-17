# Checkpoints: Class-IV Refinement

Checkpoint log for the fourth research Program, opened 2026-09-17. Each
section is a Program-scoped checkpoint: a dated statement of state that adds
no evidence. The most recent unit is first. Add a new checkpoint at the top
when a substantial unit completes; keep the bounded-claim style.

Program page: `docs/research/2026-09-17-class-iv-refinement-program.md`

## Checkpoint 2026-09-18 (fourth unit): matched completions evaluated

- **Completed:** [the matched-completion unit](../2026-09-18-matched-completion-persistence.md),
  canonical `results/matched_completion_20260918/` (summary registered with
  the fast integrity tier). Eight bases × 512 completions at height two,
  plus a 64-completion replicate tier and a 128-completion height-four arm;
  5,632 evaluations, 49.7 minutes.
- **The persistence axis decomposes.** History gain is base-dominated
  (variance component 0.0396 against the completion's 0.0116); retention is
  completion-dominated (0.0217 against 0.0348); spreading is base-dominated
  too, so retention is the one observable a refinement chooses for itself.
  P1, P2 and P4 held; P4 on both arms including the one expected to fail.
- **Two things beyond the decomposition.** History gain **anticorrelates**
  between distant bases (Spearman −0.414 for 110 against 30) rather than
  merely failing to transfer, which is unexplained and is the most
  interesting object the unit produced. And history gain is not bit-additive
  at all: cross-validated `R²` on the 24 completion bits is negative in
  every base, while retention reaches 0.271.
- **A correction to the Class-IV reading, from the control put there for
  it.** P6 failed because at height four the persistence-only control rule 5
  (1D history gain 0.976 against 110's 0.903) overtakes 110. Height two
  cannot separate them; both are at the ceiling. **Do not infer that rule
  110 is special on the persistence axis**: history-gain inheritance tracks
  the base's one-dimensional history gain, not its informal class. The
  handed census's enrichment stands; Class-IV-ness is not its explanation.
- **Replication, not blind bets, and it mattered.** Every prediction was
  calibrated on a 132-evaluation pilot measuring the same quantities; the
  canonical completions were drawn from a disjoint namespace, so the unit is
  a pre-registered out-of-sample replication and is reported as one. P3
  failed by 0.042 on one of four pilot-set thresholds (0.558 against 0.60,
  pilot 0.81 on sixteen completions) — the exact regression that framing
  anticipated. **Protocols in this Program that set thresholds from a pilot
  must say so per prediction.**
- **On the freeze amendment, stated so it is not miscredited:** P4 was
  scored on degrees-of-freedom-adjusted variance components because raw
  eta-squared is inflated for the 512-level factor. The raw fractions give
  the **same** verdict on both arms. The adjustment removed the risk of an
  artifact deciding a prediction; it did not decide this one.
- **Do not infer:** a mechanism for any of it; anything about bases outside
  the panel of eight; anything at other densities or observers; that the
  transfer matrix's cluster structure is established (its thresholds failed).
- **Next, unfrozen:** whether the sign of the history-gain transfer between
  two bases is predicted by their one-dimensional history gains, over all
  pairs of a panel. That is the first question here whose answer would be a
  mechanism rather than a distribution.

## Checkpoint 2026-09-17 (third unit): handed fiber census evaluated

- **Completed:** [the handed fiber census](../2026-09-17-handed-fiber-census.md),
  canonical `results/handed_fiber_census_20260917/` (summary registered with
  the fast integrity tier). The handed family `f(c, w, n₇)` restricts at
  height one by a coordinate projection **onto all 256 ECAs**, every fiber
  exactly `2²⁴` rules, so rule 110 has a fiber for the first time in the
  Program. P1 held and not narrowly (fiber(110) both-positive 0.543 against
  0.273 for the flagged comparator 30); P2 held in second place behind the
  mirror 124; P3 failed (no chirality effect, point estimate reversed);
  P4 held; P5 held on **both** arms against the drafting agent's expectation;
  P6 held for spreading and replicated the 64-fiber census's shape.
- **The enrichment is on the persistence axis.** Fibers 22 and 30 spread
  more than 110's and still fall far below it on the conjunction. This was
  not predicted.
- **Methodological correction, Program-wide:** the P3 calibration compared
  two *independently seeded* samples of the deduced-identical fibers 110 and
  137, so it rejects at the nominal rate by construction; it did, at
  p = 0.027, and briefly put P3's scorability in doubt. A matched-seed
  control (`control6_matched.py`: same seed stream, complemented initial
  states) shows the implementation exactly complement-covariant to
  1.6 × 10⁻¹⁵. **Null-pair calibrations in this Program must pair the draws,
  not only the distributions.** The run's own control 6 had been
  under-implemented and was completed after the fact; that is recorded as a
  deviation.
- **Do not infer:** a mechanism for the enrichment; that 110 is special
  beyond its fiber sitting in a three-way tie with 124 and 54; anything at
  other heights, densities or observers; anything about east-marked rules
  beyond what reflection deduces. The whole-census tier is twelve rules per
  fiber and cannot order individual fibers.
- **Next, unfrozen:** repeat at strip height four, now that P5 supplies a
  base-level prediction rather than a fiber ranking to reproduce; or ask
  what a fiber's enriched *members* have in common, which the census
  machinery cannot answer as posed.

## Checkpoint 2026-09-17 (second unit): 64-fiber census evaluated

- **Completed:** [the 64-fiber census](../2026-09-17-fiber-census-64.md),
  canonical `results/fiber_census_64_20260917/` (summary registered with
  the fast integrity tier). P1 held (interactions needed for both-positive
  and spreading; persistence additive out of sample), P2 failed on one
  inequality (0 and 90 swap), P3 held (affine bases not special), P4 half
  as bet (B3 for spreading; B0, not S2, for persistence).
- **Do not infer:** a mechanism for the interactions; anything at other
  heights or densities; anything about non-symmetric ECAs.
- **Next, unfrozen:** an anisotropic restriction family giving 110 a fiber;
  or an observer-covariant persistence statistic so the census transports
  across strip heights.

## Checkpoint 2026-09-17 (later): fiber census evaluated

- **Completed:** [the fiber census](../2026-09-17-fiber-census.md), canonical
  `results/fiber_census_20260917/` (summary registered with the fast
  integrity tier). P1–P3 held (fibers differ; fiber(54) both-positive 0.47
  against 0.37/0.25/0.22/0.07 for 22/0/90/204; HighLife and Life typical of
  their fibers), P4 failed (fiber(22) is 72% ballistic, not bimodal). Two
  deviations recorded in the note (a glance at the secondary pass before the
  primary finished; provenance hashes added to the evaluator after the run).
- **Do not infer:** that the base rule carries more than its fixed bits'
  activity (untested); anything about the full plane or about 110.
- **Next, unfrozen:** a 64-fiber census at 128 rules per fiber to separate
  base rule from fixed-bit activity; an anisotropic family for 110.

## Checkpoint 2026-09-17: Program opened from the GPT handoff; fiber census frozen and unrun

Authored by Claude/Fable 5.1. Myk suspended the cross-model review gates on
2026-09-17 (GPT has no GitHub access, no other agent available) and authorized
this session to integrate, self-review and merge; every record below says so.

- **Inherited and recorded (GPT-5.6 Sol, 2026-09-16/17):** the Jev semantic
  scout, Runs 1 and 2 (`2026-09-17-jev-class4-scout-record.md`; raw responses
  and frozen evaluator re-run by Fable, ranks reproduced); the
  selective-persistence × spreading discriminator (`2026-09-17-selective-persistence-discriminator-record.md`;
  report and complete tables survive, the hash-pinned protocols, runner and
  canonical JSON were lost and are reconstructed with explicit non-claims); the
  cross-dimensional 2D panel and the strip spectrum (GPT's notes as written);
  the exact strip restriction (Fable replayed `strip_restriction_exact.json`
  byte-identically). Evaluation preceded review for all of them.
- **Exact facts to build on:** width-one HighLife = ECA 54; Life and B35/S236
  = ECA 22; height-one restriction of the Life-like family is a 12-bit
  quotient onto the 64 reflection-symmetric ECAs (4096-rule fibers); height
  two is injective on the family; the selective-surprisal gap has an exact
  coarse-visible + within-fiber decomposition. Rule 110 has an empty fiber in
  this family (not reflection-symmetric).
- **Frozen and unrun:** the fiber census
  (`protocols/2026-09-17-fiber-census.md`): 512-rule samples of the
  height-one fibers of ECAs 54, 22, 90, 204, 0 at strip height two under the
  starred contract; the bet is that fiber(54) is enriched in the both-positive
  region. Jev Run 3 was acquired the same day by a child session and evaluated:
  J1/J3/J5 reproduce under operational definitions alone, J4 weakens.
- **Do not infer:** a universal Class-IV definition; anything about the full
  plane from finite strips; novelty over the storage × spreading literature;
  hash-level provenance for the 2026-09-16 discriminator; that the
  refinement-depth conjecture is well posed beyond an explicitly restricted
  family (the trivial bolt-on lemma is recorded in the protocol).
