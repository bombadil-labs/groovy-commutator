#!/usr/bin/env python3
"""Explore simple recurrence defects with the native ECA fixed."""
import io,json,sys,time
from pathlib import Path
import numpy as np
from beam_loop_round02 import ROOT,UNIT,sha,save
sys.path.insert(0,str(ROOT/'src'))
from groovy.ca import apply_rule

def trajectory(r,seed,width,burn,frames,density=.5):
 rng=np.random.default_rng(seed);x=(rng.random(width)<density).astype(np.uint8)
 for _ in range(burn):x=apply_rule(x,r)
 a=np.empty((frames,width),dtype=np.uint8)
 for t in range(frames):a[t]=x;x=apply_rule(x,r)
 return a

def recurrence(a,p,v,frames=None):
 if frames is None:frames=len(a)-p
 return a[:frames]^np.roll(a[p:p+frames],-v,axis=1)

def statistics(d):
 rho=float(d.mean());var=rho*(1-rho);cov={};cor={}
 for lag in (1,4,16):
  c=float(np.mean(d*np.roll(d,lag,axis=1)))-rho*rho
  cov[str(lag)]=c;cor[str(lag)]=c/var if var else 0.
 # Linear windows, no artificial run connecting across either boundary.
 runs=[]
 for row in d:
  z=np.r_[False,row==0,False];ends=np.flatnonzero(z[1:]!=z[:-1]);runs.extend((ends[1::2]-ends[::2]).tolist())
 return {'density':rho,'covariance':cov,'correlation':cor,'zero_run_mean':float(np.mean(runs)) if runs else 0.,'zero_run_max':max(runs,default=0)}

def atomic_npz(p,**arrays):
 b=io.BytesIO();np.savez_compressed(b,**arrays);q=p.with_suffix('.tmp');q.write_bytes(b.getvalue());q.replace(p)

def main():
 start=time.perf_counter();out=ROOT/UNIT/'round04';out.mkdir(parents=True,exist_ok=True);assert not(out/'result.json').exists()
 paths=('scripts/beam_loop_round04.py','scripts/beam_loop_round02.py','src/groovy/ca.py',UNIT+'/round04-protocol.md','experiments/on_beam_256_4d_20260914/labels.json')
 hashes={p:sha(ROOT/p) for p in paths};save(out/'freeze.json',hashes)
 labels=json.loads((ROOT/paths[-1]).read_text());reps=sorted(r for rr in labels['representatives'].values() for r in rr)
 candidates=[(p,v) for p in range(1,9) for v in sorted(range(-p,p+1),key=lambda v:(abs(v),v))]
 results=[];packed={}
 for r in reps:
  a=trajectory(r,6041501,512,512,520);rates=[float(recurrence(a,p,v,512).mean()) for p,v in candidates];i=int(np.argmin(rates));p,v=candidates[i]
  stats=statistics(recurrence(a,p,v,512));stats.update(rule=r,p=p,v=v,candidate_rates=rates,raw_activity=float((a[1:]^a[:-1]).mean()))
  results.append(stats);packed[f'r{r:03d}']=np.packbits(a,axis=1,bitorder='big')
 atomic_npz(out/'trajectories.npz',**packed)
 d={'source_hashes':hashes,'seed':6041501,'width':512,'burn':512,'frames':520,'candidates':candidates,'rules':results,'trajectory_sha256':sha(out/'trajectories.npz'),'seconds':time.perf_counter()-start}
 save(out/'result.json',d);print('seconds',d['seconds']);print(json.dumps(sorted(results,key=lambda x:-x['covariance']['16'])[:15]))
if __name__=='__main__':main()
