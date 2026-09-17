#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, importlib.util, json, math, sys, time
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('crossdim_base', HERE/'run.py')
base=importlib.util.module_from_spec(spec); sys.modules['crossdim_base']=base; spec.loader.exec_module(base)

PROTOCOL='strip-spectrum-20260917-v1'
HEIGHTS=[1,2,3,4,6,8,12,16]
RULES=[r for r in base.LIFE_RULES if r.name in {'life','highlife','day-night','b35s236'}]
WIDTH=521; BURN=512; SCORE=256; EVENT_SEEDS=6; SITES=64
T1=64; T2=128; SPREAD_SEEDS=4; ORIGINS=8


def seed(*parts):
    h=hashlib.sha256('|'.join(map(str,(PROTOCOL,)+parts)).encode()).digest()
    return int.from_bytes(h[:8],'little') & 0x7fff_ffff_ffff_ffff


def batch_successor_symbol_strip(patches: np.ndarray, rule: base.LifeRule) -> np.ndarray:
    # patches [batch,k,5], vertical periodic, horizontal causal window x=0..4.
    n,k,_=patches.shape
    b=np.zeros(9,dtype=np.uint8); s=np.zeros(9,dtype=np.uint8)
    if rule.births: b[list(rule.births)]=1
    if rule.survives: s[list(rule.survives)]=1
    vals=[]; center_idx=None
    for sy in (-1,0,1):
        for sx in (1,2,3):
            cnt=np.zeros(n,dtype=np.uint8)
            cy=sy%k
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    if dx==0 and dy==0: continue
                    cnt += patches[:,(sy+dy)%k,sx+dx]
            c=patches[:,cy,sx]
            out=np.where(c!=0,s[cnt],b[cnt]).astype(np.uint8)
            if sy==0 and sx==2: center_idx=len(vals)
            vals.append(out)
    arr=np.stack(vals,axis=1)
    c=arr[:,center_idx]
    ncount=arr.sum(axis=1)-c
    return (c*9+ncount).astype(np.uint8)


def reference_strip(rule,k,samples=100_000,max_samples=800_000):
    if k<=3:
        total=1<<(5*k)
        counts=np.zeros(18,dtype=np.int64)
        batch=4096
        shifts=np.arange(5*k,dtype=np.uint64)
        for start in range(0,total,batch):
            nums=np.arange(start,min(start+batch,total),dtype=np.uint64)
            bits=((nums[:,None]>>shifts)&1).astype(np.uint8).reshape(len(nums),k,5)
            z=batch_successor_symbol_strip(bits,rule)
            counts += np.bincount(z,minlength=18)
        return counts/counts.sum(), total, 'exact'
    cur=samples
    while True:
        rng=np.random.default_rng(seed('reference',rule.name,k,cur))
        counts=np.zeros(18,dtype=np.int64)
        left=cur
        while left:
            m=min(10000,left)
            patches=rng.integers(0,2,size=(m,k,5),dtype=np.uint8)
            z=batch_successor_symbol_strip(patches,rule)
            counts += np.bincount(z,minlength=18)
            left-=m
        p=counts/counts.sum()
        return p,cur,'monte-carlo'


def sample_events(rule,k,density):
    events=[]; total=k*WIDTH
    for rep in range(EVENT_SEEDS):
        rng=np.random.default_rng(seed('events',rule.name,k,density,rep))
        st=(rng.random((k,WIDTH))<density).astype(np.uint8)
        for _ in range(BURN): st=base.life_step(st,rule)
        flat=np.sort(rng.choice(total,size=min(SITES,total),replace=False))
        ys,xs=flat//WIDTH,flat%WIDTH
        hist=np.zeros(len(flat),dtype=np.uint8)
        for _ in range(7):
            hist=((hist<<1)|st[ys,xs])&0xff
            st=base.life_step(st,rule)
        cc=[]; hh=[]; yy=[]; zz=[]
        for _ in range(SCORE):
            cur=st[ys,xs].copy(); hist=((hist<<1)|cur)&0xff
            sym=base.life_symbols(st,ys,xs); nxt=base.life_step(st,rule)
            cc.append(cur); hh.append(hist.copy()); yy.append(nxt[ys,xs].copy()); zz.append(sym)
            st=nxt
        events.append({'current':np.concatenate(cc),'history':np.concatenate(hh),
                       'target':np.concatenate(yy),'symbol':np.concatenate(zz)})
    return events


def xdiam(diff,ox):
    ys,xs=np.nonzero(diff)
    if len(xs)==0:return 0
    off=((xs-ox+WIDTH//2)%WIDTH)-WIDTH//2
    return int(off.max()-off.min()+1)


def gdiam(diff,oy,ox):
    ys,xs=np.nonzero(diff)
    if len(xs)==0:return 0
    k=diff.shape[0]
    dx=((xs-ox+WIDTH//2)%WIDTH)-WIDTH//2
    dy=((ys-oy+k//2)%k)-k//2
    return int(max(dx.max()-dx.min(),dy.max()-dy.min())+1)


def spread(rule,k,density):
    x1=[];x2=[];g1=[];g2=[]; extinct=0
    total=k*WIDTH
    for rep in range(SPREAD_SEEDS):
        rng=np.random.default_rng(seed('spread',rule.name,k,density,rep))
        st=(rng.random((k,WIDTH))<density).astype(np.uint8)
        for _ in range(BURN): st=base.life_step(st,rule)
        for flat in rng.choice(total,size=ORIGINS,replace=False):
            oy,ox=divmod(int(flat),WIDTH); a=st.copy();b=st.copy();b[oy,ox]^=1
            aa=bb=cc=dd=None
            for t in range(1,T2+1):
                a=base.life_step(a,rule); b=base.life_step(b,rule)
                if t==T1: aa=xdiam(a^b,ox); cc=gdiam(a^b,oy,ox)
                if t==T2: bb=xdiam(a^b,ox); dd=gdiam(a^b,oy,ox)
            x1.append(aa);x2.append(bb);g1.append(cc);g2.append(dd);extinct+=int(bb==0)
    def alpha(a,b):
        ma=float(np.mean(a)); mb=float(np.mean(b))
        if ma==0 and mb==0:return 0.0
        if ma>0 and mb>0:return float(math.log2(mb/ma))
        return None
    return {'Dx64':float(np.mean(x1)),'Dx128':float(np.mean(x2)),'alpha_x':alpha(x1,x2),
            'Dg64':float(np.mean(g1)),'Dg128':float(np.mean(g2)),'alpha_g':alpha(g1,g2),
            'extinction_fraction':extinct/len(x2),'spread_trials':len(x2)}


def matched_divergence(k,density):
    a_rule=next(r for r in RULES if r.name=='life'); b_rule=next(r for r in RULES if r.name=='b35s236')
    vals=[]
    for rep in range(3):
        rng=np.random.default_rng(seed('matched-life-b35',k,density,rep))
        init=(rng.random((k,WIDTH))<density).astype(np.uint8)
        a=init.copy();b=init.copy()
        checkpoints={0,1,2,4,8,16,32,64,128,256}
        rec={}
        for t in range(257):
            if t in checkpoints: rec[str(t)]=float(np.mean(a!=b))
            if t<256: a=base.life_step(a,a_rule); b=base.life_step(b,b_rule)
        vals.append(rec)
    return {t:float(np.mean([r[t] for r in vals])) for t in vals[0]}


def equality_controls():
    rng=np.random.default_rng(seed('height1-equality'))
    row=rng.integers(0,2,size=WIDTH,dtype=np.uint8)
    rules={r.name:r for r in RULES}
    # Life == B35 on k=1; HighLife == ECA54; DayNight == ECA178.
    l=row[None,:].copy();b=row[None,:].copy();h=row[None,:].copy();d=row[None,:].copy();e54=row.copy();e178=row.copy()
    ok={'life_equals_b35':True,'highlife_equals_eca54':True,'daynight_equals_eca178':True}
    for _ in range(256):
        ok['life_equals_b35'] &= bool(np.array_equal(l,b))
        ok['highlife_equals_eca54'] &= bool(np.array_equal(h[0],e54))
        ok['daynight_equals_eca178'] &= bool(np.array_equal(d[0],e178))
        l=base.life_step(l,rules['life']); b=base.life_step(b,rules['b35s236'])
        h=base.life_step(h,rules['highlife']); d=base.life_step(d,rules['day-night'])
        e54=base.eca_step(e54,54); e178=base.eca_step(e178,178)
    return ok


def evaluate(rule,k,density):
    t=time.time(); events=sample_events(rule,k,density)
    p,nref,refmode=reference_strip(rule,k)
    r,mu,sd,missing=base.selective_r(events,p)
    # If MC missed a visited symbol, follow the frozen doubling schedule.
    if missing and k>=4:
        n=200_000
        while missing and n<=800_000:
            p,nref,refmode=reference_strip(rule,k,n,n)
            r,mu,sd,missing=base.selective_r(events,p); n*=2
    m,bll,hll,ntr,nte=base.predictive_gain(events[:4],events[4:6])
    sp=spread(rule,k,density)
    return {'rule':rule.name,'rulestring':rule.rulestring,'height':k,'density':density,
            'R_star':r,'M_star':m,'S_star':max(0,r)*max(0,m) if math.isfinite(r) else None,
            'reference_mode':refmode,'reference_samples':nref,'unsupported_symbols':missing,
            'baseline_logloss_bits':bll,'history_logloss_bits':hll,'train_events':ntr,'test_events':nte,
            **sp,'wall_seconds':time.time()-t}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--phase',choices=['primary','stress','all'],default='primary')
    ap.add_argument('--output-dir',default='results/cross_dimensional_class4_20260917')
    args=ap.parse_args(); out=Path(args.output_dir); out.mkdir(parents=True,exist_ok=True)
    eq=equality_controls()
    if not all(eq.values()): raise SystemExit(f'height-1 equality control failed: {eq}')
    densities=[0.5] if args.phase=='primary' else ([0.3,0.7] if args.phase=='stress' else [0.5,0.3,0.7])
    rows=[]; pairs=[]
    for den in densities:
      for k in HEIGHTS:
        pairs.append({'height':k,'density':den,'life_b35_hamming':matched_divergence(k,den)})
        for rule in RULES:
            r=evaluate(rule,k,den); rows.append(r)
            print(f"{rule.name:10s} k={k:2d} d={den}: S*={r['S_star']:.5g} ax={r['alpha_x']}",flush=True)
    payload={'protocol':PROTOCOL,'phase':args.phase,'equality_controls':eq,'rows':rows,'matched_pairs':pairs}
    path=out/f'strip_spectrum_{args.phase}.json'; path.write_text(json.dumps(payload,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(path)

if __name__=='__main__': main()
