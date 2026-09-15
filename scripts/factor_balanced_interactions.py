#!/usr/bin/env python3
"""Frozen factor-balanced prediction study. Scientific execution is off CI."""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict
from functools import lru_cache
from itertools import combinations, combinations_with_replacement
import json
import math
from pathlib import Path
import resource
import signal
import time

import numpy as np

from rule_ring_selectors import Case, atomic_json, canonical, compare, default_registry, sha256
from rule_ring_structure import (successors, graph_partitions, label_entropy,
                                 entropy_counts, RULES, HORIZONS, OBSERVATIONS)

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT/'experiments/factor_balanced_interactions_20260915'
BANDS = {'A':list(range(4,10)), 'B':list(range(10,17)), 'C':[17,18,20,21]}
MODELS = ('M0','M1','M2')
PAIRS = list(combinations(RULES,2))
SIZE_NAMES = ['center','gap','center_squared','gap_squared','center_gap']
ARITH_NAMES = ['div2_mean','div3_mean','v2_mean','v2_gap','v3_mean','v3_gap']
PRODUCTS = list(combinations_with_replacement(range(6),2))
FEATURE_NAMES = SIZE_NAMES + ARITH_NAMES + [f'{ARITH_NAMES[i]}*{ARITH_NAMES[j]}' for i,j in PRODUCTS]
DIMENSIONS = {'M0':5, 'M1':11, 'M2':32}
SOURCES = ['scripts/factor_balanced_interactions.py','scripts/rule_ring_structure.py',
           'scripts/rule_ring_selectors.py','src/groovy/ca.py',
           'docs/research/protocols/factor-balanced-interactions-20260915.md',
           'experiments/factor_balanced_interactions_20260915/historical-relations.json',
           'experiments/factor_balanced_interactions_20260915/historical-provenance.json']
CONTEXT = {'ensemble':'all_binary_source_states','burn_in':0,'floor':1,'cadence':1,
           'completion':'full_ECA_rule','alignment':'same_source_state',
           'study':'factor-balanced-interactions-20260915/v1'}


def family(n):
    return (int(n%2 == 0),int(n%3 == 0))


def stratum(n,m):
    return tuple(sorted((family(n),family(m))))


def ring_pairs(band):
    return [(n,m) for n,m in combinations(BANDS[band],2) if family(n) != family(m)]


def exponent(n,p):
    value = 0
    while n%p == 0:
        value += 1
        n //= p
    return value


def basis(n,m):
    c,g = (n+m)/42.,(m-n)/21.
    v2n,v2m,v3n,v3m = exponent(n,2),exponent(m,2),exponent(n,3),exponent(m,3)
    arithmetic = [(int(n%2==0)+int(m%2==0))/2.,(int(n%3==0)+int(m%3==0))/2.,
                  (v2n+v2m)/8.,abs(v2n-v2m)/4.,(v3n+v3m)/4.,abs(v3n-v3m)/2.]
    return np.array([c,g,c*c,g*g,c*g]+arithmetic+[arithmetic[i]*arithmetic[j] for i,j in PRODUCTS])


def balanced_design():
    rows,weights,audit = [],[],{}
    expected = set(combinations([(0,0),(0,1),(1,0),(1,1)],2))
    for band in ('A','B','C'):
        pairs = ring_pairs(band)
        counts = Counter(stratum(n,m) for n,m in pairs)
        assert set(counts) == expected
        audit[band] = {'rings':BANDS[band],'pairs':pairs,
                       'strata':[{ 'families':key, 'count':value} for key,value in sorted(counts.items())]}
        if band == 'C':
            continue
        for n,m in pairs:
            rows.append({'band':band,'rings':[n,m],'stratum':stratum(n,m)})
            weights.append(1./(12*counts[stratum(n,m)]))
    weights = np.array(weights)
    assert abs(weights.sum()-1) < 1e-14
    for band in ('A','B'):
        for group in expected:
            total = sum(w for row,w in zip(rows,weights) if row['band']==band and row['stratum']==group)
            assert abs(total-1/12) < 1e-14
    return rows,weights,audit


def fit_model(x,y,weights):
    design = np.column_stack([np.ones(len(x)),x])
    penalty = np.diag([0.]+[.01]*x.shape[1])
    return np.linalg.solve(design.T @ (weights[:,None]*design)+penalty,
                           design.T @ (weights*y))


def predictions(x,coefficients):
    return np.column_stack([np.ones(len(x)),x]) @ coefficients


def fit_stage():
    rows,weights,audit = balanced_design()
    history = json.loads((UNIT/'historical-relations.json').read_text())
    values = {(r['observation'],*map(int,r['rules']),r['ring']):r['vi_per_bit'] for r in history}
    x = np.stack([basis(*row['rings']) for row in rows])
    test_pairs = ring_pairs('C')
    xt = np.stack([basis(n,m) for n,m in test_pairs])
    tasks = []
    for observation in OBSERVATIONS:
        for a,b in PAIRS:
            target = np.array([abs(values[observation,a,b,m]-values[observation,a,b,n])
                               for n,m in (row['rings'] for row in rows)])
            task = {'observation':observation,'rules':[a,b],'training_targets':target.tolist(),'models':{}}
            for model in MODELS:
                dimension = DIMENSIONS[model]
                coef = fit_model(x[:,:dimension],target,weights)
                raw = predictions(xt[:,:dimension],coef)
                clipped = np.clip(raw,0,1)
                train_raw = predictions(x[:,:dimension],coef)
                train_clipped = np.clip(train_raw,0,1)
                if a==0 and b==204 and observation.startswith('future_'):
                    assert np.max(abs(target)) < 1e-12 and np.max(abs(raw)) < 1e-12
                task['models'][model] = {'coefficients':coef.tolist(),'predictions':clipped.tolist(),
                    'unclipped_predictions':raw.tolist(),'test_clipping_count':int(np.count_nonzero(raw!=clipped)),
                    'training_weighted_mae':float(weights @ abs(train_clipped-target)),
                    'training_weighted_rmse':float(np.sqrt(weights @ ((train_clipped-target)**2)))}
            tasks.append(task)
    output = {'status':'complete','design':audit,'training_rows':rows,'training_weights':weights.tolist(),
              'training_features':x.tolist(),'test_pairs':test_pairs,'test_features':xt.tolist(),
              'feature_names':FEATURE_NAMES,'models':DIMENSIONS,'penalty':.01,'tasks':tasks}
    atomic_json(UNIT/'predictions.json',output)
    return {'status':'complete','tasks':len(tasks),'models':len(MODELS),'test_pairs':len(test_pairs),
            'predictions_sha256':sha256(UNIT/'predictions.json')}


def generate_case(n,rule):
    path = UNIT/'partitions'/f'n{n:02d}_r{rule:03d}.npz'
    if path.exists():
        raise FileExistsError(f'refusing to overwrite {path}')
    nxt = successors(n,rule)
    labels = graph_partitions(nxt)
    current = np.arange(1<<n,dtype=np.uint32)
    for t in range(1,max(HORIZONS)+1):
        current = nxt[current]
        if t in HORIZONS:
            labels[f'future_{t}'] = current.copy()
    if rule==0:
        assert all(np.all(labels[f'future_{t}']==0) for t in HORIZONS)
    if rule==204:
        assert all(np.array_equal(labels[f'future_{t}'],np.arange(1<<n)) for t in HORIZONS)
    path.parent.mkdir(parents=True,exist_ok=True)
    temp = path.with_suffix('.tmp.npz')
    np.savez_compressed(temp,successor=nxt,**labels)
    temp.replace(path)
    digest = sha256(path)
    relative = str(path.relative_to(ROOT))
    cases = [Case(str(rule),n,observation,{'path':relative,'key':observation,'sha256':digest,'ring':n},
                  CONTEXT,f'{relative}#sha256={digest};{observation}') for observation in OBSERVATIONS]
    info = {'ring':n,'rule':rule,'states':1<<n,'path':relative,'sha256':digest,
            'entropies':{name:label_entropy(labels[name]) for name in OBSERVATIONS},
            'blocks':{name:int(len(np.unique(labels[name]))) for name in OBSERVATIONS},
            'max_transient':int(labels['transient_depth'].max()),'max_cycle_length':int(labels['cycle_length'].max())}
    return cases,info


VERIFIED_FILES = set()


@lru_cache(maxsize=16)
def load_partition(text):
    meta = json.loads(text)
    path = ROOT/meta['path']
    key = (str(path),meta['sha256'])
    if key not in VERIFIED_FILES:
        if sha256(path)!=meta['sha256']:
            raise ValueError('partition hash mismatch')
        VERIFIED_FILES.add(key)
    with np.load(path,allow_pickle=False) as archive:
        labels = archive[meta['key']].copy()
    assert labels.shape == (1<<meta['ring'],)
    return labels,label_entropy(labels)


@lru_cache(maxsize=None)
def relation_cached(a_text,b_text):
    a_meta,b_meta = json.loads(a_text),json.loads(b_text)
    assert a_meta['ring']==b_meta['ring']
    a,ha = load_partition(a_text)
    b,hb = load_partition(b_text)
    _,counts = np.unique(a.astype(np.uint64)*(int(b.max())+1)+b,return_counts=True)
    joint = entropy_counts(counts)
    raw = 2*joint-ha-hb
    n = a_meta['ring']
    assert -1e-11 <= raw <= n+1e-11
    return {'h_a':ha,'h_b':hb,'h_joint':joint,'vi':max(0.,min(float(n),raw)),
            'vi_per_bit':max(0.,min(1.,raw/n))}


def relation(a,b):
    return relation_cached(canonical(a),canonical(b))


def relation_change(a,b):
    return {'at_n':a['vi_per_bit'],'at_m':b['vi_per_bit'],
            'change':b['vi_per_bit']-a['vi_per_bit'],
            'absolute_change':abs(b['vi_per_bit']-a['vi_per_bit'])}


def comparison_label(new,baseline):
    difference = baseline-new
    return 'improvement' if difference>1e-12 else ('loss' if difference < -1e-12 else 'tie')


def confirm_stage(start,budget):
    seal = json.loads((UNIT/'prediction-seal.json').read_text())
    if sha256(UNIT/'predictions.json')!=seal['predictions_sha256']:
        raise ValueError('sealed predictions changed')
    fitted = json.loads((UNIT/'predictions.json').read_text())
    cases,case_info = [],[]
    for n in BANDS['C']:
        for rule in RULES:
            check_budget(start,budget)
            added,info = generate_case(n,rule)
            cases.extend(added);case_info.append(info)
            atomic_json(UNIT/'confirmation-progress.json',{'status':'running','completed_cases':case_info})
            print(f'completed n={n} rule={rule}; cases={len(case_info)}/32; {time.monotonic()-start:.1f}s',flush=True)
    atomic_json(UNIT/'cases.json',[asdict(c) for c in cases])
    registry = default_registry()
    registry.add('ring','balanced_basis',lambda n,m:dict(zip(FEATURE_NAMES,basis(n,m).tolist())))
    registry.add('relation','partition_vi',relation)
    registry.add('comparison','vi_change',relation_change)
    query = {'rules':[str(r) for r in RULES], 'max_comparisons':2000,
             'ring':[{'name':'balanced_basis'}], 'relation':[{'name':'partition_vi'}],
             'comparison':[{'name':'vi_change'}]}
    print('all fresh arrays complete; comparing partitions',flush=True)
    check_budget(start,budget)
    evidence = compare(cases,query,registry)
    atomic_json(UNIT/'evidence.json',evidence)
    by = {(row['observation'],*map(int,row['rules']),*row['rings']):row['scores']['absolute_change']
          for row in evidence['rows']}
    scores = []
    for task in fitted['tasks']:
        obs = task['observation'];a,b = task['rules']
        target = np.array([by[obs,a,b,n,m] for n,m in fitted['test_pairs']])
        row = {'observation':obs,'rules':[a,b],'targets':target.tolist(),'models':{}}
        for model in MODELS:
            saved = task['models'][model]
            predicted = np.array(saved['predictions'])
            errors = predicted-target
            row['models'][model] = {'mae':float(np.mean(abs(errors))),
                'rmse':float(np.sqrt(np.mean(errors*errors))),'errors':errors.tolist(),
                'predictions':predicted.tolist(),'clipping_count':saved['test_clipping_count']}
        row['M2_vs_M0'] = comparison_label(row['models']['M2']['mae'],row['models']['M0']['mae'])
        row['M2_vs_M1'] = comparison_label(row['models']['M2']['mae'],row['models']['M1']['mae'])
        row['strict_joint_improvement'] = row['M2_vs_M0']=='improvement' and row['M2_vs_M1']=='improvement'
        scores.append(row)
    summary = []
    for obs in OBSERVATIONS:
        panel = [row for row in scores if row['observation']==obs]
        summary.append({'observation':obs,'tasks':len(panel),
            'M2_vs_M0':dict(Counter(row['M2_vs_M0'] for row in panel)),
            'M2_vs_M1':dict(Counter(row['M2_vs_M1'] for row in panel)),
            'strict_joint_improvements':sum(row['strict_joint_improvement'] for row in panel)})
    # Recheck every immutable array after the relation cache has been used.
    for info in case_info:
        assert sha256(ROOT/info['path'])==info['sha256']
    check_budget(start,budget)
    result = {'status':'complete','rules':RULES,'widths':BANDS['C'],'case_info':case_info,
              'tasks':scores,'summary':summary,'predictions_sha256':seal['predictions_sha256'],
              'seal':seal,'evidence_sha256':sha256(UNIT/'evidence.json'),
              'source_state_cases':sum(info['states'] for info in case_info),
              'comparison_count':len(evidence['rows'])}
    atomic_json(UNIT/'confirmation-progress.json',{'status':'complete','completed_cases':case_info})
    return result


def check_budget(start,seconds):
    if time.monotonic()-start>seconds:
        raise TimeoutError('stage wall budget exhausted')
    if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>3*1024*1024:
        raise MemoryError('3-GiB resident memory budget exhausted')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage',choices=['fit','confirmation'])
    args = parser.parse_args()
    UNIT.mkdir(parents=True,exist_ok=True)
    if (UNIT/f'{args.stage}-result.json').exists():
        raise FileExistsError('refusing to overwrite completed stage')
    frozen = json.loads((UNIT/'implementation-freeze.json').read_text())
    current = {name:sha256(ROOT/name) for name in SOURCES}
    assert current == frozen['source_hashes'],'implementation/input drift after freeze'
    budget = 120 if args.stage=='fit' else 900
    def timeout(_signum,_frame):raise TimeoutError(f'{budget}-second stage alarm')
    signal.signal(signal.SIGALRM,timeout);signal.alarm(budget)
    resource.setrlimit(resource.RLIMIT_AS,(3*1024**3,3*1024**3))
    start = time.monotonic()
    execution = {'stage':args.stage,'status':'incomplete','numpy':np.__version__}
    try:
        result = fit_stage() if args.stage=='fit' else confirm_stage(start,budget)
        check_budget(start,budget)
        result['source_hashes'] = current
        atomic_json(UNIT/f'{args.stage}-result.json',result)
        execution['status']='complete'
        execution['result_sha256']=sha256(UNIT/f'{args.stage}-result.json')
    except Exception as error:
        execution['error']=f'{type(error).__name__}: {error}'
        raise
    finally:
        signal.alarm(0)
        execution['wall_seconds']=time.monotonic()-start
        execution['max_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        atomic_json(UNIT/f'{args.stage}-execution.json',execution)
        print(canonical(execution),flush=True)


if __name__=='__main__':main()
