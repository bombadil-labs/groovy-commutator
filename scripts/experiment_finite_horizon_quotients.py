"""Research030: exact finite-horizon future-context quotient chains."""
from __future__ import annotations
import argparse,hashlib,json,statistics,sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(ROOT/'scripts'))
from experiment_history_lift_closure import FULL_CLASS,state_map,compress  # noqa:E402
from experiment_contextual_quotient import TARGETS,pkey,local_entropy,refines  # noqa:E402

N=12;BLOCK=3;M=N//BLOCK;A=8;TOL=1e-10
STATES=np.arange(2**N,dtype=np.uint32)
PROTOCOLS=[
 'docs/research/protocols/finite-horizon-quotients-20260909.md',
 'docs/research/protocols/finite-horizon-quotients-order-correction-20260909.md',
]
THRESHOLDS=(0.25,0.5,0.75,0.9,1.0)
FATAL={(24,'01000010'),(24,'01000110'),(231,'01000010'),(231,'01100010')}


def observation(target):
 lut=np.asarray(target,dtype=np.uint8)
 digits=((STATES[:,None]>>(BLOCK*np.arange(M,dtype=np.uint32)))&7).astype(np.uint8)
 macro=lut[digits];w=np.asarray([2**j for j in range(M)],dtype=np.uint16)
 return (macro.astype(np.uint16)*w).sum(1).astype(np.uint16)


def contextual_quotient(labels):
 """Exact context quotient via product-space tensor slices.

 State integers are base-8 local-block digits; block zero is the final tensor
 axis after reshape. A symbol signature contains the target-label slice for
 every exact surrounding context at every coordinate.
 """
 x=np.asarray(labels,dtype=np.uint32).reshape((A,)*M);sigmap={};out=[]
 for a in range(A):
  sig=tuple(np.take(x,a,axis=M-1-j).tobytes() for j in range(M))
  if sig not in sigmap:sigmap[sig]=len(sigmap)
  out.append(sigmap[sig])
 return tuple(out)


def scan_target(step,target,max_steps=128):
 y0=compress(observation(target));k=int(y0.max())+1
 labels=y0.copy();count=int(labels.max())+1;s=STATES.copy()
 q=contextual_quotient(labels);assert q==target,(pkey(target),pkey(q))
 q0e=local_entropy(q)
 changes=[{'h':0,'quotient':pkey(q),'classes':len(set(q)),'local_entropy':q0e}]
 births={f'{a}-{b}':(0 if q[a]!=q[b] else None) for a in range(A) for b in range(a+1,A)}
 hstar=None
 for t in range(1,max_steps+1):
  s=step[s];y=y0[s]
  new=compress(labels.astype(np.uint64)*np.uint64(k)+y.astype(np.uint64));nc=int(new.max())+1
  if nc==count:
   hstar=t-1;break
  labels=new;count=nc;qnew=contextual_quotient(labels)
  assert refines(qnew,q),('nonmonotone quotient',pkey(target),t,pkey(q),pkey(qnew))
  for a in range(A):
   for b in range(a+1,A):
    key=f'{a}-{b}'
    if births[key] is None and qnew[a]!=qnew[b]:births[key]=t
  if qnew!=q:changes.append({'h':t,'quotient':pkey(qnew),'classes':len(set(qnew)),'local_entropy':local_entropy(qnew)})
  q=qnew
 if hstar is None:raise RuntimeError(f'future partition did not stabilize by {max_steps}')
 qinf=q;dq=changes[-1]['h'];assert dq<=hstar
 final_e=local_entropy(qinf);rinf=final_e-q0e
 for a in range(A):
  for b in range(a+1,A):
   assert (births[f'{a}-{b}'] is not None)==(qinf[a]!=qinf[b])
 rho_h={str(x):0 for x in THRESHOLDS}
 if rinf>TOL:
  for threshold in THRESHOLDS:
   found=None
   for c in changes:
    if (c['local_entropy']-q0e)/rinf+TOL>=threshold:found=c['h'];break
   assert found is not None;rho_h[str(threshold)]=found
 for c in changes:
  c['global_encoder_entropy']=M*c['local_entropy']
  c['rho']=0.0 if rinf<=TOL else (c['local_entropy']-q0e)/rinf
 closed=(qinf==target);assert closed==(hstar==0),('closure mismatch',pkey(target),hstar,pkey(qinf))
 rec={'target':pkey(target),'closed':closed,'hstar':hstar,'final_quotient':pkey(qinf),'quotient_discovery_time':dq,
      'quotient_early':dq<hstar,'q0_local_entropy':q0e,'qinf_local_entropy':final_e,'final_added_local_bits':rinf,
      'final_added_global_bits':M*rinf,'change_chain':changes,'split_births':births,'rho_threshold_horizons':rho_h}
 if not closed:
  rec['dq_over_hstar']=dq/hstar
  rec['half_info_before_half_hstar']=rho_h['0.5']<(hstar/2)
  rec['quotient_by_half_hstar']=dq<=hstar/2
 return rec


def scan_rule(rule,max_steps=128):
 e=state_map(rule,N);step=e[e[e]];rows=[]
 for target in TARGETS:
  rec=scan_target(step,target,max_steps);rec['rule']=rule;rec['wclass']=FULL_CLASS[rule]
  if (rule,rec['target']) in FATAL:rec['fatal_bridge_1_6_birth']=rec['split_births']['1-6']
  rows.append(rec)
 return {'rule':rule,'wclass':FULL_CLASS[rule],'targets':rows}


def hashes():
 paths=[Path(__file__),*(ROOT/p for p in PROTOCOLS)]
 return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--rule-start',type=int,default=0);ap.add_argument('--rule-end',type=int,default=256);ap.add_argument('--max-steps',type=int,default=128);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
 if not(0<=args.rule_start<args.rule_end<=256):raise SystemExit('bad rule range')
 rows=[scan_rule(r,args.max_steps) for r in range(args.rule_start,args.rule_end)]
 allr=[t for r in rows for t in r['targets']];non=[t for t in allr if not t['closed']]
 out={'experiment':'finite-horizon-quotients','schema':1,'ring_width':N,'block_size':BLOCK,'cadence':3,
      'rule_start':args.rule_start,'rule_end':args.rule_end,'source_hashes':hashes(),'rows':rows}
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({'rules':len(rows),'targets':len(allr),'nonclosed':len(non),'early_quotient':sum(t['quotient_early'] for t in non),
                   'median_dq_over_hstar':statistics.median([t['dq_over_hstar'] for t in non]) if non else None},indent=2))

if __name__=='__main__':main()
