#!/usr/bin/env python3
"""Exhaustive nine-cell causal-window test of the first six-field lift."""
import base64, hashlib, json, platform, time
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
UNIT='experiments/beam_discriminator_loop_20260915'

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,d): Path(p).write_text(json.dumps(d,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n')
def step(x,r): return ((r>>(4*np.roll(x,1,-1)+2*x+np.roll(x,-1,-1)).astype(np.uint16))&1).astype(np.uint8)
def fields(x,y,z):
 d=x^y
 return np.stack((x^np.roll(x,-1,-1),x^np.roll(x,1,-1),d,x^z,x&d,x&(1^d)),axis=1)
def keys(g,col):
 q=np.zeros(g.shape[:2],dtype=np.uint64)
 for dy in range(-3,4):
  for dx in range(-2,3): q=(q<<1)|np.roll(g,-dy,axis=1)[:,:,col+dx]
 return q
def scalar(g,j,c):
 q=0
 for dy in range(-3,4):
  for dx in range(-2,3): q=(q<<1)|int(g[(j+dy)%6,c+dx])
 return q
def constrain(q,target):
 k,inv=np.unique(q,return_inverse=True); masks=np.zeros(len(k),dtype=np.uint8)
 np.bitwise_or.at(masks,inv.ravel(),(np.uint8(1)<<target.ravel()))
 bad=np.flatnonzero(masks==3); witness=None
 if len(bad):
  b=bad[0];events=[]
  for bit in (0,1):
   at=int(np.flatnonzero((inv.ravel()==b)&(target.ravel()==bit))[0]);s,j=np.unravel_index(at,q.shape)
   events.append({'source':int(s),'phase':int(j),'target':bit})
  witness={'key':int(k[b]),'events':events}
 return k,masks,{'conflicts':len(bad),'first_witness':witness}
def main():
 start=time.perf_counter();out=ROOT/UNIT/'round01';out.mkdir(parents=True,exist_ok=True)
 assert not (out/'result.json').exists()
 sources={p:sha(ROOT/p) for p in ('scripts/beam_loop_round01.py',UNIT+'/round01-protocol.md')};save(out/'freeze.json',sources)
 w=9;x=((np.arange(1<<w)[:,None]>>np.arange(w-1,-1,-1))&1).astype(np.uint8)
 rows=[];arrays={}
 for r in range(256):
  y=step(x,r);z=step(y,r);t=step(z,r);g=fields(x,y,z);h=fields(y,z,t);q=keys(g,4)
  for s in (0,173,511):
   for j in range(6): assert scalar(g[s],j,4)==int(q[s,j])
  k,m,native=constrain(q,(g^h)[:,:,4]);kd,md,decoder=constrain(q,np.broadcast_to(x[:,None,4],q.shape));assert np.array_equal(k,kd)
  arrays[f'r{r:03d}_keys']=k;arrays[f'r{r:03d}_native']=m;arrays[f'r{r:03d}_decoder']=md
  rows.append({'rule':r,'forced':len(k),'native':native,'decoder':decoder})
 np.savez_compressed(out/'tables.npz',**arrays)
 result={'source_hashes':sources,'width':9,'radius':[3,2],'roots':rows,'native_failed':[a['rule'] for a in rows if a['native']['conflicts']],
         'decoder_failed':[a['rule'] for a in rows if a['decoder']['conflicts']],
         'table_sha256':sha(out/'tables.npz'),'seconds':time.perf_counter()-start,'python':platform.python_version(),'numpy':np.__version__}
 save(out/'result.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ('roots','source_hashes')}))
if __name__=='__main__':main()
