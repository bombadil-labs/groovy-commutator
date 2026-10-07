#!/usr/bin/env python3
"""Compile and summarize the complete exact GQR source-pair SCC census.

Usage: python experiments/jet_gqr_256/prepare_census.py [--out /path/to.json]
Requires standard-library Python3 and a C++17 compiler (g++).
"""
from __future__ import annotations
import argparse,csv,hashlib,json,subprocess,tempfile,time
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent


def bit(rule,l,c,r):return (rule>>(4*l+2*c+r))&1

def reflect(rule):
    return sum(bit(rule,r,c,l) << (4*l+2*c+r) for l in (0,1) for c in (0,1) for r in (0,1))

def conjugate(rule):
    return sum((1^bit(rule,1-l,1-c,1-r)) << (4*l+2*c+r) for l in (0,1) for c in (0,1) for r in (0,1))

def orbits():
    left=set(range(256));found=[]
    while left:
        start=min(left);todo={start};seen=set()
        while todo:
            rule=todo.pop()
            if rule in seen:continue
            seen.add(rule)
            todo.add(reflect(rule)) if reflect(rule) not in seen else None
            todo.add(conjugate(rule)) if conjugate(rule) not in seen else None
        found.append(sorted(seen));left-=seen
    return found


def run(out):
    t0=time.monotonic()
    with tempfile.TemporaryDirectory(prefix='eca_gqr_') as tmp:
        exe=Path(tmp)/'census'
        raw=Path(tmp)/'census.tsv'
        subprocess.run(['g++','-O3','-std=c++17','-Wall','-Wextra','-pedantic',str(HERE/'gqr_census.cpp'),'-o',str(exe)],check=True)
        subprocess.run([str(exe),str(raw)],check=True)
        with raw.open(newline='') as f:rows=[{k:int(v) for k,v in row.items()} for row in csv.DictReader(f,delimiter='\t')]
    assert [x['rule'] for x in rows]==list(range(256))
    by={x['rule']:x for x in rows}
    assert by[54]['mixed']==0 and by[54]['branch_pure']==4 and by[54]['pure']==8
    assert by[30]['mixed']==0 and by[30]['pure']==8 and by[30]['branch_pure']==0
    assert by[110]['mixed']==0 and by[110]['pure']==8 and by[110]['branch_pure']==0
    assert by[62]['mixed']==1 and by[62]['branch_mixed']==1
    assert by[90]['G_nz']==by[90]['Q_nz']==by[90]['R_nz']==0
    assert by[90]['edges']==262144
    categories={
       'all_zero_GQR':[x['rule'] for x in rows if x['G_nz']==x['Q_nz']==x['R_nz']==0],
       'any_branching_offdiagonal':[x['rule'] for x in rows if x['branch_mixed']+x['branch_pure']>0],
       'mixed_branching':[x['rule'] for x in rows if x['branch_mixed']>0],
       'pure_offdiagonal_branching':[x['rule'] for x in rows if x['branch_pure']>0],
       'pure_branching_without_mixed':[x['rule'] for x in rows if x['branch_pure']>0 and x['branch_mixed']==0],
       'recurrent_offdiagonal_only_cycles':[x['rule'] for x in rows if x['mixed']+x['pure']>0 and x['branch_mixed']==x['branch_pure']==0],
       'no_recurrent_offdiagonal':[x['rule'] for x in rows if x['mixed']+x['pure']==0],
       'full_local_GQR_alphabet':[x['rule'] for x in rows if x['gqr_symbols']==8]
    }
    orb=orbits()
    statuses={r:'branching' if by[r]['branch_pure']+by[r]['branch_mixed']>0 else 'cycle-only' for r in range(256)}
    differing=[o for o in orb if len({statuses[r] for r in o})>1]
    result={
      'schema':'all256_gqr_pair_scc_v1','date':'2026-10-07',
      'protocol':'docs/research/protocols/jet-gqr-census-fibonacci-invariance-20261007.md',
      'source_description':'full-line binary ECA, radius-4 GQR field, source de Bruijn contexts 8 bits',
      'definition':'A0=I XOR H; A{k+1}=A{k} o H XOR H o A{k}; output=(A1,A2,A3)',
      'controls_checked':[30,54,62,90,110],
      'rule_count':len(rows),'raw_rows':rows,
      'categories':categories,
      'counts':{name:len(members) for name,members in categories.items()},
      'max_cycle_period_histogram':{str(k):v for k,v in sorted(Counter(row['max_cycle_period'] for row in rows).items())},
      'Wolfram_reflection_conjugacy_orbits':{
         'number':len(orb),
         'category_invariant_in_every_orbit':not differing,
         'orbits_with_mixed_branching_status':differing,
         'warning':'The jet-GQR branching criterion is not necessarily invariant under complement conjugacy.'
      },
      'sources_sha256':{
         'cxx_source':hashlib.sha256((HERE/'gqr_census.cpp').read_bytes()).hexdigest(),
         'summary_runner':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
      },
      'runtime_seconds_including_compilation':time.monotonic()-t0
    }
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'rule_count':len(rows),'counts':result['counts'],'orbit_count':len(orb),
                      'orbits_with_mixed_status':len(differing),'runtime_s':result['runtime_seconds_including_compilation']},sort_keys=True,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--out',type=Path,default=ROOT/'results'/'jet_gqr_256_20261007.json')
    run(p.parse_args().out)
