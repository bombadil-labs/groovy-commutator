#!/usr/bin/env python3
"""Post-hoc finite-ring fiber diagnostic for the autonomous Rule-54 J5 factor.

Unlike the exact infinite-line factor theorem, this measures the uniform
periodic-source ensemble and distinguishes same-orbit temporal phase, eventual
coalescence, and genuinely disjoint source orbits. No interpretation about
typical full-line conditional entropy follows from the finite widths.
"""
from __future__ import annotations
import argparse,json,math
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
RULE=54

def maps(n):
    states=np.arange(1<<n,dtype=np.uint32)
    positions=np.arange(n,dtype=np.uint32)
    bits=(states[:,None]>>positions)&1
    lut=np.array([(RULE>>i)&1 for i in range(8)],dtype=np.uint8)
    table=lut[4*np.roll(bits,1,axis=1)+2*bits+np.roll(bits,-1,axis=1)]
    h=np.sum(table*(1<<positions),axis=1,dtype=np.uint64).astype(np.uint32)
    jet=[states^h]
    for _ in range(6):
        a=jet[-1]
        jet.append(a[h]^h[a])
    return h,jet

def orbit(h,x):
    seen={};seq=[];cur=x
    while cur not in seen:
        seen[cur]=len(seq);seq.append(cur);cur=int(h[cur])
    return seq,seen,seen[cur]

def mechanism(h,x,y):
    ax,idx,px=orbit(h,x);ay,idy,py=orbit(h,y)
    y_in_x=y in idx;x_in_y=x in idy
    if y_in_x and x_in_y:return 'same_source_orbit'
    if y_in_x or x_in_y:return 'one_is_future_of_other'
    if set(ax[px:])&set(ay[py:]):return 'common_eventual_cycle_different_preimages'
    return 'disjoint_source_orbits'

def profile(n):
    h,jet=maps(n)
    current=np.stack(jet[1:6],axis=1)
    _,inverse,counts=np.unique(current,axis=0,return_inverse=True,return_counts=True)
    hist=Counter(int(c) for c in counts)
    lost=sum(int(c)*math.log2(int(c)) for c in counts)/(1<<n)
    colliders=defaultdict(list)
    for source,cls in enumerate(inverse):
        if counts[cls]>1:colliders[int(cls)].append(source)
    types=Counter();sample={}
    future_agrees=True
    for members in colliders.values():
        nxt=tuple(int(level[h[members[0]]]) for level in jet[1:6])
        for y in members[1:]:
            if tuple(int(level[h[y]]) for level in jet[1:6])!=nxt:
                future_agrees=False
        for i,x in enumerate(members):
            for y in members[i+1:]:
                kind=mechanism(h,x,y)
                types[kind]+=1
                sample.setdefault(kind,{'source_x':x,'source_y':y,'xor':x^y})
    return {
        'n':n,'source_states':1<<n,'jet_image_states':len(counts),
        'fiber_histogram':{str(k):v for k,v in sorted(hist.items())},
        'colliding_fibers':len(colliders),
        'uniform_source_bits_forgotten':lost,
        'unordered_equal_jet_pairs':sum(int(c)*(int(c)-1)//2 for c in counts),
        'mechanisms':dict(types),'example_pairs':sample,
        'entire_current_J5_determines_next_J5':future_agrees
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,default=ROOT/'results'/'rule54_periodic_j5_fibers_20261007.json')
    args=ap.parse_args()
    rows={str(n):profile(n) for n in (8,10,12,14,16,18)}
    assert all(row['entire_current_J5_determines_next_J5'] for row in rows.values())
    out={
      'schema':'rule54-periodic-j5-fiber-diagnostic-v1',
      'date':'2026-10-07',
      'provenance':'post-hoc descriptive uniform finite-ring census; not a prospective classifier',
      'source':'Rule 54, uniform over all source rings at n=8,10,12,14,16,18',
      'observable':'J5=(G,Q,R,A4,A5)',
      'rows':rows
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    for n,r in rows.items():
        print(n,r['jet_image_states'],r['uniform_source_bits_forgotten'],r['mechanisms'])

if __name__=='__main__':main()
