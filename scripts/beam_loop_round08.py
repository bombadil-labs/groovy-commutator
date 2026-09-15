#!/usr/bin/env python3
"""Input-density stress test; candidate cutoffs remain those frozen at R6."""
import json,time
import numpy as np
from beam_loop_round02 import ROOT,UNIT,sha,save
from beam_loop_round04 import atomic_npz
from beam_loop_round06 import analyze

def main():
 start=time.perf_counter();out=ROOT/UNIT/'round08';out.mkdir(parents=True,exist_ok=True);assert not(out/'result.json').exists()
 paths=('scripts/beam_loop_round08.py','scripts/beam_loop_round06.py','scripts/beam_loop_round05.py','scripts/beam_loop_round04.py','scripts/beam_loop_round02.py','src/groovy/ca.py',UNIT+'/round08-protocol.md',UNIT+'/round04/result.json','experiments/on_beam_256_4d_20260914/labels.json')
 hashes={p:sha(ROOT/p) for p in paths};save(out/'freeze.json',hashes);old=json.loads((ROOT/paths[-2]).read_text());rows=[];packed={}
 for j,x in enumerate(old['rules']):
  r=x['rule']
  for density in (.1,.3,.7,.9):
   for seed in (6041531,6041532):
    row,a,curve=analyze(r,seed,2039,2048,1024,density,32,512,old['candidates']);rows.append(row);tag=f'd{int(density*10)}_s{seed}_r{r:03d}';packed[tag]=np.packbits(a,axis=1,bitorder='big');packed[tag+'_damage']=curve
  if (j+1)%16==0:print('rules',j+1,'seconds',round(time.perf_counter()-start,2),flush=True)
 counts={str(r):sum(x['selected'] for x in rows if x['rule']==r) for r in sorted(set(x['rule'] for x in rows))};selected=[int(r) for r,n in counts.items() if n>=5]
 atomic_npz(out/'trajectories.npz',**packed);d={'source_hashes':hashes,'rules':rows,'hit_counts':counts,'majority_selected':selected,'seconds':time.perf_counter()-start,'raw_sha256':sha(out/'trajectories.npz')};save(out/'result.json',d);print(json.dumps({'seconds':d['seconds'],'selected':selected,'nonzero_hit_counts':{r:n for r,n in counts.items() if n}}),flush=True)
if __name__=='__main__':main()
