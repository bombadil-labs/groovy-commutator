#!/usr/bin/env python3
"""Independent full selection audit and physical observation/provenance comparisons."""
import argparse,base64
from collections import Counter
import itertools,json,resource,tarfile,time
from pathlib import Path
import numpy as np
import catalog_oracle as o

ROOT=o.ROOT;UNIT=o.UNIT;OUTPUT=ROOT/'review/catalog-replay'
ARCHIVE=Path('/workspace/scratch/1815be08ff33/gc-pilot/experiments/uniform_jet6_cache_20260914/run/uniform_jet6_rules.tar.gz')

def finite_panel(stage):
 widths=(7,8) if stage=='discovery' else (9,)
 report=[];maximum=0.;elements=0
 with np.load(UNIT/(stage+'-metrics.npz')) as file:
  metrics=file['metrics']
  for wi,width in enumerate(widths):
   for rule in o.PANEL:
    with np.load(OUTPUT/stage/f'w{width}_r{rule:03d}.npz') as independent,np.load(UNIT/'finite'/f'w{width}_r{rule:03d}.npz') as primary:
     for a,b in [('primitive','fields'),('next_index','next_index'),('right_index','right_index')]:assert np.array_equal(independent[a],primary[b]),(stage,width,rule,a)
     expected=independent['metrics'];actual=metrics[wi,rule] if stage=='discovery' else metrics[rule]
     assert np.array_equal(np.isnan(expected),np.isnan(actual))
     delta=float(np.nanmax(np.abs(actual-expected)));assert delta<o.TOL,(width,rule,delta)
     maximum=max(maximum,delta);elements+=int(np.sum(~np.isnan(expected)))
     report.append({'width':width,'rule':rule,'metric_max_abs_error':delta,'primitive_bits_compared':int(independent['primitive'].size)})
  aliases=0
  if stage=='discovery':
   for rule in o.PANEL:
    x=o.unpack(np.arange(2048),11);labels=o.candidate_labels(o.word_labels(o.primitives(rule,x)))
    seen={};ids=[]
    for z in labels:
     key=o.canonical(z)
     if key not in seen:seen[key]=len(seen)
     ids.append(seen[key])
    assert np.array_equal(ids,file['aliases'][rule]),('aliases',rule)
    aliases+=len(ids)
 return {'cases':report,'metric_values_compared':elements,'maximum_metric_error':maximum,'local_alias_candidate_checks':aliases}

def selection():
 raw=json.loads((UNIT/'shortlist.json').read_text())
 with np.load(UNIT/'discovery-metrics.npz') as f:metrics=f['metrics']
 chosen,table=o.shortlist(metrics);own={(r['metric'],r['candidate']):r for r in table}
 assert len(raw['ranking'])==len(table)==2076
 for row in raw['ranking']:
  other=own[row['metric'],row['candidate']]
  assert np.allclose(row['interval'],other['interval'],atol=o.TOL,rtol=0)
  assert row['normalized_width']==other['normalized_width']
  assert row['negative_orbits_overlap']==[min(g) for g in other['negative_overlaps']]
  lo,hi=other['interval'];values=metrics[:,:,row['candidate'],row['metric']]
  positive,negative,disputed=o.classes();inside=(values>=lo-o.TOL)&(values<=hi+o.TOL)
  assert row['core_members_inside']==int(inside[:,positive].sum())
  assert row['core_members_total']==len(positive)*2
  assert row['disputed_orbits_overlap']==[min(g) for g in disputed if inside[:,g].any()]
 for actual,expected in zip(raw['selected'],chosen):assert actual['candidate']==expected['candidate'] and actual['metric']==expected['metric']
 assert raw['input_hashes']['discovery-metrics.npz']==o.digest(UNIT/'discovery-metrics.npz')
 return {'attempted_rankings':len(table),'selected':[{'metric':x['metric'],'candidate':x['candidate'],'negative_overlap_count':x['overlap']} for x in chosen]}

def confirmation():
 raw=json.loads((UNIT/'confirmation-result.json').read_text());short=json.loads((UNIT/'shortlist.json').read_text());slots=short['selected']
 seal=json.loads((UNIT/'confirmation-seal.json').read_text());assert o.digest(UNIT/'shortlist.json')==seal['shortlist_sha256']==raw['shortlist_sha256']
 with np.load(UNIT/'confirmation-metrics.npz') as f:verdicts=o.confirm(slots,f['metrics'])
 for actual,expected in zip(raw['width9'],verdicts):
  assert actual['candidate']==expected['candidate'] and actual['metric']==expected['metric']
  assert actual['core_members_inside']==len(expected['core_retained'])
  assert actual['negative_orbits_overlap']==[min(g) for g in expected['negative_overlaps']]
  assert actual['disputed_orbits_overlap']==[min(g['orbit']) for g in expected['disputed'] if g['inside']]
 long_count=0
 for run in raw['long_runs']:
  with np.load(UNIT/'long'/f'r{run["rule"]}_s{run["seed"]}.npz') as data:
   for row,slot in zip(run['slots'],slots):
    value=float(data['metrics'][slot['candidate'],slot['metric']]);lo,hi=slot['interval']
    assert abs(row['value']-value)<o.TOL and row['inside']==bool(lo-o.TOL<=value<=hi+o.TOL);long_count+=1
 reconstructed=[]
 for rule,seed in itertools.product((30,54,110,'radius2'),(2026091501,2026091502)):
  measured,states,words=o.trajectories(rule,seed,slots)
  with np.load(UNIT/'long'/f'r{rule}_s{seed}.npz') as primary:
   assert np.array_equal(words,primary['words'])
   target=words[1,:1024];assert np.array_equal(target,primary['target'])
   source_shape=tuple(primary['trajectory_shape']);stored=np.unpackbits(primary['trajectory_bits'])[:int(np.prod(source_shape))].reshape(source_shape)
   assert np.array_equal(states,stored)
   maximum=0.
   for row in measured:
    candidate=row['candidate'];v=np.asarray([np.nan if x is None else x for x in row['values']]);actual=primary['metrics'][candidate]
    assert np.array_equal(np.isnan(v),np.isnan(actual));error=float(np.nanmax(abs(v-actual)));assert error<o.TOL,(rule,seed,error);maximum=max(maximum,error)
   reconstructed.append({'rule':rule,'seed':seed,'maximum_metric_error':maximum,'primitive_words_compared':int(words.size),'trajectory_bits_compared':int(states.size)})
  path=OUTPUT/'long';path.mkdir(exist_ok=True)
  temporary=path/f'r{rule}_s{seed}.npz.tmp';destination=path/f'r{rule}_s{seed}.npz'
  with temporary.open('wb') as f:np.savez_compressed(f,words=words,trajectory_bits=np.packbits(states),trajectory_shape=np.asarray(states.shape))
  temporary.replace(destination)
  o.save(path/f'r{rule}_s{seed}.json',{'measurements':measured,'arrays_sha256':o.digest(destination)})
 return {'width9_verdicts':verdicts,'all_long_interval_verdicts_checked':long_count,'long_reconstruction':reconstructed,'seal':seal}

def lift(archive):
 assert o.digest(archive)=='766e4db7083fbdb551bc4aee66abc554079c5d118905f6d65aa5e5372c9418d1'
 primary=json.loads((UNIT/'lift-result.json').read_text());assert primary['status']=='complete'
 records={(r['width'],r['rule'],r['dimension']):r for r in primary['records']};prs={(r['width'],r['rule'],r['dimension'],r['contract']):r for r in primary['provenance']}
 prior_path=UNIT/'inputs/previous_result.json';assert o.digest(prior_path)=='5101ad951144527fad7f32bc3819da3b540fe3320fde34478ca99fe136fa71b3';prior={r['id']:r for r in json.loads(prior_path.read_text())['records']}
 completed=[];view_count=matches=pair_records=witnesses=0
 with tarfile.open(archive,'r|gz') as tf:
  for member in tf:
   parts=member.name.split('/')
   if not member.isfile() or len(parts)!=3 or int(parts[1][4:]) not in (0,4,18,30,54,90,110,124,126,137,147,193,204):continue
   raw=tf.extractfile(member).read();record=json.loads(raw);r=record['rule'];w=record['width'];d=record['dimension'];key=(w,r,d)
   if key not in records:continue
   ident=f'w{w}_r{r:03d}_d{d}';assert __import__('hashlib').sha256(raw).hexdigest()==prior[ident]['archive_member_sha256']
   shape=tuple(record['grid_shape']);grid=np.unpackbits(np.frombuffer(base64.b64decode(record['grid_bits_big']),np.uint8))[:int(np.prod(shape))].reshape(shape)
   root=grid
   for _ in range(d-1):root=root[:,4]^root[:,5]
   numeric=np.sum(root.astype(np.uint16)<<np.arange(w),axis=1);to_order=np.argsort(numeric)
   assert np.array_equal(np.sort(numeric),np.arange(1<<w));nxt=to_order[o.word_step(r,numeric,w)]
   root_q=o.primitives(r,root)
   expected=o.native_matches(grid,nxt,root_q)
   expected_match=sorted([[e['phase'],o.CANDIDATES.index(tuple(e['primitive_indices'])),e['root_candidates']] for e in expected])
   actual=records[key];assert sorted(actual['matches'])==expected_match,key
   assert actual['matched_views']==len(expected_match) and actual['unmatched_views']==1260-len(expected_match)
   view_count+=1260;matches+=len(expected_match)
   # Directly reconstruct all archived transition witnesses in their original labels.
   for witness in actual['transition_witnesses']:
    phase=witness['phase'];index=(slice(None),phase)+(0,)*(d-2)+(slice(None),)
    q=o.primitives(None,grid[index],grid[nxt][index],grid[nxt[nxt]][index],native=True)
    z=o.candidate_labels(o.word_labels(q))[witness['native_candidate']]
    root_z=o.candidate_labels(o.word_labels(root_q))[witness['root_candidate']]
    relation=sorted({(int(a),int(b)) for a,b in zip(z,root_z)})
    assert relation==[tuple(p) for p in witness['relabeling']]
    edges=Counter(zip(map(int,z),map(int,z[nxt])))
    assert [[a,b,n] for (a,b),n in sorted(edges.items())]==witness['transition_edges'];witnesses+=1
   relation_path=UNIT/'inputs/relations'/f'{ident}.npz';assert o.digest(relation_path)==prior[ident]['arrays_sha256']
   with np.load(relation_path) as data,np.load(UNIT/'lift'/f'{ident}.npz') as graph:
    assert np.array_equal(root,graph['root']) and np.array_equal(nxt,graph['next_index'])
    for contract in ('finite','full_input_d2') if d==2 else ('finite',):
     counts,sources,basin,full=o.provenance(data[contract+'_symbol'],data['orbit_representatives'],shape,nxt)
     pr=prs[w,r,d,contract]
     for a,b in [('pairs','free_pairs'),('same_source','same_source'),('same_successor','equal_successor'),('same_basin','same_basin'),('both_full_period','both_full_period')]:assert counts[a]==pr[b],(key,contract,a,counts,pr)
     assert np.array_equal(sources,graph['event_source']) and np.array_equal(basin,graph['basin']) and np.array_equal(full,graph['spatial_period']==w)
     assert (pr['status']=='not_applicable')==(counts['pairs']==0);pair_records+=1
   completed.append({'width':w,'rule':r,'dimension':d,'matched_views':len(expected_match)})
   if len(completed)%13==0:print(json.dumps({'lift_records':len(completed)}),flush=True)
 assert len(completed)==78 and pair_records==104
 return {'records':completed,'native_views_checked':view_count,'matched_views_checked':matches,'provenance_contracts_checked':pair_records,'transition_witnesses_checked':witnesses}

def main():
 global UNIT
 p=argparse.ArgumentParser();p.add_argument('stage',choices=['discovery','confirmation','lift']);p.add_argument('--unit',type=Path,default=UNIT);p.add_argument('--archive',type=Path,default=ARCHIVE);args=p.parse_args();UNIT=args.unit
 start=time.monotonic();result={'stage':args.stage,'oracle_source_sha256':o.digest(o.__file__),'comparison_source_sha256':o.digest(__file__)}
 if args.stage in ('discovery','confirmation'):result['finite_panel']=finite_panel(args.stage)
 if args.stage=='discovery':result['selection']=selection()
 elif args.stage=='confirmation':result['confirmation']=confirmation()
 else:result['lift']=lift(args.archive)
 result['seconds']=time.monotonic()-start;result['peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
 assert result['seconds']<600 and result['peak_rss_kib']<2*1024*1024
 result['agree']=True;OUTPUT.mkdir(exist_ok=True,parents=True);o.save(OUTPUT/(args.stage+'-comparison.json'),result)
 print(json.dumps({k:v for k,v in result.items() if k not in ('finite_panel','selection','confirmation','lift')}))
if __name__=='__main__':main()
