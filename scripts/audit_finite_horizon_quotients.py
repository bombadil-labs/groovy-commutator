"""Independent explicit-context audit for Research030 quotient chains."""
from __future__ import annotations
import argparse,itertools,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(ROOT/'scripts'))
from experiment_history_lift_closure import state_map,compress  # noqa:E402
from experiment_contextual_quotient import TARGETS,pkey,refines  # noqa:E402
N=12;BLOCK=3;M=4;A=8;STATES=np.arange(2**N,dtype=np.uint32)
CASES=[(24,'01000010'),(90,'00110011'),(101,'00000010'),(106,'00000001'),(110,'00000100'),(184,'00000001')]
BYKEY={pkey(t):t for t in TARGETS}

def obs(target):
 lut=np.asarray(target,dtype=np.uint8);digits=((STATES[:,None]>>(BLOCK*np.arange(M,dtype=np.uint32)))&7).astype(np.uint8);macro=lut[digits];w=np.asarray([2**j for j in range(M)],dtype=np.uint16);return (macro.astype(np.uint16)*w).sum(1).astype(np.uint16)
def q_explicit(labels):
 sigmap={};out=[];coords=range(M)
 for a in range(A):
  sig=[]
  for j in coords:
   others=[k for k in coords if k!=j]
   for context in itertools.product(range(A),repeat=M-1):
    d=[0]*M;d[j]=a
    for k,v in zip(others,context):d[k]=v
    state=sum(d[k]<<(BLOCK*k) for k in coords);sig.append(int(labels[state]))
  sig=tuple(sig)
  if sig not in sigmap:sigmap[sig]=len(sigmap)
  out.append(sigmap[sig])
 return tuple(out)
def chain(rule,key,max_steps=128):
 target=BYKEY[key];e=state_map(rule,N);step=e[e[e]];y0=compress(obs(target));k=int(y0.max())+1;labels=y0.copy();count=int(labels.max())+1;s=STATES.copy();q=q_explicit(labels);changes=[{'h':0,'quotient':pkey(q)}]
 for t in range(1,max_steps+1):
  s=step[s];y=y0[s];new=compress(labels.astype(np.uint64)*np.uint64(k)+y.astype(np.uint64));nc=int(new.max())+1
  if nc==count:return {'hstar':t-1,'dQ':changes[-1]['h'],'final_quotient':pkey(q),'change_chain':changes}
  labels=new;count=nc;qnew=q_explicit(labels);assert refines(qnew,q)
  if qnew!=q:changes.append({'h':t,'quotient':pkey(qnew)})
  q=qnew
 raise RuntimeError('no stabilization')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--summary',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();summary=json.loads(args.summary.read_text());rows=[]
 expected={(24,'01000010'):(1,1,'01230243'),(90,'00110011'):(2,2,'01234567'),(101,'00000010'):(23,1,'01234567'),(106,'00000001'):(19,1,'01234567'),(110,'00000100'):(13,1,'01234567'),(184,'00000001'):(2,1,'01232445')}
 for case in CASES:
  got=chain(*case);eh,ed,eq=expected[case];ok=got['hstar']==eh and got['dQ']==ed and got['final_quotient']==eq;rows.append({'rule':case[0],'target':case[1],**got,'passes':ok});assert ok,rows[-1]
 assert summary['max_quotient_discovery_time']>=max(r['dQ'] for r in rows);assert summary['max_hstar']>=max(r['hstar'] for r in rows)
 out={'ok':all(r['passes'] for r in rows),'method':'explicit product-context enumeration, independent of tensor quotient helper','selected_checks':rows};args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
