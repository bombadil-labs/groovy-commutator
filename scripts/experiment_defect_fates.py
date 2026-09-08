"""Frozen longer-horizon defect census; exact certificates on periodic backgrounds."""
from pathlib import Path
import base64,csv,hashlib,json,sys,time,zlib
import numpy as np
from experiment_column_compatibility import step2
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from groovy.ca import apply_rule
STEM=ROOT/'results/defect_fates_20260908'
MODES=['periodic','isolated']; TIMES=list(range(0,33,2))
FIELDS=['mass','ymin','ymax','xmin','xmax','local_valid','status']


def backgrounds():
    rows=[]
    for p in range(1,5):
        for word in range(1<<p):
            bits=[(word>>i)&1 for i in range(p)]
            if any(p%d==0 and bits==bits[:d]*(p//d) for d in range(1,p)):continue
            rows.append(dict(id=f'p{p}-{word:02d}',cohort='periodic',period=p,word=bits,
                bits=[bits[i%p] for i in range(-32,33)]))
    assert len(rows)==22
    for cohort,seed in [('random-a',2026090801),('random-b',2026090802)]:
        rng=np.random.default_rng(seed)
        for i in range(16):
            rows.append(dict(id=f'{cohort}-{i:02d}',cohort=cohort,seed=seed,
                bits=rng.integers(0,2,65,dtype=np.uint8).tolist()))
    return rows


def encoding(bits,ys,xs):
    s=np.asarray(bits,dtype=np.uint8)[xs//2+32]
    out=np.zeros((len(ys),len(xs)),dtype=np.uint8)
    for j,y in enumerate(ys):
        out[j]=np.where(xs%2==0,s,1) if y%3==0 else xs%2 if y%3==1 else np.where(xs%2==0,0,1^s)
    return out


def advance(field,mode):
    return step2(field)[...,1:-1] if mode=='periodic' else step2(field,shrink=True)


def tile_history(bg):
    if 'period' not in bg:return None
    p=bg['period'];bits=bg['bits']
    tile=encoding(bits,np.arange(3),np.arange(2*p))
    tiles=[tile]
    for _ in range(32):tiles.append(step2(tiles[-1]))
    return tiles


def metrics(delta,field,mode):
    ys=np.arange(3) if mode=='periodic' else np.arange(-33,36)
    xs=np.arange(-32,34)
    active=np.argwhere(delta)
    mass=len(active)
    if mass:
        lo=active.min(axis=0);hi=active.max(axis=0)
        box=[int(ys[lo[0]]),int(ys[hi[0]]),int(xs[lo[1]]),int(xs[hi[1]])]
        y0,y1=(0,len(ys)-1) if mode=='periodic' else (lo[0],hi[0])
        crop=delta[y0:y1+1,lo[1]:hi[1]+1]
        norm=(crop.shape,np.packbits(crop.ravel(),bitorder='little').tobytes(),
              (0 if mode=='periodic' else box[0],box[2]))
    else:box=[-999]*4;norm=None
    blocks=field.reshape(len(ys)//3,3,33,2).transpose(0,2,1,3)
    numbers=(blocks*(1<<np.arange(6).reshape(3,2))).sum(axis=(-1,-2))
    local=bool(((numbers==42)|(numbers==11)).all())
    status=0 if not mass else 1 if mode=='periodic' and local else 2
    return [mass,*box,int(local),status],norm


def recurrence(history,t,tiles):
    screens=[]
    for p in [2,4,6,8]:
        if t<2*p:continue
        a,b,c=[history[(t-offset)//2] for offset in [2*p,p,0]]
        if a is None or b is None or c is None:continue
        if a[:2]!=b[:2] or b[:2]!=c[:2]:continue
        v=tuple(b[2][i]-a[2][i] for i in [0,1])
        if v!=tuple(c[2][i]-b[2][i] for i in [0,1]) or max(map(abs,v))>p:continue
        certified=tiles is not None and np.array_equal(tiles[t-p],np.roll(tiles[t-2*p],v,axis=(0,1)))
        screens.append(dict(start=t-2*p,end=t,period=p,dy=v[0],dx=v[1],certified=bool(certified)))
    return screens


def write_blob(path,array,axes,extra):
    raw=array.astype('<i4').tobytes()
    payload=dict(shape=list(array.shape),dtype='<i4',order='C',axes=axes,raw_sha256=hashlib.sha256(raw).hexdigest(),
        compression='zlib+base64',data=base64.b64encode(zlib.compress(raw,9)).decode(),**extra)
    path.write_text(json.dumps(payload,indent=2)+'\n')


def main():
    start=time.time();bgs=backgrounds(); records=[]; certificates=[]
    allmetrics=np.empty((2,len(bgs),64,17,7),dtype=np.int32)
    for bi,bg in enumerate(bgs):
        tiles=tile_history(bg)
        for mi,mode in enumerate(MODES):
            ys=np.arange(3) if mode=='periodic' else np.arange(-65,68)
            xs=np.arange(-64,66)
            base=encoding(bg['bits'],ys,xs)
            field=np.broadcast_to(base,(64,*base.shape)).copy()
            for mask in range(64):
                for bit in range(6):
                    if (mask>>bit)&1:
                        y,x=divmod(bit,2)
                        field[mask,np.flatnonzero(ys==y),x+64]^=1
            histories=[[] for _ in range(64)]; hashes=[hashlib.sha256() for _ in range(64)]
            first_screen=[None]*64;first_cert=[None]*64;first_return=[None]*64
            logical=np.array(bg['bits'],dtype=np.uint8);changed=logical.copy();changed[32]^=1
            for t in range(33):
                if t%2==0:
                    margin=32-t
                    cropped=field[:,:,margin:margin+66] if mode=='periodic' else field[:,margin:margin+69,margin:margin+66]
                    outys=np.arange(3) if mode=='periodic' else np.arange(-33,36)
                    expected=encoding(logical,outys,np.arange(-32,34))
                    assert np.array_equal(cropped[0],expected)
                    if mode=='periodic':assert np.array_equal(cropped[33],encoding(changed,outys,np.arange(-32,34)))
                    for mask in range(64):
                        delta=cropped[mask]^cropped[0]
                        hashes[mask].update(np.packbits(delta.ravel(),bitorder='little').tobytes())
                        m,norm=metrics(delta,cropped[mask],mode)
                        allmetrics[mi,bi,mask,t//2]=m;histories[mask].append(norm)
                        if t and allmetrics[mi,bi,mask,0,-1]==2 and m[-1]!=2 and first_return[mask] is None:
                            first_return[mask]=t
                        for s in recurrence(histories[mask],t,tiles):
                            if first_screen[mask] is None:first_screen[mask]=s
                            if s['certified'] and first_cert[mask] is None:
                                first_cert[mask]=s
                                shape,data,origin=histories[mask][s['start']//2]
                                certificates.append(dict(background=bg['id'],mode=mode,mask=mask,**s,
                                    shape=list(shape),origin=list(origin),response=base64.b64encode(data).decode(),
                                    background_tile=tiles[s['start']].tolist()))
                    logical=apply_rule(logical,90);changed=apply_rule(changed,90)
                if t<32:field=advance(field,mode)
            for mask in range(64):
                records.append(dict(background=bg['id'],cohort=bg['cohort'],mode=mode,mask=mask,
                    first_return=first_return[mask],screen=first_screen[mask],certificate=first_cert[mask],
                    response_sha256=hashes[mask].hexdigest()))
        print(f'{bi+1}/{len(bgs)} {bg["id"]}',flush=True)
    Path(str(STEM)+'_backgrounds.json').write_text(json.dumps(bgs,indent=2)+'\n')
    Path(str(STEM)+'_cases.json').write_text(json.dumps(records,separators=(',',':'))+'\n')
    Path(str(STEM)+'_certificates.json').write_text(json.dumps(certificates,separators=(',',':'))+'\n')
    write_blob(Path(str(STEM)+'_metrics.json'),allmetrics,['mode','background','mask','sample_time','metric'],
        dict(modes=MODES,background_ids=[b['id'] for b in bgs],times=TIMES,metrics=FIELDS,empty_box=-999))
    sources=['scripts/experiment_defect_fates.py','scripts/experiment_column_compatibility.py','src/groovy/ca.py',
             'docs/research/protocols/defect-fates-20260908.md']
    metadata=dict(cases=len(records),sampled_fields=len(records)*17,certificates=len(certificates),seconds=round(time.time()-start,3),
        sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources})
    Path(str(STEM)+'_metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    print(json.dumps(metadata,indent=2))


if __name__=='__main__':main()
