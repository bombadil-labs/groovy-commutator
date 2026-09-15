"""Independent numerical audit; run only after committed prediction seal."""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import resource
import time
import numpy as np
import oracle

ROOT=Path(__file__).resolve().parents[2]
UNIT=ROOT/'experiments/factor_balanced_interactions_20260915'
OUT=Path(__file__).parent
RULES=[0,18,30,54,90,110,126,204]
HORIZONS=[1,2,4,8,16,32]
OBS=[f'future_{t}' for t in HORIZONS]+['basin','cycle_length','transient_depth']
def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj): (OUT/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
ERROR=0.
def close(a,b,tol=2e-11):
 global ERROR
 error=float(np.max(np.abs(np.array(a)-np.array(b))))
 ERROR=max(ERROR,error)
 assert error<tol,(error,a,b)
def freeze():
 seal=read(UNIT/'prediction-seal.json')
 assert seal['predictions_sha256']==sha(UNIT/'predictions.json')
 for path,digest in read(UNIT/'implementation-freeze.json')['source_hashes'].items(): assert sha(ROOT/path)==digest,path
 return seal

def fit():
 start=time.monotonic();freeze()
 p=read(UNIT/'predictions.json')
 history=read(UNIT/'historical-relations.json')
 assert sha(UNIT/'historical-relations.json')==sha(ROOT/'experiments/rule_ring_structure_20260915/compact-relations.json')
 lookup={(r['observation'],*map(int,r['rules']),r['ring']):r['vi_per_bit'] for r in history}
 pa,wa=oracle.design(range(4,10));pb,wb=oracle.design(range(10,17));pc,wc=oracle.design([17,18,20,21])
 pairs=pa+pb;weights=np.concatenate([wa/2,wb/2])
 assert [r['rings'] for r in p['training_rows']]==[list(pair) for pair in pairs]
 assert p['test_pairs']==[list(pair) for pair in pc]
 close(p['training_weights'],weights)
 close(p['training_features'],[oracle.features(*pair,2)[1:] for pair in pairs])
 close(p['test_features'],[oracle.features(*pair,2)[1:] for pair in pc])
 for task in p['tasks']:
  o=task['observation'];a,b=task['rules']
  y=np.array([abs(lookup[o,a,b,n]-lookup[o,a,b,m]) for n,m in pairs]);close(y,task['training_targets'])
  for k in range(3):
   saved=task['models'][f'M{k}'];coef=oracle.fit(pairs,weights,y,k)
   close(coef,saved['coefficients'])
   raw=np.array([oracle.features(n,m,k) for n,m in pc])@coef;pred=np.clip(raw,0,1)
   close(raw,saved['unclipped_predictions']);close(pred,saved['predictions'])
   # Clipping counts are sensitive only if an unrounded prediction crosses zero.
   primary_raw=np.array(saved['unclipped_predictions'])
   assert saved['test_clipping_count']==int(np.count_nonzero(primary_raw!=np.clip(primary_raw,0,1)))
   train=np.clip(np.array([oracle.features(n,m,k) for n,m in pairs])@coef,0,1)
   close(weights@abs(train-y),saved['training_weighted_mae']);close(np.sqrt(weights@((train-y)**2)),saved['training_weighted_rmse'])
   if a==0 and b==204 and o.startswith('future_'):close(y,np.zeros(30));close(raw,np.zeros(6))
 result={'status':'verified','tasks':len(p['tasks']),'fits':len(p['tasks'])*3,'predictions':len(p['tasks'])*18,'maximum_numeric_error':ERROR,'wall_seconds':time.monotonic()-start,'predictions_sha256':sha(UNIT/'predictions.json'),'oracle_sha256':sha(OUT/'oracle.py'),'verifier_sha256':sha(Path(__file__))}
 save('fit-verification.json',result);print(json.dumps(result),flush=True)

def cases():
 start=time.monotonic();freeze();checked=[];relations=[]
 for n in [17,18,20,21]:
  paths={r:UNIT/'partitions'/f'n{n:02d}_r{r:03d}.npz' for r in RULES}
  if not all(p.exists() for p in paths.values()):
   print(f'width {n} not complete; stopping without claiming full coverage',flush=True);break
  for rule,path in paths.items():
   data=dict(np.load(path,allow_pickle=False));nxt=data['successor'];ids=np.arange(1<<n)
   assert all(v.shape==(1<<n,) for v in data.values())
   assert np.all(nxt < 1<<n)
   replay=n==17 or (n==21 and rule in [54,90,110])
   if replay:
    expected=oracle.scalar_successor(rule,n);assert np.array_equal(nxt,expected),(n,rule,'successor')
    graph=oracle.graph(expected)
    for key,array in graph.items():assert np.array_equal(data[key],array),(n,rule,key)
   basin=data['basin'];period=data['cycle_length'];depth=data['transient_depth']
   assert np.all(basin==basin[nxt]) and np.all(period==period[nxt])
   assert np.all(depth[depth>0]==depth[nxt[depth>0]]+1)
   cyc=ids[depth==0];assert np.all(depth[nxt[cyc]]==0) and np.all(period>0)
   # Every declared cycle must close at exactly its length, with minimum label.
   seen=set()
   for node in cyc:
    node=int(node)
    if node in seen:continue
    walk=[];cur=node
    while cur not in seen:
     seen.add(cur);walk.append(cur);cur=int(nxt[cur])
    assert cur==node and all(int(period[v])==len(walk) and int(basin[v])==min(walk) for v in walk)
   current=ids
   for t in range(1,33):
    current=nxt[current]
    if t in HORIZONS:assert np.array_equal(current,data[f'future_{t}'])
   ent={key:oracle.entropy(data[key]) for key in OBS}
   if rule==90:
    for t in HORIZONS:close(ent[f'future_{t}'],oracle.rank90(n,t))
   checked.append({'ring':n,'rule':rule,'sha256':sha(path),'independent_scalar_replay':replay,'entropies':ent,'blocks':{k:len(np.unique(data[k])) for k in OBS},'max_transient':int(depth.max()),'max_cycle_length':int(period.max())})
   print(f'audited n={n} rule={rule} scalar_replay={replay} elapsed={time.monotonic()-start:.1f}s',flush=True)
  for obs in OBS:
   arrays={r:np.load(p,allow_pickle=False)[obs] for r,p in paths.items()}
   for a,b in itertools.combinations(RULES,2):
    rel=oracle.relation(arrays[a],arrays[b],n)
    if (a,b)==(54,110):
     renamed=oracle.relation((1<<n)-1-arrays[a],(1<<n)-1-arrays[b],n)
     for key in rel:close(rel[key],renamed[key])
    relations.append({'ring':n,'rules':[a,b],'observation':obs,**rel})
   print(f'relations n={n} obs={obs} elapsed={time.monotonic()-start:.1f}s',flush=True)
  save('fresh-independent-relations.json',relations)
  save('cases-verification.json',{'status':'verified' if len(checked)==32 else 'partial','cases':checked,'relation_count':len(relations),'maximum_numeric_error':ERROR,'wall_seconds':time.monotonic()-start,'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'oracle_sha256':sha(OUT/'oracle.py'),'verifier_sha256':sha(Path(__file__))})

def score():
 start=time.monotonic();freeze();r=read(UNIT/'confirmation-result.json');p=read(UNIT/'predictions.json');audit=read(OUT/'cases-verification.json');assert audit['status']=='verified'
 lookup={(v['observation'],*v['rules'],v['ring']):v for v in read(OUT/'fresh-independent-relations.json')}
 for checked,saved in zip(audit['cases'],r['case_info']):
  for key in ['ring','rule','sha256','blocks','max_transient','max_cycle_length']:assert checked[key]==saved[key],key
  for key in OBS:close(checked['entropies'][key],saved['entropies'][key])
 evidence=read(UNIT/'evidence.json');assert sha(UNIT/'evidence.json')==r['evidence_sha256']
 for row in evidence['rows']:
  o=row['observation'];a,b=map(int,row['rules']);n,m=row['rings']
  for width,rel in zip(row['rings'],row['relation_values']):
   expected=lookup[o,a,b,width]
   for key in rel:close(rel[key],expected[key])
  close(row['scores']['absolute_change'],abs(lookup[o,a,b,n]['vi_per_bit']-lookup[o,a,b,m]['vi_per_bit']))
 outcomes=[]
 for task,saved in zip(p['tasks'],r['tasks']):
  o=task['observation'];a,b=task['rules'];assert (o,[a,b])==(saved['observation'],saved['rules'])
  y=np.array([abs(lookup[o,a,b,n]['vi_per_bit']-lookup[o,a,b,m]['vi_per_bit']) for n,m in p['test_pairs']]);close(y,saved['targets']);maes=[]
  for k in range(3):
   key=f'M{k}';pred=np.array(task['models'][key]['predictions']);err=pred-y;mae=float(np.mean(abs(err)));maes.append(mae)
   close(saved['models'][key]['mae'],mae);close(saved['models'][key]['rmse'],np.sqrt(np.mean(err**2)));close(saved['models'][key]['errors'],err);close(saved['models'][key]['predictions'],pred)
  verdict=lambda k:'improvement' if maes[k]-maes[2]>1e-12 else ('loss' if maes[k]-maes[2]<-1e-12 else 'tie')
  assert saved['M2_vs_M0']==verdict(0) and saved['M2_vs_M1']==verdict(1)
  assert saved['strict_joint_improvement']==(verdict(0)==verdict(1)=='improvement')
  outcomes.append(saved)
 for summary in r['summary']:
  panel=[row for row in outcomes if row['observation']==summary['observation']]
  for key in ['M2_vs_M0','M2_vs_M1']:assert summary[key]==dict(Counter(row[key] for row in panel))
  assert summary['strict_joint_improvements']==sum(row['strict_joint_improvement'] for row in panel)
 result={'status':'verified','tasks':len(outcomes),'evidence_rows':len(evidence['rows']),'relations':len(lookup),'strict_joint_improvements':sum(row['strict_joint_improvement'] for row in outcomes),'maximum_numeric_error':ERROR,'wall_seconds':time.monotonic()-start,'confirmation_sha256':sha(UNIT/'confirmation-result.json'),'oracle_sha256':sha(OUT/'oracle.py'),'verifier_sha256':sha(Path(__file__))}
 save('score-verification.json',result);print(json.dumps(result),flush=True)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['fit','cases','score']);args=parser.parse_args();globals()[args.stage]()
