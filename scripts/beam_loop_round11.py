#!/usr/bin/env python3
"""Extend R10 disturbance trials with exactly matching early lightcones."""
import json,time
import numpy as np
from beam_loop_round02 import ROOT,UNIT,sha,save
from beam_loop_round04 import atomic_npz
from beam_loop_round10 import open_step,damage

def main():
 start=time.perf_counter();out=ROOT/UNIT/'round11';out.mkdir(parents=True,exist_ok=True);assert not(out/'result.json').exists()
 paths=('scripts/beam_loop_round11.py','scripts/beam_loop_round10.py','scripts/beam_loop_round04.py','scripts/beam_loop_round02.py',UNIT+'/round11-protocol.md',UNIT+'/round10/result.json',UNIT+'/round10/trajectories.npz')
 hashes={p:sha(ROOT/p) for p in paths};save(out/'freeze.json',hashes);old=json.loads((ROOT/paths[-2]).read_text());raw=np.load(ROOT/paths[-1]);rows=[];packed={};width=4093;burn=2048;horizon=4096
 for row in old['rules']:
  if not row['correction']:continue
  r,seed=row['radius'],row['seed'];original_length=width+2*r*(burn+1024+8+2*512);x=(np.random.default_rng(seed).random(original_length)<.5).astype(np.uint8)
  required=width+4*r*horizon+2*r*burn;extra=(required-original_length)//2;assert 2*extra+original_length==required
  rng=np.random.default_rng(seed+100000000);x=np.r_[(rng.random(extra)<.5).astype(np.uint8),x,(rng.random(extra)<.5).astype(np.uint8)]
  for _ in range(burn):x=open_step(x,r,True)
  curve,_=damage(x,r,True,width,horizon,32);tag=f'r{r}_g1_s{seed}';assert np.array_equal(curve[:513],raw[tag+'_damage']);packed[tag+'_damage']=curve
  checkpoints={}
  for t in (512,1024,2048,4096):
   alpha=float(np.log2(curve[t,2]/curve[t//2,2])) if curve[t,2]>0 and curve[t//2,2]>0 else 0.;checkpoints[str(t)]={'alpha':alpha,'selected':bool(0<row['q']<.5 and alpha>.5),'survival':float(curve[t,0]),'diameter':float(curve[t,2]),'hamming':float(curve[t,1])}
  result={'radius':r,'seed':seed,'q':row['q'],'prefix_exact':True,'checkpoints':checkpoints};rows.append(result);print(json.dumps(result),flush=True)
 atomic_npz(out/'curves.npz',**packed);d={'source_hashes':hashes,'rules':rows,'seconds':time.perf_counter()-start,'raw_sha256':sha(out/'curves.npz')};save(out/'result.json',d);print('seconds',d['seconds'],flush=True)
if __name__=='__main__':main()
