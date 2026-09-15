#!/usr/bin/env python3
"""Materialize ancestral jet fields and check macrocolumn support transport."""
import json,time
import numpy as np
from beam_loop_round02 import ROOT,UNIT,sha,save
from beam_loop_round04 import trajectory
from beam_loop_round05 import batch_step

def lift_series(a):
 x,y,z=a[:-2],a[1:-1],a[2:];f=np.roll(x,-1,axis=-1);b=np.roll(x,1,axis=-1)
 if x.ndim>2:f=np.roll(f,-1,axis=1);b=np.roll(b,-1,axis=1)
 d=x^y
 return np.stack((x^f,x^b,d,x^z,x&d,x&(1^d)),axis=1)

def support(a,b):
 d=a^b
 return d.astype(bool) if d.ndim==1 else np.any(d,axis=tuple(range(d.ndim-1)))

def inspect(a,b,tag):
 origin=support(a[0],b[0]);rows=[]
 for dim in range(1,7):
  if dim>1:
   pa,pb=a[0].copy(),b[0].copy();a=lift_series(a);b=lift_series(b)
   assert np.array_equal(a[0,4]^a[0,5],pa);assert np.array_equal(b[0,4]^b[0,5],pb)
  root_a=a[0];root_b=b[0]
  for _ in range(dim-1):root_a=root_a[4]^root_a[5];root_b=root_b[4]^root_b[5]
  actual=support(a[0],b[0]);assert np.array_equal(root_a^root_b,origin.astype(np.uint8))
  radius=2*(dim-1);upper=np.logical_or.reduce([np.roll(origin,k) for k in range(-radius,radius+1)])
  assert not np.any(origin&~actual);assert not np.any(actual&~upper)
  pos=np.flatnonzero(actual);src=np.flatnonzero(origin)
  row={**tag,'dimension':dim,'radius_bound':radius,'source_count':int(origin.sum()),'macrocolumn_count':int(actual.sum()),'physical_mismatch':float(np.mean(a[0]^b[0])),'support_checks':True}
  if tag['kind']=='perturbation':
   row.update(diameter=int(pos[-1]-pos[0]+1) if len(pos) else 0,left_extra=int(src[0]-pos[0]) if len(src) else 0,right_extra=int(pos[-1]-src[-1]) if len(src) else 0)
   assert row['left_extra']<=radius and row['right_extra']<=radius
  rows.append(row)
 return rows

def main():
 start=time.perf_counter();out=ROOT/UNIT/'round07';out.mkdir(parents=True,exist_ok=True);assert not(out/'result.json').exists()
 paths=('scripts/beam_loop_round07.py','scripts/beam_loop_round05.py','scripts/beam_loop_round04.py','scripts/beam_loop_round02.py','src/groovy/ca.py',UNIT+'/round07-protocol.md',UNIT+'/round04/result.json')
 hashes={p:sha(ROOT/p) for p in paths};save(out/'freeze.json',hashes);old={x['rule']:x for x in json.loads((ROOT/paths[-1]).read_text())['rules']};rows=[]
 for r in (0,18,54,73,110,126,204):
  a=trajectory(r,6041521,521,512,148);b=np.empty_like(a);b[0]=a[0];b[0,260]^=1
  for t in range(1,len(b)):b[t]=batch_step(b[t-1],r)
  p,v=old[r]['p'],old[r]['v']
  for t in (0,1,8,32,64,128):
   rows.extend(inspect(a[t:t+11],b[t:t+11],{'rule':r,'t':t,'kind':'perturbation'}))
   rows.extend(inspect(a[t:t+11],np.roll(a[t+p:t+p+11],-v,axis=-1),{'rule':r,'t':t,'kind':'recurrence','p':p,'v':v}))
  print('rule',r,'seconds',round(time.perf_counter()-start,2),flush=True)
 d={'source_hashes':hashes,'rows':rows,'seconds':time.perf_counter()-start,'all_support_checks':all(x['support_checks'] for x in rows)};save(out/'result.json',d);print('checks',len(rows),'seconds',d['seconds'],flush=True)
if __name__=='__main__':main()
