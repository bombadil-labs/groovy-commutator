import test, { after } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { ROOT } from './research.mjs';
import { buildResearchProgram, readResearchRecords, readPrograms, validateProgram, validatePrograms, PROGRAM } from './research-program.mjs';

const output = fs.mkdtempSync(path.join(os.tmpdir(), 'groovy-program-'));
const records = () => readResearchRecords();
const programs = () => readPrograms();
const page = (name) => fs.readFileSync(path.join(output, name), 'utf8');
after(() => fs.rmSync(output, { recursive: true, force: true }));

test('the extended record contains numbered notes and unnumbered checkpoints', () => {
  const all = records();
  const notes = all.filter((entry) => (entry.recordType || 'note') === 'note');
  const checkpoints = all.filter((entry) => entry.recordType === 'checkpoint');
  assert.ok(notes.length >= 25);
  assert.ok(checkpoints.length >= 1);
  assert.ok(checkpoints.every((entry) => entry.number === undefined && typeof entry.label === 'string' && entry.label.trim()));
  assert.equal(new Set(notes.map((entry) => entry.number)).size, notes.length);
  assert.ok(notes.every((entry) => typeof entry.number === 'string' && entry.number.length > 0));
  const checkpoint = checkpoints.find((entry) => entry.slug === 'selector-shielding');
  assert.equal(checkpoint.slug, 'selector-shielding');
  assert.equal(checkpoint.number, undefined);
  assert.equal(checkpoint.label, 'Checkpoint');
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
  assert.match(page('selector-shielding.html'), /Checkpoint · Exact selector theorem/);
  assert.match(page('selector-shielding.html'), /Source record and revision history/);
});

test('program sources and restored Research025 source exist in the repository', () => {
  for (const source of [...programs().map((p) => p.source), records().find((entry) => entry.slug === 'fiber-visibility').source]) {
    assert.ok(fs.existsSync(path.join(ROOT, source)), source);
  }
  assert.ok(fs.existsSync(PROGRAM));
});
