"""Frozen-protocol finite models; research instrument, not a core engine change.

p[k] is the physical position read as rule-table output k. All updates are
synchronous. Reproduce with python scripts/experiment_shared_state_rule.py.
"""
from pathlib import Path
import sys, json, hashlib, csv, itertools
from collections import deque, Counter
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from groovy.ca import apply_rule
OUT = ROOT / 'results'
PREFIX = 'shared_state_rule_20260907'
OFFSETS = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]
CHECKS = Counter()

def sha(data): return hashlib.sha256(data).hexdigest()
def dump(name, obj): (OUT / (PREFIX + name + '.json')).write_text(json.dumps(obj, indent=2) + '\n')
def permutations():
    ps = [tuple((i+j)%8 for i in range(8)) for j in range(8)]
    ps += [tuple((j-i)%8 for i in range(8)) for j in range(8)]
    rng = np.random.default_rng(20260907)
    while len(ps)<24:
        p = tuple(map(int,rng.permutation(8)))
        if p not in ps: ps.append(p)
    return ps

def graph(f):
    n=len(f); indeg=np.bincount(f,minlength=n); work=indeg.copy()
    q=deque(map(int,np.flatnonzero(work==0))); peeled=[]
    while q:
        x=q.popleft(); peeled.append(x); y=int(f[x]); work[y]-=1
        if work[y]==0:q.append(y)
    recurrent=work>0; labels=np.full(n,-1,dtype=np.int32); depth=np.zeros(n,dtype=np.int32)
    cycles=[]
    for x in np.flatnonzero(recurrent):
        if labels[x]>=0:continue
        cyc=[]; y=int(x)
        while labels[y]<0:
            labels[y]=len(cycles);cyc.append(y);y=int(f[y])
        assert y==x
        cycles.append(cyc)
    for x in reversed(peeled):
        labels[x]=labels[f[x]];depth[x]=depth[f[x]]+1
    lengths=np.array([len(c) for c in cycles]); basins=np.bincount(labels,minlength=len(cycles))
    assert np.all(labels>=0) and int(basins.sum())==n and int(lengths.sum())==int(recurrent.sum())
    for start in np.linspace(0,n-1,32,dtype=int):
        seen={};y=int(start)
        while y not in seen:seen[y]=len(seen);y=int(f[y])
        assert seen[y]==depth[start] and len(seen)-seen[y]==lengths[labels[start]]
        CHECKS['independent_orbits']+=1
    d=np.arange(n,dtype=np.int64)^f
    g=d[f]^f[d]
    stats=dict(states=n,image=int(np.count_nonzero(indeg)),fixed=int(np.sum(f==np.arange(n))),
        cycles=len(cycles),recurrent=int(recurrent.sum()),max_period=int(lengths.max()),
        max_transient=int(depth.max()),largest_basin=int(basins.max()),
        commutator_nonzero=int(np.count_nonzero(g)),graph_sha256=sha(f.astype('<u4').tobytes()))
    detail=dict(cycle_histogram=dict(sorted(Counter(map(int,lengths)).items())),
        longest_cycle=cycles[int(np.argmax(lengths))],indegree_histogram=dict(sorted(Counter(map(int,indeg)).items())))
    CHECKS['graph_accounting']+=1
    return stats,detail,recurrent

def ring_table():
    states=np.arange(256,dtype=np.int64); bits=(states[:,None]>>np.arange(8))&1
    address=4*np.roll(bits,1,axis=1)+2*bits+np.roll(bits,-1,axis=1)
    e=((((states[:,None,None]>>address[None,:,:])&1)<<np.arange(8)).sum(axis=2))
    for r in range(256):
        for s in range(256):
            expected=int(np.dot(apply_rule(bits[s].astype(np.uint8),r),1<<np.arange(8)))
            assert e[r,s]==expected
    CHECKS['base_engine_transitions']=65536
    return e

def local_table(p,axis):
    bits=(np.arange(512)[:,None]>>np.arange(9))&1
    a,b=(6,2) if axis=='horizontal' else (0,4)
    q=4*bits[:,a]+2*bits[:,8]+bits[:,b]
    return bits[np.arange(512),np.asarray(p)[q]].astype(np.uint8)

def windows(n):
    states=np.arange(1<<(n*n),dtype=np.int64)
    ws=np.zeros((len(states),n*n),dtype=np.int64)
    for y in range(n):
        for x in range(n):
            for k,(dy,dx) in enumerate(OFFSETS+[(0,0)]):
                ws[:,y*n+x]|=((states>>(((y+dy)%n)*n+(x+dx)%n))&1)<<k
    return ws

def global_map(lut,ws): return (lut[ws].astype(np.int64)<<np.arange(ws.shape[1])).sum(axis=1)

def rotate_states(n):
    states=np.arange(1<<(n*n),dtype=np.int64); out=np.zeros_like(states)
    for y in range(n):
        for x in range(n):out|=((states>>(y*n+x))&1)<<(x*n+(n-1-y))
    return out

def local_sweep():
    ps=np.asarray(list(itertools.permutations(range(8))),dtype=np.int64)
    bits=((np.arange(512)[:,None]>>np.arange(9))&1).astype(np.uint8)
    pop=np.array([int(x).bit_count() for x in range(512)])
    hist={}; unions=set()
    for axis,a,b in [('horizontal',6,2),('vertical',0,4)]:
        q=4*bits[:,a]+2*bits[:,8]+bits[:,b]
        tables=bits[np.arange(512)[None,:],ps[:,q]]
        assert np.all(tables[:,0]==0) and np.all(tables[:,511]==1)
        coeff=tables.copy(); essential=np.zeros(len(ps),dtype=int)
        for k in range(9):
            hi=np.flatnonzero(np.arange(512)&(1<<k));lo=hi^(1<<k)
            essential+=np.any(tables[:,hi]!=tables[:,lo],axis=1)
            coeff[:,hi]^=coeff[:,lo]
        degree=(coeff*pop).max(axis=1)
        keys=[bytes(row) for row in np.packbits(tables,axis=1)]
        unions.update(keys)
        hist[axis]={'permutations':len(ps),'distinct_tables':len(set(keys)),
            'joint_histogram':[dict(ones=int(k[0]),essential=int(k[1]),degree=int(k[2]),count=v)
              for k,v in sorted(Counter(zip(tables.sum(axis=1),essential,degree)).items())]}
        CHECKS['local_tables']+=len(ps)
    hist['distinct_tables_both_axes']=len(unions)
    return hist

def main():
    ps=permutations();e=ring_table();rows=[];details={};base_frozen=None
    z=np.arange(65536,dtype=np.int64);r=z>>8;s=z&255;swap=(s<<8)|r
    for pi,p in enumerate(ps):
        decode=((((np.arange(256)[:,None]>>p)&1)<<np.arange(8)).sum(axis=1))
        sp=e[decode[r],s]
        for mode in ['frozen','mutual','derivative']:
            rp={'frozen':r,'mutual':e[decode[s],r],'derivative':s^sp}[mode]
            f=(rp<<8)|sp
            if mode=='mutual':assert np.array_equal(f[swap],((f&255)<<8)|(f>>8));CHECKS['swap_symmetry']+=1
            if mode=='frozen':
                if pi==0:base_frozen=f.copy()
                relabel=(decode[r]<<8)|s
                assert np.array_equal((decode[f>>8]<<8)|(f&255),base_frozen[relabel])
                CHECKS['frozen_conjugacy']+=1
            stat,detail,rec=graph(f)
            stat.update(model='ring',mode=mode,encoding=pi,width=8,rule_change_recurrent=int(np.sum((rp!=r)&rec)))
            rows.append(stat);details[f'ring/{mode}/{pi}']=detail
        print('ring',pi,flush=True)
    local=local_sweep();ws={n:windows(n) for n in [3,4]}
    for pi,p in enumerate(ps):
        for axis in ['horizontal','vertical']:
            lut=local_table(p,axis)
            for w in range(512):
                b=[(w>>k)&1 for k in range(9)];a,c=(6,2) if axis=='horizontal' else (0,4)
                assert lut[w]==b[p[4*b[a]+2*b[8]+b[c]]]
                CHECKS['scalar_local_outputs']+=1
            for n in [3,4]:
                f=global_map(lut,ws[n]);stat,detail,rec=graph(f)
                stat.update(model='selector2d',mode=axis,encoding=pi,width=n,rule_change_recurrent='')
                rows.append(stat);details[f'selector2d/{axis}/{pi}/{n}']=detail
                if axis=='horizontal':
                    # Clockwise rotation maps W->N and E->S and neighbor k->k+2.
                    rotated_p=tuple((k+2)%8 for k in p)
                    fr=global_map(local_table(rotated_p,'vertical'),ws[n]);rot=rotate_states(n)
                    assert np.array_equal(rot[f],fr[rot]);CHECKS['rotation_conjugacy_states']+=len(f)
        print('selector',pi,flush=True)
    with (OUT/(PREFIX+'.csv')).open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    dump('_graphs',details);dump('_local',local)
    dump('_metadata',dict(protocol_sha256=sha((ROOT/'docs/research/protocols/shared-state-rule-20260907.md').read_bytes()),
        script_sha256=sha(Path(__file__).read_bytes()),numpy=np.__version__,encodings=ps,checks=dict(CHECKS),
        graph_count=len(rows),protocol_commit='dd7e079e7a16156f61d85e68cbb553170e786c56'))
    print(json.dumps({'graphs':len(rows),'checks':dict(CHECKS),'local':local},indent=2))
if __name__=='__main__':main()
