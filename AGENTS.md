# Groovy Commutator — agent guidance

`AGENTS.md` is canonical; `CLAUDE.md` imports it. Keep this file short.

## Start here

Read [the current research direction](docs/research/START_HERE.md), then
[the current handoff](docs/research/NEXT_TASK.md). The three executable
representation cases and bounded causal-retention audit are complete in this
unit, published through PR #282. On main, treat them as integrated before
proposing another experiment.
Read only the source lineage it needs. Do not resume an old “next unit” just
because a Program page, protocol or checkpoint proposes it.

The scientific question is: **which distinctions can a representation safely
discard, which must it retain, and what does changing representation buy us?**
The [boundaries guide](docs/research/2026-09-21-research-boundaries.md) maps
the exact results, prior art and impossibility limits. Class IV is a motivation,
not a well-defined universal target or a reason to launch another metric sweep.

## Mathematical contract

For one CA rule, `E(S) = phi(S)`, `D(S) = S XOR E(S)` and
`G(S) = D(E(S)) XOR E(D(S))`. Read `src/groovy/` module docstrings for
definitions. Same-law commutation is distinct from autonomous evolution
under a different effective law.

- Declare rule, state family, boundary, observation, cadence and horizon.
- Distinguish exact algebra, exhaustive finite computation, sampled evidence,
  conjecture and implementation failure. No finite horizon establishes an
  unbounded claim without a certificate. A timeout is not a negative result.
- Forward observed-word refinement is not an online suffix-memory bound.
  A finite-ring result is not automatically a result on the infinite line.
- Preserve failures, corrections and original canonical bytes. A hash check
  verifies provenance coherence, not scientific correctness.
- New experiments need a short decision argument: what uncertainty matters,
  what outcome changes our action, what simpler baseline must be beaten, and
  what ends the line. Keep the scope bounded; there is no automatic next unit.

## Gathering branches and cross-model review

Use one `gather/<unit>` branch and draft PR per coherent task, based on `main`.
State the purpose, scope, completion criteria and verification. Preserve
protocol → implementation → evaluation history with merge commits. Do not
force-push or overwrite shared work. Use isolated worktrees when needed.

The default research workflow has two independent review gates: before a
frozen experiment is implemented/evaluated, and before its complete unit
merges into `main`. See the [research authoring guide](docs/research/README.md#integrate-a-research-unit-through-a-gathering-pr)
for the full workflow and exception record. A gate requires explicit review
by an agent independent of that contribution, pinned to the current head;
green CI alone is not review. Material changes require renewed review.
The reviewer merges when findings are resolved and applicable checks pass.
Do not infer independence from GitHub usernames; agents may share an account.

**Dated exception:** Myk explicitly authorized repository consolidation,
closure and merges on 2026-09-21 and suspended peer review with Fable for
this reset. The [reset record](docs/research/2026-09-21-research-reset.md)
states its scope. Integration under that exception is not an independent
scientific sign-off and does not backdate review. This is not a standing
waiver for later work. Do not ask Myk to reauthorize actions already covered
by the current session's explicit instructions.

**Additional session exception, 2026-09-21:** Myk subsequently authorized
Codex to work solo on the representation case studies and bounded
[causal-retention unit](docs/research/protocols/nakamura-retention-20260921.md),
including its separately frozen [locality follow-up](docs/research/protocols/nakamura-local-retention-20260921.md),
including setup, evaluation and integration. Record self-review honestly;
this is not independent review or a standing waiver for other units.

## Evidence and cost

- Do not run an expensive historical experiment merely to orient yourself.
  Start with the canonical results and fast provenance check.
- No evaluation or replay expected or observed to exceed about ten minutes
  belongs in automatic PR, push or scheduled CI. Full scientific runs happen
  outside Actions from a pinned implementation with durable outputs and a
  stated budget. Expensive manual Actions dispatch needs Myk's explicit
  authorization to spend Actions time.
- Register new canonical results in `scripts/check_result_integrity.py` only
  after they exist. Preserve every frozen prediction key, including explicit
  not-evaluated/invalid states; do not silently omit failed or unscored claims.
- Notes and code contain the evidence; checkpoints contain state. The current
  scheduling authority is `docs/research/START_HERE.md`. Update the relevant
  Program/checkpoint when its account changes, not by copying every detail
  into multiple ledgers. Use [knowledge entries](docs/knowledge/README.md)
  for reusable claims and inspect dependencies when correcting a premise.

## Code and validation

- `src/groovy/` is the library. Prefer vectorized `ca.apply_rule` for CA work;
  exhaustive `image_ratio` is only practical on small rings, not n≈100.
- `site/src/lib/groovy-engine.js` mirrors Python math; keep them consistent
  when changing that math. Interpretive/speculative material belongs in
  `NOTES.md`, with its status stated.
- Research Markdown lives in `docs/research/`; register public notes in
  `site/content/research.json` or its `site/content/research/` shards.
  Program metadata is `site/content/research-program.json`.
- Do not edit generated `site/research/` or root `public/` files.
  Keep Vite's `/groovy-commutator/` base and relative site navigation intact.
- After notes/catalog changes, run `npm run test:research --prefix site`
  and `npm run build --prefix site`. Use `npm ci --prefix site` if needed.
  Run `python scripts/check_result_integrity.py` when integrating evidence.
  Add targeted semantic checks for actual risks, not another full replay.

The former 1,200-line guide and result ledger are preserved in the
[historical snapshot](docs/research/archive/agent-guide-2026-09-21.md).
It is evidence of earlier context, not current instructions. Use linked
research notes for established findings; do not grow this file into a ledger.
