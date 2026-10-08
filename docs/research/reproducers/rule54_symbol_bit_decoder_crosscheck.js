#!/usr/bin/env node
// Rule54 J5 source-bit decoder crosscheck; fresh scalar JS implementation.
// This script is a bounded same-author crosscheck, not independent peer review.
'use strict';
const h=(l,c,r)=>(54>>(4*l+2*c+r))&1;
function step(w,n){let v=0;for(let j=0;j<n-2;j++)v|=h((w>>j)&1,(w>>(j+1))&1,(w>>(j+2))&1)<<j;return v;}
const A=[Array.from({length:8},(_,w)=>((w>>1)&1)^h(w&1,(w>>1)&1,(w>>2)&1))];
for(let k=0;k<6;k++){
  const width=2*k+5, mask=(1<<(width-2))-1,prev=A[k],row=[];
  for(let w=0;w<(1<<width);w++)row.push(prev[step(w,width)]^h(prev[w&mask],prev[(w>>1)&mask],prev[(w>>2)&mask]));
  A.push(row);
}
function label(w){let v=0;for(let k=1;k<=5;k++)v|=A[k][(w>>(5-k))&((1<<(2*k+3))-1)]<<(k-1);return v;}
const labels=Uint8Array.from({length:8192},(_,i)=>label(i));
const hist0=Array.from({length:32},()=>[0,0]);
for(let w=0;w<8192;w++)hist0[labels[w]][(w>>6)&1]++;
const pair0=hist0.map(([x,y])=>2*x*y),groups1=new Map(),symCount1=new Uint32Array(32),triples=Array.from({length:32},()=>new Set());
for(let w=0;w<32768;w++){
  const l=labels[w&8191],m=labels[(w>>1)&8191],r=labels[(w>>2)&8191],b=(w>>7)&1;
  const key=(l<<10)|(m<<5)|r;
  let cell=groups1.get(key);if(!cell){cell=[0,0];groups1.set(key,cell);}cell[b]++;
  symCount1[m]++;triples[m].add(key);
}
const pair1=Array(32).fill(0);
for(const [key,counts] of groups1)pair1[(key>>5)&31]+=2*counts[0]*counts[1];
const marker=[1,2,3,4,5,7,11,12,13,14,15,16,17,19,20,24,29];
const ambiguous=[0,6,8,10,22,25,26,27,28,30,31];
const missing=marker.filter(s=>pair1[s]>0),sets2=new Map();
for(let w=0;w<131072;w++){
  const labels5=Array.from({length:5},(_,i)=>labels[(w>>i)&8191]);
  if(!missing.includes(labels5[2]))continue;
  const key=labels5.join(','),bit=(w>>8)&1;
  let c=sets2.get(key);if(!c){c=[0,0];sets2.set(key,c);}c[bit]++;
}
const pair2=Object.fromEntries(missing.map(s=>[s,0]));
for(const [k,c] of sets2)pair2[Number(k.split(',')[2])]+=2*c[0]*c[1];
if(hist0[1][0]+hist0[1][1]!==352||pair0[1]!==36864||symCount1[1]!==1408||triples[1].size!==20||pair1[1]!==0)throw Error('Edition 11 control mismatch');
if(missing.join(',')!=='4,11,16,20,24')throw Error('unexpected missing markers');
if(JSON.stringify(pair2)!==JSON.stringify({'4':0,'11':0,'16':384,'20':0,'24':0}))throw Error('r2 mismatch');
const result={schema:'rule54-symbol-bit-decoder-independent-js-v1', source_windows:[8192,32768,131072],
  certified_global_markers:marker, ambiguous_global_symbols:ambiguous,
  rows:[...new Set([...marker,...ambiguous])].sort((a,b)=>a-b).map(s=>({symbol:s,global_marker:marker.includes(s),
     conflicting_bit_pairs_radius0:pair0[s],conflicting_bit_pairs_radius1:pair1[s],
     conflicting_bit_pairs_radius2:s in pair2?pair2[s]:null,
     min_verified_radius:pair0[s]===0?0:pair1[s]===0?1:(s in pair2&&pair2[s]===0)?2:'>tested'}))};
console.log(JSON.stringify(result,null,2));
