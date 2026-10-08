#!/usr/bin/env python3
"""Construct Rule54 C_small from an eight-periodic successor pair.

This replaces a 3,561,416-edge full equal-jet graph with 882 local
preimage-constrained paired edges, then prunes to recurrent bi-infinite
paths. It identifies the exact 52v/58e component and the Fibonacci
two-state counting quotient of its period-eight return graph.

Post-hoc structural reconstruction, not a preregistered prediction.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from collections import Counter,defaultdict,deque

import numpy as np
import sympy as sp
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

ROOT=Path(__file__).resolve().parents[2]
import sys
sys.path.insert(0,str(ROOT/'experiments'/'jet_gqr_256'))
from jet_algebra import local_truth_tables

RULE=54
U='00100111'
V='01110010'
KNOWN_EDGE_SHA='8038efc7d2c33bca3b4ad5fbcc7acaa970feb7924de46c196ccd69418679cb7a'


def source_edges():
    words=np.arange(8192,dtype=np.uint32)
    out=np.zeros(len(words),dtype=np.uint16)
    for site in range(1,12):
        l=(words>>(site-1))&1
        c=(words>>site)&1
        r=(words>>(site+1))&1
        out|=(((RULE>>(4*l+2*c+r))&1).astype(np.uint16)<<(site-1))
    jet=np.zeros(len(words),dtype=np.uint8)
    levels=local_truth_tables(RULE)
    for level in range(1,6):
        radius=level+1
        mask=(1<<(2*radius+1))-1
        jet|=(levels[level][(words>>(6-radius))&mask].astype(np.uint8)<<(level-1))
    candidates=set()
    row_counts={}
    for phase in range(8):
        xdest=sum(int(U[(phase+i)%8])<<i for i in range(11))
        ydest=sum(int(V[(phase+i)%8])<<i for i in range(11))
        xs=words[out==xdest].tolist()
        ys=words[out==ydest].tolist()
        pairs={(int(x),int(y)) for x in xs for y in ys if jet[x]==jet[y]}
        candidates.update(pairs)
        row_counts[str(phase)]={'x_preimage_words':len(xs),'y_preimage_words':len(ys),'candidate_pairs':len(pairs)}
    return sorted(candidates),row_counts


def recurrent_component(edges):
    vertices=sorted(
       {(x&4095,y&4095) for x,y in edges}
       | {(x>>1,y>>1) for x,y in edges}
    )
    index={v:i for i,v in enumerate(vertices)}
    es=np.array([index[(x&4095,y&4095)] for x,y in edges],dtype=np.int32)
    ed=np.array([index[(x>>1,y>>1)] for x,y in edges],dtype=np.int32)
    matrix=csr_matrix((np.ones(len(es),dtype=np.uint8),(es,ed)),shape=(len(vertices),len(vertices)))
    count,ids=connected_components(matrix,directed=True,connection='strong')
    sizes=np.bincount(ids,minlength=count)
    valid=ids[es]==ids[ed]
    internals=np.bincount(ids[es[valid]],minlength=count)
    recurrent=[i for i in range(count) if internals[i]>0]
    assert len(recurrent)==1
    cid=recurrent[0]
    inside=sorted((x,y) for i,(x,y) in enumerate(edges) if valid[i] and ids[es[i]]==cid)
    assert sizes[cid]==52 and len(inside)==58
    digest=hashlib.sha256(json.dumps(inside,separators=(',',':')).encode()).hexdigest()
    assert digest==KNOWN_EDGE_SHA,digest
    members=sorted(i for i in range(len(vertices)) if ids[i]==cid)
    local={g:i for i,g in enumerate(members)}
    adj=defaultdict(list)
    A=np.zeros((len(members),len(members)),dtype=np.int64)
    for i,(x,y) in enumerate(edges):
        if valid[i] and ids[es[i]]==cid:
            u=local[int(es[i])];v=local[int(ed[i])]
            adj[u].append(v)
            A[u,v]+=1
    return len(vertices),len(edges),inside,A,adj


def return_clock(A,adj):
    phase={0:0};q=deque([0])
    while q:
        i=q.popleft()
        for j in adj[i]:
            target=(phase[i]+1)%8
            if j in phase:assert phase[j]==target
            else:phase[j]=target;q.append(j)
    assert len(phase)==A.shape[0]
    phase0=sorted(i for i in phase if phase[i]==0)
    eight=np.linalg.matrix_power(A,8)
    ret=eight[np.ix_(phase0,phase0)]
    unique=list(dict.fromkeys(tuple(int(x) for x in row) for row in ret))
    groups=[[i for i,row in enumerate(ret) if tuple(int(x) for x in row)==pattern] for pattern in unique]
    assert [len(g) for g in groups]==[2,3]
    quotient=np.array([[int(ret[g[0],h].sum()) for h in groups] for g in groups],dtype=np.int64)
    assert quotient.tolist()==[[1,1],[1,2]]
    z=sp.Symbol('z')
    assert sp.factor(sp.Matrix(quotient).charpoly(z).as_expr()) == z*z-3*z+1
    periodic={str(n):int(np.trace(np.linalg.matrix_power(A,n))) for n in (8,16,24,32)}
    assert periodic=={'8':24,'16':56,'24':144,'32':376}
    return {'phase_population':{str(i):sum(v==i for v in phase.values()) for i in range(8)},
        'phase_zero_return_matrix':ret.tolist(),
        'row_pattern_groups':groups,'two_state_return_count_quotient':quotient.tolist(),
        'quotient_charpoly':'z^2 - 3z + 1',
        'perron_eigenvalue_of_8_step_return':'phi^2',
        'spatial_pair_entropy_bits_per_site':math_log2_phi()/4,
        'periodic_pair_counts':periodic}


def math_log2_phi():
    import math
    return math.log2((1+math.sqrt(5))/2)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,default=None)
    args=ap.parse_args()
    candidates,phase_rows=source_edges()
    vertices,ne,inside,A,adj=recurrent_component(candidates)
    clock=return_clock(A,adj)
    result={
      'schema':'rule54-csmall-preimage-phase-clock-v1','date':'2026-10-07',
      'provenance':'post-hoc structural reconstruction of Claude-reviewed Rule54 C_small',
      'successor_cycle_source_x':U,'successor_cycle_source_y':V,
      'local_source_word_width':13,
      'preimage_constrained_candidate_edges':ne,
      'preimage_constrained_candidate_vertices':vertices,
      'recurrent_scc_vertices':52,'recurrent_scc_edges':58,
      'recurrent_scc_edge_sha256':KNOWN_EDGE_SHA,
      'all_candidate_phases':phase_rows,
      'phase_clock':clock
    }
    if args.output is not None:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'candidates':ne,'recurrent_edges':58,'period8_return_quotient':clock['two_state_return_count_quotient'],'pair_counts':clock['periodic_pair_counts']},indent=2))


if __name__=='__main__':main()
