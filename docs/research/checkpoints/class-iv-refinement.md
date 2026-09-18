# Checkpoints: Class-IV Refinement

Checkpoint log for the fourth research Program, opened 2026-09-17. Each
section is a Program-scoped checkpoint: a dated statement of state that adds
no evidence. The most recent unit is first. Add a new checkpoint at the top
when a substantial unit completes; keep the bounded-claim style.

Program page: `docs/research/2026-09-17-class-iv-refinement-program.md`

## Checkpoint 2026-09-18 (sixth unit): the defect algebra

- **Completed:** [the defect-algebra unit](../2026-09-18-defect-algebra.md),
  canonical `results/defect_algebra_20260918/` (registered with the fast
  integrity tier). 8 bases × 408 completions (192 random, 96 flip partners,
  120 built into five signature classes); 3,264 evaluations, 37 minutes.
- **A second theorem, independent of the census.** Flipping one cell of a
  beam state changes exactly six reads and **none lands on an exposed
  entry**, so one-step healing is `A(LL,L) ∧ B(L,R) ∧ C(R,RR)`, twelve
  pairwise bit-equalities between free entries, GF(2) rank **eleven**:
  2,048 signature classes of 8,192, a thirteen-dimensional universal-healer
  subspace, expected healing exactly `1/8`. The **edge lemma** extends the
  factorization to every step through a cluster's edges, so `A` is leftward
  growth, `C` rightward, `B` isolated survival, and the corollaries fix
  transverse extinction outright for whole classes. Re-derived by the
  executing session and asserted as a gating control. Knowledge node
  `defect-algebra` (finding, exact).
- **It resolves the fourth unit's non-additivity.** Transverse stability on
  the twelve exclusive-ors gives cross-validated `R²` 0.37–0.43 in every
  base; on the twenty-four raw bits it is **negative** in every base. The
  refinement's effect was never absent, only in the wrong coordinates.
  **Do not repeat "the completion's effect is not bit-additive" without
  this correction.**
- **The open question is answered with one exception.** Refinements built to
  satisfy all twelve sit on the beam in 83–96% of trials in seven of eight
  bases, median proximity 1.000. **P3(a) failed because under the identity
  rule they never do.** So healing isolated defects is very nearly
  sufficient for residence, and there is one base where it buys nothing.
- **P3(b) failed on a clause that is not the theorem's.** Growers never sit
  on the beam (zero everywhere, as the edge lemma requires), but in three
  bases their median proximity *exceeds* the random arm's. **Residence from
  a dense random start is not the same quantity as isolated-defect
  healing**; what sets it beyond the healing signature is the next open
  question.
- **P4(b) held although expected to fail**, so the ten dark entries appear
  unread even by dense random configurations, not merely by isolated
  defects. P1, P2, P3(c), P5, P6 held.
- **On the freeze amendment:** both growers have transverse extinction
  exactly zero, confirming the edge lemma in both directions rather than
  one. Their proximity statistics differ by up to 0.12 with no consistent
  direction, plausibly noise at 24 per cell. **Reflection is not a symmetry
  of this family**, so handedness is never deducible here; measure it.
- **Do not infer:** anything about Class-IV-ness (the object explained is
  inheritance of history gain); that residence equals healing (one base and
  three growers say otherwise); anything at other heights, densities or
  observers. Eight bases is a panel.
- **Process, second consecutive unit where it mattered.** The first launch
  stopped at the matched null-pair control with nothing computed: a dropped
  complement flag and trajectory helpers imported from the previous unit,
  carrying its seed namespace. Cost two minutes instead of a discarded run.
  **Controls before observables, able to fail, is now paying rent every
  unit.** A further rule earned here: do not import another unit's
  measurement helpers; copy them with this unit's seed function, or the
  provenance silently belongs to the other protocol.
- **Next, unfrozen:** what sets beam residence beyond the healing signature
  — the identity-rule exception and the three high-proximity grower bases
  are the two handles.

## Checkpoint 2026-09-18 (fifth unit): the beam mechanism, with a theorem

- **Completed:** [the beam-mechanism unit](../2026-09-18-beam-mechanism.md),
  canonical `results/beam_mechanism_20260918/` (summary registered with the
  fast integrity tier). 16 bases × 256 fresh completions at height two plus a
  transverse tier and a height-three arm; 4,480 evaluations, 49 minutes.
- **A theorem, and it does not depend on the census.** On a height-two strip
  the vertical wrap makes an equal-row state's condition index exactly the
  height-one exposed index, so such a state reads only entries the base rule
  fixes: **the equal-row set is exactly invariant under every rule of the
  family and the strip is the base rule on it.** Proved by index algebra,
  re-derived by the executing session rather than taken on report, and
  asserted as a gating control at heights two and three for all sixteen
  bases. Recorded as knowledge node `invariant-beam` (finding, exact).
- **The mechanism it implies, measured.** History gain is a mixture: the
  base's own one-dimensional value on the beam, a completion-set value off
  it. Beam proximity is a shared mediator; each base responds with the sign
  of its own gain minus the off-beam value; opposite-signed responses to a
  shared mediator are the anticorrelation. P1, P2, P3, P5, P6 held. The
  anticorrelation replicates at −0.341 and **reverses to +0.204** when
  conditioned on proximity; proximity transfers on **every one of the 120
  pairs**; the response ordering against one-dimensional gain is **0.960** on
  sixteen bases, eight of them never used to find the mechanism; on-beam
  medians equal the one-dimensional values and off-beam medians sit in a
  base-indifferent band from 0.029 to 0.170.
- **P4 held although it was the one expected to fail, and that cost the
  comparison it existed to make.** The previous unit put the off-beam value
  near 0.2 bits; measured here it is 0.03 to 0.17, low enough that rules 18
  and 22 still respond positively. The mixture reading (P4′) held on all ten
  testable bases and the naive sign rule agreed with it only because **no
  base on this panel falls in the discriminating window**, which needs a
  one-dimensional gain strictly between zero and that base's own off-beam
  median. A future panel wanting to separate them must be built for it.
- **P7 failed on its first arm.** The anticorrelation does not survive to
  height three (+0.074). The demoted descriptive arm says why: on-beam
  fractions are far higher at height three (0.771 against 0.458 for rule
  110), so nearly everything sits on the beam, the mixture degenerates and
  there is no off-beam population for opposite responses to act on. **This is
  a post hoc reading of a demoted number, consistent with the mechanism but
  not independent support for it.**
- **Do not infer:** that the beam explains Class-IV-ness; it explains
  inheritance of history gain. Nothing about *which* completions attract
  trajectories onto the beam, which is now the open question and is about the
  structure of a completion, not of a base. Sixteen bases is a panel, not a
  census; one contract, one density.
- **Process, recorded because it nearly went wrong.** The first canonical run
  was discarded: its matched null-pair control failed on a copy-paste bug in
  the control's own conjugate beam-state construction, **and** the
  implementation ran that control after the tiers rather than before, so a
  broken control gated nothing. Both fixed, the fix verified in isolation and
  stated before it was run, and the unit re-run in full rather than patched
  so the committed runner is the runner that produced the data. **Controls
  must run before observables and must raise; a control that cannot fail is
  worse than no control.**
- **Next, unfrozen:** what makes a completion attract trajectories onto the
  beam. The unit shows transverse stability gates beam residence almost
  perfectly downward (at most 0.034 on-beam given low stability), so the
  handle exists; an exact single-defect first-step analysis on the beam is
  the natural attack and is a pen-and-computer unit rather than a census.

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

## Checkpoint 2026-09-18, seventh unit — the dense defect algebra

**Completed.** The algebra of a dense configuration at height two, exact and
finite. Every column's two reads land in a stratum decided by the two rows'
three-cell popcount difference: `Δ = 0` exposed (base-owned), `|Δ| = 1` lit,
`|Δ| ≥ 2` dark. The 64 six-bit windows give 8 trivially agreeing cases and 28
unordered pairs — 6 exposed, 15 lit, 7 dark, **no mixed pair**. This
*characterizes* the sixth unit's 8/14/10 entry partition rather than
enumerating it. Ranks 11 and 7 over 24 free entries leave exactly 64
completions (`U++`) satisfying every free constraint. Recorded as its own
knowledge node, `dense-defect-stratification`, finding/exact.

Census: 4,160 evaluations, 20 bases × 7 arms, 57.8 min off Actions. Ten
controls first, all passing, in 170 s. **Held:** P1a, P1b, P2, P3a, P3b, P3c,
P4d, P6a. **Failed:** P4c, P4e, P5, P6b, P7. P4a/P4b split (Spearman held,
strict separation did not). P3c held at odds 0.55.

**Exact facts to build on.** β-all-hold ⇔ totalistic (16 rules), and such a
base with a `U++` completion collapses *any* state in one step — confirmed on
0, 22, 232 × all 64, `agree = 1.000` exactly. Under 204 and 51 the residual is
exactly the width-two anti-phase runs of the initial disagreement field, so
`agree = 1 − 2N_ap/521`; both bases give a **bit-identical** median
`0.9366602687140115` with strata `[50392, 0, 0]`, all blind. Disagreement
survives only through blind columns (T5), verified on trajectories. `ρ` tracks
pair survival at Spearman 0.934, and all twelve `Π = 0` bases have `ρ ≤ 0.005`.

**Corrections this unit forced.**
- The sixth unit's open question was framed around an identity exception the
  coordinator read as "no mixing." **Wrong.** Rule 51 flips every cell every
  step and has the identical residual; totalistic rule 0 heals everything.
  Permanence 1.000 / 1.000 / 0.205 / 0.031 / 0.000 on 204 / 51 / 90 / 5 /
  {0, 22, 110, 30}. Four bits of the base decide it, not activity.
- The coordinator's "base-indifferent grower floor of ~0.75", read off eight
  bases, is **refuted** on twenty: bases 54 and 18 sit at 0.316 and 0.279.

**Do not infer.**
- That the lit/blind split is clean. It is not: `K`, whose residual the
  decomposition calls lit-governed, is ordered by pair survival at −0.454
  where `U++` is at −0.992. The decomposition keeps its direction and loses
  its clean form. This is the single most important negative here, and it
  exists only because the `K` arm was restored against the draft.
- That the handed edge assignment (`e_G = β₁+β₃`, `e_G′ = β₂+β₄`) is
  established. The two scores are identical on 13 of 20 bases (Pearson 0.669),
  each grower is ordered slightly better by the *other* score, and the two
  discriminating within-base tests both failed in the reversed direction.
  **Unsupported on this panel, not refuted** — the panel lacks the power.
- That "frozen background" means "dark stratum matters." P6b reversed: `D+`
  beats random on active bases (+0.095 mean) and loses on frozen ones
  (−0.037). The frozen bases carry among the *highest* random-arm dark counts.
- Anything about height three, other densities, other observers, or `M*`.

**Open, and sharper than before.** What orders residence beyond the blind
bits, given that the blind bits order everything measured here including `K`.
Whether the handed assignment is real needs a panel where `e_G` and `e_G′`
differ on many more than seven bases.
