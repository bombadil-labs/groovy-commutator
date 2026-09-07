#!/usr/bin/env python3
"""Exact task-return costs under hindsight and explicitly reactive policies."""
from __future__ import annotations
import csv
import itertools
import json
import platform
from collections import defaultdict
from pathlib import Path
import numpy as np
from experiment_revisable_primitives import ROOT, MACROS, fee, sha, plan_record

PREFIX=ROOT/'results/returning_tasks_20260907'
METHODS=['uncompiled','frozen','replacement_oracle','revision_oracle',
         'replacement_reactive_lex','revision_reactive_lex',
         'replacement_reactive_stay','revision_reactive_stay']
FEES={mode:np.array([[fee(w,u,mode=='revision') for u in MACROS] for w in MACROS])
      for mode in ['replacement','revision']}


def oracle(costs,fees,start,tasks,k):
    tail=np.zeros(16,dtype=int); choices=[]
    for target in reversed(tasks):
        values=fees + k*costs[:,target][None,:]+tail[None,:]
        choices.append(values.argmin(axis=1))
        tail=values.min(axis=1)
    current=start;path=[]
    for choice in reversed(choices):
        current=int(choice[current]);path.append(current)
    return int(tail[start]),path


def reactive(costs,fees,start,tasks,k,stay):
    current=start;total=0;path=[]
    for target in tasks:
        values=fees[current,:]+k*costs[:,target]
        choice=int(values.argmin())
        if stay and values[current]==values[choice]:choice=current
        total+=int(values[choice]);current=choice;path.append(current)
    return total,path


def calculate(kernel,w,v,k,cycles,checks):
    c=np.array(kernel['costs'],dtype=int);tasks=[v,w]*cycles
    prefix=8+8*c[w+1,w]
    totals={'uncompiled':int(8*c[0,w]+sum(k*c[0,t] for t in tasks)),
            'frozen':int(prefix+sum(k*c[w+1,t] for t in tasks))}
    paths={'uncompiled':[None]*len(tasks),'frozen':[w]*len(tasks)}
    for mode,fees in FEES.items():
        value,path=oracle(c[1:,:],fees,w,tasks,k)
        totals[mode+'_oracle']=int(prefix+value);paths[mode+'_oracle']=path
        if cycles==1 and k==4:
            direct=min(int(fees[w,u]+k*c[u+1,v]+fees[u,z]+k*c[z+1,w])
                       for u,z in itertools.product(range(16),repeat=2))
            assert direct==value
            checks['two_block_direct_paths']+=256
        for tie in ['lex','stay']:
            value,path=reactive(c[1:,:],fees,w,tasks,k,tie=='stay')
            totals[mode+'_reactive_'+tie]=int(prefix+value);paths[mode+'_reactive_'+tie]=path
    return totals,paths


def make_witness(kernel,w,v,k,cycles,trace,category,totals,paths):
    c=np.array(kernel['costs']);tasks=[v,w]*cycles
    record={'category':category,'A':kernel['A'],'B':kernel['B'],'dispatch':kernel['dispatch'],
            'trace':trace,'K':k,'cycles':cycles,'W':MACROS[w],'V':MACROS[v],
            'totals':totals,'old_raw_job_cost':int(c[0,w]),'old_macro_job_cost':int(c[w+1,w]),'blocks':{}}
    for method in METHODS:
        blocks=[];current=w
        for target,new in zip(tasks,paths[method]):
            if new is None:management=0
            elif method=='frozen':management=0
            else:management=fee(MACROS[current],MACROS[new],method.startswith('revision'))
            plan=plan_record(kernel,new,target)
            blocks.append({'management':management,'job_cost':plan['execution_cost'],
                           'block_cost':management+k*plan['execution_cost'],'plan':plan})
            if new is not None:current=new
        record['blocks'][method]=blocks
    return record


def replay_record(record):
    for method,blocks in record['blocks'].items():
        raw=method=='uncompiled';current=record['W']
        total=8*record['old_raw_job_cost'] if raw else 8+8*record['old_macro_job_cost']
        if method.startswith('revision'):total+=record['trace']
        for block in blocks:
            macro=block['plan']['macro']
            if raw or method=='frozen' or macro==current:management=0
            else:
                changes=sum(x!=y for x,y in zip(current,macro))
                management=min(8,1+2*changes) if method.startswith('revision') else 8
            assert management==block['management']
            p=block['plan'];expanded=''.join(p['macro'] if t=='@' else t for t in p['tokens'])
            assert expanded==p['expanded_word']
            execution=len(expanded)+record['dispatch']*len(p['tokens'])
            assert execution==block['job_cost']
            assert management+record['K']*execution==block['block_cost']
            total+=block['block_cost']
            if macro is not None:current=macro
        assert total==record['totals'][method]


def main():
    protocol_path=ROOT/'docs/research/protocols/returning-tasks-20260907.json'
    p=json.loads(protocol_path.read_text());source=ROOT/p['kernel_source']
    kernels=json.loads(source.read_text())['records']
    checks={'two_block_direct_paths':0,'policy_configurations':0};aggregate={};witnesses={}
    for kernel in kernels:
        a,b,d=(kernel[x] for x in ['A','B','dispatch'])
        assert kernel['domain']=='local-rule' and kernel['window_bits']==17
        for k in p['jobs_per_block']:
            for cycles in p['cycles']:
                for w,old in enumerate(MACROS):
                    useful=8+8*kernel['costs'][w+1][w]<8*kernel['costs'][0][w]
                    for v,new in enumerate(MACROS):
                        shift=['unchanged','one_edit','far'][min(2,sum(x!=y for x,y in zip(old,new)))]
                        uncharged,paths=calculate(kernel,w,v,k,cycles,checks)
                        for trace in p['trace_reserves']:
                            totals={name:value+(trace if name.startswith('revision') else 0) for name,value in uncharged.items()}
                            key=(a,b,d,trace,k,cycles,shift,int(useful))
                            if key not in aggregate:
                                row=dict(zip(['A','B','dispatch','trace','K','cycles','shift','useful_inheritance'],key));row['cases']=0
                                for method in METHODS:row['sum_'+method]=0
                                for policy in ['oracle','reactive_lex','reactive_stay']:
                                    for base in ['uncompiled','frozen','replacement']:
                                        for relation in ['win','tie','loss']:row[f'revision_{policy}_{relation}_{base}']=0
                                for mode in ['replacement','revision']:
                                    for tie in ['lex','stay']:
                                        row[f'{mode}_{tie}_regret_cases']=0;row[f'{mode}_{tie}_regret_sum']=0;row[f'{mode}_{tie}_regret_max']=0
                                    row[mode+'_tie_changes_cost']=0
                                aggregate[key]=row
                            row=aggregate[key];row['cases']+=1;checks['policy_configurations']+=1
                            for method,value in totals.items():row['sum_'+method]+=value
                            assert totals['replacement_oracle']<=totals['frozen']
                            assert totals['replacement_oracle']-totals['revision_oracle']<=10*cycles-trace
                            if trace==0:assert totals['revision_oracle']<=totals['replacement_oracle']
                            if d==0:
                                assert totals['frozen']==totals['uncompiled']+8
                                assert totals['revision_oracle']==totals['frozen']+trace
                            for policy in ['oracle','reactive_lex','reactive_stay']:
                                for base in ['uncompiled','frozen','replacement']:
                                    other=base+'_'+policy if base=='replacement' else base
                                    gain=totals[other]-totals['revision_'+policy]
                                    relation='win' if gain>0 else 'loss' if gain<0 else 'tie'
                                    row[f'revision_{policy}_{relation}_{base}']+=1
                            for mode in ['replacement','revision']:
                                for tie in ['lex','stay']:
                                    regret=totals[mode+'_reactive_'+tie]-totals[mode+'_oracle'];assert regret>=0
                                    row[f'{mode}_{tie}_regret_cases']+=int(regret>0)
                                    row[f'{mode}_{tie}_regret_sum']+=regret
                                    row[f'{mode}_{tie}_regret_max']=max(row[f'{mode}_{tie}_regret_max'],regret)
                                row[mode+'_tie_changes_cost']+=int(totals[mode+'_reactive_lex']!=totals[mode+'_reactive_stay'])
                            if useful:
                                tests={'reactive_revision_regret':totals['revision_reactive_stay']>totals['revision_oracle'],
                                       'reactive_revision_worse_frozen':totals['revision_reactive_stay']>totals['frozen'],
                                       'tie_changes_cost':any(totals[m+'_reactive_lex']!=totals[m+'_reactive_stay'] for m in ['replacement','revision']),
                                       'repeat_revision_gain':(d,trace,k,cycles)==(1,4,4,4) and totals['replacement_oracle']-totals['revision_oracle']>1}
                                rank=(a,b,d,trace,k,cycles,old,new)
                                for category,selected in tests.items():
                                    if selected and (category not in witnesses or rank<witnesses[category][0]):
                                        witnesses[category]=(rank,make_witness(kernel,w,v,k,cycles,trace,category,totals,paths))
        print(f'Return sequences complete for {a}/{b}, dispatch={d}',flush=True)
    records=[value[1] for value in witnesses.values()]
    for r in records:replay_record(r)
    checks.update(witnesses_replayed=len(records),all_passed=True)
    rows=list(aggregate.values())
    with PREFIX.with_suffix('.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    Path(str(PREFIX)+'_witnesses.json').write_text(json.dumps(records,indent=2)+'\n')
    meta={'protocol':p,'protocol_sha256':sha(protocol_path),'script_sha256':sha(__file__),'kernel_sha256':sha(source),
          'parent_script_sha256':sha(ROOT/'scripts/experiment_revisable_primitives.py'),'python':platform.python_version(),
          'numpy':np.__version__,'aggregate_rows':len(rows),'checks':checks}
    Path(str(PREFIX)+'_metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
    print(json.dumps({'rows':len(rows),'checks':checks},indent=2))

if __name__=='__main__':main()
