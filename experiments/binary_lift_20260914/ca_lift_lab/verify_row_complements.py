"""Independent cropped-source audit of row-complement certificates and physical G.
Uses integrated ECA tables on shrinking windows, not the primary periodic code.
Verifies every negative certificate and exhaustive positive representatives.
"""
import hashlib,itertools,json,time
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent;RUN=ROOT/'runs/row_complements_8'
ZERO=1<<18;N=2048
S=((np.arange(N)[:,None]>>np.arange(11))&1).astype(np.uint8)
QN={0:(-2,1,False,False),1:(-1,2,False,False),2:(-2,1,False,True),3:(-1,2,True,False)}
def arrays(rule,mask,sign,q):
    jets=[S]
    for t in range(4):
        x=jets[-1];ix=4*x[:,:-2]+2*x[:,1:-1]+x[:,2:]
        jets.append(((rule>>ix)&1).astype(np.uint8))
    def x(t,pos):return jets[t][:,np.asarray(pos)+5-t]
    def d(t,pos):return x(t,pos)^x(t+1,pos)
    def f(t,pos):
        pos=np.asarray(pos);a=x(t,pos);delta=d(t,pos)
        m={'birth':(1-a)&delta,'death':a&delta,'stay_one':a&(1-delta),'stay_zero':(1-a)&(1-delta)}[mask]
        out=[a^x(t,pos+sign),delta,a^x(t+2,pos),m]
        if q>=0:
            l,r,nl,nr=QN[q];out.append((x(t,pos+l)^nl)&(x(t,pos+r)^nr))
        return np.stack(out,axis=1)
    a=f(0,np.arange(-2,3));b=f(1,np.arange(-2,3));c=f(2,[0])[...,0]
    pos=np.array([0,sign]);idx=4*d(0,pos-1)+2*d(0,pos)+d(0,pos+1)
    g=d(1,pos)^((rule>>idx)&1)
    carrier=np.stack([g[:,0]^g[:,1],g[:,0]],axis=1).astype(np.uint8)
    wanted=a[:,:2,2]^c[:,:2]^carrier
    def chunks(grid):return grid.astype(np.uint32)@np.array([16,8,4,2,1],dtype=np.uint32)
    return {'a':a,'b':b,'c':c,'carrier':carrier,'want':wanted,'ac':chunks(a),'bc':chunks(b),'uc':chunks(a^b),'flip':a[...,2]^b[...,2]}
def keys(chunks,order):
    n=len(order);k=np.zeros((N,n),dtype=np.uint32)
    for dy in range(-2,3):k=(k<<5)|chunks[:,[order[(p+dy)%n]for p in range(n)]]
    return k
def one_key(chunks,sample,order,phase):
    k=0
    for dy in range(-2,3):k=(k<<5)|int(chunks[sample,order[(phase+dy)%len(order)]])
    return k
def table(ks,vs):
    ks=ks.ravel();vs=vs.ravel();unique,first,inv=np.unique(ks,return_index=True,return_inverse=True)
    value=vs[first];return np.array_equal(value[inv],vs),(unique,value)
def lookup(tx,ks):
    u,v=tx;pos=np.searchsorted(u,ks);assert np.all(pos<len(u))and np.array_equal(u[pos],ks)
    return v[pos]
def tag(r):return(r['rule'],r['mask'],r['shift'],r['reference'],tuple(r['order']),r['polarity'])
def mirror(r):return sum(((r>>i)&1)<<(((i&1)<<2)|(i&2)|((i&4)>>2))for i in range(8))
def main():
    start=time.monotonic();rows=[]
    for p in sorted(RUN.glob('part-*.jsonl')):rows.extend(json.loads(s)for s in p.read_text().splitlines())
    summary=json.loads((RUN/'summary.json').read_text());assert summary['complete']and len(rows)==202752
    indexed={tag(r):r for r in rows};assert len(indexed)==len(rows)
    for r in rows:
        m=mirror(r['rule']);q=r['reference'];mq=-1 if q<0 else q^1
        other=indexed[(m,r['mask'],-r['shift'],mq,tuple(r['order']),r['polarity'])]
        assert r['gates']==other['gates'],('reflection',tag(r))
    selected={};gates=('native','source','raw','centered0','centered1')
    for r in sorted(rows,key=tag):
        if not(r['gates']['native']and r['gates']['source']):continue
        for g in gates[2:]:
            if r['gates'][g]:selected.setdefault(('positive',r['rule'],r['reference']<0,g),tag(r))
        selected.setdefault(('geometry',r['reference'],r['shift'],tuple(r['order']),r['polarity']),tag(r))
        selected.setdefault(('mask',r['mask'],r['shift'],r['reference']),tag(r))
        selected.setdefault(('polarity',r['reference'],r['shift'],r['polarity']),tag(r))
    chosen=set(selected.values());counts={'recipes':len(rows),'reflection_pairs_checked':len(rows),'certificate_pairs':0,'full_records':0,'full_gate_decisions':0,'direct_G_cells':0,'direct_native_next_cells':0};last=None;data=None
    for r in sorted(rows,key=tag):
        prefix=tag(r)[:4]
        if prefix!=last:data=arrays(*prefix);last=prefix;polarized={}
        polarity=r['polarity']
        if polarity not in polarized:
            offsets=np.array([31*((polarity>>f)&1)for f in range(len(r['order']))],dtype=np.uint32)
            polarized[polarity]=(data['ac']^offsets,data['bc']^offsets)
        ac,bc=polarized[polarity]
        order=r['order'];g=r['gates'];n=len(order)
        for name,cert in r['witnesses'].items():
            key,p0,p1=cert;assert not g[name]
            values=[]
            for p in (p0,p1):
                if p&ZERO:
                    assert key==0 and name.startswith('centered');values.append(int(name[-1]));continue
                sample=(p>>7)&2047;phase=(p>>4)&7;probe=(p>>3)&1;field=order[phase]
                actual_key=one_key(data['uc']if probe else ac,sample,order,phase);assert actual_key==key,(tag(r),name,'key')
                if probe:
                    assert field in (0,1)and name not in ('native','source')
                    value=int(data['want'][sample,field]);raw=value
                    cb=value^((r['rule']&1)if field==1 else 0)
                    if name.startswith('centered'):value=cb^int(name[-1])
                else:
                    raw=int(data['flip'][sample,field]);cb=raw
                    value=int(S[sample,5])if name=='source'else raw
                    assert ((p>>1)&1)==int(S[sample,5])
                assert(p&1)==raw and((p>>2)&1)==cb
                values.append(value)
            assert values==[0,1],(tag(r),name,values);counts['certificate_pairs']+=1
        if tag(r)not in chosen:continue
        bk=keys(ac,order);kb=keys(bc,order);phases=[order.index(0),order.index(1)];pk=keys(data['uc'],order)[:,phases];bv=data['flip'][:,order]
        assert table(bk,bv)[0]==g['native']
        assert table(bk,np.broadcast_to(S[:,5,None],(N,n)))[0]==g['source']
        for name in gates[2:]:
            z=None if name=='raw'else int(name[-1]);wanted=data['want'].copy()
            if z is not None:wanted[:,1]^=r['rule']&1;wanted^=z
            ks=np.concatenate([bk.ravel(),pk.ravel(),[]if z is None else[0]]).astype(np.uint32)
            vs=np.concatenate([bv.ravel(),wanted.ravel(),[]if z is None else[z]]).astype(np.uint8)
            ok,tx=table(ks,vs);assert ok==g[name],(tag(r),name)
            if ok:
                actual_next=lookup(tx,kb);expected_next=(data['b'][...,2]^data['c'])[:,order]
                assert np.array_equal(actual_next,expected_next),(tag(r),name,'native second step')
                actual_G=actual_next[:,phases]^bv[:,phases]^lookup(tx,pk);expected_G=data['carrier'].copy()
                if z is not None:actual_G^=z;expected_G[:,1]^=r['rule']&1
                assert np.array_equal(actual_G,expected_G),(tag(r),name,'physical G')
                counts['direct_G_cells']+=actual_G.size;counts['direct_native_next_cells']+=actual_next.size
        counts['full_records']+=1;counts['full_gate_decisions']+=5
    counts.update(status='passed',seconds=time.monotonic()-start,verifier_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),scope='Every negative certificate; full cropped-source decisions across each passing rule/family/mode, every faithful geometry, each faithful polarity/ref/sign and mask/ref/sign; direct physical G at every passing checked branch')
    (RUN/'verification.json').write_text(json.dumps(counts,indent=2)+'\n');print(json.dumps(counts),flush=True)
if __name__=='__main__':main()
