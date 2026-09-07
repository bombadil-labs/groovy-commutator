import test, { after } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { buildResearch, validateCatalog, CATALOG, ROOT } from './research.mjs';

const catalog = () => JSON.parse(fs.readFileSync(CATALOG, 'utf8'));
const output = fs.mkdtempSync(path.join(os.tmpdir(), 'groovy-research-'));
const fixtures = fs.mkdtempSync(path.join(ROOT, 'docs/research/research-test-'));
const fixtureSource = path.join(fixtures, 'note.md');
const readPage = (slug) => fs.readFileSync(path.join(output, `${slug}.html`), 'utf8');
const render = (entries = catalog()) => buildResearch({ entries, output });
after(() => {
  fs.rmSync(output, { recursive: true, force: true });
  fs.rmSync(fixtures, { recursive: true, force: true });
});

function withFixture(markdown) {
  fs.writeFileSync(fixtureSource, markdown);
  return [...catalog(), {
    slug: 'new-note', number: 'test', title: 'A new question & its limits',
    date: '2026-09-08', updated: '2026-09-08', kind: 'Research plan',
    evidence: 'open', topic: 'Observation and memory',
    summary: 'A test of adding a note through the catalog.', takeaway: 'An open question.',
    source: path.relative(ROOT, fixtureSource),
    promotion: { stage: 'research' }, related: ['history-repairability'],
  }];
}

test('published notes render with their evidence, math, and repository links', () => {
  const { inputs } = render();
  assert.equal(Object.keys(inputs).length, catalog().length + 1);
  for (const entry of catalog()) {
    const html = readPage(entry.slug);
    assert.equal((html.match(/<h1\b/g) || []).length, 1);
    assert.match(html, /aria-current="page">Research<\/a>/);
    assert.match(html, /<details class="research-toc">/);
    assert.doesNotMatch(html, /<script\b/);
    const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map((m) => m[1]);
    assert.equal(new Set(ids).size, ids.length, `duplicate IDs in ${entry.slug}`);
    for (const [, anchor] of html.matchAll(/href="#([^"]+)"/g)) {
      assert.ok(ids.includes(anchor), `missing section ${anchor} in ${entry.slug}`);
    }
  }
  const history = readPage('history-repairability');
  assert.match(history, /<math xmlns="http:\/\/www.w3.org\/1998\/Math\/MathML"/);
  assert.match(history, /role="region" aria-label="Data table" tabindex="0"/);
  assert.match(history, /https:\/\/github.com\/bombadil-labs\/groovy-commutator\/blob\//);
  const [, figure] = history.match(/<img src="(assets\/[^\"]+\.svg)"/);
  assert.ok(fs.existsSync(path.join(output, figure)));
  assert.match(readPage('affine-converse'), /href="history-repairability.html"/);
});

test('one catalog addition creates a page and an index entry with no route edit', () => {
  const entries = withFixture('# Source title\n\n## Result\n\n\\(x \\oplus y\\)\n\n## Result\n\n[Earlier experiment](../2026-09-07-history-repairability.md)\n');
  const result = render(entries);
  assert.ok(result.inputs['research-new-note']);
  assert.match(readPage('index'), /href="new-note.html">A new question &amp; its limits/);
  const html = readPage('new-note');
  assert.match(html, /id="result"/);
  assert.match(html, /id="result-1"/);
  assert.match(html, /href="history-repairability.html">Earlier experiment/);
  assert.doesNotMatch(html, /Source title/);
  render();
  assert.equal(fs.existsSync(path.join(output, 'new-note.html')), false);
});

test('evidence and promotion remain independent, and superseded notes retain a route forward', () => {
  const entries = catalog();
  entries[0].evidence = 'superseded';
  entries[0].supersededBy = 'ether-or-defects';
  entries[0].promotion = { stage: 'research' };
  entries[2].promotion = { stage: 'candidate', idea: 'An open question to explain', destination: 'Questions' };
  render(entries);
  assert.match(readPage('history-repairability'), /This note has been superseded/);
  assert.match(readPage('history-repairability'), /Continue with <a href="ether-or-defects.html"/);
  assert.match(readPage('index'), /An open question to explain/);
  assert.match(readPage('ether-or-defects'), /Open question<\/span>/);
});

test('catalog rejects duplicate identities and invalid dates', () => {
  for (const field of ['slug', 'number', 'source']) {
    const entries = catalog();
    entries[1][field] = entries[0][field];
    assert.throws(() => validateCatalog(entries), /duplicate/);
  }
  const entries = catalog();
  entries[0].date = '2026-02-30';
  assert.throws(() => validateCatalog(entries), /invalid date/);
});

test('catalog rejects broken sources, related notes, and promoted anchors', () => {
  for (const [mutate, message] of [
    [(e) => { e.source = 'docs/research/missing-note.md'; }, /missing or invalid note/],
    [(e) => { e.related = ['nonexistent']; }, /unknown or self reference/],
    [(e) => { e.promotion = { stage: 'candidate' }; }, /candidate needs/],
    [(e) => { e.promotion = { stage: 'promoted', title: 'Explanation', href: 'concepts.html#missing-anchor' }; }, /missing explainer anchor/],
    [(e) => { e.evidence = 'superseded'; }, /superseded note needs a replacement/],
  ]) {
    const entries = catalog(); mutate(entries[0]);
    assert.throws(() => validateCatalog(entries), message);
  }
});

test('missing linked evidence and invalid TeX fail the build', () => {
  assert.throws(() => render(withFixture('# Note\n\n[Data](missing.csv)\n')), /missing or invalid linked file/);
  assert.throws(() => render(withFixture('# Note\n\n\\[\\notARealCommand{x}\\]\n')), /invalid math/);
  assert.throws(() => render(withFixture('# Note\n\n# Another title\n')), /only one top-level title/);
});

test('source and data links use the deployed commit when available', () => {
  const original = process.env.GITHUB_SHA;
  process.env.GITHUB_SHA = '0123456789abcdef0123456789abcdef01234567';
  try {
    render();
    assert.match(readPage('affine-converse'), /\/blob\/0123456789abcdef0123456789abcdef01234567\/results\/history_algebra_checks.json/);
  } finally {
    if (original === undefined) delete process.env.GITHUB_SHA;
    else process.env.GITHUB_SHA = original;
  }
});
