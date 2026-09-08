"""Post-census four-cell witness, audited by scalar coordinates at every tick."""
from pathlib import Path
import hashlib,json,time
import numpy as np
from experiment_column_compatibility import step2

ROOT=Path(__file__).resolve().parents[1]
STEM=ROOT/'results/interface_state_20260908'


def scalar_step(f):
    h,w=f.shape;out=np.zeros((h-2,w-2),dtype=np.uint8)
    for y in range(1,h-1):
        for x in range(1,w-1):
            row=y+1 if f[y,x] else y-1
            column=x+int(f[y,x-1])+int(f[y,x+1])-1
            out[y-1,x-1]=f[row,column]
    return out


def main():
    start=time.time();ys=np.arange(-64,68);xs=np.arange(-64,68)
    f=np.tile(xs%2,(len(ys),1)).astype(np.uint8)
    seed=[(0,3),(1,2),(2,1),(3,0)]
    for y,x in seed:f[y+64,x+64]^=1
    other=np.tile(xs%2,(len(ys),1)).astype(np.uint8)
    # Direct original-strip encoding for the audit's independently built initial state.
    other[64,67]=0;other[65,66]=1;other[66,65]=0;other[67,64]=1
    assert np.array_equal(f,other)
    records=[];checked=0
    for t in range(33):
        assert np.array_equal(f,other);checked+=f.size
        ycoords=ys[t:len(ys)-t];xcoords=xs[t:len(xs)-t]
        background=(xcoords%2)^(t%2)
        points=np.argwhere(f^background)
        changed=[[int(ycoords[y]),int(xcoords[x])] for y,x in points]
        bounds=[min(y for y,x in changed),max(y for y,x in changed),
                min(x for y,x in changed),max(x for y,x in changed)] if changed else None
        records.append(dict(tick=t,mass=len(changed),bounds=bounds,changed=changed,
                            top=[p for p in changed if p[0]==bounds[0]] if bounds else [],
                            bottom=[p for p in changed if p[0]==bounds[1]] if bounds else []))
        if t<32:f=step2(f,shrink=True);other=scalar_step(other)
    result=dict(seed=seed,records=records,independent_cell_comparisons=checked,
                seconds=round(time.time()-start,3),
                sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in
                        ['scripts/check_interface_witness.py','docs/research/protocols/interface-witness-20260908.md']})
    Path(str(STEM)+'_witness.json').write_text(json.dumps(result,indent=2)+'\n')
    for r in records:print(r['tick'],r['mass'],r['bounds'],'top',r['top'],'bottom',r['bottom'])


if __name__=='__main__':main()
