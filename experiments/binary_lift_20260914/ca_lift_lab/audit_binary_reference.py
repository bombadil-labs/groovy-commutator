"""Binary rows P,D,M,Q: every cyclic ordering; native G on P/D only.
All candidates retain only binary cells, have no channel or row-role input,
and must decode the source and update every row from their native patch.
"""
import argparse,hashlib,itertools,json,time
from pathlib import Path
import numpy as np
from verify_polarization_proposal import d,encode
from audit_reference_covariance import reference
from audit_temporal_reach import check
ROOT=Path(__file__).resolve().parent
ORDERS=[(0,)+p for p in itertools.permutations((1,2,3))]

def keys(grid,rx,ry):
    n=grid.shape[1];mid=grid.shape[-1]//2
    result=np.zeros(grid.shape[:2],dtype=np.uint64)
    for dy in (0,)+tuple(range(1,ry+1))+tuple(range(-1,-ry-1,-1)):
        for dx in range(-rx,rx+1):result=(result<<1)|grid[:,(np.arange(n)+dy)%n,mid+dx]
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();args.output.mkdir(parents=True,exist_ok=False)
    prior=[r for r in map(json.loads,(ROOT/'runs/probe_radius_2/candidates.jsonl').read_text().splitlines()) if r['horizontal_radius']==2]
    start=time.perf_counter();records=[];rx=2;width=2*rx+7;mid=width//2
    s=((np.arange(1<<width)[:,None]>>np.arange(width-1,-1,-1))&1).astype(np.uint8)
    ek=np.array([],dtype=np.uint64);ev=np.array([],dtype=np.uint8)
    with (args.output/'candidates.jsonl').open('w') as log:
        for ry in (1,2):
            for rec in prior:
                rule=rec['rule'];choice=rec['recipe'][0];ds=d(s,rule);es=s^ds;ees=es^d(es,rule)
                a=encode(s,rule,choice);b=encode(es,rule,choice);c=encode(ees,rule,choice)
                g=d(es,rule)^ds^d(ds,rule)
                carrier=np.stack([g[:,mid]^g[:,mid+choice['shift']],g[:,mid]],axis=1)
                for qname in ('pair:-2:1','pair:-1:2'):
                    q=reference(s,rule,choice,qname);qn=reference(es,rule,choice,qname)
                    af=np.concatenate([a,q[:,None,:]],axis=1);bf=np.concatenate([b,qn[:,None,:]],axis=1)
                    # C is needed only at the P/D target rows, not the Q row.
                    desired=a[:,:2,mid]^c[:,:2,mid]^carrier
                    for order in ORDERS:
                        aa=af[:,order,:];bb=bf[:,order,:];delta=aa^bb
                        bk=keys(aa,rx,ry);pk=keys(delta,rx,ry)[:,[order.index(0),order.index(1)]]
                        bv=delta[...,mid]
                        native=check(bk,bv,ek,ev,None)
                        src=check(bk,np.repeat(s[:,mid,None],4,axis=1),ek,ev,None)
                        raw=check(bk,bv,pk,desired,None)
                        corrected=desired.copy();corrected[:,1]^=rule&1
                        centered=[check(bk,bv,pk,corrected,z) for z in (0,1)]
                        gates=native['passes'] and src['passes']
                        out={'candidate':rec['candidate'],'rule':rule,'recipe':rec['recipe'],'reference':qname,'order':order,'rx':rx,'ry':ry,'source_width':width,'native':native,'source':src,'raw':raw,'centered_branches':centered,'first_order_pass':gates,'joint_raw':gates and raw['passes'],'joint_centered':gates and any(v['passes'] for v in centered)}
                        records.append(out);log.write(json.dumps(out,separators=(',',':'))+'\n')
            log.flush()
            rows=[r for r in records if r['ry']==ry]
            print(json.dumps({'ry':ry,'seconds':round(time.perf_counter()-start,3),'counts':{k:len({r['rule'] for r in rows if r[k]}) for k in ('first_order_pass','joint_raw','joint_centered')},'rule110':{k:sum(r[k] for r in rows if r['rule']==110) for k in ('first_order_pass','joint_raw','joint_centered')}}),flush=True)
    summary={str(ry):{k:sorted({r['rule'] for r in records if r['ry']==ry and r[k]}) for k in ('first_order_pass','joint_raw','joint_centered')} for ry in (1,2)}
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (args.output/'manifest.json').write_text(json.dumps({'seconds':time.perf_counter()-start,'admitted_variants':596,'admitted_rules':192,'orders':ORDERS,'rx':2,'ry':[1,2],'source_width':11,'references':['pair:-2:1','pair:-1:2'],'bits_per_physical_cell':1,'period':4,'source_recovery_is_gate':True,'G_only_P_D_rows':True,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n')
    (args.output/'source_audit.py').write_text(Path(__file__).read_text())
if __name__=='__main__':main()
