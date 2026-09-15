#!/usr/bin/env python3
"""Open-window mechanism adversary: a rare nonlinear correction to a shift."""
import json,time
import numpy as np
from beam_loop_round02 import ROOT,UNIT,sha,save
from beam_loop_round04 import atomic_npz

def open_step(x,r,correction=True):
 y=x[...,2*r:].copy()
 if correction:
  gate=np.ones_like(y)
  for j in range(2*r):gate&=x[...,j:j+y.shape[-1]]
  y^=gate
 return y

def damage(x,r,correction,width,horizon,trials):
 c=len(x)//2;sites=np.linspace(c-width//2,c+width//2,trials,dtype=int);pad=2*r*horizon
 a=np.stack([x[j-pad:j+pad+1] for j in sites]);assert a.shape==(trials,2*pad+1);b=a.copy();b[:,pad]^=1;curve=[]
 for t in range(horizon+1):
  d=a^b;ct=d.sum(axis=1);live=ct>0;coords=np.arange(d.shape[-1])[None,:];lo=np.min(np.where(d,coords,d.shape[-1]),axis=1);hi=np.max(np.where(d,coords,-1),axis=1);span=np.where(live,hi-lo+1,0)
  curve.append((float(live.mean()),float(ct.mean()),float(span.mean())))
  if t<horizon:a=open_step(a,r,correction);b=open_step(b,r,correction)
 curve=np.array(curve);alpha=float(np.log2(curve[-1,2]/curve[horizon//2,2])) if curve[-1,2]>0 and curve[horizon//2,2]>0 else 0.
 return curve,alpha

def analyze(r,correction,seed):
 width=4093;burn=2048;frames=1024;horizon=512;margin=8*r;keep=width+2*margin
 total=width+2*r*(burn+frames+8+2*horizon);x=(np.random.default_rng(seed).random(total)<.5).astype(np.uint8)
 for _ in range(burn):x=open_step(x,r,correction)
 at_burn=x.copy();a=np.empty((frames+8,keep),dtype=np.uint8)
 for t in range(len(a)):
  mid=len(x)//2;a[t]=x[mid-keep//2:mid+keep//2+1]
  if t<len(a)-1:x=open_step(x,r,correction)
 candidates=[(p,v) for p in range(1,9) for v in sorted(range(-r*p,r*p+1),key=lambda v:(abs(v),v))];rates=[]
 for p,v in candidates:rates.append(float(np.mean(a[:frames,margin:margin+width]^a[p:p+frames,margin+v:margin+v+width])))
 i=int(np.argmin(rates));f=float(a[:,margin:margin+width].mean());q=rates[i]/(2*f*(1-f));curve,alpha=damage(at_burn,r,correction,width,horizon,32)
 bits=a[:frames,margin:margin+width];keys=np.zeros((frames,width-7),np.uint8)
 for j in range(8):keys=(keys<<1)|bits[:,j:j+width-7]
 counts=np.bincount(keys.ravel(),minlength=256);freq=counts[counts>0]/counts.sum();entropy=float(-np.sum(freq*np.log2(freq))/8)
 one=rates[candidates.index((1,-r))];row={'radius':r,'correction':correction,'seed':seed,'width':width,'p':candidates[i][0],'v':candidates[i][1],'q':q,'alpha':alpha,'selected':bool(0<q<.5 and alpha>.5),'one_density':f,'block8_entropy_per_bit':entropy,'matched_shift_error':one,'theoretical_matched_error':2.**(-2*r) if correction else 0.,'final_damage':curve[-1].tolist()}
 if not correction:assert one==0 and q==0 and alpha==0 and curve[-1,2]==1
 return row,np.packbits(a,axis=1),curve

def symmetry_checks():
 n=0
 for r in range(256):
  refl=sum(((r>>i)&1)<<(((i&1)<<2)|(i&2)|((i&4)>>2)) for i in range(8));conj=sum((1^((r>>(7-i))&1))<<i for i in range(8))
  for i in range(8):
   j=((i&1)<<2)|(i&2)|((i&4)>>2);assert ((refl>>j)&1)==((r>>i)&1);assert ((conj>>(7-i))&1)==(1^((r>>i)&1));n+=2
 for i in range(8):assert (((i&1)^(((i>>1)&1)*((i>>2)&1))))==((106>>i)&1)
 return n

def main():
 start=time.perf_counter();out=ROOT/UNIT/'round10';out.mkdir(parents=True,exist_ok=True);assert not(out/'result.json').exists()
 paths=('scripts/beam_loop_round10.py','scripts/beam_loop_round04.py','scripts/beam_loop_round02.py',UNIT+'/round10-protocol.md')
 hashes={p:sha(ROOT/p) for p in paths};save(out/'freeze.json',hashes);checks=symmetry_checks();rows=[];packed={}
 for r in (1,2,3):
  for correction in (False,True):
   for seed in (6041541,6041542):
    row,a,curve=analyze(r,correction,seed);rows.append(row);tag=f'r{r}_g{int(correction)}_s{seed}';packed[tag]=a;packed[tag+'_damage']=curve;print(json.dumps(row),flush=True)
 atomic_npz(out/'trajectories.npz',**packed);d={'source_hashes':hashes,'rules':rows,'symmetry_identity_checks':checks,'seconds':time.perf_counter()-start,'raw_sha256':sha(out/'trajectories.npz')};save(out/'result.json',d);print('seconds',d['seconds'],flush=True)
if __name__=='__main__':main()
