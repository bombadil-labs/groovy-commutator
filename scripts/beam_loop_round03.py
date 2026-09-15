#!/usr/bin/env python3
"""Follow only the previously observed D3 incompatible pairs to D4."""
import base64,hashlib,json,tarfile,time
from functools import lru_cache
from pathlib import Path
import numpy as np
from beam_loop_round02 import packed_physical,sha,save,ROOT,UNIT,ARCHIVE

def main():
 start=time.perf_counter();out=ROOT/UNIT/'round03';out.mkdir(parents=True,exist_ok=True);assert not(out/'result.json').exists()
 ps=('scripts/beam_loop_round03.py','scripts/beam_loop_round02.py',UNIT+'/round03-protocol.md',UNIT+'/round02/d3w7_pairs.npz',UNIT+'/round02/d3w8_pairs.npz')
 hashes={p:sha(ROOT/p) for p in ps};save(out/'freeze.json',hashes)
 pairs={};needed={}
 for w in (7,8):
  rows=np.load(ROOT/UNIT/f'round02/d3w{w}_pairs.npz')['rows'];pairs[w]=rows[rows[:,4]>0];needed[w]=set(map(int,pairs[w][:,:2].ravel()))
 manifest={};done=0
 with tarfile.open(ARCHIVE,'r|gz') as tf:
  for m in tf:
   if not m.name.endswith('/d4.json'):continue
   parts=m.name.split('/');w=int(parts[0][1:]);r=int(parts[1][4:])
   if r not in needed[w]:continue
   raw=tf.extractfile(m).read();d=json.loads(raw);t,k,v=packed_physical(d);del t
   path=out/f'w{w}_r{r:03d}.npz';np.savez_compressed(path,keys=k,values=v)
   manifest[path.name]={'sha256':sha(path),'record':m.name,'record_sha256':hashlib.sha256(raw).hexdigest(),'keys':len(k)}
   done+=1
   if done%16==0:print('tables',done,'seconds',round(time.perf_counter()-start,1),flush=True)
 @lru_cache(maxsize=8)
 def table(w,r):
  d=np.load(out/f'w{w}_r{r:03d}.npz');return dict(zip((k.tobytes() for k in d['keys']),map(int,d['values'])))
 results={}
 for w,rows in pairs.items():
  result=[]
  for a,b,z,o,c in rows:
   a=int(a);b=int(b);p=table(w,a);q=table(w,b);shared=p.keys()&q.keys();bad=sorted(k for k in shared if p[k]!=q[k]);zero=sum(p[k]==q[k]==0 for k in shared);one=sum(p[k]==q[k]==1 for k in shared)
   result.append({'a':a,'b':b,'previous_conflicts':int(c),'shared_zero':zero,'shared_one':one,'conflicts':len(bad),'witness':None if not bad else {'physical_1080_bits_base64':base64.b64encode(bad[0]).decode(),'a':p[bad[0]],'b':q[bad[0]]}})
  results[str(w)]={'tested_pairs':len(rows),'persistent_pairs':sum(x['conflicts']>0 for x in result),'pairs':result}
 d={'source_hashes':hashes,'domains':results,'tables':manifest,'seconds':time.perf_counter()-start};save(out/'result.json',d)
 print(json.dumps({'seconds':d['seconds'],'domains':{w:{k:v for k,v in x.items() if k!='pairs'} for w,x in results.items()}}),flush=True)
if __name__=='__main__':main()
