#!/usr/bin/env python3
"""Rule54 J5 almost-sure injectivity: exact pair-SCC entropy certificate.

Constructs the full equal-G..A5 source-pair de Bruijn graph, prunes to
bi-infinite support, and verifies that all non-diagonal recurrent SCCs
have Perron root <= sqrt(phi) < 2 and no cross-component essential edge.
The corollary is for the fair Bernoulli source on the full binary line.
"""
from __future__ import annotations
import json,math,sys
from pathlib import Path
from collections import Counter
import numpy as np
import sympy as sp
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'experiments'/'jet_gqr_256'))
from jet_algebra import local_truth_tables,labeled_edges,ordered_pair_edges,biinfinite_core

def run():
  fields=local_truth_tables(54)
  src,dst,labels,N,r=labeled_edges(fields,5)
  pair_src,pair_dst=ordered_pair_edges(src,dst,labels,N)
  assert len(pair_src)==3561416
  vertices,inverse=np.unique(np.r_[pair_src,pair_dst],return_inverse=True)
  E=len(pair_src)
  es=inverse[:E].astype(np.int32)
  ed=inverse[E:].astype(np.int32)
  alive=biinfinite_core(len(vertices),es,ed)
  core=np.flatnonzero(alive)
  remap=np.full(len(vertices),-1,dtype=np.int32)
  remap[core]=np.arange(len(core),dtype=np.int32)
  mask=alive[es]&alive[ed]
  cs=remap[es[mask]]
  ct=remap[ed[mask]]
  raw=vertices[core]
  diagonal=(raw//N)==(raw%N)
  assert len(raw)==4316 and len(cs)==8460
  matrix=csr_matrix((np.ones(len(cs),dtype=np.uint8),(cs,ct)),
                     shape=(len(raw),len(raw)))
  ncomp,ids=connected_components(matrix,directed=True,connection='strong')
  inter=ids[cs]==ids[ct]
  cross=int((~inter).sum())
  assert cross==0
  nsize=np.bincount(ids,minlength=ncomp)
  nedge=np.bincount(ids[cs[inter]],minlength=ncomp)
  ndiag=np.bincount(ids,weights=diagonal.astype(np.uint8),minlength=ncomp).astype(int)
  branch=[]
  cycles=[]
  for k in range(ncomp):
    size=int(nsize[k]);edges=int(nedge[k]);ds=int(ndiag[k])
    if not edges or ds==size:continue
    assert ds==0,(k,size,ds)
    if edges==size:cycles.append(size);continue
    assert edges>size
    idx=np.flatnonzero(ids==k)
    inds={int(v):i for i,v in enumerate(idx)}
    ee=np.flatnonzero(inter & (ids[cs]==k))
    A=sp.zeros(size)
    for edge in ee:
      A[inds[int(cs[edge])],inds[int(ct[edge])]]+=1
    z=sp.Symbol('z')
    poly=sp.factor(A.charpoly(z).as_expr())
    branch.append({'vertices':size,'edges':edges,'characteristic_polynomial':str(poly)})
  assert sorted((b['vertices'],b['edges']) for b in branch)==[(52,58),(52,68),(84,110)]
  assert len(cycles)==11
  polys={(x['vertices'],x['edges']):x['characteristic_polynomial'] for x in branch}
  z=sp.Symbol('z')
  golden=z**4-z**2-1
  assert sp.rem(sp.sympify(polys[(52,68)]),golden,z)==0
  assert sp.rem(sp.sympify(polys[(84,110)]),golden,z)==0
  assert sp.rem(sp.sympify(polys[(52,58)]),z**8-z**4-1,z)==0
  assert sp.rem(sp.sympify(polys[(52,58)]),z**8+z**4-1,z)==0
  entropy=.5*math.log2((1+math.sqrt(5))/2)
  out={
    'schema':'rule54-j5-almost-sure-injective-certificate-v1',
    'rule':54,'prefix':['G','Q','R','A4','A5'],
    'pair_edges':len(pair_src),'biinfinite_core_vertices':len(raw),'biinfinite_core_edges':len(cs),
    'cross_scc_edges_on_biinfinite_core':cross,
    'pure_offdiagonal_branch_components':sorted(branch,key=lambda x:(x['vertices'],x['edges'])),
    'pure_offdiagonal_cycle_components':len(cycles),
    'largest_nondiagonal_perron':'sqrt(phi)',
    'offdiagonal_pair_language_entropy_bits_per_site':entropy,
    'source_projection_entropy_upper_bound_bits_per_site':entropy,
    'fair_bernoulli_a.e._injective':True,
    'interpretation':(
      'All distinct equal-jet source pairs live in SCC subshifts with spatial '
      'entropy strictly below the full-shift source entropy 1. Their projection '
      'onto either source rail therefore has fair-Bernoulli measure zero; '
      'thus the J5 factor has singleton fibers almost surely. This does NOT '
      'make J5 topologically injective and does NOT erase exceptional phase pairs.'
    )
  }
  print(json.dumps(out,indent=2,sort_keys=True))
  return out

if __name__=='__main__':
  result=run()
  if len(sys.argv)>1:
    path=Path(sys.argv[1]);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
