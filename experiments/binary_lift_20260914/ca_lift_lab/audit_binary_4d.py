"""Exact 4D continuation of the 113 certified binary recursive-G paths.
All lower probe outputs, including centered zero offsets, remain symbolic.
Interned sparse XOR expressions avoid dense truth tables and bit-vector blowup.
"""
import argparse,concurrent.futures,hashlib,itertools,json,time
from pathlib import Path
import numpy as np
from verify_polarization_proposal import d,encode
from audit_reference_covariance import reference
from audit_recursive_binary import build as build3,pkeys
ROOT=Path(__file__).resolve().parent

class Algebra:
    def __init__(self):self.terms=[(),(0,)];self.ids={():0,(0,):1};self.nextvar=1;self.equations=[]
    def intern(self,t):
        t=tuple(sorted(t))
        if t not in self.ids:self.ids[t]=len(self.terms);self.terms.append(t)
        return self.ids[t]
    def var(self):
        n=self.nextvar;self.nextvar+=1;return self.intern((n,))
    def xor(self,*ids):
        terms=set()
        for i in ids:terms.symmetric_difference_update(self.terms[int(i)])
        return self.intern(terms)
    def eq(self,a,b=0):
        v=self.xor(a,b)
        if v:self.equations.append(v)
    def flip(self,arr,bits):
        unique,inv=np.unique(arr,return_inverse=True);op=np.array([self.xor(int(i),1) for i in unique],dtype=np.uint32)
        toggled=op[inv].reshape(arr.shape)
        return np.where(bits,toggled,arr).astype(np.uint32)
    def pair(self,a,b):
        pair=(a.astype(np.uint64)<<32)|b.astype(np.uint64);unique,inv=np.unique(pair,return_inverse=True)
        vals=np.array([self.xor(int(v>>np.uint64(32)),int(v&np.uint64(0xffffffff)))for v in unique],dtype=np.uint32)
        return vals[inv].reshape(a.shape)
    def solve(self):
        basis={};eqs=set(self.equations)
        for eid in eqs:
            x=sum(1<<n for n in self.terms[eid])
            while x>1:
                p=x.bit_length()-1
                if p in basis:x^=basis[p]
                else:basis[p]=x;break
            if x==1:return {'passes':False,'rank':len(basis),'equations':len(eqs),'conflicting_expression':list(self.terms[eid])}
        bits=0
        for p,row in sorted(basis.items()):
            if (row&bits).bit_count()%2 ^ (row&1):bits|=1<<p
        assert all(((sum(1<<n for n in self.terms[e])&bits).bit_count()%2)==(0 in self.terms[e]) for e in eqs)
        return {'passes':True,'rank':len(basis),'equations':len(eqs),'nonzero_variables':[n for n in range(1,self.nextvar) if (bits>>n)&1]}

class Law:
    def __init__(self,algebra):self.a=algebra;self.table={}
    def assign(self,k,e):
        if k in self.table:self.a.eq(self.table[k],e)
        else:self.table[k]=e
    def get(self,k):
        if k not in self.table:self.table[k]=self.a.var()
        return self.table[k]

def keys(grid,mid,new_phases=None):
    """Relative +2/-2 are identical on period4 axes: exact compressed key."""
    axes=grid.ndim-2;pattern=np.zeros(grid.shape[:-1],dtype=np.uint8)
    for dx in range(-2,3):pattern=(pattern<<1)|grid[...,mid+dx]
    shape=list(pattern.shape)
    if new_phases is not None:shape[1]=len(new_phases)
    nbits=5*(4**axes);nbytes=(nbits+7)//8
    packed=np.zeros((*shape,nbytes),dtype=np.uint8)
    for j,offsets in enumerate(itertools.product((0,1,2,-1),repeat=axes)):
        v=np.roll(pattern,tuple(-o for o in offsets),axis=tuple(range(1,axes+1)))
        if new_phases is not None:v=v[:,new_phases]
        byte,off=divmod(j*5,8)
        if off<=3:packed[...,byte]|=v<<(3-off)
        else:
            packed[...,byte]|=v>>(off-3);packed[...,byte+1]|=v<<(11-off)
    packed=packed.reshape(-1,nbytes)
    return np.ascontiguousarray(packed).view(f'V{nbytes}').ravel()

def shift_newest(x,dx,dy):return np.roll(x,(-dy,-dx),axis=(1,x.ndim-1))
def lift(a,b,rec):
    sign=rec['recipe'][0]['shift'];left,right=map(int,rec['reference'].split(':')[1:]);delta=a^b
    p=a^shift_newest(a,sign,1);name=rec['recipe'][0]['mask']
    if name=='birth':m=(1-a)&delta
    elif name=='death':m=a&delta
    elif name=='stay_one':m=a&(1-delta)
    else:m=(1-a)&(1-delta)
    q=shift_newest(a,left,left*sign)&shift_newest(a,right,right*sign)
    return np.stack([p,delta,m,q],axis=1)[:,rec['order']]

def prepare_lower(record):
    rec=record['first_floor'];rule=rec['rule'];order=rec['order'];phases=[order.index(0),order.index(1)];sign=rec['recipe'][0]['shift'];mode=record['recursive_G']['mode']
    s,states,pa,kids,mid=build3(rec);alg=Algebra();h2=Law(alg);h3=Law(alg)
    a,b,c=pa[:3];delta=a^b;bk=pkeys(a,mid);pk=pkeys(delta,mid)
    for k,v in zip(bk.ravel().tolist(),delta[...,mid].ravel().tolist()):h2.assign(k,v)
    z2=h2.get(0) if mode=='centered' else 0
    ds=d(s,rule);g=d(states[1],rule)^ds^d(ds,rule)
    pg=np.stack([g[:,mid]^g[:,mid+sign],g[:,mid]],axis=1)
    wanted=a[:,phases,mid]^c[:,phases,mid]^pg
    if mode=='centered':wanted[:,1]^=rule&1
    for k,v in zip(pk[:,phases].ravel().tolist(),wanted.ravel().tolist()):h2.assign(k,alg.xor(v,z2))
    # All parent first-order outputs are fixed; P/D probe outputs can depend on h2.
    kb3=keys(kids[0],mid);delta3=kids[0]^kids[1]
    for k,v in zip(kb3,delta3[...,mid].ravel()):h3.assign(bytes(k),int(v))
    zero3=bytes(10);z3=h3.get(zero3) if mode=='centered' else 0
    def e2(ks,const):
        return np.array([alg.xor(h2.get(k),int(v),z2) for k,v in zip(ks.ravel().tolist(),const.ravel().tolist())],dtype=np.uint32).reshape(ks.shape)
    g2=e2(pk,a[...,mid]^c[...,mid]);g2shift=e2(pkeys(delta,mid+sign),a[...,mid+sign]^c[...,mid+sign]);g2shift=np.roll(g2shift,-1,axis=1)
    target=np.stack([alg.pair(g2,g2shift),g2],axis=1)
    target=alg.flip(target,(kids[0][...,mid][:,phases]^kids[2][...,mid][:,phases]))
    ku3=keys(delta3,mid,new_phases=phases)
    for k,e in zip(ku3,target.ravel()):h3.assign(bytes(k),alg.xor(int(e),z3))
    # Every possible 3D temporal-probe neighborhood is covered at source width13.
    uq=np.unique(keys(delta3,mid));expr=np.array([h3.get(bytes(k)) for k in uq],dtype=np.uint32)
    lower=alg.solve();assert lower['passes'],rule
    return alg,h2,h3,z2,z3,uq,expr,lower

def selected():
    chosen={}
    for name in ['recursive_binary_3d_v2','recursive_binary_reflections']:
        for row in map(json.loads,(ROOT/'runs'/name/'candidates.jsonl').read_text().splitlines()):
            if row['recursive_G']['passes']:chosen[row['rule']]=row
    return sorted(chosen.values(),key=lambda r:(r['rule']!=110,r['rule']))

def groups(bk,targets):
    unique,first,inv=np.unique(bk,return_index=True,return_inverse=True)
    results={};vals={}
    for name,target in targets.items():
        masks=np.zeros(len(unique),dtype=np.uint8);np.bitwise_or.at(masks,inv,(1<<target.ravel()).astype(np.uint8));bad=np.flatnonzero(masks==3)
        results[name]={'passes':not len(bad),'conflicts':len(bad)};vals[name]=masks
        if len(bad):
            j=int(bad[0]);events=[int(np.flatnonzero((inv==j)&(target.ravel()==bit))[0])for bit in (0,1)]
            results[name]['witness']={'key_hex':bytes(unique[j]).hex(),'events':events}
    return unique,vals,results

def run_one(record):
    start=time.perf_counter();rec=record['first_floor'];rule=rec['rule'];mode=record['recursive_G']['mode'];order=rec['order'];phases=[order.index(0),order.index(1)];sign=rec['recipe'][0]['shift']
    left,right=map(int,rec['reference'].split(':')[1:]);lo=min(-1,left);hi=max(1,right);width=3*(hi-lo)+7;mid=3-3*lo
    s=((np.arange(1<<width)[:,None]>>np.arange(width-1,-1,-1))&1).astype(np.uint8);states=[s]
    for _ in range(4):states.append(states[-1]^d(states[-1],rule))
    floor2=[]
    for st in states:
        a=encode(st,rule,rec['recipe'][0]);q=reference(st,rule,rec['recipe'][0],rec['reference']);floor2.append(np.concatenate([a,q[:,None,:]],axis=1)[:,order])
    floor3=[lift(floor2[t],floor2[t+1],rec)for t in range(4)];floor4=[lift(floor3[t],floor3[t+1],rec)for t in range(3)]
    bk=keys(floor4[0],mid)
    shp=floor4[0].shape[:-1]
    targets={'native':(floor4[0]^floor4[1])[...,mid],'source':np.broadcast_to(s[:,mid,None,None,None],shp),'parent':np.broadcast_to(floor3[0][:,None,...,mid],shp)}
    unique,values,gates=groups(bk,targets);del bk
    out={'rule':rule,'mode':mode,'first_floor':rec,'prior_path':{'mirrored_from_rule':record.get('mirrored_from_rule')},'source_width':width,'origin':mid,'gates':gates,'first_order_pass':all(v['passes']for v in gates.values())}
    if not out['first_order_pass']:
        out['recursive_G']={'passes':False,'not_tested_due_to_first_order_failure':True};out['seconds']=time.perf_counter()-start;return out
    alg,h2,h3,z2,z3,uq,expr,lower=prepare_lower(record)
    delta3=floor3[0]^floor3[1]
    def g3_at(position):
        ks=keys(delta3,position);loc=np.searchsorted(uq,ks);assert np.all(loc<len(uq));assert np.all(uq[loc]==ks)
        e=expr[loc].reshape(floor3[0].shape[:-1]);e=alg.flip(e,floor3[0][...,position]^floor3[2][...,position])
        if z3:
            uni,iv=np.unique(e,return_inverse=True);vv=np.array([alg.xor(int(x),z3)for x in uni],dtype=np.uint32);e=vv[iv].reshape(e.shape)
        return e
    g3=g3_at(mid);g3shift=np.roll(g3_at(mid+sign),-1,axis=1)
    wanted=np.stack([alg.pair(g3,g3shift),g3],axis=1)
    wanted=alg.flip(wanted,(floor4[0][...,mid][:,phases]^floor4[2][...,mid][:,phases]))
    probe=keys(floor4[0]^floor4[1],mid,new_phases=phases)
    up,first,inv=np.unique(probe,return_index=True,return_inverse=True);del probe
    desired=wanted.ravel();represent=desired[first]
    paircode=(desired.astype(np.uint64)<<32)|represent[inv].astype(np.uint64)
    for code in np.unique(paircode):alg.eq(int(code>>np.uint64(32)),int(code&np.uint64(0xffffffff)))
    pos=np.searchsorted(unique,up);hit=pos<len(unique);hit[hit]&=unique[pos[hit]]==up[hit]
    zero=np.zeros(1,dtype='V40')[0];zeroindex=np.searchsorted(unique,zero)
    z4=0
    if mode=='centered':z4=int(values['native'][zeroindex]==2) if zeroindex<len(unique) and unique[zeroindex]==zero else alg.var()
    const=(values['native'][pos[hit]]==2).astype(np.uint8)
    for eid,bit in set(zip(represent[hit].tolist(),const.tolist())):alg.eq(alg.xor(eid,z4),bit)
    zi=np.searchsorted(up,zero)
    if mode=='centered' and zi<len(up) and up[zi]==zero:alg.eq(int(represent[zi]))
    answer=alg.solve()
    out['recursive_G']={**answer,'variables':alg.nextvar-1,'expressions':len(alg.terms),'lower_rank':lower['rank'],'lower_equations':lower['equations'],'zero_expressions':{'2D':list(alg.terms[z2]),'3D':list(alg.terms[z3]),'4D':list(alg.terms[z4])}}
    out['native_observed']=len(unique);out['probe_observed']=len(up);out['seconds']=time.perf_counter()-start
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--workers',type=int,default=4);args=ap.parse_args();args.output.mkdir(parents=True,exist_ok=False)
    start=time.perf_counter();records=[];picks=selected()
    with (args.output/'candidates.jsonl').open('w') as log, concurrent.futures.ProcessPoolExecutor(max_workers=args.workers)as pool:
        futures={pool.submit(run_one,r):r['rule']for r in picks}
        for future in concurrent.futures.as_completed(futures):
            rec=future.result();records.append(rec);log.write(json.dumps(rec,separators=(',',':'))+'\n');log.flush()
            print(json.dumps({'finished':len(records),'rule':rec['rule'],'native':rec['first_order_pass'],'G':rec['recursive_G']['passes'],'rule_seconds':round(rec['seconds'],2),'elapsed':round(time.perf_counter()-start,2),'total_native':sum(r['first_order_pass']for r in records),'total_G':sum(r['recursive_G']['passes']for r in records)}),flush=True)
    summary={k:sorted(r['rule']for r in records if r[k] if False)for k in []}
    summary={'first_order_rules':sorted(r['rule']for r in records if r['first_order_pass']),'recursive_G_rules':sorted(r['rule']for r in records if r['recursive_G']['passes']),'raw_G_rules':sorted(r['rule']for r in records if r['mode']=='raw'and r['recursive_G']['passes']),'centered_G_rules':sorted(r['rule']for r in records if r['mode']=='centered'and r['recursive_G']['passes'])}
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (args.output/'manifest.json').write_text(json.dumps({'seconds':time.perf_counter()-start,'selected_paths':len(picks),'source_width':16,'events_per_rule':4194304,'native_radius':[2]*4,'transverse_periods':[4]*3,'symbolic_lower_completions':True,'workers':args.workers,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n')
    (args.output/'source_audit.py').write_text(Path(__file__).read_text())
    print(json.dumps({'complete':True,'seconds':time.perf_counter()-start,'counts':{k:len(v)for k,v in summary.items()}}),flush=True)
if __name__=='__main__':main()
