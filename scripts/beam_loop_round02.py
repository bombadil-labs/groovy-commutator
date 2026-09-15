#!/usr/bin/env python3
"""Physical partial-table comparisons at D2 and D3."""
import base64,hashlib,json,tarfile,time
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]; UNIT='experiments/beam_discriminator_loop_20260915'
ARCHIVE=ROOT.parent/'gc-pilot/experiments/uniform_jet6_cache_20260914/run/uniform_jet6_rules.tar.gz'
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def save(p,d):Path(p).write_text(json.dumps(d,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n')
def unpack(s,shape):return np.unpackbits(np.frombuffer(base64.b64decode(s),dtype=np.uint8),bitorder='big')[:int(np.prod(shape))].reshape(shape)
def orbit(r):
 def refl(a):return sum(((a>>i)&1)<<(((i&1)<<2)|(i&2)|((i&4)>>2)) for i in range(8))
 def conj(a):return sum((1^((a>>(7-i))&1))<<i for i in range(8))
 return sorted({r,refl(r),conj(r),refl(conj(r))})
def packed_physical(record):
 g=unpack(record['grid_bits_big'],record['grid_shape']);radii=record['radii_array_order']
 reps=np.frombuffer(base64.b64decode(record['representative_flat_indices_u32le']),dtype='<u4');coords=np.unravel_index(reps,g.shape)
 offsets=list(np.ndindex(*(6 for _ in radii[:-1]),5)); bits=np.empty((len(reps),len(offsets)),dtype=np.uint8)
 for c,offset in enumerate(offsets):
  index=[coords[0]]+[ (coords[i+1]+offset[i]-(3 if i<len(radii)-1 else 2))%g.shape[i+1] for i in range(len(radii))]
  bits[:,c]=g[tuple(index)]
 packed=np.packbits(bits,axis=1,bitorder='big'); keys=[row.tobytes() for row in packed]
 assert len(set(keys))==len(reps)==record['forced_root_count']
 vals=unpack(record['forced_derivative_bits_big'],(len(reps),))
 return dict(zip(keys,map(int,vals))),packed,vals
def summarize(name,tables,out,labels):
 start=time.perf_counter();groups=[({q for q,v in t.items() if v==0},{q for q,v in t.items() if v==1}) for t in tables]
 rows=[];degree=np.zeros(256,dtype=int);occupied=degree.copy();frac=np.zeros(256);den=degree.copy()
 edge=np.eye(256,dtype=bool);vacant=0
 for a in range(256):
  az,ao=groups[a]
  for b in range(a+1,256):
   bz,bo=groups[b];z=len(az&bz);o=len(ao&bo);c=len(az&bo)+len(ao&bz);s=z+o+c;rows.append((a,b,z,o,c))
   if s:
    frac[a]+=c/s;frac[b]+=c/s;den[a]+=1;den[b]+=1
   if not c:
    edge[a,b]=edge[b,a]=True;degree[a]+=1;degree[b]+=1
    if s:occupied[a]+=1;occupied[b]+=1
    else:vacant+=1
 matrix=np.array(rows,dtype=np.uint32);np.savez_compressed(out/f'{name}_pairs.npz',rows=matrix)
 per=[{'rule':r,'forced':len(tables[r]),'degree':int(degree[r]),'occupied_degree':int(occupied[r]),'occupied_comparisons':int(den[r]),'mean_conflict_fraction':float(frac[r]/den[r]) if den[r] else None} for r in range(256)]
 spreads={}
 for key in ('degree','occupied_degree','mean_conflict_fraction'):
  spreads[key]=[{'root':r,'members':orbit(r),'range':float(max(per[s][key] for s in orbit(r))-min(per[s][key] for s in orbit(r)))} for r in range(256) if min(orbit(r))==r]
 by_class={c:{key:float(np.mean([per[r][key] for r in reps if r not in (41,106)])) for key in ('degree','occupied_degree','mean_conflict_fraction')} for c,reps in labels['representatives'].items()}
 summary={'compatible':int(degree.sum()//2),'vacuous':vacant,'occupied':int(occupied.sum()//2),'per_rule':per,'symmetry_spreads':spreads,'classes_core':by_class,'seconds':time.perf_counter()-start}
 return summary,edge
def main():
 start=time.perf_counter();out=ROOT/UNIT/'round02';out.mkdir(parents=True,exist_ok=True);assert not(out/'result.json').exists()
 paths=('scripts/beam_loop_round02.py',UNIT+'/round02-protocol.md',UNIT+'/round01/tables.npz','experiments/on_beam_256_4d_20260914/labels.json')
 sources={p:sha(ROOT/p) for p in paths};save(out/'freeze.json',sources)
 assert sha(ARCHIVE)=='766e4db7083fbdb551bc4aee66abc554079c5d118905f6d65aa5e5372c9418d1'
 labels=json.loads((ROOT/paths[-1]).read_text());tables={f'd{d}w{w}':[None]*256 for d in (2,3) for w in (7,8)};packed={};members={}
 with tarfile.open(ARCHIVE,'r|gz') as tf:
  for m in tf:
   if not m.name.endswith(('/d2.json','/d3.json')):continue
   raw=tf.extractfile(m).read();d=json.loads(raw);name=f'd{d["dimension"]}w{d["width"]}';t,ks,vs=packed_physical(d);tables[name][d['rule']]=t
   packed[f'{name}_r{d["rule"]:03d}_keys']=ks;packed[f'{name}_r{d["rule"]:03d}_values']=vs;members[m.name]=hashlib.sha256(raw).hexdigest()
 full=np.load(ROOT/UNIT/'round01/tables.npz');tables['d2full']=[]
 for r in range(256):
  ks=full[f'r{r:03d}_keys'];vals=full[f'r{r:03d}_native']-1;assert np.all(vals<=1)
  # Drop the last repeated five-bit row from full35-bit keys, then right-pad30 bits to4bytes.
  compressed=((ks>>5)<<2).astype('>u4').view(np.uint8).reshape(-1,4)
  tables['d2full'].append(dict(zip((x.tobytes() for x in compressed),map(int,vals))))
 for name in ('d2w7','d2w8'):
  for r in range(256): assert all(tables['d2full'][r].get(k)==v for k,v in tables[name][r].items())
 np.savez_compressed(out/'tables.npz',**packed)
 domains={};edges={}
 for name in tables:
  domains[name],edges[name]=summarize(name,tables[name],out,labels)
  print(name,{k:domains[name][k] for k in ('compatible','vacuous','occupied')},flush=True)
 upper=np.triu(np.ones((256,256),dtype=bool),1);changes={}
 for w in (7,8):
  a,b=edges[f'd2w{w}'],edges[f'd3w{w}'];changes[str(w)]={'lost':int(np.count_nonzero(upper&a&~b)),'gained':int(np.count_nonzero(upper&b&~a)),'shared':int(np.count_nonzero(upper&a&b))}
  assert not np.any(edges['d2full']&~a)
 result={'source_hashes':sources,'archive_member_hashes':members,'domains':domains,'cross_floor_changes':changes,'table_sha256':sha(out/'tables.npz'),'seconds':time.perf_counter()-start}
 save(out/'result.json',result);print('finished',result['seconds'],flush=True)
if __name__=='__main__':main()
