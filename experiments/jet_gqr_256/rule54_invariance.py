#!/usr/bin/env python3
"""Exact Rule54 branching equal-G..A5 fiber invariance audit.

Frozen protocol at docs/research/protocols/jet-gqr-census-fibonacci-invariance-20261007.md.
The source pair graph is an exact de Bruijn presentation of the same-output
relation. Length-three internal edge paths correspond to all 15-cell source
pairs needed to inspect one Rule54 update of a 13-cell G..A5 equal-output
pair patch. Every internal edge of an SCC lies on a bi-infinite path.
"""
from __future__ import annotations
import argparse, hashlib, json, sys, time, resource
from pathlib import Path
from collections import defaultdict, Counter
import numpy as np
import sympy as sp
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components
from scipy.sparse.linalg import eigs

from jet_algebra import local_truth_tables, labeled_edges, ordered_pair_edges, biinfinite_core

RULE=54
RADIUS=6
WIDTH=2*RADIUS+1  #13
CAP=5_000_000
MASK12=(1<<12)-1
DEFAULT_OUT=Path(__file__).resolve().parents[2] / 'results' / 'rule54_golden_invariance_20261007.json'


def f(l,c,r):
    return (RULE >> (4*l+2*c+r))&1

def step_window15_to13(w):
    out=0
    for i in range(13):
        a=(w>>i)&1;b=(w>>(i+1))&1;c=(w>>(i+2))&1
        out |= f(a,b,c)<<i
    return out

def label13(w,levels):
    return sum(int(levels[level][(w>>(RADIUS-(level+1)))&((1<<(2*(level+1)+1))-1)]) <<(level-1)
               for level in range(1,6))


def direct_label13(w):
    # Independently calculate A1..A5 from scalar source evolution and
    # recursion with zero padding. Does not use the vectorized truth tables.
    size=65
    cells=[0]*size
    center=32
    for i in range(13):cells[center-6+i]=(w>>i)&1
    def evolve(a):
        return [0]+[f(a[i-1],a[i],a[i+1]) for i in range(1,len(a)-1)]+[0]
    states=[cells]
    for _ in range(7):states.append(evolve(states[-1]))
    derivative=[[x^y for x,y in zip(states[t],states[t+1])] for t in range(7)]
    current=derivative
    for level in range(1,6):
        current=[[x^y for x,y in zip(current[t+1],evolve(current[t]))]
                 for t in range(len(current)-1)]
        result=current[0][center]
        if level==1:res=0
        res |= result<<(level-1)
    return res


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",type=Path,default=DEFAULT_OUT)
    args=parser.parse_args()
    started=time.monotonic()
    levels=local_truth_tables(RULE)
    src,dst,labels,N,r=labeled_edges(levels,5)
    cnt=np.bincount(labels)
    predicted=sum(int(c)**2 for c in cnt)
    assert predicted<=CAP, (predicted,CAP)
    a,b=ordered_pair_edges(src,dst,labels,N)
    nodes=np.unique(np.concatenate((a,b)))
    es=np.searchsorted(nodes,a).astype(np.int32)
    ed=np.searchsorted(nodes,b).astype(np.int32)
    del a,b
    alive=biinfinite_core(len(nodes),es,ed)
    chosen=np.flatnonzero(alive)
    remap=np.full(len(nodes),-1,dtype=np.int32)
    remap[chosen]=np.arange(len(chosen),dtype=np.int32)
    edge_mask=alive[es]&alive[ed]
    es1=remap[es[edge_mask]]
    ed1=remap[ed[edge_mask]]
    kept=nodes[chosen]
    pairs_x=(kept//N).astype(np.uint16)
    pairs_y=(kept%N).astype(np.uint16)
    sparse=csr_matrix((np.ones(len(es1),dtype=np.uint8),(es1,ed1)),shape=(len(kept),len(kept)))
    comp_count,comp=connected_components(sparse,directed=True,connection='strong')
    in_comp=(comp[es1]==comp[ed1])
    comp_size=np.bincount(comp,minlength=comp_count)
    comp_edges=np.bincount(comp[es1[in_comp]],minlength=comp_count)
    comp_diag=np.bincount(comp,(pairs_x==pairs_y).astype(int),minlength=comp_count)
    targets=[c for c in range(comp_count) if comp_size[c]>0 and comp_diag[c]==0 and comp_edges[c]>comp_size[c]]
    target_rows=[]
    for c in targets:
        members=np.flatnonzero(comp==c)
        ma=in_comp&(comp[es1]==c)
        internal_es=es1[ma]
        internal_ed=ed1[ma]
        lookup={int(v):i for i,v in enumerate(members)}
        adj=defaultdict(list)
        edges_list=[]
        for s,d in zip(internal_es.tolist(),internal_ed.tolist()):
            adj[s].append(d)
            edges_list.append((s,d))
        for x in adj:adj[x].sort(key=lambda v:(int(pairs_x[v]),int(pairs_y[v])))
        # SCC Perron from the exact multigraph.
        locs=np.array([lookup[int(v)] for v in internal_es],dtype=np.int32)
        locd=np.array([lookup[int(v)] for v in internal_ed],dtype=np.int32)
        n=len(members)
        A=csr_matrix((np.ones(len(locs)),(locs,locd)),shape=(n,n))
        spectral=float(np.abs(eigs(A,k=1,which='LM',return_eigenvectors=False,tol=1e-12)[0]))
        polynomial=None
        if (n,len(internal_es)) in ((52,68),(84,110)):
            z=sp.Symbol('z')
            polynomial=sp.factor(sp.Matrix(A.toarray().astype(int)).charpoly(z).as_expr())
            assert polynomial.has(z**4-z**2-1) or sp.rem(polynomial,z**4-z**2-1,z)==0
            print('exact characteristic polynomial',str(polynomial),flush=True)
        # Enumerate every pair of 15-bit source words represented by three
        # consecutive internal edges in the SCC. Each vertex is 12 source bits,
        # and each traversed edge appends the new source bit at position 12.
        paths=[]
        for v0 in members.tolist():
            for v1 in adj.get(v0,[]):
                for v2 in adj.get(v1,[]):
                    for v3 in adj.get(v2,[]):
                        wx=int(pairs_x[v0])
                        wy=int(pairs_y[v0])
                        for v,shift in ((v1,12),(v2,13),(v3,14)):
                            wx |= ((int(pairs_x[v])>>11)&1)<<shift
                            wy |= ((int(pairs_y[v])>>11)&1)<<shift
                        paths.append((wx,wy,v0,v1,v2,v3))
        paths.sort()
        equal_errors=[]
        self_errors=[]
        union_errors=[]
        labels_verified=0
        sample_check_indices=set(range(len(paths)))
        destinations=Counter()
        # Convert SCC id to membership for the union of three target SCCs.
        target_set=set(targets)
        for index,(wx,wy,v0,v1,v2,v3) in enumerate(paths):
            ex=step_window15_to13(wx)
            ey=step_window15_to13(wy)
            ax=label13(ex,levels)
            ay=label13(ey,levels)
            if index in sample_check_indices:
                assert direct_label13(ex)==ax and direct_label13(ey)==ay,(c,index,ex,ey)
                labels_verified+=1
            if ax!=ay:
                if not equal_errors:equal_errors.append({'source_x_15bit':wx,'source_y_15bit':wy,'evolved_x_13bit':ex,'evolved_y_13bit':ey,'next_jet_x':ax,'next_jet_y':ay,'changed_fields':[name for i,name in enumerate(['G','Q','R','A4','A5']) if ((ax^ay)>>i)&1]})
                continue
            start_raw=(ex&MASK12)*N + (ey&MASK12)
            end_raw=(ex>>1)*N + (ey>>1)
            aidx=np.searchsorted(kept,start_raw)
            bidx=np.searchsorted(kept,end_raw)
            valid=(aidx<len(kept) and kept[aidx]==start_raw and bidx<len(kept) and kept[bidx]==end_raw)
            membership=(int(comp[aidx]) if valid and comp[aidx]==comp[bidx] else -1)
            destinations[membership]+=1
            if membership!=c and not self_errors:
                self_errors.append({'source_x_15bit':wx,'source_y_15bit':wy,'evolved_x_13bit':ex,'evolved_y_13bit':ey,'next_pair_component_id':membership})
            if membership not in target_set and not union_errors:
                union_errors.append({'source_x_15bit':wx,'source_y_15bit':wy,'evolved_x_13bit':ex,'evolved_y_13bit':ey,'next_pair_component_id':membership})
        target_rows.append({
            'component_id':int(c),'vertices':int(comp_size[c]),'edges':int(comp_edges[c]),
            'exact_characteristic_polynomial':str(polynomial) if polynomial is not None else None,
            'perron':spectral,'first_pair_context_raw':int(kept[members[0]]),
            'three_edge_paths_tested':len(paths),'independent_scalar_spotchecks':labels_verified,
            'claim_I_next_time_same_G_A5':not equal_errors,'claim_I_first_counterexample':equal_errors[0] if equal_errors else None,
            'claim_II_image_in_same_component':not self_errors and not equal_errors,
            'claim_II_first_counterexample':self_errors[0] if self_errors else None,
            'image_in_fixed_three_component_union':not union_errors and not equal_errors,
            'union_first_counterexample':union_errors[0] if union_errors else None,
            'destination_component_histogram':{str(k):int(v) for k,v in sorted(destinations.items())},
            'any_jet_mismatch_first':equal_errors[0] if equal_errors else None
        })
        print('component',c,'verts',n,'edges',len(edges_list),'rho',round(spectral,9),'paths',len(paths),'I',not equal_errors,'II',not self_errors and not equal_errors,'union',not union_errors and not equal_errors,flush=True)
    result={
        'schema':'rule54_golden_pair_invariance_v1',
        'protocol':'docs/research/protocols/jet-gqr-census-fibonacci-invariance-20261007.md',
        'rule':54,'jet_prefix':['G','Q','R','A4','A5'],'source_radius':6,
        'pair_edges':predicted,'biinfinite_vertices':int(len(kept)),'biinfinite_edges':int(len(es1)),
        'target_components_count':len(targets),'target_components':target_rows,
        'any_all_order_single_component_invariant':any(x['claim_II_image_in_same_component'] for x in target_rows),
        'all_three_union_invariant':all(x['image_in_fixed_three_component_union'] for x in target_rows),
        'cpu_elapsed_seconds':time.monotonic()-started,'maximum_resident_set_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    }
    bysize={(c['vertices'],c['edges']):c for c in target_rows}
    plus=bysize[(52,68)]
    minus=bysize[(84,110)]
    pass_plus=plus['destination_component_histogram']=={str(minus['component_id']):plus['three_edge_paths_tested']}
    pass_minus=minus['destination_component_histogram']=={str(plus['component_id']):minus['three_edge_paths_tested']}
    result['post_primary_golden_swap']={
        'protocol':'docs/research/protocols/rule54-two-golden-scc-swap-20261007.md',
        'chosen_by':'two maximal-Perron non-diagonal branching components preselected after original three-component outcome',
        'components':[plus['component_id'],minus['component_id']],
        'plus_to_minus':pass_plus,'minus_to_plus':pass_minus,
        'full_line_forward_invariant_union':pass_plus and pass_minus,
        'all_higher_jet_levels_equal_by_induction':pass_plus and pass_minus,
        'total_three_edge_paths_checked':plus['three_edge_paths_tested']+minus['three_edge_paths_tested'],
        'all_paths_independently_checked_scalar':plus['independent_scalar_spotchecks']==plus['three_edge_paths_tested'] and minus['independent_scalar_spotchecks']==minus['three_edge_paths_tested']
    }
    result['source_hashes']={
        'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'algebra_sha256':hashlib.sha256(Path(__file__).with_name('jet_algebra.py').read_bytes()).hexdigest()
    }
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('wrote',args.out,'in',round(result['cpu_elapsed_seconds'],2),'s')
    print('post-primary golden swap:',json.dumps(result['post_primary_golden_swap'],sort_keys=True))

if __name__=='__main__':main()
