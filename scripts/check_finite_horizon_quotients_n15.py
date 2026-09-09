"""Fresh n=15 validation for Research030 finite-horizon quotient discovery."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(ROOT/'scripts'))
from experiment_history_lift_closure import state_map,compress  # noqa:E402
from experiment_contextual_quotient import TARGETS,pkey,local_entropy  # noqa:E402
N=15;BLOCK=3;M=5;A=8;STATES=np.arange(2**N,dtype=np.uint32)
CASES=[(101,'00000010',1,True),(106,'00000001',1,True),(110,'00000100',1,True),(90,'00110011',2,None),(24,'01000010',1,None),(184,'00000001',1,True)]
BYKEY={pkey(t):t for t in TARGETS}

def obs(target):
 lut=np.asarray(target,dtype=np.uint8);digits=((STATES[:,None]>>(BLOCK*np.arange(M,dtype=np.uint32)))&7).astype(np.uint8);macro=lut[digits];w=np.asarray([2**j for j in range(M)],dtype=np.uint16);return (macro.astype(np.uint16)*w).sum(1).astype(np.uint16)
def qfast(labels):
 x=np.asarray(labels,dtype=np.uint32).reshape((A,)*M);sm={};out=[]
 for a in range(A):
  sig=tuple(np.take(x,a,axis=M-1-j).tobytes() for j in range(M))
  if sig not in sm:sm[sig]=len(sm)
  out.append(sm[sig])
 return tuple(out)
def scan(rule,key,max_steps=256):
 target=BYKEY[key];e=state_map(rule,N);step=e[e[e]];y0=compress(obs(target));k=int(y0.max())+1;labels=y0.copy();count=int(labels.max())+1;s=STATES.copy();q=qfast(labels);changes=[{'h':0,'quotient':pkey(q),'classes':len(set(q)),'local_entropy':local_entropy(q)}]
 for t in range(1,max_steps+1):
  s=step[s];y=y0[s];new=compress(labels.astype(np.uint64)*np.uint64(k)+y.astype(np.uint64));nc=int(new.max())+1
  if nc==count:hstar=t-1;break
  labels=new;count=nc;qnew=qfast(labels)
  if qnew!=q:changes.append({'h':t,'quotient':pkey(qnew),'classes':len(set(qnew)),'local_entropy':local_entropy(qnew)})
  q=qnew
 else:raise RuntimeError('no stabilization')
 dq=changes[-1]['h'];return {'rule':rule,'target':key,'hstar':hstar,'quotient_discovery_time':dq,'final_quotient':pkey(q),'dq_over_hstar':dq/hstar if hstar else None,'change_chain':changes}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();rows=[]
 for rule,key,wantdq,wantearly in CASES:
  r=scan(rule,key);r['predicted_dq']=wantdq;r['dq_prediction_pass']=r['quotient_discovery_time']==wantdq;r['early_prediction_pass']=True if wantearly is None else (r['quotient_discovery_time']<r['hstar'])==wantearly;rows.append(r)
 primary=all(next(r for r in rows if r['rule']==rule)['quotient_discovery_time']==1 and next(r for r in rows if r['rule']==rule)['hstar']>1 for rule in (101,106,110))
 out={'ok':primary,'ring_width':N,'block_size':BLOCK,'cadence':3,'primary_long_memory_pass':primary,'rows':rows};args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
 if not primary:raise SystemExit(1)
if __name__=='__main__':main()
