"""Complement-odd directed-mismatch Q for the remaining Rules 23/232."""
import hashlib,itertools,json,time
from pathlib import Path
import numpy as np
from audit_binary_reference import keys,ORDERS
from verify_polarization_proposal import d,encode
from audit_temporal_reach import check

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'runs/directed_reference_23_232'
REFS=[(-2,1,0),(-2,1,1),(-1,2,0),(-1,2,1)]

def qref(s,spec):
    a,b,reverse=spec;x=np.roll(s,-a,axis=-1);y=np.roll(s,-b,axis=-1)
    return ((1-x)&y) if reverse else (x&(1-y))
def qname(spec):
    a,b,r=spec;return f"directed:{a}:{b}:{'not-left-and-right' if r else 'left-and-not-right'}"

def main():
    start=time.monotonic();OUT.mkdir(parents=True,exist_ok=False)
    s=((np.arange(2048)[:,None]>>np.arange(10,-1,-1))&1).astype(np.uint8);mid=5;empty=np.array([],dtype=np.uint64)
    records=[]
    with (OUT/'candidates.jsonl').open('w') as log:
      for rule in (23,232):
       ds=d(s,rule);es=s^ds;ees=es^d(es,rule);g=d(es,rule)^ds^d(ds,rule)
       for mask in ('birth','death','stay_one','stay_zero'):
        for shift in (-1,1):
         choice={'mask':mask,'shift':shift};a=encode(s,rule,choice);b=encode(es,rule,choice);c=encode(ees,rule,choice)
         carrier=np.stack([g[:,mid]^g[:,mid+shift],g[:,mid]],axis=1)
         desired=a[:,:2,mid]^c[:,:2,mid]^carrier;corrected=desired.copy();corrected[:,1]^=rule&1
         for spec in REFS:
          q=qref(s,spec);qn=qref(es,spec);af=np.concatenate([a,q[:,None,:]],axis=1);bf=np.concatenate([b,qn[:,None,:]],axis=1)
          # This nonlinear truth table is not any projection or complemented projection.
          truth=[((1-x)&y) if spec[2] else (x&(1-y)) for x,y in ((0,0),(0,1),(1,0),(1,1))]
          assert truth in ([0,0,1,0],[0,1,0,0])
          for order in ORDERS:
           aa=af[:,order,:];bb=bf[:,order,:];delta=aa^bb;bk=keys(aa,2,2);pk=keys(delta,2,2)[:,[order.index(0),order.index(1)]];bv=delta[...,mid]
           native=check(bk,bv,empty,empty,None);source=check(bk,np.repeat(s[:,mid,None],4,axis=1),empty,empty,None)
           raw=check(bk,bv,pk,desired,None);center=[check(bk,bv,pk,corrected,z) for z in (0,1)]
           first=native['passes'] and source['passes']
           out={'rule':rule,'recipe':[choice],'reference':qname(spec),'reference_spec':spec,'reference_truth_table_00_01_10_11':truth,'order':order,'rx':2,'ry':2,'source_width':11,
             'native':native,'source':source,'parent_recovery':source,'raw':raw,'centered_branches':center,'first_order_pass':first,'joint_raw':first and raw['passes'],'joint_centered':first and any(v['passes'] for v in center),
             'G_scope':'P/D only','off_image_outputs':'unspecified except imposed constraints'}
           records.append(out);log.write(json.dumps(out,separators=(',',':'))+'\n')
    summary={'status':'complete','rules':[23,232],'cases':len(records),'seconds':time.monotonic()-start,'per_rule':{}}
    for rule in (23,232):
      rr=[r for r in records if r['rule']==rule]
      summary['per_rule'][str(rule)]={k:{'recipes':sum(r[k] for r in rr),'exists':any(r[k] for r in rr)} for k in ('first_order_pass','joint_raw','joint_centered')}
      summary['per_rule'][str(rule)]['native']={'recipes':sum(r['native']['passes'] for r in rr),'exists':any(r['native']['passes'] for r in rr)}
      summary['per_rule'][str(rule)]['source']={'recipes':sum(r['source']['passes'] for r in rr),'exists':any(r['source']['passes'] for r in rr)}
    summary['combined']={k:{'rules':sorted({r['rule'] for r in records if r[k]}),'recipes':sum(r[k] for r in records)} for k in ('first_order_pass','joint_raw','joint_centered')}
    summary['costs']={'alphabet_bits':1,'native_neighborhood':'5x5','native_radius':2,'rows':4,'transverse_period':4,'reference_preparation_offsets':[-2,-1,1,2],'independent_information':'source line only','reference_globally_copy_or_complement':False,'reference_degenerates_to_shifted_source_on_old_obstruction_witness':True}
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (OUT/'manifest.json').write_text(json.dumps({'all_source_words':2048,'dependency_window':[-5,5],'derivative_rule':'r XOR 204','integration':'XOR','original_and_centered_G_separate':True,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n')
    print(json.dumps(summary))
if __name__=='__main__':main()
