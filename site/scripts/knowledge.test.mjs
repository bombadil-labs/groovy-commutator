import test, { after } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { readKnowledge, validateKnowledge, dependencyPaths, buildKnowledge } from './knowledge.mjs';
import { ROOT, CATALOG, buildResearch } from './research.mjs';
import { matchesKnowledge } from '../src/knowledge-index.js';

const research = JSON.parse(fs.readFileSync(CATALOG, 'utf8'));
const output = fs.mkdtempSync(path.join(os.tmpdir(), 'groovy-knowledge-'));
const fixtureDir = fs.mkdtempSync(path.join(ROOT, 'docs/knowledge/knowledge-test-'));
after(() => {
  fs.rmSync(output, { recursive: true, force: true });
  fs.rmSync(fixtureDir, { recursive: true, force: true });
});
const render = (graph = readKnowledge()) => buildKnowledge({ graph, research, output });
const html = (id) => fs.readFileSync(path.join(output, `${id}.html`), 'utf8');

test('knowledge pages show typed backlinks, research provenance, and an export', () => {
  const graph = readKnowledge(), built = render(graph);
  assert.equal(Object.keys(built.inputs).length, graph.nodes.length + 1);
  assert.match(html('affine-converse'), /Contradicted by<\/div><h3><a href="nonlinear-zero.html"/);
  assert.match(html('nonlinear-zero'), /Contradicts<\/div><h3><a href="affine-converse.html"/);
  assert.match(html('nonlinear-zero'), /href="\.\.\/affine-converse.html"/);
  assert.match(html('affine-implication'), /<math xmlns=/);
  assert.match(html('index'), /data-knowledge-filters hidden/);
  assert.match(html('index'), /href="graph.json" download/);
  const exported = JSON.parse(built.asset.source);
  assert.deepEqual(exported.edges, graph.edges);
  assert.equal(exported.nodes.length, graph.nodes.length);
  assert.equal(exported.schemaVersion, 1);
  assert.equal(built.asset.fileName, 'research/knowledge/graph.json');
  for (const node of graph.nodes) {
    assert.equal((html(node.id).match(/<h1\b/g) || []).length, 1);
    assert.doesNotMatch(html(node.id), /<script\b/);
  }
});

test('dependency traversal deduplicates diamonds and excludes support links', () => {
  const graph = { edges: [
    { source: 'a', type: 'depends_on', target: 'b' },
    { source: 'a', type: 'depends_on', target: 'c' },
    { source: 'b', type: 'depends_on', target: 'd' },
    { source: 'c', type: 'depends_on', target: 'd' },
    { source: 'q', type: 'supports', target: 'd' },
  ] };
  assert.deepEqual(dependencyPaths(graph, 'd', true), [['d', 'b'], ['d', 'c'], ['d', 'b', 'a']]);
  assert.deepEqual(dependencyPaths(graph, 'a'), [['a', 'b'], ['a', 'c'], ['a', 'b', 'd']]);
});

test('dependency and replacement cycles fail, while support cycles do not imply proof', () => {
  const graph = readKnowledge();
  graph.edges.push({ ...graph.edges[0], source: 'observed-history', target: 'history-repair' });
  assert.throws(() => validateKnowledge(graph, research), /dependency cycle/);
  const replacements = readKnowledge();
  const a = replacements.nodes.find((n) => n.id === 'history-repair'), b = replacements.nodes.find((n) => n.id === 'projection-dependence');
  a.status = b.status = 'superseded'; a.supersededBy = b.id; b.supersededBy = a.id;
  assert.throws(() => validateKnowledge(replacements, research), /replacement cycle/);
  const supported = readKnowledge();
  supported.edges.push({ source: 'zero-is-not-linearity', type: 'supports', target: 'nonlinear-zero', reason: 'Synthetic cycle to check that evidence links are not dependencies.', research: ['affine-converse'] });
  assert.doesNotThrow(() => validateKnowledge(supported, research));
});

test('superseded prerequisites flag dependents without changing their authored status', () => {
  const graph = readKnowledge();
  const experimentStatus = graph.nodes.find((n) => n.id === 'regional-prediction-test').status;
  const premise = graph.nodes.find((n) => n.id === 'history-repair');
  premise.status = 'superseded'; premise.supersededBy = 'projection-dependence';
  render(graph);
  assert.match(html('history-repair'), /Superseded by <a href="projection-dependence.html"/);
  assert.match(html('regional-prediction-test'), /Review prerequisites/);
  assert.ok(html('regional-prediction-test').includes(`class="research-status ${experimentStatus}">`));
  assert.equal(graph.nodes.find((n) => n.id === 'regional-prediction-test').status, experimentStatus);
  assert.match(html('projection-dependence'), /class="research-status replicated">Replicated experiment/);
  assert.equal(graph.nodes.find((n) => n.id === 'projection-dependence').status, 'replicated');
});

test('schema rejects missing endpoints, provenance, rationale, and invalid semantic direction', () => {
  for (const [mutate, error] of [
    [(g) => { g.nodes[1].id = g.nodes[0].id; }, /duplicate id/],
    [(g) => { g.nodes[0].status = 'refuted'; }, /invalid kind\/status/],
    [(g) => { g.edges[0].target = 'missing'; }, /unknown endpoint/],
    [(g) => { g.edges[0].type = 'support'; }, /unknown relation/],
    [(g) => { g.edges[0].reason = ' '; }, /rationale/],
    [(g) => { g.edges[0].research = ['missing-note']; }, /unknown research reference/],
    [(g) => { g.edges.push({ ...g.edges[0] }); }, /duplicate relationship/],
    [(g) => { g.edges[0].type = 'tests'; }, /tests must point/],
    [(g) => {
      // Set the fixture's lifecycle explicitly: the real experiment can advance.
      g.nodes.find((n) => n.id === 'regional-prediction-test').status = 'planned';
      g.edges.push({ source: 'regional-prediction-test', type: 'supports', target: 'phase-recovery',
        reason: 'Synthetic invalid support from a planned experiment.', research: ['ether-or-defects'] });
    }, /supports needs a finding or completed experiment/],
  ]) {
    const graph = readKnowledge(); mutate(graph);
    assert.throws(() => validateKnowledge(graph, research), error);
  }
});

test('a catalog addition creates its page, semantic backlink, and research backlink', () => {
  const source = path.join(fixtureDir, 'entry.md');
  fs.writeFileSync(source, '# New question\n\n## Context\n\nSee [the observation](../observed-history.md) and [the experiment](../../research/2026-09-07-history-repairability.md).\n');
  const graph = readKnowledge();
  graph.nodes.push({ id: 'new-question', title: 'A new question?', kind: 'question', status: 'open', summary: 'An added record.', updated: '2026-09-08', source: path.relative(ROOT, source), research: ['history-repairability'] });
  graph.edges.push({ source: 'new-question', type: 'depends_on', target: 'observed-history', reason: 'This question uses the observation definition.', research: ['history-repairability'] });
  const built = render(graph);
  assert.ok(built.inputs['knowledge-new-question']);
  assert.match(html('observed-history'), /Required by<\/div><h3><a href="new-question.html"/);
  assert.match(html('new-question'), /href="observed-history.html">the observation/);
  assert.match(html('new-question'), /href="\.\.\/history-repairability.html">the experiment/);
  const notesOutput = path.join(output, 'notes');
  buildResearch({ entries: structuredClone(research), knowledge: graph.nodes, output: notesOutput });
  assert.match(fs.readFileSync(path.join(notesOutput, 'history-repairability.html'), 'utf8'), /href="knowledge\/new-question.html"/);
  render(); assert.equal(fs.existsSync(path.join(output, 'new-question.html')), false);
});

test('search matches all terms and combines them with the kind filter', () => {
  assert.equal(matchesKnowledge('Rule 110 history repair', 'finding', 'HISTORY 110', 'finding'), true);
  assert.equal(matchesKnowledge('Rule 110 history repair', 'finding', 'history', 'theory'), false);
  assert.equal(matchesKnowledge('Rule 110 history repair', 'finding', 'history missing'), false);
  assert.equal(matchesKnowledge('Ether phase', 'theory', ' ÉTHER  '), true);
  assert.equal(matchesKnowledge('Any entry', 'question', '', ''), true);
});
