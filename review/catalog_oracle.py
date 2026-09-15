#!/usr/bin/env python3
"""Independent observation-catalog primitives and metrics; no primary imports."""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
import hashlib,itertools,json,math,resource,time
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
UNIT=ROOT/'experiments/observation_catalog_20260915'
PANEL=(0,4,18,30,54,90,110,147)
CANDIDATES=[(i,) for i in range(24)]+list(itertools.combinations(range(24),2))
NATIVE=[i for i in range(24) if i not in (14,15,16,18)]
NATIVE_CANDIDATES=[(i,) for i in NATIVE]+list(itertools.combinations(NATIVE,2))
TOL=1e-10


def digest(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for block in iter(lambda:f.read(1<<20),b''):h.update(block)
 return h.hexdigest()
def save(path,obj):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+'\n');tmp.replace(path)
def shifted(a,offset):
 return np.take(a,(np.arange(a.shape[-1])+offset)%a.shape[-1],axis=-1)
def word_step(rule,states,width):
 """Independent packed-integer finite-ring update, vectorized over all states."""
 states=np.asarray(states,dtype=np.uint32);out=np.zeros_like(states)
 for x in range(width):
  neighborhood=4*((states>>((x-1)%width))&1)+2*((states>>x)&1)+((states>>((x+1)%width))&1)
  out|=((int(rule)>>neighborhood)&1)<<x
 return out.astype(np.uint16)
def unpack(states,width):return ((np.asarray(states)[:,None]>>np.arange(width))&1).astype(np.uint8)
def field_step(rule,x):
 if rule=='radius2':return shifted(x,2)^(shifted(x,-2)&shifted(x,-1)&x&shifted(x,1))
 indices=4*shifted(x,-1)+2*x+shifted(x,1)
 return ((int(rule)>>indices)&1).astype(np.uint8)
def sensitivities(rule,x):
 if rule=='radius2':
  return np.stack((shifted(x,-2)&x&shifted(x,1),shifted(x,-2)&shifted(x,-1)&shifted(x,1),shifted(x,-2)&shifted(x,-1)&x))
 idx=4*shifted(x,-1)+2*x+shifted(x,1);u=((int(rule)>>idx)&1).astype(np.uint8)
 return np.stack([u^((int(rule)>>(idx^mask))&1).astype(np.uint8) for mask in (4,2,1)])
def primitives(rule,x,u=None,v=None,native=False):
 if u is None:u=field_step(rule,x)
 if v is None:v=field_step(rule,u)
 left,right=shifted(x,-1),shifted(x,1)
 sensitivity=np.zeros((3,)+x.shape,np.uint8) if native else sensitivities(rule,x)
 g=np.zeros_like(x) if native else u^v^field_step(rule,x^u)
 q=np.stack((x,u,v,x^u,x^v,x^left,x^right,x^shifted(x,2),
 x^shifted(u,-1),x^shifted(u,1),x^shifted(v,-2),x^shifted(v,2),
 (1^x)&u,x&(1^u),*sensitivity,(1^x)&(left|right),g,
 (1^left)&(1^x)&(1^right),(1^left)&x&(1^right),left&(1^x)&right,left&x&right,x&u))
 assert q.shape[0]==24 and q.dtype==np.uint8
 return q

def word_labels(q,at=0):
 w=q.shape[-1];return q[...,(at-1)%w]+2*q[...,at%w]+4*q[...,(at+1)%w]
def candidate_labels(single,candidates=CANDIDATES):
 return np.asarray([single[ids[0]] if len(ids)==1 else single[ids[0]]+8*single[ids[1]] for ids in candidates],np.uint8)
def canonical(a):
 """First-occurrence partition names, computed by a simple lookup dictionary."""
 aliases={};out=[]
 for value in np.asarray(a).ravel():
  value=int(value)
  if value not in aliases:aliases[value]=len(aliases)
  out.append(aliases[value])
 return bytes(out)
def entropy(*variables):
 # Integer tuples keep a separate implementation from radix/bincount estimators.
 n=len(variables[0]);assert all(len(v)==n for v in variables)
 if len(variables)==1:counts=Counter(map(int,variables[0])).values()
 else:counts=Counter(zip(*(map(int,v) for v in variables))).values()
 return math.log2(n)-math.fsum(c*math.log2(c) for c in counts)/n

def measurements(z0,z1,z2,zright,target,singles=None,ids=None):
 h0=entropy(z0);h1=entropy(z1);h01=entropy(z0,z1)
 output=[h0,h01-h0,entropy(z1,z2)-h1-entropy(z0,z1,z2)+h01,
 h0+entropy(zright)-entropy(z0,zright),entropy(z0,target)-h0]
 successors=defaultdict(set);weight=Counter(map(int,z0))
 for a,b in zip(z0,z1):successors[int(a)].add(int(b))
 output.append(sum(weight[a] for a,bs in successors.items() if len(bs)>1)/len(z0))
 if ids is not None and len(ids)==2:
  htarget=min(entropy(singles[i],target)-entropy(singles[i]) for i in ids)
  output.append(htarget-output[4])
 else:output.append(None)
 return output

def finite_case(rule,width):
 states=np.arange(1<<width,dtype=np.uint16);nxt=word_step(rule,states,width)
 x=unpack(states,width);u=unpack(nxt,width);v=unpack(nxt[nxt],width)
 q=primitives(rule,x,u,v)
 # The two independent update routes must agree before using lag maps.
 assert np.array_equal(field_step(rule,x),u)
 zsingle=word_labels(q);z=candidate_labels(zsingle);zr=candidate_labels(word_labels(q,1))
 target=zsingle[1]
 m=np.empty((300,7),np.float64)
 for i,ids in enumerate(CANDIDATES):
  m[i]=[np.nan if value is None else value for value in measurements(z[i],z[i,nxt],z[i,nxt[nxt]],zr[i],target,zsingle,ids)]
 shift=np.zeros(1<<width,np.uint16)
 for pos in range(width):shift|=((states>>((pos+1)%width))&1)<<pos
 assert np.array_equal(x[shift],shifted(x,1))
 return {'primitive':q,'next_index':nxt,'right_index':shift,'metrics':m,'z':z}

def rule_orbit(rule):
 table=[(rule>>i)&1 for i in range(8)]
 reflected=sum(table[((i&1)<<2)|(i&2)|((i&4)>>2)]<<i for i in range(8))
 complemented=sum((1^table[7-i])<<i for i in range(8))
 rtable=[(reflected>>i)&1 for i in range(8)]
 reflected_complement=sum((1^rtable[7-i])<<i for i in range(8))
 return tuple(sorted({rule,reflected,complemented,reflected_complement}))
def classes(path=None):
 lab=json.loads((path or ROOT/'experiments/on_beam_256_4d_20260914/labels.json').read_text())
 positives=sorted(set(rule_orbit(54)+rule_orbit(110)))
 negatives=sorted({rule_orbit(int(r)) for cls in ('1','2','3') for r in lab['representatives'][cls]})
 disputed=[rule_orbit(r) for r in (41,106)]
 assert not set(positives)&{r for orb in negatives for r in orb}
 assert not {r for orb in disputed for r in orb}&{r for orb in negatives for r in orb}
 return positives,negatives,disputed

def shortlist(discovery):
 """Input shape [2,256,300,7]; reconstruct every candidate rank and winner."""
 assert discovery.shape==(2,256,300,7)
 pos,neg,disputed=classes();tables=[];chosen=[]
 for metric in range(7):
  candidates=range(24,300) if metric==6 else range(300)
  ranked=[]
  for candidate in candidates:
   values=discovery[:,:,candidate,metric];lo=float(values[:,pos].min());hi=float(values[:,pos].max())
   overlap=[]
   for orbit in neg:
    v=values[:,orbit];overlap.append(bool(np.any((v>=lo-TOL)&(v<=hi+TOL))))
   spread=float(values.max()-values.min());normalized=round((hi-lo)/spread,12) if spread>TOL else 0.0
   rank=(sum(overlap),normalized,candidate)
   row={'metric':metric,'candidate':candidate,'interval':[lo,hi],'overlap':rank[0],'normalized_width':normalized,'negative_overlaps':[list(o) for o,yes in zip(neg,overlap) if yes]}
   ranked.append((rank,row))
  ranked.sort(key=lambda x:x[0]);tables.extend(r[1] for r in ranked);chosen.append(ranked[0][1])
 return chosen,tables

def confirm(slots,metrics):
 # Confirmation shape [256,300,7] or [256,7], where slot order is explicit.
 pos,neg,disputed=classes();out=[]
 for slot,row in enumerate(slots):
  values=metrics[:,row['candidate'],row['metric']] if metrics.ndim==3 else metrics[:,slot]
  lo,hi=row['interval'];inside=(values>=lo-TOL)&(values<=hi+TOL)
  out.append({'metric':row['metric'],'candidate':row['candidate'],'core_retained':[r for r in pos if inside[r]],'negative_overlaps':[list(o) for o in neg if np.any(inside[list(o)])],
   'disputed':[{'orbit':list(o),'inside':[r for r in o if inside[r]]} for o in disputed]})
 return out

def trajectories(rule,seed,slots):
 generator=np.random.Generator(np.random.PCG64(seed));x=generator.integers(0,2,size=1021,dtype=np.uint8)
 for _ in range(1024):x=field_step(rule,x)
 states=np.empty((1028,1021),np.uint8);states[0]=x
 for t in range(1,len(states)):states[t]=field_step(rule,states[t-1])
 q=primitives(rule,states[:-2],states[1:-1],states[2:]) # Q(t) t=0..1025
 locations=np.floor(np.arange(8)*1021/8).astype(int)
 single=np.stack([word_labels(q,int(x)) for x in locations],axis=-1)
 right=np.stack([word_labels(q,int(x)+1) for x in locations],axis=-1)
 # Flatten common event order: time then sample site.
 zsingle=single[:,:1024].reshape(24,-1);target=zsingle[1]
 out=[]
 for row in slots:
  candidate=row['candidate'];ids=CANDIDATES[candidate]
  def cat(data):return data[ids[0]] if len(ids)==1 else data[ids[0]]+8*data[ids[1]]
  z0=cat(single[:,:1024]).ravel();z1=cat(single[:,1:1025]).ravel();z2=cat(single[:,2:1026]).ravel();zr=cat(right[:,:1024]).ravel()
  m=measurements(z0,z1,z2,zr,target,zsingle,ids)
  out.append({'candidate':candidate,'metric':row['metric'],'values':m,'selected_value':m[row['metric']]})
 return out,states,single

def same_partition(a,b):return canonical(a)==canonical(b)
def native_matches(grid,nxt,root_q):
 """All native catalog×six newest phases, with older transverse axes zero."""
 result=[];w=grid.shape[-1];n=grid.shape[0]
 root=candidate_labels(word_labels(root_q));rootkeys={}
 for i,z in enumerate(root):rootkeys.setdefault(canonical(z),[]).append(i)
 for phase in range(6):
  index=(slice(None),phase)+(0,)*(grid.ndim-3)+(slice(None),)
  x=grid[index];u=grid[nxt][index];v=grid[nxt[nxt]][index]
  q=primitives(None,x,u,v,native=True);zs=candidate_labels(word_labels(q),NATIVE_CANDIDATES)
  for candidate,z in enumerate(zs):
   key=canonical(z)
   if key in rootkeys:
    # Exact pointed event identity after canonical renaming also yields the
    # same shared-source successor transition multiplicities.
    canonical_z=np.frombuffer(key,np.uint8)
    edges=Counter(zip(map(int,canonical_z),map(int,canonical_z[nxt])))
    for match in rootkeys[key]:
     other=np.frombuffer(canonical(root[match]),np.uint8)
     assert edges==Counter(zip(map(int,other),map(int,other[nxt])))
    result.append({'phase':phase,'native_candidate':candidate,'primitive_indices':list(NATIVE_CANDIDATES[candidate]),'root_candidates':rootkeys[key],'partition_hex':key.hex(),'transition_edges':[[a,b,c] for (a,b),c in sorted(edges.items())]})
 return result

def basins(nxt):
 """Each functional component is named by its least cycle vertex."""
 memo={}
 for start in range(len(nxt)):
  trail=[];where={};here=start
  while here not in memo and here not in where:
   where[here]=len(trail);trail.append(here);here=int(nxt[here])
  if here in memo:label=memo[here]
  else:label=min(trail[where[here]:])
  for vertex in trail:memo[vertex]=label
 return np.asarray([memo[i] for i in range(len(nxt))],np.int32)
def choose2(n):return n*(n-1)//2
def provenance(symbol,reps,shape,nxt):
 w=int(shape[-1]);per_state=int(np.prod(shape[1:-1]));sources=(np.asarray(reps)//per_state).astype(int)
 labels=np.asarray(symbol).ravel()[reps];basin=basins(nxt)
 states=np.arange(1<<w,dtype=np.uint16);full=np.ones(len(states),bool)
 for shift in range(1,w):
  rotated=((states>>shift)|(states<<(w-shift)))&((1<<w)-1)
  full &=rotated!=states
 groups=defaultdict(list)
 for source,label in zip(sources,labels):
  if label:groups[int(label)].append(int(source))
 counts=dict(pairs=0,same_source=0,same_successor=0,same_basin=0,both_full_period=0)
 for sources_in_block in groups.values():
  counts['pairs']+=choose2(len(sources_in_block))
  for name,values in [('same_source',sources_in_block),('same_successor',[int(nxt[s]) for s in sources_in_block]),('same_basin',[int(basin[s]) for s in sources_in_block])]:counts[name]+=sum(choose2(n) for n in Counter(values).values())
  counts['both_full_period']+=choose2(sum(bool(full[s]) for s in sources_in_block))
 return counts,sources,basin,full

def self_test():
 for rule in (0,30,90,110,255):
  for state in range(32):
   x=unpack([state],5)[0];f=field_step(rule,x)
   for position in range(5):
    for direction,delta in enumerate((-1,0,1)):
     perturbed=x.copy();perturbed[(position+delta)%5]^=1
     assert sensitivities(rule,x)[direction,position]==f[position]^field_step(rule,perturbed)[position]
 x=unpack(np.arange(32),5);challenge=sensitivities('radius2',x)
 for position in range(5):
  for direction,delta in enumerate((-1,0,1)):
   perturbed=x.copy();perturbed[:,(position+delta)%5]^=1
   assert np.array_equal(challenge[direction,:,position],field_step('radius2',x)[:,position]^field_step('radius2',perturbed)[:,position])
 a=np.array([0,0,1,1]);b=np.array([0,1,0,1]);assert entropy(a)==entropy(b)==1 and entropy(a,b)==2
 m=measurements(a,b,a,b,a,np.stack((a,b)),(0,1));assert abs(m[0]-1)<TOL and abs(m[1]-1)<TOL and abs(m[2]-1)<TOL and m[5]==1
 assert canonical([8,3,8,5])==canonical([2,6,2,9])
 assert tuple(basins(np.array([1,0,3,3,2])))==(0,0,3,3,3)
 return {'eca_sensitivity_scalar_cases':2400,'radius2_sensitivity_cases':480,'entropy_checks':6,'partition_and_basin_checks':2}

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--self-test',action='store_true');parser.add_argument('--finite-panel',choices=['discovery','confirmation']);parser.add_argument('--confirmation-seal',type=Path);args=parser.parse_args()
 controls=self_test()
 if args.self_test:print(json.dumps(controls));return
 assert args.finite_panel
 if args.finite_panel=='confirmation':assert args.confirmation_seal and args.confirmation_seal.is_file(),'Committed shortlist must exist before confirmation'
 output=ROOT/'review/catalog-replay'/args.finite_panel;output.mkdir(parents=True,exist_ok=True);assert not (output/'result.json').exists()
 widths=(7,8) if args.finite_panel=='discovery' else (9,)
 started=time.monotonic();cases=[]
 for width,rule in itertools.product(widths,PANEL):
  if time.monotonic()-started>600:break
  before=time.monotonic();case=finite_case(rule,width);path=output/f'w{width}_r{rule:03d}.npz'
  temporary=path.with_suffix('.npz.tmp')
  with temporary.open('wb') as f:np.savez_compressed(f,**case)
  temporary.replace(path);cases.append({'rule':rule,'width':width,'sha256':digest(path)})
  assert resource.getrusage(resource.RUSAGE_SELF).ru_maxrss<2*1024*1024
  print(json.dumps({'rule':rule,'width':width,'seconds':time.monotonic()-before}),flush=True)
 complete=len(cases)==len(widths)*len(PANEL)
 result={'complete':complete,'controls':controls,'cases':cases,'source_sha256':digest(__file__),'seconds':time.monotonic()-started,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
 save(output/('result.json' if complete else 'censored.json'),result);print(json.dumps(result))
if __name__=='__main__':main()
