"""Fresh n=15 validation of the Research028 Rule-24 greedy counterexample.

Uses direct Rule-24 evolution and explicit target future words, independently of
the primary Research028 experiment implementation.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import numpy as np

N=15;RULE=24;TOL=1e-9
TARGET=tuple(map(int,"01000010"))
ZERO=tuple(map(int,"01000020"))
DIRECT=tuple(map(int,"01020012"))
CONDITIONED=tuple(map(int,"01020032"))
OLD_GLOBAL=tuple(map(int,"01230243"))
OLD_GREEDY=tuple(map(int,"01230245"))


def canon_blocks(blocks):return tuple(sorted((tuple(sorted(b)) for b in blocks),key=lambda b:min(b)))
def blocks_from_labels(p):
 d={}
 for i,x in enumerate(p):d.setdefault(x,[]).append(i)
 return canon_blocks(tuple(tuple(v) for _,v in sorted(d.items())))
def labels_from_blocks(blocks):
 labels=[-1]*8
 for lab,b in enumerate(canon_blocks(blocks)):
  for x in b:labels[x]=lab
 return tuple(labels)
def set_partitions(elements):
 elements=tuple(sorted(elements))
 if not elements:return ((),)
 first=elements[0];out=set()
 for part in set_partitions(elements[1:]):
  out.add(canon_blocks(((first,),)+part))
  for i in range(len(part)):
   q=list(part);q[i]=tuple(sorted((first,)+q[i]));out.add(canon_blocks(tuple(q)))
 return tuple(sorted(out))
def interval():
 a,b=blocks_from_labels(TARGET);out=set()
 for pa in set_partitions(a):
  for pb in set_partitions(b):out.add(labels_from_blocks(pa+pb))
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


def fine_map():
 states=np.arange(2**N,dtype=np.uint32)
 bits=((states[:,None]>>np.arange(N,dtype=np.uint32))&1).astype(np.uint8)
 code=4*np.roll(bits,1,1)+2*bits+np.roll(bits,-1,1)
 lut=np.asarray([(RULE>>i)&1 for i in range(8)],dtype=np.uint8);o=lut[code]
 w=1<<np.arange(N,dtype=np.uint64)
 return (o.astype(np.uint64)*w).sum(1).astype(np.uint32)
def block_codes():
 states=np.arange(2**N,dtype=np.uint32)
 bits=((states[:,None]>>np.arange(N,dtype=np.uint32))&1).astype(np.uint8)
 b=bits.reshape(len(states),N//3,3)
 return (b*(1<<np.arange(3,dtype=np.uint8))).sum(2).astype(np.uint8)
CODES=block_codes()
def obs(p):
 lut=np.asarray(p,dtype=np.uint8);m=lut[CODES];base=len(set(p));w=np.asarray([base**i for i in range(N//3)],dtype=np.uint32)
 return (m.astype(np.uint32)*w).sum(1).astype(np.uint16)
def entropy(a):
 _,c=np.unique(a,return_counts=True);p=c/c.sum();return float(-(p*np.log2(p)).sum())
def future_class(step):
 target=obs(TARGET);s=np.arange(len(step),dtype=np.uint32);cols=[target.copy()]
 prev=len(np.unique(target))
 for t in range(1,128):
  s=step[s];cols.append(target[s]);word=np.stack(cols,axis=1)
  uniq,inv=np.unique(word,axis=0,return_inverse=True)
  if len(uniq)==prev:return inv.astype(np.int32),t-1
  prev=len(uniq)
 raise RuntimeError('target future did not stabilize')
def metrics(p,cinf):
 z=obs(p);hz=entropy(z);k=int(cinf.max())+1;joint=z.astype(np.uint64)*np.uint64(k)+cinf.astype(np.uint64)
 w=max(0.0,entropy(joint)-hz);closed=len(np.unique(joint))==len(np.unique(z))
 return {'H':hz,'W':w,'closed':closed}
def greedy(nodes):
 cur=TARGET;path=[cur]
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
def edge(a,b,nodes):
 dw=nodes[a]['W']-nodes[b]['W'];dh=nodes[b]['H']-nodes[a]['H'];return {'delta_W':dw,'delta_H':dh,'g':dw/dh}


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
 f=fine_map();step=f[f[f]];cinf,hstar=future_class(step);ints=interval();assert len(ints)==406
 nodes={p:metrics(p,cinf) for p in ints};ht=nodes[TARGET]['H']
 closed=[p for p in ints if nodes[p]['closed']];costs={p:nodes[p]['H']-ht for p in closed};gmin=min(costs.values())
 opts=sorted(p for p,c in costs.items() if abs(c-gmin)<TOL);path=greedy(nodes);gcost=nodes[path[-1]]['H']-ht
 zero=edge(TARGET,ZERO,nodes);direct=edge(TARGET,DIRECT,nodes);conditioned=edge(ZERO,CONDITIONED,nodes)
 checks={'greedy_suboptimal':gcost>gmin+TOL,'synergy_survives':conditioned['g']>direct['g']+TOL}
 out={'ok':all(checks.values()),'rule':RULE,'ring_width':N,'cadence':3,'target':''.join(map(str,TARGET)),'target_hstar':hstar,
      'target_W':nodes[TARGET]['W'],'interval_nodes':len(ints),'greedy_path':[''.join(map(str,p)) for p in path],
      'greedy_added_bits':gcost,'global_min_added_bits':gmin,'regret':gcost-gmin,'global_optima':[''.join(map(str,p)) for p in opts],
      'zero_bridge':{'partition':''.join(map(str,ZERO)),**zero},'same_split_before':{'partition':''.join(map(str,DIRECT)),**direct},
      'same_split_after_bridge':{'partition':''.join(map(str,CONDITIONED)),**conditioned},
      'gain_amplification':conditioned['g']/direct['g'] if abs(direct['g'])>1e-15 else None,
      'old_global_still_optimal':OLD_GLOBAL in opts,'old_greedy_still_endpoint':path[-1]==OLD_GREEDY,'checks':checks}
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
 if not out['ok']:raise SystemExit(1)
if __name__=='__main__':main()
