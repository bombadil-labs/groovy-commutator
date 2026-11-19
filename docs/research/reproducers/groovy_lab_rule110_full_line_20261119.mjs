#!/usr/bin/env node
// Exact Rule 110 audit. Run with Node; no packages or ring sampling.
import assert from "node:assert/strict";

const H = a => a.slice(1, -1).map((b, i) =>
  (110 >> (4 * a[i] + 2 * b + a[i + 2])) & 1);
const F = a => H(H(a));
const G = a => {
  const h = H(a);
  const d = h.map((b, i) => b ^ a[i + 1]);
  const hd = H(d);
  return H(h).map((b, i) => b ^ h[i + 1] ^ hd[i]);
};
const parity = b => (b >> 1) ^ (b & 1);
const alphabet = Array.from({ length: 16 }, (_, i) => [i >> 2, i & 3])
  .filter(([x, y]) => parity(x) === parity(y));
const unpack = (word, n) => Array.from({ length: n }, (_, i) =>
  alphabet[(word >> (3 * (n - i - 1))) & 7]);
const rows = pairs => [0, 1].map(j => pairs.flatMap(p => [p[j] >> 1, p[j] & 1]));
const diagonal = vertex => unpack(vertex, 4).every(([x, y]) => x === y);

function signature(a) {
  const f = F(a);
  // a covers sites -4..5; G(a) covers -2..3, f covers -2..3,
  // and G(f) covers 0..1. Initial parity is built into the alphabet.
  return [G(a)[2], G(a)[3], f[2] ^ f[3], ...G(f)].join("");
}

const allowed = [];
for (let w = 0; w < 8 ** 5; w++) {
  const pair = rows(unpack(w, 5));
  if (signature(pair[0]) === signature(pair[1])) {
    allowed.push({ from: w >> 3, to: w & 4095, pair });
  }
}
let essential = allowed;
while (true) {
  const starts = new Set(essential.map(e => e.from));
  const ends = new Set(essential.map(e => e.to));
  const next = essential.filter(e => ends.has(e.from) && starts.has(e.to));
  if (next.length === essential.length) break;
  essential = next;
}

const off = essential.filter(e => !diagonal(e.from) || !diagonal(e.to));
assert(!off.some(e => diagonal(e.from)));
const loops = off.filter(e => e.from === e.to)
  .map(e => e.pair.map(r => r.join("")).join("/")).sort();
assert.deepEqual(loops, [
  "0000000000/1111111111", "0101010101/1010101010",
  "1010101010/0101010101", "1111111111/0000000000",
]);
// A non-loop edge is cyclic iff its target can reach its source.
for (const { from, to } of off.filter(e => e.from !== e.to)) {
  const todo = [to], visited = new Set();
  while (todo.length) {
    const x = todo.pop();
    assert.notEqual(x, from);
    if (visited.has(x)) continue;
    visited.add(x);
    todo.push(...off.filter(e => e.from === x).map(e => e.to));
  }
}

function seam(i) { return i < 0 ? 0 : i % 2; }
const seamTable = [-2, -1, 0, 1].map(i => {
  const x = Array.from({ length: 5 }, (_, j) => seam(i + j - 2));
  const y = x.map(b => b ^ 1);
  const values = [x, y].map(r => [G(r)[0], F(r)[0]]);
  assert.deepEqual(values[0], values[1]);
  return [i, x.join(""), y.join(""), ...values[0]];
});
assert.deepEqual(seamTable.map(r => r.slice(3)), [[0,0], [0,1], [1,1], [0,0]]);
for (const tail of ["00000", "11111", "01010", "10101"]) {
  const r = Array.from(tail, Number);
  assert.deepEqual([G(r)[0], F(r)[0]], [0,0]);
}
const unequalF = essential.filter(e => {
  const [x, y] = e.pair.map(F);
  return x[2] !== y[2] || x[3] !== y[3];
}).map(e => e.pair.map(r => r.join("")));
assert.deepEqual([allowed.length, essential.length, off.length, unequalF.length],
  [4904, 1088, 64, 2]);
console.log(JSON.stringify({
  allowed: allowed.length, essential: essential.length, off: off.length,
  loops, unequalF, seamTable,
}, null, 2));
