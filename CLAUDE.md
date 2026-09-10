# Groovy Commutator — project context for Claude Code

## What this is
A generalization of the operator commutator `[A,B] = AB - BA` to discrete
dynamical systems (1D elementary cellular automata) instead of continuous
quantum operators. Origin demo: https://liet-codes.github.io/wet-math/commutator.html

Core construction, for a single CA rule `phi`:

```
D(S) = S XOR phi(S)            differentiation
E(S) = phi(S)                  evolution (I is trivial for elementary CA)
G(S) = C(D(E(S)), E(D(S)))     the commutator
```

`G(S)` is literally the operator commutator `[D, E]` evaluated at the state `S`.
All of this is implemented in `src/groovy/` — read the module docstrings
first, they carry the math. Full interpretive writeup and citations are in
`NOTES.md`, kept separate so this file stays short.

## Ongoing research and the public site

Start with `docs/research/2026-09-07-history-and-possibility.md` for the wider
program: how inherited structure enables further activity and remains
revisable. Observed-history prediction is one workstream. Keep it distinct
from historical influence within the dynamics and from future capability.
The finite repertoire and costed/returning-task comparisons are complete;
learning reusable primitives remains open. The latest completed unit is the
interface-state experiment and unbounded-escape proof. The 3D hypothesis is parked by explicit user
instruction; continue the fixed 2D workstream. Read its continuation below before the historical
agenda checkpoint and dimensional/provenance continuations.
Do not promote earlier dialogue's unverified numbers or ethical analogies into results.

Capture each substantial new experiment, correction, or open research plan
as a dated Markdown note in `docs/research/` and register it in
`site/content/research.json`. The site build renders these into the Research
index and individual pages. Follow `docs/research/README.md` for metadata,
evidence labels, and the promotion workflow. Keep the main pages accessible:
write full methods and mathematical detail in Research, then periodically
review candidates and write selected insights into Home, Concepts, Questions,
or The Walk with a link back to the supporting note. Evidence strength and
editorial readiness are separate decisions. Corrections to existing main-page
claims should be made promptly and linked to their research record.

Maintain the current knowledge account in `docs/knowledge/` and
`site/content/knowledge.json` as research advances. Follow
`docs/knowledge/README.md`: one focused entry per concept, finding, question,
theory, or experiment; explicit status; typed directed relationships with a
rationale and research provenance. Record dependencies deliberately rather
than inferring them from ordinary links. When a claim changes, inspect its
direct and indirect dependents and update affected accounts. Preserve refuted
theories and superseded entries. The public knowledge base generates backlinks
and review notices, but never changes conclusions automatically.

Run `npm run test:research --prefix site` and `npm run build --prefix site`
after changing notes or their catalog. Do not edit generated `site/research/`
or repo-root `public/` files. Publication remains the existing GitHub Pages
workflow; research source and result changes now also trigger that workflow.

## Established results (don't re-derive these, build on them)

1. **Affine implication (converse corrected 2026-09-07).** If `phi(S) =
   M S XOR c` is GF(2)-affine, then `G(S) = c` for every S. The converse
   previously stated here is false: nonlinear rules **4 and 200** also have
   `G ≡ 0`. Exhaustive five-cell causal-window enumeration gives zero-G
   rules {0,4,60,90,102,150,170,200,204,240} and one-G rules
   {15,51,85,105,153,165,195,255}; all other ECA commutators vary with S.
   `scripts/verify_history_algebra.py` reproduces this and the exact Rule
   90/110 comparison in `results/history_algebra_checks.json`. The affine
   implication is dimension-free; the exhaustive converse classification
   just listed is specific to elementary CA. See NOTES.md §2 for the
   mathematical derivation and the qualified QM analogy.

2. **Cross-rule commuting is a real, solved, named problem.** Moore &
   Boykett, "Commuting Cellular Automata," *Complex Systems* 11(1), 1997 —
   algebraic conditions for when two CA rules commute under composition.
   Confirmed empirically here. Related: Hedlund 1969 (the CA centralizer
   problem), the Moore–Myhill Garden of Eden theorem (non-surjectivity /
   lossy rules, relevant to the "drain" regime below).

3. **Five empirical regimes for rule PAIRS**, from
   `operators.divergence_trajectory` (two divergent unfoldings of the *same*
   initial state: path1 = repeat(A, then B), path2 = repeat(B, then A)):
   - **commute** — flat zero disagreement forever
   - **crystalline** — flat *nonzero constant* disagreement (kinematic mismatch)
   - **noisy divergence** — disagreement settles near 0.5, compressibility ≈ 1.0 (indistinguishable from noise)
   - **structured divergence** — disagreement nonzero but compressibility well below 1.0 — the genuinely new regime, doesn't exist in the single-rule case at all
   - **drain** — disagreement spikes then collapses to zero (the two paths fall into a shared trivial attractor)
   The drain regime is NOT coordination between the paths — it's caused by
   both rules independently destroying state-space information (low
   `metrics.image_ratio`, i.e. abundant Garden-of-Eden configurations).
   Confirmed directly: two paths from *unrelated* random initial conditions
   under rules 184/250 still converge to the identical all-ones fixed point
   by step ~12.

4. **Full exhaustive sweep, done** (was the open task, now complete — pilot
   findings below are superseded by this). All 256 rules, all 32,640
   unordered pairs, seeds (1,2,3,4,5), n=100, steps=100. Run via
   `scripts/run_full_sweep.py` (multiprocessing, checkpointed) →
   `results/sweep_full.parquet`; regime-classified and joined with
   per-rule `image_ratio` via `scripts/aggregate_sweep.py` →
   `results/sweep_full_classified.parquet` + `results/sweep_summary.csv`.
   Regime counts: **structured 14751 (45%)**, crystalline 7302 (22%),
   noisy 5414 (17%), drain 4009 (12%), commute 1164 (4%). Structured
   divergence — the regime with no single-rule analog — is the *modal*
   outcome at full scale, not a rare special case. Mean
   `min(image_ratio_a, image_ratio_b)` by regime: drain 0.214, structured
   0.195, commute 0.245, crystalline 0.140, noisy 0.319 — drain's
   image_ratio range overlaps heavily with crystalline and structured,
   reconfirming at full scale (not just the rule-4 counterexample) that
   image_ratio alone does not cleanly separate the regimes.
   `classify.classify_regime`'s thresholds have since been checked
   against the real distribution (result 6) and the drain count above has
   a known inflation (result 5).

5. **Drain mechanism, answered — with a label correction** (2026-07-01,
   `scripts/experiment_drain_predictor.py` → `results/drain_predictor.parquet`
   + `site/src/data/drain_predictor.json`). Two findings:
   - **The sweep's drain label conflates two populations.** Of 4,009
     labeled drains, 2,754 never converge (median final disagreement
     0.418 — the `peak - final > 0.15` shape rule fires on early
     transients). True convergence (final = 0 after peak > 0) covers
     2,150 pairs: 1,255 labeled drain + 895 "quiet drains" filed under
     crystalline because their transient peak stayed below 0.15. Honest
     drain census ≈ 2,150 pairs (6.6%), not 4,009 (12.3%).
   - **What predicts true convergence: two properties of the PAIR,
     computed exhaustively at n=12.** (a) The eventual image of the
     composed round map — push all 2^12 states through (phi_b ∘ phi_a)
     repeatedly, dedup between rounds, until the image stops shrinking —
     collapses to a tiny set, AND (b) the two orderings' eventual images
     are the *same* set (Jaccard overlap). Converged pairs: median image
     3 states, median overlap 1.0. Crystalline is the near-miss: similar
     collapse (median 92 states) into *disjoint* attractors (overlap
     0.046). AUC for converged-vs-rest 0.908 by image size (old
     min-image_ratio baseline: 0.692); the crisp rule "shared attractor
     ≤ 4 states" gets precision 0.76 / recall 0.68 — n=12 exhaustive
     structure predicting n=100 sampled behavior. The rule-4
     counterexample fully resolves: 4/30, 4/126, 4/54 collapse to shared
     images of 3, 1, 1 states; 4/18 keeps 67 states at overlap 0.47 and
     doesn't drain. The residual predictor error is NOT mainly ring-size
     mismatch — measured (`scripts/experiment_drain_scaling.py` →
     `site/src/data/drain_scaling.json`, all 2,150 converged + 6,000
     sampled non-converged): AUC 0.893 / 0.912 / 0.908 / 0.915 at
     n = 8/10/12/14. Saturates by n≈10; even 256 states nearly matches
     16,384. Remaining error is dominated by the ground truth (5 sampled
     seeds per pair at n=100), not the predictor's scale. The best
     operating point does sharpen slowly with n (F1 0.84 at n=8 → 0.88
     at n=14 with threshold scaled to 64 states).

6. **Classifier thresholds validated against the full distribution**
   (2026-07-01, `scripts/experiment_threshold_check.py` →
   `site/src/data/threshold_check.json`). The compressibility histogram
   of the 27,467 shape-undecided pairs is genuinely bimodal at the low
   end, and `CRYSTALLINE_COMPRESSIBILITY = 0.10` sits in the empirical
   valley (the 0.10–0.12 bin is the histogram minimum). The noisy cut is
   soft — no valley, a smooth ramp into the incompressible spike at 1.0 —
   but the headline "structured is the modal regime" is robust: it holds
   for any noisy cut in [0.60, 0.98] and any crystalline cut up to ~0.20.
   Verdict: keep 0.10/0.85, no refit needed; the structured/noisy split
   specifically should be described as a judgment call, not a natural
   boundary.

7. **Pre-hoc composition (4-input rules): implemented; collapse theorem;
   coupling produces emergence** (2026-07-01, `src/groovy/prehoc.py`,
   JS mirror in `site/src/lib/groovy-engine.js`,
   `scripts/experiment_prehoc_coupling.py` → `results/prehoc_coupling.csv`
   + `site/src/data/prehoc_coupling.json`).
   - A 16-entry 4-input table (indexed `8x + 4l + 2c + r`) is exactly an
     ordered pair of elementary rules — x selects per cell which applies.
     Only 512/65,536 tables (0.8%) are post-hoc separable
     (f = g(l,c,r) XOR h(x)).
   - **Collapse theorem**: if x is any same-time radius-1 function of the
     same state (x = mu(S), mu elementary), the 4-input rule collapses to
     the elementary rule `table[8*mu[idx] + idx]`. The absential field IS
     elementary rule 50; D(·,psi) IS elementary rule psi ^ 204 — so
     feeding a rule its own derivative or absential field pre-hoc buys
     nothing new. Escape requires input from another *time* (memory, cf.
     `secondorder.py`) or another *trajectory*. Verified computationally
     in Python and live in-browser on the questions page.
   - Mutually coupled layers (each layer's x = the other layer's current
     state): 1,500 random pre-hoc samples span the full compressibility
     range (median 0.70) while 1,500 post-hoc XOR controls pile up at
     noise (median 1.01). Three "emergent" examples found where all four
     component rules are boring alone (solo compressibility < 0.10) but
     the coupled system is structured — robust across 20 seeds each:
     (77,55|44,23), (237,93|71,221), (164,235|223,160). Suggestive, not
     established: one sampling run, one (mutual, symmetric) topology, one
     lattice size.

8. **Non-uniform CA (rule-as-state): implemented; second collapse
   theorem; selection appears uninvited** (2026-07-01,
   `src/groovy/nonuniform.py`, JS mirror in
   `site/src/lib/groovy-engine.js`, `scripts/experiment_nonuniform.py` →
   `results/nonuniform_rulefield.csv` + `site/src/data/nonuniform.json`).
   Closes the "rule sharing state's dimensionality" open direction.
   - Rule field R = (n,)-array of rule numbers; `apply_rule_field` steps
     each cell by its own rule; `rule_field_bitplanes` exposes R as 8
     state-shaped binary fields (all existing diagnostics apply).
   - **Read-from-state collapses**: rule numbers re-read each step from
     the 8 state bits around each cell (`read_rule_field`) make
     S(t+1)[i] a fixed function of S(t)[i-3..i+4] — i.e. ONE uniform
     radius-4 CA. Verified cell-by-cell against the explicit 256-entry
     window LUT. Same moral as the prehoc collapse theorem: same-time
     rule extraction remains a fixed local CA. A persistent rule field is
     one different construction, not a prerequisite for meaningful
     instruction/state representations (see the September 8 shared-space note).
   - **State-gated rule transport** (`step_gated_diffusion`: live cell
     copies left neighbor's rule, dead cell keeps its own; R persists):
     60 seeds, n=100, 200 steps. Diversity falls 82 → 20 median distinct
     rules and STABILIZES (never below 15) — sustained polyculture, not
     monoculture. Selection gradient is perfectly monotone:
     P(rule value survives | popcount) = 0.875 at popcount 0 falling to
     0.000 at popcount 8; restless-rule (bit0=1) cell share halves
     (0.498 → 0.189); yet cell share peaks at popcount 2-3, not 0 —
     persistence needs quiescence (only live cells get overwritten) but
     propagation needs live neighbors. Every heterogeneous condition
     (frozen random field 0.16, mosaic 0.11, gated transport 0.14,
     read-from-state 0.26) lands state-trajectory compressibility in the
     structured band, vs uniform baselines at the extremes (rule 4:
     0.03; rules 30/90: 1.00; rule 110: 0.82). Transport-scheme
     robustness now tested (`scripts/experiment_nonuniform_transport.py`
     → `site/src/data/nonuniform_transport.json`, 60 runs each):
     rightward copy reproduces every statistic (symmetry control); gated
     XOR-recombination — which INVENTS rules (57% of final cells carry
     values absent at t0, diversity plateau ~67 not ~20) — still shows
     the same selection direction (final pool enriched 2.1× at popcount
     0, depleted ~3× at the restless end, restless bit 0.50 → 0.25).
     The quiescence pressure belongs to the gate (only live cells get
     overwritten), not the variation mechanism. Plateau-vs-n scaling
     (`scripts/experiment_nonuniform_scaling.py`): median plateau
     10/21.5/36.5/63/96.5 distinct rules at n=50/100/200/400/800,
     log-log slope 0.81, each verified flat out to t=1600 — genuinely
     stable polycultures at every size, sublinear in n. Dimension
     robustness (`scripts/experiment_nonuniform_2d.py` +
     `ca2d.apply_rule_field_2d`/`step_gated_transport_2d`): per-cell
     Life-like rules (9-bit born/survive masks) on a 64×64 torus
     reproduce everything — monotone survival gradient 1.000 → 0.000
     across born-popcount 0→9, mean born-popcount 4.5 → 2.6, restless
     born-on-0 bit 0.50 → 0.36, stable ~283-rule polyculture. Remaining
     caveat: correlation, not proven mechanism.

9. **Pair-lineage meta-evolution: bigger rule space does not buy
   open-endedness** (2026-07-01, `scripts/experiment_metaevolution_pairs.py`
   → `results/metaevolution_pairs.csv` +
   `site/src/data/metaevolution_pairs.json`). Lineage protocol lifted to
   coupled two-layer pre-hoc systems (4 component rules = 2^32 configs;
   generator = 8-bit samples of A, B, A^B, absential(A); handoff
   classified on old-vs-new system disagreement of layer A). 40 seeds,
   60-generation budget: 98% lock-in, onto fixed points and 2-cycles
   only, median 14 generations (vs ~10 in single-rule space) — a 16
   million× larger space bought ~2× longer search and no open-endedness.
   Points "why do lineages settle" away from rule-space size toward the
   state→rule feedback structure. Suggestive: one generator
   construction, one topology.

10. **Absential Class-IV detector: established negative (fair 2D test);
   affine theorem is dimension-free** (2026-07-01, `src/groovy/ca2d.py`
   — Python 2D engine at parity with the JS one,
   `scripts/experiment_absential_2d.py` → `results/absential_2d.csv` +
   `site/src/data/absential_2d.json`). Seven Life-like rules from soup
   (60×60 — NOT 64×64, the parity rule is nilpotent on power-of-two
   tori; Day & Night at 0.5 soup density, it dies at 0.15), settled
   window steps 140-240, 8 seeds. Absential-field compressibility is a
   monotone rescaling of raw-state compressibility in every condition —
   slightly MORE compressible in 1D, slightly LESS in 2D (denser Moore
   halo), never cross-cutting — including the hypothesis's home turf
   (pure still-life fields 0.005 raw / 0.005 abs; pure glider fields
   0.034 / 0.051). Hypothesis dead; stop testing it. Consolation
   results: (a) plain settled-window compressibility bands the informal
   classes on its own (frozen 0.01-0.02, Class IV tight middle band
   0.32-0.36, additive 0.61, chaos 0.79); (b) B1357/S1357 "Replicator"
   is neighbor parity = the 2D rule 90, and G2 ≡ 0 on 50/50 random
   grids (Life nonzero on 50/50 controls) — the affine theorem (result
   1) is not a 1D artifact.

11. **The run calculus; U-engine slice read out of the sweep** (2026-07-03,
   `src/groovy/operators.py::identity/orbit/run` + JS mirror, laws
   asserted in `scripts/experiment_run_calculus.py`; slice lookup in
   `scripts/experiment_u_engine_slice.py` → `results/u_engine_slice.csv`;
   full writeup NOTES.md §10). Every spacetime picture is
   `run(gauge, base, S0)[t] = gauge(base^t(S0))`; `orbit` is the only
   iteration; `engine(F) = run(F, F)` (reflexive) = orbit of a composite.
   Laws: runs are LINEAR in the gauge (`run(f⊕g, base) = run(f,base) ⊕
   run(g,base)`, so the G gallery is the (D∘E)-gallery ⊕ (E∘D)-gallery);
   re-anchoring `run(g∘base, base)[t] = run(g, base)[t+1]` is a
   gauge-stance theorem with no engine analog; reflexivity breaks
   linearity (E ⊕ D = id as maps, yet engine(E) ⊕ engine(D) ≠ engine(id),
   ~0.48 disagreement). R(A,B) reformulates as: when is the XOR of two
   engine runs itself an engine run? Since D(·,φ) is rule φ^204, the
   single-rule U construction (engines E∘D vs D∘E) is
   divergence_trajectory(φ^204, φ) — already classified by the full
   sweep: U spans all five regimes (structured 106 / drain 58 /
   crystalline 56 / noisy 26 / commute 10 per rule); the commute set is
   exactly the 8 linear rules (a linear map commutes with any polynomial
   in itself) plus nonlinear {4, 200}; the 8 biased-affine rules are all
   crystalline at mean disagreement 0.99. Notation conventions now
   site-wide: identity map = blackboard 𝟙 (NOT `I`, which stays
   integration); φ = the base's rule, ψ = a gauge's ingredient rule.

## Research continuation: history and possibility (2026-09-07)

`docs/research/2026-09-07-future-repertoire.md` records a protocol committed
before evaluation: all initial states on widths 6/9/11, 66 pairs from rules
{0,4,30,51,54,90,110,150,170,184,204,250}, all exactly-h action words for
h=0..6, identity and population-count views. Scripts
`experiment_future_repertoire.py` and `report_future_repertoire.py` generate
2,772 aggregate rows, six independently replayed witnesses, summary and figure.
Engine, direct-word/set, zero-horizon, and identity/reset controls pass.

At h=6 under identity, equal-size/different-set cases are 258/2763/10615
and equal-set/different-action-map cases are 281/831/2399 at widths 6/9/11.
The respective denominators are 4224/33792/135168 pair-state cases. These are
exact bounded counts, not independent samples. Simple reset/complement and
Rule 4/30 examples separate counts, set membership, and action responses;
the reset/complement example also restores an option at two ticks that was
absent at one. These distinctions are not unique to complex rules.

Possibility here comes from declared external actions. Different histories
act through different complete present states; no intrinsic agency, viability,
or new action invention was measured. Exactly-h sets need not grow with h,
and different pairs have different action alphabets. Do not rank intrinsic
freedom by their set sizes.

The next unit is now complete in `docs/research/2026-09-07-costed-primitives.md`
and `docs/research/2026-09-07-macro-local-equivalence.md`. Scripts
`experiment_revisable_primitives.py` and `experiment_macro_local_equivalence.py`
compare four library policies with explicit physical, dispatch, construction,
trace, and revision costs. There are 294,912 finite configurations plus 98,304
all-width local-map configurations; all encodings, engine, witness, and
price-bound checks pass. All-width equivalence is established on every
17-bit causal window for words up to eight ticks; shortest-program search
is still bounded to eight ticks.

At primary dispatch=1, trace=4, K=4, useful inherited macros give revision
wins over replacement in 364/384 one-edit changes (mean saving 0.802), versus
91/1056 farther changes (mean saving -1.902). No unchanged task wins. The
single-transition saving is bounded by 5 minus trace price, so at most one
unit here: a property of the cost schedule, not a new CA law. Macro expansion
preserves physical-budget reachability; savings require priced dispatch.
The first six-cell shortcut ABBBA = ABBAABBA for rules 4/30 fails on 11,264
of 131,072 unrestricted windows; preserve its bounded scope and counterexample.

The original revisable-primitives proposal is partly implemented. Given
macros, free oracle planning, and one task transition are explicit limits.
The returning-task extension is now complete in
`docs/research/2026-09-07-returning-tasks.md`: 294,912 configurations using
only all-width kernels; direct enumeration of 4,194,304 two-block macro paths
agrees with dynamic programming. A free-trace Rule 4/30 witness saves one
unit on the changed job but adds two on the returning job. A separate
present-cost tie leaves returning costs of 13 versus 10. At primary prices,
farther-change hindsight revision wins rise from 430/1056 for one return
cycle (mean -0.691 units) to 893/1056 for four (mean +8.599). These are shared
configurations, not independent replicates. Reactive policies deliberately
do not learn the recurring schedule; oracle gains include future information.
The original future-repertoire insight is promoted into Concepts #possibility.
Separately address learning/discovery and search costs before claiming
adaptation. The user subsequently confirmed the recovered Narrative Calculus
gist and explicitly selected shared state/rule spaces and the eight-neighbor
2D connection as the next experiment; the full parallel-chat tail remains
unavailable and is not treated as evidence.

## Research continuation: shared state and rule space (2026-09-08)

Completed `docs/research/2026-09-08-shared-state-rule.md`, with protocol and
implementation committed before evaluation. `experiment_shared_state_rule.py`
enumerates 168 complete graphs: 24 encodings × three eight-cell ring modes,
plus 24 encodings × two address axes × two square sizes (3/4). Every pair
(r,s) is included in ring graphs; all states are included in square graphs.
All 80,640 local permutation/axis cases are evaluated on all 512 inputs.

The eight-neighbor selector has r_k = neighbor[p[k]], q = 4W+2C+E (or 4N+2C+S),
and next center = neighbor[p[q]]. Every permutation has nine essential inputs,
exactly six quartic terms and degree four. There are 36,000 distinct functions
per axis. The proof and independent polynomial audit were post-enumeration.
These local results hold independently of grid size; global cycle results do not.

The default 4x4 horizontal/vertical selectors have longest cycles 12/4 and
fixed points 2/66. Rotate both axis and decoder to obtain conjugate dynamics;
changing only the axis is a different intervention. Frozen ring longest cycle
40 is encoding-invariant. Mutual ring longest cycles range 2–8, derivative
replacement 3–6 across the declared encodings: feedback alone does not sustain
novelty. Full states still have one successor under a fixed meta-law.

65,536 engine checks, 5,376 independent orbits, all graph accounting,
24 frozen conjugacies and mutual symmetries, 24,576 scalar local checks,
1,585,152 rotated-state comparisons and 24,576 independent polynomial outputs
pass. Source/result hashes and all selected encodings are recorded.

Next: compare a principled Gray-code assignment and geometric controls on
larger grids; separately specify a locally represented changeable decoder.
Do not infer that expanding same-time instructions to a fixed local rule
makes them meaningless, or that memory is the only interesting mechanism.

## Dimensional research direction and interpretation contract (2026-09-10)

Read docs/research/2026-09-10-dimensional-vision-and-interpretation.md for the
durable user-requested account of the vision. Keep it visible in the Program.

- Seek recurring spatial dimensions, coherent trajectories, new native states,
  and organization increasingly sustained by the unfolding. "Turtle beam" is
  the objective; metaphysical and prime analogies are not established results.
- Truth-table bits have configuration addresses; state bits have spatial
  addresses. Eight bits supplies no unique physical arrangement. State-as-rule
  claims must state the law, state family, and encoding/interpreter together.
- Separate family preservation, exact representation, restoration, and
  endogenous organization. ALL256 axial rules preserve copied-field symmetry;
  the special66 additionally reproduce the old law at the same macro cadence.
- Compensated re-encodings may change locality and edit costs. Invertible
  observation relabelings preserve closure automatically; substantive tests
  compare different retained information or explicit physical constraints.
- Radius, alphabet, correction depth, spatial dimension, time, and program
  edit support are separate resources. Guarded controls remain useful. No C4
  scoring or naturalness claim; retain failed attempts and freeze rescues.
- The completed transverse-difference test below resolves whether erased
  per-column baselines affect future differences, relative to that observation.

## Research continuation: agreed issue burndown underway (2026-09-10)

The user authorized executing the ordered burndown. The gradient experiment
remains complete. This primary session owns #61,#62,#65,#66,#68,#67. At the
user's request, #63/#64 are reserved for a parallel agent using their signed
scopes. The primary session integrates shared catalogs, Program pages, this
continuation and the burndown, then reviews and merges the parallel PRs. Protocol-writing issues do not authorize claiming unrun results.
Use one substantive PR per issue and `Closes #N` on its completing PR. Keep the
checkpoint's burndown status, PR link and date current in that same PR.

- #61 shared synthesis: completed in PR71 (2026-09-10). Read
  docs/research/2026-09-10-shared-closure-account.md. Both Programs now state the
  same invariant-family/cadence contract and distinguish a candidate-law error
  from failure of every factor. Rule255 supplies the unchanged exact control.
- Eight knowledge entries restore Research022–028/035 provenance, with explicit
  prerequisite edges and unchanged prior nodes/edges. No experiment was rerun
  and no earlier evidence label changed. Preserve the parallel source-recoder
  work; its current PR55 does not edit these Program sources or knowledge files.
- #62 successor-set archive: completed in PR73 (2026-09-10). The original
  script/stdout, reproducible replay and research/knowledge account retain
  exploratory provenance, finite-ring scope and exact weighting conventions.
  Both Programs leave the broader sound-approximation question open.
- #65 relabeling archive: completed in PR74 (2026-09-10). The exact local
  identity and transformed transport use a decoded old-state gate and old
  arrays. The original script/stdout retain exploratory provenance; the
  unspecified rule-field lift remains open. No geometric or selection claim.
- #66 inventory: completed in PR75 (2026-09-10). Four source-hashed sets and
  all six pairwise intersections preserve finite/intrinsic role budgets and
  distinct constructors. The four nonlinear gradient sources remain visible.
  No new CA census or conserved-density search was run.
- #68 Concepts: completed in PR76 (2026-09-10), at concepts.html#resonance.
  Four sourced relationships remain distinct; the vision note is promoted
  editorially while its evidence stays open. The knowledge contract links back.
- Next in order: freeze issue67's bounded second-lift comparison. No new census
  is authorized by this protocol-writing deliverable; register execution as planned.

## Research continuation: gradient interventions completed; pause for issues (2026-09-10)

Read docs/research/2026-09-10-gradient-intervention-costs.md. This is the current
dimensional checkpoint. Preserve parallel Erased Distinctions work and unrelated
metadata. The user requested completion of this unit, then a pause to address
the agreed issues. Do not automatically start another experiment.

- Protocol frozen at f69b156c; implementation 8fe10964 precedes execution.
  First execution passed without corrections or protocol deviations.
- All flat fields and simultaneous flat XOR actions on (4),(2,2),(2,2,2),
  ten sources, horizons 0/1/4, every changed-edge budget. Mask enumeration
  matches an independent plaquette-nullspace enumeration word for word.
- 31,495,680 endpoint queries; 1,558,080 state/budget/observation comparisons;
  38,400 interface endpoint checks. Native/reference evolution and minimum-cost
  versus direct reachable-set counts agree; zero discrepancies.
- General edge-support theorem: minimum cost to change loop vector h is
  sum N/n_i over changed directions. Disjoint parallel loops give the lower
  bound; seam masks attain it. Zero-loop masks are periodic-potential gradients.
  Edge and owning-site minima are separate; first witnesses need not coincide.
- Eight nonconstant self-dual sources preserve the chosen loop sector.
  Constants erase every edited gradient after one step. Under the known-state,
  deterministic, one-shot hard-budget contract, capacity is log2 of the integer
  reachable-outcome count. No uncertain-state prior or endogenous controller.
- Period-two geometry makes all eight nonconstants bijective on flat fields:
  twisted l=r XOR h reduces each axial pass to a shift/identity and possibly
  complement. Their 2D/3D full-field counts describe action geometry, not
  general nonlinear reversibility. The four-site ring loses within-sector
  distinctions for 142/212 (12 outputs) and 178/232 (8), despite conserved loops.
- P multiplies edge and site costs by the added period m while preserving
  edited trajectories. Both tested interfaces have m=2. Of 1,024 native (2,2,2)
  masks,32 are inherited,512 outside-image masks change the new loop bit, and
  480 outside-image masks leave it zero. At target budget8, inherited actions
  give27 full-field outcomes versus126 native for nonconstants at t=0/1/4.
  Native (4,2) frontiers were not enumerated. Minimum old-loop revision costs
  are not improved by native (2,2,2) masks, though available outcomes increase.
- Canonical JSON results/gradient_interventions_20260910.json SHA256:
  89093341369ef505d6bb2d2a53cd7be00864bbb035adcd4072360c006c3d3630.
  Dedicated CI replays the exact output using the unchanged loop evaluators.
- The ordered issue burndown and completion criteria are now in the intervention
  checkpoint's `Issue burndown` section: #61, #62, #65, #66, #68, #67, #63, #64.
  The first five consolidate/publish existing work. #67/#63 are agreed protocol
  deliverables: register later implementation/evaluation explicitly as planned
  work before closing the proposals. #64 requires the working online arm.
  This checklist update does not resume experiments or close any issue.
- PAUSE / agreed issue queue: #61 synthesis and missing provenance; #62 archive
  finite successor sets; #63 freeze hidden-state static intervention channels;
  #64 conservative online suffix learner; #65 archive relabeling/transport;
  #66 cross-constructor inventory; #67 bounded two-completion second lift;
  #68 Concepts promotion. Signed final agreement links are in the checkpoint.
  Original issue bodies include withdrawn claims: use the signed scope, not
  those claims. The current gradient audit does not complete #63 or #67.
- User workflow preference: each PR that fully implements an issue's agreed
  scope should say `Closes #N`. Related or prerequisite work should only link
  the issue. Truly redundant/no-op issues may be closed with a signed reason.
  None of #61–68 is a no-op: each retains concrete work. Agreement on scope
  is not completion. No issues are closed by this checkpoint.

## Research continuation: gradient loops completed (2026-09-10)

Read docs/research/2026-09-10-gradient-loop-invariants.md. Preserve the parallel
Erased Distinctions work and unrelated metadata.

- Frozen protocol at 9e5de20f; implementation bf62df70 precedes evaluation.
  First execution passed; no corrections or protocol deviations.
- Native Q_d integrates local edge neighborhoods under both temporary anchors.
  Independent Boolean halo contraction evolves twisted binary potentials and
  infers output twists from endpoint differences, not the predicted invariant.
- All flat fields on (4), (2,2), (2,2,2): 16, 32, 1,024. Plaquette ranks
  0, 3, 14 certify completeness alongside unique anchored-potential encoding.
- Eight nonconstant sources preserve all loop bits; constants 0/255 erase them.
  General proof: translation covariance plus complement response kappa gives
  h'=kappa*h. This is all-dimensional; finite tests validate implementations.
- Replication copies edge components and appends zero; inherited loop bits
  persist. Nonzero loop sectors are gradients of twisted infinite potentials,
  not periodic tile potentials. No curl-violating ambient updates are chosen.
- 10,720 base rule/field cases, 42,880 macro updates, 995,840 component checks.
  480 interface cases, 1,920 interface ticks, 40,960 target component checks.
  Both native/reference streams agree. Canonical JSON has all sector transitions.
- Local edge reads 3/18/81 and reconstructed vertices 4/15/54 in 1D/2D/3D.
  Storage d bits/site; periodic topology and supplied replication remain costs.
- User's control refinement is recorded visibly in the vision note: persistence,
  possible futures, and usable intervention power differ. A measurement of
  control is not an implemented endogenous mechanism. Do not claim empowerment
  from arbitrary observed action correlation or entropy without a probability law.
- The separately frozen intervention protocol is now completed in the
  continuation above. The original protocol remains unchanged as its freeze.

## Research continuation: full-gradient closure completed (2026-09-10)

Read docs/research/2026-09-10-full-gradient-closure.md. Preserve the parallel
Erased Distinctions work and all unrelated metadata.

- Protocol at e1a1ef70; verifier 33d19a2e precedes evaluation. No corrections
  or deviations. Same 66 ordered axial laws, observation J=(T_x,T_y).
- R0 passes 0,204,255. R1 passes 0,142,150,170,178,204,212,232,240,255.
  The four new nonlinear sources are majority with zero or one input negated.
  Their joint gradient caps are not componentwise copies of the source rule;
  the source axial order remains significant for these four.
- General binary local criterion: g(p) XOR g(complement p) must be constant.
  If it varies, two disjoint windows force different next gradients for a
  source and its complement. In this 66-rule domain, nonconstant passing
  sources are exactly the eight self-dual ECA; constants have response 0.
- All 56 R1 failures give complementary 15-site patches. Fill the omitted
  corner 0/1 and repeat 4x4: complete identical J fields, different next J.
  All witnesses independently replayed. The 3x3 torus hides 128/254 by uniform
  outputs; preserve its 12 finite-functional sources rather than claiming 10.
- Audit:2,162,688 local windows,4,325,376 window/budget checks;33,792 Boolean
  G windows and complement pairs;33,792 periodic updates,304,128 output cells;
  59,904 cap-site checks;112 extension updates,1,792 output cells. Canonical CI.
- Of 262,144 local 18-bit gradient neighborhoods,16,384 are reachable, with
  two source preimages and four independent plaquette constraints. Packed
  R1 cap 4,096 bytes; d edge bits/site. Broad ambient 4-symbol grammar permits
  2^491520 off-image completions; none is selected as physically preferred.
- Analytic all-dimension consequence: self-dual axial composites factor
  through all d gradients; replication copies components and appends zero.
  Q_(d+1)P=P Q_d on valid gradients. This is a proof, not a higher-d census,
  and retains source dynamics only modulo global complement.
- The separately frozen native-gradient and loop experiment is completed above.
  Its invariant depends on declared topology; it does not establish intrinsic
  dimension, prime factors, self-assembly, or affordable intervention.

## Research continuation: transverse-difference closure completed (2026-09-10)

Read docs/research/2026-09-10-transverse-difference-closure.md. Preserve the
parallel Erased Distinctions work and all unrelated metadata.

- Original protocol at869bc08f; implementation0b0475a9 precedes evaluation.
  No implementation corrections or original-protocol deviations. All66 axial
  compatible sources, observation T_y(X)=X XOR its next-y translate.
- Radius0 closes exactly0,204,255; radius1 exactly0,150,170,204,240,255.
  These six are the selected affine controls: zero, identity, diagonal shifts,
  and3x3 parity on differences. All512 local T neighborhoods are reachable.
- All60 other sources fail R1. Identical nine vertical edges on a3x4 source
  patch imply column-constant source XOR. Periods3/4 extend every local pair
  to identical complete T fields with different next T. No deterministic
  update on T alone, even nonlocal, exists for any of these60 sources.
- Original3x3 periodic census finds57 full-field obstructions;128,232,254
  appear closed because AND/majority/OR produce uniform outputs on that torus.
  Preserve this finite aliasing. Supplement protocol+verifier2bfd6fb8 precede
  replay of ALL60 local witnesses; no selection, altered law, or repair.
- Original audit:270,336 local windows,540,672 rule/budget windows;33,792
  periodic updates,304,128 output cells,41,472 cap-cell predictions. Supplement:
  120 periodic updates,1,440 output cells. Independent Boolean/local evaluators,
  exact canonical artifacts, source digest, and dedicated CI reproduction.
- Full-field counterexamples remain counterexamples when copied into higher
  axes, retaining the observed second-axis direction, by exact intertwining.
  This does not classify all possible observations or orientations.
- The separately frozen full-gradient comparison is now completed above.
  Its added information and storage cost remain explicit, and the original
  transverse-only failures and certificates remain unchanged.

## Research continuation: guard-free axial family completed (2026-09-10)

Read docs/research/2026-09-10-guard-free-axial-lift.md. Continue only the
dimensional workstream; preserve parallel Erased Distinctions sources and metadata.

- Protocol c5c380ec and implementation3e694a1f precede evaluation. No corrections
  or deviations. G_(r,d) applies the same ECA along each axis, in fixed order.
  Full binary ambient lattice, no guards or role species, Moore radius<=1.
- Exactly66 sources preserve literal replication at EVERY interface:0,255,
  and all even words128..254. First and second exact censuses agree. For any
  nonconstant source the local composite has both bits in its one-site range,
  by independent child slabs. Hence f000=0,f111=1 is necessary and sufficient
  at every dimension; constants also pass. This is not global surjectivity.
- Exactly24 sources commute across axes: all16 affine plus eight AND/OR
  functions. Pairwise commutation on slices implies all-dimensional axis
  permutation equivariance. This does not mean reflection invariance.
- Exactly14 satisfy both:0,128,136,150,160,170,192,204,238,240,250,252,254,255.
  They are constants, copies, parity, AND/OR. Another52 are compatible with
  ordered axes. Rule32 fails this recipe; its correction-cap result stands.
- Complete audits:2,048 first-interface cases,131,072 second-interface cases,
  131,072 axis-order cases; independent Boolean array evaluator. Every width4,
  2x2,2x2x2 state for all256 rules:73,728 macro updates,557,056 output cells,
  independently checked by a local recursive tree. Canonical JSON and CI.
- Replication is still prepared and gives zero added-axis information density;
  a source edit changes an infinite line. Original r remains in the law.
  Costs:d sequential lattice passes or(3^d-1)/2 naive lookups per output.
  No endogenous program, self-assembly, novelty, or intrinsic-dimension claim.
- The transverse-difference experiment is completed in the continuation above.
  Preserve its original protocol, the finite aliasing, and the separately
  frozen witness-extension supplement. Guarded controls remain useful.

## Research continuation: extension freedom and dimensional-beam objective (2026-09-10)

Read docs/research/2026-09-10-extension-freedom.md. This is the dimensional
workstream; preserve the parallel Erased Distinctions sources and metadata.

- User clarified the destination: recurring dimensional construction, coherent
  lower-dimensional trajectories, additional higher-level possibilities, and
  endogenous organization. "Turtle beam"/"unus mundus" are motivation, not
  established claims. Guarded constructions remain useful controls; do not
  substitute their supplied compatibility for naturally selected organization.
- Spatial dimension, correction depth and time differ. Minimum ancestry needs
  an encoding/causal/resource contract; no skipped levels along composed total
  adjacent lifts. Injective lifts preserve ancestral rank; compatible dynamics
  cannot increase it. No intrinsic dimension or prime-factor result follows.
- Extension-freedom protocol f4caa22f, implementation1ecaba36 precede evaluation;
  no corrections/deviations. Source Rule32, all128 seven-bit causal windows.
  Of64 pair neighborhoods15 are realized;2^98 radius-one pair updates agree.
  This broad logical grammar is not wholly executable by the physical one.
- All65,536 native top tuples were independently audited on16 contexts.
  128 pass, giving four effective functions with32 aliases each. Top ECA-only
  choices are exactly128/160. Their difference detects top101, absent on-image.
  Physical encodings differ in stored programs, even when data images agree.
- Complete physical controls: all source words at widths4/6, both caps,8ticks;
  off-image top zero at width21,8ticks; all256 source/lambda fields at width4,
  copying mode,4ticks. 2,738 timepoints,922,216 stored-symbol comparisons.
- With top words128+32*lambda, old V gates lambda copying from the left.
  288 actual instruction-bit changes; encoded data remain exact. This neutral
  freedom is dormant on the image, not autonomous revision of source dynamics.
- Off-image top zero grows as[-t,t] under128 and{-t,-t+2,...,t} under160.
  Neither heals generally. Same encoded dynamics does not fix ambient dynamics.
- The planned guard-free axial experiment is now completed in the continuation
  above. Its frozen protocol remains unchanged; preserve all failures and
  distinguish its prepared replication from naturally selected organization.

## Research continuation: finite physical correction cap completed (2026-09-10)

Read docs/research/2026-09-10-rule32-physical-cap.md. Preserve the parallel
Erased Distinctions workstream and its shared metadata entries.

- The frozen Rule32 physical/edit protocol is complete. Existing H2, hold
  mode, scale9, rows-1..2; bottom(32,60), top(128,240), guards(204,240)/0.
  H2 J E(S)=J E(F32(S)) for every source and time by local proof/induction.
  No extra future rows. Prepared roles/occupancy remain architectural resources.
- 68 occupied symbols/source site (64 program+4 data), span36, radius9,
  source preparation radius<=2, one tick. No source reconstruction/compression.
- verify_rule32_physical_cap.py and matching dated JSON reproduce384 local
  semantic assertions,64 physical neighborhoods,64 guard cases, and15,520
  field timepoints (4,854,656 occupied/29,857,376 explicit blank comparisons).
- Protocol f65a63ea; implementation1edb7f77 corrected before first execution
  at4d71ba01: derivative test window centering off by one. Recorded correction,
  no protocol deviations, ambient interpreter unchanged.
- All40 width3/5 source words pass40ticks. Zero-cap control fails first at
  width5/source11/tick1: actual(28,0), expected(28,8). Ten mismatched timepoints.
- All1,360 single native instruction/data edits match complete physical fields
  through8ticks. Of1,280 program edits,260 ever change undamaged data and145
  leave the same-ring K1 image. No edited instruction reverts in hold mode.
- All80 data edits recover bytick5, but ALL baseline pairs extinguish bytick3.
  Do not infer general maintenance, durable recovery from tick8 agreement,
  or full-shift image membership from finite-ring membership.
- Post-audit DEDUCTION: alternating infinite S has K1=(1,1), a persistent
  encoded fixed point. One top data zero expands exactly to|x|<=t under128.
  Top leaf bit7 edit128->0 atx0 creates zeros|x|<=t-1 for t>=1. Thus even
  data-trajectory recovery is not general; these are not just unrepaired bits.
- Follow-up and user clarification are recorded in the extension-freedom continuation above.
  The earlier next question was intentional semantic program revision. Decide the
  old/new interpretation, allowed edit and re-preparation/maintenance resources
  before freezing a concrete next experiment. Do not automatically treat an
  intended new native dynamics as an error, or add repair machinery without
  a specified semantic target. No further routing polishing as a substitute.
- Scope failures to this law. No C4, novelty or universal-program claims.

## Research continuation: exact local caps and the Rule32 candidate (2026-09-10)

The local-cap census is complete. Read docs/research/2026-09-10-local-correction-caps.md.
Preserve the parallel Erased Distinctions files and shared metadata entries.

- Frozen protocol1a012ae and implementation1fa5353b precede evaluation.
  All256 homogeneous ECA, K/O, h0..2,R0..2, full causal windows<=11bits.
  4,608 budgets:1,094 pass and3,514 explicit conflicts. No fixes/deviations.
- Independent tuple recursion checks348,160 truth entries and reconstructs
  all2,064,384 source-window fibers, matching the integer-table evaluator.
  CI reproduces results/local_correction_caps_20260910.json.
- Union of passing depths/radii:135 rules in K,150 in O. At h1/R2 counts
  are123/120; at h2/R2 they are94/150. Depth can increase the required cap
  radius (Rule11 h1/R2 passes, h2/R2 fails). Whole-field fibers still agree.
- Post-census exact Rule32 identity: A2[x]=A1[x-1] AND A1[x+1]. Thus
  U'=F32(U) XOR V, V'=F128(V) closes (A0,A1) for all source states/times.
  Standalone verify_rule32_cap_identity.py checks128 seven-bit windows.
  Nonconstant cap160; top update128. No derivative-only cap at testedR<=2,
  but no arbitrary-radius exclusion. Two represented bits/site vs one for S.
- Follow-up complete above: docs/research/protocols/rule32-physical-cap-20260910.md.
  Historical frozen setup: Commit implementation before evaluation. ExistingH2,
  hold mode, rows-1..2, bottom(32,60), top(128,240), guards(204,240)/data0.
  Audit complete symbols, local proof, widths3/5 all source words40ticks,
  failed zero-cap control, and34 one-cell edits through8ticks.
- Edited-native execution, undamaged data recovery, ring-image membership,
  and program recovery are different contracts. No automatic semantic repair.
  Do not claim generic source-law editing or full-shift image membership
  from finite-ring tests. Freeze any rescue separately.
- No C4 selection, novelty, compression, or universal-program claim.

## Research continuation: finite boundaries and stored correction transport (2026-09-10)

The dimensional control now has finite transverse preparation; the workstream
has returned to commutator correction closure. Read both new notes before
continuing. Preserve the parallel Erased Distinctions work and metadata.

- docs/research/2026-09-10-finite-routing-boundaries.md: unchanged five-symbol
  radius-nine H_d realizes masked sources (Omega,P,S). Missing neighbors
  freeze data; absent left programs cannot be copied. B is not occupied zero.
- The lift has mask Omega times {-1,0,1}, inherited P appended with172
  centrally, and constant guard tuples/data1,0. Guards freeze because their
  outward neighbor is absent. Execution, gated whole-program copying and
  inherited one-cell edits commute recursively for every finite dimension.
- Complete-macrocell thickness is27 physical coordinates per new axis;
  occupied sites per initial logical site after k lifts are3^k[8(d+k)+1].
  This is finite transverse thickness, not finite total support for an
  infinite source. Occupancy edits and role self-assembly are not established.
- The finite-boundary frozen audit passes26,619 assertions, with both
  missing-as-zero and insufficient-thickness failures retained. No protocol
  changes or implementation corrections were needed.
- docs/research/2026-09-10-stored-correction-transport.md: tuple(r,60)
  physically executes F(row) XOR next row. All source and transport bits
  occupy cells. Source r is homogeneous and held in this extension.
- Preparing A_0..A_H gives exact U_k(t)=A_k(F^t(S)) for k+t<=H.
  The zero cap is NOT indefinite closure: Rule255/all-zero source/H=2 has
  first wrong rows2,1,0 at ticks1,2,3. Layout stays valid. The separate
  frozen audit passes51,202 assertions and retains this scoped cap failure.
- Both results are reproduced by verify_finite_routing_boundaries.py and
  verify_stored_correction_transport.py, with matching dated JSON files.
- Follow-up completed in the local-cap continuation above; historical next protocol:
  docs/research/protocols/local-correction-caps-20260910.md.
  All256 fixed ECA, h=0..2, capR=0..2, full causal windows (max11 bits).
  Compare K_h and O_h local caps with the complete-source baseline; retain
  failure pairs and certificate hashes. Recover known affine/Rule232 controls.
- A local cap certificate is not yet a physically encoded cap. After the
  census select a representable nontrivial candidate and freeze its physical
  program and instruction-edit repair contract separately. No further
  control-family polishing unless it serves this correction question.
- C4 remains background only. Scope failures to budget/architecture, retain
  them, and freeze rescues. No novelty or intrinsic-universality claim.

## Research continuation: added routing tables are editable (2026-09-09)

The next dimensional unit is complete; see
docs/research/2026-09-09-editable-routing-tables.md and its frozen protocol.
Preserve the parallel Erased Distinctions thread and its publication metadata.

- Native P=(r,h2,...,hd) has d editable eight-bit tables. Each added table
  reads the preceding result and the two data neighbors on its axis.
  The ordered chain, axis assignments and hold/copy policy remain fixed.
- Place byte j along axis j in a scale-nine macrocell: 8d+1 occupied sites
  out of 9^d, five symbols, radius nine, one tick. Local evaluation reads
  8d program bits and 2d+1 data bits and evaluates d tables; constant tick
  count does not mean constant circuit complexity as dimension grows.
- Appending selector word 172 with separate guard Qd=(204,172,...) lifts
  every native source program/data field. Both retention and state-gated
  copying of the entire tuple commute, including inherited one-cell edits.
  The proof repeats for every finite d; whole-field audits reach 4D.
- Newly introduced table edits may alter the relation to the previous source.
  Exactly 64 appended words preserve old dynamics on the (0,1) rails
  (bits 1=0, 5=1); 192 counterexamples are retained. This does not restrict
  the routing words allowed in a source being lifted next.
- There are 30,496 local data functions among 65,536 two-word programs.
  Syntax aliases and dormant instructions are explicit; every program slot
  has a causal context, not guaranteed activity in every enclosing program.
- verify_editable_routing_tables.py passes 2,236,434 assertions; canonical
  JSON is results/editable_routing_tables_20260909.json. Protocol and code
  were committed before execution, with no corrections/deviations. CI
  reproduces the exact result. Counts are not independent scientific samples.
- Follow-up complete: the finite-boundary checkpoint above retains occupancy
  explicitly and uses missing-input retention. The current target is a local
  correction cap, not further boundary optimization.
- Existing exact CA simulation theory is the comparison baseline. No
  novelty, intrinsic-universality, arbitrary editable syntax, or self-assembly
  claim is established. C4 remains background only. Scope failures to the
  attempted architecture and freeze rescues before evaluation.

## Research continuation: editable spatial Rail programs (2026-09-09)

The dimensional workstream now has an exact stored-program witness; see
docs/research/2026-09-09-spatial-rail-programs.md and its two frozen protocols.
It is separate from the Erased Distinctions workstream and does not unpark a
special-dimension hypothesis.

- Native programs are ECA leaf words with one Rail wrapper per added dimension.
  Eight program bits occupy actual P cells, with one D cell and B padding in
  each 9^d-site macrocell. A uniform five-symbol CA of radius nine executes the
  grammar in one tick. Tags/layout and wrapper structure are fixed resources.
- Place the source program/data at the new central interface; use a fixed
  identity guard program (204) with zero/one data off the interface. The guard
  repairs the earlier repeated-program 64-source limitation: all 256 starting
  ECA programs and arbitrary heterogeneous native fields lift exactly.
- One local data or program-bit edit is one physical symbol edit through both
  lifts. The second interface applies to arbitrary valid 2D program/data fields,
  not just first-lift images. Local proofs give all finite higher dimensions.
- A separately frozen extension preserves state-gated left-neighbor copying of
  entire program words. Programs change autonomously while the same complete
  commuting identities hold. This is transport, not arbitrary program synthesis.
- Audit scripts verify_spatial_rail_programs.py and verify_spatial_rail_transport.py
  reproduce the paired results/spatial_rail_*_20260909.json files. The main audit
  passes 109,876 assertions and the transport extension 974, including actual
  program changes. Do not conflate aggregate field equality with independent
  samples or claim an optimized binary radius-one realization.
- User clarification: Class IV is background intuition only; do not use it to
  motivate reasoning, architecture selection, or a selectivity requirement.
  Negative findings are scoped to an attempt and can be revisited by an explicit
  revision. Preserve the failed candidate and freeze a rescue before evaluation.
- Follow-up completed: the editable-routing checkpoint above stores each added
  table explicitly. Its ordered topology remains fixed. Smaller role alphabets
  and marker self-organization are still separate experiments.

## Research continuation: dimensional compatibility (2026-09-08)

`docs/research/2026-09-08-dimensional-lift.md` defines the outer-totalistic
2*3^d-bit table encoding in two adjacent layers and the ternary interpreter.
For H = complement plus full spatial reflection J, F H = H F in every positive
dimension. This is an interpreter symmetry on all configurations, not a
cross-dimensional projection or Class-IV selector. D(HX)=J D(X), while the
Groovy covariance defect is F(JD(X)) XOR JF(D(X)). On the d=1 interpreter's
3x3 periodic grid it is nonzero on 504/512 states (saved witness starts at 1).

`verify_dimensional_lift.py` verifies the proof on all 512 d=1 local patches,
9,728 affine-basis cases covering all d=2 local patches, sampled d=3/4 cases,
and all 512 finite global states. Initial code was committed before execution. A deductive follow-up defines
T_X(delta)=F(X) XOR F(X XOR delta); all 262,144 base/change pairs satisfy its
symmetry, and T_X(D(X))=D(F(X)) holds for every binary map by definition.
The latter is not a selective invariant. Context can be the present base
state, without a stored history.
The higher-dimensional interpreter is not outer-totalistic (same-center,
same-population counterexample); identical overlapping table windows force a
constant layer in the direct unblocked representation. These are scoped
obstructions, not a general impossibility of spatially represented programs.

The user explicitly proposed dimensional persistence as a possible Class-IV
characterization. Record as proposed only: no score or enrichment exists.
The current 64-rule outer-totalistic ECA domain admits 54/90 but excludes
30/106/110. Out-of-domain is not failure. Decode-only round trips can be
true by construction; known history repair also occurs for Rule 30 and does
not independently identify Class IV.

Next priority supersedes the Gray-code comparison: specify spatially compatible
encodings and nontrivial invariant families, with a fixed evolution-sensitive
decoding criterion and declared representation budget. Broaden the lift before
attempting the full ECA comparison. Keep symmetry equivalence and disputed
class labels explicit. Recovered parallel-session material is now supplied by
the user in this thread; its conjectures are not experimental results.

## Research continuation: provenance and action responses (2026-09-08)

`docs/research/2026-09-08-spacetime-provenance.md` answers the user's provenance
question for 1D rows stacked into a 2D panel. Protocol and implementation were
committed before evaluation. All 256 rules and every initial ring at n=6/8/10,
observed transitions 0..6, future horizons 1..4, autonomous and fixed cell-0 flip:
168 aggregate rows. Candidate rules are exactly r & M = V for visited-input
mask M, hence 2^(8-popcount(M)) candidates. The rule remains fixed for every
entire future; no re-selection at each step.

Primary t=2,h=4: autonomous/flipped ambiguous panels are 1384/2260 of 6696 at
n6, 5444/8998 of 36154 at n8, and 17604/29548 of 173148 at n10. At n8,t6,h4,
96/42718 panels have natural future ambiguity versus 4134 after the flip;
10430 still have rule ambiguity. Report distinct-panel denominators; CSV also
retains generating-pair weighting. No class labels or independent replicates.

The zero n6 panel has 128 possible rules, identical natural futures forever,
and 38 four-step futures after a flip. Panel [3,25,8] under rules9/137 agrees
at next row35 then diverges to40/41. Seed23 at n8 exposes all eight rule-table
inputs in one transition; [23,0] uniquely identifies rule0. Purpose-specific
future codes can need fewer bits than identifying the rule; codebook/decoder
cost is not modeled and side information is not inferred from absent data.

32,768 package-engine comparisons, 1,300,744 candidate multiplicities,
189 direct row-partition checks, 10,405,952 future bounds, 2,064,384 nested-mask
cases and 135 witness replays pass. The content-addressed witness provenance
JSON has eight nodes and 135 derivation edges; it is not the full enumeration
and is separate from the semantic knowledge graph.

Next compatibility work must distinguish preserving a rule, preserving natural
continuation, and preserving responses to a declared action set. Choose target,
representation budget and decoder before scoring. This full-ECA observational
map does not yet implement a higher-dimensional evolutionary law or remove the
outer-totalistic domain restriction from the separate dimensional interpreter.

## Research continuation: invariant column encodings (2026-09-08)

`docs/research/2026-09-08-column-compatibility.md` completes the next fixed-
interpreter compatibility unit. Protocol and instrument were committed before
evaluation. All ordered distinct vertical codewords a,b at heights 1..6 and
cadences k=1..3 give 16,002 conditions. A row-type constraint graph decides
existence at EVERY finite vertical height for each of 256 ECA targets and
each cadence. Only 23/232 occur at k1; none at k2/3. This is not an exclusion
of larger horizontal blocks, drift, higher cadences, or other upper laws.

Crucial distinction: 18/50/54 finite codes remain valid under F^k at k1/2/3;
only 18/0/0 give radius-one lower rules. The others carry wider-neighborhood
dynamics. Thus absence of an ECA target is not failure of all dimensional
compatibility. The 18 successful records reduce to two canonical families:
vertically repeated data (232, majority) and alternating data/complement
(23, complement-majority). No Class-IV labels or enrichment were evaluated.

The independent audit rebuilds all 17,472 vertical truth constraints with
Boolean truth sets and checks 796 variable-edge return paths; all 768 graph
decisions agree. Primary checks include 2,130,432 local window pairs, 40,960
package-engine comparisons, 16,002 finite/graph agreements, 150 symmetries,
5,120 matched trajectory and 3,072 action-word state comparisons.

Deductive follow-up: in every positive lower dimension d, repeat arbitrary
data planes with m-1 zero planes between them, m>=2. Each interpreter tick
moves the data one transverse step and one step in every spatial coordinate.
After m ticks, F_(d+1)^m E_(d,m) = E_(d,m) diagonal_shift_d^m. This is proved
locally; checks include 14,080 1D state/tick cases and 288 full-field ticks in
lower dimensions 2/3. It is a simple transport family, not a proof that one
interpreter simulates the preceding dimensional interpreter.

Matched logical flips toggle a XOR b per column/vertical period; arbitrary
finite matched action words are preserved by the intertwining identity.
One physical cell flip is different: on the 2x7 Rule-23 code, 28/128 states
return to valid code by tick4, but only 18 match undamaged evolution. Damage
tests are tiny periodic tori, not isolated defects in an infinite plane.

Next: explicitly allow a bounded amount of horizontal packing or fixed drift,
while holding the upper law, action dictionary, and evaluation budget fixed.
Seek interactions beyond transport. Do not extend the failed radius-one
criterion into an unrestricted impossibility claim. Remainder feedback still
needs its own law and controls; the boundary question remains parked.

## Research continuation: blocks and moving frames (2026-09-08)

`docs/research/2026-09-08-block-compatibility.md` completes the previous next
step. Protocol a968c9d and both instruments 6d246c4 were committed before
evaluation. All rectangles m*w<=6, every ordered distinct binary code pair,
k=1/2/3, |u|/|v|<=k with vertical equivalence mod m. Fixed upper law; no class
labels. Criterion F^k E = T_(v,u) E phi_r. Frame motion is observation, never
a physical repair between updates.

781,050 candidates, 9,022 successes, 1,218 canonical records, 22 literal
targets in 11 reflection/state-complement rule orbits. Columns stationary
admit 2 targets, columns with frames 8, all rectangles stationary 14, all with
frames 22. Targets: 0/15/23/51/60/85/90/102/128/136/153/165/170/192/195/204/232/
238/240/252/254/255. No 54/110 within this budget; no unbounded exclusion.

Main exact witness: E(s_i) has rows (s_i,1),(0,1),(0,1 XOR s_i), periodically
repeated vertically. A42/B11, bitindex2*y+j. F E = T_(0,-1) E phi60 =
T_(0,1) E phi102; F^2 E = E phi90. Six cells per logical bit per period,
two physical flips per matched logical flip. Area6 is minimal for multi-input
affine targets only within the frozen search. Writing logical right shift tau,
phi102=I XOR tau^-1 gives tau*phi102^2=tau XOR tau^-1=phi90. The duplicated
middle terms cancel. This is exact mixing beyond the conveyor, not a defined
remainder-feedback operation or evidence of universal computation.

All outcomes independently audited using Boolean truth sets and shrinking
windows; no primary update/decoder import. Primary: 47,211,984 causal assignment
checks, 16,002 prior column checks, 60,778 symmetries. For 26 selected witnesses,
16,640 laboratory trajectory and 19,968 action-word state comparisons. Report
replays the same physical trajectory under all three readouts and verifies
every plotted block. Source hashes, rejection witnesses and full outcome
matrices are in results/block_compatibility_20260908*.

Next mathematical target: determine whether the block mechanism supports a
genuine 2D input field in the 3D interpreter with a fixed encoding/action map.
User steering during this run: parallel Wet Math work suggests a representation
specific to exactly three dimensions, absent below AND above. Record as
proposed theory three-dimensional-exception, not as this experiment's result.
Exact squad argument was not recovered. Need its object, dimension meaning,
allowed maps and preserved property before freezing a 2D/3D/4D test. Three
rows in a 2D block are not three spatial dimensions. Do not invent a mechanism
to fit three or conflate ordinary storage with operational invariance. The
boundary/individuation question remains parked; remainder feedback undefined.

## Research continuation: isolated and periodic defects (2026-09-08)

User explicitly parked the three-dimensional hypothesis and requested work on
what is already before us. Do not ask for its formulation or make a dimensional
comparison the next prerequisite. The previous paragraph's 3D next target is
superseded as an active priority, not mathematically refuted.

`docs/research/2026-09-08-encoded-defects.md` completes the next fixed-2D unit.
Protocol ef79c56 and both instruments a2b59a2 were committed before evaluation.
All 64 six-cell XOR masks, 512 logical backgrounds (-4..4), periodic vertical
application versus one isolated block; fine times 0/2/4. Shrinking causal
windows cover every affected block without artificial boundaries. Thus the
isolated cases are genuine finite defects on the infinite encoded plane.

No initially invalid case returns at fine ticks 2 or 4: 31,744 periodic and
32,256 isolated cases. Repeated mask 33 is a valid logical flip from the start;
it has one background-independent response. At tick 4, its individual masks
1/32 each have 200 responses in periodic mode; isolated 1/32 have 177 each,
isolated 33 has 200. Pair interaction J=delta_pair XOR delta_A XOR delta_B
is nonzero on all 512 backgrounds for periodic (1,32) at ticks 2/4; isolated
pair has zero at tick 2 and 440/512 nonzero at tick 4. All 15 periodic pairs
interact on all backgrounds at tick 4; 14/15 isolated pairs do, except (1,32).

Crucial validity distinction: isolated mask 33 initially leaves all individual
blocks valid but violates equality between vertical copies. For finite isolated
damage, global recovery at any finite time must equal undamaged evolution,
since remote unchanged copies fix all logical content. This is architecture-
specific, not a general no-go for localized computation.

Independent bitset audit agrees on 196,608 full sampled response fields, 384
aggregate records, all classifications, and 90 pair records. Source hashes,
response digests, compact classifications and witnesses in results/encoded_
defects_20260908*. No permanence claim: horizon four fine ticks, sampled at
the stationary even phase. Other shifted phases are not classified.

Next within 2D: determine whether invalid responses spread, move away, or
enter another usable representation. Freeze a longer causal horizon or derive
a structural constraint before calling a survivor persistent. Preserve the
distinction between loss of the original code and loss of all organization.
Remainder feedback remains undefined; boundary/individuation stays parked.

## Research continuation: longer fates and a finite strip (2026-09-08)

`docs/research/2026-09-08-defect-fates.md` completes the 32-tick unit. Frozen
protocol 7512927, both instruments and wording clarification 1a9a923. 6,912
trajectories: 64 masks, 2 modes, 22 minimal-period<=4 aligned backgrounds plus
two independent cohorts of 16 saved random 65-bit words (seeds2026090801/02).
Finite shrinking causal windows, even samples0..32. General backgrounds are
sampled, not an exhaustive extension of Research016's all-background result.
Independent uint64 truth-set audit matches every one of 117,504 response fields,
every metric and recurrence decision. No original-code return among6,750
initially invalid cases; no three-shape screen passes at periods2/4/6/8.
No full-state recurrence certificates, hence no eligible object for the
predeclared conditional perturbation stage. Do not claim periodic-object proof.

Post-census finding: masks6/24 on the zero logical background keep two-row
support and Rule-90 pulse masses. Hypothesis and exact checker committed in
58c9f6f before checking. Let B be horizontal01 repeated at every y. U(s)
replaces ONLY rows0/1 with (0,1 XOR s_i),(s_i,1). Then F^2 U=U phi90 for
all logical inputs and all widths. First tick: row0=(1 XOR left XOR center,0),
row1=(1,center XOR right), all other rows complement B. Second tick returns
to U(left XOR right). All8local triples checked with independent updates;
1,280 fine-field and640coarse-state comparisons at widths5/7 plus768matched
action-word states. A logical flip toggles just (0,2i+1),(1,2i): two physical
cells total, no vertical replication. Background preparation remains a cost;
do not confuse finite action support with absence of a specified environment.

This strip is not vertically repeated every2rows, so it does not contradict
the earlier minimum within periodic block encodings. Isolated masks6/24 on B
are already in U or its translate at time0, not a spontaneously formed code
after a transient. They remain outside E. At t=2n the pulse has mass
2^(1+popcount(n)) and span4n+2: from tick30 to32, mass32->4 but span62->66.
Cancellation/sparsity is not spatial reassembly or a demonstrated fold-in.

Next concrete 2D lead: independent data strips, separated as a control and
adjacent as a coupling test. Determine exact coexistence and interaction laws
before making claims about compositional computation. The ambient F stays
fixed; no fitted decoder. 3D and boundary/individuation remain parked.

## Research continuation: strips compose or interact (2026-09-08)

`docs/research/2026-09-08-coupled-strips.md` completes the two-strip unit.
Protocol c186318 and three instruments 06edcb9 committed before evaluation.
Keep F, horizontal alignment, and cadence two fixed. V_g encodes independent
rows a,b in strips beginning at 0 and g+2; g=0..4 background rows between.
All 64 six-bit logical triples checked for every gap, including ALL output
constant cells and exterior rows. Independent uint64 audit agrees on 320
cases, 200 output/residual polynomials, validity and cross-influence.

For g=1..4, every input preserves V_g and yields independent Rule90(a/b).
The two-phase buffer argument proves the same for ALL g>=1 and any aligned
collection of strips, including infinitely many independently variable rows.
The buffer's 01 phase reads constant bottom-odd1/top-even0 cells, becoming10;
its 10 phase reads constant top-odd0/bottom-even1 cells, returning01. Thus
no data cross it in this invariant family. One row is minimal under this
fixed architecture, not a universal isolation distance.

For g=0, only17/64 local inputs stay valid, all equal independent outputs.
The other47 leave the code; there is no total logical H in this code at
cadence2. Composition residual C=F^2 V XOR V(phi90a,phi90b) lies only in the
touching rows1/2. Two physical cells in each strip depend on the other row.
Residual monomials all mix a/b variables; degrees4/5. First-tick interaction
relative to independent evolution is [[a*b,b*(a XOR a_right)],
[a*(b_left XOR b),a*b]]. Nonzero on32 local inputs at tick1 versus47 at tick2;
different stage counts do not establish pointwise monotonicity. Both rows
identically1 give nonzero tick1 interaction but zero tick2 residual, returning
the zero logical pair. First failed triple pair100/100 decodes1/1 while
constant physical cell(y2,x0) is incorrectly1. Reading candidate bits alone
conceals loss of the encoding.

Gaps1/2: all pairs of ring states at widths5/7 for four coarse steps. Gap1,
width5: all64 length-three words over none/topflip/bottomflip/both, all1024
initial pairs. Independently computed671,744fine fields;139,264coarse paired
states;196,608action-word states. No vertical torus. Local and action
identities prove arbitrary finite matched action words independently of tests.

Next: a bounded enlarged joint representation that retains the interface
residual as state. Fix its variables, decoder, locality and cadence before
testing closure under repeated F. Adjacency's current-code failure is not a
no-go for all coupled descriptions. The physical F remains fixed. 3D and
the separate boundary/individuation thread remain parked.

## Research continuation: the interface escapes (2026-09-08)

`docs/research/2026-09-08-interface-state.md` completes Research019. Main
protocol 740e12f; instruments/storage clarification bd222be; NumPy index-type
fix a7d38d5 before any successful output. Keep F, alignment and cadence2 fixed.
W retains six physical bits per block: (0,1),(1,0),(1,1),(2,0),(2,1),(3,0).
Fixed cells (0,0)=0,(3,1)=1; exterior B. It contains V_0 and all F^2 V_0.

All 64^3 unrestricted symbol triples: 69264/262144 preserve W; 114688 change
exterior rows. Actual original-pair causal census t=2,4,6,8 has respectively
64/64,625/1024,3544/16384,11200/262144 valid W patterns; exterior-change counts
0,183,10321,237892. Local horizon-specific counts, not survival probabilities.
Independent encoders/update/summaries agree on all541760 complete fields.

Post-census witness protocol/instrument53d9e9b: a_1=1,b_0=1, otherwise zero;
physical XOR seed (0,3),(1,2),(2,1),(3,0). Scalar audit checks341968 cells
through32ticks. At t4 the extreme rows contain only(-1,4) and(4,-1).
Subsequent local proof: with all rows above r in B_t,
delta_next(r-1,x)=B_t(x)*delta(r,x-1); below r,
delta_next(r+1,x)=(1 XOR B_t(x))*delta(r,x+1).
Thus top(3-t,t), bottom(t,3-t) for EVERY t>=4; vertical span2t-2. Both tips
retain the required background polarity, and radius1 forbids farther escape.
384 local formula checks corroborate the argument. At t32 mass840, span62.
The growing wake is NOT an isolated traveling object. The all-time claim
comes from induction, not extrapolation of finite pictures.

Consequence: no exact fixed-height horizontal-band encoding against B can
contain this orbit, even in a translating frame. More cells within any
fixed-height band cannot repair that. Does NOT exclude symbolic descriptions
of growing support, other encodings, special inputs, or controlled encounters.

Next bounded lead: fix pulse shapes/law/adjacency and vary relative horizontal
position, classifying which encounters launch outward fronts versus cancel or
remain unresolved. Use the extreme-row identity where applicable; finite runs
do not prove indefinite confinement. No fold-in or logical gate established.
The 3D and separate boundary/individuation threads remain parked.

## Research agenda checkpoint: preserve unfinished threads (2026-09-08)

After discussing [Thinking Like a Function](https://myk.pub/thinking-like-a-function-16),
the user asked to record the boundary question and revisit earlier unfinished
work before choosing the next experiment. No new experiment was selected or
run at this checkpoint. The following is a backlog, not a new frozen protocol.

- **Previously recorded next priority — dimensional compatibility.** The local
  encoding and symmetry audit are complete; a globally compatible evolving
  representation remains open. Specify how overlapping encodings coexist,
  remain valid under evolution, and decode across dimensions with a fixed
  budget. The provenance experiment is complete but does not supply that
  higher-dimensional dynamics. It adds the requirement to distinguish rule
  identity, natural continuation, and responses to declared interventions.
- **Related open question — remainder feedback.** Can a specified feedback
  law sustain compatibility between representations? Earlier mutual and
  derivative replacement models cycled on the tested finite systems. Feeding
  a compatibility mismatch back into the dimensional construction remains
  undefined and untested. Full-base-state change transport closes by identity;
  a bounded-context criterion would need separate design and evaluation.
- **Deferred spatial controls.** Compare Gray-code and geometric assignments
  on larger grids; separately define a locally stored changeable decoder.
  The dimensional-compatibility priority explicitly deferred these questions,
  rather than completing them. See the shared-state/rule continuation above.
- **Earlier open branches.** Learning/discovering reusable primitives with
  charged search and uncertain future tasks; residual-error structure and
  training-budget controls in the regional history experiment; selective
  historical influence, reciprocal constraint, and decomposition/reconstitution
  in `docs/research/2026-09-07-history-and-possibility.md`. Earlier dialogue's
  state-gated derivative-memory measurements still require artifact recovery
  and verification; the separate `mu(S_previous)` reversibility study is not
  a substitute for that model.
- **Parked boundary/individuation question.** How are process boundaries
  established, sustained, changed, or dissolved, and which forms of continuity
  let a unit remain usable within larger processes? Record the user's
  function-as-holon correction as motivation for later operational definitions.
  This question does not automatically supersede the unfinished work above.

The proposed Class-IV connection remains downstream of a defined, nontrivial
compatibility criterion; there is still no persistence score or enrichment
result. This checkpoint adds no experimental finding.

## Research continuation: observed history (2026-09-07)

Recovered **Analysis of Collusion Wiki** research is indexed in
`docs/research/2026-09-07-history-repairability.md`. Read that first for this
workstream; the unchanged earlier notes and source hashes are under
`docs/research/archive/`.

- **Exact checks:** D90=150, D110=162; G110 has degree 4, four monomials,
  10/32 nonzero local windows. The reported dyadic derivative ANF counts
  through horizon 8 reproduce. Rule 90 has exact dyadic parity closure;
  Rule 110 has no radius-one closure for any nonconstant binary block map
  at b=2, strides 1–2, or b=3, strides 1–3. These are bounded claims.
- **Reproduced broad sweep:** all values in the recovered 176-row parity
  and 256-row majority tables reproduced to 1e-12 (the recovered script's
  `wclass` header differs from the archived CSV's `class`). Summary JSON
  reproduced byte for byte. The legacy canonical label for 41 conflicts
  with its cited source; 106's III/IV status is disputed. Keep class
  enrichment exploratory, and don't count equivalent rules as independent.
- **Independent-seed validation:** `experiment_history_validation.py`, 12
  rules × 5 observations × 2 ring widths × 4 test seeds × 7 depths = 3,360
  rows, trained on a disjoint eight-seed ensemble. Matched targets and
  low-support backoff reproduce strong Rule-110 repair, while Rule 30
  also repairs under majority and derivative observations. There is no
  projection-independent Class-IV classifier here. Report seed ranges,
  coverage, and exact projection/cadence with every error curve.
- **Regional follow-up completed:** see `docs/research/2026-09-07-ether-regions.md`
  and `scripts/experiment_ether_regions.py`. Frozen-protocol Rule 110 test:
  two training ensembles, eight shared held-out seeds, widths 420/840, five
  observers, two past-only ether detectors. All 320 departure-region paired
  comparisons improve at h=6; these share data and are not independent
  replicates. Departures contribute 40.4–74.8% of total gain depending on
  observation, width, and detector; background also contributes substantially.
  Primary-detector departure neighborhoods contain 97.2–100% of pooled
  residual error. History beats the equal-bit radius-ten snapshot in all
  160 paired seed comparisons, with better support coverage: this is an
  estimator/budget finding, not proof of irreducible temporal information.
  The detector labels local incompatibility, not glider species or collisions.
- **Next within this workstream:** independently classify residual-error structures; separately vary
  training budget at fixed width for spatial versus temporal contexts. Only
  then estimate sufficient-history scaling or fit reduced dynamics with
  explicit memory. Low empirical error does not prove finite-memory closure.

## New instruments (added 2026-06-30, from a separate chat-interface exploration)

Four directions came out of a parallel conversation; two are implemented,
one is a clear extension, one is intentionally left open. See `NOTES.md`
section 6 for the full writeup and citations.

- **Absential field** (`metrics.absential_field`, `operators.absential_trajectory`)
  — cells that are off but adjacent to an on cell (closed-neighborhood
  dilation minus the live set), distinct from "void" cells with no live
  neighbor. The candidate fast Class-IV-detector use is now settled
  negative — see established result 10 (fair 2D test with real gliders
  and still lifes; absential compressibility always tracks raw). The
  field itself remains a fine instrument (it IS elementary rule 50, per
  the prehoc collapse theorem).
- **Second-order / reversible memory** (`secondorder.py`) — Margolus-Fredkin
  style `S(t+1) = phi(S(t)) XOR S(t-1)`, plus the generalized
  `run_second_order_mu`: memory passed through an arbitrary rule mu.
  Exact result (2026-07-01, `scripts/experiment_memory_variants.py` →
  `site/src/data/memory_variants.json`): reversibility holds iff mu is
  invertible; only {15, 51, 85, 170, 204, 240} are invertible at every
  ring size (others sneak in at particular n — e.g. 14-16 bijective
  rules at odd n, exactly 6 at n=12); the D-memory variant is
  mu = phi^204 (prehoc identity), hence reversible exactly for
  phi ∈ {0, 60, 102, 153, 195, 255}. Backward reconstruction verified
  for all six; docstring carries the derivation.
- **Meta-evolution / rules birthing rules** (`metaevolution.py`) — each
  generation derives a child rule from the current state via a generator
  function, classifies the parent→child handoff with `classify_regime`,
  then (replace mode) adopts the child and evolves under it.
  The generator comparison is now run at scale (2026-07-01,
  `scripts/experiment_metaevolution_scale.py` →
  `results/metaevolution_scale.csv` + `site/src/data/metaevolution.json`:
  5 generators × 40 independent initial states, cycle_window=12).
  Established: the affine-degenerate control G(·,90) locks in at exactly
  2.0 generations with zero variance (theorem-pinned floor); every
  information-carrying generator searches 3-5× longer with separated
  bootstrap CIs (g30 6.1 < absential 7.2 < d90_sample 10.0 ≈
  population_count 11.2); lock-in 100% across the board.
  CORRECTION to the old 8-seed reading: "richer generator → longer
  search" does NOT hold beyond the zero/nonzero information split —
  population count ties the 8-bit derivative sample at the top.
  Two methodology traps found and fixed, recorded in the script
  docstring: (a) replicating across STARTING RULES is pseudo-replication
  (state-only generators make everything after the first handoff depend
  only on the initial state); (b) the default cycle_window=6 detector
  (periods ≤ 3) misread period-4/5 cycles as "never locked" — the
  supposed ~5% open-ended lineages were locked all along (seed 9:
  23→41→19→43 forever), confirmed by chasing them to 400 generations.
  Every locking lineage locks within ~27 generations.
- **Non-uniform / heterogeneous CA** (rule space sharing state's
  dimensionality, i.e. per-cell rules instead of one global rule) — now
  implemented, see established result 8 (`nonuniform.py`). The
  historically-grounded framing (von Neumann's self-reproducing automaton
  carried construction instructions as patterns in the same substrate
  they acted on) admits a useful representational statement: same-time
  rule extraction expands to a bigger uniform CA. This does not invalidate
  the instructional interpretation or establish memory as the only useful
  mechanism; see the September 8 shared-space note.

## Conventions
- Use `src/groovy/ca.py`'s vectorized `apply_rule` for anything beyond toy
  scale. The chat-session origin code used a Python-loop CA step; it's
  correct (cross-checked against this package — see git history / NOTES.md)
  but much slower. Don't reintroduce the loop version.
- `image_ratio` is exhaustive enumeration over `2**n` states — only
  tractable up to roughly n=16–18. Don't call it at the n~100-200 scale used
  for `divergence_trajectory`.
- Keep the interpretive/speculative material (the QM correspondence
  detail, the Jung/Pauli/Unus Mundus framing) in `NOTES.md`, not in
  docstrings or the open task list — those are for the math and the code.

## Working guidelines

**Repo layout, what each piece is for:**
- `src/groovy/` — the library. Source of truth for the math; docstrings
  carry derivations, not just usage.
- `notebooks/` — narrated exploration. Good for working out a new regime
  or sanity-checking a sweep, not a substitute for putting real results
  in `results/` or real findings in `NOTES.md`/`CLAUDE.md`.
- `results/` — sweep outputs (parquet/csv) and generated figures. Treat
  this as data, not scratch space — name files so it's clear what
  parameters produced them (rule range, seed count, date if it matters).
- `site/` — the GitHub Pages site's source (React + Vite, five main pages
  plus generated Research pages):
  home/concepts/questions/remainder/explorer — the questions page was
  called "findings" before a copy pass restructured it around named
  questions each answered by embedded data, per the confidence-labeling
  convention; `remainder.html` ("The Walk" in the nav) is a narrative
  guided tour of the jam-session findings (NOTES.md §9) whose demos all
  compute live in-browser, quoting at-scale statistics from the
  experiment scripts; the concepts page's `#run` section defines the run
  calculus (result 11) and every rendered field on concepts/explorer
  carries a run-signature badge — `RunSig.jsx`, with the Explorer
  deriving signatures from the card graph at render time, never storing
  them in `?seed=` URLs, so keep it that way when adding card types.
  `site/src/lib/groovy-engine.js` is a hand-ported JS mirror of
  `src/groovy/*.py` (1D functions) plus a 2D Life-like extension the
  Python package doesn't have yet — if you change the Python math, update
  the JS to match, and vice versa. Static figures the site embeds (e.g.
  `regime_heatmap.png`) live in `site/public/assets/img/` (Vite's own
  static-passthrough convention, distinct from the repo-root `public/`)
  and are produced by `scripts/build_findings_assets.py` — keep that
  script as the source of those PNGs rather than letting the site
  recompute full sweeps itself; the site's live-computed charts
  (Questions page) work from small hardcoded/checked-in datasets, not
  from re-running `scripts/`. The Questions page's data-backed charts
  read `site/src/data/*.json`, which are *generated* by the matching
  `scripts/experiment_*.py` — regenerate via the script rather than
  hand-editing the JSON.
  **`vite.config.js`'s `base: '/groovy-commutator/'` is load-bearing** —
  this deploys as a GitHub Pages *project* site, not a user/root site, so
  every Vite-emitted asset URL needs that prefix or it 404s against the
  domain root (this shipped broken once already: HTML loaded, 200, but
  the JS bundle 404'd and the page rendered blank). Internal nav links and
  image `src` in the components are deliberately relative (no leading
  `/`) instead of using the base — don't "fix" them back to absolute.
- `public/` (repo root) — **generated**, gitignored. `npm run build
  --prefix site` produces it; `.github/workflows/pages.yml` does this in
  CI before every deploy. Never edit its contents directly — changes
  belong in `site/`. `.claude/launch.json`'s `site-dev` (Vite, hot reload)
  is the normal way to preview. Its `site-preview` config serves the
  built `public/` directly at the server root, **not** under
  `/groovy-commutator/`, so it can't catch base-path bugs like the one
  above — it's for checking page content/behavior only. To actually
  verify the base path, serve `public/` from inside a `groovy-commutator/`
  subdirectory of some root and load it from there.
- `NOTES.md` — the "why": citations, QM correspondence, the speculative
  interpretive thread. `CLAUDE.md` (this file) — the "what to build
  next" and established results to build on without re-deriving.

**Before adding a new "established result"**: it needs to survive being
checked, not just observed once. Confirm computationally (a script or
notebook cell that reproduces it), then promote it from notebook/scratch
into `CLAUDE.md` with enough detail that a future session doesn't need
to rerun it to trust it. If a finding is suggestive but small-sample
(like the pilot sweep), say so explicitly — don't let pilot-scale
findings read as settled.

**Git workflow:**
- Commit at meaningful checkpoints (a result lands, a sweep finishes, a
  module is added) rather than after every small edit — but don't let
  uncommitted work pile up across sessions either.
- Write commit messages that explain *why* a change happened, not just
  what changed — especially for results commits (what swept, what
  changed since the last one).
- Large sweep outputs are fine to commit if they're the actual
  deliverable of the open task (the whole point is having the full
  256-rule sweep checked in) — just keep them as compact formats
  (parquet over loose CSVs-per-pair) rather than raw dumps.
- Don't force-push or rewrite history on `main` without being asked.
