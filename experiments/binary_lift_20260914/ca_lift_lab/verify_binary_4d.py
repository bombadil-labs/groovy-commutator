"""Targeted exhaustive independent 4D verification.
Interval-cropped fields, chunked explicit bit patches, adjacent-key consistency,
and set-based low-pivot GF2 elimination. Reuses the already audited lower-law
symbolic constraints; directly checks the concrete 4D physical G on successes.
"""
import argparse,concurrent.futures,itertools,json,time
from pathlib import Path
import numpy as np
from verify_recursive_binary import combine,negate,stack,mask,source_step,value
from audit_binary_4d import prepare_lower,selected
ROOT=Path(__file__).resolve().parent

def shifted(f,dx,dy=0):return f[0]-dx,np.roll(f[1],-dy,axis=1)if dy else f[1]
def encode_field(a,b,rec,parent=False):
    sign=rec['recipe'][0]['shift'];left,right=map(int,rec['reference'].split(':')[1:]);delta=combine(a,b)
    p=combine(a,shifted(a,sign,1 if parent else 0))
    q=combine(shifted(a,left,left*sign if parent else 0),shifted(a,right,right*sign if parent else 0),np.bitwise_and)
    return stack([p,delta,mask(a,delta,rec['recipe'][0]['mask']),q],rec['order'])

def keys(f,i,new_phases=None):
    start,a=f;d=a.ndim-2;mid=i-start;outputs=[]
    for begin in range(0,len(a),1024):
        block=a[begin:begin+1024,...,mid-2:mid+3];parts=[]
        for offsets in itertools.product((0,1,2,-1),repeat=d):
            p=np.roll(block,tuple(-x for x in offsets),axis=tuple(range(1,d+1)))
            if new_phases is not None:p=p[:,new_phases]
            parts.append(p)
        bits=np.concatenate(parts,axis=-1);b=np.packbits(bits,axis=-1,bitorder='big');size=b.shape[-1]
        outputs.append(np.ascontiguousarray(b.reshape(-1,size)).view(f'V{size}').ravel())
    return np.concatenate(outputs)

def low_solve(equations,terms):
    basis={}
    for eid in set(equations):
        row=set(terms[eid])
        while row-{0}:
            p=min(row-{0})
            if p in basis:row.symmetric_difference_update(basis[p])
            else:basis[p]=row;break
        if row=={0}:return False,len(basis)
    return True,len(basis)

def xor_vector(alg,a,b):
    pairs=np.empty(a.size,dtype=[('a','u4'),('b','u4')]);pairs['a']=a.ravel();pairs['b']=np.broadcast_to(b,a.shape).ravel()
    uni,iv=np.unique(pairs,return_inverse=True);vals=np.array([alg.xor(int(t['a']),int(t['b']))for t in uni],dtype=np.uint32)
    return vals[iv].reshape(a.shape)

def run_one(args):
    record,expected=args;start=time.perf_counter();rec=record['first_floor'];rule=rec['rule'];mid=expected['origin'];w=expected['source_width'];order=rec['order'];phases=[order.index(0),order.index(1)];sign=rec['recipe'][0]['shift'];mode=record['recursive_G']['mode']
    src=[(0,((np.arange(1<<w)[:,None]>>np.arange(w-1,-1,-1))&1).astype(np.uint8))]
    for _ in range(5):src.append(source_step(src[-1],rule))
    f2=[encode_field(src[t],src[t+1],rec)for t in range(5)]
    f3=[encode_field(f2[t],f2[t+1],rec,True)for t in range(4)]
    f4=[encode_field(f3[t],f3[t+1],rec,True)for t in range(3)];delta=combine(f4[0],f4[1]);n=len(src[0][1])
    bk=keys(f4[0],mid);orderkeys=np.argsort(bk,kind='stable');sortedkeys=bk[orderkeys];same=sortedkeys[1:]==sortedkeys[:-1]
    bv=value(delta,mid).ravel();shape=f4[0][1].shape[:-1]
    targets={'native':bv,'source':np.broadcast_to(value(src[0],mid)[:,None,None,None],shape).ravel(),'parent':np.broadcast_to(value(f3[0],mid)[:,None],shape).ravel()}
    for name,vals in targets.items():
        v=vals[orderkeys];good=not np.any(same&(v[1:]!=v[:-1]));assert good==expected['gates'][name]['passes'],(rule,name)
    take=np.r_[True,~same];bu=sortedkeys[take].copy();baseval=bv[orderkeys][take].copy();del sortedkeys,same,orderkeys,bk
    if not expected['first_order_pass']:return {'rule':rule,'passed':True,'gate_decisions':3,'G_tested':False,'seconds':time.perf_counter()-start}
    alg,h2,h3,z2,z3,uq,expr,lower=prepare_lower(record);d3=combine(f3[0],f3[1])
    def g3_at(position):
        ks=keys(d3,position);loc=np.searchsorted(uq,ks);assert np.all(loc<len(uq))and np.all(uq[loc]==ks)
        e=expr[loc].reshape(f3[0][1].shape[:-1]);e=xor_vector(alg,e,(value(f3[0],position)^value(f3[2],position)).astype(np.uint32));return xor_vector(alg,e,np.uint32(z3))
    g3=g3_at(mid);g3s=np.roll(g3_at(mid+sign),-1,axis=1);carrier=np.stack([xor_vector(alg,g3,g3s),g3],axis=1)
    desired=xor_vector(alg,carrier,(value(f4[0],mid)[:,phases]^value(f4[2],mid)[:,phases]).astype(np.uint32)).ravel()
    pk=keys(delta,mid,phases);sort=np.argsort(pk,kind='stable');sk=pk[sort];sv=desired[sort];same=sk[1:]==sk[:-1]
    equations=list(alg.equations)
    differences=same&(sv[1:]!=sv[:-1])
    pairs=set(zip(sv[:-1][differences].tolist(),sv[1:][differences].tolist()))
    for a,b in pairs:equations.append(alg.xor(a,b))
    first=np.r_[True,~same];pu=sk[first].copy();pe=sv[first].copy();del sk,sv,sort,same
    loc=np.searchsorted(bu,pu);hit=loc<len(bu);hit[hit]&=bu[loc[hit]]==pu[hit]
    zero=np.zeros(1,dtype='V40')[0];zi=np.searchsorted(bu,zero);z4=0
    if mode=='centered':z4=int(baseval[zi])if zi<len(bu)and bu[zi]==zero else alg.var()
    for e,v in set(zip(pe[hit].tolist(),baseval[loc[hit]].tolist())):equations.append(alg.xor(e,z4,v))
    zi=np.searchsorted(pu,zero)
    if mode=='centered'and zi<len(pu)and pu[zi]==zero:equations.append(int(pe[zi]))
    good,rank=low_solve(equations,alg.terms);assert good==expected['recursive_G']['passes'],rule
    result={'rule':rule,'passed':True,'gate_decisions':3,'G_tested':True,'G_pass':good,'independent_rank':rank,'source_words':n,'direct_G_cells':0}
    if good:
        nonzero=set(expected['recursive_G']['nonzero_variables'])
        evaluate=lambda eid:sum(t==0 or t in nonzero for t in alg.terms[int(eid)])%2
        assert all(evaluate(e)==0 for e in equations)
        pv=np.array([evaluate(alg.xor(int(e),z4))for e in pe],dtype=np.uint8)
        future=keys(f4[1],mid);loc=np.searchsorted(bu,future);assert np.all(loc<len(bu))and np.all(bu[loc]==future)
        flip=baseval[loc].reshape(shape);assert np.array_equal(flip,value(f4[1],mid)^value(f4[2],mid));del future
        loc=np.searchsorted(pu,pk);actualprobe=pv[loc].reshape(n,2,4,4)
        actual=flip[:,phases]^value(delta,mid)[:,phases]^actualprobe
        if mode=='centered':actual^=evaluate(z4)
        uni,iv=np.unique(carrier,return_inverse=True);ev=np.array([evaluate(e)for e in uni],dtype=np.uint8);want=ev[iv].reshape(carrier.shape)
        assert np.array_equal(actual,want);result['direct_G_cells']=actual.size
    result['seconds']=time.perf_counter()-start;return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run',type=Path,required=True);ap.add_argument('--rules',type=int,nargs='+',required=True);ap.add_argument('--workers',type=int,default=3);ap.add_argument('--name',default='verification');args=ap.parse_args();start=time.perf_counter()
    found={r['rule']:r for r in map(json.loads,(args.run/'candidates.jsonl').read_text().splitlines())};picks={r['rule']:r for r in selected()}
    tasks=[(picks[r],found[r])for r in args.rules];results=[]
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers)as pool:
        for result in pool.map(run_one,tasks):results.append(result);print(json.dumps(result),flush=True)
    out={'status':'passed','rules':args.rules,'scope':'targeted independent exhaustive 4D checks; lower symbolic tables reused from audited lower construction','results':results,'seconds':time.perf_counter()-start}
    (args.run/(args.name+'.json')).write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
