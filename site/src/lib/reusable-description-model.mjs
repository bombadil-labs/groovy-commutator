// Exact, small examples; no inferred laws or external data.
export function cappedValuation(n, k = 3) {
  if (!Number.isSafeInteger(n) || !Number.isInteger(k) || k < 1 || k > 16) {
    throw new RangeError('Use a safe integer and a cap between 1 and 16.');
  }
  const modulus = 2 ** k;
  let r = ((n % modulus) + modulus) % modulus;
  if (r === 0) return k;
  let result = 0;
  while (r % 2 === 0) { r /= 2; result += 1; }
  return result;
}

export function futurePartition(k, depth) {
  const modulus = 2 ** k;
  const groups = new Map();
  for (let r = 0; r < modulus; r += 1) {
    const word = Array.from({ length: depth + 1 }, (_, t) => cappedValuation(r + t, k));
    const key = word.join(',');
    if (!groups.has(key)) groups.set(key, { word, residues: [] });
    groups.get(key).residues.push(r);
  }
  const partition = [...groups.values()];
  const labels = Array(modulus);
  partition.forEach((g, i) => g.residues.forEach(r => { labels[r] = i; }));
  return partition.map(g => ({
    ...g,
    nextGroups: [...new Set(g.residues.map(r => labels[(r + 1) % modulus]))],
  }));
}

export function evolve(rule, row) {
  const n = row.length;
  if (n < 1 || row.some(x => x !== 0 && x !== 1)) throw new RangeError('Binary nonempty ring required.');
  return row.map((_, i) => (rule >> ((row[(i + n - 1) % n] << 2) | (row[i] << 1) | row[(i + 1) % n])) & 1);
}
export const xor = (a, b) => a.map((x, i) => x ^ b[i]);
export function groovy(rule, row) {
  const next = evolve(rule, row);
  return xor(xor(next, evolve(rule, next)), evolve(rule, xor(row, next)));
}
export function caExample() {
  const source = [...'0101010'].map(Number);
  const y = groovy(32, source);
  const cases = [128, 160].map(rule => {
    const next = evolve(rule, y);
    const next2 = evolve(rule, next);
    const difference = xor(y, next);
    return { rule, next: next.join(''), next2: next2.join(''), difference: difference.join(''),
      evolvedDifference: evolve(rule, difference).join(''), g: groovy(rule, y).join('') };
  });
  const complement = source.map(x => 1 - x);
  return { source: source.join(''), sourceNext: evolve(32, source).join(''), y: y.join(''),
    cases, xorWitness: { zeroG: groovy(32, Array(7).fill(0)).join(''),
      oneG: groovy(32, Array(7).fill(1)).join(''), operand: source.join(''),
      operandG: y.join(''), complement: complement.join(''), complementG: groovy(32, complement).join('') } };
}
export function comparisonRecord() {
  return { arithmetic: [1, 2, 3, 4].map(k => ({ k, modulus: 2 ** k,
    values: Array.from({ length: 2 ** k }, (_, r) => cappedValuation(r, k)),
    partitions: Array.from({ length: 2 ** k }, (_, depth) => futurePartition(k, depth)),
  })), ca: caExample() };
}
