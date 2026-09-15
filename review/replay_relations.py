#!/usr/bin/env python3
"""Independent direct-coordinate replay; deliberately imports no primary code."""
import argparse,base64,hashlib,itertools,json,resource,tarfile,time
from pathlib import Path
import numpy as np

PANEL=(0,4,18,30,54,90,110,124,126,137,147,193,204)
BASE=Path(__file__).resolve().parents[1]
OLD=Path('/workspace/scratch/1815be08ff33')
ARCHIVE=OLD/'gc-pilot/experiments/uniform_jet6_cache_20260914/run/uniform_jet6_rules.tar.gz'
MANIFEST=ARCHIVE.with_name('archive_manifest.json')
FULL=OLD/'gc-discriminator/experiments/beam_discriminator_loop_20260915/round01/tables.npz'
PRIOR=BASE/'results/commutator_completion_20260915.json'
OUT=BASE/'review/replay'

def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def save(path,value):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 temp=path.with_suffix(path.suffix+'.tmp');temp.write_text(json.dumps(value,sort_keys=True,separators=(',',':'))+'\n');temp.replace(path)
def bits(data,shape):
 b=np.unpackbits(np.frombuffer(base64.b64decode(data,validate=True),np.uint8),bitorder='big');n=int(np.prod(shape));assert not b[n:].any();return b[:n].reshape(shape)
def rows(x):
 x=np.ascontiguousarray(x);return x.view('V'+str(x.shape[1])).ravel()
def exact_keys(grid,events,whole=False):
 """Gather literal relative coordinates then bit-pack, with no key DAG."""
 shape=grid.shape;d=grid.ndim-1
 offsets=np.array(list(itertools.product(*([range(6)]*(d-1)+[range(shape[-1]) if whole else range(-2,3)]))),dtype=np.int32)
 coords=np.array(np.unravel_index(events,shape),dtype=np.int32).T
 nbytes=(len(offsets)+7)//8;result=np.empty((len(events),nbytes),np.uint8)
 for start in range(0,len(events),1024):
  cs=coords[start:start+1024];index=np.broadcast_to(cs[:,0,None],(len(cs),len(offsets))).copy()
  for ax in range(d):index=index*shape[ax+1]+(cs[:,ax+1,None]+offsets[None,:,ax])%shape[ax+1]
  result[start:start+len(cs)]=np.packbits(grid.ravel()[index],axis=1,bitorder='big')
 return rows(result)
def find(keys,values,query):
 p=np.searchsorted(keys,query);ok=p<len(keys);p=np.minimum(p,len(keys)-1);ok &=keys[p]==query
 v=np.zeros(len(query),np.uint8);v[ok]=values[p[ok]];return ok,v

def summarize(s,c):
 s=s.ravel();c=c.ravel();u=int(s.max()) if len(s) else 0
 labels=np.unique(s[s>0]);equal=opposite=0
 for label in labels:
  z=int(np.sum((s==label)&(c==0)));o=int(np.sum((s==label)&(c==1)))
  equal+=z*(z-1)//2+o*(o-1)//2;opposite+=z*o
 return dict(events=len(s),ambiguous=int(np.sum(s>0)),variables=len(labels),rank=int(np.sum(s>0))-len(labels),equal_pairs=equal,opposite_pairs=opposite,fixed_zero=int(np.sum((s==0)&(c==0))),fixed_one=int(np.sum((s==0)&(c==1))))

def summarize_fast(s,c):
 s=s.ravel();c=c.ravel();length=int(s.max())+1
 totals=np.bincount(s,minlength=length)[1:].astype(np.int64)
 ones=np.bincount(s[c==1],minlength=length)[1:].astype(np.int64);zeros=totals-ones
 return dict(events=len(s),ambiguous=int(totals.sum()),variables=int(np.sum(totals>0)),rank=int(totals.sum()-np.sum(totals>0)),equal_pairs=int(np.sum(zeros*(zeros-1)//2+ones*(ones-1)//2)),opposite_pairs=int(np.sum(zeros*ones)),fixed_zero=int(np.sum((s==0)&(c==0))),fixed_one=int(np.sum((s==0)&(c==1))))

def full_d2(full,rule):
 k=full[f'r{rule:03d}_keys'];v=(full[f'r{rule:03d}_native']-1).astype(np.uint8)
 # Source integer order is seven rows at offsets -3..3. Drop repeated row,
 # rotate transverse order to offsets 0..5, matching literal coordinate keyer.
 b=((k[:,None]>>np.arange(34,-1,-1,dtype=np.uint64))&1).astype(np.uint8).reshape(-1,7,5)
 b=b[:,[3,4,5,0,1,2],:].reshape(-1,30)
 keys=rows(np.packbits(b,axis=1,bitorder='big'));order=np.argsort(keys)
 assert len(np.unique(keys))==len(keys)
 return keys[order],v[order]

def audit(record,full,prior):
 w=record['width'];d=record['dimension'];r=record['rule'];ident=f'w{w}_r{r:03d}_d{d}'
 shape=(1<<w,)+(6,)*(d-1)+(w,);assert record['grid_shape']==list(shape)
 grid=bits(record['grid_bits_big'],shape)
 events=np.arange(0,grid.size,w,dtype=np.int32)
 q=exact_keys(grid,events)
 reps=np.frombuffer(base64.b64decode(record['representative_flat_indices_u32le'],validate=True),dtype='<u4')
 rk=exact_keys(grid,reps);rv=bits(record['forced_derivative_bits_big'],(len(reps),))
 sort=np.argsort(rk);rk=rk[sort];rv=rv[sort]
 assert len(np.unique(rk))==len(rk)==record['forced_root_count']
 assert np.array_equal(np.unique(q),rk)
 ok,v=find(rk,rv,q);assert ok.all();v=v.reshape(shape[:-1])
 root=grid
 for _ in range(d-1):root=root[:,4]^root[:,5]
 family={x.tobytes():i for i,x in enumerate(root)};assert len(family)==1<<w
 delta=np.empty_like(grid)
 for x in range(w):
  shift=np.array([family[y.tobytes()] for y in np.roll(root,-x,axis=-1)])
  assert np.array_equal(grid[shift],np.roll(grid,-x,axis=-1))
  delta[...,x]=v[shift]
 whole_family={x.tobytes():i for i,x in enumerate(grid)};assert len(whole_family)==1<<w
 successor=grid^delta
 next_idx=np.array([whole_family[x.tobytes()] for x in successor])
 lut=np.array([(r>>i)&1 for i in range(8)],np.uint8)
 expected=lut[4*np.roll(root,1,axis=-1)+2*root+np.roll(root,-1,axis=-1)]
 assert np.array_equal(root[next_idx],expected)
 t=(grid^grid[next_idx[next_idx]])[...,0].ravel()
 dq=exact_keys(delta,events)
 fullkeys=exact_keys(grid,events,whole=True)
 unique,representatives,orbit=np.unique(fullkeys,return_index=True,return_inverse=True)
 contracts={'finite':(rk,rv)}
 if d==2:contracts['full_input_d2']=full_d2(full,r)
 out={'id':ident,'dimension':d,'rule':r,'width':w,'spatial_orbits':len(unique),'longitudinal_events':len(q),'contracts':{}}
 arrays={'orbit_ids':orbit.reshape(shape[:-1]),'representatives':representatives,'grid_shape':np.array(shape)}
 for name,(keys,values) in contracts.items():
  known,value=find(keys,values,dq);constant=t^value
  free=np.unique(dq[~known]);symbol=np.zeros(len(dq),np.int32);symbol[~known]=np.searchsorted(free,dq[~known])+1
  assert np.array_equal(symbol,symbol[representatives][orbit])
  assert np.array_equal(constant,constant[representatives][orbit])
  long=summarize_fast(symbol,constant);spatial=summarize_fast(symbol[representatives],constant[representatives])
  old=prior[(ident,name)]
  assert long['ambiguous']*w==old['free_cells']
  assert long['variables']==old['free_keys']
  assert long['fixed_zero']*w==old['fixed_zero'] and long['fixed_one']*w==old['fixed_one']
  assert long['equal_pairs']*w*w+long['ambiguous']*w*(w-1)//2==old['equal_G_pairs_from_shared_variable']
  assert long['opposite_pairs']*w*w==old['opposite_G_pairs_from_shared_variable']
  out['contracts'][name]={'longitudinal':long,'spatial':spatial}
  arrays[name+'_symbol']=symbol.reshape(shape[:-1]);arrays[name+'_constant']=constant.reshape(shape[:-1])
 return out,arrays

def transfer(parent,child,pa,ca,contract):
 ps=pa[contract+'_symbol'].ravel()[pa['representatives']]
 pc=pa[contract+'_constant'].ravel()[pa['representatives']]
 pid=pa['orbit_ids'].ravel();cp=ca['orbit_ids'];reps=pa['representatives']
 checks=[]
 for phase in range(6):
  mapped=cp[:,phase].ravel();f=mapped[reps]
  checks.append({'well_defined':bool(np.array_equal(mapped,f[pid])),'injective':len(np.unique(f))==len(f)})
 group={}
 for i,s in enumerate(ps):
  if s:group.setdefault(int(s),[]).append(i)
 denominator=sum(len(g)*(len(g)-1)//2 for g in group.values())
 cs=ca['finite_symbol'];cc=ca['finite_constant']
 outputs=[]
 for phases in [(0,),(1,),(2,),(3,),(4,),(5,),(4,5)]:
  valid=all(checks[j]['well_defined'] and checks[j]['injective'] for j in phases)
  counts={'fixed_agree':0,'fixed_reverse':0,'free_agree':0,'free_reverse':0}
  example=None
  if valid:
   ss=[cs[:,j].ravel()[reps] for j in phases];constant=np.bitwise_xor.reduce([cc[:,j].ravel()[reps] for j in phases])
   signatures=[]
   for i in range(len(ps)):
    support=set()
    for vec in ss:
     if vec[i]:
      if int(vec[i]) in support:support.remove(int(vec[i]))
      else:support.add(int(vec[i]))
    signatures.append(tuple(sorted(support)))
   for indices in group.values():
    subgroups={}
    for i in indices:subgroups.setdefault(signatures[i],[]).append(i)
    for signature,ids in subgroups.items():
     n=len(ids);v=pc[ids]^constant[ids];one=int(v.sum());zero=n-one
     agree=one*(one-1)//2+zero*(zero-1)//2;reverse=one*zero;kind='free' if signature else 'fixed'
     counts[kind+'_agree']+=agree;counts[kind+'_reverse']+=reverse
     if n>=2 and example is None:example={'parent_orbits':[int(ids[0]),int(ids[1])],'parent_parity':int(pc[ids[0]]^pc[ids[1]]),'child_parity':int(constant[ids[0]]^constant[ids[1]]),'nonempty_support':bool(signature)}
  outputs.append({'phases':list(phases),'valid_map':valid,'denominator':denominator,'survival':sum(counts.values()) if valid and denominator else None,**counts,'example':example})
 blocks=np.moveaxis(cs,1,-1).reshape(-1,6)
 nfree=(blocks>0).sum(axis=1);allfree=int(np.sum(nfree==6));allfixed=int(np.sum(nfree==0));mixed=int(np.sum((nfree>0)&(nfree<6)))
 unique_free=np.unique(cs[cs>0]);distinct=len(unique_free)==int(np.sum(cs>0))
 zero_rank=child['contracts']['finite']['longitudinal']['rank']==0
 assert zero_rank==distinct
 return {'parent':parent['id'],'child':child['id'],'parent_contract':contract,'map_checks':checks,'readouts':outputs,'sibling_no_go':{'child_longitudinal_zero_rank':zero_rank,'all_free_blocks':allfree,'all_fixed_blocks':allfixed,'mixed_blocks':mixed,'distinct_free_variables':distinct,'conditions_verified':bool(zero_rank and not mixed),'nonvacuous_all_free_comparison':allfree>=2}}

def controls():
 # Compare packed keys against scalar physical coordinates including wrap.
 g=(np.arange(3*6*6*7).reshape(3,6,6,7)%3==0).astype(np.uint8)
 for whole in (False,True):
  events=np.array([0,7,88,g.size-1]);actual=exact_keys(g,events,whole)
  offsets=list(itertools.product(range(6),range(6),range(7) if whole else range(-2,3)))
  for event,key in zip(events,actual):
   source,y,z,x=np.unravel_index(event,g.shape)
   literal=[g[source,(y+dy)%6,(z+dz)%6,(x+dx)%7] for dy,dz,dx in offsets]
   assert bytes(key)==np.packbits(literal,bitorder='big').tobytes()
 for w in (2,3,7,8):
  s=np.array([1,1,1,2,2,0]);c=np.array([0,0,1,0,1,1],np.uint8)
  a=summarize_fast(s,c);b=summarize_fast(np.repeat(s,w),np.repeat(c,w))
  assert b['equal_pairs']==w*w*a['equal_pairs']+a['ambiguous']*w*(w-1)//2
  assert b['opposite_pairs']==w*w*a['opposite_pairs']
 return {'literal_key_cases':8,'translation_formula_cases':4}

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--controls-only',action='store_true');args=parser.parse_args()
 control=controls()
 if args.controls_only:print(json.dumps(control));return
 OUT.mkdir(parents=True,exist_ok=True);assert not (OUT/'result.json').exists()
 prior=json.loads(PRIOR.read_text());pins=prior['raw_input_hashes']
 assert sha(ARCHIVE)==pins[ARCHIVE.name];assert sha(FULL)==pins['experiments/beam_discriminator_loop_20260915/round01/tables.npz'];assert sha(MANIFEST)==pins[MANIFEST.name]
 manifest={x['path']:x for x in json.loads(MANIFEST.read_text())['members']}
 p={(x['id'],x['contract']):x for x in prior['records']}
 # Input recovery is excluded from the ten-minute scientific budget.
 selected=[]
 with tarfile.open(ARCHIVE,'r|gz') as tar:
  for member in tar:
   if not member.isfile() or not member.name.endswith(('/d2.json','/d3.json','/d4.json')):continue
   # Names alone prune most entries before decompression into JSON.
   if not any('/rule'+str(r).zfill(3)+'/' in '/'+member.name for r in PANEL):continue
   raw=tar.extractfile(member).read();record=json.loads(raw)
   if record['rule'] not in PANEL:continue
   assert hashlib.sha256(raw).hexdigest()==manifest[member.name]['sha256'];selected.append(record)
 assert len(selected)==78,len(selected)
 selected.sort(key=lambda x:(x['width'],x['rule'],x['dimension']))
 start=time.monotonic();results=[];transfers=[];case_arrays={};case_results={}
 with np.load(FULL) as full:
  for record in selected:
   if time.monotonic()-start>600:break
   before=time.monotonic();result,arrays=audit(record,full,p)
   ident=result['id'];results.append(result);case_arrays[ident]=arrays;case_results[ident]=result
   np.savez_compressed(OUT/(ident+'.npz'),**arrays);save(OUT/(ident+'.json'),result)
   d=record['dimension'];parent_id=f'w{record["width"]}_r{record["rule"]:03d}_d{d-1}'
   if d>2:
    pr=case_results[parent_id];pa=case_arrays[parent_id]
    for contract in pr['contracts']:transfers.append(transfer(pr,result,pa,arrays,contract))
    del case_arrays[parent_id]
   if d==4:del case_arrays[ident]
   assert resource.getrusage(resource.RUSAGE_SELF).ru_maxrss<2*1024*1024
   print(json.dumps({'completed':len(results),'id':ident,'case_seconds':round(time.monotonic()-before,3),'seconds':round(time.monotonic()-start,3)}),flush=True)
  complete=len(results)==78
  result={'reviewer':'Codex (OpenAI), /root/relations_review','source_sha256':sha(__file__),'input_hashes':pins,'controls':control,'complete':complete,'records':results,'transfers':transfers,'seconds':time.monotonic()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
  save(OUT/('result.json' if complete else 'censored.json'),result)
  print(json.dumps({k:v for k,v in result.items() if k not in ('records','transfers')}))
if __name__=='__main__':main()
