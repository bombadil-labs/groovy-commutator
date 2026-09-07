# Maintaining the knowledge base

The knowledge base is the current account of individual concepts, findings,
questions, theories, and experiments. Research notes preserve the dated path
through the work. Main pages provide accessible explanations. Keep these
connected without copying the full research narrative into every entry.

## Add or update an entry

Write a short Markdown file in `docs/knowledge/` and register it as a node in
`site/content/knowledge.json`. Start with a single `#` title. State the current
claim or question, its scope and limits, and what would change the account.
Link to registered research notes for the full methods and evidence. A research
plan is a valid source for an open question; linking it does not make it evidence
of a result. Add a dated revision paragraph when the conclusion changes.

Each node has a stable `id`, `title`, `kind`, `status`, plain-language `summary`,
`updated` date, Markdown `source`, and a nonempty `research` array of note slugs.
Its URL is `/groovy-commutator/research/knowledge/<id>.html`. IDs, source files,
and URLs are unique. Do not change a published ID or remove a refuted idea just
because its conclusion changed.

| Kind | Allowed status values |
| --- | --- |
| `concept` | `defined` |
| `finding` | `exact`, `replicated`, `exploratory`, `superseded` |
| `question` | `open`, `partly-answered`, `answered` |
| `theory` | `proposed`, `supported`, `refuted`, `superseded` |
| `experiment` | `planned`, `completed` |

`exact` requires stated mathematical or enumeration bounds. `replicated` means
the repeated experiment described in the source, not necessarily independent
external replication. `supported` is not a synonym for proven; `completed`
does not imply a successful result. Record the qualifications in the body.

Example node (replace example values with the actual entry):

```json
{
  "id": "a-new-question",
  "title": "A specific question?",
  "kind": "question",
  "status": "open",
  "summary": "What remains uncertain and why it matters.",
  "updated": "2026-09-08",
  "source": "docs/knowledge/a-new-question.md",
  "research": ["history-repairability"]
}
```

## Record a semantic relationship once

Edges are directed triples, with an explicit reason and research provenance.
Read every edge as **source → relation → target**. A plain Markdown link is
navigation; it does not create a semantic edge. Use the `edges` array to make
a relationship available to backlinks, dependency traversal, and export.

```json
{
  "source": "nonlinear-zero",
  "type": "contradicts",
  "target": "affine-converse",
  "reason": "A nonlinear rule with constant zero commutator is an exact counterexample to the converse.",
  "research": ["affine-converse"]
}
```

| Relation | Meaning of A → B | Backlink on B |
| --- | --- | --- |
| `depends_on` | A relies on B as a premise, definition, or experimental setup. | Required by A |
| `supports` | Finding or completed experiment A provides scoped evidence for finding or theory B. | Supported by A |
| `contradicts` | Finding or completed experiment A provides scoped counterevidence to finding or theory B. | Contradicted by A |
| `tests` | Experiment A investigates question, theory, or finding B. A planned test supplies no result. | Tested by A |

The rationale must explain the particular relationship and its limits. Do not
infer support from shared keywords. A single pair can have distinct relations
(a finding may both depend on and receive support from another finding); an
identical source/type/target triple is stored only once. Backlinks are generated
automatically, so never add a duplicate inverse edge.

Only `depends_on` is treated as a prerequisite relation. Its graph must be
acyclic. Other relation cycles are allowed, but mutual support does not amount
to proof. Add a new relation vocabulary only when needed, with a precise
direction, inverse label, validation rules, and documentation in
`site/scripts/knowledge.mjs`.

## Review dependencies when a claim changes

“What relies on this?” follows incoming `depends_on` edges to list direct and
indirect dependents, showing one shortest path for each. It is a review aid;
not every consequence of a result will have been recorded. Support and
contradiction links appear separately and do not become dependencies implicitly.

When a prerequisite is refuted or superseded, dependent pages show a review
notice, including indirect paths. The system does not change their statuses
automatically. Inspect the rationale, repeat affected checks where necessary,
and update the relevant entries and research notes. A proposed or exploratory
premise also warrants judgment even though it does not trigger this notice.

Use `refuted` to retain a rejected theory and its counterevidence. Use
`superseded` for a finding or theory replaced by a new entry, setting
`supersededBy` to its ID. Replacement chains must also be acyclic. Keep old
evidence files intact and write an explicit revision note. For a correction
affecting a main-page explanation, follow the Research promotion guide and
correct that explanation promptly.

## Validate and publish

From the repository root:

```bash
npm run test:research --prefix site
npm run build --prefix site
```

The build validates IDs, kinds/statuses, sources, provenance references,
relationship endpoints/types, duplicate edges, dependency cycles, replacements,
Markdown evidence links, and equations. It creates the index, each entry,
backlinks to research notes, and a stable `research/knowledge/graph.json` export.
The export includes schema version 1, node and edge records, relation meanings,
allowed kinds/statuses, local page URLs, and source URLs pinned to the deployed
commit in CI. URLs in the export are relative to the export's directory.

The site is edited through repository files, including through the Bombadil
Labs MCP. The public pages provide browsing and a searchable index; they do
not contain a browser editor. Git preserves the revision history. Generated
files under `site/research/` and repo-root `public/` are not committed.
Changes to `docs/knowledge/` trigger the existing main-branch Pages workflow.

Research notes automatically link back to the knowledge entries that cite them.
Markdown links to registered entries and research notes resolve to their public
pages; other repository links open the source files on GitHub. External URLs
and arbitrary fragments still require author review.
