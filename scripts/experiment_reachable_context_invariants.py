"""Research033: exact generated reachable-context invariants for paired block-3 ECA dynamics."""
from __future__ import annotations
import argparse,hashlib,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(ROOT/'scripts'))
from experiment_causal_witness_automaton import PAIR_LIST,TARGETS,horizon_masks  # noqa:E402
from experiment_causal_witness_horizon import FULL_CLASS,macro_rule  # noqa:E402
A=8;PAIR_A=64;DIAGONAL=tuple(8*a+a for a in range(A));PROTOCOL='docs/research/protocols/reachable-context-invariants-20260909.md';NODE_BUDGET=5_000_000
VISIBLE_TARGET_MASK=[]
for u in range(A):
 for v in range(A):
  m=0
  for tid,t in enumerate(TARGETS):
   if t[u]!=t[v]:m|=1<<tid
  VISIBLE_TARGET_MASK.append(m)
def fh(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def congruence_requirements(g):
 out=[]
 for a in range(A):
  for b in range(A):
   m=0
   for x in range(A):
    for y in range(A):
     for u,v in ((int(g[64*a+8*x+y]),int(g[64*b+8*x+y])),(int(g[64*x+8*a+y]),int(g[64*x+8*b+y])),(int(g[64*x+8*y+a]),int(g[64*x+8*y+b]))):m|=1<<(8*u+v)
   out.append(m)
 return tuple(out)
def kernel(t):
 m=0
 for a in range(A):
  for b in range(A):
   if t[a]==t[b]:m|=1<<(8*a+b)
 return m
def congruence(req,t):
 r=kernel(t);rounds=0
 while True:
  n=0
  for c in range(64):
   bit=1<<c
   if r&bit and not(req[c]&~r):n|=bit
  rounds+=1
  if n==r:return r,rounds
  r=n
def paired_table(g):
 p=np.arange(64,dtype=np.int16);u=p//8;v=p%8;x=p[:,None,None];y=p[None,:,None];z=p[None,None,:]
 return (8*g[64*u[x]+8*u[y]+u[z]]+g[64*v[x]+8*v[y]+v[z]]).astype(np.uint8).reshape(-1)
def symbol_closure(ph,seed):
 s=np.asarray(sorted(set(DIAGONAL+(seed,))),dtype=np.int16);rounds=0
 while True:
  idx=(4096*s[:,None,None]+64*s[None,:,None]+s[None,None,:]).reshape(-1);n=np.unique(np.concatenate((s,ph[idx].astype(np.int16))));rounds+=1
  if len(n)==len(s):return s,rounds
  s=n
def edge_closure(ph,seed):
 e=np.zeros((64,64),dtype=bool);d=np.asarray(DIAGONAL,dtype=np.intp);e[np.ix_(d,d)]=True;e[d,seed]=True;e[seed,d]=True;rounds=0
 while True:
  n=e.copy()
  for p1,p2 in np.argwhere(e):
   pre=np.flatnonzero(e[:,p1]);post=np.flatnonzero(e[p2,:])
   if not len(pre) or not len(post):continue
   lo=np.unique(ph[4096*pre+64*p1+p2].astype(np.intp));hi=np.unique(ph[4096*p1+64*p2+post].astype(np.intp));n[np.ix_(lo,hi)]=True
  rounds+=1
  if np.array_equal(n,e):return e,rounds
  e=n
def visible_mask(symbols):
 m=0
 for s in symbols:m|=VISIBLE_TARGET_MASK[int(s)]
 return m
def witnesses(rule):
 c=[0]*len(PAIR_LIST)
 for h in range(4):c=[a|b for a,b in zip(c,horizon_masks(rule,h,NODE_BUDGET)['masks'])]
 return tuple(c)
def ids(mask):
 out=[]
 while mask:
  b=mask&-mask;out.append(b.bit_length()-1);mask^=b
 return out
def edge_hex(e):
 out=[]
 for row in e:
  m=0
  for j in np.flatnonzero(row):m|=1<<int(j)
  out.append(f'{m:016x}')
 return out
def scan(rule):
 g=macro_rule(rule);w=witnesses(rule);req=congruence_requirements(g);rels=[congruence(req,t)[0] for t in TARGETS];res={};absent=cc=0
 for tid,t in enumerate(TARGETS):
  r=rels[tid]
  for p,(a,b) in enumerate(PAIR_LIST):
   if (w[p]>>tid)&1:continue
   absent+=1
   if (r>>(8*a+b))&1:cc+=1
   else:res[p]=res.get(p,0)|(1<<tid)
 ph=paired_table(g);langs=[];sn=en=eo=rem=0
 for p,rm in sorted(res.items()):
  a,b=PAIR_LIST[p];seed=8*a+b;s,sr=symbol_closure(ph,seed);sm=visible_mask(s);sc=rm&~sm;e,er=edge_closure(ph,seed);verts=np.flatnonzero(e.any(0)|e.any(1));em=visible_mask(verts);ec=rm&~em;only=ec&~sc;left=rm&em
  if sc&~ec:raise AssertionError((rule,p,'hierarchy'))
  sn+=sc.bit_count();en+=ec.bit_count();eo+=only.bit_count();rem+=left.bit_count();langs.append({'pair_index':p,'pair':f'{a}-{b}','seed_symbol':seed,'residual_target_ids':ids(rm),'symbol_certified_target_ids':ids(sc),'edge_certified_target_ids':ids(ec),'edge_only_target_ids':ids(only),'unresolved_target_ids':ids(left),'generated_symbol_count':int(len(s)),'generated_symbols':[int(x) for x in s],'symbol_rounds':sr,'generated_edge_count':int(e.sum()),'edge_rows_hex':edge_hex(e),'edge_rounds':er})
 return {'rule':rule,'wclass':FULL_CLASS[rule],'finite_witness_absent_through_h3':absent,'congruence_certified':cc,'noncongruence_residual':sum(x.bit_count() for x in res.values()),'residual_seed_languages':len(res),'new_symbol_certificates':sn,'edge_certificates':en,'edge_only_certificates':eo,'remaining_after_edge':rem,'languages':langs}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--rule-start',type=int,default=0);ap.add_argument('--rule-end',type=int,default=256);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 if not(0<=a.rule_start<a.rule_end<=256):raise SystemExit('bad rule range')
 rows=[scan(r) for r in range(a.rule_start,a.rule_end)];out={'experiment':'reachable-context-invariants','schema':1,'rule_start':a.rule_start,'rule_end':a.rule_end,'block_size':3,'cadence':3,'targets':len(TARGETS),'source_hashes':{'scripts/experiment_reachable_context_invariants.py':fh(Path(__file__)),PROTOCOL:fh(ROOT/PROTOCOL)},'rows':rows};a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'rules':len(rows),'finite_absent':sum(r['finite_witness_absent_through_h3'] for r in rows),'congruence_certified':sum(r['congruence_certified'] for r in rows),'residual':sum(r['noncongruence_residual'] for r in rows),'new_symbol_certificates':sum(r['new_symbol_certificates'] for r in rows),'edge_certificates':sum(r['edge_certificates'] for r in rows),'remaining_after_edge':sum(r['remaining_after_edge'] for r in rows)},indent=2))
if __name__=='__main__':main()
