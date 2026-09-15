#!/usr/bin/env python3
"""Finite empty-interval probabilities with explicit censoring and lift bounds."""
import json,time
import numpy as np
from beam_loop_round02 import ROOT,UNIT,sha,save
from beam_loop_round04 import recurrence
from beam_loop_round07 import lift_series
LENGTHS=(1,2,4,8,16,32,64,128,256)

def probabilities(d,lengths=LENGTHS):
 w=d.shape[-1];ls=sorted(set(lengths));assert max(ls)<=w
 ext=np.concatenate((d,d[:,:max(ls)-1]),axis=1);cs=np.pad(np.cumsum(ext,axis=1,dtype=np.int32),((0,0),(1,0)))
 return {str(l):{'count':int(np.count_nonzero(cs[:,l:l+w]==cs[:,:w])),'total':int(d.size)} for l in ls}

def tail_summary(d):
 counts=probabilities(d);p={k:x['count']/x['total'] for k,x in counts.items()}
 slopes={str(l):float((np.log(p[str(l)])-np.log(p[str(2*l)]))/l) if p[str(l)]>0 and p[str(2*l)]>0 else None for l in LENGTHS[:-1]}
 return {'intervals':counts,'slopes':slopes,'density':float(d.mean())}

def main():
 start=time.perf_counter();out=ROOT/UNIT/'round09';out.mkdir(parents=True,exist_ok=True);assert not(out/'result.json').exists()
 paths=('scripts/beam_loop_round09.py','scripts/beam_loop_round07.py','scripts/beam_loop_round04.py','scripts/beam_loop_round02.py',UNIT+'/round09-protocol.md',UNIT+'/round06/result.json',UNIT+'/round06/trajectories.npz')
 hashes={p:sha(ROOT/p) for p in paths};save(out/'freeze.json',hashes);old=json.loads((ROOT/paths[-2]).read_text());data=np.load(ROOT/paths[-1]);rows=[];transport=[]
 for row in old['rules']:
  r,seed,w,p,v=[row[k] for k in ('rule','seed','width','p','v')];tag=f's{seed}_r{r:03d}';a=np.unpackbits(data[tag],axis=1,bitorder='big')[:,:w];d=recurrence(a,p,v,1024)
  rows.append({'rule':r,'seed':seed,'p':p,'v':v,'alpha':row['alpha'],'q':row['q'],**tail_summary(d)})
  if seed==6041511 and r in (0,18,54,73,110,126,204):
   ga=a[:260];gb=np.roll(a[p:p+260],-v,axis=1);source=(ga[:256]^gb[:256]);source_probs=probabilities(source,[l+2*radius for l in LENGTHS for radius in (0,2,4)])
   for dim in (1,2,3):
    if dim>1:ga=lift_series(ga);gb=lift_series(gb)
    residual=(ga[:256]^gb[:256]);b=residual if dim==1 else np.any(residual,axis=tuple(range(1,residual.ndim-1))).astype(np.uint8);stats=tail_summary(b);radius=2*(dim-1)
    for l in LENGTHS:
     lower=source_probs[str(l+2*radius)]['count'];upper=source_probs[str(l)]['count'];actual=stats['intervals'][str(l)]['count'];assert lower<=actual<=upper
    transport.append({'rule':r,'dimension':dim,'radius':radius,'bounds_passed':True,**stats})
 d={'source_hashes':hashes,'rules':rows,'transport':transport,'seconds':time.perf_counter()-start};save(out/'result.json',d);print('seconds',d['seconds'],'transport',len(transport),flush=True)
if __name__=='__main__':main()
