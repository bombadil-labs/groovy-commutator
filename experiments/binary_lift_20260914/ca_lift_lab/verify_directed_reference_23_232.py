"""Independent cropped-source verification of directed-Q cases."""
import json,time
from pathlib import Path
import numpy as np
from harness import Compiler,derive,load_operator
from verify_binary_reference import keys
from verify_reference_covariance import center,table,lookup
from verify_probe_radius import consistent

ROOT=Path(__file__).resolve().parent;RUN=ROOT/'runs/directed_reference_23_232'
def ref(s,name,qr=2):
    parts=name.split(':');a,b=int(parts[1]),int(parts[2]);reverse=parts[3]=='not-left-and-right';n=s.shape[-1]
    take=lambda off:s[:,qr+off:n-qr+off]
    x,y=take(a),take(b)
    return ((1-x)&y) if reverse else (x&(1-y))

def main():
    start=time.monotonic();op=load_operator(ROOT/'lifts/fixed_transverse.py');records=list(map(json.loads,(RUN/'candidates.jsonl').read_text().splitlines()))
    empty=np.array([],dtype=np.uint64);counts={'records':0,'independent_decisions':0,'direct_G_cells':0,'direct_next_cells':0}
    for rec in records:
        rx=rec['rx'];ry=rec['ry'];rule=rec['rule'];path=rec['recipe'];path[0].update(offsets=[],geometry='straight');order=rec['order'];name=rec['reference']
        cp=Compiler(rule,rx+2,op);qs=[ref(cp.jets[t],name) for t in range(3)]
        grids=[np.concatenate([cp.encode(path,t)[...,1:-1],qs[t][:,None,:]],axis=1) for t in range(3)]
        ds=cp.source_masks[0];g=cp.source_masks[1]^ds[:,1:-1]^derive(ds,rule);mid=g.shape[-1]//2
        carrier=np.stack([g[:,mid]^g[:,mid+path[0]['shift']],g[:,mid]],axis=1)
        wanted=center(grids[0])[:,:2]^center(grids[2])[:,:2]^carrier
        a,b,c=[grid[:,order,:] for grid in grids];delta=a[...,1:-1]^b
        bk=keys(a,rx,ry);pk=keys(delta,rx,ry)[:,[order.index(0),order.index(1)]];bv=center(delta)
        assert consistent(bk,bv,empty,empty)==rec['native']['passes']
        assert consistent(bk,np.repeat(center(cp.source)[:,None],4,axis=1),empty,empty)==rec['source']['passes']
        assert rec['parent_recovery']['passes']==rec['source']['passes']
        assert consistent(bk,bv,pk,wanted)==rec['raw']['passes']
        corrected=wanted.copy();corrected[:,1]^=rule&1
        cs=[consistent(bk,bv,pk,corrected,z) for z in (0,1)]
        assert cs==[v['passes'] for v in rec['centered_branches']]
        counts['records']+=1;counts['independent_decisions']+=6
        if rec['joint_raw'] or rec['joint_centered']:
            z=None if rec['joint_raw'] else cs.index(True);tx=table(bk,bv,pk,wanted if z is None else corrected,z)
            bkeys=keys(b,rx,ry);second=lookup(tx,bkeys)
            assert np.array_equal(second,center(b)^center(c));counts['direct_next_cells']+=second.size
            phases=[order.index(0),order.index(1)]
            actual=second[:,phases]^center(delta)[:,phases]^lookup(tx,pk);expected=carrier.copy()
            if z is not None:actual^=z;expected[:,1]^=rule&1
            assert np.array_equal(actual,expected);counts['direct_G_cells']+=actual.size
    counts.update(status='passed',seconds=time.monotonic()-start)
    (RUN/'verification.json').write_text(json.dumps(counts,indent=2)+'\n');print(json.dumps(counts))
if __name__=='__main__':main()
