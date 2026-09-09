"""Research029: direct future-context quotient and greedy safety margins.

Constructs the canonical minimum sufficient local representation directly from
future-context signatures. No global partition-interval search is used.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(ROOT/'scripts'))
from experiment_history_lift_closure import FULL_CLASS,state_map,compress  # noqa:E402

N=12;BLOCK=3;M=N//BLOCK;A=8;TOL=1e-10
PROTOCOLS=[
 'docs/research/protocols/contextual-quotient-20260908.md',
 'docs/research/protocols/contextual-quotient-cost-tie-20260908.md',
]
STATES=np.arange(2**N,dtype=np.uint32)
BITS=((STATES[:,None]>>np.arange(N,dtype=np.uint32))&1).astype(np.uint8)
BLOCKS=BITS.reshape(len(STATES),M,BLOCK)
CODES=(BLOCKS*(1<<np.arange(BLOCK,dtype=np.uint8))).sum(2).astype(np.uint8)


def canonicalize(p):
 remap={};out=[]
 for x in p:
  if x not in remap:remap[x]=len(remap)
  out.append(remap[x])
 return tuple(out)
def pkey(p):return ''.join(map(str,p))
def target_from_mask(mask):return canonicalize(tuple(0 if ((mask>>i)&1) else 1 for i in range(A)))
TARGETS=tuple(target_from_mask(mask) for mask in range(1,256) if (mask&1) and mask!=255)
assert len(TARGETS)==127

def blocks_of(p):
 d={}
 for i,x in enumerate(p):d.setdefault(x,[]).append(i)
 return tuple(tuple(v) for _,v in sorted(d.items()))
def labels_from_blocks(bs):
 bs=sorted([tuple(sorted(b)) for b in bs],key=lambda b:min(b));lab=[-1]*A
 for i,b in enumerate(bs):
  for x in b:lab[x]=i
 return canonicalize(tuple(lab))
def refines(fine,coarse):
 return all(fine[i]!=fine[j] or coarse[i]==coarse[j] for i in range(A) for j in range(A))

@lru_cache(maxsize=None)
def covers(p):
 out=set();bs=blocks_of(p)
 for ci,C in enumerate(bs):
  if len(C)<2:continue
  first=C[0];rest=C[1:]
  for mask in range(1<<len(rest)):
   left=(first,)+tuple(rest[j] for j in range(len(rest)) if (mask>>j)&1)
   if len(left)==len(C):continue
   ls=set(left);right=tuple(x for x in C if x not in ls);old=list(bs);old.pop(ci)
   out.add(labels_from_blocks(old+[left,right]))
 return tuple(sorted(out,key=pkey))

@lru_cache(maxsize=None)
def local_entropy(p):
 c=np.bincount(np.asarray(p,dtype=np.int16));c=c[c>0].astype(float);pr=c/A
 return float(-(pr*np.log2(pr)).sum())

class ObsCache:
 def __init__(self):self.cache={}
 def get(self,p):
  if p in self.cache:return self.cache[p]
  lut=np.asarray(p,dtype=np.uint8);mac=lut[CODES];k=len(set(p));w=np.asarray([k**i for i in range(M)],dtype=np.uint32)
  arr=(mac.astype(np.uint32)*w).sum(1).astype(np.uint16);self.cache[p]=arr;return arr

def entropy(labels):
 _,c=np.unique(labels,return_counts=True);pr=c/len(labels);return float(-(pr*np.log2(pr)).sum())

def target_future(step,target_obs,max_steps=128):
 y0=compress(target_obs);k=int(y0.max())+1;labels=y0.copy();count=k;s=STATES.copy()
 for t in range(1,max_steps+1):
  s=step[s];y=y0[s];new=compress(labels.astype(np.uint64)*np.uint64(k)+y.astype(np.uint64));nc=int(new.max())+1
  if nc==count:return labels,t-1
  labels=new;count=nc
 raise RuntimeError('future partition did not stabilize')

def contextual_quotient(cinf):
 sigmap={};out=[]
 for a in range(A):
  sig=tuple(tuple(cinf[CODES[:,j]==a].tolist()) for j in range(M))
  if sig not in sigmap:sigmap[sig]=len(sigmap)
  out.append(sigmap[sig])
 return canonicalize(tuple(out))

def metric(p,cinf,oc):
 z=oc.get(p);hz=M*local_entropy(p);k=int(cinf.max())+1;joint=z.astype(np.uint64)*np.uint64(k)+cinf.astype(np.uint64)
 w=max(0.0,entropy(joint)-hz);closed=len(np.unique(joint))==len(np.unique(z))
 return hz,w,closed

def choose(opts,policy):
 maxg=max(o['gain'] for o in opts)
 if policy=='canonical':return min(opts,key=lambda o:(-o['gain'],o['key']))
 tied=[o for o in opts if maxg-o['gain']<=TOL]
 if policy=='cost':return min(tied,key=lambda o:(o['cost'],o['key']))
 raise ValueError(policy)

def replay(target,cinf,qstar,oc,policy):
 cur=target;path=[pkey(cur)];steps=[];different_zero=0
 while cur!=qstar:
  h,w,_=metric(cur,cinf,oc);opts=[]
  for child in covers(cur):
   hc,wc,_=metric(child,cinf,oc);cost=hc-h;gain=(w-wc)/cost;safe=refines(qstar,child)
   opts.append({'partition':child,'key':pkey(child),'gain':gain,'cost':cost,'safe':safe})
  safe=[o for o in opts if o['safe']];unsafe=[o for o in opts if not o['safe']]
  bestsafe=max((o['gain'] for o in safe),default=math.inf)
  bestunsafe=max((o['gain'] for o in unsafe),default=-math.inf)
  margin=math.inf if not unsafe else bestsafe-bestunsafe
  picked=choose(opts,policy)
  steps.append({'from':pkey(cur),'to':picked['key'],'gain':picked['gain'],'cost':picked['cost'],'safe':picked['safe'],
                'margin':margin,'best_safe_gain':bestsafe,'best_unsafe_gain':bestunsafe})
  path.append(picked['key'])
  if not picked['safe']:
   return {'optimal':False,'path':path,'steps':steps,'first_unsafe':steps[-1]}
  cur=picked['partition']
 return {'optimal':True,'path':path,'steps':steps,'first_unsafe':None}

def quotient_sufficient(qstar,cinf,oc):
 return metric(qstar,cinf,oc)[2]

def scan_rule(rule):
 e=state_map(rule,N);step=e[e[e]];oc=ObsCache();rows=[]
 for target in TARGETS:
  tobs=oc.get(target);cinf,hstar=target_future(step,tobs);q=contextual_quotient(cinf)
  assert refines(q,target)
  assert quotient_sufficient(q,cinf,oc)
  target_closed=(q==target)
  if target_closed:
   rows.append({'rule':rule,'wclass':FULL_CLASS[rule],'target':pkey(target),'closed':True,'hstar':hstar,'quotient':pkey(q),
                'quotient_entropy':metric(q,cinf,oc)[0]});continue
  canonical=replay(target,cinf,q,oc,'canonical');cost=replay(target,cinf,q,oc,'cost')
  cmargins=[s['margin'] for s in canonical['steps'] if math.isfinite(s['margin'])]
  minmargin=min(cmargins,default=math.inf);minabs=min((abs(x) for x in cmargins),default=math.inf)
  zero_steps=sum(abs(x)<=TOL for x in cmargins);negative_steps=sum(x < -TOL for x in cmargins)
  rows.append({'rule':rule,'wclass':FULL_CLASS[rule],'target':pkey(target),'closed':False,'hstar':hstar,'quotient':pkey(q),
               'quotient_entropy':metric(q,cinf,oc)[0],'canonical_optimal':canonical['optimal'],'cost_optimal':cost['optimal'],
               'paths_differ':canonical['path']!=cost['path'],'canonical_path':canonical['path'],'cost_path':cost['path'],
               'canonical_min_margin':minmargin,'canonical_min_abs_margin':minabs,'canonical_zero_margin_steps':zero_steps,
               'canonical_strict_negative_steps':negative_steps,'canonical_first_unsafe':canonical['first_unsafe'],
               'cost_first_unsafe':cost['first_unsafe']})
 return {'rule':rule,'wclass':FULL_CLASS[rule],'targets':rows,'cached_observers':len(oc.cache)}

def hashes():
 paths=[Path(__file__),*(ROOT/p for p in PROTOCOLS)]
 return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--rule-start',type=int,default=0);ap.add_argument('--rule-end',type=int,default=256);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
 if not(0<=args.rule_start<args.rule_end<=256):raise SystemExit('bad rule range')
 rows=[scan_rule(r) for r in range(args.rule_start,args.rule_end)]
 out={'experiment':'contextual-quotient','schema':1,'ring_width':N,'block_size':BLOCK,'cadence':3,'rule_start':args.rule_start,'rule_end':args.rule_end,
      'source_hashes':hashes(),'rows':rows};args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2)+'\n')
 n=[t for r in rows for t in r['targets'] if not t['closed']]
 print(json.dumps({'rules':len(rows),'nonclosed':len(n),'canonical_failures':sum(not t['canonical_optimal'] for t in n),'cost_failures':sum(not t['cost_optimal'] for t in n)},indent=2))
if __name__=='__main__':main()
