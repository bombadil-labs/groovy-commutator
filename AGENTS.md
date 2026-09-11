# Groovy Commutator — project context for coding agents

This file is the canonical agent guidance (`AGENTS.md`). `CLAUDE.md` imports it
unchanged; Codex reads it directly. Edit this file, not `CLAUDE.md`.

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

## Gathering branches and cross-model review

Agreed with Myk on 2026-09-11. This is the default for research, corrections,
code, and repository maintenance, including changes to this guidance.

- Use one gathering branch per coherent unit of related work, based on
  `main`; prefer the name `gather/<unit>`. Open a draft gathering PR into `main` as soon as there is a diff.
  State the question or purpose, scope, owner, completion criteria, related
  issues, and the other-model reviewer. Keep unrelated programs in separate
  gathering branches.
- Branch chunks from that gathering branch (for example
  `work/<unit>/<chunk>`). Other prefixes, including harness-assigned
  `claude/...` branches, are fine when tooling constrains names; the PR base
  and gathering-PR link define the role. Open sub-PRs back into the gathering
  branch and link its PR.
  Authors may self-review and self-merge sub-PRs after relevant checks pass
  and findings are resolved. A sub-PR merge is integration, not independent
  scientific sign-off. Preserve protocol, implementation, and evaluation
  commit order. Use merge commits for sub-PRs carrying protocol →
  implementation → evaluation commits, and for gathering PRs whose history
  carries that provenance; do not squash away the evidence of that order.
- Before experimental implementation and evaluation, obtain explicit
  other-model review of the frozen protocol, as specified in
  `docs/research/README.md`. A protocol sub-PR is a convenient review point.
  Self-merging that sub-PR does not waive this gate. Record its reviewed
  revision and review link; material changes to predictions, domain, budget,
  or scoring require renewed review before the affected evaluation.
- If the other model is unavailable at protocol freeze, Myk may explicitly
  authorize implementation/evaluation to proceed. Record on the protocol:
  `Protocol review: none at freeze; run authorized by Myk <date>`, with a
  reference to that authorization. Record any implementation authorization
  separately if needed. The results note must say evaluation preceded review.
  Unavailability alone is not authorization. Retrospective review follows the
  correction path; this exception does not waive other-model review before
  merge into `main`. Without authorization, keep the protocol unrun and
  continue useful work outside the gated experiment.
- When the unit is complete, update its notes, knowledge dependencies,
  Program and checkpoint as applicable. List its sub-PRs, deviations,
  negative findings, verification, and unresolved limits in the gathering PR.
  Mark it ready and obtain explicit review from the other model: Claude/Fable
  reviews Codex-led work, and Codex reviews Claude/Fable-led work. Review the
  combined argument, implementation, results, and interpretation.
- Do not merge a gathering PR into `main` until relevant checks are green,
  review findings are resolved, and the other model explicitly signs off on
  the current head SHA. Material changes after review require renewed review;
  after any head change, the reviewer must confirm applicability to the new
  head. If both models authored the unit, state their contributions and
  cross-review each other's work; self-review alone is insufficient.
- A signed PR comment is acceptable when agents share a GitHub account and
  GitHub cannot record a separate formal approval. Include agent/model/session
  identity, date, reviewed SHA, review scope and an explicit sign-off or list
  of remaining blockers. CI success, silence, and a thumbs-up reaction alone
  are not sign-off.
- **The reviewer merges** (agreed with Myk 2026-09-11, replacing "the author
  merges after the gate"). When the reviewing model's gate-2 review finds no
  blockers and every check on that head is green, it merges the gathering PR
  itself, with a merge commit, in the same pass as the sign-off. If a required
  check is still running, the sign-off says it is conditional on that check,
  and whichever side first sees it green merges. Gate-1 protocol approvals
  are never merges. Nothing else changes: the sign-off is still signed and
  pinned to the head SHA, red checks or unresolved findings still block, and
  a head change after review still needs renewed review.
- Put `Closes #...` on the gathering PR that actually resolves an issue.
  Sub-PRs use `Refs #...`; partial work does not close an issue. Use PR
  links for integration/review state and checkpoints for durable research state.
- Do not push directly to `main` or bypass the gathering review gate unless
  Myk explicitly authorizes an exception. Already-run or already-merged work
  receives dated retrospective review/correction; never backdate review or
  imply it preceded evaluation.
- This is an agent workflow, not a claim that branch protection enforces model
  identity. Keep applicable CI enabled for sub-PRs as well as gathering PRs;
  a missing check is not a passing check. Pages publication stays on `main`.
- Result replays run in two tiers (2026-09-11). Every canonical result JSON
  records the SHA-256 of its verifier and inputs; every pull request touching
  an audit's files runs `scripts/check_result_integrity.py`, which recomputes
  those hashes in seconds. That tier establishes provenance coherence only
  (a verifier or input edited without regeneration); it does not inspect
  result content. The full byte-for-byte replay is the content and
  determinism check: it runs on any pull request that modifies the canonical
  result file itself, on pushes to `main`, weekly, and on manual dispatch.
  A new result file must be registered in the integrity script and its
  workflow must carry both tiers.

## Ongoing research and the public site

Start with `docs/research/2026-09-07-history-and-possibility.md` for the wider
program: how inherited structure enables further activity and remains
revisable. Observed-history prediction is one workstream. Keep it distinct
from historical influence within the dynamics and from future capability.
The finite repertoire and costed/returning-task comparisons are complete;
learning reusable primitives remains open. The latest completed unit is the
interface-state experiment and unbounded-escape proof. The 3D hypothesis is parked by explicit user
instruction; continue the fixed 2D workstream. Read its checkpoint log in `docs/research/checkpoints/history-and-possibility.md`
and the lab-scope [unfinished-threads checkpoint](docs/research/2026-09-08-unfinished-threads.md).
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

12. **Representation invariants, first audit** (2026-09-11,
   `scripts/verify_representation_invariants.py` →
   `results/representation_invariants_20260910.json`, program page
   `docs/research/2026-09-10-representation-invariants-program.md`). Two
   declared transformations of ECA: complement conjugation `T_c` (`S ↦ ¬S`,
   `r ↦ r̃`) and reflection `T_m`. Exact: reflection preserves the result-1
   commutator classification for all 256 rules, derivative-observation
   closure, and all 4,608 local-cap budgets. Complement conjugation maps the
   affine bias `c ↦ c ⊕ M𝟙 ⊕ 1` (0↔255, 60↔195, 90↔165, 102↔153) and sends
   the nonlinear zero-G rules 4, 200 to 223, 236 whose G varies; the native
   commutator is complement-covariant **iff the rule is self-dual** (16
   rules); the defect is the complement response `F(x) ⊕ ¬F(¬x)` at
   `x = D(S)`, and the iff is proved by the exhaustive five-cell local check
   (defect radius 2), not by the identity alone; transporting the derivative as a state (`D ↦ ¬D`) makes
   all 256 covariant. Derivative closure holds for the same 30 rules at
   n = 6, 8, 10. Sweep regime labels agree 95.1% (reflection) / 93.9%
   (complement) between a pair and its image, commute pairs exactly; the
   raw statistics agree under 30%, so this is stability of a sampled result,
   not an invariance; the frozen clause that disagreements concentrate on
   two named boundaries is unsupported (they carry 28%/26%). One frozen
   prediction failed: the cap-radius shift under complement is not bounded
   by `h` (the target row transforms too), failing on four h=0 cells; 18
   further flagged cells were right-censored at R ≤ 2, not violations. The
   corrected bound was then frozen and confirmed on all 22 flagged cells
   at R ≤ 6 (`scripts/verify_cap_census_complement_extension.py`): every
   missing cap exists at radius 3 and the shift is 1 or 2, never above h+1.
   Whole-census shift census at R ≤ 4 (`scripts/verify_cap_shift_census.py`):
   O-coordinate caps are exactly complement-invariant at every radius; K
   shifts are 0/1/2 with max 2 (132↔222, 160↔250 at h=2); no cap is created
   or destroyed; the depth-0 cap set of either kind equals the 30-rule
   derivative-closure set (post hoc, exact within budgets). The 2-block
   recoding (`scripts/verify_higher_block_recoding.py`, forward radius 1,
   inverse 0, two stored bits per site; the executed ambient law has
   radius 2 off the family, a recorded deviation, and a radius-1
   componentwise completion gives the same on-family results) leaves cap
   radius unchanged in 665 of 674 decided cells and
   reduces it by one in 9, never more; D, G and derivative closure transport
   componentwise. The Research026 observer family is closed under complement
   and reversal, so that census's scalar summaries are covariant by
   deduction, with optimal observers corresponding under an explicit
   permutation. Codex's retrospective review (2026-09-11) is recorded in
   each protocol's dated addendum. Fifth unit, first non-injective
   transformation (`scripts/verify_parity_coarse_graining.py`, protocol
   reviewed before implementation): neighbor parity `π = rule 102` as an
   observation closes for exactly the 32 constant-complement-response rules
   (16 complement-invariant + 16 self-dual) at every ring `n ≤ 12`, each
   with an elementary factor (`r` and `r̃` share one; fixed points are the 8
   linear rules); the commutator is covariant by linearity; the 224 other
   rules have refinement depth `h_* ∈ {1, 2}`, now certified for every ring
   size by the sixth unit (`scripts/verify_parity_history_bound.py`: a
   finite check on `L`-admissible 8-words plus a lemma; depth-2 set exactly
   {22, 73, 104, 109, 146, 151, 182, 233}, realized at n = 5; rings 7, 9,
   11, 14 agree; run authorized by Myk before Codex's retrospective gate-1
   sign-off; accepted after Codex's gate-2 sign-off, merged in PR #89). Fifth unit accepted after Codex's
   gate-2 sign-off, merged in PR #88. Seventh unit
   (`scripts/verify_linear_observations.py`, gate-1 reviewed): all eight
   linear rules as observations on rings 6–12; closure is decided by the
   kernel: complement-pair kernels (60, 102, 90 on odd rings) reproduce the
   32 and the certified depths; rule 90 on even rings and rule 150 on rings
   divisible by 3 close exactly the 16 affine rules; depth under those
   kernels reaches 4 and varies with ring size. Accepted after Codex's gate-2
   sign-off, merged in PR #91. Eighth unit (`scripts/verify_block_majority.py`,
   gate-1 reviewed): rule 232 (majority) as the first non-linear observation
   on rings 6–12 closes exactly 22 rules, the same at every ring: 14 exact
   commuters with 232 and 8 rules whose observed successor is a constant
   field; the affine rules beyond constants, identity, shifts and their
   complements do not close; depth reaches 16 at ring 12 and grows with the
   ring; neither the parity 32 nor this set contains the other. Accepted
   after Codex's gate-2 sign-off at `7c33051`, merged in PR #92.
   Ninth unit (`scripts/verify_isolated_cell.py`, gate-1 reviewed after one
   witness correction): rule 4 (isolated-cell detection, not self-dual) as
   an observation on rings 6–12 closes exactly 33 rules at every ring: 9
   exact commuters {0,4,42,112,170,200,204,232,240}, 24 rules collapsing to
   the all-zeros field, and rules 123 and 251, closed with a non-constant
   factor that is not the rule (frozen commute-or-collapse prediction
   failed); 251 = ¬F_4 is a function of the observation, 123 is not and
   only shares 251's observed successor on the tested rings; the affine rules beyond
   constants, identity, shifts and complements are not closed; depth
   reaches 22 at ring 12 and is not monotone in the ring; the census is
   complement-covariant when the observation is conjugated to rule 223 and
   not complement-invariant. Accepted after Codex's gate-2 sign-off at
   `5bfa5c8`, merged in PR #93.
   Tenth unit (`scripts/verify_complement_observation.py`, gate-1
   reviewed): observations 32, 200, 22 with conjugates on rings 6–12. The
   complement rule ¬ψ = 255−ψ always closes with factor ψ∘¬ and, for these
   non-self-dual observations, lies in the residual class X = C \ (K ∪ Z);
   the frozen prediction that X is inside ¬ψ's observational-equivalence
   class failed for 32 and 200 (and at ring 6 for 22): under 32 X's four
   rules are each equivalent to a commuter, under 200 X's 17 rules form six
   classes with no commuter and 16 factors not radius-1 on the image, under
   22 the closed set is ring-dependent. Observational equivalence
   (ψ∘F_r = ψ∘F_s) is decided by the 32 five-cell words and is the same at
   every ring n ≥ 5, verified exhaustively for 32, 200, 22, 4; under 4 the
   class {123, 232, 251} certifies the ninth unit's 123 ≡ 251 identity for
   all rings. Depth annex: majority's record rules reach h_* = 25, 26, 28,
   31 at rings 13–16 (bet held); rule 4's record pair 19, 19, 28, 25.
   Accepted after Codex's gate-2 sign-off at `18e900b`, merged in PR #94.
   Eleventh unit (`scripts/verify_wiring_dilation.py`, gate-1 reviewed):
   wiring as a transformation, neighborhood dilation d ∈ {2, 3} on rings
   6–12 under observations 232 and 4. With gcd(d, n) = 1 and the
   observation dilated with the rule, every census and the result-1
   commutator classification are exactly preserved (conjugation by
   i ↦ d·i mod n; 14 cells). With the observation left standard (d = 2,
   rings 7, 9, 11) the closed set shrinks 22→12 (232) and 33→17 (4), the
   observation rule leaves K, depth tables move, and the census equals the
   standard one under the observation rewired to offset d⁻¹ mod n. With
   d | n the automaton is d interleaved n/d-rings and every census, depth
   included, equals the small-ring census; the result-1 classification
   departs from 10/8/238 only on components with fewer than 5 cells.
   Accepted after Codex's gate-2 sign-off at `1b1e071`, merged in PR #99.
   Twelfth unit (`scripts/verify_factor_radius.py`, gate-1 reviewed after
   one witness correction): the locality radius ρ of the factor on the
   image for every closed rule under observations 232, 4, 32, 200, 22 on
   rings 6–12. Observations 200 and 4 are idempotent, so the factor is
   ψ∘F_r on the image and ρ ≤ 2 (theorem): the tenth unit's sixteen
   non-elementary rule-200 factors are exactly the closed rules at ρ = 2,
   every other closed rule under 200 and 4 has ρ ≤ 1. Under the
   non-idempotent 232, 32, 22 every closed rule present at all seven rings
   has ρ ≤ 1 (census; the frozen bet was ≤ 2), except rule 223 at ring 6
   under 22, closed at that ring only, with ρ = 3, a window covering the
   whole six-cell configuration (the one failed cell; a warning sign in
   this census, not a characterization of finite-ring closures). Collapse ρ = 0, commuters ρ ≤ 1, radius 0 also covers
   cellwise factors such as the identity's; tables reflection-invariant
   and complement-covariant to 236 and 223. Gate-2 pending on PR #110.

## Checkpoint logs (read before continuing any workstream)

A checkpoint is a dated statement of state: what a unit completed, what is
frozen and unrun, what is parked, what not to infer. It adds no evidence and
carries no evidence label. Each Program keeps its checkpoints in a log under
`docs/research/checkpoints/`:

- `dimensional-lift.md` — Dimensional Closure and the Commutator Lift, including
  its 2D encoding lineage and the dimensional vision contract.
- `erased-distinctions.md` — Dynamics of Erased Distinctions (its running account
  is the Program page; the log starts from the next unit).
- `history-and-possibility.md` — the history-and-possibility precursor, from
  which the planned learning-and-revising-primitives program branches.
- `representation-invariants.md` — Invariants Across Representation Contracts,
  opened 2026-09-10: which properties survive a declared change of interpreter.

Read the most recent checkpoint for the workstream you are continuing, plus its
Program page, before doing anything. Add new checkpoints there, not here. A
checkpoint that should be public is also registered in the research catalog
with `recordType: "checkpoint"` (see `docs/research/README.md`). A new Program
gets a new log and an entry in `site/content/research-program.json`.

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
  in `results/` or real findings in `NOTES.md`/`AGENTS.md`.
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
  interpretive thread. `AGENTS.md` (this file) — the "what to build
  next" and established results to build on without re-deriving;
  `CLAUDE.md` only imports it.

**Before adding a new "established result"**: it needs to survive being
checked, not just observed once. Confirm computationally (a script or
notebook cell that reproduces it), then promote it from notebook/scratch
into `AGENTS.md` with enough detail that a future session doesn't need
to rerun it to trust it. If a finding is suggestive but small-sample
(like the pilot sweep), say so explicitly — don't let pilot-scale
findings read as settled.

**Git workflow:**
- Commit at meaningful milestones (a result lands, a sweep finishes, a
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
