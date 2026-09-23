import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import test from 'node:test';
import { comparisonRecord, cappedValuation } from '../src/lib/reusable-description-model.mjs';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const record = JSON.parse(fs.readFileSync(path.join(root, 'results/reusable_descriptions_20260923.json')));

test('browser arithmetic and periodic CA fields match the separately computed Python record', () => {
  assert.deepEqual(comparisonRecord(), record.examples);
});

test('the recorded scope and mathematical implementations retain their pinned bytes', () => {
  for (const [p, digest] of Object.entries(record.sha256)) {
    assert.equal(createHash('sha256').update(fs.readFileSync(path.join(root, p))).digest('hex'), digest, p);
  }
});

test('capped readout respects residues, including zero and negative integers', () => {
  for (let n = -24; n <= 24; n += 1) assert.equal(cappedValuation(n), cappedValuation(n + 32));
  assert.equal(cappedValuation(0), 3);
  assert.equal(cappedValuation(-4), 2);
  assert.throws(() => cappedValuation(1.5));
});
