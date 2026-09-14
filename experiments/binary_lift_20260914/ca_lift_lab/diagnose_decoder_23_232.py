"""Exact decoder obstruction for Rules 23/232 in the P/D/M/Q family.

Classify local source collisions by known phase, then verify a stronger global
complement collision for every mask/sign/Q/order recipe on a period-2 or
period-6 source orbit.  A pointwise whole-image collision defeats every local
decoder radius, even with row labels; it does not obstruct native quotient
dynamics.
"""
import hashlib,json,time
from pathlib import Path
import numpy as np
from audit_binary_reference import keys
from verify_polarization_proposal import d,encode
from audit_reference_covariance import reference

ROOT=Path(__file__).resolve().parent
RUN=ROOT/'runs/binary_fresh_all256'
OUT=ROOT/'runs/decoder_obstruction_23_232'

def collision(k,b):
    order=np.argsort(k,kind='stable');ks=k[order];bs=b[order]
    bad=np.flatnonzero((ks[1:]==ks[:-1])&(bs[1:]!=bs[:-1]))
    if not len(bad):return None
    j=int(bad[0]);return {'key':int(ks[j]),'event_indices':[int(order[j]),int(order[j+1])],'bits':[int(bs[j]),int(bs[j+1])]}

def ring(pattern):return np.array([[int(x) for x in pattern]],dtype=np.uint8)

def main():
    start=time.monotonic();OUT.mkdir(parents=True,exist_ok=False)
    rows=[r for r in map(json.loads,(RUN/'candidates.jsonl').read_text().splitlines()) if r['rule'] in (23,232)]
    assert len(rows)==192 and all(not r['source']['passes'] for r in rows)
    s=((np.arange(2048)[:,None]>>np.arange(10,-1,-1))&1).astype(np.uint8);mid=5
    records=[];global_checks=0;phase_checks=0
    for rec in rows:
        rule=rec['rule'];choice=rec['recipe'][0];qname=rec['reference'];order=tuple(rec['order'])
        a=encode(s,rule,choice);q=reference(s,rule,choice,qname)
        grid=np.concatenate([a,q[:,None,:]],axis=1)[:,order,:];bk=keys(grid,2,2);target=np.repeat(s[:,mid,None],4,axis=1)
        phases=[]
        for phase in range(4):
            w=collision(bk[:,phase],target[:,phase]);phase_checks+=1
            phases.append({'physical_phase':phase,'field':('P','D',choice['mask'],'Q')[order[phase]],'passes':w is None,'collision':w})
        # D_232 is the isolated-center indicator. D_23 is its complement.
        # For birth/death, mask equality under S->~S needs D=0 everywhere;
        # for stay masks it needs D=1. Pick alternating (D_232=1) or
        # 000111 (D_232=0), swapping them between the two rules.
        want_d232=0 if ((choice['mask'] in ('birth','death'))==(rule==232)) else 1
        pattern='000111' if want_d232==0 else '01';x=ring(pattern);xc=1-x
        def enc(z):
            base=encode(z,rule,choice);qv=reference(z,rule,choice,qname)
            return np.concatenate([base,qv[:,None,:]],axis=1)[:,order,:]
        ex,ec=enc(x),enc(xc);nx=x^d(x,rule);nc=xc^d(xc,rule)
        enx,encx=enc(nx),enc(nc)
        assert np.array_equal(ex,ec) and np.array_equal(enx,encx)
        assert np.array_equal(d(x,rule),d(xc,rule));assert np.all(x!=xc)
        global_checks+=1
        records.append({'rule':rule,'mask':choice['mask'],'shift':choice['shift'],'reference':qname,'order':order,
          'known_phase_decoder_passes':[p['passes'] for p in phases],'phase_collisions':phases,
          'whole_image_collision':{'period':len(pattern),'source':pattern,'complement':''.join(str(int(v)) for v in xc[0]),
            'prepared_equal_pointwise':True,'next_prepared_equal_pointwise':True,'source_center_differs':True,
            'D_is_complement_invariant':True,'P_is_complement_invariant':True,'M_is_zero_on_witness':bool(not ex[:,order.index(2)].any()),
            'Q_is_zero_on_witness':bool(not ex[:,order.index(3)].any())}})
    assert all(not any(r['known_phase_decoder_passes']) for r in records)
    summary={'status':'passed','recipes':len(records),'rules':[23,232],'known_phase_checks':phase_checks,
      'known_phase_failures':sum(4-sum(r['known_phase_decoder_passes']) for r in records),'whole_image_collisions':global_checks,
      'periods':[2,6],'cause':'global color bit erased on complement-paired period-2/6 source orbits',
      'implications':['not an unlabeled-row ambiguity','row order and phase labels cannot repair it','no decoder radius repairs unchanged encoding','native evolution is quotient dynamics and remains consistent'],
      'next_reference_hypothesis':'replace AND Q by a complement-odd directed mismatch x AND (NOT y), or its reverse, at the same distance-three offsets',
      'seconds':time.monotonic()-start}
    (OUT/'collisions.jsonl').write_text(''.join(json.dumps(r,separators=(',',':'))+'\n' for r in records))
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (OUT/'manifest.json').write_text(json.dumps({'exhaustive_recipes':True,'source_words_for_local_phase_check':2048,
      'local_native_radius':2,'whole_image_proof':'direct periodic formula for every recipe','alphabet_bits':1,'G_not_tested':True,
      'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n')
    print(json.dumps(summary))

if __name__=='__main__':main()
