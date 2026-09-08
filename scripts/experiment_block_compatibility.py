"""Frozen-budget block/moving-frame search for the fixed ternary 2D law.

See docs/research/protocols/block-compatibility-20260908.md. Complete outcomes
are int16 matrices in documented zlib/base64 JSON; positive records are CSV.
No class labels. Translations describe a fixed observer frame, not repairs.
"""
from pathlib import Path
import base64
import csv
import hashlib
import json
import sys
import time
import zlib
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from groovy.ca import apply_rule
from experiment_column_compatibility import step2,bits,pack,rule_reflect,rule_complement,rule_orbit

STEM=ROOT/'results/block_compatibility_20260908'
CHECKS={}


def count(key,n=1):CHECKS[key]=CHECKS.get(key,0)+int(n)


def frame_v(v,m,k):
    return min((x for x in range(-k,k+1) if (x-v)%m==0),key=lambda x:(abs(x),x))


def vertical_frames(m,k):
    return sorted({frame_v(v,m,k) for v in range(-k,k+1)})


def parameters(m):
    return [(k,u,v) for k in [1,2,3] for u in range(-k,k+1) for v in vertical_frames(m,k)]


def interval(w,k,u):
    return min(-1,(u-k)//w),max(1,(u+w-1+k)//w)


def pairs(area):
    n=2**area
    i=np.arange(n*(n-1))
    a=i//(n-1);b=i%(n-1);b=b+(b>=a)
    return a,b


def pair_index(a,b,area):
    assert a!=b
    return a*(2**area-1)+b-(b>a)


def encode(states,m,w,a,b):
    aa,bb=bits(a,m*w).reshape(m,w),bits(b,m*w).reshape(m,w)
    return np.where(states[...,None,:,None],bb[:,None,:],aa[:,None,:]).reshape(states.shape[:-1]+(m,states.shape[-1]*w))


def signature(r):
    lut=np.array([(r>>q)&1 for q in range(8)],dtype=np.uint8)
    essential=[name for bit,name in [(2,'left'),(1,'center'),(0,'right')]
               if any(lut[q]!=lut[q^(1<<bit)] for q in range(8))]
    anf=lut.copy()
    for bit in range(3):
        for q in range(8):
            if q&(1<<bit):anf[q]^=anf[q^(1<<bit)]
    terms=[q for q in range(8) if anf[q]]
    degree=max((q.bit_count() for q in terms),default=0)
    kind='constant' if not essential else 'single-input' if len(essential)==1 else 'multi-input affine' if degree<=1 else 'multi-input nonlinear'
    return dict(rule=r,essential=essential,arity=len(essential),degree=degree,anf_masks=terms,
                kind=kind,symmetry_orbit=rule_orbit(r),output_ones=int(lut.sum()))


def canonical(v):
    m,w,a,b,k,u,dy=[v[key] for key in ['m','w','a','b','k','u','v']]
    r=v['rule'];aa=bits(a,m*w).reshape(m,w);bb=bits(b,m*w).reshape(m,w)
    for p in range(1,m+1):
        if m%p==0 and np.array_equal(aa,np.tile(aa[:p],(m//p,1))) and np.array_equal(bb,np.tile(bb[:p],(m//p,1))):
            aa,bb,m=aa[:p],bb[:p],p;break
    variants=[]
    for reflect in [False,True]:
        x,y=(1-aa[::-1,::-1],1-bb[::-1,::-1]) if reflect else (aa,bb)
        rr=rule_reflect(r) if reflect else r
        uu=-u if reflect else u;vv=frame_v(-dy if reflect else dy,m,k)
        for shift in range(m):
            a0,b0=pack(np.roll(x,shift,axis=0).flat),pack(np.roll(y,shift,axis=0).flat)
            variants.extend([(m*w,m,w,a0,b0,k,uu,vv,rr),(m*w,m,w,b0,a0,k,uu,vv,rule_complement(rr))])
    return min(variants)


def search_rectangle(m,w):
    area=m*w;n=2**area;a,b=pairs(area);code=bits(np.arange(n),area).reshape(n,m,w)
    params=parameters(m);columns={p:i for i,p in enumerate(params)}
    outcomes=np.full((len(a),len(params)),-3,dtype=np.int16)
    rejected={};success=[]
    for k in [1,2,3]:
        for u in range(-k,k+1):
            low,high=interval(w,k,u);length=high-low+1
            inputs=bits(np.arange(2**length),length)
            q=4*inputs[:,-1-low]+2*inputs[:,-low]+inputs[:,1-low]
            reps=np.array([np.flatnonzero(q==j)[0] for j in range(8)])
            xx=-low*w+u+np.arange(w)
            assert xx.min()-k>=0 and xx.max()+k<length*w
            for start in range(0,len(a),128):
                end=min(start+128,len(a));aa,bb=code[a[start:end]],code[b[start:end]]
                field=np.where(inputs[None,:,None,:,None],bb[:,None,:,None,:],aa[:,None,:,None,:]).reshape(end-start,len(inputs),m,length*w)
                for _ in range(k):field=step2(field)
                for v in vertical_frames(m,k):
                    yy=(np.arange(m)+v)%m
                    out=field[:,:,yy[:,None],xx[None,:]]
                    is_a=(out==aa[:,None,:,:]).all(axis=(-2,-1))
                    is_b=(out==bb[:,None,:,:]).all(axis=(-2,-1))
                    valid=(is_a|is_b).all(axis=-1)
                    lut=is_b[:,reps]
                    local=(is_b==lut[:,q]).all(axis=-1)
                    rules=(lut*np.left_shift(1,np.arange(8))).sum(axis=-1).astype(np.int16)
                    status=np.where(~valid,-1,np.where(~local,-2,rules)).astype(np.int16)
                    outcomes[start:end,columns[(k,u,v)]]=status
                    count('causal_assignment_candidate_checks',len(inputs)*(end-start))
                    for category,tag in [('off-code',-1),('outer-context',-2)]:
                        key=(k,u,v,category)
                        if key not in rejected and np.any(status==tag):
                            j=int(np.flatnonzero(status==tag)[0])
                            bad=np.flatnonzero(~(is_a[j]|is_b[j]) if tag==-1 else is_b[j]!=lut[j,q])
                            z=int(bad[0]);other=int(reps[q[z]]) if tag==-2 else -1
                            rejected[key]=dict(m=m,w=w,k=k,u=u,v=v,category=category,a=int(a[start+j]),b=int(b[start+j]),
                                logical_low=low,logical_high=high,input=z,other_input=other,output_block=pack(out[j,z].flat))
                    for j in np.flatnonzero(status>=0):
                        success.append(dict(m=m,w=w,area=area,a=int(a[start+j]),b=int(b[start+j]),k=k,u=u,v=v,
                                            rule=int(status[j]),physical_flips=int(a[start+j]^b[start+j]).bit_count()))
    assert not np.any(outcomes==-3)
    census=[]
    for index,(k,u,v) in enumerate(params):
        col=outcomes[:,index];good=col[col>=0]
        census.append(dict(m=m,w=w,area=area,k=k,u=u,v=v,candidates=len(a),off_code=int((col==-1).sum()),
                           wider_context=int((col==-2).sum()),accepted=int(len(good)),rules=' '.join(map(str,sorted(set(good.tolist()))))))
    return outcomes,params,success,census,list(rejected.values())


def verify_symmetries(outcomes,success):
    for row in success:
        m,w,a,b,k,u,v,r=[row[key] for key in ['m','w','a','b','k','u','v','rule']]
        matrix,params=outcomes[(m,w)];index={p:i for i,p in enumerate(params)}
        assert matrix[pair_index(b,a,m*w),index[(k,u,v)]]==rule_complement(r)
        aa,bb=bits(a,m*w).reshape(m,w),bits(b,m*w).reshape(m,w)
        for shift in range(m):
            a0,b0=pack(np.roll(aa,shift,axis=0).flat),pack(np.roll(bb,shift,axis=0).flat)
            assert matrix[pair_index(a0,b0,m*w),index[(k,u,v)]]==r
            a1,b1=pack(np.roll(1-aa[::-1,::-1],shift,axis=0).flat),pack(np.roll(1-bb[::-1,::-1],shift,axis=0).flat)
            assert matrix[pair_index(a1,b1,m*w),index[(k,-u,frame_v(-v,m,k))]]==rule_reflect(r)
            count('encoding_symmetries',2)
        count('encoding_symmetries')


def selection_key(v):
    return tuple(v[key] for key in ['area','m','w','a','b','k'])+(abs(v['u'])+abs(v['v']),v['u'],v['v'])


def verify_actions(success):
    selected={}
    for r in sorted({v['rule'] for v in success}):
        all_r=[v for v in success if v['rule']==r]
        for group in [all_r,[v for v in all_r if v['u']==v['v']==0],[v for v in all_r if v['w']>1]]:
            if group:
                v=min(group,key=selection_key);selected[selection_key(v)+(r,)]=v
    selected=list(selected.values())
    for v in selected:
        m,w,a,b,k,u,dy,r=[v[key] for key in ['m','w','a','b','k','u','v','rule']]
        for n in [5,7]:
            states=bits(np.arange(2**n),n);logical=states.copy();field=encode(states,m,w,a,b)
            for t in range(1,5):
                logical=np.stack([apply_rule(s,r) for s in logical])
                for _ in range(k):field=step2(field)
                expected=np.roll(encode(logical,m,w,a,b),(t*dy,t*u),axis=(-2,-1))
                assert np.array_equal(field,expected),(v,n,t)
                count('laboratory_trajectory_states',len(states))
            if n==5:
                mask=bits(a^b,m*w).reshape(m,w)
                for word in range(8):
                    logical=states.copy();field=encode(states,m,w,a,b)
                    for t in range(3):
                        if (word>>t)&1:
                            logical[:,0]^=1
                            yy=(np.arange(m)+t*dy)%m;xx=(np.arange(w)+t*u)%(n*w)
                            field[:,yy[:,None],xx[None,:]]^=mask
                        logical=np.stack([apply_rule(s,r) for s in logical])
                        for _ in range(k):field=step2(field)
                        expected=np.roll(encode(logical,m,w,a,b),((t+1)*dy,(t+1)*u),axis=(-2,-1))
                        assert np.array_equal(field,expected),(v,n,word,t)
                        count('laboratory_action_word_states',len(states))
    return selected


def write_json(suffix,obj):Path(str(STEM)+suffix+'.json').write_text(json.dumps(obj,indent=2)+'\n')


def write_csv(suffix,rows):
    with Path(str(STEM)+suffix+'.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)


def main():
    started=time.time();outcomes={};success=[];census=[];rejected=[];encoded=[]
    for m in range(1,7):
        for w in range(1,6//m+1):
            matrix,params,good,aggregate,bad=search_rectangle(m,w)
            outcomes[(m,w)]=(matrix,params);success.extend(good);census.extend(aggregate);rejected.extend(bad)
            raw=matrix.astype('<i2').tobytes()
            encoded.append(dict(m=m,w=w,shape=list(matrix.shape),parameters=params,
                data=base64.b64encode(zlib.compress(raw,9)).decode(),raw_sha256=hashlib.sha256(raw).hexdigest()))
            print(f'{m}x{w}: {matrix.size} candidates, {len(good)} successes, rules {sorted({v["rule"] for v in good})}',flush=True)
    old=list(csv.DictReader((ROOT/'results/column_compatibility_20260908.csv').open()))
    for row in old:
        m,a,b,k=[int(row[key]) for key in ['m','a','b','k']]
        matrix,params=outcomes[(m,1)]
        expected=int(row['rule']) if int(row['rule'])>=0 else -1 if int(row['off_code']) else -2
        assert int(matrix[pair_index(a,b,m),params.index((k,0,0))])==expected
        count('previous_zero_frame_column_conditions')
    verify_symmetries(outcomes,success)
    selected=verify_actions(success)
    signatures=[signature(r) for r in sorted({v['rule'] for v in success})]
    canonical_count=len({canonical(v) for v in success})
    by_rule=[]
    for sig in signatures:
        group=[v for v in success if v['rule']==sig['rule']]
        by_rule.append(dict(**sig,encodings=len(group),stationary=sum(v['u']==v['v']==0 for v in group),
                            blocked=sum(v['w']>1 for v in group),minimal=min(group,key=selection_key)))
    summary=dict(candidates=sum(matrix.size for matrix,params in outcomes.values()),
        rectangles=len(outcomes),successes=len(success),canonical_encodings=canonical_count,
        admitted_rules=[s['rule'] for s in signatures],rules=by_rule,
        no_frame_rules=sorted({v['rule'] for v in success if v['u']==v['v']==0}),
        column_frame_rules=sorted({v['rule'] for v in success if v['w']==1}),
        block_frame_rules=sorted({v['rule'] for v in success if v['w']>1}),
        selected_action_checks=selected)
    write_json('_outcomes',dict(schema_version=1,dtype='<i2',order='C',codec='base64 of zlib compressed raw bytes',
        status={'off_code':-1,'outer_context':-2,'elementary_rule':'0..255'},
        pair_order='A=0..2^(m*w)-1; for each A, B ascending with B!=A; index A*(2^(m*w)-1)+B-(B>A)',
        rectangles=encoded))
    write_csv('_successes',success);write_csv('_census',census);write_json('_rejections',rejected)
    write_json('_summary',summary)
    sources=['scripts/experiment_block_compatibility.py','scripts/experiment_column_compatibility.py',
             'src/groovy/ca.py','docs/research/protocols/block-compatibility-20260908.md']
    write_json('_metadata',dict(checks=CHECKS,seconds=round(time.time()-started,3),numpy=np.__version__,
        sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources},
        scope='Every ordered binary block pair with area<=6, k1..3, |u|/|v|<=k with vertical periods identified. No class labels.'))
    print(json.dumps({key:summary[key] for key in ['candidates','rectangles','successes','canonical_encodings','admitted_rules','no_frame_rules','column_frame_rules','block_frame_rules']},indent=2),flush=True)


if __name__=='__main__':main()
