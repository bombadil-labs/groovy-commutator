"""Independent audit of the first Research028 greedy-repair counterexample.

This script deliberately does not import the Research028 experiment/aggregator.
It evolves Rule 24 directly, builds explicit target future words, independently
enumerates the 406 target refinements, and reconstructs greedy/global costs.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

N=12
RULE=24
TARGET=tuple(map(int,"01000010"))
GREEDY_FINAL=tuple(map(int,"01230245"))
GLOBAL_FINAL=tuple(map(int,"01230243"))
GREEDY_FIRST=tuple(map(int,"01200210"))
ZERO_FIRST=tuple(map(int,"01000020"))
SPLIT_DIRECT=tuple(map(int,"01020012"))
SPLIT_AFTER_ZERO=tuple(map(int,"01020032"))
TOL=1e-9


def canon_blocks(blocks):
    return tuple(sorted((tuple(sorted(b)) for b in blocks),key=lambda b:min(b)))


def labels_from_blocks(blocks):
    labels=[-1]*8
    for lab,b in enumerate(canon_blocks(blocks)):
        for x in b: labels[x]=lab
    return tuple(labels)


def blocks_from_labels(p):
    d={}
    for i,x in enumerate(p):d.setdefault(x,[]).append(i)
    return canon_blocks(tuple(tuple(v) for _,v in sorted(d.items())))


def set_partitions(elements):
    elements=tuple(sorted(elements))
    if not elements:return ((),)
    first=elements[0]
    tail=set_partitions(elements[1:])
    out=set()
    for part in tail:
        out.add(canon_blocks(((first,),)+part))
        for i in range(len(part)):
            q=list(part);q[i]=tuple(sorted((first,)+q[i]));out.add(canon_blocks(tuple(q)))
    return tuple(sorted(out))


def target_interval():
    a,b=blocks_from_labels(TARGET)
    out=set()
    for pa in set_partitions(a):
        for pb in set_partitions(b):
            out.add(labels_from_blocks(pa+pb))
    return tuple(sorted(out,key=lambda p:(len(set(p)),p)))


def covers(p):
    out=set()
    for C in blocks_from_labels(p):
        if len(C)<2:continue
        first=C[0];rest=C[1:]
        for mask in range(1<<len(rest)):
            left=(first,)+tuple(rest[j] for j in range(len(rest)) if (mask>>j)&1)
            if len(left)==len(C):continue
            ls=set(left);right=tuple(x for x in C if x not in ls)
            old=[b for b in blocks_from_labels(p) if b!=C]
            out.add(labels_from_blocks(tuple(old)+(left,right)))
    return tuple(sorted(out))


def fine_state_map():
    states=np.arange(2**N,dtype=np.uint32)
    bits=((states[:,None]>>np.arange(N,dtype=np.uint32))&1).astype(np.uint8)
    code=4*np.roll(bits,1,axis=1)+2*bits+np.roll(bits,-1,axis=1)
    lut=np.asarray([(RULE>>i)&1 for i in range(8)],dtype=np.uint8)
    out=lut[code]
    weights=(1<<np.arange(N,dtype=np.uint64))
    return (out.astype(np.uint64)*weights).sum(1).astype(np.uint32)


def observation(p):
    states=np.arange(2**N,dtype=np.uint32)
    bits=((states[:,None]>>np.arange(N,dtype=np.uint32))&1).astype(np.uint8)
    b=bits.reshape(len(states),N//3,3)
    code=(b*(1<<np.arange(3,dtype=np.uint8))).sum(2)
    lut=np.asarray(p,dtype=np.uint8);macro=lut[code];base=len(set(p))
    weights=np.asarray([base**i for i in range(N//3)],dtype=np.uint32)
    return (macro.astype(np.uint32)*weights).sum(1).astype(np.uint16)


def entropy_rows(a):
    _,c=np.unique(a,axis=0,return_counts=True);prob=c/c.sum()
    return float(-(prob*np.log2(prob)).sum())


def entropy_labels(a):
    _,c=np.unique(a,return_counts=True);prob=c/c.sum()
    return float(-(prob*np.log2(prob)).sum())


def explicit_future(step,target_obs,max_steps=64):
    s=np.arange(len(step),dtype=np.uint32)
    cols=[target_obs.copy()]
    prev=len(np.unique(np.stack(cols,axis=1),axis=0))
    for t in range(1,max_steps+1):
        s=step[s];cols.append(target_obs[s])
        word=np.stack(cols,axis=1);count=len(np.unique(word,axis=0))
        if count==prev:return word,t-1
        prev=count
    raise RuntimeError('future word did not stabilize')


def metrics(p,word):
    z=observation(p);hz=entropy_labels(z)
    joint=np.concatenate([z[:,None],word],axis=1)
    w=entropy_rows(joint)-hz
    closed=len(np.unique(joint,axis=0))==len(np.unique(z))
    return {'H':hz,'W':max(0.0,w),'closed':closed}


def greedy(nodes):
    path=[TARGET];cur=TARGET
    while not nodes[cur]['closed']:
        choices=[]
        for child in covers(cur):
            if child not in nodes:continue
            dh=nodes[child]['H']-nodes[cur]['H']
            if dh<=1e-12:continue
            g=(nodes[cur]['W']-nodes[child]['W'])/dh
            choices.append((-g,''.join(map(str,child)),child))
        if not choices:raise AssertionError('no greedy child')
        cur=min(choices)[2];path.append(cur)
    return path


def edge_gain(a,b,nodes):
    dw=nodes[a]['W']-nodes[b]['W'];dh=nodes[b]['H']-nodes[a]['H']
    return {'delta_W':dw,'delta_H':dh,'g':dw/dh}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    fine=fine_state_map();step=fine[fine[fine]]
    tobs=observation(TARGET);word,hstar=explicit_future(step,tobs)
    ints=target_interval();assert len(ints)==406
    nodes={p:metrics(p,word) for p in ints}
    ht=nodes[TARGET]['H']
    closed=[p for p in ints if nodes[p]['closed']]
    costs={p:nodes[p]['H']-ht for p in closed}
    global_cost=min(costs.values());opts=sorted(p for p,c in costs.items() if abs(c-global_cost)<TOL)
    gpath=greedy(nodes);gcost=nodes[gpath[-1]]['H']-ht
    zero=edge_gain(TARGET,ZERO_FIRST,nodes)
    direct=edge_gain(TARGET,SPLIT_DIRECT,nodes)
    conditioned=edge_gain(ZERO_FIRST,SPLIT_AFTER_ZERO,nodes)
    checks={
      'interval_406':len(ints)==406,
      'global_named_closed':nodes[GLOBAL_FINAL]['closed'],
      'global_cost':abs(global_cost-5.754887502163468)<TOL,
      'global_named_optimal':GLOBAL_FINAL in opts,
      'greedy_final':gpath[-1]==GREEDY_FINAL,
      'greedy_cost':abs(gcost-6.754887502163468)<TOL,
      'regret_one':abs((gcost-global_cost)-1.0)<TOL,
      'zero_first_gain':abs(zero['delta_W'])<TOL,
      'synergy':conditioned['g']>direct['g']+TOL,
    }
    out={'ok':all(checks.values()),'rule':RULE,'ring_width':N,'cadence':3,'target':''.join(map(str,TARGET)),
         'target_hstar':hstar,'target_W':nodes[TARGET]['W'],'interval_nodes':len(ints),
         'greedy_path':[''.join(map(str,p)) for p in gpath],'greedy_added_bits':gcost,
         'global_min_added_bits':global_cost,'global_optima':[''.join(map(str,p)) for p in opts],
         'zero_gain_bridge':{'partition':''.join(map(str,ZERO_FIRST)),**zero},
         'same_split_before':{'partition':''.join(map(str,SPLIT_DIRECT)),**direct},
         'same_split_after_bridge':{'partition':''.join(map(str,SPLIT_AFTER_ZERO)),**conditioned},
         'gain_amplification':conditioned['g']/direct['g'],'checks':checks}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
    if not out['ok']:raise SystemExit(1)

if __name__=='__main__':main()
