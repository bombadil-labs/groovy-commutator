#!/usr/bin/env python3
"""Recover unreadable R3 cache files, preserving the frozen scientific procedure."""
import base64, hashlib, io, json, os, tarfile, time
from functools import lru_cache
from pathlib import Path
import numpy as np
from beam_loop_round02 import packed_physical, sha, save, ROOT, UNIT, ARCHIVE

def main():
 start=time.perf_counter(); out=ROOT/UNIT/'round03'
 hashes=json.loads((out/'freeze.json').read_text())
 assert all(sha(ROOT/p)==h for p,h in hashes.items())
 pairs={};needed={};bad={};manifest={}
 for w in (7,8):
  rows=np.load(ROOT/UNIT/f'round02/d3w{w}_pairs.npz')['rows'];pairs[w]=rows[rows[:,4]>0];needed[w]=set(map(int,pairs[w][:,:2].ravel()))
  for r in sorted(needed[w]):
   p=out/f'w{w}_r{r:03d}.npz'
   try:
    with np.load(p) as z:
     assert len(z['keys'])==len(z['values'])
   except Exception as e:bad[p.name]={'error':repr(e),'prior_bytes':p.stat().st_size if p.exists() else None}
 recovery={'failure':'Initial R3 comparison failed with EOFError; 31 cache files were empty on inspection. Root cause unknown; disk had 29GiB free. No scientific outputs were read before repair.','repair_script_sha256':sha(Path(__file__)),'bad_files':bad}
 save(out/'recovery-freeze.json',recovery)
 with tarfile.open(ARCHIVE,'r|gz') as tf:
  for m in tf:
   if not m.name.endswith('/d4.json'):continue
   parts=m.name.split('/');w=int(parts[0][1:]);r=int(parts[1][4:])
   if r not in needed[w]:continue
   raw=tf.extractfile(m).read();d=json.loads(raw);p=out/f'w{w}_r{r:03d}.npz'
   if p.name in bad:
    _,k,v=packed_physical(d);buf=io.BytesIO();np.savez_compressed(buf,keys=k,values=v)
    q=p.with_suffix('.repair');q.write_bytes(buf.getvalue());q.replace(p)
    with np.load(p) as z:assert np.array_equal(k,z['keys']) and np.array_equal(v,z['values'])
    print('repaired',p.name,'seconds',round(time.perf_counter()-start,1),flush=True)
   with np.load(p) as z:assert len(z['keys'])==d['forced_root_count']
   manifest[p.name]={'sha256':sha(p),'record':m.name,'record_sha256':hashlib.sha256(raw).hexdigest(),'keys':d['forced_root_count']}
 @lru_cache(maxsize=8)
 def table(w,r):
  with np.load(out/f'w{w}_r{r:03d}.npz') as z:return dict(zip((k.tobytes() for k in z['keys']),map(int,z['values'])))
 results={}
 for w,rows in pairs.items():
  result=[]
  for a,b,z,o,c in rows:
   a=int(a);b=int(b);p=table(w,a);q=table(w,b);shared=p.keys()&q.keys();badkeys=sorted(k for k in shared if p[k]!=q[k]);zero=sum(p[k]==q[k]==0 for k in shared);one=sum(p[k]==q[k]==1 for k in shared)
   result.append({'a':a,'b':b,'previous_conflicts':int(c),'shared_zero':zero,'shared_one':one,'conflicts':len(badkeys),'witness':None if not badkeys else {'physical_1080_bits_base64':base64.b64encode(badkeys[0]).decode(),'a':p[badkeys[0]],'b':q[badkeys[0]]}})
  results[str(w)]={'tested_pairs':len(rows),'persistent_pairs':sum(x['conflicts']>0 for x in result),'pairs':result}
 result={'source_hashes':hashes,'domains':results,'tables':manifest,'recovery':recovery,'recovery_seconds':time.perf_counter()-start,'initial_generation_seconds_lower_bound':215.7}
 save(out/'result.json',result);print(json.dumps({w:{k:v for k,v in x.items() if k!='pairs'} for w,x in results.items()}),flush=True)
if __name__=='__main__':main()
