"""Independent cropped-source two-channel census and direct physical-G check."""
import argparse,json,time
from pathlib import Path
import numpy as np
from harness import Compiler,derive,load_operator
from verify_temporal_reach import read
from verify_probe_radius import consistent

def ref(s,rule,sign,name,qr):
    n=s.shape[-1];take=lambda off:s[:,qr+off:n-qr+off]
    x=take(0)
    if name=='none':return np.zeros_like(x)
    if name=='S':return x
    if name=='P':return x^take(sign)
    idx=4*take(-1)+2*x+take(1);ds=(((rule^204)>>idx)&1).astype(np.uint8)
    if name=='D':return ds
    if name=='birth':return (1-x)*ds
    if name=='death':return x*ds
    if name=='stay_one':return x*(1-ds)
    if name=='stay_zero':return (1-x)*(1-ds)
    if name.startswith('pair:'):
        left,right=map(int,name.split(':')[1:]);return take(left)*take(right)
    bit={'AL':4,'AC':2,'AR':1}[name]
    return (((rule>>idx)^(rule>>(idx^bit)))&1).astype(np.uint8)

def keys(x,q,rx):
    w=2*rx+1;m=q.shape[-1]//2
    v=q[:,m-rx:m+rx+1] @ (np.uint64(1)<<np.arange(w-1,-1,-1,dtype=np.uint64))
    return read(x,rx)*(1<<w)+v[:,None]

def center(a):return a[...,a.shape[-1]//2]

def table(bk,bv,pk,pv,z):
    out={} if z is None else {0:z}
    for k,v in zip(bk.ravel().tolist(),bv.ravel().tolist()):
        assert k not in out or out[k]==v;out[k]=v
    for k,v in zip(pk.ravel().tolist(),pv.ravel().tolist()):
        v^=z or 0;assert k not in out or out[k]==v;out[k]=v
    return out

def lookup(t,ks):return np.array([t[int(k)] for k in ks.ravel()],dtype=np.uint8).reshape(ks.shape)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run',type=Path,required=True);args=ap.parse_args();started=time.perf_counter()
    root=Path(__file__).resolve().parent;op=load_operator(root/'lifts/fixed_transverse.py')
    manifest=json.loads((args.run/'manifest.json').read_text());qr=manifest.get('q_radius',1)
    records=list(map(json.loads,(args.run/'candidates.jsonl').read_text().splitlines()))
    prior={(r['candidate'],r['horizontal_radius']):r for r in map(json.loads,(root/'runs/probe_radius_2/candidates.jsonl').read_text().splitlines())}
    last=None;checks=0;direct=0;controls=0
    for rec in records:
        tag=(rec['candidate'],rec['radius']);rx=rec['radius'];rule=rec['rule'];path=rec['recipe'];name=rec['reference']
        if tag!=last:
            cp=Compiler(rule,rx+qr,op);a=cp.encode(path);b=cp.encode(path,1);c=cp.encode(path,2);delta=cp.mask(path)
            ds=cp.source_masks[0];g=cp.source_masks[1]^ds[:,1:-1]^derive(ds,rule);mid=g.shape[-1]//2
            carrier=np.stack([g[:,mid]^g[:,mid+path[0]['shift']],g[:,mid]],axis=1)
            wanted=center(a)[:,:2]^center(c)[:,:2]^carrier;bv=center(delta)
            last=tag
        q=ref(cp.source,rule,path[0]['shift'],name,qr);qn=ref(cp.jets[1],rule,path[0]['shift'],name,qr);qnn=ref(cp.jets[2],rule,path[0]['shift'],name,qr);dq=q[:,1:-1]^qn
        bk=keys(a,q,rx);pk=keys(delta,dq,rx)[:,:2];qv=np.repeat(center(dq)[:,None],3,axis=1)
        qgood=consistent(bk,qv,np.array([],dtype=np.uint64),np.array([],dtype=np.uint8))
        assert qgood==rec['reference_update']['passes']
        assert consistent(bk,bv,pk,wanted)==rec['raw']['passes']
        corrected=wanted.copy();corrected[:,1]^=rule&1
        centered=[consistent(bk,bv,pk,corrected,z) for z in (0,1)]
        assert centered==[v['passes'] for v in rec['centered_branches']]
        checks+=4
        if name=='none':
            old=prior[tag]['probes']['temporal']
            assert rec['raw']['passes']==old['raw']['passes'] and centered==[v['passes'] for v in old['centered_branches']];controls+=1
        if rec['joint_raw'] or rec['joint_centered']:
            z=None if rec['joint_raw'] else centered.index(True);desired=wanted if z is None else corrected
            tx=table(bk,bv,pk,desired,z);tq=table(bk,qv,np.array([],dtype=np.uint64),np.array([],dtype=np.uint8),None)
            bkeys=keys(b,qn,rx)
            # Both components actually advance the prepared state a second time.
            assert np.array_equal(lookup(tx,bkeys),center(b)^center(c))
            assert np.array_equal(lookup(tq,bkeys),np.repeat((center(qn)^center(qnn))[:,None],3,axis=1))
            actual=lookup(tx,bkeys)[:,:2]^center(delta)[:,:2]^lookup(tx,pk)
            expected=carrier.copy()
            if z is not None:actual^=z;expected[:,1]^=rule&1
            assert np.array_equal(actual,expected),(rule,name,rx)
            direct+=actual.size
    result={'status':'passed','records':len(records),'independent_branch_and_update_decisions':checks,'no_reference_controls_match_prior':controls,'direct_physical_G_cell_checks':direct,'seconds':time.perf_counter()-started}
    (args.run/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
if __name__=='__main__':main()
