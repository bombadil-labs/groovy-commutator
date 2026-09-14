"""Independent cropped-source checks of binary native laws and physical G."""
import argparse,json,time
from pathlib import Path
import numpy as np
from harness import Compiler,derive,load_operator
from verify_reference_covariance import ref,center,table,lookup
from verify_probe_radius import consistent

def keys(grid,rx,ry):
    n=grid.shape[-1];mid=n//2;b=grid[...,mid-rx:mid+rx+1]
    offsets=[0]+list(range(1,ry+1))+list(range(-1,-ry-1,-1))
    block=np.concatenate([np.roll(b,-y,axis=1) for y in offsets],axis=-1)
    return block@(np.uint64(1)<<np.arange(block.shape[-1]-1,-1,-1,dtype=np.uint64))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run',type=Path,required=True);args=ap.parse_args();start=time.perf_counter();root=Path(__file__).resolve().parent
    op=load_operator(root/'lifts/fixed_transverse.py');records=list(map(json.loads,(args.run/'candidates.jsonl').read_text().splitlines()))
    empty=np.array([],dtype=np.uint64);counts={'records':0,'independent_decisions':0,'direct_G_cells':0,'direct_next_cells':0}
    last=None
    for rec in records:
        rx=rec['rx'];ry=rec['ry'];rule=rec['rule'];path=rec['recipe'];order=rec['order'];qname=rec['reference'];tag=(rec['candidate'],qname,ry)
        if tag!=last:
            cp=Compiler(rule,rx+2,op)
            qs=[ref(cp.jets[t],rule,path[0]['shift'],qname,2) for t in range(3)]
            grids=[np.concatenate([cp.encode(path,t)[...,1:-1],qs[t][:,None,:]],axis=1) for t in range(3)]
            ds=cp.source_masks[0];g=cp.source_masks[1]^ds[:,1:-1]^derive(ds,rule);mid=g.shape[-1]//2
            carrier=np.stack([g[:,mid]^g[:,mid+path[0]['shift']],g[:,mid]],axis=1)
            wanted=center(grids[0])[:,:2]^center(grids[2])[:,:2]^carrier;last=tag
        a,b,c=[grid[:,order,:] for grid in grids];delta=a[...,1:-1]^b
        bk=keys(a,rx,ry);pk=keys(delta,rx,ry)[:,[order.index(0),order.index(1)]];bv=center(delta)
        assert consistent(bk,bv,empty,empty)==rec['native']['passes']
        assert consistent(bk,np.repeat(center(cp.source)[:,None],4,axis=1),empty,empty)==rec['source']['passes']
        assert consistent(bk,bv,pk,wanted)==rec['raw']['passes']
        corrected=wanted.copy();corrected[:,1]^=rule&1
        cs=[consistent(bk,bv,pk,corrected,z) for z in (0,1)]
        assert cs==[v['passes'] for v in rec['centered_branches']]
        counts['records']+=1;counts['independent_decisions']+=5
        if rec['joint_raw'] or rec['joint_centered']:
            z=None if rec['joint_raw'] else cs.index(True);tx=table(bk,bv,pk,wanted if z is None else corrected,z)
            kb=keys(b,rx,ry);second=lookup(tx,kb)
            assert np.array_equal(second,center(b)^center(c));counts['direct_next_cells']+=second.size
            phases=[order.index(0),order.index(1)]
            actual=second[:,phases]^center(delta)[:,phases]^lookup(tx,pk);expected=carrier.copy()
            if z is not None:actual^=z;expected[:,1]^=rule&1
            assert np.array_equal(actual,expected);counts['direct_G_cells']+=actual.size
        if counts['records']%4000==0:print(json.dumps({'verified_records':counts['records'],'seconds':round(time.perf_counter()-start,2)}),flush=True)
    counts.update(status='passed',seconds=time.perf_counter()-start)
    (args.run/'verification.json').write_text(json.dumps(counts,indent=2)+'\n');print(json.dumps(counts),flush=True)
if __name__=='__main__':main()
