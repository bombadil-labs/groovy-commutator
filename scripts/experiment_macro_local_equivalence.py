#!/usr/bin/env python3
"""Audit macro equivalence on every causal window, then repeat cost accounting."""
from __future__ import annotations
import csv
import itertools
import json
import platform
from collections import defaultdict
from pathlib import Path
import numpy as np
from experiment_revisable_primitives import (
    ROOT, MACROS, WORDS, encode, comparison_totals, plan_record, sha, vector_map,
)
from groovy.ca import rule_lut

PREFIX = ROOT / 'results/macro_local_equivalence_20260907'
PATTERNS = np.arange(1 << 17, dtype=np.uint32)


def local_tables(a, b, checks):
    tables = {'': np.array([0, 1], dtype=np.uint8)}
    packed = {}
    for word in WORDS:
        h = len(word)
        if h:
            p = np.arange(1 << (2*h+1), dtype=np.uint32)
            previous = tables[word[:-1]]
            mask = (1 << (2*h-1)) - 1
            tables[word] = rule_lut(a if word[-1] == 'A' else b)[
                4 * previous[p & mask] + 2 * previous[(p >> 1) & mask]
                + previous[(p >> 2) & mask]]
        if h <= 3:
            expected = (vector_map(2*h+1,a,b,word) >> h) & 1
            assert np.array_equal(tables[word],expected)
            checks['minimal_window_outputs'] += len(expected)
        expanded = tables[word][(PATTERNS >> (8-h)) & ((1 << (2*h+1))-1)]
        packed[word] = np.packbits(expanded,bitorder='little').tobytes()
    return packed


def direct_window(a, b, word):
    # Independent space-time evolution with shrinking boundaries; no periodic wrap.
    cells = ((PATTERNS[:,None] >> np.arange(17)) & 1).astype(np.uint8)
    for letter in word:
        cells = rule_lut(a if letter == 'A' else b)[
            4*cells[:,:-2] + 2*cells[:,1:-1] + cells[:,2:]]
    return cells[:,cells.shape[1]//2]


def local_kernels(a, b, packed, dispatches):
    groups = defaultdict(list)
    for i, word in enumerate(WORDS): groups[packed[word]].append(i)
    targets = [packed[v*2] for v in MACROS]
    classes = [targets.index(t) for t in targets]
    lengths = np.array([len(w) for w in WORDS])
    issued = np.array([[encode(w,macro)[0] for w in WORDS] for macro in [None]+MACROS])
    out=[]
    for d in dispatches:
        prices = lengths[None,:] + d*issued
        costs=np.zeros((17,16),dtype=int); realizations=np.zeros_like(costs)
        for v,target in enumerate(targets):
            candidates=np.array(groups[target])
            best=candidates[np.argmin(prices[:,candidates],axis=1)]
            costs[:,v]=prices[np.arange(17),best];realizations[:,v]=best
        out.append({'n':'all-widths','domain':'local-rule','window_bits':17,'A':a,'B':b,'dispatch':d,
                    'target_classes':classes,'costs':costs.tolist(),'realizations':realizations.tolist()})
    return out


def main():
    protocol_path=ROOT/'docs/research/protocols/macro-local-equivalence-20260907.json'
    parent_path=ROOT/'docs/research/protocols/revisable-primitives-20260907.json'
    protocol=json.loads(protocol_path.read_text());parent=json.loads(parent_path.read_text())
    assert protocol['rule_pairs']==parent['rule_pairs'] and protocol['causal_window_bits']==17
    parent_kernels=json.loads((ROOT/'results/revisable_primitives_20260907_kernels.json').read_text())['records']
    old_witnesses=json.loads((ROOT/'results/revisable_primitives_20260907_witnesses.json').read_text())
    checks={'minimal_window_outputs':0,'direct_witness_outputs':0,'finite_cost_entries':0}
    kernels=[]; audit=[]; widths=[]
    for a,b in protocol['rule_pairs']:
        packed=local_tables(a,b,checks)
        current=local_kernels(a,b,packed,parent['dispatch_costs']);kernels.extend(current)
        seen=set()
        for witness in old_witnesses:
            if (witness['A'],witness['B'])!=(a,b):continue
            for plan in [witness['old_plan']]+list(witness['new_plans'].values()):
                pair=(plan['expanded_word'],plan['target_word'])
                if pair in seen:continue
                seen.add(pair)
                x,y=(direct_window(a,b,w) for w in pair)
                assert np.packbits(x,bitorder='little').tobytes()==packed[pair[0]]
                assert np.packbits(y,bitorder='little').tobytes()==packed[pair[1]]
                checks['direct_witness_outputs']+=2*len(x)
                unequal=np.flatnonzero(x!=y)
                audit.append({'A':a,'B':b,'program':pair[0],'target':pair[1],
                              'equal_all_widths':not len(unequal),
                              'counterexample_window':int(unequal[0]) if len(unequal) else None,
                              'different_windows':len(unequal)})
        for local in current:
            for finite in parent_kernels:
                if (finite['A'],finite['B'],finite['dispatch'])!=(a,b,local['dispatch']):continue
                lc,fc=np.array(local['costs']),np.array(finite['costs'])
                assert np.all(fc<=lc)
                checks['finite_cost_entries']+=lc.size
                finite_classes=finite['target_classes'];local_classes=local['target_classes']
                accidental=0
                for i,j in itertools.combinations(range(16),2):
                    if local_classes[i]==local_classes[j]:assert finite_classes[i]==finite_classes[j]
                    accidental+=int(finite_classes[i]==finite_classes[j] and local_classes[i]!=local_classes[j])
                widths.append({'n':finite['n'],'A':a,'B':b,'dispatch':local['dispatch'],
                               'cost_entries':int(lc.size),'finite_cost_lower':int((fc<lc).sum()),
                               'finite_only_target_equalities':accidental,
                               'local_target_classes':len(set(local_classes)),
                               'finite_target_classes':len(set(finite_classes))})
        print(f'Local tables complete for {a}/{b}',flush=True)
    aggregates={};witnesses={};cases=0
    for kernel in kernels:
        a,b,d=(kernel[k] for k in ('A','B','dispatch'))
        for trace in parent['trace_reserves']:
            for k in parent['postchange_jobs']:
                for w,old in enumerate(MACROS):
                    useful=8+8*kernel['costs'][w+1][w] < 8*kernel['costs'][0][w]
                    for v,new in enumerate(MACROS):
                        shift=['unchanged','one_edit','far'][min(2,sum(x!=y for x,y in zip(old,new)))]
                        key=(a,b,d,trace,k,shift,int(useful))
                        if key not in aggregates:
                            row=dict(zip(('A','B','dispatch','trace','K','shift','useful_inheritance'),key))
                            row.update(cases=0,same_task_map=0)
                            for arm in ('uncompiled','frozen','replace','revisable'):row['sum_'+arm]=0
                            for base in ('uncompiled','frozen','replace'):
                                for relation in ('win','tie','loss'):row[f'revision_{relation}_{base}']=0
                            aggregates[key]=row
                        row=aggregates[key];values,chosen=comparison_totals(kernel,w,v,k,trace)
                        # A one-step patch saves at most five management units; retention pays no fee.
                        assert values['replace']-values['revisable'] <= 5-trace
                        row['cases']+=1;cases+=1
                        row['same_task_map']+=int(kernel['target_classes'][w]==kernel['target_classes'][v])
                        for arm,value in values.items():row['sum_'+arm]+=value
                        for base in ('uncompiled','frozen','replace'):
                            gain=values[base]-values['revisable'];relation='win' if gain>0 else 'loss' if gain<0 else 'tie'
                            row[f'revision_{relation}_{base}']+=1
                        if useful and (d,trace,k)==(1,4,4):
                            categories={'revision_beats_all':all(values['revisable']<values[base] for base in ('uncompiled','frozen','replace')),
                                        'revision_loses_replacement':values['revisable']>values['replace']}
                            for category,selected in categories.items():
                                if selected and category not in witnesses:
                                    plans={arm:plan_record(kernel,chosen[arm],v) for arm in chosen}
                                    witnesses[category]={'category':category,'A':a,'B':b,'W':old,'V':new,'dispatch':d,'trace':trace,'K':k,'totals':values,'plans':plans}
    for witness in witnesses.values():
        for plan in witness['plans'].values():
            x=direct_window(witness['A'],witness['B'],plan['expanded_word'])
            y=direct_window(witness['A'],witness['B'],plan['target_word'])
            assert np.array_equal(x,y)
            checks['direct_witness_outputs']+=2*len(x)
    rows=list(aggregates.values())
    for suffix,records in [('.csv',rows),('_finite_comparison.csv',widths)]:
        with Path(str(PREFIX)+suffix).open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
    Path(str(PREFIX)+'_kernels.json').write_text(json.dumps({'macros':MACROS,'primitive_words':WORDS,'records':kernels},separators=(',',':'))+'\n')
    Path(str(PREFIX)+'_audit.json').write_text(json.dumps({'parent_programs':audit,'local_witnesses':list(witnesses.values())},indent=2)+'\n')
    checks.update(policy_cases=cases,all_passed=True)
    metadata={'protocol':protocol,'protocol_sha256':sha(protocol_path),'parent_protocol_sha256':sha(parent_path),
              'script_sha256':sha(__file__),'parent_script_sha256':sha(ROOT/'scripts/experiment_revisable_primitives.py'),
              'parent_kernels_sha256':sha(ROOT/'results/revisable_primitives_20260907_kernels.json'),
              'ca_engine_sha256':sha(ROOT/'src/groovy/ca.py'),'python':platform.python_version(),'numpy':np.__version__,
              'aggregate_rows':len(rows),'checks':checks}
    Path(str(PREFIX)+'_metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    print(json.dumps({'rows':len(rows),'checks':checks,'parent_audit':audit},indent=2))

if __name__=='__main__':main()
