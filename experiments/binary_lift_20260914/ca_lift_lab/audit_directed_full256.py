"""Full first-floor census for a reflection-closed directed-Q pair."""
import hashlib,json,time
from pathlib import Path
import numpy as np
from audit_binary_reference import keys,ORDERS
from verify_polarization_proposal import d,encode
from audit_temporal_reach import check

ROOT=Path(__file__).resolve().parent;OUT=ROOT/'runs/directed_full256'
REFS=[(-2,1,0),(-1,2,1)]
def qref(s,spec):
    a,b,reverse=spec;x=np.roll(s,-a,axis=-1);y=np.roll(s,-b,axis=-1)
    return ((1-x)&y) if reverse else (x&(1-y))
def qname(spec):
    a,b,r=spec;return f"directed:{a}:{b}:{'not-left-and-right' if r else 'left-and-not-right'}"
def tag(r):
    c=r['recipe'][0];return (r['rule'],c['mask'],c['shift'],r['reference'],tuple(r['order']))
def reflect_rule(r):
    out=0
    for i in range(8):
        j=((i&1)<<2)|(i&2)|((i&4)>>2);out|=((r>>i)&1)<<j
    return out

def main():
    start=time.monotonic();OUT.mkdir(parents=True,exist_ok=False)
    old=[r for r in map(json.loads,(ROOT/'runs/directed_reference_23_232/candidates.jsonl').read_text().splitlines()) if r['reference'] in {qname(x) for x in REFS}]
    cache={tag(r):r for r in old};assert len(cache)==192
    s=((np.arange(2048)[:,None]>>np.arange(10,-1,-1))&1).astype(np.uint8);mid=5;empty=np.array([],dtype=np.uint64);records=list(cache.values());new=0;complete=True
    with (OUT/'candidates.jsonl').open('w') as log:
      for r in old:log.write(json.dumps(r,separators=(',',':'))+'\n')
      for rule in range(256):
       ds=d(s,rule);es=s^ds;ees=es^d(es,rule);g=d(es,rule)^ds^d(ds,rule)
       for mask in ('birth','death','stay_one','stay_zero'):
        for shift in (-1,1):
         choice={'mask':mask,'shift':shift}
         if all((rule,mask,shift,qname(spec),order) in cache for spec in REFS for order in ORDERS):continue
         if time.monotonic()-start>112:complete=False;break
         a=encode(s,rule,choice);b=encode(es,rule,choice);c=encode(ees,rule,choice)
         carrier=np.stack([g[:,mid]^g[:,mid+shift],g[:,mid]],axis=1);desired=a[:,:2,mid]^c[:,:2,mid]^carrier;corrected=desired.copy();corrected[:,1]^=rule&1
         for spec in REFS:
          name=qname(spec);q=qref(s,spec);qn=qref(es,spec);af=np.concatenate([a,q[:,None,:]],axis=1);bf=np.concatenate([b,qn[:,None,:]],axis=1)
          for order in ORDERS:
           if (rule,mask,shift,name,order) in cache:continue
           aa=af[:,order,:];bb=bf[:,order,:];delta=aa^bb;bk=keys(aa,2,2);pk=keys(delta,2,2)[:,[order.index(0),order.index(1)]];bv=delta[...,mid]
           native=check(bk,bv,empty,empty,None);source=check(bk,np.repeat(s[:,mid,None],4,axis=1),empty,empty,None);raw=check(bk,bv,pk,desired,None);center=[check(bk,bv,pk,corrected,z) for z in (0,1)];first=native['passes'] and source['passes']
           rec={'rule':rule,'recipe':[choice],'reference':name,'reference_spec':spec,'reference_truth_table_00_01_10_11':[0,0,1,0] if not spec[2] else [0,1,0,0],'order':order,'rx':2,'ry':2,'source_width':11,'native':native,'source':source,'parent_recovery':source,'raw':raw,'centered_branches':center,'first_order_pass':first,'joint_raw':first and raw['passes'],'joint_centered':first and any(v['passes'] for v in center),'G_scope':'P/D only','off_image_outputs':'unspecified except imposed constraints'}
           records.append(rec);cache[tag(rec)]=rec;log.write(json.dumps(rec,separators=(',',':'))+'\n');new+=1
        if not complete:break
       if not complete:break
       if rule%64==63:log.flush();print(json.dumps({'through_rule':rule,'new':new,'seconds':round(time.monotonic()-start,2)}),flush=True)
    gates=('first_order_pass','joint_raw','joint_centered');summary={'status':'complete' if complete else 'checkpointed','expected_cases':24576,'cases':len(records),'reused':len(old),'new':new,'seconds':time.monotonic()-start,'gates':{}}
    sym=list(map(json.loads,(ROOT/'runs/binary_fresh_all256/candidates.jsonl').read_text().splitlines()))
    for gate in gates:
      dr={r['rule'] for r in records if r[gate]};sr={r['rule'] for r in sym if r[gate]};union=dr|sr
      summary['gates'][gate]={'directed_rules':sorted(dr),'directed_count':len(dr),'symmetric_count':len(sr),'intersection_count':len(dr&sr),'directed_only':sorted(dr-sr),'symmetric_only':sorted(sr-dr),'union_count':len(union),'union_missing':sorted(set(range(256))-union),'reflection_closed':all(reflect_rule(r) in dr for r in dr)}
    if complete:assert len(records)==24576
    faithful=[r for r in records if r['first_order_pass']]
    matched={r for r in range(256) if any((x['recipe'][0]['mask'] in ('birth','death'))==(bool(r&1)) for x in faithful if x['rule']==r)}
    summary['mask_selector']={'event_mask_if_derivative_at_zero_is_one_else_stay_mask_rules':sorted(matched),'count':len(matched)}
    summary['costs']={'alphabet_bits':1,'native_radius':2,'native_neighborhood':'5x5','rows':4,'transverse_period':4,'source_window':11,'source_assignments':2048,'independent_information':'source line only','reference_globally_copy':False,'G_scope':'P/D only'}
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');(OUT/'manifest.json').write_text(json.dumps({'reflection_pair':[qname(x) for x in REFS],'derivative':'r XOR 204','integration':'XOR','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n');print(json.dumps({k:v for k,v in summary.items() if k!='gates'}|{'gate_counts':{k:{q:v for q,v in x.items() if not isinstance(v,list)} for k,x in summary['gates'].items()}}))
if __name__=='__main__':main()
