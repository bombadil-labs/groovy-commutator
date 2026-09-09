import test, { after } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { ROOT } from './research.mjs';
import { buildResearchProgram, readResearchRecords, validateProgram, PROGRAM } from './research-program.mjs';

const output = fs.mkdtempSync(path.join(os.tmpdir(), 'groovy-program-'));
const records = () => readResearchRecords();
const program = () => JSON.parse(fs.readFileSync(PROGRAM, 'utf8'));
const page = (name) => fs.readFileSync(path.join(output, name), 'utf8');
after(() => fs.rmSync(output, { recursive: true, force: true }));

test('the extended record contains numbered notes plus one unnumbered checkpoint', () => {
  const all = records();
  const notes = all.filter((entry) => (entry.recordType || 'note') === 'note');
  const checkpoints = all.filter((entry) => entry.recordType === 'checkpoint');
  assert.ok(notes.length >= 25);
  assert.equal(checkpoints.length, 1);
  assert.equal(new Set(notes.map((entry) => entry.number)).size, notes.length);
  assert.ok(notes.every((entry) => typeof entry.number === 'string' && entry.number.length > 0));
  const checkpoint = checkpoints[0];
  assert.equal(checkpoint.slug, 'selector-shielding');
  assert.equal(checkpoint.number, undefined);
  assert.equal(checkpoint.label, 'Checkpoint');
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

test('the living program validates against registered evidence', () => {
  assert.doesNotThrow(() => validateProgram(program(), records()));
  const bad = program();
  bad.supports = ['missing-record'];
  assert.throws(() => validateProgram(bad, records()), /unknown program support/);
});

test('program, records, and local evidence links render as first-class routes', () => {
  const result = buildResearchProgram({ output });
  assert.equal(Object.keys(result.inputs).length, records().length + 2);
  assert.match(page('index.html'), /href="program.html">Dynamics of Erased Distinctions/);
  assert.match(page('program.html'), /aria-current="page">Program<\/a>/);
  assert.match(page('program.html'), /href="observation-closure.html">Research022/);
  assert.match(page('fiber-visibility.html'), /Note 025 · Exact fiber-visibility census/);
  assert.match(page('block3-representation-design.html'), /Note 028 · Exact block-3 representation-design census/);
  assert.match(page('selector-shielding.html'), /Checkpoint · Exact selector theorem/);
  assert.match(page('selector-shielding.html'), /Source record and revision history/);
});

test('program source and restored Research025 source exist in the repository', () => {
  for (const source of [program().source, records().find((entry) => entry.slug === 'fiber-visibility').source]) {
    assert.ok(fs.existsSync(path.join(ROOT, source)), source);
  }
});
