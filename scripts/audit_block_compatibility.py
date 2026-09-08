"""Independently audit every block/frame outcome using Boolean truth sets.

No primary update or decoder is imported. Physical horizontal boundaries
shrink each tick, rather than wrapping as in the primary array calculation.
"""
from pathlib import Path
import base64
import hashlib
import json
import time
import zlib
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
STEM=ROOT/'results/block_compatibility_20260908'


def setup(w,k,u):
    positions={p//w for p in range(u-k,u+w+k)}|{-1,0,1}
    low,high=min(positions),max(positions);n=high-low+1
    full=(1<<(2**n))-1
    variables=[sum(((z>>i)&1)<<z for z in range(2**n)) for i in range(n)]
    q=[4*((z>>(-1-low))&1)+2*((z>>(-low))&1)+((z>>(1-low))&1) for z in range(2**n)]
    rule_for_truth={sum(((r>>j)&1)<<z for z,j in enumerate(q)):r for r in range(256)}
    return low,variables,full,rule_for_truth


def evolve_truth(m,w,a,b,k,variables,full):
    grid=[]
    for y in range(m):
        row=[]
        for var in variables:
            for j in range(w):
                bit=y*w+j;zero=(a>>bit)&1;diff=((a^b)>>bit)&1
                row.append((full if zero else 0)^(var if diff else 0))
        grid.append(row)
    for _ in range(k):
        output=[]
        for y in range(m):
            row=[]
            for x in range(1,len(grid[0])-1):
                left,c,right=grid[y][x-1:x+2]
                n0=(full^left)&(full^right);n1=left^right;n2=left&right
                above=grid[(y-1)%m];below=grid[(y+1)%m]
                zero=(n0&above[x-1])|(n1&above[x])|(n2&above[x+1])
                one=(n0&below[x-1])|(n1&below[x])|(n2&below[x+1])
                row.append(((full^c)&zero)|(c&one))
            output.append(row)
        grid=output
    return grid


def classify(grid,m,w,a,b,v,x,full,rule_for_truth):
    first=((a^b)&-(a^b)).bit_length()-1
    y0,j0=divmod(first,w)
    truth=grid[(y0+v)%m][x+j0]^(full if (a>>first)&1 else 0)
    for y in range(m):
        for j in range(w):
            bit=y*w+j
            expected=(full if (a>>bit)&1 else 0)^(truth if ((a^b)>>bit)&1 else 0)
            if grid[(y+v)%m][x+j]!=expected:return -1
    return rule_for_truth.get(truth,-2)


def main():
    started=time.time();checked=groups=0
    records=json.loads(Path(str(STEM)+'_outcomes.json').read_text())
    assert {(r['m'],r['w']) for r in records['rectangles']}=={(m,w) for m in range(1,7) for w in range(1,7) if m*w<=6}
    for record in records['rectangles']:
        m,w=record['m'],record['w'];alphabet=2**(m*w)
        params=[tuple(p) for p in record['parameters']]
        expected=[]
        for k in [1,2,3]:
            vs=sorted({min((j for j in range(-k,k+1) if (j-v)%m==0),key=lambda j:(abs(j),j)) for v in range(-k,k+1)})
            expected.extend((k,u,v) for u in range(-k,k+1) for v in vs)
        assert params==expected
        raw=zlib.decompress(base64.b64decode(record['data']))
        assert hashlib.sha256(raw).hexdigest()==record['raw_sha256']
        original=np.frombuffer(raw,dtype='<i2').reshape(record['shape'])
        assert original.shape==(alphabet*(alphabet-1),len(params))
        index={p:i for i,p in enumerate(params)}
        for k in [1,2,3]:
            for u in range(-k,k+1):
                low,variables,full,rule_for_truth=setup(w,k,u)
                x=-low*w+u-k
                vs=[v for kk,uu,v in params if kk==k and uu==u]
                pair=0
                for a in range(alphabet):
                    for b in range(alphabet):
                        if a==b:continue
                        grid=evolve_truth(m,w,a,b,k,variables,full)
                        for v in vs:
                            result=classify(grid,m,w,a,b,v,x,full,rule_for_truth)
                            assert result==original[pair,index[(k,u,v)]],(m,w,a,b,k,u,v,result,original[pair,index[(k,u,v)]])
                            checked+=1
                        pair+=1;groups+=1
        print(f'Audited {m}x{w}: {original.size} outcomes, total {checked}',flush=True)
    output=dict(independent_outcomes=checked,independent_truth_evolutions=groups,
                seconds=round(time.time()-started,3),
                script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                scope='Every saved outcome, independently checked with truth sets and shrinking horizontal windows; includes complete enumeration of the protocol parameter grid.')
    Path(str(STEM)+'_audit.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))


if __name__=='__main__':main()
