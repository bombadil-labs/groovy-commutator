# Writing research, then explaining it

Research is the public working scientific record. It now has three layers:

1. **Program** — a living synthesis of what the project currently thinks, with
   exact results and open proof boundaries stated together.
2. **Notes and checkpoints** — the chronological lab record: protocols,
   experiments, corrections, failed predictions, and bounded claims.
3. **Knowledge** — compact reusable findings and relationships extracted from
   the record without erasing their evidence trail.

The main React pages remain an accessible route into the original calculus and
instruments. Promotion to those pages is still useful when an idea deserves a
newcomer-facing explanation, but Research is no longer only a staging area for
main-site content. Some mature technical ideas belong in the Program itself.

The [knowledge base](../knowledge/README.md) keeps the current account of
individual findings, questions, theories, and experiments, with typed
relationships and dependency paths. After a substantial research checkpoint,
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

## Keep the Program's continuation log

Each Program has a dated continuation log in `docs/research/continuations/`
(one file per Program, plus `lab.md` for cross-program checkpoints). When a
substantial unit completes, add a section at the top of the relevant file:
what was completed, what is frozen and unrun, and what not to infer. The logs
are read by agent sessions before continuing a workstream; `AGENTS.md` points
at them. A new Program gets a new file when it is registered.

## Add a research note or checkpoint

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
   number. A deliberately unnumbered research checkpoint may instead use
   `"recordType": "checkpoint"` plus a short `label`. The catalog title,
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
checkpoints follow numbered notes from the same update date. Keep the original
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

## Authorship and review

Notes, checkpoints, and frozen protocols carry a short provenance line near the
top, after the title and status:

```
Authored by: <person or agent session>. Reviewed by: <person or agent session>, <date>.
```

Name agents by their signed identity as used in issues (for example
"Codex (OpenAI)" or "Claude Code, Fable 5.1") and people by name. For a frozen
protocol the review happens **before** the implementation commit and before any
evaluation; record the reviewer and date on the protocol itself, and link the
issue thread or PR where the review took place. A note with no reviewer says
`Reviewed by: none` rather than omitting the line. Existing notes are not
edited retroactively; add the line when a note is next revised.

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
