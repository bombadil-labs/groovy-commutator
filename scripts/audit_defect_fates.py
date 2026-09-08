"""Independent uint64 truth-set audit: one bit for each of 64 physical masks."""
from pathlib import Path
import base64,hashlib,json,time,zlib
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
STEM=ROOT/'results/defect_fates_20260908'
FULL=np.uint64(2**64-1)


def mux(left,center,right,up,down):
    a=~(left|right);b=left^right;c=left&right
    above=(a&up[0])|(b&up[1])|(c&up[2])
    below=(a&down[0])|(b&down[1])|(c&down[2])
    return ((~center)&above)|(center&below)


def advance(grid,mode):
    if mode=='periodic':
        up=np.roll(grid,1,axis=0);down=np.roll(grid,-1,axis=0)
        return mux(grid[:,:-2],grid[:,1:-1],grid[:,2:],
                   [up[:,:-2],up[:,1:-1],up[:,2:]],[down[:,:-2],down[:,1:-1],down[:,2:]])
    return mux(grid[1:-1,:-2],grid[1:-1,1:-1],grid[1:-1,2:],
               [grid[:-2,:-2],grid[:-2,1:-1],grid[:-2,2:]],
               [grid[2:,:-2],grid[2:,1:-1],grid[2:,2:]])


def unpack(grid):
    raw=np.frombuffer(grid.astype('<u8').tobytes(),dtype=np.uint8)
    return np.unpackbits(raw,bitorder='little').reshape(*grid.shape,64).transpose(2,0,1)


def encode_value(s,y,x):
    if y%3==0:return s if x%2==0 else 1
    if y%3==1:return x%2
    return 0 if x%2==0 else 1-s


def tiles(bg):
    if 'period' not in bg:return None
    word=bg['word'];p=len(word)
    g=np.array([[encode_value(word[(x//2)%p],y,x) for x in range(2*p)] for y in range(3)],dtype=np.uint64)
    values=[g]
    for _ in range(32):
        padded=np.pad(values[-1],((1,1),(1,1)),mode='wrap')
        values.append(advance(padded,'isolated')&1)
    return values


def assess(d,x,mode):
    loc=np.where(d!=0);mass=len(loc[0]);h=d.shape[0]
    if mass:
        yl,yh=int(loc[0].min()),int(loc[0].max());xl,xh=int(loc[1].min()),int(loc[1].max())
        offset=0 if mode=='periodic' else -33
        box=[yl+offset,yh+offset,xl-32,xh-32]
        a,b=(0,h-1) if mode=='periodic' else (yl,yh)
        n=d[a:b+1,xl:xh+1]
        norm=(n.shape,np.packbits(n.ravel(),bitorder='little').tobytes(),(0 if mode=='periodic' else box[0],box[2]))
    else:box=[-999]*4;norm=None
    local=bool((x[0::3,1::2]==1).all() and (x[1::3,0::2]==0).all() and
               (x[1::3,1::2]==1).all() and (x[2::3,0::2]==0).all() and
               (x[0::3,0::2]!=x[2::3,1::2]).all())
    status=0 if not mass else 1 if mode=='periodic' and local else 2
    return [mass,*box,int(local),status],norm


def scan(hist,t,tile):
    found=[]
    for distance in range(1,5):
        p=2*distance
        if len(hist)<2*distance+1:continue
        a,b,c=hist[-1-2*distance],hist[-1-distance],hist[-1]
        if any(n is None for n in [a,b,c]):continue
        if not (a[0]==b[0]==c[0] and a[1]==b[1]==c[1]):continue
        dy=b[2][0]-a[2][0];dx=b[2][1]-a[2][1]
        if (dy,dx)!=(c[2][0]-b[2][0],c[2][1]-b[2][1]) or abs(dy)>p or abs(dx)>p:continue
        ok=False
        if tile is not None:
            older=tile[t-2*p];later=tile[t-p]
            ok=all(later[y,x]==older[(y-dy)%older.shape[0],(x-dx)%older.shape[1]]
                   for y in range(older.shape[0]) for x in range(older.shape[1]))
        found.append(dict(start=t-2*p,end=t,period=p,dy=dy,dx=dx,certified=ok))
    return found


def main():
    start=time.time();bgs=json.loads(Path(str(STEM)+'_backgrounds.json').read_text())
    cases=json.loads(Path(str(STEM)+'_cases.json').read_text());assert len(cases)==6912
    bycase={(r['background'],r['mode'],r['mask']):r for r in cases}
    saved=json.loads(Path(str(STEM)+'_metrics.json').read_text())
    raw=zlib.decompress(base64.b64decode(saved['data']))
    assert hashlib.sha256(raw).hexdigest()==saved['raw_sha256']
    metrics=np.frombuffer(raw,dtype='<i4').reshape(2,54,64,17,7)
    certs=json.loads(Path(str(STEM)+'_certificates.json').read_text())
    bycert={(r['background'],r['mode'],r['mask']):r for r in certs}
    # Regenerate supplied random words and verify every periodic phase definition.
    for cohort,seed in [('random-a',2026090801),('random-b',2026090802)]:
        rng=np.random.default_rng(seed)
        for b in [r for r in bgs if r['cohort']==cohort]:assert b['bits']==rng.integers(0,2,65,dtype=np.uint8).tolist()
    for b in bgs:
        if 'period' in b:assert b['bits']==[b['word'][i%b['period']] for i in range(-32,33)]
    masks=[np.uint64(sum(1<<m for m in range(64) if (m>>bit)&1)) for bit in range(6)]
    for bi,bg in enumerate(bgs):
        tile=tiles(bg)
        for mi,mode in enumerate(['periodic','isolated']):
            yr=range(3) if mode=='periodic' else range(-65,68)
            grid=np.array([[FULL if encode_value(bg['bits'][x//2+32],y,x) else 0 for x in range(-64,66)] for y in yr],dtype=np.uint64)
            for bit in range(6):
                y,x=divmod(bit,2);grid[y if mode=='periodic' else y+65,x+64]^=masks[bit]
            hashes=[hashlib.sha256() for _ in range(64)];history=[[] for _ in range(64)]
            screens=[None]*64;certificates=[None]*64;returns=[None]*64
            for t in range(33):
                if t%2==0:
                    m=32-t
                    g=grid[:,m:m+66] if mode=='periodic' else grid[m:m+69,m:m+66]
                    values=unpack(g)
                    for mask in range(64):
                        delta=values[mask]^values[0]
                        hashes[mask].update(np.packbits(delta.ravel(),bitorder='little').tobytes())
                        row,norm=assess(delta,values[mask],mode)
                        assert np.array_equal(row,metrics[mi,bi,mask,t//2]),(bg['id'],mode,mask,t)
                        history[mask].append(norm)
                        if t and metrics[mi,bi,mask,0,-1]==2 and row[-1]!=2 and returns[mask] is None:returns[mask]=t
                        for s in scan(history[mask],t,tile):
                            if screens[mask] is None:screens[mask]=s
                            if s['certified'] and certificates[mask] is None:
                                certificates[mask]=s
                                c=bycert[bg['id'],mode,mask];norm0=history[mask][s['start']//2]
                                assert c['shape']==list(norm0[0]) and base64.b64decode(c['response'])==norm0[1] and c['origin']==list(norm0[2])
                                assert c['background_tile']==tile[s['start']].tolist()
                if t<32:grid=advance(grid,mode)
            for mask in range(64):
                r=bycase[bg['id'],mode,mask]
                assert r['response_sha256']==hashes[mask].hexdigest()
                assert r['screen']==screens[mask] and r['certificate']==certificates[mask] and r['first_return']==returns[mask]
        print(bg['id'],'all fields, metrics, recurrence decisions match',flush=True)
    result=dict(cases=6912,sampled_response_fields=117504,all_metrics_and_hashes_match=True,
        all_recurrence_decisions_match=True,certificates=len(certs),seconds=round(time.time()-start,3),
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    Path(str(STEM)+'_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
