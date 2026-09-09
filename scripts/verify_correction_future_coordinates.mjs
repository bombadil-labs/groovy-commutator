#!/usr/bin/env node
/**
 * Deductive audit, 2026-09-09. No class labels or fitted hypotheses.
 * Run: node scripts/verify_correction_future_coordinates.mjs
 * Optional output: redirect stdout to a JSON file.
 *
 * The body is dependency-free JavaScript so the identical calculation can
 * also run in the chat JavaScript runtime. All finite domains are explicit.
 * These checks audit the accompanying algebraic proof; finite-ring closure
 * is never promoted to infinite-lattice closure.
 */
function insist(ok, message) { if (!ok) throw new Error(message); }

function correction(F, A) {
  return A.map((value, s) => A[F[s]] ^ F[value]);
}
function forwardReadout(F, coordinates) {
  let row = coordinates.slice();
  const future = [row[0]];
  while (row.length > 1) {
    row = row.slice(0, -1).map((value, j) => F[value] ^ row[j + 1]);
    future.push(row[0]);
  }
  return future;
}
function inverseReadout(F, future) {
  let row = future.slice();
  const coordinates = [row[0]];
  while (row.length > 1) {
    row = row.slice(0, -1).map((value, t) => row[t + 1] ^ F[value]);
    coordinates.push(row[0]);
  }
  return coordinates;
}
function equal(a,b) { return a.length === b.length && a.every((v,i)=>v===b[i]); }
function decode(code, size, base) {
  const values=[];
  for(let j=0;j<size;j++) { values.push(code % base); code=Math.floor(code/base); }
  return values;
}
function ecaStep(rule, state, width) {
  let result=0;
  for(let x=0;x<width;x++) {
    const l=(state>>((x+width-1)%width))&1;
    const c=(state>>x)&1;
    const r=(state>>((x+1)%width))&1;
    result|=((rule>>(4*l+2*c+r))&1)<<x;
  }
  return result;
}
function canonicalPartition(values) {
  const ids=new Map();
  return values.map(value=>{
    const key=value.join(',');
    if(!ids.has(key)) ids.set(key,ids.size);
    return ids.get(key);
  });
}
function deterministicGiven(keys, outputs) {
  const seen=new Map();
  for(let s=0;s<keys.length;s++) {
    const key=keys[s].join(',');
    if(seen.has(key) && seen.get(key)!==outputs[s]) return false;
    seen.set(key,outputs[s]);
  }
  return true;
}
function localCorrection(rule, table, radius) {
  const childRadius=radius+1, out=[];
  for(let word=0;word<(1<<(2*childRadius+1));word++) {
    let evolved=0;
    for(let x=0;x<2*radius+1;x++) {
      const q=4*((word>>x)&1)+2*((word>>(x+1))&1)+((word>>(x+2))&1);
      evolved|=((rule>>q)&1)<<x;
    }
    const mask=(1<<(2*radius+1))-1;
    const left=table[word&mask], center=table[(word>>1)&mask], right=table[(word>>2)&mask];
    out.push(table[evolved]^((rule>>(4*left+2*center+right))&1));
  }
  return out;
}
function shrinkStep(rule, row) {
  const next=[];
  for(let x=1;x<row.length-1;x++)
    next.push((rule>>(4*row[x-1]+2*row[x]+row[x+1]))&1);
  return next;
}
function localAt(table, radius, row, center) {
  let word=0;
  for(let x=-radius;x<=radius;x++) word|=row[center+x]<<(x+radius);
  return table[word];
}

function runAudit() {
  const result={protocol:'deductive audit; no preregistered empirical prediction',
    class_labels_loaded:false, arbitrary_maps:{}, eca_rings:{}, local_windows:{}};
  let arbitraryWords=0, mapStateChecks=0, partitionChecks=0;
  // ALL 256 endomaps and ALL 256 observations on the two-bit state space.
  for(let fc=0;fc<256;fc++) {
    const F=decode(fc,4,4);
    for(let word=0;word<256;word++) {
      const coords=decode(word,4,4);
      const future=forwardReadout(F,coords);
      insist(equal(coords,inverseReadout(F,future)),'word inverse');
      insist(equal(coords,forwardReadout(F,inverseReadout(F,coords))),'word forward');
      arbitraryWords++;
    }
    for(let ac=0;ac<256;ac++) {
      const A=decode(ac,4,4), tower=[A];
      for(let k=0;k<3;k++) tower.push(correction(F,tower[k]));
      const coordinates=[], futures=[];
      for(let s=0;s<4;s++) {
        const coords=tower.map(T=>T[s]);
        let current=s; const future=[];
        for(let t=0;t<4;t++) { future.push(A[current]);current=F[current]; }
        insist(equal(forwardReadout(F,coords),future),'operator/readout mismatch');
        coordinates.push(coords); futures.push(future); mapStateChecks++;
      }
      for(let h=0;h<=3;h++) {
        const c=coordinates.map(v=>v.slice(0,h+1)), b=futures.map(v=>v.slice(0,h+1));
        insist(equal(canonicalPartition(c),canonicalPartition(b)),'fiber mismatch');
        partitionChecks++;
      }
    }
  }
  result.arbitrary_maps={state_bits:2,evolutions:256,observations_per_evolution:256,
    max_correction_index:3,arbitrary_word_roundtrips:arbitraryWords,
    evolution_observation_state_checks:mapStateChecks,partition_checks:partitionChecks};

  const width=8, maxIndex=4, records=[];
  let ringStateChecks=0, ringPartitionChecks=0;
  for(let rule=0;rule<256;rule++) {
    const F=Array.from({length:1<<width},(_,s)=>ecaStep(rule,s,width));
    const D=F.map((v,s)=>v^s), tower=[D];
    for(let k=0;k<maxIndex;k++) tower.push(correction(F,tower[k]));
    const coordinates=[], futures=[];
    for(let s=0;s<F.length;s++) {
      const coords=tower.map(T=>T[s]); let current=s;const future=[];
      for(let t=0;t<=maxIndex;t++) {future.push(D[current]);current=F[current];}
      insist(equal(forwardReadout(F,coords),future),'ECA forward');
      coordinates.push(coords);futures.push(future);ringStateChecks++;
    }
    let closure=null;
    const fiberCounts=[];
    for(let h=0;h<=maxIndex;h++) {
      const c=coordinates.map(v=>v.slice(0,h+1)), b=futures.map(v=>v.slice(0,h+1));
      const p=canonicalPartition(c);
      insist(equal(p,canonicalPartition(b)),'ECA partition');
      fiberCounts.push(new Set(p).size);ringPartitionChecks++;
      if(h<maxIndex) {
        const closed=deterministicGiven(c,tower[h+1]);
        insist(closed===deterministicGiven(b,futures.map(v=>v[h+1])),'closure equivalence');
        if(closed&&closure===null)closure=h;
      }
    }
    records.push({rule,first_closed_index_through_3:closure,
      distinct_correction_maps_through_4:new Set(tower.map(T=>T.join(','))).size,
      predictive_fiber_counts:fiberCounts});
  }
  result.eca_rings={width,max_correction_index:maxIndex,rules:256,
    state_checks:ringStateChecks,partition_checks:ringPartitionChecks,
    records};

  // No torus: direct local composition tables versus shrinking-window time
  // evolution and the triangular inverse. Every 11-bit word, all 256 ECAs.
  let windows=0, coordinateBits=0, transportBits=0;
  for(let rule=0;rule<256;rule++) {
    let D=[];
    for(let w=0;w<8;w++)D.push(((w>>1)&1)^((rule>>(4*(w&1)+2*((w>>1)&1)+((w>>2)&1)))&1));
    const tables=[D];
    for(let k=0;k<4;k++)tables.push(localCorrection(rule,tables[k],k+1));
    for(let word=0;word<2048;word++) {
      const initial=decode(word,11,2), history=[];
      let current=initial.slice();
      for(let t=0;t<=4;t++) {
        history.push(current.slice(1,-1).map((v,j)=>
          v^((rule>>(4*current[j]+2*v+current[j+2]))&1)));
        current=shrinkStep(rule,current);
      }
      // Transform whole shrinking observation rows; F is applied horizontally.
      let differenceRows=history;
      for(let k=0;k<=4;k++) {
        insist(differenceRows[0][(differenceRows[0].length-1)/2]===tables[k][(word>>(4-k))&((1<<(2*k+3))-1)],'local future coordinates');
        coordinateBits++;
        if(k<4)differenceRows=differenceRows.slice(0,-1).map((row,t)=>{
          const transported=shrinkStep(rule,row);
          return transported.map((v,j)=>v^differenceRows[t+1][j]);
        });
      }
      const evolved=shrinkStep(rule,initial);
      for(let k=0;k<4;k++) {
        const r=k+1;
        const l=localAt(tables[k],r,initial,4);
        const c=localAt(tables[k],r,initial,5);
        const right=localAt(tables[k],r,initial,6);
        const transported=((rule>>(4*l+2*c+right))&1)^localAt(tables[k+1],r+1,initial,5);
        insist(transported===localAt(tables[k],r,evolved,4),'local spatial transport');
        transportBits++;
      }
      windows++;
    }
  }
  result.local_windows={rules:256,window_bits:11,max_correction_index:4,
    windows,coordinate_bit_checks:coordinateBits,transport_bit_checks:transportBits};
  result.failures=0;
  return result;
}

function canonical(value) {
  if (Array.isArray(value)) return value.map(canonical);
  if (value !== null && typeof value === 'object')
    return Object.fromEntries(Object.keys(value).sort().map(key => [key, canonical(value[key])]));
  return value;
}
console.log(JSON.stringify(canonical(runAudit()), null, 2));
