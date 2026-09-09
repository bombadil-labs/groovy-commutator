/** Extended Research publisher: Program + chronological records + Knowledge.
 *
 * The original research.mjs remains the low-level Markdown/rendering primitive
 * and legacy note builder. This module owns the richer publishing model as the
 * section grows beyond a numbered lab notebook.
 */
import fs from 'node:fs';
import path from 'node:path';
import {
  SITE, ROOT, EVIDENCE, esc, dateLabel, repoUrl, renderMarkdown, sourceRef, layout as legacyLayout,
  validateCatalog as validateLegacyCatalog, researchWatch,
} from './research.mjs';

export { researchWatch };
export const CATALOG = path.join(SITE, 'content/research.json');
export const CATALOG_DIR = path.join(SITE, 'content/research');
export const PROGRAM = path.join(SITE, 'content/research-program.json');

const entryUrl = (entry) => `${entry.slug}.html`;

export function catalogFiles() {
  const shards = fs.existsSync(CATALOG_DIR)
    ? fs.readdirSync(CATALOG_DIR).filter((name) => name.endsWith('.json')).sort().map((name) => path.join(CATALOG_DIR, name))
    : [];
  return [CATALOG, ...shards];
}

export function readResearchRecords() {
  return catalogFiles().flatMap((file) => JSON.parse(fs.readFileSync(file, 'utf8')));
}

export function validateRecords(records) {
  // Reuse the established evidence/promotion/link contract. A checkpoint is
  // deliberately unnumbered in the public model, so give the legacy validator
  // a synthetic identity only for validation.
  const normalized = records.map((entry) => entry.recordType === 'checkpoint'
    ? { ...entry, number: `checkpoint-${entry.slug}` }
    : entry);
  validateLegacyCatalog(normalized);
  const checkpointLabels = new Set();
  for (const entry of records) {
    const type = entry.recordType || 'note';
    if (!['note', 'checkpoint'].includes(type)) throw new Error(`Research: unknown record type in ${entry.slug}`);
    if (type === 'checkpoint') {
      if (typeof entry.label !== 'string' || !entry.label.trim()) throw new Error(`Research: checkpoint needs a label in ${entry.slug}`);
      if (checkpointLabels.has(entry.label)) throw new Error(`Research: duplicate checkpoint label ${entry.label}`);
      checkpointLabels.add(entry.label);
    }
  }
  return records;
}

export function validateProgram(program, records) {
  if (!program || typeof program !== 'object') throw new Error('Research: program metadata must be an object');
  for (const field of ['title', 'eyebrow', 'date', 'updated', 'status', 'summary', 'thesis', 'source']) {
    if (typeof program[field] !== 'string' || !program[field].trim()) throw new Error(`Research: missing program ${field}`);
  }
  if (!['living', 'stable', 'superseded'].includes(program.status)) throw new Error('Research: unknown program status');
  if (!Array.isArray(program.supports) || !program.supports.length) throw new Error('Research: program needs supporting records');
  const slugs = new Set(records.map((entry) => entry.slug));
  for (const slug of program.supports) if (!slugs.has(slug)) throw new Error(`Research: unknown program support ${slug}`);
  const source = path.resolve(ROOT, program.source);
  if (!source.startsWith(ROOT + path.sep) || !fs.existsSync(source)) throw new Error(`Research: missing program source ${program.source}`);
  return program;
}

function layout(title, description, content, { section = 'notes' } = {}) {
  let html = legacyLayout(title, description, content, { section: section === 'program' ? 'notes' : section });
  html = html.replace(
    '<link rel="stylesheet" href="../src/styles/tokens.css"><link rel="stylesheet" href="../src/styles/research.css">',
    '<link rel="stylesheet" href="../src/styles/tokens.css"><link rel="stylesheet" href="../src/styles/research.css"><link rel="stylesheet" href="../src/styles/research-program.css">',
  );
  const current = (name) => section === name ? ' aria-current="page"' : '';
  html = html.replace(/<nav class="research-sections" aria-label="Research navigation">[\s\S]*?<\/nav>/, `<nav class="research-sections" aria-label="Research navigation">
<a href="program.html"${current('program')}>Program</a>
<a href="index.html"${current('notes')}>Notes</a>
<a href="knowledge/index.html"${current('knowledge')}>Knowledge</a>
</nav>`);
  return html;
}

function badge(entry) { return `<span class="research-status ${entry.evidence}">${EVIDENCE[entry.evidence]}</span>`; }
function promotion(entry) {
  const p = entry.promotion;
  if (p.stage === 'promoted') return `<a class="research-promotion" href="../${esc(p.href)}">${esc(p.title)} →</a>`;
  if (p.stage === 'candidate') return '<span class="research-promotion">Candidate for an explainer</span>';
  return '<span class="research-promotion">Research only</span>';
}
function railLabel(entry) { return entry.recordType === 'checkpoint' ? '◆' : entry.number; }
function publicLabel(entry) { return entry.recordType === 'checkpoint' ? entry.label : `Note ${entry.number}`; }

function renderIndex(records, program) {
  const candidates = records.filter((entry) => entry.promotion.stage === 'candidate');
  const topics = [...new Set(records.map((entry) => entry.topic))];
  const rows = records.map((entry) => `<article class="research-entry">
    <span class="research-number" aria-hidden="true">${esc(railLabel(entry))}</span><div>
    <div class="research-meta"><time datetime="${entry.date}">${dateLabel(entry.date)}</time><span>${esc(entry.kind)}</span><span>${esc(entry.topic)}</span></div>
    <h3><a href="${entryUrl(entry)}">${esc(entry.title)}</a></h3><p>${esc(entry.summary)}</p>
    <div class="research-entry-foot">${badge(entry)}${promotion(entry)}</div></div></article>`).join('');
  return layout('Research', 'The living program, chronological research record, and knowledge base of the Groovy Commutator project.', `
    <p class="research-kicker">The working record</p><h1 class="research-heading">Research</h1>
    <p class="research-intro">The project now keeps three layers here: a living Program that compresses the current theory, chronological Notes and checkpoints that preserve how the evidence developed, and a Knowledge base of smaller reusable claims.</p>
    <section class="research-program-feature" aria-labelledby="program-feature-title">
      <p class="research-kicker">${esc(program.eyebrow)}</p><h2 id="program-feature-title"><a href="program.html">${esc(program.title)}</a></h2>
      <p>${esc(program.summary)}</p>
      <div class="research-entry-foot"><span class="research-status program-living">${esc(program.status === 'living' ? 'Living synthesis' : program.status)}</span><span>Updated ${dateLabel(program.updated)}</span><a href="program.html">Read the current program →</a></div>
    </section>
    <div class="research-layout"><section aria-labelledby="notes"><h2 id="notes" class="research-section-title">Research notes and checkpoints · ${records.length} records</h2>${rows}</section>
    <aside class="research-sidebar" aria-label="About the research">
      <section><h2>Program, notes, knowledge</h2><p>The Program says what the project currently thinks. Notes retain protocols, negative results, and corrections. Knowledge extracts compact claims without erasing their evidence trail.</p><a href="program.html">Read the Program →</a></section>
      <section><h2>From research to explanation</h2><p>The main pages remain the accessible entrance to the original calculus and instruments. Research is no longer only a staging area for them; some mature technical ideas belong here as a living program.</p><a href="../questions.html">Explore the questions →</a></section>
      <section id="to-explain"><h2>To explain next</h2>${candidates.length ? `<ul>${candidates.map((entry) => `<li><a href="${entryUrl(entry)}">${esc(entry.promotion.idea)}</a><small>Candidate for ${esc(entry.promotion.destination)}</small></li>`).join('')}</ul>` : '<p>No explanations are queued.</p>'}<p>Editorial readiness is separate from the strength of the evidence.</p></section>
      <section><h2>Threads</h2><ul>${topics.map((topic) => `<li>${esc(topic)}<small>${records.filter((entry) => entry.topic === topic).length} records</small></li>`).join('')}</ul></section>
    </aside></div>`);
}

function renderProgram(program, records, context) {
  const source = path.resolve(ROOT, program.source);
  const { body, headings, minutes } = renderMarkdown(source, context);
  const supports = program.supports.map((slug) => records.find((entry) => entry.slug === slug));
  return layout(program.title, program.summary, `<article class="research-article research-program-article">
    <a class="research-back" href="index.html">← Research notes</a>
    <div class="research-meta"><span>${esc(program.eyebrow)}</span><time datetime="${program.date}">${dateLabel(program.date)}</time><span>${minutes} min read</span><span>Updated ${dateLabel(program.updated)}</span></div>
    <h1 class="research-heading">${esc(program.title)}</h1><p class="research-summary">${esc(program.summary)}</p>
    <div class="research-article-status"><span class="research-status program-living">${esc(program.status === 'living' ? 'Living synthesis' : program.status)}</span></div>
    <p class="research-takeaway"><strong>Current thesis</strong>${esc(program.thesis)}</p>
    ${headings.length ? `<details class="research-toc"><summary>In this program</summary><ul>${headings.map((h) => `<li><a href="#${h.id}">${esc(h.text)}</a></li>`).join('')}</ul></details>` : ''}
    <div class="research-prose">${body}</div>
    <p class="research-source"><a href="${esc(repoUrl(program.source, context.ref))}">Source synthesis and revision history</a></p>
    <section class="research-related"><h2>Evidence lineage</h2><p>This synthesis is supported by the records below. Mixed evidence strengths and open boundaries remain stated in the source records.</p><ul>${supports.map((entry) => `<li><a href="${entryUrl(entry)}">${esc(entry.title)}</a> <span class="kb-inline-kind">${esc(publicLabel(entry))}</span></li>`).join('')}</ul></section>
  </article>`, { section: 'program' });
}

function patchKnowledgeNavigation(output) {
  const knowledgeDir = path.join(output, 'knowledge');
  if (!fs.existsSync(knowledgeDir)) return;
  for (const name of fs.readdirSync(knowledgeDir)) {
    if (!name.endsWith('.html')) continue;
    const file = path.join(knowledgeDir, name);
    let html = fs.readFileSync(file, 'utf8');
    html = html.replace(/<nav class="research-sections" aria-label="Research navigation">[\s\S]*?<\/nav>/, `<nav class="research-sections" aria-label="Research navigation">
<a href="../program.html">Program</a>
<a href="../index.html">Notes</a>
<a href="../knowledge/index.html" aria-current="page">Knowledge</a>
</nav>`);
    fs.writeFileSync(file, html);
  }
}

export function buildResearchProgram({ records: suppliedRecords, program: suppliedProgram, knowledge = [], output = path.join(SITE, 'research') } = {}) {
  const records = validateRecords(suppliedRecords ?? readResearchRecords())
    .sort((a, b) => b.updated.localeCompare(a.updated) || String(a.recordType === 'checkpoint' ? `zz-${a.label}` : a.number).localeCompare(String(b.recordType === 'checkpoint' ? `zz-${b.label}` : b.number)));
  const program = validateProgram(suppliedProgram ?? JSON.parse(fs.readFileSync(PROGRAM, 'utf8')), records);
  fs.mkdirSync(output, { recursive: true });
  for (const file of fs.readdirSync(output)) if (file.endsWith('.html')) fs.unlinkSync(path.join(output, file));

  const ref = sourceRef();
  const bySource = new Map([[path.resolve(ROOT, program.source), 'program.html'], ...records.map((entry) => [path.resolve(ROOT, entry.source), entryUrl(entry)]), ...knowledge.map((node) => [path.resolve(ROOT, node.source), `knowledge/${node.id}.html`])]);
  const dependencies = new Set([...catalogFiles(), PROGRAM]);
  const context = { bySource, ref, output, dependencies };
  const inputs = { research: path.join(output, 'index.html'), 'research-program': path.join(output, 'program.html') };

  fs.writeFileSync(inputs.research, renderIndex(records, program));
  fs.writeFileSync(inputs['research-program'], renderProgram(program, records, context));
  for (const entry of records) {
    const source = path.resolve(ROOT, entry.source);
    const { body, headings, minutes } = renderMarkdown(source, context);
    const replacement = entry.supersededBy && records.find((other) => other.slug === entry.supersededBy);
    const concepts = knowledge.filter((node) => node.research.includes(entry.slug));
    const related = entry.related.map((slug) => records.find((other) => other.slug === slug));
    const html = layout(entry.title, entry.summary, `<article class="research-article">
      <a class="research-back" href="index.html">← All research</a>
      <div class="research-meta"><span>${esc(publicLabel(entry))} · ${esc(entry.kind)}</span><time datetime="${entry.date}">${dateLabel(entry.date)}</time><span>${minutes} min read</span></div>
      <h1 class="research-heading">${esc(entry.title)}</h1><p class="research-summary">${esc(entry.summary)}</p>
      <div class="research-article-status">${badge(entry)}${promotion(entry)}</div>
      ${replacement ? `<div class="research-correction">This record has been superseded. Continue with <a href="${entryUrl(replacement)}">${esc(replacement.title)}</a>.</div>` : ''}
      <p class="research-takeaway"><strong>The idea</strong>${esc(entry.takeaway)}</p>
      ${headings.length ? `<details class="research-toc"><summary>In this record</summary><ul>${headings.map((h) => `<li><a href="#${h.id}">${esc(h.text)}</a></li>`).join('')}</ul></details>` : ''}
      <div class="research-prose">${body}</div>
      <p class="research-source"><a href="${esc(repoUrl(entry.source, ref))}">Source record and revision history</a></p>
      ${concepts.length ? `<section class="research-related"><h2>In the knowledge base</h2><ul>${concepts.map((node) => `<li><a href="knowledge/${node.id}.html">${esc(node.title)}</a> <span class="kb-inline-kind">${esc(node.kind)}</span></li>`).join('')}</ul></section>` : ''}
      ${related.length ? `<section class="research-related"><h2>Continue the thread</h2><ul>${related.map((other) => `<li><a href="${entryUrl(other)}">${esc(other.title)}</a></li>`).join('')}</ul></section>` : ''}
    </article>`);
    const file = path.join(output, entryUrl(entry));
    fs.writeFileSync(file, html);
    inputs[`research-${entry.slug}`] = file;
  }
  patchKnowledgeNavigation(output);
  return { inputs, dependencies: [...dependencies] };
}
