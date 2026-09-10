import test, { after } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { ROOT } from './research.mjs';
import { buildResearchProgram, readResearchRecords, readPrograms, validateProgram, validatePrograms, validateRecords, PROGRAM } from './research-program.mjs';

const output = fs.mkdtempSync(path.join(os.tmpdir(), 'groovy-program-'));
const records = () => readResearchRecords();
const programs = () => readPrograms();
const page = (name) => fs.readFileSync(path.join(output, name), 'utf8');
after(() => fs.rmSync(output, { recursive: true, force: true }));

test('the record contains numbered notes, labeled notes, and scoped checkpoints', () => {
  const all = records();
  const notes = all.filter((entry) => (entry.recordType || 'note') === 'note');
  const numbered = notes.filter((entry) => entry.number !== undefined);
  const labeled = notes.filter((entry) => entry.number === undefined);
  const checkpoints = all.filter((entry) => entry.recordType === 'checkpoint');
  assert.ok(numbered.length >= 25);
  assert.ok(labeled.length >= 1);
  assert.ok(checkpoints.length >= 2);
  assert.equal(new Set(numbered.map((entry) => entry.number)).size, numbered.length);
  assert.ok(labeled.every((entry) => typeof entry.label === 'string' && entry.label.trim() && entry.scope === undefined));
  assert.ok(checkpoints.every((entry) => entry.number === undefined && entry.evidence === 'state' && typeof entry.scope === 'string'));
  const shielding = labeled.find((entry) => entry.slug === 'selector-shielding');
  assert.equal(shielding.label, 'Selector shielding');
  assert.ok(labeled.every((entry) => !/checkpoint/i.test(entry.label)), 'labels no longer use the word checkpoint for notes');
  const lab = checkpoints.find((entry) => entry.slug === 'unfinished-threads');
  assert.equal(lab.scope, 'lab');
  const vision = checkpoints.find((entry) => entry.slug === 'dimensional-vision-and-interpretation');
  assert.equal(vision.scope, 'dimensional-lift');
});

test('checkpoint validation: scope, state evidence, no number, not evidence for a program', () => {
  const all = records();
  const slugs = programs().map((p) => p.slug);
  assert.doesNotThrow(() => validateRecords(all, slugs));
  const cp = structuredClone(all.find((entry) => entry.slug === 'unfinished-threads'));
  assert.throws(() => validateRecords([...all.filter((e) => e.slug !== cp.slug), { ...cp, scope: 'nowhere' }], slugs), /scope must be "lab" or a Program slug/);
  assert.throws(() => validateRecords([...all.filter((e) => e.slug !== cp.slug), { ...cp, evidence: 'exact' }], slugs), /carries evidence "state"/);
  assert.throws(() => validateRecords([...all.filter((e) => e.slug !== cp.slug), { ...cp, number: '999' }], slugs), /never numbered/);
  const note = structuredClone(all.find((entry) => entry.slug === 'selector-shielding'));
  assert.throws(() => validateRecords([...all.filter((e) => e.slug !== note.slug), { ...note, evidence: 'state' }], slugs), /reserved for checkpoints/);
  assert.throws(() => validateRecords([...all.filter((e) => e.slug !== note.slug), { ...note, scope: 'lab' }], slugs), /only checkpoints carry a scope/);
  const program = structuredClone(programs()[0]);
  program.supports = [...program.supports, 'unfinished-threads'];
  assert.throws(() => validateProgram(program, all), /checkpoint is not evidence/);
});

test('sofic defect-orbit has one canonical publication identity', () => {
  const note = records().find((entry) => entry.slug === 'sofic-defect-orbit');
  assert.ok(note);
  assert.equal(note.number, '036');

  const banned = [
    ['Research', '035'].join(''),
    ['Note', '035'].join(''),
    ['Note ', '035'].join(''),
    'internal_research_line',
  ];
  const lineage = [
    note.source,
    'docs/research/protocols/sofic-defect-orbit-20260909.md',
    'docs/research/protocols/sofic-defect-orbit-resource-addendum-20260909.md',
    'docs/research/protocols/sofic-defect-orbit-lazy-union-recovery-20260909.md',
    'docs/research/protocols/sofic-defect-orbit-raw-slice-recovery-20260909.md',
    'docs/research/protocols/sofic-defect-orbit-public-numbering-20260909.md',
    'scripts/experiment_sofic_defect_orbit.py',
    'scripts/experiment_sofic_defect_orbit_lazy.py',
    'scripts/experiment_sofic_defect_orbit_raw.py',
    'scripts/aggregate_sofic_defect_orbit.py',
    'scripts/aggregate_sofic_defect_orbit_lazy.py',
    'scripts/aggregate_sofic_defect_orbit_raw.py',
    'results/sofic_defect_orbit_20260909.json',
    'results/sofic_defect_orbit_lazy_20260909.json',
    'results/sofic_defect_orbit_raw_control_20260909.json',
    'results/sofic_defect_orbit_provenance_20260909.json',
  ];
  for (const relative of lineage) {
    const text = fs.readFileSync(path.join(ROOT, relative), 'utf8');
    for (const token of banned) assert.equal(text.includes(token), false, `${relative} contains stale alias ${token}`);
  }

  const provenance = JSON.parse(fs.readFileSync(path.join(ROOT, 'results/sofic_defect_orbit_provenance_20260909.json'), 'utf8'));
  assert.equal(provenance.canonical_slug, 'sofic-defect-orbit');
  assert.equal(provenance.note_number, '036');
  assert.equal(provenance.alternate_internal_note_number, null);
  assert.equal(provenance.scientific_semantics_changed, false);
  assert.match(provenance.source_hashes_semantics, /frozen prepublication source bytes/);
  for (const relative of provenance.historical_results.slice(0, 2)) {
    const result = JSON.parse(fs.readFileSync(path.join(ROOT, relative), 'utf8'));
    assert.ok(result.source_hashes && Object.keys(result.source_hashes).length > 0);
  }
});

test('same-day numbered notes render newest number first', () => {
  buildResearchProgram({ output });
  const html = page('index.html');
  const pos35 = html.indexOf('href="ternary-commutator-lift.html"');
  const pos34 = html.indexOf('href="window3-reachable-language.html"');
  const pos33 = html.indexOf('href="reachable-context-invariants.html"');
  assert.ok(pos35 >= 0 && pos34 >= 0 && pos33 >= 0);
  assert.ok(pos35 < pos34 && pos34 < pos33);
});

test('multiple living programs validate against registered evidence', () => {
  const ps = programs();
  assert.ok(ps.length >= 2);
  assert.deepEqual(new Set(ps.map((p) => p.slug)), new Set(['erased-distinctions', 'dimensional-lift']));
  assert.doesNotThrow(() => validatePrograms(ps, records()));
  const bad = structuredClone(ps[0]);
  bad.supports = ['missing-record'];
  assert.throws(() => validateProgram(bad, records()), /unknown program support/);
  assert.throws(() => validatePrograms([ps[0], { ...ps[1], slug: ps[0].slug }], records()), /duplicate program slug/);
});

test('program landing, program routes, records, and local evidence links render as first-class routes', () => {
  const result = buildResearchProgram({ output });
  assert.equal(Object.keys(result.inputs).length, records().length + programs().length + 2);
  assert.match(page('index.html'), /href="program-erased-distinctions.html">Dynamics of Erased Distinctions/);
  assert.match(page('index.html'), /href="program-dimensional-lift.html">Dimensional Closure and the Commutator Lift/);
  assert.match(page('program.html'), /aria-current="page">Programs<\/a>/);
  assert.match(page('program.html'), /program-erased-distinctions.html/);
  assert.match(page('program.html'), /program-dimensional-lift.html/);
  assert.match(page('program-erased-distinctions.html'), /href="observation-closure.html">Research022/);
  assert.match(page('program-dimensional-lift.html'), /href="ternary-commutator-lift.html">The commuting square grows a ternary spatial address/);
  assert.match(page('program-dimensional-lift.html'), /href="program-erased-distinctions.html">Dynamics of Erased Distinctions/);
  assert.match(page('fiber-visibility.html'), /Note 025 · Exact fiber-visibility census/);
  assert.match(page('block3-representation-design.html'), /Note 028 · Exact block-3 representation-design census/);
  assert.match(page('selector-shielding.html'), /Selector shielding · Exact selector theorem/);
  assert.match(page('unfinished-threads.html'), /Checkpoint · Lab · Checkpoint: lab-wide backlog/);
  assert.match(page('dimensional-vision-and-interpretation.html'), /Checkpoint · Dimensional Closure and the Commutator Lift/);
  assert.match(page('index.html'), /Checkpoint · state, no new evidence/);
  assert.match(page('selector-shielding.html'), /Source record and revision history/);
});

test('program sources and restored Research025 source exist in the repository', () => {
  for (const source of [...programs().map((p) => p.source), records().find((entry) => entry.slug === 'fiber-visibility').source]) {
    assert.ok(fs.existsSync(path.join(ROOT, source)), source);
  }
  assert.ok(fs.existsSync(PROGRAM));
});
