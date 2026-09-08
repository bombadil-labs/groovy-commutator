"""Frozen W closure and original-pair reachable-state censuses; array evolution."""
from pathlib import Path
import hashlib, json, time, zlib
import numpy as np
from experiment_column_compatibility import step2

ROOT = Path(__file__).resolve().parents[1]
STEM = ROOT / 'results/interface_state_20260908'
FREE = [(0,1),(1,0),(1,1),(2,0),(2,1),(3,0)]


def encode(indices, mode, ticks):
    radius = ticks//2
    ys = np.arange(-2*ticks, 4+2*ticks)
    xs = np.arange(-ticks, 2+ticks)
    f = np.broadcast_to((xs%2)[None,None,:], (len(indices),len(ys),len(xs))).copy().astype(np.uint8)
    for j,x in enumerate(xs):
        block = x//2+radius
        if mode == 'free':
            for v,(y,parity) in enumerate(FREE):
                if x%2 == parity:
                    f[:,y+2*ticks,j] = (indices >> (6*block+v)) & 1
        else:
            a = (indices >> (2*block)) & 1
            b = (indices >> (2*block+1)) & 1
            if x%2:
                f[:,2*ticks,j] = 1^a
                f[:,2+2*ticks,j] = 1^b
            else:
                f[:,1+2*ticks,j] = a
                f[:,3+2*ticks,j] = b
    return f


def words_of(f):
    flat = f.reshape(len(f),-1).astype(np.uint64)
    return np.bitwise_or.reduce(flat << np.arange(flat.shape[1],dtype=np.uint64),axis=1)


def describe(words, mode, ticks):
    rows = list(range(-ticks,4+ticks))
    cells = [(y,x) for y in rows for x in range(2)]
    fields = ((words[:,None] >> np.arange(len(cells),dtype=np.uint64)) & 1).astype(np.uint8)
    changed = fields ^ np.tile([0,1],len(rows))
    fixed = [j for j,c in enumerate(cells) if c not in FREE]
    exterior = [j for j,(y,x) in enumerate(cells) if y<0 or y>3]
    bad = changed[:,fixed].any(axis=1)
    outside = changed[:,exterior].any(axis=1)
    nbits = 18 if mode=='free' else 2*(ticks+1)
    def witness(q):
        q = int(q)
        return dict(input_index=q,input_bits=[(q>>j)&1 for j in range(nbits)],
                    output_word=int(words[q]),output=fields[q].reshape(len(rows),2).tolist(),
                    failed_cells=[list(cells[j]) for j in fixed if changed[q,j]])
    violations=[]
    for j in fixed:
        failed=np.flatnonzero(changed[:,j])
        violations.append(dict(y=cells[j][0],x=cells[j][1],count=len(failed),
                               first_witness=witness(failed[0]) if len(failed) else None))
    affected=[y for j,(y,x) in enumerate(cells) if changed[:,j].any()]
    return dict(mode=mode,ticks=ticks,inputs=len(words),output_rows=rows,
                valid_inputs=int((~bad).sum()),exterior_changed_inputs=int(outside.sum()),
                affected_row_bounds=[min(affected),max(affected)] if affected else None,
                first_failure=witness(np.flatnonzero(bad)[0]) if bad.any() else None,
                fixed_cell_violations=violations,
                output_sha256=hashlib.sha256(words.astype('<u8').tobytes()).hexdigest())


def main():
    start=time.time(); records=[]
    for mode,ticks in [('free',2)]+[('reachable',t) for t in [2,4,6,8]]:
        nbits=18 if mode=='free' else 2*(ticks+1)
        words=np.zeros(1<<nbits,dtype=np.uint64)
        for offset in range(0,len(words),2048):
            q=np.arange(offset,min(offset+2048,len(words)),dtype=np.uint64)
            f=encode(q,mode,ticks)
            for _ in range(ticks): f=step2(f,shrink=True)
            words[offset:offset+len(q)]=words_of(f)
        record=describe(words,mode,ticks);records.append(record)
        # The scratch cache supports exact independent array comparison; it is reproducible.
        np.save('/tmp/interface_state_'+mode+'_'+str(ticks)+'.npy',words)
        if mode=='free':
            packed=dict(format='zlib hex of uint64 little-endian in input-index order',
                        output_sha256=record['output_sha256'],data=zlib.compress(words.astype('<u8').tobytes(),9).hex())
            Path(str(STEM)+'_free_outputs.json').write_text(json.dumps(packed,indent=2)+'\n')
        print(mode,ticks,'valid',record['valid_inputs'],'/',len(words),'outside',record['exterior_changed_inputs'],flush=True)
    sources=['scripts/experiment_interface_state.py','scripts/experiment_column_compatibility.py',
             'docs/research/protocols/interface-state-20260908.md']
    result=dict(censuses=records,seconds=round(time.time()-start,3),
                sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources})
    Path(str(STEM)+'_census.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
