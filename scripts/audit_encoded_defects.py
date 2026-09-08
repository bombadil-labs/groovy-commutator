"""Independent truth-set audit of every finite-cone defect response."""
from pathlib import Path
import base64
import hashlib
import json
import time
import zlib
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
STEM = ROOT / 'results/encoded_defects_20260908'
ALL = (1 << 512) - 1


def evolve(grid):
    out = []
    for y in range(1, len(grid)-1):
        row = []
        for x in range(1, len(grid[0])-1):
            l,c,r = grid[y][x-1:x+2]
            left = ALL ^ (l | r)
            middle = l ^ r
            right = l & r
            above = (left & grid[y-1][x-1]) | (middle & grid[y-1][x]) | (right & grid[y-1][x+1])
            below = (left & grid[y+1][x-1]) | (middle & grid[y+1][x]) | (right & grid[y+1][x+1])
            row.append(((ALL ^ c) & above) | (c & below))
        out.append(row)
    return out


def array(grid, t):
    m = 4-t
    data = b''.join(grid[y][x].to_bytes(64, 'little') for y in range(m,m+15) for x in range(m,m+10))
    return np.unpackbits(np.frombuffer(data, dtype=np.uint8),bitorder='little').reshape(15,10,512).transpose(2,0,1)


def digest(a):
    return hashlib.sha256(np.packbits(a.ravel(),bitorder='little').tobytes()).hexdigest()


def main():
    start = time.time()
    saved = json.loads(Path(str(STEM)+'_responses.json').read_text())
    classes = json.loads(Path(str(STEM)+'_classifications.json').read_text())
    raw = zlib.decompress(base64.b64decode(classes['data']))
    assert hashlib.sha256(raw).hexdigest() == classes['raw_sha256']
    statuses = np.frombuffer(raw, dtype=np.uint8).reshape(2,64,3,512)
    assert len(saved['records']) == 384 and len(saved['pairs']) == 90
    records = {(r['mode'],r['mask'],r['fine_ticks']):r for r in saved['records']}
    pairs = {(r['mode'],r['a'],r['b'],r['fine_ticks']):r for r in saved['pairs']}
    truth = {i:sum(1 << b for b in range(512) if (b >> (i+4)) & 1) for i in range(-4,5)}
    initial = []
    for y in range(-10,13):
        row = []
        for x in range(-8,10):
            s = truth[x//2]
            row.append((s if x%2==0 else ALL) if y%3==0 else
                       (0 if x%2==0 else ALL) if y%3==1 else
                       (0 if x%2==0 else ALL^s))
        initial.append(row)
    natural = {}; grid = initial
    for t in range(5):
        if t%2==0:
            natural[t] = array(grid,t)
        if t<4:
            grid = evolve(grid)
    responses = np.empty((2,64,3,512,15,10),dtype=np.uint8)
    for mi,mode in enumerate(['periodic','isolated']):
        for mask in range(64):
            grid = [row.copy() for row in initial]
            for yi,y in enumerate(range(-10,13)):
                if mode == 'periodic' or 0<=y<=2:
                    for x in [0,1]:
                        if (mask >> (2*(y%3)+x)) & 1:
                            grid[yi][x+8] ^= ALL
            for t in range(5):
                if t%2==0:
                    observed = array(grid,t); delta = observed ^ natural[t]
                    responses[mi,mask,t//2] = delta
                    r = records[mode,mask,t]
                    assert digest(delta)==r['response_sha256'],(mode,mask,t,'response')
                    # Direct code constraints, independent of primary integer codeword decoder.
                    local = np.ones(512,dtype=bool)
                    for y in range(0,15,3):
                        for x in range(0,10,2):
                            local &= (observed[:,y,x+1]==1) & (observed[:,y+1,x]==0)
                            local &= (observed[:,y+1,x+1]==1) & (observed[:,y+2,x]==0)
                            local &= (observed[:,y,x] != observed[:,y+2,x+1])
                    same = delta.sum(axis=(1,2))==0
                    valid = local if mode=='periodic' else same
                    status = np.where(same,0,np.where(valid,1,2)).astype(np.uint8)
                    assert np.array_equal(status,statuses[mi,mask,t//2])
                    actual = dict(same=int(same.sum()),valid_changed=int((valid & ~same).sum()),
                        outside=int((~valid).sum()),local_valid=int(local.sum()),
                        local_valid_changed=int((local & ~same).sum()),changed_cells=int(delta.sum()),
                        distinct_responses=len(np.unique(np.packbits(delta.reshape(512,-1),axis=1,bitorder='little'),axis=0)))
                    for key,value in actual.items():
                        assert r[key]==value,(mode,mask,t,key)
                if t<4:
                    grid = evolve(grid)
        print(mode,'all response fields and classifications match',flush=True)
    for mi,mode in enumerate(['periodic','isolated']):
        for a in range(6):
            for b in range(a+1,6):
                for ti,t in enumerate([0,2,4]):
                    delta=responses[mi,(1<<a)|(1<<b),ti]^responses[mi,1<<a,ti]^responses[mi,1<<b,ti]
                    r=pairs[mode,a,b,t]
                    assert digest(delta)==r['interaction_sha256']
                    assert int(delta.any(axis=(1,2)).sum())==r['nonlinear_backgrounds']
                    assert int(delta.sum())==r['changed_cells']
    result=dict(response_fields=196608, aggregate_records=384,pair_records=90,
        all_classifications_match=True, seconds=round(time.time()-start,3),
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    Path(str(STEM)+'_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
