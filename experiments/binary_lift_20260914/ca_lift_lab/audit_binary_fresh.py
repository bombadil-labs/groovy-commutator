"""Full unfiltered radius-two census; cache identical old four-row cases."""
import hashlib,itertools,json,time
from pathlib import Path
import numpy as np
from audit_binary_reference import keys,ORDERS
from verify_polarization_proposal import d,encode
from audit_reference_covariance import reference
from audit_temporal_reach import check

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'runs/binary_fresh_all256'
def tag(r):
    c=r['recipe'][0]
    return (r['rule'],c['mask'],c['shift'],r['reference'],tuple(r['order']))

def main():
    start=time.monotonic();OUT.mkdir(exist_ok=True)
    old=[r for r in map(json.loads,(ROOT/'runs/binary_reference_4rows/candidates.jsonl').read_text().splitlines()) if r['rx']==2 and r['ry']==2]
    cache={tag(r):r for r in old}
    assert len(cache)==7152
    logpath=OUT/'candidates.jsonl'
    if logpath.exists():
        cache.update({tag(r):r for r in map(json.loads,logpath.read_text().splitlines())})
    else:
        logpath.write_text(''.join(json.dumps(r,separators=(',',':'))+'\n' for r in old))
    s=((np.arange(2048)[:,None]>>np.arange(10,-1,-1))&1).astype(np.uint8)
    empty=np.array([],dtype=np.uint64);mid=5;new=0;complete=True
    with logpath.open('a') as log:
        for rule in range(256):
            ds=d(s,rule);es=s^ds;ees=es^d(es,rule);g=d(es,rule)^ds^d(ds,rule)
            for mi,mask in enumerate(('birth','death','stay_one','stay_zero')):
                for shift in (-1,1):
                    choice={'mask':mask,'shift':shift}
                    missing=[(q,o) for q in ('pair:-2:1','pair:-1:2') for o in ORDERS if (rule,mask,shift,q,o) not in cache]
                    if not missing:continue
                    if time.monotonic()-start>112:
                        complete=False;break
                    a=encode(s,rule,choice);b=encode(es,rule,choice);c=encode(ees,rule,choice)
                    carrier=np.stack([g[:,mid]^g[:,mid+shift],g[:,mid]],axis=1)
                    desired=a[:,:2,mid]^c[:,:2,mid]^carrier
                    corrected=desired.copy();corrected[:,1]^=rule&1
                    for qname in ('pair:-2:1','pair:-1:2'):
                        q=reference(s,rule,choice,qname);qn=reference(es,rule,choice,qname)
                        af=np.concatenate([a,q[:,None,:]],axis=1);bf=np.concatenate([b,qn[:,None,:]],axis=1)
                        for order in ORDERS:
                            key=(rule,mask,shift,qname,order)
                            if key in cache:continue
                            aa=af[:,order,:];bb=bf[:,order,:];delta=aa^bb
                            bk=keys(aa,2,2);pk=keys(delta,2,2)[:,[order.index(0),order.index(1)]];bv=delta[...,mid]
                            native=check(bk,bv,empty,empty,None)
                            src=check(bk,np.repeat(s[:,mid,None],4,axis=1),empty,empty,None)
                            raw=check(bk,bv,pk,desired,None)
                            centered=[check(bk,bv,pk,corrected,z) for z in (0,1)]
                            gates=native['passes'] and src['passes']
                            out={'candidate':10000+rule*8+mi*2+(shift==1),'rule':rule,'recipe':[choice],'reference':qname,'order':order,'rx':2,'ry':2,'source_width':11,'native':native,'source':src,'raw':raw,'centered_branches':centered,'first_order_pass':gates,'joint_raw':gates and raw['passes'],'joint_centered':gates and any(v['passes'] for v in centered),'provenance':'fresh_unfiltered'}
                            cache[key]=out;log.write(json.dumps(out,separators=(',',':'))+'\n');new+=1
                if not complete:break
            if not complete:break
            if rule%64==63:log.flush();print(json.dumps({'through_rule':rule,'new_cases':new,'seconds':round(time.monotonic()-start,2)}),flush=True)
    rows=list(cache.values());gates=('first_order_pass','joint_raw','joint_centered')
    summary={'complete':complete,'expected_cases':24576,'actual_cases':len(rows),'reused_cases':7152,'new_this_run':new,'seconds':time.monotonic()-start,'gates':{},'separate_first_order':{g:sorted({r['rule'] for r in rows if r[g]['passes']}) for g in ('native','source')}}
    for gate in gates:
        passed=sorted({r['rule'] for r in rows if r[gate]});previous={r['rule'] for r in old if r[gate]}
        summary['gates'][gate]={'rules':passed,'count':len(passed),'new_rules':sorted(set(passed)-previous),'failed_rules':sorted(set(range(256))-set(passed)) if complete else None}
    if complete:assert len(cache)==24576
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (OUT/'manifest.json').write_text(json.dumps({'complete':complete,'source_width':11,'dependency_window':[-5,5],'native_radius':2,'all_source_words':2048,'source_derivative':'r XOR 204','alphabet_bits':1,'period':4,'source_recovery_is_parent_recovery_at_first_floor':True,'G_only_P_D':True,'off_image_outputs':'unspecified except imposed G probes and centered zero branch','old_cache_sha256':hashlib.sha256((ROOT/'runs/binary_reference_4rows/candidates.jsonl').read_bytes()).hexdigest(),'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n')
    print(json.dumps(summary),flush=True)

if __name__=='__main__':main()
