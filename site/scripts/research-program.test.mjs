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

test('the extended record contains numbered notes plus an unnumbered checkpoint', () => {
  const all = records();
  assert.equal(all.length, 26);
  assert.equal(all.filter((entry) => (entry.recordType || 'note') === 'note').length, 25);
  const checkpoint = all.find((entry) => entry.recordType === 'checkpoint');
  assert.equal(checkpoint.slug, 'selector-shielding');
  assert.equal(checkpoint.number, undefined);
  assert.equal(checkpoint.label, 'Checkpoint');
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
  assert.match(page('selector-shielding.html'), /Checkpoint · Exact selector theorem/);
  assert.match(page('selector-shielding.html'), /Source record and revision history/);
});

test('program source and restored Research025 source exist in the repository', () => {
  for (const source of [program().source, records().find((entry) => entry.slug === 'fiber-visibility').source]) {
    assert.ok(fs.existsSync(path.join(ROOT, source)), source);
  }
});
