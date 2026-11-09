#!/usr/bin/env python3
"""Independent NumPy/SciPy replay of Rule54 J5 factor, radius and preimage clock.

Builds Boolean commutator truth tables from definitions with no repository
imports. Same-author replication only; independent peer review still pending.
"""
from collections import defaultdict, deque
from hashlib import sha256
import json
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

rule=54
def h(left,middle,right):
    return ((rule>>(4*left+2*middle+right))&1).astype(np.uint8)

w=np.arange(8,dtype=np.uint32)
a=[((w>>1)&1).astype(np.uint8)^h(w&1,(w>>1)&1,(w>>2)&1)]
for k in range(6):
    r=k+1
    words=np.arange(1<<(2*r+3),dtype=np.uint32)
    evolved=np.zeros(len(words),dtype=np.uint32)
    for j in range(2*r+1):
        evolved|=h((words>>j)&1,(words>>(j+1))&1,(words>>(j+2))&1).astype(np.uint32)<<j
    mask=(1<<(2*r+1))-1
    x=a[-1][words&mask]; y=a[-1][(words>>1)&mask]; z=a[-1][(words>>2)&mask]
    a.append(a[-1][evolved]^h(x,y,z))

edges=np.arange(8192,dtype=np.uint32)
base=4096
labels=np.zeros(len(edges),dtype=np.uint8)
for k in range(1,6):
    shift=6-(k+1)
    labels|=a[k][(edges>>shift)&((1<<(2*k+3))-1)]<<(k-1)
ss=[];tt=[]
for tag in range(32):
    b=edges[labels==tag]
    x=np.repeat(b,len(b));y=np.tile(b,len(b))
    ss.append((x&4095)*base+(y&4095))
    tt.append((x>>1)*base+(y>>1))
s=np.concatenate(ss);t=np.concatenate(tt)
assert len(s)==3561416
v,inv=np.unique(np.concatenate([s,t]),return_inverse=True)
E=len(s);src=inv[:E].astype(np.int32);dst=inv[E:].astype(np.int32)

alive=np.ones(len(v),dtype=bool)
for iteration in range(100):
    keep=alive[src]&alive[dst]
    incoming=np.bincount(dst[keep],minlength=len(v))
    outgoing=np.bincount(src[keep],minlength=len(v))
    newer=alive&(incoming>0)&(outgoing>0)
    if np.array_equal(newer,alive):break
    alive=newer
else:raise AssertionError("core pruning failed to converge")
keep=alive[src]&alive[dst]
assert int(alive.sum())==4316 and int(keep.sum())==8460

adj=defaultdict(list)
for p,q in zip(src[keep],dst[keep]):adj[int(p)].append(int(q))
paths=bad=0
for i0 in np.flatnonzero(alive):
    for i1 in adj.get(int(i0),[]):
        for i2 in adj.get(i1,[]):
            for i3 in adj.get(i2,[]):
                xs=[int(v[i]//base) for i in (i0,i1,i2,i3)]
                ys=[int(v[i]%base) for i in (i0,i1,i2,i3)]
                x=xs[0]|((xs[1]>>11)<<12)|((xs[2]>>11)<<13)|((xs[3]>>11)<<14)
                y=ys[0]|((ys[1]>>11)<<12)|((ys[2]>>11)<<13)|((ys[3]>>11)<<14)
                paths+=1
                bad+=int(a[6][x]!=a[6][y])
assert paths==33162 and bad==0

words=np.arange(32768,dtype=np.uint32)
packed=np.zeros(len(words),dtype=np.uint32)
for site in range(3):
    w=(words>>site)&8191
    label=np.zeros(len(words),dtype=np.uint32)
    for k in range(1,6):
        shift=6-(k+1)
        label|=a[k][(w>>shift)&((1<<(2*k+3))-1)].astype(np.uint32)<<(k-1)
    packed|=label<<(5*site)
groups=defaultdict(lambda:[[],[]])
for word,key in enumerate(packed):groups[int(key)][int(a[6][word])].append(word)
xs=[];ys=[]
for zero,one in groups.values():
    if zero and one:
        xs.append(np.repeat(np.asarray(zero,dtype=np.uint32),len(one)))
        ys.append(np.tile(np.asarray(one,dtype=np.uint32),len(zero)))
x=np.concatenate(xs);y=np.concatenate(ys)
assert len(x)==196196
start=(x&4095)*base+(y&4095)
finish=(x>>3)*base+(y>>3)
i0=np.searchsorted(v,start);i3=np.searchsorted(v,finish)
assert np.all(v[i0]==start) and np.all(v[i3]==finish)
left=[np.ones(len(v),dtype=bool)];right=[np.ones(len(v),dtype=bool)]
for i in range(5):
    left.append(np.bincount(dst,weights=left[-1][src].astype(np.uint8),minlength=len(v))>0)
    right.append(np.bincount(src,weights=right[-1][dst].astype(np.uint8),minlength=len(v))>0)
def failures(l,r):return int(np.count_nonzero(left[l-1][i0]&right[r-1][i3]))
counts=[failures(n,n) for n in range(1,7)]
assert counts==[196196,5428,334,98,12,0]
assert failures(6,5)==4 and failures(5,6)==4

U="00100111";V="01110010"
succ=np.zeros(len(edges),dtype=np.uint32)
for p in range(1,12):
    succ|=h((edges>>(p-1))&1,(edges>>p)&1,(edges>>(p+1))&1).astype(np.uint32)<<(p-1)
candidates=set()
for phase in range(8):
    ux=sum(int(U[(phase+j)%8])<<j for j in range(11))
    vy=sum(int(V[(phase+j)%8])<<j for j in range(11))
    vx=np.flatnonzero(succ==ux)
    vyw=np.flatnonzero(succ==vy)
    candidates.update((int(x),int(y)) for x in vx for y in vyw if labels[x]==labels[y])
CE=sorted(candidates)
CV=sorted({(x&4095,y&4095) for x,y in CE}|{(x>>1,y>>1) for x,y in CE})
ci={context:i for i,context in enumerate(CV)}
cs=np.array([ci[(x&4095,y&4095)] for x,y in CE],dtype=np.int32)
ct=np.array([ci[(x>>1,y>>1)] for x,y in CE],dtype=np.int32)
sm=csr_matrix((np.ones(len(CE),dtype=np.uint8),(cs,ct)),shape=(len(CV),len(CV)))
ncomp, ids=connected_components(sm,directed=True,connection="strong")
intern=ids[cs]==ids[ct]
cycles=[i for i in range(ncomp) if np.any(intern&(ids[cs]==i))]
assert len(cycles)==1
chosen=cycles[0]
member=sorted(np.flatnonzero(ids==chosen))
inside=sorted((x,y) for j,(x,y) in enumerate(CE) if intern[j] and ids[cs[j]]==chosen)
assert (len(CE),len(CV),len(member),len(inside))==(882,704,52,58)
edge_sha=sha256(json.dumps(inside,separators=(",",":")).encode()).hexdigest()
assert edge_sha=="8038efc7d2c33bca3b4ad5fbcc7acaa970feb7924de46c196ccd69418679cb7a"
local={int(g):i for i,g in enumerate(member)}
A=np.zeros((52,52),dtype=np.int64)
for i in range(len(CE)):
    if intern[i] and ids[cs[i]]==chosen:
        A[local[int(cs[i])],local[int(ct[i])]]+=1
phase={0:0}; queue=deque([0])
while queue:
    v0=queue.popleft()
    for v1 in np.flatnonzero(A[v0]):
        v1=int(v1);target=(phase[v0]+1)%8
        if v1 in phase:assert phase[v1]==target
        else:phase[v1]=target;queue.append(v1)
assert len(phase)==52
pop=[sum(x==i for x in phase.values()) for i in range(8)]
R8=np.linalg.matrix_power(A,8)
block=[v for v,p in sorted(phase.items()) if p==0]
B=R8[np.ix_(block,block)]
patterns=list(dict.fromkeys(tuple(int(x) for x in row) for row in B))
groups=[[j for j,row in enumerate(B) if tuple(int(x) for x in row)==pattern] for pattern in patterns]
quotient=[[int(B[groups[i][0],groups[j]].sum()) for j in range(len(groups))] for i in range(len(groups))]
assert pop==[5,8,8,5,5,8,8,5] and quotient==[[1,1],[1,2]]
period_counts={str(n):int(np.trace(np.linalg.matrix_power(A,n))) for n in (8,16,24,32)}
assert period_counts=={"8":24,"16":56,"24":144,"32":376}

report={"schema":"rule54-J5-independent-graph-audit-v1",
        "pair_edges":E,"pair_vertices_before_prune":len(v),
        "biinfinite_vertices":int(alive.sum()),"biinfinite_edges":int(keep.sum()),
        "three_edge_paths":paths,"A6_disagreements":bad,
        "bad_contexts_by_symmetric_radius_1_to_6":counts,
        "bad_contexts_after_left_only_extension":failures(6,5),
        "bad_contexts_after_right_only_extension":failures(5,6),
        "transient_clock":{"candidate_edges":len(CE),"candidate_vertices":len(CV),
                           "SCC_vertices":len(member),"SCC_edges":len(inside),
                           "edge_sha256":edge_sha,"phase_population":pop,
                           "eight_step_quotient":quotient,"periodic_paths":period_counts},
        "status":"same-author independent implementation, not peer review"}
print(json.dumps(report,indent=2))
