# Writing research, then explaining it

Research is the public working record. The main site is an accessible route
into the ideas. Keep a finding's full methods and qualifications in a research
note, then give selected insights their own explanation in the main pages.
Both remain available and link to each other.

The [knowledge base](../knowledge/README.md) keeps the current account of
individual findings, questions, theories, and experiments, with typed
relationships and dependency paths. After a substantial research checkpoint,
update the relevant knowledge entries and their relationships. Cite the note
from each entry; the site generates links back in both directions.

## Add a research note

1. Write `docs/research/YYYY-MM-DD-short-name.md`. Start with a single `#`
   title, then use `##` sections. Lead with the question and a plain-language
   answer, or say explicitly that the experiment has not been run.
2. Record the setup, definitions, evidence, limits, and next question. Link to
   reproducible scripts and saved results; include seeds, sizes, parameters,
   and uncertainty where relevant. Distinguish measured results, exact claims,
   and interpretation. Preserve negative results and failed conjectures.
3. Add an entry to `site/content/research.json` using the next unused note
   number. The catalog title, summary, and takeaway are the accessible entrance
   to the longer note. Choose a stable slug; its public path is
   `/groovy-commutator/research/<slug>.html`.
4. Validate and build from the repository root:

   ```bash
   npm ci --prefix site
   npm run test:research --prefix site
   npm run build --prefix site
   ```

No page component or route list needs editing. Vite generates the index and
all registered notes, renders equations at build time, and bundles local
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

The index orders notes by most recent update, then note number. Keep the
original publication date and update `updated` when the substance changes.
Use existing topic names when continuing a thread. `kind` describes the
document (for example Experiment, Correction, or Research plan).

## Evidence and editorial readiness are separate

| Evidence value | Meaning |
| --- | --- |
| `open` | A question or protocol awaiting results. |
| `exploratory` | An observation with limited checks or unresolved robustness. |
| `replicated` | An experiment repeated under the controls described in the note; not a universal theorem or a claim of external replication. |
| `exact` | An algebraic derivation or exhaustive computation, with its domain and bounds stated. |
| `superseded` | A retained record whose current account is another registered note; set `supersededBy` to that note's slug. |

A note can contain claims with different strengths. Choose the label for its
central result and qualify individual claims in the body. An exact result
can remain specialist material; an open question can deserve an accessible
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

`site/scripts/research.mjs` owns rendering and catalog validation.
`site/src/styles/research.css` owns Research styling. All pages share the
navigation entries in `site/src/data/navigation.js`.
