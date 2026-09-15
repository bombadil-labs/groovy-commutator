#!/usr/bin/env python3
"""Independent larger-sample validation of the frozen R5 finite classifier."""
import json,time
import numpy as np
from beam_loop_round02 import ROOT,UNIT,sha,save
from beam_loop_round04 import trajectory,recurrence,atomic_npz
from beam_loop_round05 import batch_step

def damage(r,x,trials,horizon):
 w=len(x);assert 2*horizon+1<w;c=w//2;coords=np.arange(w)[None,:]
 sites=np.linspace(0,w-1,trials,dtype=int);a=np.stack([np.roll(x,c-int(j)) for j in sites]);b=a.copy();b[:,c]^=1;rows=[]
 for t in range(horizon+1):
  d=a^b;count=d.sum(axis=1);live=count>0;lo=np.min(np.where(d,coords,w),axis=1);hi=np.max(np.where(d,coords,-1),axis=1);span=np.where(live,hi-lo+1,0)
  rows.append((float(live.mean()),float(count.mean()),float(span.mean())))
  if t<horizon:a=batch_step(a,r);b=batch_step(b,r)
 q=np.array(rows);alpha=float(np.log2(q[horizon,2]/q[horizon//2,2])) if q[horizon,2]>0 and q[horizon//2,2]>0 else 0.
 return q,alpha

def analyze(r,seed,width,burn,frames,density,trials,horizon,candidates):
 a=trajectory(r,seed,width,burn,frames+8,density);rates=[float(recurrence(a,p,v,frames).mean()) for p,v in candidates];i=int(np.argmin(rates));p,v=candidates[i];f=float(a.mean());q=rates[i]/(2*f*(1-f)) if 0<f<1 else 0.
 curve,alpha=damage(r,a[0],trials,horizon)
 row={'rule':r,'seed':seed,'width':width,'burn':burn,'frames':frames,'initial_density':density,'p':p,'v':v,'mismatch':rates[i],'one_density':f,'q':q,'alpha':alpha,'selected':bool(0<q<.5 and alpha>.5),'final_damage':curve[-1].tolist()}
 return row,a,curve

def main():
 start=time.perf_counter();out=ROOT/UNIT/'round06';out.mkdir(parents=True,exist_ok=True);assert not(out/'result.json').exists()
 paths=('scripts/beam_loop_round06.py','scripts/beam_loop_round05.py','scripts/beam_loop_round04.py','scripts/beam_loop_round02.py','src/groovy/ca.py',UNIT+'/round06-protocol.md',UNIT+'/round04/result.json','experiments/on_beam_256_4d_20260914/labels.json')
 hashes={p:sha(ROOT/p) for p in paths};save(out/'freeze.json',hashes);old=json.loads((ROOT/paths[-2]).read_text());rows=[];packed={}
 for j,x in enumerate(old['rules']):
  r=x['rule']
  for seed in range(6041511,6041515):
   row,a,curve=analyze(r,seed,2039,2048,1024,.5,32,512,old['candidates']);rows.append(row);tag=f's{seed}_r{r:03d}';packed[tag]=np.packbits(a,axis=1,bitorder='big');packed[tag+'_damage']=curve
  if (j+1)%16==0:print('rules',j+1,'seconds',round(time.perf_counter()-start,2),flush=True)
 counts={str(r):sum(x['selected'] for x in rows if x['rule']==r) for r in sorted(set(x['rule'] for x in rows))};selected=[int(r) for r,n in counts.items() if n>=3]
 atomic_npz(out/'trajectories.npz',**packed);d={'source_hashes':hashes,'rules':rows,'hit_counts':counts,'majority_selected':selected,'seconds':time.perf_counter()-start,'raw_sha256':sha(out/'trajectories.npz')};save(out/'result.json',d);print(json.dumps({'seconds':d['seconds'],'selected':selected,'nonzero_hit_counts':{r:n for r,n in counts.items() if n}}),flush=True)
if __name__=='__main__':main()
