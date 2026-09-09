import fs from 'node:fs';
import path from 'node:path';
import { ROOT, SITE, esc, dateLabel, existingRepoPath, sourceRef, repoUrl, layout, renderMarkdown } from './research.mjs';

import { readResearchRecords, catalogFiles } from './research-program.mjs';

export const KNOWLEDGE = path.join(SITE, 'content/knowledge.json');
export const KINDS = {
  concept: ['defined'], finding: ['exact', 'replicated', 'exploratory', 'superseded'],
  question: ['open', 'partly-answered', 'answered'], theory: ['proposed', 'supported', 'refuted', 'superseded'],
  experiment: ['planned', 'completed'],
};
export const STATUS = {
  defined: 'Definition', exact: 'Exact within stated bounds', replicated: 'Replicated experiment',
  exploratory: 'Exploratory', superseded: 'Superseded', open: 'Open',
  'partly-answered': 'Partly answered', answered: 'Answered', proposed: 'Proposed',
  supported: 'Supported', refuted: 'Refuted', planned: 'Planned', completed: 'Completed',
};
export const RELATIONS = {
  depends_on: { label: 'Depends on', inverse: 'Required by', meaning: 'A relies on B as a premise, definition, or experimental setup. Changes to B may require reviewing A.' },
  supports: { label: 'Supports', inverse: 'Supported by', meaning: 'A provides evidence for B within the stated scope. Support alone does not establish B.' },
  contradicts: { label: 'Contradicts', inverse: 'Contradicted by', meaning: 'A provides counterevidence to B within the stated scope.' },
  tests: { label: 'Tests', inverse: 'Tested by', meaning: 'Experiment A is designed to investigate B. A planned test supplies no result.' },
};
const check = (condition, message) => { if (!condition) throw new Error(`Knowledge: ${message}`); };
const hasText = (value) => typeof value === 'string' && value.trim().length > 0;
const link = (node) => `<a href="${node.id}.html">${esc(node.title)}</a>`;
const badge = (node) => `<span class="research-status ${node.status}">${STATUS[node.status]}</span>`;

export function readKnowledge() { return JSON.parse(fs.readFileSync(KNOWLEDGE, 'utf8')); }

export function validateKnowledge(graph, research) {
  check(graph?.schemaVersion === 1 && Array.isArray(graph.nodes) && Array.isArray(graph.edges), 'expected schemaVersion 1, nodes, and edges');
  const nodes = new Map(), sources = new Set(), notes = new Set(research.map((r) => r.slug));
  const validateResearch = (refs, label) => {
    check(Array.isArray(refs) && refs.length > 0 && refs.every((r) => notes.has(r)) && new Set(refs).size === refs.length, `missing, duplicate, or unknown research reference in ${label}`);
  };
  for (const node of graph.nodes) {
    for (const field of ['id', 'title', 'kind', 'status', 'summary', 'updated', 'source']) check(hasText(node[field]), `missing ${field}`);
    check(/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(node.id) && !['index', 'graph'].includes(node.id), `invalid id ${node.id}`);
    check(!nodes.has(node.id) && !sources.has(node.source), `duplicate id or source: ${node.id}`);
    check(Object.hasOwn(KINDS, node.kind) && KINDS[node.kind].includes(node.status), `invalid kind/status in ${node.id}`);
    check(/^\d{4}-\d{2}-\d{2}$/.test(node.updated) && !Number.isNaN(Date.parse(node.updated)) && new Date(node.updated).toISOString().slice(0, 10) === node.updated, `invalid date in ${node.id}`);
    check(node.source.startsWith('docs/knowledge/') && node.source.endsWith('.md'), `invalid source in ${node.id}`);
    existingRepoPath(node.source, 'knowledge entry');
    validateResearch(node.research, node.id);
    nodes.set(node.id, node); sources.add(node.source);
  }
  for (const node of graph.nodes) {
    check(!node.supersededBy || (node.status === 'superseded' && nodes.has(node.supersededBy) && node.supersededBy !== node.id), `invalid replacement in ${node.id}`);
    check(node.status !== 'superseded' || node.supersededBy, `superseded entry needs a replacement: ${node.id}`);
  }
  const triples = new Set();
  for (const edge of graph.edges) {
    check(nodes.has(edge.source) && nodes.has(edge.target) && edge.source !== edge.target, `unknown endpoint or self-link: ${edge.source} → ${edge.target}`);
    check(Object.hasOwn(RELATIONS, edge.type), `unknown relation ${edge.type}`);
    check(hasText(edge.reason), `relationship needs a rationale: ${edge.source} → ${edge.target}`);
    validateResearch(edge.research, `${edge.source} → ${edge.target}`);
    const key = JSON.stringify([edge.source, edge.type, edge.target]);
    check(!triples.has(key), `duplicate relationship ${key}`); triples.add(key);
    const from = nodes.get(edge.source), to = nodes.get(edge.target);
    if (edge.type === 'tests') check(from.kind === 'experiment' && ['question', 'theory', 'finding'].includes(to.kind), 'tests must point from an experiment to a question, theory, or finding');
    if (['supports', 'contradicts'].includes(edge.type)) {
      check(from.kind === 'finding' || (from.kind === 'experiment' && from.status === 'completed'), `${edge.type} needs a finding or completed experiment as its source`);
      check(['finding', 'theory'].includes(to.kind), `${edge.type} must target a finding or theory`);
    }
  }
  function rejectCycles(next, label) {
    const active = new Set(), done = new Set();
    function visit(id) {
      check(!active.has(id), `${label} cycle at ${id}`);
      if (done.has(id)) return;
      active.add(id); for (const target of next(id)) visit(target); active.delete(id); done.add(id);
    }
    for (const id of nodes.keys()) visit(id);
  }
  rejectCycles((id) => graph.edges.filter((e) => e.type === 'depends_on' && e.source === id).map((e) => e.target), 'dependency');
  rejectCycles((id) => nodes.get(id).supersededBy ? [nodes.get(id).supersededBy] : [], 'replacement');
  return graph;
}

/** One shortest dependency path per reachable entry; evidence links never propagate dependency. */
export function dependencyPaths(graph, id, reverse = false) {
  const visited = new Set([id]), queue = [[id]], result = [];
  for (let i = 0; i < queue.length; i++) {
    const route = queue[i], current = route.at(-1);
    for (const edge of graph.edges) {
      if (edge.type !== 'depends_on' || (reverse ? edge.target : edge.source) !== current) continue;
      const next = reverse ? edge.source : edge.target;
      if (visited.has(next)) continue;
      visited.add(next); const chain = [...route, next]; queue.push(chain); result.push(chain);
    }
  }
  return result;
}

export function buildKnowledge({ graph = readKnowledge(), research = readResearchRecords(), output = path.join(SITE, 'research/knowledge') } = {}) {
  validateKnowledge(graph, research);
  const nodes = new Map(graph.nodes.map((n) => [n.id, n]));
  const notes = new Map(research.map((n) => [n.slug, n]));
  const ref = sourceRef(), dependencies = new Set([KNOWLEDGE, ...catalogFiles()]);
  const bySource = new Map([
    ...graph.nodes.map((n) => [path.resolve(ROOT, n.source), `${n.id}.html`]),
    ...research.map((n) => [path.resolve(ROOT, n.source), `../${n.slug}.html`]),
  ]);
  fs.mkdirSync(output, { recursive: true });
  for (const name of fs.readdirSync(output)) if (name.endsWith('.html')) fs.unlinkSync(path.join(output, name));
  const inputs = {};
  const write = (id, title, summary, body, script = '') => {
    const file = path.join(output, `${id}.html`);
    fs.writeFileSync(file, layout(title, summary, body, { depth: 2, section: 'knowledge', script }));
    inputs[`knowledge-${id}`] = file;
  };
  const researchLinks = (refs) => refs.map((id) => `<a href="../${id}.html">${esc(notes.get(id).title)}</a>`).join(' · ');
  const routeLinks = (route) => route.map((id) => link(nodes.get(id))).join(' <span class="kb-connector">depends on</span> ');
  const rows = graph.nodes.map((n) => {
    const search = [n.id, n.title, n.summary, n.kind, STATUS[n.status]].join(' ').toLowerCase();
    return `<article class="kb-entry" data-knowledge-entry data-kind="${n.kind}" data-search="${esc(search)}">
      <div class="research-meta"><span>${esc(n.kind)}</span><time datetime="${n.updated}">${dateLabel(n.updated)}</time></div>
      <h2>${link(n)}</h2><p>${esc(n.summary)}</p>${badge(n)}</article>`;
  }).join('');
  write('index', 'Knowledge base', 'Findings, questions, theories, and the relationships between them.', `
    <h1 class="kb-heading">Knowledge base</h1><p class="kb-intro">The current claims, open questions, and their connections. Research notes preserve how we got here.</p>
    <div class="kb-layout"><section aria-label="Knowledge entries">
      <form class="kb-filters" data-knowledge-filters hidden role="search">
        <label>Find an entry<input type="search" name="query" placeholder="Try “commutator” or “history”" autocomplete="off"></label>
        <label>Type<select name="kind"><option value="">All types</option>${Object.keys(KINDS).map((k) => `<option value="${k}">${k[0].toUpperCase() + k.slice(1)}</option>`).join('')}</select></label>
        <button type="reset">Clear</button>
      </form>
      <p class="kb-count" data-knowledge-count role="status">${graph.nodes.length} entries</p>
      <p data-knowledge-empty hidden>No entries match. Try another word or choose all types.</p>${rows}
    </section><aside class="research-sidebar kb-sidebar">
      <section><h2>Follow a connection</h2><p>Each relationship gives its direction, a reason, and the research behind it. Backlinks show both sides.</p><p>On an entry, “What relies on this?” follows dependencies through the record. A changed premise calls for review; it does not automatically change a conclusion.</p></section>
      <section><h2>Relationship meanings</h2><dl class="kb-definitions">${Object.values(RELATIONS).map((r) => `<dt>${r.label}</dt><dd>${esc(r.meaning)}</dd>`).join('')}</dl></section>
      <section><h2>Reuse the record</h2><p><a href="graph.json" download>Download the structured graph</a></p><p><a href="${esc(repoUrl('docs/knowledge/README.md', ref))}">Editing and relationship guide</a></p></section>
    </aside></div>`, 'src/knowledge-index.js');

  for (const node of graph.nodes) {
    const { body } = renderMarkdown(path.resolve(ROOT, node.source), { bySource, ref, output, dependencies, reservedIds: ['connections', 'dependents', 'record'] });
    const incoming = graph.edges.filter((e) => e.target === node.id), outgoing = graph.edges.filter((e) => e.source === node.id);
    const relationshipList = (edges, inward) => edges.length ? `<ul class="kb-relations">${edges.map((e) => {
      const other = nodes.get(inward ? e.source : e.target), r = RELATIONS[e.type];
      return `<li><div class="kb-relation-label">${inward ? r.inverse : r.label}</div><h3>${link(other)}</h3>${badge(other)}<p>${esc(e.reason)}</p><div class="kb-citation">Research: ${researchLinks(e.research)}</div></li>`;
    }).join('')}</ul>` : '<p class="kb-empty">No relationships recorded in this direction.</p>';
    const impact = dependencyPaths(graph, node.id, true);
    const questionable = dependencyPaths(graph, node.id).filter((route) => ['refuted', 'superseded'].includes(nodes.get(route.at(-1)).status));
    write(node.id, node.title, node.summary, `<article class="kb-article">
      <a class="research-back" href="index.html">← All knowledge</a>
      <div class="research-meta"><span>${esc(node.kind)}</span><span>Updated <time datetime="${node.updated}">${dateLabel(node.updated)}</time></span></div>
      <h1 class="kb-heading">${esc(node.title)}</h1><p class="research-summary">${esc(node.summary)}</p>${badge(node)}
      ${node.supersededBy ? `<p class="research-correction">Superseded by ${link(nodes.get(node.supersededBy))}. This record is retained.</p>` : ''}
      ${questionable.length ? `<aside class="kb-review"><h2>Review prerequisites</h2><p>A recorded dependency is refuted or superseded. Review these paths before relying on this entry; its status has not been changed automatically.</p><ul>${questionable.map((route) => `<li>${routeLinks(route)} <strong>(${STATUS[nodes.get(route.at(-1)).status]})</strong></li>`).join('')}</ul></aside>` : ''}
      <nav class="kb-jump" aria-label="In this entry"><a href="#record">Current account</a><a href="#connections">Connections</a><a href="#dependents">What relies on this?</a></nav>
      <div id="record" class="research-prose kb-prose">${body}</div>
      <section id="connections" class="kb-section"><h2>Connections</h2><div class="kb-connections"><section><h3>From this entry</h3>${relationshipList(outgoing, false)}</section><section><h3>Backlinks</h3>${relationshipList(incoming, true)}</section></div></section>
      <section id="dependents" class="kb-section"><h2>What relies on this?</h2>${impact.length ? `<p>Direct and indirect dependents, with one shortest path for each. Only “depends on” links are followed.</p><ul class="kb-paths">${impact.map((route) => `<li>${routeLinks([...route].reverse())}</li>`).join('')}</ul>` : '<p>No dependent entries are recorded yet.</p>'}</section>
      <section class="kb-section"><h2>Research record</h2><ul>${node.research.map((id) => `<li>${researchLinks([id])}</li>`).join('')}</ul><p class="research-source"><a href="${esc(repoUrl(node.source, ref))}">Source entry and revision history</a></p></section>
    </article>`);
  }
  const exported = {
    ...graph, sourceRef: ref, relations: RELATIONS, kinds: KINDS, statuses: STATUS,
    dependencySemantics: 'A depends_on B; traverse incoming depends_on edges for affected dependents. Statuses are authored, not inferred. A cycle of supports edges is not a proof.',
    nodes: graph.nodes.map((n) => ({ ...n, url: `${n.id}.html`, sourceUrl: repoUrl(n.source, ref) })),
    research: research.map((r) => ({ id: r.slug, title: r.title, url: `../${r.slug}.html` })),
  };
  const source = JSON.stringify(exported, null, 2) + '\n';
  fs.writeFileSync(path.join(output, 'graph.json'), source);
  return { inputs, dependencies: [...dependencies], asset: { type: 'asset', fileName: 'research/knowledge/graph.json', source } };
}

export function knowledgeAsset(asset) {
  return { name: 'knowledge-graph-export', generateBundle() { this.emitFile(asset); } };
}
