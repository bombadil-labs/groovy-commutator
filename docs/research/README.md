# Writing research, then explaining it

For the active research question and task, read [START_HERE](START_HERE.md).
This file is the authoring/workflow guide, not the research agenda. Older
“next” sections do not reopen parked work.

[FINDINGS.md](FINDINGS.md) is the accessible running synthesis: what we were
curious about, what we tried, what we found, and within which limits. Update
it when a unit ends; link evidence and preserve corrections and inconclusive
outcomes. It adds no evidence or independent review. The
[portfolio survey](2026-09-22-program-survey.md) explains current scheduling.

Research is the public working scientific record. It is built from five
primitives, each with one job:

1. **Note** — adds evidence and carries an evidence label: an experiment, a
   proof, a correction, a failed prediction, a bounded claim. Numbered, or
   labeled when deliberately unnumbered.
2. **Protocol** — frozen intent, written and committed before any evidence
   exists (`docs/research/protocols/`).
3. **Checkpoint** — a dated statement of state: what is settled, open, parked,
   and what the next frozen thing is. It adds no evidence and carries no
   evidence label. Every checkpoint has a scope: one Program, or the lab.
4. **Program** — a living synthesis of what one research line currently
   thinks, with exact results and open proof boundaries stated together.
5. **Knowledge entry** — one compact reusable claim with typed relationships,
   extracted from the record without erasing its evidence trail.

A checkpoint must never be the only record of a result: if it states a number,
the number lives in a note and the checkpoint cites it.

The main React pages remain an accessible route into the original calculus and
instruments. Promotion to those pages is still useful when an idea deserves a
newcomer-facing explanation, but Research is no longer only a staging area for
main-site content. Some mature technical ideas belong in the Program itself.

The [knowledge base](../knowledge/README.md) keeps the current account of
individual findings, questions, theories, and experiments, with typed
relationships and dependency paths. After a substantial research unit,
update the relevant knowledge entries and their relationships. Cite the note
from each entry; the site generates links back in both directions.

## Update the living Program

The current Program metadata lives in `site/content/research-program.json`; its
Markdown source is named there. The public route is
`/groovy-commutator/research/program.html`.

Update the Program when multiple notes change the project's working theory, not
after every experiment. Treat it as a compression layer rather than a new
research result: preserve uncertainty, link every major claim to supporting
records, and keep failed predictions in the chronological notes instead of
rewriting history. The `supports` list must name registered research records.

## Keep the Program's checkpoint log

Each Program has a dated checkpoint log in `docs/research/checkpoints/` (one
file per Program). When a substantial unit completes, add a checkpoint at the
top of the relevant file: what was completed, what is frozen and unrun, and
what not to infer. The logs are read by agent sessions before continuing a
workstream; `AGENTS.md` points at them. A new Program gets a new log when it
is registered. A checkpoint that should be public, such as a lab-wide agenda,
is written as its own dated Markdown file and registered in the catalog with
`"recordType": "checkpoint"`, a `scope` (`"lab"` or a Program slug), a
`label`, and `"evidence": "state"`; it never appears in a Program's `supports`
list because it is not evidence.

## Add a research note

1. Write `docs/research/YYYY-MM-DD-short-name.md`. Start with a single `#`
   title, then use `##` sections. Lead with the question and a plain-language
   answer, or say explicitly that the experiment has not been run.
2. Record the setup, definitions, evidence, limits, and next question. Link to
   reproducible scripts and saved results; include seeds, sizes, parameters,
   and uncertainty where relevant. Distinguish measured results, exact claims,
   and interpretation. Preserve negative results and failed conjectures.
3. Add an entry to the research catalog. `site/content/research.json` is the
   original catalog; larger research waves may be kept as JSON array shards
   under `site/content/research/`. Ordinary notes use the next unused note
   number. A deliberately unnumbered note instead carries a short `label` in
   place of `number` (and no `recordType`). The catalog title,
   summary, and takeaway are the accessible entrance to the longer record.
   Choose a stable slug; its public path is
   `/groovy-commutator/research/<slug>.html`.
4. Validate and build from the repository root:

   ```bash
   npm ci --prefix site
   npm run test:research --prefix site
   npm run build --prefix site
   ```

No page component or route list needs editing. Vite generates the index and
all registered records, renders equations at build time, and bundles local
figures and math fonts. The generated `site/research/` and repo-root `public/`
directories are ignored by git. The existing Pages workflow deploys from
`main`; changes under `site/`, `docs/research/`, or `results/` trigger it.

Example catalog entry (replace every example value with the actual note):

```json
{
  "slug": "a-new-question",
  "number": "004",
  "title": "A question a reader can understand?",
  "date": "2026-09-08",
  "updated": "2026-09-08",
  "kind": "Experiment",
  "evidence": "exploratory",
  "topic": "Observation and memory",
  "summary": "What was tested, what happened, and the key limitation.",
  "takeaway": "One concrete idea to carry away, with appropriate uncertainty.",
  "source": "docs/research/2026-09-08-a-new-question.md",
  "promotion": { "stage": "research" },
  "related": ["history-repairability"]
}
```

Catalog identities are validated across the original file and every shard. The
index orders records by most recent update, then note number; unnumbered
labeled notes follow numbered notes from the same update date, and
checkpoints follow both. Keep the original
publication date and update `updated` when the substance changes. Use existing
topic names when continuing a thread. `kind` describes the document (for
example Experiment, Correction, or Research plan).

## Evidence and editorial readiness are separate

| Evidence value | Meaning |
| --- | --- |
| `open` | A question or protocol awaiting results. |
| `exploratory` | An observation with limited checks or unresolved robustness. |
| `replicated` | An experiment repeated under the controls described in the note; not a universal theorem or a claim of external replication. |
| `exact` | An algebraic derivation or exhaustive computation, with its domain and bounds stated. |
| `superseded` | A retained record whose current account is another registered note; set `supersededBy` to that note's slug. |
| `state` | A checkpoint: a dated statement of state with no new evidence. Only valid with `"recordType": "checkpoint"`. |

A note can contain claims with different strengths. Choose the label for its
central result and qualify individual claims in the body. An exact result can
remain specialist material; an open question can deserve an accessible
explanation. Promotion does not upgrade the evidence label.

| Promotion stage | Fields | Effect |
| --- | --- | --- |
| `research` | `stage` | The note stays in the research record. |
| `candidate` | `stage`, `idea`, `destination` | Its proposed explanation appears in “To explain next” on the index. Destination is Home, Concepts, Questions, or The Walk. |
| `promoted` | `stage`, `title`, `href` | The note links to an existing explanation, such as `concepts.html#commutator`. |

## Periodically promote an insight

At a useful research milestone, review the index's **To explain next** list.
Ask whether each idea is useful to a newcomer, whether its evidence and limits
can be explained honestly, and where it fits in the site's existing story.
There is no automatic evidence threshold or scheduled publishing process.

Write a short, accessible explanation in the selected main page, using an
example or live demo when it helps. Give the explanation a stable anchor and
link it to the research note for details. Then change the note's promotion
record to `promoted`, pointing back to that explanation. Keep the original
note, methods, and result files in place. The affine-converse correction is
the first example of this connection; the snapshot/history result is queued
as a candidate for Questions.

Correct false claims in the main content when discovered; do not wait for a
larger editorial pass. Record what changed and why in Research.

## Integrate a research unit through a gathering PR

Follow the canonical [gathering-branch workflow](../../AGENTS.md#gathering-branches-and-review).
A draft `gather/<unit>` PR into `main` carries the unit's scope and completion
criteria. Small sub-PRs target that branch and may be self-merged after
self-review and relevant checks. Integration into the gathering branch does
not publish a result on `main`.

Myk retired the standing cross-agent review gates on 2026-09-22. Freeze a
protocol before implementation and evaluation, and record any later material
change as a deviation. Previously observed outcomes must remain labeled
exploratory or post hoc. Myk asks for review case by case; a requested review
names its reviewer, pins the current head SHA and states its scope. Merge into
`main` at Myk's direction.

Result files are guarded in two tiers. Every pull request touching an audit
runs a fast check that recomputes the SHA-256 hashes each canonical JSON
records for its verifier and inputs (`scripts/check_result_integrity.py`);
this proves provenance coherence, not result content.

Keep automatic CI cost-bounded. A scientific evaluation or full replay expected
or observed to exceed about ten minutes does **not** run automatically on pull
requests, pushes to `main`, or schedules. Generate the canonical result once
outside GitHub Actions from the pinned implementation and record that execution;
perform required independent full replays outside Actions during author/reviewer
verification. Expensive `workflow_dispatch` jobs are emergency/manual escape
hatches only and require Myk's explicit authorization to spend Actions time.
Short byte-for-byte replays that fit comfortably inside the ten-minute CI budget
may remain automatic. Existing expensive workflows must be converted before
their next execution; already-running jobs from before this policy may finish
but are not automatically rerun. Register every new result file in the integrity
script and document both the fast automatic tier and the off-CI full-replay path.

The gathering PR lists sub-PRs and issue closure references. Notes and
protocols retain their own authorship/review provenance, distinguishing
pre-evaluation and retrospective review. Update the Program, dependent
knowledge entries and checkpoint when applicable; a checkpoint must not
describe work as reviewed or accepted before that has happened.
Preserve original protocols and datasets when correcting a completed run.

### Multiple collaborating agents

Several agents contribute to this repository. When Myk asks one agent to
review another's work, the reviewer must not have authored the contribution it
reviews. For jointly authored work, record contribution boundaries.

A collaborator may introduce a new research Program through a normal gathering
PR. The proposal should make the research question or thesis legible, situate
it relative to the existing Programs without assuming it belongs to one of
them, state scope and non-claims, sketch the initial research agenda, name its
owner(s), and add the Program/checkpoint registration
when the proposal is accepted. A distinct outside perspective is allowed to
remain a distinct Program; conceptual overlap alone is not grounds to collapse
it into an existing line.

Agents may share a GitHub account, so provenance is semantic rather than tied to
GitHub username. Sign substantive PR comments/reviews with agent/model/session
identity and date, and pin reviews to the exact head SHA and scope. Branch names,
PR context, commit authorship and signed comments together identify who authored
and who reviewed a unit.

## Authorship and review

Notes, checkpoints, and frozen protocols carry a short provenance line near the
top, after the title and status:

```
Authored by: <person or agent session>. Reviewed by: <person or agent session>, <date>.
```

Name agents by their signed identity as used in issues (for example
"Codex (OpenAI)" or "Claude Code, Fable 5.1") and people by name. Work without
review says `Reviewed by: none`; since 2026-09-22 that is the normal state and
does not block evaluation. When Myk requests review of a frozen protocol before
evaluation, record the reviewer, date and reviewed revision on the protocol and
link the thread or PR. A review after evaluation is retrospective; never
present it as pre-run approval. Existing notes are not edited retroactively;
add the line when a note is next revised.

## Formatting, evidence links, and revisions

- Use ordinary Markdown, fenced code blocks, and tables. Raw HTML is displayed
  as text. Equations support `\( ... \)`, `\[ ... \]`, `$ ... $` (without
  spaces beside the delimiters), and `$$ ... $$`. Invalid TeX fails the build.
- Relative links are resolved from the Markdown file. Links to another
  registered note become local Research links; links to scripts, data,
  archives, and other repository files open on GitHub. CI pins those source
  links to the commit being deployed. Missing local files fail the build.
- Local images use paths such as `../../results/figure.svg`; supported types
  are SVG, PNG, JPEG, GIF, and WebP. Give figures useful alternative text.
  Wide tables and display equations scroll within the article on small screens.
- Keep published slugs and section headings stable when other pages link to
  them. Catalog references and promoted main-page anchors are validated during
  the build. External URLs and arbitrary fragment links are not fetched or
  validated; check those when adding them.
- For a small correction, add a dated revision paragraph and update `updated`.
  For a materially different conclusion, publish a new note and mark the old
  one `superseded`, with `supersededBy` pointing to its replacement. Preserve
  original datasets and archived conversation files instead of silently
  rewriting the evidence.

`site/scripts/research-program.mjs` owns the Program/records publishing model
and reuses the Markdown primitives in `site/scripts/research.mjs`.
`site/src/styles/research.css` owns the established Research styling;
`site/src/styles/research-program.css` adds the Program layer. All pages share
the navigation entries in `site/src/data/navigation.js`.
