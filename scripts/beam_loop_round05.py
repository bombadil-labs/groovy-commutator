#!/usr/bin/env python3
"""Prime-width recurrence validation and controlled local disturbance growth."""
import json,time
import numpy as np
from beam_loop_round02 import ROOT,UNIT,sha,save
from beam_loop_round04 import trajectory,recurrence,statistics,atomic_npz

def batch_step(x,r):
 return ((np.uint16(r)>>(4*np.roll(x,1,axis=-1)+2*x+np.roll(x,-1,axis=-1)).astype(np.uint16))&1).astype(np.uint8)

def damage(r,x,trials=16,horizon=256):
 w=len(x);assert 2*horizon+1<w;c=w//2
 sites=np.linspace(0,w-1,trials,dtype=int);a=np.stack([np.roll(x,c-int(j)) for j in sites]);b=a.copy();b[:,c]^=1
 rows=[];coords=np.arange(w)[None,:]
 for t in range(horizon+1):
  d=a^b;count=d.sum(axis=1);live=count>0
  lo=np.min(np.where(d,coords,w),axis=1);hi=np.max(np.where(d,coords,-1),axis=1);span=np.where(live,hi-lo+1,0)
  rows.append((float(live.mean()),float(count.mean()),float(span.mean())))
  if t<horizon:a=batch_step(a,r);b=batch_step(b,r)
 q=np.array(rows);growth=float(np.log2(q[256,2]/q[128,2])) if q[256,2]>0 and q[128,2]>0 else 0.
 return q,{'growth_128_256':growth,'checkpoints':{str(t):{'survival':q[t,0],'hamming':q[t,1],'diameter':q[t,2]} for t in (16,32,64,128,256)}}

def main():
 start=time.perf_counter();out=ROOT/UNIT/'round05';out.mkdir(parents=True,exist_ok=True);assert not(out/'result.json').exists()
 paths=('scripts/beam_loop_round05.py','scripts/beam_loop_round04.py','scripts/beam_loop_round02.py','src/groovy/ca.py',UNIT+'/round05-protocol.md',UNIT+'/round04/result.json')
 hashes={p:sha(ROOT/p) for p in paths};save(out/'freeze.json',hashes);old=json.loads((ROOT/paths[-1]).read_text());candidates=old['candidates'];results=[];packed={}
 for j,oldrow in enumerate(old['rules']):
  r=oldrow['rule']
  for w in (509,1021):
   for seed in (6041502,6041503,6041504):
    a=trajectory(r,seed,w,1024,520);rates=[float(recurrence(a,p,v,512).mean()) for p,v in candidates];i=int(np.argmin(rates));p,v=candidates[i]
    s=statistics(recurrence(a,p,v,512));f=float(a.mean());s.update(rule=r,width=w,seed=seed,p=p,v=v,one_density=f,normalized_density=s['density']/(2*f*(1-f)) if 0<f<1 else 0.,old_pair_density=float(recurrence(a,oldrow['p'],oldrow['v'],512).mean()))
    tag=f'w{w}_s{seed}_r{r:03d}';packed[tag]=np.packbits(a,axis=1,bitorder='big')
    if w==1021:q,ds=damage(r,a[0]);s['damage']=ds;packed[tag+'_damage']=q
    results.append(s)
  if (j+1)%16==0:print('rules',j+1,'seconds',round(time.perf_counter()-start,2),flush=True)
 atomic_npz(out/'trajectories.npz',**packed);d={'source_hashes':hashes,'rules':results,'seconds':time.perf_counter()-start,'raw_sha256':sha(out/'trajectories.npz')};save(out/'result.json',d);print('seconds',d['seconds'],flush=True)
if __name__=='__main__':main()
