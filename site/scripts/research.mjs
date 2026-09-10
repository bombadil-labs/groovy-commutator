/** Render repository Markdown into static, shareable Research pages.
 * Vite consumes the generated HTML and bundles the CSS, fonts, and figures.
 * Authored files live in docs/research + site/content/research.json, never in
 * the generated site/research directory. No renderer is shipped to readers.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import MarkdownIt from 'markdown-it';
import texmath from 'markdown-it-texmath';
import katex from 'katex';
import { PAGES } from '../src/data/navigation.js';

export const SITE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
export const ROOT = path.dirname(SITE);
export const CATALOG = path.join(SITE, 'content/research.json');
export const EVIDENCE = {
  open: 'Open question', exploratory: 'Exploratory', replicated: 'Replicated experiment',
  exact: 'Exact within stated bounds', superseded: 'Superseded',
  state: 'Checkpoint · state, no new evidence',
};
const STAGES = ['research', 'candidate', 'promoted'];
export const esc = (x) => String(x).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
export const requireValue = (condition, message) => { if (!condition) throw new Error(`Research: ${message}`); };
export const dateLabel = (s) => new Intl.DateTimeFormat('en-GB', { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC' }).format(new Date(`${s}T00:00:00Z`));
const entryUrl = (entry) => `${entry.slug}.html`;

export function existingRepoPath(relative, label) {
  const absolute = path.resolve(ROOT, relative);
  requireValue(absolute.startsWith(ROOT + path.sep) && fs.existsSync(absolute), `missing or invalid ${label}: ${relative}`);
  requireValue(fs.realpathSync(absolute).startsWith(fs.realpathSync(ROOT) + path.sep), `external symlink in ${label}`);
  return absolute;
}

export function validateCatalog(entries) {
  requireValue(Array.isArray(entries) && entries.length > 0, 'catalog must contain entries');
  const slugs = new Set();
  const numbers = new Set();
  const sources = new Set();
  for (const e of entries) {
    for (const field of ['slug', 'number', 'title', 'date', 'updated', 'kind', 'evidence', 'topic', 'summary', 'takeaway', 'source']) {
      requireValue(typeof e[field] === 'string' && e[field].trim(), `missing ${field} in ${e.slug || 'entry'}`);
    }
    requireValue(/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(e.slug) && e.slug !== 'index', `invalid slug ${e.slug}`);
    requireValue(!slugs.has(e.slug) && !numbers.has(e.number) && !sources.has(e.source), `duplicate slug, number, or source in ${e.slug}`);
    slugs.add(e.slug); numbers.add(e.number); sources.add(e.source);
    for (const date of [e.date, e.updated]) {
      requireValue(/^\d{4}-\d{2}-\d{2}$/.test(date) && !Number.isNaN(Date.parse(date)) && new Date(date).toISOString().slice(0, 10) === date, `invalid date in ${e.slug}`);
    }
    requireValue(e.updated >= e.date, `updated precedes publication in ${e.slug}`);
    requireValue(Object.hasOwn(EVIDENCE, e.evidence), `unknown evidence label in ${e.slug}`);
    requireValue(STAGES.includes(e.promotion?.stage), `unknown promotion stage in ${e.slug}`);
    requireValue(e.source.startsWith('docs/research/') && e.source.endsWith('.md'), `source must be research Markdown in ${e.slug}`);
    existingRepoPath(e.source, 'note');
    if (e.promotion.stage === 'candidate') {
      requireValue(e.promotion.idea && ['Home', 'Concepts', 'Questions', 'The Walk'].includes(e.promotion.destination), `candidate needs an idea and destination in ${e.slug}`);
    }
    if (e.promotion.stage === 'promoted') {
      const href = e.promotion.href;
      requireValue(typeof href === 'string' && /^(index|concepts|questions|remainder)\.html(?:#[a-z0-9-]+)?$/.test(href), `invalid explainer link in ${e.slug}`);
      requireValue(e.promotion.title, `promoted note needs a link title in ${e.slug}`);
      const [file, anchor] = href.split('#');
      const page = { 'index.html': 'Home', 'concepts.html': 'Concepts', 'questions.html': 'Questions', 'remainder.html': 'Remainder' }[file];
      if (anchor) {
        const component = fs.readFileSync(path.join(SITE, 'src/components', `${page}.jsx`), 'utf8');
        requireValue(component.includes(`id="${anchor}"`), `missing explainer anchor ${href}`);
      }
    }
  }
  for (const e of entries) {
    requireValue(Array.isArray(e.related), `related must be an array in ${e.slug}`);
    for (const slug of [...e.related, ...(e.supersededBy ? [e.supersededBy] : [])]) {
      requireValue(slugs.has(slug) && slug !== e.slug, `unknown or self reference ${slug} in ${e.slug}`);
    }
    requireValue(e.evidence !== 'superseded' || e.supersededBy, `superseded note needs a replacement in ${e.slug}`);
  }
  return entries;
}

export function sourceRef() {
  if (process.env.GITHUB_SHA) return process.env.GITHUB_SHA;
  try { return execFileSync('git', ['branch', '--show-current'], { cwd: ROOT, encoding: 'utf8' }).trim() || 'main'; }
  catch { return 'main'; }
}

export function repoUrl(relative, ref, fragment = '') {
  return `https://github.com/bombadil-labs/groovy-commutator/blob/${ref.split('/').map(encodeURIComponent).join('/')}/${relative.split(path.sep).map(encodeURIComponent).join('/')}${fragment}`;
}

function nav(prefix) {
  return `<header class="gc-header"><nav class="gc-nav" aria-label="Main navigation">
    <a href="${prefix}index.html" class="gc-nav-brand" style="font-family:'Lora',serif">Groovy Commutator</a>
    <div class="gc-nav-links">${PAGES.map((p) => `<a href="${prefix}${p.href}" class="gc-nav-link${p.key === 'research' ? ' active' : ''}"${p.key === 'research' ? ' aria-current="page"' : ''}>${p.label}</a>`).join('')}</div>
  </nav></header>`;
}

export function layout(title, description, content, { depth = 1, section = 'notes', script = '' } = {}) {
  const prefix = '../'.repeat(depth);
  const researchPrefix = '../'.repeat(depth - 1);
  return `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)} — Groovy Commutator</title><meta name="description" content="${esc(description)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=IBM+Plex+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="${prefix}src/styles/tokens.css"><link rel="stylesheet" href="${prefix}src/styles/research.css">
<link rel="stylesheet" href="${prefix}node_modules/katex/dist/katex.min.css">
</head><body class="research-page"><a class="research-skip" href="#main">Skip to content</a>${nav(prefix)}
<main id="main" class="research-shell"><nav class="research-sections" aria-label="Research navigation">
<a href="${researchPrefix}index.html"${section === 'notes' ? ' aria-current="page"' : ''}>Research notes</a>
<a href="${researchPrefix}knowledge/index.html"${section === 'knowledge' ? ' aria-current="page"' : ''}>Knowledge base</a>
</nav>${content}</main>
<footer class="gc-footer"><div class="gc-footer-inner">An ongoing investigation. <a href="${researchPrefix}index.html">Research index</a> · <a href="${prefix}concepts.html">Start with the concepts</a> · <a href="https://github.com/bombadil-labs/groovy-commutator">Source and data</a></div></footer>
${script ? `<script type="module" src="${prefix}${script}"></script>` : ''}
</body></html>`;
}

function badge(e) { return `<span class="research-status ${e.evidence}">${EVIDENCE[e.evidence]}</span>`; }
function promotion(e) {
  const p = e.promotion;
  if (p.stage === 'promoted') return `<a class="research-promotion" href="../${esc(p.href)}">${esc(p.title)} →</a>`;
  if (p.stage === 'candidate') return '<span class="research-promotion">Candidate for an explainer</span>';
  return '<span class="research-promotion">Research only</span>';
}

function renderIndex(entries) {
  const program = entries.find((e) => e.slug === 'history-and-possibility');
  const candidates = entries.filter((e) => e.promotion.stage === 'candidate');
  const topics = [...new Set(entries.map((e) => e.topic))];
  const rows = entries.map((e) => `<article class="research-entry">
    <span class="research-number" aria-hidden="true">${esc(e.number)}</span><div>
    <div class="research-meta"><time datetime="${e.date}">${dateLabel(e.date)}</time><span>${esc(e.kind)}</span><span>${esc(e.topic)}</span></div>
    <h3><a href="${entryUrl(e)}">${esc(e.title)}</a></h3><p>${esc(e.summary)}</p>
    <div class="research-entry-foot">${badge(e)}${promotion(e)}</div></div></article>`).join('');
  return layout('Research', 'Experiments, exact results, corrections, and open questions from the Groovy Commutator project.', `
    <p class="research-kicker">The working record</p><h1 class="research-heading">Research</h1>
    <p class="research-intro">Experiments, results, and questions still taking shape. Each note keeps the evidence, the limits, and a way to pick up the thread.</p>
    <div class="research-layout"><section aria-labelledby="notes"><h2 id="notes" class="research-section-title">Research notes · ${entries.length} entries</h2>${rows}</section>
    <aside class="research-sidebar" aria-label="About the research">
      ${program ? `<section><h2>The wider program</h2><p>How does inherited structure enable further activity, and when does it become difficult to revise? Prediction is one part of that question.</p><a href="${entryUrl(program)}">History and possibility →</a></section>` : ''}
      <section><h2>From research to explanation</h2><p>The main pages introduce the ideas. This is where we test them. When an insight is ready, we give it an accessible explanation and keep a link back to the work.</p><a href="../questions.html">Explore the questions →</a></section>
      <section id="to-explain"><h2>To explain next</h2>${candidates.length ? `<ul>${candidates.map((e) => `<li><a href="${entryUrl(e)}">${esc(e.promotion.idea)}</a><small>Candidate for ${esc(e.promotion.destination)}</small></li>`).join('')}</ul>` : '<p>No explanations are queued. The current work remains in the notes.</p>'}<p>Editorial readiness is separate from the strength of the evidence.</p></section>
      <section><h2>Threads</h2><ul>${topics.map((topic) => `<li>${esc(topic)}<small>${entries.filter((e) => e.topic === topic).length} ${entries.filter((e) => e.topic === topic).length === 1 ? 'note' : 'notes'}</small></li>`).join('')}</ul></section>
    </aside></div>`);
}

export function renderMarkdown(source, { bySource, ref, output, dependencies, reservedIds = [] }) {
  dependencies.add(source);
  const mathErrors = [];
  const engine = { renderToString(tex, options) {
    try { return katex.renderToString(tex, options); }
    catch (error) { mathErrors.push(error.message); throw error; }
  } };
  // texmath retains its engine module-wide; reset it on a Vite restart.
  texmath.katex = engine;
  const md = new MarkdownIt({ html: false, linkify: false, typographer: false })
    .use(texmath, { engine, delimiters: ['brackets', 'dollars'], katexOptions: { throwOnError: true, trust: false, strict: 'ignore', output: 'htmlAndMathml' } });
  md.renderer.rules.table_open = () => '<div class="table-scroll" role="region" aria-label="Data table" tabindex="0"><table>\n';
  md.renderer.rules.table_close = () => '</table></div>\n';
  const markdown = fs.readFileSync(source, 'utf8').replace(/^# [^\n]*\n/, '');
  const tokens = md.parse(markdown, {});
  const headings = [];
  const usedIds = new Set(['main', ...reservedIds]);
  function headingId(text) {
    const base = text.toLowerCase().normalize('NFKD').replace(/[^a-z0-9\s-]/g, '').trim().replace(/\s+/g, '-') || 'section';
    let id = base, n = 1;
    while (usedIds.has(id)) id = `${base}-${n++}`;
    usedIds.add(id); return id;
  }
  function localTarget(href) {
    const [file, ...fragment] = href.split('#');
    const absolute = existingRepoPath(path.relative(ROOT, path.resolve(path.dirname(source), decodeURIComponent(file))), 'linked file');
    return { absolute, fragment: fragment.length ? `#${fragment.join('#')}` : '' };
  }
  function transform(token) {
    if (token.type === 'link_open') {
      const href = token.attrGet('href');
      if (href && !/^(?:[a-z][a-z0-9+.-]*:|#|\/)/i.test(href)) {
        const { absolute, fragment } = localTarget(href);
        const linked = bySource.get(absolute);
        token.attrSet('href', linked ? `${linked}${fragment}` : repoUrl(path.relative(ROOT, absolute), ref, fragment));
      }
    }
    if (token.type === 'image') {
      const src = token.attrGet('src');
      if (!/^https?:\/\//i.test(src)) {
        const { absolute } = localTarget(src);
        requireValue(/\.(svg|png|jpe?g|gif|webp)$/i.test(absolute), `unsupported image in ${source}`);
        dependencies.add(absolute);
        const bytes = fs.readFileSync(absolute);
        const name = `${createHash('sha256').update(bytes).digest('hex').slice(0, 12)}-${path.basename(absolute)}`;
        fs.mkdirSync(path.join(output, 'assets'), { recursive: true });
        fs.writeFileSync(path.join(output, 'assets', name), bytes);
        token.attrSet('src', `assets/${name}`);
      }
      token.attrSet('loading', 'lazy');
    }
    for (const child of token.children || []) transform(child);
  }
  for (let i = 0; i < tokens.length; i++) {
    const token = tokens[i];
    requireValue(!(token.type === 'heading_open' && token.tag === 'h1'), `only one top-level title is allowed in ${source}`);
    if (token.type === 'heading_open') {
      const text = tokens[i + 1].content;
      const id = headingId(text); token.attrSet('id', id);
      if (token.tag === 'h2') headings.push({ text, id });
    }
    transform(token);
  }
  mathErrors.length = 0;
  const body = md.renderer.render(tokens, md.options, {});
  requireValue(!mathErrors.length, `invalid math in ${source}: ${mathErrors.join('; ')}`);
  const minutes = Math.max(1, Math.ceil(markdown.split(/\s+/).length / 180));
  return { body, headings, minutes };
}

export function buildResearch({ entries: catalogEntries, knowledge = [], output = path.join(SITE, 'research') } = {}) {
  const entries = validateCatalog(catalogEntries ?? JSON.parse(fs.readFileSync(CATALOG, 'utf8')))
    .sort((a, b) => b.updated.localeCompare(a.updated) || a.number.localeCompare(b.number));
  fs.mkdirSync(output, { recursive: true });
  // Only remove generated HTML. Hand-authored sources are elsewhere.
  for (const file of fs.readdirSync(output)) if (file.endsWith('.html')) fs.unlinkSync(path.join(output, file));
  const ref = sourceRef();
  const bySource = new Map([...entries.map((e) => [path.resolve(ROOT, e.source), entryUrl(e)]), ...knowledge.map((n) => [path.resolve(ROOT, n.source), `knowledge/${n.id}.html`])]);
  const dependencies = new Set([CATALOG]);
  const inputs = { research: path.join(output, 'index.html') };
  fs.writeFileSync(inputs.research, renderIndex(entries));
  for (const e of entries) {
    const source = path.resolve(ROOT, e.source);
    dependencies.add(source);
    const { body, headings, minutes } = renderMarkdown(source, { bySource, ref, output, dependencies });
    const replacement = e.supersededBy && entries.find((x) => x.slug === e.supersededBy);
    const concepts = knowledge.filter((n) => n.research.includes(e.slug));
    const related = e.related.map((slug) => entries.find((x) => x.slug === slug));
    const html = layout(e.title, e.summary, `<article class="research-article">
      <a class="research-back" href="index.html">← All research</a>
      <div class="research-meta"><span>Note ${esc(e.number)} · ${esc(e.kind)}</span><time datetime="${e.date}">${dateLabel(e.date)}</time><span>${minutes} min read</span>${e.updated !== e.date ? `<span>Updated ${dateLabel(e.updated)}</span>` : ''}</div>
      <h1 class="research-heading">${esc(e.title)}</h1><p class="research-summary">${esc(e.summary)}</p>
      <div class="research-article-status">${badge(e)}${promotion(e)}</div>
      ${replacement ? `<div class="research-correction">This note has been superseded. Continue with <a href="${entryUrl(replacement)}">${esc(replacement.title)}</a>.</div>` : ''}
      <p class="research-takeaway"><strong>The idea</strong>${esc(e.takeaway)}</p>
      ${headings.length ? `<details class="research-toc"><summary>In this note</summary><ul>${headings.map((h) => `<li><a href="#${h.id}">${esc(h.text)}</a></li>`).join('')}</ul></details>` : ''}
      <div class="research-prose">${body}</div>
      <p class="research-source"><a href="${esc(repoUrl(e.source, ref))}">Source note and revision history</a></p>
      ${concepts.length ? `<section class="research-related"><h2>In the knowledge base</h2><ul>${concepts.map((n) => `<li><a href="knowledge/${n.id}.html">${esc(n.title)}</a> <span class="kb-inline-kind">${esc(n.kind)}</span></li>`).join('')}</ul></section>` : ''}
      ${related.length ? `<section class="research-related"><h2>Continue the thread</h2><ul>${related.map((x) => `<li><a href="${entryUrl(x)}">${esc(x.title)}</a></li>`).join('')}</ul></section>` : ''}
    </article>`);
    const file = path.join(output, entryUrl(e));
    fs.writeFileSync(file, html); inputs[`research-${e.slug}`] = file;
  }
  return { inputs, dependencies: [...dependencies] };
}

export function researchWatch(dependencies) {
  return {
    name: 'research-markdown-watch',
    configureServer(server) {
      server.watcher.add(dependencies);
      server.watcher.on('change', (file) => {
        if (dependencies.includes(file)) server.restart();
      });
    },
  };
}
