// Frozen protocol: docs/research/2026-09-09-selector-two-lift-protocol.md
// Dependency-free exact audit; run with Node.js 22.
function canonical(value) {
  if (Array.isArray(value)) return value.map(canonical);
  if (value !== null && typeof value === "object")
    return Object.fromEntries(Object.keys(value).sort().map(k => [k, canonical(value[k])]));
  return value;
}

function runAudit() {
  let assertions = 0;
  const check = (condition, message) => {
    assertions++;
    if (!condition) throw new Error(message);
  };
  const bit = (r, q) => (r >> q) & 1;
  const bits = (q, n) => Array.from({length:n}, (_, i) => (q >> i) & 1);
  const base = rule => ({kind:"eca", dim:1, rule});
  const rail = inner => ({kind:"rail", dim:inner.dim + 1, inner});
  function ast(p, inputs) {
    if (p.kind === "eca") return bit(p.rule, 4 * inputs[0] + 2 * inputs[1] + inputs[2]);
    return inputs[2 * p.dim - 1 + ast(p.inner, inputs)];
  }
  const f = (rule, b) => bit(rule, 4 * b[0] + 2 * b[1] + b[2]);
  const h = (rule, b) => f(rule, b) === 0 ? b[3] : b[4];
  const k = (rule, b) => h(rule, b) === 0 ? b[5] : b[6];

  // Spatial interpreter shares only the declared AST with the local interpreter.
  // Coordinates retain higher axes while a nested selector reads its central slice.
  function at(p, c, get) {
    if (p.kind === "eca") {
      const left = c.slice(), right = c.slice();
      left[0]--; right[0]++;
      return bit(p.rule, 4 * get(left) + 2 * get(c) + get(right));
    }
    const b = at(p.inner, c, get), next = c.slice();
    next[p.dim - 1] += b === 0 ? 1 : -1;
    return get(next);
  }
  function localEmbeddingPass(rule, dimension) {
    const p = dimension === 1 ? base(rule) : rail(base(rule));
    const lifted = rail(p);
    let passes = true, firstFailure = null, comparisons = 0;
    for (let q = 0; q < (1 << (2 * dimension + 1)); q++) {
      const b = bits(q, 2 * dimension + 1);
      function lower(c) {
        if (c[0] === -1) return b[0];
        if (c[0] === 1) return b[2];
        if (dimension === 2 && c[1] === 1) return b[3];
        if (dimension === 2 && c[1] === -1) return b[4];
        return b[1];
      }
      const evolved = dimension === 1 ? f(rule, b) : h(rule, b);
      const get = c => c[dimension] > 0 ? 0 : c[dimension] < 0 ? 1 : lower(c);
      for (let layer = -2; layer <= 2; layer++) {
        const c = Array(dimension + 1).fill(0); c[dimension] = layer;
        const actual = at(lifted, c, get);
        const expected = layer > 0 ? 0 : layer < 0 ? 1 : evolved;
        comparisons++;
        if (actual !== expected) {
          passes = false;
          firstFailure ??= {patch:b, layer, actual, expected};
        }
      }
    }
    return {passes, firstFailure, comparisons};
  }

  const firstTables = new Set(), secondTables = new Set();
  const firstRules = [], secondRules = [], endpointGroups = {};
  let firstLocal = 0, secondLocal = 0, interventions = 0;
  let firstEncodingComparisons = 0, secondEncodingComparisons = 0;
  const failureWitnesses = [];
  for (let rule = 0; rule < 256; rule++) {
    const p1 = rail(base(rule)), p2 = rail(p1);
    let t1 = "", t2 = "";
    for (let q = 0; q < 32; q++) {
      const b = bits(q, 5), actual = ast(p1, b);
      check(actual === h(rule, b), "first local truth table");
      t1 += actual; firstLocal++;
    }
    for (let q = 0; q < 128; q++) {
      const b = bits(q, 7), actual = ast(p2, b);
      check(actual === k(rule, b), "second local truth table");
      t2 += actual; secondLocal++;
    }
    firstTables.add(t1); secondTables.add(t2);
    for (let q = 0; q < 8; q++) {
      const patch = [(q >> 2) & 1, (q >> 1) & 1, q & 1, 0, 1, 0, 1];
      const changed = rule ^ (1 << q);
      check(ast(p1, patch) === bit(rule, q), "first instruction recovery");
      check(ast(p2, patch) === bit(rule, q), "second instruction recovery");
      check(ast(p1, patch) !== ast(rail(base(changed)), patch), "first intervention");
      check(ast(p2, patch) !== ast(rail(rail(base(changed))), patch), "second intervention");
      interventions += 2;
    }
    const a = localEmbeddingPass(rule, 1), b = localEmbeddingPass(rule, 2);
    const expectedFirst = bit(rule, 0) === 0 && bit(rule, 7) === 1;
    check(a.passes === expectedFirst, "first interface endpoint criterion");
    check(b.passes, "second interface arbitrary local source");
    firstEncodingComparisons += a.comparisons;
    secondEncodingComparisons += b.comparisons;
    if (a.passes) firstRules.push(rule);
    else failureWitnesses.push({rule, ...a.firstFailure});
    if (b.passes) secondRules.push(rule);
    const endpoints = String(bit(rule, 0)) + String(bit(rule, 7));
    endpointGroups[endpoints] = (endpointGroups[endpoints] ?? 0) + 1;
    check(ast(p1, Array(5).fill(0)) === 0, "first zero quiescence");
    check(ast(p1, Array(5).fill(1)) === 1, "first one quiescence");
    check(ast(p2, Array(7).fill(0)) === 0, "second zero quiescence");
    check(ast(p2, Array(7).fill(1)) === 1, "second one quiescence");
  }
  check(firstTables.size === 256 && secondTables.size === 256, "program injectivity");
  check(firstRules.length === 64 && secondRules.length === 256, "interface census");

  // Independent full-field implementation: direct scalar updates on source tori.
  function sourceStep(rule, field, dimension) {
    const out = new Uint8Array(field.length), width = dimension === 1 ? 5 : 3;
    for (let i = 0; i < field.length; i++) {
      const x = i % width, row = i - x;
      const q = 4 * field[row + (x + width - 1) % width] +
        2 * field[i] + field[row + (x + 1) % width];
      const control = bit(rule, q);
      if (dimension === 1) out[i] = control;
      else {
        const y = Math.floor(i / width);
        out[i] = field[((y + (control === 0 ? 1 : 2)) % 3) * 3 + x];
      }
    }
    return out;
  }
  function fieldAudit(rule, state, dimension, ticks, radius) {
    const count = dimension === 1 ? 5 : 9;
    let sourceField = Uint8Array.from(bits(state, count));
    let layers = Array.from({length:2 * radius + 1}, (_, j) =>
      j === radius ? sourceField.slice() : new Uint8Array(count).fill(j < radius ? 1 : 0));
    let comparisons = 0;
    for (let t = 0; t < ticks; t++) {
      const next = [];
      for (let j = 1; j < layers.length - 1; j++) {
        const control = sourceStep(rule, layers[j], dimension);
        next.push(Uint8Array.from(control, (b, i) => layers[j + (b === 0 ? 1 : -1)][i]));
      }
      layers = next; radius--;
      sourceField = sourceStep(rule, sourceField, dimension);
      for (let j = 0; j < layers.length; j++)
        for (let i = 0; i < count; i++) {
          const expected = j === radius ? sourceField[i] : j < radius ? 1 : 0;
          check(layers[j][i] === expected, "whole-field interface " + dimension);
          comparisons++;
        }
    }
    return comparisons;
  }
  let firstFieldCases = 0, firstFieldComparisons = 0;
  for (const rule of firstRules) for (let state = 0; state < 32; state++) {
    firstFieldComparisons += fieldAudit(rule, state, 1, 4, 5); firstFieldCases++;
  }
  let secondFieldCases = 0, secondFieldComparisons = 0;
  for (let rule = 0; rule < 256; rule++) for (let state = 0; state < 512; state++) {
    secondFieldComparisons += fieldAudit(rule, state, 2, 3, 4); secondFieldCases++;
  }

  // Both transverse axes are open. Discard one boundary cell on each axis/tick.
  function composedAudit(rule, state, actions) {
    const width = 5;
    let radius = 5, side = 11, sourceField = Uint8Array.from(bits(state, width));
    let field = new Uint8Array(width * side * side);
    const index = (x, y, z, s) => x + width * (y + s * z);
    const encoded = (x, y, z) => z > 0 ? 0 : z < 0 ? 1 :
      y > 0 ? 0 : y < 0 ? 1 : sourceField[x];
    for (let z = 0; z < side; z++) for (let y = 0; y < side; y++)
      for (let x = 0; x < width; x++) field[index(x,y,z,side)] = encoded(x,y-radius,z-radius);
    let comparisons = 0;
    for (let t = 0; t < 4; t++) {
      if (actions) {
        const x = t % width;
        sourceField[x] ^= 1;
        field[index(x, radius, radius, side)] ^= 1;
      }
      const smaller = side - 2, next = new Uint8Array(width * smaller * smaller);
      for (let z = 1; z < side - 1; z++) for (let y = 1; y < side - 1; y++)
        for (let x = 0; x < width; x++) {
          const atIndex = (a,b,c) => field[index(a,b,c,side)];
          const control1 = bit(rule, 4 * atIndex((x+width-1)%width,y,z) +
            2 * atIndex(x,y,z) + atIndex((x+1)%width,y,z));
          const control2 = atIndex(x, y + (control1 === 0 ? 1 : -1), z);
          next[index(x,y-1,z-1,smaller)] = atIndex(x,y,z+(control2 === 0 ? 1 : -1));
        }
      field = next; side = smaller; radius--;
      sourceField = sourceStep(rule, sourceField, 1);
      for (let z = 0; z < side; z++) for (let y = 0; y < side; y++)
        for (let x = 0; x < width; x++) {
          check(field[index(x,y,z,side)] === encoded(x,y-radius,z-radius),
            "composed field/action preservation");
          comparisons++;
        }
    }
    return comparisons;
  }
  let composedCases = 0, composedComparisons = 0, actionCases = 0, actionComparisons = 0;
  for (const rule of firstRules) for (let state = 0; state < 32; state++) {
    composedComparisons += composedAudit(rule, state, false); composedCases++;
    actionComparisons += composedAudit(rule, state, true); actionCases++;
  }
  return {
    protocol:"docs/research/2026-09-09-selector-two-lift-protocol.md",
    protocolFreezeCommit:"344e67434e735b948b3ff4aaa81cb24f25be8c44",
    schemaVersion:1,
    assertionCount:assertions,
    local:{sources:256, firstLiftComparisons:firstLocal, secondLiftComparisons:secondLocal,
      firstDistinctPrograms:firstTables.size, secondDistinctPrograms:secondTables.size,
      instructionInterventionWitnesses:interventions},
    interfaces:{firstPassingRules:firstRules, firstPassingCount:firstRules.length,
      secondPassingCount:secondRules.length, firstComparisons:firstEncodingComparisons,
      secondComparisons:secondEncodingComparisons, endpointGroups, firstFailureWitnesses:failureWitnesses},
    fields:{
      first:{cases:firstFieldCases, siteComparisons:firstFieldComparisons, ticks:4, sourceRingWidth:5, initialTransverseRadius:5},
      second:{cases:secondFieldCases, siteComparisons:secondFieldComparisons, ticks:3, sourceTorus:[3,3], initialTransverseRadius:4},
      composed:{cases:composedCases, siteComparisons:composedComparisons, ticks:4, sourceRingWidth:5, initialTransverseRadii:[5,5]},
      composedWithActions:{cases:actionCases, siteComparisons:actionComparisons, ticks:4, sourceRingWidth:5, initialTransverseRadii:[5,5]}
    },
    protocolDeviations:[],
    scope:"Exact audits of a routing grammar and half-space encoding; active mutable program data are not established."
  };
}

console.log(JSON.stringify(canonical(runAudit()), null, 2));
