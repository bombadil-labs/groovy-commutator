#!/usr/bin/env python3
"""Compare primary artifacts to the independently constructed physical replay."""
import hashlib,json
from pathlib import Path
import numpy as np
B=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def partition(a,b):
 a=a.ravel();b=b.ravel();assert a.shape==b.shape
 pairs=np.unique(np.column_stack((a,b)),axis=0)
 assert len(pairs)==len(np.unique(a))==len(np.unique(b))
def main():
 p=json.loads((B/'experiments/commutator_relations_20260915/result.json').read_text())
 r=json.loads((B/'review/replay/result.json').read_text())
 ri={x['id']:x for x in r['records']};assert len(ri)==len(p['records'])==78
 compared_symbols=0;compared_events=0
 for meta in p['records']:
  ident=meta['id'];other=ri[ident]
  assert meta['full_spatial_orbits']==other['spatial_orbits']
  assert meta['events_x0']==other['longitudinal_events']
  with np.load(B/'experiments/commutator_relations_20260915/records'/f'{ident}.npz') as a,np.load(B/'review/replay'/f'{ident}.npz') as b:
   assert np.array_equal(a['grid_shape'],b['grid_shape'])
   partition(a['orbit_ids'],b['orbit_ids'])
   for contract,stats in meta['contracts'].items():
    for level in ('longitudinal','spatial'):
     x=dict(stats[level]);x['ambiguous']=x.pop('ambiguous_events');assert x==other['contracts'][contract][level],(ident,contract,level,x,other['contracts'][contract][level])
    aa=a[contract+'_symbol'];bb=b[contract+'_symbol']
    assert np.array_equal(aa==0,bb==0)
    partition(aa,bb)
    assert np.array_equal(a[contract+'_constant'],b[contract+'_constant'])
    compared_symbols+=1;compared_events+=aa.size
    c=stats['child_sibling_blocks'];blocks=np.moveaxis(bb,1,-1).reshape(-1,6);nfree=(blocks>0).sum(axis=1)
    assert c['all_free']==np.sum(nfree==6) and c['all_fixed']==np.sum(nfree==0) and c['mixed']==np.sum((nfree>0)&(nfree<6))
 # Reconstruct all 2,048 algebraic census rows from the immutable prior counts.
 old=json.loads((B/'results/commutator_completion_20260915.json').read_text())
 oldi={(x['id'],x['contract']):x for x in old['records']}
 for census in p['census']:
  x=oldi[census['id'],census['contract']];w=x['width'];m=x['free_cells'];u=x['free_keys'];eq=x['equal_G_pairs_from_shared_variable'];op=x['opposite_G_pairs_from_shared_variable']
  assert census['ambiguous_events']==m//w and m%w==0
  assert census['variables']==u and census['rank']==m//w-u
  assert census['equal_pairs']*w*w+m*(w-1)//2==eq
  assert census['opposite_pairs']*w*w==op
 assert len(p['census'])==2048
 rt={(x['parent'],x['parent_contract']):x for x in r['transfers']}
 readouts=0
 for pt in p['transfers']:
  ident=f'w{pt["width"]}_r{pt["rule"]:03d}_d{pt["parent_dimension"]}'
  for contract,prs in pt['contracts'].items():
   rr=rt[ident,contract]
   for x,y in zip(pt['maps'],rr['map_checks']):assert x['respects_quotient']==y['well_defined'] and x['injective']==y['injective']
   for x,y in zip(prs,rr['readouts']):
    if not y['valid_map']:assert x['status']=='invalid_address_map';continue
    assert x['eligible_pairs']==y['denominator']
    for a,b in [('fixed_agree','fixed_agree'),('fixed_reverse','fixed_reverse'),('shared_nonempty_agree','free_agree'),('shared_nonempty_reverse','free_reverse')]:assert x[a]==y[b],(ident,contract,x,y)
    if y['denominator']:assert x['surviving_pairs']==y['survival']
    else:assert x['status']=='not_applicable' and x['survival_fraction'] is None
    readouts+=1
 result={'reviewer':'Codex (OpenAI), /root/relations_review','agree':True,'physical_records':78,'symbolic_contracts':compared_symbols,'pointed_events_compared':compared_events,'census_contracts':2048,'readout_transfer_records':readouts,'primary_result_sha256':sha(B/'experiments/commutator_relations_20260915/result.json'),'replay_result_sha256':sha(B/'review/replay/result.json'),'comparison_source_sha256':sha(__file__)}
 (B/'review/comparison.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
