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
  independent-agent review of the frozen protocol, as specified in
  `docs/research/README.md`. A protocol sub-PR is a convenient review point.
  Self-merging that sub-PR does not waive this gate. Record its reviewed
  revision and review link; material changes to predictions, domain, budget,
  or scoring require renewed review before the affected evaluation.
- If no independent collaborating agent is available at protocol freeze, Myk may explicitly
  authorize implementation/evaluation to proceed. Record on the protocol:
  `Protocol review: none at freeze; run authorized by Myk <date>`, with a
  reference to that authorization. Record any implementation authorization
  separately if needed. The results note must say evaluation preceded review.
  Unavailability alone is not authorization. Retrospective review follows the
  correction path; this exception does not waive independent-agent review before
  merge into `main`. Without authorization, keep the protocol unrun and
  continue useful work outside the gated experiment.
- When the unit is complete, update its notes, knowledge dependencies,
  Program and checkpoint as applicable. List its sub-PRs, deviations,
  negative findings, verification, and unresolved limits in the gathering PR.
  Mark it ready and obtain explicit review from an **independent collaborating
  agent**. Codex and Claude/Fable remain the default reciprocal reviewers, but
  additional collaborators may join the same review pool. The reviewer must not
  have authored the work being independently gated. Review the combined
  argument, implementation, results, and interpretation.
- Do not merge a gathering PR into `main` until relevant checks are green,
  review findings are resolved, and an independent collaborating agent
  explicitly signs off on the current head SHA. Material changes after review
  require renewed review; after any head change, the reviewer must confirm
  applicability to the new head. If multiple agents authored the unit, state
  their contributions and arrange cross-review so that each independently gated
  contribution is reviewed by an agent who did not author it; self-review alone
  is insufficient.
- A signed PR comment is acceptable when agents share a GitHub account and
  GitHub cannot record a separate formal approval. Include agent/model/session
  identity, date, reviewed SHA, review scope and an explicit sign-off or list
  of remaining blockers. CI success, silence, and a thumbs-up reaction alone
  are not sign-off.
- **Additional collaborators are first-class participants.** A collaborator
  may propose a new research Program in its own gathering PR, contribute
  protocol/implementation/evaluation sub-PRs, and review work from other
  agents. A new Program proposal should state its thesis/question, relationship
  to existing Programs, scope and non-claims, initial research agenda, owner(s),
  and intended review pool; when accepted it gets the normal Program registry
  entry and checkpoint log. Do not force a genuinely distinct proposal into an
  existing Program merely because its vocabulary overlaps.
- Identify agent work by the **signed agent/model/session provenance and PR
  context**, not GitHub username alone. Different agents may legitimately share
  the same GitHub account. Branch names, PR bodies, signed comments, commit
  authorship and session/model signatures are coordination evidence. A newly
  participating agent should use the same signed-review format from its first
  contribution so automated/manual review cycles can recognize its work.
- Review sharing is many-to-many, not a fixed Codex↔Fable pairing. Any
  participating agent may perform Gate 1 or Gate 2 for another agent's work if
  it is independent of that work and has read the current protocol/context.
  Prefer diversity of reviewers across successive units when practical, but do
  not require a particular vendor/model family. The scientific requirement is
  independent review, not brand identity.
- **The reviewer merges** (agreed with Myk 2026-09-11, replacing "the author
  merges after the gate"). When the reviewing agent's gate-2 review finds no
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
- Result verification has two tiers (updated with Myk on 2026-09-12 to bound
  GitHub Actions cost). Every canonical result JSON records the SHA-256 of its
  verifier and inputs; every pull request touching an audit's files runs
  `scripts/check_result_integrity.py`, which recomputes those hashes in seconds.
  That fast tier establishes provenance coherence only (a verifier or input
  edited without regeneration); it does not inspect result content.
- **Do not put long research evaluations or replays in automatic CI.** A job
  expected or observed to take more than about 10 minutes must not run from
  `pull_request`, `push`, or `schedule` triggers. Generate the canonical result
  once outside GitHub Actions from the pinned, reviewed implementation, record
  the execution provenance, and verify the committed bytes with the fast
  integrity tier. Perform any required independent byte-for-byte replay outside
  Actions as part of author/reviewer verification. A manual `workflow_dispatch`
  for an expensive replay may remain only as an exceptional escape hatch and
  must not be used without Myk's explicit authorization to spend Actions time.
  Short replays that remain comfortably inside the 10-minute CI budget may stay
  automatic. In-flight expensive Actions runs that predate this rule may finish,
  but do not automatically rerun them. Convert existing expensive workflows
  before their next execution. A new result file must still be registered in
  the integrity script and its workflow/verification record must identify its
  fast automatic tier and, when applicable, its off-CI full-replay procedure.

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
   and complement-covariant to 236 and 223. Accepted after Codex's gate-2
   sign-off at `4d44aa8`, merged in PR #110.
   Thirteenth unit (`scripts/verify_ring_closure_certificate.py`, gate-1
   reviewed after two correction rounds): closure at every ring size,
   certified. Pairs with equal observations are closed walks in a
   16-vertex pair graph; a rule fails closure at ring n ≥ 4 iff a
   violating three-edge walk (a five-cell pair block with disagreeing
   observed successors) has a return walk of length n−3, read off
   boolean matrix powers, which repeat (k ≤ 7, p ∈ {1,2,3} here), so
   finitely many powers decide every ring; a closure lost at ring n is
   lost at every multiple (theorem). Observations 232, 4, 32, 200, 22,
   102 have the same closed set at every ring n ≥ 7 (22, 33, 33, 42, 11,
   32 rules), equal to full-shift closure; 223 under 22 closes at rings
   3–6 and never from 7 on; rings 3–5 carry many window-sized extra
   closures. 90 alternates
   forever (32 odd / 16 affine even), 150 with period 3 (all 256 off
   multiples of 3 / 16 affine on them). 32 = 4∘¬, so C_32 = conj C_4
   (post hoc). Accepted after Codex's gate-2 sign-off at `4fbb2d5`,
   merged in PR #116.
   Fourteenth unit (`scripts/verify_depth_one_certificate.py`, gate-1
   reviewed after one correction round): refinement depth at most one,
   certified at every ring. Pairs agreeing on ψ and ψ∘F_r are closed
   walks in a 256-vertex pair graph per (ψ, r); a violating three-edge
   walk (seven-cell pair block with disagreeing two-step observed
   successors) with a return walk of length n−3 breaks depth one at
   ring n ≥ 4; boolean powers repeat (≤ 33 here, cap 1024, nothing
   censored). Depth-one sets constant from ring 10 under 232, 4, 32,
   200 (118, 81, 81, 144 rules); period 3 from ring 28 under 22 (183 off
   multiples of 3, 115 on them); parity 248 everywhere; 90 period 4
   (248 odd, 130/138 even), 150 period 6 (256 off multiples of 3,
   100/98 on them). Failed bet: all-ring depth one ≠ full-shift depth
   one under 232, 200, 22, 102 (16, 8, 22, 8 rules have depth one at
   every ring but not on the full shift); closure had no such gap.
   Accepted after Codex's gate-2 sign-off at `25fc0d1`, merged in PR
   #120.
   Fifteenth unit (`scripts/verify_full_shift_depth_two.py`, gate-1
   reviewed after one correction round): full-shift refinement depth at
   most two for all eight observations and all 256 rules, decided by
   reachability in a sparse 4096-vertex pair graph per (ψ, r) (six-cell
   pair vertices, seven-cell edges agreeing on ψ, ψF, ψF², nine-cell
   violating blocks), no matrix powers, no ring certificate at depth
   two. FS² sizes 178, 97, 97, 172, 186, 256, 236, 222 under 232, 4, 32,
   200, 22, 102, 90, 150; parity's 256 by a full-shift deduction from
   the sixth unit's finite certificate, made in this unit. Both bets
   failed: 24 of the fourteenth unit's 54 gap pairs have full-shift
   depth ≥ 3 (232: 58, 78, 92, 114, 141, 163, 177, 197; 200: 135, 149,
   157, 199; 22: twelve rules), so a rule can have depth ≤ 1 on every
   ring and ≥ 3 on the line; and the rings-3-to-14 depth-two gap
   (intersection of D²(n) minus FS²) is nonempty for every observation
   but parity (20, 4, 4, 12, 30, 0, 6, 12 rules), including 4, 32, 90,
   150, which had no depth-one gap. All 54 earlier witnesses realized
   as explicit eventually periodic pairs. Accepted after Codex's gate-2
   sign-off at `8aa35fd`, merged in PR #132 as `3636598`.
   Sixteenth unit (`scripts/verify_full_shift_depth_three.py`, gate-1
   reviewed after one correction round): full-shift depth at most three
   under 232, 200, 22, 4 (conjugates computed; 32 by the deduction
   F_32 = F_4∘¬, F_223 = ¬∘F_32) by sparse reachability on 65,536-vertex
   pair graphs (eight-cell pair vertices, nine-cell edges, eleven-cell
   violating blocks), 121 min. FS³ sizes 198, 181, 234, 106. All three
   bets held: of the 24 deep rules only 4 (under 22: 143, 166, 180, 213)
   have full-shift depth exactly three and 20 have depth ≥ 4; the
   rings-3-to-14 depth-three gap is nonempty under all four (8, 11, 8,
   10 rules); the full-shift class "exactly three" is nonempty under all
   four (20, 9, 48, 9). The ladder of full-shift class against ring class
   is diagonal only at closure. Accepted after Codex's gate-2 sign-off at
   `f33b779`, re-confirmed at the reconciliation head `d4bf27b`, merged in
   PR #144 as `93dcec8`.
   Seventeenth unit (`scripts/verify_full_shift_depth_three_linear.py`,
   gate-1 reviewed by an independent collaborating agent, OpenAI GPT-6
   Astra Pro): full-shift depth at most three under the deferred linear
   observations 90 and 150 (conjugate 165 computed directly; 150
   self-dual), same sparse 65,536-vertex machinery. `FS³` has 250 rules
   under 90 and 246 under 150 (`FS²` was 236 and 222). Twelve rules are
   excluded by pen from the seventh unit's ring depths as controls; of
   the remaining 18 under 90, 14 have full-shift depth exactly three and
   4 (41, 97, 107, 121) at least four; all 24 remaining under 150 have
   depth exactly three. The rings-3-to-14 depth-three gap is nonempty
   under 90 (those same four rules) but **empty under 150** — the first
   time in the program a gap closes rather than widens between depth
   levels, so whether periodic configurations decide a level is a
   property of the pair (observation, level), not of depth alone. The
   ladder is diagonal at closure and depth one under both, off-diagonal
   only at the fifteenth unit's depth-two gap rules, and entirely
   diagonal at the top under 150. Accepted after gate-2 sign-off by
   OpenAI GPT-5.6 Sol at `a1d422c`, conditional on a CI-cost correction
   (reconciliation had accidentally re-triggered the unit's long replay;
   sub-PR #203 bounded it to a manual-authorization escape hatch),
   applicability re-confirmed at `557c3da`; merged in PR #174 as
   `06fa771`.
   Eighteenth unit (`scripts/verify_depth_two_certificate.py`, gate-1
   reviewed): a ring certificate at depth two, certified at every ring
   `n ≥ 4`, reusing the fifteenth unit's 4096-vertex pair graph `G²_{ψ,r}`
   but with boolean powers computed sparsely (out-degree ≤ 4, packed
   64-bit rows) instead of the dense 4096×4096 product the fifteenth unit
   judged out of budget. Refinement depth at most two is decided for all
   256 rules under all eight observations, with nothing censored (cap
   1024 never approached; largest preperiod `k = 40`, rule 123 under 22).
   Three of five predictions held: P1 (criterion exact against the
   fifteenth unit's recorded sets; every `FS¹` rule has no closed
   violating walk; divisibility; dense cross-check), P2 (certificates
   reported), P5 (complement/reflection covariance exact for all 2,048
   pairs). P3's period bets partially failed: `P_4 = P_32 = 2`, not the
   bet 1 (one oscillating rule each, 50 and its conjugate 179); `P_22 =
   12`, not the bet 3 (3 divides the true period); the kernel controls
   and `P_90 = 4`, `P_150 = 6` held. **P4, the main bet, failed under
   observation 22 alone**: twelve rules (104–111, 120, 121, 124, 125)
   leave `D²_22(n)` first at ring 24, not within rings 3–14, so the
   all-ring depth-two gap under 22 is 18 rules, not the predicted 30 (the
   gap is still nonempty for exactly the seven observations other than
   parity: 20, 4, 4, 12, 18, 6, 12). Post hoc, not predicted: `D²_ψ^∞`
   equals exactly the set of rules with no closed violating walk, under
   these eight observations — an observation fenced as such, not a
   proved general theorem. Determinism confirmed by a full second
   off-Actions execution, byte-identical. Accepted after gate-2 sign-off
   by OpenAI GPT-5.6 Sol at `ba7596e`, conditional on two process-only
   fixes (B1: removing a `PEND` allowance in `check_result_integrity.py`
   that would have let a future deletion of this now-evaluated canonical
   result evade the fast integrity tier; B2: updating the gathering PR's
   own body, which had gone stale) both resolved on that same head;
   merged in PR #206 as `bec0ef3`.
   Nineteenth unit (`scripts/verify_closed_violation_depth_three.py`,
   gate-1 reviewed after two correction rounds): the eighteenth unit's
   post hoc identity `D²_ψ^∞ = {r : V²_cl = ∅}` is a theorem at every
   refinement depth, not a coincidence of eight graphs — **Lemma A**: a
   closed violating walk whose endpoints share a strong component
   supplies a return walk of length `m ≥ 1` (the violating walk itself
   when the ends coincide), so the ring criterion fails at `n = m + 3`;
   hence `D^h_ψ^∞ = {r : V^h_cl = ∅}` at every depth `h`. Applied to the
   sixteenth unit's 65,536-vertex depth-three pair graph with **zero
   matrix powers at any depth**, this decides the all-ring depth-three
   set, first failing ring and eventual period the eighteenth unit had
   declared out of reach on cost grounds. All-ring depth-three set sizes
   206, 116, 116, 187, 242, 254, 246 and gaps against the full shift 8,
   10, 10, 6, 8, 4, 0 rules under 232, 4, 32, 200, 22, 90, 150 (gap
   nonempty under exactly six, as bet). The rings-3-to-14 window
   overstates the all-ring gap under **200** alone (five rules — 41, 97,
   169, 225, 233 — leave at ring 16), not under 22 as at depth two, whose
   window is exact at depth three; the eventual periods `P³_ψ = 1, 2, 2,
   1, 1, 2, 6` do not carry up uniformly from the certified depth-two 1,
   2, 2, 1, 12, 4, 6 (collapsing under 22, halving under 90, persisting
   at 2 under 4/32 on an entirely different rule population) — **ring
   windows and eventual periods are properties of the pair (observation,
   depth level), not of depth alone**, extending the seventeenth unit's
   qualitative finding to these quantitative invariants. Corollary B
   (no eventually oscillating rule is constant-diagonal-anchored) held
   with zero exceptions; the general diagonal-anchoring bet held under 22
   and failed under 232 and 200, where a post hoc, one-observation
   association (not a proven cause) connects the late/non-anchored rules
   under 200 to component count. No ring certificate at depth three: the
   onset beyond which the eventual pattern holds is undetermined. One
   bounded artifact-completeness deviation: the canonical JSON omits
   observation 102 from the serialized per-observation dictionaries
   (theorem-trivial, `FS³_102` is all 256 rules, no verdict change).
   Determinism confirmed by full rerun across two independent
   environments (not a same-machine self-rerun): Myk's canonical local
   run and an independent execution in this session, from the identical
   pinned implementation head, byte-identical (SHA-256
   `e2c961a9...d85a6e`), the session's run taking 70.9 minutes. Accepted
   after Codex's (OpenAI GPT-5.6 Sol) gate-2 sign-off at `a12b95c`,
   conditional on five records/scope corrections (G2-B1–B5: an
   all-ring-vs-per-ring wording fix, softened post-hoc causal language,
   corrected run-provenance attribution, completed gathering-PR
   metadata, and the Program-table row plus the observation-102
   deviation record) resolved records-only in sub-PR #226 with no
   scientific or verifier change; merged in PR #218 as `33ddae7`.

13. **The affine-oriented jet lift is a theorem** (2026-09-17,
   `docs/research/2026-09-17-affine-oriented-lift-theorem.md`, proof by
   GPT-5.6 Sol imported verbatim in `docs/research/proofs/`, Fable's
   independent verification `scripts/verify_affine_lift.py` →
   `results/affine_lift_20260917.json`, ~10 min, off Actions). Every binary
   finite-memory CA on Z^d has an exact, locally recoverable,
   self-synchronizing lift by the six-field grammar
   `(X⊕τ_{v+}X, 1⊕X⊕τ_{v−}X, X⊕HX, X⊕H²X, 0, X)` on a period-six axis,
   rails `±e` at entry with inherited memory `M+{−e,0,e}` and new-axis
   radius 3, then diagonals `a_n ± e` with one radius-3 axis per later
   floor, through every finite depth. Verified on all 256 ECAs (all 512
   dependency words), eight radius-two parents (2^15 words each), Conway's
   Life, the D3 diagonal recursion for all 256 roots, and the row-algebra
   witnesses. Beam-only: off-beam completion is free and no ambient class
   follows. Not unique (a period-3 necklace code is a simpler valid lift;
   coset-induced CA are the trivial layered prior art). Binary only.
   Companion exact identities on the 7-ring, all 256 rules: centered
   `G°(X) = B_H(X, D_H X)` (polarization on the trajectory graph; all-pairs
   polarization vanishes iff affine, the restriction also for 4 and 200);
   `G = ∂H_X(D_HX) ⊕ H(D_HX)` is the tangent-versus-point defect, which is
   why native lifted G is completion-dependent; the two-beam product lift
   transports `K_t = D_H(H^tX) ⊕ H^t(D_HX)` (`K_1 = G`) completion-free at
   every depth, with cocycle `K_{t+1} = G(H^tX) ⊕ ∂H(K_t)`. Review gates
   were suspended by Myk for this integration (GPT had no GitHub access);
   author and verifier differ, the merge was self-gated.

14. **First-floor forced tables cached, section 37 verified, the lift
   metric does not predict pair regimes** (2026-09-17,
   `docs/research/2026-09-17-forced-tables.md`,
   `scripts/forced_tables_20260917.py` → `results/forced_tables_20260917/`,
   11 min, off Actions). Ring-free full-input tables for all 256 ECAs (768
   to 3,072 forced entries of 2³⁵; 110: 1,374), zero collisions; every
   invariant GPT reported in proof section 37 reproduces exactly (hull
   dimension 30 for all rules; output degrees 4/51/201; 30,320 compatible
   and 17,926 nonvacuous pairs; the 88-value orbit fingerprint). Cohabitation
   is exactly reflection-invariant and complement-covariant; the 16 affine
   rules are a compatible clique; every one of the sweep's 1,164 commuting
   pairs cohabits, and nonvacuous-meeting rates fall commute 0.89 > drain
   0.67 > crystalline 0.55 > structured 0.52 > noisy 0.47. **Failed bet:**
   the conflict metric's AUC for commute-versus-rest is 0.537 against 0.527
   for truth-table Hamming distance, so cohabitation carries almost no
   dynamical ordering beyond the eight table bits. On an eight-rule panel
   D3 cohabitation equals D2 cohabitation. Maximal cliques of the
   nonvacuous graph are censored (tens of millions) and uninformative. The
   orbit fingerprint is identifying: anonymous probes get coarse summaries
   only. Self-gated under Myk's suspended review gates.

15. **Rule 110 has a refinement fiber, and it is enriched; chirality is not
   detectable** (2026-09-17, `docs/research/2026-09-17-handed-fiber-census.md`,
   `experiments/handed_fiber_census_20260917/` →
   `results/handed_fiber_census_20260917/`, 46 min, off Actions). The
   Life-like family reaches only the 64 reflection-symmetric ECAs, so the
   Class-IV Program's headline rule had no fiber. The **handed family**
   `f(c, w, n₇)` (centre, west neighbour, count of the other seven; 32-entry
   table, index `16c + 8w + n₇`) contains the Life-like family and its
   height-one restriction is a **coordinate projection onto all 256 ECAs,
   every fiber exactly `2²⁴` rules** — the eight exposed indices
   `{0,3,18,21,10,13,28,31}` are distinct. Height two reaches all 32
   conditions, so it is a genuine refinement with no bolt-on freedom.
   Census at height two, contract otherwise unchanged, 5,268 rules: fiber(110)
   is both-positive at 0.543, in a three-way tie with its mirror 124 (0.555)
   and 54 (0.531), far above 30 (0.273), 90 (0.223), 0 (0.164), 204 (0.105).
   **The enrichment is on the persistence axis, not spreading** — fibers 22
   and 30 spread more (0.922, 0.906 vs 0.844) and still fall far below,
   persisting at 0.469 and 0.312 against 0.629. Across all 256 bases a base's
   own 1D phenotype predicts its fiber's on **both** axes (spreading
   p ≈ 2e-16, persistence p ≈ 3e-9, descriptive); the 64-census's
   non-additivity replicates in eight bits with the same shape (interactions
   win out of sample for spreading only). **Failed bet:** chirality is not
   detectable — fiber(124) is indistinguishable from fiber(110) (spread 0.852
   vs 0.844, p = 0.81, estimate reversed), so marking a direction changes
   which rules are in a fiber without changing what the fiber is like.
   **Methodological lesson worth carrying:** the frozen null-pair calibration
   compared two *independently seeded* samples of the deduced-identical fibers
   110 and 137 and so rejects at the nominal rate by construction; it did
   (p = 0.027). A matched-seed control (same seeds, complemented initial
   states) shows the implementation exactly complement-covariant to 1.6e-15.
   Null-pair calibrations must pair the draws, not only the distributions.
   Self-gated under Myk's suspended review gates; protocol drafted by
   Fable 5.1, amended and executed by Opus 5.

16. **Persistence decomposes: the base sets history gain, the completion sets
   retention** (2026-09-18,
   `docs/research/2026-09-18-matched-completion-persistence.md`,
   `experiments/matched_completion_20260918/` →
   `results/matched_completion_20260918/`, 50 min, off Actions). Persistence
   is `R* > 0 ∧ M* > 0`. Because the handed restriction is a coordinate
   projection, **a 24-bit completion is one object shared by every fiber**:
   `embed(r, u)` exists for every base, so the base can be varied with the
   completion and every seed held fixed across them. Grid: 8 bases
   {110, 54, 22, 5, 30, 90, 0, 204} × 512 completions at height two, a
   64-completion replicate tier, a 128-completion height-four arm; 5,632
   evaluations. **History gain is base-dominated** (df-adjusted variance
   component 0.0396 vs the completion's 0.0116) and **retention is
   completion-dominated** (0.0217 vs 0.0348); spreading is base-dominated
   too, so retention is the one observable the refinement chooses. Holding a
   completion fixed, 110 beats 30 on `M*` for 87.1% of completions with a
   null `R*` difference (sign 0.488, mean 0.011). `M*>0` fractions separate
   sharply (110 0.986, 22 0.984, 5 0.980, 54 0.975 vs 30 0.467, 90 0.564);
   `R*>0` is flat (0.674 down to 0.258). Two unpredicted structural facts:
   `M*` **anticorrelates** between distant bases rather than failing to
   transfer (Spearman −0.414 for 110/30, −0.254 for 110/90, while 54, 5, 22
   run positive) — unexplained, and the best open question here; and `M*` is
   **not bit-additive at all** (cross-validated `R²` negative in all eight
   bases) while `R*` reaches 0.271. **Failed bets:** P3 by 0.042 on one
   pilot-set threshold (110/54 transfer 0.558 vs 0.60, pilot 0.81 on sixteen
   completions); P5's conjunction (`R*` additivity 0.271 > 0.25 ceiling;
   spreading test-retest 0.842 < 0.90 in base 110, while `M*` and `R*` are
   ≥ 0.955 everywhere); and **P6, which corrects the Class-IV reading** — at
   height four the persistence-only control rule 5 (1D `M` 0.976 vs 110's
   0.903) overtakes 110 on mean `M*`, 0.290 vs 0.277, height two being at the
   ceiling for both. **So history-gain inheritance tracks the base's
   one-dimensional history gain, not its informal class**: result 15's
   enrichment stands, Class-IV-ness is not its explanation. Two process
   lessons: predictions calibrated on a pilot must be declared a
   pre-registered replication per prediction (P3 failed exactly as that
   framing anticipates); and P4 was scored on df-adjusted variance components
   because raw `η²` is inflated for the 512-level factor, but **raw gives the
   same verdict on both arms** — the adjustment removed an artifact risk, it
   did not decide the outcome. Self-gated under Myk's suspended review gates;
   protocol drafted by Fable 5.1, amended and executed by Opus 5.

17. **The invariant beam: an exact theorem, and why history gain
   anticorrelates between rules** (2026-09-18,
   `docs/research/2026-09-18-beam-mechanism.md`,
   `experiments/beam_mechanism_20260918/` →
   `results/beam_mechanism_20260918/`, 49 min, off Actions).
   **Theorem (exact, independent of the census).** On a height-two strip the
   vertical wrap sends both off-rows onto the other row, so a state with equal
   rows has Moore count `3L+2C+3R` and west neighbour `L`, making its condition
   index `16C + 8L + (2L+2C+3R)` — **exactly the height-one exposed index** for
   `(L,C,R)`. Those entries are fixed by the base ECA and unreachable by any
   completion, so **the equal-row set (the *beam*) is exactly invariant under
   every rule of the handed family, and on it the strip IS the base rule**: a
   closed, shift-invariant, `F`-invariant subsystem conjugate to the base
   elementary automaton. Verified for 16 bases × 8 completions × 256 steps at
   heights 2 and 3 as a gating control.
   **Mechanism.** History gain is therefore a mixture — the base's own 1D value
   on the beam, a completion-set value off it — so beam proximity is a *shared*
   mediator and each base responds with the sign of its 1D gain minus the
   off-beam value. Opposite-signed responses to a shared mediator are result
   16's anticorrelation. Measured on 16 bases × 256 fresh completions: the
   anticorrelation replicates at −0.341 (bootstrap [−0.444, −0.227]) and
   **reverses to +0.204** conditioned on the two proximities (+0.163 on
   transverse stability); transfer sign equals the product of response signs in
   53 of 55 strong pairs; beam proximity transfers at ≥ 0.349 on **all 120
   pairs**; response ordering against 1D gain is **0.960** (bootstrap [0.919,
   0.972]) over 16 bases, 8 of them never used to find the mechanism; on-beam
   medians equal the 1D values (5: 0.968 vs 0.976; 33: 0.556 vs 0.563; 22:
   0.132 vs 0.137; chaotic ≈ −0.003 vs 0) while off-beam medians occupy a
   base-indifferent band 0.029–0.170; retention is unmediated (0.623 raw vs
   0.634 partial), so the beam is specific to history gain.
   **Failed bet, and a design lesson:** P4, expected to fail, held. The off-beam
   value is 0.03–0.17, not the ~0.2 result 16 implied, so rules 18 and 22 still
   respond positively and the naive sign rule agreed with the mixture reading
   (P4′, which held on all ten testable bases). **No base on this panel falls in
   the discriminating window** — 1D gain strictly between 0 and that base's own
   off-beam median — so the comparison P4 existed to make did not happen.
   **P7 failed:** the anticorrelation does not survive to height three (+0.074),
   because on-beam fractions there are far higher (0.771 vs 0.458 for rule 110)
   and the mixture degenerates. Post hoc reading of a demoted descriptive arm.
   **Process lesson, learned the hard way:** the first canonical run was
   discarded because its matched null-pair control failed on a copy-paste bug
   in the control's own conjugate beam-state construction, **and** because the
   implementation ran that control *after* the tiers, so a broken control gated
   nothing. **Controls must run before observables and must raise; a control
   that cannot fail is worse than no control.** Re-run in full rather than
   patched so the committed runner is the runner that produced the data.
   Open: *which* completions attract trajectories onto the beam (transverse
   stability gates residence almost perfectly downward, ≤ 0.034 on-beam given
   low stability). Self-gated under Myk's suspended review gates; protocol
   drafted by Fable 5.1, amended and executed by Opus 5.

18. **The defect algebra: twelve exclusive-ors decide what a refinement does
   to the beam** (2026-09-18, `docs/research/2026-09-18-defect-algebra.md`,
   `experiments/defect_algebra_20260918/` →
   `results/defect_algebra_20260918/`, 37 min, off Actions).
   **Theorem (exact, independent of the census).** Flip one cell of a beam
   state: exactly six reads change and **none of the post-flip reads lands on
   an exposed entry**, so the damage is carried entirely by free entries.
   One-step healing is `A(LL,L) ∧ B(L,R) ∧ C(R,RR)` — twelve pairwise
   bit-equalities between free entries, GF(2) rank **11**, giving 2,048
   signature classes of 8,192 refinements each, a 13-dimensional
   universal-healer subspace, and expected one-step healing exactly `1/8`.
   The `A` pairs are 1 table index apart, `B` 14, `C` 6. **Edge lemma:** for
   any defect cluster the column west of its leftmost defect reads the `A`
   pair and the column east of its rightmost reads `C`, regardless of the
   interior, so `A` is leftward growth, `C` rightward, `B` isolated survival
   at **every** step; hence `A` or `C` never holding ⇒ transverse extinction
   0, both always holding ⇒ confinement, all twelve ⇒ immediate healing.
   Re-derived from the read-index definition by the executing session and
   asserted as a gating control (six perturbed reads none exposed, 14 lit /
   10 dark, factorization for all three blocks, rank 11, cell sizes exactly
   8,192, simulated step = violated-constraint count on 256 pairs, zero
   mismatches).
   **This corrects result 16.** History gain and transverse stability were
   recorded there as "not bit-additive at all" (negative CV `R²` on the 24
   raw bits). On the **twelve exclusive-ors** transverse stability gives CV
   `R²` **0.369–0.433** in every base, against **−0.145 to −0.271** on the
   raw bits. The effect was never absent; the basis was wrong. Do not repeat
   the non-additivity claim without this.
   Census, 8 bases × 408 completions (192 random, 96 flip partners, 120 built
   into five signature cells): P1, P2, P3(c), P4, P5, P6 held. `H1` (the
   beam-measure-weighted healing rate) predicts transverse stability at
   Spearman 0.685–0.865. **P3(a) failed on one base of eight**: universal
   healers sit on the beam in 83–96% of trials with median proximity 1.000 in
   seven bases and **never under the identity rule 204**, so healing isolated
   defects is very nearly sufficient for residence, with one exception.
   **P3(b) failed on a non-theorem clause**: growers never sit on the beam
   (0 everywhere, as required), but in three bases their median proximity
   *exceeds* the random arm's — **residence from a dense random start is not
   the same quantity as isolated-defect healing**, and what sets it is the
   open question. **P4(b) held although expected to fail**: dark-entry flips
   leave beam proximity as well as transverse stability nearly unchanged, so
   the ten dark entries appear unread even by dense random states.
   **Freeze amendment, and a standing rule:** the eastward-grower cell was
   run rather than deduced, because **reflection is not a symmetry of the
   handed family** (it maps to the east-marked family — the same reason
   result 15's chirality question needed measuring). Both growers have
   transverse extinction exactly 0, confirming the edge lemma in both
   directions; their proximity statistics differ by ≤ 0.12 with no consistent
   direction, plausibly noise at 24 per cell.
   **Process lessons:** the first launch stopped at the matched null-pair
   control with nothing computed (dropped complement flag; trajectory helpers
   imported from result 17's unit, carrying its seed namespace), costing two
   minutes instead of a discarded run — controls-before-observables is paying
   rent every unit. New rule earned here: **do not import another unit's
   measurement helpers; copy them with this unit's seed function**, or the
   provenance silently belongs to the other protocol. Self-gated under Myk's
   suspended review gates; protocol drafted by Fable 5.1, amended and executed
   by Opus 5.

19. **The dense defect algebra: popcount decides which entries a column reads**
   (2026-09-18, `docs/research/2026-09-18-dense-defect-algebra.md`,
   `experiments/dense_defect_algebra_20260918/` →
   `results/dense_defect_algebra_20260918/`, 58 min, off Actions).
   **Theorem (exact).** At height two both rows of a column read one table
   entry each, and the stratum of *both* reads is decided by `Δ`, the
   difference of the rows' three-cell popcounts: `Δ = 0` reads **exposed**
   entries (owned by the base ECA), `|Δ| = 1` reads **lit**, `|Δ| ≥ 2` reads
   **dark**. The 64 six-bit windows give 8 trivially agreeing cases and 28
   unordered pairs — **6 exposed, 15 lit, 7 dark, no mixed pair**. This
   **characterizes result 18's 8/14/10 entry partition instead of enumerating
   it**: the counts were what they were because of what two popcounts can do.
   GF(2) ranks 11 and 7 over 24 free entries leave exactly **64** completions
   satisfying every free constraint (`U++`), one per connected component;
   result 18's twelve are a subset of the fifteen and the three extra lit
   pairs are implied. **T3:** β-all-hold ⇔ the base is totalistic (exactly 16
   rules), and such a base with a `U++` completion collapses *any* state in one
   step (confirmed on 0, 22, 232 × all 64: `agree = 1.000` exactly). **T4:**
   under 204 and 51 the residual is exactly the width-two anti-phase runs of
   the initial disagreement field, `agree = 1 − 2N_ap/521`; both bases give a
   **bit-identical** median `0.9366602687140115` with strata `[50392, 0, 0]`
   — all blind — while differing sharply on every other arm. **T5:**
   disagreement survives only through blind columns, verified on trajectories.
   **This corrects the reading of result 18's open question.** The identity
   exception is **not** about the base contributing no mixing: rule 51 flips
   every cell every step and has the identical residual, while totalistic rule
   0 heals every planted pair. Permanence 1.000 / 1.000 / 0.205 / 0.031 /
   0.000 on 204 / 51 / 90 / 5 / {0, 22, 110, 30}. **Four bits of the base
   decide it, not activity.** Do not repeat the activity reading.
   Census: 20 bases × 7 arms × 208 completions = 4,160 evaluations; ten
   controls first, all passing, in 170 s. `ρ` tracks pair survival at Spearman
   **0.934**; all twelve `Π = 0` bases have `ρ ≤ 0.005` and `P(on) ≥ 0.95`.
   **Failed bets, three of them the executing session's own.** (a) The
   "base-indifferent grower floor of ~0.75", read post hoc off eight bases, is
   **refuted** on twenty — bases 54 and 18 sit at 0.316 and 0.279. (b) The
   stratum decomposition's **specificity fails**: the confined cell `K`, whose
   residual it calls lit-governed, is ordered by pair survival at −0.454 where
   `U++` is at −0.992 — the decomposition keeps its direction and loses its
   clean form. This is the unit's most important negative and it exists only
   because the `K` arm was restored against the draft, which had dropped it as
   "not needed" while resting its central argument on it. (c) The **handed**
   edge assignment (`e_G = β₁+β₃`, `e_G′ = β₂+β₄`) is **unsupported on this
   panel, not refuted**: the two scores are identical on 13 of 20 bases
   (Pearson 0.669), each grower is ordered slightly better by the *other*
   score, and both discriminating within-base tests failed in the reversed
   direction. (d) The dark-bit bet **reversed**: `D+` beats random on *active*
   bases (mean +0.095) and loses on *frozen* ones (−0.037) — beam-frozen does
   not mean dark-quiet, since the frozen bases carry among the highest
   random-arm dark counts. Self-gated under Myk's suspended review gates;
   protocol drafted by Fable 5.1, amended (K arm restored, integer control)
   and executed by Opus 5.

20. **Permanent structures: the isolated-defect gadget is exact, and specificity
   fails twice** (2026-09-18,
   `docs/research/2026-09-18-permanent-structures.md`,
   `experiments/permanent_structures_20260918/` →
   `results/permanent_structures_20260918/`, 81 min, off Actions).
   **Theorem (exact).** Residence is not a transient — the disagreement field is
   already permanent when scoring begins. Under `A ∧ C` an isolated defect's west
   flank reads `A(LL,L)`, the defect column `B(L,R)`, the east flank `C(R,RR)`,
   and the columns two out are inert, so `(L, d₀, d₁, R)` is a **deterministic
   16-state automaton with a 2-bit input** from the background. SAFE/DOOMED
   partition the 57,344 confined refinements into **`K∀` 24,576 / `K∃` 28,672 /
   `K⊥` 4,096**. Gadget against the real step: **0 mismatches of 22,270**. On the
   four frozen-context bases (204, 51, 0, 8) iterating it predicts **every one of
   6,144 transverse trials' healing step exactly**; across all 36 bases the
   partition bounds extinction with **0 violations of 1,728**, every `K⊥` at
   `T_ext = 1`, no SAFE-started trial ever healing. **T0:** `γ` is a function of
   `β`, so the 256 rules are **16 blocks of 16**. **T1:** `|D_{t+1}| = Σ_p v_p
   N_p(t)` exact at 0 of 512 — residence is affine in the 22 violation bits *at
   fixed census*.
   **Independence horizon.** Under `A ∧ C` the defect set never grows, but a
   cluster perturbs the agreeing background (flanks take the forced values, not
   the base's) and that perturbation travels at speed one: **two clusters
   separated by `s` columns are independent for `t < s` and no further**. First
   mismatch never precedes step `s` (minimum 4, 6, 8 at `s` = 4, 6, 8); none
   within 128 steps once `s ≥ 12`. Established by refuting **two** successive
   stronger claims — the draft's, and the executing session's own freeze
   correction of it (15 violations of 72).
   **Main positive:** residence **is** permanence on the confined arm — pooled
   Spearman **−0.836**, ≤ −0.6 in every one of 36 bases.
   **Main negative, and the one to carry:** the stratum decomposition's
   **specificity fails a second time, under a test built to be fair to it**.
   Result 19's P7 was *mis-formed* (`K ⊂ A ∧ C` inherits a blind term, so some
   ordering was guaranteed). This unit subtracts the shared term by construction
   and `K∀`'s **non-blind** term is still ordered by pair survival at **+0.829**
   against a predicted `|ρ| ≤ 0.4`. The decomposition has direction, not
   specificity. Do not restate it as specific.
   **Failed bets.** P6 is a **design failure of the executing session**: a
   36-base panel with 23 discriminating on `e_G ≠ e_G′` (against result 19's
   seven) was chosen precisely to decide handedness, and returned **10 of 23
   against a chance expectation of 11.5** — no signal, yet inside the
   pre-registered "unsupported" band rather than the ≤ 9 called a refutation.
   Handedness is **not refuted**; the banding left a dead zone. P3c failed **not
   on its named risk** (51 vs 90 behaved as predicted at 0.859 vs 1.0; bases 50
   and 178 broke it at 0.8125). P3b **inverted** (`K∃` spread 0.188 < `K∀` 0.297,
   ratio 0.63 against ≥ 2). P4b failed at 12 of 36 — the relationship is nearly
   as strong on the random arm, so the gadget's applicability does not by itself
   distinguish the confined arm. P7c is **zero of 36** — gadget class does not
   make residence additive.
   **Correction, same day:** two frozen predictions of this unit, P3(d) and
   P5(c), were **never scored** — no flank-change field in the rows, no key in
   the evaluator — and the note and checkpoint originally reported them as
   unsupported. Their status is **not evaluated**, and this unit gives **no
   evidence either way on a base-only predictor** of the `K∃` position. The
   implementation silently dropped two frozen predictions and the pilot test
   caught only crashes, not incompleteness. **An evaluator must score every
   frozen prediction or name the ones it does not and why, and a control must
   assert the scored key set equals the frozen set.**
   **Process rules earned here.** *Verify on the adversarial cell, not a random
   draw* — uniform draws from the confined set are dominated by fast-healing
   classes, which is how two successive independence claims passed their checks
   and died in the control. *Test the evaluator against pilot rows before calling
   it frozen* (result 19's was committed untested and crashed on load). *Stage
   results directories by path while a run is in flight*, never `git add -A`.
   Self-gated under Myk's suspended review gates; protocol drafted by Fable 5.1,
   amended (independence radius, later itself refuted) and executed by Opus 5.

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
- `class-iv-refinement.md` — Class-IV Refinement, opened 2026-09-17 from the
  GPT handoff after the lift theorem: which distinctions and observables a
  representation change exposes, and whether a source rule's refinement fiber
  is enriched in the persistence × spreading phenotype. Its inherited units
  (Jev scout, the 54/110 discriminator with partial provenance, the 2D panel,
  the exact strip quotient) are recorded there.

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
